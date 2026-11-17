#!/usr/bin/env python3
"""Wayback (Internet Archive) fallback for ocas-sift sift.fetch.

RECOVERY-ONLY. Call this ONLY after live fetch + Jina Reader have both failed on
a confirmed hard-block (page-gone 404/410/451, or a bot/auth wall where live is
genuinely impossible). It must NOT fire on soft 429/5xx where a retry helps.

Design discipline — written around the exact reasons prior art was removed
(dondai1234/Hound deleted its archive fallback in v10.4.1 for "latency on every
hard-blocked fetch" + unreliability):

  1. HARD 8s TOTAL TIMEOUT. The fallback can never hang the fetch chain. Two
     network calls (availability check + snapshot fetch) share one wall-clock
     budget; if it blows, we bail cleanly.
  2. FIRES ONLY ON CONFIRMED HARD-BLOCK. It is the final tier, never a default
     primary path, so it adds zero latency to successful live fetches.
  3. ALWAYS MARKS STALENESS. Returns source='archive.org' + archived_at always,
     and is_stale=True / content_age_days. Downstream synthesis + ocas-sift
     fact-verify CANNOT mistake a years-old snapshot for live, current content.
  4. PURE STDLIB + optional html2text. No new hard dependency. html2text is
     already expected by sift's Scrapling pipeline; if absent we degrade to a
     minimal tag-stripper (rough but readable).

Usage:
    python3 wayback_fallback.py <url> [--json]
Exit 0 = recovered (content_ok True). Exit 1 = nothing recovered.
Prints Markdown (or --json envelope) to stdout.

In agent use, call recover(url) and merge the returned envelope into the
sift.fetch response, surfacing source/archived_at/content_age_days so the user
and downstream skills see it is archived, not live.
"""
from __future__ import annotations

import argparse
import gzip
import json
import re
import sys
import time
import zlib

import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone

AVAILABILITY_API = "https://archive.org/wayback/available"
WAYBACK_SNAPSHOT = "https://web.archive.org/web/{ts}id_/{url}"
TOTAL_TIMEOUT_S = 8.0
UA = "ocas-sift/wayback-fallback (+https://github.com/indigokarasu/sift)"

_BLOCK_PATTERNS = (
    "excluded from the wayback machine",
    "this url has been excluded",
    "access denied",
    "robotstxt",
)


def _decode_body(raw: bytes, encoding: str) -> bytes:
    enc = (encoding or "").lower()
    try:
        if "gzip" in enc:
            return gzip.decompress(raw)
        if "deflate" in enc:
            try:
                return zlib.decompress(raw, -zlib.MAX_WBITS)
            except zlib.error:
                return zlib.decompress(raw)
        if "br" in enc:
            try:
                import brotli  # type: ignore[import-untyped]  # optional; wayback sometimes brotlis

                return brotli.decompress(raw)
            except Exception:
                return raw  # no brotli: leave bytes; caller degrades
    except Exception:
        return raw
    return raw


def _request(url: str, timeout: float) -> tuple[int, str]:
    # Ask for uncompressed (identity) so we never get a gzip/brotli body that
    # urllib won't decode; decode defensively anyway if a server ignores it.
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept-Encoding": "identity"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            charset = r.headers.get_content_charset() or "utf-8"
            raw = _decode_body(r.read(), r.headers.get("Content-Encoding", ""))
            return r.status, raw.decode(charset, "replace")
    except urllib.error.HTTPError as e:
        body = _decode_body(e.read(), e.headers.get("Content-Encoding", "")) if e.headers else e.read()
        return e.code, body.decode("utf-8", "replace")
    except (urllib.error.URLError, TimeoutError, OSError) as e:
        return 0, f"network_error: {e}"


# Cache optional html2text module import at top-level to avoid expensive sys.path module lookup
# failures on every _html_to_markdown invocation when html2text is absent.
try:
    import html2text  # type: ignore[import-untyped]  # optional dep, already expected by sift's scrapling pipeline
except ImportError:
    html2text = None  # type: ignore[assignment]


def _html_to_markdown(html: str) -> str:
    if html2text is not None:
        try:
            h = html2text.HTML2Text()
            h.body_width = 0
            h.ignore_images = False
            h.ignore_links = False
            return h.handle(html)
        except Exception:
            pass
    # Minimal stdlib fallback: strip script/style/head, turn block tags into
    # newlines, then strip remaining tags. Rough but readable.
    html = re.sub(r"(?is)<(script|style|head|noscript)\b.*?</\1>", " ", html)
    html = re.sub(r"(?i)</(p|div|h[1-6]|li|tr|br|section|article)>", "\n", html)
    html = re.sub(r"(?i)<br\s*/?>", "\n", html)
    html = re.sub(r"(?s)<[^>]+>", "", html)
    html = re.sub(r"[ \t]+", " ", html)
    html = re.sub(r"\n{3,}", "\n\n", html)
    return html.strip()


