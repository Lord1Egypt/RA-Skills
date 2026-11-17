# -*- coding: utf-8 -*-
"""人工驱动 Meta 分析案例（HITL 逐闸）演示脚本 —— catalog 驱动版。

用法：
  python run_case_human.py list
      → 列出全部案例（id / 标题 / 类别 / 效应量 / 模板）。

  python run_case_human.py start [--case C04] [--pause-at A4,B4,C3,C4] [--engine local]
      → 载入案例（默认 C01），注入其研究数据，跑到第一个红线闸停靠。
      --case <id>    从 cases/case_catalog.json 载入指定案例
      --pause-at     逗号分隔的阶段停靠点（默认仅 4 个红线闸；可填任意阶段做软停）
      --engine       计算路径（默认 coze，走本地 R 镜像 run_task.R，不经 coze 云；
                      local = 本地 numpy 确定性实现 b1_pairwise_python）

  python run_case_human.py decide <session_path> <action> <stage_id> [--revision-file f.json]
      action ∈ {approved, rejected, revised}

计算默认走本地 R 引擎镜像（coze 代码同源，run_task.R），不经 coze 云。
A2 文献检索被 patch 为返回案例数据集（演示用，避免联网）；A3 直通（人工已定数据集）。
红线闸（A4/B4/C3/C4）需人工决策方可放行；软停（A1/A3/C1）自动推进。
"""
import sys
import os
import json
import argparse
import math

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "cases"))  # case_catalog

import coze_client as cc
import block_a
import block_b  # noqa: F401
import fullflow
import case_catalog as cat

# —— 离线真实 R 计算（coze 镜像，不经 coze 云）——
cc.run_stage = cc.run_stage_local

CASES_DIR = os.path.join(HERE, "..", "cases")
DEFAULT_PAUSE = {"A4.data_extraction", "B4.quality_gate", "C3.ref_verify", "C4.evidence_qa"}


# ── 按模板把案例研究归一化为 block_b 可消费的行 ──────────────────────────────
def _se_from_ci(lower, upper):
    return (float(upper) - float(lower)) / (2 * 1.96)


def _fisher_z(r):
    r = max(min(float(r), 0.999999), -0.999999)
    return 0.5 * math.log((1 + r) / (1 - r))


