#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
knowledge.py — 火一五 Odoo「知识库 Knowledge」管理（knowledge.article）

字段坑（详见 references/odoo-knowledge-documents-api.md）：
  - body 是 Html；icon 是存 emoji 的普通 Char。
  - 根文章必须有 internal_permission（直接 create 不传会自动补 'write'）。
  - 收藏/取消用 action_toggle_favorite（返回 bool）；移动用 move_to(parent_id)。
  - is_user_favorite / user_has_access 是可搜 compute 字段。
  - 权限/成员不能直接写 member 表，用 set_internal_permission / invite_members。

命令
  list     列文章   默认顶级；--fav 我收藏 / --mine 我编辑的
  tree     看某文章的子文章层级
  search   全文搜（标题+正文）
  show     读文章正文 + 子文章
  add      建文章   --title [--body --icon --parent]
  fav      收藏/取消收藏（toggle）
  move     移动到某父文章下  move <id> --parent <pid>

示例
  python3 knowledge.py search 退款流程
  python3 knowledge.py add --title "产品手册" --body "正文..." --icon 📘
  python3 knowledge.py show 12
"""

from __future__ import annotations

import argparse
import json
import re
import sys

from odoo_client import Odoo, OdooError
from odoo_utils import from_utc, m2o_name, render_table

MODEL = "knowledge.article"
CATEGORY = {"workspace": "工作区", "private": "私有", "shared": "共享"}


def _html_to_text(html: str, limit: int = 800) -> str:
    if not html:
        return ""
    t = re.sub(r"<(br|/p|/h[1-6]|/div|/li|/tr)\s*/?>", "\n", html, flags=re.I)
    t = re.sub(r"<[^>]+>", "", t)
    for a, b in [("&nbsp;", " "), ("&amp;", "&"), ("&lt;", "<"), ("&gt;", ">"),
                 ("&quot;", '"'), ("&#39;", "'")]:
        t = t.replace(a, b)
    t = re.sub(r"\n{3,}", "\n\n", t).strip()
    return t[:limit] + ("\n…（更多见 odoo）" if len(t) > limit else "")


def _title(a: dict) -> str:
    return (a.get("icon") or "📄") + " " + (a.get("name") or "(无标题)")


def cmd_list(odoo: Odoo, args):
    uid = odoo.ensure_uid()
    if args.fav:
        domain, scope = [("is_user_favorite", "=", True)], "我的收藏"
    elif args.mine:
        domain, scope = [("last_edition_uid", "=", uid)], "我编辑的"
    else:
        domain, scope = [("user_has_access", "=", True), ("parent_id", "=", False)], "顶级文章"
    arts = odoo.search_read(
        MODEL, domain,
        ["id", "name", "icon", "is_user_favorite", "category", "last_edition_date"],
        order="favorite_count desc, write_date desc", limit=args.limit)
    if args.json:
        print(json.dumps(arts, ensure_ascii=False, default=str))
        return
    rows = [[a["id"], _title(a)[:30], CATEGORY.get(a.get("category"), a.get("category") or "-"),
             "⭐" if a.get("is_user_favorite") else "",
             from_utc(a.get("last_edition_date") or "", "%Y-%m-%d") or "-"] for a in arts]
    print(render_table(rows, ["ID", "标题", "分类", "收藏", "最后编辑"]))
    print(f"\n共 {len(arts)} 篇（{scope}）")


def cmd_tree(odoo: Odoo, args):
    kids = odoo.search_read(
        MODEL, [["parent_id", "=", args.id]], ["id", "name", "icon", "category"],
        order="sequence, id")
    p = odoo.read(MODEL, [args.id], ["name", "icon"])
    if not p:
        raise OdooError(f"文章 #{args.id} 不存在。")
    print(f"📂 {_title(p[0])} 的子文章：")
    rows = [[k["id"], _title(k)[:34]] for k in kids]
    print(render_table(rows, ["ID", "标题"]) if rows else "（无子文章）")


def cmd_search(odoo: Odoo, args):
    domain = ["|", ("name", "ilike", args.query), ("body", "ilike", args.query)]
    domain = ["&", ("user_has_access", "=", True)] + domain
    arts = odoo.search_read(MODEL, domain, ["id", "name", "icon", "category"], limit=args.limit)
    if args.json:
        print(json.dumps(arts, ensure_ascii=False, default=str))
        return
    rows = [[a["id"], _title(a)[:34], CATEGORY.get(a.get("category"), "-")] for a in arts]
    print(f"🔍 搜「{args.query}」：")
    print(render_table(rows, ["ID", "标题", "分类"]) if rows else "（无匹配）")


def cmd_show(odoo: Odoo, args):
    a = odoo.read(MODEL, [args.id], ["name", "icon", "body", "category", "last_edition_date", "child_ids"])
    if not a:
        raise OdooError(f"文章 #{args.id} 不存在。")
    a = a[0]
    print(f"📖 {_title(a)}  [{CATEGORY.get(a.get('category'), '-')}]")
    print(f"   最后编辑：{from_utc(a.get('last_edition_date') or '', '%Y-%m-%d %H:%M') or '-'}")
    print("\n" + (_html_to_text(a.get("body")) or "（空）"))
    kids = a.get("child_ids") or []
    if kids:
        sub = odoo.read(MODEL, kids, ["id", "name", "icon"])
        print("\n子文章：" + "  ".join(f"#{s['id']} {_title(s)}" for s in sub))


def cmd_add(odoo: Odoo, args):
    body = args.body or ""
    if body and "<" not in body:
        body = f"<h1>{args.title}</h1>" + "".join(f"<p>{l}</p>" for l in body.splitlines())
    vals = {"name": args.title}
    if body:
        vals["body"] = body
    if args.icon:
        vals["icon"] = args.icon
    if args.parent:
        vals["parent_id"] = args.parent
    aid = odoo.create(MODEL, vals)
    where = f"（在 #{args.parent} 下）" if args.parent else ""
    print(f"✅ 已新建知识库文章 #{aid}：{args.title}{where}")


def cmd_fav(odoo: Odoo, args):
    state = odoo.execute_kw(MODEL, "action_toggle_favorite", [[args.id]])
    print(f"{'⭐ 已收藏' if state else '☆ 已取消收藏'} 文章 #{args.id}")


def cmd_move(odoo: Odoo, args):
    odoo.execute_kw(MODEL, "move_to", [[args.id]], {"parent_id": args.parent})
    print(f"✅ 文章 #{args.id} 已移到 #{args.parent} 下")


def build_parser():
    p = argparse.ArgumentParser(description="火一五 Odoo 知识库管理")
    p.add_argument("--tools-md")
    p.add_argument("--json", action="store_true")
    sub = p.add_subparsers(dest="cmd", required=True)

    li = sub.add_parser("list", help="列文章")
    li.add_argument("--fav", action="store_true", help="我收藏的")
    li.add_argument("--mine", action="store_true", help="我编辑的")
    li.add_argument("--limit", type=int, default=80)

    tr = sub.add_parser("tree", help="某文章的子文章")
    tr.add_argument("id", type=int)

    se = sub.add_parser("search", help="全文搜")
    se.add_argument("query")
    se.add_argument("--limit", type=int, default=40)

    sh = sub.add_parser("show", help="读文章正文")
    sh.add_argument("id", type=int)

    ad = sub.add_parser("add", help="建文章")
    ad.add_argument("--title", required=True)
    ad.add_argument("--body")
    ad.add_argument("--icon", help="emoji 图标")
    ad.add_argument("--parent", type=int, help="父文章 id（建子文章）")

    fv = sub.add_parser("fav", help="收藏/取消收藏")
    fv.add_argument("id", type=int)

    mv = sub.add_parser("move", help="移动到某父文章下")
    mv.add_argument("id", type=int)
    mv.add_argument("--parent", required=True, type=int)
    return p


def main(argv=None):
    args = build_parser().parse_args(argv if argv is not None else sys.argv[1:])
    try:
        odoo = Odoo(tools_md=args.tools_md)
        dispatch = {"list": cmd_list, "tree": cmd_tree, "search": cmd_search,
                    "show": cmd_show, "add": cmd_add, "fav": cmd_fav, "move": cmd_move}
        dispatch[args.cmd](odoo, args)
    except OdooError as e:
        print(f"❌ {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
