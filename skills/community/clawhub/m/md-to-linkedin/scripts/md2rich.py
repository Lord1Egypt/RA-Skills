#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.11"
# dependencies = ["markdown", "beautifulsoup4"]
# ///
"""Convert a Markdown article into rich text LinkedIn's article editor accepts.

LinkedIn has no Markdown, no table control and no code-block control. This
converts to semantic HTML — the tags its editor keeps on paste — and degrades
the two unsupported constructs into things it can hold:

  headings, paragraphs, bold/italic, lists, quotes, links, rules  -> kept
  tables                                                          -> bullet list
  fenced code                                                     -> kept as <pre><code>
  images                                                          -> [Image: alt] + checklist

LinkedIn's article editor does not render tables, so flattening is the default:
each row becomes a bullet with the first cell bold and the rest joined by a
middle dot. Use --keep-tables for a target that does render them. Code blocks
are kept; --degrade-code exists for editors that drop <pre>.

The fragment goes to the clipboard as text/html (wl-copy) for a direct paste,
and a self-contained HTML file is written for the browser-copy fallback.
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

import markdown
from bs4 import BeautifulSoup, NavigableString, Tag

BASE_DEFAULT = "https://github.com/j3ffyang/ai-thoughts/blob/main/docs/"

KEEP = {
    "p", "h1", "h2", "h3", "h4", "strong", "em", "b", "i", "code",
    "ul", "ol", "li", "blockquote", "a", "hr", "br",
    "pre", "table", "thead", "tbody", "tr", "th", "td", "caption",
}
# Cells may carry spans; everything else loses its attributes on purpose.
KEEP_ATTRS = {"th": {"colspan", "rowspan"}, "td": {"colspan", "rowspan"}}
DROP = {"script", "style", "head", "title", "meta", "link"}

FRONTMATTER = re.compile(r"\A---\n.*?\n---\n", re.S)


def _squash(text: str) -> str:
    """Collapse runs of whitespace without inventing spaces between nodes."""
    return re.sub(r"\s+", " ", text).strip()


def _keep_indent(line: str) -> str:
    """HTML collapses runs of spaces, so leading indentation becomes NBSP."""
    stripped = line.lstrip(" ")
    return "\u00a0" * (len(line) - len(stripped)) + stripped


def strip_frontmatter(text: str) -> str:
    return FRONTMATTER.sub("", text, count=1)


def table_to_list(table: Tag, soup: BeautifulSoup) -> Tag:
    """A LinkedIn article cannot hold a table. Each row becomes one bullet:
    the first cell bolded, the rest joined with a middle dot."""
    rows = []
    for tr in table.find_all("tr"):
        cells = [_squash(c.get_text()) for c in tr.find_all(["th", "td"])]
        cells = [c for c in cells if c]
        if cells:
            rows.append(cells)

    ul = soup.new_tag("ul")
    for cells in rows:
        li = soup.new_tag("li")
        first = soup.new_tag("strong")
        first.string = cells[0]
        li.append(first)
        if len(cells) > 1:
            li.append(NavigableString(" — " + " · ".join(cells[1:])))
        ul.append(li)
    return ul


def pre_to_quote(pre: Tag, soup: BeautifulSoup) -> Tag:
    """No code block on LinkedIn. A quote is the closest thing that keeps the
    lines visibly separate; indentation inside a line is not preserved."""
    code = pre.find("code")
    body = (code or pre).get_text()
    quote = soup.new_tag("blockquote")
    p = soup.new_tag("p")
    for i, line in enumerate(body.rstrip("\n").split("\n")):
        if i:
            p.append(soup.new_tag("br"))
        p.append(NavigableString(_keep_indent(line)))
    quote.append(p)
    return quote


def rewrite_link(a: Tag, base: str) -> None:
    href = a.get("href", "")
    if href.startswith(("http://", "https://", "mailto:")):
        return
    if href.startswith("#"):
        a.unwrap()
        return
    a["href"] = base.rstrip("/") + "/" + href.lstrip("./")


def _table_page(table_html: str, title: str) -> str:
    return f"""<!doctype html>
