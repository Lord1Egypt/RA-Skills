#!/usr/bin/env python3
"""
ODT document tool powered by odfdo.

Requires: pip install odfdo

Usage:
  python odt_tool.py inspect      <file.odt>
  python odt_tool.py to-text      <file.odt>
  python odt_tool.py create       <file.odt> [--title <title>]
  python odt_tool.py append       <file.odt> --text <text> [--heading <level>] [--style <style>]
  python odt_tool.py replace      <file.odt> --find <pattern> --sub <replacement> [--regex]
  python odt_tool.py set-meta     <file.odt> --title <t> [--subject <s>] [--description <d>]
  python odt_tool.py set-font     <file.odt> --font <name> [--size <pt>]
  python odt_tool.py set-outline  <file.odt> [--numbered] [--plain]
  python odt_tool.py merge-styles <file.odt> --template <template.odt>
"""

import argparse
import json
import re
import sys
from pathlib import Path


def _require_odfdo() -> None:
    try:
        import odfdo  # noqa: F401
    except ImportError:
        print("ERROR: odfdo is not installed. Run: pip install odfdo", file=sys.stderr)
        sys.exit(1)


# ---------------------------------------------------------------------------
# inspect
# ---------------------------------------------------------------------------

def cmd_inspect(path: str) -> None:
    _require_odfdo()
    from odfdo import Document, Header, Paragraph

    doc = Document(path)
    body = doc.body

    meta = doc.meta
    info: dict = {
        "title": meta.title,
        "subject": meta.subject,
        "description": meta.description,
        "creator": meta.creator,
        "creation_date": str(meta.creation_date) if meta.creation_date else None,
    }
    print("=== Metadata ===")
    print(json.dumps({k: v for k, v in info.items() if v}, indent=2))

    print("\n=== Structure ===")
    i = 0
    for child in body.children:
        if isinstance(child, Header):
            text = child.inner_text or ""
            if text.strip():
                print(f"  {i:>4}: [Heading {child.level}] {text[:80]}")
                i += 1
        elif isinstance(child, Paragraph):
            style = child.style or ""
            text = child.inner_text or ""
            if not text.strip():
                continue
            tag = f"[{style}]" if style else "[para]"
            print(f"  {i:>4}: {tag} {text[:80].replace(chr(10), ' ')}")
            i += 1

    tables = body.tables
    if tables:
        print(f"\n=== Tables ({len(tables)}) ===")
        for t in tables:
            name = t.name or "(unnamed)"
            rows = t.nrows
            cols = t.ncols
            print(f"  {name}: {rows}r × {cols}c")


# ---------------------------------------------------------------------------
# to-text
# ---------------------------------------------------------------------------

def cmd_to_text(path: str) -> None:
    _require_odfdo()
    from odfdo import Document, Header, Paragraph

    doc = Document(path)
    lines = []
    for child in doc.body.children:
        if isinstance(child, (Header, Paragraph)):
            text = child.inner_text or ""
            if text.strip():
                lines.append(text)
    print("\n".join(lines))


# ---------------------------------------------------------------------------
# create
# ---------------------------------------------------------------------------

def cmd_create(path: str, title: str | None = None) -> None:
    _require_odfdo()
    from odfdo import Document, Header

    doc = Document("text")
    if title:
        doc.meta.title = title
        doc.body.append(Header(1, title))
    doc.save(path, pretty=True)
    print(f"OK created: {path}")


# ---------------------------------------------------------------------------
# append
# ---------------------------------------------------------------------------

def cmd_append(path: str, text: str, heading: int | None = None, style: str | None = None) -> None:
    _require_odfdo()
    from odfdo import Document, Header, Paragraph

    doc = Document(path)

    if heading is not None:
        level = max(1, min(6, heading))
        element = Header(level, text)
    elif style:
        element = Paragraph(text, style=style)
    else:
        element = Paragraph(text)

    doc.body.append(element)
    doc.save(path, pretty=True)
    print(f"OK appended to: {path}")


# ---------------------------------------------------------------------------
# replace
# ---------------------------------------------------------------------------

def cmd_replace(path: str, find: str, sub: str, use_regex: bool = False) -> None:
    _require_odfdo()
    from odfdo import Document, Header, Paragraph

    doc = Document(path)
    count = 0

    # el.replace(pattern, new) treats pattern as a regex; escape for plain-text mode
    pattern = find if use_regex else re.escape(find)
    elements: list = list(doc.body.paragraphs) + list(doc.body.headers)
    for el in elements:
        text = el.inner_text or ""
        if re.search(pattern, text):
            n = el.replace(pattern, sub)
            count += n

    doc.save(path, pretty=True)
    print(f"OK replaced {count} occurrence(s) in: {path}")


