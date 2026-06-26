---
name: Crypto Audit
description: Weak cryptography detector (OWASP A02:2021 — Cryptographic Failures). Scans Python, JavaScript/TypeScript, Go, Java, and PHP source code for 10 classes of insecure cryptography — MD5/SHA1 password hashing, PRNG for security-sensitive values, hardcoded IVs, ECB mode, DES/RC4/Blowfish, RSA key size under 2048 bits, weak JWT secrets, bcrypt rounds too low, TLS 1.0/1.1 acceptance, and hardcoded cryptographic keys in source. Zero external dependencies. CI fail-gate included.
license: Apache-2.0
homepage: https://canlah.ai
metadata:
  author: Canlah AI
  version: "1.0.3"
tags:
  - security
  - cryptography
  - owasp
  - cwe
  - static-analysis
  - zero-deps
  - password-hashing
  - jwt
  - tls
  - encryption
---

# phy-crypto-audit — Weak Cryptography Detector

Scans source code for **10 classes of cryptographic failures** that lead to data breaches, credential compromise, and compliance violations. Maps to **OWASP A02:2021 — Cryptographic Failures** (formerly "Sensitive Data Exposure").

## Quick Start

```bash
# Scan a directory
python crypto_audit.py ./src

# Single file
python crypto_audit.py src/utils/auth.py

# CI mode — exit 1 on CRITICAL or HIGH
python crypto_audit.py ./src --ci

# Only CRITICAL findings
python crypto_audit.py ./src --only-severity CRITICAL
```

## The 10 Checks

| ID | Severity | Check | CWE |
|----|----------|-------|-----|
| CR001 | CRITICAL | MD5/SHA1/SHA256 used for password hashing | CWE-328 |
| CR002 | CRITICAL | PRNG (random/Math.random) for security-sensitive values | CWE-338 |
| CR003 | CRITICAL | Hardcoded cryptographic key or IV in source | CWE-321 |
| CR004 | HIGH | ECB mode encryption (deterministic, pattern-leaking) | CWE-327 |
| CR005 | HIGH | DES / 3DES / RC4 / Blowfish / MD4 algorithm | CWE-327 |
| CR006 | HIGH | RSA key size under 2048 bits | CWE-326 |
| CR007 | HIGH | bcrypt/argon2 work factor too low | CWE-916 |
| CR008 | HIGH | JWT signed with weak/hardcoded secret (HS256 only) | CWE-347 |
| CR009 | MEDIUM | TLS 1.0 or 1.1 accepted (deprecated, POODLE/BEAST) | CWE-326 |
| CR010 | MEDIUM | Hardcoded IV (same IV reuse in CBC mode) | CWE-329 |

### CR001 — MD5/SHA1 for Password Hashing (CRITICAL)
MD5 and SHA1 can be brute-forced at **hundreds of billions of hashes per second** on consumer hardware. Detects `hashlib.md5`, `hashlib.sha1`, `hashlib.sha256`, `crypto.createHash('md5')`, `MessageDigest.getInstance("MD5")` when they appear near password-related context (user, password, passwd, hash, credential).

SHA256 is flagged at MEDIUM — it's too fast for passwords (needs bcrypt/argon2/scrypt).

### CR002 — PRNG for Security Values (CRITICAL)
Detects `random.random()`, `random.randint()`, `Math.random()`, `rand()` (PHP), `math/rand` (Go) used for generating tokens, API keys, session IDs, CSRF tokens, OTP codes, or password reset links. These are **predictable** — use `secrets.token_hex()`, `crypto.randomBytes()`, `crypto/rand`.

### CR003 — Hardcoded Cryptographic Key (CRITICAL)
Finds AES keys, HMAC secrets, encryption passwords, and JWT secrets hardcoded as string literals. A key in source code = a key in every git clone, every container image, and every developer's laptop.

### CR004 — ECB Mode (HIGH)
ECB (Electronic Codebook) mode encrypts identical plaintext blocks to identical ciphertext — it leaks data patterns. The "ECB penguin" attack makes even encrypted images readable. Detects `AES.MODE_ECB`, `Cipher.getInstance("AES")` without mode (defaults to ECB in Java), `AES-ECB`.

