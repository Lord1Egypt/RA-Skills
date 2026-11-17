#!/usr/bin/env python3
"""Read-only structural checks; this does not prove meaning or runtime truth."""

import argparse
import json
import re
from pathlib import Path

SECTIONS = (
    "Goal and acceptance", "Current state and evidence", "Workspace and change ownership",
    "Decisions and boundaries", "Next step and validation", "On-demand references",
    "Coverage and gaps", "New-session handoff prompt",
)
PLACEHOLDERS = re.compile(
    r"<(?:project-root|compact-handoff|root|handoff-path|skill-dir)>"
    r"|\{\{[^\n{}]+\}\}|\[TODO:[^\n\]]*\]"
)


def without_fences(text: str) -> str:
    """Blank fenced examples while preserving offsets for section parsing."""
    lines = []
    marker = None
    length = 0
    for line in text.splitlines(keepends=True):
        fence = re.match(r"^\s*(`{3,}|~{3,})(.*)$", line)
        if fence:
            run, suffix = fence.groups()
            if marker is None:
                marker, length = run[0], len(run)
            elif run[0] == marker and len(run) >= length and not suffix.strip():
                marker = None
            lines.append(re.sub(r"[^\r\n]", " ", line))
        else:
            lines.append(line if marker is None else re.sub(r"[^\r\n]", " ", line))
    return "".join(lines)


def decode_path(path: str) -> str:
    """Decode percent-encoded UTF-8 path bytes without URL/network libraries."""
    def decode_match(match: re.Match) -> str:
        raw = bytes.fromhex(match.group(0).replace("%", ""))
        return raw.decode("utf-8", errors="replace")

    return re.sub(r"(?:%[0-9a-fA-F]{2})+", decode_match, path)


def check_handoff(path: Path, project_root: Path) -> dict:
    errors = []
    result = {
        "status": "fail", "characters": None, "opener_characters": None,
        "local_links_checked": 0, "errors": errors,
        "limitations": [
            "Structural success does not prove semantic completeness, runtime facts, or authorization.",
            "Character count is not token count; only explicit Markdown link existence is checked.",
            "Anchor targets are not checked and linked documents are not read.",
        ],
    }
    if not project_root.is_dir():
        errors.append("Project root does not exist or is not a directory.")
        return result
    if not path.is_file():
        errors.append("Handoff file does not exist or is not a file.")
        return result
    try:
        content = path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        errors.append(f"Could not read the handoff: {type(exc).__name__}.")
        return result
    result["characters"] = len(content)
    if len(content) > 6000:
        errors.append("Handoff exceeds 6,000 characters; preserve critical content and review it manually.")
    if PLACEHOLDERS.search(content):
        errors.append("A known unfilled placeholder remains.")
    visible = without_fences(content)
    headings = list(re.finditer(r"^##[ \t]+([^\n]+)$", visible, re.MULTILINE))
    sections = {}
    for index, match in enumerate(headings):
        title = match.group(1).strip()
        end = headings[index + 1].start() if index + 1 < len(headings) else len(content)
        if title in sections:
            errors.append(f"Duplicate section: {title}")
        sections[title] = content[match.end():end].strip()
    for title in SECTIONS:
        if title not in sections or not sections[title]:
            errors.append(f"Missing or empty section: {title}")
    opener = sections.get("New-session handoff prompt", "")
    result["opener_characters"] = len(opener)
    if len(opener) > 1000:
        errors.append("New-session prompt exceeds 1,000 characters.")
    if str(project_root) not in opener or str(path) not in opener:
        errors.append("The prompt must contain the actual absolute project-root and handoff paths.")
    for target in re.findall(r"\[[^\]\n]*\]\((<[^>\n]+>|[^\s)]+)\)", visible):
        target = target.strip("<>")
        link_path = target.split("#", 1)[0].split("?", 1)[0]
        if not link_path or link_path.startswith("//") or re.match(r"^[A-Za-z][A-Za-z0-9+.-]*:", link_path):
            continue
        link = Path(decode_path(link_path))
        if not link.is_absolute():
            link = path.parent / link
        result["local_links_checked"] += 1
        if not link.exists():
            errors.append(f"Local link does not exist: {target}")
    result["status"] = "structural-pass" if not errors else "fail"
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("handoff", type=Path)
    parser.add_argument("--project-root", required=True, type=Path)
    args = parser.parse_args()
    try:
        result = check_handoff(args.handoff.expanduser().resolve(), args.project_root.expanduser().resolve())
    except (OSError, ValueError) as exc:
        result = {"status": "fail", "errors": [f"Path check failed: {type(exc).__name__}."]}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["status"] == "structural-pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
