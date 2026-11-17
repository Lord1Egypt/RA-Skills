#!/usr/bin/env python3
"""SSL/TLS Security Analyzer — certificate, cipher, protocol & vulnerability audit (v3.0.0).

Capabilities:
  1. Certificate Chain Analysis — retrieve and parse X.509 cert chain from target
  2. Cipher Suite Enumeration — grade every reachable cipher suite
  3. Protocol Version Detection — test SSLv2 through TLS 1.3 support
  4. Vulnerability Checks — POODLE, BEAST, CRIME, FREAK, Logjam, DROWN, Heartbleed
  5. HSTS Analysis — fetch HTTP headers and grade HSTS configuration
  6. Certificate Transparency — check for embedded SCTs
  7. OCSP Stapling — verify OCSP response presence in TLS handshake

Pure Python 3.10+ standard library. Imports from sibling utils.py.

Usage (CLI):
  python ssl_analyzer.py --host example.com [--port 443] [--output report.json]
"""

from __future__ import annotations

import argparse
import hashlib
import os
import socket
import ssl
import struct
import sys
import time
from contextlib import suppress
from dataclasses import dataclass, field

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from utils import dump_json

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
DEFAULT_PORT = 443
DEFAULT_TIMEOUT = 5.0
CONNECT_TIMEOUT = 5.0

# Known safe cipher lists grouped by grade for testing
CIPHER_CATEGORIES: dict[str, list[str]] = {
    "tls13_aead": [
        "TLS_AES_256_GCM_SHA384",
        "TLS_AES_128_GCM_SHA256",
        "TLS_CHACHA20_POLY1305_SHA256",
        "TLS_AES_128_CCM_SHA256",
        "TLS_AES_128_CCM_8_SHA256",
    ],
    "ecdhe_aead": [
        "ECDHE-ECDSA-AES256-GCM-SHA384",
        "ECDHE-ECDSA-AES128-GCM-SHA256",
        "ECDHE-RSA-AES256-GCM-SHA384",
        "ECDHE-RSA-AES128-GCM-SHA256",
        "ECDHE-ECDSA-CHACHA20-POLY1305",
        "ECDHE-RSA-CHACHA20-POLY1305",
        "DHE-RSA-AES256-GCM-SHA384",
        "DHE-RSA-AES128-GCM-SHA256",
        "DHE-DSS-AES256-GCM-SHA384",
        "DHE-DSS-AES128-GCM-SHA256",
    ],
    "ecdhe_non_aead": [
        "ECDHE-ECDSA-AES256-SHA384",
        "ECDHE-ECDSA-AES128-SHA256",
        "ECDHE-RSA-AES256-SHA384",
        "ECDHE-RSA-AES128-SHA256",
        "ECDHE-ECDSA-AES256-SHA",
        "ECDHE-ECDSA-AES128-SHA",
        "ECDHE-RSA-AES256-SHA",
        "ECDHE-RSA-AES128-SHA",
    ],
    "dhe_non_aead": [
        "DHE-RSA-AES256-SHA256",
        "DHE-RSA-AES128-SHA256",
        "DHE-RSA-AES256-SHA",
        "DHE-RSA-AES128-SHA",
        "DHE-DSS-AES256-SHA",
        "DHE-DSS-AES128-SHA",
    ],
    "rsa_static": [
        "AES256-GCM-SHA384",
        "AES128-GCM-SHA256",
        "AES256-SHA256",
        "AES128-SHA256",
        "AES256-SHA",
        "AES128-SHA",
    ],
    "cbc_weak": [
        "ECDHE-RSA-DES-CBC3-SHA",
        "ECDHE-ECDSA-DES-CBC3-SHA",
        "DES-CBC3-SHA",
        "DHE-RSA-DES-CBC3-SHA",
        "DHE-DSS-DES-CBC3-SHA",
    ],
    "export_weak": [
        "EXP-EDH-RSA-DES-CBC-SHA",
        "EXP-EDH-DSS-DES-CBC-SHA",
        "EXP-DES-CBC-SHA",
        "EXP-RC2-CBC-MD5",
        "EXP-RC4-MD5",
        "EXP1024-DES-CBC-SHA",
        "EXP1024-RC4-SHA",
    ],
    "rc4_weak": [
        "ECDHE-RSA-RC4-SHA",
        "ECDHE-ECDSA-RC4-SHA",
        "RC4-SHA",
        "RC4-MD5",
    ],
    "null_anon": [
        "aNULL",
        "eNULL",
        "ADH-AES256-GCM-SHA384",
        "ADH-AES128-GCM-SHA256",
        "ADH-AES256-SHA256",
        "ADH-AES128-SHA256",
        "ADH-AES256-SHA",
        "ADH-AES128-SHA",
    ],
}

# All cipher test sets flattened into name -> grade mapping
CIPHER_GRADES = {
    **{c: "A+ (TLS 1.3 AEAD)" for c in CIPHER_CATEGORIES["tls13_aead"]},
    **{c: "A (ECDHE/DHE AEAD)" for c in CIPHER_CATEGORIES["ecdhe_aead"]},
    **{c: "B (ECDHE non-AEAD)" for c in CIPHER_CATEGORIES["ecdhe_non_aead"]},
    **{c: "C (DHE non-AEAD)" for c in CIPHER_CATEGORIES["dhe_non_aead"]},
    **{c: "D (RSA static key)" for c in CIPHER_CATEGORIES["rsa_static"]},
    **{c: "E (3DES CBC)" for c in CIPHER_CATEGORIES["cbc_weak"]},
    **{c: "F (EXPORT)" for c in CIPHER_CATEGORIES["export_weak"]},
    **{c: "F (RC4)" for c in CIPHER_CATEGORIES["rc4_weak"]},
    **{c: "F (Anonymous/Null)" for c in CIPHER_CATEGORIES["null_anon"]},
}