def normalize_case(case):
    """返回 (rows, nma_contrasts_or_None, engine_hint, offline_note)。

    rows: 喂给 extension_table 的研究行（已是 block_b 能识别的形状）。
    nma_contrasts: TPL-09 时构建的对比列表（TE/seTE/t1/t2/studlab），否则 None。
    engine_hint: 'coze'（本地 R 镜像）或 'local'（numpy）。
    offline_note: 该形状离线计算的说明/限制。
    """
    tid = case["template_id"]
    em = case["effect_measure"]
    studies = case["studies"]
    note = ""

    if tid == "TPL-01":  # 二分类 2x2（OR/RR/RD） → ai/bi/ci/di
        rows = []
        for s in studies:
            rows.append({
                "study": s.get("study"), "year": s.get("year"),
                "ai": s["event_exp"], "bi": s["n_exp"] - s["event_exp"],
                "ci": s["event_ctrl"], "di": s["n_ctrl"] - s["event_ctrl"],
                "arm": s.get("arm", ""),
            })
        if em == "RD":
            note = "RD 本地 numpy 引擎按 MD 路径处理（与 OR/RR 对数尺度不同）；精确 RD 需 coze R 引擎 metabin(sm='RD')。"
        return rows, None, "coze", note, None

    if tid == "TPL-02":  # 连续型两臂
        rows = []
        if em == "SMD":  # 标准化均数差：逐研究 Hedges 标准化为 TE/seTE（本地 numpy 走通用逆方差）
            for s in studies:
                m1, s1, n1 = s["mean_exp"], s["sd_exp"], s["n_exp"]
                m2, s2, n2 = s["mean_ctrl"], s["sd_ctrl"], s["n_ctrl"]
                sp = math.sqrt(((n1 - 1) * s1 ** 2 + (n2 - 1) * s2 ** 2) / (n1 + n2 - 2))
                d = (m1 - m2) / sp if sp else 0.0
                se = math.sqrt(1.0 / n1 + 1.0 / n2 + d ** 2 / (2 * (n1 + n2)))
                rows.append({"study": s.get("study"), "year": s.get("year"),
                             "TE": d, "seTE": se, "_em": "SMD"})
            return rows, None, "local", "SMD 已按 Hedges 标准化为 TE/seTE，走本地 numpy 通用逆方差合并。", None
        # MD：原始均数差（本地 numpy MD 路径）
        for s in studies:
            rows.append({
                "study": s.get("study"), "year": s.get("year"),
                "mean_e": s["mean_exp"], "sd_e": s["sd_exp"], "n_e": s["n_exp"],
                "mean_c": s["mean_ctrl"], "sd_c": s["sd_ctrl"], "n_c": s["n_ctrl"],
            })
        return rows, None, "local", "连续型 MD 走本地 numpy（b1_pairwise_python）。", None

    if tid == "TPL-03":  # 已有效应量 → TE/seTE（通用逆方差）
        rows = []
        for s in studies:
            rows.append({
                "study": s.get("study"), "year": s.get("year"),
                "TE": float(s["effect_size"]),
                "seTE": _se_from_ci(s["lower95"], s["upper95"]),
                "_em": s.get("effect_type"),
            })
        return rows, None, "local", "已有效应量走本地 numpy 通用逆方差合并。", None

    if tid == "TPL-08":  # 生存 HR → TE=lnHR, seTE（按 HR 对数路径）
        rows = []
        for s in studies:
            rows.append({
                "study": s.get("study"), "year": s.get("year"),
                "treatment": s.get("treatment", ""),
                "TE": float(s["lnHR"]), "seTE": float(s["se_lnHR"]),
            })
        return rows, None, "local", "生存 HR 以 lnHR±se 走通用逆方差合并（HR 对数尺度）。", None

    if tid == "TPL-11":  # 多臂 RCT → 每对比拆为 ai/bi/ci/di（OR）
        rows = []
        for s in studies:
            rows.append({
                "study": s.get("study"), "comparison": s.get("comparison", ""),
                "ai": s["event_A"], "bi": s["n_A"] - s["event_A"],
                "ci": s["event_B"], "di": s["n_B"] - s["event_B"],
            })
        return rows, None, "coze", "多臂 RCT 按「活性药 vs 对照」对比拆为 pairwise OR。", None

    if tid == "TPL-09":  # 网状 Meta → 构建「全部两两对比」（TE/seTE/t1/t2/studlab）
        # 关键：netmeta 的对比接口（TE/seTE）要求每个多臂研究提供 C(k,2) 条对比，
        # 而非仅「各活性臂 vs 参考臂」。以 3 臂研究为例须给 3 条对比（含活性臂互比），
        # 否则报 "wrong number of comparisons"。参考干预 = 在每个研究都出现的共同对照（如安慰剂）。
        by_study = {}
        for s in studies:
            by_study.setdefault(s["study"], []).append(s)
        arm_presence = {}
        for arms in by_study.values():
            for a in arms:
                arm_presence[a["arm"]] = arm_presence.get(a["arm"], 0) + 1
        ref = next((nm for nm, cnt in arm_presence.items()
                    if cnt == len(by_study)), None)
        contrasts = []
        for st, arms in by_study.items():
            m = len(arms)
            for i in range(m):
                for j in range(i + 1, m):
                    a, b = arms[i], arms[j]
                    a2, b2 = a["event"] + 0.5, (a["n"] - a["event"]) + 0.5
                    c2, d2 = b["event"] + 0.5, (b["n"] - b["event"]) + 0.5
                    TE = math.log((a2 * d2) / (b2 * c2))
                    se = math.sqrt(1 / a2 + 1 / b2 + 1 / c2 + 1 / d2)
                    contrasts.append({"TE": TE, "seTE": se,
                                      "t1": a["arm"], "t2": b["arm"], "studlab": st})
        note = "网状 Meta：arm-based → 全部两两对比（含非参考臂互比），本地 netmeta（b1_nma_r）。"
        return contrasts, contrasts, "nma", note, ref

    # TPL-04(IRR)/TPL-05(ZCOR)/TPL-06(单组率)/TPL-07(单组均值)/TPL-10(DTA)
    # 本地 numpy/block_b 暂不覆盖，需 metafor 模型（coze 路径，当前冻结）。
    return studies, None, "coze", (
        "该数据形状（%s）本地 numpy 引擎不覆盖，需 coze R 引擎（metafor）路径；"
        "当前开发期冻结未部署，B1 将返回「无可计算研究」。案例数据/模板本身有效。" % tid), None


def _patch_engine(engine_hint, nma_contrasts, nma_reference=None):
    """运行时 patch block_b，使本地计算按形状正确路由（不改发布代码）。"""
    if engine_hint == "local":
        _orig = block_b.b1_meta_analysis

        def _local(studies, effect_measure="OR", engine="coze", nma=False, network_studies=None):
            return _orig(studies, effect_measure, engine="local", nma=nma,
                         network_studies=network_studies)
        block_b.b1_meta_analysis = _local
    if nma_contrasts is not None:
        _orig = block_b.b1_meta_analysis
        _ct = nma_contrasts
        _ref = nma_reference

        def _nma(studies, effect_measure="OR", engine="coze", nma=False, network_studies=None):
            return _orig(studies, effect_measure, engine=engine, nma=True,
                         network_studies=_ct, nma_reference=_ref)
        block_b.b1_meta_analysis = _nma


