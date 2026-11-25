#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.11"
# dependencies = ["markdown", "beautifulsoup4"]
# ///
"""Convert a Markdown article into a Medium paste payload.

Medium's editor deletes an <img> whose src is a data: URI, with no error and no
placeholder. So unlike the LinkedIn converter, this one never inlines bytes:
every image points at a public URL, and the payload is only called ready once
those URLs are actually pushed.

Medium has no table model, so tables become PNGs at 2x (hosted like any image)
or bullet lists. The article's H1 is dropped and printed, because a paste never
fills Medium's Title field.

Two routes reach Medium, and this script targets the better one. Pasting into
the editor keeps multi-line code. The importer at medium.com/p/import flattens
<pre> to a single line and drops tables, so it is not served here.
"""

from __future__ import annotations

import argparse
import re
import signal
import subprocess
import sys
import time
from pathlib import Path

import markdown
from bs4 import BeautifulSoup, NavigableString, Tag

BASE_DEFAULT = "https://github.com/j3ffyang/ai-thoughts/blob/main/docs/"
IMAGE_BASE_DEFAULT = "https://raw.githubusercontent.com/j3ffyang/ai-thoughts/main/"
REMOTE_REF_DEFAULT = "j3ffyang/main"

KEEP = {
    "p", "h1", "h2", "h3", "strong", "em", "b", "i", "code",
    "ul", "ol", "li", "blockquote", "a", "hr", "br", "pre", "img",
}
# Medium's editor has no table model, so no table tags survive.
KEEP_ATTRS = {"img": {"src", "alt"}}
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
    """Medium draws no table. Each row becomes one bullet: the first cell
    bolded, the rest joined with a middle dot."""
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


def _same_pixels(a: Path, b: Path) -> bool:
    """True when two PNGs hold the same picture, whatever their bytes say.

    A re-render is not byte-identical — ImageMagick embeds metadata — so bytes
    would flag an unchanged table as edited and block a payload that is already
    hosted. Pixels are the honest comparison.
    """
    try:
        # -fuzz 2% because the encoder is palette-reducing: an older file made by
        # the same pipeline compares exactly, but one made before that step would
        # otherwise read as changed and be regenerated on every run.
        done = subprocess.run(
            ["magick", "compare", "-metric", "AE", "-fuzz", "2%", str(a), str(b), "null:"],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=60,
        )
    except (OSError, subprocess.SubprocessError):
        return False
    return done.returncode == 0


def render_table_png(table: Tag, out: Path) -> None:
    """Screenshot one table with headless Chromium, then trim to content.

    Chromium renders at 2x for crisp text; the window is deliberately wider and
    taller than any table, and ImageMagick trims the surplus away. An existing
    file whose pixels match is kept as-is, so a pushed image stays valid across
    re-runs.
    """
    out = out.resolve()
    rows = table.find_all("tr")
    cols = max((len(r.find_all(["th", "td"])) for r in rows), default=1)
    width = max(900, 300 * cols)

    html_path = out.with_name(f".{out.stem}.src.html")
    png_path = out.with_name(f".{out.stem}.shot.png")
    new_path = out.with_name(f".{out.stem}.new.png")
    html_path.write_text(_table_page(str(table), out.stem), encoding="utf-8")

    subprocess.run(
        ["chromium", "--headless", "--no-sandbox", "--disable-gpu",
         "--hide-scrollbars", "--force-device-scale-factor=2",
         f"--window-size={width},4000", f"--screenshot={png_path}",
         html_path.as_uri()],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        timeout=120, check=True,
    )
    # Keep the file small as well as crisp: trim to content, cap the long edge at
    # twice the widest display width the images are pasted at, then drop metadata
    # and palette-reduce. A table is flat colour, so 64 colours is visually free
    # at this size. The filename and directory never change, because the hosted
    # URL is this path and published posts keep pointing at it.
    subprocess.run(
        ["magick", str(png_path), "-trim", "+repage",
         "-bordercolor", "white", "-border", "12",
         "-resize", "1600x>", "-strip", "-colors", "64", str(new_path)],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        timeout=60, check=True,
    )
    if out.exists() and _same_pixels(out, new_path):
        new_path.unlink(missing_ok=True)
    else:
        new_path.replace(out)
    for leftover in (html_path, png_path):
        leftover.unlink(missing_ok=True)


