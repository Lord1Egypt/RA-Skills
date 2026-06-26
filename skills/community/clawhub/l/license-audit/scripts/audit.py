#!/usr/bin/env python3
"""
License Audit — Trivy-powered multi-language license compliance scanner.

Supports:
  - Local paths:        python3 audit.py /path/to/project
  - Remote git repos:   python3 audit.py https://github.com/user/repo.git

Requires: trivy, python3, git
"""

import argparse
import json
import os
import re
import subprocess
import sys
import tempfile
import shutil
import time
import urllib.parse
import urllib.request
from typing import Optional
from datetime import datetime

# ── License risk classification ────────────────────────────────────

HIGH_RISK = {
    "GPL-1.0", "GPL-1.0-only", "GPL-1.0-or-later",
    "GPL-2.0", "GPL-2.0-only", "GPL-2.0-or-later",
    "GPL-3.0", "GPL-3.0-only", "GPL-3.0-or-later",
    "AGPL-1.0", "AGPL-1.0-only", "AGPL-1.0-or-later",
    "AGPL-3.0", "AGPL-3.0-only", "AGPL-3.0-or-later",
    "EUPL-1.0", "EUPL-1.1", "EUPL-1.2",
}

MEDIUM_RISK = {
    "LGPL-2.0", "LGPL-2.0-only", "LGPL-2.0-or-later",
    "LGPL-2.1", "LGPL-2.1-only", "LGPL-2.1-or-later",
    "LGPL-3.0", "LGPL-3.0-only", "LGPL-3.0-or-later",
    "MPL-1.0", "MPL-1.1", "MPL-2.0",
    "EPL-1.0", "EPL-2.0",
    "CDDL-1.0", "CDDL-1.1", "CPL-1.0",
    "BSL-1.0", "BUSL-1.1", "SSPL-1.0",
    "Elastic-2.0",
    "CC-BY-NC-1.0", "CC-BY-NC-2.0", "CC-BY-NC-2.5",
    "CC-BY-NC-3.0", "CC-BY-NC-4.0", "CC-BY-NC-SA-1.0",
}

AMBIGUOUS_LICENSES = {
    "various", "various licenses", "see individual",
    "similar to", "custom", "proprietary",
}

# ── Stack detection ────────────────────────────────────────────────

# Maps manifest filename → (stack_label, trivy_type, needs_install, install_cmd, notes)
STACK_MANIFESTS = {
    # Node
    "package.json":        ("Node.js",  "node",   True,  "pnpm install / npm install",
                            "node_modules must be present for license data"),
    "pnpm-lock.yaml":      ("Node.js",  "node",   True,  "pnpm install",
                            "lockfile-only scan gives no license info"),
    "yarn.lock":           ("Node.js",  "node",   True,  "yarn install",
                            "lockfile-only scan gives no license info"),
    "package-lock.json":   ("Node.js",  "node",   True,  "npm install",
                            "lockfile-only scan gives no license info"),
    # Python
    "pyproject.toml":      ("Python",   "python", False, None,
                            "trivy reads pyproject.toml directly"),
    "requirements.txt":    ("Python",   "python", False, None,
                            "trivy reads requirements.txt directly"),
    "Pipfile.lock":        ("Python",   "python", False, None,
                            "trivy reads Pipfile.lock directly"),
    "poetry.lock":         ("Python",   "python", False, None,
                            "trivy reads poetry.lock directly"),
    # Java / Kotlin
    "pom.xml":             ("Java/Maven",  "java", False, None,
                            "trivy reads pom.xml directly"),
    "build.gradle":        ("Java/Gradle", "java", False, None,
                            "trivy reads build.gradle directly"),
    "build.gradle.kts":    ("Kotlin/Gradle", "java", False, None,
                            "trivy reads build.gradle.kts directly"),
    # C# / .NET
    "packages.config":     ("C#/.NET",  "nuget",  False, None,
                            "packages.config: trivy gets pkg names but not licenses; "
                            "NuGet API lookup is used automatically"),
    ".csproj":             ("C#/.NET",  "nuget",  False, None,
                            "PackageReference: trivy may not resolve licenses; "
                            "NuGet API lookup is used automatically"),
    "*.sln":               ("C#/.NET",  "nuget",  False, None, ""),
    # Go
    "go.mod":              ("Go",       "go",     False, None,
                            "trivy reads go.mod directly"),
    # Rust
    "Cargo.toml":          ("Rust",     "rust",   False, None,
                            "trivy reads Cargo.toml directly"),
    # C/C++
    "conanfile.txt":       ("C/C++ (Conan)", "c",  False, None,
                            "trivy reads conanfile.txt directly"),
    "conanfile.py":        ("C/C++ (Conan)", "c",  False, None,
                            "trivy reads conanfile.py directly"),
    "CMakeLists.txt":      ("C/C++ (CMake)", "c",  False, None,
                            "no standard manifest; trivy may find nothing"),
    # Ruby
    "Gemfile.lock":        ("Ruby",     "ruby",   False, None,
                            "trivy reads Gemfile.lock directly"),
    # PHP
    "composer.lock":       ("PHP",      "php",    False, None,
                            "trivy reads composer.lock directly"),
}


