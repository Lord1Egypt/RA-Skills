"""风格画廊 — 把同一张 YAML/Mermaid 规格用全部 10 种风格渲染成一张对比图。

用法
====

    # 通过 CLI
    python3 scripts/create-flow-chart.py -i spec.yaml --gallery -o /tmp/gallery.png

    # 直接调用
    python3 scripts/gallery.py -i spec.yaml -o /tmp/gallery.png
    python3 scripts/gallery.py -i spec.yaml -o /tmp/gallery.png \
        --cols 3 --styles modern,dark,minimal,ocean,forest,xiaohongshu

拼接逻辑：每个风格单独渲染成 PNG，按网格贴到一张大图上，每格上方打上风格名。
"""
from __future__ import annotations

import argparse
import sys
import tempfile
from pathlib import Path
from typing import List, Optional

sys.path.insert(0, str(Path(__file__).parent))

from flowchart_core import parse, to_mermaid, to_plantuml, to_dot, FlowChart  # noqa: E402
from flowchart_render import render  # noqa: E402
from styles import get_style, list_styles, to_mermaid_init_directive, to_plantuml_skinparam  # noqa: E402


def _pick_engine(fc: FlowChart) -> str:
    if fc.diagram_type in ("swimlane", "plantuml_raw"):
        return "plantuml"
    if fc.diagram_type == "dot_raw":
        return "dot"
    return "mermaid"


def _render_one(fc: FlowChart, style, out_path: str, scale: float = 2.5) -> str:
    engine = _pick_engine(fc)
    if engine == "mermaid":
        src = to_mermaid(
            fc,
            to_mermaid_init_directive(style, diagram_type=fc.diagram_type),
            style=style,
        )
    elif engine == "plantuml":
        src = to_plantuml(fc, to_plantuml_skinparam(style))
    else:
        src = to_dot(fc, style=style)
    return render(src, out_path, engine=engine, background=style.background,
                   scale=scale)


def build_gallery(spec_path: str, out_path: str,
                   styles: Optional[List[str]] = None,
                   cols: int = 3,
                   cell_width: int = 720,
                   padding: int = 36,
                   title_font_size: int = 28,
                   label_font_size: int = 20) -> str:
    """把一张规格渲染成 10 种风格的对比图。"""
    from PIL import Image, ImageDraw, ImageFont

    fc = parse(spec_path)

    # 要渲染的风格列表
    if styles:
        style_keys = [s.strip() for s in styles if s.strip()]
    else:
        style_keys = list(list_styles().keys())

    tmp = Path(tempfile.mkdtemp(prefix="huo15-gallery-"))
    rendered: List[tuple] = []   # [(key, name, png_path)]
    for key in style_keys:
        try:
            style = get_style(key)
        except Exception as e:
            print(f"[warn] 跳过 {key}: {e}", file=sys.stderr)
            continue
        png = tmp / f"{key}.png"
        try:
            _render_one(fc, style, str(png))
            rendered.append((key, style.name, str(png)))
        except Exception as e:
            print(f"[warn] {key} 渲染失败: {e}", file=sys.stderr)

    if not rendered:
        raise RuntimeError("没有任何风格成功渲染")

    # 等比缩放到 cell_width
    imgs = []
    max_h = 0
    for key, name, path in rendered:
        im = Image.open(path).convert("RGBA")
        ratio = cell_width / im.width
        new_h = int(im.height * ratio)
        im = im.resize((cell_width, new_h), Image.LANCZOS)
        imgs.append((key, name, im))
        max_h = max(max_h, new_h)

    # 每格尺寸
    cell_h = max_h + int(label_font_size * 1.8)
    n = len(imgs)
    rows = (n + cols - 1) // cols

    # 大图尺寸（留出顶部标题）
    title_h = int(title_font_size * 2.2)
    W = cols * cell_width + (cols + 1) * padding
    H = title_h + rows * cell_h + (rows + 1) * padding
    canvas = Image.new("RGB", (W, H), "#FFFFFF")
    draw = ImageDraw.Draw(canvas)

    # 字体
    font = _load_font(title_font_size)
    font_small = _load_font(label_font_size)

    title = "huo15-flow-chart Style Gallery"
    try:
        bbox = draw.textbbox((0, 0), title, font=font)
        tw = bbox[2] - bbox[0]
    except Exception:
        tw = len(title) * title_font_size // 2
    draw.text(((W - tw) // 2, padding // 2), title,
              fill="#0F172A", font=font)

    for idx, (key, name, im) in enumerate(imgs):
        r = idx // cols
        c = idx % cols
        x = padding + c * (cell_width + padding)
        y = title_h + padding + r * (cell_h + padding)
        # 底色（轻灰卡片）
        card_pad = 12
        draw.rectangle(
            [x - card_pad // 2, y - card_pad // 2,
             x + cell_width + card_pad // 2, y + cell_h + card_pad // 2],
            fill="#FAFAFA", outline="#E5E7EB", width=1,
        )
        label = f"{name}  ·  {key}"
        try:
            bbox = draw.textbbox((0, 0), label, font=font_small)
            lw = bbox[2] - bbox[0]
        except Exception:
            lw = len(label) * label_font_size // 2
        draw.text((x + (cell_width - lw) // 2, y),
                  label, fill="#1E293B", font=font_small)
        # 图像居中
        img_y = y + int(label_font_size * 1.5)
        img_x = x + (cell_width - im.width) // 2
        canvas.paste(im, (img_x, img_y), im)

    canvas.save(out_path)
    return out_path


def _load_font(size: int):
    """加载字体，优先中文字体。"""
    from PIL import ImageFont
    candidates = [
        "/System/Library/Fonts/PingFang.ttc",
        "/System/Library/Fonts/Hiragino Sans GB.ttc",
        "/System/Library/Fonts/Helvetica.ttc",
        "C:/Windows/Fonts/msyh.ttc",
        "C:/Windows/Fonts/msyhbd.ttc",
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
    ]
    for p in candidates:
        if Path(p).exists():
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                continue
    return ImageFont.load_default()


def main() -> int:
    ap = argparse.ArgumentParser(description="huo15-flow-chart 风格画廊（同图 10 风格对比）")
    ap.add_argument("--input", "-i", required=True)
    ap.add_argument("--output", "-o", required=True, help=".png 路径")
    ap.add_argument("--styles", default="", help="风格清单（逗号分隔），默认全部 10 种")
    ap.add_argument("--cols", type=int, default=3)
    ap.add_argument("--cell-width", type=int, default=720)
    args = ap.parse_args()

    styles = [s for s in args.styles.split(",") if s.strip()] if args.styles else None
    try:
        path = build_gallery(args.input, args.output, styles=styles, cols=args.cols,
                              cell_width=args.cell_width)
        print(f"✓ {path}")
        return 0
    except Exception as e:
        print(f"[错误] {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
