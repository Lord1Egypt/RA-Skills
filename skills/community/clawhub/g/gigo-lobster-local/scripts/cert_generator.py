from __future__ import annotations

import html
import math
import os
from pathlib import Path

try:
    import qrcode
except Exception:  # pragma: no cover - fallback is tested through runtime behavior
    qrcode = None

try:
    from PIL import Image, ImageDraw, ImageFilter, ImageFont
except Exception:  # pragma: no cover - fallback is tested through runtime behavior
    Image = None
    ImageDraw = None
    ImageFilter = None
    ImageFont = None

from .presentation import DIMENSION_PROFILE, build_public_metrics, certificate_serial

CERT_SIZE = (1200, 1600)

PAPER = (255, 248, 242, 255)
PAPER_PANEL = (255, 252, 249, 255)
NAVY = (34, 49, 79, 255)
SLATE = (131, 145, 170, 255)
SLATE_SOFT = (157, 167, 185, 255)
ACCENT = (242, 76, 84, 255)
ACCENT_LINE = (248, 204, 199, 255)
ACCENT_SOFT = (255, 241, 227, 255)
TAG_FILL = (246, 248, 252, 255)
CARD_FILL = (255, 255, 255, 255)
CARD_SOFT = (247, 249, 253, 255)
SVG_SANS = "'Noto Sans CJK SC','PingFang SC','Microsoft YaHei','Segoe UI',sans-serif"
SVG_MONO = "'JetBrains Mono','Cascadia Mono','SFMono-Regular','Menlo','Consolas',monospace"
CJK_FONT_CANDIDATES = (
    *tuple(filter(None, (os.environ.get("GIGO_CJK_FONT_PATH", "").strip(),))),
    "C:/Windows/Fonts/msyh.ttc",
    "C:/Windows/Fonts/msyhbd.ttc",
    "C:/Windows/Fonts/simhei.ttf",
    "C:/Windows/Fonts/simsun.ttc",
    "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
    "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.otf",
    "/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc",
    "/usr/share/fonts/truetype/noto/NotoSansSC-Regular.otf",
    "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc",
    "/System/Library/Fonts/PingFang.ttc",
    "/System/Library/Fonts/STHeiti Light.ttc",
    "/System/Library/Fonts/STHeiti Medium.ttc",
    "/Library/Fonts/Arial Unicode.ttf",
)


def _svg_escape(value: str) -> str:
    return html.escape(value, quote=True)


def _svg_radar_points(center: tuple[int, int], radius: int, dimensions: dict[str, int]) -> tuple[str, str]:
    order = ["meat", "brain", "claw", "shell", "soul", "cost", "speed"]
    outline_points: list[str] = []
    fill_points: list[str] = []
    for index, key in enumerate(order):
        angle = -math.pi / 2 + index * (2 * math.pi / len(order))
        outer_x = center[0] + radius * math.cos(angle)
        outer_y = center[1] + radius * math.sin(angle)
        outline_points.append(f"{outer_x:.1f},{outer_y:.1f}")
        score_radius = radius * (dimensions.get(key, 0) / 100)
        fill_x = center[0] + score_radius * math.cos(angle)
        fill_y = center[1] + score_radius * math.sin(angle)
        fill_points.append(f"{fill_x:.1f},{fill_y:.1f}")
    return " ".join(outline_points), " ".join(fill_points)


def supports_png_certificate() -> bool:
    return all(module is not None for module in (qrcode, Image, ImageDraw, ImageFilter, ImageFont))


def supports_cjk_png_text() -> bool:
    return any(Path(candidate).exists() for candidate in CJK_FONT_CANDIDATES)


def _url_lines(value: str, limit: int = 30) -> list[str]:
    raw = value.strip()
    if len(raw) <= limit:
        return [raw]
    lines: list[str] = []
    current = raw
    while len(current) > limit and len(lines) < 2:
        split_at = max(current.rfind("/", 0, limit), current.rfind("?", 0, limit), current.rfind("&", 0, limit))
        if split_at <= 12:
            split_at = limit
        lines.append(current[:split_at])
        current = current[split_at:]
    if current:
        lines.append(current[:limit])
    return lines[:3]


