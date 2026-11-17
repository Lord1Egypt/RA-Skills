"""Canonical public-HTTPS URL checks shared by skill tooling."""

from __future__ import annotations

import ipaddress
import re
import socket
from typing import Any
from urllib.parse import urlsplit

MAX_PUBLIC_URL_LENGTH = 2048
IANA_POLICY_REVIEWED_DATE = "2026-08-19"
# Frozen from IANA's IPv4/IPv6 Special-Purpose Address and Special-Use Domain
# Name registries on the review date above, plus common private namespace
# suffixes that must never be resolved by this tooling.
SPECIAL_USE_DOMAIN_SUFFIXES = {
    "alt",
    "arpa",
    "corp",
    "example",
    "example.com",
    "example.net",
    "example.org",
    "home",
    "internal",
    "invalid",
    "lan",
    "local",
    "localhost",
    "onion",
    "test",
}
IPV4_NON_PUBLIC_NETWORKS = tuple(
    ipaddress.ip_network(network)
    for network in (
        "0.0.0.0/8",
        "10.0.0.0/8",
        "100.64.0.0/10",
        "127.0.0.0/8",
        "169.254.0.0/16",
        "172.16.0.0/12",
        "192.0.0.0/24",
        "192.0.2.0/24",
        "192.31.196.0/24",
        "192.52.193.0/24",
        "192.88.99.0/24",
        "192.168.0.0/16",
        "192.175.48.0/24",
        "198.18.0.0/15",
        "198.51.100.0/24",
        "203.0.113.0/24",
        "224.0.0.0/4",
        "240.0.0.0/4",
    )
)
IPV6_PUBLIC_UNICAST_NETWORK = ipaddress.ip_network("2000::/3")
IPV6_NON_PUBLIC_NETWORKS = tuple(
    ipaddress.ip_network(network)
    for network in (
        "2001::/23",
        "2001:db8::/32",
        "2002::/16",
        "2620:4f:8000::/48",
        "3fff::/20",
    )
)
DNS_LABEL_RE = re.compile(r"[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?")
UPPER_HEX_DIGITS = frozenset("0123456789ABCDEF")
URI_UNRESERVED_BYTES = frozenset(
    b"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-._~"
)


def is_public_unicast_address(
    address: ipaddress.IPv4Address | ipaddress.IPv6Address,
) -> bool:
    if isinstance(address, ipaddress.IPv4Address):
        return not any(address in network for network in IPV4_NON_PUBLIC_NETWORKS)
    return address in IPV6_PUBLIC_UNICAST_NETWORK and not any(
        address in network for network in IPV6_NON_PUBLIC_NETWORKS
    )


def is_special_use_hostname(hostname: str) -> bool:
    if "." not in hostname:
        return True
    return any(
        hostname == suffix or hostname.endswith(f".{suffix}")
        for suffix in SPECIAL_USE_DOMAIN_SUFFIXES
    )


def _canonical_host(hostname: str) -> tuple[str | None, ipaddress.IPv4Address | ipaddress.IPv6Address | None]:
    """Return the canonical ASCII host and any literal address it represents."""
    if hostname.endswith("."):
        return None, None

    if ":" in hostname:
        try:
            literal = ipaddress.ip_address(hostname)
        except ValueError:
            return None, None
        canonical = literal.compressed.lower()
        if hostname.lower() != canonical:
            return None, None
        return canonical, literal

    try:
        canonical = hostname.encode("idna").decode("ascii").lower()
    except UnicodeError:
        return None, None
    if hostname.lower() != canonical:
        return None, None
    if len(canonical) > 253 or any(
        not DNS_LABEL_RE.fullmatch(label) for label in canonical.split(".")
    ):
        return None, None

    try:
        literal = ipaddress.ip_address(canonical)
    except ValueError:
        try:
            # Catch browser-compatible integer, octal, hexadecimal, and short IPv4 forms.
            literal = ipaddress.ip_address(socket.inet_aton(canonical))
        except OSError:
            literal = None
        else:
            if canonical != str(literal):
                return None, None
    return canonical, literal