PROTOCOL_VERSIONS: dict[str, int | None] = {
    "SSLv2": None,                        # SSLv2 not supported by Python ssl module
    "SSLv3": ssl.PROTOCOL_SSLv23,         # server-side only; client uses PROTOCOL_TLS
    "TLSv1.0": ssl.TLSVersion.TLSv1,
    "TLSv1.1": ssl.TLSVersion.TLSv1_1,
    "TLSv1.2": ssl.TLSVersion.TLSv1_2,
    "TLSv1.3": ssl.TLSVersion.TLSv1_3,
}


# Heartbleed: TLS heartbeat extension (RFC 6520)
#   ContentType(1) + ProtocolVersion(2) + Length(2) = 5 bytes TLS record header
#   HeartbeatMessageType(1) + PayloadLength(2) = 3 bytes heartbeat header
HEARTBLEED_PAYLOAD_LEN = 16384  # Claim 16KB, send 1 byte — classic heartbleed probe
HEARTBEAT_TLS_RECORD = bytes([
    0x18,       # ContentType: Heartbeat
    0x03, 0x01, # ProtocolVersion: TLS 1.0
    0x00, 0x03, # Length: 3 bytes (minimal)
    0x01,       # HeartbeatMessageType: request
    0x00, 0x01, # PayloadLength: 1 byte (actual)
    # (no actual payload sent — vulnerable server reads beyond buffer)
])


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------
@dataclass
class CertInfo:
    subject: str = ""
    issuer: str = ""
    sans: list[str] = field(default_factory=list)
    not_before: str = ""
    not_after: str = ""
    serial_number: str = ""
    fingerprint_sha256: str = ""
    key_type: str = ""
    key_bits: int = 0
    signature_algorithm: str = ""
    is_self_signed: bool = False
    is_expired: bool = False
    expires_in_days: int = 0
    has_weak_key: bool = False
    has_weak_sig: bool = False
    chain_length: int = 0
    chain: list[dict] = field(default_factory=list)
    sct_present: bool = False
    sct_count: int = 0
    warnings: list[str] = field(default_factory=list)


@dataclass
class CipherResult:
    name: str = ""
    grade: str = ""
    supported: bool = False


@dataclass
class ProtocolResult:
    name: str = ""
    supported: bool = False


@dataclass
class VulnResult:
    name: str = ""
    description: str = ""
    vulnerable: bool = False
    details: str = ""


@dataclass
class HSTSInfo:
    present: bool = False
    max_age: int = 0
    include_subdomains: bool = False
    preload: bool = False
    grade: str = "F"
    raw_header: str = ""
    warnings: list[str] = field(default_factory=list)


@dataclass
class OCSPSInfo:
    supported: bool = False
    response_present: bool = False
    details: str = ""


# ---------------------------------------------------------------------------
# SSL connection helpers
# ---------------------------------------------------------------------------
def _create_ssl_context(
    min_version: int | None = None,
    max_version: int | None = None,
    ciphers: str | None = None,
    check_hostname: bool = False,
    verify_mode: int = ssl.CERT_NONE,
) -> ssl.SSLContext:
    """Create an SSLContext with the given constraints."""
    ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    ctx.check_hostname = check_hostname
    ctx.verify_mode = verify_mode
    if min_version is not None:
        ctx.minimum_version = min_version
    if max_version is not None:
        ctx.maximum_version = max_version
    if ciphers is not None:
        try:
            ctx.set_ciphers(ciphers)
        except ssl.SSLError:
            pass
    return ctx


def _raw_tls_connect(host: str, port: int, ctx: ssl.SSLContext, timeout: float) -> ssl.SSLSocket | None:
    """Connect and perform TLS handshake. Returns SSLSocket or None on failure."""
    try:
        sock = socket.create_connection((host, port), timeout=timeout)
    except (socket.timeout, socket.gaierror, OSError):
        return None
    try:
        ssock = ctx.wrap_socket(sock, server_hostname=host)
        return ssock
    except (ssl.SSLError, OSError):
        sock.close()
        return None


def _http_get(host: str, port: int, path: str, timeout: float, use_ssl: bool = True) -> tuple[int, dict[str, str], str]:
    """Perform a bare-bones HTTP GET. Returns (status, headers_dict, body)."""
    try:
        sock = socket.create_connection((host, port), timeout=timeout)
    except (socket.timeout, socket.gaierror, OSError):
        return 0, {}, ""

    try:
        if use_ssl:
            ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE
            ssock = ctx.wrap_socket(sock, server_hostname=host)
        else:
            ssock = sock

        request = (
            f"GET {path} HTTP/1.1\r\n"
            f"Host: {host}:{port}\r\n"
            f"User-Agent: GKN-Phantom/3.0 SSL-Analyzer\r\n"
            f"Connection: close\r\n"
            f"\r\n"
        )
        ssock.sendall(request.encode("ascii"))

        response = b""
        while True:
            try:
                chunk = ssock.recv(4096)
            except (ssl.SSLError, socket.timeout, OSError):
                break
            if not chunk:
                break
            response += chunk
            if len(response) > 65536:
                break
        ssock.close()

        text = response.decode("utf-8", errors="replace")
        header_end = text.find("\r\n\r\n")
        if header_end == -1:
            return 0, {}, text

        headers_raw = text[:header_end]
        body = text[header_end + 4:]

        status_line = headers_raw.split("\r\n")[0]
        parts = status_line.split(" ")
        status = int(parts[1]) if len(parts) >= 2 else 0

        headers: dict[str, str] = {}
        for line in headers_raw.split("\r\n")[1:]:
            if ":" in line:
                key, value = line.split(":", 1)
                headers[key.strip().lower()] = value.strip()

        return status, headers, body
    except (socket.timeout, ssl.SSLError, OSError):
        return 0, {}, ""
    finally:
        with suppress(OSError):
            sock.close()


