"""
Grounding Gate — Layer 2 semi-deterministic checks for non-coding task verification.
Uses stdlib only (no external deps). Runs after Structural Gate, before LLM Council.
"""
from dataclasses import dataclass, field
from datetime import datetime
import ipaddress
import logging
import os
import re
import socket
import urllib.error
import urllib.request
from urllib.parse import urlparse


logger = logging.getLogger(__name__)

IP_BLOCKLIST = [
    ipaddress.ip_network("169.254.0.0/16"),
    ipaddress.ip_network("10.0.0.0/8"),
    ipaddress.ip_network("127.0.0.0/8"),
    ipaddress.ip_network("172.16.0.0/12"),
    ipaddress.ip_network("192.168.0.0/16"),
]


def _get_blocked_ips() -> list[ipaddress._BaseNetwork]:
    return IP_BLOCKLIST


def _is_private_ip(ip_str: str) -> bool:
    ip = ipaddress.ip_address(ip_str)
    return bool(ip.is_private or ip.is_loopback or ip.is_link_local or ip.is_reserved)


def _resolve_and_validate_host(url: str) -> tuple[bool, str]:
    parsed = urlparse(url)
    host = parsed.hostname
    if not host:
        return False, "missing hostname"

    try:
        ip = ipaddress.ip_address(host)
        if _is_private_ip(str(ip)):
            return False, f"blocked private IP: {ip}"
        return True, str(ip)
    except ValueError:
        pass

    try:
        addr_info = socket.getaddrinfo(host, None)
    except OSError as exc:
        return False, f"dns lookup failed: {exc}"

    ips: list[str] = []
    for family, _socktype, _proto, _canon, sockaddr in addr_info:
        if family == socket.AF_INET:
            ip_str = sockaddr[0]
        elif family == socket.AF_INET6:
            ip_str = sockaddr[0]
        else:
            continue
        ips.append(ip_str)
        if _is_private_ip(ip_str):
            return False, f"blocked private IP: {ip_str}"

    if not ips:
        return False, "no A/AAAA records found"

    return True, ips[0]


@dataclass
class GroundingResult:
    passed: bool
    failures: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    details: str = ""

    @property
    def summary(self) -> str:
        parts = []
        if self.failures:
            parts.append(f"FAIL: {'; '.join(self.failures)}")
        if self.warnings:
            parts.append(f"WARN: {'; '.join(self.warnings)}")
        if not parts:
            return "Grounding Gate: PASS ✅"
        status = "FAIL ❌" if self.failures else "PASS ⚠️"
        return f"Grounding Gate: {status} — " + " | ".join(parts)


def _extract_urls(text: str) -> list[str]:
    return re.findall(r"https?://[^\s\)\]\>\"\']+", text)[:5]  # max 5


def _check_url(url: str, timeout: int = 3, max_retries: int = 2) -> bool:
    parsed = urlparse(url)
    if parsed.scheme.lower() == "file":
        logger.warning("Blocked file URL in grounding gate: %s", url)
        return False
    if parsed.scheme and parsed.scheme.lower() not in ("http", "https"):
        logger.warning("Blocked non-HTTP URL in grounding gate: %s", url)
        return False
    if not parsed.hostname:
        logger.warning("Blocked URL without hostname in grounding gate: %s", url)
        return False

    if os.environ.get("GOVERNED_NO_NETWORK") == "1":
        logger.warning("Skipping URL check due to GOVERNED_NO_NETWORK=1: %s", url)
        return True

    ok, reason = _resolve_and_validate_host(url)
    if not ok:
        logger.warning("Blocked URL in grounding gate: %s (%s)", url, reason)
        return False

    for attempt in range(1, max_retries + 1):
        try:
            logger.info("HTTP HEAD %s attempt %d/%d", url, attempt, max_retries)
            req = urllib.request.Request(
                url,
                method="HEAD",
                headers={"User-Agent": "governed-agents-verifier/1.0"},
            )
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                return resp.status < 400
        except Exception:
            continue
    return False


def run_grounding_gate(output: str, profile: dict) -> GroundingResult:
    checks = profile.get("grounding_checks", [])
    failures: list[str] = []
    warnings: list[str] = []

    for check in checks:
        if check == "url_reachable":
            urls = _extract_urls(output)
            if urls:
                for url in urls:
                    logger.info("Grounding gate probing URL: %s", url)
                dead = [u for u in urls if not _check_url(u)]
                if dead:
                    failures.append(
                        f"url_reachable: unreachable — {', '.join(dead[:2])}"
                    )
            # No URLs found = no failure (structural gate handles sources_list)

        elif check == "citations_present":
            citation_patterns = [
                r"\w+ et al\.",  # Author et al.
                r"\[\d+\]",  # [1]
                r"\(\w+ \d{4}\)",  # (Smith 2024)
                r"\(\w+,? \d{4}\)",  # (Smith, 2024)
            ]
            has_citation = any(re.search(p, output) for p in citation_patterns)
            if not has_citation:
                failures.append("citations_present: no citation patterns found")

        elif check == "numbers_consistent":
            # Heuristic: warn if same number appears with conflicting units
            numbers = re.findall(
                r"\b(\d+(?:\.\d+)?)\s*(%|users?|requests?|ms|seconds?)",
                output,
            )
            seen: dict[str, str] = {}
            for num, unit in numbers:
                if num in seen and seen[num] != unit:
                    warnings.append(
                        f"numbers_consistent: '{num}' used with both '{seen[num]}' and '{unit}'"
                    )
                seen[num] = unit

        elif check == "cross_refs_resolve":
            refs = re.findall(
                r'(?:see section|as described in|refer to)\s+["\']?([^"\'\n,\.]+)',
                output,
                re.IGNORECASE,
            )
            for ref in refs:
                ref_clean = ref.strip().lower()
                if ref_clean and ref_clean not in output.lower():
                    failures.append(
                        f"cross_refs_resolve: reference '{ref.strip()}' not found in output"
                    )

        elif check == "dates_valid":
            date_patterns = [
                (r"\b(\d{4})-(\d{2})-(\d{2})\b", "%Y-%m-%d"),
                (r"\b(\d{2})\.(\d{2})\.(\d{4})\b", "%d.%m.%Y"),
            ]
            now = datetime.now()
            for pattern, fmt in date_patterns:
                matches = re.findall(pattern, output)
                for match in matches:
                    try:
                        if fmt == "%Y-%m-%d":
                            date_str = f"{match[0]}-{match[1]}-{match[2]}"
                        else:
                            date_str = f"{match[0]}.{match[1]}.{match[2]}"
                        date = datetime.strptime(date_str, fmt)
                        years_diff = (now - date).days / 365
                        if years_diff > 10:
                            warnings.append(
                                f"dates_valid: date '{date_str}' is >10 years in the past"
                            )
                        elif years_diff < -5:
                            warnings.append(
                                f"dates_valid: date '{date_str}' is >5 years in the future"
                            )
                    except ValueError:
                        pass
        # Unknown checks skipped silently

    return GroundingResult(
        passed=len(failures) == 0,
        failures=failures,
        warnings=warnings,
        details="\n".join(failures + [f"WARN: {w}" for w in warnings])
        or "All grounding checks passed",
    )
