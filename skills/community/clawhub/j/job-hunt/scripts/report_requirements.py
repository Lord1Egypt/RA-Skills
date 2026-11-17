#!/usr/bin/env python3
"""Write `report-layout-requirements.yaml` for a report the bundled renderer draws.

`references/layout-review.md` asks for "documented defaults" when the user gave no
report template, and nothing documented them. In the 2026-10-29 simulation all
three agents read deliver.py, check_layout.py and layout_requirements.py to
rebuild the values, and two of them wrote different fonts for the same renderer.
The values below are the ones `deliver._render_portable_report` draws with;
`test_report_requirements.py` renders a report and measures it against them, so a
change to the renderer that is not made here fails the suite.

The text samples are the report's own first title, section heading and body line,
so run this after `report.md` exists and before `render_report.py`.

Exit codes: 0 written; 2 could not run — no report.md, a requirements file is
already there (requirements are not rewritten to fit an output), or the report is
one the bundled renderer does not draw (a user template, right-to-left text).
"""
from __future__ import annotations

import argparse
import pathlib
import re
import sys

import yaml

import deliver

PAGE = [595.28, 841.89]                 # A4
TEXT_BOUNDS = [56, 56, 539, 816]        # text column 56–539 pt; body from 64 pt; footer ends near 813 pt
SIZES = {"title": 18, "heading": 14, "subheading": 12.6, "body": 12,
         "table": 11.5, "contents": 10.5, "footer": 8}
NAVY = 0x17365D                         # titles, headings and links


_CJK = re.compile(r"[\u3000-\u9fff\uac00-\ud7af\uff00-\uffef]")
_USABLE_WIDTH = TEXT_BOUNDS[2] - TEXT_BOUNDS[0]


def _display(line: str) -> str:
    """What the PDF prints for one Markdown line: link labels, no emphasis marks."""
    line = re.sub(r"!?\[([^\]]*)\]\([^)]*\)", r"\1", line)
    return re.sub(r"[*_`]", "", line).strip()


def _needle(text: str, size: float, everything: str) -> str | None:
    """The shortest prefix of `text` that fits on its first PDF line and occurs
    once in the whole report.

    Uniqueness is the point. The gate checks every line that contains a sample,
    so a section heading that the contents list repeats at 10.5 pt, or a title
    prefix that the body repeats, fails a report that is fine.
    """
    fits = lambda s: sum(size if _CJK.match(c) else size * 0.62 for c in s) <= _USABLE_WIDTH
    if _CJK.search(text):
        prefixes = [text[:n] for n in range(min(6, len(text)), len(text) + 1)]
    else:
        words = text.split()
        prefixes = [" ".join(words[:n]) for n in range(min(2, len(words)), len(words) + 1)]
    for prefix in prefixes:
        if not fits(prefix):
            break
        if everything.count(prefix) == 1:
            return prefix
    return None


def _samples(markdown: str, font: str) -> list[dict] | str:
    """A title, a heading and a body line, each as literal text printed once."""
    lines = [raw.strip() for raw in markdown.splitlines()]
    everything = "\n".join(_display(line.lstrip("#").strip()) for line in lines)
    candidates = {"title": [], "heading": [], "body": []}
    for line in lines:
        if line.startswith("# "):
            candidates["title"].append((_display(line[2:]), SIZES["title"]))
        elif line.startswith("## "):
            candidates["heading"].append((_display(line[3:]), SIZES["heading"]))
        elif line.startswith("### "):
            candidates["heading"].append((_display(line[4:]), SIZES["subheading"]))
        elif line and not re.match(r"[#>|\-*+`\[!]|\d+[.)]\s", line):
            candidates["body"].append((_display(line), SIZES["body"]))
    # Prefer a section heading; a sub-heading is used only when the contents
    # list repeats every section heading.
    candidates["heading"].sort(key=lambda c: c[1] != SIZES["heading"])
    out = []
    for role, color in (("title", NAVY), ("heading", NAVY), ("body", None)):
        found = next(((needle, size) for text, size in candidates[role]
                      if (needle := _needle(text, size, everything))), None)
        if found is None:
            return (f"no {role} text in report.md is printed exactly once on one line; "
                    "write text_samples by hand with region_pt")
        sample = {"role": role, "text": found[0], "size_pt": found[1], "fonts": [font]}
        if color is not None:
            sample["color"] = color
        out.append(sample)
    return out


