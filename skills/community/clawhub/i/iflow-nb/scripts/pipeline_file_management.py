#!/usr/bin/env python3
"""
Pipeline 5: 文件管理 — 重命名、删除单个文件、批量删除、列出文件

用法:
  python pipeline_file_management.py list --kb "竞品分析"
  python pipeline_file_management.py rename --kb "竞品分析" --file "nb_test" --new-name "Q1报告.md"
  python pipeline_file_management.py delete --kb "竞品分析" --file "旧版报告" --force
  python pipeline_file_management.py batch-delete --kb "竞品分析" --files "test_001,test_002" --force
"""
import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from iflow_common import log, api_post, find_kb, output


def get_file_list(collection_id):
    return api_post(f"/api/v1/knowledge/pageQueryContents?collectionId={collection_id}&pageNum=1&pageSize=100")


def find_file_by_keyword(items, keyword):
    for item in items:
        if keyword in (item.get("fileName") or ""):
            return item
    return None


def main():
    parser = argparse.ArgumentParser(description="Pipeline 5: 文件管理")
    parser.add_argument("action", choices=["list", "rename", "delete", "batch-delete"], help="操作类型")
    parser.add_argument("--kb", default="", help="知识库名称")
    parser.add_argument("--kb-id", default="", help="知识库 ID")
    parser.add_argument("--file", default="", help="文件名关键字")
    parser.add_argument("--files", default="", help="多个文件名关键字，逗号分隔")
    parser.add_argument("--new-name", default="", help="新文件名")
    parser.add_argument("--force", action="store_true", help="跳过删除确认")
    args = parser.parse_args()

    collection_id = find_kb(args.kb or None, args.kb_id or None)
    log(f"知识库 ID: {collection_id}")

    contents_resp = get_file_list(collection_id)
    items = contents_resp.get("data", [])

    # ═══ list ═══
    if args.action == "list":
        total = int(contents_resp.get("total", 0))
        files_out = [{"contentId": it["contentId"], "fileName": it.get("fileName"),
                       "status": it.get("status"), "contentType": it.get("contentType")} for it in items]
        log(f"共 {total} 个文件")
        for it in items:
            log(f"  - {it.get('fileName')} [{it.get('status')}]")
        output({"collectionId": collection_id, "total": total, "files": files_out})
        return

    # ═══ rename ═══
    if args.action == "rename":
        if not args.file or not args.new_name:
            log("rename 需要 --file 和 --new-name 参数")
            sys.exit(1)
        matched = find_file_by_keyword(items, args.file)
        if not matched:
            log(f"未找到包含 '{args.file}' 的文件")
            sys.exit(1)

        cid = matched["contentId"]
        ct = matched.get("contentType", "")
        old_name = matched.get("fileName", "")
        log(f'找到文件「{old_name}」，重命名为「{args.new_name}」')

        resp = api_post("/api/v1/knowledge/updateContent2Collection", {
            "collectionId": collection_id, "contentType": ct,
            "contentId": cid, "removeFlag": False,
            "extra": {"fileName": args.new_name},
        })
        if resp.get("success") is not True:
            log(f"重命名失败: {resp.get('message', '未知错误')}")
            sys.exit(1)
        log("已重命名")
        output({"action": "rename", "collectionId": collection_id,
                "contentId": cid, "oldName": old_name, "newName": args.new_name})
        return

    # ═══ delete ═══
    if args.action == "delete":
        if not args.file:
            log("delete 需要 --file 参数")
            sys.exit(1)
        matched = find_file_by_keyword(items, args.file)
        if not matched:
            log(f"未找到包含 '{args.file}' 的文件")
            sys.exit(1)

        cid = matched["contentId"]
        ct = matched.get("contentType", "")
        fname = matched.get("fileName", "")

        if not args.force:
            confirm = input(f">>> 确认删除文件「{fname}」？此操作不可恢复。[y/N] ")
            if confirm.lower() != "y":
                log("用户取消删除")
                output({"error": "用户取消删除"})
                return

        log(f'正在删除「{fname}」')
        resp = api_post("/api/v1/knowledge/updateContent2Collection", {
            "collectionId": collection_id, "contentType": ct,
            "contentId": cid, "removeFlag": True, "extra": {},
        })
        if resp.get("success") is not True:
            log(f"删除失败: {resp.get('message', '未知错误')}")
            sys.exit(1)

        remaining = int(api_post(f"/api/v1/knowledge/pageQueryContents?collectionId={collection_id}&pageNum=1&pageSize=50").get("total", 0))
        log(f"已删除「{fname}」，剩余 {remaining} 个文件")
        output({"action": "delete", "collectionId": collection_id,
                "contentId": cid, "fileName": fname, "remaining": remaining})
        return

    # ═══ batch-delete ═══
    if args.action == "batch-delete":
        if not args.files:
            log("batch-delete 需要 --files 参数")
            sys.exit(1)

        keywords = [k.strip() for k in args.files.split(",")]
        matched_ids = []
        matched_names = []

        for kw in keywords:
            m = find_file_by_keyword(items, kw)
            if not m:
                log(f"跳过: 未找到包含「{kw}」的文件")
                continue
            matched_ids.append(m["contentId"])
            matched_names.append(m.get("fileName", ""))

        if not matched_ids:
            log("未找到任何匹配的文件")
            sys.exit(1)

        log(f"找到 {len(matched_ids)} 个文件待删除:")
        for i, name in enumerate(matched_names):
            log(f"  {i + 1}. {name}")

        if not args.force:
            confirm = input(">>> 确认全部删除？此操作不可恢复。[y/N] ")
            if confirm.lower() != "y":
                log("用户取消删除")
                output({"error": "用户取消删除"})
                return

        resp = api_post("/api/v1/knowledge/batchDeleteCollectionContent", {
            "collectionId": collection_id, "contentIds": matched_ids,
        })
        if resp.get("success") is not True:
            log(f"批量删除失败: {resp.get('message', '未知错误')}")
            sys.exit(1)

        remaining = int(api_post(f"/api/v1/knowledge/pageQueryContents?collectionId={collection_id}&pageNum=1&pageSize=50").get("total", 0))
        log(f"已删除 {len(matched_ids)} 个文件，剩余 {remaining} 个")
        output({"action": "batch-delete", "collectionId": collection_id,
                "deleted": len(matched_ids), "remaining": remaining})


if __name__ == "__main__":
    main()
