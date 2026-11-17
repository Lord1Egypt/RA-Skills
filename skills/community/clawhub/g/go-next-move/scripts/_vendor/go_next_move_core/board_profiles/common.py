from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

import cv2
import numpy as np


@dataclass(frozen=True)
class IntersectionFeatures:
    row: int
    col: int
    board_size: int
    x: float
    y: float
    cell: float
    mean_v: float
    mean_s: float
    dark_fraction: float
    very_dark_fraction: float
    bright_fraction: float
    bright_low_sat: float
    white_core: float
    center_low_sat: float
    edge_contrast: float
    center_dark_fraction: float


CellClassifier = Callable[[IntersectionFeatures], str]


def classify_intersections(
    warped: np.ndarray,
    xfit,
    yfit,
    board_size: int,
    classify_cell: CellClassifier,
) -> list[list[str]]:
    hsv = cv2.cvtColor(warped, cv2.COLOR_BGR2HSV)
    gray = cv2.cvtColor(warped, cv2.COLOR_BGR2GRAY)
    size = warped.shape[0]
    cell = (xfit.spacing + yfit.spacing) / 2.0
    radius = max(8, int(cell * 0.36))
    board: list[list[str]] = []

    for row in range(board_size):
        y = yfit.offset + row * yfit.spacing
        cells = []
        for col in range(board_size):
            x = xfit.offset + col * xfit.spacing
            x0 = max(0, int(round(x - radius)))
            x1 = min(size, int(round(x + radius + 1)))
            y0 = max(0, int(round(y - radius)))
            y1 = min(size, int(round(y + radius + 1)))
            yy, xx = np.ogrid[y0:y1, x0:x1]
            distance2 = (xx - x) ** 2 + (yy - y) ** 2
            circle = distance2 <= radius**2
            center = distance2 <= (radius * 0.45) ** 2
            ring = (distance2 >= (radius * 0.58) ** 2) & circle
            patch_gray_full = gray[y0:y1, x0:x1]
            patch_hsv_full = hsv[y0:y1, x0:x1]
            patch_gray = patch_gray_full[circle]
            patch_hsv = patch_hsv_full[circle]
            if patch_gray.size == 0:
                cells.append(".")
                continue

            center_hsv = patch_hsv_full[center]
            ring_hsv = patch_hsv_full[ring]
            center_gray = patch_gray_full[center]
            if center_hsv.size and ring_hsv.size:
                center_low_sat = float((center_hsv[:, 1] < 65).mean())
                edge_contrast = float(center_hsv[:, 2].mean() - ring_hsv[:, 2].mean())
            else:
                center_low_sat = 0.0
                edge_contrast = 0.0

            features = IntersectionFeatures(
                row=row,
                col=col,
                board_size=board_size,
                x=x,
                y=y,
                cell=cell,
                mean_v=float(patch_hsv[:, 2].mean()),
                mean_s=float(patch_hsv[:, 1].mean()),
                dark_fraction=float((patch_gray < 82).mean()),
                very_dark_fraction=float((patch_gray < 55).mean()),
                bright_fraction=float((patch_gray > 165).mean()),
                bright_low_sat=float(((patch_hsv[:, 2] > 170) & (patch_hsv[:, 1] < 70)).mean()),
                white_core=float(((patch_hsv[:, 2] > 185) & (patch_hsv[:, 1] < 65)).mean()),
                center_low_sat=center_low_sat,
                edge_contrast=edge_contrast,
                center_dark_fraction=float((center_gray < 120).mean()) if center_gray.size else 1.0,
            )
            cells.append(classify_cell(features))
        board.append(cells)
    return board


def suspicious_white_count_warning(black_stones: int, white_stones: int) -> list[str]:
    if white_stones > max(70, black_stones * 2 + 20):
        return ["Suspicious white-stone count; verify recognition before using the position for analysis."]
    return []
