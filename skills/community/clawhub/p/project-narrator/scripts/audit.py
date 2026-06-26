#!/usr/bin/env python3
"""
project-narrator: Audit an existing PROJECT-NARRATIVE.md against workspace reality.

Reads the narrative, extracts referenced paths and claims, checks them against
the actual filesystem, and reports drift with severity levels.

Usage:
    python3 audit.py --workspace /path/to/project
    python3 audit.py --workspace /path/to/project --narrative docs/NARRATIVE.md
    python3 audit.py --workspace /path/to/project --check-urls
    python3 audit.py --workspace /path/to/project --quiet
"""

import argparse
import os
import re
import sys
import urllib.request
import urllib.error
from datetime import datetime
from pathlib import Path


SEVERITY_ORDER = {"CRITICAL": 0, "WARNING": 1, "INFO": 2}

# Known file extensions for path heuristic
KNOWN_EXTENSIONS = {
    ".py", ".sh", ".ts", ".js", ".jsx", ".tsx", ".json", ".md", ".html",
    ".yaml", ".yml", ".toml", ".css", ".scss", ".sql", ".rs", ".go",
    ".rb", ".php", ".java", ".kt", ".swift", ".c", ".cpp", ".h",
    ".vue", ".svelte", ".env", ".lock", ".txt", ".cfg", ".ini",
    ".xml", ".csv", ".graphql", ".prisma", ".tf", ".hcl",
}

# API route prefixes — these are endpoints, not file paths
API_ROUTE_PREFIXES = (
    "/api/", "/brief", "/feed", "/dashboard", "/admin", "/timeline",
    "/welcome", "/.well-known/", "/auth", "/login", "/logout",
    "/signup", "/register", "/callback", "/webhook",
)

# URL / command prefixes to skip
URL_COMMAND_PREFIXES = (
    "http://", "https://", "curl ", "wget ",
    "GET ", "POST ", "PUT ", "DELETE ", "PATCH ", "HEAD ", "OPTIONS ",
)

# Tree drawing characters to strip
TREE_CHARS_RE = re.compile(r"[├└│─┬┤┼┐┘┌┏┓┗┛┣┫┳┻╋]+")

# Characters that indicate "not a file path" at the start
BAD_START_CHARS = {"$", "{", "(", "*", "#", ">", "|", "!", "~", "@", "&", "+", "=", "<"}

# Patterns in content that indicate "not a file path"
BAD_CONTENT_PATTERNS = [" — ", " | ", "](", "](http", "**", "##", "->", "=>"]


class Finding:
    def __init__(self, severity, category, message, details=None):
        self.severity = severity
        self.category = category
        self.message = message
        self.details = details

    def __str__(self):
        icon = {"CRITICAL": "🔴", "WARNING": "🟡", "INFO": "🔵"}[self.severity]
        line = f"{icon} [{self.severity}] {self.category}: {self.message}"
        if self.details:
            line += f"\n     {self.details}"
        return line


def read_narrative(path):
    """Read and return narrative content."""
    try:
        return path.read_text()
    except OSError as e:
        print(f"Error reading narrative: {e}", file=sys.stderr)
        sys.exit(1)


def _strip_code_blocks(content):
    """Remove fenced code blocks from content."""
    return re.sub(r"```[^\n]*\n.*?\n```", "", content, flags=re.DOTALL)


def _strip_table_lines(content):
    """Remove markdown table lines (lines with | delimiters) unless they look like paths."""
    lines = []
    for line in content.splitlines():
        stripped = line.strip()
        # It's a table line if it starts and ends with | (or starts with |)
        if stripped.startswith("|") and "|" in stripped[1:]:
            # Keep the line only if it contains something that looks like a real path
            # (has / and ends with a known extension)
            cells = stripped.split("|")
            has_real_path = False
            for cell in cells:
                cell = cell.strip().strip("`")
                if "/" in cell and any(cell.endswith(ext) for ext in KNOWN_EXTENSIONS):
                    has_real_path = True
                    break
            if not has_real_path:
                continue
        lines.append(line)
    return "\n".join(lines)


