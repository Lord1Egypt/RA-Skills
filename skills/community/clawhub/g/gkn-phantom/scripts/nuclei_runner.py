#!/usr/bin/env python3
"""Nuclei Integration Module for GKN-Phantom (v3.0.0).

Comprehensive Nuclei template management, smart selection, execution planning,
result parsing, deduplication, and fallback guide generation. Designed to
integrate with the tech_fingerprint.py output for context-aware template
selection.

Capabilities:
  1. Nuclei Detection — auto-detect nuclei binary in PATH (Linux & Windows)
  2. Template Management — scan template directories, build index with
     structured metadata (ID, name, severity, tags, description, CVEs)
  3. Smart Template Selection — match template tags against detected
     technologies from tech_fingerprint output; prioritize by severity
  4. Execution Planning — generate execution plan with estimated time,
     rate limiting, concurrency settings, and target assignment
  5. Result Parsing — parse nuclei JSON output into GKN-Phantom Finding
     schema with severity mapping
  6. Deduplication — deduplicate findings by (template_id, host, matched_at)
  7. Fallback Mode — generate manual scanning guide with template download
     URLs and command examples when nuclei is not installed
  8. Template Validation — validate YAML template syntax and required fields

All operations are deterministic. No external network dependencies beyond
reading local files and running the nuclei binary.

Usage (CLI):
  python nuclei_runner.py --targets targets.json --tech tech_stack.json
  python nuclei_runner.py --targets targets.json --tech tech_stack.json --severity critical,high
  python nuclei_runner.py --check-install
  python nuclei_runner.py --list-templates --tag cve,oast
  python nuclei_runner.py --generate-plan --templates-dir ~/.nuclei-templates/ --tech wordpress,php
  python nuclei_runner.py --output plan.json
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import time
from dataclasses import dataclass, field
from typing import Any

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from utils import load_json, dump_json, utc_now_iso  # noqa: E402

# =============================================================================
# Constants & Defaults
# =============================================================================

DEFAULT_TEMPLATES_DIR_WIN = os.path.expanduser(r"~\nuclei-templates")
DEFAULT_TEMPLATES_DIR_UNIX = os.path.expanduser("~/.nuclei-templates/")
DEFAULT_RATE_LIMIT = 150    # requests per second
DEFAULT_CONCURRENCY = 25    # concurrent templates
DEFAULT_BULK_SIZE = 25      # targets per nuclei invocation

# ---- v5.1 scope limits (fix: unbounded template scope caused timeouts) ----
DEFAULT_MAX_TEMPLATES = 150        # hard cap on templates per execution plan
DEFAULT_TIME_BUDGET_SECONDS = 1800 # total scan time budget (30 min)
DEFAULT_REQUEST_TIMEOUT = 10       # per-request timeout passed to nuclei (-timeout)
DEFAULT_RETRIES = 1                # per-request retries passed to nuclei (-retries)
MIN_TIME_BUDGET_SECONDS = 60
# Tags excluded by default: noisy / slow / high-request-volume categories that
# blow past time budgets. Re-enable with --allow-noisy.
NOISY_TAGS_DEFAULT = ("dos", "fuzz", "intrusive")
VALID_SEVERITIES = {"critical", "high", "medium", "low", "info", "unknown"}
# Default severity scope for execution plans. info/low templates are numerous
# and low-yield; they are opt-in via --severity to keep runs within budget.
PLAN_DEFAULT_SEVERITIES = ["critical", "high", "medium"]

SEVERITY_ORDER = ["critical", "high", "medium", "low", "info", "unknown"]
SEVERITY_WEIGHT: dict[str, int] = {
    "critical": 5, "high": 4, "medium": 3, "low": 2, "info": 1, "unknown": 0,
}

# Official nuclei template GitHub repo
NUCLEI_TEMPLATES_REPO = "https://github.com/projectdiscovery/nuclei-templates.git"
NUCLEI_DOWNLOAD_URL = "https://github.com/projectdiscovery/nuclei/releases"

# Common nuclei binary names
NUCLEI_BINARY_NAMES = ["nuclei", "nuclei.exe"]

# Severity → GKN-Phantom severity mapping
SEVERITY_MAP: dict[str, str] = {
    "critical": "critical",
    "high":     "high",
    "medium":   "medium",
    "low":      "low",
    "info":     "info",
    "unknown":  "low",
}

# Template YAML required top-level fields
TEMPLATE_REQUIRED_FIELDS = ["id", "info"]
TEMPLATE_INFO_REQUIRED_FIELDS = ["name", "author", "severity"]

# Technology → nuclei tag mapping (for smart selection)
TECH_TAG_MAP: dict[str, list[str]] = {
    "nginx":         ["nginx", "nginx-config", "nginx-status"],
    "Apache":        ["apache", "apache-config", "apache-status", "cve-2021-41773", "cve-2021-42013"],
    "IIS":           ["iis", "microsoft", "windows", "asp"],
    "Tomcat":        ["tomcat", "apache", "java", "cve-2020-1938"],
    "Jetty":         ["jetty", "java"],
    "Caddy":         ["caddy"],
    "LiteSpeed":     ["litespeed", "litespeed-cache"],
    "WordPress":     ["wordpress", "wp-plugin", "wp-theme", "wp-login", "xmlrpc"],
    "Drupal":        ["drupal", "drupal-core", "cve-2018-7600", "cve-2019-6340"],
    "Joomla":        ["joomla", "joomla-component"],
    "Magento":       ["magento", "magento2", "adobe-commerce"],
    "Shopify":       ["shopify"],
    "PHP":           ["php", "php-config", "phpinfo", "php-cgi", "phpunit"],
    "ASP.NET":       ["asp", "asp-net", "mvc", "iis", "windows"],
    "Express":       ["express", "nodejs", "node-js"],
    "Django":        ["django", "python", "debug"],
    "Flask":         ["flask", "python", "werkzeug"],
    "Rails":         ["rails", "ruby", "ruby-on-rails"],
    "Laravel":       ["laravel", "lumen", "php", "env-exposure"],
    "Next.js":       ["nextjs", "next-js", "nodejs", "react"],
    "Nuxt.js":       ["nuxtjs", "nuxt-js", "vue"],
    "React":         ["react", "reactjs"],
    "Vue.js":        ["vue", "vuejs"],
    "Angular":       ["angular", "angularjs"],
    "jQuery":        ["jquery"],
    "MySQL":         ["mysql", "sql", "database"],
    "PostgreSQL":    ["postgres", "postgresql", "sql", "database"],
    "MSSQL":         ["mssql", "sql-server", "sql", "database"],
    "MongoDB":       ["mongodb", "nosql", "database"],
    "Redis":         ["redis", "nosql"],
    "Oracle":        ["oracle", "oracle-db", "sql", "database"],
    "Cloudflare":    ["cloudflare", "cdn", "waf"],
    "AWS CloudFront":["cloudfront", "aws", "cdn"],
    "Fastly":        ["fastly", "cdn"],
    "Akamai":        ["akamai", "cdn"],
    "Linux":         ["linux", "unix", "lfi"],
    "Windows":       ["windows", "win", "iis"],
    "Docker":        ["docker", "containers"],
    "Kubernetes":    ["kubernetes", "k8s", "containers"],
    "Jenkins":       ["jenkins", "ci-cd", "devops"],
    "GitLab":        ["gitlab", "ci-cd", "devops"],
    "Grafana":       ["grafana", "monitoring"],
    "Spring Boot":   ["spring", "spring-boot", "java", "actuator"],
    "GraphQL":       ["graphql", "api"],
    "REST":          ["rest", "api", "swagger", "openapi"],
    "WebSocket":     ["websocket", "ws"],
    "S3":            ["aws", "s3", "bucket"],
    "Firebase":      ["firebase", "gcp", "google"],
    "Jira":          ["jira", "atlassian"],
    "Confluence":    ["confluence", "atlassian", "cve-2022-26134"],
    "SharePoint":    ["sharepoint", "microsoft", "office365"],
    "Citrix":        ["citrix", "cve-2019-19781", "cve-2020-8193"],
    "VMware":        ["vmware", "vcenter", "esxi", "cve-2021-21972"],
    "SAP":           ["sap", "netweaver"],
    "ColdFusion":    ["coldfusion", "adobe", "cfm"],
    "DNN":           ["dotnetnuke", "dnn", "asp-net"],
    "Umbraco":       ["umbraco", "cms", "asp-net"],
    "TYPO3":         ["typo3", "cms", "php"],
    "PrestaShop":    ["prestashop", "cms", "php"],
    "OpenCart":      ["opencart", "cms", "php"],
    "Ghost":         ["ghost", "cms", "nodejs"],
    "Symfony":       ["symfony", "php", "framework"],
    "Yii":           ["yii", "php", "framework"],
    "CakePHP":       ["cakephp", "php", "framework"],
    "CodeIgniter":   ["codeigniter", "php", "framework"],
    "Zend":          ["zend", "laminas", "php"],
    "Strapi":        ["strapi", "cms", "nodejs"],
    "Wix":           ["wix"],
    "Squarespace":   ["squarespace"],
    "Bootstrap":     ["bootstrap"],
    "Tailwind CSS":  ["tailwind", "tailwindcss"],
    "Prototype Pollution": ["prototype-pollution", "pp", "javascript"],
}


# =============================================================================
# Dataclasses
# =============================================================================

@dataclass
class TemplateMeta:
    """Metadata for a single nuclei template."""
    id: str
    name: str
    severity: str  # critical | high | medium | low | info
    tags: list[str] = field(default_factory=list)
    description: str = ""
    author: str = ""
    cves: list[str] = field(default_factory=list)
    references: list[str] = field(default_factory=list)
    file_path: str = ""
    protocol: str = ""  # http | dns | tcp | file | ssl | etc.

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "severity": self.severity,
            "tags": self.tags,
            "description": self.description,
            "author": self.author,
            "cves": self.cves,
            "references": self.references,
            "file_path": self.file_path,
            "protocol": self.protocol,
        }

    @property
    def severity_weight(self) -> int:
        return SEVERITY_WEIGHT.get(self.severity.lower(), 0)


@dataclass
class Finding:
    """GKN-Phantom Finding schema mapped from nuclei result."""
    type: str
    target: str
    severity: str
    title: str
    description: str
    evidence: dict[str, Any] = field(default_factory=dict)
    template_id: str = ""
    matched_at: str = ""
    confidence: float = 0.85
    status: str = "detected"
    reproducible: bool = True
    safe_poc: bool = True

    def to_dict(self) -> dict[str, Any]:
        return {
            "type": self.type,
            "target": self.target,
            "severity": self.severity,
            "title": self.title,
            "description": self.description,
            "evidence": self.evidence,
            "template_id": self.template_id,
            "matched_at": self.matched_at,
            "confidence": self.confidence,
            "status": self.status,
            "reproducible": self.reproducible,
            "safe_poc": self.safe_poc,
        }


@dataclass
class ExecutionPlan:
    """A planned nuclei execution (v5.1: scope-limited by default)."""
    nuclei_available: bool
    template_count: int
    target_count: int
    estimated_time_seconds: int
    rate_limit: int
    concurrency: int
    severity_filter: list[str]
    templates: list[TemplateMeta]
    targets: list[str]
    commands: list[str]
    warnings: list[str] = field(default_factory=list)
    # ---- v5.1 scope-limit fields ----
    max_templates: int = DEFAULT_MAX_TEMPLATES
    time_budget_seconds: int = DEFAULT_TIME_BUDGET_SECONDS
    request_timeout: int = DEFAULT_REQUEST_TIMEOUT
    excluded_tags: list[str] = field(default_factory=list)
    removed_template_count: int = 0
    scope_limited: bool = False
    support_files: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "nuclei_available": self.nuclei_available,
            "template_count": self.template_count,
            "target_count": self.target_count,
            "estimated_time_seconds": self.estimated_time_seconds,
            "estimated_time_human": _human_duration(self.estimated_time_seconds),
            "rate_limit": self.rate_limit,
            "concurrency": self.concurrency,
            "severity_filter": self.severity_filter,
            "templates": [t.to_dict() for t in self.templates],
            "targets": self.targets,
            "commands": self.commands,
            "warnings": self.warnings,
            "scope_limits": {
                "max_templates": self.max_templates,
                "time_budget_seconds": self.time_budget_seconds,
                "time_budget_human": _human_duration(self.time_budget_seconds),
                "request_timeout": self.request_timeout,
                "excluded_tags": self.excluded_tags,
                "removed_template_count": self.removed_template_count,
                "scope_limited": self.scope_limited,
            },
            "support_files": self.support_files,
        }


@dataclass
class FallbackGuide:
    """Manual scanning guide when nuclei is not installed."""
    templates: list[TemplateMeta]
    download_url: str
    install_commands: list[str]
    run_examples: list[str]
    notes: list[str]

    def to_dict(self) -> dict[str, Any]:
        return {
            "templates": [t.to_dict() for t in self.templates],
            "download_url": self.download_url,
            "install_commands": self.install_commands,
            "run_examples": self.run_examples,
            "notes": self.notes,
        }


# =============================================================================
# 1. Nuclei Detection
# =============================================================================

def detect_nuclei() -> tuple[bool, str | None, str | None]:
    """Check if nuclei binary is available in PATH.

    Returns:
        (available, binary_path, version_string)
    """
    for name in NUCLEI_BINARY_NAMES:
        path = shutil.which(name)
        if path:
            try:
                proc = subprocess.run(
                    [path, "-version"],
                    capture_output=True, text=True, timeout=10,
                )
                version = proc.stdout.strip() or proc.stderr.strip()
                # Extract version from output like "nuclei v3.1.0" or "[INF] Nuclei Engine v3.1.0"
                m = re.search(r"v?(\d+\.\d+\.\d+)", version)
                ver_str = m.group(1) if m else version[:60]
                return (True, path, ver_str)
            except (subprocess.TimeoutExpired, OSError, FileNotFoundError):
                continue
    return (False, None, None)


def check_nuclei_install(verbose: bool = True) -> dict[str, Any]:
    """Produce a detailed installation check result."""
    available, path, version = detect_nuclei()
    result: dict[str, Any] = {
        "nuclei_available": available,
        "binary_path": path,
        "version": version,
        "timestamp": utc_now_iso(),
    }
    if not available:
        result["suggestions"] = _install_suggestions()
    return result


def _install_suggestions() -> list[str]:
    """Return commands to install nuclei."""
    suggestions = [
        "## Install nuclei",
    ]
    if sys.platform == "win32":
        suggestions.extend([
            "# Option 1: Download binary",
            f"# Visit {NUCLEI_DOWNLOAD_URL}",
            "# Download nuclei_windows_amd64.zip and extract to PATH",
            "",
            "# Option 2: Via go install",
            "go install -v github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest",
        ])
    else:
        suggestions.extend([
            "# Option 1: Direct install (Linux/macOS)",
            "curl -L https://github.com/projectdiscovery/nuclei/releases/latest/download/nuclei_linux_amd64.zip -o nuclei.zip",
            "unzip nuclei.zip && chmod +x nuclei && sudo mv nuclei /usr/local/bin/",
            "",
            "# Option 2: Via go install",
            "go install -v github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest",
            "",
            "# Option 3: Via package manager",
            "brew install nuclei           # macOS",
            "apt install nuclei            # Kali / Parrot",
        ])
    suggestions.extend([
        "",
        "## Install/update templates",
        "nuclei -update-templates",
        f"# or: git clone {NUCLEI_TEMPLATES_REPO}",
    ])
    return suggestions


# =============================================================================
# 2. Template Management
# =============================================================================

def _get_default_templates_dir() -> str:
    """Return the default templates directory for the current platform."""
    if sys.platform == "win32":
        return os.path.join(os.path.expanduser("~"), "nuclei-templates")
    return os.path.expanduser("~/.nuclei-templates/")


def scan_templates(
    templates_dir: str | None = None,
    tag_filter: list[str] | None = None,
    severity_filter: list[str] | None = None,
) -> list[TemplateMeta]:
    """Scan a templates directory and build a template index.

    Args:
        templates_dir: Path to templates directory. Auto-detects if None.
        tag_filter: Only include templates matching at least one tag.
        severity_filter: Only include templates matching severity.

    Returns:
        List of TemplateMeta, sorted by severity weight descending.
    """
    if templates_dir is None:
        templates_dir = _get_default_templates_dir()

    if not os.path.isdir(templates_dir):
        return []

    templates: list[TemplateMeta] = []
    for root, dirs, files in os.walk(templates_dir):
        # Skip .git directory
        dirs[:] = [d for d in dirs if d != ".git"]
        for filename in files:
            if filename.endswith((".yaml", ".yml")):
                filepath = os.path.join(root, filename)
                meta = _parse_template_yaml(filepath)
                if meta is not None:
                    templates.append(meta)

    # Apply tag filter
    if tag_filter:
        tag_set = {t.lower() for t in tag_filter}
        templates = [
            t for t in templates
            if tag_set & {tag.lower() for tag in t.tags}
        ]

    # Apply severity filter
    if severity_filter:
        sev_set = {s.lower() for s in severity_filter}
        templates = [
            t for t in templates
            if t.severity.lower() in sev_set
        ]

    # Sort by severity weight descending, then by name
    templates.sort(key=lambda t: (-t.severity_weight, t.name))
    return templates


def _parse_template_yaml(filepath: str) -> TemplateMeta | None:
    """Parse a single template YAML file into TemplateMeta.

    Uses a lightweight YAML subset parser (pure stdlib) to avoid external
    dependencies.
    """
    try:
        with open(filepath, "r", encoding="utf-8", errors="replace") as fh:
            content = fh.read()
    except (OSError, UnicodeDecodeError):
        return None

    # Parse top-level fields using simple line-based parsing
    # (avoiding full YAML dependency)
    fields = _parse_simple_yaml_top(content)

    template_id = fields.get("id", "")
    if not template_id:
        return None

    info = fields.get("info", {})
    if isinstance(info, dict):
        name = info.get("name", "")
        severity = info.get("severity", "unknown")
        description = info.get("description", "")
        author = info.get("author", "")
        tags_raw = info.get("tags", "")
        references_raw = info.get("reference", [])
        # tags can be string or list
        if isinstance(tags_raw, str):
            tags = [t.strip() for t in tags_raw.split(",") if t.strip()]
        elif isinstance(tags_raw, list):
            tags = [str(t).strip() for t in tags_raw if str(t).strip()]
        else:
            tags = []
        # references
        if isinstance(references_raw, str):
            references = [references_raw]
        elif isinstance(references_raw, list):
            references = [str(r) for r in references_raw]
        else:
            references = []

        # Extract CVEs from tags and references
        cves = _extract_cves(tags, references)
    else:
        name = template_id
        severity = "unknown"
        description = ""
        author = ""
        tags = []
        references = []
        cves = []

    # Determine protocol from the request/network fields
    protocol = ""
    if "http:" in content or "HTTP:" in content or "requests:" in content:
        protocol = "http"
    elif "dns:" in content or "DNS:" in content:
        protocol = "dns"
    elif "tcp:" in content or "TCP:" in content:
        protocol = "tcp"
    elif "ssl:" in content or "SSL:" in content:
        protocol = "ssl"
    elif "file:" in content or "FILE:" in content:
        protocol = "file"
    elif "javascript:" in content or "code:" in content:
        protocol = "code"
    elif "websocket:" in content:
        protocol = "websocket"
    elif "network:" in content:
        protocol = "network"

    return TemplateMeta(
        id=template_id,
        name=name,
        severity=severity.lower(),
        tags=tags,
        description=description,
        author=author,
        cves=cves,
        references=references,
        file_path=filepath,
        protocol=protocol,
    )


# Minimal YAML-like parser for top-level fields
def _parse_simple_yaml_top(content: str) -> dict[str, Any]:
    """Parse top-level key: value pairs from a YAML-like template.

    Designed specifically for nuclei template YAML structure. This is not a
    general-purpose YAML parser but handles the 99% case for nuclei templates.
    """
    result: dict[str, Any] = {}
    # Try to split into top-level sections. This only handles the two most
    # common patterns: `id: <value>` and `info:\n  key: value\n  key: value`
    lines = content.split("\n")

    # Extract `id:` (top-level)
    for line in lines:
        m = re.match(r"^id:\s*(.*)", line)
        if m:
            result["id"] = m.group(1).strip().strip('"').strip("'")
            break

    # Extract `info:` block
    info: dict[str, Any] = {}
    in_info = False
    current_key = ""
    current_val_lines: list[str] = []

    for line in lines:
        if re.match(r"^info:\s*$", line) or re.match(r"^info:", line):
            in_info = True
            continue

        if in_info:
            # Check if we're back to top level (non-indented)
            if line and not line.startswith((" ", "\t")):
                # Flush current key
                if current_key:
                    info[current_key] = _finalize_val(current_key, current_val_lines)
                    current_key = ""
                    current_val_lines = []
                in_info = False
                continue

            # Check for a new key in the info block
            m = re.match(r"^\s{2,}([\w-]+)\s*:\s*(.*)", line)
            if m:
                if current_key:
                    info[current_key] = _finalize_val(current_key, current_val_lines)
                current_key = m.group(1)
                current_val_lines = [m.group(2).strip()]
            elif current_key:
                current_val_lines.append(line.strip())

    # Flush last key
    if current_key and in_info:
        info[current_key] = _finalize_val(current_key, current_val_lines)

    if info:
        result["info"] = info

    return result


def _finalize_val(key: str, val_lines: list[str]) -> Any:
    """Convert collected lines into the appropriate Python type."""
    raw = " ".join(v for v in val_lines if v and v != "|" and v != "|-").strip()

    if key == "tags":
        # Tags format: "tag1,tag2,tag3"
        return raw.strip('"').strip("'")

    if key == "reference":
        # Could be single URL or block list. Return as-is for now.
        if raw.startswith("-"):
            # It's a list
            return [v.strip().lstrip("-").strip() for v in val_lines if v.strip().startswith("-")]
        return raw

    if key == "classification":
        return {}

    return raw.strip('"').strip("'")


def _extract_cves(tags: list[str], references: list[str]) -> list[str]:
    """Extract CVE identifiers from tags and references."""
    cves: list[str] = []
    cve_pattern = re.compile(r"(?:CVE-\d{4}-\d{4,})", re.IGNORECASE)
    for source in tags + references:
        found = cve_pattern.findall(source)
        cves.extend(f.upper() for f in found)
    return sorted(set(cves))


# =============================================================================
# 3. Smart Template Selection
# =============================================================================

def select_templates_by_tech(
    templates: list[TemplateMeta],
    tech_data: dict[str, Any] | None,
    extra_tags: list[str] | None = None,
) -> list[TemplateMeta]:
    """Select templates relevant to detected technologies.

    Matches template tags against technology names from a tech_fingerprint
    output JSON. Falls back to all templates if no tech data is available.

    Args:
        templates: Full list of available templates.
        tech_data: TechFingerprint.to_dict() output from tech_fingerprint.py.
        extra_tags: Additional tag keywords to match.

    Returns:
        Filtered and sorted list of relevant templates.
    """
    if not tech_data:
        return templates

    # Collect all technology names from the fingerprint
    tech_names: set[str] = set()
    for category in ("server", "language", "framework", "cms", "javascript",
                     "cdn", "waf", "database", "os", "platform"):
        for det in tech_data.get(category, []):
            tech_names.add(det.get("name", ""))

    # Also extract tag-like keywords from extra tags
    if extra_tags:
        tech_names.update(extra_tags)

    # Map technology names to nuclei tags
    candidate_tags: set[str] = set()
    for tech_name in tech_names:
        mapped = TECH_TAG_MAP.get(tech_name, [tech_name.lower()])
        candidate_tags.update(t.lower() for t in mapped)

    if not candidate_tags:
        return templates

    # Score each template by tag overlap
    scored: list[tuple[int, TemplateMeta]] = []
    for tmpl in templates:
        tmpl_tags = {t.lower() for t in tmpl.tags}
        overlap = len(candidate_tags & tmpl_tags)
        if overlap > 0:
            # Weighted: overlap count * severity weight
            score = overlap * 10 + tmpl.severity_weight
            scored.append((score, tmpl))

    # Sort by score descending
    scored.sort(key=lambda x: -x[0])
    return [t for _, t in scored]


def select_templates_by_severity(
    templates: list[TemplateMeta],
    severities: list[str],
) -> list[TemplateMeta]:
    """Filter templates by allowed severities."""
    sev_set = {s.lower().strip() for s in severities}
    return [t for t in templates if t.severity.lower() in sev_set]


def select_templates_by_tag(
    templates: list[TemplateMeta],
    tags: list[str],
) -> list[TemplateMeta]:
    """Filter templates by matching tags."""
    tag_set = {t.lower().strip() for t in tags}
    return [
        t for t in templates
        if tag_set & {tag.lower() for tag in t.tags}
    ]


# =============================================================================
# 4. Execution Planning
# =============================================================================

def generate_execution_plan(
    templates: list[TemplateMeta],
    targets: list[str],
    rate_limit: int = DEFAULT_RATE_LIMIT,
    concurrency: int = DEFAULT_CONCURRENCY,
    severity_filter: list[str] | None = None,
) -> ExecutionPlan:
    """Generate a nuclei execution plan.

    Estimates time based on template count, target count, rate limit, and
    assumes ~2 HTTP requests per template on average.
    """
    nuclei_ok, binary_path, version = detect_nuclei()

    if severity_filter:
        sev_set = {s.lower() for s in severity_filter}
        templates = [t for t in templates if t.severity.lower() in sev_set]

    # Estimate time: templates * targets * avg_requests_per_template / rate_limit
    avg_requests = 2.0  # conservative average requests per template
    total_requests = len(templates) * len(targets) * avg_requests
    efficient_requests = total_requests / concurrency
    estimated_seconds = int(efficient_requests / (rate_limit if rate_limit > 0 else 1))

    # Build commands
    commands = _build_nuclei_commands(
        templates, targets, rate_limit, concurrency, binary_path or "nuclei"
    )

    warnings: list[str] = []
    if not nuclei_ok:
        warnings.append("nuclei binary not found in PATH — fallback to manual mode")
    if len(templates) > 500:
        warnings.append(f"Large template count ({len(templates)}). Consider narrowing by severity or tags.")
    if len(targets) * len(templates) > 10000:
        warnings.append("High total request count (>10k). Increase rate_limit for faster scans.")
    if estimated_seconds > 3600:
        warnings.append(f"Estimated scan time exceeds 1 hour ({_human_duration(estimated_seconds)}).")

    return ExecutionPlan(
        nuclei_available=nuclei_ok,
        template_count=len(templates),
        target_count=len(targets),
        estimated_time_seconds=estimated_seconds,
        rate_limit=rate_limit,
        concurrency=concurrency,
        severity_filter=severity_filter or [],
        templates=templates,
        targets=targets,
        commands=commands,
        warnings=warnings,
    )


def _build_nuclei_commands(
    templates: list[TemplateMeta],
    targets: list[str],
    rate_limit: int,
    concurrency: int,
    binary: str,
) -> list[str]:
    """Build nuclei CLI command strings."""
    commands: list[str] = []

    # Group targets into bulk batches
    for i in range(0, len(targets), DEFAULT_BULK_SIZE):
        batch = targets[i:i + DEFAULT_BULK_SIZE]

        # If we have many templates, reference by tag/severity patterns
        # instead of individual template IDs to keep command length manageable
        if len(templates) <= 50:
            # Include all template IDs
            tids = ",".join(t.id for t in templates)
            template_arg = f"-id {tids}"
        elif len(templates) <= 200:
            # Include only critical/high
            critical_high = [t for t in templates if t.severity in ("critical", "high")]
            if critical_high:
                tids = ",".join(t.id for t in critical_high[:50])
                template_arg = f"-id {tids}"
            else:
                template_arg = "-s critical,high,medium"
        else:
            template_arg = "-s critical,high,medium"

        # Determine tag-based filtering from templates
        tags_set: set[str] = set()
        for t in templates:
            tags_set.update(t.tags[:3])  # top 3 tags per template
        tag_arg = ""
        if tags_set and len(tags_set) <= 20:
            tag_arg = f"-tags {','.join(sorted(tags_set)[:10])}"

        # Build targets
        targets_arg = " ".join(batch)

        cmd_parts = [
            binary,
            "-u", targets_arg,
            "-json",
            "-rl", str(rate_limit),
            "-c", str(concurrency),
            "-timeout", str(DEFAULT_REQUEST_TIMEOUT),
            "-stats",
            "-no-color",
        ]
        if template_arg and "-id" not in cmd_parts:
            cmd_parts.append(template_arg)
        if tag_arg:
            cmd_parts.append(tag_arg)

        commands.append(" ".join(cmd_parts))

    return commands


# =============================================================================
# 5. Result Parsing
# =============================================================================

def parse_nuclei_output(json_lines: str) -> list[Finding]:
    """Parse nuclei JSON line output into GKN-Phantom Finding objects.

    Nuclei outputs one JSON object per line when run with -json flag.

    Args:
        json_lines: Raw nuclei stdout (JSON lines format).

    Returns:
        List of Finding objects.
    """
    findings: list[Finding] = []
    if not json_lines.strip():
        return findings

    for line in json_lines.strip().split("\n"):
        line = line.strip()
        if not line:
            continue
        try:
            entry = json.loads(line)
        except json.JSONDecodeError:
            continue

        finding = _map_nuclei_entry(entry)
        if finding:
            findings.append(finding)

    return findings


def _map_nuclei_entry(entry: dict[str, Any]) -> Finding | None:
    """Map a single nuclei JSON entry to a GKN-Phantom Finding."""
    # Required fields
    template_id = entry.get("template-id", entry.get("templateID", ""))
    if not template_id:
        return None

    info = entry.get("info", {})
    if isinstance(info, dict):
        name = info.get("name", template_id)
        severity = info.get("severity", "unknown")
        description = info.get("description", "")
    else:
        name = template_id
        severity = "unknown"
        description = ""

    matched_at = entry.get("matched-at", entry.get("matched", ""))
    host = entry.get("host", "")
    target = host or matched_at

    # Map severity
    gkn_severity = SEVERITY_MAP.get(severity.lower(), "low")

    # Build evidence
    evidence: dict[str, Any] = {
        "request": entry.get("request", ""),
        "response": entry.get("response", ""),
        "extracted_results": entry.get("extracted-results", entry.get("extracted_results", [])),
        "curl_command": entry.get("curl-command", entry.get("curl_command", "")),
        "ip": entry.get("ip", ""),
        "timestamp": entry.get("timestamp", utc_now_iso()),
    }

    # Determine finding type from template tags/name
    ftype = _classify_finding_type(entry)

    return Finding(
        type=ftype,
        target=target,
        severity=gkn_severity,
        title=name,
        description=description,
        evidence=evidence,
        template_id=template_id,
        matched_at=matched_at,
        confidence=0.85,
        status="detected",
        reproducible=True,
        safe_poc=True,
    )


def _classify_finding_type(entry: dict[str, Any]) -> str:
    """Heuristically determine the GKN-Phantom finding type from nuclei output."""
    info = entry.get("info", {})
    tags_raw = info.get("tags", "") if isinstance(info, dict) else ""
    if isinstance(tags_raw, list):
        tags_raw = ",".join(tags_raw)
    tags = tags_raw.lower()

    type_map: list[tuple[list[str], str]] = [
        (["sqli", "sql-injection", "blind-sqli", "error-sqli", "union-sqli"], "sqli"),
        (["xss", "cross-site-scripting", "reflected-xss", "stored-xss", "dom-xss"], "xss"),
        (["ssrf", "server-side-request-forgery"], "ssrf"),
        (["xxe", "xml-external-entity"], "xxe"),
        (["rce", "remote-code-execution", "command-injection"], "rce"),
        (["lfi", "local-file-inclusion", "path-traversal"], "path_traversal"),
        (["ssti", "server-side-template-injection"], "ssti"),
        (["idor", "insecure-direct-object-reference"], "idor"),
        (["csrf", "cross-site-request-forgery"], "csrf"),
        (["open-redirect", "url-redirect"], "open_redirect"),
        (["file-upload", "unrestricted-file-upload"], "file_upload"),
        (["auth-bypass", "authentication-bypass", "login-bypass"], "auth_bypass"),
        (["exposure", "exposed", "config-exposure", "env-exposure", "backup-files"], "data_exposure"),
        (["misconfig", "misconfiguration", "default-login", "default-credentials"], "misconfig"),
        (["cors", "cors-misconfig"], "cors_misconfig"),
        (["cve", "known-vulnerability"], "known_vuln"),
        (["nosql", "nosql-injection", "mongodb-injection"], "nosql_injection"),
        (["ldap", "ldap-injection"], "ldap_injection"),
        (["crlf", "crlf-injection", "http-splitting"], "crlf_injection"),
        (["subdomain-takeover", "takeover"], "subdomain_takeover"),
        (["cache-poisoning", "web-cache-poisoning"], "cache_poisoning"),
        (["smuggling", "http-request-smuggling"], "http_smuggling"),
        (["prototype-pollution", "pp"], "prototype_pollution"),
        (["jwt", "jwt-attack", "jwt-none-alg"], "jwt_deep_analysis"),
        (["race-condition", "toctou"], "race_condition"),
        (["deserialization", "insecure-deserialization"], "deserialization"),
        (["panel", "login-panel", "admin-panel", "exposed-panel"], "component_exposure"),
        (["phpinfo", "debug", "debug-mode"], "info_leak"),
        (["cgi", "cgi-stdin"], "command_injection"),
    ]

    for keywords, ftype in type_map:
        if any(kw in tags for kw in keywords):
            return ftype

    # Check the name/title too
    name = info.get("name", "") if isinstance(info, dict) else ""
    name_lower = name.lower()
    for keywords, ftype in type_map:
        if any(kw in name_lower for kw in keywords):
            return ftype

    return "generic_vuln"


# =============================================================================
# 6. Deduplication
# =============================================================================

def deduplicate_findings(findings: list[Finding]) -> list[Finding]:
    """Deduplicate findings by (template_id, host, matched_at).

    Uses SHA-256 hash for exact dedup. Keeps the first occurrence.
    """
    seen: set[str] = set()
    deduped: list[Finding] = []

    for f in findings:
        key_parts = [
            f.template_id or "",
            f.target or "",
            f.matched_at or "",
        ]
        key = "|".join(key_parts)
        key_hash = hashlib.sha256(key.encode("utf-8")).hexdigest()

        if key_hash not in seen:
            seen.add(key_hash)
            deduped.append(f)

    return deduped


def _finding_fingerprint(finding: Finding) -> str:
    """Generate a short stable fingerprint for a finding."""
    payload = json.dumps(
        {
            "template_id": finding.template_id,
            "target": finding.target,
            "matched_at": finding.matched_at,
            "type": finding.type,
        },
        sort_keys=True,
        ensure_ascii=False,
    )
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()[:16]


# =============================================================================
# 7. Fallback Mode
# =============================================================================

def generate_fallback_guide(
    templates: list[TemplateMeta],
    targets: list[str],
) -> FallbackGuide:
    """Generate a manual scanning guide when nuclei is not installed.

    Includes template descriptions, download instructions, and ready-to-run
    command examples.
    """
    # Sort by severity for priority
    templates = sorted(templates, key=lambda t: -t.severity_weight)

    install_commands = _install_suggestions()

    run_examples: list[str] = []
    if targets and templates:
        # Example 1: all templates, first target
        example_target = targets[0]
        critical_templates = [t for t in templates if t.severity == "critical"][:3]
        high_templates = [t for t in templates if t.severity == "high"][:3]

        if critical_templates:
            tids = ",".join(t.id for t in critical_templates)
            run_examples.append(
                f"# Run critical templates against {example_target}\n"
                f"nuclei -u {example_target} -id {tids} -json -o results_critical.json"
            )

        if high_templates:
            tids = ",".join(t.id for t in high_templates)
            run_examples.append(
                f"# Run high-severity templates against {example_target}\n"
                f"nuclei -u {example_target} -id {tids} -json -o results_high.json"
            )

        # Bulk scan example
        run_examples.append(
            f"# Scan all {len(targets)} targets with critical+high severity\n"
            f"nuclei -l targets.txt -s critical,high -json -rl 150 -o results.json"
        )

        # Tag-based scan
        tags_set: set[str] = set()
        for t in templates[:50]:
            tags_set.update(t.tags[:2])
        if tags_set:
            top_tags = sorted(tags_set)[:5]
            run_examples.append(
                f"# Scan by relevant tags\n"
                f"nuclei -l targets.txt -tags {','.join(top_tags)} -json -o results_tagged.json"
            )

    notes = [
        "Nuclei binary was not found in PATH on this system.",
        "Install nuclei and download templates, then run the commands below.",
        "The templates listed are the ones most relevant to the detected technology stack.",
        f"Template repo: {NUCLEI_TEMPLATES_REPO}",
        f"Nuclei releases: {NUCLEI_DOWNLOAD_URL}",
        "After installation, run: nuclei -update-templates",
    ]

    return FallbackGuide(
        templates=templates,
        download_url=NUCLEI_TEMPLATES_REPO,
        install_commands=install_commands,
        run_examples=run_examples,
        notes=notes,
    )


# =============================================================================
# 8. Template Validation
# =============================================================================

def validate_template(
    filepath: str,
    strict: bool = True,
) -> tuple[bool, list[str]]:
    """Validate a single nuclei template YAML file.

    Args:
        filepath: Path to the template YAML file.
        strict: If True, check for all recommended fields.

    Returns:
        (valid, list_of_errors)
    """
    errors: list[str] = []

    if not os.path.isfile(filepath):
        return (False, [f"File not found: {filepath}"])

    try:
        with open(filepath, "r", encoding="utf-8", errors="replace") as fh:
            content = fh.read()
    except OSError as e:
        return (False, [f"Cannot read file: {e}"])

    if not content.strip():
        return (False, ["Empty template file"])

    # Check YAML syntax (basic structural checks)
    has_id = bool(re.search(r"^\s*id\s*:", content, re.MULTILINE))
    has_info = bool(re.search(r"^\s*info\s*:", content, re.MULTILINE))
    has_request = bool(
        re.search(r"^\s*requests?\s*:", content, re.MULTILINE) or
        re.search(r"^\s*http\s*:", content, re.MULTILINE) or
        re.search(r"^\s*dns\s*:", content, re.MULTILINE) or
        re.search(r"^\s*tcp\s*:", content, re.MULTILINE) or
        re.search(r"^\s*ssl\s*:", content, re.MULTILINE) or
        re.search(r"^\s*file\s*:", content, re.MULTILINE) or
        re.search(r"^\s*code\s*:", content, re.MULTILINE) or
        re.search(r"^\s*self-contained\s*:", content, re.MULTILINE) or
        re.search(r"^\s*workflows?\s*:", content, re.MULTILINE)
    )

    if not has_id:
        errors.append("Missing required field: 'id'")
    if not has_info:
        errors.append("Missing required field: 'info'")

    if strict and has_info:
        # Check info sub-fields
        info_match = re.search(r"^\s*info\s*:(.*?)(?=^\S|\Z)", content, re.MULTILINE | re.DOTALL)
        if info_match:
            info_block = info_match.group(1)
            if not re.search(r"^\s+name\s*:", info_block, re.MULTILINE):
                errors.append("Missing recommended field: 'info.name'")
            if not re.search(r"^\s+author\s*:", info_block, re.MULTILINE):
                errors.append("Missing recommended field: 'info.author'")
            if not re.search(r"^\s+severity\s*:", info_block, re.MULTILINE):
                errors.append("Missing required field: 'info.severity'")
            else:
                # Validate severity value
                sev_match = re.search(r"^\s+severity\s*:\s*(\S+)", info_block, re.MULTILINE)
                if sev_match:
                    sev = sev_match.group(1).strip().lower()
                    valid_sevs = {"critical", "high", "medium", "low", "info", "unknown"}
                    if sev not in valid_sevs:
                        errors.append(f"Invalid severity '{sev}'. Must be one of: {', '.join(sorted(valid_sevs))}")
            if not re.search(r"^\s+description\s*:", info_block, re.MULTILINE):
                errors.append("Missing recommended field: 'info.description'")

    if strict and not has_request:
        errors.append("No request/network section found — template may not produce matches")

    return (len(errors) == 0, errors)


def validate_templates_batch(templates_dir: str) -> dict[str, Any]:
    """Validate all templates in a directory. Returns summary."""
    if not os.path.isdir(templates_dir):
        return {"error": f"Directory not found: {templates_dir}", "results": []}

    results: list[dict[str, Any]] = []
    valid_count = 0
    invalid_count = 0

    for root, dirs, files in os.walk(templates_dir):
        dirs[:] = [d for d in dirs if d != ".git"]
        for filename in files:
            if filename.endswith((".yaml", ".yml")):
                filepath = os.path.join(root, filename)
                valid, errors = validate_template(filepath, strict=True)
                if valid:
                    valid_count += 1
                else:
                    invalid_count += 1
                    results.append({
                        "file": filepath,
                        "valid": valid,
                        "errors": errors,
                    })

    return {
        "total": valid_count + invalid_count,
        "valid": valid_count,
        "invalid": invalid_count,
        "invalid_details": results,
    }


# =============================================================================
# Helper utilities
# =============================================================================

def _human_duration(seconds: int) -> str:
    """Convert seconds to a human-readable duration string."""
    if seconds < 60:
        return f"{seconds}s"
    if seconds < 3600:
        mins = seconds // 60
        secs = seconds % 60
        return f"{mins}m {secs}s"
    hours = seconds // 3600
    mins = (seconds % 3600) // 60
    return f"{hours}h {mins}m"


def _load_tech_data(source: str | None) -> dict[str, Any] | None:
    """Load tech fingerprint data from a JSON file path or raw JSON string."""
    if not source:
        return None
    try:
        if os.path.isfile(source):
            return load_json(source)
        # Try parsing as inline JSON
        return json.loads(source)
    except (json.JSONDecodeError, FileNotFoundError):
        return None


def _load_targets(source: str) -> list[str]:
    """Load targets from a JSON file or newline-delimited file."""
    if not source:
        return []
    try:
        if os.path.isfile(source):
            data = load_json(source)
            if isinstance(data, list):
                return [str(t) for t in data if t]
            if isinstance(data, dict):
                # Try common keys
                for key in ("targets", "urls", "hosts", "domains"):
                    if key in data:
                        return [str(t) for t in data[key] if t]
                # Single target
                for key in ("target", "url", "host"):
                    if key in data:
                        return [str(data[key])]
            return []
        # Try as comma-separated or newline-separated inline
        cleaned = source.strip()
        if "\n" in cleaned:
            return [l.strip() for l in cleaned.split("\n") if l.strip()]
        return [t.strip() for t in cleaned.split(",") if t.strip()]
    except (json.JSONDecodeError, FileNotFoundError):
        # Treat as comma-separated inline
        return [t.strip() for t in source.split(",") if t.strip()]


# =============================================================================
# CLI
# =============================================================================

def main() -> int:
    ap = argparse.ArgumentParser(
        description="GKN-Phantom Nuclei Integration Module (v3.0)"
    )

    # Mode selection
    ap.add_argument(
        "--targets",
        help="Targets JSON file, comma-separated list, or JSON array string"
    )
    ap.add_argument(
        "--tech",
        help="Technology fingerprint JSON file (from tech_fingerprint.py) or inline JSON"
    )
    ap.add_argument(
        "--check-install", action="store_true",
        help="Check if nuclei is installed and print status"
    )
    ap.add_argument(
        "--list-templates", action="store_true",
        help="List available templates"
    )
    ap.add_argument(
        "--generate-plan", action="store_true",
        help="Generate a nuclei execution plan"
    )
    ap.add_argument(
        "--validate-templates", action="store_true",
        help="Validate template YAML files in the templates directory"
    )
    ap.add_argument(
        "--parse-results",
        help="Parse nuclei JSON output file into GKN-Phantom findings"
    )

    # Options
    ap.add_argument(
        "--templates-dir",
        help="Path to nuclei templates directory (auto-detected if not specified)"
    )
    ap.add_argument(
        "--severity", default="critical,high,medium,low,info",
        help="Severity filter, comma-separated (default: critical,high,medium,low,info)"
    )
    ap.add_argument(
        "--tag",
        help="Filter templates by tags, comma-separated"
    )
    ap.add_argument(
        "--rate-limit", type=int, default=DEFAULT_RATE_LIMIT,
        help=f"Rate limit in requests/second (default: {DEFAULT_RATE_LIMIT})"
    )
    ap.add_argument(
        "--concurrency", type=int, default=DEFAULT_CONCURRENCY,
        help=f"Concurrent templates (default: {DEFAULT_CONCURRENCY})"
    )
    ap.add_argument(
        "--output", "-o",
        help="Output JSON file path (default: stdout)"
    )
    args = ap.parse_args()

    # Parse severities
    severity_filter = [s.strip().lower() for s in args.severity.split(",") if s.strip()]
    tag_filter = [t.strip().lower() for t in (args.tag or "").split(",") if t.strip()] or None

    output: dict[str, Any] = {}
    output_json = ""

    # Mode: check install
    if args.check_install:
        output = check_nuclei_install(verbose=True)
        output_json = dump_json(output)

    # Mode: validate templates
    elif args.validate_templates:
        tdir = args.templates_dir or _get_default_templates_dir()
        output = validate_templates_batch(tdir)
        output_json = dump_json(output)

    # Mode: parse nuclei results
    elif args.parse_results:
        try:
            with open(args.parse_results, "r", encoding="utf-8") as fh:
                raw = fh.read()
        except OSError as e:
            print(f"Error reading results file: {e}", file=sys.stderr)
            return 1
        findings = parse_nuclei_output(raw)
        deduped = deduplicate_findings(findings)
        output = {
            "total_raw": len(findings),
            "total_deduped": len(deduped),
            "findings": [f.to_dict() for f in deduped],
        }
        output_json = dump_json(output)

    # Mode: list templates
    elif args.list_templates:
        tdir = args.templates_dir or _get_default_templates_dir()
        templates = scan_templates(
            templates_dir=tdir,
            tag_filter=tag_filter or None,
            severity_filter=severity_filter if severity_filter else None,
        )
        if tag_filter:
            templates = select_templates_by_tag(templates, tag_filter)
        output = {
            "templates_dir": tdir,
            "count": len(templates),
            "templates": [t.to_dict() for t in templates],
        }
        output_json = dump_json(output)

    # Mode: generate plan
    elif args.generate_plan:
        tdir = args.templates_dir or _get_default_templates_dir()
        templates = scan_templates(
            templates_dir=tdir,
            tag_filter=tag_filter or None,
            severity_filter=severity_filter if severity_filter else None,
        )

        # Apply tech-based smart selection
        tech_data = _load_tech_data(args.tech)
        if tech_data and tag_filter:
            extra_tags = tag_filter
        else:
            extra_tags = tag_filter

        if tech_data or tag_filter:
            templates = select_templates_by_tech(templates, tech_data, extra_tags)

        targets = _load_targets(args.targets) if args.targets else ["https://example.com"]

        # Generate plan or fallback guide
        nuclei_ok, _, _ = detect_nuclei()
        if nuclei_ok:
            plan = generate_execution_plan(
                templates=templates,
                targets=targets,
                rate_limit=args.rate_limit,
                concurrency=args.concurrency,
                severity_filter=severity_filter,
            )
            output = plan.to_dict()
        else:
            guide = generate_fallback_guide(templates, targets)
            output = {
                "nuclei_available": False,
                "fallback_guide": guide.to_dict(),
            }
        output_json = dump_json(output)

    # Mode: full scan plan (default when targets+tech provided)
    elif args.targets:
        tdir = args.templates_dir or _get_default_templates_dir()
        templates = scan_templates(
            templates_dir=tdir,
            severity_filter=severity_filter if severity_filter else None,
        )

        tech_data = _load_tech_data(args.tech)
        if tech_data or tag_filter:
            templates = select_templates_by_tech(templates, tech_data, tag_filter)

        targets = _load_targets(args.targets)

        nuclei_ok, _, _ = detect_nuclei()
        if nuclei_ok:
            plan = generate_execution_plan(
                templates=templates,
                targets=targets,
                rate_limit=args.rate_limit,
                concurrency=args.concurrency,
                severity_filter=severity_filter,
            )
            output = plan.to_dict()
        else:
            guide = generate_fallback_guide(templates, targets)
            output = {
                "nuclei_available": False,
                "fallback_guide": guide.to_dict(),
            }
        output_json = dump_json(output)

    # Mode: default (show help-like status)
    else:
        nuclei_ok, path, version = detect_nuclei()
        tdir = args.templates_dir or _get_default_templates_dir()
        template_count = len(scan_templates(templates_dir=tdir))
        output = {
            "nuclei_available": nuclei_ok,
            "nuclei_version": version or "N/A",
            "nuclei_path": path or "N/A",
            "templates_dir": tdir,
            "templates_count": template_count,
            "timestamp": utc_now_iso(),
        }
        output_json = dump_json(output)

    # Output
    if args.output:
        with open(args.output, "w", encoding="utf-8") as fh:
            fh.write(output_json + "\n")
        print(f"nuclei_runner: output written to {args.output}", file=sys.stderr)
    else:
        print(output_json)

    return 0


if __name__ == "__main__":
    sys.exit(main())