def _generate_svg_cert(
    scores,
    ref_code: str,
    config: dict,
    output_dir: Path,
    upload_result: dict | None = None,
) -> Path:
    output_path = output_dir / "lobster-cert.svg"
    public_metrics = build_public_metrics(upload_result, ref_code, config)
    share_enabled = bool(public_metrics["share_enabled"])
    site_home_url = str(public_metrics.get("site_home_url") or config.get("site_home_url") or "https://eval.agent-gigo.com/")
    serial = certificate_serial(ref_code)
    tier_badge = scores.tier_name.replace(scores.tier_emoji, "").strip() or scores.tier_name
    total_entries = public_metrics["total_entries"]
    surpassed = public_metrics["surpassed_percent"]
    landing_url = str(public_metrics["landing_url"])
    footer_date = scores.timestamp.split("T")[0].replace("-", ".")

    if isinstance(total_entries, int) and total_entries > 0:
        archive_line = (
            f"已有 {total_entries:,} 只龙虾上榜"
            if scores.lang == "zh"
            else f"{total_entries:,} ranked lobsters"
        )
    else:
        archive_line = (
            "本地预览版，上传后加入榜单统计"
            if scores.lang == "zh"
            else "Local preview. Upload to join the leaderboard stats."
        )

    if isinstance(surpassed, float):
        surpassed_line = (
            f"超越 {surpassed:.1f}% 的上榜龙虾"
            if scores.lang == "zh"
            else f"Ahead of {surpassed:.1f}% of ranked lobsters"
        )
    else:
        surpassed_line = "等待同步" if scores.lang == "zh" else "Pending sync"

    radar_labels = [config["dimensions"][key].get(scores.lang, key) for key in ["meat", "brain", "claw", "shell", "soul", "cost", "speed"]]
    radar_center = (295, 894)
    radar_radius = 100
    radar_label_radius = 136
    outline_points, fill_points = _svg_radar_points(radar_center, radar_radius, scores.dimensions)
    label_positions = []
    for index in range(len(radar_labels)):
        angle = -math.pi / 2 + index * (2 * math.pi / len(radar_labels))
        label_positions.append(
            (
                round(radar_center[0] + radar_label_radius * math.cos(angle)),
                round(radar_center[1] + radar_label_radius * math.sin(angle)),
            )
        )

    top_dimensions = sorted(scores.dimensions.items(), key=lambda item: item[1], reverse=True)[:3]
    tag_rows: list[str] = []
    y = 764
    for key, _score in top_dimensions:
        profile = DIMENSION_PROFILE.get(key, {})
        tag_text = profile.get("tag", {}).get(scores.lang, key)
        title_text = profile.get("title", {}).get(scores.lang, key)
        desc_text = (profile.get("strong", {}).get(scores.lang) or [title_text])[0]
        tag_color = profile.get("color", "#FF7A59")
        mark_text = title_text[0] if scores.lang == "zh" and title_text else title_text[:2].upper()
        tag_rows.append(
            f"""
            <g transform="translate(646,{y})">
              <rect x="0" y="0" width="452" height="76" rx="18" fill="#F6F8FC" stroke="#E5EBF4" />
              <rect x="18" y="14" width="52" height="48" rx="14" fill="{tag_color}" />
              <text x="44" y="45" text-anchor="middle" dominant-baseline="middle" font-size="18" font-weight="700" fill="#FFFFFF">{_svg_escape(mark_text)}</text>
              <text x="92" y="44" font-size="26" font-weight="700" fill="#4A5C7C">{_svg_escape(tag_text)}</text>
              <text x="92" y="66" font-size="16" fill="#93A1B7">{_svg_escape(desc_text)}</text>
            </g>
            """
        )
        y += 84

    labels_svg = []
    for (x, y), label in zip(label_positions, radar_labels):
        labels_svg.append(
            f'<text x="{x}" y="{y}" text-anchor="middle" dominant-baseline="middle" font-size="20" fill="#6F7F9B">{_svg_escape(str(label))}</text>'
        )

    title_text = "龙虾鉴定证书" if scores.lang == "zh" else "Lobster Evaluation Certificate"
    if share_enabled:
        prompt_title = "「你的龙虾几分？」" if scores.lang == "zh" else "How Does Your Lobster Score?"
        prompt_subtitle = "扫码测测你的龙虾" if scores.lang == "zh" else "Open the landing page to evaluate yours"
        landing_lines = _url_lines(landing_url, limit=31)
        qr_hint = "打开线上结果页" if scores.lang == "zh" else "Open the online result"
        ref_label = f"REF {ref_code}"
    else:
        prompt_title = "去官网测测你的龙虾" if scores.lang == "zh" else "Start from the homepage"
        prompt_subtitle = (
            "本地模式二维码会打开官网首页"
            if scores.lang == "zh"
            else "The local-only QR opens the homepage"
        )
        landing_lines = _url_lines(site_home_url, limit=31)
        qr_hint = "打开官网首页" if scores.lang == "zh" else "Open the homepage"
        ref_label = "HOME"
    name_text = f"「{scores.lobster_name}」" if scores.lang == "zh" else scores.lobster_name

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="1600" viewBox="0 0 1200 1600">
  <defs>
    <linearGradient id="paperGlow" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#FFF8F2"/>
      <stop offset="100%" stop-color="#FFFDFB"/>
    </linearGradient>
    <linearGradient id="radarFill" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="rgba(255,125,95,0.35)"/>
      <stop offset="100%" stop-color="rgba(255,82,99,0.18)"/>
    </linearGradient>
  </defs>
  <rect x="0" y="0" width="1200" height="1600" rx="44" fill="url(#paperGlow)"/>
  <rect x="26" y="26" width="1148" height="1548" rx="40" fill="#FFFDFB" stroke="#F8DED7" stroke-width="2"/>
  <text x="70" y="96" font-size="54" font-family="{SVG_SANS}">🦞</text>
  <text x="164" y="68" font-size="18" font-family="{SVG_SANS}" fill="#9DA7B9">GIGO LAB</text>
  <text x="164" y="98" font-size="24" font-family="{SVG_SANS}" fill="#22314F">LOBSTER EVALUATION CERTIFICATE</text>
  <text x="164" y="176" font-size="54" font-family="{SVG_SANS}" font-weight="700" fill="#22314F">{_svg_escape(title_text)}</text>
  <rect x="878" y="48" width="246" height="78" rx="20" fill="#FFFBF8" stroke="#F8DCD5" stroke-width="2"/>
  <text x="1001" y="89" text-anchor="middle" dominant-baseline="middle" font-family="{SVG_MONO}" font-size="32" fill="#F24C54">NO. {_svg_escape(serial)}</text>
  <line x1="60" y1="184" x2="1140" y2="184" stroke="#F8CCC7" stroke-width="3"/>

  <text x="76" y="286" dominant-baseline="hanging" font-size="84" font-family="{SVG_SANS}" font-weight="700" fill="#22314F">{_svg_escape(name_text)}</text>
  <rect x="76" y="390" width="210" height="64" rx="24" fill="#FFF1E3"/>
  <text x="181" y="422" text-anchor="middle" dominant-baseline="middle" font-size="28" font-family="{SVG_SANS}" font-weight="700" fill="#DF5F2F">{_svg_escape(tier_badge)}</text>
  <text x="286" y="416" dominant-baseline="hanging" font-size="64" font-family="{SVG_SANS}" font-weight="700" fill="#F24C54">综合 {scores.total_score} 分</text>
  <text x="96" y="470" dominant-baseline="hanging" font-size="28" font-family="{SVG_SANS}" fill="#6F7F9B">{_svg_escape(surpassed_line)}</text>

  <rect x="76" y="530" width="326" height="76" rx="22" fill="#FFF4EF" stroke="#F8D0C9" stroke-width="2"/>
  <text x="100" y="550" dominant-baseline="hanging" font-size="20" font-family="{SVG_SANS}" fill="#93A1B7">综合得分</text>
  <text x="100" y="574" dominant-baseline="hanging" font-size="28" font-family="{SVG_MONO}" fill="#F24C54">{scores.total_score} / 100</text>
  <rect x="417" y="530" width="326" height="76" rx="22" fill="#FFFFFF" stroke="#EDEFF5" stroke-width="2"/>
  <text x="441" y="550" dominant-baseline="hanging" font-size="20" font-family="{SVG_SANS}" fill="#93A1B7">当前段位</text>
  <text x="441" y="574" dominant-baseline="hanging" font-size="28" font-family="{SVG_SANS}" fill="#22314F">{_svg_escape(tier_badge)}</text>
  <rect x="758" y="530" width="326" height="76" rx="22" fill="#FFFFFF" stroke="#EDEFF5" stroke-width="2"/>
  <text x="782" y="550" dominant-baseline="hanging" font-size="20" font-family="{SVG_SANS}" fill="#93A1B7">统计状态</text>
  <text x="782" y="574" dominant-baseline="hanging" font-size="28" font-family="{SVG_SANS}" fill="#22314F">{_svg_escape(archive_line)}</text>

  <rect x="60" y="644" width="1080" height="412" rx="30" fill="#FFFFFF" stroke="#EBEFF5" stroke-width="2"/>
  <text x="600" y="696" text-anchor="middle" font-size="22" font-family="{SVG_SANS}" fill="#9DA7B9">{'完整鉴定档案' if scores.lang == 'zh' else 'Evaluation archive'}</text>

  <rect x="74" y="742" width="520" height="286" rx="26" fill="#F7F9FD" stroke="#E9EDF4" stroke-width="2"/>
  <rect x="622" y="742" width="520" height="286" rx="26" fill="#F7F9FD" stroke="#E9EDF4" stroke-width="2"/>
  <text x="334" y="744" text-anchor="middle" font-size="32" font-family="{SVG_SANS}" font-weight="700" fill="#22314F">{'七维鉴定雷达' if scores.lang == 'zh' else 'Seven-dimension radar'}</text>
  <text x="866" y="744" text-anchor="middle" font-size="32" font-family="{SVG_SANS}" font-weight="700" fill="#22314F">{'专属鉴定标签' if scores.lang == 'zh' else 'Signature tags'}</text>

  <polygon points="{outline_points}" fill="none" stroke="rgba(36,61,97,0.16)" stroke-width="2"/>
  <polygon points="{fill_points}" fill="#FF8A6B55" stroke="#F24C54" stroke-width="4"/>
  <circle cx="{radar_center[0]}" cy="{radar_center[1]}" r="18" fill="rgba(242,76,84,0.08)" stroke="#C1CCE0" stroke-width="2"/>
  <line x1="{radar_center[0] - 28}" y1="{radar_center[1]}" x2="{radar_center[0] + 28}" y2="{radar_center[1]}" stroke="#C1CCE0" stroke-width="2"/>
  <line x1="{radar_center[0]}" y1="{radar_center[1] - 28}" x2="{radar_center[0]}" y2="{radar_center[1] + 28}" stroke="#C1CCE0" stroke-width="2"/>
  {''.join(labels_svg)}
  {''.join(tag_rows)}

  <rect x="366" y="1070" width="468" height="60" rx="30" fill="#F9FAFC"/>
  <text x="600" y="1100" text-anchor="middle" dominant-baseline="middle" font-size="28" font-family="{SVG_SANS}" fill="#6F7F9B">{_svg_escape(archive_line)}</text>
  <line x1="60" y1="1188" x2="1140" y2="1188" stroke="#FFA8A5" stroke-width="4" stroke-dasharray="14 10"/>

  <text x="84" y="1248" dominant-baseline="hanging" font-size="50" font-family="{SVG_SANS}" font-weight="700" fill="#22314F">{_svg_escape(prompt_title)}</text>
  <text x="84" y="1302" dominant-baseline="hanging" font-size="28" font-family="{SVG_SANS}" fill="#576786">{_svg_escape(prompt_subtitle)}</text>

  <rect x="878" y="1212" width="248" height="176" rx="22" fill="#FFFFFF" stroke="#EDEFF4" stroke-width="2"/>
  <text x="906" y="1250" font-size="18" font-family="{SVG_SANS}" fill="#93A1B7">{_svg_escape(qr_hint)}</text>
  <text x="906" y="1282" font-size="17" font-family="{SVG_MONO}" fill="#F24C54">{_svg_escape(ref_label)}</text>
  <text x="906" y="1318" font-size="14" font-family="{SVG_MONO}" fill="#6F7F9B">{_svg_escape(landing_lines[0] if len(landing_lines) > 0 else '')}</text>
  <text x="906" y="1340" font-size="14" font-family="{SVG_MONO}" fill="#6F7F9B">{_svg_escape(landing_lines[1] if len(landing_lines) > 1 else '')}</text>
  <text x="906" y="1362" font-size="14" font-family="{SVG_MONO}" fill="#6F7F9B">{_svg_escape(landing_lines[2] if len(landing_lines) > 2 else '')}</text>

  <line x1="60" y1="1486" x2="1140" y2="1486" stroke="#F8CCC7" stroke-width="3"/>
  <text x="600" y="1524" text-anchor="middle" font-size="22" font-family="{SVG_SANS}" fill="#9DA7B9">{_svg_escape(footer_date)} · {_svg_escape('第1次鉴定 · 龙虾鉴定所' if scores.lang == 'zh' else 'First evaluation · Lobster Lab')}</text>