def _is_valid_file_path(ref):
    """Check if a string looks like a real file path reference."""
    # Length check
    if len(ref) < 3 or len(ref) > 150:
        return False

    # Must contain / or end with known extension
    has_slash = "/" in ref
    has_extension = any(ref.endswith(ext) for ext in KNOWN_EXTENSIONS)
    if not has_slash and not has_extension:
        return False

    # Skip if starts with bad characters
    if ref[0] in BAD_START_CHARS:
        return False

    # Skip API routes
    for prefix in API_ROUTE_PREFIXES:
        if ref.startswith(prefix):
            return False

    # Skip URLs and commands
    ref_lower = ref.lower()
    for prefix in URL_COMMAND_PREFIXES:
        if ref_lower.startswith(prefix.lower()):
            return False

    # Skip if contains bad patterns (markdown formatting, etc.)
    for pattern in BAD_CONTENT_PATTERNS:
        if pattern in ref:
            return False

    # Skip if it looks like a route with method prefix
    if re.match(r"^(GET|POST|PUT|DELETE|PATCH|HEAD)\s+/", ref):
        return False

    # Skip if it looks like a URL path (starts with / and has query params or fragments)
    if ref.startswith("/") and ("?" in ref or "&" in ref):
        return False

    # Skip if it looks like a domain path (contains .ai/, .com/, .io/, .org/, .net/)
    if re.search(r'\.\w{2,4}/', ref):
        return False

    # Skip if it starts with / and doesn't look like a relative project path
    # (API routes start with / but real file refs are usually relative)
    if ref.startswith("/") and not has_extension:
        # Only allow /paths if they match typical project structure
        # e.g., /src/..., /lib/..., but not /api/..., /admin, etc.
        return False

    # Skip if it contains spaces (unless it's a path with escaped spaces, rare)
    if " " in ref:
        return False

    # Skip pure version strings like "v1.0", ">=3.8"
    if re.match(r"^[v>=<~^]?\d", ref):
        return False

    return True


def extract_file_paths(content, workspace):
    """Extract file/directory paths referenced in the narrative."""
    paths = set()

    # First, strip code blocks and table content to reduce false positives
    cleaned = _strip_code_blocks(content)
    cleaned = _strip_table_lines(cleaned)

    # Paths in backticks that look like file paths
    backtick_refs = re.findall(r"`([^`]+)`", cleaned)
    for ref in backtick_refs:
        ref = ref.strip()
        # Skip obvious commands
        if ref.startswith(("npm ", "npx ", "python", "pip ", "cargo ", "go ",
                           "docker ", "kubectl ", "git ", "make ", "brew ",
                           "apt ", "yarn ", "pnpm ", "node ", "deno ", "bun ")):
            continue
        if ref.startswith("http") or ref.startswith("git@"):
            continue
        if "=" in ref and "/" not in ref:  # env vars like KEY=value
            continue

        if _is_valid_file_path(ref):
            paths.add(ref)

    return paths


def extract_file_map_entries(content):
    """Extract entries from the File Map section, handling tree characters."""
    entries = set()

    file_map_match = re.search(r"## File Map\s*\n```\n(.*?)\n```", content, re.DOTALL)
    if not file_map_match:
        return entries

    for line in file_map_match.group(1).splitlines():
        # Strip tree drawing characters
        entry = TREE_CHARS_RE.sub("", line)
        # Strip leading/trailing whitespace
        entry = entry.strip()
        # Strip trailing comments (# comment)
        entry = re.sub(r"\s+#\s+.*$", "", entry)
        # Strip trailing /
        entry = entry.rstrip("/")
        # Skip empty, ellipsis, or parenthetical
        if not entry or entry.startswith("...") or entry.startswith("("):
            continue
        entries.add(entry)

    return entries


def extract_urls(content):
    """Extract URLs from the narrative."""
    urls = set()
    # Markdown links
    urls.update(re.findall(r"\[.*?\]\((https?://[^\s)]+)\)", content))
    # Bare URLs
    urls.update(re.findall(r"(?<!\()(https?://[^\s\)>\]]+)", content))
    return urls


def extract_script_refs(content):
    """Extract script names referenced in the narrative."""
    scripts = set()
    # npm run <script>
    scripts.update(re.findall(r"`npm run (\S+)`", content))
    # python/python3 <script>
    scripts.update(re.findall(r"`python3?\s+(\S+\.py)`", content))
    return scripts