def _extracted_font_name(code: str) -> str:
    """The font name a PDF reader reports for text the renderer draws with `code`.

    Not `pymupdf.Font(code).name`: the built-in Helvetica is called "Helvetica"
    there but reads back as "NimbusSans-Regular", and the gate compares what it
    reads back.
    """
    import pymupdf
    with pymupdf.open() as doc:
        page = doc.new_page()
        writer = pymupdf.TextWriter(page.rect)
        writer.append((50, 50), "Ab", font=pymupdf.Font(code), fontsize=12)
        writer.write_text(page)
        return page.get_text("dict")["blocks"][0]["lines"][0]["spans"][0]["font"]


def requirements(markdown: str) -> dict | str:
    style = deliver._portable_report_style(markdown)
    if style is None:
        return ("this report is not drawn by the bundled renderer; write the "
                "requirements from the reference as references/layout-review.md describes")
    font = _extracted_font_name(style["font"])
    samples = _samples(markdown, font)
    if isinstance(samples, str):
        return samples
    headings = [line[3:].strip() for line in markdown.splitlines() if line.startswith("## ")]
    return {
        "reference": None,
        "expectations": {
            "fonts": f"Bundled renderer default: one embedded face, {font}, for all text; "
                     "no host-font substitution",
            "font_sizes": "Title {title} pt; section headings {heading} pt; sub-headings "
                          "{subheading} pt; body and list items {body} pt; table text {table} pt; "
                          "contents links {contents} pt; footer {footer} pt".format(**SIZES),
            "page_geometry": "A4 595.28 x 841.89 pt; text column 56–539 pt; body from 64 pt "
                             "to 770 pt; footer baseline 811 pt",
            "headings_and_rules": "Navy #17365d title, headings and links; tables with a "
                                  "pale header band and light row rules; no card frames",
            "dates_and_alignment": "All text left-aligned at 56 pt; footer label left and "
                                   f"page number right ({style['page'].format(number='N')})",
            "paragraph_spacing": "Body leading 1.35 x size; table rows 15.5 pt; no stacked "
                                 "blank lines",
            "content_order": "Title, metadata, contents, then the sections in this order: "
                             + "; ".join(headings),
            "pagination_and_clipping": "Headings stay with their first block; table headers "
                                       "repeat on a continued table; no clipped or "
                                       "overlapping text on any page",
        },
        "page_size_pt": PAGE,
        "text_bounds_pt": TEXT_BOUNDS,
        "text_samples": samples,
    }


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--workspace", required=True)
    args = parser.parse_args(argv)
    ws = pathlib.Path(args.workspace)
    md, out = ws / "report.md", ws / "report-layout-requirements.yaml"
    if not md.is_file():
        print(f"cannot run: {md} does not exist; write the report first", file=sys.stderr)
        return 2
    if out.exists():
        print(f"cannot run: {out} already exists. Requirements are not regenerated to fit "
              "an output; record a user's change under user_overrides instead.", file=sys.stderr)
        return 2
    result = requirements(md.read_text(encoding="utf-8"))
    if isinstance(result, str):
        print(f"cannot run: {result}", file=sys.stderr)
        return 2
    out.write_text(yaml.safe_dump(result, allow_unicode=True, sort_keys=False), encoding="utf-8")
    print(f"Wrote {out}")
    return 0


if __name__ == "__main__":
    from cli_io import configure_output

    configure_output()
    sys.exit(main())