def detect_stacks(target: str) -> list[dict]:
    """
    Walk the target directory (up to depth 3) and return detected stacks.
    Each entry: {stack, manifest, path, needs_install, install_cmd, notes}
    """
    if not os.path.isdir(target):
        return []

    found = {}  # stack_label → first manifest found
    for root, dirs, files in os.walk(target):
        # Skip hidden dirs and common noise
        dirs[:] = [d for d in dirs if not d.startswith(".")
                   and d not in ("node_modules", "__pycache__", "bin", "obj",
                                 ".git", "dist", "build", "target", "out")]
        depth = root.replace(target, "").count(os.sep)
        if depth > 3:
            dirs.clear()
            continue

        for fname in files:
            for manifest, info in STACK_MANIFESTS.items():
                if manifest.startswith("*"):
                    # glob-style: match by extension
                    if fname.endswith(manifest[1:]):
                        key = info[0]
                        if key not in found:
                            found[key] = {
                                "stack": info[0], "manifest": fname,
                                "path": os.path.join(root, fname),
                                "needs_install": info[2],
                                "install_cmd": info[3], "notes": info[4],
                            }
                else:
                    if fname == manifest:
                        key = info[0]
                        if key not in found:
                            found[key] = {
                                "stack": info[0], "manifest": fname,
                                "path": os.path.join(root, fname),
                                "needs_install": info[2],
                                "install_cmd": info[3], "notes": info[4],
                            }
    return list(found.values())


def check_node_modules(target: str) -> bool:
    """Return True if at least one node_modules dir exists under target."""
    for root, dirs, _ in os.walk(target):
        if "node_modules" in dirs:
            return True
        dirs[:] = [d for d in dirs if d not in (".git",)]
        if root.replace(target, "").count(os.sep) > 2:
            break
    return False


def print_stack_summary(stacks: list[dict], target: str):
    """Print detected stacks and any pre-scan warnings."""
    if not stacks:
        print(f"   Stacks detected: (none — scanning anyway)")
        return

    labels = [s["stack"] for s in stacks]
    print(f"   Stacks detected: {', '.join(labels)}")

    warnings = []
    for s in stacks:
        if s["needs_install"] and not check_node_modules(target):
            warnings.append(
                f"   ⚠️  {s['stack']}: node_modules not found.\n"
                f"      Run `{s['install_cmd']}` first, otherwise all packages will show as UNKNOWN."
            )
        if s["notes"] and not s["needs_install"]:
            # Only show non-trivial notes
            if "API" in s["notes"] or "may not" in s["notes"]:
                print(f"   ℹ️  {s['stack']}: {s['notes']}")

    if warnings:
        print()
        for w in warnings:
            print(w)
        print()


# ── NuGet license enrichment ───────────────────────────────────────

# Map common licenseUrl patterns to SPDX identifiers
_LICENSE_URL_SPDX = {
    "mit": "MIT", "apache-2": "Apache-2.0", "apache2": "Apache-2.0",
    "bsd-2": "BSD-2-Clause", "bsd-3": "BSD-3-Clause",
    "lgpl-2.1": "LGPL-2.1", "lgpl-3": "LGPL-3.0",
    "gpl-2": "GPL-2.0", "gpl-3": "GPL-3.0",
    "mpl-2": "MPL-2.0", "ms-pl": "MS-PL", "ms-rl": "MS-RL",
    "isc": "ISC", "unlicense": "Unlicense", "cc0": "CC0-1.0",
}


def _spdx_from_url(url: str) -> Optional[str]:
    """Infer SPDX identifier from a license URL."""
    if not url:
        return None
    # Exact NuGet licenses endpoint: https://licenses.nuget.org/MIT
    m = re.search(r"licenses\.nuget\.org/([^/?#]+)", url, re.I)
    if m:
        return urllib.parse.unquote(m.group(1))
    # Infer from URL keywords
    lower = url.lower()
    for keyword, spdx in _LICENSE_URL_SPDX.items():
        if keyword in lower:
            return spdx
    return None


