#!/usr/bin/env python3
"""
project-narrator: Generate a PROJECT-NARRATIVE.md scaffold by scanning a workspace.

Discovers project structure, dependencies, infrastructure, scripts, and git history,
then outputs a structured markdown template filled with what it found.

Usage:
    python3 generate.py --workspace /path/to/project
    python3 generate.py --workspace /path/to/project --output docs/NARRATIVE.md
"""

import argparse
import json
import os
import re
import subprocess
import sys
from collections import Counter
from datetime import datetime
from pathlib import Path


def run_cmd(cmd, cwd=None):
    """Run a shell command, return stdout or empty string on failure."""
    try:
        result = subprocess.run(
            cmd, capture_output=True, text=True, timeout=15, cwd=cwd
        )
        return result.stdout.strip() if result.returncode == 0 else ""
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return ""


def detect_package_managers(workspace):
    """Detect which package managers / project configs exist."""
    managers = {}
    checks = {
        "package.json": "Node.js (npm/yarn/pnpm)",
        "pyproject.toml": "Python (pyproject.toml)",
        "requirements.txt": "Python (pip)",
        "Cargo.toml": "Rust (cargo)",
        "go.mod": "Go (modules)",
        "Gemfile": "Ruby (bundler)",
        "composer.json": "PHP (composer)",
        "pom.xml": "Java (Maven)",
        "build.gradle": "Java/Kotlin (Gradle)",
    }
    for filename, label in checks.items():
        path = workspace / filename
        if path.exists():
            managers[filename] = label
    return managers


def parse_package_json(workspace):
    """Extract name, scripts, and dependencies from package.json."""
    pj = workspace / "package.json"
    if not pj.exists():
        return None
    try:
        data = json.loads(pj.read_text())
        return {
            "name": data.get("name", "unknown"),
            "version": data.get("version", ""),
            "scripts": list(data.get("scripts", {}).keys()),
            "dependencies": list(data.get("dependencies", {}).keys()),
            "devDependencies": list(data.get("devDependencies", {}).keys()),
        }
    except (json.JSONDecodeError, OSError):
        return None


def parse_pyproject(workspace):
    """Extract basic info from pyproject.toml (simple parser, no toml lib needed)."""
    pp = workspace / "pyproject.toml"
    if not pp.exists():
        return None
    try:
        text = pp.read_text()
        name_match = re.search(r'^name\s*=\s*"([^"]+)"', text, re.MULTILINE)
        version_match = re.search(r'^version\s*=\s*"([^"]+)"', text, re.MULTILINE)
        return {
            "name": name_match.group(1) if name_match else "unknown",
            "version": version_match.group(1) if version_match else "",
        }
    except OSError:
        return None


def parse_env_example(workspace):
    """Parse .env.example for variable names (no values)."""
    env_file = workspace / ".env.example"
    if not env_file.exists():
        env_file = workspace / ".env.sample"
    if not env_file.exists():
        return []
    try:
        lines = env_file.read_text().splitlines()
        variables = []
        for line in lines:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                var_name = line.split("=", 1)[0].strip()
                variables.append(var_name)
        return variables
    except OSError:
        return []


def scan_scripts_dir(workspace):
    """List files in scripts/ with their first-line comments."""
    scripts_dir = workspace / "scripts"
    if not scripts_dir.is_dir():
        return []
    results = []
    for f in sorted(scripts_dir.iterdir()):
        if f.is_file() and not f.name.startswith("."):
            try:
                first_lines = f.read_text().splitlines()[:5]
                comment = ""
                for line in first_lines:
                    stripped = line.strip()
                    if stripped.startswith("#") and not stripped.startswith("#!"):
                        comment = stripped.lstrip("# ").strip()
                        break
                    if stripped.startswith("//") or stripped.startswith("/*"):
                        comment = stripped.lstrip("/ *").strip()
                        break
                    if stripped.startswith('"""') or stripped.startswith("'''"):
                        comment = stripped.strip("\"' ").strip()
                        break
                results.append((f.name, comment))
            except (OSError, UnicodeDecodeError):
                results.append((f.name, "(could not read)"))
    return results


