#!/usr/bin/env python3
"""Validate generated decks against the frozen Light IDE template contract."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path


EXPECTED_STYLE_SHA256 = "1878A4A997EE1A7CBEF6673FC53A9526A0B2CB589B309D1D1A1E5467F2FE249D"
EXPECTED_SHELL_SHA256 = "CC84CB960961307A4FC93F13421FC0763E3E8ED0E424429A1FB7AFE210C5FDEB"

REQUIRED_IDS = ["stage", "deck", "bar", "counter", "hint", "notes"]
FORBIDDEN = [
    (r"fonts\.googleapis\.com", "external Google Fonts are forbidden"),
    (r"WebGL|THREE\.|canvas\.getContext\(\s*['\"]webgl", "WebGL / 3D backgrounds are forbidden"),
    (r"Playfair|Noto Serif|Inter,|Helvetica Neue", "foreign type systems would break Light IDE UI"),
    (r"--ink\b|--paper\b", "foreign presentation theme tokens are forbidden"),
]

STYLE_RE = re.compile(r"<style>(.*?)</style>", re.S | re.I)
TITLE_RE = re.compile(r"<title>.*?</title>", re.S | re.I)
CLASS_ATTR_RE = re.compile(r"\bclass\s*=\s*(['\"])(.*?)\1", re.S | re.I)
CSS_CLASS_RE = re.compile(r"\.([A-Za-z_][\w-]*)")
SECTION_RE = re.compile(r"<section\b(?P<attrs>[^>]*)>(?P<body>.*?)</section>", re.S | re.I)
INLINE_STYLE_RE = re.compile(r"\bstyle\s*=\s*(['\"])(.*?)\1", re.S | re.I)
SLOTS = [
    ("<!-- SLIDES_START -->", "<!-- SLIDES_END -->"),
    ("// ANIMATIONS_START", "// ANIMATIONS_END"),
]

ALLOWED_INLINE_PROPERTIES = {
    "align-items",
    "border-color",
    "color",
    "display",
    "flex",
    "flex-direction",
    "font-size",
    "gap",
    "height",
    "justify-content",
    "left",
    "margin",
    "margin-bottom",
    "margin-left",
    "margin-right",
    "margin-top",
    "position",
    "top",
    "width",
}
ALLOWED_INLINE_FONT_SIZES = {"22px"}
ALLOWED_INLINE_COLORS = {"var(--amber)", "var(--ink2)", "var(--teal)"}


def _compact(text: str) -> str:
    return re.sub(r"\s+", "", text)


def _sha256(text: str) -> str:
    return hashlib.sha256(_compact(text).encode("utf-8")).hexdigest().upper()


def extract_style(html: str) -> str:
    match = STYLE_RE.search(html)
    return match.group(1) if match else ""


def style_sha256(style: str) -> str:
    return _sha256(style)


def shell_source(html: str) -> str | None:
    masked, title_count = TITLE_RE.subn("<title></title>", html, count=1)
    if title_count != 1:
        return None
    for start, end in SLOTS:
        slot = re.compile(re.escape(start) + r".*?" + re.escape(end), re.S)
        masked, count = slot.subn(start + end, masked)
        if count != 1:
            return None
    return masked


def shell_sha256(html: str) -> str:
    shell = shell_source(html)
    return _sha256(shell) if shell is not None else ""


def _class_names(fragment: str) -> list[str]:
    names: list[str] = []
    for match in CLASS_ATTR_RE.finditer(fragment):
        names.extend(match.group(2).split())
    return names


def _slides(html: str) -> list[tuple[str, str]]:
    slides: list[tuple[str, str]] = []
    for match in SECTION_RE.finditer(html):
        attrs, body = match.group("attrs"), match.group("body")
        if "slide" in _class_names(attrs):
            slides.append((attrs, body))
    return slides


def _validate_slide_contract(
    html: str,
    style: str,
    errors: list[str],
    source: str,
) -> None:
    allowed_classes = set(CSS_CLASS_RE.findall(style))
    for class_name in sorted(set(_class_names(html)) - allowed_classes):
        errors.append(f"{source}: unknown class .{class_name}; use template classes only")

    slides = _slides(html)
    if not slides:
        errors.append(f'{source}: at least one <section class="slide"> is required')
        return

    for index, (attrs, body) in enumerate(slides, start=1):
        if re.search(r"<script\b|\bon\w+\s*=", body, re.I):
            errors.append(f"{source}: slide {index} contains executable HTML")
        if not re.search(r"\bdata-title\s*=\s*(['\"]).+?\1", attrs, re.S | re.I):
            errors.append(f"{source}: slide {index} missing data-title")
        aside_attrs = re.findall(r"<aside\b([^>]*)>", body, re.S | re.I)
        if not any("notes" in _class_names(aside) for aside in aside_attrs):
            errors.append(f'{source}: slide {index} missing <aside class="notes">')
        if len(re.findall(r"<h[12]\b", body, re.I)) != 1:
            errors.append(f"{source}: slide {index} must contain exactly 1 h1/h2")

        callout_count = sum(
            "callout" in match.group(2).split()
            for match in CLASS_ATTR_RE.finditer(body)
        )
        if callout_count > 1:
            errors.append(f"{source}: slide {index} has more than 1 callout")

        for points in re.finditer(
            r"<ul\b[^>]*class\s*=\s*(['\"])[^'\"]*\bpts\b[^'\"]*\1[^>]*>(.*?)</ul>",
            body,
            re.S | re.I,
        ):
            if len(re.findall(r"<li\b", points.group(2), re.I)) > 4:
                errors.append(f"{source}: slide {index} has more than 4 .pts items")

        for style_match in INLINE_STYLE_RE.finditer(body):
            declarations = [
                item.strip()
                for item in style_match.group(2).split(";")
                if item.strip()
            ]
            for declaration in declarations:
                if ":" not in declaration:
                    errors.append(
                        f"{source}: slide {index} has invalid inline style {declaration!r}"
                    )
                    continue
                prop, value = (
                    part.strip().lower() for part in declaration.split(":", 1)
                )
                if prop not in ALLOWED_INLINE_PROPERTIES:
                    errors.append(
                        f"{source}: slide {index} inline style property {prop} is not allowed"
                    )
                if prop == "font-size" and value not in ALLOWED_INLINE_FONT_SIZES:
                    errors.append(
                        f"{source}: slide {index} inline font-size {value} is not allowed"
                    )
                if prop == "color" and value not in ALLOWED_INLINE_COLORS:
                    errors.append(
                        f"{source}: slide {index} inline color {value} is not allowed"
                    )


def validate_html(
    html: str,
    source: str = "deck.html",
    template_html: str | None = None,
    allow_placeholders: bool = False,
) -> dict:
    errors: list[str] = []
    style = extract_style(html)
    reference_style = extract_style(template_html) if template_html else style

    if not style:
        errors.append(f"{source}: missing <style> block")
    if style and template_html and _compact(style) != _compact(reference_style):
        errors.append(
            f"{source}: <style> drifted from assets/template.html; copy the template"
        )

    if template_html:
        shell = shell_source(html)
        template_shell = shell_source(template_html)
        if shell is None:
            errors.append(f"{source}: title or editable-slot markers are missing")
        elif template_shell is None or _compact(shell) != _compact(template_shell):
            errors.append(
                f"{source}: template shell drifted; edit only title, slides, and animations slots"
            )
    elif Path(source).name == "template.html":
        if style_sha256(style) != EXPECTED_STYLE_SHA256:
            errors.append(f"{source}: <style> drifted from the original PPT snapshot")
        if shell_sha256(html) != EXPECTED_SHELL_SHA256:
            errors.append(f"{source}: frozen template shell drifted")

    for element_id in REQUIRED_IDS:
        if not re.search(
            rf"\bid\s*=\s*(['\"]){re.escape(element_id)}\1",
            html,
            re.I,
        ):
            errors.append(f"{source}: required element #{element_id} missing")

    for pattern, reason in FORBIDDEN:
        if re.search(pattern, html, re.I):
            errors.append(f"{source}: {reason}")

    if not allow_placeholders and "[必填]" in html:
        errors.append(f"{source}: unfinished [必填] placeholder found")

    _validate_slide_contract(html, reference_style, errors, source)
    return {"source": source, "ok": not errors, "errors": errors}


def validate_path(path: Path, template: Path | None = None) -> dict:
    html = path.read_text(encoding="utf-8")
    template_html = template.read_text(encoding="utf-8") if template else None
    return validate_html(
        html,
        source=str(path),
        template_html=template_html,
        allow_placeholders=template is None and path.name == "template.html",
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate a Light IDE HTML deck")
    parser.add_argument("html", type=Path, help="Generated or template HTML")
    parser.add_argument(
        "--template",
        type=Path,
        default=Path(__file__).resolve().parent.parent / "assets" / "template.html",
        help="Frozen template used as the UI and runtime source of truth",
    )
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    if not args.html.is_file():
        print(f"ERROR: {args.html} not found", file=sys.stderr)
        return 2

    template = args.template if args.html.resolve() != args.template.resolve() else None
    report = validate_path(args.html, template=template)
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    elif report["ok"]:
        print(f"OK {args.html}")
    else:
        print(f"FAIL {args.html}")
        for error in report["errors"]:
            print(f"- {error}")
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
