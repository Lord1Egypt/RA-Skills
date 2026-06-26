"""
quantize: AI 出图 (或原图) -> grid.json + quantized.png

流程:
  1. 缩放到 grid_w × grid_h, 用 PIL.LANCZOS 抗锯齿。
  2. 每格取像素 (单格已经是 1x1, 直接读 RGB)。
  3. RGB -> Lab, 对色板每色算 CIEDE2000 ΔE, 取最小 (逐像素 snap, 不聚类)。
  4. forbid_colors / palette_subset 提前过滤候选集。
  5. 如果 max_colors 设了: 数频次取 top-K, 不在 top-K 的色板色再 snap 进 top-K (色板色 → 色板色)。
  6. must_include_colors 检查: 缺哪个就找 ΔE 最大的格子强制替换 (粗糙版, 仅占位)。
  7. 写 grid.json + 渲染 quantized.png (每格一个色块, 还没有网格线 / 色号 / BOM, 那是 render 干的)。

usage:
    python scripts/quantize.py \\
        --spec outputs/run/spec.json \\
        --image outputs/run/ai_pixel.png \\
        --palette palettes/mard_221.csv \\
        --out-dir outputs/run/
"""

import argparse
import csv
import json
from collections import Counter
from pathlib import Path
from typing import Optional

import numpy as np
from PIL import Image
from scipy.ndimage import label
from skimage import color as skcolor


