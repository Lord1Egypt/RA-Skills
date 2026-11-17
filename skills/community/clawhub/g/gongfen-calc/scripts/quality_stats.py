"""quality_stats —— 质检 + 统计口径（分档、覆盖度、自检、批次评级）。"""
from __future__ import annotations

import json
import math
import re
from collections import Counter
from pathlib import Path

import numpy as np

import params as P
from excel_io import is_null, norm_str
from field_recognize import parse_date_range

# ============================================================ 基础统计
def percentile(values, qs):
    if not values:
        return None
    return np.percentile(np.asarray(values, dtype=float), qs, method="linear")


def band(values, absolute_bands=None):
    """分位数相对分档（右闭）。返回 (levels, mode, edges)。

    退化条件：n < MIN_N_PERCENTILE 或 P10 == P90 → 绝对档。
    """
    vals = [float(v) for v in values if v is not None]
    n = len(vals)
    if n == 0:
        return [], "empty", []
    if n < P.MIN_N_PERCENTILE:
        edges = list(absolute_bands or [])
        levels = [1 + sum(v > e for e in edges) for v in vals]
        return levels, "absolute", edges

    p10, p30, p70, p90 = percentile(vals, list(P.PERCENTILES))
    if p10 == p90:
        edges = list(absolute_bands or [])
        levels = [1 + sum(v > e for e in edges) for v in vals]
        return levels, "absolute_degenerate", edges

    edges = [p10, p30, p70, p90]
    levels = [1 + sum(v > e for e in edges) for v in vals]
    return levels, "relative", [round(float(e), 4) for e in edges]


def rank_quintile(values):
    """兜底：等频五分（用于无绝对阈值的维度且样本过小）。"""
    idx = sorted(range(len(values)), key=lambda i: (values[i] is None, values[i]))
    n = len(values)
    levels = [None] * n
    for rank, i in enumerate(idx):
        if values[i] is None:
            continue
        levels[i] = min(5, 1 + int(rank * 5 / max(n, 1)))
    return levels


def _rank(data):
    order = sorted(range(len(data)), key=lambda i: data[i])
    ranks = [0.0] * len(data)
    i = 0
    while i < len(order):
        j = i
        while j + 1 < len(order) and data[order[j + 1]] == data[order[i]]:
            j += 1
        avg = (i + j) / 2.0 + 1
        for k in range(i, j + 1):
            ranks[order[k]] = avg
        i = j + 1
    return ranks


def pearson(a, b):
    if len(a) < 2:
        return None
    x, y = np.asarray(a, float), np.asarray(b, float)
    if x.std() == 0 or y.std() == 0:
        return None
    return float(np.corrcoef(x, y)[0, 1])


def spearman(a, b):
    if len(a) < 2:
        return None
    return pearson(_rank(a), _rank(b))


def entropy_levels(levels):
    p = Counter(levels)
    n = sum(p.values())
    if n == 0:
        return None
    ent = 0.0
    for k in range(1, 6):
        prob = p.get(k, 0) / n
        if prob > 0:
            ent -= prob * math.log(prob)
    return ent / math.log(5)


