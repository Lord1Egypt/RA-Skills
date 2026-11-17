"""Offline, bounded preflight hints; not a JavaScript parser or security boundary."""

import ipaddress
import re
import socket
from html.parser import HTMLParser
from pathlib import PurePosixPath
from urllib.parse import unquote, urlsplit

LIMIT = 20
CSS_URL = re.compile(r"""url\(\s*(?:"([^"]*)"|'([^']*)'|([^\s)]+))\s*\)""", re.I)
CSS_IMPORT = re.compile(r"""@import\s+["']([^"']+)["']""", re.I)


def css_links(text):
    text = re.sub(r"/\*.*?\*/", "", text, flags=re.S)
    imports = CSS_IMPORT.findall(text)
    if any(url.strip().startswith(("data:", "blob:")) for url in imports) or re.search(
        r"@import\s+url\(\s*[\"']?(?:data|blob):", text, re.I
    ):
        raise RuntimeError("Hosted stylesheet imports cannot use data/blob URLs")
    return [next((v for v in match if v), "") for match in CSS_URL.findall(text)] + imports


def srcset_links(value):
    # URLs may contain commas (notably data URLs); descriptors end at the next comma.
    links = []
    while value.strip(" ,\t\n\r\f\v"):
        value = value.lstrip(" ,\t\n\r\f\v")
        match = re.match(r"\S+", value)
        if not match:
            break
        url = match[0]
        value = value[len(url) :]
        if url.endswith(","):
            links.append(url.rstrip(","))
        else:
            links.append(url)
            _, _, value = value.partition(",")
    return links