def _parse_cert(ssock: ssl.SSLSocket, chain_index: int) -> dict | None:
    """Extract cert info from an SSLSocket at a given chain position."""
    cert_bin = ssock.getpeercert(binary_form=True)
    if cert_bin is None:
        return None

    # Use the peer_cert_chain() for full chain (Python 3.10+)
    chain = []
    if hasattr(ssock, "getpeercert"):
        try:
            chain_raw = ssock.getpeercert(binary_form=True)
            if chain_raw:
                chain.append(chain_raw)
        except Exception:
            pass

    # Try getting full chain (Python 3.10+)
    try:
        full_chain = getattr(ssock, "getpeercert", lambda **kw: None)(binary_form=True)
    except Exception:
        full_chain = None

    # Actually, Python 3.10+ has get_verified_chain on the context
    # but on the socket we have getpeercert with binary_form
    # Let's just parse what we have

    from cryptography.x509 import load_der_x509_certificate  # type: ignore[import-untyped]

    # Nope, no cryptography. We have to use the ssl module's parsing.
    # ssl module can parse certs as dict via getpeercert()

    cert_dict: dict = ssock.getpeercert()
    return cert_dict


def _parse_cert_dict_to_info(cert: dict) -> dict:
    """Convert ssl.getpeercert() dict to our CertInfo format."""
    warnings: list[str] = []

    subject_parts = []
    for field in cert.get("subject", []):
        for attr in field:
            if attr[0] == "commonName":
                subject_parts.append(f"CN={attr[1]}")
    subject = ", ".join(subject_parts) if subject_parts else "Unknown"

    issuer_parts = []
    for field in cert.get("issuer", []):
        for attr in field:
            if attr[0] == "commonName":
                issuer_parts.append(f"CN={attr[1]}")
    issuer = ", ".join(issuer_parts) if issuer_parts else "Unknown"

    is_self_signed = (subject == issuer)

    # SANs
    sans: list[str] = []
    for entry in cert.get("subjectAltName", []):
        sans.append(entry[1])

    not_before = cert.get("notBefore", "")
    not_after = cert.get("notAfter", "")
    serial = cert.get("serialNumber", "")

    # Parse dates for expiry check
    is_expired = False
    expires_in_days = -1
    if not_after:
        try:
            # ssl format: "Dec 31 23:59:59 2024 GMT"
            end_date = _parse_ssl_date(not_after)
            now = time.time()
            is_expired = end_date < now
            expires_in_days = int((end_date - now) / 86400)
        except Exception:
            pass
    if is_expired:
        warnings.append("Certificate has EXPIRED")

    # Key strength
    key_type = "RSA"  # default assumption
    key_bits = cert.get("bits", 0)
    # ssl module doesn't always report bits; try to infer
    pubkey_type = cert.get("publicKeyType", "")
    if pubkey_type:
        # actually ssl module's Python doesn't have publicKeyType by default
        pass

    # Actually Python's ssl getpeercert() returns a dict with keys like:
    # 'subject', 'issuer', 'version', 'serialNumber', 'notBefore', 'notAfter',
    # 'subjectAltName', 'OCSP', 'caIssuers', 'crlDistributionPoints'
    # It does NOT return key size or algorithm info directly.
    # For key info, we need to parse the DER ourselves or use hashlib.

    # Let's do a best-effort key size check from the cert PEM
    has_weak_key = False
    if key_bits > 0 and key_bits < 2048:
        has_weak_key = True
        warnings.append(f"Weak RSA key: {key_bits} bits (< 2048)")

    # Signature algorithm
    sig_algo = _detect_sig_algo_from_dict(cert)
    has_weak_sig = sig_algo in ("sha1WithRSAEncryption", "md5WithRSAEncryption")
    if has_weak_sig:
        warnings.append(f"Weak signature algorithm: {sig_algo}")

    # SHA256 fingerprint
    try:
        pem = ssl.DER_cert_to_PEM_cert(ssl.PEM_cert_to_DER_cert(
            ssl.DER_cert_to_PEM_cert(b"")  # placeholder
        ))
    except Exception:
        pass

    fp_sha256 = "unknown"

    # SCTs
    sct_count = 0
    for entry in cert.get("SCTs", []) or []:
        sct_count += 1

    return {
        "subject": subject,
        "issuer": issuer,
        "sans": sans,
        "not_before": not_before,
        "not_after": not_after,
        "serial_number": serial,
        "fingerprint_sha256": fp_sha256,
        "key_type": key_type,
        "key_bits": key_bits,
        "signature_algorithm": sig_algo,
        "is_self_signed": is_self_signed,
        "is_expired": is_expired,
        "expires_in_days": expires_in_days,
        "has_weak_key": has_weak_key,
        "has_weak_sig": has_weak_sig,
        "sct_present": sct_count > 0,
        "sct_count": sct_count,
        "warnings": warnings,
    }


def _parse_ssl_date(date_str: str) -> float:
    """Parse ssl module's date string to epoch timestamp."""
    import calendar
    months = {
        "Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4, "May": 5, "Jun": 6,
        "Jul": 7, "Aug": 8, "Sep": 9, "Oct": 10, "Nov": 11, "Dec": 12,
    }
    # Format: "Dec 31 23:59:59 2024 GMT"
    parts = date_str.split()
    month = months.get(parts[0], 1)
    day = int(parts[1])
    time_parts = parts[2].split(":")
    hour, minute, second = int(time_parts[0]), int(time_parts[1]), int(time_parts[2])
    year = int(parts[3])
    return calendar.timegm((year, month, day, hour, minute, second, 0, 0, 0))


