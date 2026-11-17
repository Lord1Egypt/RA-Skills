#!/usr/bin/env python3
"""LYGO Site Card — public page identity card. HTTPS GET or local HTML. No subprocess."""
from __future__ import annotations

import argparse
import hashlib
import ipaddress
import json
import re
import socket
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path
from typing import Any, Optional
from urllib.parse import urljoin, urlparse

VERSION = "1.0.0"
SIG = "Delta9Phi963-SITE-CARD-v1.0.0"
UA = "LYGO-Site-Card/1.0 (+https://clawhub.ai/deepseekoracle/lygo-site-card)"
MAX_BODY = 400_000
HEADER_KEYS = (
    "content-security-policy",
    "content-security-policy-report-only",
    "strict-transport-security",
    "x-frame-options",
    "x-content-type-options",
    "referrer-policy",
    "permissions-policy",
    "cross-origin-opener-policy",
    "content-type",
    "cache-control",
)


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def https_only(url: str) -> bool:
    p = urlparse(url)
    return p.scheme == "https" and bool(p.hostname) and not p.username and not p.password


def _public_host(host: str) -> bool:
    try:
        infos = socket.getaddrinfo(host, 443, type=socket.SOCK_STREAM)
    except OSError:
        return False
    for info in infos:
        try:
            ip = ipaddress.ip_address(info[4][0])
        except ValueError:
            return False
        if ip.is_private or ip.is_loopback or ip.is_link_local or ip.is_reserved or ip.is_multicast:
            return False
    return True


def allowed_url(url: str) -> bool:
    if not https_only(url):
        return False
    host = (urlparse(url).hostname or "").lower()
    if host in {"localhost"}:
        return False
    return _public_host(host)


class _AllowRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        if not allowed_url(newurl):
            raise urllib.error.HTTPError(newurl, code, "redirect blocked", headers, fp)
        return urllib.request.HTTPRedirectHandler.redirect_request(
            self, req, fp, code, msg, headers, newurl
        )


def get(url: str, timeout: int = 16) -> dict[str, Any]:
    if not allowed_url(url):
        return {"ok": False, "url": url, "error": "blocked_host", "status": None, "headers": {}, "body": b""}
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "*/*"})
    opener = urllib.request.build_opener(_AllowRedirect)
    try:
        with opener.open(req, timeout=timeout) as r:
            raw = r.read(MAX_BODY)
            headers = {k.lower(): v for k, v in r.headers.items()}
            return {
                "ok": True,
                "url": r.geturl() or url,
                "status": getattr(r, "status", 200),
                "headers": headers,
                "body": raw,
            }
    except Exception as e:
        return {"ok": False, "url": url, "error": str(e)[:220], "status": None, "headers": {}, "body": b""}


class _Page(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.title_parts: list[str] = []
        self._in_title = False
        self.metas: list[dict[str, str]] = []
        self.canonical: Optional[str] = None
        self.json_ld: list[str] = []
        self._in_ld = False
        self._ld_buf: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, Optional[str]]]) -> None:
        a = {k.lower(): (v or "") for k, v in attrs}
        if tag == "title":
            self._in_title = True
        if tag == "meta":
            self.metas.append(a)
        if tag == "link" and a.get("rel", "").lower() == "canonical" and a.get("href"):
            self.canonical = a["href"]
        if tag == "script" and "ld+json" in a.get("type", "").lower():
            self._in_ld = True
            self._ld_buf = []

    def handle_endtag(self, tag: str) -> None:
        if tag == "title":
            self._in_title = False
        if tag == "script" and self._in_ld:
            self._in_ld = False
            blob = "".join(self._ld_buf).strip()
            if blob:
                self.json_ld.append(blob[:4000])

    def handle_data(self, data: str) -> None:
        if self._in_title:
            self.title_parts.append(data)
        if self._in_ld:
            self._ld_buf.append(data)


