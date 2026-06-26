#!/usr/bin/env python3
"""
像素素材处理脚本 — 将AI生成的sprite sheet处理为Godot可用格式
功能：去背景 → 切帧 → NEAREST缩放 → 输出sprite sheet + 单帧PNG
"""

import argparse
import os
import sys
from pathlib import Path
from collections import Counter

try:
    from PIL import Image
except ImportError:
    print("错误：需要 Pillow，请运行 pip install Pillow")
    sys.exit(1)


def detect_bg_color(img: Image.Image) -> tuple:
    """采样四角像素，取众数作为背景色"""
    w, h = img.size
    corners = [img.getpixel((0, 0)), img.getpixel((w - 1, 0)),
               img.getpixel((0, h - 1)), img.getpixel((w - 1, h - 1))]
    # 取RGB（忽略alpha）
    corners_rgb = [c[:3] if len(c) >= 3 else c for c in corners]
    return Counter(corners_rgb).most_common(1)[0][0]


def remove_background(img: Image.Image, bg_color: tuple, tolerance: int = 30) -> Image.Image:
    """将接近背景色的像素设为透明"""
    img = img.convert("RGBA")
    r, g, b = bg_color[:3]
    pixels = img.load()
    w, h = img.size

    for y in range(h):
        for x in range(w):
            pr, pg, pb, pa = pixels[x, y]
            if abs(pr - r) <= tolerance and abs(pg - g) <= tolerance and abs(pb - b) <= tolerance:
                pixels[x, y] = (pr, pg, pb, 0)

    return img


def find_content_bounds(img: Image.Image) -> tuple:
    """找到非透明区域的边界 (left, top, right, bottom)"""
    img = img.convert("RGBA")
    bbox = img.getbbox()  # 返回非透明区域的bbox
    if bbox is None:
        print("警告：整张图都是透明的，无法检测内容边界")
        return (0, 0, img.width, img.height)
    return bbox


def detect_grid(img: Image.Image, cols: int | None = None) -> tuple:
    """
    自动检测网格布局，返回 (cols, rows)
    通过扫描每行/列的透明像素来找到分割线
    """
    img_gray = img.convert("RGBA")
    w, h = img_gray.size
    pixels = img_gray.load()

    # 统计每列和每行的非透明像素数
    col_nonempty = []
    for x in range(w):
        has_content = any(pixels[x, y][3] > 0 for y in range(h))
        col_nonempty.append(1 if has_content else 0)

    row_nonempty = []
    for y in range(h):
        has_content = any(pixels[x, y][3] > 0 for x in range(w))
        row_nonempty.append(1 if has_content else 0)

    # 找到空白列/行作为分割线
    def count_splits(line):
        splits = 0
        in_gap = False
        for v in line:
            if v == 0 and not in_gap:
                in_gap = True
                splits += 1
            elif v == 1:
                in_gap = False
        return max(splits, 1)

    if cols is None:
        cols = count_splits(col_nonempty)
    rows = count_splits(row_nonempty)

    return cols, rows


