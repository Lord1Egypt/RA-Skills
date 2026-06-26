"""
extract_svg: AI 出图 -> raw.svg (vision 阶段, 不做色板 snap)

grounding 思路 (借鉴 perler_grid_extract.py):
  1. 灰度 + adaptiveThreshold(INV) -> 网格线=1, 色块内部=0
     这一步是关键 — 它把规则网格线和图像主体的边分离, 主体的强边几乎消掉,
     投影只剩网格信号 (Sobel 投影做不到, 主体边会主导 row/col_signal)。
  2. binary 沿 axis 投影 -> 1D signal, 周期性峰就是格线位置。
  3. scipy.signal.find_peaks 找显著峰; 相邻峰距中位数 = cell 周期估计;
     再用 distance=period*0.6 重新精确定位每条线 (允许不等距)。
  4. 相邻两条线之间是一格, 中央 inset 区域取 RGB 中位数, 中位数抗抗锯齿。

写出每格一个 <rect fill="rgb(R,G,B)"> 的 SVG, 沿用 svg_to_grid.py 契约
(<g data-grid-w data-grid-h> + <rect data-row data-col fill>)。

不在这里做的事 (留给下游):
  - 色板 snap / max_colors / must_include  -> svg_to_grid + quantize
  - 背景跳过 / 内部白窟窿保护              -> quantize.detect_bg_and_pure_fg_masks
  - 色号标注 / BOM / pattern.png          -> render_pattern

usage:
    python scripts/extract_svg.py <ai_pixel.png> <out.svg> [--debug-dir <dir>]
"""

import argparse
from pathlib import Path

import cv2
import numpy as np
from scipy.signal import find_peaks


def detect_grid_lines(
    img_bgr: np.ndarray, debug_dir: Path | None = None
) -> tuple[list[float], list[float]]:
    """
    返回 (xs, ys): 垂直/水平网格线坐标列表 (升序, 浮点)。
    含图像最外两边 (0 和 W-1 / H-1) 时不强制补; xs/ys 由峰检测直接产出。
    """
    H, W = img_bgr.shape[:2]
    gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)

    # 自适应阈值 + INV: 局部偏暗的细线 (网格) -> 1, 局部均匀的色块内部 -> 0
    binary = cv2.adaptiveThreshold(
        gray, 1,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY_INV,
        blockSize=15, C=5,
    )

    row_proj = binary.sum(axis=1).astype(np.float32)  # (H,) 水平线响应
    col_proj = binary.sum(axis=0).astype(np.float32)  # (W,) 垂直线响应

    def estimate_period(proj: np.ndarray, min_period: int = 8) -> int | None:
        height = proj.mean() + 0.3 * proj.std()
        peaks, _ = find_peaks(proj, distance=min_period, height=height)
        if len(peaks) < 3:
            return None
        return int(np.median(np.diff(peaks)))

    period_x = estimate_period(col_proj) or 20
    period_y = estimate_period(row_proj) or 20

    xs_peaks, _ = find_peaks(
        col_proj,
        distance=max(5, int(period_x * 0.6)),
        height=col_proj.mean(),
    )
    ys_peaks, _ = find_peaks(
        row_proj,
        distance=max(5, int(period_y * 0.6)),
        height=row_proj.mean(),
    )
    xs = sorted(float(x) for x in xs_peaks)
    ys = sorted(float(y) for y in ys_peaks)

    if len(xs) < 2 or len(ys) < 2:
        raise RuntimeError(
            f"网格检测失败: xs={len(xs)} ys={len(ys)}. "
            "看 debug_dir/grid_lines.png, 或 adaptiveThreshold 的 blockSize/C 不合适."
        )

    diffs_x, diffs_y = np.diff(xs), np.diff(ys)
    cv_x = float(diffs_x.std() / diffs_x.mean())
    cv_y = float(diffs_y.std() / diffs_y.mean())
    print(
        f"[grid] xs={len(xs)} (Δ={diffs_x.mean():.2f}±{diffs_x.std():.2f}, CV={cv_x:.3f}) "
        f"| ys={len(ys)} (Δ={diffs_y.mean():.2f}±{diffs_y.std():.2f}, CV={cv_y:.3f})"
    )
    if cv_x > 0.1 or cv_y > 0.1:
        print("[grid] WARN: 间距方差较大 (CV>10%), 先看 grid_lines.png 校验")

    if debug_dir is not None:
        vis = img_bgr.copy()
        for x in xs:
            cv2.line(vis, (int(x), 0), (int(x), H - 1), (0, 0, 255), 1)
        for y in ys:
            cv2.line(vis, (0, int(y)), (W - 1, int(y)), (0, 255, 0), 1)
        cv2.imwrite(str(debug_dir / "grid_lines.png"), vis)

    return xs, ys


