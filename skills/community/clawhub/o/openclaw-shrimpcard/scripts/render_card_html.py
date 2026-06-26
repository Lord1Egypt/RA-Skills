#!/usr/bin/env python3
import argparse
import base64
import html
import json
import mimetypes
import re
from copy import deepcopy
from pathlib import Path

from selfie_styles import get_role_style
from skill_paths import CARD_TEMPLATE_PATH, SHARE_CARD_SCHEMA_PATH
from validate_final_bundle import validate_final_bundle
from validate_json import validate


def load_json(path: Path):
    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def file_to_data_url(path: Path) -> str:
    mime_type = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
    encoded = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:{mime_type};base64,{encoded}"


def resolve_local_asset_url(value: str, base_dir: Path | None = None) -> str:
    if value.startswith(("http://", "https://", "data:")):
        return value

    candidate = Path(value)
    candidates = []
    if candidate.is_absolute():
        candidates.append(candidate)
    else:
        candidates.append(candidate)
        if base_dir is not None:
            candidates.append(base_dir / candidate)

    for item in candidates:
        if item.exists() and item.is_file():
            return file_to_data_url(item)
    return value


def inline_local_assets(card: dict, base_dir: Path | None = None) -> dict:
    rendered = deepcopy(card)
    for field in ["image", "qr"]:
        asset = rendered.get(field)
        if isinstance(asset, str) and asset:
            resolved = resolve_local_asset_url(asset, base_dir)
            if resolved.startswith("data:"):
                rendered[field] = {"data_url": resolved}
            continue
        if not isinstance(asset, dict):
            continue

        data_url = asset.get("data_url")
        url = asset.get("url")
        if data_url or not url:
            continue

        resolved = resolve_local_asset_url(url, base_dir)
        if resolved.startswith("data:"):
            updated = dict(asset)
            updated["data_url"] = resolved
            rendered[field] = updated
    return rendered


def normalize_card_payload(card: dict, base_dir: Path | None = None) -> dict:
    return inline_local_assets(card, base_dir)


def validate_payload(card: dict):
    validate(card, load_json(SHARE_CARD_SCHEMA_PATH))


def localized_card(card: dict, lang: str = "zh") -> dict:
    localized = card.get("i18n", {}).get(lang, {})
    merged = dict(card)
    if isinstance(localized, dict):
        for field in [
            "role",
            "tagline",
            "value_line",
            "best_for",
            "proof_anchor",
            "spread_line",
            "memory_basis",
            "selfie_prompt",
            "poster_headline",
            "poster_subline",
            "share_caption",
        ]:
            if localized.get(field):
                merged[field] = localized[field]
        for field in ["top_capabilities", "persona_tags", "share_keywords"]:
            if isinstance(localized.get(field), list) and localized.get(field):
                merged[field] = localized[field]
    merged.pop("i18n", None)
    return merged


def replace_tag_content(template: str, tag: str, element_id: str, content: str) -> str:
    pattern = rf'(<{tag}[^>]*id="{element_id}"[^>]*>)(.*?)(</{tag}>)'
    return re.sub(
        pattern,
        lambda match: f"{match.group(1)}{content}{match.group(3)}",
        template,
        count=1,
        flags=re.DOTALL,
    )


def replace_inner_html_by_class(template: str, class_name: str, content: str) -> str:
    pattern = rf'(<div[^>]*class="{class_name}"[^>]*>)(.*?)(</div>)'
    return re.sub(
        pattern,
        lambda match: f"{match.group(1)}{content}{match.group(3)}",
        template,
        count=1,
        flags=re.DOTALL,
    )


def replace_image_tag(template: str, element_id: str, src: str | None) -> str:
    pattern = rf'<img([^>]*id="{element_id}"[^>]*)\s*/?>'
    if src:
        return re.sub(
            pattern,
            lambda match: f'<img{match.group(1)} src="{html.escape(src, quote=True)}" style="display:block;">',
            template,
            count=1,
        )
    return template