def _git(repo: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(["git", "-C", str(repo), *args],
                          capture_output=True, text=True)


def blob_at(repo: Path, ref: str, relpath: str) -> str | None:
    """The blob hash of relpath at ref, or None when the ref lacks it."""
    result = _git(repo, "rev-parse", f"{ref}:{relpath}")
    return result.stdout.strip() if result.returncode == 0 else None


def blob_local(repo: Path, path: Path) -> str | None:
    result = _git(repo, "hash-object", str(path))
    return result.stdout.strip() if result.returncode == 0 else None


def host_status(repo: Path | None, ref: str, path: Path, relpath: str) -> str:
    """hosted | changed since push | not pushed | uncheckable."""
    if repo is None:
        return "uncheckable"
    pushed = blob_at(repo, ref, relpath)
    if pushed is None:
        return "not pushed"
    local = blob_local(repo, path)
    if local is not None and local != pushed:
        return "changed since push"
    return "hosted"


def convert(md_text: str, base: str, *, tables: str = "image",
            image_dir: Path | None = None, stem: str = "table",
            source_dir: Path | None = None,
            ) -> tuple[str, list[str], list[tuple[Tag, Path, str]], list[str]]:
    """Return (soup, notes, images, title_lines).

    The DOM comes back undecoded: the caller sets each image's src, which needs
    the URL base and the repo root. Decoding before that would ship <img> tags
    with no source at all.
    """
    html = markdown.markdown(
        strip_frontmatter(md_text),
        extensions=["extra", "sane_lists", "nl2br"],
    )
    soup = BeautifulSoup(html, "html.parser")
    notes: list[str] = []
    title_lines: list[str] = []

    for tag in soup.find_all(list(DROP)):
        tag.decompose()

    # Medium's quote is one block. A <p> nested inside <blockquote> gives its
    # editor a paragraph boundary to turn into an empty line, so a
    # single-paragraph quote is flattened to its text. A multi-paragraph quote
    # keeps its <p>s: there the breaks are the point.
    for quote in soup.find_all("blockquote"):
        kids = [c for c in quote.contents
                if not (isinstance(c, NavigableString) and not c.strip())]
        if len(kids) == 1 and isinstance(kids[0], Tag) and kids[0].name == "p":
            inner = kids[0]
            moved = [c.extract() for c in list(inner.contents)]
            quote.clear()
            for child in moved:
                quote.append(child)

    # The first H1 is the article title, and Medium's title lives in its own
    # field. Leaving it in the body pastes a second title.
    first_h1 = soup.find("h1")
    if first_h1 is not None:
        title_lines.append(_squash(first_h1.get_text()))
        first_h1.decompose()
        notes.append("first H1 dropped — type it into Medium's Title field")

    for extra in soup.find_all("h1"):
        extra.name = "h2"
        notes.append("a second H1 demoted to H2")

    # Medium's editor offers title, subtitle and two heading sizes.
    for deep in soup.find_all(["h4", "h5", "h6"]):
        was = deep.name
        deep.name = "h3"
        notes.append(f"<{was}> demoted to h3 — Medium has no h4 or below")

    sources: dict[int, tuple[Path, str]] = {}
    table_pngs: list[str] = []

    if tables == "list":
        for n, table in enumerate(soup.find_all("table"), 1):
            table.replace_with(table_to_list(table, soup))
            notes.append(f"table {n} flattened to a bullet list")
    else:
        for n, table in enumerate(soup.find_all("table"), 1):
            # Skip empty header cells: a comparison table often leaves the
            # first corner blank, and that blank would take a caption slot.
            head = [h for h in (_squash(c.get_text()) for c in table.find_all("th")) if h][:2]
            caption = " / ".join(h for h in head if h) or f"table {n}"
            target = ((image_dir or Path(".")) / f"{stem}-table-{n}.png").resolve()
            try:
                render_table_png(table, target)
                img = soup.new_tag("img")
                img["alt"] = caption
                sources[id(img)] = (target, caption)
                table.replace_with(img)
                table_pngs.append(f"{target.name}  ({caption})")
            except (FileNotFoundError, OSError, ValueError,
                    subprocess.SubprocessError) as exc:
                table.replace_with(table_to_list(table, soup))
                notes.append(f"table {n}: render failed "
                             f"({exc.__class__.__name__}), flattened")

    for pre in soup.find_all("pre"):
        holder = pre.find("code") or pre
        text = holder.get_text()
        trimmed = text.rstrip("\n")
        if trimmed != text:
            holder.string = trimmed

    for img in soup.find_all("img"):
        if id(img) in sources:
            continue
        alt = img.get("alt") or "image"
        src = img.get("src", "")
        if src.startswith(("http://", "https://")):
            notes.append(f"remote image kept as-is: {alt}")
            continue
        if src.startswith("data:"):
            notes.append(f"data: URI image — Medium deletes these; host it: {alt}")
            continue
        path = (source_dir or Path(".")) / src
        sources[id(img)] = (path.resolve(), alt)
        if img.find_parent("a") is not None:
            notes.append(f"image sits inside a link — Medium may drop it: {alt}")

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

    images = [(img, *sources[id(img)]) for img in soup.find_all("img")
              if id(img) in sources]

    return soup, notes, images, title_lines


def main() -> int:
    ap = argparse.ArgumentParser(description="Markdown -> Medium paste payload")
    ap.add_argument("source", type=Path, help="markdown file")
    ap.add_argument("--out", type=Path, default=None,
                    help="html output path (default: <source>-medium.html)")
    ap.add_argument("--image-dir", type=Path, default=None,
                    help="where table PNGs go (default: imgs/medium-tables/ beside a docs/ article)")
    ap.add_argument("--image-base", default=IMAGE_BASE_DEFAULT,
                    help="public URL prefix for hosted images")
    ap.add_argument("--base", default=BASE_DEFAULT,
                    help="base URL for relative links")
    ap.add_argument("--tables", choices=("image", "list"), default="image",
                    help="image: screenshot each table to PNG and host it (default); "
                         "list: flatten to a bullet list, no hosting needed")
    ap.add_argument("--remote-ref", default=REMOTE_REF_DEFAULT,
                    help="ref the image URLs must exist in (default: j3ffyang/main)")
    ap.add_argument("--allow-unpushed", action="store_true",
                    help="write the payload even when an image is not pushed (Medium "
                         "will drop it without a word)")
    ap.add_argument("--clip", action="store_true",
                    help="also put the payload on the clipboard with wl-copy")
    ap.add_argument("--print", dest="print_html", action="store_true",
                    help="print the fragment to stdout instead of writing a file")
    args = ap.parse_args()

    if not args.source.exists():
        print(f"no such file: {args.source}", file=sys.stderr)
        return 1

    source_dir = args.source.parent
    out_dir = args.out.parent if args.out else source_dir
    if args.image_dir is not None:
        image_dir = args.image_dir
    elif source_dir.name == "docs":
        image_dir = source_dir.parent / "imgs" / "medium-tables"
    else:
        image_dir = out_dir / "medium-tables"
    image_dir = image_dir.resolve()
    image_dir.mkdir(parents=True, exist_ok=True)

    repo = None
    probe = _git(source_dir, "rev-parse", "--show-toplevel")
    if probe.returncode == 0:
        repo = Path(probe.stdout.strip())

    md_text = args.source.read_text(encoding="utf-8")
    soup, notes, images, title_lines = convert(
        md_text, args.base,
        tables=args.tables,
        image_dir=image_dir,
        stem=args.source.stem,
        source_dir=source_dir,
    )

    base = args.image_base.rstrip("/") + "/"
    blocked: list[tuple[str, str, str]] = []
    rows: list[tuple[str, str, str]] = []
    for img, path, alt in images:
        if repo is None:
            img["src"] = path.as_uri()
            rows.append((alt, "uncheckable", "no git repo found"))
            blocked.append((alt, "uncheckable", str(path)))
            continue
        try:
            relpath = path.relative_to(repo).as_posix()
        except ValueError:
            img["src"] = path.as_uri()
            rows.append((alt, "outside repo", "cannot be hosted from here"))
            blocked.append((alt, "outside repo", str(path)))
            continue
        img["src"] = base + relpath
        status = host_status(repo, args.remote_ref, path, relpath)
        rows.append((alt, status, relpath))
        if status != "hosted":
            blocked.append((alt, status, relpath))

    fragment = soup.decode()
    fragment = re.sub(r">\n\s*<", "><", fragment).strip()

    if args.print_html:
        print(fragment)
    else:
        out = args.out or args.source.with_name(f"{args.source.stem}-medium.html")
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(fragment, encoding="utf-8")
        print(f"html:    {out}")

    if title_lines:
        print(f"\ntitle:   {title_lines[0]}")
        print("  type this into Medium's Title field — a paste never fills it")

    if rows:
        print(f"\n{len(rows)} image(s), hosted at {base}:")
        for i, (alt, status, relpath) in enumerate(rows, 1):
            print(f"  {i}. [{status}] {alt}")
            print(f"     {relpath}")

    if blocked:
        sys.stdout.flush()
        print(f"\nBLOCKED — {len(blocked)} image(s) will not appear in Medium:", file=sys.stderr)
        for alt, status, relpath in blocked:
            print(f"  - {alt}: {status} ({relpath})", file=sys.stderr)
        print("  Medium deletes an image it cannot fetch without saying so.", file=sys.stderr)
        print("  commit and push the images, then run this again:", file=sys.stderr)
        try:
            add_dir = image_dir.relative_to(repo).as_posix() if repo else "imgs/"
        except ValueError:
            add_dir = "imgs/"
        print(f"    git add {add_dir} && git commit -m 'docs: host images' "
              f"&& git push {args.remote_ref.split('/')[0]} main", file=sys.stderr)
        if not args.allow_unpushed:
            print("  (payload written anyway; --allow-unpushed silences the exit code)",
                  file=sys.stderr)
            return 1

    if args.clip and not args.print_html:
        try:
            proc = subprocess.Popen(
                ["wl-copy", "-f", "--type", "text/html"],
                stdin=subprocess.PIPE, stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL, text=True, start_new_session=True,
            )
            try:
                proc.stdin.write(fragment)
                proc.stdin.close()
            except OSError as exc:
                print(f"clipboard: wl-copy closed early ({exc.__class__.__name__})",
                      file=sys.stderr)
            else:
                time.sleep(0.2)
                if proc.poll() is not None:
                    print(f"clipboard: wl-copy exited with status {proc.returncode}",
                          file=sys.stderr)
                else:
                    print(f"clipboard: ready — wl-copy pid {proc.pid} (keep it alive)")
        except FileNotFoundError:
            print("clipboard: wl-copy not found — copy the file from a browser",
                  file=sys.stderr)

    if notes:
        print("\nconverted, check before publishing:")
        for note in notes:
            print(f"  - {note}")

    return 0


if __name__ == "__main__":
    # `| head` is a normal way to inspect the report; die quietly on a closed
    # pipe instead of failing during interpreter shutdown.
    signal.signal(signal.SIGPIPE, signal.SIG_DFL)
    raise SystemExit(main())