# ============================================================ 工时防护
def apply_hours_protection(tasks, colmap):
    """偏离度打折 + 日期矛盾标记。绝不静默修改原始申报值。"""
    hours_vals = [t["values"].get("hours", {}).get("parsed") for t in tasks]
    ok = [v for v in hours_vals if v is not None]
    notes = {"discount": None, "conflicts": [], "mode": "none"}

    if len(ok) >= P.HOURS_DEVIATION_MIN_N:
        p90 = float(np.percentile(ok, 90))
        for t in tasks:
            hv = t["values"].get("hours", {}).get("parsed")
            if hv is None:
                continue
            eff = min(hv, p90) + P.HOURS_DEVIATION_FACTOR * max(0.0, hv - p90)
            t["values"]["hours"]["effective"] = round(eff, 4)
            if eff < hv - 1e-9:
                t["values"]["hours"]["flags"].append("deviation_discounted")
        notes["discount"] = {"p90": round(p90, 4), "factor": P.HOURS_DEVIATION_FACTOR}
        notes["mode"] = "deviation_discount"
    else:
        for t in tasks:
            hv = t["values"].get("hours", {}).get("parsed")
            if hv is not None:
                t["values"]["hours"]["effective"] = hv
        notes["mode"] = "no_discount_small_sample"

    # 日期矛盾：声称工时 > 可用工时 × 1.5 → 只标记，不改分
    for t in tasks:
        hv = t["values"].get("hours", {}).get("parsed")
        avail = t["meta"].get("avail_hours")
        if hv is None or not avail:
            continue
        if hv <= avail * P.HOURS_EXEMPT_RATIO:
            # 物理可行 → 豁免打折（"大"不等于"假"），阈值与矛盾标记同一根线
            t["values"]["hours"]["effective"] = hv
            t["values"]["hours"]["exempt_physical"] = True
            t["values"]["hours"]["flags"].append("exempt_physical")
        if hv > avail * P.HOURS_CONFLICT_RATIO:
            t["values"]["hours"]["flags"].append("date_conflict")
            t["flags"].append("hours_date_conflict")
            notes["conflicts"].append({
                "task_id": t["task_id"], "task_name": t["task_name"],
                "claimed_hours": hv, "available_hours": round(avail, 2),
                "ratio": round(hv / avail, 2),
                "action": "仅标记，不自动改分，请人工复核",
            })
    return notes


def compute_avail_hours(tasks):
    """起止日期 → 可用工时（自然日 × 8 × 0.7，不扣节假日）。"""
    out = []
    for t in tasks:
        days = t["meta"].get("natural_days")
        if days:
            avail = days * P.HOURS_PER_MANDAY * P.WORKDAY_FACTOR
            t["meta"]["avail_hours"] = round(avail, 2)
            out.append((t["values"].get("hours", {}).get("parsed"), avail))
    return out


# ============================================================ 等级计算
BANDED_DIMS = ("hours", "money", "collab")
DIRECT_DIMS = ("difficulty", "risk", "urgency", "quality", "reuse")


def compute_levels(tasks, enabled_dims):
    """为启用维度计算 1–5 档位。返回分档说明。"""
    info = {}
    for dim in enabled_dims:
        if dim in BANDED_DIMS:
            idx = [i for i, t in enumerate(tasks)
                   if t["values"].get(dim, {}).get("parsed") is not None]
            vals = [tasks[i]["values"][dim]["parsed"] for i in idx]
            if dim == "hours":
                # 定金口径：分档一律用**原始工时**。打折只作用于工分系数 K_偏离，
                # 不用 h_eff 分档（否则绝对档下会二次惩罚，且与 K_偏离 重复打折）
                vals = [tasks[i]["values"][dim]["parsed"] for i in idx]
                levels, mode, edges = band(vals, P.ABSOLUTE_BANDS)
            elif dim == "money":
                levels, mode, edges = band(vals)
                if mode.startswith("absolute"):
                    levels = rank_quintile(vals)
                    mode = "rank_quintile"
            else:
                edges = list(P.COLLAB_LEVEL_CUTS)
                levels = [1 + sum(v > e for e in edges) for v in vals]
                mode = "cuts"
            for pos, i in enumerate(idx):
                tasks[i]["values"][dim]["level"] = int(levels[pos])
            info[dim] = {"mode": mode, "edges": edges, "n": len(idx)}
        elif dim in DIRECT_DIMS:
            n_ok = 0
            for t in tasks:
                lv = t["values"].get(dim, {}).get("level")
                if lv is not None:
                    n_ok += 1
            info[dim] = {"mode": "direct", "n": n_ok}
        else:
            info[dim] = {"mode": "excluded", "n": 0}
    return info