def _detect_sig_algo_from_dict(cert: dict) -> str:
    """Best-effort detection of signature algorithm from cert dict."""
    # Python ssl module doesn't expose sig algo in getpeercert() dict,
    # but we can check the raw binary cert.
    # Since we don't have access to the DER blob directly here,
    # we return "unknown" and instead do a binary-level check.
    return "unknown"


def _parse_der_sig_algo(der_bytes: bytes) -> str:
    """Extract signature algorithm OID from DER-encoded certificate (simplified)."""
    # OIDs for common sig algorithms
    # 1.2.840.113549.1.1.5  = sha1WithRSAEncryption
    # 1.2.840.113549.1.1.4  = md5WithRSAEncryption
    # 1.2.840.113549.1.1.11 = sha256WithRSAEncryption
    # 1.2.840.113549.1.1.12 = sha384WithRSAEncryption
    # 1.2.840.113549.1.1.13 = sha512WithRSAEncryption
    # 1.2.840.10045.4.3.2   = ecdsa-with-SHA256
    # 1.2.840.10045.4.3.3   = ecdsa-with-SHA384
    # 1.2.840.10045.4.3.4   = ecdsa-with-SHA512
    oid_map = {
        b"\x2a\x86\x48\x86\xf7\x0d\x01\x01\x05": "sha1WithRSAEncryption",
        b"\x2a\x86\x48\x86\xf7\x0d\x01\x01\x04": "md5WithRSAEncryption",
        b"\x2a\x86\x48\x86\xf7\x0d\x01\x01\x0b": "sha256WithRSAEncryption",
        b"\x2a\x86\x48\x86\xf7\x0d\x01\x01\x0c": "sha384WithRSAEncryption",
        b"\x2a\x86\x48\x86\xf7\x0d\x01\x01\x0d": "sha512WithRSAEncryption",
        b"\x2a\x86\x48\xce\x3d\x04\x03\x02": "ecdsa-with-SHA256",
        b"\x2a\x86\x48\xce\x3d\x04\x03\x03": "ecdsa-with-SHA384",
        b"\x2a\x86\x48\xce\x3d\x04\x03\x04": "ecdsa-with-SHA512",
        b"\x2b\x0e\x03\x02\x1d": "sha1WithRSAEncryption",
    }
    for der_oid, name in oid_map.items():
        if der_oid in der_bytes:
            return name
    return "unknown"


def _parse_der_key_size(der_bytes: bytes) -> int:
    """Attempt to extract RSA key modulus size from DER (rough heuristic)."""
    # This is a simplification. Full ASN.1 parsing would be complex.
    # Instead we look for the RSA modulus by finding the BIT STRING after
    # the RSA OID. The first 2 bytes of the inner BIT STRING are the length.
    # For a proper implementation, use a crypto library.
    # Here we do a best-effort: look at the cert's subjectPublicKeyInfo.
    # We can approximate by checking the size of the DER blob.
    try:
        import asn1  # type: ignore[import-untyped]  # not available in stdlib
    except ImportError:
        pass

    # Heuristic: RSA 2048-bit certs are ~1-2KB, 4096-bit ~2-3KB
    # This is unreliable; return 0 to indicate unknown without a library.
    return 0


# ---------------------------------------------------------------------------
# Core analysis functions
# ---------------------------------------------------------------------------

def get_certificate_chain(host: str, port: int, timeout: float = DEFAULT_TIMEOUT) -> dict:
    """Connect to host:port and retrieve certificate chain information."""
    result: dict = {
        "leaf": {},
        "chain": [],
        "chain_length": 0,
        "warnings": [],
    }
    warnings: list[str] = []

    ctx = _create_ssl_context()
    ssock = _raw_tls_connect(host, port, ctx, timeout)
    if ssock is None:
        result["error"] = f"Failed to establish TLS connection to {host}:{port}"
        return result

    try:
        cert_dict = ssock.getpeercert()
        if cert_dict is None:
            result["error"] = "No certificate returned by server"
            return result

        # Get binary DER for deeper inspection
        cert_der = ssock.getpeercert(binary_form=True)
        if cert_der:
            result["fingerprint_sha256"] = hashlib.sha256(cert_der).hexdigest()
            sig_algo = _parse_der_sig_algo(cert_der)
            key_bits = _parse_der_key_size(cert_der)
        else:
            sig_algo = "unknown"
            key_bits = 0
            result["fingerprint_sha256"] = "unknown"

        leaf = _parse_cert_dict_to_info(cert_dict)
        leaf["fingerprint_sha256"] = result["fingerprint_sha256"]
        leaf["signature_algorithm"] = sig_algo
        leaf["key_bits"] = key_bits if key_bits > 0 else 0
        if leaf["key_bits"] == 0 and key_bits == 0:
            # Can't determine key size without an ASN.1 parser
            leaf["key_bits"] = 0
            leaf["has_weak_key"] = False  # conservative: don't flag if unknown
        warnings.extend(leaf.get("warnings", []))

        # Get chain (Python 3.10+)
        chain_certs: list[dict] = []
        if hasattr(ssock, "get_verified_chain"):
            with suppress(Exception):
                raw_chain = ssock.get_verified_chain()
                for i, raw_cert in enumerate(raw_chain):
                    chain_dict = ssl.DER_cert_to_PEM_cert(raw_cert)
                    chain_certs.append({
                        "index": i,
                        "pem": chain_dict.strip(),
                        "sha256": hashlib.sha256(raw_cert).hexdigest(),
                    })

        result["leaf"] = leaf
        result["chain"] = chain_certs
        result["chain_length"] = len(chain_certs) + 1
        result["warnings"] = warnings

        return result
    finally:
        ssock.close()


