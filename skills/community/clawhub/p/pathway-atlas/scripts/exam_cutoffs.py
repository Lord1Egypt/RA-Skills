"""Deterministic score calibration from comparable exam/gaokao cutoff pairs."""
from __future__ import annotations

import math


def estimate_cutoff_score(score, pairs, maximum, margin_points=10):
    """Interpolate inside anchors; use nearby line difference otherwise.

    Margins are disclosed planning assumptions, not measured prediction errors.
    Callers establish provenance and comparable full-score/subject contexts.
    """
    points = sorted(pairs)
    values = [score, maximum, margin_points, *(v for pair in points for v in pair)]
    if any(type(v) not in (int, float) or not math.isfinite(v) for v in values):
        raise ValueError("cutoff values must be finite numbers")
    if not 0 < maximum <= 900 or not 0 <= score <= maximum or not 5 <= margin_points <= 100:
        raise ValueError("cutoff score or margin is outside its range")
    if any(not 0 <= value <= maximum for pair in points for value in pair):
        raise ValueError("cutoff exceeds the comparable full score")
    if any(b[0] <= a[0] or b[1] <= a[1] for a, b in zip(points, points[1:])):
        raise ValueError("cutoff pairs must increase strictly in both scores")
    if not points:
        return None
    if len(points) >= 2 and points[0][0] <= score <= points[-1][0]:
        left, right = next((a, b) for a, b in zip(points, points[1:]) if a[0] <= score <= b[0])
        center = left[1] + (score - left[0]) * (right[1] - left[1]) / (right[0] - left[0])
        method = "相邻对应划线插值"
        used = [left, right]
    else:
        near = min(points, key=lambda point: abs(point[0] - score))
        if abs(score - near[0]) > maximum * 0.15:
            return None
        center = near[1] + score - near[0]
        margin_points = max(20, margin_points)
        method = "单线线差法" if len(points) == 1 else "区间外就近线差法（有限外推）"
        used = [near]
    if not 0 <= center <= maximum:
        return None
    return {"score": round(center, 1),
            "score_bounds": [round(max(0, center - margin_points), 1),
                             round(min(maximum, center + margin_points), 1)],
            "calculation": method, "used_pairs": used, "margin_points": margin_points}


def rank_at_score(score, rows):
    """Return cumulative rank and whether interpolation, not an exact row, was used."""
    points = sorted((value, rank) for rank, value in rows)
    for value, rank in points:
        if value == score:
            return (round(rank), False) if rank > 0 else (None, False)
    for (s0, r0), (s1, r1) in zip(points, points[1:]):
        if s0 < score < s1 and r0 > 0 and r1 > 0:
            return round(r0 + (score - s0) * (r1 - r0) / (s1 - s0)), True
    return None, False