# ============================================================ 质检
def check(bundle, header, colmap, tasks, excluded_rows, raw_row_count) -> dict:
    warnings, blockers = [], []
    n = len(tasks)

    def warn(code, level, msg, echo=None):
        warnings.append({"code": code, "level": level, "msg": msg, "echo": echo or {}})

    # 1 文件层
    if bundle.get("formula_uncomputed"):
        warn("W_FORMULA_UNCOMPUTED", "info",
             f"检测到 {bundle['formula_uncomputed']} 个公式格未计算（读数为空），建议用 Excel 打开另存", {})
    if bundle.get("encoding") and bundle["encoding"] not in ("utf-8-sig", "utf-8"):
        warn("W_ENCODING_CONVERTED", "info",
             f"文件编码为 {bundle['encoding']}，已按该编码解析", {"encoding": bundle["encoding"]})

    # 2 必填门槛
    mapped = {c["mapped_to"] for c in colmap["columns"]}
    if "task_name" not in mapped:
        echo = _failure_echo(colmap)
        echo["missing_required"] = ["任务名称列（任务/事项/标题 任一别名）"]
        blockers.append({"code": "E_NO_TASK_NAME", "msg": "未识别到任务名称列", "echo": echo})
    # 用户口径：只要识别到任务名称或描述就执行分析，缺失的维度不分析（降权重重分配）。
    # 因此「无可量化维度」不再阻断，仅降级提示；唯一阻断条件是没有任务名/描述列。
    quant = {"hours", "money", "difficulty", "risk", "priority", "quality", "collab"}
    if not (mapped & quant):
        echo = _failure_echo(colmap)
        echo["missing_required"] = []
        echo["suggestions"] = [
            "工时（或 人天/耗时/起止日期）—— 补齐后覆盖度可从 20% 提升到约 40%",
            "优先级（P0-P3）或截止日期 —— 补齐后可达 50% 进入可排名区间",
            "金额（或 合同额/营收）—— 补齐后可启用经济效益维度",
        ]
        warn("W_NO_QUANT_DIM", "degrade",
             "未识别到任何可量化维度（无工时/金额/优先级/质量记录），"
             "仅按任务名与描述推断难度；结果仅供排序参考，不能用于分配",
             echo)

    # 3 样本量
    if n and n < P.MIN_TASKS:
        warn("W_SMALL_SAMPLE", "degrade",
             f"任务数 {n} < 3，禁用分位数分档，改用绝对档，样本量不足、分档精度下降", {"n": n})

    # 4 任务名质量
    names = [t["task_name"] for t in tasks]
    if names:
        uniq = len(set(names)) / len(names)
        if uniq < P.DUP_NAME_RATIO_WARN:
            warn("W_LOW_NAME_UNIQUENESS", "warn",
                 f"任务名唯一率仅 {uniq:.0%}，疑似选错列（可能选中了类型/状态列）", {"uniq": round(uniq, 3)})
        placeholder = sum(1 for x in names if re_like_placeholder(x))
        if placeholder / max(len(names), 1) > 0.8:
            warn("W_PLACEHOLDER_NAMES", "warn",
                 f"{placeholder}/{len(names)} 条任务名为「任务N」类占位名，无业务含义，无法人工复核", {})

    # 5 缺失率
    for dim in ("hours", "money", "difficulty", "risk", "urgency", "collab", "quality"):
        if dim not in mapped:
            continue
        got = sum(1 for t in tasks
                  if (t["values"].get(dim, {}).get("parsed") is not None
                      or t["values"].get(dim, {}).get("level") is not None))
        rate = got / max(n, 1)
        if rate == 0:
            warn(f"W_DIM_EMPTY_{dim.upper()}", "warn", f"{P.DIM_LABELS.get(dim, dim)} 全部为空，该维度不启用", {})
        elif rate < P.COL_NULL_RATE_DROP:
            warn(f"W_DIM_SPARSE_{dim.upper()}", "info",
                 f"{P.DIM_LABELS.get(dim, dim)} 有效覆盖 {rate:.0%}，低于 {P.COL_NULL_RATE_DROP:.0%}，建议补充", {})

    # 6 金额：非空且非 0
    money_valid = [t for t in tasks if (t["values"].get("money", {}).get("parsed") or 0) > 0]
    money_rate = len(money_valid) / max(n, 1)
    if "money" in mapped and money_rate < P.DIM_COVERAGE_CLOSE:
        warn("W_MONEY_COVERAGE_LOW", "info",
             f"金额有效覆盖（非空且非 0）{money_rate:.0%}，低于 50% 关闭线，将关闭 C 维并把权重转入 A/B", {})

    # 7 异常值
    hi = [t for t in tasks if (t["values"].get("hours", {}).get("parsed") or 0) > P.MAX_HOURS_ABSURD]
    if hi:
        warn("W_HOURS_ABSURD", "warn",
             f"{len(hi)} 条任务工时 > {P.MAX_HOURS_ABSURD} 小时，疑似异常，已标记未剔除",
             {"tasks": [t["task_id"] for t in hi]})
    neg = [t for t in tasks if (t["values"].get("hours", {}).get("parsed") or 0) < 0]
    if neg:
        warn("W_HOURS_NEGATIVE", "warn",
             f"{len(neg)} 条任务工时为负（可能为返工扣减），不参与分位数计算",
             {"tasks": [t["task_id"] for t in neg]})

    # 8 重复
    dup_full = Counter(
        (t["task_name"], str(t["values"].get("hours", {}).get("parsed")),
         str(t["values"].get("money", {}).get("parsed"))) for t in tasks)
    dups = sum(c - 1 for c in dup_full.values() if c > 1)
    if dups:
        warn("W_DUPLICATE_ROWS", "warn",
             f"检测到 {dups} 条完全重复任务行（任务名+工时+金额相同），已保留首条", {"count": dups})

    # 9 日期
    if "urgency" in mapped:
        deadlines = [t["meta"].get("deadline") for t in tasks]
        dd = [d for d in deadlines if d]
        if dd and len(set(dd)) == 1 and len(dd) > 2:
            warn("W_DEADLINE_HOMOGENEOUS", "warn",
                 f"{len(dd)} 条任务截止日期完全相同（{dd[0]}），紧迫性维度无区分度", {"deadline": str(dd[0])})

    # 10 剔除
    if excluded_rows:
        warn("W_ROWS_EXCLUDED", "info",
             f"已剔除 {len(excluded_rows)} 行（合计/小计/备注/空行/重复表头），明细见附录", {})

    # 11 隐藏行列
    for sheet in bundle["sheets"]:
        if sheet.get("hidden_cols"):
            warn("W_HIDDEN_COLS", "info",
                 f"检测到 {len(sheet['hidden_cols'])} 个隐藏列（sheet={sheet['name']}），已忽略", {})

    return {
        "warnings": warnings,
        "blockers": blockers,
        "n_raw_rows": raw_row_count,
        "n_data_rows": n,
        "n_excluded": len(excluded_rows),
        "excluded_rows": excluded_rows,
        "money_valid_rate": round(money_rate, 4),
    }