# ── 形状无关的人工核验清单 ────────────────────────────────────────────────────
def _summarize(r):
    ff = r.get("fullflow", {})
    await_ = ff.get("await", {})
    sid = await_.get("stage_id")
    stages = r.get("stages") or []
    kind = await_.get("kind")
    print("\n===== 人工核验清单（阶段 %s，类型 %s）=====" % (sid, kind))
    prompt = await_.get("prompt")
    if prompt:
        print("提示:", prompt)
    if sid == "A4.data_extraction":
        for s in stages:
            if (s.get("stage") or {}).get("id") == "A4.data_extraction":
                rows = (s.get("stage_result") or {}).get("extracted_rows") or []
                print("已抽取研究数:", len(rows))
                for row in rows:
                    info = {k: v for k, v in row.items()
                            if k not in ("_review",) and v not in (None, "")}
                    print("   ·", info)
    elif sid == "B4.quality_gate":
        for s in stages:
            st = (s.get("stage") or {}).get("id")
            sr = s.get("stage_result") or {}
            if st == "B1.meta_analysis":
                pw = sr.get("pairwise") or {}
                print("合并效应(随机): TE=", pw.get("TE_random"),
                      " 95%CI:", pw.get("ci_random"), " p:", pw.get("p_random"),
                      " I2:", pw.get("I2"), " k:", pw.get("k"))
                nma = sr.get("nma") or {}
                if nma.get("status") == "ok":
                    print("NMA:", nma.get("league") or nma.get("summary")
                          or json.dumps({k: nma.get(k) for k in ("TE", "seTE")}, ensure_ascii=False))
            if st == "B4.quality_gate":
                print("质量门报告:", json.dumps(sr, ensure_ascii=False)[:600])
    elif sid in ("C3.ref_verify", "C4.evidence_qa"):
        for s in stages:
            st = (s.get("stage") or {}).get("id")
            if st == sid:
                sr = s.get("stage_result") or {}
                if "manuscript" in sr:
                    print("稿件（前 800 字）:\n", str(sr["manuscript"])[:800])
                elif "references" in sr:
                    print("参考文献数:", len(sr["references"]))
                    for ref in sr["references"][:8]:
                        print("   ·", ref)
                else:
                    print("stage_result 键:", list(sr.keys())[:10])
    elif kind == "done":
        print("流程已完成（C4 放行）。可渲染 HTML 报告。")
    elif kind == "handoff_confirm":
        print("块间交接确认：", json.dumps(ff.get("handoff_preview"), ensure_ascii=False))
    print("=====================================\n")


def cmd_list():
    print("案例库（%d 个）：" % len(cat.CASES))
    print("%-6s %-10s %-10s %-22s %s" % ("ID", "类别", "效应量", "模板", "标题"))
    for c in cat.CASES:
        print("%-6s %-10s %-10s %-22s %s" % (c["id"], c["category"], c["effect_measure"],
                                             c["template_id"], c["title"]))


def cmd_start(case_id="C01", pause_at=None, engine=None):
    case = cat.case_by_id(case_id)
    rows, nma_contrasts, engine_hint, note, nma_reference = normalize_case(case)
    if engine:
        engine_hint = engine
    _patch_engine(engine_hint, nma_contrasts, nma_reference)

    # 注入案例数据集（避免 A2 联网；A3 直通）
    block_a.a2_literature_search = lambda *a, **k: (rows, [], None)
    block_a.a3_screening = lambda studies, **k: (studies, {"note": "人工指定数据集，跳过自动筛选"})

    pa = DEFAULT_PAUSE if pause_at is None else set(pause_at.split(","))
    print("载入案例 %s — %s" % (case_id, case["title"]))
    print("模板 %s | 效应量 %s | 计算路径 %s" % (case["template_id"], case["effect_measure"], engine_hint))
    if note:
        print("注：", note)

    r = fullflow.run_fullflow(
        case["topic"], extraction_table=rows,
        effect_measure=case["effect_measure"], nma=(nma_contrasts is not None),
        pause_at=pa, session_dir=os.path.join(HERE, "..", "cases"))
    _summarize(r)
    print("SESSION:", r["fullflow"].get("session_path"))
    return r


def cmd_decide(session_path, action, stage_id, revision_file=None):
    dec = {"action": action, "stage_id": stage_id, "decided_by": "user"}
    if action == "revised" and revision_file:
        dec["revision"] = json.load(open(revision_file, encoding="utf-8"))
    r = fullflow.resume_fullflow(session_path, dec)
    if "error" in r:
        print("ERROR:", r["error"])
        return r
    _summarize(r)
    print("SESSION:", r.get("fullflow", {}).get("session_path") or session_path)
    return r


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd")
    sub.add_parser("list")
    p = sub.add_parser("start")
    p.add_argument("--case", default="C01")
    p.add_argument("--pause-at", default=None)
    p.add_argument("--engine", default=None, choices=["coze", "local"])
    p = sub.add_parser("decide")
    p.add_argument("session")
    p.add_argument("action")
    p.add_argument("stage_id")
    p.add_argument("--revision-file", default=None)
    args = ap.parse_args()
    if args.cmd == "list":
        cmd_list()
    elif args.cmd == "start":
        cmd_start(args.case, args.pause_at, args.engine)
    elif args.cmd == "decide":
        cmd_decide(args.session, args.action, args.stage_id, args.revision_file)
    else:
        ap.print_help()
