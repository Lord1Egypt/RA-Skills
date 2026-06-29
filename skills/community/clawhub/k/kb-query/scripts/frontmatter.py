from __future__ import annotations


def strip_frontmatter(content: str) -> str:
    if not content.startswith("---"):
        return content
    end = content.find("\n---", 3)
    if end < 0:
        return content
    return content[end + 4 :].lstrip()


def parse_title(content: str, fallback: str) -> str:
    if not content.startswith("---"):
        return fallback
    end = content.find("\n---", 3)
    if end < 0:
        return fallback
    for line in content[3:end].splitlines():
        if line.strip().startswith("title:"):
            value = line.split(":", 1)[1].strip()
            if value.startswith('"') and value.endswith('"'):
                value = value[1:-1]
            return value or fallback
    return fallback
