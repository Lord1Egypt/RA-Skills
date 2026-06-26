from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps


SKILL_DIR = Path(__file__).resolve().parents[1]
ASSET_DIR = SKILL_DIR / "assets"
LOGO_PATH = ASSET_DIR / "icon-small.jpg"

WIDTH = 960
HEIGHT = 540
BG = "#FAF8F4"
TEXT = "#1F1F1F"
MUTED = "#666666"
ACCENT = "#B71F1F"
ACCENT_SOFT = "#F8E8E8"
CARD = "#FFFFFF"
BORDER = "#E7E1DA"
SOFT = "#F3EEE8"


@dataclass(frozen=True)
class DemoSpec:
    output: Path
    language: str
    title: str
    subtitle: str
    chips: tuple[str, str]
    cards: list[tuple[str, str, str]]
    footer_prefix: str
    footer_suffix: str
    footer_lines: list[list[str]]
    right_badge: str
    right_caption: str


def load_font(size: int, language: str, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    if language == "zh":
        candidates = [
            "/System/Library/Fonts/Hiragino Sans GB.ttc",
            "/System/Library/Fonts/STHeiti Medium.ttc",
            "/System/Library/Fonts/STHeiti Light.ttc",
            "/System/Library/Fonts/Supplemental/Songti.ttc",
            "/System/Library/Fonts/Supplemental/Arial Unicode.ttf",
        ]
    else:
        candidates = [
            "/System/Library/Fonts/Supplemental/Arial Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Arial.ttf",
            "/System/Library/Fonts/Supplemental/Arial Unicode.ttf",
            "/System/Library/Fonts/Arial.ttf",
        ]

    for candidate in candidates:
        path = Path(candidate)
        if path.exists():
            try:
                return ImageFont.truetype(str(path), size=size)
            except OSError:
                continue

    return ImageFont.load_default()


def rounded_box(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], fill: str, outline: str, radius: int = 24, width: int = 2) -> None:
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def draw_centered_text(draw: ImageDraw.ImageDraw, xy: tuple[int, int], text: str, font, fill: str) -> None:
    bbox = draw.textbbox((0, 0), text, font=font)
    w = bbox[2] - bbox[0]
    h = bbox[3] - bbox[1]
    draw.text((xy[0] - w / 2, xy[1] - h / 2), text, font=font, fill=fill)


def chip(draw: ImageDraw.ImageDraw, xy: tuple[int, int], text: str, fill: str, text_fill: str, font) -> int:
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    pad_x = 16
    pad_y = 9
    x, y = xy
    draw.rounded_rectangle((x, y, x + tw + pad_x * 2, y + th + pad_y * 2), radius=999, fill=fill)
    draw.text((x + pad_x, y + pad_y - 1), text, font=font, fill=text_fill)
    return x + tw + pad_x * 2


def add_lines(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], lines: list[str], font, fill: str, line_gap: int = 8) -> None:
    x1, y1, x2, y2 = box
    y = y1
    for line in lines:
        draw.text((x1, y), line, font=font, fill=fill)
        bbox = draw.textbbox((0, 0), line, font=font)
        y += (bbox[3] - bbox[1]) + line_gap
        if y > y2:
            break