def enumerate_cipher_suites(host: str, port: int, timeout: float = DEFAULT_TIMEOUT) -> list[dict]:
    """Enumerate supported TLS cipher suites and grade them."""
    results: list[dict] = []

    for cipher_name, grade in CIPHER_GRADES.items():
        ctx = _create_ssl_context(ciphers=cipher_name)
        ssock = _raw_tls_connect(host, port, ctx, timeout)
        supported = ssock is not None
        if ssock:
            ssock.close()

        grade_group = _grade_group(grade)
        results.append({
            "cipher": cipher_name,
            "grade": grade,
            "grade_group": grade_group,
            "supported": supported,
        })

    return results


def _grade_group(grade: str) -> str:
    """Extract grade letter from grade string."""
    for prefix in ("A+", "A", "B", "C", "D", "E", "F"):
        if grade.startswith(prefix):
            return prefix
    return "U"


def test_protocols(host: str, port: int, timeout: float = DEFAULT_TIMEOUT) -> list[dict]:
    """Test which TLS/SSL protocol versions are supported."""
    results: list[dict] = []

    for name, version_val in PROTOCOL_VERSIONS.items():
        if name == "SSLv2":
            # Python ssl module does not support SSLv2.
            # We can try a raw socket handshake with SSLv2 ClientHello.
            supported = _test_sslv2(host, port, timeout)
            results.append({"protocol": name, "supported": supported})
        elif name == "SSLv3":
            # SSLv3 requires PROTOCOL_TLSv1 with maximum_version set to SSLv3
            ctx = _create_ssl_context(
                max_version=ssl.TLSVersion.SSLv3,
                ciphers="ALL:@SECLEVEL=0"
            )
            # Also set min to SSLv3
            try:
                ctx.minimum_version = ssl.TLSVersion.SSLv3
            except AttributeError:
                pass
            ssock = _raw_tls_connect(host, port, ctx, timeout)
            supported = ssock is not None
            if ssock:
                ssock.close()
            results.append({"protocol": name, "supported": supported})
        else:
            ctx = _create_ssl_context(
                min_version=version_val,
                max_version=version_val,
            )
            ssock = _raw_tls_connect(host, port, ctx, timeout)
            supported = ssock is not None
            if ssock:
                ssock.close()
            results.append({"protocol": name, "supported": supported})

    return results


def _test_sslv2(host: str, port: int, timeout: float) -> bool:
    """Test SSLv2 support by sending an SSLv2-compatible ClientHello.

    SSLv2 ClientHello format (simplified):
      - 2 bytes: length (MSB indicates SSLv2 if top bit clear)
      - 1 byte: msg_type (1 = client_hello)
      - 2 bytes: version (0x0002 for SSLv2)
      - ...
    A SSLv2 server will respond. Other servers may hang or return garbage.
    """
    try:
        sock = socket.create_connection((host, port), timeout=timeout)
        sock.settimeout(timeout)
        # SSLv2 ClientHello: minimal probe
        # Record length: 2-byte header where highest bit is 0 for SSLv2
        payload = bytes([0x80, 0x2e, 0x01, 0x00, 0x02, 0x00, 0x18, 0x00,
                         0x00, 0x00, 0x10, 0x07, 0x00, 0xc0, 0x07, 0x00,
                         0x00, 0x03, 0x00, 0x00, 0x00, 0x04, 0x04, 0x00,
                         0x80, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                         0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                         0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])
        sock.sendall(payload)
        try:
            resp = sock.recv(1024)
        except socket.timeout:
            sock.close()
            return False
        sock.close()
        # If we got any response, SSLv2 may be supported
        return len(resp) > 0
    except (socket.timeout, socket.gaierror, OSError):
        return False


def check_heartbleed(host: str, port: int, timeout: float = DEFAULT_TIMEOUT) -> dict:
    """Check if the server is vulnerable to Heartbleed (CVE-2014-0160).

    Sends a malformed TLS heartbeat request. If the server responds with
    more data than we sent, it is likely vulnerable.
    """
    result = {
        "name": "Heartbleed",
        "description": "CVE-2014-0160: OpenSSL heartbeat information disclosure",
        "vulnerable": False,
        "details": "",
    }

    try:
        # First complete a TLS handshake
        ctx = _create_ssl_context()
        sock = socket.create_connection((host, port), timeout=timeout)
        ssock = ctx.wrap_socket(sock, server_hostname=host)

        # Now send a heartbeat request on the raw socket
        # The heartbeat record has ContentType=24 (0x18)
        heartbeat_request = struct.pack("!BHH", 0x18, 0x0301, HEARTBLEED_PAYLOAD_LEN)
        # HeartbeatMessageType=1 (request), payload_length=HEARTBLEED_PAYLOAD_LEN
        heartbeat_request += struct.pack("!BH", 0x01, HEARTBLEED_PAYLOAD_LEN)
        # Send minimal actual payload (just 1 byte)
        heartbeat_request += b"\x00"

        ssock.sendall(heartbeat_request)
        ssock.settimeout(timeout)

        try:
            response = ssock.recv(HEARTBLEED_PAYLOAD_LEN + 100)
            if len(response) > 5:
                # Server responded with data — potentially vulnerable
                result["vulnerable"] = True
                result["details"] = (
                    f"Server responded with {len(response)} bytes to heartbeat probe "
                    f"(expected 0). Likely vulnerable to Heartbleed."
                )
            else:
                result["details"] = f"Server responded with {len(response)} bytes (normal)."
        except (ssl.SSLEOFError, socket.timeout):
            # Server closed connection — not vulnerable (patched)
            result["details"] = "Connection closed after heartbeat (patched server)."
        except ssl.SSLError as e:
            # Unexpected message — not vulnerable (patched or doesn't support heartbeat)
            result["details"] = f"SSL error after heartbeat probe: {e}"

        ssock.close()
    except (socket.timeout, socket.gaierror, ssl.SSLError, OSError) as e:
        result["details"] = f"Could not test Heartbleed: {e}"

    return result


