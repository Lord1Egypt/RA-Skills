"""score —— 降权重重分配、完整度分层、层内排名、工分与总分。

契约：只读 parse 层产出的 JSON，不接触 Excel。
调用顺序：quality → stats.assess → score（assessment 为 None 直接抛错）。

口径（主理人裁定，唯一实现，不接受第二种写法）：
    ① 分档用**原始工时 h**（P10/30/70/90 或绝对档），不用打折后的 h_eff
    ② 小计 S = Σ(score_i × W_i) / ΣW_i   —— S 里**不含任何 K**，否则会双重打折
    ③ 单任务工分 P = S × 20 × K_偏离 × K_体量 × K_角色 × K_子任务
    ④ K_偏离 = h_eff / h，只作用于工分，不回写 S、不回写分档
    ⑤ 不存在 hours_deviation_weight_compression 开关；不做「削 B 权重 + 回补」

红线：绝不产出"某人应得 X 分/应评为 X 级"；不产出淘汰/扣罚名单。
"""
from __future__ import annotations

import math

import params as P


# ============================================================ 小计 S
def valid_dims(task, weights):
    """有档位且权重 > 0 的维度。F 技能门槛永不进小计。"""
    out = []
    for dim, w in weights.items():
        if dim in P.NEVER_SCORED or w <= 0:
            continue
        v = task["values"].get(dim) or {}
        if v.get("level") is not None:
            out.append(dim)
    return out


def subtotal(task, weights):
    """S = Σ(level × W) / ΣW。无有效维度返回 None —— 绝不填 0、绝不填中位 3。"""
    valid = valid_dims(task, weights)
    if not valid:
        return None
    denom = sum(weights[d] for d in valid)
    if denom <= 0:
        return None
    numer = sum(task["values"][d]["level"] * weights[d] for d in valid)
    return numer / denom


# ============================================================ 三个系数
def k_deviation(task):
    """K_偏离 = h_eff / h。返回 (系数, 证据)。物理可行则豁免为 1.0。"""
    h = task["values"].get("hours") or {}
    raw, eff = h.get("parsed"), h.get("effective")
    if h.get("exempt_physical"):
        return 1.0, None
    if not raw or raw <= 0 or eff is None:
        return 1.0, None
    k = max(0.0, min(1.0, float(eff) / float(raw)))
    if k > 0.9999:
        return 1.0, None
    return round(k, 4), {"original_hours": round(float(raw), 2),
                         "effective_hours": round(float(eff), 2)}


def k_volume(task, median_h):
    """K_体量 = 1 + 0.1×log2(h/中位h)，封顶 1.3 / 保底 0.8。默认关闭。"""
    if not P.K_VOLUME_ENABLED or not median_h:
        return 1.0, None
    h = (task["values"].get("hours") or {}).get("parsed")
    if not h or h <= 0:
        return 1.0, None
    lo, hi = P.K_VOLUME_CAP
    k = max(lo, min(hi, 1.0 + 0.1 * math.log2(float(h) / float(median_h))))
    if abs(k - 1.0) < 1e-9:
        return 1.0, None
    return round(k, 4), {"hours": round(float(h), 2), "median_hours": round(float(median_h), 2)}


def k_role(task):
    """K_角色：角色列极不可采，默认 1.0（不启用即恒等）。"""
    return float(P.K_ROLE_DEFAULT), None


def k_subtask(task, by_id):
    """K_子任务：父任务被判为**独立任务**时，子任务折价，防父子重复计分。

    父任务被判为容器时父本身不计分，子任务按 1.0 正常计分。
    """
    pid = task.get("parent_id")
    if not pid:
        return 1.0, None
    parent = by_id.get(pid)
    if parent is None or parent.get("is_container"):
        return 1.0, None
    return float(P.SUBTASK_FACTOR), (
        f"父任务 {pid} 判为独立任务（父工时 > 1.1×子任务之和），"
        f"子任务按 {P.SUBTASK_FACTOR:.2f} 折价以防父子重复计分")