def make_frame(spec: DemoSpec, step: int, focus: int) -> Image.Image:
    title_font = load_font(42, spec.language, bold=True)
    subtitle_font = load_font(20, spec.language)
    body_font = load_font(24, spec.language)
    small_font = load_font(16, spec.language)
    label_font = load_font(18, spec.language, bold=True)

    img = Image.new("RGB", (WIDTH, HEIGHT), BG)
    draw = ImageDraw.Draw(img)

    draw.rectangle((0, 0, WIDTH, 12), fill=ACCENT)
    draw.rectangle((0, HEIGHT - 14, WIDTH, HEIGHT), fill=SOFT)

    logo = Image.open(LOGO_PATH).convert("RGB")
    logo = ImageOps.contain(logo, (170, 170))
    img.paste(logo, (44, 34))

    draw.text((238, 44), spec.title, font=title_font, fill=TEXT)
    draw.text((238, 98), spec.subtitle, font=subtitle_font, fill=MUTED)

    cx = 238
    cy = 138
    cx = chip(draw, (cx, cy), spec.chips[0], ACCENT_SOFT, ACCENT, small_font) + 10
    chip(draw, (cx, cy), spec.chips[1], "#F0F0F0", TEXT, small_font)

    cards = spec.cards
    start_x = 40
    gap = 20
    card_w = 205
    card_h = 120
    y = 240

    for idx, (num, label, desc) in enumerate(cards):
        x = start_x + idx * (card_w + gap)
        active = idx == focus
        card_y = y - 8 if active else y
        fill = ACCENT_SOFT if active else CARD
        outline = ACCENT if active else BORDER
        rounded_box(draw, (x, card_y, x + card_w, card_y + card_h), fill=fill, outline=outline, radius=24, width=3 if active else 2)

        draw.ellipse((x + 18, card_y + 18, x + 50, card_y + 50), fill=ACCENT if active else SOFT, outline=None)
        draw_centered_text(draw, (x + 34, card_y + 35), num, label_font, "#FFFFFF" if active else TEXT)

        draw.text((x + 64, card_y + 18), label, font=label_font, fill=TEXT)
        draw.text((x + 18, card_y + 64), desc, font=small_font, fill=MUTED)

    connector_y = y + 62
    for idx in range(3):
        x1 = start_x + (idx + 1) * card_w + idx * gap + 8
        x2 = x1 + gap - 16
        draw.line((x1, connector_y, x2, connector_y), fill=BORDER, width=6)
        draw.polygon([(x2, connector_y), (x2 - 10, connector_y - 8), (x2 - 10, connector_y + 8)], fill=BORDER)

    rounded_box(draw, (40, 385, 920, 505), fill=CARD, outline=BORDER, radius=28, width=2)
    draw.text((68, 408), f"{spec.footer_prefix}{step + 1}{spec.footer_suffix}", font=small_font, fill=ACCENT)
    add_lines(draw, (68, 434, 860, 490), spec.footer_lines[step], body_font, TEXT)

    draw.rounded_rectangle((760, 408, 890, 454), radius=999, fill=SOFT, outline=None)
    draw.text((792, 416), spec.right_badge, font=label_font, fill=ACCENT)
    draw.text((760, 468), spec.right_caption, font=small_font, fill=MUTED)

    return img


def build_specs() -> list[DemoSpec]:
    english = DemoSpec(
        output=ASSET_DIR / "demo.gif",
        language="en",
        title="JD Scorecard Skill",
        subtitle="Turn a job post into a usable hiring rubric.",
        chips=("Public skill", "Private product"),
        cards=[
            ("1", "Paste JD", "Role, location, must-haves"),
            ("2", "Scorecard", "Filters, weights, thresholds"),
            ("3", "Questions", "10-minute screening call"),
            ("4", "Shortlist", "Reject, review, recommend"),
        ],
        footer_prefix="Step ",
        footer_suffix="",
        footer_lines=[
            ["Start with the JD text.", "The skill extracts role signals, filters, and exclusions."],
            ["Must-haves become filters.", "Nice-to-haves stay non-blocking."],
            ["Questions test real work.", "They help catch resume inflation."],
            ["Red flags are explicit.", "Recruiters can reject faster."],
            ["Same scorecard, same standard.", "Less debate, faster decision."],
        ],
        right_badge="60 sec",
        right_caption="From JD to shortlist",
    )

    chinese = DemoSpec(
        output=ASSET_DIR / "demo-zh.gif",
        language="zh",
        title="JD 评分卡 Skill",
        subtitle="把招聘 JD 快速变成可执行的筛选标准。",
        chips=("公开版", "私有版"),
        cards=[
            ("1", "粘贴 JD", "岗位、地点、必须项"),
            ("2", "生成评分卡", "筛选条件、权重、阈值"),
            ("3", "面试问题", "10 分钟筛选提问"),
            ("4", "进入 shortlist", "拒绝、复核、推荐"),
        ],
        footer_prefix="第",
        footer_suffix="步",
        footer_lines=[
            ["先贴 JD。", "系统会提取岗位信号、筛选条件和淘汰项。"],
            ["必须项变成 filters。", "加分项保持非阻塞。"],
            ["问题直接问到工作。", "帮你快速识别简历灌水。"],
            ["红旗显式提示。", "HR 可以更快做决定。"],
            ["同一套评分卡，同一标准。", "少争论，快 shortlist。"],
        ],
        right_badge="60 秒",
        right_caption="从 JD 到 shortlist",
    )

    return [english, chinese]


def main() -> None:
    for spec in build_specs():
        frames = [make_frame(spec, step, min(step, 3)) for step in range(5)]
        frames[0].save(
            spec.output,
            save_all=True,
            append_images=frames[1:],
            duration=900,
            loop=0,
            optimize=True,
            disposal=2,
        )
        print(f"Wrote {spec.output}")


if __name__ == "__main__":
    main()