class Document(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.scripts = []
        self.styles = []
        self.flags = set()
        self.section = None
        self.inline = []

    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        if tag == "base":
            raise RuntimeError("Remove <base> before publishing; use relative paths under /p/")
        if tag in {"object", "embed"}:
            raise RuntimeError("Hosted pages block object/embed; replace with HTML, image or video")
        for key in ("src", "poster"):
            if values.get(key):
                self.links.append((values[key], tag))
        if tag == "link" and values.get("href"):
            self.links.append((values["href"], tag))
        for key in ("srcset", "imagesrcset"):
            self.links.extend((url, "image") for url in srcset_links(values.get(key) or ""))
        self.styles.append(values.get("style") or "")
        self.scripts.extend(value for key, value in attrs if key.startswith("on") and value)
        if tag in {"iframe", "form"} or values.get("srcdoc"):
            self.flags.add("embedded_or_form")
        if tag == "meta" and (values.get("http-equiv") or "").lower() == "refresh":
            self.flags.add("navigation")
        if tag == "a" and values.get("href"):
            href = values["href"].strip()
            if href.startswith(("/", "javascript:")):
                self.flags.add("navigation")
        if tag in {"style", "script"}:
            self.section, self.inline = tag, []

    def handle_data(self, data):
        if self.section:
            self.inline.append(data)

    def handle_endtag(self, tag):
        if tag == self.section:
            (self.styles if tag == "style" else self.scripts).append("".join(self.inline))
            self.section = None


def reference(source, link, names, kind="asset"):
    link = link.strip()
    try:
        parsed = urlsplit(link)
        hostname = parsed.hostname or ""
    except ValueError:
        raise RuntimeError(f"{source}: malformed resource URL") from None
    try:
        address = ipaddress.ip_address(hostname)
        private = not address.is_global
    except ValueError:
        try:
            private = not ipaddress.ip_address(socket.inet_aton(hostname)).is_global
        except OSError:
            private = hostname.lower() in {"localhost", "0.0.0.0"} or hostname.lower().endswith(
                (".localhost", ".local")
            )
    if private or parsed.scheme == "file":
        raise RuntimeError(
            f"{source}: replace local-only resource with a bundled or public HTTPS asset"
        )
    if parsed.scheme == "http":
        raise RuntimeError(
            f"{source}: HTTP resource is incompatible with HTTPS hosting; use HTTPS or bundle it"
        )
    if kind == "iframe" and link == "about:blank":
        return False
    if parsed.scheme in {"data", "blob"}:
        if kind in {"script", "link"}:
            raise RuntimeError(f"{source}: hosted script/style policy blocks data/blob URLs")
        return False
    if parsed.scheme and parsed.scheme != "https":
        raise RuntimeError(f"{source}: unsupported resource URL scheme")
    if parsed.scheme == "https" or parsed.netloc:
        return True
    if not parsed.path:
        return False
    path = unquote(parsed.path)
    if "\\" in path or any(ord(c) < 32 for c in path):
        raise RuntimeError(f"{source}: ambiguous resource path; use forward slashes")
    if path.startswith("/"):
        raise RuntimeError(
            f"{source}: use relative asset paths for /p/ hosting; build with a relative base (./)"
        )
    parts = list(PurePosixPath(source).parent.parts)
    for part in path.split("/"):
        if part in {"", "."}:
            continue
        if part == "..":
            if not parts:
                raise RuntimeError(f"{source}: resource escapes the published directory")
            parts.pop()
        else:
            parts.append(part)
    target = "/".join(parts)
    if target not in names:
        raise RuntimeError(
            f"{source}: missing resource {target[:160]}; publish its static directory"
        )
    return False


RULES = {
    "runtime_paths": (
        r"""(?:fetch\s*\(|import\s*\(|from\s+|import\s+|new\s+(?:URL|Worker)\s*\()\s*["'`]""",
        "Review literal and computed URLs: imports resolve from the module; fetch resolves from the document. Root paths escape /p/<id>/; bare imports need an import map or build.",
    ),
    "network": (
        r"\b(?:fetch|XMLHttpRequest|WebSocket|EventSource|sendBeacon)\b",
        "Verify HTTPS API availability, CORS and preflight, credentials and a visible failure fallback. CSP blocks WebSockets; no-cors does not make response bodies readable.",
    ),
    "blocked_capability": (
        r"\b(?:Worker|SharedWorker|serviceWorker|geolocation)\b",
        "Workers, service workers and geolocation are blocked by hosting policy; remove the dependency or provide a working fallback.",
    ),
    "media_permission": (
        r"\b(?:getUserMedia|SpeechRecognition|webkitSpeechRecognition)\b",
        "Camera and microphone require visitor permission in a secure context. Start from a user action; handle denial, unavailable devices and unsupported browsers visibly. Review where audio/video is processed or sent.",
    ),
    "shared_origin": (
        r"\b(?:localStorage|sessionStorage|cookie|indexedDB|postMessage|opener)\b|\b(?:top|parent)\s*\.",
        "Review shared-origin storage and window access. Never read platform credentials or other works; namespace storage. Check postMessage origin AND source, avoid wildcard secret delivery.",
    ),
    "html_injection": (
        r"\b(?:innerHTML|outerHTML|insertAdjacentHTML|document\.write|eval)\b",
        "Trace URL, form and remote inputs into HTML/script sinks; use textContent or appropriate sanitization. Static hints do not prove absence of XSS.",
    ),
    "browser_gesture": (
        r"\b(?:clipboard|requestFullscreen|AudioContext|\.play\s*\()",
        "Test user-gesture requirements and rejection handling for clipboard, fullscreen and media playback, including mobile browsers.",
    ),
}
FLAG_MESSAGES = {
    "embedded_or_form": "Review iframe/srcdoc and form destinations, sensitive-data transmission and embedded page framing restrictions.",
    "navigation": "Review redirects and links: root navigation leaves the work, and history routes need hash routing or real HTML files; no SPA fallback is provided.",
}


def review(files):
    findings = []
    count = 0
    external = False

    def add(source, code, message):
        nonlocal count
        count += 1
        if len(findings) < LIMIT:
            findings.append({"file": source, "code": code, "message": message})

    for name, value in files.items():
        suffix = PurePosixPath(name).suffix.lower()
        if suffix not in {".html", ".htm", ".css", ".js", ".mjs", ".svg"}:
            continue
        try:
            content = value.decode("utf-8")
        except UnicodeDecodeError:
            raise RuntimeError(f"Use UTF-8 for {name[:160]}") from None
        links, scripts = [], []
        if suffix in {".html", ".htm"}:
            parser = Document()
            parser.feed(content)
            parser.close()
            links.extend(parser.links)
            for style in parser.styles:
                links.extend((url, "style") for url in css_links(style))
            scripts.extend(parser.scripts)
            for flag in sorted(parser.flags):
                add(name, flag, FLAG_MESSAGES[flag])
        elif suffix == ".css":
            links.extend((url, "style") for url in css_links(content))
        else:
            scripts.append(content)
        for url, kind in links:
            external |= reference(name, url, files, kind)
        code = "\n".join(scripts)
        for key, (pattern, message) in RULES.items():
            if re.search(pattern, code):
                add(name, key, message)
        if re.search(r"""["'`](?:https?:)?//""", code):
            external = True
            add(
                name,
                "external_code",
                "Review external URLs and dependencies in code; HTTP/local addresses and third-party scripts need particular care. Nothing was fetched or executed by this check.",
            )
    if external:
        add(
            "index.html",
            "external_resources",
            "External dependencies remain external: verify TLS, MIME types, script integrity/source, CDN availability and cross-origin module/font/API permissions.",
        )
    return {
        "external_resources": external,
        "review": {
            "findings": findings,
            "has_more": count > LIMIT,
            "total": count,
            "browser_verified": False,
        },
    }
