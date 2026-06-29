#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
todo.py — 火一五 Odoo「待办 / To-do」管理

待办本质：project.task 记录，且 project_id 为空（私有）+ 指派给本人。模型字段坑见
references/odoo-todo-api.md。

命令
  add      新建待办      --title 必填，可选 --desc/--deadline/--priority/--stage/--tags
  list     列出待办      默认未完成；--all 全部 / --done 已完成 / --stage 按个人阶段 / --limit
  done     标记已完成    done <id> [<id> ...]
  reopen   重新打开      reopen <id> ...
  cancel   取消          cancel <id> ...
  update   修改          update <id> [--title/--desc/--deadline/--priority/--stage]
  stages   列出我的个人阶段（Inbox/Today/This Week/...）

示例
  python3 todo.py add --title "跟进三和红木分账" --deadline 2026-06-10 --priority 2
  python3 todo.py list
  python3 todo.py done 1234
"""

from __future__ import annotations

import argparse
import json
import sys

from odoo_client import Odoo, OdooError
from odoo_utils import (
    CLOSED_STATES, from_utc, m2o_name, priority_label, render_table,
    state_label, to_utc,
)

MODEL = "project.task"
# 「这是一条待办」的判定（与 Odoo To-do 应用主视图 domain 一致）
TODO_DOMAIN = lambda uid: [
    ("user_ids", "in", [uid]),
    ("project_id", "=", False),
    ("parent_id", "=", False),
]
LIST_FIELDS = [
    "id", "name", "state", "priority", "date_deadline",
    "personal_stage_type_id", "tag_ids",
]


def _html(desc: str) -> str:
    """纯文本转最简 HTML；已含标签的原样返回。"""
    desc = desc or ""
    if "<" in desc and ">" in desc:
        return desc
    return "".join(f"<p>{line}</p>" for line in desc.splitlines()) or ""


def _resolve_personal_stage(odoo: Odoo, uid: int, name: str):
    """按名字找当前用户的个人阶段 id。"""
    ids = odoo.search(
        "project.task.type",
        [["user_id", "=", uid], ["name", "=", name]],
        limit=1,
    )
    if not ids:
        # 模糊再试一次
        ids = odoo.search(
            "project.task.type",
            [["user_id", "=", uid], ["name", "ilike", name]],
            limit=1,
        )
    return ids[0] if ids else None


def _resolve_tags(odoo: Odoo, names: list[str]) -> list[int]:
    """标签名 -> id（不存在则创建）。"""
    out = []
    for n in names:
        n = n.strip()
        if not n:
            continue
        ids = odoo.search("project.tags", [["name", "=", n]], limit=1)
        out.append(ids[0] if ids else odoo.create("project.tags", {"name": n}))
    return out


def cmd_add(odoo: Odoo, args):
    uid = odoo.ensure_uid()
    vals = {
        "name": args.title,
        "user_ids": [(6, 0, [uid])],   # 指派给自己 → 进「我的待办」
        # 不传 project_id：保持 False = 私有待办
    }
    if args.desc:
        vals["description"] = _html(args.desc)
    if args.deadline:
        vals["date_deadline"] = to_utc(args.deadline)
    if args.priority:
        vals["priority"] = str(args.priority)
    if args.stage:
        sid = _resolve_personal_stage(odoo, uid, args.stage)
        if sid:
            vals["personal_stage_type_id"] = sid
        else:
            sys.stderr.write(f"⚠️  没找到个人阶段「{args.stage}」，将落到默认 Inbox。\n")
    if args.tags:
        vals["tag_ids"] = [(6, 0, _resolve_tags(odoo, args.tags.split(",")))]

    tid = odoo.create(MODEL, vals)
    if args.json:
        print(json.dumps({"id": tid, "title": args.title}, ensure_ascii=False))
    else:
        print(f"✅ 已新建待办 #{tid}：{args.title}")
        if args.deadline:
            print(f"   截止：{args.deadline}  优先级：{priority_label(str(args.priority or 0))}")


def cmd_list(odoo: Odoo, args):
    uid = odoo.ensure_uid()
    domain = TODO_DOMAIN(uid) + [("active", "=", True)]
    if args.done:
        domain.append(("state", "in", list(CLOSED_STATES)))
    elif not args.all:
        domain.append(("is_closed", "=", False))
    if args.stage:
        # personal_stage_type_id 是 store=False 无 search 的 related 字段，不能点路径筛。
        # 走个人阶段关联表（project.task.stage.personal）拿 task_id 更可靠。
        sid = _resolve_personal_stage(odoo, uid, args.stage)
        if sid:
            rel = odoo.search_read(
                "project.task.stage.personal",
                [["user_id", "=", uid], ["stage_id", "=", sid]], ["task_id"])
            tids = [r["task_id"][0] for r in rel if r.get("task_id")]
            domain.append(("id", "in", tids or [0]))
        else:
            sys.stderr.write(f"⚠️  没找到个人阶段「{args.stage}」。\n")
            domain.append(("id", "in", [0]))

    tasks = odoo.search_read(
        MODEL, domain, LIST_FIELDS,
        order="priority desc, date_deadline asc, id desc", limit=args.limit,
    )
    if args.json:
        print(json.dumps(tasks, ensure_ascii=False, default=str))
        return
    rows = [
        [
            t["id"],
            state_label(t["state"]),
            priority_label(str(t.get("priority", "0"))),
            from_utc(t.get("date_deadline") or "", "%Y-%m-%d %H:%M") or "-",
            m2o_name(t.get("personal_stage_type_id")) or "-",
            (t["name"][:40] + "…") if len(t.get("name") or "") > 41 else t.get("name"),
        ]
        for t in tasks
    ]
    print(render_table(rows, ["ID", "状态", "优先级", "截止", "阶段", "标题"]))
    print(f"\n共 {len(tasks)} 条" + ("（全部）" if args.all else "（未完成）" if not args.done else "（已完成）"))


def _set_state(odoo: Odoo, ids: list[int], state: str, word: str, as_json: bool):
    odoo.write(MODEL, ids, {"state": state})
    if as_json:
        print(json.dumps({"ids": ids, "state": state}, ensure_ascii=False))
    else:
        print(f"✅ 已{word} {len(ids)} 条待办：{', '.join('#' + str(i) for i in ids)}")


def cmd_update(odoo: Odoo, args):
    uid = odoo.ensure_uid()
    vals = {}
    if args.title:
        vals["name"] = args.title
    if args.desc is not None:
        vals["description"] = _html(args.desc)
    if args.deadline:
        vals["date_deadline"] = to_utc(args.deadline)
    if args.priority is not None:
        vals["priority"] = str(args.priority)
    if args.stage:
        sid = _resolve_personal_stage(odoo, uid, args.stage)
        if sid:
            vals["personal_stage_type_id"] = sid
    if not vals:
        raise OdooError("没有要更新的字段。")
    odoo.write(MODEL, [args.id], vals)
    print(f"✅ 已更新待办 #{args.id}：{', '.join(vals.keys())}")


def cmd_stages(odoo: Odoo, args):
    uid = odoo.ensure_uid()
    stages = odoo.search_read(
        "project.task.type", [["user_id", "=", uid]],
        ["id", "name", "sequence", "fold"], order="sequence",
    )
    rows = [[s["id"], s["name"], s["sequence"], "折叠" if s["fold"] else ""] for s in stages]
    print(render_table(rows, ["ID", "个人阶段", "顺序", "标记"]))


def build_parser():
    p = argparse.ArgumentParser(description="火一五 Odoo 待办管理")
    p.add_argument("--tools-md", help="凭据文件路径（默认 ~/.huo15/tools.md）")
    p.add_argument("--json", action="store_true", help="输出 JSON")
    sub = p.add_subparsers(dest="cmd", required=True)

    a = sub.add_parser("add", help="新建待办")
    a.add_argument("--title", required=True)
    a.add_argument("--desc", help="内容/描述")
    a.add_argument("--deadline", help="截止日期 YYYY-MM-DD[ HH:MM]")
    a.add_argument("--priority", type=int, choices=[0, 1, 2, 3], help="0普通 1中 2高 3紧急")
    a.add_argument("--stage", help="个人阶段名，如 Today")
    a.add_argument("--tags", help="标签，逗号分隔")

    li = sub.add_parser("list", help="列出待办")
    li.add_argument("--all", action="store_true", help="含已完成")
    li.add_argument("--done", action="store_true", help="只看已完成")
    li.add_argument("--stage", help="按个人阶段名筛选")
    li.add_argument("--limit", type=int, default=80)

    for name, word in [("done", "完成"), ("reopen", "重开"), ("cancel", "取消")]:
        sp = sub.add_parser(name, help=f"{word}待办")
        sp.add_argument("ids", nargs="+", type=int)

    u = sub.add_parser("update", help="修改待办")
    u.add_argument("id", type=int)
    u.add_argument("--title")
    u.add_argument("--desc")
    u.add_argument("--deadline")
    u.add_argument("--priority", type=int, choices=[0, 1, 2, 3])
    u.add_argument("--stage")

    sub.add_parser("stages", help="列出我的个人阶段")
    return p


def main(argv=None):
    args = build_parser().parse_args(argv if argv is not None else sys.argv[1:])
    try:
        odoo = Odoo(tools_md=args.tools_md)
        if args.cmd == "add":
            cmd_add(odoo, args)
        elif args.cmd == "list":
            cmd_list(odoo, args)
        elif args.cmd == "done":
            _set_state(odoo, args.ids, "1_done", "完成", args.json)
        elif args.cmd == "reopen":
            _set_state(odoo, args.ids, "01_in_progress", "重开", args.json)
        elif args.cmd == "cancel":
            _set_state(odoo, args.ids, "1_canceled", "取消", args.json)
        elif args.cmd == "update":
            cmd_update(odoo, args)
        elif args.cmd == "stages":
            cmd_stages(odoo, args)
    except OdooError as e:
        print(f"❌ {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
