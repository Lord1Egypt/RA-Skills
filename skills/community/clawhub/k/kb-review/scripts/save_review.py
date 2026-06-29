from __future__ import annotations

import argparse
import json
from pathlib import Path

import catalog
import gitea_api as g
from utils import json_fail, now_str, sanitize_filename


def out(data: dict) -> None:
    print(json.dumps(data, ensure_ascii=False))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--owner", required=True)
    parser.add_argument("--repo", required=True)
    parser.add_argument("--title", required=True)
    parser.add_argument("--review_file", required=True)
    parser.add_argument("--brief", default="")
    parser.add_argument("--scope", default="personal")
    parser.add_argument("--project_id", default="")
    args = parser.parse_args()
    src = Path(args.review_file)
    if not src.exists():
        out(json_fail("review_file_not_found", f"找不到综述草稿：{src}"))
        return
    safe = sanitize_filename(args.title)
    path = f"reviews/{safe}.md"
    try:
        g.put_file(args.owner, args.repo, path, src.read_text(encoding="utf-8"), f"paper-kb review: {safe}")
        cat = catalog.read(args.owner, args.repo)
        item = {
            "name": args.title,
            "file": path,
            "brief": args.brief,
            "scope": args.scope,
            "project_id": args.project_id,
            "updated_at": now_str(),
        }
        reviews = cat.setdefault("reviews", [])
        replaced = False
        for i, old in enumerate(reviews):
            if old.get("name") == args.title:
                reviews[i] = item
                replaced = True
                break
        if not replaced:
            reviews.append(item)
        catalog.write(args.owner, args.repo, cat)
        catalog.regen_index(args.owner, args.repo, args.repo, cat)
    except Exception as exc:
        out(json_fail("save_review_failed", str(exc)))
        return
    out({"success": True, "replaced": replaced, "path": path, "page_url": f"{g.GITEA_URL}/{args.owner}/{args.repo}/src/branch/main/{path}"})


if __name__ == "__main__":
    main()
