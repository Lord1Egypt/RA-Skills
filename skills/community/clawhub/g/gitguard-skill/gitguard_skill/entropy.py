"""
Secret detection via Shannon entropy + known credential-pattern matching.

Algorithm overview
-------------------
1. Tokenize each line into candidate strings (quoted values, assignment
   right-hand-sides, bare high-entropy tokens).
2. Compute the Shannon entropy of each candidate token:

       H(X) = -sum( p(x) * log2(p(x)) )   for each symbol x in token

   Random secrets (API keys, hashes, base64 blobs) cluster in a
   high-entropy band; English words and typical source code do not.
3. Cross-reference against known high-confidence patterns (AWS keys,
   private key headers, JWT structure, Slack tokens, generic
   "key/secret/token/password = ..." assignments) to raise confidence
   and classify severity even when entropy alone is ambiguous.
4. Findings are always returned with a REDACTED preview -- the raw
   secret value is never stored or displayed, only its position and a
   masked preview, so this tool is safe to run against your own
   repositories and share results with teammates.

This module only scans files that are already on disk / tracked in the
scanned repository. It performs no network calls and does not exfiltrate
anything -- it is a defensive, local-first tool.
"""
from __future__ import annotations

import math
import re
from pathlib import Path

from .models import SecretFinding, Severity