def recover(url: str, timeout_s: float = TOTAL_TIMEOUT_S) -> dict:
    """Attempt Internet Archive recovery for `url`. Returns an envelope dict.

    Envelope fields mirror the sift.fetch ResponseModel so they merge cleanly:
    source, archived_at, url, content, content_ok, status, content_age_days,
    is_stale, next_action, summary.
    """
    deadline = time.monotonic() + timeout_s
    envelope = {
        "source": "archive.org",
        "archived_at": "",
        "url": "",
        "content": "",
        "content_ok": False,
        "status": 0,
        "content_age_days": None,
        "is_stale": True,
        "next_action": "archive_unavailable",
        "summary": "Internet Archive had no usable snapshot.",
    }

    # Step 1: availability check (fast existence probe).
    remain = deadline - time.monotonic()
    if remain <= 0.5:
        return envelope
    api_url = f"{AVAILABILITY_API}?url={urllib.parse.quote(url, safe='')}"
    status, body = _request(api_url, timeout=min(remain, timeout_s))
    try:
        data = json.loads(body) if body and body.startswith("{") else {}
    except json.JSONDecodeError:
        data = {}
    # An unreachable or erroring archive is NOT the same as an unarchived page.
    # Reporting both as "no usable snapshot" told the caller to give up on the
    # URL when the right move was to retry later, and hid archive.org outages
    # entirely. Distinguish them by the status the request already returned.
    if status != 200 or not data:
        envelope["next_action"] = "archive_error"
        envelope["summary"] = (
            "Internet Archive availability check failed "
            f"(HTTP {status if status else 'no response'}); snapshot presence is "
            "UNKNOWN, not ruled out — retry later rather than treating this URL "
            "as unarchived."
        )
        return envelope
    closest = (data.get("archived_snapshots") or {}).get("closest") or {}
    if not closest.get("available") or not closest.get("timestamp"):
        envelope["summary"] = "Internet Archive has no snapshot of this URL."
        return envelope
    ts = closest["timestamp"]
    snapshot_url = WAYBACK_SNAPSHOT.format(ts=ts, url=urllib.parse.quote(url, safe=":/%?=&#"))

    # Step 2: fetch the un-rewritten (id_) snapshot.
    remain = deadline - time.monotonic()
    if remain <= 0.5:
        return envelope
    status, html = _request(snapshot_url, timeout=min(remain, timeout_s))
    # Performance optimization: evaluate status != 200 and len(html) < 200 first
    # to avoid allocating multi-megabyte html.lower() copies on failed or tiny responses.
    if status != 200 or len(html) < 200:
        envelope["status"] = status
        envelope["summary"] = "Snapshot fetched but blocked, excluded, or empty."
        return envelope

    low = html.lower()
    if any(p in low for p in _BLOCK_PATTERNS):
        envelope["status"] = status
        envelope["summary"] = "Snapshot fetched but blocked, excluded, or empty."
        return envelope

    content = _html_to_markdown(html)
    if len(content.strip()) < 80:
        envelope["status"] = status
        envelope["summary"] = "Snapshot recovered but extraction yielded no text."
        return envelope

    # Step 3: honesty fields — always mark staleness.
    archived_at = ""
    age_days = None
    try:
        snap_date = datetime.strptime(ts[:8], "%Y%m%d").replace(tzinfo=timezone.utc)
        age_days = (datetime.now(timezone.utc) - snap_date).days
        archived_at = snap_date.strftime("%Y-%m-%d")
    except ValueError:
        pass
    envelope.update(
        url=snapshot_url,
        content=content,
        content_ok=True,
        status=status,
        archived_at=archived_at,
        content_age_days=age_days,
        is_stale=True,
        next_action="archive_recovered",
        summary=(
            f"Recovered from Internet Archive snapshot dated "
            f"{archived_at} ({age_days} days old). Archived, not live."
        ),
    )
    return envelope


def main() -> int:
    ap = argparse.ArgumentParser(description="Internet Archive (Wayback) recovery for sift.fetch")
    ap.add_argument("url")
    ap.add_argument("--format", choices=["concise", "detailed"], default="concise",
                    help="Output verbosity: concise=key fields (default), detailed=full envelope")
    args = ap.parse_args()

    env = recover(args.url)
    if args.format == "concise" and env.get("content_ok"):
        # High-signal fields only — ~70% token savings for downstream synthesis
        print(json.dumps({
            "source": "archive.org",
            "archived_at": env.get("archived_at"),
            "content_age_days": env.get("content_age_days"),
            "is_stale": env.get("is_stale"),
            "summary": env.get("summary"),
        }, indent=2, ensure_ascii=False))
    elif args.format == "detailed":
        print(json.dumps(env, indent=2, ensure_ascii=False))
    else:
        # concise + failure → actionable envelope
        print(json.dumps({
            "content_ok": False,
            "status": env.get("status"),
            "next_action": env.get("next_action"),
            "summary": env.get("summary"),
            "actionable_guidance": (
                "Retry the live fetch later (soft 429/5xx), or check archive.org health if 'archive_error'; "
                "escalate to donsetch fetch for bot walls (exit 3)."
            ) if not env.get("content_ok") else None,
        }, indent=2, ensure_ascii=False))
    return 0 if env["content_ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