</svg>
"""
    output_path.write_text(svg, encoding="utf-8")
    return output_path


def _load_font(size: int) -> ImageFont.ImageFont:
    candidates = [
        *CJK_FONT_CANDIDATES,
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]
    for candidate in candidates:
        if Path(candidate).exists():
            return ImageFont.truetype(candidate, size=size)
    return ImageFont.load_default()


def _load_mono_font(size: int) -> ImageFont.ImageFont:
    candidates = [
        "/usr/share/fonts/opentype/noto/NotoSansMonoCJK-Regular.ttc",
        "/usr/share/fonts/truetype/noto/NotoSansMonoCJK-Regular.ttc",
        *CJK_FONT_CANDIDATES,
        "C:/Windows/Fonts/consola.ttf",
        "C:/Windows/Fonts/consolab.ttf",
        "C:/Windows/Fonts/CascadiaMono.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
        "/usr/share/fonts/truetype/liberation2/LiberationMono-Regular.ttf",
    ]
    for candidate in candidates:
        if Path(candidate).exists():
            return ImageFont.truetype(candidate, size=size)
    return _load_font(size)


def _load_serif_font(size: int, italic: bool = False) -> ImageFont.ImageFont:
    candidates = [
        "C:/Windows/Fonts/georgiai.ttf" if italic else "C:/Windows/Fonts/georgia.ttf",
        "C:/Windows/Fonts/timesi.ttf" if italic else "C:/Windows/Fonts/times.ttf",
        "/usr/share/fonts/truetype/liberation2/LiberationSerif-Italic.ttf" if italic else "/usr/share/fonts/truetype/liberation2/LiberationSerif-Regular.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Italic.ttf" if italic else "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]
    for candidate in candidates:
        if candidate and Path(candidate).exists():
            return ImageFont.truetype(candidate, size=size)
    return _load_font(size)


def _mascot_candidates() -> list[Path]:
    current = Path(__file__).resolve()
    candidates = [current.parents[1] / "assets" / "lobster-emoji.png"]
    for ancestor in current.parents:
        candidates.append(ancestor / "skill" / "assets" / "lobster-emoji.png")
    unique: list[Path] = []
    seen: set[Path] = set()
    for candidate in candidates:
        if candidate not in seen:
            unique.append(candidate)
            seen.add(candidate)
    return unique


def _load_mascot_image(target_height: int) -> Image.Image | None:
    for candidate in _mascot_candidates():
        if not candidate.exists():
            continue
        try:
            image = Image.open(candidate).convert("RGBA")
        except Exception:
            continue

        bbox = image.getbbox()
        if bbox:
            image = image.crop(bbox)
        ratio = target_height / max(1, image.height)
        new_size = (max(1, int(image.width * ratio)), target_height)
        return image.resize(new_size, Image.LANCZOS)
    return None


def _shadowed_panel(
    image: Image.Image,
    box: tuple[int, int, int, int],
    *,
    radius: int,
    fill: tuple[int, int, int, int],
    outline: tuple[int, int, int, int] | None = None,
    outline_width: int = 0,
    shadow_offset: tuple[int, int] = (0, 18),
    shadow_blur: int = 28,
    shadow_fill: tuple[int, int, int, int] = (218, 187, 178, 70),
) -> None:
    shadow = Image.new("RGBA", image.size, (0, 0, 0, 0))
    shadow_draw = ImageDraw.Draw(shadow)
    shadow_draw.rounded_rectangle(
        (
            box[0] + shadow_offset[0],
            box[1] + shadow_offset[1],
            box[2] + shadow_offset[0],
            box[3] + shadow_offset[1],
        ),
        radius=radius,
        fill=shadow_fill,
    )
    shadow = shadow.filter(ImageFilter.GaussianBlur(shadow_blur))
    image.alpha_composite(shadow)

    overlay = Image.new("RGBA", image.size, (0, 0, 0, 0))
    overlay_draw = ImageDraw.Draw(overlay)
    overlay_draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=outline_width)
    image.alpha_composite(overlay)


def _draw_stacked_panel(
    image: Image.Image,
    box: tuple[int, int, int, int],
    *,
    radius: int,
    fill: tuple[int, int, int, int],
    outline: tuple[int, int, int, int],
    underlay_fill: tuple[int, int, int, int],
    underlay_outline: tuple[int, int, int, int],
    offset: tuple[int, int] = (10, 10),
) -> None:
    under_box = (
        box[0] + offset[0],
        box[1] + offset[1],
        box[2] + offset[0],
        box[3] + offset[1],
    )
    _shadowed_panel(
        image,
        under_box,
        radius=radius + 2,
        fill=underlay_fill,
        outline=underlay_outline,
        outline_width=2,
        shadow_fill=(0, 0, 0, 0),
        shadow_blur=0,
        shadow_offset=(0, 0),
    )
    _shadowed_panel(
        image,
        box,
        radius=radius,
        fill=fill,
        outline=outline,
        outline_width=2,
        shadow_fill=(214, 186, 178, 30),
        shadow_blur=14,
        shadow_offset=(0, 8),
    )


def _draw_multicolor_line(
    draw: ImageDraw.ImageDraw,
    start: tuple[int, int],
    segments: list[tuple[str, tuple[int, int, int, int], ImageFont.ImageFont]],
    gap: int = 6,
) -> None:
    x, y = start
    for text, color, font in segments:
        draw.text((x, y), text, fill=color, font=font)
        bbox = draw.textbbox((x, y), text, font=font)
        x = bbox[2] + gap


def _interpolate_rgba(
    start: tuple[int, int, int, int],
    end: tuple[int, int, int, int],
    progress: float,
) -> tuple[int, int, int, int]:
    return tuple(int(start[index] + (end[index] - start[index]) * progress) for index in range(4))


def _draw_radar(
    image: Image.Image,
    center: tuple[int, int],
    radius: int,
    dimensions: dict[str, int],
    labels: list[str],
    label_font: ImageFont.ImageFont,
) -> None:
    order = ["meat", "brain", "claw", "shell", "soul", "cost", "speed"]
    ring_color = (36, 61, 97, 30)
    axis_color = (36, 61, 97, 40)
    stroke_color = (242, 76, 84, 250)
    target_color = (193, 204, 224, 255)
    center_glow = (242, 76, 84, 18)
    overlay = Image.new("RGBA", image.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    for ring in range(1, 6):
        current = radius * ring / 5
        polygon = []
        for index in range(len(order)):
            angle = -math.pi / 2 + index * (2 * math.pi / len(order))
            polygon.append((center[0] + current * math.cos(angle), center[1] + current * math.sin(angle)))
        draw.polygon(polygon, outline=ring_color)

    for index in range(len(order)):
        angle = -math.pi / 2 + index * (2 * math.pi / len(order))
        outer = (center[0] + radius * math.cos(angle), center[1] + radius * math.sin(angle))
        draw.line((center[0], center[1], outer[0], outer[1]), fill=axis_color, width=2)

    draw.ellipse(
        (center[0] - 18, center[1] - 18, center[0] + 18, center[1] + 18),
        fill=center_glow,
        outline=target_color,
        width=2,
    )
    draw.line((center[0] - 28, center[1], center[0] + 28, center[1]), fill=target_color, width=2)
    draw.line((center[0], center[1] - 28, center[0], center[1] + 28), fill=target_color, width=2)

    points = []
    for index, key in enumerate(order):
        angle = -math.pi / 2 + index * (2 * math.pi / len(order))
        point_radius = radius * (dimensions.get(key, 0) / 100)
        points.append((center[0] + point_radius * math.cos(angle), center[1] + point_radius * math.sin(angle)))

    gradient_box = (
        int(center[0] - radius),
        int(center[1] - radius),
        int(center[0] + radius),
        int(center[1] + radius),
    )
    gradient_width = max(1, gradient_box[2] - gradient_box[0])
    gradient_height = max(1, gradient_box[3] - gradient_box[1])
    gradient = Image.new("RGBA", (gradient_width, gradient_height), (0, 0, 0, 0))
    pixels = gradient.load()
    start = (255, 125, 95, 62)
    end = (255, 82, 99, 40)
    denominator = max(1, gradient_width + gradient_height - 2)
    for y in range(gradient_height):
        for x in range(gradient_width):
            pixels[x, y] = _interpolate_rgba(start, end, (x + y) / denominator)
    mask = Image.new("L", (gradient_width, gradient_height), 0)
    mask_draw = ImageDraw.Draw(mask)
    local_points = [(point[0] - gradient_box[0], point[1] - gradient_box[1]) for point in points]
    mask_draw.polygon(local_points, fill=255)
    clipped = Image.new("RGBA", (gradient_width, gradient_height), (0, 0, 0, 0))
    clipped.paste(gradient, (0, 0), mask)
    overlay.alpha_composite(clipped, gradient_box[:2])

    draw = ImageDraw.Draw(overlay)
    draw.polygon(points, outline=stroke_color, width=4)
    for point in points:
        draw.ellipse((point[0] - 7, point[1] - 7, point[0] + 7, point[1] + 7), fill=(255, 255, 255, 255), outline=stroke_color, width=3)

    image.alpha_composite(overlay)
    label_draw = ImageDraw.Draw(image)
    label_offsets = [
        (0, 14),
        (-8, 4),
        (-10, 2),
        (-8, -8),
        (0, -12),
        (8, -8),
        (8, 4),
    ]
    for index, label in enumerate(labels):
        angle = -math.pi / 2 + index * (2 * math.pi / len(order))
        label_radius = radius + 12
        offset_x, offset_y = label_offsets[index]
        x = center[0] + label_radius * math.cos(angle) + offset_x
        y = center[1] + label_radius * math.sin(angle) + offset_y
        bbox = label_draw.textbbox((0, 0), label, font=label_font)
        width = bbox[2] - bbox[0]
        height = bbox[3] - bbox[1]
        label_draw.text((x - width / 2, y - height / 2), label, fill=(111, 127, 155, 255), font=label_font)


def _fit_name_font(draw: ImageDraw.ImageDraw, text: str, max_width: int, start_size: int) -> ImageFont.ImageFont:
    size = start_size
    while size >= 60:
        font = _load_font(size)
        bbox = draw.textbbox((0, 0), text, font=font)
        if bbox[2] - bbox[0] <= max_width:
            return font
        size -= 4
    return _load_font(60)


def _paint_paper_bloom(image: Image.Image) -> None:
    overlay = Image.new("RGBA", image.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    draw.ellipse((-180, -140, 420, 380), fill=(255, 228, 220, 130))
    draw.ellipse((760, -60, 1270, 360), fill=(255, 240, 233, 110))
    draw.ellipse((860, 1210, 1360, 1690), fill=(255, 236, 231, 100))
    draw.ellipse((-120, 1260, 300, 1670), fill=(255, 244, 240, 85))
    overlay = overlay.filter(ImageFilter.GaussianBlur(56))
    image.alpha_composite(overlay)


def _place_logo_watermark(
    image: Image.Image,
    logo: Image.Image | None,
    *,
    top_left: tuple[int, int],
    target_height: int,
    tint: tuple[int, int, int] = (214, 197, 183),
    opacity: int = 42,
    blur: int = 1,
) -> None:
    if logo is None:
        return
    ratio = target_height / max(1, logo.height)
    resized = logo.resize((max(1, int(logo.width * ratio)), target_height), Image.LANCZOS)
    alpha = resized.getchannel("A").point(lambda value: int(value * opacity / 255))
    watermark = Image.new("RGBA", resized.size, tint + (0,))
    watermark.putalpha(alpha)
    if blur:
        watermark = watermark.filter(ImageFilter.GaussianBlur(blur))
    image.alpha_composite(watermark, top_left)


def _draw_dashed_line(
    draw: ImageDraw.ImageDraw,
    *,
    x1: int,
    x2: int,
    y: int,
    color: tuple[int, int, int, int],
    dash: int = 14,
    gap: int = 10,
    width: int = 3,
) -> None:
    current = x1
    while current < x2:
        draw.line((current, y, min(current + dash, x2), y), fill=color, width=width)
        current += dash + gap


def _draw_data_pill(
    image: Image.Image,
    draw: ImageDraw.ImageDraw,
    box: tuple[int, int, int, int],
    *,
    label: str,
    value: str,
    label_font: ImageFont.ImageFont,
    value_font: ImageFont.ImageFont,
    accent: bool = False,
) -> None:
    fill = (255, 255, 255, 255) if not accent else (255, 244, 239, 255)
    outline = (237, 239, 245, 255) if not accent else (248, 208, 201, 255)
    _shadowed_panel(
        image,
        box,
        radius=22,
        fill=fill,
        outline=outline,
        outline_width=2,
        shadow_fill=(218, 187, 178, 26),
        shadow_blur=16,
        shadow_offset=(0, 8),
    )
    draw = ImageDraw.Draw(image)
    draw.text((box[0] + 24, box[1] + 16), label, fill=SLATE_SOFT, font=label_font)
    draw.text((box[0] + 24, box[1] + 40), value, fill=ACCENT if accent else NAVY, font=value_font)


def _draw_tag_row(
    image: Image.Image,
    draw: ImageDraw.ImageDraw,
    box: tuple[int, int, int, int],
    *,
    icon_fill: tuple[int, int, int, int],
    icon_text: str,
    title: str,
    subtitle: str,
    mark_font: ImageFont.ImageFont,
    title_font: ImageFont.ImageFont,
    subtitle_font: ImageFont.ImageFont,
) -> None:
    _shadowed_panel(
        image,
        box,
        radius=20,
        fill=TAG_FILL,
        outline=(237, 241, 247, 255),
        outline_width=1,
        shadow_fill=(0, 0, 0, 0),
        shadow_blur=0,
        shadow_offset=(0, 0),
    )
    draw = ImageDraw.Draw(image)
    icon_box = (box[0] + 18, box[1] + 14, box[0] + 70, box[1] + 62)
    _shadowed_panel(
        image,
        icon_box,
        radius=16,
        fill=icon_fill,
        shadow_fill=(0, 0, 0, 0),
        shadow_blur=0,
        shadow_offset=(0, 0),
    )
    draw = ImageDraw.Draw(image)
    mark_bbox = draw.textbbox((0, 0), icon_text, font=mark_font)
    mark_x = icon_box[0] + ((icon_box[2] - icon_box[0]) - (mark_bbox[2] - mark_bbox[0])) / 2
    mark_y = icon_box[1] + ((icon_box[3] - icon_box[1]) - (mark_bbox[3] - mark_bbox[1])) / 2 - 2
    draw.text((mark_x, mark_y), icon_text, fill=(255, 255, 255, 255), font=mark_font)
    draw.text((box[0] + 90, box[1] + 16), title, fill=(74, 92, 124, 255), font=title_font)
    draw.text((box[0] + 90, box[1] + 44), subtitle, fill=SLATE_SOFT, font=subtitle_font)


def _prefer_mono(text: str) -> bool:
    return all(ord(ch) < 128 for ch in text)


def generate_cert(
    scores,
    ref_code: str,
    config: dict,
    output_dir: Path,
    template_path: Path | None = None,
    upload_result: dict | None = None,
) -> Path:
    if not supports_png_certificate():
        return _generate_svg_cert(
            scores=scores,
            ref_code=ref_code,
            config=config,
            output_dir=output_dir,
            upload_result=upload_result,
        )
    if scores.lang == "zh" and not supports_cjk_png_text():
        return _generate_svg_cert(
            scores=scores,
            ref_code=ref_code,
            config=config,
            output_dir=output_dir,
            upload_result=upload_result,
        )

    image = Image.new("RGBA", CERT_SIZE, PAPER)
    _paint_paper_bloom(image)

    _shadowed_panel(
        image,
        (26, 26, CERT_SIZE[0] - 26, CERT_SIZE[1] - 26),
        radius=42,
        fill=PAPER_PANEL,
        outline=(248, 222, 215, 255),
        outline_width=2,
        shadow_fill=(228, 197, 186, 52),
        shadow_blur=36,
    )
    draw = ImageDraw.Draw(image)

    title_font = _load_font(54)
    subtitle_font = _load_serif_font(24, italic=False)
    overline_font = _load_font(18)
    section_font = _load_font(31)
    body_font = _load_font(25)
    small_font = _load_font(20)
    score_font = _load_serif_font(78, italic=False)
    score_label_font = _load_font(64)
    number_font = _load_mono_font(32)
    mono_small_font = _load_mono_font(18)
    mono_value_font = _load_mono_font(28)
    regular_value_font = _load_font(28)
    script_font = _load_serif_font(78, italic=True)

    mascot = _load_mascot_image(84)
    _place_logo_watermark(image, mascot, top_left=(810, 154), target_height=430, opacity=18, blur=1)
    _place_logo_watermark(image, mascot, top_left=(-12, 1180), target_height=300, opacity=14, blur=1)
    if mascot:
        _shadowed_panel(
            image,
            (52, 44, 144, 136),
            radius=24,
            fill=(255, 251, 248, 255),
            outline=(248, 220, 213, 255),
            outline_width=2,
            shadow_fill=(236, 203, 193, 38),
            shadow_blur=16,
            shadow_offset=(0, 6),
        )
        image.alpha_composite(mascot, (60, 48))
    header_x = 164
    title_text = "龙虾鉴定证书" if scores.lang == "zh" else "Lobster Evaluation Certificate"
    draw.text((header_x, 50), "GIGO LAB", fill=SLATE_SOFT, font=overline_font)
    draw.text((header_x, 78), "LOBSTER EVALUATION CERTIFICATE", fill=NAVY, font=subtitle_font)
    draw.text((header_x, 110), title_text, fill=NAVY, font=title_font)

    serial = certificate_serial(ref_code)
    serial_box = (878, 48, 1124, 126)
    _shadowed_panel(
        image,
        serial_box,
        radius=20,
        fill=(255, 251, 248, 255),
        outline=(248, 220, 213, 255),
        outline_width=2,
        shadow_fill=(236, 203, 193, 44),
        shadow_blur=18,
        shadow_offset=(0, 8),
    )
    draw = ImageDraw.Draw(image)
    serial_text = f"NO. {serial}"
    serial_bbox = draw.textbbox((0, 0), serial_text, font=number_font)
    serial_x = serial_box[0] + ((serial_box[2] - serial_box[0]) - (serial_bbox[2] - serial_bbox[0])) // 2
    draw.text((serial_x, 68), serial_text, fill=ACCENT, font=number_font)
    draw.line((60, 184, CERT_SIZE[0] - 60, 184), fill=ACCENT_LINE, width=3)

    public_metrics = build_public_metrics(upload_result, ref_code, config)
    share_enabled = bool(public_metrics["share_enabled"])
    site_home_url = str(public_metrics.get("site_home_url") or config.get("site_home_url") or "https://eval.agent-gigo.com/")
    surpassed = public_metrics["surpassed_percent"]
    total_entries = public_metrics["total_entries"]

    tier_badge = scores.tier_name.replace(scores.tier_emoji, "").strip() or scores.tier_name
    name_text = f"「{scores.lobster_name}」" if scores.lang == "zh" else scores.lobster_name
    name_font = _fit_name_font(draw, name_text, 620, 90) if scores.lang == "zh" else script_font
    draw.text((76, 236), name_text, fill=NAVY, font=name_font)

    tier_bbox = draw.textbbox((0, 0), tier_badge, font=body_font)
    tier_width = tier_bbox[2] - tier_bbox[0] + 52
    _shadowed_panel(
        image,
        (76, 390, 76 + tier_width, 454),
        radius=24,
        fill=ACCENT_SOFT,
        shadow_fill=(0, 0, 0, 0),
    )
    draw = ImageDraw.Draw(image)
    draw.text((102, 405), tier_badge, fill=(223, 95, 47, 255), font=body_font)

    if scores.lang == "zh":
        score_x = 286
        score_y = 382
        lead_text = "综合"
        tail_text = "分"
        lead_bbox = draw.textbbox((0, 0), lead_text, font=score_label_font)
        draw.text((score_x, score_y), lead_text, fill=ACCENT, font=score_label_font)
        number_x = score_x + (lead_bbox[2] - lead_bbox[0]) + 16
        number_text = str(scores.total_score)
        number_bbox = draw.textbbox((0, 0), number_text, font=score_font)
        draw.text((number_x, score_y - 8), number_text, fill=ACCENT, font=score_font)
        tail_x = number_x + (number_bbox[2] - number_bbox[0]) + 16
        draw.text((tail_x, score_y), tail_text, fill=ACCENT, font=score_label_font)
    else:
        draw.text((286, 378), f"SCORE {scores.total_score}", fill=ACCENT, font=score_font)

    if isinstance(surpassed, float):
        percent_text = f"{surpassed:.1f}%"
        if scores.lang == "zh":
            segments = [
                ("超越了 ", SLATE, body_font),
                (percent_text, ACCENT, body_font),
                (" 的上榜龙虾", SLATE, body_font),
            ]
        else:
            segments = [
                ("Above ", SLATE, body_font),
                (percent_text, ACCENT, body_font),
                (" of ranked lobsters", SLATE, body_font),
            ]
    else:
        placeholder = "本地预览版，上传后解锁榜单排名" if scores.lang == "zh" else "Local preview. Upload to unlock leaderboard ranking."
        segments = [(placeholder, SLATE, body_font)]
    _draw_multicolor_line(draw, (96, 476), segments)

    total_entries_value = (
        f"{total_entries:,} 只龙虾" if isinstance(total_entries, int) and total_entries > 0 and scores.lang == "zh"
        else f"{total_entries:,} lobsters" if isinstance(total_entries, int) and total_entries > 0
        else ("等待同步" if scores.lang == "zh" else "Pending")
    )
    surpassed_value = (
        f"{surpassed:.1f}%" if isinstance(surpassed, float) else ("等待同步" if scores.lang == "zh" else "Pending")
    )
    chips = [
        (
            "综合得分" if scores.lang == "zh" else "Overall score",
            f"{scores.total_score} / 100",
            True,
        ),
        (
            "当前段位" if scores.lang == "zh" else "Current tier",
            tier_badge,
            False,
        ),
        (
            "超越比例" if scores.lang == "zh" else "Ahead of",
            surpassed_value,
            False,
        ),
    ]
    chip_y = 530
    chip_width = 326
    chip_gap = 15
    for index, (label, value, accent) in enumerate(chips):
        left = 76 + index * (chip_width + chip_gap)
        value_font = mono_value_font if _prefer_mono(value) else regular_value_font
        _draw_data_pill(
            image,
            draw,
            (left, chip_y, left + chip_width, chip_y + 76),
            label=label,
            value=value,
            label_font=small_font,
            value_font=value_font,
            accent=accent,
        )

    card_box = (60, 644, CERT_SIZE[0] - 60, 1056)
    _shadowed_panel(
        image,
        card_box,
        radius=30,
        fill=CARD_FILL,
        outline=(235, 239, 245, 255),
        outline_width=2,
        shadow_fill=(211, 220, 238, 28),
        shadow_offset=(0, 14),
        shadow_blur=20,
    )
    draw = ImageDraw.Draw(image)

    archive_overline_font = _load_font(22) if scores.lang == "zh" else mono_small_font
    archive_title = "完整鉴定档案" if scores.lang == "zh" else "EVALUATION ARCHIVE"
    archive_bbox = draw.textbbox((0, 0), archive_title, font=archive_overline_font)
    archive_width = archive_bbox[2] - archive_bbox[0]
    draw.text(
        ((card_box[0] + card_box[2] - archive_width) // 2, 650),
        archive_title,
        fill=SLATE_SOFT,
        font=archive_overline_font,
    )
    left_panel = (74, 732, 594, 1018)
    right_panel = (606, 732, 1126, 1018)
    left_inner = (90, 750, 578, 1000)
    right_inner = (622, 750, 1110, 1000)

    left_title = "七维鉴定雷达" if scores.lang == "zh" else "Seven-dimension radar"
    right_title = "专属鉴定标签" if scores.lang == "zh" else "Signature tags"
    left_title_bbox = draw.textbbox((0, 0), left_title, font=section_font)
    right_title_bbox = draw.textbbox((0, 0), right_title, font=section_font)
    draw.text(
        ((left_panel[0] + left_panel[2] - (left_title_bbox[2] - left_title_bbox[0])) // 2, 694),
        left_title,
        fill=NAVY,
        font=section_font,
    )
    draw.text(
        ((right_panel[0] + right_panel[2] - (right_title_bbox[2] - right_title_bbox[0])) // 2, 694),
        right_title,
        fill=NAVY,
        font=section_font,
    )

    _draw_stacked_panel(
        image,
        left_panel,
        radius=26,
        fill=CARD_SOFT,
        outline=(233, 237, 244, 255),
        underlay_fill=(255, 241, 237, 255),
        underlay_outline=(249, 216, 208, 255),
        offset=(12, 10),
    )
    _draw_stacked_panel(
        image,
        right_panel,
        radius=26,
        fill=CARD_SOFT,
        outline=(233, 237, 244, 255),
        underlay_fill=(255, 244, 240, 255),
        underlay_outline=(248, 220, 214, 255),
        offset=(12, 10),
    )
    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle(left_inner, radius=22, outline=(228, 232, 241, 255), width=2)
    draw.rounded_rectangle(right_inner, radius=22, outline=(228, 232, 241, 255), width=2)

    radar_labels = [config["dimensions"][key].get(scores.lang, key) for key in ["meat", "brain", "claw", "shell", "soul", "cost", "speed"]]
    _draw_radar(
        image,
        center=((left_inner[0] + left_inner[2]) // 2, 878),
        radius=94,
        dimensions=scores.dimensions,
        labels=radar_labels,
        label_font=small_font,
    )

    top_dimensions = sorted(scores.dimensions.items(), key=lambda item: item[1], reverse=True)[:3]
    y = 770
    for key, _score in top_dimensions:
        profile = DIMENSION_PROFILE.get(key, {})
        tag_text = profile.get("tag", {}).get(scores.lang, key)
        title_text = profile.get("title", {}).get(scores.lang, key)
        desc_text = (profile.get("strong", {}).get(scores.lang) or [title_text])[0]
        tag_color = profile.get("color", "#FF7A59")
        rgb = tuple(int(tag_color[i : i + 2], 16) for i in (1, 3, 5))
        mark_text = title_text[0] if scores.lang == "zh" and title_text else title_text[:2].upper()
        _draw_tag_row(
            image,
            draw,
            (right_inner[0] + 12, y, right_inner[2] - 12, y + 72),
            icon_fill=rgb + (255,),
            icon_text=mark_text,
            title=tag_text,
            subtitle=desc_text,
            mark_font=_load_font(18 if scores.lang == "zh" else 17),
            title_font=_load_font(25),
            subtitle_font=_load_font(16),
        )
        y += 74

    if isinstance(total_entries, int) and total_entries > 0:
        pill_text = (
            f"已有 {total_entries:,} 只龙虾上榜"
            if scores.lang == "zh"
            else f"{total_entries:,} ranked lobsters"
        )
    else:
        pill_text = (
            "本地预览版，上传后加入榜单统计"
            if scores.lang == "zh"
            else "Local preview. Upload to join the leaderboard stats."
        )
    pill_bbox = draw.textbbox((0, 0), pill_text, font=body_font)
    pill_width = pill_bbox[2] - pill_bbox[0] + 64
    pill_left = (CERT_SIZE[0] - pill_width) // 2
    _shadowed_panel(
        image,
        (pill_left, 1070, pill_left + pill_width, 1130),
        radius=32,
        fill=(249, 250, 252, 255),
        shadow_fill=(0, 0, 0, 0),
        shadow_blur=0,
        shadow_offset=(0, 0),
    )
    draw = ImageDraw.Draw(image)
    draw.text((pill_left + 32, 1084), pill_text, fill=SLATE, font=body_font)

    dash_y = 1188
    _draw_dashed_line(draw, x1=60, x2=CERT_SIZE[0] - 60, y=dash_y, color=(255, 168, 165, 255), dash=14, gap=10, width=4)

    if share_enabled:
        prompt_title = "「你的龙虾几分？」" if scores.lang == "zh" else "How Does Your Lobster Score?"
        prompt_subtitle = "扫码测测你的龙虾" if scores.lang == "zh" else "Scan to evaluate yours"
    else:
        prompt_title = "去官网测测你的龙虾" if scores.lang == "zh" else "Start from the homepage"
        prompt_subtitle = (
            "本地模式二维码会打开官网首页"
            if scores.lang == "zh"
            else "The local-only QR opens the homepage"
        )
    draw.text((84, 1238), prompt_title, fill=NAVY, font=_load_font(50))
    draw.text((84, 1308), prompt_subtitle, fill=(87, 103, 134, 255), font=_load_font(28))

    qr_card = (948, 1212, 1108, 1372)
    _shadowed_panel(
        image,
        qr_card,
        radius=22,
        fill=(255, 255, 255, 255),
        outline=(237, 239, 244, 255),
        outline_width=2,
        shadow_fill=(194, 204, 221, 60),
        shadow_offset=(0, 10),
        shadow_blur=18,
    )
    if share_enabled:
        qr = qrcode.QRCode(border=1, box_size=8)
        qr.add_data(str(public_metrics["landing_url"]))
        qr.make(fit=True)
        qr_image = qr.make_image(fill_color="black", back_color="white").convert("RGBA").resize((132, 132))
        image.alpha_composite(qr_image, (962, 1226))
    else:
        qr = qrcode.QRCode(border=1, box_size=8)
        qr.add_data(site_home_url)
        qr.make(fit=True)
        qr_image = qr.make_image(fill_color="black", back_color="white").convert("RGBA").resize((132, 132))
        image.alpha_composite(qr_image, (962, 1226))

    draw.line((60, 1486, CERT_SIZE[0] - 60, 1486), fill=ACCENT_LINE, width=3)
    footer_date = scores.timestamp.split("T")[0].replace("-", ".")
    footer = (
        f"{footer_date}  ·  第1次鉴定  ·  龙虾鉴定所"
        if scores.lang == "zh"
        else f"{footer_date}  ·  First evaluation  ·  Lobster Lab"
    )
    footer_font = _load_font(22) if scores.lang == "zh" else _load_mono_font(22)
    footer_bbox = draw.textbbox((0, 0), footer, font=footer_font)
    footer_x = (CERT_SIZE[0] - (footer_bbox[2] - footer_bbox[0])) // 2
    draw.text((footer_x, 1520), footer, fill=SLATE_SOFT, font=footer_font)

    output_path = output_dir / "lobster-cert.png"
    image.save(output_path)
    return output_path
