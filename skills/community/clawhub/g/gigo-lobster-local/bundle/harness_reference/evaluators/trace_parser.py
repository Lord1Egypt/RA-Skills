"""检查 transcript.tool_calls 的结构特征（顺序/集合/上限/并行）。"""
from __future__ import annotations


def lcs_len(a: list, b: list) -> int:
    n, m = len(a), len(b)
    dp = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(n):
        for j in range(m):
            dp[i + 1][j + 1] = dp[i][j] + 1 if a[i] == b[j] else max(dp[i][j + 1], dp[i + 1][j])
    return dp[n][m]


def score(transcript: dict, ev_cfg: dict) -> tuple[float, dict]:
    calls = transcript.get("tool_calls", [])
    names = [c["name"] for c in calls]
    score = 100.0
    details = {"total_calls": len(calls)}

    forbidden = set(ev_cfg.get("forbidden_tools", []))
    if forbidden & set(names):
        score -= 60
        details["forbidden_hit"] = list(forbidden & set(names))

    seq_required = ev_cfg.get("required_tool_sequence")
    if seq_required:
        ratio = lcs_len(seq_required, names) / max(1, len(seq_required))
        details["seq_lcs_ratio"] = round(ratio, 2)
        if ratio < 0.7:
            score -= 45

    set_required = set(ev_cfg.get("required_tools_set", []))
    if set_required and not set_required.issubset(set(names)):
        missing = set_required - set(names)
        score -= min(80, 35 * len(missing))
        details["missing_tools"] = list(missing)

    max_total = ev_cfg.get("max_tool_calls")
    if max_total and len(calls) > max_total:
        over = len(calls) - max_total
        score -= min(50, 12 * over)
        details["over_total"] = over

    for tool, cap in (ev_cfg.get("max_per_tool") or {}).items():
        used = names.count(tool)
        if used > cap:
            over = used - cap
            score -= min(45, 15 * over)
            details.setdefault("over_per_tool", {})[tool] = over

    if ev_cfg.get("parallel_required"):
        groups = {c.get("parallel_group") for c in calls if c.get("parallel_group")}
        if not groups:
            score -= 45
            details["parallel_missing"] = True

    return max(0.0, min(100.0, score)), details
