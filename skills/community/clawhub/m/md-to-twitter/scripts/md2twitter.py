#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.11"
# dependencies = ["markdown", "beautifulsoup4", "requests"]
# ///
"""Turn a Markdown article into an X thread, and optionally post it.

X has no rich text and no way to carry an image in a paste. A thread is plain
text, split at 280 weighted characters, with each image uploaded and attached to
the post that mentions it. So this converts to a numbered script you can copy
from, and `--post` does the copying for you.

Formatting is degraded on purpose: X renders no bold, no headings, no tables, no
code blocks. Markers are stripped and the words are kept. Links survive as text
plus URL, because a URL costs 23 characters however long it is.

Character counting follows X's weighted rules: most characters cost 1, CJK and
emoji cost 2, and every URL costs 23. See --limit to change the ceiling.
"""

from __future__ import annotations

import argparse
import base64
import hashlib
import hmac
import json
import mimetypes
import os
import re
import secrets
import subprocess
import sys
import time
import urllib.parse
from dataclasses import dataclass, field
from pathlib import Path

import markdown
import requests
from bs4 import BeautifulSoup, NavigableString, Tag

API = "https://api.x.com"
DEFAULT_LIMIT = 280
MAX_IMAGES = 4
MAX_IMAGE_BYTES = 5 * 1024 * 1024
BASE = "https://github.com/j3ffyang/ai-thoughts/blob/main/docs/"

# Code points X counts as two: CJK, Hangul, kana, full-width forms, emoji.
WEIGHT2 = (
    (0x1100, 0x115F), (0x2E80, 0x303E), (0x3041, 0x33FF),
    (0x3400, 0x4DBF), (0x4E00, 0x9FFF), (0xA000, 0xA4CF),
    (0xAC00, 0xD7A3), (0xF900, 0xFAFF), (0xFE30, 0xFE4F),
    (0xFF00, 0xFF60), (0xFFE0, 0xFFE6), (0x1F000, 0x1FAFF),
    (0x20000, 0x3FFFD),
)

FRONTMATTER = re.compile(r"\A---\n.*?\n---\n", re.S)
URL_RE = re.compile(r"https?://[^\s<>\"']+")
TRAILING = ".,;:!?)]}'\""

MIME = {
    ".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg",
    ".gif": "image/gif", ".webp": "image/webp",
}


@dataclass
class Post:
    text: str = ""
    images: list[Path] = field(default_factory=list)

    def weight(self) -> int:
        return weighted_len(self.text)


def _weight2(cp: int) -> bool:
    return any(lo <= cp <= hi for lo, hi in WEIGHT2)


def _url_spans(text: str) -> list[tuple[int, int]]:
    spans = []
    for m in URL_RE.finditer(text):
        end = m.end()
        while end > m.start() and text[end - 1] in TRAILING:
            end -= 1
        spans.append((m.start(), end))
    return spans


def weighted_len(text: str) -> int:
    """X's counting rule: 1 per character, 2 for CJK/emoji, 23 per URL."""
    spans = _url_spans(text)
    total = 0
    i = 0
    while i < len(text):
        for start, end in spans:
            if i == start:
                total += 23
                i = end
                break
        else:
            total += 2 if _weight2(ord(text[i])) else 1
            i += 1
    return total