def parse_html(body: bytes, base: str) -> dict[str, Any]:
    text = body.decode("utf-8", errors="replace")
    p = _Page()
    try:
        p.feed(text)
        p.close()
    except Exception:
        pass
    title = re.sub(r"\s+", " ", "".join(p.title_parts)).strip()[:240]
    desc = ""
    html_csp = None
    html_referrer = None
    for m in p.metas:
        name = (m.get("name") or m.get("property") or "").lower()
        equiv = (m.get("http-equiv") or "").lower()
        if name in {"description", "og:description"} and m.get("content"):
            desc = m["content"].strip()[:400]
            if name == "description":
                pass
        if equiv == "content-security-policy" and m.get("content"):
            html_csp = m["content"].strip()[:500]
        if name == "referrer" and m.get("content"):
            html_referrer = m["content"].strip()[:120]
    types: list[str] = []
    for blob in p.json_ld:
        try:
            obj = json.loads(blob)
        except json.JSONDecodeError:
            continue
        rows = obj if isinstance(obj, list) else [obj]
        for row in rows:
            if isinstance(row, dict) and row.get("@type"):
                t = row["@type"]
                types.append(t if isinstance(t, str) else json.dumps(t))
    canon = p.canonical
    if canon:
        canon = urljoin(base, canon)
    return {
        "title": title or None,
        "description": desc or None,
        "canonical": canon,
        "json_ld_types": types[:8],
        "html_csp": html_csp,
        "html_referrer": html_referrer,
    }


def security_headers(headers: dict[str, str]) -> dict[str, Optional[str]]:
    return {k: headers.get(k) for k in HEADER_KEYS}


def yield_card(card: dict[str, Any]) -> str:
    if not card.get("ok"):
        return "SHADOW"
    hdr = card.get("security_headers") or {}
    has_csp = bool(hdr.get("content-security-policy") or hdr.get("content-security-policy-report-only"))
    has_ref = bool(hdr.get("referrer-policy"))
    has_title = bool(card.get("title"))
    if card.get("status") != 200 or not has_title:
        return "DRIFT"
    if not has_csp and not has_ref:
        return "DRIFT"
    return "ALIGNED"


def origin_of(url: str) -> str:
    p = urlparse(url)
    return f"{p.scheme}://{p.netloc}"


def card_from_body(url: str, status: Optional[int], headers: dict[str, str], body: bytes, ok: bool, error: Optional[str] = None) -> dict[str, Any]:
    parsed = parse_html(body, url) if body else {
        "title": None, "description": None, "canonical": None, "json_ld_types": [],
        "html_csp": None, "html_referrer": None,
    }
    digest = hashlib.sha256(body).hexdigest() if body else None
    hdr = security_headers(headers)
    # GitHub Pages cannot set CSP/HSTS HTTP headers; meta http-equiv still counts.
    if not hdr.get("content-security-policy") and parsed.get("html_csp"):
        hdr["content-security-policy"] = "meta " + str(parsed.get("html_csp"))[:240]
    if not hdr.get("referrer-policy") and parsed.get("html_referrer"):
        hdr["referrer-policy"] = "meta " + str(parsed.get("html_referrer"))
    out = {
        "signature": SIG,
        "version": VERSION,
        "utc": utc_now(),
        "ok": ok,
        "url": url,
        "status": status,
        "error": error,
        "bytes": len(body),
        "sha256": digest,
        "title": parsed.get("title"),
        "description": parsed.get("description"),
        "canonical": parsed.get("canonical"),
        "json_ld_types": parsed.get("json_ld_types") or [],
        "security_headers": hdr,
        "html_equiv": {"csp": parsed.get("html_csp"), "referrer": parsed.get("html_referrer")},
        "companions": {},
        "live_star_chart_write": False,
    }
    out["yield"] = yield_card(out)
    return out


def companions(page_url: str) -> dict[str, Any]:
    origin = origin_of(page_url)
    rows = {}
    for path, key in (
        ("/.well-known/security.txt", "security_txt_well_known"),
        ("/security.txt", "security_txt"),
        ("/robots.txt", "robots_txt"),
    ):
        got = get(origin + path)
        rows[key] = {
            "ok": bool(got.get("ok") and got.get("status") == 200),
            "status": got.get("status"),
            "url": origin + path,
            "bytes": len(got.get("body") or b""),
        }
    return rows


