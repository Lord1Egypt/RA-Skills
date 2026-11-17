#!/usr/bin/env python3
"""Directory & File Brute-Forcing Module for GKN-Phantom (v3.0.0).

Advanced directory and file discovery engine with intelligent response
analysis, custom-404 detection, recursive probing, and technology-aware
wordlist prioritization.

Capabilities:
  1. Smart Embedded Wordlists — 10 curated categories (GENERAL, ADMIN,
     BACKUP, API, CONFIG, UPLOAD, LOGS, EXPOSED, SHELL, BACKEND_TECH)
     totalling 100+ common paths.
  2. Extension-Based Discovery — Appends 19 common extensions (.php,
     .asp, .jsp, .json, .xml, .bak, etc.) to each path entry.
  3. Rate Limiting — Configurable RPS (default 5) with automatic
     exponential backoff on 429 / connection errors.
  4. Response Analysis — Content-length filtering, status-code
     categorization, content-type tracking, SimHash fuzzy similarity.
  5. Recursive Discovery — Optional: when a directory is confirmed,
     probe one level deeper with the same wordlist.
  6. Technology-Aware — Accepts a technology-stack fingerprint to
     reorder wordlist priority (WordPress → wp-* first, Java →
     WEB-INF/* first, etc.).
  7. Smart Filtering — Auto-detect custom 404 pages via baseline
     probing + SimHash similarity comparison.

Usage (CLI):
  python directory_fuzzer.py --url https://target.com --wordlist general,admin,backup
  python directory_fuzzer.py --url https://target.com --wordlist all --extensions php,asp,aspx --depth 2 --rps 5
  python directory_fuzzer.py --url https://target.com --wordlist all --tech wordpress,php --depth 1
  python directory_fuzzer.py --batch targets.json --mode quick
  python directory_fuzzer.py --batch targets.json --mode normal
  python directory_fuzzer.py --batch targets.json --mode deep

Output: structured JSON with discovered paths grouped by status code,
including response size, content-type, redirect location, and baseline
similarity score.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import ssl
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from collections import defaultdict
from dataclasses import dataclass, field
from typing import Any

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from utils import load_json, dump_json

# =============================================================================
# Embedded Wordlists — curated paths organized by category
# =============================================================================

WORDLISTS: dict[str, list[str]] = {
    "GENERAL": [
        "robots.txt",
        "sitemap.xml",
        "crossdomain.xml",
        ".htaccess",
        ".env",
        ".git/config",
        ".svn/entries",
        "web.config",
        "server-status",
        "server-info",
    ],
    "ADMIN": [
        "admin",
        "administrator",
        "backend",
        "panel",
        "manage",
        "login",
        "cms",
        "wp-admin",
        "administrator/index.php",
    ],
    "BACKUP": [
        "backup",
        "bak",
        "old",
        "test",
        "dev",
        "staging",
        "temp",
        "tmp",
        ".bak",
        ".old",
        ".swp",
        "~",
        ".save",
        ".orig",
    ],
    "API": [
        "api",
        "api/v1",
        "api/v2",
        "graphql",
        "gql",
        "swagger",
        "swagger-ui",
        "api-docs",
        "v2/api-docs",
        "v3/api-docs",
        "openapi.json",
    ],
    "CONFIG": [
        "config",
        "configuration",
        "settings",
        ".env",
        ".env.backup",
        ".env.local",
        ".env.production",
        "app.config",
        "web.config",
        "config.php",
        "config.inc",
        "wp-config.php",
        "database.yml",
        "settings.py",
    ],
    "UPLOAD": [
        "upload",
        "uploads",
        "files",
        "attachments",
        "images",
        "img",
        "assets",
        "static",
        "media",
        "resources",
        "storage",
    ],
    "LOGS": [
        "logs",
        "log",
        "error",
        "error_log",
        "debug",
        "trace",
        "stacktrace",
        "phpinfo",
        "info",
        "status",
        "health",
        "metrics",
    ],
    "EXPOSED": [
        ".DS_Store",
        ".idea",
        ".vscode",
        ".gitignore",
        "package.json",
        "composer.json",
        "Gemfile",
        "requirements.txt",
        "Dockerfile",
        "docker-compose.yml",
        "Makefile",
        "README.md",
        "CHANGELOG.md",
        "LICENSE",
    ],
    "SHELL": [
        "cmd",
        "shell",
        "exec",
        "console",
        "terminal",
        "phpmyadmin",
        "adminer",
        "pma",
        "db",
        "database",
        "sql",
        "mysql",
    ],
    "BACKEND_TECH": [
        "actuator",
        "actuator/health",
        "actuator/env",
        "actuator/mappings",
        "druid/index.html",
        "/jmx",
        "/jolokia",
        "/heapdump",
        "/threaddump",
    ],
}

# Canonical name mapping for category aliases
CATEGORY_ALIASES: dict[str, str] = {
    "general": "GENERAL",
    "admin": "ADMIN",
    "backup": "BACKUP",
    "api": "API",
    "config": "CONFIG",
    "upload": "UPLOAD",
    "uploads": "UPLOAD",
    "logs": "LOGS",
    "log": "LOGS",
    "exposed": "EXPOSED",
    "shell": "SHELL",
    "backend_tech": "BACKEND_TECH",
    "backend": "BACKEND_TECH",
}

# =============================================================================
# Extensions for file discovery
# =============================================================================

EXTENSIONS: list[str] = [
    ".php",
    ".asp",
    ".aspx",
    ".jsp",
    ".do",
    ".action",
    ".html",
    ".htm",
    ".json",
    ".xml",
    ".txt",
    ".pdf",
    ".zip",
    ".tar.gz",
    ".sql",
    ".bak",
    ".old",
    ".orig",
    ".inc",
    ".conf",
]

# =============================================================================
# Technology-Aware Priority Paths
# =============================================================================

TECH_PRIORITY_PATHS: dict[str, list[str]] = {
    "wordpress": [
        "wp-admin",
        "wp-login.php",
        "wp-content",
        "wp-includes",
        "wp-config.php",
        "wp-cron.php",
        "wp-json",
        "xmlrpc.php",
        "wp-trackback.php",
        "wp-signup.php",
    ],
    "php": [
        "phpinfo.php",
        "phpmyadmin",
        "config.php",
        "admin.php",
        "upload.php",
        "install.php",
        "setup.php",
        "info.php",
    ],
    "java": [
        "WEB-INF/web.xml",
        "WEB-INF/classes",
        "META-INF",
        "actuator",
        "actuator/health",
        "actuator/env",
        "actuator/mappings",
        "/jmx",
        "/jolokia",
        "struts",
        "spring",
    ],
    "spring": [
        "actuator",
        "actuator/health",
        "actuator/env",
        "actuator/mappings",
        "actuator/heapdump",
        "actuator/threaddump",
        "swagger-ui.html",
        "v2/api-docs",
        "v3/api-docs",
    ],
    "dotnet": [
        "web.config",
        "app.config",
        "elmah.axd",
        "trace.axd",
        "aspnet_client",
        "bin",
        "App_Data",
        "App_Code",
    ],
    "iis": [
        "web.config",
        "iisstart.htm",
        "trace.axd",
        "aspnet_client",
    ],
    "apache": [
        "server-status",
        "server-info",
        ".htaccess",
        ".htpasswd",
        "cgi-bin",
        "icons",
        "manual",
    ],
    "tomcat": [
        "manager/html",
        "host-manager/html",
        "examples",
        "docs",
        "WEB-INF/web.xml",
        "META-INF/context.xml",
    ],
    "nginx": [
        "nginx_status",
        "nginx-stub-status",
        ".nginx.conf",
    ],
    "django": [
        "admin",
        "api",
        "static",
        "media",
        "settings.py",
        "database.yml",
    ],
    "flask": [
        "admin",
        "api",
        "static",
        "config.py",
        "debug",
        "console",
    ],
    "nodejs": [
        "package.json",
        "node_modules",
        ".npmrc",
        ".env",
        "package-lock.json",
    ],
    "react": [
        "package.json",
        "node_modules",
        "static",
        "asset-manifest.json",
        "service-worker.js",
    ],
    "angular": [
        "package.json",
        "node_modules",
        "assets",
        "environments",
        "angular.json",
    ],
    "laravel": [
        ".env",
        "storage",
        "vendor",
        "composer.json",
        "artisan",
        "public",
        "resources",
    ],
    "drupal": [
        "user/login",
        "admin",
        "node",
        "sites/default",
        "sites/default/settings.php",
        "modules",
        "themes",
    ],
    "joomla": [
        "administrator",
        "components",
        "modules",
        "templates",
        "configuration.php",
        "plugins",
    ],
}

# =============================================================================
# Mode configurations (--batch --mode)
# =============================================================================

MODE_CONFIGS: dict[str, dict[str, Any]] = {
    "quick": {
        "categories": ["GENERAL", "ADMIN"],
        "extensions": [],
        "depth": 0,
        "rps": 10,
        "description": "Fast scan: GENERAL + ADMIN wordlists, no extensions, no recursion",
    },
    "normal": {
        "categories": ["GENERAL", "ADMIN", "API", "CONFIG", "BACKEND_TECH"],
        "extensions": [".php", ".asp", ".aspx", ".jsp", ".html", ".json", ".xml", ".txt", ".bak", ".old"],
        "depth": 1,
        "rps": 5,
        "description": "Balanced scan: 5 categories, common extensions, 1 level recursion",
    },
    "deep": {
        "categories": [
            "GENERAL", "ADMIN", "BACKUP", "API", "CONFIG", "UPLOAD",
            "LOGS", "EXPOSED", "SHELL", "BACKEND_TECH",
        ],
        "extensions": EXTENSIONS,
        "depth": 2,
        "rps": 3,
        "description": "Thorough scan: all categories, all extensions, 2 levels recursion",
    },
}

# =============================================================================
# SimHash — lightweight fuzzy hashing for response similarity
# =============================================================================

def simhash(text: str, hash_bits: int = 64) -> int:
    """Compute a SimHash fingerprint of *text* for near-duplicate detection.

    Tokenises the input into character trigrams, hashes each token, and
    aggregates the weighted bit-vectors.  Returns a *hash_bits*-bit integer
    whose Hamming distance from another SimHash approximates the cosine
    distance between the original documents.

    Standard-library only; no external dependencies.
    """
    if not text:
        return 0

    # Use character trigrams as features (robust to small edits)
    tokens = [text[i : i + 3] for i in range(len(text) - 2)]
    if not tokens:
        tokens = [text]

    vector = [0] * hash_bits

    for token in tokens:
        digest = hashlib.md5(token.encode("utf-8", errors="replace")).hexdigest()
        h = int(digest, 16)
        for i in range(hash_bits):
            if h & (1 << i):
                vector[i] += 1
            else:
                vector[i] -= 1

    result = 0
    for i in range(hash_bits):
        if vector[i] > 0:
            result |= 1 << i

    return result


def hamming_distance(a: int, b: int) -> int:
    """Return the Hamming distance between two SimHash integers."""
    return (a ^ b).bit_count()


def normalized_body_hash(body: str) -> str:
    """Return SHA-256 of a whitespace-stripped, lowercased body for exact
    duplicate detection."""
    normalized = re.sub(r"\s+", " ", body).strip().lower()
    return hashlib.sha256(normalized.encode("utf-8", errors="replace")).hexdigest()


# =============================================================================
# Data Classes
# =============================================================================

@dataclass
class FuzzResult:
    """A single path probing result."""

    path: str
    url: str
    status_code: int
    content_length: int
    content_type: str
    redirect_location: str
    body_hash: str
    simhash_val: int
    baseline_similarity: float
    is_directory: bool
    is_custom_404: bool
    error: str


@dataclass
class ScanResult:
    """Aggregate result for one target."""

    target: str
    wordlists: list[str]
    extensions: list[str]
    depth: int
    rps: float
    mode: str
    tech_stack: list[str]
    total_requests: int
    duration_seconds: float
    baseline_404_size: int
    baseline_404_hash: str
    custom_404_detected: bool
    results: dict[str, list[dict[str, Any]]]
    directories_found: list[str]
    summary: dict[str, int]


# =============================================================================
# Directory Fuzzer Engine
# =============================================================================

class DirectoryFuzzer:
    """Advanced directory and file brute-forcing engine.

    Parameters
    ----------
    config : dict
        Configuration dictionary with keys:
        - target: str (base URL)
        - wordlists: list[str] (category names)
        - extensions: list[str] (file extensions)
        - depth: int (recursion depth)
        - rps: float (requests per second)
        - timeout: float (request timeout in seconds)
        - user_agent: str
        - tech_stack: list[str]
        - no_verify_ssl: bool
        - verbose: bool
    """

    def __init__(self, config: dict[str, Any]) -> None:
        self.target: str = self._normalize_base_url(config.get("target", ""))
        self.wordlist_categories: list[str] = config.get("wordlists", ["GENERAL", "ADMIN"])
        self.extensions: list[str] = config.get("extensions", [])
        self.depth: int = int(config.get("depth", 1))
        self.rps: float = float(config.get("rps", 5.0))
        self.timeout: float = float(config.get("timeout", 10.0))
        self.user_agent: str = config.get(
            "user_agent",
            "GKN-Phantom/3.0 DirectoryFuzzer",
        )
        self.tech_stack: list[str] = config.get("tech_stack", [])
        self.no_verify_ssl: bool = bool(config.get("no_verify_ssl", False))
        self.verbose: bool = bool(config.get("verbose", False))

        # Internal state
        self._last_request_time: float = 0.0
        self._backoff_multiplier: float = 1.0
        self._baseline_404_size: int | None = None
        self._baseline_404_simhash: int | None = None
        self._baseline_404_hash: str = ""
        self._opener: urllib.request.OpenerDirector | None = None
        self._seen_urls: set[str] = set()
        self._wordlist: list[str] = []

        # Build the wordlist once
        self._build_wordlist()

    # ---- URL helpers -----------------------------------------------------------

    @staticmethod
    def _normalize_base_url(url: str) -> str:
        """Ensure the base URL ends with a single '/'."""
        url = url.strip().rstrip("/")
        if not url.startswith(("http://", "https://")):
            url = "https://" + url
        return url + "/"

    @staticmethod
    def _join_url(base: str, path: str) -> str:
        """Join a relative *path* to *base*, preserving the path structure."""
        base_parsed = urllib.parse.urlparse(base)
        # Clean leading slashes/dots from path
        path = path.lstrip("/")
        full_path = base_parsed.path.rstrip("/") + "/" + path
        # Rebuild URL with normalized path
        result = urllib.parse.urlunparse(
            (
                base_parsed.scheme,
                base_parsed.netloc,
                full_path,
                base_parsed.params,
                base_parsed.query,
                base_parsed.fragment,
            )
        )
        return result

    # ---- HTTP ----------------------------------------------------------------

    def _build_opener(self) -> urllib.request.OpenerDirector:
        """Create a urllib opener that does NOT follow redirects and optionally
        skips SSL verification."""

        class _NoRedirectHandler(urllib.request.HTTPRedirectHandler):
            def redirect_request(self, req, fp, code, msg, headers, newurl):
                return None

            # Map all redirect status codes
            http_error_301 = redirect_request   # type: ignore[assignment]
            http_error_302 = redirect_request   # type: ignore[assignment]
            http_error_303 = redirect_request   # type: ignore[assignment]
            http_error_307 = redirect_request   # type: ignore[assignment]
            http_error_308 = redirect_request   # type: ignore[assignment]

        handlers: list[Any] = [_NoRedirectHandler()]

        if self.no_verify_ssl:
            ctx = ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE
            handlers.append(urllib.request.HTTPSHandler(context=ctx))

        opener = urllib.request.OpenerDirector()
        for h in handlers:
            opener.add_handler(h)
        # Add default handlers not overridden
        opener.add_handler(urllib.request.ProxyHandler())
        opener.add_handler(urllib.request.UnknownHandler())
        opener.add_handler(urllib.request.HTTPHandler())
        opener.add_handler(urllib.request.HTTPDefaultErrorHandler())
        opener.add_handler(urllib.request.HTTPErrorProcessor())
        if not self.no_verify_ssl:
            opener.add_handler(urllib.request.HTTPSHandler())

        return opener

    def _make_request(self, url: str) -> dict[str, Any]:
        """Perform a single HTTP GET and return response metadata.

        Never raises — all errors are captured in the returned dict.
        """
        result: dict[str, Any] = {
            "status_code": 0,
            "content_length": 0,
            "content_type": "",
            "redirect_location": "",
            "body": "",
            "error": "",
        }

        if self._opener is None:
            self._opener = self._build_opener()

        req = urllib.request.Request(url)
        req.add_header("User-Agent", self.user_agent)
        req.add_header("Accept", "*/*")

        try:
            resp = self._opener.open(req, timeout=self.timeout)
            result["status_code"] = resp.getcode() or 0
            result["content_type"] = resp.headers.get("Content-Type", "")
            result["redirect_location"] = resp.headers.get("Location", "")

            # Read body (cap at 256 KB to avoid memory issues on large files)
            body = resp.read(256 * 1024)
            try:
                body_str = body.decode("utf-8", errors="replace")
            except Exception:
                body_str = body.decode("latin-1", errors="replace")
            result["body"] = body_str
            result["content_length"] = len(body)

        except urllib.error.HTTPError as e:
            result["status_code"] = e.code
            result["content_type"] = e.headers.get("Content-Type", "") if hasattr(e, "headers") else ""
            body = e.read() if hasattr(e, "read") else b""
            try:
                result["body"] = body.decode("utf-8", errors="replace")
            except Exception:
                result["body"] = body.decode("latin-1", errors="replace")
            result["content_length"] = len(body)
            # For 3xx with an HTTPError (rare), capture Location
            if hasattr(e, "headers"):
                result["redirect_location"] = e.headers.get("Location", "")

        except urllib.error.URLError as e:
            result["error"] = str(e.reason) if hasattr(e, "reason") else str(e)

        except (TimeoutError, OSError) as e:
            result["error"] = str(e)

        except Exception as e:
            result["error"] = f"{type(e).__name__}: {e}"

        return result

    # ---- Rate limiting ---------------------------------------------------------

    def _apply_rate_limit(self) -> None:
        """Block until it is safe to send the next request."""
        interval = 1.0 / (self.rps * max(self._backoff_multiplier, 0.1))
        elapsed = time.monotonic() - self._last_request_time
        if elapsed < interval:
            time.sleep(interval - elapsed)
        self._last_request_time = time.monotonic()

    def _adjust_backoff(self, result: dict[str, Any]) -> None:
        """Increase backoff on server stress signals; decay otherwise."""
        if result["error"] or result["status_code"] in (429, 503):
            self._backoff_multiplier = min(self._backoff_multiplier * 2.0, 16.0)
            if self.verbose:
                print(
                    f"[backoff] multiplier={self._backoff_multiplier:.1f}x  "
                    f"status={result['status_code']} error={result['error']}",
                    file=sys.stderr,
                )
        else:
            # Gradually decay
            if self._backoff_multiplier > 1.0:
                self._backoff_multiplier = max(self._backoff_multiplier * 0.95, 1.0)

    # ---- Wordlist construction -------------------------------------------------

    def _build_wordlist(self) -> None:
        """Assemble the path wordlist from selected categories, optionally
        reordered by technology stack."""
        paths: list[str] = []

        # Gather from selected categories
        for cat in self.wordlist_categories:
            resolved = CATEGORY_ALIASES.get(cat.lower(), cat.upper())
            entries = WORDLISTS.get(resolved, WORDLISTS.get(cat.upper(), []))
            paths.extend(entries)

        # Deduplicate while preserving order
        seen: set[str] = set()
        unique: list[str] = []
        for p in paths:
            p_clean = p.strip().lstrip("/")
            if p_clean and p_clean not in seen:
                seen.add(p_clean)
                unique.append(p_clean)
        paths = unique

        # Prioritise technology-specific paths
        if self.tech_stack:
            paths = self._prioritize_for_tech(paths)

        self._wordlist = paths

    def _prioritize_for_tech(self, paths: list[str]) -> list[str]:
        """Prepend technology-specific priority paths to the front of the
        wordlist while deduplicating."""
        priority: list[str] = []
        for tech in self.tech_stack:
            tech_lower = tech.lower()
            for tech_key, tech_paths in TECH_PRIORITY_PATHS.items():
                if tech_lower in tech_key or tech_key in tech_lower:
                    for tp in tech_paths:
                        tp_clean = tp.strip().lstrip("/")
                        if tp_clean and tp_clean not in priority:
                            priority.append(tp_clean)

        # Remove priority entries from the main list (they'll be prepended)
        priority_set = set(priority)
        remaining = [p for p in paths if p not in priority_set]

        return priority + remaining

    # ---- Response analysis -----------------------------------------------------

    def _is_directory_listing(self, body: str) -> bool:
        """Heuristic check: does *body* look like a directory listing?"""
        if not body:
            return False
        indicators = [
            "<title>Index of ",
            "Index of /",
            "Parent Directory</a>",
            "[DIR]",
            "Directory Listing For",
            "<h1>Directory: ",
            "To Parent Directory</a>",
            "<a href=\"/\">",
        ]
        body_lower = body.lower()
        score = sum(1 for ind in indicators if ind.lower() in body_lower)
        # Also check for multiple <a href> links to non-parent entries
        link_count = len(re.findall(r'<a\s+href="[^"]*"[^>]*>', body, re.IGNORECASE))
        if link_count >= 5:
            score += 1
        return score >= 2

    def _guess_content_type_dir(self, status_code: int, content_type: str, body: str) -> bool:
        """Return True if this response is likely a browsable directory."""
        if status_code in (301, 302, 307, 308):
            return True
        if status_code == 200 and self._is_directory_listing(body):
            return True
        return False

    # ---- Custom 404 detection --------------------------------------------------

    def _probe_baseline_404(self) -> None:
        """Request a guaranteed-nonexistent path to establish a 404 baseline."""
        probe_url = self._join_url(self.target, f"PTSKILLTEST-nonexistent-{os.urandom(4).hex()}")
        result = self._make_request(probe_url)

        self._baseline_404_size = result["content_length"]
        self._baseline_404_hash = normalized_body_hash(result["body"])
        self._baseline_404_simhash = simhash(result["body"]) if result["body"] else None

        if self.verbose:
            print(
                f"[baseline] 404 probe → status={result['status_code']} "
                f"size={self._baseline_404_size} hash={self._baseline_404_hash[:12]}...",
                file=sys.stderr,
            )

    def _is_custom_404(
        self, status_code: int, content_length: int, body: str
    ) -> tuple[bool, float]:
        """Return (is_custom_404, similarity_score) for a response.

        A page is flagged as a custom 404 when:
          - It returns 200 (or 301/302 to an error page) BUT
          - Its content-length matches the known 404 baseline, OR
          - Its SimHash is very close to the 404 baseline (Hamming <= 8).
        """
        if self._baseline_404_size is None or self._baseline_404_simhash is None:
            return False, 0.0

        similarity = 0.0

        # Exact content-length match (strong signal)
        if content_length == self._baseline_404_size and status_code == 200:
            similarity = max(similarity, 0.85)

        # SimHash comparison
        if body:
            body_sh = simhash(body)
            dist = hamming_distance(body_sh, self._baseline_404_simhash)
            # Hamming distance 0-3: nearly identical; 4-8: very similar
            sh_similarity = max(0.0, 1.0 - dist / 32.0)
            similarity = max(similarity, sh_similarity)

            # Exact normalized body hash match
            if normalized_body_hash(body) == self._baseline_404_hash:
                similarity = 1.0

        is_custom = similarity >= 0.75
        return is_custom, similarity

    # ---- Core fuzzing logic ----------------------------------------------------

    def _probe_path(self, base_url: str, path: str) -> FuzzResult | None:
        """Probe a single path relative to *base_url*. Returns None if skipped."""
        url = self._join_url(base_url, path)

        # Skip duplicates
        if url in self._seen_urls:
            return None
        self._seen_urls.add(url)

        # Rate limit
        self._apply_rate_limit()

        # Request
        raw = self._make_request(url)
        self._adjust_backoff(raw)

        # Analyze
        status = raw["status_code"]
        content_len = raw["content_length"]
        content_type = raw["content_type"]
        redirect = raw["redirect_location"]
        body = raw["body"]
        error = raw["error"]

        body_hash = normalized_body_hash(body)
        sh = simhash(body)

        is_custom_404, similarity = self._is_custom_404(status, content_len, body)
        is_dir = self._guess_content_type_dir(status, content_type, body)

        return FuzzResult(
            path=path,
            url=url,
            status_code=status,
            content_length=content_len,
            content_type=content_type,
            redirect_location=redirect,
            body_hash=body_hash,
            simhash_val=sh,
            baseline_similarity=round(similarity, 4),
            is_directory=is_dir,
            is_custom_404=is_custom_404,
            error=error,
        )

    def fuzz(self) -> ScanResult:
        """Execute the full directory fuzzing scan against the target.

        Returns a ScanResult with all discoveries grouped by status code.
        """
        start_time = time.monotonic()

        if self.verbose:
            print(
                f"[fuzz] target={self.target}  wordlists={self.wordlist_categories}  "
                f"extensions={self.extensions}  depth={self.depth}  rps={self.rps}  "
                f"tech={self.tech_stack}",
                file=sys.stderr,
            )

        # Establish 404 baseline first
        self._probe_baseline_404()

        # Collect all results
        all_results: list[FuzzResult] = []
        directories_found: list[str] = []

        # Initial probe at depth 0
        queue: list[tuple[str, int]] = [(self.target, 0)]
        probed_dirs: set[str] = set()

        total_requests = 0

        while queue:
            base_url, current_depth = queue.pop(0)

            # Normalize
            base_url = base_url.rstrip("/") + "/"
            if base_url in probed_dirs:
                continue
            probed_dirs.add(base_url)

            for entry in self._wordlist:
                # --- Probe the bare path ---
                fr = self._probe_path(base_url, entry)
                if fr is not None:
                    total_requests += 1
                    # Skip results that are likely custom 404s
                    if not fr.is_custom_404:
                        all_results.append(fr)

                    if fr.is_directory and not fr.is_custom_404:
                        dir_path = base_url.rstrip("/") + "/" + entry.lstrip("/")
                        directories_found.append(dir_path)

                        # Enqueue for recursive probing
                        if current_depth < self.depth:
                            queue.append((dir_path, current_depth + 1))

                    if self.verbose and not fr.is_custom_404:
                        self._log_result(fr)

                # --- Probe with extensions ---
                for ext in self.extensions:
                    ext_entry = entry + ext
                    fr_ext = self._probe_path(base_url, ext_entry)
                    if fr_ext is not None:
                        total_requests += 1
                        if not fr_ext.is_custom_404:
                            all_results.append(fr_ext)

                        if fr_ext.is_directory and not fr_ext.is_custom_404:
                            dir_path = base_url.rstrip("/") + "/" + ext_entry.lstrip("/")
                            directories_found.append(dir_path)
                            if current_depth < self.depth:
                                queue.append((dir_path, current_depth + 1))

                        if self.verbose and not fr_ext.is_custom_404:
                            self._log_result(fr_ext)

        # Group results by status code
        grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)

        for fr in all_results:
            result_dict = {
                "path": fr.path,
                "url": fr.url,
                "status_code": fr.status_code,
                "content_length": fr.content_length,
                "content_type": fr.content_type,
                "redirect_location": fr.redirect_location,
                "baseline_similarity": fr.baseline_similarity,
                "is_directory": fr.is_directory,
            }
            if fr.error:
                result_dict["error"] = fr.error

            if 200 <= fr.status_code < 300:
                grouped["2xx"].append(result_dict)
            elif 300 <= fr.status_code < 400:
                grouped["3xx"].append(result_dict)
            elif fr.status_code == 401:
                grouped["401"].append(result_dict)
            elif fr.status_code == 403:
                grouped["403"].append(result_dict)
            elif fr.status_code == 404:
                grouped["404"].append(result_dict)
            elif 400 <= fr.status_code < 500:
                grouped["4xx_other"].append(result_dict)
            elif 500 <= fr.status_code < 600:
                grouped["5xx"].append(result_dict)
            else:
                grouped["error"].append(result_dict)

        duration = round(time.monotonic() - start_time, 2)

        # Summary
        summary = {
            "total_found": len(all_results),
            "total_2xx": len(grouped.get("2xx", [])),
            "total_3xx": len(grouped.get("3xx", [])),
            "total_protected": len(grouped.get("401", [])) + len(grouped.get("403", [])),
            "total_errors": len(grouped.get("5xx", [])) + len(grouped.get("error", [])),
            "directories": len(directories_found),
            "files": len(
                [r for r in all_results if not r.is_directory and r.status_code == 200]
            ),
        }

        return ScanResult(
            target=self.target,
            wordlists=self.wordlist_categories,
            extensions=self.extensions,
            depth=self.depth,
            rps=self.rps,
            mode="custom",
            tech_stack=self.tech_stack,
            total_requests=total_requests,
            duration_seconds=duration,
            baseline_404_size=self._baseline_404_size or 0,
            baseline_404_hash=self._baseline_404_hash,
            custom_404_detected=self._baseline_404_size is not None,
            results=dict(grouped),
            directories_found=sorted(set(directories_found)),
            summary=summary,
        )

    def _log_result(self, fr: FuzzResult) -> None:
        """Print a one-line result to stderr for verbose mode."""
        label = (
            f"[{fr.status_code}]"
            if fr.status_code
            else "[ERR]"
        )
        size = f"{fr.content_length}B" if fr.content_length else "0B"
        dir_flag = " [DIR]" if fr.is_directory else ""
        sim_flag = f" sim={fr.baseline_similarity:.2f}" if fr.baseline_similarity > 0 else ""
        print(
            f"  {label:>7s} {size:>10s} {fr.content_type[:30]:30s} "
            f"{fr.path}{dir_flag}{sim_flag}",
            file=sys.stderr,
        )


# =============================================================================
# ScanResult serialisation
# =============================================================================

def scan_result_to_dict(sr: ScanResult) -> dict[str, Any]:
    """Convert a ScanResult to a JSON-serialisable dict."""
    return {
        "scan_info": {
            "target": sr.target,
            "wordlists": sr.wordlists,
            "extensions": sr.extensions,
            "depth": sr.depth,
            "rps": sr.rps,
            "mode": sr.mode,
            "tech_stack": sr.tech_stack,
            "total_requests": sr.total_requests,
            "duration_seconds": sr.duration_seconds,
        },
        "baseline": {
            "known_404_size": sr.baseline_404_size,
            "known_404_hash": sr.baseline_404_hash,
            "custom_404_detected": sr.custom_404_detected,
        },
        "results": sr.results,
        "directories_found": sr.directories_found,
        "summary": sr.summary,
    }


# =============================================================================
# Batch runner
# =============================================================================

def run_batch(
    targets: list[str],
    mode: str,
    tech_stack: list[str] | None = None,
    no_verify_ssl: bool = False,
    verbose: bool = False,
) -> dict[str, Any]:
    """Run the fuzzer against a list of targets using a predefined mode.

    Parameters
    ----------
    targets : list[str]
        List of target base URLs.
    mode : str
        One of 'quick', 'normal', 'deep'.
    tech_stack : list[str] | None
        Technology stack hints for wordlist prioritisation.
    no_verify_ssl : bool
        Skip SSL certificate verification.
    verbose : bool
        Print progress to stderr.

    Returns
    -------
    dict
        Aggregated results keyed by target URL.
    """
    mode_cfg = MODE_CONFIGS.get(mode)
    if mode_cfg is None:
        return {"error": f"unknown mode '{mode}'. Choose: quick, normal, deep"}

    all_results: dict[str, Any] = {
        "mode": mode,
        "mode_description": mode_cfg["description"],
        "target_count": len(targets),
        "results": {},
    }

    for target in targets:
        config: dict[str, Any] = {
            "target": target,
            "wordlists": mode_cfg["categories"],
            "extensions": mode_cfg["extensions"],
            "depth": mode_cfg["depth"],
            "rps": mode_cfg["rps"],
            "tech_stack": tech_stack or [],
            "no_verify_ssl": no_verify_ssl,
            "verbose": verbose,
        }

        fuzzer = DirectoryFuzzer(config)
        sr = fuzzer.fuzz()
        all_results["results"][target] = scan_result_to_dict(sr)

    return all_results


# =============================================================================
# CLI
# =============================================================================

def _parse_wordlist_arg(raw: str) -> list[str]:
    """Parse a comma-separated category string. 'all' selects every category."""
    if raw.strip().lower() == "all":
        return list(WORDLISTS.keys())
    categories = [c.strip() for c in raw.split(",") if c.strip()]
    return categories


def _parse_extensions_arg(raw: str) -> list[str]:
    """Parse comma-separated extensions; 'all' selects the default set."""
    if raw.strip().lower() == "all":
        return list(EXTENSIONS)
    exts = [e.strip() for e in raw.split(",") if e.strip()]
    # Ensure dot prefix
    return [e if e.startswith(".") else f".{e}" for e in exts]


def _load_batch_targets(path: str) -> list[str]:
    """Load targets from a JSON file (array of strings or array of {url:...})."""
    data = load_json(path)
    if isinstance(data, list):
        result: list[str] = []
        for item in data:
            if isinstance(item, str):
                result.append(item)
            elif isinstance(item, dict):
                url = item.get("url", item.get("target", ""))
                if url:
                    result.append(url)
        return result
    if isinstance(data, dict):
        urls = data.get("targets", data.get("urls", []))
        if isinstance(urls, list):
            return urls
    return []


def main() -> int:
    ap = argparse.ArgumentParser(
        description="GKN-Phantom Directory & File Brute-Forcer (v3.0.0)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python directory_fuzzer.py --url https://target.com --wordlist general,admin,backup
  python directory_fuzzer.py --url https://target.com --wordlist all --extensions php,asp --depth 2 --rps 5
  python directory_fuzzer.py --url https://target.com --wordlist all --tech wordpress,php
  python directory_fuzzer.py --batch targets.json --mode quick
  python directory_fuzzer.py --batch targets.json --mode deep --tech java,spring
        """,
    )

    ap.add_argument(
        "--url",
        help="Single target base URL (e.g. https://target.com)",
    )
    ap.add_argument(
        "--batch",
        help="Path to a JSON file containing a list of target URLs",
    )
    ap.add_argument(
        "--wordlist",
        default="general,admin",
        help="Comma-separated category names or 'all' (default: general,admin)",
    )
    ap.add_argument(
        "--extensions",
        default="",
        help="Comma-separated extensions or 'all' (default: none)",
    )
    ap.add_argument(
        "--depth",
        type=int,
        default=1,
        help="Recursion depth for directory discovery (default: 1)",
    )
    ap.add_argument(
        "--rps",
        type=float,
        default=5.0,
        help="Maximum requests per second (default: 5)",
    )
    ap.add_argument(
        "--tech",
        default="",
        help="Comma-separated technology stack hints for wordlist priority",
    )
    ap.add_argument(
        "--mode",
        default="",
        choices=["quick", "normal", "deep"],
        help="Predefined scan mode (only with --batch)",
    )
    ap.add_argument(
        "--timeout",
        type=float,
        default=10.0,
        help="Per-request timeout in seconds (default: 10)",
    )
    ap.add_argument(
        "--user-agent",
        default="GKN-Phantom/3.0 DirectoryFuzzer",
        help="Custom User-Agent header",
    )
    ap.add_argument(
        "--no-verify-ssl",
        action="store_true",
        default=False,
        help="Disable SSL certificate verification",
    )
    ap.add_argument(
        "--output",
        "-o",
        default="",
        help="Write JSON output to a file instead of stdout",
    )
    ap.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        default=False,
        help="Print progress to stderr",
    )

    args = ap.parse_args()

    # Validate arguments
    if not args.url and not args.batch:
        print("directory_fuzzer: --url or --batch required", file=sys.stderr)
        return 2

    tech_stack = [t.strip() for t in args.tech.split(",") if t.strip()]

    # ---- Batch mode ----
    if args.batch:
        mode = args.mode or "normal"
        batch_targets = _load_batch_targets(args.batch)
        if not batch_targets:
            print(
                f"directory_fuzzer: no targets found in '{args.batch}'",
                file=sys.stderr,
            )
            return 1

        if args.verbose:
            print(
                f"[batch] mode={mode}  targets={len(batch_targets)}  "
                f"tech={tech_stack}",
                file=sys.stderr,
            )

        result = run_batch(
            targets=batch_targets,
            mode=mode,
            tech_stack=tech_stack,
            no_verify_ssl=args.no_verify_ssl,
            verbose=args.verbose,
        )

        output = dump_json(result)
        if args.output:
            with open(args.output, "w", encoding="utf-8") as fh:
                fh.write(output)
        else:
            print(output)
        return 0 if "error" not in result else 1

    # ---- Single-target mode ----
    wordlists = _parse_wordlist_arg(args.wordlist)
    extensions = _parse_extensions_arg(args.extensions) if args.extensions else []

    config: dict[str, Any] = {
        "target": args.url,
        "wordlists": wordlists,
        "extensions": extensions,
        "depth": args.depth,
        "rps": args.rps,
        "timeout": args.timeout,
        "user_agent": args.user_agent,
        "tech_stack": tech_stack,
        "no_verify_ssl": args.no_verify_ssl,
        "verbose": args.verbose,
    }

    fuzzer = DirectoryFuzzer(config)
    sr = fuzzer.fuzz()
    output = dump_json(scan_result_to_dict(sr))

    if args.output:
        with open(args.output, "w", encoding="utf-8") as fh:
            fh.write(output)
        if args.verbose:
            print(f"[output] written to {args.output}", file=sys.stderr)
    else:
        print(output)

    return 0


if __name__ == "__main__":
    sys.exit(main())
