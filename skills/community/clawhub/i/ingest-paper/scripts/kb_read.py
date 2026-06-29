# -*- coding: utf-8 -*-
"""
kb_read.py — 读取知识库（查询 Skill 的核心读取工具）

用法：
    # 列出目录（含 brief 和 base_url，一次 API 调用）
    python3 kb_read.py --open_id ou_xxx --list all
    python3 kb_read.py --open_id ou_xxx --list concepts

    # 读取某个页面的完整内容
    python3 kb_read.py --open_id ou_xxx --read "concepts/力控制"
    python3 kb_read.py --open_id ou_xxx --read "summaries/某论文标题"

输出单行 JSON。--list 输出中的 base_url 用于拼接页面的可点击链接：
    页面完整链接 = base_url + 页面file路径
    例：http://.../mayidan/paper-kb/src/branch/main/ + summaries/xxx.md
"""
from __future__ import annotations

import argparse
import json
import sys

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
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--list", choices=["concepts", "resources", "documents", "all"])
    mode.add_argument("--read", help="页面路径，如 concepts/力控制（可不带 .md）")
    parser.add_argument("--log_question", default="",
                        help="列目录时若带上用户的查询问题，会顺手写入 log.md（确保查询必被记录）")
    args = parser.parse_args()

    user = kb.get_user_by_open_id(args.open_id)
    if user is None:
        _fail("user_not_registered", "该用户尚未注册，请先完成初始化。")
    username = user["gitea_username"]
    base_url = f"{g.GITEA_URL}/{username}/{kb.REPO_NAME}/src/branch/main/"

    if args.list:
        if args.log_question:
            kb.append_query_log(username, args.log_question)
        catalog = kb.read_catalog(username)
        payload = {
            "success": True,
            "research_direction": user.get("research_direction", ""),
            "base_url": base_url,
            "repo_url": f"{g.GITEA_URL}/{username}/{kb.REPO_NAME}",
        }
        if args.list == "all":
            payload.update({
                "documents": catalog["documents"],
                "concepts": catalog["concepts"],
                "resources": catalog["resources"],
            })
        else:
            payload[args.list] = catalog[args.list]
        _out(payload)
        return

    path = args.read.strip().strip("/")
    if not path.endswith(".md"):
        path += ".md"
    result = g.get_file(username, kb.REPO_NAME, path)
    if result is None:
        _fail("page_not_found", f"页面 {path} 不存在。")
    content, _ = result
    _out({"success": True, "path": path, "content": content,
          "page_url": base_url + path})


if __name__ == "__main__":
    main()
