from __future__ import annotations

import argparse
import json
from pathlib import Path

import catalog
import gitea_api as g
from utils import json_fail, sanitize_filename


KINDS = {
    "concept": ("concepts", "concepts"),
    "resource": ("resources", "resources"),
    "person": ("people", "people"),
    "review": ("reviews", "reviews"),
    "import": ("imports", "imports"),
}


def out(data: dict) -> None:
    print(json.dumps(data, ensure_ascii=False))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--owner", required=True)
    parser.add_argument("--repo", required=True)
    parser.add_argument("--kind", required=True, choices=sorted(KINDS))
    parser.add_argument("--name", required=True)
    parser.add_argument("--file", required=True)
    parser.add_argument("--brief", default="")
    parser.add_argument("--resource_type", default="")
    args = parser.parse_args()
    src = Path(args.file)
    if not src.exists():
        out(json_fail("file_not_found", f"找不到页面文件：{src}"))
        return
    folder, cat_key = KINDS[args.kind]
    safe = sanitize_filename(args.name)
    path = f"{folder}/{safe}.md"
    try:
        g.put_file(args.owner, args.repo, path, src.read_text(encoding="utf-8"), f"paper-kb {args.kind}: {safe}")
        cat = catalog.read(args.owner, args.repo)
        entry = {"name": args.name, "file": path, "brief": args.brief}
        if args.kind == "resource":
            entry["resource_type"] = args.resource_type or "其他"
        items = cat.setdefault(cat_key, [])
        replaced = False
        for i, old in enumerate(items):
            if old.get("name") == args.name:
                items[i] = entry
                replaced = True
                break
        if not replaced:
            items.append(entry)
        catalog.write(args.owner, args.repo, cat)
        catalog.regen_index(args.owner, args.repo, args.repo, cat)
    except Exception as exc:
        out(json_fail("save_page_failed", str(exc)))
        return
    out({"success": True, "replaced": replaced, "path": path, "page_url": f"{g.GITEA_URL}/{args.owner}/{args.repo}/src/branch/main/{path}"})


if __name__ == "__main__":
    main()