def replace_placeholder_visibility(template: str, element_id: str, hidden: bool) -> str:
    pattern = rf'(<div[^>]*id="{element_id}"[^>]*)(>)'
    if hidden:
        return re.sub(
            pattern,
            lambda match: f'{match.group(1)} style="display:none;"{match.group(2)}',
            template,
            count=1,
        )
    return template


def replace_theme_variables(template: str, theme: dict) -> str:
    border = theme.get("border", "#111111")
    background = theme.get("background", "#FFF7DF")
    accent = theme.get("accent", "#FF7548")
    tag_colors = theme.get("tag_colors") if isinstance(theme.get("tag_colors"), list) else []
    tag_1 = tag_colors[0] if len(tag_colors) > 0 else "#FFD865"
    tag_2 = tag_colors[1] if len(tag_colors) > 1 else "#FFB78A"
    tag_3 = tag_colors[2] if len(tag_colors) > 2 else "#9DE2D3"
    style = (
        f'--bg:{html.escape(background, quote=True)};'
        f'--border:{html.escape(border, quote=True)};'
        f'--accent:{html.escape(accent, quote=True)};'
        f'--accent-strong:{html.escape(tag_3, quote=True)};'
        f'--accent-2:{html.escape(tag_3, quote=True)};'
        f'--tag-1:{html.escape(tag_1, quote=True)};'
        f'--tag-2:{html.escape(tag_2, quote=True)};'
        f'--tag-3:{html.escape(tag_3, quote=True)};'
    )
    pattern = r'(<main class="page")(>)'
    return re.sub(
        pattern,
        lambda match: f'{match.group(1)} style="{style}"{match.group(2)}',
        template,
        count=1,
    )


def render_persona_tags(tags: list[str]) -> str:
    colors = ["var(--tag-1)", "var(--tag-2)", "var(--tag-3)"]
    items = []
    for index, tag in enumerate(tags[:3]):
        items.append(
            f'<span class="persona-tag" style="background: {colors[index]};">{html.escape(tag)}</span>'
        )
    return "".join(items)


def render_meta_keywords(keywords: list[str]) -> str:
    return "".join(
        f'<span class="meta-pill">{html.escape(keyword)}</span>'
        for keyword in keywords[:4]
    )


def infer_poster_badge(card: dict) -> str:
    name = str(card.get("name", "")).strip()
    if "ShrimpCard" in name:
        return "ShrimpCard"
    if name and len(name) <= 18:
        return name
    return "Share Card"


def render_owner(owner: dict, lang: str) -> str:
    lines = []
    owner_label = "主人" if lang == "zh" else "DEPLOYED BY"
    if owner.get("name"):
        lines.append(f"<p class=\"owner-line\">{owner_label} {html.escape(owner['name'])}</p>")
    if owner.get("contact"):
        lines.append(f"<p class=\"owner-line\">{html.escape(owner['contact'])}</p>")
    return "".join(lines)


def replace_html_lang(template: str, lang: str) -> str:
    return re.sub(r'(<html lang=")([^"]+)(">)', rf"\1{lang}\3", template, count=1)


