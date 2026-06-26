#!/usr/bin/env python3
"""Generate .gitignore files for any project type.

Supports 200+ languages/frameworks via GitHub's gitignore templates,
with options to combine multiple templates and add custom rules.
"""

import argparse
import json
import os
import sys
import urllib.request
import urllib.error


GITHUB_API = "https://api.github.com/gitignore/templates"
CACHE_DIR = os.path.expanduser("~/.cache/gitignore-gen")
CACHE_FILE = os.path.join(CACHE_DIR, "templates.json")
CACHE_MAX_AGE = 86400  # 24 hours


def get_cached_list():
    """Return cached template list if fresh enough."""
    if os.path.exists(CACHE_FILE):
        age = os.time() - os.path.getmtime(CACHE_FILE) if hasattr(os, "time") else float("inf")
        try:
            import time as _time
            age = _time.time() - os.path.getmtime(CACHE_FILE)
        except Exception:
            age = float("inf")
        if age < CACHE_MAX_AGE:
            try:
                with open(CACHE_FILE) as f:
                    return json.load(f)
            except Exception:
                pass
    return None


def fetch_template_list():
    """Fetch available template names from GitHub API."""
    cached = get_cached_list()
    if cached:
        return cached
    try:
        req = urllib.request.Request(GITHUB_API, headers={"Accept": "application/json"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            templates = json.loads(resp.read().decode())
        os.makedirs(CACHE_DIR, exist_ok=True)
        with open(CACHE_FILE, "w") as f:
            json.dump(templates, f)
        return templates
    except urllib.error.URLError as e:
        print(f"Error fetching templates: {e}", file=sys.stderr)
        return []


def fetch_template(name):
    """Fetch a single gitignore template by name."""
    url = f"{GITHUB_API}/{name}"
    try:
        req = urllib.request.Request(url, headers={"Accept": "application/json"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode())
        return data.get("source", "")
    except urllib.error.URLError as e:
        print(f"Error fetching template '{name}': {e}", file=sys.stderr)
        return None


def find_template(query, templates):
    """Find the best matching template name (case-insensitive)."""
    query_lower = query.lower()
    # Exact match
    for t in templates:
        if t.lower() == query_lower:
            return t
    # Starts with
    for t in templates:
        if t.lower().startswith(query_lower):
            return t
    # Contains
    for t in templates:
        if query_lower in t.lower():
            return t
    return None


def cmd_list(args):
    """List available templates."""
    templates = fetch_template_list()
    if not templates:
        print("No templates available. Check your internet connection.", file=sys.stderr)
        return 1
    if args.filter:
        filt = args.filter.lower()
        templates = [t for t in templates if filt in t.lower()]
    for t in templates:
        print(t)
    print(f"\n{len(templates)} template(s) found.", file=sys.stderr)
    return 0


def cmd_generate(args):
    """Generate a .gitignore from one or more templates."""
    templates_list = fetch_template_list()
    if not templates_list:
        print("Cannot fetch template list.", file=sys.stderr)
        return 1

    parts = []
    for name in args.templates:
        match = find_template(name, templates_list)
        if not match:
            print(f"Template not found: '{name}'. Use 'list' to see available templates.", file=sys.stderr)
            return 1
        print(f"Using template: {match}", file=sys.stderr)
        source = fetch_template(match)
        if source is None:
            return 1
        parts.append(f"### {match} ###\n{source}")

    if args.extras:
        extras = "\n".join(args.extras)
        parts.append(f"### Custom rules ###\n{extras}")

    content = "\n\n".join(parts) + "\n"

    if args.output:
        outpath = args.output
    else:
        outpath = os.path.join(os.getcwd(), ".gitignore")

    if args.append and os.path.exists(outpath):
        with open(outpath, "a") as f:
            f.write("\n" + content)
        print(f"Appended to {outpath}", file=sys.stderr)
    elif args.stdout:
        print(content, end="")
    else:
        if os.path.exists(outpath) and not args.force:
            print(f"{outpath} already exists. Use --force to overwrite or --append to add.", file=sys.stderr)
            return 1
        with open(outpath, "w") as f:
            f.write(content)
        print(f"Written to {outpath}", file=sys.stderr)
    return 0


def cmd_detect(args):
    """Auto-detect project type and suggest templates."""
    directory = args.directory or os.getcwd()
    detected = []
    files = set()
    try:
        for item in os.listdir(directory):
            files.add(item.lower())
    except OSError as e:
        print(f"Cannot read directory: {e}", file=sys.stderr)
        return 1

    # Detection rules: (file/pattern, template name)
    rules = [
        ({"package.json"}, "Node"),
        ({"requirements.txt", "setup.py", "pyproject.toml", "pipfile"}, "Python"),
        ({"gemfile"}, "Ruby"),
        ({"cargo.toml"}, "Rust"),
        ({"go.mod"}, "Go"),
        ({"pom.xml", "build.gradle", "build.gradle.kts"}, "Java"),
        ({"composer.json"}, "Composer"),
        ({"pubspec.yaml"}, "Dart"),
        ({"mix.exs"}, "Elixir"),
        ({"project.clj"}, "Clojure"),
        ({"stack.yaml", "cabal.project"}, "Haskell"),
        ({"Package.swift"}, "Swift"),
        ({"terraform.tf", "main.tf"}, "Terraform"),
        ({"docker-compose.yml", "docker-compose.yaml", "dockerfile"}, "Global/Docker"),
        ({".idea"}, "JetBrains"),
        ({".vscode"}, "VisualStudioCode"),
        ({".env"}, "Global/DotEnv"),
    ]

    for patterns, template in rules:
        if patterns & files:
            detected.append(template)

    # Check extensions
    exts = set()
    for item in os.listdir(directory):
        _, ext = os.path.splitext(item)
        if ext:
            exts.add(ext.lower())

    ext_map = {
        ".cs": "VisualStudio",
        ".kt": "Java",
        ".scala": "Scala",
        ".r": "R",
        ".jl": "Julia",
        ".lua": "Lua",
        ".tex": "TeX",
        ".elm": "Elm",
    }
    for ext, template in ext_map.items():
        if ext in exts and template not in detected:
            detected.append(template)

    if detected:
        print("Detected project types:")
        for d in detected:
            print(f"  - {d}")
        print(f"\nSuggested command:", file=sys.stderr)
        templates_str = " ".join(detected)
        print(f"  python3 gitignore_gen.py generate {templates_str}", file=sys.stderr)
    else:
        print("No project type detected. Use 'list' to browse available templates.")
    return 0


def main():
    parser = argparse.ArgumentParser(
        description="Generate .gitignore files from GitHub templates",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""Examples:
  %(prog)s list                          # List all templates
  %(prog)s list --filter java            # Filter templates
  %(prog)s generate Python Node          # Combine Python + Node
  %(prog)s generate Rust --stdout        # Print to stdout
  %(prog)s generate Go --extra '*.local' # Add custom rules
  %(prog)s detect                        # Auto-detect project type
  %(prog)s detect /path/to/project       # Detect from path
""",
    )

    sub = parser.add_subparsers(dest="command", help="Command to run")

    # list
    p_list = sub.add_parser("list", help="List available gitignore templates")
    p_list.add_argument("--filter", "-f", help="Filter templates by name")

    # generate
    p_gen = sub.add_parser("generate", help="Generate a .gitignore file")
    p_gen.add_argument("templates", nargs="+", help="Template names (e.g., Python Node)")
    p_gen.add_argument("--output", "-o", help="Output file path (default: ./.gitignore)")
    p_gen.add_argument("--stdout", action="store_true", help="Print to stdout instead of file")
    p_gen.add_argument("--append", "-a", action="store_true", help="Append to existing .gitignore")
    p_gen.add_argument("--force", action="store_true", help="Overwrite existing .gitignore")
    p_gen.add_argument("--extra", "-e", dest="extras", action="append", help="Extra ignore patterns")

    # detect
    p_det = sub.add_parser("detect", help="Auto-detect project type from directory")
    p_det.add_argument("directory", nargs="?", help="Project directory (default: cwd)")

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        return 0

    if args.command == "list":
        return cmd_list(args)
    elif args.command == "generate":
        return cmd_generate(args)
    elif args.command == "detect":
        return cmd_detect(args)


if __name__ == "__main__":
    sys.exit(main() or 0)