def load_palette(csv_path: Path) -> list[dict]:
    rows: list[dict] = []
    with csv_path.open("r", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            rows.append({
                "id": int(row["id"]),
                "code": row["code"],
                "hex": row["hex"],
                "rgb": np.array([int(row["r"]), int(row["g"]), int(row["b"])], dtype=np.float64),
                "series": row.get("series", ""),
                "name_zh": row.get("name_zh", ""),
                "name_en": row.get("name_en", ""),
            })
    if not rows:
        raise ValueError(f"empty palette: {csv_path}")
    return rows


def filter_palette(
    palette: list[dict],
    subset: Optional[list[str]],
    forbid: Optional[list[str]],
) -> list[dict]:
    out = palette
    if subset:
        s = set(subset)
        out = [c for c in out if c["code"] in s]
    if forbid:
        f = set(forbid)
        out = [c for c in out if c["code"] not in f]
    if not out:
        raise ValueError("palette became empty after subset/forbid filtering")
    return out


def rgb_to_lab(rgb_uint8: np.ndarray) -> np.ndarray:
    """rgb_uint8: (..., 3) uint8 -> Lab float."""
    arr = rgb_uint8.astype(np.float64) / 255.0
    # skimage expects [..., 3] in [0,1]
    return skcolor.rgb2lab(arr)


def nearest_palette_idx(query_lab: np.ndarray, palette_lab: np.ndarray) -> np.ndarray:
    """
    query_lab: (N, 3), palette_lab: (P, 3)
    returns: (N,) int index into palette.
    Uses CIEDE2000 from skimage; fallback to euclidean Lab distance if unavailable.
    """
    # skimage.color.deltaE_ciede2000 expects matched shapes; we tile.
    q = query_lab[:, None, :]  # (N, 1, 3)
    p = palette_lab[None, :, :]  # (1, P, 3)
    # broadcast to (N, P, 3)
    q_b = np.broadcast_to(q, (q.shape[0], p.shape[1], 3))
    p_b = np.broadcast_to(p, (q.shape[0], p.shape[1], 3))
    de = skcolor.deltaE_ciede2000(q_b, p_b)  # (N, P)
    return np.argmin(de, axis=1)


def downsample(img: Image.Image, gw: int, gh: int) -> np.ndarray:
    """Resize to grid size with anti-alias. Returns (gh, gw, 3) uint8."""
    if img.mode != "RGB":
        img = img.convert("RGB")
    small = img.resize((gw, gh), Image.LANCZOS)
    return np.array(small, dtype=np.uint8)


def downsample_grid_aware(
    img: Image.Image, gw: int, gh: int, inset: float = 0.25
) -> np.ndarray:
    """
    AI 出图自带网格线 + 假设网格严格 gw×gh 等大时使用: 在每格中央取中位数。

    缺点: 如果 AI 实际画的格数不是 gw×gh (常见, AI 不严格守 prompt 格数),
    每个 patch 会跨多个 AI 格, 中位数变成相邻格混色 — 改用 downsample_by_detected_grid。
    """
    if img.mode != "RGB":
        img = img.convert("RGB")
    arr = np.array(img, dtype=np.uint8)
    H_src, W_src, _ = arr.shape
    cell_w = W_src / gw
    cell_h = H_src / gh

    out = np.zeros((gh, gw, 3), dtype=np.uint8)
    for r in range(gh):
        for c in range(gw):
            y0 = int(r * cell_h + cell_h * inset)
            y1 = int((r + 1) * cell_h - cell_h * inset)
            x0 = int(c * cell_w + cell_w * inset)
            x1 = int((c + 1) * cell_w - cell_w * inset)
            if y1 <= y0:
                y1 = y0 + 1
            if x1 <= x0:
                x1 = x0 + 1
            patch = arr[y0:y1, x0:x1, :].reshape(-1, 3)
            out[r, c, :] = np.median(patch, axis=0).astype(np.uint8)
    return out


def detect_grid_lines(
    img_arr: np.ndarray,
    axis: int,
    bg_strip_width: int = 80,
    grey_low: int = 170,
    grey_high: int = 245,
    grey_chroma_max: int = 12,
    line_frac_threshold: float = 0.4,
) -> list[float]:
    """
    在图像背景区 (白底 strip) 上找 AI 画的浅灰网格线位置。

    axis=1: 找垂直网格线, 在顶部 strip 沿水平方向 scan, 返回 x 坐标列表
    axis=0: 找水平网格线, 在右侧 strip 沿垂直方向 scan, 返回 y 坐标列表

    判定一个像素是网格线: RGB 三通道都在 [grey_low, grey_high] 且通道间 std < grey_chroma_max
    (即近灰色, 不是彩色)。一行/一列里 grey 占比 > line_frac_threshold 视为网格线候选。

    最后把连续的网格线候选 (相距 ≤ 2 像素) 聚成一段, 取中心点。
    """
    H, W, _ = img_arr.shape
    if axis == 1:
        strip = img_arr[:bg_strip_width, :, :]   # (sh, W, 3)
        scan_axis = 0
    else:
        strip = img_arr[:, W - bg_strip_width:, :]   # (H, sw, 3)
        scan_axis = 1

    s_min = strip.min(axis=-1)
    s_max = strip.max(axis=-1)
    is_grey_pixel = (
        (s_min >= grey_low) & (s_max <= grey_high) & (s_max - s_min <= grey_chroma_max)
    )
    frac = is_grey_pixel.mean(axis=scan_axis)
    is_line = frac > line_frac_threshold
    line_idx = np.where(is_line)[0]
    if len(line_idx) == 0:
        return []

    diffs = np.diff(line_idx)
    splits = np.where(diffs > 2)[0]
    starts = np.concatenate([[line_idx[0]], line_idx[splits + 1]])
    ends = np.concatenate([line_idx[splits], [line_idx[-1]]])
    centers = (starts + ends) / 2.0
    return [float(x) for x in centers]


def downsample_by_detected_grid(
    img: Image.Image, inset: float = 0.25
) -> tuple[np.ndarray, int, int]:
    """
    检测 AI 画的真实网格, 按真实网格切, 每格中央取中位数。无降采样混色损失。

    流程:
      1. detect_grid_lines 找出竖/横网格线在原图的位置
      2. 边界补齐 (如果第一/最后一条线不靠图边)
      3. 每相邻两条网格线之间是一个 "格", 取该格中间 (1 - 2*inset) 区域中位数

    返回 (rgb_grid, gw, gh): rgb_grid 形状 (gh, gw, 3), gw/gh 是检测到的实际格数。
    """
    if img.mode != "RGB":
        img = img.convert("RGB")
    arr = np.array(img, dtype=np.uint8)
    H_src, W_src, _ = arr.shape

    v_lines = detect_grid_lines(arr, axis=1)
    h_lines = detect_grid_lines(arr, axis=0)
    if len(v_lines) < 2 or len(h_lines) < 2:
        raise RuntimeError(
            f"detect_grid: too few lines (vertical={len(v_lines)}, horizontal={len(h_lines)}). "
            "AI 可能没画清楚网格线。换张图或回退 downsample_grid_aware。"
        )

    if v_lines[0] > 5:
        v_lines = [0.0] + v_lines
    if v_lines[-1] < W_src - 5:
        v_lines = v_lines + [float(W_src - 1)]
    if h_lines[0] > 5:
        h_lines = [0.0] + h_lines
    if h_lines[-1] < H_src - 5:
        h_lines = h_lines + [float(H_src - 1)]

    gw = len(v_lines) - 1
    gh = len(h_lines) - 1
    out = np.zeros((gh, gw, 3), dtype=np.uint8)
    for r in range(gh):
        y_top, y_bot = h_lines[r], h_lines[r + 1]
        cell_h = y_bot - y_top
        y0 = int(y_top + cell_h * inset)
        y1 = int(y_bot - cell_h * inset)
        if y1 <= y0:
            y1 = y0 + 1
        for c in range(gw):
            x_left, x_right = v_lines[c], v_lines[c + 1]
            cell_w = x_right - x_left
            x0 = int(x_left + cell_w * inset)
            x1 = int(x_right - cell_w * inset)
            if x1 <= x0:
                x1 = x0 + 1
            patch = arr[y0:y1, x0:x1, :].reshape(-1, 3)
            out[r, c, :] = np.median(patch, axis=0).astype(np.uint8)
    return out, gw, gh


def hex_to_rgb_array(hex_str: str) -> np.ndarray:
    h = hex_str.lstrip("#")
    return np.array([int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)], dtype=np.uint8)