def check_file_map(content, workspace):
    """Compare the File Map section against actual directory."""
    findings = []

    file_map_entries = extract_file_map_entries(content)
    if not file_map_entries:
        findings.append(Finding("WARNING", "File Map", "No File Map section found in narrative"))
        return findings

    # Get actual top-level items
    skip = {".git", ".venv", ".next", ".nuxt", "node_modules", "__pycache__",
            "dist", "build", "target", "vendor"}
    actual_top = set()
    try:
        for item in workspace.iterdir():
            if item.name.startswith(".") and item.name in skip:
                continue
            if item.name in skip:
                continue
            actual_top.add(item.name + ("/" if item.is_dir() else ""))
    except PermissionError:
        pass

    documented_top = set()
    for d in file_map_entries:
        parts = d.split("/") if "/" in d else [d]
        name = parts[0]
        documented_top.add(name.rstrip("/"))

    actual_names = {n.rstrip("/") for n in actual_top}

    # Find missing (in docs but not on disk)
    for name in documented_top - actual_names:
        findings.append(Finding(
            "CRITICAL", "File Map",
            f"Documented item `{name}` no longer exists on disk"
        ))

    # Find undocumented (on disk but not in docs)
    for name in actual_names - documented_top:
        findings.append(Finding(
            "WARNING", "File Map",
            f"Undocumented item on disk: `{name}`"
        ))

    return findings


def check_narrative_freshness(content):
    """Check when the narrative was last updated."""
    findings = []
    date_match = re.search(r"\*Last updated:\s*(\d{4}-\d{2}-\d{2})\*", content)
    if not date_match:
        findings.append(Finding(
            "WARNING", "Freshness",
            "No 'Last updated' date found in narrative"
        ))
        return findings, None

    try:
        last_updated = datetime.strptime(date_match.group(1), "%Y-%m-%d")
        age_days = (datetime.now() - last_updated).days

        if age_days > 30:
            findings.append(Finding(
                "CRITICAL", "Freshness",
                f"Narrative is {age_days} days old — likely significantly outdated",
                "Consider running `narrator update` or `narrator generate`"
            ))
        elif age_days > 14:
            findings.append(Finding(
                "WARNING", "Freshness",
                f"Narrative is {age_days} days old — may need review"
            ))
        else:
            findings.append(Finding(
                "INFO", "Freshness",
                f"Narrative was updated {age_days} day(s) ago"
            ))
        return findings, last_updated
    except ValueError:
        findings.append(Finding(
            "WARNING", "Freshness",
            f"Could not parse date: {date_match.group(1)}"
        ))
        return findings, None


def check_referenced_paths(content, workspace):
    """Check that referenced file paths exist."""
    findings = []
    paths = extract_file_paths(content, workspace)

    for p in sorted(paths):
        # Normalize: strip leading ./
        clean = p.lstrip("./")
        target = workspace / clean
        if not target.exists():
            # Fallback: check common subdirectories (scripts/, src/, config/, etc.)
            found = False
            for subdir in ["scripts", "src", "config", "lib", "api", "bin"]:
                alt = workspace / subdir / clean
                if alt.exists():
                    found = True
                    break
            if not found:
                findings.append(Finding(
                    "CRITICAL", "File Reference",
                    f"Referenced path `{p}` does not exist"
                ))

    return findings


def check_urls(content):
    """Check that URLs in the narrative are reachable."""
    findings = []
    urls = extract_urls(content)

    for url in sorted(urls):
        try:
            req = urllib.request.Request(url, method="HEAD")
            req.add_header("User-Agent", "project-narrator-audit/1.0")
            urllib.request.urlopen(req, timeout=10)
        except urllib.error.HTTPError as e:
            if e.code >= 400:
                findings.append(Finding(
                    "WARNING", "URL Check",
                    f"URL returned HTTP {e.code}: {url}"
                ))
        except (urllib.error.URLError, OSError, ValueError):
            findings.append(Finding(
                "WARNING", "URL Check",
                f"URL unreachable: {url}"
            ))

    return findings


def check_todo_sections(content):
    """Count remaining TODO placeholders."""
    findings = []
    todos = re.findall(r"<!--\s*TODO:", content)
    if todos:
        findings.append(Finding(
            "INFO", "Completeness",
            f"{len(todos)} TODO placeholder(s) remain in the narrative",
            "These sections need human input to complete"
        ))
    return findings


