#!/usr/bin/env python3
"""Dependency Check - linkfox-tiktok-shop-return-refund -> linkfox-tiktok-shop-auth."""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

REQUIRED_SKILL = "linkfox-tiktok-shop-auth"
DEPENDENCY_EXIT_CODE = 42


def _split_path_list(raw: str | None) -> list[Path]:
    if not raw or not raw.strip():
        return []
    return [Path(p).expanduser() for p in raw.split(os.pathsep) if p.strip()]


def candidate_skill_roots() -> list[Path]:
    roots: list[Path] = []
    for env_var in ("LINKFOX_SKILLS_DIR", "SKILLS_DIR", "CURSOR_SKILLS_DIR"):
        p = os.environ.get(env_var)
        if p:
            roots.append(Path(p).expanduser())
    roots.extend(_split_path_list(os.environ.get("HERMES_SKILLS_EXTERNAL_DIRS")))
    for env_var in ("OPENCLAW_WORKSPACE", "OPENCLAW_ROOT", "OPENCLAW_WORKDIR"):
        ws = os.environ.get(env_var)
        if ws:
            w = Path(ws).expanduser()
            roots.append(w / "skills")
            roots.append(w / ".agents" / "skills")
    oc_skills = os.environ.get("OPENCLAW_SKILLS_DIR")
    if oc_skills:
        roots.append(Path(oc_skills).expanduser())
    try:
        cwd = Path.cwd()
        roots.append(cwd / "skills")
        roots.append(cwd / ".agents" / "skills")
    except OSError:
        pass
    here = Path(__file__).resolve()
    if len(here.parents) >= 3:
        roots.append(here.parents[2])
    home = Path.home()
    roots.extend(
        [
            home / ".claude" / "skills",
            home / ".cursor" / "skills",
            home / ".linkfox" / "skills",
            home / ".openclaw" / "skills",
            home / ".hermes" / "skills",
        ]
    )
    seen: set[Path] = set()
    unique: list[Path] = []
    for r in roots:
        try:
            rr = r.resolve()
        except OSError:
            rr = r
        if rr not in seen:
            seen.add(rr)
            unique.append(r)
    return unique


def locate_dependency() -> Path | None:
    for root_dir in candidate_skill_roots():
        target = root_dir / REQUIRED_SKILL / "SKILL.md"
        if target.is_file():
            return target
    return None


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    found = locate_dependency()
    if found is not None:
        payload = {"skill": REQUIRED_SKILL, "skillMdPath": str(found)}
        if args.json:
            print(json.dumps({**payload, "status": "ok"}, ensure_ascii=False, indent=2))
        print(f"DEPENDENCY_OK: {json.dumps(payload, ensure_ascii=False)}", file=sys.stderr)
        sys.exit(0)
    payload = {
        "missingSkill": REQUIRED_SKILL,
        "reason": "linkfox-tiktok-shop-return-refund 依赖 linkfox-tiktok-shop-auth，未找到其 SKILL.md。",
        "searchedRoots": [str(p) for p in candidate_skill_roots()],
        "marketplaceUrl": "https://skill.linkfox.com/",
    }
    if args.json:
        print(json.dumps({**payload, "status": "missing"}, ensure_ascii=False, indent=2))
    print(f"DEPENDENCY_MISSING: {json.dumps(payload, ensure_ascii=False)}", file=sys.stderr)
    sys.exit(DEPENDENCY_EXIT_CODE)


if __name__ == "__main__":
    main()