def detect_bg_and_pure_fg_masks(
    grid_rgb: np.ndarray, bg_hex: str, threshold_de: float = 4.0
) -> tuple[np.ndarray, np.ndarray]:
    """
    把"接近 bg 颜色"的格子分成两类:
      - bg_mask: 真背景 = 从图像边界连通进来的近 bg 格子 (跳过, 不拼)
      - pure_fg_mask: 内部白窟窿 = 接近 bg 但被前景围起来的格子
                      (例如白猫脸上、胸口的纯白毛, 应该正常拼成"色板里最接近 bg 的那个豆")

    threshold_de=4 偏严: 略带奶白的毛 (ΔE ≈ 6-9) 不会进这两个 mask, 走正常 K-Means。
    """
    bg_rgb = hex_to_rgb_array(bg_hex)
    bg_lab = rgb_to_lab(bg_rgb.reshape(1, 1, 3))[0, 0]
    cell_lab = rgb_to_lab(grid_rgb)
    de = np.sqrt(np.sum((cell_lab - bg_lab) ** 2, axis=-1))
    near_bg = de < threshold_de  # (H, W) bool

    labeled, _ = label(near_bg)
    H, W = near_bg.shape
    border_labels: set[int] = set()
    border_labels.update(int(x) for x in labeled[0, :])
    border_labels.update(int(x) for x in labeled[-1, :])
    border_labels.update(int(x) for x in labeled[:, 0])
    border_labels.update(int(x) for x in labeled[:, -1])
    border_labels.discard(0)

    if border_labels:
        bg_mask = np.isin(labeled, list(border_labels))
    else:
        bg_mask = np.zeros_like(near_bg)
    pure_fg_mask = near_bg & ~bg_mask
    return bg_mask, pure_fg_mask