# ============================================================ 完整度 / 分层
def completeness(task, weights, denom=None):
    """完整度 = 该任务有效维度权重和 / 本批启用维度权重和。

    分母用「本批启用权重和」（裁定②）而非固定 100：分层问的是"这个任务相对**本批次
    能拿到的满分**有多全"，不是相对理论满池。同时输出 completeness_vs_100 供对照。
    「整批维度不足」由批次级覆盖度分支负责，两套机制不互相串。
    """
    w = sum(weights[d] for d in valid_dims(task, weights))
    base = denom if denom else 100.0
    return w / base if base else 0.0


def layer_of(comp):
    """两刀分层（裁定③）：>=90 → L1，>=60 → L2，<60 → L3。"""
    pct = comp * 100
    if pct >= P.LAYER_L1:
        return "L1"
    if pct >= P.LAYER_L2:
        return "L2"
    return "L3"


# ============================================================ 主计算
def compute(tasks, assessment, hours_protection=None, force_points=False):
    """assessment 为 None 时抛错 —— 防止绕过「先评级后打分」的顺序约束。

    force_points：人工显式要求「明知覆盖度不足也要出工分」时才为 True（CLI --force-points）。
    默认 False —— 分支判定的降级结论优先，脚本不替人做这个决定。
    """
    if not assessment:
        raise ValueError("score 必须在 batch_assessment 之后调用（收到 None）。"
                         "调用顺序应为 quality → stats.assess → score。")

    weights = assessment["weight_raw"]
    denom = assessment.get("weight_total") or 100.0
    branch = assessment.get("branch") or "A_NORMAL"
    # 裁定④：|S| <= 2 时 40% 上限数学不可满足 → 强制降级且不输出工分
    emit_points = force_points or branch not in ("D_DEGENERATE", "C_DESCRIPTIVE")

    by_id = {t["task_id"]: t for t in tasks}
    hours_raw = [(t["values"].get("hours") or {}).get("parsed") for t in tasks]
    hours_ok = sorted(v for v in hours_raw if v)
    median_h = hours_ok[len(hours_ok) // 2] if hours_ok else None
    p90 = ((hours_protection or {}).get("discount") or {}).get("p90")

    scored, frozen, containers = [], [], []
    discounted = []

    for t in tasks:
        if t.get("is_container"):
            containers.append({"task_id": t["task_id"], "task_name": t["task_name"],
                               "reason": t.get("parent_reason", "容器父任务：工时 ≈ 子任务之和")})
            continue

        comp = completeness(t, weights, denom)
        comp100 = completeness(t, weights, 100.0)
        s = subtotal(t, weights)
        kd, kd_ev = k_deviation(t)
        kv, kv_ev = k_volume(t, median_h)
        kr, kr_ev = k_role(t)
        ks, ks_ev = k_subtask(t, by_id)

        rec = {
            "task_id": t["task_id"],
            "task_name": t["task_name"],
            "completeness": round(comp, 4),
            "completeness_vs_100": round(comp100, 4),
            "layer": layer_of(comp),
            "subtotal": round(s, P.ROUND_DIGITS) if s is not None else None,
            "k_deviation": kd,
            "k_volume": kv,
            "k_role": kr,
            "k_subtask": ks,
            "valid_dims": valid_dims(t, weights),
            "flags": list(t.get("flags", [])),
        }
        if s is not None:
            k_total = kd * kv * kr * ks
            rec["k_total"] = round(k_total, 4)
            rec["points"] = (round(s * P.POINT_MULTIPLIER * k_total, P.ROUND_DIGITS)
                             if emit_points else None)
        else:
            rec["k_total"] = 0.0
            rec["points"] = None

        if s is None:
            rec["note"] = "无任何有效维度，按规则冻结（不填 0、不排名）"
            rec["rank_within_layer"] = None
            rec["rank_scope"] = "FROZEN-无有效维度"
            frozen.append(rec)
            continue

        # 被打折的任务单列，evidence 不得为空
        if kd < 1.0:
            base_pts = s * P.POINT_MULTIPLIER * kv * kr * ks
            rec_ev = {
                "task_id": t["task_id"],
                "task_name": t["task_name"],
                "original_hours": (kd_ev or {}).get("original_hours"),
                "p90_hours": p90,
                "effective_hours": (kd_ev or {}).get("effective_hours"),
                "k_deviation": kd,
                "subtotal": rec["subtotal"],
                "points_before_discount": round(base_pts, P.ROUND_DIGITS),
                "points_after_discount": rec["points"],
                "evidence": (f"原始工时 {(kd_ev or {}).get('original_hours')}h > 本批 P90 "
                             f"{p90}h；超 P90 部分按 {P.HOURS_DEVIATION_FACTOR:.0%} 计入 → "
                             f"h_eff={(kd_ev or {}).get('effective_hours')}h；"
                             f"K_偏离={kd}。小计 S 与分档仍用原始工时，未受打折影响。"),
            }
            discounted.append(rec_ev)
            rec["flags"].append("deviation_discounted")

        if ks_ev:
            rec["flags"].append("subtask_discounted")
        if kv_ev:
            rec["flags"].append("volume_adjusted")
        (scored if rec["layer"] in ("L1", "L2", "L3") else frozen).append(rec)

    # 层内排名（跨层不可比）
    for layer in ("L1", "L2", "L3"):
        group = [r for r in scored if r["layer"] == layer]
        group.sort(key=lambda r: -r["subtotal"])
        for i, r in enumerate(group, 1):
            r["rank_within_layer"] = i
            r["rank_scope"] = f"{layer}({len(group)}条)"

    l1_l2 = [r for r in scored if r["layer"] in ("L1", "L2")]
    sum_l1l2 = round(sum(r["subtotal"] for r in l1_l2), P.ROUND_DIGITS)
    sum_all = round(sum(r["subtotal"] for r in scored), P.ROUND_DIGITS)
    pts_l1l2 = round(sum(r["points"] or 0 for r in l1_l2), P.ROUND_DIGITS)
    pts_all = round(sum(r["points"] or 0 for r in scored), P.ROUND_DIGITS)

    summary = {
        "n_scored": len(scored),
        "n_l1": sum(1 for r in scored if r["layer"] == "L1"),
        "n_l2": sum(1 for r in scored if r["layer"] == "L2"),
        "n_l3": sum(1 for r in scored if r["layer"] == "L3"),
        "n_out": len(frozen),          # 无任何有效维度，冻结
        "n_container": len(containers),
        "n_discounted": len(discounted),
        # 主口径（裁定①）：总分 = L1 + L2，L3 数据不足不参与分配
        "total_score_L1_L2": sum_l1l2,
        "total_points_L1_L2": pts_l1l2,
        # 参考口径：含 L3 —— 只作对照，不建议纳入分配
        "total_score_with_l3": sum_all,
        "total_points_with_l3": pts_all,
        "l3_in_total": P.INCLUDE_L3_IN_TOTAL,
        "points_emitted": emit_points,
        "points_forced": bool(force_points and branch in ("D_DEGENERATE", "C_DESCRIPTIVE")),
        "points_suppressed_reason": (None if emit_points else
                                     f"本批落入 {branch} 分支，按规则不输出工分"),
        "completeness_denom": round(denom, 2),
        "completeness_note": (f"完整度分母 = 本批启用维度权重和 {round(denom, 2)}"
                             f"（非固定 100）；completeness_vs_100 为对照值"),
        "layer_rule": "L1 ≥90% / L2 60%–90% / L3 <60%（两刀）",
        "median_hours": round(median_h, 2) if median_h else None,
        "p90_hours": p90,
    }
    if P.INCLUDE_L3_IN_TOTAL:
        summary["total_score"] = sum_all
        summary["total_points"] = pts_all
    else:
        summary["total_score"] = sum_l1l2
        summary["total_points"] = pts_l1l2

    return {
        "tasks": scored + frozen,
        "ranked_tasks": scored,
        "frozen_tasks": frozen,
        "container_tasks": containers,
        "discounted_tasks": discounted,
        "summary": summary,
    }
