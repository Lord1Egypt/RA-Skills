from __future__ import annotations

from dataclasses import dataclass
import re


PLACEHOLDER_RE = re.compile(r"\[(?:INSERT VALUE|数据待填写)\]")
DATE_PATTERNS = [
    re.compile(r"^\d{4}-\d{2}-\d{2}$"),
    re.compile(r"^\d{4}-\d{2}$"),
    re.compile(r"^\d{4}$"),
    re.compile(r"^Q[1-4] \d{4}$"),
    re.compile(r"^Day \d+$"),
    re.compile(r"^Week \d+$"),
    re.compile(r"^Month \d+$"),
]
RECOMMENDED_FRONTMATTER_FIELDS = [
    "title",
    "lang",
    "report_class",
    "audience",
    "decision_goal",
    "must_include",
    "must_avoid",
    "abstract",
]


@dataclass(frozen=True)
class IRBlock:
    tag: str
    params: dict[str, str]
    body: str


def result(status: str, auto_downgrade_target: str | None = None) -> dict[str, str]:
    data = {"status": status}
    if auto_downgrade_target:
        data["auto_downgrade_target"] = auto_downgrade_target
    return data


def non_empty_lines(body: str) -> list[str]:
    return [line.rstrip() for line in body.splitlines() if line.strip()]


def has_real_number(text: str) -> bool:
    return bool(re.search(r"\d", text)) and not PLACEHOLDER_RE.search(text)


def is_short_kpi_value(value: str) -> bool:
    stripped = value.strip()
    if PLACEHOLDER_RE.search(stripped):
        return False
    if not has_real_number(stripped):
        return False
    if len(re.findall(r"[A-Za-z]+", stripped)) > 3:
        return False
    cjk_count = len(re.findall(r"[\u4e00-\u9fff]", stripped))
    if cjk_count > 8:
        return False
    return len(stripped) <= 24


def parse_kpi_items(body: str) -> list[dict[str, str]] | None:
    lines = non_empty_lines(body)
    if not lines:
        return None

    if lines[0].strip() == "items:":
        items: list[dict[str, str]] = []
        current: dict[str, str] | None = None
        for raw in lines[1:]:
            line = raw.strip()
            if raw.startswith("  - "):
                if current:
                    items.append(current)
                match = re.match(r"- label:\s*(.+)$", line)
                if not match:
                    return None
                current = {"label": match.group(1).strip()}
                continue
            if current is None or not raw.startswith("    "):
                return None
            field_match = re.match(r"(value|delta|note):\s*(.+)$", line)
            if not field_match:
                return None
            current[field_match.group(1)] = field_match.group(2).strip()
        if current:
            items.append(current)
        return items or None

    short_line_items: list[dict[str, str]] = []
    for line in lines:
        match = re.match(r"^- ([^:]+): (.+?)(?: ([↑↓→].+))?$", line)
        if not match:
            return None
        short_line_items.append(
            {
                "label": match.group(1).strip(),
                "value": match.group(2).strip(),
                "delta": (match.group(3) or "").strip(),
            }
        )
    return short_line_items


def validate_kpi(body: str, report_class: str = "data") -> dict[str, str]:
    items = parse_kpi_items(body)
    if not items:
        return result("invalid_syntax", "callout")

    if any("value" not in item or not item["value"] for item in items):
        return result("invalid_syntax", "callout")

    if any(not is_short_kpi_value(item["value"]) for item in items):
        return result("invalid_semantics", "callout")

    return result("valid")


def validate_timeline(body: str) -> dict[str, str]:
    for line in non_empty_lines(body):
        match = re.match(r"^- ([^:]+): (.+)$", line)
        if not match:
            return result("invalid_syntax", "list")
        date = match.group(1).strip()
        if not any(pattern.match(date) for pattern in DATE_PATTERNS):
            return result("invalid_semantics", "list")
    return result("valid")