def palette_idx_of_color(palette: list[dict], hex_str: str) -> int:
    """色板里离 hex_str 最近的那个色 (CIEDE2000)。"""
    target_lab = rgb_to_lab(hex_to_rgb_array(hex_str).reshape(1, 1, 3))[0, 0]
    pal_lab = rgb_to_lab(np.stack([c["rgb"] for c in palette], axis=0).astype(np.uint8))
    return int(nearest_palette_idx(target_lab[None, :], pal_lab)[0])


def quantize_to_palette(
    grid_rgb: np.ndarray,
    palette: list[dict],
) -> np.ndarray:
    """直接逐像素 CIEDE2000 最近邻 (没有 K-Means 这一步)。grid_rgb: (H, W, 3) uint8 -> (H, W) int idx."""
    H, W, _ = grid_rgb.shape
    flat = grid_rgb.reshape(-1, 3)
    flat_lab = rgb_to_lab(flat)
    pal_lab = rgb_to_lab(np.stack([c["rgb"] for c in palette], axis=0).astype(np.uint8))
    idx = nearest_palette_idx(flat_lab, pal_lab)
    return idx.reshape(H, W)


def palette_first_topk(
    grid_rgb: np.ndarray,
    palette: list[dict],
    max_colors: int,
    fg_mask: Optional[np.ndarray] = None,
) -> np.ndarray:
    """
    "色板优先 + 频率截断"量化:固定色板场景下比 K-Means 更准。

    为什么不用 K-Means: K-Means 在 K=max_colors 个像素簇里求 Lab 平均得到
    簇心, 簇心通常落在"色板里两色之间", 再 snap 引第二层失真。本场景的
    具体例子: 猫毛 Lab≈(96,1,5) + 暗影虎斑 Lab≈(50,5,15) 合成簇心 (亮度
    中性灰) → snap 后既不是奶油也不是棕, 而是某个 a 接近 0 的中间色。

    本函数直接做:
      1. 每像素 CIEDE2000 → 全色板 (221 色) 最近邻;
      2. 数频次, 取 top max_colors;
      3. 不在 top-K 的色板色, 在 top-K 内 CIEDE2000 找最近, 像素重映射过去
         (色板色 → 色板色, 色板内 ΔE 通常 <8, 失真可控)。

    fg_mask: True 的像素参与量化; False 处 idx=0 (上层用 bg_mask 屏蔽显示)。
    """
    H, W, _ = grid_rgb.shape
    idx_full = quantize_to_palette(grid_rgb, palette)  # (H, W) idx into full palette

    if fg_mask is None:
        fg_mask = np.ones((H, W), dtype=bool)

    fg_idx = idx_full[fg_mask]
    counts = np.bincount(fg_idx, minlength=len(palette))
    nonzero_used = int((counts > 0).sum())

    out = np.zeros_like(idx_full)
    if nonzero_used <= max_colors:
        out[fg_mask] = idx_full[fg_mask]
        return out

    top_k = np.argsort(-counts)[:max_colors]               # (K,)
    top_set = set(int(x) for x in top_k)

    pal_lab = rgb_to_lab(np.stack([c["rgb"] for c in palette], axis=0).astype(np.uint8))
    top_k_lab = pal_lab[top_k]                              # (K, 3)

    remap = np.arange(len(palette))
    minor = [i for i in range(len(palette)) if i not in top_set and counts[i] > 0]
    if minor:
        minor_lab = pal_lab[minor]                          # (M, 3)
        minor_to_topk = nearest_palette_idx(minor_lab, top_k_lab)  # (M,) into top_k
        for m, t in zip(minor, minor_to_topk):
            remap[m] = int(top_k[int(t)])

    out[fg_mask] = remap[idx_full[fg_mask]]
    return out


