#!/usr/bin/env python3
"""Hyperframes project generator for Video Studio.

The JSON file is an intermediate manifest. The renderable output is the
generated HTML project directory containing index.html and relative assets.
"""

from __future__ import annotations

import argparse
import base64
import json
import mimetypes
import re
import shutil
import subprocess
import sys
import time
import wave
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[1]
CACHE_DIR = BASE_DIR / ".cache"
ASSET_DIR = CACHE_DIR / "assets"
PROJECT_DIR = CACHE_DIR / "hyperframes"
RENDER_DIR = CACHE_DIR / "renders"
TEMPLATE_FILE = BASE_DIR / "templates" / "video_templates.json"
EMBED_LIMIT_BYTES = 128 * 1024


FALLBACK_TEMPLATES = {
    "product_launch": {
        "name": "Product Launch",
        "resolution": {"width": 1920, "height": 1080},
        "style": {"palette": ["#0B0F19", "#F8FAFC", "#22D3EE", "#A3E635"], "font": "Inter"},
        "frames": [
            {"id": "hook", "role": "hook", "duration": 3, "motion": "depth_push"},
            {"id": "problem", "role": "problem", "duration": 4, "motion": "parallax_reveal"},
            {"id": "solution", "role": "solution", "duration": 5, "motion": "3d_like_orbit"},
            {"id": "feature_grid", "role": "feature_grid", "duration": 6, "motion": "staggered_cards"},
            {"id": "cta", "role": "cta", "duration": 3, "motion": "logo_lockup"},
        ],
    },
    "data_story": {
        "name": "Data Story",
        "resolution": {"width": 1920, "height": 1080},
        "style": {"palette": ["#111827", "#F9FAFB", "#38BDF8", "#F59E0B"], "font": "Inter"},
        "frames": [
            {"id": "headline_metric", "role": "headline_metric", "duration": 3, "motion": "count_up"},
            {"id": "kpi_progress", "role": "kpi_progress", "duration": 5, "motion": "bar_fill"},
            {"id": "chart_sequence", "role": "chart_sequence", "duration": 6, "motion": "axis_draw"},
            {"id": "insight", "role": "insight", "duration": 4, "motion": "callout_focus"},
            {"id": "summary", "role": "summary", "duration": 3, "motion": "ranked_list"},
        ],
    },
    "minimalist_quote": {
        "name": "Minimalist Quote",
        "resolution": {"width": 1080, "height": 1920},
        "style": {"palette": ["#050505", "#F5F5F4", "#D4AF37"], "font": "Geist"},
        "frames": [
            {"id": "silence_open", "role": "silence_open", "duration": 2, "motion": "fade_in"},
            {"id": "quote_part_1", "role": "quote_part_1", "duration": 4, "motion": "kinetic_type"},
            {"id": "quote_part_2", "role": "quote_part_2", "duration": 4, "motion": "slow_tracking"},
            {"id": "attribution", "role": "attribution", "duration": 3, "motion": "soft_lockup"},
        ],
    },
}


def load_templates() -> dict:
    if TEMPLATE_FILE.exists():
        with TEMPLATE_FILE.open("r", encoding="utf-8") as handle:
            return json.load(handle)
    return FALLBACK_TEMPLATES


def _print(payload: dict) -> None:
    print(json.dumps(payload, indent=2, sort_keys=True))


def _read_json(path: Path) -> dict:
    with path.expanduser().open("r", encoding="utf-8") as handle:
        return json.load(handle)


def _safe_name(value: str) -> str:
    return "".join(char if char.isalnum() or char in ("-", "_") else "-" for char in value).strip("-")[:60] or "video"


def _resolve_path(value: str) -> Path:
    path = Path(value).expanduser()
    if not path.is_absolute():
        path = (Path.cwd() / path).resolve()
    return path


def _asset_to_payload(path: Path, embed: bool) -> dict:
    payload = {
        "source": str(path.resolve()),
        "name": path.name,
        "mime": mimetypes.guess_type(path.name)[0] or "application/octet-stream",
        "exists": path.exists(),
    }
    if embed and path.exists() and path.stat().st_size <= EMBED_LIMIT_BYTES:
        payload["base64"] = base64.b64encode(path.read_bytes()).decode("ascii")
    return payload


