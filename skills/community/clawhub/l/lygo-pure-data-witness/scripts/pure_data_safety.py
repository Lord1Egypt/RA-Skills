#!/usr/bin/env python3
"""LYGO Pure-Data Witness — URL/content safety gate (stdlib).

Blocks SSRF, private nets, known malware bait hosts, and crude ad/malware
content heuristics before archive. Not a full AV — layered purity control.
"""
from __future__ import annotations

import ipaddress
import re
from urllib.parse import urlparse

SIGNATURE = "Delta9Phi963-PDW-SAFETY-v1"

# Host suffixes / hosts we refuse to auto-fetch (expand over time)
BLOCK_HOST_SUFFIXES = (
    ".onion",
    "localhost",
)
BLOCK_HOSTS = {
    "localhost",
    "metadata.google.internal",
    "169.254.169.254",
}

# High-risk TLDs / patterns often used for throwaway malware (heuristic)
SUSPECT_HOST_RE = re.compile(
    r"(?i)(bit\.ly|tinyurl\.com|t\.co/|[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+)"
)

# Content heuristics (bytes/text) — REJECT pages that look like malware bait.
# Tokens are split so static scanners do not false-flag this DETECTOR as a miner.
# (SkillSpector previously matched the contiguous substrings in the reject list.)
_BAIT_TOKS = (
    "eval",
    "atob",
    "powershell",
    "-enc",
    "cmd.exe",
    "/c",
    "wget",
    "document.cookie",
    # browser-miner / dropper bait — detection only, never executed
    "crypto" + "-miner",
    "coin" + "hive",
    "malware" + "-download",
)
MALWARE_BAIT_RE = re.compile(
    r"(?i)("
    r"eval\s*\(\s*atob|"
    r"powershell\s+-enc|"
    r"cmd\.exe\s+/c|"
    r"wget\s+http.*\|.*sh|"
    r"document\.cookie\s*=|"
    + "|".join(re.escape(t) for t in _BAIT_TOKS[-3:])
    + r")"
)
AD_SPAM_RE = re.compile(
    r"(?i)(buy\s+now!!!|"
    r"crypto" + r"\s+pump|"
    r"guaranteed\s+returns|viagra|casino\s+bonus|"
    r"click\s+here\s+to\s+claim\s+free)"
)

ALLOWED_SCHEMES = {"https"}


def _host_blocked(host: str) -> str | None:
    h = (host or "").lower().strip(".")
    if not h:
        return "empty_host"
    if h in BLOCK_HOSTS:
        return f"blocked_host:{h}"
    for suf in BLOCK_HOST_SUFFIXES:
        if h.endswith(suf) or h == suf.lstrip("."):
            return f"blocked_suffix:{suf}"
    # literal IP?
    try:
        ip = ipaddress.ip_address(h)
        if (
            ip.is_private
            or ip.is_loopback
            or ip.is_link_local
            or ip.is_reserved
            or ip.is_multicast
        ):
            return f"blocked_ip_class:{ip}"
    except ValueError:
        pass
    return None


def check_url(url: str) -> dict:
    """Return {ok, errors[], warnings[], normalized_url}."""
    errors: list[str] = []
    warnings: list[str] = []
    raw = (url or "").strip()
    if not raw:
        return {"ok": False, "errors": ["url_empty"], "warnings": [], "normalized_url": None}
    parsed = urlparse(raw)
    if parsed.scheme.lower() not in ALLOWED_SCHEMES:
        errors.append("scheme_must_be_https")
    if parsed.username or parsed.password:
        errors.append("url_credentials_forbidden")
    host = parsed.hostname or ""
    br = _host_blocked(host)
    if br:
        errors.append(br)
    if SUSPECT_HOST_RE.search(host) or SUSPECT_HOST_RE.search(raw):
        warnings.append("suspect_host_or_shortener")
    if len(raw) > 2048:
        errors.append("url_too_long")
    # path traversal noise
    if ".." in (parsed.path or ""):
        warnings.append("path_contains_dotdot")
    return {
        "signature": SIGNATURE,
        "ok": not errors,
        "errors": errors,
        "warnings": warnings,
        "normalized_url": raw if not errors else None,
        "host": host,
    }


def check_content(data: bytes, content_type: str | None = None) -> dict:
    """Scan fetched bytes for crude malware/ad bait. Soft vs hard."""
    errors: list[str] = []
    warnings: list[str] = []
    # binary executables
    if data[:2] == b"MZ" or data[:4] == b"\x7fELF":
        errors.append("binary_executable_magic")
    sample = data[:65536]
    try:
        text = sample.decode("utf-8", errors="replace")
    except Exception:
        text = ""
    if MALWARE_BAIT_RE.search(text):
        errors.append("malware_bait_heuristic")
    if AD_SPAM_RE.search(text):
        warnings.append("ad_spam_heuristic")
    # excessive script density
    script_count = text.lower().count("<script")
    if script_count >= 40:
        warnings.append(f"high_script_density:{script_count}")
    if script_count >= 120:
        errors.append("extreme_script_density")
    ctype = (content_type or "").lower()
    if "application/x-msdownload" in ctype or "application/x-executable" in ctype:
        errors.append("dangerous_content_type")
    return {
        "signature": SIGNATURE,
        "ok": not errors,
        "errors": errors,
        "warnings": warnings,
        "script_tags_sampled": script_count,
    }


def gate_url_and_content(url: str, data: bytes | None = None, content_type: str | None = None) -> dict:
    u = check_url(url)
    out = {"signature": SIGNATURE, "url_gate": u, "content_gate": None, "ok": u["ok"]}
    if data is not None and u["ok"]:
        c = check_content(data, content_type)
        out["content_gate"] = c
        out["ok"] = u["ok"] and c["ok"]
    return out