# ---------------------------------------------------------------------------
# set-meta
# ---------------------------------------------------------------------------

def cmd_set_meta(
    path: str,
    title: str | None = None,
    subject: str | None = None,
    description: str | None = None,
) -> None:
    _require_odfdo()
    from odfdo import Document

    doc = Document(path)
    if title is not None:
        doc.meta.title = title
    if subject is not None:
        doc.meta.subject = subject
    if description is not None:
        doc.meta.description = description
    doc.save(path, pretty=True)
    print(f"OK metadata updated: {path}")


# ---------------------------------------------------------------------------
# set-font
# ---------------------------------------------------------------------------

def cmd_set_font(path: str, font: str, size: str | None = None, preserve_mono: bool = True) -> None:
    """Set font across the entire document — default style AND all named/automatic overrides."""
    _require_odfdo()
    from odfdo import Document

    # Named styles that intentionally use monospace fonts — skip unless user says otherwise
    _MONO_STYLES = {
        "Preformatted_20_Text", "Preformatted Text",
        "Example", "Teletype",
        "Source_20_Code", "Source Code",
        "Internet_20_Link", "Internet Link",
    }

    doc = Document(path)
    pt = (size if size.endswith("pt") else f"{size}pt") if size else None
    # ODF uses quoted font-family values when the name contains spaces
    font_family = f"'{font}'" if " " in font else font

    # Declare font face so LibreOffice/Collabora can find it
    existing_names = {
        s.get_attribute("style:name")
        for s in doc.get_styles()
        if s.tag == "style:font-face"
    }
    if font not in existing_names:
        from odfdo.element import Element
        face = Element.from_tag("style:font-face")
        face.set_attribute("style:name", font)
        face.set_attribute("svg:font-family", font_family)
        face.set_attribute("style:font-family-generic", "swiss")
        face.set_attribute("style:font-pitch", "variable")
        doc.insert_style(face, automatic=False)

    def _apply(tp: object, style_name: str = "") -> None:
        """Apply font (and optionally size) to a text-properties element."""
        if preserve_mono and style_name in _MONO_STYLES:
            return
        # style:font-name — logical name reference (links to font-face declaration)
        tp.set_attribute("style:font-name", font)
        tp.set_attribute("style:font-name-asian", font)
        tp.set_attribute("style:font-name-complex", font)
        # fo:font-family / style:font-family-* — the actual family Collabora/LO renders with
        tp.set_attribute("fo:font-family", font_family)
        tp.set_attribute("style:font-family-asian", font_family)
        tp.set_attribute("style:font-family-complex", font_family)
        if pt:
            tp.set_attribute("fo:font-size", pt)
            tp.set_attribute("style:font-size-asian", pt)
            tp.set_attribute("style:font-size-complex", pt)

    updated = 0

    # 1. Named + default styles (styles.xml)
    for s in doc.get_styles():
        style_name = s.get_attribute("style:name") or ""
        for tp in s.get_elements("style:text-properties"):
            _apply(tp, style_name)
            updated += 1

    # 2. Automatic styles (content.xml — inline overrides on individual elements)
    for section in doc.content.get_elements("office:automatic-styles"):
        for s in section.children:
            style_name = s.get_attribute("style:name") or ""
            for tp in s.get_elements("style:text-properties"):
                _apply(tp, style_name)
                updated += 1

    doc.save(path, pretty=True)
    size_msg = f" at {size}pt" if size else ""
    print(f"OK font set to '{font}'{size_msg} across {updated} style rule(s): {path}")


# ---------------------------------------------------------------------------
# set-outline
# ---------------------------------------------------------------------------

def cmd_set_outline(path: str, numbered: bool = False) -> None:
    """Control heading outline numbering (numbered=True for 1.1.1, False for plain)."""
    _require_odfdo()
    from odfdo import Document

    doc = Document(path)
    level_styles = doc.styles.xpath("//text:outline-level-style")

    if not level_styles:
        print("ERROR: no outline-level-style elements found", file=sys.stderr)
        sys.exit(1)

    for lvl in level_styles:
        level = int(lvl.get_attribute("text:level") or 1)
        if numbered:
            lvl.set_attribute("style:num-format", "1")
            lvl.set_attribute("style:num-suffix", ".")
            if level > 1:
                lvl.set_attribute("text:display-levels", str(level))
        else:
            lvl.set_attribute("style:num-format", "")
            lvl.set_attribute("style:num-suffix", "")
            try:
                lvl.del_attribute("text:display-levels")
            except (KeyError, AttributeError):
                pass

    doc.save(path, pretty=True)
    mode = "numbered (1.1.1...)" if numbered else "plain (no numbers)"
    print(f"OK outline set to {mode}: {path}")


