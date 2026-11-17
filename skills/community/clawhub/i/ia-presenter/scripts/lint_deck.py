#!/usr/bin/env python3
"""Lint an iA Presenter deck (a .iapresenter bundle or a bare .md file).

Usage: lint_deck.py PATH [--json] [--strict]

Checks render-breaking mistakes (ERROR) and weak-slide patterns (WARN):
  E001 space-indented line where a TAB was probably intended
  E002 TAB in front of a table row / code fence (becomes a code block)
  E003 /assets/ file referenced but missing from the bundle
  E004 remote image URL without an image extension (treated as text)
  E005 unknown or invalid content-block / chart metadata
  E006 unknown "Layout:" name
  E010 bundle missing text.md / info.json, invalid JSON, theme id not lowercase
  W101 slide has no visible element (notes only)
  W102 wall of text: > 60 visible words on one slide
  W103 "Layout: Columns" (broken in 2.0.2) / "Layout: Grid" with a heading
  W104 deck ends on "Thank you" / "Questions"
  W105 metadata line separated from its block by a blank line (ignored by the app)
  W106 deck starts with "---"
Exit code 1 when any ERROR (or, with --strict, any WARN) is found.
"""
import json
import os
import re
import sys

LAYOUTS = {"cover", "title", "section", "default", "split", "grid", "columns",
           "title-and-columns", "caption", "image", "caption-top"}
IMAGE_EXT = re.compile(r"\.(jpe?g|gif|webp|a?png|tiff?|svg)(\?.*)?$", re.I)
CONTENT_BLOCK = re.compile(r"^(/assets/\S.*|/Theme/\S.*|https?://\S+)$")
META_KEYS = {
    "size": {"cover", "contain"},
    "x": {"left", "center", "right"},
    "y": {"top", "center", "bottom"},
    "background": {"true", "false"},
    "filter": {"lighten", "darken", "grayscale", "sepia", "blur"},
    "opacity": {f"{n}%" for n in range(10, 101, 10)} | {str(n) for n in range(10, 101, 10)},
    "title": None, "alt": None, "class": None, "caption": None, "header": None, "footer": None,
    "chart": {"bar", "line", "pie", "donut"},
    "orientation": {"horizontal", "vertical"},
    "bar-type": {"stacked", "separated"},
    "line-type": {"step", "steps", "normal", "spline"},
    "color-type": {"sequential", "differential"},
    "xlabel": None, "ylabel": None,
    "xformat": {"date", "number", "percent"},
    "colors": None,
}
META_LINE = re.compile(r"^([A-Za-z][A-Za-z-]*):\s*(.*)$")
TABLE_ROW = re.compile(r"^\s*\|")
HEADING = re.compile(r"^#{1,6}\s")
THANKS = re.compile(r"^(#+\s*)?(thank you|thanks|questions\??|q&a|any questions\??)\s*!?\s*$", re.I)


class Finding:
    def __init__(self, line, code, level, msg):
        self.line, self.code, self.level, self.msg = line, code, level, msg

    def as_dict(self):
        return {"line": self.line, "code": self.code, "level": self.level, "message": self.msg}