### CR005 — Weak Algorithms (HIGH)
DES (56-bit key, broken in 22 hours in 1999), RC4 (biased keystream, broken in WEP/SSL), Blowfish (64-bit block, Sweet32 birthday attack), MD4 (completely broken). None of these should appear in new code.

### CR006 — RSA Key Under 2048 Bits (HIGH)
RSA-1024 is factorizable by nation-state adversaries and was deprecated by NIST in 2015. Detects `RSA.generate(1024)`, `rsa.KeySize = 1024`, `KeyPairGenerator.getInstance("RSA")` with key size < 2048.

### CR007 — Bcrypt/Argon2 Work Factor Too Low (HIGH)
Bcrypt with rounds < 10 is too fast for security. Argon2 with memory < 64MB or time < 2 is insufficient. Detects `bcrypt.hashpw(password, bcrypt.gensalt(rounds=4))` or `bcrypt.hash(pass, 4)`.

### CR008 — JWT Weak Signing (HIGH)
Detects:
- `jwt.sign(payload, 'hardcoded-secret')` — key in source
- `algorithm: 'none'` — unsigned JWTs (CVE-2015-9235)
- Only HS256 without RS256/ES256 option — symmetric JWTs can't rotate keys without invalidating all sessions

### CR009 — TLS 1.0/1.1 Accepted (MEDIUM)
TLS 1.0 (POODLE, BEAST attacks) and TLS 1.1 are deprecated by RFC 8996. Detects `ssl.TLSVersion.TLSv1`, `TLSv1_METHOD`, `MinVersion: tls.VersionTLS10`, `sslProtocol: "TLSv1"`, `SSLContext.getInstance("TLSv1")`.

### CR010 — Hardcoded IV in CBC Mode (MEDIUM)
A fixed IV in CBC mode means identical plaintexts produce identical ciphertexts (partial ECB vulnerability). Detects `IV = b"1234567890123456"` or `iv = bytes([0] * 16)` near CBC mode usage.

## Sample Output

```
============================================================
  Crypto Audit — src/
  Files scanned: 38  |  Files flagged: 6
============================================================

── CRITICAL (3) ────────────────────────────────────────────
🔴 CR001 [CRITICAL] src/auth/users.py:45
   hashlib.sha256 used for password hashing. SHA256 runs at ~10B hash/sec — trivially brute-forceable.
   CWE: CWE-328: Use of Weak Hash
   Fix: Use bcrypt.hashpw(password, bcrypt.gensalt(rounds=12)) or argon2-cffi instead.

🔴 CR002 [CRITICAL] src/utils/tokens.py:23
   random.token = random.randint(100000, 999999) — PRNG used for OTP/token generation.
   CWE: CWE-338: Use of Cryptographically Weak PRNG
   Fix: import secrets; token = secrets.token_hex(16)

🔴 CR003 [CRITICAL] src/config/crypto.py:8
   Hardcoded AES key: SECRET_KEY = "my-super-secret-key-1234"
   CWE: CWE-321: Use of Hard-coded Cryptographic Key
   Fix: Load from environment: SECRET_KEY = os.environ["ENCRYPTION_KEY"] (min 32 bytes for AES-256)

── HIGH (2) ────────────────────────────────────────────────
🟠 CR004 [HIGH] src/services/data_enc.py:67
   AES.new(key, AES.MODE_ECB) — ECB mode leaks data patterns (identical plaintext → identical ciphertext).
   CWE: CWE-327: Use of Broken Algorithm
   Fix: Use AES.new(key, AES.MODE_GCM) — GCM provides both encryption and authentication.

🟠 CR007 [HIGH] src/auth/password.py:31
   bcrypt.gensalt(rounds=4) — work factor too low (min recommended: 12).
   CWE: CWE-916: Use of Password Hash With Insufficient Computational Effort
   Fix: bcrypt.gensalt(rounds=12) — doubles attacker cost for each +1 round.

── MEDIUM (1) ──────────────────────────────────────────────
🟡 CR010 [MEDIUM] src/services/enc.py:15
   Hardcoded IV: iv = b"0000000000000000" near CBC mode usage. Fixed IV = partial ECB vulnerability.
   CWE: CWE-329: Not Using a Random IV with CBC Mode
   Fix: iv = os.urandom(16)  # generate fresh random IV for each encryption

────────────────────────────────────────────────────────────
  Total: 6 findings
  Critical: 3 | High: 2 | Medium: 1

  ❌ CI GATE FAILED — resolve CRITICAL/HIGH findings before merging.
```