<html><head><meta charset="utf-8"><title>{title}</title>
<style>
  body {{ margin: 0; background: #fff;
         font: 15px/1.45 -apple-system, "Segoe UI", Roboto, sans-serif; color: #111; }}
  table {{ border-collapse: collapse; margin: 16px; }}
  th, td {{ border: 1px solid #c9ced3; padding: 8px 14px; text-align: left;
            vertical-align: top; }}
  th {{ background: #f2f5f8; font-weight: 600; }}
  tr:nth-child(even) td {{ background: #fafbfc; }}
  code {{ font-family: ui-monospace, monospace; font-size: 13px; }}
</style></head><body>{table_html}</body></html>"""


def render_table_png(table: Tag, out: Path) -> None:
    """Screenshot one table with headless Chromium, then trim to content.

    Chromium renders at 2x for crisp text; the window is deliberately wider and
    taller than any table, and ImageMagick trims the surplus away.
    """
    out = out.resolve()
    rows = table.find_all("tr")
    cols = max((len(r.find_all(["th", "td"])) for r in rows), default=1)
    width = max(900, 300 * cols)

    # Temp names must not collide with `out`: with_suffix(".png") on a .png
    # target is the target, and the cleanup then deletes the finished image.
    html_path = out.with_name(f".{out.stem}.src.html")
    png_path = out.with_name(f".{out.stem}.shot.png")
    html_path.write_text(_table_page(str(table), out.stem), encoding="utf-8")

    subprocess.run(
        ["chromium", "--headless", "--no-sandbox", "--disable-gpu",
         "--hide-scrollbars", "--force-device-scale-factor=2",
         f"--window-size={width},4000", f"--screenshot={png_path}",
         html_path.as_uri()],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        timeout=120, check=True,
    )
    subprocess.run(
        ["magick", str(png_path), "-trim", "+repage",
         "-bordercolor", "white", "-border", "12", str(out)],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        timeout=60, check=True,
    )
    for leftover in (html_path, png_path):
        leftover.unlink(missing_ok=True)


def convert(md_text: str, base: str, *, tables: str = "flatten",
            degrade_code: bool = False, image_dir: Path | None = None,
            stem: str = "table") -> tuple[str, list[str], list[str], list[str]]:
    html = markdown.markdown(
        strip_frontmatter(md_text),
        extensions=["extra", "sane_lists", "nl2br"],
    )
    soup = BeautifulSoup(html, "html.parser")
    notes: list[str] = []
    images: list[str] = []

    for tag in soup.find_all(list(DROP)):
        tag.decompose()

    table_pngs: list[str] = []
    if tables == "flatten":
        for n, table in enumerate(soup.find_all("table"), 1):
            table.replace_with(table_to_list(table, soup))
            notes.append(f"table {n} flattened to a bullet list")
    elif tables == "image":
        for n, table in enumerate(soup.find_all("table"), 1):
            head = [_squash(c.get_text()) for c in table.find_all("th")][:2]
            caption = " / ".join(h for h in head if h) or f"table {n}"
            target = (image_dir or Path(".")) / f"{stem}-table-{n}.png"
            try:
                render_table_png(table, target)
                table_pngs.append(f"{target.name}  ({caption})")
                placeholder = soup.new_tag("p")
                em = soup.new_tag("em")
                em.string = f"[Table {n}: {caption} — upload {target.name}]"
                placeholder.append(em)
                table.replace_with(placeholder)
            except (FileNotFoundError, OSError, ValueError, subprocess.SubprocessError) as exc:
                table.replace_with(table_to_list(table, soup))
                notes.append(f"table {n}: render failed ({exc.__class__.__name__}), flattened")

    # A fenced block keeps the newline before its closing fence, and <pre>
    # renders that as an empty line under the code. Strip it here rather than
    # apologising for it in the editor.
    for pre in soup.find_all("pre"):
        holder = pre.find("code") or pre
        text = holder.get_text()
        trimmed = text.rstrip("\n")
        if trimmed != text:
            holder.string = trimmed

    if degrade_code:
        for n, pre in enumerate(soup.find_all("pre"), 1):
            pre.replace_with(pre_to_quote(pre, soup))
            notes.append(f"code block {n} flattened to a quote")

    for img in soup.find_all("img"):
        alt = img.get("alt") or "image"
        src = img.get("src", "")
        images.append(f"{alt}  ({src})")
        placeholder = soup.new_tag("p")
        em = soup.new_tag("em")
        em.string = f"[Image: {alt}]"
        placeholder.append(em)
        img.replace_with(placeholder)

    for a in soup.find_all("a"):
        rewrite_link(a, base)

    for tag in soup.find_all(True):
        if tag.name in KEEP:
            allowed = KEEP_ATTRS.get(tag.name, set())
            for attr in list(tag.attrs):
                if tag.name == "a" and attr in ("href", "title"):
                    continue
                if attr in allowed:
                    continue
                del tag[attr]
            continue
        tag.unwrap()

    fragment = soup.decode()
    # No newlines between tags: some editors turn a newline between blocks into
    # an extra blank line on paste. Only newlines are removed, never a space —
    # a meaningful space between two inline tags stays put.
    fragment = re.sub(r">\n\s*<", "><", fragment)
    fragment = fragment.strip()
    return fragment, notes, images, table_pngs


def wrap_document(fragment: str, title: str) -> str:
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>{title}</title>
<style>
  body {{ max-width: 46rem; margin: 3rem auto; padding: 0 1.25rem;
         font: 18px/1.6 -apple-system, "Segoe UI", Roboto, sans-serif; color: #1b1f23; }}
  h1 {{ font-size: 2rem; line-height: 1.2; }}
  h2 {{ font-size: 1.4rem; margin-top: 2rem; }}
  p {{ margin: 0 0 .55em; }}
  blockquote {{ border-left: 3px solid #c9ced3; margin: 1.25rem 0; padding: .25rem 1rem;
                color: #444; }}
  code {{ font-family: ui-monospace, monospace; background: #f2f4f6; padding: .1rem .3rem; }}
</style>
</head>
<body>
{fragment}
</body>
</html>
"""


def main() -> int:
    ap = argparse.ArgumentParser(description="Markdown -> LinkedIn rich text")
    ap.add_argument("source", type=Path, help="markdown file")
    ap.add_argument("--image-dir", type=Path, default=None,
                    help="where table PNGs go (default: imgs/linkedin-tables/ beside a docs/ article)")
    ap.add_argument("--out", type=Path, default=None,
                    help="html output path (default: <source>-linkedin.html, beside the article)")
    ap.add_argument("--base", default=BASE_DEFAULT,
                    help="base URL for relative links")
    ap.add_argument("--no-clip", action="store_true", help="do not touch the clipboard")
    ap.add_argument("--tables", choices=("flatten", "image", "keep"), default="flatten",
                    help="flatten: bullet list (default, what LinkedIn can hold); "
                         "image: screenshot each table to PNG and leave a placeholder; "
                         "keep: emit <table> for a target that renders it")
    ap.add_argument("--degrade-code", action="store_true",
                    help="flatten code blocks into quotes (use only if the editor drops them)")
    ap.add_argument("--docx", action="store_true",
                    help="also convert the HTML to .docx with soffice, for pasting from Writer")
    ap.add_argument("--styled", action="store_true",
                    help="write a full HTML document with CSS, for reading in a browser "
                         "(the default file is the paste payload and must not be copied whole)")
    ap.add_argument("--print", dest="print_html", action="store_true",
                    help="print the fragment to stdout instead of writing a file")
    args = ap.parse_args()

    if not args.source.exists():
        print(f"no such file: {args.source}", file=sys.stderr)
        return 1

    md_text = args.source.read_text(encoding="utf-8")
    out_dir = (args.out.parent if args.out else args.source.parent)
    if args.image_dir is not None:
        image_dir = args.image_dir
    elif args.source.parent.name == "docs":
        # project layout: docs/<article>.md pairs with imgs/linkedin-tables/
        image_dir = args.source.parent.parent / "imgs" / "linkedin-tables"
    else:
        image_dir = out_dir / "linkedin-tables"
    image_dir.mkdir(parents=True, exist_ok=True)
    fragment, notes, images, table_pngs = convert(
        md_text, args.base,
        tables=args.tables,
        degrade_code=args.degrade_code,
        image_dir=image_dir,
        stem=args.source.stem,
    )

    title = args.source.stem
    # The file exists to be copied into the editor, so it holds the fragment —
    # never a full document. A <title>/<style> block in the payload shows up as
    # literal CSS text in some editors. --styled writes the preview instead.
    payload = wrap_document(fragment, title) if args.styled else fragment

    if args.print_html:
        print(fragment)
    else:
        out = args.out or args.source.with_name(f"{title}-linkedin.html")
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(payload, encoding="utf-8")
        print(f"html:    {out}")

    if not args.no_clip:
        try:
            # `wl-copy -f` serves the clipboard until something replaces it. Run
            # it in its own session: forked into ours, it dies when the parent's
            # process group is cleaned up, and the paste then finds an empty
            # clipboard. Detached, it outlives this script.
            proc = subprocess.Popen(
                ["wl-copy", "-f", "--type", "text/html"],
                stdin=subprocess.PIPE, stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL, text=True, start_new_session=True,
            )
            proc.stdin.write(fragment)
            proc.stdin.close()
            print("clipboard: rich text ready — paste into the article editor")
            print(f"clipboard owner: wl-copy pid {proc.pid} (keep it alive until you paste)")
        except FileNotFoundError:
            print("clipboard: wl-copy not found — use the html file and copy from a browser",
                  file=sys.stderr)
        except subprocess.TimeoutExpired:
            print("clipboard: wl-copy did not return — use the html file instead",
                  file=sys.stderr)
        except subprocess.SubprocessError as exc:
            print(f"clipboard: wl-copy failed ({exc})", file=sys.stderr)

    if args.docx and not args.print_html:
        try:
            subprocess.run(
                ["soffice", "--headless", "--convert-to", "docx",
                 "--outdir", str(out.parent), str(out)],
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                timeout=120, check=True,
            )
            print(f"docx:    {out.with_suffix('.docx')}  (open in Writer, copy, paste)")
        except (FileNotFoundError, subprocess.SubprocessError) as exc:
            print(f"docx: conversion failed ({exc.__class__.__name__})", file=sys.stderr)

    if table_pngs:
        print(f"\ntables rendered to PNG in {image_dir} — upload each at its placeholder:")
        for i, png in enumerate(table_pngs, 1):
            print(f"  {i}. {png}")

    if images:
        print("\nimages to upload by hand, in order:")
        for i, img in enumerate(images, 1):
            print(f"  {i}. {img}")

    if notes:
        print("\nconverted, check before publishing:")
        for n in notes:
            print(f"  - {n}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