def validate_chart(chart_type: str, body: str, report_class: str = "data") -> dict[str, str]:
    text = "\n".join(non_empty_lines(body))
    if chart_type in {"bar", "line", "pie", "radar"}:
        needed = ["labels:", "datasets:", "- label:", "data:"]
    elif chart_type == "scatter":
        needed = ["datasets:", "- label:", "points:"]
    elif chart_type == "funnel":
        needed = ["stages:", "- label:", "value:"]
    elif chart_type == "sankey":
        needed = ["nodes:", "links:"]
    else:
        return result("invalid_syntax", "table")

    if any(marker not in text for marker in needed):
        return result("invalid_syntax", "table")

    if report_class in {"narrative", "mixed"} and PLACEHOLDER_RE.search(text) and not has_real_number(text):
        return result("invalid_semantics", "table")

    return result("valid")


def validate_diagram(diagram_type: str, body: str) -> dict[str, str]:
    text = "\n".join(non_empty_lines(body))
    if diagram_type == "sequence":
        needed = ["actors:", "steps:", "from:", "to:", "msg:"]
    elif diagram_type == "flowchart":
        needed = ["nodes:", "edges:", "id:", "kind:", "label:", "from:", "to:"]
    elif diagram_type == "tree":
        needed = ["root:", "children:"]
    elif diagram_type == "mindmap":
        needed = ["center:", "branches:"]
    else:
        return result("invalid_syntax", "callout")

    if any(marker not in text for marker in needed):
        return result("invalid_syntax", "callout")
    return result("valid")


def extract_block(source: str, tag: str) -> tuple[str, str]:
    lines = source.splitlines()
    for idx, line in enumerate(lines):
        if line.startswith(f":::{tag}"):
            header = line
            body: list[str] = []
            for inner in lines[idx + 1 :]:
                if inner.strip() == ":::":
                    return header, "\n".join(body)
                body.append(inner)
    raise AssertionError(f"Block {tag!r} not found")


def parse_frontmatter(source: str) -> tuple[dict[str, object], str]:
    lines = source.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}, source

    end_index: int | None = None
    for index in range(1, len(lines)):
        if lines[index].strip() == "---":
            end_index = index
            break

    if end_index is None:
        return {}, source

    frontmatter_lines = lines[1:end_index]
    body = "\n".join(lines[end_index + 1 :])
    frontmatter: dict[str, object] = {}
    current_list_key: str | None = None
    for raw in frontmatter_lines:
        if not raw.strip():
            continue
        if raw.startswith("  - ") and current_list_key:
            frontmatter.setdefault(current_list_key, [])
            values = frontmatter[current_list_key]
            if isinstance(values, list):
                values.append(raw[4:].strip())
            continue
        current_list_key = None
        if ":" not in raw:
            continue
        key, value = raw.split(":", 1)
        key = key.strip()
        value = value.strip()
        if not value:
            frontmatter[key] = []
            current_list_key = key
            continue
        frontmatter[key] = value.strip("\"'")
    return frontmatter, body


def iter_blocks(source: str) -> list[IRBlock]:
    blocks: list[IRBlock] = []
    lines = source.splitlines()
    index = 0
    while index < len(lines):
        line = lines[index]
        if not line.startswith(":::"):
            index += 1
            continue
        header = line[3:].strip()
        if not header:
            index += 1
            continue
        parts = header.split()
        tag = parts[0]
        params: dict[str, str] = {}
        for token in parts[1:]:
            if "=" not in token:
                continue
            key, value = token.split("=", 1)
            params[key.strip()] = value.strip()
        body_lines: list[str] = []
        index += 1
        while index < len(lines) and lines[index].strip() != ":::":
            body_lines.append(lines[index])
            index += 1
        blocks.append(IRBlock(tag=tag, params=params, body="\n".join(body_lines)))
        index += 1
    return blocks


def validate_block(block: IRBlock, report_class: str) -> dict[str, str]:
    if block.tag == "kpi":
        return validate_kpi(block.body, report_class=report_class)
    if block.tag == "timeline":
        return validate_timeline(block.body)
    if block.tag == "chart":
        return validate_chart(block.params.get("type", ""), block.body, report_class=report_class)
    if block.tag == "diagram":
        return validate_diagram(block.params.get("type", ""), block.body)
    return result("valid")


def collect_heading_lines(source: str) -> list[str]:
    _, body = parse_frontmatter(source)
    return [line[3:].strip() for line in body.splitlines() if line.startswith("## ")]


def component_counts(source: str) -> dict[str, int]:
    counts: dict[str, int] = {}
    for block in iter_blocks(source):
        counts[block.tag] = counts.get(block.tag, 0) + 1
    return counts
