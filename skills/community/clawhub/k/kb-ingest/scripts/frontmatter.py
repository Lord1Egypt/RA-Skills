from __future__ import annotations

from datetime import datetime, timezone


def now_iso() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat()


def yaml_escape(value: object) -> str:
    text = "" if value is None else str(value)
    return '"' + text.replace("\\", "\\\\").replace('"', '\\"') + '"'


def render_frontmatter(data: dict) -> str:
    lines = ["---"]
    for key in ["id", "title", "type", "kbType", "createdAt", "updatedAt", "generatedBy", "sourceFileId", "sourceId", "taskId"]:
        if key in data:
            lines.append(f"{key}: {yaml_escape(data[key])}")
    sources = data.get("sources", [])
    lines.append("sources:")
    if not sources:
        lines.append("  []")
    else:
        for source in sources:
            lines.append("  - sourceId: " + yaml_escape(source.get("sourceId", "")))
            for key in ["sourceFileId", "title", "path", "originalPath", "fileName", "sourceType", "sha256", "page", "url"]:
                lines.append(f"    {key}: {yaml_escape(source.get(key, ''))}")
    lines.append("---")
    return "\n".join(lines) + "\n\n"