# --- Known high-confidence patterns -----------------------------------
KNOWN_PATTERNS: list[tuple[str, re.Pattern, Severity, float]] = [
    ("aws_access_key", re.compile(r"AKIA[0-9A-Z]{16}"), Severity.CRITICAL, 0.97),
    ("aws_secret_key", re.compile(r"(?i)aws_secret_access_key\s*[:=]\s*['\"]?[A-Za-z0-9/+=]{40}"), Severity.CRITICAL, 0.95),
    ("private_key_header", re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"), Severity.CRITICAL, 0.99),
    ("github_token", re.compile(r"gh[pousr]_[A-Za-z0-9]{36,}"), Severity.CRITICAL, 0.97),
    ("slack_token", re.compile(r"xox[baprs]-[0-9A-Za-z-]{10,}"), Severity.HIGH, 0.9),
    ("jwt", re.compile(r"eyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+"), Severity.MEDIUM, 0.6),
    ("generic_assignment", re.compile(
        r"(?i)(api[_-]?key|secret|token|password|passwd|pwd)\s*[:=]\s*['\"]([^'\"\s]{8,})['\"]"
    ), Severity.HIGH, 0.7),
    ("stripe_key", re.compile(r"sk_(live|test)_[0-9a-zA-Z]{20,}"), Severity.CRITICAL, 0.97),
    ("supabase_service_key", re.compile(r"eyJhbGciOi[A-Za-z0-9_.-]{40,}"), Severity.HIGH, 0.75),
]

# Common false-positive tokens we should never flag even at high entropy.
ALLOWLIST_SUBSTRINGS = {
    "lorem ipsum", "example.com", "your_api_key_here", "xxxxxxxx",
    "changeme", "placeholder", "sha256-", "sha384-", "sha512-",
    "your-secret", "your_secret", "your-key", "your_key",
}

# Search-dork operator syntax indicates the line is a QUERY TEMPLATE
# (e.g. security.sensitive_data dork strings like
# '"-----BEGIN RSA PRIVATE KEY-----"'), not an embedded credential.
# These strings are meant to be *searched for*, not secrets *in* this file.
DORK_OPERATOR_INDICATORS = ("site:", "filetype:", "inurl:", "intitle:", "-site:")

# Bare URL / identifier shapes that trigger high entropy but are not secrets.
IDENTIFIER_RE = re.compile(r"^[A-Z][A-Z0-9_]*$")  # ALL_CAPS_CONST_NAME, no secret entropy signal

# File extensions worth scanning; skip binaries / lockfiles / minified assets.
SCANNABLE_EXTENSIONS = {
    ".py", ".js", ".ts", ".jsx", ".tsx", ".json", ".yaml", ".yml",
    ".env", ".sh", ".bash", ".toml", ".ini", ".cfg", ".php", ".rb",
    ".go", ".java", ".rs", ".html", ".md", ".txt",
}

SKIP_DIR_NAMES = {".git", "node_modules", "venv", ".venv", "__pycache__", "dist", "build"}

# Candidate token extraction: quoted strings and bare alnum/symbol runs >= 16 chars.
# NOTE: deliberately excludes '.' and ':' from the bare-token charset so
# Python attribute chains (module.attr) and f-string format specs
# (value:.2f) don't get swept up as single high-entropy tokens. Full URLs
# are stripped from the line *before* tokenization instead (see
# _strip_urls) so they never reach this regex at all.
TOKEN_RE = re.compile(r"""['"]([A-Za-z0-9_\-/+=.]{12,})['"]|(?<![\w])([A-Za-z0-9_\-/+=]{20,})(?![\w])""")

URL_STRIP_RE = re.compile(r"https?://\S+")

# Lowercase snake_case / file-path shaped tokens (e.g. "search_dorks_skill/
# analyzer" or "my_module_name") are source-code identifiers or paths, not
# secrets -- real secrets almost always mix case and/or include digits.
SNAKE_PATH_RE = re.compile(r"^[a-z][a-z0-9_/]*$")

# Common placeholder markers beyond the substring allowlist above.
PLACEHOLDER_VALUE_RE = re.compile(r"(?i)^your[-_]")



def shannon_entropy(s: str) -> float:
    """Compute Shannon entropy (bits/char) of a string."""
    if not s:
        return 0.0
    freq: dict[str, int] = {}
    for ch in s:
        freq[ch] = freq.get(ch, 0) + 1
    length = len(s)
    entropy = 0.0
    for count in freq.values():
        p = count / length
        entropy -= p * math.log2(p)
    return entropy


def _redact(token: str) -> str:
    """Return a masked preview: first 4 + last 4 chars only."""
    if len(token) <= 10:
        return "*" * len(token)
    return f"{token[:4]}{'*' * (len(token) - 8)}{token[-4:]}"


def _is_allowlisted(line_lower: str) -> bool:
    return any(a in line_lower for a in ALLOWLIST_SUBSTRINGS)


def scan_line(line: str, line_number: int, file_path: str,
              entropy_threshold: float = 4.0) -> list[SecretFinding]:
    """Scan a single line for secrets. Returns zero or more findings."""
    findings: list[SecretFinding] = []
    line_lower = line.lower()
    if _is_allowlisted(line_lower):
        return findings

    # A line written as a search-dork query template (e.g. a string like
    # '"-----BEGIN RSA PRIVATE KEY-----"' used to *search for* exposed keys
    # on a target site) is not an embedded secret in this file -- skip it.
    is_dork_template = any(ind in line_lower for ind in DORK_OPERATOR_INDICATORS)
    if is_dork_template:
        return findings

    # 1) Known high-confidence patterns first (these win regardless of entropy).
    matched_pattern = False
    for name, pattern, severity, confidence in KNOWN_PATTERNS:
        m = pattern.search(line)
        if m:
            token = m.group(0)
            findings.append(SecretFinding(
                file=file_path,
                line_number=line_number,
                line_preview=_redact(token),
                entropy=round(shannon_entropy(token), 2),
                pattern_matched=name,
                severity=severity,
                confidence=confidence,
            ))
            matched_pattern = True

    if matched_pattern:
        return findings

    # 2) Fallback: generic high-entropy token detection.
    #    Strip full URLs first so they never get chopped into misleading
    #    high-entropy fragments by the tokenizer.
    scan_target = URL_STRIP_RE.sub(" ", line)
    for match in TOKEN_RE.finditer(scan_target):
        token = match.group(1) or match.group(2)
        if not token:
            continue
        if IDENTIFIER_RE.match(token) or SNAKE_PATH_RE.match(token) or PLACEHOLDER_VALUE_RE.match(token):
            continue  # CONST_NAMES, snake_case/paths, and "your-..." placeholders aren't secrets
        ent = shannon_entropy(token)
        if ent >= entropy_threshold and len(set(token)) > 6:
            # Heuristic confidence scales with how far above threshold we are.
            confidence = min(0.85, 0.4 + (ent - entropy_threshold) * 0.15)
            findings.append(SecretFinding(
                file=file_path,
                line_number=line_number,
                line_preview=_redact(token),
                entropy=round(ent, 2),
                pattern_matched="high_entropy",
                severity=Severity.MEDIUM if ent < 4.5 else Severity.HIGH,
                confidence=round(confidence, 2),
            ))
    return findings


def scan_file(path: Path, entropy_threshold: float = 4.0) -> list[SecretFinding]:
    findings: list[SecretFinding] = []
    try:
        text = path.read_text(errors="ignore")
    except (UnicodeDecodeError, OSError):
        return findings
    for i, line in enumerate(text.splitlines(), start=1):
        if len(line) > 2000:
            continue  # skip minified/huge lines, not worth scanning
        findings.extend(scan_line(line, i, str(path), entropy_threshold))
    return findings


def scan_repo(repo_path: str, entropy_threshold: float = 4.0,
              max_files: int = 5000) -> list[SecretFinding]:
    """Walk a repository and scan all text files for exposed secrets."""
    root = Path(repo_path)
    findings: list[SecretFinding] = []
    scanned = 0
    for p in root.rglob("*"):
        if scanned >= max_files:
            break
        if not p.is_file():
            continue
        if any(part in SKIP_DIR_NAMES for part in p.parts):
            continue
        if p.suffix.lower() not in SCANNABLE_EXTENSIONS and p.name != ".env":
            continue
        scanned += 1
        findings.extend(scan_file(p, entropy_threshold))
    return findings