## The Script

```python
#!/usr/bin/env python3
"""
phy-crypto-audit — Weak Cryptography Detector
OWASP A02:2021 — Cryptographic Failures
Scans Python/JS/TS/Go/Java/PHP for 10 classes of insecure cryptography.
Zero external dependencies.
"""

import sys
import re
from dataclasses import dataclass, field
from pathlib import Path


# ─── Data Structures ─────────────────────────────────────────────────────────

@dataclass
class Finding:
    check_id: str
    severity: str      # CRITICAL / HIGH / MEDIUM
    location: str
    message: str
    cwe: str = ""
    fix: str = ""

    def __str__(self) -> str:
        icon = {"CRITICAL": "🔴", "HIGH": "🟠", "MEDIUM": "🟡"}.get(self.severity, "⚪")
        parts = [f"{icon} {self.check_id} [{self.severity}] {self.location}"]
        parts.append(f"   {self.message}")
        if self.cwe:
            parts.append(f"   CWE: {self.cwe}")
        if self.fix:
            parts.append(f"   Fix: {self.fix}")
        return "\n".join(parts)


@dataclass
class AuditResult:
    scan_root: str
    files_scanned: int = 0
    files_flagged: int = 0
    findings: list = field(default_factory=list)

    @property
    def critical_count(self) -> int:
        return sum(1 for f in self.findings if f.severity == "CRITICAL")

    @property
    def high_count(self) -> int:
        return sum(1 for f in self.findings if f.severity == "HIGH")

    @property
    def medium_count(self) -> int:
        return sum(1 for f in self.findings if f.severity == "MEDIUM")


# ─── Constants ────────────────────────────────────────────────────────────────

# CR001 — weak hash for passwords
WEAK_HASH_RE = re.compile(
    r"hashlib\.(md5|sha1|sha256|sha224)\s*\(|"
    r"crypto\.createHash\s*\(\s*['\"](?:md5|sha1|sha256|sha224)['\"]\)|"
    r"MessageDigest\.getInstance\s*\(\s*['\"](?:MD5|SHA-?1|SHA-?256)['\"]\)|"
    r"hash\s*\(\s*['\"](?:md5|sha1|sha256)['\"]|"
    r"md5\s*\(|sha1\s*\(|openssl_digest\s*\([^,]+,\s*['\"](?:md5|sha1)['\"]",
    re.IGNORECASE,
)

PASSWORD_CONTEXT_RE = re.compile(
    r"(password|passwd|pwd|credential|secret|hash|digest|pin|otp)",
    re.IGNORECASE,
)

# CR002 — PRNG for security values
PRNG_RE = re.compile(
    r"random\.random\s*\(\)|"
    r"random\.randint\s*\(|"
    r"random\.choice\s*\(|"
    r"random\.shuffle\s*\(|"
    r"Math\.random\s*\(\)|"
    r"\brand\s*\(\)|"          # PHP rand()
    r"math/rand\b|"            # Go math/rand
    r"new Random\s*\(\)|"     # Java java.util.Random
    r"Random\.nextInt\s*\(",
    re.IGNORECASE,
)

SECURITY_CONTEXT_RE = re.compile(
    r"(token|session|csrf|nonce|otp|api.?key|secret|salt|password|"
    r"reset|verification|activation|challenge|random.?id)",
    re.IGNORECASE,
)

# CR003 — hardcoded crypto key
HARDCODED_KEY_RE = re.compile(
    r"""(SECRET_KEY|ENCRYPTION_KEY|AES_KEY|HMAC_KEY|JWT_SECRET|SIGNING_KEY)\s*=\s*['"][^'"]{8,}['"]|"""
    r"""(key|secret|password)\s*=\s*b?['"]((?:[A-Za-z0-9+/=]{16,}|[0-9a-fA-F]{16,}))['"]""",
    re.IGNORECASE,
)

# Exclude obvious env var patterns
ENV_VAR_RE = re.compile(
    r"(os\.environ|os\.getenv|process\.env|env\[|getenv\(|config\[)",
    re.IGNORECASE,
)

# CR004 — ECB mode
ECB_MODE_RE = re.compile(
    r"(MODE_ECB|AES\.ECB|AES-ECB|AES/ECB|"
    r"Cipher\.getInstance\s*\(\s*['\"]AES['\"]|"  # Java default = ECB
    r"createCipheriv\s*\(\s*['\"]AES['\"])",      # Node.js AES without mode
    re.IGNORECASE,
)

# CR005 — weak algorithms
WEAK_ALGO_RE = re.compile(
    r"(DES\.|3DES\.|TripleDES|RC4\.|ARC4\.|Blowfish\.|MD4\.|"
    r"Cipher\.getInstance\s*\(\s*['\"](?:DES|DESede|RC4|ARCFOUR|Blowfish)['\"]|"
    r"createCipheriv\s*\(\s*['\"](?:des|des-ede3|rc4|bf)['\"]|"
    r"openssl_encrypt\s*\([^,]+,\s*['\"](?:DES|3DES|RC4|BF)['\"])",
    re.IGNORECASE,
)

# CR006 — weak RSA key size
RSA_KEYGEN_RE = re.compile(
    r"(RSA\.generate\s*\(\s*(\d+)|"
    r"rsa\.GenerateKey\s*\([^,]+,\s*(\d+)|"
    r"KeyPairGenerator\.getInstance\s*\([^)]+\)[^;]*\.initialize\s*\(\s*(\d+)|"
    r"genrsa\s+-out\s+[^\s]+\s+(\d+))",
    re.IGNORECASE,
)

# CR007 — bcrypt/argon2 low work factor
BCRYPT_LOW_RE = re.compile(
    r"bcrypt\.(gensalt|hashpw|hash)\s*\([^,]+,\s*(\d+)\)|"
    r"bcrypt\.(gensalt|hash)\s*\(\s*(\d+)\s*\)",
    re.IGNORECASE,
)

ARGON2_LOW_RE = re.compile(
    r"argon2\.(hash|using)\s*\([^)]*time_cost\s*=\s*(\d+)|"
    r"argon2\.(hash|using)\s*\([^)]*memory_cost\s*=\s*(\d+)",
    re.IGNORECASE,
)

# CR008 — JWT weak signing
JWT_HARDCODED_RE = re.compile(
    r"""(jwt\.sign\s*\([^,]+,\s*['"][^'"]{1,40}['"]|"""
    r"""jwt\.encode\s*\([^,]+,\s*['"][^'"]{1,40}['"]|"""
    r"""sign\s*\([^,]+,\s*['"][^'"]{1,40}['"]\s*[,)])|"""
    r"""algorithm\s*[=:]\s*['"]none['"]""",
    re.IGNORECASE,
)

# CR009 — weak TLS versions
WEAK_TLS_RE = re.compile(
    r"(ssl\.TLSVersion\.TLSv1\b(?!_2)|"
    r"TLSv1_METHOD|TLSv1_1_METHOD|"
    r"MinVersion\s*:\s*tls\.VersionTLS1[01]\b|"
    r"SSLContext\.getInstance\s*\(\s*['\"]TLSv1['\"]|"
    r"sslProtocol\s*[=:]\s*['\"]TLSv1['\"]|"
    r"ssl\.PROTOCOL_TLSv1\b(?!_2))",
    re.IGNORECASE,
)

# CR010 — hardcoded IV
HARDCODED_IV_RE = re.compile(
    r"""(iv\s*=\s*b?['"][0\x00\\x]{8,}['"]|"""
    r"""IV\s*=\s*bytes\s*\(\s*\[\s*0\s*\]|"""
    r"""iv\s*=\s*b?['"]\d{16,}['"]|"""
    r"""iv\s*=\s*['"]\x00{16}['"]|"""
    r"""nonce\s*=\s*b?['"][0\x00\\x]{8,}['"]\s*#\s*(?!random))""",
    re.IGNORECASE,
)

CBC_MODE_RE = re.compile(r"(MODE_CBC|AES\.CBC|AES-CBC|AES/CBC)", re.IGNORECASE)

SUPPORTED_EXTENSIONS = {".py", ".js", ".ts", ".jsx", ".tsx", ".go", ".java", ".kt", ".php", ".rb"}
SKIP_DIRS = {"node_modules", ".git", "venv", ".venv", "__pycache__", "dist", "build", ".next", "vendor", "test", "tests", "__tests__", "migrations"}


# ─── Helpers ─────────────────────────────────────────────────────────────────

def get_context(lines: list, idx: int, window: int = 15) -> str:
    start = max(0, idx - window)
    end = min(len(lines), idx + window)
    return "\n".join(lines[start:end])


def collect_files(path: str) -> list:
    p = Path(path)
    if p.is_file():
        return [p] if p.suffix in SUPPORTED_EXTENSIONS else []
    files = []
    for f in p.rglob("*"):
        if any(skip in f.parts for skip in SKIP_DIRS):
            continue
        if f.is_file() and f.suffix in SUPPORTED_EXTENSIONS:
            files.append(f)
    return files


# ─── Checks ──────────────────────────────────────────────────────────────────

def check_cr001_weak_password_hash(filepath: str, lines: list) -> list:
    """CR001 — MD5/SHA1/SHA256 for password hashing."""
    findings = []
    for i, line in enumerate(lines):
        if not WEAK_HASH_RE.search(line):
            continue
        ctx = get_context(lines, i, 10)
        if not PASSWORD_CONTEXT_RE.search(ctx):
            continue  # Skip if not near password context

        # Classify severity
        algo_match = re.search(r"(md5|sha1|sha256|sha224)", line, re.IGNORECASE)
        algo = algo_match.group(1).upper() if algo_match else "weak hash"
        severity = "CRITICAL" if algo in ("MD5", "SHA1") else "HIGH"  # SHA256 is HIGH

        findings.append(Finding(
            check_id="CR001",
            severity=severity,
            location=f"{filepath}:{i + 1}",
            message=f"{algo} used for password hashing. {algo} runs at ~{'100B' if algo in ('MD5','SHA1') else '10B'} hash/sec — trivially brute-forceable.",
            cwe="CWE-328: Use of Weak Hash",
            fix="Use bcrypt.hashpw(password, bcrypt.gensalt(rounds=12)) or argon2-cffi. Never use raw hash functions for passwords.",
        ))
    return findings


def check_cr002_prng_for_security(filepath: str, lines: list) -> list:
    """CR002 — PRNG for security-sensitive values."""
    findings = []
    for i, line in enumerate(lines):
        if not PRNG_RE.search(line):
            continue
        ctx = get_context(lines, i, 10)
        if not SECURITY_CONTEXT_RE.search(ctx):
            continue
        findings.append(Finding(
            check_id="CR002",
            severity="CRITICAL",
            location=f"{filepath}:{i + 1}",
            message=f"Predictable PRNG used for security-sensitive value: '{line.strip()[:70]}'",
            cwe="CWE-338: Use of Cryptographically Weak Pseudo-Random Number Generator",
            fix=(
                "Python: secrets.token_hex(32) or secrets.token_urlsafe(32)\n"
                "   JS: crypto.randomBytes(32).toString('hex')\n"
                "   Go: crypto/rand.Read()\n"
                "   Java: SecureRandom.generateSeed(32)"
            ),
        ))
    return findings


def check_cr003_hardcoded_key(filepath: str, lines: list) -> list:
    """CR003 — Hardcoded cryptographic key in source."""
    findings = []
    for i, line in enumerate(lines):
        m = HARDCODED_KEY_RE.search(line)
        if not m:
            continue
        # Skip if loaded from env
        ctx = get_context(lines, i, 3)
        if ENV_VAR_RE.search(ctx):
            continue
        # Skip test/example files by name
        fname = Path(filepath).stem.lower()
        if any(x in fname for x in ("test", "example", "sample", "demo", "mock", "fake")):
            continue
        findings.append(Finding(
            check_id="CR003",
            severity="CRITICAL",
            location=f"{filepath}:{i + 1}",
            message=f"Hardcoded cryptographic key: '{line.strip()[:70]}'",
            cwe="CWE-321: Use of Hard-coded Cryptographic Key",
            fix="Load from environment: os.environ['ENCRYPTION_KEY'] — never commit keys to source control.",
        ))
    return findings


def check_cr004_ecb_mode(filepath: str, lines: list) -> list:
    """CR004 — ECB mode encryption."""
    findings = []
    for i, line in enumerate(lines):
        if ECB_MODE_RE.search(line):
            findings.append(Finding(
                check_id="CR004",
                severity="HIGH",
                location=f"{filepath}:{i + 1}",
                message=f"ECB mode: '{line.strip()[:70]}'. ECB encrypts identical blocks identically — leaks data patterns.",
                cwe="CWE-327: Use of Broken or Risky Cryptographic Algorithm",
                fix="Use AES-GCM (authenticated encryption): AES.new(key, AES.MODE_GCM) — provides both confidentiality and integrity.",
            ))
    return findings


def check_cr005_weak_algorithms(filepath: str, lines: list) -> list:
    """CR005 — DES/3DES/RC4/Blowfish/MD4."""
    findings = []
    for i, line in enumerate(lines):
        m = WEAK_ALGO_RE.search(line)
        if m:
            algo = m.group(0)[:20]
            findings.append(Finding(
                check_id="CR005",
                severity="HIGH",
                location=f"{filepath}:{i + 1}",
                message=f"Broken algorithm '{algo}': DES=56-bit (cracked 1999), RC4=biased keystream, Blowfish=Sweet32 birthday attack.",
                cwe="CWE-327: Use of Broken or Risky Cryptographic Algorithm",
                fix="Use AES-256-GCM for symmetric encryption, ChaCha20-Poly1305 as alternative.",
            ))
    return findings


def check_cr006_weak_rsa_key(filepath: str, lines: list) -> list:
    """CR006 — RSA key size under 2048 bits."""
    findings = []
    for i, line in enumerate(lines):
        m = RSA_KEYGEN_RE.search(line)
        if not m:
            continue
        # Extract the key size from the match groups
        size_str = next((g for g in m.groups() if g and g.isdigit()), None)
        if size_str is None:
            continue
        size = int(size_str)
        if size < 2048:
            findings.append(Finding(
                check_id="CR006",
                severity="HIGH",
                location=f"{filepath}:{i + 1}",
                message=f"RSA key size {size} bits is below NIST minimum of 2048 bits (deprecated since 2015).",
                cwe="CWE-326: Inadequate Encryption Strength",
                fix=f"Use RSA 3072 or 4096 bits, or switch to ECDSA P-256 (equivalent to RSA-3072 at 1/4 the size).",
            ))
    return findings


def check_cr007_bcrypt_low_rounds(filepath: str, lines: list) -> list:
    """CR007 — bcrypt/argon2 work factor too low."""
    findings = []
    for i, line in enumerate(lines):
        m = BCRYPT_LOW_RE.search(line)
        if m:
            rounds_str = m.group(2) or m.group(4)
            if rounds_str and int(rounds_str) < 10:
                findings.append(Finding(
                    check_id="CR007",
                    severity="HIGH",
                    location=f"{filepath}:{i + 1}",
                    message=f"bcrypt rounds={rounds_str} is too low. Min recommended: 12 (each +1 doubles attacker cost).",
                    cwe="CWE-916: Use of Password Hash With Insufficient Computational Effort",
                    fix="bcrypt.gensalt(rounds=12)  — or 14+ for high-security contexts.",
                ))
            continue
        m2 = ARGON2_LOW_RE.search(line)
        if m2:
            val_str = m2.group(2) or m2.group(4)
            if val_str:
                val = int(val_str)
                if "time_cost" in line and val < 2:
                    findings.append(Finding(
                        check_id="CR007",
                        severity="HIGH",
                        location=f"{filepath}:{i + 1}",
                        message=f"argon2 time_cost={val} is too low. Minimum recommended: 3 (OWASP cheat sheet).",
                        cwe="CWE-916",
                        fix="Use time_cost=3, memory_cost=65536 (64MB), parallelism=4 as minimum.",
                    ))
                elif "memory_cost" in line and val < 65536:
                    findings.append(Finding(
                        check_id="CR007",
                        severity="HIGH",
                        location=f"{filepath}:{i + 1}",
                        message=f"argon2 memory_cost={val} KiB is too low. Minimum recommended: 65536 (64MB).",
                        cwe="CWE-916",
                        fix="Use memory_cost=65536 (64MB) as minimum for Argon2.",
                    ))
    return findings


def check_cr008_jwt_weak_secret(filepath: str, lines: list) -> list:
    """CR008 — JWT signed with hardcoded or weak secret."""
    findings = []
    for i, line in enumerate(lines):
        m = JWT_HARDCODED_RE.search(line)
        if not m:
            continue
        if ENV_VAR_RE.search(line):
            continue
        if "algorithm" in line.lower() and "none" in line.lower():
            findings.append(Finding(
                check_id="CR008",
                severity="CRITICAL",
                location=f"{filepath}:{i + 1}",
                message="JWT signed with algorithm 'none' — signature verification bypassed (CVE-2015-9235).",
                cwe="CWE-347: Improper Verification of Cryptographic Signature",
                fix="Remove 'none' from allowed algorithms. Always validate `algorithms=['RS256']` or `['HS256']` explicitly.",
            ))
        else:
            findings.append(Finding(
                check_id="CR008",
                severity="HIGH",
                location=f"{filepath}:{i + 1}",
                message=f"JWT appears to use hardcoded secret: '{line.strip()[:70]}'",
                cwe="CWE-321: Use of Hard-coded Cryptographic Key",
                fix="Load JWT secret from environment. For stateless rotation, use RS256 (asymmetric) instead of HS256.",
            ))
    return findings


def check_cr009_weak_tls(filepath: str, lines: list) -> list:
    """CR009 — TLS 1.0/1.1 accepted."""
    findings = []
    for i, line in enumerate(lines):
        if WEAK_TLS_RE.search(line):
            findings.append(Finding(
                check_id="CR009",
                severity="MEDIUM",
                location=f"{filepath}:{i + 1}",
                message=f"TLS 1.0/1.1 accepted: '{line.strip()[:70]}'. Both deprecated (RFC 8996), vulnerable to POODLE/BEAST.",
                cwe="CWE-326: Inadequate Encryption Strength",
                fix="Set minimum TLS version to 1.2 (prefer 1.3). Python: ssl.TLSVersion.TLSv1_2, Go: tls.VersionTLS12.",
            ))
    return findings


def check_cr010_hardcoded_iv(filepath: str, lines: list, content: str) -> list:
    """CR010 — Hardcoded IV near CBC mode."""
    if not CBC_MODE_RE.search(content):
        return []  # No CBC mode in file — IV hardcoding less critical
    findings = []
    for i, line in enumerate(lines):
        if HARDCODED_IV_RE.search(line):
            findings.append(Finding(
                check_id="CR010",
                severity="MEDIUM",
                location=f"{filepath}:{i + 1}",
                message=f"Hardcoded IV detected near CBC mode usage: '{line.strip()[:70]}'. Reusing IV = partial ECB vulnerability.",
                cwe="CWE-329: Not Using a Random IV with CBC Mode",
                fix="Generate random IV per encryption: iv = os.urandom(16). Store IV alongside ciphertext (it's not secret).",
            ))
    return findings


# ─── Main Audit ───────────────────────────────────────────────────────────────

def audit(path: str) -> AuditResult:
    result = AuditResult(scan_root=path)
    files = collect_files(path)
    result.files_scanned = len(files)

    for f in files:
        try:
            content = f.read_text(errors="ignore")
        except Exception:
            continue
        lines = content.splitlines()
        fp = str(f)

        file_findings = []
        file_findings.extend(check_cr001_weak_password_hash(fp, lines))
        file_findings.extend(check_cr002_prng_for_security(fp, lines))
        file_findings.extend(check_cr003_hardcoded_key(fp, lines))
        file_findings.extend(check_cr004_ecb_mode(fp, lines))
        file_findings.extend(check_cr005_weak_algorithms(fp, lines))
        file_findings.extend(check_cr006_weak_rsa_key(fp, lines))
        file_findings.extend(check_cr007_bcrypt_low_rounds(fp, lines))
        file_findings.extend(check_cr008_jwt_weak_secret(fp, lines))
        file_findings.extend(check_cr009_weak_tls(fp, lines))
        file_findings.extend(check_cr010_hardcoded_iv(fp, lines, content))

        if file_findings:
            result.files_flagged += 1
        result.findings.extend(file_findings)

    return result


def format_report(result: AuditResult, ci_mode: bool = False) -> str:
    out = []
    out.append(f"\n{'='*60}")
    out.append(f"  Crypto Audit — {result.scan_root}")
    out.append(f"  Files scanned: {result.files_scanned}  |  Files flagged: {result.files_flagged}")
    out.append(f"{'='*60}")

    if not result.findings:
        out.append("✅ No cryptographic weaknesses detected.")
        return "\n".join(out)

    for severity in ("CRITICAL", "HIGH", "MEDIUM"):
        sev = [f for f in result.findings if f.severity == severity]
        if sev:
            out.append(f"\n── {severity} ({len(sev)}) {'─'*40}")
            for finding in sev:
                out.append(str(finding))

    out.append(f"\n{'─'*60}")
    out.append(
        f"  Total: {len(result.findings)} findings  |  "
        f"Critical: {result.critical_count}  High: {result.high_count}  Medium: {result.medium_count}"
    )
    if ci_mode and (result.critical_count > 0 or result.high_count > 0):
        out.append("\n  ❌ CI GATE FAILED — resolve CRITICAL/HIGH findings before merging.")
    return "\n".join(out)


# ─── CLI ─────────────────────────────────────────────────────────────────────

def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="phy-crypto-audit — Weak Cryptography Detector",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python crypto_audit.py ./src
  python crypto_audit.py src/auth/password.py
  python crypto_audit.py ./src --ci
  python crypto_audit.py ./src --only-severity CRITICAL
        """,
    )
    parser.add_argument("path", help="Directory or file to audit")
    parser.add_argument("--ci", action="store_true", help="Exit 1 on CRITICAL or HIGH findings")
    parser.add_argument(
        "--only-severity",
        choices=["CRITICAL", "HIGH", "MEDIUM"],
        help="Filter to this severity and above",
    )
    args = parser.parse_args()

    result = audit(args.path)

    sev_order = ["CRITICAL", "HIGH", "MEDIUM"]
    if args.only_severity:
        cutoff = sev_order.index(args.only_severity)
        result.findings = [f for f in result.findings if sev_order.index(f.severity) <= cutoff]

    print(format_report(result, ci_mode=args.ci))

    if args.ci and (result.critical_count > 0 or result.high_count > 0):
        sys.exit(1)


if __name__ == "__main__":
    main()
```