# ---------------------------------------------------------------------------
# merge-styles
# ---------------------------------------------------------------------------

def cmd_merge_styles(path: str, template_path: str) -> None:
    """Apply all styles from a template ODT into the target document."""
    _require_odfdo()
    from odfdo import Document

    doc = Document(path)
    template = Document(template_path)
    doc.merge_styles_from(template)
    doc.save(path, pretty=True)
    print(f"OK styles merged from '{template_path}' into '{path}'")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="ODT document tool using odfdo",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    sub = parser.add_subparsers(dest="cmd", required=True)

    # inspect
    p = sub.add_parser("inspect", help="Show document structure and metadata")
    p.add_argument("file", help="Path to .odt file")

    # to-text
    p = sub.add_parser("to-text", help="Extract all text content")
    p.add_argument("file", help="Path to .odt file")

    # create
    p = sub.add_parser("create", help="Create a new blank ODT document")
    p.add_argument("file", help="Output path")
    p.add_argument("--title", default=None, help="Document title (also inserted as H1)")

    # append
    p = sub.add_parser("append", help="Append a paragraph or heading")
    p.add_argument("file", help="Path to .odt file")
    p.add_argument("--text", required=True, help="Text to append")
    p.add_argument("--heading", type=int, default=None, metavar="LEVEL",
                   help="Insert as heading at given level (1-6)")
    p.add_argument("--style", default=None, help="Named paragraph style to apply")

    # replace
    p = sub.add_parser("replace", help="Find and replace text")
    p.add_argument("file", help="Path to .odt file")
    p.add_argument("--find", required=True, help="Text or pattern to find")
    p.add_argument("--sub", required=True, help="Replacement text")
    p.add_argument("--regex", action="store_true", help="Treat --find as a regex pattern")

    # set-meta
    p = sub.add_parser("set-meta", help="Set document metadata fields")
    p.add_argument("file", help="Path to .odt file")
    p.add_argument("--title", default=None)
    p.add_argument("--subject", default=None)
    p.add_argument("--description", default=None)

    # set-font
    p = sub.add_parser("set-font", help="Set font across the whole document (all style layers)")
    p.add_argument("file", help="Path to .odt file")
    p.add_argument("--font", required=True, help="Font name, e.g. 'Noto Sans'")
    p.add_argument("--size", default=None, help="Font size in points, e.g. 11")
    p.add_argument("--no-preserve-mono", action="store_true",
                   help="Also change monospace/code styles (default: leave them alone)")

    # set-outline
    p = sub.add_parser("set-outline", help="Control heading outline numbering")
    p.add_argument("file", help="Path to .odt file")
    group = p.add_mutually_exclusive_group(required=True)
    group.add_argument("--numbered", action="store_true", help="Use 1. / 1.1 / 1.1.1 numbering")
    group.add_argument("--plain", action="store_true", help="Remove all heading numbers")

    # merge-styles
    p = sub.add_parser("merge-styles", help="Apply all styles from a template ODT")
    p.add_argument("file", help="Target .odt file")
    p.add_argument("--template", required=True, help="Template .odt to copy styles from")

    args = parser.parse_args()

    if args.cmd == "inspect":
        cmd_inspect(args.file)
    elif args.cmd == "to-text":
        cmd_to_text(args.file)
    elif args.cmd == "create":
        cmd_create(args.file, args.title)
    elif args.cmd == "append":
        cmd_append(args.file, args.text, args.heading, args.style)
    elif args.cmd == "replace":
        cmd_replace(args.file, args.find, args.sub, args.regex)
    elif args.cmd == "set-meta":
        cmd_set_meta(args.file, args.title, args.subject, args.description)
    elif args.cmd == "set-font":
        cmd_set_font(args.file, args.font, args.size, preserve_mono=not args.no_preserve_mono)
    elif args.cmd == "set-outline":
        cmd_set_outline(args.file, numbered=args.numbered)
    elif args.cmd == "merge-styles":
        cmd_merge_styles(args.file, args.template)


if __name__ == "__main__":
    main()