def main():
    parser = argparse.ArgumentParser(
        description="处理AI生成的sprite sheet为Godot可用格式",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python process_sprite_sheet.py input.png --output-dir ./out --target-size 48 --cols 4
  python process_sprite_sheet.py input.png --bg-color white --target-size 32
  python process_sprite_sheet.py input.png --no-remove-bg
        """)
    parser.add_argument("input", help="输入图片路径（AI生成的sprite sheet）")
    parser.add_argument("--output-dir", "-o", default="./output",
                        help="输出目录（默认: ./output）")
    parser.add_argument("--target-size", "-s", type=int, default=48,
                        help="每帧目标尺寸（正方形，默认: 48）")
    parser.add_argument("--cols", "-c", type=int, default=None,
                        help="列数（帧数，默认自动检测）")
    parser.add_argument("--rows", "-r", type=int, default=None,
                        help="行数（默认自动检测）")
    parser.add_argument("--bg-color", choices=["white", "black", "auto"],
                        default="auto", help="背景色（默认: auto自动检测）")
    parser.add_argument("--bg-tolerance", type=int, default=30,
                        help="去背景容差（0-255，默认: 30）")
    parser.add_argument("--no-remove-bg", action="store_true",
                        help="不去除背景")
    parser.add_argument("--no-single-frames", action="store_true",
                        help="不输出单帧PNG")
    parser.add_argument("--no-spritesheet", action="store_true",
                        help="不输出横排sprite sheet")
    parser.add_argument("--padding", type=int, default=2,
                        help="帧间间距（sprite sheet用，默认: 2）")

    args = parser.parse_args()

    # 验证输入
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"错误：文件不存在: {args.input}")
        sys.exit(1)

    # 加载图片
    print(f"📷 加载图片: {args.input}")
    img = Image.open(input_path)
    print(f"   尺寸: {img.width}x{img.height}, 模式: {img.mode}")

    # 创建输出目录
    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    frames_dir = out_dir / "frames"
    frames_dir.mkdir(exist_ok=True)

    # 确定背景色
    bg_color = None
    if not args.no_remove_bg:
        if args.bg_color == "auto":
            bg_color = detect_bg_color(img)
            print(f"🎨 检测到背景色: RGB{bg_color}")
        elif args.bg_color == "white":
            bg_color = (255, 255, 255)
        elif args.bg_color == "black":
            bg_color = (0, 0, 0)

    # 去背景
    if bg_color and not args.no_remove_bg:
        print("✂️  去除背景...")
        img = remove_background(img, bg_color, args.bg_tolerance)

    # 裁剪到内容区域
    bbox = find_content_bounds(img)
    if bbox != (0, 0, img.width, img.height):
        print(f"📐 裁剪内容区域: {bbox}")
        img = img.crop(bbox)

    # 检测网格
    cols, rows = detect_grid(img, args.cols)
    if args.rows:
        rows = args.rows
    print(f"📊 网格布局: {cols}列 x {rows}行 ({cols * rows}帧)")

    # 计算每帧尺寸
    content_w, content_h = img.size
    # 计算帧宽高（去除分割间距）
    # 先扫描找到实际分割线位置
    def split_positions(line_sum, total_len):
        """根据某轴的非空统计找到分割位置"""
        positions = [0]
        in_gap = False
        gap_start = 0
        for i in range(total_len):
            if not in_gap and line_sum[i] == 0:
                in_gap = True
                gap_start = i
            elif in_gap and line_sum[i] == 1:
                in_gap = False
                # 取间距中间作为分割点
                mid = (gap_start + i) // 2
                positions.append(mid)
        positions.append(total_len)
        return positions

    # 简单方案：直接均分内容区域
    frame_w = content_w // cols
    frame_h = content_h // rows

    # 切割帧
    frames = []
    for row in range(rows):
        for col in range(cols):
            left = col * frame_w
            top = row * frame_h
            frame = img.crop((left, top, left + frame_w, top + frame_h))
            frames.append(frame)

    print(f"🧩 切割完成: {len(frames)}帧, 原始帧尺寸: {frame_w}x{frame_h}")

    # NEAREST缩放到目标尺寸
    target = args.target_size
    if frame_w != target or frame_h != target:
        print(f"🔍 NEAREST缩放: {frame_w}x{frame_h} → {target}x{target}")
        # 先判断是否为非正方形帧，保持比例缩放
        if frame_w != frame_h:
            scale = target / min(frame_w, frame_h)
            new_w = int(frame_w * scale)
            new_h = int(frame_h * scale)
        else:
            new_w = new_h = target

        scaled_frames = []
        for f in frames:
            scaled = f.resize((new_w, new_h), Image.NEAREST)
            scaled_frames.append(scaled)
        frames = scaled_frames
        frame_w, frame_h = new_w, new_h
    else:
        print(f"   尺寸已是 {target}x{target}，无需缩放")

    # 输出单帧
    stem = input_path.stem
    if not args.no_single_frames:
        print(f"💾 输出单帧到: {frames_dir}/")
        for i, f in enumerate(frames):
            frame_path = frames_dir / f"{stem}_frame_{i:02d}.png"
            f.save(frame_path)

    # 输出横排sprite sheet
    if not args.no_spritesheet:
        padding = args.padding
        sheet_w = frame_w * len(frames) + padding * (len(frames) - 1)
        sheet_h = frame_h
        sheet = Image.new("RGBA", (sheet_w, sheet_h), (0, 0, 0, 0))

        for i, f in enumerate(frames):
            x = i * (frame_w + padding)
            sheet.paste(f, (x, 0))

        sheet_path = out_dir / f"{stem}_spritesheet.png"
        sheet.save(sheet_path)
        print(f"💾 输出sprite sheet: {sheet_path}")
        print(f"   尺寸: {sheet_w}x{sheet_h}, Godot设置: hframes={len(frames)}")

    print(f"\n✅ 完成！输出目录: {out_dir.resolve()}")


if __name__ == "__main__":
    main()