def re_like_placeholder(name: str) -> bool:
    s = norm_str(name)
    return bool(re.match(r"^(任务|事项|工作项|item|task)\s*\d*$", s, re.I))


def _failure_echo(colmap):
    """失败必须回显三件套：已识别列名 / 缺失必要字段 / 建议补充列。"""
    mapped = [{"raw_name": c["raw_name"], "mapped_to": c["mapped_to"],
               "confidence": c["confidence"], "method": c["method"]}
              for c in colmap["columns"]]
    all_cols = [c["raw_name"] for c in colmap["columns"]] + \
               [u["raw_name"] for u in colmap["unmapped"]]
    return {
        "recognized_columns": mapped,
        "all_column_names": all_cols,
        "missing_required": ["任务名称（任务/事项/标题 任一别名）"],
        "suggested_columns": [
            "任务名称", "难度等级（或 复杂度/类型/标签）",
            "工时（或 人天/耗时/起止日期）", "金额（或 合同额/营收/收益）",
            "优先级（P0-P3）", "截止日期",
        ],
    }


# ============================================================ 批次评级
def cap_weights(norm: dict) -> dict:
    """单维归一权重 40% 封顶（仅 |S| >= 3 时数学上可满足）。"""
    if len(norm) <= 2:
        return dict(norm)
    w = dict(norm)
    for _ in range(20):
        over = {k: v for k, v in w.items() if v > P.WEIGHT_CAP + 1e-9}
        if not over:
            break
        excess = sum(v - P.WEIGHT_CAP for v in over.values())
        for k in over:
            w[k] = P.WEIGHT_CAP
        under = {k: v for k, v in w.items() if v < P.WEIGHT_CAP - 1e-9}
        if not under:
            break
        base = sum(under.values())
        for k in under:
            w[k] += excess * (w[k] / base)
    total = sum(w.values())
    return {k: v / total for k, v in w.items()} if total else w