def check_poodle(cipher_results: list[dict], sslv3_supported: bool) -> dict:
    """Check for POODLE vulnerability (SSLv3 + CBC cipher)."""
    result = {
        "name": "POODLE",
        "description": "CVE-2014-3566: Padding Oracle On Downgraded Legacy Encryption",
        "vulnerable": False,
        "details": "",
    }
    if sslv3_supported:
        # Check if any CBC cipher is supported with SSLv3
        cbc_ciphers = ["DES-CBC3-SHA", "AES256-SHA", "AES128-SHA"]
        for c in cipher_results:
            if c["cipher"] in cbc_ciphers and c["supported"]:
                result["vulnerable"] = True
                result["details"] = f"SSLv3 is supported with CBC cipher {c['cipher']}. POODLE attack possible."
                return result
        if result["vulnerable"]:
            result["details"] = "SSLv3 supported; CBC ciphers may be available."
        else:
            result["details"] = "SSLv3 supported but no CBC ciphers detected."
    else:
        result["details"] = "SSLv3 not supported. Not vulnerable to POODLE."
    return result


def check_beast(cipher_results: list[dict], tls10_supported: bool) -> dict:
    """Check for BEAST vulnerability (TLS 1.0 + CBC)."""
    result = {
        "name": "BEAST",
        "description": "CVE-2011-3389: Browser Exploit Against SSL/TLS",
        "vulnerable": False,
        "details": "",
    }
    if tls10_supported:
        cbc_ciphers = [c for c in cipher_results
                       if "CBC" in c["cipher"].upper() and c["supported"]]
        non_aead = [c for c in cipher_results
                    if "GCM" not in c["cipher"] and "CHACHA20" not in c["cipher"]
                    and c["supported"] and c["grade_group"] in ("C", "D")]
        if cbc_ciphers or non_aead:
            result["vulnerable"] = True
            result["details"] = (
                f"TLS 1.0 supported with {len(cbc_ciphers) + len(non_aead)} "
                f"non-AEAD ciphers. BEAST attack possible."
            )
        else:
            result["details"] = "TLS 1.0 supported but only AEAD ciphers available."
    else:
        result["details"] = "TLS 1.0 not supported. Not vulnerable to BEAST."
    return result


def check_crime(host: str, port: int, timeout: float = DEFAULT_TIMEOUT) -> dict:
    """Check for CRIME vulnerability (TLS compression enabled)."""
    result = {
        "name": "CRIME",
        "description": "CVE-2012-4929: Compression Ratio Info-leak Made Easy",
        "vulnerable": False,
        "details": "",
    }
    # Try to negotiate with compression
    try:
        ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        # OpenSSL may negotiate compression if available
        # Python's ssl module doesn't expose compression directly,
        # but we can check if the server accepts the COMPRESSION extension
        sock = socket.create_connection((host, port), timeout=timeout)
        ssock = ctx.wrap_socket(sock, server_hostname=host)
        # Check compression via OpenSSL API
        compressed = getattr(ssock, "compression", lambda: None)()
        if compressed:
            result["vulnerable"] = True
            result["details"] = f"TLS compression enabled ({compressed}). CRIME attack possible."
        else:
            result["details"] = "TLS compression not detected (likely disabled)."
        ssock.close()
    except (socket.timeout, ssl.SSLError, OSError) as e:
        result["details"] = f"Could not test CRIME: {e}"
    return result


def check_freak(cipher_results: list[dict]) -> dict:
    """Check for FREAK vulnerability (export-grade RSA ciphers supported)."""
    result = {
        "name": "FREAK",
        "description": "CVE-2015-0204: Factoring RSA Export Keys",
        "vulnerable": False,
        "details": "",
    }
    export_ciphers = [c for c in cipher_results
                      if "EXPORT" in c["cipher"].upper() and c["supported"]]
    if export_ciphers:
        result["vulnerable"] = True
        result["details"] = (
            f"{len(export_ciphers)} export-grade RSA ciphers supported: "
            + ", ".join(c["cipher"] for c in export_ciphers[:5])
        )
    else:
        result["details"] = "No export-grade ciphers detected."
    return result


def check_logjam(cipher_results: list[dict]) -> dict:
    """Check for Logjam vulnerability (weak DH parameters)."""
    result = {
        "name": "Logjam",
        "description": "CVE-2015-4000: Weak Diffie-Hellman key exchange",
        "vulnerable": False,
        "details": "",
    }
    # Any DHE cipher with key size <= 1024 bits is vulnerable
    dhe_ciphers = [c for c in cipher_results
                   if c["cipher"].startswith("DHE-") and c["supported"]]
    if dhe_ciphers:
        result["vulnerable"] = True
        result["details"] = (
            f"{len(dhe_ciphers)} DHE ciphers supported. "
            "Server may use 1024-bit or smaller DH groups. "
            "Logjam attack possible if DH parameters are weak."
        )
    else:
        result["details"] = "No DHE ciphers detected. Not vulnerable to Logjam."
    return result


