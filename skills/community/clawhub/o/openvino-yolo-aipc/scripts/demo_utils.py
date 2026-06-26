from __future__ import annotations

import cv2
import numpy as np


def draw_panel(frame: np.ndarray, lines: list[str], anchor: str = "top-right") -> None:
    font = cv2.FONT_HERSHEY_SIMPLEX
    scale = 0.65
    thickness = 2
    padding = 12
    line_gap = 10
    sizes = [cv2.getTextSize(line, font, scale, thickness)[0] for line in lines]
    panel_width = max(size[0] for size in sizes) + padding * 2
    panel_height = sum(size[1] for size in sizes) + line_gap * (len(lines) - 1) + padding * 2

    if anchor == "top-right":
        x1 = frame.shape[1] - panel_width - 18
        y1 = 18
    elif anchor == "bottom-left":
        x1 = 18
        y1 = frame.shape[0] - panel_height - 18
    else:
        x1 = 18
        y1 = 18

    x2 = x1 + panel_width
    y2 = y1 + panel_height
    overlay = frame.copy()
    cv2.rectangle(overlay, (x1, y1), (x2, y2), (20, 20, 20), -1)
    cv2.addWeighted(overlay, 0.65, frame, 0.35, 0, frame)

    y = y1 + padding
    for line, size in zip(lines, sizes):
        y += size[1]
        cv2.putText(frame, line, (x1 + padding, y), font, scale, (245, 245, 245), thickness, cv2.LINE_AA)
        y += line_gap
