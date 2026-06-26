#!/usr/bin/env python3
import ipaddress
import json
import re
import socket
import sys
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

ALLOWED_SCHEMES = {"http", "https"}
MAX_RESPONSE_BYTES = 5 * 1024 * 1024
READ_CHUNK_SIZE = 8192
SUSPICIOUS_PATTERNS = [
    re.compile(rb"<!DOCTYPE", re.IGNORECASE),
    re.compile(rb"<!ENTITY", re.IGNORECASE),
]
CONTENT_TYPE_HINTS = ("xml", "rss", "atom")
USER_AGENT = "openclaw-skill-podcast-manager/1.0"


class FeedProbeError(Exception):
    pass


def fail(url, message, exit_code=1):
    print(json.dumps({"feedUrl": url, "error": message}, ensure_ascii=False))
    sys.exit(exit_code)


def text(node, tag):
    el = node.find(tag)
    return (el.text or "").strip() if el is not None and el.text else ""


def sanitize_url(url):
    parsed = urllib.parse.urlparse(url)
    scheme = (parsed.scheme or "").lower()
    if scheme not in ALLOWED_SCHEMES:
        raise FeedProbeError(f"scheme_not_allowed: {parsed.scheme or 'none'}")
    host = parsed.hostname
    if not host:
        raise FeedProbeError("missing_host")
    if host.lower() == "localhost":
        raise FeedProbeError("host_not_allowed: localhost")
    service = parsed.port or (443 if scheme == "https" else 80)
    ensure_safe_ip(host, service)
    return url


def ensure_safe_ip(host, service):
    try:
        infos = socket.getaddrinfo(host, service, family=socket.AF_UNSPEC, type=socket.SOCK_STREAM)
    except OSError as exc:
        raise FeedProbeError(f"dns_resolution_error: {exc}")
    seen = set()
    for info in infos:
        sockaddr = info[4]
        ip_str = sockaddr[0]
        if ip_str in seen:
            continue
        seen.add(ip_str)
        try:
            ip = ipaddress.ip_address(ip_str)
        except ValueError:
            raise FeedProbeError(f"invalid_ip_address: {ip_str}")
        if (
            ip.is_loopback
            or ip.is_link_local
            or ip.is_private
            or ip.is_reserved
            or ip.is_unspecified
            or (hasattr(ip, "is_multicast") and ip.is_multicast)
        ):
            raise FeedProbeError(f"blocked_ip_range: {ip_str}")


def validate_http_response(resp):
    status = getattr(resp, "status", None)
    if status is None or not (200 <= status < 300):
        raise FeedProbeError(f"http_status_error: {status}")
    content_type = resp.getheader("Content-Type", "")
    normalized = content_type.lower()
    if not any(hint in normalized for hint in CONTENT_TYPE_HINTS):
        raise FeedProbeError(f"unexpected_content_type: {content_type or 'none'}")


def read_response_with_limit(resp):
    buffer = bytearray()
    total = 0
    while True:
        chunk = resp.read(READ_CHUNK_SIZE)
        if not chunk:
            break
        if total + len(chunk) > MAX_RESPONSE_BYTES:
            raise FeedProbeError("max_response_size_exceeded")
        buffer.extend(chunk)
        total += len(chunk)
    return bytes(buffer)


def check_suspicious_xml(data):
    for pattern in SUSPICIOUS_PATTERNS:
        if pattern.search(data):
            raise FeedProbeError("suspicious_xml_pattern_detected")


def fetch_feed(url):
    sanitized = sanitize_url(url)
    req = urllib.request.Request(sanitized, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            validate_http_response(resp)
            return read_response_with_limit(resp)
    except urllib.error.HTTPError as exc:
        raise FeedProbeError(f"http_status_error: {exc.code}")
    except urllib.error.URLError as exc:
        raise FeedProbeError(f"network_error: {exc.reason}")
    except socket.timeout as exc:
        raise FeedProbeError(f"network_timeout: {exc}")


def main():
    if len(sys.argv) != 2:
        print("usage: feed_probe.py <feed-url>", file=sys.stderr)
        sys.exit(2)

    url = sys.argv[1]
    try:
        data = fetch_feed(url)
        check_suspicious_xml(data)
    except FeedProbeError as exc:
        fail(url, str(exc))
    except ET.ParseError as exc:
        fail(url, f"xml_parse_error: {exc}")

    try:
        root = ET.fromstring(data)
    except ET.ParseError as exc:
        fail(url, f"xml_parse_error: {exc}")

    out = {"feedUrl": url, "title": "", "link": "", "episodes": []}

    channel = root.find("channel")
    if channel is not None:
        out["title"] = text(channel, "title")
        out["link"] = text(channel, "link")
        for item in channel.findall("item")[:5]:
            out["episodes"].append(
                {
                    "title": text(item, "title"),
                    "guid": text(item, "guid") or text(item, "link"),
                    "pubDate": text(item, "pubDate"),
                    "link": text(item, "link"),
                }
            )
    else:
        ns = {"a": "http://www.w3.org/2005/Atom"}
        out["title"] = (root.findtext("a:title", default="", namespaces=ns) or "").strip()
        link_el = root.find("a:link", ns)
        out["link"] = link_el.attrib.get("href", "") if link_el is not None else ""
        for entry in root.findall("a:entry", ns)[:5]:
            link_el = entry.find("a:link", ns)
            out["episodes"].append(
                {
                    "title": (entry.findtext("a:title", default="", namespaces=ns) or "").strip(),
                    "guid": (entry.findtext("a:id", default="", namespaces=ns) or "").strip(),
                    "pubDate": (entry.findtext("a:updated", default="", namespaces=ns) or "").strip(),
                    "link": link_el.attrib.get("href", "") if link_el is not None else "",
                }
            )

    print(json.dumps(out, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
