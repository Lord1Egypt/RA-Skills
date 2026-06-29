#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
documents.py — 火一五 Odoo「文档 Documents」管理（documents.document）

⚠️ Odoo 19 架构变化（详见 references/odoo-knowledge-documents-api.md）：
  - 文件夹就是 documents.document 且 type='folder'（无独立 documents.folder）。
  - 无 documents.share / workflow.rule；权限走 access_internal / documents.access。
  - 上传直接 create {name, datas(base64), folder_id}，自动建 ir.attachment。
  - 下载用 access_url / access_token，或 /web/content/<attachment_id>。
  - 建标签需文档管理员权限；普通用户只能用已有标签。

命令
  folders   列所有文件夹
  list      列文档   --folder <名字/id> / --tag <名字>
  search    全文搜（名字+内容索引）
  upload    上传文件 --file <本地路径> [--folder <名字/id>] [--name]
  link      取某文档的下载链接
  tags      列标签
  tag       给文档打/去标签  tag <id> --add 合同 [--remove 草稿]

示例
  python3 documents.py folders
  python3 documents.py upload --file ~/report.pdf --folder 财务
  python3 documents.py link 123
"""

from __future__ import annotations

import argparse
import base64
import json
import mimetypes
import os
import sys

from odoo_client import Odoo, OdooError
from odoo_utils import m2o_name, render_table

MODEL = "documents.document"
TAG = "documents.tag"


def _human_size(n) -> str:
    try:
        n = float(n or 0)
    except (TypeError, ValueError):
        return str(n)
    for unit in ("B", "KB", "MB", "GB"):
        if n < 1024:
            return f"{n:.0f}{unit}" if unit == "B" else f"{n:.1f}{unit}"
        n /= 1024
    return f"{n:.1f}TB"


def _resolve_folder(odoo: Odoo, ref):
    if ref in (None, ""):
        return None
    if str(ref).isdigit():
        return int(ref)
    ids = odoo.search(MODEL, [["type", "=", "folder"], ["name", "ilike", str(ref)]], limit=1)
    if not ids:
        raise OdooError(f"找不到文件夹「{ref}」。")
    return ids[0]


def cmd_folders(odoo: Odoo, args):
    fs = odoo.search_read(
        MODEL, [["type", "=", "folder"]],
        ["id", "name", "folder_id", "access_internal"], order="sequence, name", limit=args.limit)
    if args.json:
        print(json.dumps(fs, ensure_ascii=False, default=str))
        return
    rows = [[f["id"], f["name"], m2o_name(f.get("folder_id")) or "(顶级)",
             f.get("access_internal") or "-"] for f in fs]
    print(render_table(rows, ["ID", "文件夹", "上级", "默认权限"]))
    print(f"\n共 {len(fs)} 个文件夹")


def cmd_list(odoo: Odoo, args):
    domain = [("type", "!=", "folder")]
    if args.folder:
        domain.append(("folder_id", "=", _resolve_folder(odoo, args.folder)))
    if args.tag:
        tids = odoo.search(TAG, [["name", "ilike", args.tag]], limit=1)
        domain.append(("tag_ids", "in", tids or [0]))
    docs = odoo.search_read(
        MODEL, domain,
        ["id", "name", "mimetype", "file_size", "type", "owner_id", "folder_id"],
        order="write_date desc", limit=args.limit)
    if args.json:
        print(json.dumps(docs, ensure_ascii=False, default=str))
        return
    rows = [[d["id"], (d.get("name") or "")[:32], d.get("type"),
             _human_size(d.get("file_size")), m2o_name(d.get("folder_id")) or "-",
             m2o_name(d.get("owner_id")) or "-"] for d in docs]
    print(render_table(rows, ["ID", "名称", "类型", "大小", "文件夹", "拥有者"]))
    print(f"\n共 {len(docs)} 个文档")


def cmd_search(odoo: Odoo, args):
    docs = odoo.search_read(
        MODEL, ["|", ("name", "ilike", args.query), ("index_content", "ilike", args.query)],
        ["id", "name", "mimetype", "folder_id"], limit=args.limit)
    if args.json:
        print(json.dumps(docs, ensure_ascii=False, default=str))
        return
    rows = [[d["id"], (d.get("name") or "")[:36], m2o_name(d.get("folder_id")) or "-"] for d in docs]
    print(f"🔍 搜「{args.query}」：")
    print(render_table(rows, ["ID", "名称", "文件夹"]) if rows else "（无匹配）")


def cmd_upload(odoo: Odoo, args):
    path = os.path.expanduser(args.file)
    if not os.path.isfile(path):
        raise OdooError(f"文件不存在：{path}")
    with open(path, "rb") as f:
        data = base64.b64encode(f.read()).decode()
    name = args.name or os.path.basename(path)
    vals = {"name": name, "datas": data,
            "mimetype": mimetypes.guess_type(path)[0] or "application/octet-stream"}
    if args.folder:
        vals["folder_id"] = _resolve_folder(odoo, args.folder)
    did = odoo.create(MODEL, vals)
    print(f"✅ 已上传文档 #{did}：{name}" + (f"（→ {args.folder}）" if args.folder else ""))


def cmd_link(odoo: Odoo, args):
    d = odoo.read(MODEL, [args.id], ["name", "access_token", "access_url", "attachment_id", "type", "url"])
    if not d:
        raise OdooError(f"文档 #{args.id} 不存在。")
    d = d[0]
    print(f"🔗 文档 #{args.id}：{d.get('name')}")
    if d.get("type") == "url" and d.get("url"):
        print(f"   外链：{d['url']}")
    if d.get("access_url"):
        print(f"   UI 链接：{d['access_url']}")
    if d.get("access_token"):
        print(f"   下载（凭 token）：{odoo.url}/documents/content/{d['access_token']}?download=true")
    if d.get("attachment_id"):
        print(f"   下载（需登录）：{odoo.url}/web/content/{d['attachment_id'][0]}?download=true")


def cmd_tags(odoo: Odoo, args):
    tags = odoo.search_read(TAG, [], ["id", "name", "color"], order="name", limit=args.limit)
    rows = [[t["id"], t["name"]] for t in tags]
    print(render_table(rows, ["ID", "标签"]))
    print(f"\n共 {len(tags)} 个标签")


def cmd_tag(odoo: Odoo, args):
    cmds = []
    for name in (args.add or "").split(","):
        name = name.strip()
        if not name:
            continue
        ids = odoo.search(TAG, [["name", "=", name]], limit=1)
        if not ids:
            raise OdooError(f"标签「{name}」不存在（新建标签需文档管理员权限）。先 `documents.py tags` 看已有标签。")
        cmds.append((4, ids[0]))
    for name in (args.remove or "").split(","):
        name = name.strip()
        if not name:
            continue
        ids = odoo.search(TAG, [["name", "=", name]], limit=1)
        if ids:
            cmds.append((3, ids[0]))
    if not cmds:
        raise OdooError("用 --add 或 --remove 指定标签。")
    odoo.write(MODEL, [args.id], {"tag_ids": cmds})
    print(f"✅ 文档 #{args.id} 标签已更新")


def build_parser():
    p = argparse.ArgumentParser(description="火一五 Odoo 文档管理")
    p.add_argument("--tools-md")
    p.add_argument("--json", action="store_true")
    sub = p.add_subparsers(dest="cmd", required=True)

    fo = sub.add_parser("folders", help="列文件夹")
    fo.add_argument("--limit", type=int, default=100)

    li = sub.add_parser("list", help="列文档")
    li.add_argument("--folder", help="文件夹名字/id")
    li.add_argument("--tag", help="标签名")
    li.add_argument("--limit", type=int, default=100)

    se = sub.add_parser("search", help="全文搜")
    se.add_argument("query")
    se.add_argument("--limit", type=int, default=50)

    up = sub.add_parser("upload", help="上传文件")
    up.add_argument("--file", required=True, help="本地文件路径")
    up.add_argument("--folder", help="目标文件夹名字/id")
    up.add_argument("--name", help="文档名（默认用文件名）")

    lk = sub.add_parser("link", help="取下载链接")
    lk.add_argument("id", type=int)

    sub.add_parser("tags", help="列标签").add_argument("--limit", type=int, default=100)

    tg = sub.add_parser("tag", help="给文档打/去标签")
    tg.add_argument("id", type=int)
    tg.add_argument("--add", help="加标签，逗号分隔")
    tg.add_argument("--remove", help="去标签，逗号分隔")
    return p


def main(argv=None):
    args = build_parser().parse_args(argv if argv is not None else sys.argv[1:])
    try:
        odoo = Odoo(tools_md=args.tools_md)
        dispatch = {"folders": cmd_folders, "list": cmd_list, "search": cmd_search,
                    "upload": cmd_upload, "link": cmd_link, "tags": cmd_tags, "tag": cmd_tag}
        dispatch[args.cmd](odoo, args)
    except OdooError as e:
        print(f"❌ {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
