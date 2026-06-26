#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

BULLET_RE = re.compile(r"^[-*]\s+(.*)$")
KV_RE = re.compile(r"^-?\s*([^:#]+):\s*(.*)$")


def slugify(text: str) -> str:
    return text.strip().lower().replace("/", "_").replace(" ", "_")


def parse_md(path: str) -> dict:
    lines = Path(path).read_text(encoding="utf-8").splitlines()
    data: dict[str, object] = {}
    current_key: str | None = None
    current_list: list[str] = []

    def flush_list():
        nonlocal current_key, current_list
        if current_key and current_list:
            data[current_key] = current_list[:]
        current_list = []

    for raw in lines:
        line = raw.strip()
        if not line:
            continue
        if line.startswith("##"):
            flush_list()
            current_key = slugify(line.lstrip("# "))
            continue
        if line.startswith("#"):
            continue
        bullet = BULLET_RE.match(line)
        if bullet and current_key:
            item = bullet.group(1).strip()
            if ":" in item and current_key not in {"core_stack", "priority_titles", "nice-to-have_titles", "companies", "agencies_/_patterns", "keywords"}:
                k, v = item.split(":", 1)
                data[slugify(k)] = v.strip()
            else:
                current_list.append(item)
            continue
        kv = KV_RE.match(line)
        if kv:
            flush_list()
            key = slugify(kv.group(1))
            value = kv.group(2).strip()
            current_key = key
            if value:
                data[key] = value
            else:
                current_list = []
            continue
    flush_list()
    return data


def to_profile(project_dir: str) -> dict:
    project = Path(project_dir)
    profile = parse_md(str(project / "PROFILE.md")) if (project / "PROFILE.md").exists() else {}
    roles = parse_md(str(project / "TARGET_ROLES.md")) if (project / "TARGET_ROLES.md").exists() else {}
    rules = parse_md(str(project / "SEARCH_RULES.md")) if (project / "SEARCH_RULES.md").exists() else {}

    stack = profile.get("core_stack") or profile.get("stack") or []
    if isinstance(stack, str):
        stack = [stack]

    target_roles = roles.get("priority_titles") or roles.get("target_roles") or []
    if isinstance(target_roles, str):
        target_roles = [target_roles]

    exclude_keywords = rules.get("excluded_keywords") or rules.get("exclusions") or []
    if isinstance(exclude_keywords, str):
        exclude_keywords = [exclude_keywords]

    salary_floor_raw = rules.get("salary_floor") or roles.get("floor")
    salary_floor = None
    if isinstance(salary_floor_raw, str):
        digits = re.sub(r"\D", "", salary_floor_raw)
        salary_floor = int(digits) if digits else None

    remote_mode = str(roles.get("remote_/_hybrid_/_office") or profile.get("timezone_preference") or rules.get("remote_mode") or "").lower()
    if "remote" not in remote_mode and "удал" in remote_mode:
        remote_mode = "remote"
    elif "hybrid" in remote_mode or "гибрид" in remote_mode:
        remote_mode = "hybrid"
    elif any(x in remote_mode for x in ["office", "офис"]):
        remote_mode = "office"
    else:
        remote_mode = ""

    return {
        "target_roles": target_roles,
        "stack": stack,
        "remote_mode": remote_mode,
        "salary_floor": salary_floor,
        "exclude_keywords": exclude_keywords,
    }


def main():
    if len(sys.argv) != 2:
        print("Usage: profile_to_json.py <project-dir>", file=sys.stderr)
        sys.exit(2)
    print(json.dumps(to_profile(sys.argv[1]), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
