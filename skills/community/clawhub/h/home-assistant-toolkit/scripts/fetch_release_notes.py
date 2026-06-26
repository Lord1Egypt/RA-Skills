#!/usr/bin/env python3
"""
Fetch latest Home Assistant release notes and generate a reference file.

Usage:
  python3 fetch_release_notes.py                        # fetches last 3 releases
  python3 fetch_release_notes.py --last 5               # last 5 releases
  python3 fetch_release_notes.py --version 2026.5       # specific version

All arguments optional. Output defaults to references/ha-release-notes.md.

Sources:
  - GitHub releases API (public, read-only, no auth required)
"""

import argparse
import json
import os
import sys
import re
from datetime import datetime

try:
    import urllib.request
    import urllib.error
except ImportError:
    print("Error: requires Python 3 with urllib", file=sys.stderr)
    sys.exit(1)


HA_GITHUB_RELEASES = "https://api.github.com/repos/home-assistant/core/releases"


def fetch_url(url: str, headers: dict = None) -> str:
    """Fetch URL content as string."""
    hdrs = {"User-Agent": "HA-Skill-Updater/1.0"}
    if headers:
        hdrs.update(headers)
    req = urllib.request.Request(url, headers=hdrs)
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return resp.read().decode("utf-8", errors="replace")
    except Exception as e:
        print(f"Error fetching {url}: {e}", file=sys.stderr)
        return ""


def fetch_github_releases(count: int = 5) -> list:
    """Fetch recent releases from GitHub API."""
    url = f"{HA_GITHUB_RELEASES}?per_page={count}"
    data = fetch_url(url)
    if not data:
        return []
    try:
        releases = json.loads(data)
        # Filter to stable releases only (no beta/rc)
        stable = []
        for r in releases:
            tag = r.get("tag_name", "")
            if r.get("prerelease"):
                continue
            if "b" in tag or "rc" in tag:
                continue
            stable.append({
                "tag": tag,
                "name": r.get("name", tag),
                "published": r.get("published_at", ""),
                "url": r.get("html_url", ""),
                "body": r.get("body", ""),
            })
        return stable
    except json.JSONDecodeError:
        return []


def filter_changelog(body: str) -> str:
    """
    Filter the GitHub release body to keep only relevant parts:
    - Sections related to Breaking Changes
    - Lines containing (breaking-change)
    - Exclude lists of PRs and user links at the end
    """
    if not body:
        return ""
        
    lines = body.split("\n")
    filtered_lines = []
    
    in_breaking_section = False
    
    for line in lines:
        line_strip = line.strip()
        if not line_strip:
            if filtered_lines and filtered_lines[-1]: # Keep only single newlines
                filtered_lines.append("")
            continue
            
        # Ignore link definitions like [#123]: ... or [@user]: ...
        if re.match(r'^\[(#?\w+)\]:', line_strip):
            continue

        lower = line_strip.lower()
        
        # Detect Breaking Changes section header
        if line_strip.startswith("#") and ("breaking change" in lower or "backward-incompatible" in lower):
            in_breaking_section = True
            filtered_lines.append(line)
            continue
        elif line_strip.startswith("#") and in_breaking_section:
            # Another section started
            in_breaking_section = False
            
        # Keep lines in breaking section or lines with (breaking-change) tag
        if in_breaking_section:
            filtered_lines.append(line)
        elif "(breaking-change)" in lower:
            filtered_lines.append(line)
            
    # If no breaking changes found, keep the first paragraph as a summary
    if not [l for l in filtered_lines if l.strip() and not l.strip().startswith("#")]:
        for line in lines:
            ls = line.strip()
            if ls and not ls.startswith("#") and not ls.startswith("["):
                filtered_lines.append(line)
                break
    
    result = "\n".join(filtered_lines).strip()
    return result if result else "*No breaking changes or detailed summary available.*"