def _nuget_license(pkg_id: str, version: str) -> Optional[str]:
    """
    Query NuGet v3 registration index for license info.
    Returns SPDX string or None on failure.
    Supports both new (licenseExpression) and old (licenseUrl) packages.
    """
    try:
        url = f"https://api.nuget.org/v3/registration5-semver1/{pkg_id.lower()}/index.json"
        req = urllib.request.Request(url, headers={"User-Agent": "license-audit/1.0"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read())

        # Walk pages and items to find the matching version
        ver_lower = version.lower()
        for page in data.get("items", []):
            for item in page.get("items", []):
                cat = item.get("catalogEntry", {})
                if cat.get("version", "").lower() == ver_lower:
                    expr = cat.get("licenseExpression", "").strip()
                    if expr:
                        return expr
                    lic_url = cat.get("licenseUrl", "")
                    return _spdx_from_url(lic_url)
        return None
    except Exception:
        return None


def enrich_nuget(results: dict, stacks: list[dict]) -> dict:
    """
    For C#/.NET projects where trivy returned UNKNOWN packages,
    look up licenses via NuGet API and re-classify.
    """
    is_nuget = any(s["stack"] == "C#/.NET" for s in stacks)
    if not is_nuget:
        return results

    unknowns_to_enrich = [
        item for item in results["UNKNOWN"]
        if not item["license"] or not item.get("all_licenses")
    ]

    if not unknowns_to_enrich:
        return results

    print(f"   🔎 NuGet API: looking up licenses for {len(unknowns_to_enrich)} packages...")
    enriched = 0
    remaining_unknown = []

    for item in unknowns_to_enrich:
        lic = _nuget_license(item["name"], item["version"])
        if lic:
            item["license"] = lic
            item["all_licenses"] = [lic]
            tier = classify_license(lic)
            results[tier].append(item)
            enriched += 1
        else:
            item["license"] = f"(NuGet API: not found — check https://www.nuget.org/packages/{item['name']})"
            remaining_unknown.append(item)

    results["UNKNOWN"] = [
        item for item in results["UNKNOWN"]
        if item not in unknowns_to_enrich
    ] + remaining_unknown

    if enriched:
        print(f"   ✅ Enriched {enriched} packages via NuGet API")
    if remaining_unknown:
        print(f"   ⚠️  {len(remaining_unknown)} packages still unknown after NuGet lookup")

    return results


# ── Trivy ──────────────────────────────────────────────────────────

def is_git_url(target: str) -> bool:
    return bool(
        target.startswith("https://") and target.endswith(".git")
        or target.startswith("git@")
        or target.startswith("ssh://")
    ) or bool(
        target.startswith("https://") and any(
            p in target for p in ["github.com", "gitlab.com", "bitbucket.org", "gitee.com"]
        )
    )


def ensure_trivy() -> str:
    """Return path to trivy, installing it if not found."""
    path = shutil.which("trivy")
    if path:
        return path
    print("⚠️  Trivy not found. Installing...")
    if sys.platform == "darwin":
        subprocess.run(["brew", "install", "trivy"], check=True)
    else:
        subprocess.run(
            "curl -sfL https://raw.githubusercontent.com/aquasecurity/trivy/main/contrib/install.sh | sh -s -- -b /usr/local/bin",
            shell=True, check=True,
        )
    return shutil.which("trivy") or "trivy"


def run_trivy(target: str, is_repo_url: bool) -> dict:
    if is_repo_url:
        cmd = ["trivy", "repo", "--scanners", "license", "--format", "json",
               "--quiet", "--no-progress", target]
    else:
        cmd = ["trivy", "fs", "--scanners", "license", "--format", "json",
               "--quiet", "--no-progress", target]

    trivy_bin = ensure_trivy()
    cmd[0] = trivy_bin

    print(f"🔍 Scanning: {target}")
    print(f"   Command: {' '.join(cmd)}\n")

    result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)

    if result.returncode != 0:
        stderr = result.stderr
        if "Permission denied" in stderr or "could not read Username" in stderr:
            print("❌ Git auth failed. Set GH_TOKEN or ensure ssh-add -l shows your key.")
            sys.exit(1)
        if "repository not found" in stderr.lower():
            print("❌ Repository not found.")
            sys.exit(1)
        print(f"❌ Trivy failed:\n{stderr}")
        sys.exit(1)

    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError:
        # Trivy sometimes emits warning lines before the JSON blob.
        # Find the largest valid JSON object in stdout rather than the first.
        best = None
        for line in result.stdout.splitlines():
            line = line.strip()
            if line.startswith("{"):
                try:
                    candidate = json.loads(line)
                    # Prefer the object that actually contains scan results
                    if best is None or len(candidate) > len(best):
                        best = candidate
                except json.JSONDecodeError:
                    continue
        if best is not None:
            return best
        print("❌ Failed to parse Trivy output")
        sys.exit(1)


# ── Classification ─────────────────────────────────────────────────

def classify_license(lic: str) -> str:
    lic_clean = lic.strip()
    lower = lic_clean.lower()

    for ambiguous in AMBIGUOUS_LICENSES:
        if ambiguous in lower:
            return "UNKNOWN"

    # Exact SPDX match first (covers "GPL-2.0-only", "AGPL-3.0", etc.)
    if lic_clean in HIGH_RISK:
        return "HIGH"
    if lic_clean in MEDIUM_RISK:
        return "MEDIUM"

    # Full-text fallback for non-SPDX license strings (e.g. "GNU General Public License v2")
    upper = lic_clean.upper()

    # Check LGPL / Lesser variants before GPL to avoid false HIGH matches
    if re.search(r'\bLGPL\b', upper) or "LESSER" in upper:
        return "MEDIUM"

    for kw in ["GNU GENERAL PUBLIC LICENSE", "AFFERO GENERAL PUBLIC LICENSE"]:
        if kw in upper:
            return "HIGH"
    # "GPL" alone: only match as a whole word to avoid false hits on e.g. "LGPL"
    if re.search(r'\bGPL\b', upper):
        return "HIGH"
    if re.search(r'\bAGPL\b', upper):
        return "HIGH"

    for kw in ["MOZILLA PUBLIC LICENSE", "ECLIPSE PUBLIC LICENSE",
               "COMMON DEVELOPMENT AND DISTRIBUTION", "BUSINESS SOURCE LICENSE",
               "CREATIVE COMMONS ATTRIBUTION-NONCOMMERCIAL",
               "SERVER SIDE PUBLIC LICENSE", "ELASTIC LICENSE"]:
        if kw in upper:
            return "MEDIUM"

    if "UNKNOWN" in upper or lic_clean == "":
        return "UNKNOWN"
    return "LOW"


