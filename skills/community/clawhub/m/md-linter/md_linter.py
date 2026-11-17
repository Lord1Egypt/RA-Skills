#!/usr/bin/env python3
"""
Markdown Linter & Fixer — lint, check, and auto-fix Markdown files.

Commands: check, toc, links, frontmatter, format
Zero dependencies (Python stdlib only).
"""

import sys
import os
import re
import json
import urllib.request
import urllib.error
import socket


# ── helpers ──────────────────────────────────────────────────────────────

def read_file(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def write_file(path, content):
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


def split_frontmatter(text):
    """Split text into (frontmatter_yaml, body) or (None, text) if no frontmatter."""
    m = re.match(r"^---\s*\n(.*?\n)---\s*\n(.*)", text, re.DOTALL)
    if m:
        return m.group(1).strip(), m.group(2)
    return None, text


def heading_re():
    return re.compile(r"^(#{1,6})\s+(.+)$", re.MULTILINE)


# ── commands ─────────────────────────────────────────────────────────────

def cmd_check(args):
    """Lint a Markdown file for common issues."""
    exit_code = 0
    for path in args.paths:
        issues = lint_file(path)
        if issues:
            print(f"\u274c {path}: {len(issues)} issue(s)")
            for issue in issues:
                print(f"  line {issue['line']}: {issue['message']}")
            exit_code = 1
        else:
            print(f"\u2705 {path}: no issues found")
    sys.exit(exit_code)


def lint_file(path):
    """Run all lint checks on a single file and return a list of issue dicts."""
    text = read_file(path)
    lines = text.split("\n")
    issues = []

    # Check 1: Trailing whitespace
    for i, line in enumerate(lines, 1):
        if line.rstrip("\r") != line.rstrip("\r").rstrip() and line.strip():
            issues.append({"line": i, "message": "Trailing whitespace"})

    # Check 2: Multiple blank lines
    for i in range(len(lines) - 2):
        if lines[i].strip() == "" and lines[i + 1].strip() == "" and lines[i + 2].strip() == "":
            issues.append({"line": i + 1, "message": "Multiple consecutive blank lines"})
            break  # report once

    # Check 3: Heading spacing (no space after #)
    for i, line in enumerate(lines, 1):
        if re.match(r"^#+[A-Za-z]", line):
            issues.append({"line": i, "message": "Missing space after heading marker (use '# title')"})

    # Check 4: Heading level jumps (e.g. # then ### without ##)
    headings = []
    for i, line in enumerate(lines, 1):
        m = re.match(r"^(#{1,6})\s", line)
        if m:
            headings.append((i, len(m.group(1))))
    for j in range(1, len(headings)):
        prev_level = headings[j - 1][1]
        curr_level = headings[j][1]
        if curr_level > prev_level + 1:
            issues.append({"line": headings[j][0],
                           "message": f"Heading level jumps from {prev_level} to {curr_level} (expected max {prev_level + 1})"})

    # Check 5: Broken reference-style links [text][ref] where [ref] is undefined
    refs = set(re.findall(r"\[([^\]]+)\]\[([^\]]*)\]", text))
    defined_refs = set()
    for m in re.finditer(r"^\[([^\]]+)\]:\s*\S+", text, re.MULTILINE):
        defined_refs.add(m.group(1))
    for display, ref in refs:
        target = ref if ref else display
        if target not in defined_refs:
            idx = text.find(f"[{display}][{ref}]")
            line_num = text[:idx].count("\n") + 1 if idx >= 0 else "?"
            issues.append({"line": line_num, "message": f"Undefined reference link '[{display}][{ref}]'"})

    return issues


def cmd_toc(args):
    """Generate a table of contents from headings."""
    text = read_file(args.path)
    _, body = split_frontmatter(text)

    headings = []
    for m in re.finditer(r"^(#{1,6})\s+(.+)$", body, re.MULTILINE):
        level = len(m.group(1)) - 1  # 0-indexed depth
        title = m.group(2).strip()
        anchor = title.lower().replace(" ", "-")
        anchor = re.sub(r"[^a-z0-9\-]", "", anchor)
        headings.append({"level": level, "title": title, "anchor": anchor})

    if not headings:
        print("No headings found.")
        sys.exit(0)

    # Build TOC lines
    toc_lines = ["## Table of Contents", ""]
    for h in headings:
        indent = "  " * h["level"]
        toc_lines.append(f'{indent}- [{h["title"]}](#{h["anchor"]})')
    toc_text = "\n".join(toc_lines)

    if args.insert:
        # Insert after the frontmatter or at the top
        fm_yaml, body = split_frontmatter(text)
        # Check if TOC already exists (remove old one)
        body = re.sub(r"^## Table of Contents\n.*?(?=\n#|\Z)", "", body, flags=re.DOTALL).strip()
        new_body = toc_text + "\n\n" + body
        if fm_yaml:
            new_text = f"---\n{fm_yaml}\n---\n\n{new_body}"
        else:
            new_text = new_body
        write_file(args.path, new_text)
        print(f"\u2705 TOC inserted into {args.path}")
    else:
        print(toc_text)


def cmd_links(args):
    """Check for broken links in a Markdown file."""
    text = read_file(args.path)
    issues = []
    exit_code = 0

    # Check local file references in [text](link) patterns
    for m in re.finditer(r"\[([^\]]+)\]\(([^)]+)\)", text):
        link = m.group(2)
        display = m.group(1)
        line_num = text[: m.start()].count("\n") + 1

        # Skip external URLs, anchors, mailto, and reference links
        if link.startswith(("http://", "https://", "#", "mailto:")):
            continue
        # Don't validate absolute system paths
        if link.startswith("/") or link.startswith(("C:", "c:")):
            continue

        # Check relative file existence
        base_dir = os.path.dirname(args.path) or "."
        target = os.path.normpath(os.path.join(base_dir, link))
        if not os.path.exists(target):
            issues.append({"line": line_num, "link": link, "display": display, "status": "FILE NOT FOUND"})
            exit_code = 1

    if args.check_external:
        # Check HTTP links
        for m in re.finditer(r"\[([^\]]+)\]\(((?:https?://)[^)]+)\)", text):
            link = m.group(2)
            display = m.group(1)
            line_num = text[: m.start()].count("\n") + 1
            try:
                req = urllib.request.Request(link, method="HEAD")
                req.add_header("User-Agent", "md-linter/1.0")
                resp = urllib.request.urlopen(req, timeout=5)
                if resp.status >= 400:
                    issues.append({"line": line_num, "link": link, "display": display, "status": f"HTTP {resp.status}"})
                    exit_code = 1
            except (urllib.error.URLError, socket.timeout, ValueError) as e:
                issues.append({"line": line_num, "link": link, "display": display, "status": f"ERROR: {e}"})
                exit_code = 1

    if issues:
        for issue in issues:
            print(f"  line {issue['line']}: [{issue['display']}]({issue['link']}) \u2192 {issue['status']}")
    else:
        print(f"\u2705 {args.path}: all links OK")

    sys.exit(exit_code)


def cmd_frontmatter(args):
    """Validate YAML frontmatter fields."""
    text = read_file(args.path)
    fm_yaml, body = split_frontmatter(text)
    issues = []
    exit_code = 0

    if fm_yaml is None:
        print(f"\u274c {args.path}: no YAML frontmatter found")
        sys.exit(1)

    # Parse basic YAML (key: value pairs)
    fields = {}
    for line in fm_yaml.split("\n"):
        m = re.match(r"^([a-zA-Z_][a-zA-Z0-9_\-]*)\s*:\s*(.*)", line)
        if m:
            fields[m.group(1)] = m.group(2).strip()

    # Check required fields
    required = args.require.split(",") if args.require else []
    for field in required:
        field = field.strip()
        if field not in fields:
            issues.append(f"Missing required field: '{field}'")
            exit_code = 1

    if args.expect:
        for pair in args.expect.split(","):
            pair = pair.strip()
            if "=" not in pair:
                continue
            key, expected = pair.split("=", 1)
            actual = fields.get(key.strip())
            if actual != expected.strip():
                issues.append(f"Field '{key.strip()}': expected '{expected.strip()}', got '{actual}'")
                exit_code = 1

    if issues:
        for issue in issues:
            print(f"  \u274c {issue}")
    else:
        print(f"\u2705 {args.path}: frontmatter valid")

    sys.exit(exit_code)


def cmd_format(args):
    """Auto-fix common Markdown formatting issues."""
    text = read_file(args.path)
    original = text
    changes = []

    # Fix 1: Remove trailing whitespace
    fixed = []
    for line in text.split("\n"):
        stripped = line.rstrip()
        if stripped != line:
            changes.append("Removed trailing whitespace")
        fixed.append(stripped)
    text = "\n".join(fixed)

    # Fix 2: Ensure space after heading markers (#Title -> # Title)
    text = re.sub(r"^(#+)([A-Za-z])", r"\1 \2", text, flags=re.MULTILINE)
    if text != original:
        changes.append("Fixed heading spacing")

    # Fix 3: Ensure blank line before headings (except first line or after frontmatter)
    text = re.sub(r"([^\n])\n(#{1,6}\s)", r"\1\n\n\2", text)

    # Fix 4: Normalize list markers (ensure space after - or *)
    text = re.sub(r"^(\s*[-*+])([A-Za-z0-9])", r"\1 \2", text, flags=re.MULTILINE)

    if text == original:
        print(f"\u2705 {args.path}: already formatted")
        return

    if args.write:
        write_file(args.path, text)
        print(f"\u2705 {args.path}: {len(changes)} fix(es) applied")
    else:
        print(text)


# ── argparse ─────────────────────────────────────────────────────────────

def build_parser():
    import argparse
    parser = argparse.ArgumentParser(
        description="Markdown Linter & Fixer \u2014 lint, check, auto-fix Markdown files"
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("check", help="Lint Markdown files for issues")
    p.add_argument("paths", nargs="+", metavar="FILE", help="Markdown files to check")
    p.add_argument("--verbose", "-v", action="store_true", help="Verbose output")

    p = sub.add_parser("toc", help="Generate or insert a table of contents")
    p.add_argument("path", help="Markdown file path")
    p.add_argument("--insert", action="store_true", help="Insert TOC into the file")

    p = sub.add_parser("links", help="Check for broken links")
    p.add_argument("path", help="Markdown file path")
    p.add_argument("--check-external", "-e", action="store_true", help="Check HTTP links via HEAD requests")

    p = sub.add_parser("frontmatter", help="Validate YAML frontmatter")
    p.add_argument("path", help="Markdown file path")
    p.add_argument("--require", default="", help="Comma-separated required fields")
    p.add_argument("--expect", default="", help="Comma-separated key=value expectations")

    p = sub.add_parser("format", help="Auto-fix formatting issues")
    p.add_argument("path", help="Markdown file path")
    p.add_argument("--write", "-w", action="store_true", help="Write changes to file")

    sub.add_parser("self-test", help="Run built-in self tests")

    return parser


def _self_test():
    """Real test of split_frontmatter + lint_file core. Returns 0/1."""
    import tempfile, os

    # 1. split_frontmatter on a file with frontmatter.
    fm_md = "---\nname: x\nversion: 1.0.0\n---\n# Heading\n\nbody text\n"
    fm, body = split_frontmatter(fm_md)
    if fm is None or "name: x" not in fm:
        print("self-test: FAIL (split_frontmatter frontmatter)")
        return 1
    if "# Heading" not in body:
        print("self-test: FAIL (split_frontmatter body)")
        return 1

    # 2. lint_file detects trailing whitespace + heading space issue.
    d = tempfile.mkdtemp(prefix="md_selftest_")
    try:
        p = os.path.join(d, "bad.md")
        with open(p, "w", encoding="utf-8") as f:
            f.write("#Heading-no-space   \n\nnormal line\n")
        issues = lint_file(p)
        messages = " ".join(i["message"] for i in issues)
        if "Trailing whitespace" not in messages:
            print("self-test: FAIL (trailing whitespace not detected)")
            return 1
        if "space after heading" not in messages:
            print("self-test: FAIL (heading spacing not detected)")
            return 1
    finally:
        import shutil
        shutil.rmtree(d, ignore_errors=True)

    print("self-test: PASS")
    return 0


def main():
    parser = build_parser()
    args = parser.parse_args()
    if args.command == "self-test":
        sys.exit(_self_test())
    cmds = {
        "check": cmd_check,
        "toc": cmd_toc,
        "links": cmd_links,
        "frontmatter": cmd_frontmatter,
        "format": cmd_format,
    }
    cmds[args.command](args)


if __name__ == "__main__":
    main()