def generate_release_reference(releases: list, output_path: str, user_version: str = None, max_body_length: int = 15000):
    """Generate the release notes reference markdown file."""
    lines = []
    lines.append("# Home Assistant Release Notes Reference")
    lines.append("")
    lines.append(f"*Auto-generated on {datetime.now().strftime('%Y-%m-%d %H:%M')}*")
    if user_version:
        lines.append(f"*User's HA version: **{user_version}** — only releases up to this version are included*")
    lines.append(f"*Covers {len(releases)} release(s)*")
    lines.append("")
    lines.append("To update this file, run:")
    lines.append("```bash")
    lines.append("python3 scripts/fetch_release_notes.py --last 3 --output references/ha-release-notes.md")
    lines.append("```")
    lines.append("")
    lines.append("---")
    lines.append("")

    for rel in releases:
        tag = rel.get("tag", "unknown")
        name = rel.get("name", tag)
        published = rel.get("published", "")
        url = rel.get("url", "")

        lines.append(f"## {name}")
        lines.append("")
        if published:
            pub_date = published[:10] if published else ""
            lines.append(f"**Released**: {pub_date}")
        if url:
            lines.append(f"**GitHub**: {url}")

        # Blog link — use published date for the day (HA blogs on release day)
        parts = tag.split(".")
        if len(parts) >= 2 and published:
            pub_parts = published[:10].split("-")  # YYYY-MM-DD
            day = pub_parts[2] if len(pub_parts) == 3 else "01"
            blog_url = (f"https://www.home-assistant.io/blog/{parts[0]}/"
                       f"{parts[1].zfill(2)}/{day}/release-{parts[0]}{parts[1]}/")
            lines.append(f"**Blog**: {blog_url}")

        lines.append("")

        # Include filtered release body
        body = rel.get("body", "")
        if body:
            body_clean = filter_changelog(body)
            if len(body_clean) > max_body_length:
                body_clean = body_clean[:max_body_length] + f"\n\n*[Truncated at {max_body_length} chars]*"
            lines.append(body_clean)
            lines.append("")

        lines.append("---")
        lines.append("")

    # Footer with useful links
    lines.append("## Useful Links")
    lines.append("")
    lines.append("- Release schedule: https://www.home-assistant.io/faq/release/")
    lines.append("- All releases: https://github.com/home-assistant/core/releases")
    lines.append("- Blog: https://www.home-assistant.io/blog/")
    lines.append("- Breaking changes: check each release's blog post")
    lines.append("- Security advisories: https://www.home-assistant.io/security")

    output = "\n".join(lines)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(output)

    print(f"Release notes written to {output_path}", file=sys.stderr)
    print(f"Covered releases: {', '.join(r['tag'] for r in releases)}", file=sys.stderr)


def parse_ha_version(version_str: str):
    """Parse HA version string into comparable tuple. '2026.4.0' -> (2026, 4, 0)"""
    try:
        parts = version_str.split(".")
        return tuple(int(p) for p in parts[:3])
    except (ValueError, AttributeError):
        return (0, 0, 0)


def load_user_version():
    """Load user's HA version from ha-state.json."""
    state_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                              "references", "ha-state.json")
    try:
        with open(state_path) as f:
            state = json.load(f)
            return state.get("ha_version")
    except Exception:
        return None


def save_fetch_timestamp():
    """Update last_release_fetch in ha-state.json."""
    state_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                              "references", "ha-state.json")
    try:
        state = {}
        if os.path.exists(state_path):
            with open(state_path) as f:
                state = json.load(f)
        state["last_release_fetch"] = datetime.now().isoformat()
        with open(state_path, "w") as f:
            json.dump(state, f, indent=2)
    except Exception:
        pass


def main():
    # Default output path resolves relative to the project root
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    default_output = os.path.join(project_root, "references", "ha-release-notes.md")

    parser = argparse.ArgumentParser(description="Fetch HA release notes")
    parser.add_argument("--version", help="Specific version to fetch (e.g., 2026.4)")
    parser.add_argument("--up-to", help="Max version to include (e.g., 2026.4.0). "
                        "If omitted, reads from ha-state.json (set by scan_integrations.py)")
    parser.add_argument("--last", type=int, default=3, help="Fetch last N applicable releases (default: 3)")
    parser.add_argument("--ignore-version", action="store_true",
                        help="Ignore user's HA version, fetch latest releases regardless")
    parser.add_argument("--output", default=default_output, help="Output file")
    parser.add_argument("--max-body-length", type=int, default=15000, help="Truncate release body at N characters (default: 15000)")
    args = parser.parse_args()

    # Determine the user's version ceiling
    user_version = None
    if args.up_to:
        user_version = args.up_to
    elif not args.ignore_version:
        user_version = load_user_version()

    if user_version:
        user_ver_tuple = parse_ha_version(user_version)
        print(f"User HA version: {user_version}", file=sys.stderr)
        print(f"Will only include releases <= {user_version}", file=sys.stderr)
    else:
        user_ver_tuple = None
        print("No user version detected — fetching latest releases.", file=sys.stderr)
        print("Run scan_integrations.py first, or use --up-to / --ignore-version", file=sys.stderr)

    print("Fetching Home Assistant releases from GitHub...", file=sys.stderr)
    all_releases = fetch_github_releases(count=max(args.last * 3, 20))

    if args.version:
        # Filter to specific version only
        releases = [r for r in all_releases if r["tag"].startswith(args.version)]
        if not releases:
            print(f"Version {args.version} not found in recent releases", file=sys.stderr)
            sys.exit(1)
    else:
        # Filter by user version ceiling
        if user_ver_tuple:
            releases = [
                r for r in all_releases
                if parse_ha_version(r["tag"]) <= user_ver_tuple
            ]
            if not releases:
                print(f"No releases found <= {user_version}. "
                      f"Available: {', '.join(r['tag'] for r in all_releases[:5])}",
                      file=sys.stderr)
                print("Try --ignore-version to fetch latest anyway.", file=sys.stderr)
                sys.exit(1)
        else:
            releases = all_releases

        releases = releases[:args.last]

    if not releases:
        print("No releases found!", file=sys.stderr)
        sys.exit(1)

    # Add user version info to the header
    generate_release_reference(releases, args.output, user_version=user_version, max_body_length=args.max_body_length)
    save_fetch_timestamp()


if __name__ == "__main__":
    main()
