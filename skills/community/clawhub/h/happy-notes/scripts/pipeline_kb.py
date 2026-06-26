#!/usr/bin/env python3
"""Pipeline KB: 知识库管理（list/create/delete/update/info）

用法:
  python3 scripts/pipeline_kb.py list [--keyword "搜索词"]
  python3 scripts/pipeline_kb.py create --name "知识库名称" [--description "描述"]
  python3 scripts/pipeline_kb.py delete --kb "知识库名称" --force
  python3 scripts/pipeline_kb.py update --kb "知识库名称" [--name "新名称"] [--description "新描述"]
  python3 scripts/pipeline_kb.py info --kb "知识库名称"
"""

import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from iflow_common import log, api_get, api_post, api_post_form, find_kb, check_success, output


def main():
    parser = argparse.ArgumentParser(description="知识库管理")
    sub = parser.add_subparsers(dest="action", required=True,
                                help="操作类型: list / create / delete / update / info")

    # list
    p_list = sub.add_parser("list", help="列出知识库")
    p_list.add_argument("--keyword", default="", help="搜索关键词")

    # create
    p_create = sub.add_parser("create", help="创建知识库")
    p_create.add_argument("--name", required=True, help="知识库名称")
    p_create.add_argument("--description", default="", help="知识库描述")

    # delete
    p_delete = sub.add_parser("delete", help="删除知识库")
    p_delete.add_argument("--kb", default="", help="知识库名称")
    p_delete.add_argument("--kb-id", default="", help="知识库 ID")
    p_delete.add_argument("--force", action="store_true", help="跳过确认")

    # update
    p_update = sub.add_parser("update", help="修改知识库名称或描述")
    p_update.add_argument("--kb", default="", help="知识库名称")
    p_update.add_argument("--kb-id", default="", help="知识库 ID")
    p_update.add_argument("--name", default="", help="新名称")
    p_update.add_argument("--description", default="", help="新描述")

    # info
    p_info = sub.add_parser("info", help="查看知识库详情")
    p_info.add_argument("--kb", default="", help="知识库名称")
    p_info.add_argument("--kb-id", default="", help="知识库 ID")

    args = parser.parse_args()

    if args.action == "list":
        import urllib.parse
        encoded = urllib.parse.quote(args.keyword)
        resp = api_get(f"/api/v1/knowledge/pageQueryCollections?pageNum=1&pageSize=100&keyword={encoded}")
        items = resp.get("data", [])
        results = []
        for item in items:
            extra = item.get("extra") or {}
            results.append({
                "collectionId": item.get("code"),
                "name": item.get("name"),
                "description": item.get("description", ""),
                "totalFiles": extra.get("totalCnt", 0),
            })
        log(f"共 {len(results)} 个知识库")
        output({"total": len(results), "knowledgeBases": results})

    elif args.action == "create":
        desc = args.description or args.name
        log(f'创建知识库「{args.name}」')
        resp = api_post("/api/v1/knowledge/saveCollection",
                        {"collectionName": args.name, "description": desc})
        collection_id = resp.get("data")
        if not collection_id:
            log(f"创建失败: {resp.get('message', '未知错误')}")
            sys.exit(1)
        log(f"知识库已创建: {collection_id}")
        output({"collectionId": collection_id, "name": args.name})

    elif args.action == "delete":
        kb_id = find_kb(args.kb or None, args.kb_id or None, allow_fuzzy=False)
        if not args.force:
            if not sys.stdin.isatty():
                log("非交互模式下必须使用 --force 参数")
                sys.exit(1)
            confirm = input(f">>> 确认删除知识库？此操作不可恢复。[y/N] ")
            if confirm.lower() != "y":
                log("已取消")
                sys.exit(0)
        log(f"删除知识库: {kb_id}")
        # 注意：clearCollection API 始终返回 data: false（不论知识库是否存在），
        # 因此只能通过 success 字段判断请求是否成功，不能用 data 字段判断。
        resp = api_post_form("/api/v1/knowledge/clearCollection",
                            {"collectionId": kb_id})
        if resp.get("success") is not True:
            msg = resp.get("message", "未知错误")
            log(f"删除可能失败: {msg}")
            output({"action": "delete", "collectionId": kb_id, "warning": msg})
        else:
            log("知识库已删除")
            output({"action": "delete", "collectionId": kb_id})

    elif args.action == "update":
        kb_id = find_kb(args.kb or None, args.kb_id or None)
        if not args.name and not args.description:
            log("--name 或 --description 至少提供一个")
            sys.exit(1)
        # API 要求 collectionName 和 description 都必须传，先查当前值补齐
        current = api_get(f"/api/v1/knowledge/queryCollection?collectionId={kb_id}")
        current_data = current.get("data") or {}
        if not current_data.get("name"):
            log("查询当前知识库信息失败，无法安全更新（避免清空名称）")
            sys.exit(1)
        body = {
            "collectionId": kb_id,
            "collectionName": args.name or current_data.get("name", ""),
            "description": args.description or current_data.get("description", ""),
        }
        log(f"更新知识库: {kb_id}")
        resp = api_post("/api/v1/knowledge/modifyCollections", body)
        if not check_success(resp, "更新知识库"):
            sys.exit(1)
        log("知识库已更新")
        output({"action": "update", "collectionId": kb_id,
                "name": args.name or None, "description": args.description or None})

    elif args.action == "info":
        kb_id = find_kb(args.kb or None, args.kb_id or None)
        resp = api_get(f"/api/v1/knowledge/queryCollection?collectionId={kb_id}")
        data = resp.get("data")
        if not data:
            log("知识库不存在或查询失败")
            sys.exit(1)
        extra = data.get("extra") or {}
        output({
            "collectionId": data.get("code"),
            "name": data.get("name"),
            "description": data.get("description", ""),
            "totalFiles": extra.get("totalCnt", 0),
            "gmtCreate": data.get("gmtCreate"),
            "gmtModified": data.get("gmtModified"),
        })


if __name__ == "__main__":
    main()