def cmd_card(url: Optional[str], file: Optional[str], with_companions: bool) -> dict[str, Any]:
    if file:
        path = Path(file)
        if not path.is_file():
            return {"ok": False, "error": "file_missing", "path": str(path), "signature": SIG}
        body = path.read_bytes()[:MAX_BODY]
        card = card_from_body("file://" + path.name, 200, {}, body, True)
        card["source"] = "local_file"
        card["path"] = str(path)
        return card
    if not url:
        return {"ok": False, "error": "need_url_or_file", "signature": SIG}
    got = get(url)
    card = card_from_body(
        got.get("url") or url,
        got.get("status"),
        got.get("headers") or {},
        got.get("body") or b"",
        bool(got.get("ok")),
        got.get("error"),
    )
    card["source"] = "https_get"
    if with_companions and card.get("ok"):
        card["companions"] = companions(card["url"])
    return card


def cmd_headers(url: str) -> dict[str, Any]:
    got = get(url)
    hdr = security_headers(got.get("headers") or {})
    present = [k for k, v in hdr.items() if v]
    missing = [k for k, v in hdr.items() if not v]
    return {
        "signature": SIG,
        "ok": bool(got.get("ok")),
        "url": got.get("url") or url,
        "status": got.get("status"),
        "error": got.get("error"),
        "security_headers": hdr,
        "present": present,
        "missing": missing,
        "yield": "ALIGNED" if got.get("ok") and ("content-security-policy" in present or "referrer-policy" in present) else ("SHADOW" if not got.get("ok") else "DRIFT"),
    }


def cmd_compare(a: str, b: str) -> dict[str, Any]:
    ca = cmd_card(a, None, False)
    cb = cmd_card(b, None, False)
    keys = ("title", "canonical", "status", "yield", "sha256")
    drift = []
    for k in keys:
        if ca.get(k) != cb.get(k):
            drift.append({"field": k, "a": ca.get(k), "b": cb.get(k)})
    ha = ca.get("security_headers") or {}
    hb = cb.get("security_headers") or {}
    for k in HEADER_KEYS:
        if bool(ha.get(k)) != bool(hb.get(k)):
            drift.append({"field": "header:" + k, "a": ha.get(k), "b": hb.get(k)})
    return {
        "signature": SIG,
        "ok": True,
        "a": {"url": ca.get("url"), "yield": ca.get("yield"), "title": ca.get("title")},
        "b": {"url": cb.get("url"), "yield": cb.get("yield"), "title": cb.get("title")},
        "drift": drift,
        "same_body": ca.get("sha256") == cb.get("sha256") and bool(ca.get("sha256")),
    }


def maybe_write(doc: dict[str, Any], out: Optional[str], consent: bool) -> dict[str, Any]:
    if not out:
        return doc
    if not consent:
        doc = dict(doc)
        doc["write"] = "refused_need_i_consent"
        return doc
    path = Path(out)
    path.write_text(json.dumps(doc, indent=2) + "\n", encoding="utf-8")
    doc = dict(doc)
    doc["wrote"] = str(path)
    return doc


def main(argv: Optional[list[str]] = None) -> int:
    ap = argparse.ArgumentParser(description="LYGO Site Card — public page identity card")
    sub = ap.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("card", help="Build a card from URL or local HTML")
    c.add_argument("url", nargs="?")
    c.add_argument("--file", help="Local HTML file (no network)")
    c.add_argument("--no-companions", action="store_true")
    c.add_argument("--write")
    c.add_argument("--i-consent", action="store_true")
    h = sub.add_parser("headers", help="Security header presence")
    h.add_argument("url")
    h.add_argument("--write")
    h.add_argument("--i-consent", action="store_true")
    d = sub.add_parser("compare", help="Diff two public pages")
    d.add_argument("url_a")
    d.add_argument("url_b")
    d.add_argument("--write")
    d.add_argument("--i-consent", action="store_true")
    args = ap.parse_args(argv)

    if args.cmd == "card":
        doc = cmd_card(args.url, args.file, with_companions=not args.no_companions)
        doc = maybe_write(doc, args.write, args.i_consent)
    elif args.cmd == "headers":
        doc = maybe_write(cmd_headers(args.url), args.write, args.i_consent)
    else:
        doc = maybe_write(cmd_compare(args.url_a, args.url_b), args.write, args.i_consent)
    print(json.dumps(doc, indent=2))
    return 0 if doc.get("ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