def count_source_files(workspace):
    """Count source files by extension, skipping common non-source dirs."""
    skip_dirs = {
        "node_modules", ".git", "__pycache__", ".venv", "venv",
        "dist", "build", ".next", ".nuxt", "target", "vendor",
        ".tox", "coverage", ".cache",
    }
    ext_map = {
        ".py": "Python", ".js": "JavaScript", ".ts": "TypeScript",
        ".tsx": "TypeScript (JSX)", ".jsx": "JavaScript (JSX)",
        ".rs": "Rust", ".go": "Go", ".rb": "Ruby", ".php": "PHP",
        ".java": "Java", ".kt": "Kotlin", ".swift": "Swift",
        ".c": "C", ".cpp": "C++", ".h": "C/C++ Header",
        ".css": "CSS", ".scss": "SCSS", ".html": "HTML",
        ".vue": "Vue", ".svelte": "Svelte",
        ".sql": "SQL", ".sh": "Shell", ".bash": "Shell",
    }
    counts = Counter()
    for root, dirs, files in os.walk(workspace):
        dirs[:] = [d for d in dirs if d not in skip_dirs]
        for f in files:
            ext = Path(f).suffix.lower()
            if ext in ext_map:
                counts[ext_map[ext]] += 1
    return dict(counts.most_common())


def detect_infrastructure(workspace):
    """Detect infrastructure-related files."""
    infra = []
    checks = [
        ("Dockerfile", "Docker"),
        ("docker-compose.yml", "Docker Compose"),
        ("docker-compose.yaml", "Docker Compose"),
        ("wrangler.toml", "Cloudflare Workers"),
        ("wrangler.jsonc", "Cloudflare Workers"),
        ("vercel.json", "Vercel"),
        ("netlify.toml", "Netlify"),
        ("serverless.yml", "Serverless Framework"),
        ("serverless.yaml", "Serverless Framework"),
        ("terraform.tf", "Terraform"),
        ("fly.toml", "Fly.io"),
        ("render.yaml", "Render"),
        ("railway.json", "Railway"),
        ("Procfile", "Heroku / PaaS"),
        (".github/workflows", "GitHub Actions"),
        (".gitlab-ci.yml", "GitLab CI"),
    ]
    for filename, label in checks:
        target = workspace / filename
        if target.exists():
            infra.append(label)
    return infra


def detect_api_routes(workspace):
    """Attempt to find API route patterns in source files."""
    route_patterns = [
        # Express / Hono
        (r"""(?:app|router)\.(get|post|put|delete|patch)\s*\(\s*['"]([^'"]+)['"]""", "{}"),
        # FastAPI
        (r"""@(?:app|router)\.(get|post|put|delete|patch)\s*\(\s*['"]([^'"]+)['"]""", "{}"),
        # Next.js App Router (from file paths)
    ]
    routes = []
    skip_dirs = {"node_modules", ".git", "__pycache__", ".venv", "dist", "build", "target"}
    source_exts = {".py", ".js", ".ts", ".tsx", ".jsx"}

    for root, dirs, files in os.walk(workspace):
        dirs[:] = [d for d in dirs if d not in skip_dirs]
        rel_root = Path(root).relative_to(workspace)

        # Next.js App Router detection
        if "route.ts" in files or "route.js" in files:
            route_path = "/" + str(rel_root).replace("app/", "", 1).replace("\\", "/")
            route_path = re.sub(r"\[([^\]]+)\]", r":\1", route_path)
            routes.append(f"  - `{route_path}` (Next.js App Router)")

        for f in files:
            if Path(f).suffix.lower() not in source_exts:
                continue
            filepath = Path(root) / f
            try:
                content = filepath.read_text(errors="ignore")[:50000]  # cap read size
                for pattern, _fmt in route_patterns:
                    matches = re.findall(pattern, content)
                    for match in matches[:20]:  # cap matches per file
                        method, path = match
                        routes.append(f"  - `{method.upper()} {path}`")
            except OSError:
                continue

    return list(dict.fromkeys(routes))[:50]  # dedupe, cap at 50


def get_git_info(workspace):
    """Get git remote URL and recent log."""
    remote = run_cmd(["git", "remote", "get-url", "origin"], cwd=workspace)
    log = run_cmd(
        ["git", "log", "--oneline", "--no-decorate", "-20"],
        cwd=workspace,
    )
    branch = run_cmd(["git", "branch", "--show-current"], cwd=workspace)
    return {
        "remote": remote,
        "branch": branch or "unknown",
        "log": log.splitlines() if log else [],
    }


def get_project_name(workspace, pkg_json, pyproject):
    """Determine project name from available sources."""
    if pkg_json and pkg_json.get("name"):
        return pkg_json["name"]
    if pyproject and pyproject.get("name"):
        return pyproject["name"]
    return workspace.name


def load_config(workspace, config_path=None):
    """Load narrator.json config if it exists."""
    if config_path:
        cfg_file = Path(config_path)
    else:
        cfg_file = Path(workspace) / "narrator.json"
    if cfg_file.exists():
        try:
            return json.loads(cfg_file.read_text())
        except (json.JSONDecodeError, OSError):
            print(f"Warning: Could not parse {cfg_file}", file=sys.stderr)
    return {}


