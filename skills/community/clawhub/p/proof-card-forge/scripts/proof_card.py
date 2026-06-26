#!/usr/bin/env python3
import argparse
import html
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import quote


def main():
    parser = argparse.ArgumentParser(description="Generate an SVG and Markdown proof card for a skill.")
    parser.add_argument("--audit", help="Skill Package Doctor audit JSON")
    parser.add_argument("--name")
    parser.add_argument("--description")
    parser.add_argument("--score", type=int)
    parser.add_argument("--grade")
    parser.add_argument("--status")
    parser.add_argument("--version")
    parser.add_argument("--url")
    parser.add_argument("--checked-at")
    parser.add_argument("--out-svg", default="proof-card.svg")
    parser.add_argument("--out-md", default="proof-card.md")
    parser.add_argument("--out-json")
    parser.add_argument("--force", action="store_true", help="Overwrite existing output files")
    args = parser.parse_args()

    card = card_from_args(args)
    write(args.out_svg, render_svg(card), force=args.force)
    write(args.out_md, render_markdown(card, args.out_svg), force=args.force)
    if args.out_json:
        write(args.out_json, json.dumps(card, indent=2) + "\n", force=args.force)
    print(json.dumps(card, indent=2))


def card_from_args(args):
    audit = load_audit(args.audit) if args.audit else {}
    metadata = audit.get("metadata", {}) if isinstance(audit.get("metadata"), dict) else {}
    name = args.name or metadata.get("name") or "skill"
    score = clamp(args.score if args.score is not None else audit.get("score", 0), 0, 100)
    ok = bool(audit.get("ok")) if "ok" in audit else score >= 80
    grade = args.grade or audit.get("grade") or ("publish-ready" if ok else "unchecked")
    status = args.status or ("PASS" if ok else "CHECK")
    checked_at = args.checked_at or audit.get("checkedAt") or datetime.now(timezone.utc).isoformat()
    return {
        "name": safe_text(name, 80),
        "description": safe_text(args.description or metadata.get("description") or "Skill package proof card.", 180),
        "score": score,
        "grade": safe_text(str(grade), 48),
        "status": safe_text(str(status).upper(), 16),
        "version": safe_text(args.version or metadata.get("version") or "not set", 32),
        "url": safe_url(args.url or metadata.get("homepage") or ""),
        "checkedAt": safe_text(str(checked_at), 64),
    }


def load_audit(path):
    with Path(path).open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise SystemExit("Audit JSON must be an object.")
    return data


def render_markdown(card, svg_path):
    label = markdown_text(f"{card['name']} proof card")
    target = card["url"] or svg_path
    return f"[![{label}]({markdown_destination(svg_path)})]({markdown_destination(target)})\n"


def render_svg(card):
    accent = "#00A676" if card["score"] >= 90 else "#FFB000" if card["score"] >= 70 else "#FF5F8F"
    title = escape(card["name"][:34])
    grade = escape(card["grade"].replace("-", " "))
    checked = escape(card["checkedAt"][:10])
    return f'''<svg viewBox="0 0 760 260" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="{title} proof card">
  <rect width="760" height="260" rx="8" fill="#121417"/>
  <path d="M0 198h760v62H0z" fill="#F7EFDA"/>
  <path d="M512 0h248v260H406z" fill="{accent}"/>
  <path d="M630 0h130v260H532z" fill="#4D35A3"/>
  <text x="32" y="58" fill="#F8FAF6" font-family="Inter,system-ui,sans-serif" font-size="34" font-weight="850">{title}</text>
  <text x="34" y="92" fill="#CFFFF0" font-family="Inter,system-ui,sans-serif" font-size="18" font-weight="780">Proof Card Forge</text>
  {metric(36, 174, card["score"], "Score")}
  {metric(198, 174, card["status"], "Status")}
  {metric(360, 174, card["version"], "Version")}
  {metric(522, 174, checked, "Checked")}
  <text x="34" y="232" fill="#372F28" font-family="Inter,system-ui,sans-serif" font-size="14" font-weight="800">{grade} / shareable proof card</text>
</svg>'''


def metric(x, y, value, label):
    return f'''<text x="{x}" y="{y}" fill="#F8FAF6" font-family="Inter,system-ui,sans-serif" font-size="32" font-weight="900">{escape(str(value))}</text>
  <text x="{x}" y="{y + 25}" fill="#E7EBDC" font-family="Inter,system-ui,sans-serif" font-size="13" font-weight="760">{escape(label)}</text>'''


def safe_text(value, limit):
    text = re.sub(r"\s+", " ", str(value or "")).strip()
    return text[:limit]


def safe_url(value):
    text = str(value or "").strip()
    return text if re.match(r"^https://[^\s<>]+$", text) else ""


def markdown_text(value):
    text = html.escape(str(value), quote=False)
    return re.sub(r"([\\\[\]`*_{}()#+.!|>\-])", r"\\\1", text)


def markdown_destination(value):
    text = str(value or "").strip()
    if not text:
        return ""
    return quote(text, safe="/:#?&=%@+.,;~_-")


def clamp(value, low, high):
    try:
        number = int(value)
    except (TypeError, ValueError):
        number = low
    return max(low, min(high, number))


def escape(value):
    return html.escape(str(value), quote=True)


def write(path, text, force=False):
    out = Path(path).resolve()
    out.parent.mkdir(parents=True, exist_ok=True)
    if out.exists() and not force:
        raise SystemExit(f"Refusing to overwrite existing file without --force: {out}")
    out.write_text(text, encoding="utf-8")


if __name__ == "__main__":
    main()