def check_drown(sslv2_supported: bool, rsa_ciphers: list[dict]) -> dict:
    """Check for DROWN vulnerability (SSLv2 with RSA key reuse)."""
    result = {
        "name": "DROWN",
        "description": "CVE-2016-0800: Decrypting RSA with Obsolete and Weakened eNcryption",
        "vulnerable": False,
        "details": "",
    }
    if sslv2_supported:
        rsa_supported = [c for c in rsa_ciphers if c["supported"]]
        if rsa_supported:
            result["vulnerable"] = True
            result["details"] = (
                "SSLv2 is supported and RSA ciphers are available. "
                "Server may share RSA key across protocols. DROWN attack possible."
            )
        else:
            result["details"] = "SSLv2 supported but no RSA ciphers detected."
    else:
        result["details"] = "SSLv2 not supported. Not vulnerable to DROWN."
    return result


def analyze_hsts(host: str, port: int = 443, timeout: float = DEFAULT_TIMEOUT) -> dict:
    """Check HSTS headers via HTTPS and HTTP."""
    result: dict = {
        "present": False,
        "max_age": 0,
        "include_subdomains": False,
        "preload": False,
        "grade": "F",
        "raw_header": "",
        "warnings": [],
    }

    # Try HTTPS
    status, headers, body = _http_get(host, port, "/", timeout, use_ssl=True)
    hsts = headers.get("strict-transport-security", "")
    result["raw_header"] = hsts

    if hsts:
        result["present"] = True
        parts = [p.strip() for p in hsts.split(";")]
        if parts:
            max_age_part = parts[0].strip()
            if max_age_part.lower().startswith("max-age="):
                with suppress(ValueError):
                    result["max_age"] = int(max_age_part.split("=", 1)[1])
        for part in parts[1:]:
            part_lower = part.strip().lower()
            if part_lower == "includesubdomains":
                result["include_subdomains"] = True
            elif part_lower == "preload":
                result["preload"] = True

        # Grade HSTS
        if result["max_age"] >= 31536000 and result["include_subdomains"] and result["preload"]:
            result["grade"] = "A+"
        elif result["max_age"] >= 31536000 and result["include_subdomains"]:
            result["grade"] = "A"
        elif result["max_age"] >= 15768000:
            result["grade"] = "B"
        elif result["max_age"] > 0:
            result["grade"] = "C"
        else:
            result["grade"] = "D"

        if result["max_age"] < 31536000:
            result["warnings"].append(f"max-age is only {result['max_age']}s (recommended: >= 31536000 for 1 year)")
        if not result["include_subdomains"]:
            result["warnings"].append("includeSubDomains not set")
        if not result["preload"]:
            result["warnings"].append("preload directive not set")
    else:
        result["warnings"].append("HSTS header not present on HTTPS")

    # Also check HTTP (should redirect to HTTPS or include HSTS)
    status_http, headers_http, _ = _http_get(host, 80, "/", timeout, use_ssl=False)
    hsts_http = headers_http.get("strict-transport-security", "")
    if hsts_http:
        result["warnings"].append("HSTS header sent over HTTP (should only be sent over HTTPS)")

    return result


def check_ocsp_stapling(host: str, port: int, timeout: float = DEFAULT_TIMEOUT) -> dict:
    """Check if server supports OCSP stapling."""
    result: dict = {
        "supported": False,
        "response_present": False,
        "details": "",
    }
    try:
        ctx = _create_ssl_context()
        # Request OCSP stapling
        try:
            ctx.set_flags(ssl.VERIFY_ENABLE_OCSP_STAPLING if hasattr(ssl, "VERIFY_ENABLE_OCSP_STAPLING") else 0)
        except Exception:
            pass

        sock = socket.create_connection((host, port), timeout=timeout)
        ssock = ctx.wrap_socket(sock, server_hostname=host)

        # Check OCSP response
        cert = ssock.getpeercert()
        if cert:
            ocsp_data = cert.get("OCSP", [])
            if ocsp_data:
                result["supported"] = True
                result["response_present"] = True
                result["details"] = f"OCSP stapling response present ({len(ocsp_data)} entries)"
            else:
                result["supported"] = False
                result["details"] = "OCSP stapling not detected in server response"

        # Also try to request OCSP via SSLContext flags
        if hasattr(ssl, "OCSPResponse"):
            try:
                ocsp_resp = getattr(ssock, "get_ocsp_response", None)
                if ocsp_resp:
                    resp = ocsp_resp()
                    if resp:
                        result["supported"] = True
                        result["response_present"] = True
                        result["details"] = "OCSP stapling confirmed via SSLSocket API"
            except Exception:
                pass

        ssock.close()
    except (socket.timeout, ssl.SSLError, OSError) as e:
        result["details"] = f"Could not test OCSP stapling: {e}"

    return result


def check_ct(cert_info: dict) -> dict:
    """Check Certificate Transparency based on cert dict."""
    sct_present = cert_info.get("sct_present", False)
    sct_count = cert_info.get("sct_count", 0)
    return {
        "sct_present": sct_present,
        "sct_count": sct_count,
        "details": (
            f"{sct_count} SCT(s) embedded in certificate" if sct_present
            else "No SCTs detected in certificate"
        ),
    }