def parse_results(data: dict) -> dict:
    results = {"HIGH": [], "MEDIUM": [], "LOW": [], "UNKNOWN": []}
    seen = set()

    for result in data.get("Results", []):
        target_file = result.get("Target", "unknown")
        for pkg in result.get("Packages", []):
            name = pkg.get("Name", "unknown")
            version = pkg.get("Version", "?")
            raw_licenses = pkg.get("Licenses")
            relationship = pkg.get("Relationship", "direct")

            if not raw_licenses:
                key = (name, "__NO_INFO__")
                if key in seen:
                    continue
                seen.add(key)
                results["UNKNOWN"].append({
                    "name": name, "version": version,
                    "license": "",   # blank → eligible for enrichment
                    "all_licenses": [],
                    "relationship": relationship, "target": target_file,
                })
                continue

            for lic in raw_licenses:
                key = (name, lic)
                if key in seen:
                    continue
                seen.add(key)
                tier = classify_license(lic)
                results[tier].append({
                    "name": name, "version": version,
                    "license": lic, "all_licenses": raw_licenses,
                    "relationship": relationship, "target": target_file,
                })

    return results


# ── Terminal report ────────────────────────────────────────────────

def _unknown_hint(item: dict, stacks: list[dict]) -> str:
    """Return a friendly per-stack hint for why a package is unknown."""
    stack_labels = [s["stack"] for s in stacks]
    name = item["name"]

    if "Node.js" in stack_labels:
        return "(run pnpm/npm/yarn install first)"
    if "C#/.NET" in stack_labels:
        return f"(check https://www.nuget.org/packages/{name})"
    if "Java/Maven" in stack_labels or "Java/Gradle" in stack_labels:
        return f"(check https://mvnrepository.com/artifact/{name})"
    if "Python" in stack_labels:
        return f"(check https://pypi.org/project/{name})"
    if "Go" in stack_labels:
        return "(check pkg.go.dev)"
    if "Rust" in stack_labels:
        return f"(check https://crates.io/crates/{name})"
    if "C/C++ (Conan)" in stack_labels:
        return f"(check https://conan.io/center/{name})"
    return "(manual verification needed)"


def print_report(results: dict, target: str, stacks: list[dict] = None):
    stacks = stacks or []
    total = sum(len(v) for v in results.values())

    print("=" * 85)
    print("📋 LICENSE AUDIT REPORT")
    print(f"   Target: {target}")
    print(f"   Dependencies scanned: {total}")
    print("=" * 85)

    sections = [
        ("HIGH",    "🔴 HIGH RISK — Strong copyleft (GPL/AGPL)"),
        ("MEDIUM",  "🟡 MEDIUM RISK — Conditional copyleft (LGPL/MPL/EPL/BSL)"),
        ("UNKNOWN", "⚠️  UNKNOWN — Manual verification needed"),
        ("LOW",     "🟢 LOW RISK — Commercial-friendly (Apache/MIT/BSD)"),
    ]

    for tier, label in sections:
        items = results[tier]
        if not items:
            continue
        print(f"\n{label} ({len(items)}):")
        print("-" * 85)

        items_sorted = sorted(items, key=lambda x: (x["relationship"] != "direct", x["name"]))
        for item in items_sorted:
            rel = "  [transitive]" if item["relationship"] != "direct" else ""
            dual = ""
            if len(item["all_licenses"]) > 1:
                others = [l for l in item["all_licenses"] if l != item["license"]]
                if others:
                    dual = f"  (also: {', '.join(others)})"

            lic_display = item["license"] or _unknown_hint(item, stacks)
            print(f"  {item['name']}@{item['version']}{rel}")
            print(f"    License: {lic_display}{dual}")

    print(f"\n{'=' * 85}")
    print(f"🔴 HIGH: {len(results['HIGH'])}  |  🟡 MEDIUM: {len(results['MEDIUM'])}  "
          f"|  ⚠️ UNKNOWN: {len(results['UNKNOWN'])}  |  🟢 LOW: {len(results['LOW'])}")
    print(f"   Total: {total} unique (package, license) pairs")

    if results["HIGH"]:
        print(f"\n❌ {len(results['HIGH'])} high-risk licenses found — review before commercial use!")


# ── Markdown ───────────────────────────────────────────────────────

