from __future__ import annotations

import math

import cv2
import numpy as np

from . import common


PROFILE_NAME = "white-plastic-or-paper"


def is_profile(warped: np.ndarray) -> bool:
    return estimate_score(warped) >= 1.0


def estimate_score(warped: np.ndarray) -> float:
    hsv = cv2.cvtColor(warped, cv2.COLOR_BGR2HSV)
    median_saturation = float(np.median(hsv[:, :, 1]))
    bright_low_saturation = float(((hsv[:, :, 2] > 170) & (hsv[:, :, 1] < 70)).mean())
    return 1.0 if median_saturation < 65.0 and bright_low_saturation > 0.35 else 0.0


def classify_intersections(warped: np.ndarray, xfit, yfit, board_size: int) -> list[list[str]]:
    gray = cv2.cvtColor(warped, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(cv2.GaussianBlur(gray, (3, 3), 0), 25, 70)

    def classify_cell(features: common.IntersectionFeatures) -> str:
        return classify_white_plastic_cell(features, edges)

    return common.classify_intersections(warped, xfit, yfit, board_size, classify_cell)


def classify_white_plastic_cell(features: common.IntersectionFeatures, edges: np.ndarray) -> str:
    outline_coverage, outline_axis_share = circular_outline_score(edges, features.x, features.y, features.cell)
    white_outline_ok = outline_coverage > 0.42 and outline_axis_share < 0.74
    is_outer_grid_line = (
        features.row in {0, features.board_size - 1}
        or features.col in {0, features.board_size - 1}
    )
    white_ok = (
        not is_outer_grid_line
        and (
            (
                features.bright_fraction > 0.72
                and features.mean_v > 210.0
                and features.mean_s < 70.0
                and features.center_low_sat > 0.94
                and features.center_dark_fraction < 0.08
                and (features.edge_contrast > -2.0 or white_outline_ok)
            )
            or (
                white_outline_ok
                and features.edge_contrast > 14.0
                and features.white_core > 0.65
                and features.bright_fraction > 0.70
                and features.center_dark_fraction < 0.10
                and features.mean_s < 70.0
            )
        )
    )
    black_ok = features.dark_fraction > 0.55 or (
        features.mean_v < 95.0 and features.dark_fraction > 0.42
    )

    if black_ok:
        return "B"
    if white_ok:
        return "W"
    return "."


def circular_outline_score(edges: np.ndarray, x: float, y: float, cell: float) -> tuple[float, float]:
    inner = cell * 0.32
    outer = cell * 0.54
    margin = int(math.ceil(outer + 2.0))
    height, width = edges.shape[:2]
    x0 = max(0, int(round(x - margin)))
    x1 = min(width, int(round(x + margin + 1)))
    y0 = max(0, int(round(y - margin)))
    y1 = min(height, int(round(y + margin + 1)))
    if x1 <= x0 or y1 <= y0:
        return 0.0, 1.0

    yy, xx = np.mgrid[y0:y1, x0:x1]
    dx = xx - x
    dy = yy - y
    distance = np.sqrt(dx * dx + dy * dy)
    annulus = (distance >= inner) & (distance <= outer)
    edge_mask = (edges[y0:y1, x0:x1] > 0) & annulus
    if int(edge_mask.sum()) < 8:
        return 0.0, 1.0

    bins = 24
    angles = np.arctan2(dy[edge_mask], dx[edge_mask])
    indexes = ((angles + np.pi) / (2 * np.pi) * bins).astype(int)
    indexes = np.clip(indexes, 0, bins - 1)
    counts = np.bincount(indexes, minlength=bins)
    covered = float((counts >= 2).sum()) / float(bins)

    axis_mask = np.zeros(bins, dtype=bool)
    for axis_bin in (0, bins // 4, bins // 2, 3 * bins // 4, bins - 1):
        for delta in (-1, 0, 1):
            axis_mask[(axis_bin + delta) % bins] = True
    axis_share = float(counts[axis_mask].sum()) / float(max(1, counts.sum()))
    return covered, axis_share


def assess_recognition(black_stones: int, white_stones: int) -> tuple[list[str], bool]:
    warnings = [
        "White plastic/paper board detected; white-stone recognition is low confidence and should be verified before analysis."
    ]
    warnings.extend(common.suspicious_white_count_warning(black_stones, white_stones))
    return warnings, False