def assess(colmap, tasks, quality) -> dict:
    """权重、覆盖度、有效自由度（打分之前必须调用）。"""
    mapped = {c["mapped_to"] for c in colmap["columns"]}
    dim_fields = {
        "difficulty": "difficulty", "hours": "hours", "money": "money",
        "risk": "risk", "quality": "quality", "urgency": "priority",
        "collab": "collab", "reuse": "reuse",
    }
    enabled, coverage = [], {}
    n = max(len(tasks), 1)
    # 启用门槛：A 用关键词命中率 20%（缺列也能靠任务名判定）；J 需有交付物列且命中率 20%；
    # 其余按有效值率 50%
    thresholds = {"difficulty": P.A_KEYWORD_MIN_HIT_RATE, "reuse": P.A_KEYWORD_MIN_HIT_RATE}
    for dim, field in dim_fields.items():
        if dim in P.PERMANENTLY_OFF:
            coverage[dim] = 0.0
            continue
        if dim == "reuse" and "reuse" not in mapped:
            # J 只在表里有交付物列时启用 —— 仅凭任务名里出现「看板/模板」就开一个 5 分维度
            # 会让完整度分母虚高、噪声进总分（这是上一版实测暴露的问题）
            coverage[dim] = 0.0
            continue
        got = sum(1 for t in tasks
                  if (t["values"].get(dim, {}).get("parsed") is not None
                      or t["values"].get(dim, {}).get("level") is not None))
        rate = got / n
        if dim == "money":
            rate = sum(1 for t in tasks if (t["values"].get("money", {}).get("parsed") or 0) > 0) / n
        coverage[dim] = round(rate, 4)
        # A 困难程度：用户要求必须从任务名/描述判断，命中率低只提示、不关闭维度
        if dim == "difficulty" and P.A_FORCE_ENABLE:
            if rate > 0:
                enabled.append(dim)
            continue
        if rate >= thresholds.get(dim, P.DIM_COVERAGE_CLOSE):
            enabled.append(dim)

    base = {d: P.WEIGHTS.get(d, 0.0) for d in enabled if P.WEIGHTS.get(d, 0.0) > 0}
    for d, add in P.MONEY_CLOSE_TRANSFER.items():
        if d in base:
            base[d] += add

    # 覆盖度 = 已启用维度基础权重和 / 100（上限 100）
    weight_total = round(min(100.0, sum(base.values())), 2)
    raw_sum = sum(base.values())
    prelim = {d: w / raw_sum for d, w in base.items()} if raw_sum else {}
    norm = cap_weights(prelim)
    norm = {d: round(v, 4) for d, v in norm.items()}

    n_eff = (sum(norm.values()) ** 2 / sum(v ** 2 for v in norm.values())
             if norm and sum(v ** 2 for v in norm.values()) else 0.0)
    max_single = max(norm.values()) if norm else 0.0

    if weight_total >= P.COVERAGE_NORMAL:
        grade = "A_正常"
    elif weight_total >= P.COVERAGE_RANK:
        grade = "B_可排名"
    else:
        grade = "C_仅描述"

    flags = []
    if max_single > P.WEIGHT_CONCENTRATION:
        top = max(norm, key=norm.get)
        flags.append({"code": "W_WEIGHT_CONCENTRATED",
                      "msg": f"{P.DIM_LABELS[top]} 归一化权重 {max_single:.0%} > 35%，"
                             f"结果对该维度锚点高度敏感，须先校准该维度"})
    if len(norm) <= 2:
        flags.append({"code": "W_CAP_UNSATISFIABLE",
                      "msg": f"仅 {len(norm)} 个维度，40% 单维上限数学上不可满足，"
                             f"强制转「仅排序参考」分支"})
    if any(v < P.MIN_WEIGHT_KEEP for v in norm.values()):
        weak = [P.DIM_LABELS[d] for d, v in norm.items() if v < P.MIN_WEIGHT_KEEP]
        flags.append({"code": "W_WEAK_DIM",
                      "msg": f"{'/'.join(weak)} 权重 < 5%，对结果影响微弱（保留不并入）"})
    if n_eff < P.N_EFF_MIN:
        flags.append({"code": "W_LOW_EFFECTIVE_DIM",
                      "msg": f"有效自由度仅 {n_eff:.2f} 个（<{P.N_EFF_MIN}），体系不足以支撑分配"})
    if "money" not in enabled:
        flags.append({"code": "W_MONEY_DIM_OFF",
                      "msg": "C 经济效益维度未启用，权重按通用归一化回补给其他维度"})

    return {
        "enabled_dims": sorted(enabled),
        "weight_raw": base,
        "weight_normalized": norm,
        "weight_total": weight_total,
        "n_eff": round(n_eff, 2),
        "max_single_weight": round(max_single, 4),
        "coverage_grade": grade,
        "coverage_by_dim": coverage,
        "flags": flags,
        "branch": None,   # 由 run 在完成自检后填入
    }