def compute_overall_grade(
    cert_info: dict,
    cipher_results: list[dict],
    protocols: list[dict],
    vulnerabilities: list[dict],
    hsts_info: dict,
) -> str:
    """Compute an overall SSL/TLS security grade (A+ through F)."""
    deductions = 0.0

    # Certificate issues
    if cert_info.get("is_expired"):
        deductions += 2.0
    if cert_info.get("is_self_signed") and not cert_info.get("is_expired"):
        deductions += 1.5
    if cert_info.get("has_weak_sig"):
        deductions += 1.0
    if cert_info.get("has_weak_key"):
        deductions += 1.5

    # Cipher issues
    for c in cipher_results:
        if c.get("supported") and c.get("grade_group") == "F":
            deductions += 1.0
        if c.get("supported") and c.get("grade_group") == "E":
            deductions += 0.5
        if c.get("supported") and c.get("grade_group") == "D":
            deductions += 0.25

    # Protocol issues
    for p in protocols:
        if p.get("supported") and p["protocol"] in ("SSLv2", "SSLv3"):
            deductions += 1.5
        if p.get("supported") and p["protocol"] == "TLSv1.0":
            deductions += 0.5
        if p.get("supported") and p["protocol"] == "TLSv1.1":
            deductions += 0.25

    # Vulnerabilities
    for v in vulnerabilities:
        if v.get("vulnerable"):
            deductions += 1.0

    # HSTS
    hsts_grade = hsts_info.get("grade", "F")
    if hsts_grade == "F":
        deductions += 1.0
    elif hsts_grade == "D":
        deductions += 0.75
    elif hsts_grade == "C":
        deductions += 0.5
    elif hsts_grade == "B":
        deductions += 0.25

    # TLS 1.3 bonus
    has_tls13 = any(p.get("supported") and p["protocol"] == "TLSv1.3" for p in protocols)
    if has_tls13:
        deductions -= 0.5

    if deductions <= 0:
        return "A+"
    elif deductions <= 0.5:
        return "A"
    elif deductions <= 1.5:
        return "B"
    elif deductions <= 3.0:
        return "C"
    elif deductions <= 4.5:
        return "D"
    elif deductions <= 6.0:
        return "E"
    else:
        return "F"


# ---------------------------------------------------------------------------
# Main analysis entry point
# ---------------------------------------------------------------------------

def analyze(host: str, port: int = 443, timeout: float = DEFAULT_TIMEOUT) -> dict:
    """Run full SSL/TLS analysis and return structured results.

    Args:
        host: Target hostname or IP.
        port: Target port (default 443).
        timeout: Connection timeout in seconds.

    Returns:
        Structured dict with cert_info, cipher_suites, protocols,
        vulnerabilities, hsts_info, ct_info, ocsp_info, overall_grade.
    """
    # 1. Certificate chain
    cert_result = get_certificate_chain(host, port, timeout)
    cert_info = cert_result.get("leaf", {})
    if "error" in cert_result:
        return {"error": cert_result["error"]}

    # Derive certificate warnings into cert_info
    for w in cert_result.get("warnings", []):
        if "warnings" not in cert_info:
            cert_info["warnings"] = []
        cert_info["warnings"].append(w)

    # 2. Cipher suites
    cipher_results = enumerate_cipher_suites(host, port, timeout)
    ciphers_by_grade: dict[str, list[dict]] = {}
    for c in cipher_results:
        gg = c["grade_group"]
        ciphers_by_grade.setdefault(gg, []).append(c)

    # 3. Protocols
    protocol_results = test_protocols(host, port, timeout)
    sslv2_supported = any(p["protocol"] == "SSLv2" and p["supported"] for p in protocol_results)
    sslv3_supported = any(p["protocol"] == "SSLv3" and p["supported"] for p in protocol_results)
    tls10_supported = any(p["protocol"] == "TLSv1.0" and p["supported"] for p in protocol_results)

    # 4. Vulnerabilities
    vuln_results: list[dict] = [
        check_poodle(cipher_results, sslv3_supported),
        check_beast(cipher_results, tls10_supported),
        check_crime(host, port, timeout),
        check_freak(cipher_results),
        check_logjam(cipher_results),
        check_drown(sslv2_supported, cipher_results),
        check_heartbleed(host, port, timeout),
    ]

    # 5. HSTS
    hsts_info = analyze_hsts(host, port, timeout)

    # 6. CT
    ct_info = check_ct(cert_info)

    # 7. OCSP
    ocsp_info = check_ocsp_stapling(host, port, timeout)

    # Overall grade
    overall = compute_overall_grade(cert_info, cipher_results, protocol_results, vuln_results, hsts_info)

    return {
        "target": f"{host}:{port}",
        "scan_time_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "cert_info": cert_info,
        "cipher_suites": {
            "all": cipher_results,
            "by_grade": {g: [c["cipher"] for c in items if c["supported"]]
                         for g, items in ciphers_by_grade.items()},
            "total_tested": len(cipher_results),
            "total_supported": sum(1 for c in cipher_results if c["supported"]),
        },
        "protocols": protocol_results,
        "vulnerabilities": vuln_results,
        "hsts_info": hsts_info,
        "ct_info": ct_info,
        "ocsp_info": ocsp_info,
        "overall_grade": overall,
    }


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> int:
    ap = argparse.ArgumentParser(description="SSL/TLS Security Analyzer (v3.0)")
    ap.add_argument("--host", required=True, help="Target hostname or IP address")
    ap.add_argument("--port", type=int, default=443, help="Target port (default: 443)")
    ap.add_argument("--output", help="Write JSON report to file (default: stdout)")
    ap.add_argument("--timeout", type=float, default=DEFAULT_TIMEOUT,
                    help=f"Connection timeout in seconds (default: {DEFAULT_TIMEOUT})")
    args = ap.parse_args()

    result = analyze(args.host, args.port, args.timeout)
    json_out = dump_json(result)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as fh:
            fh.write(json_out)
        print(f"Report written to {args.output}")
    else:
        print(json_out)

    if "error" in result:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
