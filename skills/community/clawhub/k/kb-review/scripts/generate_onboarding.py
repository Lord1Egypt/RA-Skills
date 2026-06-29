from __future__ import annotations

import argparse
import json
from pathlib import Path

import catalog
import gitea_api as g
from utils import json_fail, sanitize_filename


def out(data: dict) -> None:
    print(json.dumps(data, ensure_ascii=False))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--owner", required=True)
    parser.add_argument("--repo", required=True)
    parser.add_argument("--title", required=True)
    parser.add_argument("--file", required=True)
    parser.add_argument("--brief", default="")
    parser.add_argument("--project_id", default="")
    args = parser.parse_args()
    src = Path(args.file)
    if not src.exists():
        out(json_fail("file_not_found", f"找不到 onboarding 草稿：{src}"))
        return
    safe = sanitize_filename(args.title)
    path = f"onboarding/{safe}.md"
    try:
        g.put_file(args.owner, args.repo, path, src.read_text(encoding="utf-8"), f"paper-kb onboarding: {safe}")
        cat = catalog.read(args.owner, args.repo)
        reviews = cat.setdefault("reviews", [])
        reviews.append({"name": args.title, "file": path, "brief": args.brief, "project_id": args.project_id, "kind": "onboarding"})
        catalog.write(args.owner, args.repo, cat)
        catalog.regen_index(args.owner, args.repo, args.repo, cat)
    except Exception as exc:
        out(json_fail("save_onboarding_failed", str(exc)))
        return
    out({"success": True, "path": path, "page_url": f"{g.GITEA_URL}/{args.owner}/{args.repo}/src/branch/main/{path}"})


if __name__ == "__main__":
    main()
