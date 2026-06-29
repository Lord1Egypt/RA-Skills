#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
project.py — 火一五 Odoo「项目 / Project」管理

项目层： list / show / add / edit / archive / unarchive
任务层： tasks / task-add / task-move / task-assign / task-done / task-update

字段坑（详见 references/odoo-project-api.md）：
  - 任务负责人 user_ids 是 Many2many，写 [(6,0,[ids])]；项目负责人是 user_id(单)。
  - 任务「分配工时」字段是 allocated_hours（不是 planned_hours）。
  - date_deadline 是 Datetime；state 用 '01_in_progress' / '1_done' 等编号字符串。
  - 任务阶段 project.task.type 必须属于该任务的项目（project_ids 含 project_id）。

示例
  python3 project.py list
  python3 project.py show 5
  python3 project.py task-add --project 5 --title "首页设计" --assignee 我 --deadline 2026-06-20
  python3 project.py task-move 88 --stage 进行中
"""

from __future__ import annotations

import argparse
import json
import sys

from odoo_client import Odoo, OdooError
from odoo_utils import (
    from_utc, hours, m2o_name, priority_label, render_table, state_label, to_utc,
)

P_MODEL = "project.project"
T_MODEL = "project.task"
STAGE_MODEL = "project.task.type"


# --------------------------------------------------------------------------- #
# 名字 -> id 解析（让用户能用名字而不是 id）
# --------------------------------------------------------------------------- #
def _resolve_project(odoo: Odoo, ref) -> int:
    if isinstance(ref, int) or (isinstance(ref, str) and ref.isdigit()):
        return int(ref)
    res = odoo.name_search(P_MODEL, ref, limit=1)
    if not res:
        raise OdooError(f"找不到项目「{ref}」。")
    return res[0][0]


def _resolve_users(odoo: Odoo, names: str) -> list[int]:
    uid = odoo.ensure_uid()
    out = []
    for n in names.split(","):
        n = n.strip()
        if not n:
            continue
        if n in ("我", "me", "self"):
            out.append(uid)
            continue
        if n.isdigit():
            out.append(int(n))
            continue
        res = odoo.name_search("res.users", n, args=[["share", "=", False]], limit=1)
        if not res:
            raise OdooError(f"找不到用户「{n}」。")
        out.append(res[0][0])
    return out


def _resolve_partner(odoo: Odoo, name: str):
    if not name:
        return None
    if name.isdigit():
        return int(name)
    res = odoo.name_search("res.partner", name, limit=1)
    if not res:
        raise OdooError(f"找不到客户/联系人「{name}」。")
    return res[0][0]


def _resolve_task_stage(odoo: Odoo, project_id: int, name: str):
    """找属于该项目的看板阶段 id。"""
    for op in ("=", "ilike"):
        ids = odoo.search(
            STAGE_MODEL,
            [["project_ids", "in", [project_id]], ["name", op, name]],
            limit=1,
        )
        if ids:
            return ids[0]
    return None


def _group_count(g: dict) -> int:
    for k in ("__count", "stage_id_count", "state_count"):
        if k in g:
            return g[k]
    return 0


# --------------------------------------------------------------------------- #
# 项目层
# --------------------------------------------------------------------------- #
def cmd_list(odoo: Odoo, args):
    domain = [] if args.all else [("active", "=", True)]
    if args.mine:
        domain.append(("user_id", "=", odoo.ensure_uid()))
    projects = odoo.search_read(
        P_MODEL, domain,
        ["id", "name", "user_id", "partner_id", "task_count", "stage_id", "date"],
        order="sequence, name", limit=args.limit,
    )
    if args.json:
        print(json.dumps(projects, ensure_ascii=False, default=str))
        return
    rows = [
        [p["id"], p["name"], m2o_name(p.get("user_id")) or "-",
         m2o_name(p.get("partner_id")) or "-", p.get("task_count", 0),
         m2o_name(p.get("stage_id")) or "-"]
        for p in projects
    ]
    print(render_table(rows, ["ID", "项目", "负责人", "客户", "任务数", "阶段"]))
    print(f"\n共 {len(projects)} 个项目")


def cmd_show(odoo: Odoo, args):
    pid = _resolve_project(odoo, args.project)
    p = odoo.read(P_MODEL, [pid], [
        "name", "user_id", "partner_id", "date_start", "date",
        "stage_id", "privacy_visibility", "task_count", "description",
    ])
    if not p:
        raise OdooError(f"项目 #{pid} 不存在。")
    p = p[0]
    print(f"📁 项目 #{pid}：{p['name']}")
    print(f"   负责人：{m2o_name(p.get('user_id')) or '-'}   客户：{m2o_name(p.get('partner_id')) or '-'}")
    print(f"   起止：{p.get('date_start') or '-'} ~ {p.get('date') or '-'}   阶段：{m2o_name(p.get('stage_id')) or '-'}")
    print(f"   可见性：{p.get('privacy_visibility')}   任务数：{p.get('task_count', 0)}")

    # 按看板阶段统计任务
    groups = odoo.formatted_read_group(
        T_MODEL, [["project_id", "=", pid]], ["stage_id"], ["__count"]
    )
    if groups:
        print("\n   各阶段任务：")
        rows = [[m2o_name(g.get("stage_id")) or "(无阶段)", _group_count(g)] for g in groups]
        for line in render_table(rows, ["阶段", "任务数"]).splitlines():
            print("   " + line)


def cmd_add(odoo: Odoo, args):
    vals = {"name": args.name}
    if args.manager:
        vals["user_id"] = _resolve_users(odoo, args.manager)[0]
    if args.customer:
        vals["partner_id"] = _resolve_partner(odoo, args.customer)
    if args.start:
        vals["date_start"] = to_utc(args.start)[:10]
    if args.deadline:
        vals["date"] = to_utc(args.deadline)[:10]
    if args.desc:
        vals["description"] = f"<p>{args.desc}</p>"
    if args.privacy:
        vals["privacy_visibility"] = args.privacy
    pid = odoo.create(P_MODEL, vals)
    print(f"✅ 已新建项目 #{pid}：{args.name}")


def cmd_edit(odoo: Odoo, args):
    pid = _resolve_project(odoo, args.project)
    vals = {}
    if args.name:
        vals["name"] = args.name
    if args.manager:
        vals["user_id"] = _resolve_users(odoo, args.manager)[0]
    if args.customer:
        vals["partner_id"] = _resolve_partner(odoo, args.customer)
    if args.start:
        vals["date_start"] = to_utc(args.start)[:10]
    if args.deadline:
        vals["date"] = to_utc(args.deadline)[:10]
    if args.privacy:
        vals["privacy_visibility"] = args.privacy
    if not vals:
        raise OdooError("没有要修改的字段。")
    odoo.write(P_MODEL, [pid], vals)
    print(f"✅ 已更新项目 #{pid}：{', '.join(vals.keys())}")


def cmd_archive(odoo: Odoo, args, active: bool):
    pid = _resolve_project(odoo, args.project)
    odoo.write(P_MODEL, [pid], {"active": active})
    print(f"✅ 项目 #{pid} 已{'恢复' if active else '归档'}")


# --------------------------------------------------------------------------- #
# 任务层
# --------------------------------------------------------------------------- #
TASK_FIELDS = [
    "id", "name", "stage_id", "user_ids", "state", "priority",
    "date_deadline", "allocated_hours",
]


def cmd_tasks(odoo: Odoo, args):
    pid = _resolve_project(odoo, args.project)
    domain = [["project_id", "=", pid]]
    if not args.all:
        domain.append(["is_closed", "=", False])
    if args.stage:
        domain.append(["stage_id.name", "ilike", args.stage])
    tasks = odoo.search_read(
        T_MODEL, domain, TASK_FIELDS,
        order="stage_id, priority desc, date_deadline asc", limit=args.limit,
    )
    if args.json:
        print(json.dumps(tasks, ensure_ascii=False, default=str))
        return
    rows = []
    for t in tasks:
        assignees = _user_names(odoo, t.get("user_ids"))
        rows.append([
            t["id"], m2o_name(t.get("stage_id")) or "-", state_label(t["state"]),
            priority_label(str(t.get("priority", "0"))),
            from_utc(t.get("date_deadline") or "", "%Y-%m-%d") or "-",
            assignees or "-",
            (t["name"][:36] + "…") if len(t.get("name") or "") > 37 else t.get("name"),
        ])
    print(render_table(rows, ["ID", "阶段", "状态", "优先级", "截止", "负责人", "标题"]))
    print(f"\n项目 #{pid} 共 {len(tasks)} 个任务" + ("（全部）" if args.all else "（未完成）"))


_USER_CACHE: dict = {}


def _user_names(odoo: Odoo, user_ids) -> str:
    """user_ids（id 列表）-> 名字串，带缓存少往返。"""
    if not user_ids:
        return ""
    miss = [i for i in user_ids if i not in _USER_CACHE]
    if miss:
        for u in odoo.read("res.users", miss, ["name"]):
            _USER_CACHE[u["id"]] = u["name"]
    return ", ".join(_USER_CACHE.get(i, str(i)) for i in user_ids)


def cmd_task_add(odoo: Odoo, args):
    pid = _resolve_project(odoo, args.project)
    vals = {"name": args.title, "project_id": pid}
    if args.assignee:
        vals["user_ids"] = [(6, 0, _resolve_users(odoo, args.assignee))]
    if args.deadline:
        vals["date_deadline"] = to_utc(args.deadline)
    if args.priority is not None:
        vals["priority"] = str(args.priority)
    if args.hours is not None:
        vals["allocated_hours"] = args.hours
    if args.desc:
        vals["description"] = f"<p>{args.desc}</p>"
    if args.stage:
        sid = _resolve_task_stage(odoo, pid, args.stage)
        if sid:
            vals["stage_id"] = sid
        else:
            sys.stderr.write(f"⚠️  项目内没有阶段「{args.stage}」，按默认阶段创建。\n")
    tid = odoo.create(T_MODEL, vals)
    print(f"✅ 已在项目 #{pid} 新建任务 #{tid}：{args.title}")


def cmd_task_move(odoo: Odoo, args):
    t = odoo.read(T_MODEL, [args.task], ["project_id"])
    if not t:
        raise OdooError(f"任务 #{args.task} 不存在。")
    pid = t[0]["project_id"][0] if t[0].get("project_id") else None
    if not pid:
        raise OdooError(f"任务 #{args.task} 没有所属项目，无法用看板阶段。")
    sid = _resolve_task_stage(odoo, pid, args.stage)
    if not sid:
        raise OdooError(f"项目内找不到阶段「{args.stage}」。")
    odoo.write(T_MODEL, [args.task], {"stage_id": sid})
    print(f"✅ 任务 #{args.task} 已移到阶段「{args.stage}」")


def cmd_task_assign(odoo: Odoo, args):
    user_ids = _resolve_users(odoo, args.users)
    odoo.write(T_MODEL, [args.task], {"user_ids": [(6, 0, user_ids)]})
    print(f"✅ 任务 #{args.task} 负责人已设为：{_user_names(odoo, user_ids)}")


def cmd_task_done(odoo: Odoo, args):
    odoo.write(T_MODEL, args.tasks, {"state": "1_done"})
    print(f"✅ 已完成任务：{', '.join('#' + str(i) for i in args.tasks)}")


def cmd_task_update(odoo: Odoo, args):
    vals = {}
    if args.title:
        vals["name"] = args.title
    if args.deadline:
        vals["date_deadline"] = to_utc(args.deadline)
    if args.priority is not None:
        vals["priority"] = str(args.priority)
    if args.hours is not None:
        vals["allocated_hours"] = args.hours
    if args.desc is not None:
        vals["description"] = f"<p>{args.desc}</p>"
    if not vals:
        raise OdooError("没有要更新的字段。")
    odoo.write(T_MODEL, [args.task], vals)
    print(f"✅ 已更新任务 #{args.task}：{', '.join(vals.keys())}")


# --------------------------------------------------------------------------- #
def build_parser():
    p = argparse.ArgumentParser(description="火一五 Odoo 项目与任务管理")
    p.add_argument("--tools-md")
    p.add_argument("--json", action="store_true")
    sub = p.add_subparsers(dest="cmd", required=True)

    li = sub.add_parser("list", help="列出项目")
    li.add_argument("--all", action="store_true", help="含已归档")
    li.add_argument("--mine", action="store_true", help="只看我负责的")
    li.add_argument("--limit", type=int, default=100)

    sh = sub.add_parser("show", help="项目详情 + 任务统计")
    sh.add_argument("project", help="项目 id 或名称")

    ad = sub.add_parser("add", help="新建项目")
    ad.add_argument("--name", required=True)
    ad.add_argument("--manager", help="项目负责人（名字/id/我）")
    ad.add_argument("--customer", help="客户（名字/id）")
    ad.add_argument("--start", help="开始日期 YYYY-MM-DD")
    ad.add_argument("--deadline", help="到期日期 YYYY-MM-DD")
    ad.add_argument("--desc")
    ad.add_argument("--privacy", choices=["followers", "invited_users", "employees", "portal"])

    ed = sub.add_parser("edit", help="编辑项目")
    ed.add_argument("project")
    ed.add_argument("--name")
    ed.add_argument("--manager")
    ed.add_argument("--customer")
    ed.add_argument("--start")
    ed.add_argument("--deadline")
    ed.add_argument("--privacy", choices=["followers", "invited_users", "employees", "portal"])

    for name in ("archive", "unarchive"):
        sp = sub.add_parser(name, help=f"{'归档' if name == 'archive' else '恢复'}项目")
        sp.add_argument("project")

    tk = sub.add_parser("tasks", help="列出项目任务")
    tk.add_argument("project")
    tk.add_argument("--all", action="store_true")
    tk.add_argument("--stage")
    tk.add_argument("--limit", type=int, default=200)

    ta = sub.add_parser("task-add", help="在项目下新建任务")
    ta.add_argument("--project", required=True)
    ta.add_argument("--title", required=True)
    ta.add_argument("--assignee", help="负责人，逗号分隔（名字/id/我）")
    ta.add_argument("--deadline")
    ta.add_argument("--priority", type=int, choices=[0, 1, 2, 3])
    ta.add_argument("--hours", type=float, help="分配工时（小时）")
    ta.add_argument("--stage")
    ta.add_argument("--desc")

    tm = sub.add_parser("task-move", help="把任务移到某看板阶段")
    tm.add_argument("task", type=int)
    tm.add_argument("--stage", required=True)

    tas = sub.add_parser("task-assign", help="设置任务负责人")
    tas.add_argument("task", type=int)
    tas.add_argument("--users", required=True, help="逗号分隔")

    td = sub.add_parser("task-done", help="标记任务完成")
    td.add_argument("tasks", nargs="+", type=int)

    tu = sub.add_parser("task-update", help="修改任务")
    tu.add_argument("task", type=int)
    tu.add_argument("--title")
    tu.add_argument("--deadline")
    tu.add_argument("--priority", type=int, choices=[0, 1, 2, 3])
    tu.add_argument("--hours", type=float)
    tu.add_argument("--desc")
    return p


def main(argv=None):
    args = build_parser().parse_args(argv if argv is not None else sys.argv[1:])
    try:
        odoo = Odoo(tools_md=args.tools_md)
        dispatch = {
            "list": cmd_list, "show": cmd_show, "add": cmd_add, "edit": cmd_edit,
            "tasks": cmd_tasks, "task-add": cmd_task_add, "task-move": cmd_task_move,
            "task-assign": cmd_task_assign, "task-done": cmd_task_done,
            "task-update": cmd_task_update,
        }
        if args.cmd == "archive":
            cmd_archive(odoo, args, active=False)
        elif args.cmd == "unarchive":
            cmd_archive(odoo, args, active=True)
        else:
            dispatch[args.cmd](odoo, args)
    except OdooError as e:
        print(f"❌ {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
