#!/usr/bin/env python3
"""Update pack.md — scan a package's sub-skills and refresh the registry."""

import argparse
import re
import sys
from pathlib import Path

#!/usr/bin/env python3
"""Update pack.md — scan a package's sub-skills and refresh the registry."""

import argparse
import re
import sys
from pathlib import Path

# Resolve skills directory: this script lives at skills/<package-skill>/scripts/
SKILLS_DIR = Path(__file__).resolve().parents[2]

SAFE_NAME_RE = re.compile(r'^[a-zA-Z0-9_-]+$')


def parse_frontmatter(text: str) -> dict:
    """Extract YAML frontmatter fields from a SKILL.md."""
    m = re.match(r'^---\s*\n(.*?)\n---', text, re.DOTALL)
    if not m:
        return {}
    fm = {}
    for line in m.group(1).splitlines():
        if ':' in line:
            key, _, val = line.partition(':')
            val = val.strip().strip('"').strip("'")
            fm[key.strip()] = val
    return fm


def read_skill_description(skill_path: Path) -> tuple[str, str]:
    """Return (name, description) from a skill's SKILL.md frontmatter."""
    skill_md = skill_path / "SKILL.md"
    if not skill_md.exists():
        print(f"  Warning: {skill_md} not found", file=sys.stderr)
        return skill_path.name, ""
    text = skill_md.read_text(encoding="utf-8")
    fm = parse_frontmatter(text)
    return fm.get("name", skill_path.name), fm.get("description", "")


def scan_subs(package_dir: Path) -> list[dict]:
    """Scan sub/*/SKILL.md and return list of {name, description, dir}."""
    subs = []
    sub_dir = package_dir / "sub"
    if not sub_dir.exists():
        return subs
    for child in sorted(sub_dir.iterdir()):
        if child.is_dir() and (child / "SKILL.md").exists():
            name, desc = read_skill_description(child)
            subs.append({"name": name, "description": desc, "dir": child.name})
    return subs


def write_pack_md(package_dir: Path, subs: list[dict]):
    """Write pack.md registry."""
    package_name = package_dir.name
    lines = [f"# {package_name} Registry\n"]
    lines.append(f"Auto-generated. {len(subs)} sub-skills.\n")
    for s in subs:
        lines.append(f"- **{s['name']}** — {s['description']}")
    (package_dir / "pack.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"  Updated pack.md ({len(subs)} entries)")


def update(package_name: str):
    """Scan and update pack.md for a package."""
    if not SAFE_NAME_RE.match(package_name):
        print(f"Error: invalid package name '{package_name}'", file=sys.stderr)
        sys.exit(1)
    package_dir = (SKILLS_DIR / package_name).resolve()
    if not str(package_dir).startswith(str(SKILLS_DIR)):
        print(f"Error: path traversal detected", file=sys.stderr)
        sys.exit(1)
    if not package_dir.exists():
        print(f"Error: package '{package_name}' not found", file=sys.stderr)
        sys.exit(1)

    subs = scan_subs(package_dir)
    write_pack_md(package_dir, subs)
    print(f"Package '{package_name}': {len(subs)} sub-skills found.")
    for s in subs:
        print(f"  - {s['name']}")


def main():
    parser = argparse.ArgumentParser(description="Update pack.md for a skill package")
    parser.add_argument("package", help="Package name to scan")
    args = parser.parse_args()
    update(args.package)


if __name__ == "__main__":
    main()
