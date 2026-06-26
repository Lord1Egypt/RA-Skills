"""版面分析：多栏阅读顺序重建。

当前实现：双栏检测 + 重排。算法：
  1. 把页面 block 的 x 中心聚成两簇（k-means k=2 等价的中点切分）
  2. 若两簇质心间距 > 页宽的 ``col_gap_ratio``，且每簇 ≥ ``min_blocks_per_col``，
     视为双栏；否则保持原序（单栏）
  3. 双栏：先按 top_y 输出左栏，再输出右栏
"""
from __future__ import annotations

from typing import Any


def _x_center(bbox) -> float:
    return (bbox[0] + bbox[2]) / 2


def detect_two_columns(
    blocks: list[dict[str, Any]],
    page_width: float,
    left_band_ratio: float = 0.40,
    right_band_ratio: float = 0.60,
    min_blocks_per_col: int = 4,
) -> tuple[list[dict], list[dict]] | None:
    """若识别为双栏，返回 (left_blocks, right_blocks)；否则返回 None。

    判据（严格化，避免误判）：
      1) 必须同时存在"左栏"（x_center < left_band_ratio × page_width）和
         "右栏"（x_center > right_band_ratio × page_width）的 block
      2) 每栏至少 min_blocks_per_col 个 block
      3) 中间带（页面中心附近）的 block 数不超过两栏之和的 30%——否则更像
         单栏（正文居中、短标题各自居中导致 x_center 分散）
    """
    if len(blocks) < min_blocks_per_col * 2:
        return None
    left_x = page_width * left_band_ratio
    right_x = page_width * right_band_ratio
    left, right, middle = [], [], []
    for b in blocks:
        cx = _x_center(b["source_bbox"])
        if cx < left_x:
            left.append(b)
        elif cx > right_x:
            right.append(b)
        else:
            middle.append(b)
    if len(left) < min_blocks_per_col or len(right) < min_blocks_per_col:
        return None
    if len(middle) > 0.3 * (len(left) + len(right)):
        return None
    return left, right


def reorder_reading_order(
    blocks: list[dict[str, Any]],
    page_width: float,
) -> list[dict[str, Any]]:
    """对单页 blocks 重排阅读顺序。识别为双栏则左→右，否则按 top_y。"""
    two = detect_two_columns(blocks, page_width)
    if two is None:
        return sorted(blocks, key=lambda b: (b["source_bbox"][1], b["source_bbox"][0]))
    left, right = two
    left.sort(key=lambda b: b["source_bbox"][1])
    right.sort(key=lambda b: b["source_bbox"][1])
    return left + right