def sample_cells(
    img_bgr: np.ndarray,
    xs: list[float],
    ys: list[float],
    inset_ratio: float = 0.22,
    debug_dir: Path | None = None,
) -> np.ndarray:
    """
    每相邻两条网格线之间是一格, 中央 inset 区域取 RGB 中位数。
    返回 (gh, gw, 3) uint8 RGB.
    """
    gw, gh = len(xs) - 1, len(ys) - 1
    out = np.zeros((gh, gw, 3), dtype=np.uint8)
    sample_vis = img_bgr.copy() if debug_dir is not None else None

    for r in range(gh):
        y0, y1 = int(ys[r]), int(ys[r + 1])
        h = y1 - y0
        dy = max(1, int(round(h * inset_ratio)))
        for c in range(gw):
            x0, x1 = int(xs[c]), int(xs[c + 1])
            w = x1 - x0
            dx = max(1, int(round(w * inset_ratio)))
            patch = img_bgr[y0 + dy : y1 - dy, x0 + dx : x1 - dx]
            if patch.size == 0:
                continue
            bgr = np.median(patch.reshape(-1, 3), axis=0).astype(np.uint8)
            out[r, c] = bgr[::-1]  # BGR -> RGB
            if sample_vis is not None:
                cv2.rectangle(
                    sample_vis,
                    (x0 + dx, y0 + dy),
                    (x1 - dx, y1 - dy),
                    (0, 255, 255),
                    1,
                )

    if sample_vis is not None:
        cv2.imwrite(str(debug_dir / "cells.png"), sample_vis)

    return out


def grid_to_svg(grid_rgb: np.ndarray, cell_px: int) -> str:
    gh, gw, _ = grid_rgb.shape
    W, H = gw * cell_px, gh * cell_px
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
        f'viewBox="0 0 {W} {H}" shape-rendering="crispEdges">',
        f'<g data-grid-w="{gw}" data-grid-h="{gh}" data-cell-px="{cell_px}">',
    ]
    for r in range(gh):
        for c in range(gw):
            R, G, B = (int(v) for v in grid_rgb[r, c])
            x, y = c * cell_px, r * cell_px
            parts.append(
                f'<rect x="{x}" y="{y}" width="{cell_px}" height="{cell_px}" '
                f'fill="rgb({R},{G},{B})" data-row="{r}" data-col="{c}"/>'
            )
    parts.append("</g></svg>\n")
    return "\n".join(parts)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("src", type=Path)
    ap.add_argument("dst", type=Path, help="raw.svg")
    ap.add_argument("--cell_px", type=int, default=20)
    ap.add_argument("--inset", type=float, default=0.22)
    ap.add_argument(
        "--debug-dir",
        type=Path,
        default=None,
        help="dump grid_lines.png + cells.png 用于人眼校验 grounding",
    )
    args = ap.parse_args()

    img = cv2.imread(str(args.src))
    if img is None:
        raise FileNotFoundError(f"读不了图: {args.src}")
    H, W = img.shape[:2]
    print(f"[extract] {args.src} {W}x{H}")

    if args.debug_dir is not None:
        args.debug_dir.mkdir(parents=True, exist_ok=True)

    xs, ys = detect_grid_lines(img, debug_dir=args.debug_dir)
    grid_rgb = sample_cells(img, xs, ys, args.inset, debug_dir=args.debug_dir)
    gh, gw, _ = grid_rgb.shape
    print(f"[extract] grid {gw} x {gh} = {gw * gh} cells")

    args.dst.parent.mkdir(parents=True, exist_ok=True)
    args.dst.write_text(grid_to_svg(grid_rgb, args.cell_px), encoding="utf-8")
    print(f"[extract] raw.svg -> {args.dst}")


if __name__ == "__main__":
    main()