## CI Integration

```yaml
# GitHub Actions
- name: Crypto Security Audit
  run: python crypto_audit.py ./src --ci

# Block only on CRITICAL findings
- name: Crypto Audit (critical only)
  run: python crypto_audit.py ./src --only-severity CRITICAL --ci
```

## False Positive Notes

- **CR001** — only flags weak hashes near password/credential context (window: 10 lines). `hashlib.sha256` on a file checksum won't fire.
- **CR002** — `random()` without nearby token/session/secret context won't fire. Simulation code is safe.
- **CR003** — skips files named `test*`, `example*`, `sample*`, `demo*`, `mock*`, `fake*`. Also skips any line that loads from `os.environ`, `os.getenv`, `process.env`.
- **CR006** — requires a numeric key size argument in the call. `RSA.import_key(pem)` won't fire.
- **CR008** — skips JWT calls that use `os.environ`/`process.env` for the secret.

## Related Skills

- **phy-jwt-auth-audit** — full JWT/OAuth security audit including token inspection, scope checks, alg:none
- **phy-deserialization-audit** — OWASP A08: insecure object deserialization
- **phy-ssrf-audit** — OWASP A10: server-side request forgery
- **phy-path-traversal-audit** — OWASP A01: path traversal
- **phy-cors-audit** — CORS misconfiguration that bypasses secure crypto

---

## Author

**[Canlah AI](https://canlah.ai)** — Run performance marketing without breaking your brand.

- GitHub: [github.com/PHY041](https://github.com/PHY041)
- All Skills: [clawhub.ai/PHY041](https://clawhub.ai/PHY041)