# ============================================================ 自检
def selfcheck(tasks, assessment) -> dict:
    enabled = assessment["enabled_dims"]
    out = {}

    # A/B 相关性
    ab = [t for t in tasks
          if t["values"].get("difficulty", {}).get("level") is not None
          and t["values"].get("hours", {}).get("level") is not None]
    corr = {"executed": False, "n": len(ab), "note": f"样本量 {len(ab)} < {P.MIN_N_CORRELATION}，重合性检验未执行"}
    if len(ab) >= P.MIN_N_CORRELATION:
        a = [t["values"]["difficulty"]["level"] for t in ab]
        b = [t["values"]["hours"]["level"] for t in ab]
        rho = spearman(a, b)
        r = pearson(a, b)
        corr = {"executed": True, "n": len(ab), "spearman": round(rho, 4) if rho is not None else None,
                "pearson": round(r, 4) if r is not None else None,
                "flag": bool(rho is not None and abs(rho) > P.CORRELATION_THRESHOLD)}
        if corr["flag"]:
            corr["msg"] = (f"难度与工时 Spearman ρ={rho:.2f}（>0.7），两维度高度重合，"
                           f"实际在重复计分")
    out["correlation"] = corr

    # 分布偏斜
    skew = {}
    for dim in enabled:
        lv = [t["values"].get(dim, {}).get("level") for t in tasks]
        lv = [x for x in lv if x is not None]
        if not lv:
            continue
        n = len(lv)
        p = {k: sum(1 for x in lv if x == k) / n for k in range(1, 6)}
        ent = entropy_levels(lv)
        mean = sum(lv) / n
        sd = (sum((x - mean) ** 2 for x in lv) / n) ** 0.5
        # 样本量 < 5 时偏松/偏严判定不成立（2 条同档就 100%），只保留分布集中提示
        small = n < P.MIN_N_PERCENTILE
        f_loose = (not small) and (
            (p[4] + p[5]) > P.LOOSE_P45_RATIO or (mean > P.LOOSE_MEAN and sd < P.LOOSE_SD))
        f_harsh = (not small) and (p[1] + p[2]) > P.HARSH_P12_RATIO
        f_flat = ent is not None and ent < P.ENTROPY_MIN
        skew[dim] = {"n": n, "mean": round(mean, 3), "sd": round(sd, 3),
                     "p4_p5": round(p[4] + p[5], 3), "p1_p2": round(p[1] + p[2], 3),
                     "entropy": round(ent, 3) if ent is not None else None,
                     "flag_loose": bool(f_loose), "flag_harsh": bool(f_harsh),
                     "flag_flat": bool(f_flat),
                     "small_sample": bool(small),
                     "dist": [round(p[k], 3) for k in range(1, 6)]}
        if small:
            skew[dim]["note"] = (f"样本量 n={n} < {P.MIN_N_PERCENTILE}，"
                                 f"偏松/偏严判定不成立，只看分布是否集中")
    out["skew"] = skew

    # 退化：A/B 单维排名一致性
    deg = {"n_eff": assessment["n_eff"], "rank_consistency_AB": None, "verdict": None}
    ab_pairs = [t for t in tasks
                if t["values"].get("difficulty", {}).get("level") is not None
                and t["values"].get("hours", {}).get("level") is not None]
    if len(ab_pairs) >= P.MIN_N_CORRELATION:
        ra = _rank([t["values"]["difficulty"]["level"] for t in ab_pairs])
        rb = _rank([t["values"]["hours"]["level"] for t in ab_pairs])
        rc = spearman(ra, rb)
        deg["rank_consistency_AB"] = round(rc, 4) if rc is not None else None
        if rc is not None and rc > P.RANK_CONSISTENCY_MAX:
            deg["verdict"] = (f"难度排名与工时排名一致性 ρ={rc:.2f}（>0.85），"
                              f"两个维度给出几乎相同的排序，体系实际只有一个有效自由度")
    out["degeneracy"] = deg

    # A 维估算占比（原「双轮一致性」在纯脚本下不可执行）
    a_tasks = [t for t in tasks if t["values"].get("difficulty", {}).get("level") is not None]
    if a_tasks:
        est = sum(1 for t in a_tasks
                  if "qualitative" in (t["values"]["difficulty"].get("flags") or []))
        out["a_estimate"] = {
            "n": len(a_tasks), "estimated": est,
            "ratio": round(est / len(a_tasks), 4),
            "flag": (est / len(a_tasks)) > 0.50,
            "note": ("本批困难程度主要来自关键词推断（占比 %.0f%%），建议人工抽检；"
                     "可在配置中提供『任务类型→难度』映射表提升客观性" % (100 * est / len(a_tasks))),
        }
    else:
        out["a_estimate"] = {"n": 0, "note": "A 维未启用"}

    # 疑似拆分（批内）
    out["split_detect"] = split_detect(tasks)
    return out