def apply_static_card_markup(template: str, card: dict, lang: str) -> str:
    static_card = localized_card(card, lang)
    role_backdrop = get_role_style(static_card.get("role", ""))["backdrop"]
    image_src = None
    image = static_card.get("image")
    if isinstance(image, dict):
        image_src = image.get("data_url") or image.get("url")
    elif isinstance(image, str):
        image_src = image

    photo_pattern = r'(<section class="poster-photo")([^>]*)(>)'
    backdrop = html.escape(role_backdrop, quote=True)
    guide_mode = "true" if not image_src else "false"
    empty_state = "false" if image_src else "true"
    template = re.sub(
        photo_pattern,
        lambda match: (
            f'{match.group(1)} data-role-backdrop="{backdrop}" '
            f'data-guide-mode="{guide_mode}" data-empty="{empty_state}"'
            f'{match.group(2)}{match.group(3)}'
        ),
        template,
        count=1,
    )
    card_pattern = r'(<article class="poster-card"[^>]*id="exportCard"[^>]*)(>)'
    template = re.sub(
        card_pattern,
        lambda match: f'{match.group(1)} data-role-backdrop="{backdrop}" data-guide-mode="{guide_mode}"{match.group(2)}',
        template,
        count=1,
    )
    template = replace_theme_variables(template, static_card.get("theme", {}))

    replacements = {
        ("span", "posterBadge"): html.escape(infer_poster_badge(static_card)),
        ("h1", "name"): html.escape(static_card.get("name", "")),
        ("div", "role"): html.escape(static_card.get("role", "")),
        ("p", "tagline"): html.escape(static_card.get("tagline", "")),
        ("div", "shareCaption"): html.escape(static_card.get("share_caption", "")),
        ("h2", "sideHeadline"): html.escape(
            static_card.get("poster_headline")
            or static_card.get("role", "")
        ),
        ("p", "subheadline"): html.escape(
            static_card.get("poster_subline")
            or static_card.get("value_line")
            or static_card.get("tagline", "")
        ),
        ("div", "bestFor"): html.escape(static_card.get("best_for", "")),
        ("div", "spreadReason"): html.escape(static_card.get("spread_line", "")),
        ("div", "proofAnchor"): html.escape(static_card.get("proof_anchor", "")),
        ("div", "memoryBasis"): html.escape(static_card.get("memory_basis", "")),
        ("pre", "selfiePrompt"): html.escape(static_card.get("selfie_prompt", "")),
    }
    for (tag, element_id), content in replacements.items():
        template = replace_tag_content(template, tag, element_id, content)

    template = replace_tag_content(
        template,
        "div",
        "personaTags",
        render_persona_tags(static_card.get("persona_tags", [])),
    )
    template = replace_tag_content(
        template,
        "div",
        "metaKeywords",
        render_meta_keywords(static_card.get("share_keywords", [])),
    )
    template = replace_tag_content(template, "div", "ownerBlock", render_owner(static_card.get("owner", {}), lang))
    template = replace_image_tag(template, "mainImage", image_src)
    template = replace_placeholder_visibility(template, "photoPlaceholder", bool(image_src))
    return template


def inject_data(template: str, card_data: dict, lang: str) -> str:
    payload = json.dumps(card_data, ensure_ascii=False, indent=2)
    script = "<script>\n" f"window.__CARD_DATA__ = {payload};\n" "</script>\n"
    marker = "<!-- CARD_DATA -->"
    if marker in template:
        return template.replace(marker, script)
    return template.replace("</body>", script + "</body>")


def render_html_from_template(template_text: str, card_data: dict, lang: str) -> str:
    normalized_card = normalize_card_payload(card_data)
    localized_payload = localized_card(normalized_card, lang)
    localized_template = replace_html_lang(template_text, "zh-CN" if lang == "zh" else "en")
    static_markup = apply_static_card_markup(localized_template, localized_payload, lang)
    return inject_data(static_markup, localized_payload, lang)


def main():
    parser = argparse.ArgumentParser(description="Render final share-card HTML from share-card JSON")
    parser.add_argument("card_json", help="Path to share-card JSON")
    parser.add_argument("--out", default="selfie-card.html", help="Output HTML path")
    parser.add_argument(
        "--template",
        default=str(CARD_TEMPLATE_PATH),
        help="HTML template path",
    )
    parser.add_argument(
        "--allow-missing-image-preview",
        action="store_true",
        help="Allow rendering an incomplete preview card without a final attached image",
    )
    parser.add_argument(
        "--lang",
        choices=["zh", "en"],
        default="zh",
        help="Default language to render in the exported HTML",
    )
    args = parser.parse_args()

    card_path = Path(args.card_json)
    template_path = Path(args.template)
    card = normalize_card_payload(load_json(card_path), card_path.parent)
    validate_payload(card)
    if not args.allow_missing_image_preview:
        validate_final_bundle(card, card_path.parent)

    template = template_path.read_text(encoding="utf-8")
    rendered = render_html_from_template(template, card, args.lang)

    out_path = Path(args.out)
    out_path.write_text(rendered, encoding="utf-8")


if __name__ == "__main__":
    main()
