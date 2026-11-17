#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scripts/extract_assist.py — 数据提取助手（LLM 草稿 + 人工核验闸）

定位（对齐 review_workflow.md §3 与 §0.2）：
  - 引擎/coze 不存提取表；本脚本只负责「结构化 + 校验 + 护栏」，不做任何数值计算。
  - 真正的抽取由 agent/LLM 在对话中读全文（OA 或用户上传 PDF→md）后提出草稿行；
    本脚本把这些草稿固化成可直接喂 run_meta.py 的 Type 1/2/3 CSV，并强制人工核验。

三种子命令：
  scaffold  生成空白抽取表（仅含 Type 列，可直接喂 run_meta --data），并写一份
            <csv>.provenance.json 同伴文件，verified_by_human=NO。
            --studies-file 可接收 Stage3 人工确认的最终纳入清单（json/txt/csv），
            自动预填 study 列（与 --studies 合并去重），来源记入 provenance 溯源。
  validate  校验已填 CSV：列名/数值合理性/NR 缺失标记；并检查同伴 provenance 的
            verified_by_human 标记（未核验 → 警告，不强行阻断，由 run_meta 守卫拦截）。
  stamp     在人工确认后把 provenance 的 verified_by_human 置 YES（必须带 --confirm）。

关键约定：
  - 抽取 CSV 只含 Type 数据列（与 data_templates.md 一一对应），不含溯源列，
    以便 run_meta.py --data 直接消费，不干扰 build_request 的列检测。
  - 溯源信息（来源文件 / 页码表号）存在同伴 .provenance.json 的 per-study 列表里，
    不污染数据列。
  - 任何无法从原文定位的数值 → 填 "NR"（not reported），绝不可臆造。