def estimate_tokens(text):
    """Rough token estimate (~4 chars per token for English text)."""
    return len(text) // 4


def generate_narrative(workspace, output_path, config_path=None):
    """Generate the narrative scaffold."""
    workspace = Path(workspace).resolve()
    if not workspace.is_dir():
        print(f"Error: {workspace} is not a directory", file=sys.stderr)
        sys.exit(1)

    # Load config
    config = load_config(workspace, config_path)
    sections_config = config.get("sections", {})

    # Gather info
    managers = detect_package_managers(workspace)
    pkg_json = parse_package_json(workspace)
    pyproject = parse_pyproject(workspace)
    env_vars = parse_env_example(workspace)
    scripts = scan_scripts_dir(workspace)
    source_counts = count_source_files(workspace)
    infra = detect_infrastructure(workspace)
    routes = detect_api_routes(workspace)
    git = get_git_info(workspace)
    project_name = get_project_name(workspace, pkg_json, pyproject)
    today = datetime.now().strftime("%Y-%m-%d")

    # Build output
    lines = []
    lines.append(f"# {project_name}: The Complete Narrative")
    lines.append(f"*Last updated: {today}*")
    lines.append("")

    # What Is This Project?
    lines.append("## What Is This Project?")
    lines.append("")
    lines.append("<!-- TODO: Describe the project in 2-3 sentences. What does it do? Who is it for? -->")
    lines.append("")
    if git["remote"]:
        lines.append(f"**Repository:** {git['remote']}")
        lines.append(f"**Default branch:** {git['branch']}")
        lines.append("")

    # Current Status
    lines.append("## Current Status")
    lines.append("")
    lines.append("<!-- TODO: Is this in production? Alpha? Actively developed? Maintained? -->")
    lines.append("")

    # Architecture
    lines.append("## Architecture")
    lines.append("")
    if source_counts:
        lines.append("**Languages:**")
        for lang, count in source_counts.items():
            lines.append(f"  - {lang}: {count} files")
        lines.append("")
    if managers:
        lines.append("**Package managers / project files:**")
        for filename, label in managers.items():
            lines.append(f"  - `{filename}` — {label}")
        lines.append("")
    if pkg_json:
        if pkg_json["dependencies"]:
            lines.append(f"**Dependencies ({len(pkg_json['dependencies'])}):** {', '.join(pkg_json['dependencies'][:15])}")
            if len(pkg_json["dependencies"]) > 15:
                lines.append(f"  ... and {len(pkg_json['dependencies']) - 15} more")
            lines.append("")
    lines.append("<!-- TODO: Describe the high-level architecture. What are the main components? How do they communicate? -->")
    lines.append("")

    # Infrastructure
    lines.append("## Infrastructure")
    lines.append("")
    if infra:
        lines.append("**Detected:**")
        for i in infra:
            lines.append(f"  - {i}")
        lines.append("")
    else:
        lines.append("<!-- No infrastructure config files detected. -->")
        lines.append("")
    lines.append("<!-- TODO: Where does this run? What services does it depend on? Databases? CDNs? -->")
    lines.append("")

    # Pipeline / Workflow
    lines.append("## Pipeline / Workflow")
    lines.append("")
    lines.append("<!-- TODO: How does code get from local to production? CI/CD? Manual deploy? -->")
    lines.append("")

    # API Routes
    lines.append("## API Routes")
    lines.append("")
    if routes:
        lines.append("**Discovered routes:**")
        for r in routes:
            lines.append(r)
        lines.append("")
    else:
        lines.append("<!-- No API routes auto-detected. Add them manually if applicable. -->")
        lines.append("")

    # Scripts
    lines.append("## Scripts")
    lines.append("")
    if pkg_json and pkg_json["scripts"]:
        lines.append("**package.json scripts:**")
        for s in pkg_json["scripts"]:
            lines.append(f"  - `npm run {s}`")
        lines.append("")
    if scripts:
        lines.append("**scripts/ directory:**")
        for name, comment in scripts:
            if comment:
                lines.append(f"  - `{name}` — {comment}")
            else:
                lines.append(f"  - `{name}`")
        lines.append("")
    if not scripts and not (pkg_json and pkg_json["scripts"]):
        lines.append("<!-- No scripts detected. -->")
        lines.append("")

    # Configuration
    lines.append("## Configuration")
    lines.append("")
    if env_vars:
        lines.append("**Environment variables** (from .env.example):")
        for var in env_vars:
            lines.append(f"  - `{var}`")
        lines.append("")
    lines.append("<!-- TODO: What configuration is needed to run this project? -->")
    lines.append("")

    # Security Model
    lines.append("## Security Model")
    lines.append("")
    lines.append("<!-- TODO: How is auth handled? API keys? OAuth? What's the trust boundary? -->")
    lines.append("")

    # Known Issues
    lines.append("## Known Issues")
    lines.append("")
    lines.append("<!-- TODO: What's broken? What's fragile? What workarounds exist? -->")
    lines.append("<!-- This section prevents repeating past mistakes. Be honest. -->")
    lines.append("")

    # Design Principles
    lines.append("## Design Principles")
    lines.append("")
    lines.append("<!-- THIS IS THE MOST IMPORTANT SECTION. -->")
    lines.append("<!-- Architecture can be reverse-engineered. Design intent cannot. -->")
    lines.append("<!-- Document WHY you made the choices you made. Examples: -->")
    lines.append("<!-- - Why this database over alternatives? -->")
    lines.append("<!-- - Why this hosting platform? -->")
    lines.append("<!-- - What tradeoffs were accepted? -->")
    lines.append("<!-- - What was explicitly rejected, and why? -->")
    lines.append("")

    # Changelog
    if sections_config.get("changelog", True):
        lines.append("## Changelog")
        lines.append("")
        if git["log"]:
            lines.append("**Recent commits:**")
            for entry in git["log"]:
                lines.append(f"  - {entry}")
            lines.append("")
        lines.append("<!-- TODO: Track significant changes here, not just commits. -->")
        lines.append("")

    # Key Credentials & IDs
    if sections_config.get("credentials", True):
        lines.append("## Key Credentials & IDs")
        lines.append("")
        lines.append("<!-- List credential NAMES and WHERE they're stored. NEVER put actual secrets here. -->")
        lines.append("<!-- Example: Stripe API key — stored in ~/.openclaw/secrets/stripe.key -->")
        lines.append("")

    # File Map
    if sections_config.get("file_map", True):
        lines.append("## File Map")
        lines.append("")
        lines.append("```")
        # Generate a tree-like listing (top 2 levels)
        for item in sorted(workspace.iterdir()):
            if item.name.startswith(".") and item.name in {".git", ".venv", ".next", ".nuxt"}:
                continue
            if item.name in {"node_modules", "__pycache__", "dist", "build", "target", "vendor"}:
                continue
            if item.is_dir():
                lines.append(f"{item.name}/")
                try:
                    children = sorted(item.iterdir())[:20]
                    for child in children:
                        if child.name.startswith("."):
                            continue
                        suffix = "/" if child.is_dir() else ""
                        lines.append(f"  {child.name}{suffix}")
                    if len(list(item.iterdir())) > 20:
                        lines.append(f"  ... ({len(list(item.iterdir())) - 20} more)")
                except PermissionError:
                    lines.append("  (permission denied)")
            else:
                lines.append(item.name)
        lines.append("```")
        lines.append("")

    # Write output
    output = Path(output_path) if output_path else workspace / "PROJECT-NARRATIVE.md"
    if not output.is_absolute():
        output = workspace / output

    # Archive previous version before overwriting (prevents drift carryover)
    if output.exists():
        archive_dir = workspace / "narrative-archive"
        archive_dir.mkdir(exist_ok=True)
        timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
        archive_path = archive_dir / f"NARRATIVE-{timestamp}.md"
        import shutil
        shutil.copy2(output, archive_path)
        print(f"  📦 Archived previous narrative → {archive_path.name}")

    # Always write fresh — never append or patch, to prevent drift accumulation
    content = "\n".join(lines)
    output.write_text(content)
    tokens = estimate_tokens(content)
    print(f"Generated narrative scaffold: {output}")
    print(f"  Detected: {len(managers)} package manager(s), {len(infra)} infra config(s)")
    print(f"  Found: {sum(source_counts.values())} source files across {len(source_counts)} language(s)")
    print(f"  Routes: {len(routes)}, Scripts: {len(scripts)}")
    print(f"  Estimated narrative size: ~{tokens:,} tokens")
    print(f"\n  Next: Fill in the TODO sections — the script found structure, you add intent.")


def main():
    parser = argparse.ArgumentParser(
        description="Generate a PROJECT-NARRATIVE.md scaffold from workspace scan"
    )
    parser.add_argument(
        "--workspace", "-w",
        default=".",
        help="Path to project workspace (default: current directory)",
    )
    parser.add_argument(
        "--output", "-o",
        default=None,
        help="Output file path (default: PROJECT-NARRATIVE.md in workspace)",
    )
    parser.add_argument(
        "--config", "-c",
        default=None,
        help="Path to narrator.json config file (default: narrator.json in workspace)",
    )
    args = parser.parse_args()
    generate_narrative(args.workspace, args.output, args.config)


if __name__ == "__main__":
    main()
