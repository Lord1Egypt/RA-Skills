# -*- coding: utf-8 -*-
"""
save_page.py — 保存概念页或资源页（上传 + catalog + index 重新生成）

用法：
    # 概念页
    python3 save_page.py --open_id ou_xxx --kind concept \
        --name "力控制" --file /tmp/paperkb/concept_力控制.md \
        --brief "机械系统通过力反馈调整动作的控制方法"

    # 资源页
    python3 save_page.py --open_id ou_xxx --kind resource \
        --name "DexYCB" --file /tmp/paperkb/resource_DexYCB.md \
        --brief "大规模手-物体交互数据集" --resource_type 数据集

输出单行 JSON：
    {"success": true, "page_path": "concepts/力控制.md", "page_url": "...",
     "replaced": false}
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import gitea_api as g
import kb_common as kb


def _out(payload: dict) -> None:
    print(json.dumps(payload, ensure_ascii=False))


def _fail(error: str, message: str) -> None:
    _out({"success": False, "error": error, "message": message})
    sys.exit(0)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--open_id", required=True)
    parser.add_argument("--kind", required=True, choices=["concept", "resource"])
    parser.add_argument("--name", required=True)
    parser.add_argument("--file", required=True, help="页面 Markdown 内容的本地路径")
    parser.add_argument("--brief", default="")
    parser.add_argument("--resource_type", default="",
                        help="资源类型：数据集/开源项目/工具/硬件/其他")
    args = parser.parse_args()

    user = kb.get_user_by_open_id(args.open_id)
    if user is None:
        _fail("user_not_registered", "该用户尚未注册，请先完成初始化。")
    username = user["gitea_username"]

    src = Path(args.file)
    if not src.exists():
        _fail("file_not_found", f"找不到页面内容文件:{src}")
    content = src.read_text(encoding="utf-8")

    safe_name = kb.sanitize_filename(args.name)
    folder = "concepts" if args.kind == "concept" else "resources"
    page_path = f"{folder}/{safe_name}.md"

    try:
        g.put_file(username, kb.REPO_NAME, page_path, content,
                   f"paper-kb {args.kind}: {safe_name}")
    except g.GiteaError as exc:
        _fail("upload_failed", f"上传页面失败：{exc}")

    entry = {"name": args.name.strip(), "file": page_path,
             "brief": args.brief.strip()}
    if args.kind == "resource":
        entry["resource_type"] = args.resource_type.strip() or "其他"

    catalog = kb.read_catalog(username)
    replaced = kb.upsert_page(
        catalog, "concepts" if args.kind == "concept" else "resources", entry)
    try:
        kb.write_catalog(username, catalog)
        kb.regen_index(username, user.get("research_direction", ""), catalog)
    except g.GiteaError as exc:
        _fail("catalog_failed", f"更新目录失败：{exc}")

    _out({
        "success": True,
        "replaced": replaced,
        "page_path": page_path,
        "page_url": f"{g.GITEA_URL}/{username}/{kb.REPO_NAME}/src/branch/main/{page_path}",
    })


if __name__ == "__main__":
    main()