def enforce_must_include(
    idx_grid: np.ndarray,
    palette: list[dict],
    must_codes: list[str],
) -> np.ndarray:
    if not must_codes:
        return idx_grid
    code_to_idx = {c["code"]: i for i, c in enumerate(palette)}
    present = set(palette[i]["code"] for i in np.unique(idx_grid))
    missing = [c for c in must_codes if c in code_to_idx and c not in present]
    if not missing:
        return idx_grid

    # for each missing code: find the cell whose Lab is closest to the missing color
    # and replace that single cell. (粗糙版 — 仅在没出现时作为兜底插入一个像素)
    H, W = idx_grid.shape
    cur_rgb = np.stack([palette[i]["rgb"] for i in idx_grid.ravel()], axis=0).astype(np.uint8)
    cur_lab = rgb_to_lab(cur_rgb)  # (H*W, 3)
    for code in missing:
        target_lab = rgb_to_lab(palette[code_to_idx[code]]["rgb"].astype(np.uint8)[None, :])[0]
        de = np.linalg.norm(cur_lab - target_lab, axis=1)
        cell = int(np.argmin(de))
        idx_grid.flat[cell] = code_to_idx[code]
        cur_lab[cell] = target_lab
    return idx_grid


def render_quantized_png(
    idx_grid: np.ndarray,
    palette: list[dict],
    cell_px: int,
    out_path: Path,
    bg_mask: Optional[np.ndarray] = None,
) -> None:
    """Plain blocky preview without grid lines / codes. Background cells stay white."""
    H, W = idx_grid.shape
    img = np.full((H, W, 3), 255, dtype=np.uint8)  # default white = bg
    for i, c in enumerate(palette):
        m = idx_grid == i
        if bg_mask is not None:
            m = m & ~bg_mask
        img[m] = c["rgb"].astype(np.uint8)
    full = Image.fromarray(img, "RGB").resize((W * cell_px, H * cell_px), Image.NEAREST)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    full.save(out_path)