def split_detect(tasks) -> dict:
    """首次运行只能做批内空间检测：只提示，不判定。"""
    flags = []
    n = len(tasks)
    if n == 0:
        return {"mode": "intra_batch", "flags": flags}

    hours = {t["task_id"]: (t["values"].get("hours", {}).get("parsed") or 0) for t in tasks}
    total_h = sum(hours.values()) or 1.0

    # ① 前缀聚类
    def stem(name):
        import re
        s = norm_str(name)
        s = re.sub(r"[（(].*?[)）]", "", s)
        s = re.sub(r"第?\d+期|\d+月|\d+$|[-_]v\d+", "", s)
        return s[:6]

    clusters = {}
    for t in tasks:
        clusters.setdefault(stem(t["task_name"]), []).append(t)
    for key, group in clusters.items():
        if len(group) >= 3:
            share = sum(hours[g["task_id"]] for g in group) / total_h
            if share >= 0.30:
                flags.append({"rule": "prefix_cluster", "cluster": key,
                              "count": len(group), "hours_share": round(share, 3),
                              "msg": f"「{key}」相关任务 {len(group)} 条，占全批工时 {share:.0%}，疑似拆分"})

    # ② 工时粒度同质化
    vals = [v for v in hours.values() if v]
    if vals:
        coarse = sum(1 for v in vals if int(v) in (8, 16, 24, 40)) / len(vals)
        med = float(np.median(vals))
        if coarse > 0.70 and med < 8:
            flags.append({"rule": "coarse_granularity", "ratio": round(coarse, 3),
                          "median": round(med, 2),
                          "msg": "工时大量集中在 8/16/24/40 且中位 <8h，疑似按整天凑数"})

    # ③ 颗粒度过细
    avg_len = sum(len(t["task_name"]) for t in tasks) / n
    if avg_len < 6 and n > 30:
        flags.append({"rule": "too_fine", "avg_len": round(avg_len, 2), "n": n,
                      "msg": f"任务名平均 {avg_len:.1f} 字且 {n} 条，颗粒度过细"})

    # ④ 高难度但工时极短
    hi = [t for t in tasks if (t["values"].get("difficulty", {}).get("level") or 0) >= 4]
    if hi and vals:
        p30 = float(np.percentile(vals, 30))
        short = [t for t in hi if (hours[t["task_id"]] or 0) < p30]
        if len(short) / len(hi) > 0.50:
            flags.append({"rule": "difficulty_hours_paradox",
                          "ratio": round(len(short) / len(hi), 3),
                          "msg": "高难度档（4–5）中工时低于全批 P30 的比例 >50%，既难又极短，逻辑矛盾"})
    return {"mode": "intra_batch", "flags": flags}