def render_markdown(results: dict, target: str, stacks: list[dict] = None) -> str:
    stacks = stacks or []
    total = sum(len(v) for v in results.values())
    lines = []
    lines.append("# 📋 License Audit Report")
    lines.append("")
    lines.append(f"**Target:** `{target}`  ")
    lines.append(f"**Dependencies scanned:** {total}  ")
    if stacks:
        lines.append(f"**Stacks:** {', '.join(s['stack'] for s in stacks)}  ")
    lines.append(f"**Tool:** [Trivy](https://github.com/aquasecurity/trivy)  ")
    lines.append("")

    tier_config = [
        ("HIGH",    "🔴 HIGH — Strong copyleft",       "GPL / AGPL — likely commercial blocker"),
        ("MEDIUM",  "🟡 MEDIUM — Conditional copyleft", "LGPL / MPL / EPL / BSL — review terms"),
        ("UNKNOWN", "⚠️ UNKNOWN",                       "Manual verification needed"),
        ("LOW",     "🟢 LOW — Commercial-friendly",     "Apache / MIT / BSD — safe for commercial use"),
    ]

    for tier, label, desc in tier_config:
        items = results[tier]
        if not items:
            continue
        lines.append(f"## {label}")
        lines.append(f"_{desc}_")
        lines.append("")
        lines.append("| Package | Version | License | Relation |")
        lines.append("|---------|---------|---------|----------|")
        for item in sorted(items, key=lambda x: (x["relationship"] != "direct", x["name"])):
            name = item["name"].replace("|", "\\|")
            lic = (item["license"] or _unknown_hint(item, stacks)).replace("|", "\\|")
            rel = "transitive" if item["relationship"] != "direct" else "direct"
            dual = ""
            if len(item["all_licenses"]) > 1:
                others = [l for l in item["all_licenses"] if l != item["license"]]
                if others:
                    dual = f" (also: {', '.join(others)})"
            lines.append(f"| `{name}` | {item['version']} | {lic}{dual} | {rel} |")
        lines.append("")

    lines.append("---")
    lines.append("| Risk Tier | Count |")
    lines.append("|-----------|-------|")
    for tier, emoji in [("HIGH","🔴"), ("MEDIUM","🟡"), ("UNKNOWN","⚠️"), ("LOW","🟢")]:
        lines.append(f"| {emoji} {tier} | {len(results[tier])} |")
    lines.append(f"| **Total** | **{total}** |")

    if results["HIGH"]:
        lines.append(f"\n> ❌ **{len(results['HIGH'])} high-risk licenses found** — review before commercial use!")

    return "\n".join(lines) + "\n"


# ── HTML ───────────────────────────────────────────────────────────

def render_html(results: dict, target: str, stacks: list[dict] = None) -> str:
    stacks = stacks or []
    total = sum(len(v) for v in results.values())
    tier_config = [
        ("HIGH",    "#dc2626", "#fef2f2", "🔴 HIGH — Strong Copyleft (GPL/AGPL)"),
        ("MEDIUM",  "#d97706", "#fffbeb", "🟡 MEDIUM — Conditional (LGPL/MPL/EPL/BSL)"),
        ("UNKNOWN", "#6b7280", "#f9fafb", "⚠️ UNKNOWN — Needs Review"),
        ("LOW",     "#16a34a", "#f0fdf4", "🟢 LOW — Commercial-Friendly"),
    ]

    tier_sections = []
    for tier, color, bg, label in tier_config:
        items = results[tier]
        if not items:
            continue
        rows = []
        for item in sorted(items, key=lambda x: (x["relationship"] != "direct", x["name"])):
            lic = item["license"] or _unknown_hint(item, stacks)
            rel = "transitive" if item["relationship"] != "direct" else "direct"
            rel_cls = "rel-transitive" if rel == "transitive" else ""
            dual = ""
            if len(item["all_licenses"]) > 1:
                others = [l for l in item["all_licenses"] if l != item["license"]]
                if others:
                    dual = f'<span class="dual">also: {", ".join(others)}</span>'
            rows.append(
                f'<tr class="{rel_cls}">'
                f'<td class="pkg">{item["name"].replace("&","&amp;").replace("<","&lt;")}</td>'
                f'<td class="ver">{item["version"]}</td>'
                f'<td class="lic">{lic.replace("&","&amp;").replace("<","&lt;")}{dual}</td>'
                f'<td class="rel">{rel}</td>'
                f'</tr>'
            )
        tier_sections.append(f"""
        <div class="tier" style="border-left:4px solid {color}">
            <h2 style="background:{bg};color:{color};padding:12px 16px;margin:0">
                {label} <span class="count">({len(items)})</span>
            </h2>
            <table>
                <thead><tr>
                    <th>Package</th><th>Version</th><th>License</th><th>Relation</th>
                </tr></thead>
                <tbody>{"".join(rows)}</tbody>
            </table>
        </div>""")

    stack_badge = ""
    if stacks:
        badges = " ".join(f'<span class="badge">{s["stack"]}</span>' for s in stacks)
        stack_badge = f'<div class="stacks">{badges}</div>'

    high_count = len(results["HIGH"])
    status_color = "#dc2626" if high_count > 0 else "#16a34a"
    status_text = f"❌ {high_count} HIGH-risk" if high_count > 0 else "✅ CLEAN"

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>License Audit — {target}</title>
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;
     background:#0f172a;color:#e2e8f0;padding:24px;max-width:1100px;margin:0 auto}}