def build_grid_json(
    idx_grid: np.ndarray,
    palette: list[dict],
    spec: dict,
    bg_mask: Optional[np.ndarray] = None,
) -> dict:
    H, W = idx_grid.shape
    if bg_mask is None:
        bg_mask = np.zeros((H, W), dtype=bool)
    cells: list[list] = []
    counts: Counter = Counter()
    for r in range(H):
        row_out: list = []
        for c in range(W):
            if bg_mask[r, c]:
                row_out.append(None)
            else:
                i = int(idx_grid[r, c])
                row_out.append(palette[i]["code"])
                counts[i] += 1
        cells.append(row_out)
    bom = []
    for i, c in sorted(counts.items(), key=lambda kv: -kv[1]):
        bom.append({
            "code": palette[i]["code"],
            "hex": palette[i]["hex"],
            "name_zh": palette[i]["name_zh"],
            "count": int(c),
        })
    bead_count = int(sum(counts.values()))
    bg_cells = int(bg_mask.sum())
    return {
        "spec_id": spec.get("spec_id", "unknown"),
        "palette_id": spec.get("palette_id", "mard_221"),
        "size": [W, H],
        "bead_count": bead_count,
        "bg_cells": bg_cells,
        "cells": cells,
        "bom": bom,
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--spec", required=True)
    ap.add_argument("--image", required=True, help="AI pixel image (or original)")
    ap.add_argument("--palette", required=True)
    ap.add_argument("--out-dir", required=True)
    args = ap.parse_args()

    spec = json.loads(Path(args.spec).read_text(encoding="utf-8"))
    palette_full = load_palette(Path(args.palette))
    palette = filter_palette(
        palette_full,
        spec.get("palette_subset"),
        spec.get("forbid_colors"),
    )

    img = Image.open(args.image)
    detect_grid = spec.get("detect_grid_from_image", False)
    if detect_grid:
        # AI 画了网格 + 我们 detect 真实位置 + 按真实格切。spec 里的 grid_w/grid_h
        # 仅作为给 AI 的"建议", detect 出的实际格数会覆盖它。
        grid_rgb, gw_detected, gh_detected = downsample_by_detected_grid(img)
        spec["grid_w"] = gw_detected
        spec["grid_h"] = gh_detected
        downsample_mode = (
            f"detected grid (AI 实际画了 {gw_detected} 列 × {gh_detected} 行 = "
            f"{gw_detected * gh_detected} 格)"
        )
    elif spec.get("ai_draws_grid", True):
        grid_rgb = downsample_grid_aware(img, spec["grid_w"], spec["grid_h"])
        downsample_mode = "grid-aware (median, assume strict gw×gh)"
    else:
        grid_rgb = downsample(img, spec["grid_w"], spec["grid_h"])
        downsample_mode = "LANCZOS resize"
    print(f"[quantize] downsample mode: {downsample_mode}")

    # 把 resize 后但还没 snap 色板的图存一份, 方便定位失真来源:
    # 如果 downsampled 看着已经走样了 -> 是采样/AI 出图本身的锅
    # 如果 downsampled 还行但 quantized 走样了 -> 是色板 snap 的锅
    out_dir_early = Path(args.out_dir)
    out_dir_early.mkdir(parents=True, exist_ok=True)
    cell_px_preview = spec.get("cell_px", 40)
    H_, W_, _ = grid_rgb.shape
    Image.fromarray(grid_rgb, "RGB").resize(
        (W_ * cell_px_preview, H_ * cell_px_preview), Image.NEAREST
    ).save(out_dir_early / "downsampled.png")
    print(f"[quantize] downsampled (sampled cells before palette snap) -> "
          f"{out_dir_early/'downsampled.png'}")

    bg_mask = None
    pure_fg_mask = None
    bg_hex = spec.get("background_color")
    if spec.get("background_mode") in ("solid", "remove") and bg_hex:
        bg_mask, pure_fg_mask = detect_bg_and_pure_fg_masks(grid_rgb, bg_hex)
        print(f"[quantize] bg (跳过): {int(bg_mask.sum())} cells | "
              f"内部白窟窿 (强制 snap 到色板纯色): {int(pure_fg_mask.sum())} cells")

    # 量化时排除 bg 格子和"内部白窟窿":前者根本不拼,后者下面单独 snap 到 H1
    quant_exclude = bg_mask
    if pure_fg_mask is not None:
        quant_exclude = (bg_mask | pure_fg_mask) if bg_mask is not None else pure_fg_mask
    fg_mask_quant = ~quant_exclude if quant_exclude is not None else None

    max_colors = spec.get("max_colors")
    if max_colors:
        idx_grid = palette_first_topk(
            grid_rgb, palette, int(max_colors), fg_mask=fg_mask_quant
        )
    else:
        idx_grid = quantize_to_palette(grid_rgb, palette)

    # 内部白窟窿强制 snap 到色板里离 bg_color 最近的那个色 (白底就是 H1)
    if pure_fg_mask is not None and pure_fg_mask.any() and bg_hex:
        bg_pal_idx = palette_idx_of_color(palette, bg_hex)
        idx_grid[pure_fg_mask] = bg_pal_idx

    idx_grid = enforce_must_include(idx_grid, palette, spec.get("must_include_colors") or [])

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    grid_json = build_grid_json(idx_grid, palette, spec, bg_mask=bg_mask)
    (out_dir / "grid.json").write_text(
        json.dumps(grid_json, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    render_quantized_png(idx_grid, palette, spec.get("cell_px", 40),
                         out_dir / "quantized.png", bg_mask=bg_mask)

    print(f"[quantize] grid -> {out_dir/'grid.json'}")
    print(f"[quantize] quantized.png -> {out_dir/'quantized.png'}")
    print(f"[quantize] {len(grid_json['bom'])} distinct colors; "
          f"{grid_json['bead_count']} beads (skipped {grid_json['bg_cells']} bg cells); "
          f"top 5: {[b['code'] for b in grid_json['bom'][:5]]}")


if __name__ == "__main__":
    main()
