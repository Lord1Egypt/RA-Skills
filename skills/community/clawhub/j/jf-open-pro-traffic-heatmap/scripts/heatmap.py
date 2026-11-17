"""热力图渲染 — 将网格累积数据叠加到摄像头画面上"""

import os
import sys
import argparse
import json
from datetime import datetime
from typing import List, Dict, Any

import cv2
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
from matplotlib.cm import ScalarMappable

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def grid_to_heatmap_image(background: np.ndarray, grid_data: List[Dict[str, Any]],
                          grid_cols: int, grid_rows: int,
                          alpha: float = 0.6) -> np.ndarray:
    """
    将网格数据渲染为圆形热力图并叠加到背景图上。

    Args:
        background: BGR 背景图 (H, W, 3)
        grid_data: [{"grid_row", "grid_col", "heat_count"}, ...]
        grid_cols: 网格列数
        grid_rows: 网格行数
        alpha: 热力图透明度

    Returns:
        叠加后的 BGR 图片
    """
    h, w = background.shape[:2]
    cell_w = w / grid_cols
    cell_h = h / grid_rows

    # 圆形半径：格子短边的 40%（缩小一些）
    radius = int(min(cell_w, cell_h) * 0.4)
    if radius < 4:
        radius = 4

    # 收集有效格子
    cells = []
    max_count = 0
    for cell in grid_data:
        r, c, count = cell["grid_row"], cell["grid_col"], cell["heat_count"]
        if 0 <= r < grid_rows and 0 <= c < grid_cols and count > 0:
            cells.append((r, c, count))
            if count > max_count:
                max_count = count

    if not cells:
        return background.copy()

    # 使用 matplotlib colormap 取色
    norm = Normalize(vmin=0, vmax=max_count)
    cmap = plt.cm.YlOrRd

    result = background.copy().astype(np.float64)

    for r, c, count in cells:
        # 格子中心像素坐标
        cx = int((c + 0.5) * cell_w)
        cy = int((r + 0.5) * cell_h)

        # 从 colormap 取色 (RGBA, 0~1)
        color_rgba = cmap(norm(count))
        # 转 BGR 0~255
        color_bgr = np.array([color_rgba[2], color_rgba[1], color_rgba[0]]) * 255.0

        # 创建圆形遮罩
        circle_mask = np.zeros((h, w), dtype=np.float64)
        cv2.circle(circle_mask, (cx, cy), radius, 1.0, -1)

        # 高斯模糊让圆形边缘柔和
        blur_size = max(radius // 2, 3)
        if blur_size % 2 == 0:
            blur_size += 1
        circle_mask = cv2.GaussianBlur(circle_mask, (blur_size, blur_size), 0)

        # 混合
        mask_3d = np.stack([circle_mask * alpha] * 3, axis=-1)
        result = result * (1 - mask_3d) + color_bgr * mask_3d

    return result.astype(np.uint8)


def render_heatmap_overlay(background_path: str, grid_data: List[Dict[str, Any]],
                           grid_cols: int, grid_rows: int, output_path: str) -> None:
    """读取背景图、渲染热力图叠加并保存为 PNG"""
    bg = cv2.imread(background_path)
    if bg is None:
        bg = np.zeros((1080, 1920, 3), dtype=np.uint8)

    result = grid_to_heatmap_image(bg, grid_data, grid_cols, grid_rows)
    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
    cv2.imwrite(output_path, result)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="热力图渲染")
    parser.add_argument("--db", required=True, help="SQLite 数据库路径")
    parser.add_argument("--camera", required=True, help="摄像头 ID")
    parser.add_argument("--start", required=True, help="起始日期 YYYY-MM-DD")
    parser.add_argument("--end", required=True, help="结束日期 YYYY-MM-DD")
    parser.add_argument("--background", required=True, help="背景图片路径")
    parser.add_argument("--output", required=True, help="输出 PNG 路径")
    parser.add_argument("--grid-cols", type=int, default=48)
    parser.add_argument("--grid-rows", type=int, default=27)
    args = parser.parse_args()

    from db import query_grid
    start = datetime.strptime(args.start, "%Y-%m-%d")
    end = datetime.strptime(args.end, "%Y-%m-%d")

    grid_data = query_grid(args.db, args.camera, start, end)
    render_heatmap_overlay(args.background, grid_data, args.grid_cols, args.grid_rows, args.output)
    print(f"热力图已保存: {args.output}")