def _squash(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def inline_text(tag: Tag, images: list[Path], source_dir: Path) -> str:
    """Flatten inline markup to plain text, collecting any images found."""
    out: list[str] = []
    for child in tag.children:
        if isinstance(child, NavigableString):
            out.append(str(child))
            continue
        if not isinstance(child, Tag):
            continue
        name = child.name
        if name == "img":
            src = child.get("src", "")
            if src and not src.startswith(("http://", "https://", "data:")):
                images.append((source_dir / src).resolve())
            continue
        if name == "a":
            href = child.get("href", "")
            label = _squash(child.get_text())
            if href and not href.startswith(("#", "mailto:")):
                if href.startswith(("http://", "https://")):
                    out.append(f"{label} ({href})" if label and label != href else href)
                    continue
                out.append(f"{label} ({BASE.rstrip('/')}/{href.lstrip('./')})"
                           if label and label != href else href)
                continue
            out.append(label)
            continue
        if name == "code":
            out.append(f"`{child.get_text()}`")
            continue
        out.append(inline_text(child, images, source_dir))
    return "".join(out)


def block_text(tag: Tag, images: list[Path], source_dir: Path) -> str:
    name = tag.name
    if name in ("h1", "h2", "h3", "h4", "h5", "h6"):
        return _squash(inline_text(tag, images, source_dir))
    if name == "p":
        return _squash(inline_text(tag, images, source_dir))
    if name in ("ul", "ol"):
        lines = []
        for i, li in enumerate(tag.find_all("li", recursive=False), 1):
            body = _squash(inline_text(li, images, source_dir))
            lines.append(f"{i}. {body}" if name == "ol" else f"• {body}")
        return "\n".join(lines)
    if name == "blockquote":
        body = _squash(inline_text(tag, images, source_dir))
        return "\n".join(f"> {line}" for line in body.split("\n"))
    if name == "pre":
        holder = tag.find("code") or tag
        return holder.get_text().rstrip("\n")
    if name == "table":
        rows = []
        for tr in tag.find_all("tr"):
            cells = [_squash(inline_text(c, images, source_dir))
                     for c in tr.find_all(["th", "td"])]
            cells = [c for c in cells if c]
            if cells:
                # "|" separates cells; an em-dash inside a cell stays readable.
                rows.append(" | ".join(cells))
        return "\n".join(rows)
    if name == "hr":
        return ""
    return _squash(inline_text(tag, images, source_dir))


def _block_page(fragment: str, kind: str) -> str:
    """A minimal page that renders one block the way its screenshot should look."""
    if kind == "code":
        style = (
            "body { margin: 0; background: #fff; }"
            "pre { display: inline-block; margin: 16px; padding: 14px 18px;"
            " background: #f6f8fa; border: 1px solid #d0d7de; border-radius: 6px;"
            " font: 14px/1.55 ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;"
            " color: #111; white-space: pre; }"
        )
    else:
        style = (
            "body { margin: 0; background: #fff;"
            " font: 15px/1.45 -apple-system, 'Segoe UI', Roboto, sans-serif; }"
            "table { border-collapse: collapse; margin: 16px; }"
            "th, td { border: 1px solid #c9ced6; padding: 8px 14px;"
            " text-align: left; vertical-align: top; }"
            "th { background: #f2f5f8; }"
            "code { font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; }"
        )
    return (
        '<!doctype html><html><head><meta charset="utf-8">'
        f"<style>{style}</style></head><body>{fragment}</body></html>"
    )


def render_block_png(tag: Tag, out: Path, kind: str) -> None:
    """Screenshot one code block or table with headless Chromium, then trim it.

    The sibling skills draw tables this way; X needs the same trick for code,
    because X renders neither. Chromium renders at 2x for crisp text and
    ImageMagick trims the surplus window.
    """
    out = out.resolve()
    width = 900
    if kind == "table":
        rows = tag.find_all("tr")
        cols = max((len(r.find_all(["th", "td"])) for r in rows), default=1)
        width = max(900, 300 * cols)
    src = out.with_name(f".{out.stem}.src.html")
    shot = out.with_name(f".{out.stem}.shot.png")
    src.write_text(_block_page(str(tag), kind), encoding="utf-8")
    subprocess.run(
        ["chromium", "--headless", "--no-sandbox", "--disable-gpu",
         "--hide-scrollbars", "--force-device-scale-factor=2",
         f"--window-size={width},4000", f"--screenshot={shot}",
         src.as_uri()],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        timeout=120, check=True,
    )
    # Trim, cap the long edge at twice the widest display width, drop metadata
    # and palette-reduce: a table or code block is flat colour, so 64 colours is
    # visually free. The filename never changes — the bytes are uploaded.
    subprocess.run(
        ["magick", str(shot), "-trim", "+repage",
         "-bordercolor", "white", "-border", "12",
         "-resize", "1600x>", "-strip", "-colors", "64", str(out)],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        timeout=60, check=True,
    )
    for leftover in (src, shot):
        leftover.unlink(missing_ok=True)


def split_sentences(text: str) -> list[str]:
    parts = re.split(r"(?<=[.!?])\s+", text)
    return [p for p in parts if p]


def pack(chunks: list[str], limit: int, sep: str) -> list[str]:
    """Greedily join chunks under the limit; never drop a chunk."""
    out: list[str] = []
    current = ""
    for chunk in chunks:
        candidate = f"{current}{sep}{chunk}" if current else chunk
        if weighted_len(candidate) <= limit:
            current = candidate
            continue
        if current:
            out.append(current)
        if weighted_len(chunk) <= limit:
            current = chunk
            continue
        # A single chunk is too long: cut it at words, then hard.
        words = chunk.split(" ")
        piece = ""
        for word in words:
            cand = f"{piece} {word}" if piece else word
            if weighted_len(cand) <= limit:
                piece = cand
                continue
            if piece:
                out.append(piece)
            while weighted_len(word) > limit:
                cut = _hard_cut(word, limit)
                out.append(cut)
                word = word[len(cut):]
            piece = word
        if piece:
            out.append(piece)
        current = ""
    if current:
        out.append(current)
    return out


def split_block(text: str, limit: int) -> list[str]:
    """Split a block under the limit, keeping rows and sentences whole.

    A table row or a list item is a line; cutting one mid-phrase reads worse
    than starting a new post. So lines are packed first, and only a line that
    is itself too long gets cut at sentence, then word, boundaries.
    """
    if "\n" in text:
        return pack(text.split("\n"), limit, "\n")
    return pack(split_sentences(text), limit, " ")


def _hard_cut(word: str, limit: int) -> str:
    total = 0
    for i, ch in enumerate(word):
        total += 2 if _weight2(ord(ch)) else 1
        if total > limit:
            return word[:i]
    return word


def convert(md_text: str, source_dir: Path, limit: int = DEFAULT_LIMIT,
            number: bool = False, code: str = "text", tables: str = "text",
            image_dir: Path | None = None, stem: str = "block"
            ) -> tuple[list[Post], list[str]]:
    html = markdown.markdown(
        FRONTMATTER.sub("", md_text, count=1),
        extensions=["extra", "sane_lists", "nl2br"],
    )
    soup = BeautifulSoup(html, "html.parser")
    notes: list[str] = []

    budget = limit - (len("99/99 ") if number else 0)
    posts: list[Post] = []
    current = Post()

    def flush() -> None:
        nonlocal current
        if current.text.strip() or current.images:
            posts.append(current)
        current = Post()

    code_no = 0
    table_no = 0
    for tag in soup.find_all(True, recursive=False):
        images: list[Path] = []
        text = block_text(tag, images, source_dir)
        text = text.strip()

        if tag.name == "pre" and code == "image":
            code_no += 1
            target = (image_dir or source_dir) / f"{stem}-code-{code_no}.png"
            render_block_png(tag, target, "code")
            images.append(target)
            text = ""
        elif tag.name == "table" and tables == "image":
            table_no += 1
            target = (image_dir or source_dir) / f"{stem}-table-{table_no}.png"
            render_block_png(tag, target, "table")
            images.append(target)
            text = ""

        if images:
            if len(current.images) + len(images) > MAX_IMAGES:
                flush()
            current.images.extend(images)

        if not text:
            continue

        pieces = [text]
        if weighted_len(text) > budget:
            pieces = split_block(text, budget)

        for piece in pieces:
            candidate = f"{current.text}\n\n{piece}" if current.text else piece
            if weighted_len(candidate) <= budget:
                current.text = candidate
                continue
            flush()
            current.text = piece
            if weighted_len(piece) > budget:
                notes.append("a block exceeded the limit and was split mid-sentence")

    flush()

    if number and len(posts) > 1:
        total = len(posts)
        for i, post in enumerate(posts, 1):
            post.text = f"{i}/{total} {post.text}"

    if not posts:
        notes.append("nothing convertible: the article produced no text")

    return posts, notes


def load_credentials() -> dict[str, str] | None:
    keys = ("consumer_key", "consumer_secret", "access_token", "access_token_secret")
    env_map = {
        "consumer_key": "X_CONSUMER_KEY",
        "consumer_secret": "X_CONSUMER_SECRET",
        "access_token": "X_ACCESS_TOKEN",
        "access_token_secret": "X_ACCESS_TOKEN_SECRET",
    }
    found = {k: os.environ.get(env_map[k], "") for k in keys}
    if all(found.values()):
        return found
    path = Path.home() / ".config" / "md-to-twitter" / "keys.json"
    if path.is_file():
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return None
        if all(data.get(k) for k in keys):
            return {k: data[k] for k in keys}
    return None


def oauth_header(method: str, url: str, creds: dict[str, str]) -> str:
    """OAuth 1.0a HMAC-SHA1. JSON and multipart bodies are not signed."""
    params = {
        "oauth_consumer_key": creds["consumer_key"],
        "oauth_nonce": secrets.token_hex(16),
        "oauth_signature_method": "HMAC-SHA1",
        "oauth_timestamp": str(int(time.time())),
        "oauth_token": creds["access_token"],
        "oauth_version": "1.0",
    }
    enc = lambda s: urllib.parse.quote(str(s), safe="~")  # noqa: E731
    base = "&".join([
        method.upper(),
        enc(url),
        enc("&".join(f"{enc(k)}={enc(v)}" for k, v in sorted(params.items()))),
    ])
    key = f"{enc(creds['consumer_secret'])}&{enc(creds['access_token_secret'])}"
    digest = hmac.new(key.encode(), base.encode(), hashlib.sha1).digest()
    params["oauth_signature"] = base64.b64encode(digest).decode()
    return "OAuth " + ", ".join(f'{enc(k)}="{enc(v)}"' for k, v in sorted(params.items()))


def upload_image(path: Path, creds: dict[str, str]) -> str:
    if not path.is_file():
        raise FileNotFoundError(f"image not found: {path}")
    size = path.stat().st_size
    if size > MAX_IMAGE_BYTES:
        raise ValueError(f"{path.name} is {size / 1048576:.1f} MB; X accepts 5 MB")
    url = f"{API}/2/media/upload"
    headers = {"Authorization": oauth_header("POST", url, creds)}
    mime = MIME.get(path.suffix.lower()) or mimetypes.guess_type(path.name)[0] or "image/png"
    with path.open("rb") as fh:
        resp = requests.post(
            url, headers=headers, timeout=120,
            files={"media": (path.name, fh, mime)},
            data={"media_category": "tweet_image"},
        )
    if resp.status_code >= 300:
        raise RuntimeError(f"media upload failed ({resp.status_code}): {resp.text[:300]}")
    body = resp.json()
    data = body.get("data") or body
    media_id = data.get("id") or data.get("media_id_string") or data.get("media_id")
    if not media_id:
        raise RuntimeError(f"media upload returned no id: {str(body)[:300]}")
    return str(media_id)


def create_post(text: str, media_ids: list[str], creds: dict[str, str],
                reply_to: str | None = None) -> str:
    url = f"{API}/2/tweets"
    payload: dict = {}
    if text.strip():
        payload["text"] = text
    if media_ids:
        payload["media"] = {"media_ids": media_ids}
    if reply_to:
        payload["reply"] = {"in_reply_to_tweet_id": reply_to}
    headers = {
        "Authorization": oauth_header("POST", url, creds),
        "Content-Type": "application/json",
    }
    resp = requests.post(url, headers=headers, json=payload, timeout=60)
    if resp.status_code >= 300:
        raise RuntimeError(f"post failed ({resp.status_code}): {resp.text[:300]}")
    body = resp.json()
    tweet_id = (body.get("data") or {}).get("id")
    if not tweet_id:
        raise RuntimeError(f"post returned no id: {str(body)[:300]}")
    return str(tweet_id)


def main() -> int:
    ap = argparse.ArgumentParser(description="Markdown -> X thread")
    ap.add_argument("source", type=Path, help="markdown file")
    ap.add_argument("--out", type=Path, default=None,
                    help="thread text output (default: <source>-twitter.txt)")
    ap.add_argument("--limit", type=int, default=DEFAULT_LIMIT,
                    help=f"characters per post (default {DEFAULT_LIMIT})")
    ap.add_argument("--number", action="store_true",
                    help="prefix each post with n/N")
    ap.add_argument("--post", action="store_true",
                    help="post the thread to X (needs OAuth 1.0a credentials)")
    ap.add_argument("--reply-to", default=None,
                    help="tweet id to chain this post under")
    ap.add_argument("--at", type=int, default=None,
                    help="act on post N only (1-based): print it, or with --post, "
                         "post that one and print the command for the next")
    ap.add_argument("--dry-run", action="store_true",
                    help="with --post: print what would be sent, touch nothing")
    ap.add_argument("--print", dest="print_text", action="store_true",
                    help="print the thread to stdout instead of writing a file")
    ap.add_argument("--code", choices=("text", "image"), default="text",
                    help="text: keep code blocks as plain text (default); "
                         "image: screenshot each code block to PNG and attach it")
    ap.add_argument("--tables", choices=("text", "image"), default="text",
                    help="text: flatten tables to one line per row (default); "
                         "image: screenshot each table to PNG and attach it")
    ap.add_argument("--image-dir", type=Path, default=None,
                    help="where block PNGs go (default: imgs/twitter-blocks/ "
                         "beside a docs/ article)")
    args = ap.parse_args()

    if not args.source.exists():
        print(f"no such file: {args.source}", file=sys.stderr)
        return 1

    image_dir = args.image_dir
    if image_dir is None and (args.code == "image" or args.tables == "image"):
        if args.source.parent.name == "docs":
            image_dir = args.source.parent.parent / "imgs" / "twitter-blocks"
        else:
            image_dir = args.source.parent / "twitter-blocks"
    if image_dir is not None:
        image_dir.mkdir(parents=True, exist_ok=True)

    md_text = args.source.read_text(encoding="utf-8")
    posts, notes = convert(md_text, args.source.parent,
                           limit=args.limit, number=args.number,
                           code=args.code, tables=args.tables,
                           image_dir=image_dir, stem=args.source.stem)

    if not posts:
        for note in notes:
            print(f"note: {note}", file=sys.stderr)
        return 1

    if args.at is not None:
        if not 1 <= args.at <= len(posts):
            print(f"there is no post {args.at}: the thread has {len(posts)}",
                  file=sys.stderr)
            return 1
        chosen = [(args.at, posts[args.at - 1])]
    else:
        chosen = list(enumerate(posts, 1))

    # With --number the text already carries "n/N", so the marker would say it twice.
    thread = "\n\n---\n\n".join(
        (f"[{i}/{len(posts)}]\n" if len(posts) > 1 and not args.number else "") + p.text
        + (("\n" + "\n".join(f"  [image: {img.name}]" for img in p.images)) if p.images else "")
        for i, p in chosen
    )

    if args.print_text or (args.at is not None and not args.post):
        print(thread)
    elif args.at is None:
        out = args.out or args.source.with_name(f"{args.source.stem}-twitter.txt")
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(thread + "\n", encoding="utf-8")
        print(f"thread:  {out}")

    if args.at is None:
        total_images = sum(len(p.images) for p in posts)
        print(f"posts:   {len(posts)}  ({total_images} image(s))")
        for i, post in enumerate(posts, 1):
            flag = f"  images: {', '.join(img.name for img in post.images)}" if post.images else ""
            print(f"  {i}. {post.weight():3d} chars{flag}")
    else:
        i, post = chosen[0]
        flag = f"  images: {', '.join(img.name for img in post.images)}" if post.images else ""
        print(f"\npost {i}/{len(posts)}: {post.weight():3d} chars{flag}")

    if notes:
        print("\nnotes:")
        for note in notes:
            print(f"  - {note}")

    if not args.post:
        if args.at is not None:
            print("\nrun with --post to send just this one")
        else:
            print("\ncopy each post from the file above, or run with --post to send it")
        return 0

    if args.dry_run:
        print("\ndry run: nothing sent. Would post:")
        for i, post in chosen:
            print(f"  {i}. {post.text[:80]!r}... "
                  f"({len(post.images)} image(s))")
        return 0

    creds = load_credentials()
    if creds is None:
        print("\nno X credentials found. Set X_CONSUMER_KEY, X_CONSUMER_SECRET,\n"
              "X_ACCESS_TOKEN and X_ACCESS_TOKEN_SECRET, or write them to\n"
              "~/.config/md-to-twitter/keys.json as\n"
              '{"consumer_key": "...", "consumer_secret": "...",\n'
              ' "access_token": "...", "access_token_secret": "..."}',
              file=sys.stderr)
        return 1

    reply_to = args.reply_to
    posted: list[str] = []
    try:
        for i, post in chosen:
            media_ids = [upload_image(img, creds) for img in post.images]
            tweet_id = create_post(post.text, media_ids, creds, reply_to)
            posted.append(tweet_id)
            reply_to = tweet_id
            print(f"posted {i}/{len(posts)}: https://x.com/i/status/{tweet_id}")
            if args.at is not None and i < len(posts):
                # One at a time: hand back the command for the next post.
                print(f"next: --at {i + 1} --post --reply-to {tweet_id}")
    except (RuntimeError, OSError, ValueError, requests.RequestException) as exc:
        print(f"\nstopped at post {len(posted) + 1}/{len(posts)}: {exc}", file=sys.stderr)
        if posted:
            print(f"posted so far: {posted[-1]}", file=sys.stderr)
            print(f"resume with --reply-to {posted[-1]}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
