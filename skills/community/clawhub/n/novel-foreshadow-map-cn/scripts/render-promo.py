#!/usr/bin/env python3
"""Create the deterministic Chinese promo layout from the generated illustration."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = Path(__file__).resolve().parent.parent


def font(size: int):
    """Load an installed CJK-capable font without relying on a host file path."""
    for family in (
        "PingFang SC",
        "Hiragino Sans GB",
        "Noto Sans CJK SC",
        "Microsoft YaHei",
        "Arial Unicode MS",
    ):
        try:
            return ImageFont.truetype(family, size)
        except OSError:
            continue
    return ImageFont.load_default()


source = Image.open(ROOT / "assets/icon-source.png").convert("RGB")
canvas = Image.new("RGB", (1600, 900), "#f7f2e7")
art = source.resize((780, 780), Image.Resampling.LANCZOS)
mask = Image.new("L", art.size, 0)
md = ImageDraw.Draw(mask)
md.rounded_rectangle((18, 18, 762, 762), radius=72, fill=255)
art.putalpha(mask.filter(ImageFilter.GaussianBlur(1)))
canvas.paste(art, (800, 60), art)
draw = ImageDraw.Draw(canvas)
regular = font(28)
bold = font(92)
identity = font(31)
small = font(25)
ink, muted, red = "#5a1720", "#5e6261", "#a42b32"
draw.text((98, 110), "小说创作 · 连续性修订", font=regular, fill=ink)
draw.line((98, 157, 430, 157), fill=red, width=4)
draw.text((94, 238), "伏笔\n回收清单", font=bold, fill=ink, spacing=6)
draw.text((100, 488), "NOVEL FORESHADOW MAP", font=identity, fill=ink)
draw.multiline_text((100, 552), "把线索的埋点、兑现与\n回收位置，一次理清。", font=small, fill=muted, spacing=12)
draw.text((100, 780), "一个章节，一张可执行的线索表", font=small, fill=muted)
canvas.save(ROOT / "assets/promo-1600x900.png", "PNG", optimize=True)