def check_package_json_drift(content, workspace):
    """Check if documented dependencies/scripts match package.json."""
    findings = []
    pj = workspace / "package.json"
    if not pj.exists():
        return findings

    try:
        import json
        data = json.loads(pj.read_text())
    except (json.JSONDecodeError, OSError):
        return findings

    # Check for documented npm scripts that no longer exist
    actual_scripts = set(data.get("scripts", {}).keys())
    doc_scripts = set(re.findall(r"`npm run (\S+)`", content))

    for s in doc_scripts - actual_scripts:
        findings.append(Finding(
            "CRITICAL", "Scripts",
            f"Documented script `npm run {s}` no longer exists in package.json"
        ))

    for s in actual_scripts - doc_scripts:
        findings.append(Finding(
            "WARNING", "Scripts",
            f"Script `npm run {s}` exists but is not documented"
        ))

    return findings


def run_audit(workspace, narrative_path, check_urls_flag, quiet=False):
    """Run the full audit. Returns exit code: 0=clean, 1=warnings, 2=critical."""
    workspace = Path(workspace).resolve()
    if not workspace.is_dir():
        print(f"Error: {workspace} is not a directory", file=sys.stderr)
        sys.exit(1)

    if narrative_path:
        nar_path = Path(narrative_path)
        if not nar_path.is_absolute():
            nar_path = workspace / nar_path
    else:
        nar_path = workspace / "PROJECT-NARRATIVE.md"

    if not nar_path.exists():
        print(f"Error: Narrative not found at {nar_path}", file=sys.stderr)
        print("Run `narrator generate` first to create one.", file=sys.stderr)
        sys.exit(1)

    content = read_narrative(nar_path)
    all_findings = []

    # Run checks
    freshness_findings, last_updated = check_narrative_freshness(content)
    all_findings.extend(freshness_findings)
    all_findings.extend(check_referenced_paths(content, workspace))
    all_findings.extend(check_file_map(content, workspace))
    all_findings.extend(check_todo_sections(content))
    all_findings.extend(check_package_json_drift(content, workspace))

    if check_urls_flag:
        print("Checking URLs (this may take a moment)...")
        all_findings.extend(check_urls(content))

    # Sort by severity
    all_findings.sort(key=lambda f: SEVERITY_ORDER.get(f.severity, 99))

    # Filter for quiet mode
    if quiet:
        all_findings = [f for f in all_findings if f.severity == "CRITICAL"]

    # Output
    print(f"\n{'=' * 60}")
    print(f"  PROJECT NARRATIVE AUDIT")
    print(f"  Workspace: {workspace}")
    print(f"  Narrative: {nar_path}")
    print(f"{'=' * 60}\n")

    if not all_findings:
        print("✅ No issues found. Narrative appears consistent with workspace.")
        return 0

    # Count by severity
    counts = {}
    for f in all_findings:
        counts[f.severity] = counts.get(f.severity, 0) + 1

    for finding in all_findings:
        print(finding)
        print()

    print(f"{'─' * 60}")
    print(f"Summary: ", end="")
    parts = []
    for sev in ["CRITICAL", "WARNING", "INFO"]:
        if sev in counts:
            parts.append(f"{counts[sev]} {sev}")
    print(", ".join(parts))

    total_actionable = counts.get("CRITICAL", 0) + counts.get("WARNING", 0)
    print(f"Actionable findings: {total_actionable}")

    if counts.get("CRITICAL", 0) > 0:
        print("\n⚠️  Critical issues found — narrative needs immediate update.")
        return 2
    elif counts.get("WARNING", 0) > 0:
        print("\n📝 Warnings found — consider running `narrator update`.")
        return 1
    else:
        print("\nℹ️  Only informational findings. Narrative is in decent shape.")
        return 0


def main():
    parser = argparse.ArgumentParser(
        description="Audit PROJECT-NARRATIVE.md against workspace reality"
    )
    parser.add_argument(
        "--workspace", "-w",
        default=".",
        help="Path to project workspace (default: current directory)",
    )
    parser.add_argument(
        "--narrative", "-n",
        default=None,
        help="Path to narrative file (default: PROJECT-NARRATIVE.md in workspace)",
    )
    parser.add_argument(
        "--check-urls",
        action="store_true",
        help="Also check that URLs in the narrative are reachable",
    )
    parser.add_argument(
        "--quiet", "-q",
        action="store_true",
        help="Only show CRITICAL findings",
    )
    args = parser.parse_args()
    exit_code = run_audit(args.workspace, args.narrative, args.check_urls, args.quiet)
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