def _html_escape(value: object) -> str:
    return (
        str(value if value is not None else "")
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def _css_string(value: object) -> str:
    return str(value if value is not None else "").replace("\\", "\\\\").replace('"', '\\"')


def _script_json(value: object) -> str:
    return json.dumps(value, sort_keys=True).replace("</", "<\\/")


def _slug_words(value: str, limit: int = 16) -> list[str]:
    words = re.findall(r"[A-Za-z0-9][A-Za-z0-9+.#%/-]*", value)
    return words[:limit] or ["Video", "Studio"]


def _extract_cjk_phrases(value: str, limit: int = 16) -> list[str]:
    """Extract CJK (Chinese/Japanese/Korean) phrases from text."""
    # Chinese: 一-鿿, Japanese Kanji: same range + 㐀-䶿
    # Japanese Hiragana: ぀-ゟ, Katakana: ゠-ヿ
    # Korean Hangul: 가-힯
    phrases = re.findall(r"[一-鿿㐀-䶿぀-ゟ゠-ヿ가-힯]{2,}", value)
    return phrases[:limit]


def _extract_non_latin_words(value: str, limit: int = 16) -> list[str]:
    """Extract words from non-Latin scripts (Arabic, Hindi, Thai, etc.)."""
    # Arabic: ؀-ۿ, Devanagari (Hindi): ऀ-ॿ, Thai: ฀-๿
    # Cyrillic: Ѐ-ӿ, Greek: Ͱ-Ͽ
    words = re.findall(r"[؀-ۿऀ-ॿ฀-๿Ѐ-ӿͰ-Ͽ]{2,}", value)
    return words[:limit]


def _clean_prompt_prefix(value: str) -> str:
    return re.sub(r"^(video\s+theme|theme|topic|title|subject|brief)\s*[:：-]\s*", "", value.strip(), flags=re.I)


def _brief_sentences(value: str) -> list[str]:
    cleaned = re.sub(r"\s+", " ", value).strip()
    # Split on sentence endings from all major languages
    # English: . ! ?  Chinese: 。！？  Japanese: 。！？
    # Arabic/Urdu: ؟  Hindi: ।  Korean: 。  General: ; ;
    chunks = re.split(r"(?<=[.!?。！？؟।；])\s*|[\n;；]+", cleaned)
    sentences = [_clean_prompt_prefix(chunk.strip(" -")) for chunk in chunks if chunk.strip(" -")]
    sentences = [sentence for sentence in sentences if sentence and len(sentence) > 1]
    if len(sentences) >= 2:
        return sentences
    # For single sentence or no sentence: extract phrases from all supported scripts
    cjk = _extract_cjk_phrases(cleaned, 20)
    non_latin = _extract_non_latin_words(cleaned, 20)
    english = _slug_words(cleaned, 20)
    all_words = cjk + non_latin + english
    if not all_words:
        return ["A clear story for the audience."]
    return [" ".join(all_words[index : index + 8]) for index in range(0, len(all_words), 8)]


def _title_from_brief(value: str, fallback: str) -> str:
    sentences = _brief_sentences(value)
    first = sentences[0] if sentences else fallback
    first = _clean_prompt_prefix(first)
    first = re.sub(r"^(create|make|build|generate|turn)\s+(a|an|the)?\s*", "", first, flags=re.I)
    words = first.split()
    return " ".join(words[:7]).strip(" .,:;") or fallback


ROLE_HEADLINES = {
    "hook": "Open With The Promise",
    "problem": "Name The Pain",
    "solution": "Reveal The Solution",
    "feature_grid": "Show The Proof",
    "cta": "Make The Next Step Clear",
    "title": "Feature In Focus",
    "before_state": "Before The Change",
    "demo_step": "Show The Workflow",
    "after_state": "After The Change",
    "takeaway": "What Viewers Remember",
    "headline_metric": "Lead With The Number",
    "kpi_progress": "Track The Momentum",
    "chart_sequence": "Show The Trend",
    "insight": "Explain What It Means",
    "summary": "Close With The Takeaway",
    "question": "Start With The Question",
    "definition": "Define The Idea",
    "key_point": "Make The Point Concrete",
    "example": "Ground It In An Example",
    "recap": "Recap The Lesson",
    "quote": "Let The Quote Breathe",
    "quote_part_1": "Set The Line",
    "quote_part_2": "Land The Thought",
    "attribution": "Credit The Voice",
    "event_hook": "Announce The Moment",
    "speaker_intro": "Introduce The Host",
    "agenda": "Preview The Agenda",
    "date_time": "Lock The Date",
    "version_title": "New Release",
    "update_item": "What Changed",
    "availability": "Available Now",
    "product_hero": "Lead With The Product",
    "benefit": "Why It Matters",
    "offer": "Make The Offer Clear",
}


def _strip_sentence_endings(text: str) -> str:
    """Remove trailing sentence punctuation from text."""
    return re.sub(r"[.。!！?？;；:：,，\s]+$", "", text).strip()


def _frame_copy(frame: dict, project: dict, index: int) -> dict:
    item = dict(frame)
    role = str(item.get("role") or "scene")

    # Priority 1: explicit frame_contents from the request (agent-generated per-frame copy)
    frame_contents = project.get("frame_contents") or []
    if index < len(frame_contents):
        fc = frame_contents[index]
        item["headline"] = item.get("headline") or fc.get("headline") or ""
        item["caption"] = item.get("caption") or fc.get("caption") or ""
        return item

    # Priority 2: brief-driven content with role-based fallback
    brief = str(project.get("brief") or "")
    sentences = _brief_sentences(brief)
    title = _title_from_brief(brief, str(project.get("template_name") or "Video"))
    topic = _extract_topic(brief)

    # Headline: use brief content when available, role-based fallback otherwise
    if index == 0:
        default_headline = _strip_sentence_endings(title)
    elif sentences:
        # Cycle through sentences (handles more frames than sentences)
        sentence = sentences[index % len(sentences)]
        words = sentence.split()
        candidate = _strip_sentence_endings(" ".join(words[:8]))
        default_headline = candidate if len(candidate) > 3 else ROLE_HEADLINES.get(role, role.replace("_", " ").title())
    else:
        default_headline = ROLE_HEADLINES.get(role, role.replace("_", " ").title())

    # Caption: use brief content when available, role-based fallback otherwise
    if sentences and len(sentences) > 1:
        # Cycle through sentences for captions too
        caption_source = sentences[index % len(sentences)]
    elif topic:
        # Single-topic brief: combine topic with role context
        caption_source = f"{topic} — {ROLE_HEADLINES.get(role, 'Next step')}"
    else:
        caption_source = str(project.get("best_for") or "")

    item["headline"] = item.get("headline") or default_headline
    item["caption"] = item.get("caption") or caption_source
    return item


def _extract_topic(brief: str) -> str:
    """Extract the main topic from a brief, removing style/duration instructions."""
    # Remove style/technical keywords (English, Chinese, Japanese, Korean)
    style_pattern = (
        r"(high[- ]?end|cinematic|professional|style|aspect|ratio|duration|seconds|fps|resolution"
        r"|高清|电影感|专业|风格|时长|分辨率"
        r"|シネマティック|プロフェッショナル|スタイル|解像度"
        r"|시네마틱|프로페셔널|스타일|해상도)[^.。！？!？]*[.。！？!？]"
    )
    cleaned = re.sub(style_pattern, "", brief, flags=re.I)
    time_pattern = r"\d+\s*[-–]?\s*\d*\s*(second|sec|minute|min|fps|秒|分钟|セカンド|ミニート|초|분)[^.。！？!？]*[.。！？!？]"
    cleaned = re.sub(time_pattern, "", cleaned, flags=re.I)
    # Remove prompt prefixes
    prefix_pattern = (
        r"(video|theme|topic|title|subject|brief|视频|主题|标题|動画|テーマ|タイトル|비디오|주제|제목)\s*[:：-]\s*"
    )
    cleaned = re.sub(prefix_pattern, "", cleaned.strip(), flags=re.I)
    verb_pattern = r"^(create|make|build|generate|turn|制作|创建|生成|作成|構築|생성|만들기)\s*"
    cleaned = re.sub(verb_pattern, "", cleaned, flags=re.I)
    # Remove sentences that are just instructions
    cleaned = re.sub(r"[^.。!！?？؟।]*[.。!！?？؟।]", "", cleaned)
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    if not cleaned:
        return ""
    # Try CJK phrases, then non-Latin words, then English words
    cjk = _extract_cjk_phrases(cleaned, 8)
    if cjk:
        return " ".join(cjk[:4])
    non_latin = _extract_non_latin_words(cleaned, 8)
    if non_latin:
        return " ".join(non_latin[:4])
    words = cleaned.split()
    return " ".join(words[:6]).strip(" .,:;")


def _deduplicate_words(words: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for word in words:
        key = word.lower().strip(".,:;!?")
        if key not in seen and len(key) > 1:
            seen.add(key)
            result.append(word)
    return result


def _generated_visual(project: dict, frame: dict, index: int) -> str:
    template = str(project.get("template") or "")
    raw_words = _slug_words(str(frame.get("caption") or project.get("brief") or ""), 12)
    words = _deduplicate_words(raw_words)
    if not words:
        words = ["Video", "Studio"]
    label = _html_escape(frame.get("headline") or frame.get("role") or "Scene")
    chips = "".join(f"<span>{_html_escape(word)}</span>" for word in words[:5])
    number = f"{index + 1:02d}"
    if template == "data_story":
        bars = "".join(
            f'<i style="--bar:{min(92, 32 + i * 14)}%"><b>{_html_escape(words[i % len(words)] if words else "KPI")}</b></i>'
            for i in range(4)
        )
        return f'<div class="visual-panel data-panel"><strong>{label}</strong><div class="bars">{bars}</div><em>{number}</em></div>'
    if template in {"explainer", "feature_demo", "changelog"}:
        nodes = "".join(f"<span>{_html_escape(word)}</span>" for word in words[:4])
        return f'<div class="visual-panel diagram-panel"><strong>{label}</strong><div class="nodes">{nodes}</div><em>{number}</em></div>'
    if template == "minimalist_quote":
        quote = _html_escape(" ".join(words[:9]) or label)
        return f'<div class="visual-panel quote-panel"><strong>“{quote}”</strong><em>{number}</em></div>'
    return f'<div class="visual-panel card-panel"><strong>{label}</strong><div class="chips">{chips}</div><em>{number}</em></div>'


def resolve_assets(assets: list[str], embed: bool) -> list[dict]:
    ASSET_DIR.mkdir(parents=True, exist_ok=True)
    resolved = []
    for asset in assets:
        path = _resolve_path(asset)
        resolved.append(_asset_to_payload(path, embed))
    return resolved


def _media_kind(asset: dict) -> str:
    mime = str(asset.get("mime") or "")
    if mime.startswith("image/"):
        return "image"
    if mime.startswith("audio/"):
        return "audio"
    if mime.startswith("video/"):
        return "video"
    return "other"


def _copy_render_assets(project: dict, html_dir: Path) -> tuple[list[dict], dict]:
    asset_out_dir = html_dir / "assets"
    asset_out_dir.mkdir(parents=True, exist_ok=True)
    copied = []
    used_names: set[str] = set()
    for asset in project.get("assets", []):
        source = Path(str(asset.get("source", "")))
        item = dict(asset)
        item["render_src"] = None
        if source.exists() and source.is_file() and _media_kind(asset) in {"image", "video"}:
            name = source.name
            stem = source.stem
            suffix = source.suffix
            index = 1
            while name in used_names:
                name = f"{stem}-{index}{suffix}"
                index += 1
            used_names.add(name)
            target = asset_out_dir / name
            shutil.copy2(source, target)
            item["render_src"] = f"assets/{name}"
        copied.append(item)

    audio_info = dict(project.get("audio") or {})
    audio_path = Path(str(audio_info.get("path") or ""))
    if audio_path.exists() and audio_path.is_file():
        audio_name = audio_path.name
        target = asset_out_dir / audio_name
        if target.resolve() != audio_path.resolve():
            shutil.copy2(audio_path, target)
        audio_info["render_src"] = f"assets/{audio_name}"
    else:
        audio_info["render_src"] = None
    return copied, audio_info


def _get_layout(template_key: str) -> str:
    """Map template to layout type."""
    layout_map = {
        "product_launch": "split_full",
        "feature_demo": "timeline_flow",
        "data_story": "stats_grid",
        "minimalist_quote": "hero_center",
        "explainer": "step_flow",
        "before_after": "testimonial_card",
        "customer_testimonial": "testimonial_card",
        "event_promo": "banner_announce",
        "changelog": "timeline_flow",
        "ecommerce_promo": "stats_grid",
        "cinematic_hero": "hero_center",
        "split_showcase": "split_full",
        "step_by_step": "timeline_flow",
        "metrics_dashboard": "stats_grid",
        "social_card": "hero_center",
        "announcement": "banner_announce",
    }
    return layout_map.get(template_key, "split_grid")


def _layout_css(layout: str, width: int, height: int, font: str) -> str:
    """Return layout-specific CSS."""
    common = f'''
    * {{ box-sizing: border-box; margin: 0; }}
    html, body {{ width: 100%; height: 100%; overflow: hidden; background: var(--bg); color: var(--fg);
      font-family: {font}, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; }}
    body {{ width: var(--w); height: var(--h); transform-origin: top left; }}
    .scene {{ position: absolute; inset: 0; overflow: hidden; pointer-events: none; }}
    .progress {{ position: absolute; left: 0; bottom: 0; height: 8px; width: 100%; transform: scaleX(0); transform-origin: left center; background: linear-gradient(90deg, var(--accent), var(--accent-2)); z-index: 8; border-radius: 0 4px 0 0; }}
    .eyebrow {{ margin: 0 0 20px; color: var(--accent); font-size: clamp(18px, 1.6vw, 32px); font-weight: 700; text-transform: uppercase; letter-spacing: 0.08em; }}
    h1 {{ margin: 0; font-size: clamp(56px, 5.6vw, 120px); line-height: 1.0; letter-spacing: -0.02em; text-wrap: balance; }}
    .caption {{ margin: 24px 0 0; max-width: 820px; font-size: clamp(24px, 2vw, 42px); line-height: 1.3; color: color-mix(in srgb, var(--fg) 70%, transparent); }}
    .visual {{ width: 100%; height: 100%; object-fit: cover; }}'''

    if layout == "hero_center":
        return common + """
    #main { position: relative; width: var(--w); height: var(--h); overflow: hidden; isolation: isolate;
      background: var(--bg); }
    .hero-glow { position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%);
      width: 120%; height: 120%; pointer-events: none; z-index: 0;
      background: radial-gradient(ellipse at 50% 50%, color-mix(in srgb, var(--accent) 22%, transparent) 0%, transparent 55%); }
    .hero-line { position: absolute; bottom: 20%; left: 50%; transform: translateX(-50%);
      width: 180px; height: 2px; background: linear-gradient(90deg, transparent, var(--accent), transparent); opacity: 0.5; z-index: 1; }
    .scene-content { position: absolute; inset: 0; display: flex; flex-direction: column; align-items: center; justify-content: center;
      padding: 12%; text-align: center; z-index: 2; }
    .copy { max-width: 88%; }
    h1 { font-size: clamp(68px, 7.2vw, 160px); letter-spacing: -0.03em; font-weight: 800; }
    .caption { margin: 36px auto 0; max-width: 680px; font-size: clamp(26px, 2.4vw, 48px); line-height: 1.25; }
    @media (max-aspect-ratio: 1/1) { h1 { font-size: clamp(44px, 9vw, 110px); } }"""

    if layout == "split_full":
        return common + """
    #main { position: relative; width: var(--w); height: var(--h); overflow: hidden; isolation: isolate; background: var(--bg); }
    .scene-content { position: absolute; inset: 0; display: grid; grid-template-columns: 1fr 1fr; z-index: 2; }
    .copy { display: flex; flex-direction: column; justify-content: center; padding: 10% 8% 10% 10%; }
    h1 { font-size: clamp(48px, 4.8vw, 104px); }
    .visual-block { position: relative; overflow: hidden; background: color-mix(in srgb, var(--bg) 85%, #000); }
    .visual-block img { width: 100%; height: 100%; object-fit: cover; }
    .visual-fallback { position: absolute; inset: 0; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 32px;
      background: radial-gradient(circle at 60% 40%, color-mix(in srgb, var(--accent) 15%, transparent), transparent 50%),
                  linear-gradient(135deg, color-mix(in srgb, var(--bg) 92%, #000), color-mix(in srgb, var(--bg) 80%, #000)); }
    .visual-fallback .vf-number { font-size: clamp(120px, 12vw, 280px); font-weight: 900; line-height: 1;
      background: linear-gradient(135deg, color-mix(in srgb, var(--accent) 20%, transparent), color-mix(in srgb, var(--accent-2) 15%, transparent));
      -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; }
    .visual-fallback .vf-chips { display: flex; flex-wrap: wrap; gap: 12px; justify-content: center; max-width: 80%; }
    .visual-fallback .vf-chip { padding: 10px 18px; border-radius: 10px; font-size: clamp(16px, 1.4vw, 26px); font-weight: 600;
      border: 1px solid color-mix(in srgb, var(--accent) 30%, transparent);
      background: color-mix(in srgb, var(--accent) 10%, transparent);
      color: color-mix(in srgb, var(--accent) 80%, var(--fg)); }
    @media (max-aspect-ratio: 1/1) { .scene-content { grid-template-columns: 1fr; grid-template-rows: 1fr 1fr; } .copy { padding: 6%; } }"""

    if layout == "timeline_flow":
        return common + """
    #main { position: relative; width: var(--w); height: var(--h); overflow: hidden; isolation: isolate;
      background: var(--bg); }
    .tl-glow { position: absolute; top: 0; right: 0; width: 60%; height: 60%; pointer-events: none; z-index: 0;
      background: radial-gradient(circle at 80% 20%, color-mix(in srgb, var(--accent) 15%, transparent), transparent 45%); }
    .tl-line { position: absolute; top: 18%; left: 8%; right: 8%; height: 3px; z-index: 1;
      background: linear-gradient(90deg, var(--accent), color-mix(in srgb, var(--accent) 20%, transparent)); opacity: 0.3; border-radius: 2px; }
    .tl-dot { position: absolute; top: 18%; width: 14px; height: 14px; border-radius: 50%; background: var(--accent); z-index: 1; transform: translate(-50%, -50%); }
    .tl-dot-1 { left: 20%; }
    .tl-dot-2 { left: 50%; }
    .tl-dot-3 { left: 80%; }
    .scene-content { position: absolute; inset: 0; display: flex; flex-direction: column; justify-content: center; padding: 10% 10% 10% 10%; z-index: 2; }
    .copy { max-width: 65%; }
    .step-number { font-size: clamp(100px, 10vw, 220px); font-weight: 900; line-height: 1; margin-bottom: 16px;
      background: linear-gradient(135deg, var(--accent), var(--accent-2)); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; opacity: 0.7; }
    .caption { margin: 20px 0 0; font-size: clamp(22px, 1.8vw, 38px); }
    @media (max-aspect-ratio: 1/1) { .copy { max-width: 92%; } h1 { font-size: clamp(40px, 7vw, 90px); } }"""

    if layout == "stats_grid":
        return common + """
    #main { position: relative; width: var(--w); height: var(--h); overflow: hidden; isolation: isolate;
      background: linear-gradient(160deg, color-mix(in srgb, var(--bg) 95%, #000), var(--bg)); }
    .scene-content { position: absolute; inset: 0; display: grid; grid-template-columns: 1fr 1fr; grid-template-rows: 1fr 1fr; gap: 4%; padding: 7%; z-index: 2; }
    .stat-card { display: flex; flex-direction: column; justify-content: center; padding: 7% 8%; border-radius: 20px;
      background: color-mix(in srgb, var(--fg) 6%, transparent);
      border: 1px solid color-mix(in srgb, var(--fg) 10%, transparent);
      box-shadow: 0 8px 32px color-mix(in srgb, #000 15%, transparent); }
    .stat-number { font-size: clamp(56px, 5.2vw, 120px); font-weight: 900; line-height: 1;
      background: linear-gradient(135deg, var(--accent), var(--accent-2)); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; }
    h1 { font-size: clamp(28px, 2.6vw, 52px); margin-top: 8px; font-weight: 700; }
    .stat-label { font-size: clamp(18px, 1.6vw, 32px); color: color-mix(in srgb, var(--fg) 55%, transparent); margin-top: 6px; }
    @media (max-aspect-ratio: 1/1) { .scene-content { grid-template-columns: 1fr; grid-template-rows: repeat(4, 1fr); } }"""

    if layout == "testimonial_card":
        return common + """
    #main { position: relative; width: var(--w); height: var(--h); overflow: hidden; isolation: isolate;
      background: var(--bg); }
    .quote-glow { position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%);
      width: 80%; height: 80%; pointer-events: none; z-index: 0;
      background: radial-gradient(ellipse at 50% 50%, color-mix(in srgb, var(--accent) 12%, transparent), transparent 55%); }
    .scene-content { position: absolute; inset: 0; display: flex; flex-direction: column; align-items: center; justify-content: center;
      padding: 12%; text-align: center; z-index: 2; }
    .copy { max-width: 80%; }
    .quote-mark { font-size: clamp(100px, 9vw, 200px); line-height: 0.5; opacity: 0.25; font-family: Georgia, "Times New Roman", serif;
      color: var(--accent); margin-bottom: 20px; }
    h1 { font-size: clamp(48px, 4.8vw, 104px); font-style: italic; line-height: 1.12; font-weight: 600; }
    .caption { margin: 32px auto 0; font-size: clamp(22px, 2vw, 38px); color: color-mix(in srgb, var(--fg) 60%, transparent); }
    .attribution { margin-top: 40px; font-size: clamp(20px, 1.8vw, 34px); color: var(--accent); font-weight: 600; letter-spacing: 0.02em; }
    @media (max-aspect-ratio: 1/1) { h1 { font-size: clamp(36px, 7vw, 80px); } }"""

    if layout == "step_flow":
        return common + """
    #main { position: relative; width: var(--w); height: var(--h); overflow: hidden; isolation: isolate;
      background: var(--bg); }
    .step-glow { position: absolute; left: 0; top: 0; width: 40%; height: 100%; pointer-events: none; z-index: 0;
      background: linear-gradient(90deg, color-mix(in srgb, var(--accent) 10%, transparent), transparent); }
    .scene-content { position: absolute; inset: 0; display: grid; grid-template-columns: 0.32fr 0.68fr; align-items: center; padding: 8%; z-index: 2; }
    .step-number { font-size: clamp(160px, 16vw, 360px); font-weight: 900; text-align: center; line-height: 0.85;
      background: linear-gradient(180deg, var(--accent), color-mix(in srgb, var(--accent) 30%, transparent));
      -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; opacity: 0.55; }
    .copy { padding-left: 8%; }
    h1 { font-size: clamp(44px, 4.2vw, 92px); }
    @media (max-aspect-ratio: 1/1) { .scene-content { grid-template-columns: 1fr; grid-template-rows: auto 1fr; } .step-number { font-size: clamp(100px, 20vw, 200px); } .copy { padding-left: 0; text-align: center; } }"""

    if layout == "banner_announce":
        return common + """
    #main { position: relative; width: var(--w); height: var(--h); overflow: hidden; isolation: isolate;
      background: var(--bg); }
    .banner-glow { position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%);
      width: 100%; height: 80%; pointer-events: none; z-index: 0;
      background: radial-gradient(ellipse at 50% 50%, color-mix(in srgb, var(--accent) 20%, transparent), transparent 50%); }
    .scene-content { position: absolute; inset: 0; display: flex; flex-direction: column; align-items: center; justify-content: center;
      padding: 10%; text-align: center; z-index: 2; }
    .copy { max-width: 82%; }
    h1 { font-size: clamp(56px, 6vw, 140px); letter-spacing: -0.02em; }
    .banner-line { width: clamp(80px, 8vw, 160px); height: 3px; background: linear-gradient(90deg, var(--accent), var(--accent-2));
      margin: 28px auto; border-radius: 2px; }
    .caption { margin: 0 auto; font-size: clamp(22px, 2vw, 40px); }
    @media (max-aspect-ratio: 1/1) { h1 { font-size: clamp(40px, 8vw, 100px); } }"""

    # split_grid (fallback)
    return common + """
    #main { position: relative; width: var(--w); height: var(--h); overflow: hidden; isolation: isolate;
      background: var(--bg); }
    .backdrop { position: absolute; inset: 0; background:
      linear-gradient(90deg, color-mix(in srgb, var(--accent) 8%, transparent), transparent 50%),
      repeating-linear-gradient(90deg, transparent 0 80px, color-mix(in srgb, var(--fg) 4%, transparent) 80px 81px); opacity: 0.6; }
    .scene-content { position: absolute; inset: 0; display: grid; grid-template-columns: 1.02fr .98fr; gap: 4%; align-items: center; padding: 7%; z-index: 2; }
    .copy { max-width: 92%; }
    .visual-block { position: relative; aspect-ratio: 4 / 3; display: grid; place-items: center;
      border: 1px solid color-mix(in srgb, var(--fg) 14%, transparent); border-radius: 20px;
      background: linear-gradient(135deg, color-mix(in srgb, var(--fg) 8%, transparent), color-mix(in srgb, var(--accent) 8%, transparent));
      box-shadow: 0 32px 80px color-mix(in srgb, #000 25%, transparent); overflow: hidden; }
    .visual-panel { width: 100%; height: 100%; padding: 8%; display: flex; flex-direction: column; justify-content: space-between;
      background: radial-gradient(circle at 20% 12%, color-mix(in srgb, var(--accent) 22%, transparent), transparent 34%),
                  linear-gradient(160deg, color-mix(in srgb, var(--fg) 8%, transparent), color-mix(in srgb, var(--bg) 70%, transparent)); }
    .visual-panel strong { font-size: clamp(30px, 2.8vw, 58px); line-height: 1.05; max-width: 86%; font-weight: 700; }
    .visual-panel em { align-self: flex-end; font-style: normal; font-size: clamp(48px, 4.5vw, 100px); font-weight: 850;
      background: linear-gradient(135deg, var(--accent), var(--accent-2)); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; }
    .chips { display: flex; flex-wrap: wrap; gap: 12px; max-width: 90%; }
    .chips span { padding: 10px 14px; border-radius: 8px; border: 1px solid color-mix(in srgb, var(--fg) 18%, transparent);
      background: color-mix(in srgb, var(--bg) 50%, transparent); font-size: clamp(18px, 1.4vw, 28px); }
    @media (max-aspect-ratio: 1/1) { .scene-content { grid-template-columns: 1fr; } .visual-block { width: 100%; align-self: end; } }"""


def _layout_frame_html(layout: str, index: int, frame: dict, project: dict, visual_html: str, media_html: str) -> str:
    """Generate frame HTML based on layout type."""
    start = float(frame.get("start", 0))
    scene_duration = float(frame.get("duration", 1))
    headline = _html_escape(frame.get("headline") or "")
    caption = _html_escape(frame.get("caption") or "")
    eyebrow = _html_escape(project.get("template_name") or "")

    if layout == "hero_center":
        return f'''
      <div id="scene-{index}" class="clip scene" data-start="{start:.3f}" data-duration="{scene_duration:.3f}" data-track-index="{index + 1}">
        <div class="hero-glow"></div>
        <div class="hero-line"></div>
        <div class="scene-content">
          <div class="copy">
            <h1>{headline}</h1>
            <p class="caption">{caption}</p>
          </div>
        </div>
      </div>'''

    if layout == "split_full":
        if media_html:
            visual_content = media_html
        else:
            raw_words = _slug_words(str(frame.get("caption") or project.get("brief") or ""), 8)
            words = _deduplicate_words(raw_words)[:6]
            if not words:
                words = ["Product", "Launch"]
            chips_html = "".join(f'<span class="vf-chip">{_html_escape(w)}</span>' for w in words)
            number = f"{index + 1:02d}"
            visual_content = f'''<div class="visual-fallback">
            <div class="vf-number">{number}</div>
            <div class="vf-chips">{chips_html}</div>
          </div>'''
        return f'''
      <div id="scene-{index}" class="clip scene" data-start="{start:.3f}" data-duration="{scene_duration:.3f}" data-track-index="{index + 1}">
        <div class="scene-content">
          <div class="copy">
            <p class="eyebrow">{eyebrow}</p>
            <h1>{headline}</h1>
            <p class="caption">{caption}</p>
          </div>
          <div class="visual-block">{visual_content}</div>
        </div>
      </div>'''

    if layout == "timeline_flow":
        return f'''
      <div id="scene-{index}" class="clip scene" data-start="{start:.3f}" data-duration="{scene_duration:.3f}" data-track-index="{index + 1}">
        <div class="tl-glow"></div>
        <div class="tl-line"></div>
        <div class="tl-dot tl-dot-1"></div>
        <div class="tl-dot tl-dot-2"></div>
        <div class="tl-dot tl-dot-3"></div>
        <div class="scene-content">
          <div class="copy">
            <div class="step-number">{index + 1:02d}</div>
            <h1>{headline}</h1>
            <p class="caption">{caption}</p>
          </div>
        </div>
      </div>'''

    if layout == "stats_grid":
        words = _slug_words(str(frame.get("caption") or ""), 4)
        stat_value = words[0] if words else "—"
        return f'''
      <div id="scene-{index}" class="clip scene" data-start="{start:.3f}" data-duration="{scene_duration:.3f}" data-track-index="{index + 1}">
        <div class="scene-content">
          <div class="stat-card">
            <span class="stat-number">{_html_escape(stat_value)}</span>
            <h1>{headline}</h1>
            <p class="caption">{caption}</p>
          </div>
        </div>
      </div>'''

    if layout == "testimonial_card":
        return f'''
      <div id="scene-{index}" class="clip scene" data-start="{start:.3f}" data-duration="{scene_duration:.3f}" data-track-index="{index + 1}">
        <div class="quote-glow"></div>
        <div class="scene-content">
          <div class="copy">
            <div class="quote-mark">"</div>
            <h1>{headline}</h1>
            <p class="caption">{caption}</p>
          </div>
        </div>
      </div>'''

    if layout == "step_flow":
        return f'''
      <div id="scene-{index}" class="clip scene" data-start="{start:.3f}" data-duration="{scene_duration:.3f}" data-track-index="{index + 1}">
        <div class="step-glow"></div>
        <div class="scene-content">
          <div class="step-number">{index + 1}</div>
          <div class="copy">
            <p class="eyebrow">{eyebrow}</p>
            <h1>{headline}</h1>
            <p class="caption">{caption}</p>
          </div>
        </div>
      </div>'''

    if layout == "banner_announce":
        return f'''
      <div id="scene-{index}" class="clip scene" data-start="{start:.3f}" data-duration="{scene_duration:.3f}" data-track-index="{index + 1}">
        <div class="banner-glow"></div>
        <div class="scene-content">
          <div class="copy">
            <p class="eyebrow">{eyebrow}</p>
            <h1>{headline}</h1>
            <div class="banner-line"></div>
            <p class="caption">{caption}</p>
          </div>
        </div>
      </div>'''

    # split_grid fallback
    return f'''
      <div id="scene-{index}" class="clip scene" data-start="{start:.3f}" data-duration="{scene_duration:.3f}" data-track-index="{index + 1}">
        <div class="backdrop"></div>
        <div class="scene-content">
          <div class="copy">
            <p class="eyebrow">{eyebrow}</p>
            <h1>{headline}</h1>
            <p class="caption">{caption}</p>
          </div>
          <div class="visual-block">{visual_html}</div>
        </div>
      </div>'''


def _generated_visual(project: dict, frame: dict, index: int) -> str:
    """Generate visual panel content. Only used for split_grid fallback layout."""
    template = str(project.get("template") or "")
    raw_words = _slug_words(str(frame.get("caption") or project.get("brief") or ""), 12)
    words = _deduplicate_words(raw_words)
    if not words:
        words = ["Video", "Studio"]
    chips = "".join(f"<span>{_html_escape(word)}</span>" for word in words[:5])
    number = f"{index + 1:02d}"
    if template == "data_story":
        bars = "".join(
            f'<i style="--bar:{min(92, 32 + i * 14)}%"><b>{_html_escape(words[i % len(words)] if words else "KPI")}</b></i>'
            for i in range(4)
        )
        return f'<div class="visual-panel data-panel"><div class="bars">{bars}</div><em>{number}</em></div>'
    if template in {"explainer", "feature_demo", "changelog"}:
        nodes = "".join(f"<span>{_html_escape(word)}</span>" for word in words[:4])
        return f'<div class="visual-panel diagram-panel"><div class="nodes">{nodes}</div><em>{number}</em></div>'
    if template == "minimalist_quote":
        quote = _html_escape(" ".join(words[:6]) or "")
        return f'<div class="visual-panel quote-panel"><strong>{quote}</strong><em>{number}</em></div>'
    return f'<div class="visual-panel card-panel"><div class="chips">{chips}</div><em>{number}</em></div>'


def _render_html(project: dict, html_dir: Path) -> Path:
    copied_assets, audio_info = _copy_render_assets(project, html_dir)
    width = int(project["resolution"]["width"])
    height = int(project["resolution"]["height"])
    duration = float(project["duration"])
    fps = int(project.get("fps", 30))
    template_key = str(project.get("template") or "")
    layout = _get_layout(template_key)
    palette = list((project.get("style") or {}).get("palette") or ["#0B0F19", "#F8FAFC", "#22D3EE", "#A3E635"])
    while len(palette) < 4:
        palette.append(palette[-1])
    font = str((project.get("style") or {}).get("font") or "Inter")

    image_assets = [asset for asset in copied_assets if _media_kind(asset) == "image" and asset.get("render_src")]
    frames = [_frame_copy(frame, project, index) for index, frame in enumerate(project.get("frames", []))]
    title = project.get("title") or project.get("template_name") or "Hyperframes Video Studio"
    audio_tag = ""
    if audio_info.get("render_src"):
        audio_tag = (
            f'<audio id="narration" src="{_html_escape(audio_info["render_src"])}" '
            f'data-start="0" data-duration="{duration:.3f}" data-track-index="{len(frames) + 2}" '
            'data-volume="1" preload="auto"></audio>'
        )

    frame_html = []
    for index, frame in enumerate(frames):
        media = image_assets[index % len(image_assets)] if image_assets else None
        media_src = f'<img class="visual" src="{_html_escape(media["render_src"])}" alt="">' if media else ""
        visual_html = _generated_visual(project, frame, index)
        frame_html.append(_layout_frame_html(layout, index, frame, project, visual_html, media_src))

    layout_css = _layout_css(layout, width, height, font)

    # Layout-specific GSAP targets (list of class selectors per layout)
    if layout == "hero_center":
        gsap_classes = [".copy"]
    elif layout == "split_full":
        gsap_classes = [".copy", ".visual-block"]
    elif layout == "stats_grid":
        gsap_classes = [".stat-card"]
    elif layout == "step_flow":
        gsap_classes = [".step-number", ".copy"]
    elif layout == "testimonial_card":
        gsap_classes = [".copy"]
    elif layout == "banner_announce":
        gsap_classes = [".copy"]
    else:
        gsap_classes = [".copy", ".visual-block"]

    def _gsap_sel(scene_id: str | None, classes: list[str]) -> str:
        """Build GSAP selector with optional scene ID prefix for each class."""
        if scene_id:
            prefix = f"#{scene_id} " if not scene_id.startswith(".") else f"{scene_id} "
        else:
            prefix = ""
        return ", ".join(f"{prefix}{c}" for c in classes)

    gsap_hide = _gsap_sel(".scene", gsap_classes)
    gsap_show0 = _gsap_sel("scene-0", gsap_classes)

    html = f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="hyperframes:duration" content="{duration:.3f}">
  <meta name="hyperframes:fps" content="{fps}">
  <meta name="hyperframes:width" content="{width}">
  <meta name="hyperframes:height" content="{height}">
  <title>{_html_escape(title)}</title>
  <style>
    :root {{
      --w: {width}px;
      --h: {height}px;
      --duration: {duration:.3f}s;
      --bg: {_css_string(palette[0])};
      --fg: {_css_string(palette[1])};
      --accent: {_css_string(palette[2])};
      --accent-2: {_css_string(palette[3])};
    }}
    {layout_css}
  </style>
</head>
<body>
  <div id="main" data-composition-id="main" data-start="0" data-duration="{duration:.3f}" data-width="{width}" data-height="{height}">
    {"".join(frame_html)}
    <div class="progress"></div>
    {audio_tag}
  </div>
  <script id="video-project" type="application/json">{_script_json(project)}</script>
  <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
  <script>
    window.__timelines = window.__timelines || {{}};
    const tl = gsap.timeline({{ paused: true }});
    tl.set("{gsap_hide}", {{ opacity: 0, x: 0, y: 0, scale: 1 }}, 0);
    tl.set("{gsap_show0}", {{ opacity: 1 }}, 0);
    tl.fromTo(".progress", {{ scaleX: 0, transformOrigin: "left center" }}, {{ scaleX: 1, duration: {duration:.6f}, ease: "none" }}, 0);
'''
    for index, frame in enumerate(frames):
        start = float(frame.get("start", 0))
        scene_duration = float(frame.get("duration", 1))
        scene_end = start + scene_duration
        exit_time = start + scene_duration - 0.4
        if exit_time < start + 0.05:
            exit_time = start + 0.05
        scene_sel = _gsap_sel(f"scene-{index}", gsap_classes)
        html += f'''
    tl.fromTo("{scene_sel}", {{ y: 40, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.5, ease: "power3.out" }}, {start:.3f});
    tl.to("{scene_sel}", {{ y: -25, opacity: 0, duration: 0.4, ease: "power2.in" }}, {exit_time:.3f});
    tl.set("{scene_sel}", {{ opacity: 0 }}, {scene_end:.3f});
'''
    html += f'''
    window.__timelines["main"] = tl;
  </script>
</body>
</html>
'''
    html_dir.mkdir(parents=True, exist_ok=True)
    html_path = html_dir / "index.html"
    html_path.write_text(html, encoding="utf-8")
    (html_dir / "project.json").write_text(json.dumps(project, indent=2, sort_keys=True), encoding="utf-8")
    return html_path


def _load_manifest(path_value: str) -> dict | None:
    path = _resolve_path(path_value)
    if not path.exists():
        return None
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def _assets_from_manifest(manifest: dict | None) -> list[str]:
    if not manifest:
        return []
    values = []
    for item in manifest.get("items", []):
        if item.get("kind") in {"image", "audio", "video", "document", "text"} and item.get("path"):
            values.append(item["path"])
    return values


def _content_brief_from_manifest(manifest: dict | None) -> str:
    if not manifest:
        return ""
    excerpts = []
    for item in manifest.get("items", []):
        text = str(item.get("text_excerpt") or "").strip()
        if text:
            excerpts.append(f"{item.get('name')}: {text[:800]}")
        if len(excerpts) >= 8:
            break
    return "\n".join(excerpts)


def _wav_duration(path: Path) -> float | None:
    try:
        with wave.open(str(path), "rb") as handle:
            return handle.getnframes() / float(handle.getframerate())
    except Exception:
        return None


def _ffprobe_duration(path: Path) -> float | None:
    ffprobe = shutil.which("ffprobe")
    if not ffprobe or not path.exists():
        return _wav_duration(path)
    command = [
        ffprobe,
        "-v",
        "error",
        "-show_entries",
        "format=duration",
        "-of",
        "default=noprint_wrappers=1:nokey=1",
        str(path),
    ]
    try:
        return float(subprocess.check_output(command, text=True).strip())
    except Exception:
        return _wav_duration(path)


def _scale_frames(frames: list[dict], target_duration: float | None) -> list[dict]:
    # Always compute start/end times for each frame
    if target_duration:
        current = sum(float(frame["duration"]) for frame in frames)
        if current > 0:
            scale = target_duration / current
        else:
            scale = 1.0
    else:
        scale = 1.0

    result = []
    start = 0.0
    for frame in frames:
        duration = round(max(0.5, float(frame["duration"]) * scale), 3)
        item = dict(frame)
        item["duration"] = duration
        item["start"] = round(start, 3)
        start += duration
        item["end"] = round(start, 3)
        result.append(item)
    return result


def _resolution_for_aspect(aspect_ratio: str | None, default: dict) -> dict:
    mapping = {
        "16:9": {"width": 1920, "height": 1080},
        "9:16": {"width": 1080, "height": 1920},
        "1:1": {"width": 1080, "height": 1080},
        "4:5": {"width": 1080, "height": 1350},
    }
    return mapping.get(str(aspect_ratio or ""), default)


def build_project(request: dict) -> dict:
    templates = load_templates()
    template_key = request.get("template")
    if template_key not in templates:
        return {
            "status": "invalid_request",
            "message": f"Unknown template '{template_key}'.",
            "templates": sorted(templates),
        }

    template = templates[template_key]
    asset_manifest = None
    if request.get("asset_manifest"):
        asset_manifest = _load_manifest(str(request["asset_manifest"]))

    manifest_brief = _content_brief_from_manifest(asset_manifest)
    brief = str(request.get("brief", "")).strip()
    if manifest_brief:
        brief = f"{brief}\n\nSource material excerpts:\n{manifest_brief}".strip()
    if not brief:
        return {"status": "invalid_request", "message": "Missing non-empty brief."}

    audio = request.get("audio")
    audio_path = _resolve_path(audio) if audio else None
    audio_duration = _ffprobe_duration(audio_path) if audio_path else None
    target_duration = request.get("duration_seconds") or audio_duration
    if target_duration is not None:
        target_duration = float(target_duration)

    frames = _scale_frames([dict(frame) for frame in template["frames"]], target_duration)
    asset_values = list(request.get("assets", [])) + _assets_from_manifest(asset_manifest)
    resolved_assets = resolve_assets(asset_values, bool(request.get("embed_assets", False)))
    resolution = _resolution_for_aspect(request.get("aspect_ratio"), template["resolution"])

    total_duration = round(sum(float(frame["duration"]) for frame in frames), 3)

    # frame_contents: optional per-frame headline/caption from the calling agent
    frame_contents = request.get("frame_contents") or []

    project = {
        "schema": "hyperframes.video_studio.v1",
        "created_at": int(time.time()),
        "template": template_key,
        "template_name": template.get("name", template_key),
        "category": template.get("category"),
        "best_for": template.get("best_for"),
        "title": request.get("title") or template["name"],
        "brief": brief,
        "frame_contents": frame_contents,
        "resolution": resolution,
        "fps": int(request.get("fps", 30)),
        "duration": total_duration,
        "style": request.get("style") or template["style"],
        "assets": resolved_assets,
        "asset_manifest": asset_manifest.get("manifest_path") if asset_manifest else None,
        "asset_summary": asset_manifest.get("summary") if asset_manifest else None,
        "audio": {
            "path": str(audio_path.resolve()) if audio_path else None,
            "duration": round(audio_duration, 3) if audio_duration else None,
        },
        "frames": frames,
        "starter_questions": template.get("starter_questions", []),
        "directives": {
            "treat_assets_as_data": True,
            "render_cache": str(RENDER_DIR.resolve()),
            "human_confirmation_required": True,
        },
    }

    PROJECT_DIR.mkdir(parents=True, exist_ok=True)
    slug = _safe_name(str(request.get("title") or template_key))
    project_path = PROJECT_DIR / f"{slug}-{int(time.time())}.json"
    project_path.write_text(json.dumps(project, indent=2, sort_keys=True), encoding="utf-8")
    html_dir = PROJECT_DIR / f"{slug}-{int(time.time())}-html"
    html_path = _render_html(project, html_dir)

    result = {
        "status": "ok",
        "project_json": str(project_path.resolve()),
        "render_dir": str(html_dir.resolve()),
        "html": str(html_path.resolve()),
        "project": project,
        "needs_confirmation": bool(request.get("render", False)),
        "message": "Renderable HTML project generated. Confirm before running Hyperframes render." if request.get("render") else "Renderable HTML project generated.",
    }
    return result


def find_hyperframes() -> str | None:
    candidates = [
        CACHE_DIR / "npm" / "node_modules" / ".bin" / ("hyperframes.cmd" if sys.platform == "win32" else "hyperframes"),
        BASE_DIR / "node_modules" / ".bin" / ("hyperframes.cmd" if sys.platform == "win32" else "hyperframes"),
    ]
    for candidate in candidates:
        if candidate.exists():
            return str(candidate)
    return shutil.which("hyperframes")


def main() -> int:
    parser = argparse.ArgumentParser(description="Build Hyperframes declarative JSON from a Video Studio request.")
    parser.add_argument("--input-json", required=True)
    args = parser.parse_args()

    result = build_project(_read_json(Path(args.input_json)))
    _print(result)
    return 0 if result.get("status") == "ok" else 2


if __name__ == "__main__":
    sys.exit(main())