纯 stdlib，无第三方依赖（对齐 scripts/ 约定）。
"""
import argparse
import csv
import json
import os
import re
import sys

# ---------------------------------------------------------------------------
# Type schema（与 references/data_templates.md 严格对应）
# kind: str | int | float | opt(int/float 可选)
# ---------------------------------------------------------------------------
SCHEMA = {
    "binary": {
        "cols": [
            ("study", "str"), ("n_exp", "int"), ("event_exp", "int"),
            ("n_ctrl", "int"), ("event_ctrl", "int"), ("year", "opt"), ("arm", "opt"),
        ],
        "measure_hint": "OR / RR / RD",
    },
    "continuous": {
        "cols": [
            ("study", "str"), ("n_exp", "int"), ("mean_exp", "float"), ("sd_exp", "float"),
            ("n_ctrl", "int"), ("mean_ctrl", "float"), ("sd_ctrl", "float"), ("year", "opt"),
        ],
        "measure_hint": "MD / SMD",
    },
    "precomputed": {
        "cols": [
            ("study", "str"), ("effect_type", "str"), ("effect_size", "float"),
            ("lower95", "float"), ("upper95", "float"), ("year", "opt"),
        ],
        "measure_hint": "lnOR / SMD / ROM / ZCOR / logHR（已取对数）",
    },
    "rate": {
        "cols": [
            ("study", "str"), ("a", "int"), ("b", "float"),
            ("c", "int"), ("d", "float"), ("year", "opt"),
        ],
        "measure_hint": "IRR（a/c=事件数, b/d=人时）",
    },
    "correlation": {
        "cols": [("study", "str"), ("r", "float"), ("n", "int"), ("year", "opt")],
        "measure_hint": "Pearson r",
    },
    "single_proportion": {
        "cols": [("study", "str"), ("events", "int"), ("n", "int"), ("year", "opt")],
        # 2026-09-01 统一：coze 主路径 single_group_meta 走 meta::metaprop(sm="PLOGIT")，
        # 故提示对齐为 PLOGIT / PRAW / PASF（与 references/single_group_meta.md 一致）。
        # 本地 core（meta_analysis_core.R single_proportion）用 metafor::escalc(measure="PLO")，
        # PLO 即 meta 包的 PLOGIT，同为 logit 变换、功能等价，仅所属 R 包不同。
        "measure_hint": "PLOGIT / PRAW / PASF",
    },
    "single_mean": {
        "cols": [("study", "str"), ("mean", "float"), ("sd", "float"), ("n", "int"), ("year", "opt")],
        "measure_hint": "MN",
    },
}

NR_VALUES = {"", "nr", "na", "nan", "none", "n/a", "not reported", "未报道", "未报告"}


def _is_nr(v):
    return str(v).strip().lower() in NR_VALUES


def _to_num(v):
    """返回 (ok, value). NR / 空 → (False, None) 表示缺失而非错误。"""
    s = str(v).strip()
    if _is_nr(s):
        return False, None
    try:
        return True, float(s)
    except ValueError:
        return None, None  # 非数字且非 NR → 真错误


def provenance_path(csv_path):
    return csv_path + ".provenance.json"


def load_provenance(csv_path):
    p = provenance_path(csv_path)
    if not os.path.exists(p):
        return None
    with open(p, encoding="utf-8") as f:
        return json.load(f)


def write_provenance(csv_path, data):
    with open(provenance_path(csv_path), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def read_studies_file(path):
    """从「最终纳入清单」文件读取研究名列表（供 scaffold --studies-file 自动预填）。

    支持：
      - .json：顶层数组 of str，或 {"included":[...]} / {"studies":[...]} / {"study_list":[...]}
      - .txt ：每行一个（跳过空行与 # 注释）
      - .csv ：取 'study' 列或第一列（首行若是表头则跳过）
    返回去空、去重、保序的研究名列表。
    """
    if not os.path.exists(path):
        print("[ERROR] 找不到纳入清单文件 %s" % path)
        sys.exit(2)
    ext = os.path.splitext(path)[1].lower()
    names = []
    if ext == ".json":
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, list):
            names = [str(x).strip() for x in data]
        elif isinstance(data, dict):
            for key in ("included", "studies", "study_list"):
                if key in data and isinstance(data[key], list):
                    names = [str(x).strip() for x in data[key]]
                    break
            if not names:
                print("[ERROR] JSON 清单未找到 included/studies/study_list 键：%s" % list(data.keys()))
                sys.exit(2)
        else:
            print("[ERROR] JSON 清单格式不支持（需为数组或含 included/studies 的对象）")
            sys.exit(2)
    else:
        with open(path, encoding="utf-8") as f:
            lines = [ln.strip() for ln in f if ln.strip() and not ln.strip().startswith("#")]
        if ext == ".csv":
            rows = list(csv.reader(lines))
            header = [c.lower() for c in rows[0]] if rows else []
            if header and "study" in header:
                idx = header.index("study")
                names = [r[idx] for r in rows[1:] if r and r[idx].strip()]
            else:
                names = [r[0] for r in rows if r and r[0].strip()]
        else:
            names = lines
    seen, out = set(), []
    for n in names:
        n = n.strip()
        if n and n not in seen:
            seen.add(n)
            out.append(n)
    return out


# ---------------------------------------------------------------------------
# subcommand: scaffold
# ---------------------------------------------------------------------------
# 协变量列默认类型映射：数值型协变量（latitude/age/mean_followup 等）→ float 校验；
# 分类协变量（allocation/vaccine_type/strain/region 等）→ 字符串透传，仅查非空。
# 用户可通过 --covariates-json 精细指定类型，未指定则按此表 + 启发式。
NUMERIC_COVARIATE_HINTS = {
    "latitude", "lat", "longitude", "lon", "age", "age_mean", "mean_age",
    "followup", "followup_years", "followup_months", "mean_followup",
    "dose", "bacillus_count", "cfu", "bacille", "year",
}
# 明确的分类型协变量（不在数值表且常见为字符串者，可放宽启发式命中）
CATEGORICAL_COVARIATE_HINTS = {
    "allocation", "allocation_method", "alloc_method", "randomization",
    "vaccine", "vaccine_type", "strain", "bcg_strain", "manufacturer",
    "region", "country", "continent", "route", "age_group", "population",
}


def _covariate_kind(col, numeric_override=None):
    """决定协变量列的校验类型：'int'|'float'|'str'。
    优先级：--covariates-json 显式 > NUMERIC_COVARIATE_HINTS 数值提示 > CATEGORICAL 字符串提示
    > 启发式（列名含 age/lat/follow/dose 数字语义 → float，否则 str）。
    """
    if numeric_override and col in numeric_override:
        return "float"
    base = col.lower().replace("_", "")
    if col in NUMERIC_COVARIATE_HINTS or base in {x.replace("_", "") for x in NUMERIC_COVARIATE_HINTS}:
        return "float"
    if col in CATEGORICAL_COVARIATE_HINTS:
        return "str"
    # 启发式：含常见数值语义子串 → float
    if any(tok in base for tok in ("lat", "lon", "age", "follow", "dose", "year", "count", "num")):
        return "float"
    return "str"


def cmd_scaffold(args):
    if args.type not in SCHEMA:
        print("[ERROR] 未知 type=%s；支持: %s" % (args.type, ", ".join(SCHEMA)))
        sys.exit(2)
    # 协变量列：--covariates 逗号分隔（如 "latitude,allocation,vaccine_type"）动态追加。
    # 这是 P0 修复（BCG 案例打脸）：原 binary 模板只有主结局列，纬度/分配方法等在提取
    # 阶段即被丢弃，亚组/元回归做不了。现在协变量与主列同表固化，provenance 记录。
    cov_cols = [c.strip() for c in (args.covariates or "").split(",") if c.strip()]
    cov_types = {}
    if args.covariates_json:
        cov_types = json.loads(args.covariates_json) if isinstance(args.covariates_json, str) else args.covariates_json
    cols = [c for c, _ in SCHEMA[args.type]["cols"]]
    cols += cov_cols  # 追加协变量列（位于 year 之后，保持主列位置不变）
    # 纳入清单自动预填：--studies-file（最终纳入清单文件）与 --studies（逗号串）合并去重
    file_studies = read_studies_file(args.studies_file) if args.studies_file else []
    comma_studies = [s.strip() for s in (args.studies or "").split(",") if s.strip()]
    seen, studies = set(), []
    for s in file_studies + comma_studies:
        if s and s not in seen:
            seen.add(s)
            studies.append(s)
    rows = [{"study": s} for s in studies] if studies else []

    out = args.out
    with open(out, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        for r in rows:
            w.writerow({c: r.get(c, "") for c in cols})

    prov = {
        "schema_type": args.type,
        "measure_hint": SCHEMA[args.type]["measure_hint"],
        "verified_by_human": False,
        "generated_by": "extract_assist.py scaffold",
        "included_list_source": args.studies_file or "",  # 最终纳入清单来源（自动预填溯源）
        "covariates": {c: _covariate_kind(c, cov_types) for c in cov_cols},  # 协变量列 + 校验类型
        "source_manifest": [],   # agent 填写：[{study, source_file, source_loc}]
        "note": "抽取草稿表。数值须能追溯到原文页码/表号；无法定位填 NR。人工核验后运行 stamp --confirm。",
    }
    write_provenance(out, prov)
    print("[OK] 空白抽取表 -> %s" % out)
    print("[OK] 溯源同伴文件 -> %s" % provenance_path(out))
    print("     类型=%s | 必填列=%s" % (args.type, ", ".join(cols)))
    if cov_cols:
        print("     协变量列=%s（%s）" % (", ".join(cov_cols),
              ", ".join("%s:%s" % (c, _covariate_kind(c, cov_types)) for c in cov_cols)))
    if args.studies_file:
        print("     纳入清单来源=%s（自动预填 %d 个研究）" % (args.studies_file, len(file_studies)))
    print("     verified_by_human=NO —— 未经人工核验，run_meta 守卫会拦截。")


# ---------------------------------------------------------------------------
# subcommand: validate
# ---------------------------------------------------------------------------
def cmd_validate(args):
    csv_path = args.csv
    if not os.path.exists(csv_path):
        print("[ERROR] 找不到 %s" % csv_path)
        sys.exit(2)

    with open(csv_path, encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        header = reader.fieldnames or []
        rows = list(reader)

    # 推断 type：匹配【必填】列集合（仅非 opt 列）。
    # 选填列（year/arm 等）存在与否不影响推断——对齐 data_templates.md（year/arm 标「选填」）。
    # 旧逻辑误将 opt 列当必填做 issubset 判定，导致用户按文档必填列填表（不含 arm）时被判
    # 「无法推断 Type」。例如 binary 必填={study,n_exp,event_exp,n_ctrl,event_ctrl}，
    # 用户填这 5 列 + study 即应匹配，year/arm 可选。
    stype = None
    for t, spec in SCHEMA.items():
        req = {c for c, k in spec["cols"] if k != "opt"}
        if req.issubset(set(header)) and "study" in header:
            stype = t
            break
    if stype is None:
        print("[ERROR] 无法从列名推断 Type（%s）。请与 data_templates.md 对齐。"
              " 必填列示例见 data_templates.md（选填列 year/arm 可省略）。" % ", ".join(header))
        sys.exit(2)

    spec = SCHEMA[stype]
    errors = []
    warnings = []
    nr_studies = []
    zero_event_cells = []   # P0-3：零事件单元记录
    double_zero_rows = []   # P0-3：双零单元行（RR 完全无信息，须阻断/剔除）

    # 协变量列信息：优先取 provenance.covariates（scaffold 写入），
    # 否则从表头中「非 schema 主列」的列推断（存量表兼容）。
    prov = load_provenance(csv_path)
    prov_cov = (prov or {}).get("covariates") or {}
    schema_cols = {c for c, _ in spec["cols"]}
    header_set = set(header)
    extra_cols = [c for c in header if c not in schema_cols and c != "study"]
    cov_meta = {}  # col -> kind
    for c in extra_cols:
        if isinstance(prov_cov, dict) and c in prov_cov:
            cov_meta[c] = prov_cov[c]      # scaffold 记录的类型优先
        else:
            cov_meta[c] = _covariate_kind(c)  # 存量表/无记录 → 启发式推断

    for i, row in enumerate(rows, start=2):  # 行号从 2 起（含表头）
        study = row.get("study", "").strip() or "<row %d>" % i
        for col, kind in spec["cols"]:
            if col == "study":
                if not row.get("study", "").strip():
                    errors.append("行%d: study 为空" % i)
                continue
            if kind == "opt":
                continue
            if kind == "str":
                # 字符串列（如 precomputed 的 effect_type）透传，不做数值校验；
                # 旧逻辑对它调 _to_num 会误报「非数值且非 NR」，导致 precomputed 轨无法通过校验。
                continue
            raw = row.get(col, "")
            ok, val = _to_num(raw)
            if ok is None:
                errors.append("行%d [%s] %s=%r 非数值且非 NR" % (i, study, col, raw))
            elif ok is False:
                # 缺失（NR/空）
                nr_studies.append((study, col))
                if col in ("n_exp", "event_exp", "n_ctrl", "event_ctrl") and _is_nr(raw):
                    warnings.append("行%d [%s] %s=NR（缺失将被剔除或敏感性分析处理）" % (i, study, col))
            else:
                # 数值合理性
                if kind == "int" and abs(val - round(val)) > 1e-9:
                    errors.append("行%d [%s] %s=%s 应为整数" % (i, study, col, raw))
                if col in ("n_exp", "n_ctrl") and val <= 0:
                    errors.append("行%d [%s] %s=%s 必须 >0" % (i, study, col, raw))
                if col in ("event_exp", "event_ctrl") and (val < 0 or val > (row.get("n_" + col.split("_")[1] + "_", 1e9) if False else 1e9)):
                    # 占位：下方单独做 event<=n 检查
                    pass
        # event <= n 检查（仅 binary）
        if stype == "binary":
            for exp in (("event_exp", "n_exp"), ("event_ctrl", "n_ctrl")):
                ec, nc = row.get(exp[0], ""), row.get(exp[1], "")
                ok_e, ve = _to_num(ec)
                ok_n, vn = _to_num(nc)
                if ok_e and ok_n and ve > vn:
                    errors.append("行%d [%s] %s=%s > %s=%s" % (i, study, exp[0], ve, exp[1], vn))
                # P0-3 零事件单元：event=0 记录（供 RR/OR 连续性校正判定）
                if ok_e and ve == 0:
                    zero_event_cells.append((i, study, exp[0]))
            # 双零单元检测：event_exp=0 且 event_ctrl=0 → RR/OR 完全无信息，
            # metafor::escalc 会抛 "invalid 'pos' value"，必须剔除或用 RD/OR 替代。
            ok_ee, v_ee = _to_num(row.get("event_exp", ""))
            ok_ec, v_ec = _to_num(row.get("event_ctrl", ""))
            if ok_ee and ok_ec and v_ee == 0 and v_ec == 0:
                double_zero_rows.append((i, study))
        # P0-3 协变量列校验：数值型做类型/范围检查，分类型仅查非 NR 空值
        for c, kind in cov_meta.items():
            raw = row.get(c, "")
            if _is_nr(raw):
                continue  # NR 协变量：不阻断，标注缺失（可被 metareg 剔除）
            if kind == "str":
                continue  # 分类协变量字符串透传
            ok_c, vc = _to_num(raw)
            if ok_c is None:
                errors.append("行%d [%s] 协变量 %s=%r 非数值（需 %s）" % (i, study, c, raw, kind))
            elif kind == "int" and ok_c and abs(vc - round(vc)) > 1e-9:
                errors.append("行%d [%s] 协变量 %s=%s 应为整数" % (i, study, c, raw))
        # CI 方向检查（precomputed）
        if stype == "precomputed":
            ok_l, vl = _to_num(row.get("lower95", ""))
            ok_u, vu = _to_num(row.get("upper95", ""))
            if ok_l and ok_u and vl > vu:
                errors.append("行%d [%s] lower95(%s) > upper95(%s)" % (i, study, vl, vu))
        # r 范围
        if stype == "correlation":
            ok_r, vr = _to_num(row.get("r", ""))
            if ok_r and not (-1.0 - 1e-9 <= vr <= 1.0 + 1e-9):
                errors.append("行%d [%s] r=%s 超出 [-1,1]" % (i, study, vr))

    # P0-2 多臂/多对照独立性检测：同一 study 出现多行 → 每行是同一试验的一个臂/对照比较，
    # 直接全部纳入会破坏独立性假设（同一试验样本被重复使用，SE 低估、I² 失真）。
    # 不强行阻断（多臂 metareg/稳健方差估计是合法分析），但必须显式提示。
    if stype in ("binary", "continuous"):
        study_counts = {}
        for row in rows:
            s = (row.get("study") or "").strip()
            if s:
                study_counts[s] = study_counts.get(s, 0) + 1
        multi = {s: n for s, n in study_counts.items() if n > 1}
        if multi:
            arms_note = (" 检测到同一研究多行（多臂/多对照）：%s。"
                         " 多行=同一试验的多个臂/对照比较，直接全纳会破坏独立性假设、低估 SE。"
                         " 请确认每行 arm 列已正确标识臂，并考虑多臂稳健方差估计（RVE）或按臂拆分为独立比较。"
                         % "; ".join("%s×%d" % kv for kv in list(multi.items())[:8]))
            warnings.append(arms_note)

    # P0-3 零事件单元（仅 binary 有 2×2 结构）：
    #   - 单零（exp 或 ctrl 一方为 0）→ 告警：RR/OR 无定义，引擎自动连续性校正（+0.5）可算；
    #   - 双零（两者皆 0）→ 硬错误：该研究 RR/OR 完全无信息，metafor::escalc 抛
    #     "invalid 'pos' value"，须剔除该研究或改用 risk difference（RD）。
    if stype == "binary" and zero_event_cells:
        cell_keys = sorted({c for _, _, c in zero_event_cells})
        if double_zero_rows:
            dz = "; ".join("行%d [%s]" % (i, s) for i, s in double_zero_rows)
            errors.append(
                "检测到 %d 个双零事件单元研究（%s）：两组事件均为 0，RR/OR 完全无信息，"
                "RR 合并会触发引擎 'invalid pos' 错误。请剔除这些研究，或改用 risk difference（--measure RD）。"
                % (len(double_zero_rows), dz)
            )
        warnings.append(
            "检测到 %d 个零事件单元（%s），RR/OR 在这些单元无定义；"
            "引擎将自动做连续性校正（+0.5），如需 risk difference 请用 --measure RD 重跑。"
            % (len(zero_event_cells), ", ".join(sorted(set(cell_keys))))
        )
        for i, study, c in zero_event_cells[:8]:
            print("  [ZERO] 行%d [%s] %s=0" % (i, study, c))

    # 同伴 provenance 校验
    prov = load_provenance(csv_path)
    verified = bool(prov.get("verified_by_human")) if prov else False
    if prov is None:
        warnings.append("无同伴 .provenance.json：run_meta 会按「人工可信 CSV」放行（不拦截）。"
                        " 若本表由 extract_assist 生成，请先 stamp --confirm。")
    elif not verified:
        warnings.append("verified_by_human=NO：run_meta 守卫将拦截（返回 META_STATUS=unverified_extraction）。"
                        " 人工核验后运行 stamp --confirm。")

    # 报告
    print("=== 抽取表校验 / extraction validation ===")
    print("file: %s" % csv_path)
    print("inferred type: %s" % stype)
    print("rows: %d | NR/缺失单元格: %d" % (len(rows), len(nr_studies)))
    if nr_studies:
        print("  NR 明细(前10): " + "; ".join("%s.%s" % x for x in nr_studies[:10]))
    if cov_meta:
        print("协变量列: " + ", ".join("%s(%s)" % (c, k) for c, k in cov_meta.items()))
    print("verified_by_human: %s" % verified)
    print("-" * 60)
    for w in warnings:
        print("[WARN] " + w)
    for e in errors:
        print("[ERROR] " + e)
    print("-" * 60)
    if errors:
        print("[RESULT] 校验不通过：%d 个硬错误，须修正后才能 stamp/计算。" % len(errors))
        sys.exit(1)
    if not verified:
        print("[RESULT] 结构通过，但未人工核验；run_meta 守卫会拦截。请核验后 stamp --confirm。")
        sys.exit(0)
    print("[RESULT] 校验通过且已人工核验 ✅ 可直接喂 run_meta.py --data %s" % csv_path)


# ---------------------------------------------------------------------------
# subcommand: stamp
# ---------------------------------------------------------------------------
def cmd_stamp(args):
    csv_path = args.csv
    prov = load_provenance(csv_path)
    if prov is None:
        print("[ERROR] 无同伴 .provenance.json，无法 stamp。请先用 scaffold 生成。")
        sys.exit(2)
    if not args.confirm:
        print("[DRY-RUN] 将把 verified_by_human 置 YES。确认人工已逐行核验（含来源页码/表号）后加 --confirm。")
        sys.exit(0)
    prov["verified_by_human"] = True
    write_provenance(csv_path, prov)
    print("[OK] verified_by_human=YES -> %s" % provenance_path(csv_path))
    print("     现在 run_meta.py --data %s 将通过守卫。" % csv_path)


# ---------------------------------------------------------------------------
# subcommand: types
# ---------------------------------------------------------------------------
def cmd_types(args):
    print("支持的 Type（与 data_templates.md 对应）：")
    for t, spec in SCHEMA.items():
        cols = ", ".join(c for c, _ in spec["cols"])
        print("  %-18s %s" % (t, cols))
        print("  %-18s  效应量提示: %s" % ("", spec["measure_hint"]))


def main():
    ap = argparse.ArgumentParser(description="meta-analysis 数据提取助手（草稿+人工核验闸）")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p_sc = sub.add_parser("scaffold", help="生成空白抽取表 + provenance 同伴文件")
    p_sc.add_argument("--type", required=True, help="binary/continuous/precomputed/rate/correlation/single_proportion/single_mean")
    p_sc.add_argument("--out", required=True, help="输出 CSV 路径")
    p_sc.add_argument("--studies", default="", help="逗号分隔的研究名，预填 study 列（可选）")
    p_sc.add_argument("--studies-file", default="", help="最终纳入清单文件（json/txt/csv），自动预填 study 列；与 --studies 合并去重。建议由 Stage3 人工确认后持久化")
    p_sc.add_argument("--covariates", default="", help="协变量列（逗号分隔，如 'latitude,allocation,vaccine_type'），追加到 binary/continuous 表；BCG 等需元回归/亚组分析时必填")
    p_sc.add_argument("--covariates-json", default=None, help="协变量类型覆盖 JSON（{列: 'int'|'float'|'str'}），未指定列自动按列名启发式判定")
    p_sc.set_defaults(func=cmd_scaffold)

    p_va = sub.add_parser("validate", help="校验已填 CSV 结构与数值合理性")
    p_va.add_argument("--csv", required=True, help="待校验 CSV")
    p_va.set_defaults(func=cmd_validate)

    p_st = sub.add_parser("stamp", help="人工核验通过后标记 verified_by_human=YES")
    p_st.add_argument("--csv", required=True, help="抽取 CSV")
    p_st.add_argument("--confirm", action="store_true", help="确认人工已核验（无此旗为 dry-run）")
    p_st.set_defaults(func=cmd_stamp)

    p_ty = sub.add_parser("types", help="列出支持的 Type 与列")
    p_ty.set_defaults(func=cmd_types)

    args = ap.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