# ============================================================ baseline
def load_baseline(path) -> dict | None:
    p = Path(path)
    if not p.exists():
        return None
    try:
        return json.loads(p.read_text(encoding="utf-8-sig"))
    except Exception:
        return None


def write_baseline(path, payload) -> None:
    Path(path).write_text(json.dumps(payload, ensure_ascii=False, indent=2),
                          encoding="utf-8-sig")


def compare_baseline(tasks, baseline, freeze) -> dict:
    if not baseline:
        return {"available": False,
                "note": "首次运行无历史批次，环比检测已存档，下次运行生效"}
    old_freeze = baseline.get("caliber_freeze") or {}
    if old_freeze and old_freeze != freeze:
        return {"available": False,
                "note": "换算系数与历史批次不一致，环比检测已禁用（跨批次不可比）"}
    n = len(tasks)
    hours = [t["values"].get("hours", {}).get("parsed") for t in tasks]
    hours = [h for h in hours if h]
    mean_h = sum(hours) / len(hours) if hours else 0
    dn = (n - baseline.get("n_tasks", 0)) / max(baseline.get("n_tasks", 1), 1)
    dh = (mean_h - baseline.get("mean_hours", 0)) / max(baseline.get("mean_hours", 1e-9), 1e-9)
    flag = dn > 0.5 and dh < -0.3
    return {"available": True, "delta_task_ratio": round(dn, 3),
            "delta_mean_hours": round(dh, 3), "flag": bool(flag),
            "note": "任务数环比 +50% 且平均工时环比 −30%，疑似拆分" if flag else "环比未见异常"}