.header{{text-align:center;padding:48px 0 32px}}
.header h1{{font-size:2em;margin-bottom:8px}}
.header .meta{{color:#94a3b8;font-size:0.9em}}
.status{{display:inline-block;margin-top:16px;padding:8px 24px;border-radius:8px;
         font-weight:700;font-size:1.1em;background:{status_color}22;color:{status_color}}}
.stacks{{margin-top:12px}}
.badge{{display:inline-block;margin:0 4px;padding:3px 10px;border-radius:12px;
        background:#1e293b;color:#94a3b8;font-size:0.8em}}
.summary{{display:flex;gap:16px;justify-content:center;margin:32px 0 40px;flex-wrap:wrap}}
.summary-card{{background:#1e293b;border-radius:12px;padding:20px 28px;text-align:center;min-width:110px}}
.summary-card .num{{font-size:2.2em;font-weight:800}}
.summary-card .label{{color:#94a3b8;font-size:0.85em;margin-top:4px}}
.high .num{{color:#dc2626}}.medium .num{{color:#d97706}}.low .num{{color:#16a34a}}.unknown .num{{color:#6b7280}}
.tier{{margin-bottom:24px;background:#1e293b;border-radius:12px;overflow:hidden}}
.tier h2{{font-size:1em}}.tier .count{{font-weight:400;color:#94a3b8}}
table{{width:100%;border-collapse:collapse;font-size:0.88em}}
th{{text-align:left;padding:10px 16px;color:#64748b;font-weight:600;border-bottom:1px solid #334155}}
td{{padding:8px 16px;border-bottom:1px solid #1e293b}}
tr:hover{{background:#33415522}}
.pkg{{font-family:'SF Mono','Fira Code',monospace;font-size:0.85em;max-width:340px;
      overflow:hidden;text-overflow:ellipsis;white-space:nowrap}}
.ver{{color:#94a3b8;white-space:nowrap}}.lic{{color:#e2e8f0;white-space:nowrap}}
.rel{{color:#64748b;font-size:0.8em;text-transform:uppercase;white-space:nowrap}}
.rel-transitive{{opacity:0.65}}
.dual{{color:#f59e0b;font-size:0.85em;margin-left:6px}}
.footer{{text-align:center;padding:40px 0;color:#475569;font-size:0.8em}}
.footer a{{color:#64748b}}
</style>
</head>
<body>
<div class="header">
    <h1>📋 License Audit Report</h1>
    <div class="meta">Target: <code>{target}</code> · {total} dependencies · Powered by Trivy</div>
    {stack_badge}
    <div class="status">{status_text}</div>
</div>
<div class="summary">
    <div class="summary-card high"><div class="num">{len(results["HIGH"])}</div><div class="label">🔴 High</div></div>
    <div class="summary-card medium"><div class="num">{len(results["MEDIUM"])}</div><div class="label">🟡 Medium</div></div>
    <div class="summary-card unknown"><div class="num">{len(results["UNKNOWN"])}</div><div class="label">⚠️ Unknown</div></div>
    <div class="summary-card low"><div class="num">{len(results["LOW"])}</div><div class="label">🟢 Low</div></div>
</div>
{"".join(tier_sections)}
<div class="footer">
    Generated by <a href="https://github.com/aquasecurity/trivy">Trivy</a> · License Audit Skill
</div>
</body>
</html>"""


# ── Feishu markdown ────────────────────────────────────────────────

def _build_feishu_markdown(results: dict, target: str, stacks: list[dict] = None) -> str:
    stacks = stacks or []
    total = sum(len(v) for v in results.values())
    lines = []

    stack_str = ", ".join(s["stack"] for s in stacks) if stacks else "unknown"
    lines.append('<callout emoji="📋" background-color="light-blue">')
    lines.append("**License Audit Report**  ")
    lines.append(f"Target: `{target}`  ")
    lines.append(f"Stacks: {stack_str}  ")
    lines.append(f"Dependencies: {total} · Powered by Trivy")
    lines.append("</callout>")
    lines.append("")

    h, m, u, l = (len(results[k]) for k in ("HIGH", "MEDIUM", "UNKNOWN", "LOW"))
    lines.append('<grid cols="4">')
    for label, count, emoji, color in [
        ("High Risk", h, "🔴", "red"),
        ("Medium",    m, "🟡", "orange"),
        ("Unknown",   u, "⚠️", "gray"),
        ("Low Risk",  l, "🟢", "green"),
    ]:
        lines.append("<column>")
        lines.append(f'<callout emoji="{emoji}" background-color="light-{color}">')
        lines.append(f"**{count}**  ")
        lines.append(label)
        lines.append("</callout>")
        lines.append("</column>")
    lines.append("</grid>")
    lines.append("")

    tier_config = [
        ("HIGH",    "🔴 HIGH — Strong Copyleft (GPL/AGPL)",        "light-red"),
        ("MEDIUM",  "🟡 MEDIUM — Conditional (LGPL/MPL/EPL/BSL)",  "light-orange"),
        ("UNKNOWN", "⚠️ UNKNOWN — Manual Check Required",           "light-gray"),
        ("LOW",     "🟢 LOW — Commercial-Friendly (Apache/MIT/BSD)","light-green"),
    ]

    for tier, label, bg in tier_config:
        items = results[tier]
        if not items:
            continue
        lines.append(f'<callout emoji="" background-color="{bg}">')
        lines.append(f"**{label}** ({len(items)})")
        lines.append("</callout>")
        lines.append("")
        lines.append("| Package | Version | License | Relation |")
        lines.append("|---------|---------|---------|----------|")
        for item in sorted(items, key=lambda x: (x["relationship"] != "direct", x["name"])):
            name = item["name"].replace("|", "\\|")
            lic = (item["license"] or _unknown_hint(item, stacks)).replace("|", "\\|")
            rel = "transitive" if item["relationship"] != "direct" else "direct"
            dual = ""
            if len(item["all_licenses"]) > 1:
                others = [x for x in item["all_licenses"] if x != item["license"]]
                if others:
                    dual = f" (also: {', '.join(others)})"
            lines.append(f"| `{name}` | {item['version']} | {lic}{dual} | {rel} |")
        lines.append("")

    if results["HIGH"]:
        lines.append('<callout emoji="❌" background-color="light-red">')
        lines.append(f'**{len(results["HIGH"])} high-risk licenses found — review before commercial use!**')
        lines.append("</callout>")

    return "\n".join(lines) + "\n"


# ── Feishu Doc ─────────────────────────────────────────────────────

def _check_lark_cli():
    if not shutil.which("lark-cli"):
        print("❌ lark-cli not found.")
        sys.exit(1)


def publish_feishu_doc(results: dict, target: str, stacks: list[dict] = None,
                       folder_token: str = None) -> str:
    _check_lark_cli()
    stacks = stacks or []
    title = f"License Audit — {os.path.basename(target.rstrip('/'))}"
    md = _build_feishu_markdown(results, target, stacks)

    tmp_dir = tempfile.mkdtemp()
    tmp_filename = "audit_report.md"
    try:
        with open(os.path.join(tmp_dir, tmp_filename), "w", encoding="utf-8") as f:
            f.write(md)
        cmd = ["lark-cli", "docs", "+create",
               "--title", title, "--markdown", f"@{tmp_filename}", "--as", "user"]
        if folder_token:
            cmd += ["--folder-token", folder_token]
        print("📄 Creating Feishu Doc...")
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60, cwd=tmp_dir)
    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)

    if result.returncode != 0:
        print(f"❌ Failed to create Feishu doc:\n{result.stderr}")
        return ""
    try:
        resp = json.loads(result.stdout)
        doc_url = (resp.get("data") or {}).get("doc_url", "")
        if not doc_url:
            doc_url = resp.get("doc_url") or resp.get("url", "(see output above)")
        return f"✅ Feishu Doc created: {doc_url}"
    except json.JSONDecodeError:
        return result.stdout.strip()


# ── Feishu Base ────────────────────────────────────────────────────

def publish_feishu_base(results: dict, target: str, stacks: list[dict] = None,
                        folder_token: str = None) -> str:
    _check_lark_cli()
    stacks = stacks or []
    project_name = os.path.basename(target.rstrip("/"))
    if project_name.endswith(".git"):
        project_name = project_name[:-4]
    base_name = f"License Audit — {project_name}"

    print("📊 Creating Feishu Base...")
    cmd = ["lark-cli", "base", "+base-create", "--name", base_name, "--as", "user"]
    if folder_token:
        cmd += ["--folder-token", folder_token]
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
    if r.returncode != 0:
        print(f"❌ Failed to create Base:\n{r.stderr}")
        return r.stderr

    try:
        base_resp = json.loads(r.stdout)
        base_data = base_resp.get("data", {}).get("base", {})
        base_token = base_data.get("base_token", "")
        base_url = base_data.get("url", "")
    except (json.JSONDecodeError, AttributeError):
        m = re.search(r'"base_token"\s*:\s*"([^"]+)"', r.stdout)
        base_token = m.group(1) if m else ""
        m2 = re.search(r'"url"\s*:\s*"([^"]+)"', r.stdout)
        base_url = m2.group(1) if m2 else ""

    if not base_token:
        print(f"❌ Could not parse base token from:\n{r.stdout}")
        return r.stdout

    print(f"   Base: {base_url or base_token}")
    print("   Creating table...")
    cmd = ["lark-cli", "base", "+table-create",
           "--base-token", base_token, "--name", "Dependencies", "--as", "user"]
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
    if r.returncode != 0:
        print(f"❌ Failed to create table:\n{r.stderr}")
        return f"Base created: {base_url}\nTable creation failed: {r.stderr}"

    table_id = ""
    try:
        tdata = json.loads(r.stdout)
        table_id = tdata.get("data", {}).get("table", {}).get("id", "")
    except (json.JSONDecodeError, AttributeError):
        pass
    if not table_id:
        m = re.search(r'"(?:table_id|id)"\s*:\s*"(tbl[^"]+)"', r.stdout)
        table_id = m.group(1) if m else ""

    if not table_id:
        print(f"❌ Could not parse table_id from:\n{r.stdout}")
        return f"Base: {base_url}\nCould not parse table_id"

    print("   Removing default empty table...")
    tl = subprocess.run(
        ["lark-cli", "base", "+table-list", "--base-token", base_token, "--as", "user"],
        capture_output=True, text=True, timeout=15,
    )
    try:
        for tbl in json.loads(tl.stdout).get("data", {}).get("tables", []):
            if tbl.get("id") != table_id:
                subprocess.run(
                    ["lark-cli", "base", "+table-delete",
                     "--base-token", base_token, "--table-id", tbl["id"],
                     "--as", "user", "--yes"],
                    capture_output=True, text=True, timeout=15,
                )
    except Exception:
        pass

    print("   Adding fields...")
    for fld in [
        {"name": "Package",      "type": "text"},
        {"name": "Version",      "type": "text"},
        {"name": "License",      "type": "text"},
        {"name": "Risk Tier",    "type": "select",
         "options": [{"name": "🔴 HIGH"}, {"name": "🟡 MEDIUM"},
                     {"name": "⚠️ UNKNOWN"}, {"name": "🟢 LOW"}]},
        {"name": "Relation",     "type": "text"},
        {"name": "Dual License", "type": "text"},
    ]:
        payload = {"name": fld["name"], "type": fld["type"]}
        if "options" in fld:
            payload["options"] = fld["options"]
            payload["multiple"] = False
        subprocess.run(
            ["lark-cli", "base", "+field-create",
             "--base-token", base_token, "--table-id", table_id,
             "--json", json.dumps(payload), "--as", "user"],
            capture_output=True, text=True, timeout=15,
        )

    all_records = []
    for tier, tier_label in [("HIGH","🔴 HIGH"),("MEDIUM","🟡 MEDIUM"),
                              ("UNKNOWN","⚠️ UNKNOWN"),("LOW","🟢 LOW")]:
        for item in sorted(results[tier], key=lambda x: (x["relationship"] != "direct", x["name"])):
            dual = ""
            if len(item.get("all_licenses", [])) > 1:
                others = [x for x in item["all_licenses"] if x != item["license"]]
                if others:
                    dual = ", ".join(others)
            lic = item["license"] or _unknown_hint(item, stacks)
            rel = "transitive" if item["relationship"] != "direct" else "direct"
            all_records.append([item["name"], item["version"], lic, tier_label, rel, dual])

    print(f"   Inserting {len(all_records)} records...")
    batch_size = 200
    for i in range(0, len(all_records), batch_size):
        batch = all_records[i:i + batch_size]
        payload = json.dumps({
            "fields": ["Package", "Version", "License", "Risk Tier", "Relation", "Dual License"],
            "rows": batch,
        })
        rb = subprocess.run(
            ["lark-cli", "base", "+record-batch-create",
             "--base-token", base_token, "--table-id", table_id,
             "--as", "user", "--json", payload],
            capture_output=True, text=True, timeout=60,
        )
        if rb.returncode != 0:
            print(f"   ⚠️  Batch {i//batch_size + 1} failed: {rb.stderr[:200]}")
        if i + batch_size < len(all_records):
            time.sleep(0.6)

    return f"✅ Feishu Base created: {base_url}\n   {len(all_records)} records inserted"


# ── Main ───────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Multi-language license compliance audit (Trivy-based)"
    )
    parser.add_argument("target", help="Local path or git repo URL")
    parser.add_argument(
        "--format",
        choices=["table", "json", "markdown", "html", "feishu-doc", "feishu-base"],
        default="table",
        help="Output format (default: table)",
    )
    parser.add_argument(
        "--output", "-o", default=None,
        help="Output file path. For markdown/html/json, defaults to "
             "license-audit-<project>.<ext> in the current directory.",
    )
    parser.add_argument(
        "--feishu-folder", default=None,
        help="Feishu folder token for doc/base creation",
    )
    parser.add_argument(
        "--no-enrich", action="store_true",
        help="Skip NuGet/API license enrichment for unknown packages",
    )
    args = parser.parse_args()

    target = args.target
    is_url = is_git_url(target)

    if not is_url and not os.path.exists(target):
        print(f"❌ Path not found: {target}")
        sys.exit(1)

    # Detect stacks and warn before scanning
    stacks = detect_stacks(target) if not is_url else []
    print_stack_summary(stacks, target)

    try:
        data = run_trivy(target, is_url)
    except subprocess.TimeoutExpired:
        print("❌ Scan timed out (10 min).")
        sys.exit(1)

    results = parse_results(data)

    # Enrich UNKNOWN packages via language-specific APIs
    if not args.no_enrich:
        results = enrich_nuget(results, stacks)

    # Derive auto output filename
    _t = target.rstrip("/")
    project_name = os.path.basename(_t[:-4] if _t.endswith(".git") else _t) or "project"
    safe_name = re.sub(r"[^a-zA-Z0-9_-]", "-", project_name).strip("-") or "project"

    if args.format == "json":
        content = json.dumps({
            "target": target,
            "stacks": [s["stack"] for s in stacks],
            "summary": {tier: len(items) for tier, items in results.items()},
            "results": results,
        }, indent=2)
    elif args.format == "markdown":
        content = render_markdown(results, target, stacks)
    elif args.format == "html":
        content = render_html(results, target, stacks)
    elif args.format == "feishu-doc":
        content = publish_feishu_doc(results, target, stacks, args.feishu_folder)
    elif args.format == "feishu-base":
        content = publish_feishu_base(results, target, stacks, args.feishu_folder)
    else:
        print_report(results, target, stacks)
        content = None

    if content is not None:
        out_path = args.output
        if out_path is None and args.format in ("markdown", "html", "json"):
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            ext = {"markdown": "md", "html": "html", "json": "json"}[args.format]
            out_path = os.path.join(os.getcwd(), f"license-audit-{safe_name}-{ts}.{ext}")
        if out_path:
            with open(out_path, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"✅ Report written to {out_path}")
        else:
            print(content)

    if results["HIGH"]:
        sys.exit(1)
    elif args.format == "table":
        print("\n✅ No high-risk copyleft licenses found.")


if __name__ == "__main__":
    main()