def lint_text(text, bundled=None):
    out = []
    lines = text.split("\n")
    slides = []          # list of (start_line, [lines])
    cur = []
    start = 1
    for i, raw in enumerate(lines, 1):
        if raw.strip() == "---" and not raw.startswith("\t"):
            slides.append((start, cur))
            cur, start = [], i + 1
        else:
            cur.append((i, raw))
    slides.append((start, cur))

    in_fence = False
    for s_start, slide in slides:
        visible_words = 0
        has_visible = False
        layout = None
        prev_was_block = False      # previous non-empty line was a content block/table/metadata
        prev_blank = False
        for idx, (i, raw) in enumerate(slide):
            stripped = raw.strip()
            if stripped.startswith("```"):
                in_fence = not in_fence
                has_visible = True
                if raw.startswith("\t"):
                    out.append(Finding(i, "E002", "ERROR", "TAB before a code fence turns it into an indented code block"))
                prev_was_block, prev_blank = False, False
                continue
            if in_fence:
                continue
            if stripped == "":
                prev_blank = True
                continue
            # Layout / Class directive on first non-empty line
            if idx == 0 or all(l[1].strip() == "" for l in slide[:idx]):
                m = re.match(r"^(Layout|Class):\s*(.+)$", stripped, re.I)
                if m:
                    if m.group(1).lower() == "layout":
                        layout = m.group(2).strip().lower()
                        if layout not in LAYOUTS:
                            out.append(Finding(i, "E006", "ERROR", f'unknown Layout "{m.group(2).strip()}" (known: {", ".join(sorted(LAYOUTS))})'))
                        elif layout == "columns":
                            out.append(Finding(i, "W103", "WARN", '"Layout: Columns" renders unusably small in 2.0.2 – use Title-and-Columns or auto layout'))
                    prev_was_block, prev_blank = False, False
                    continue
            if raw.startswith("\t"):
                body = raw.lstrip("\t")
                if TABLE_ROW.match(body):
                    out.append(Finding(i, "E002", "ERROR", "TAB before a table row turns the table into a code block – tables must be flush-left"))
                has_visible = True
                visible_words += len(body.split())
                prev_was_block, prev_blank = False, False
                continue
            if re.match(r"^ {2,}\S", raw) and not TABLE_ROW.match(raw) and not re.match(r"^ {2,}[-*+]\s|^ {2,}\d+\.\s", raw):
                out.append(Finding(i, "E001", "ERROR", "line indented with spaces – use a real TAB to make text visible (spaces make it notes)"))
            if HEADING.match(stripped):
                has_visible = True
                visible_words += len(stripped.split()) - 1
                if layout == "grid":
                    out.append(Finding(i, "W103", "WARN", '"Layout: Grid" turns this heading into a grid cell – use Title-and-Columns for a title row'))
                    layout = None
                prev_was_block, prev_blank = False, False
                continue
            if TABLE_ROW.match(raw):
                has_visible = True
                prev_was_block, prev_blank = True, False
                continue
            if CONTENT_BLOCK.match(stripped) and not raw.startswith(" "):
                has_visible = True
                if stripped.startswith("http") and not IMAGE_EXT.search(stripped) and "unsplash.com" not in stripped and "youtube.com" not in stripped and "youtu.be" not in stripped:
                    out.append(Finding(i, "E004", "ERROR", "remote URL has no image extension (.jpg/.png/.webp/.gif/.svg…) – the app treats it as text"))
                if stripped.startswith("/assets/") and bundled is not None:
                    rel = stripped[len("/assets/"):].strip()
                    if rel not in bundled:
                        out.append(Finding(i, "E003", "ERROR", f"missing asset: assets/{rel}"))
                prev_was_block, prev_blank = True, False
                continue
            m = META_LINE.match(stripped)
            if m and (prev_was_block or (prev_blank and idx > 0 and m.group(1).lower() in META_KEYS)):
                key, val = m.group(1).lower(), m.group(2).strip()
                if prev_blank and not prev_was_block:
                    out.append(Finding(i, "W105", "WARN", f'"{m.group(1)}:" is separated from its block by a blank line – the app ignores it'))
                if key not in META_KEYS:
                    out.append(Finding(i, "E005", "ERROR", f'unknown metadata key "{m.group(1)}" (known: {", ".join(sorted(META_KEYS))})'))
                else:
                    allowed = META_KEYS[key]
                    if allowed is not None and val.strip('"').lower() not in allowed:
                        out.append(Finding(i, "E005", "ERROR", f'invalid value "{val}" for {m.group(1)} (allowed: {", ".join(sorted(allowed))})'))
                prev_blank = False
                continue
            # plain notes paragraph
            prev_was_block, prev_blank = False, False
        if not has_visible and any(l[1].strip() for l in slide):
            out.append(Finding(s_start, "W101", "WARN", "slide has nothing visible (notes only)"))
        if visible_words > 60:
            out.append(Finding(s_start, "W102", "WARN", f"wall of text: {visible_words} visible words on one slide"))
    if lines and lines[0].strip() == "---":
        out.append(Finding(1, "W106", "WARN", "deck starts with a slide break – remove the leading ---"))
    # closing slide
    last_visible = [l for l in reversed(slides[-1][1]) if l[1].strip() and (HEADING.match(l[1].strip()) or l[1].startswith("\t"))]
    if last_visible and THANKS.match(last_visible[0][1].strip().lstrip("\t")):
        out.append(Finding(last_visible[0][0], "W104", "WARN", 'deck ends on "Thank you / Questions" – close on a landing line or an ask'))
    return out