def _canonical_path_error(path: str) -> str | None:
    decoded_bytes = bytearray()
    index = 0
    while index < len(path):
        character = path[index]
        if ord(character) > 127:
            return "path must use ASCII URI syntax; percent-encode non-ASCII characters"
        if character != "%":
            decoded_bytes.append(ord(character))
            index += 1
            continue
        escape = path[index + 1 : index + 3]
        if len(escape) != 2 or any(digit not in UPPER_HEX_DIGITS for digit in escape):
            return "path percent escapes must use canonical uppercase %HH syntax"
        decoded = int(escape, 16)
        if decoded in URI_UNRESERVED_BYTES:
            return "path must not percent-encode unreserved URI characters"
        decoded_bytes.append(decoded)
        index += 3
    try:
        decoded_path = decoded_bytes.decode("utf-8")
    except UnicodeDecodeError:
        return "path percent escapes must form valid UTF-8"
    if any(
        ord(character) < 32
        or ord(character) == 127
        or character.isspace()
        or character in "<>\\"
        for character in decoded_path
    ):
        return "path must not encode whitespace, controls, angle brackets, or backslashes"
    return None


def resolve_public_addresses(
    hostname: str,
    port: int,
) -> tuple[ipaddress.IPv4Address | ipaddress.IPv6Address, ...]:
    canonical_host, literal = _canonical_host(hostname)
    if canonical_host is None:
        raise ValueError("must use a canonical ASCII or IDNA authority")
    if literal is not None:
        if not is_public_unicast_address(literal):
            raise ValueError(
                "must target a globally routable unicast IP address outside special-purpose ranges"
            )
        return (literal,)

    addresses: set[ipaddress.IPv4Address | ipaddress.IPv6Address] = set()
    for _family, _type, _proto, _canonname, sockaddr in socket.getaddrinfo(
        canonical_host,
        port,
        type=socket.SOCK_STREAM,
    ):
        address = ipaddress.ip_address(sockaddr[0].split("%", 1)[0])
        if not is_public_unicast_address(address):
            raise ValueError(
                "DNS must resolve only to globally routable unicast IP addresses outside "
                "special-purpose ranges"
            )
        addresses.add(address)
    if not addresses:
        raise socket.gaierror(f"No addresses returned for {canonical_host}")
    return tuple(sorted(addresses, key=lambda address: (address.version, address.packed)))


def public_https_url_error(value: Any, *, resolve_dns: bool = False) -> str | None:
    """Return a neutral validation error, or ``None`` for a canonical public URL."""
    if not isinstance(value, str) or not value:
        return "must be a nonempty canonical public HTTPS URL"
    if len(value) > MAX_PUBLIC_URL_LENGTH:
        return f"must be no longer than {MAX_PUBLIC_URL_LENGTH} characters"
    if any(ord(character) < 32 or ord(character) == 127 for character in value) or any(
        character.isspace() for character in value
    ):
        return "must not contain whitespace or control characters"
    if any(character in value for character in "<>"):
        return "must not contain angle brackets"
    if "\\" in value:
        return "must not contain backslashes"

    try:
        parsed = urlsplit(value)
        hostname = parsed.hostname
        explicit_port = parsed.port
    except ValueError:
        return "is not a valid URL"
    if parsed.scheme != "https" or not parsed.netloc or not hostname:
        return "must be a canonical public HTTPS URL"
    if "%" in parsed.netloc:
        return "must not contain percent-encoded authority characters"
    if parsed.username is not None or parsed.password is not None:
        return "must not contain embedded credentials"
    if parsed.query:
        return "must not contain a query string; use a canonical public page URL"
    if parsed.fragment:
        return "must not contain a URL fragment"
    path_problem = _canonical_path_error(parsed.path)
    if path_problem:
        return path_problem

    canonical_host, literal = _canonical_host(hostname)
    if canonical_host is None:
        return "must use a canonical ASCII or IDNA authority"
    expected_authority = (
        f"[{canonical_host}]" if isinstance(literal, ipaddress.IPv6Address) else canonical_host
    )
    if explicit_port is not None:
        expected_authority += f":{explicit_port}"
    if parsed.netloc != expected_authority:
        return "must use a canonical ASCII or IDNA authority"
    if explicit_port == 0:
        return "must use a valid nonzero HTTPS port"

    if literal is None and is_special_use_hostname(canonical_host):
        return "must not target a single-label or special-use hostname"
    if literal is not None and not is_public_unicast_address(literal):
        return "must target a globally routable unicast IP address outside special-purpose ranges"

    if resolve_dns and literal is None:
        try:
            resolve_public_addresses(canonical_host, explicit_port or 443)
        except ValueError as exc:
            return str(exc)
    return None
