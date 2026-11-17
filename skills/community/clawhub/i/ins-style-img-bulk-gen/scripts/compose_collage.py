"""
2x2 / 3x3 宫格拼图工具 (ins-style-img-bulk-gen)

把多张同尺寸图片拼成 1 张宫格图，用于 cover 模式的 2x2 / 3x3 拼图。
支持可选的间隙（gap）和背景色。

Usage:
    python compose_collage.py -i a.jpg d.jpg c.jpg d.jpg -o out.jpg
    python compose_collage.py -i *.jpg -o out.jpg --layout 3x2 --gap 24 --bg 245,240,232

默认 layout = 2x2（cover 模式硬性要求）。

⚠️ 2026-09-20 迭代：默认 cell 比例 = 小红书标准 3:4 竖图
    - 4 张 cell 先 resize 到 3:4（默认），再拼成 2x2 → 输出整体仍是 ~3:4
    - 输出尺寸默认 1080x1440（小红书 cover 标准），可通过 --target-size 覆盖
"""
import argparse
from pathlib import Path
from PIL import Image


# 小红书默认输出尺寸：1080x1440 (3:4) cover 标准
DEFAULT_TARGET_W = 1080
DEFAULT_TARGET_H = 1440
# 小红书默认 cell 比例：3:4 竖图（与 cover 一致）
DEFAULT_CELL_ASPECT = "3:4"


def _parse_aspect(s):
    """'3:4' / '4:3' / '1:1' / '16:9' -> (w, h) tuple of floats."""
    s = str(s).strip()
    if ":" in s:
        a, b = s.split(":", 1)
        return float(a), float(b)
    if "x" in s.lower():
        a, b = s.lower().split("x", 1)
        return float(a), float(b)
    raise ValueError(f"--cell-aspect 格式错误: {s}（用 W:H 如 3:4）")


def _resize_cell_to_aspect(img, aspect_w, aspect_h):
    """把 cell 图片 resize 成给定比例（保持比例，居中裁剪）。"""
    w, h = img.size
    cur_ratio = w / h
    target_ratio = aspect_w / aspect_h

    if abs(cur_ratio - target_ratio) < 0.01:
        # 比例已经接近，直接用
        return img

    if cur_ratio > target_ratio:
        # 当前更宽 → 按高裁剪两侧
        new_w = int(h * target_ratio)
        left = (w - new_w) // 2
        return img.crop((left, 0, left + new_w, h))
    else:
        # 当前更窄 → 按宽裁剪上下
        new_h = int(w / target_ratio)
        top = (h - new_h) // 2
        return img.crop((0, top, w, top + new_h))


def compose_grid(images, layout="2x2", gap=24, bg=(245, 240, 232),
                 cell_aspect=DEFAULT_CELL_ASPECT, target_size=None):
    """把 images 拼成 layout 网格的宫格图。

    Args:
        images: 4/6/9/... 张同尺寸图片（路径或 PIL.Image）
        layout: "2x2" / "3x3" / "2x3" / "3x2"（rows x cols）
        gap: 宫格之间的像素间隙（0 = 无缝拼接）
        bg: 间隙的背景色 (R, G, B)
        cell_aspect: 每个 cell 的目标比例，默认 "3:4"（小红书标准）
                     输入图片会被居中裁剪到该比例
        target_size: (w, h) 最终输出目标尺寸；如果给出，最后把整张图 resize 过去
                     默认 None → 保持按 cell 实际尺寸拼出的自然尺寸
                     设为 (1080, 1440) → 小红书标准 cover

    Returns:
        PIL.Image: 拼好的宫格图
    """
    rows, cols = (int(x) for x in layout.lower().split("x"))
    n = rows * cols
    if len(images) != n:
        raise ValueError(
            f"layout={layout} 需要 {n} 张图，实际给了 {len(images)} 张"
        )

    # 路径 → PIL
    imgs = [Image.open(p) if isinstance(p, (str, Path)) else p for p in images]

    # 1. 把每张图按 cell_aspect 居中裁剪
    aspect_w, aspect_h = _parse_aspect(cell_aspect)
    imgs = [_resize_cell_to_aspect(im, aspect_w, aspect_h) for im in imgs]

    # 2. 以第一张为基准尺寸（裁剪后已经同比例），统一 resize
    target_w, target_h = imgs[0].size
    imgs = [im.resize((target_w, target_h)) for im in imgs]

    # 3. 总尺寸
    out_w = cols * target_w + (cols - 1) * gap
    out_h = rows * target_h + (rows - 1) * gap

    canvas = Image.new("RGB", (out_w, out_h), bg)

    for idx, im in enumerate(imgs):
        r = idx // cols
        c = idx % cols
        x = c * (target_w + gap)
        y = r * (target_h + gap)
        canvas.paste(im, (x, y))

    # 4. 如指定 target_size，最后 resize 到目标尺寸
    if target_size is not None:
        tw, th = target_size
        canvas = canvas.resize((tw, th), Image.LANCZOS)

    return canvas


def main():
    p = argparse.ArgumentParser(description="宫格拼图工具")
    p.add_argument("-i", "--inputs", nargs="+", required=True,
                   help="输入图片路径（按 左上→右上→左下→右下 顺序）")
    p.add_argument("-o", "--output", required=True, help="输出宫格图路径")
    p.add_argument("--layout", default="2x2", help="网格布局，默认 2x2")
    p.add_argument("--gap", type=int, default=24, help="间隙像素，默认 24")
    p.add_argument("--bg", default="245,240,232",
                   help="间隙背景色 R,G,B，默认 245,240,232（暖白，与 INS 色调一致）")
    p.add_argument("--cell-aspect", default=DEFAULT_CELL_ASPECT,
                   help=f"cell 目标比例 W:H，默认 {DEFAULT_CELL_ASPECT}（小红书标准竖图）"
                        f"；输入图按此比例居中裁剪")
    p.add_argument("--target-size", default=None,
                   help=f"最终输出尺寸 WxH，如 1080x1440（小红书 cover 标准）；"
                        f"默认不缩放（保持拼图自然尺寸）")
    args = p.parse_args()

    bg = tuple(int(x) for x in args.bg.split(","))
    if len(bg) != 3:
        raise ValueError("--bg 必须是 R,G,B 三个 0-255 整数，用逗号分隔")

    target_size = None
    if args.target_size:
        try:
            tw, th = args.target_size.lower().split("x")
            target_size = (int(tw), int(th))
        except Exception:
            raise ValueError("--target-size 必须是 WxH 格式，如 1080x1440")

    canvas = compose_grid(
        args.inputs, args.layout, args.gap, bg,
        cell_aspect=args.cell_aspect, target_size=target_size,
    )
    canvas.save(args.output)
    print(
        f"OK: {args.layout} 宫格 ({len(args.inputs)} 图) → {args.output}  |  "
        f"cell 比例 {args.cell_aspect}  |  输出尺寸 {canvas.size[0]}x{canvas.size[1]}px  |  "
        f"gap {args.gap}px  |  bg {bg}"
    )


if __name__ == "__main__":
    main()