def lint_path(path):
    findings = []
    if os.path.isdir(path):
        text_md = os.path.join(path, "text.md")
        info = os.path.join(path, "info.json")
        if not os.path.isfile(text_md):
            return [Finding(0, "E010", "ERROR", "bundle has no text.md")]
        if not os.path.isfile(info):
            findings.append(Finding(0, "E010", "ERROR", "bundle has no info.json"))
        else:
            try:
                with open(info, encoding="utf-8") as f:
                    data = json.load(f)
                tpl = (data.get("net.ia.presenter") or {}).get("template")
                if tpl and tpl != tpl.lower():
                    findings.append(Finding(0, "E010", "ERROR", f'info.json template "{tpl}" must be lowercase (e.g. "new york")'))
                if data.get("type") != "net.daringfireball.markdown":
                    findings.append(Finding(0, "W110", "WARN", 'info.json "type" should be "net.daringfireball.markdown"'))
            except Exception as e:
                findings.append(Finding(0, "E010", "ERROR", f"info.json is not valid JSON: {e}"))
        bundled = set()
        adir = os.path.join(path, "assets")
        if os.path.isdir(adir):
            for root, _, files in os.walk(adir):
                for fn in files:
                    bundled.add(os.path.relpath(os.path.join(root, fn), adir))
        with open(text_md, encoding="utf-8") as f:
            text = f.read()
        findings += lint_text(text, bundled)
        return findings, text
    with open(path, encoding="utf-8") as f:
        text = f.read()
    return lint_text(text, None), text


def main(argv):
    if not argv or argv[0] in ("-h", "--help"):
        print(__doc__)
        return 0
    as_json = "--json" in argv
    strict = "--strict" in argv
    path = [a for a in argv if not a.startswith("--")][0]
    res = lint_path(path)
    findings, text = res if isinstance(res, tuple) else (res, "")
    slides = text.count("\n---\n") + 1 if text else 0
    notes_words = sum(len(l.split()) for l in text.split("\n") if l.strip() and not l.startswith("\t") and not HEADING.match(l) and not TABLE_ROW.match(l) and not CONTENT_BLOCK.match(l.strip()) and not META_LINE.match(l.strip()) and l.strip() != "---")
    minutes = notes_words / 110.0
    errs = sum(1 for f in findings if f.level == "ERROR")
    warns = sum(1 for f in findings if f.level == "WARN")
    if as_json:
        print(json.dumps({"path": path, "slides": slides, "notes_words": notes_words, "est_minutes": round(minutes, 1),
                          "errors": errs, "warnings": warns, "findings": [f.as_dict() for f in findings]}, indent=2))
    else:
        for f in sorted(findings, key=lambda f: (f.line, f.code)):
            print(f"{path}:{f.line}: [{f.code}] {f.level}: {f.msg}")
        print(f"{slides} slides · ~{notes_words} note words ≈ {minutes:.1f} min at 110 wpm · {errs} errors, {warns} warnings")
    return 1 if errs or (strict and warns) else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
