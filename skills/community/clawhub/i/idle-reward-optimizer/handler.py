import json
import re
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent
SKILL_FILE = SKILL_DIR / "SKILL.md"


def _read_skill_file():
    return SKILL_FILE.read_text(encoding="utf-8")


def _split_frontmatter(content):
    match = re.match(r"^---\s*\n(.*?)\n---\s*\n?(.*)$", content, re.DOTALL)
    if match:
        return match.group(1), match.group(2)
    return "", content


def _parse_frontmatter(frontmatter):
    meta = {}
    for line in frontmatter.splitlines():
        line = line.strip()
        if not line or ":" not in line:
            continue
        key, value = line.split(":", 1)
        meta[key.strip()] = value.strip().strip('"').strip("'")
    return meta


def _load_skill_meta(skill_name):
    content = _read_skill_file()
    frontmatter, _ = _split_frontmatter(content)
    parsed = _parse_frontmatter(frontmatter)
    return {
        "name": parsed.get("name", skill_name or SKILL_DIR.name),
        "description": parsed.get("description", ""),
    }


def _load_prompt_template(skill_name):
    del skill_name
    content = _read_skill_file()
    _, body = _split_frontmatter(content)
    return body.strip()


def _extract_title(body):
    match = re.search(r"^#\s+(.+)$", body, re.MULTILINE)
    if match:
        return match.group(1).strip()
    return SKILL_DIR.name.replace("-", " ").title()


def _extract_chinese_name(body):
    match = re.search(r"^Chinese name:\s*(.+)$", body, re.MULTILINE | re.IGNORECASE)
    return match.group(1).strip() if match else ""


def _parse_sections(body):
    sections = {}
    pattern = re.compile(r"^##\s+(.+?)\n(.*?)(?=^##\s+|\Z)", re.MULTILINE | re.DOTALL)
    for heading, content in pattern.findall(body):
        sections[heading.strip().lower()] = content.strip()
    return sections


def _normalize_input(user_input):
    if user_input is None:
        return ""
    if isinstance(user_input, str):
        return user_input.strip()
    return json.dumps(user_input, ensure_ascii=False, indent=2, sort_keys=True)


def _extract_items(text):
    items = []
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        if re.match(r"^[-*]\s+", line):
            items.append(re.sub(r"^[-*]\s+", "", line))
        elif re.match(r"^\d+\.\s+", line):
            items.append(re.sub(r"^\d+\.\s+", "", line))
    if items:
        return items
    collapsed = " ".join(line.strip() for line in text.splitlines() if line.strip())
    return [collapsed] if collapsed else []


def _limit_for_mode(mode):
    normalized = (mode or "guide").strip().lower()
    if normalized in {"brief", "compact", "quick"}:
        return 2
    if normalized in {"full", "deep", "extended"}:
        return None
    return 4


def _render_list(title, items, mode, ordered=False):
    limit = _limit_for_mode(mode)
    chosen = items if limit is None else items[:limit]
    if not chosen:
        return []
    lines = [f"## {title}"]
    for index, item in enumerate(chosen, start=1):
        prefix = f"{index}." if ordered else "-"
        lines.append(f"{prefix} {item}")
    lines.append("")
    return lines


def handle(args):
    if not isinstance(args, dict):
        args = {"input": args}

    skill_name = args.get("skill_name", "")
    user_input = args.get("input", "")
    mode = args.get("mode", "guide")

    meta = _load_skill_meta(skill_name)
    template = _load_prompt_template(skill_name)

    normalized_mode = (mode or "guide").strip().lower()
    if normalized_mode == "meta":
        return {"result": json.dumps(meta, ensure_ascii=False, indent=2)}
    if normalized_mode in {"prompt", "template"}:
        return {"result": template}

    sections = _parse_sections(template)
    title = _extract_title(template)
    chinese_name = _extract_chinese_name(template)
    normalized_input = _normalize_input(user_input)

    lines = [f"# {title}"]
    lines.append(f"- Skill slug: {meta['name']}")
    if chinese_name:
        lines.append(f"- Chinese name: {chinese_name}")
    lines.append(f"- Mode: {mode}")
    if meta["description"]:
        lines.append(f"- Summary: {meta['description']}")
    lines.append("")

    if normalized_input:
        lines.append("## User context")
        lines.append(normalized_input)
        lines.append("")

    lines.extend(_render_list("Purpose", _extract_items(sections.get("purpose", "")), mode))
    lines.extend(_render_list("Use cases", _extract_items(sections.get("use this skill when", "")), mode))
    lines.extend(_render_list("Inputs to collect", _extract_items(sections.get("inputs to collect", "")), mode))
    lines.extend(_render_list("Workflow", _extract_items(sections.get("workflow", "")), mode, ordered=True))
    lines.extend(_render_list("Output format", _extract_items(sections.get("output format", "")), mode))
    lines.extend(_render_list("Quality bar", _extract_items(sections.get("quality bar", "")), mode))
    lines.extend(_render_list("Edge cases and limits", _extract_items(sections.get("edge cases and limits", "")), mode))
    lines.extend(_render_list("Compatibility notes", _extract_items(sections.get("compatibility notes", "")), mode))

    section_count = len([name for name in sections if sections[name]])
    lines.append("## Prompt template status")
    lines.append(f"- Loaded from SKILL.md with {section_count} structured sections.")
    lines.append("- This handler returns a descriptive guidance card and does not perform external actions.")

    return {"result": "\n".join(lines).strip()}


if __name__ == "__main__":
    print(json.dumps(handle({"skill_name": SKILL_DIR.name, "input": "demo", "mode": "guide"}), ensure_ascii=False, indent=2))
