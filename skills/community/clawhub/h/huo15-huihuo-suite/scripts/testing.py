#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
testing.py — 火一五 Odoo「测试验收」Bug / Sprint / 标签管理

模型（详见 references/odoo-testing-api.md）：
  - huo15.test.bug       测试验收 Bug（主模型，含状态机）
  - huo15.test.sprint    测试迭代 / Sprint
  - huo15.test.bug.tag   测试验收 Bug 标签

Bug 状态机：new → confirmed → in_progress → resolved → closed
            （resolved 可 reopen 回 in_progress；closed 可 reset 回 new）
关键坑：state 全走 action_* 方法（手 write 不会写 resolve_date/verifier_id/reopen_count）；
        priority 是 p0/p1/p2/p3（不是 project.task 的 0-3 数字）；
        create 必填 project_id；bug_delete 仅「测试验收/管理员」可用。

命令
  Bug:
    bug-add      登记 Bug
    bug-list     列 Bug（默认我的活跃）
    bug-show     详情
    bug-update   改字段
    confirm / start / resolve / verify / reopen / wontfix / duplicate / reset  状态流转
    bug-delete   删除（需管理员）

  Sprint:
    sprint-list / sprint-show / sprint-add / sprint-start / sprint-done / sprint-reset / sprint-add-bugs

  标签:
    tag-list / tag-add

  统计:
    stats        按维度聚合

示例
  python3 testing.py bug-add --title "登录验证码任意输入可登录" --project 域品汇 --severity high
  python3 testing.py bug-list --mine
  python3 testing.py resolve 88
  python3 testing.py verify 88
  python3 testing.py stats --by severity
"""

from __future__ import annotations

import argparse
import json
import sys

from odoo_client import Odoo, OdooError
from odoo_utils import from_utc, hours, m2o_id, m2o_name, render_table

BUG = "huo15.test.bug"
SPRINT = "huo15.test.sprint"
TAG = "huo15.test.bug.tag"

SEVERITY = {"serious": "🔴严重", "high": "🟠高", "medium": "🟡中", "low": "🔵低"}
PRIORITY = {"p0": "P0", "p1": "P1", "p2": "P2", "p3": "P3"}
STATE = {
    "new": "🆕新建", "confirmed": "✔️已确认", "in_progress": "🔧处理中",
    "resolved": "✅已解决", "closed": "📦已关闭",
}
RESOLUTION = {
    "fixed": "已修复", "wontfix": "不予处理", "duplicate": "重复",
    "cannotreproduce": "无法复现", "bydesign": "设计如此",
}
ACTIVE_STATES = ("new", "confirmed", "in_progress", "resolved")

LIST_FIELDS = [
    "id", "bug_code", "name", "state", "severity", "priority",
    "reporter_id", "report_date", "assignee_id", "sprint_id",
    "reopen_count", "effective_hours", "project_id",
]


# --------------------------------------------------------------------------- #
# 名字 → id 解析
# --------------------------------------------------------------------------- #
def _resolve(odoo: Odoo, model: str, ref, label: str, args=None):
    """名字/id/我 → id；空入参返回 None。"""
    if ref in (None, ""):
        return None
    s = str(ref)
    if model == "res.users" and s in ("我", "me", "self"):
        return odoo.ensure_uid()
    if s.isdigit():
        return int(s)
    res = odoo.name_search(model, s, args=args or [], limit=1)
    if not res:
        raise OdooError(f"找不到{label}「{ref}」。")
    return res[0][0]


def _resolve_bug(odoo: Odoo, ref) -> int:
    """支持 id / 'BUG-00001' / 标题模糊匹配。"""
    if isinstance(ref, int):
        return ref
    s = str(ref)
    if s.isdigit():
        return int(s)
    # 先按 bug_code 精确
    ids = odoo.search(BUG, [["bug_code", "=", s]], limit=1)
    if ids:
        return ids[0]
    res = odoo.name_search(BUG, s, limit=1)
    if not res:
        raise OdooError(f"找不到 Bug「{ref}」（可传 id 或 BUG-00001 或标题关键词）。")
    return res[0][0]


def _resolve_tags(odoo: Odoo, names: str) -> list:
    """标签名 -> id（不存在则建）。"""
    out = []
    for n in (names or "").split(","):
        n = n.strip()
        if not n:
            continue
        ids = odoo.search(TAG, [["name", "=", n]], limit=1)
        out.append(ids[0] if ids else odoo.create(TAG, {"name": n}))
    return out


def _html(desc: str) -> str:
    desc = desc or ""
    if "<" in desc and ">" in desc:
        return desc
    return "".join(f"<p>{line}</p>" for line in desc.splitlines()) or ""


def _p(p: str) -> str:
    """数字 0-3 / p0-p3 → Odoo 的 p0..p3。"""
    p = str(p).lower().strip()
    if p.isdigit():
        return f"p{int(p)}"
    if p.startswith("p") and p[1:].isdigit():
        return p
    return p


# --------------------------------------------------------------------------- #
# Bug
# --------------------------------------------------------------------------- #
def cmd_bug_add(odoo: Odoo, args):
    uid = odoo.ensure_uid()
    if not args.title:
        raise OdooError("--title 必填（Bug 标题）。")
    if not args.project:
        raise OdooError("--project 必填（所属项目）。")
    pid = _resolve(odoo, "project.project", args.project, "项目")
    vals = {
        "name": args.title,
        "project_id": pid,
        "severity": args.severity,
        "priority": _p(args.priority),
    }
    if args.desc:
        vals["description"] = _html(args.desc)
    if args.assignee:
        vals["assignee_id"] = _resolve(odoo, "res.users", args.assignee, "解决人")
    if args.reporter:
        vals["reporter_id"] = _resolve(odoo, "res.users", args.reporter, "呈报人")
    if args.task:
        vals["task_id"] = _resolve(odoo, "project.task", args.task, "任务")
    if args.sprint:
        vals["sprint_id"] = _resolve(odoo, SPRINT, args.sprint, "迭代")
    if args.found_version:
        vals["found_version"] = args.found_version
    if args.tags:
        vals["tag_ids"] = [(6, 0, _resolve_tags(odoo, args.tags))]
    if args.cc:
        cc_ids = [_resolve(odoo, "res.users", n, "抄送人") for n in args.cc.split(",") if n.strip()]
        vals["cc_user_ids"] = [(6, 0, cc_ids)]

    bid = odoo.create(BUG, vals)
    rec = odoo.read(BUG, [bid], ["bug_code"])[0]
    if args.json:
        print(json.dumps({"id": bid, "bug_code": rec["bug_code"]}, ensure_ascii=False))
        return
    print(f"✅ 已登记 Bug #{bid} [{rec['bug_code']}]：{args.title}")
    print(f"   项目：{args.project}  严重度：{SEVERITY.get(args.severity, args.severity)}  优先级：{_p(args.priority).upper()}")
    if args.assignee:
        print(f"   解决人：{args.assignee}")


def cmd_bug_list(odoo: Odoo, args):
    uid = odoo.ensure_uid()
    domain = []
    # 范围筛选（mine / reported 互斥但都补「谁」）
    if args.mine:
        domain.append(("assignee_id", "=", uid))
    if args.reported_by_me:
        domain.append(("reporter_id", "=", uid))
    # 状态筛选：显式 > 默认活跃（除非 --all 关闭默认）
    if args.state:
        domain.append(("state", "=", args.state))
    elif args.closed:
        domain.append(("state", "=", "closed"))
    elif not args.all:
        # 默认：活跃 Bug（不含已关闭）；--all 才看全部
        domain.append(("state", "in", list(ACTIVE_STATES)))
    if args.project:
        domain.append(("project_id", "=", _resolve(odoo, "project.project", args.project, "项目")))
    if args.assignee and not args.mine:
        domain.append(("assignee_id", "=", _resolve(odoo, "res.users", args.assignee, "解决人")))
    if args.reporter and not args.reported_by_me:
        domain.append(("reporter_id", "=", _resolve(odoo, "res.users", args.reporter, "呈报人")))
    if args.sprint:
        domain.append(("sprint_id", "=", _resolve(odoo, SPRINT, args.sprint, "迭代")))
    if args.severity:
        domain.append(("severity", "=", args.severity))
    if args.priority:
        domain.append(("priority", "=", _p(args.priority)))
    if args.tag:
        domain.append(("tag_ids", "in", _resolve_tags(odoo, args.tag)))
    if args.search:
        domain.append(("name", "ilike", args.search))

    order = "state, severity desc, priority desc, id desc" \
        if args.order == "auto" else args.order
    rows_data = odoo.search_read(BUG, domain, LIST_FIELDS, order=order, limit=args.limit)
    if args.json:
        print(json.dumps(rows_data, ensure_ascii=False, default=str))
        return
    rows = []
    for r in rows_data:
        rows.append([
            r["id"],
            r.get("bug_code") or "-",
            STATE.get(r["state"], r["state"]),
            SEVERITY.get(r.get("severity"), r.get("severity") or "-"),
            PRIORITY.get(r.get("priority"), r.get("priority") or "-"),
            m2o_name(r.get("assignee_id")) or "-",
            m2o_name(r.get("sprint_id")) or "-",
            r.get("reopen_count") or 0,
            hours(r.get("effective_hours")),
            (r["name"][:34] + "…") if len(r.get("name") or "") > 35 else r.get("name"),
        ])
    print(render_table(rows, ["ID", "编号", "状态", "严重", "优先", "解决人", "迭代", "打回", "工时", "标题"]))
    scope = _scope_label(args)
    print(f"\n共 {len(rows_data)} 条（{scope}）")


def _scope_label(args):
    if args.state:
        return f"状态={STATE.get(args.state, args.state)}"
    if args.closed:
        return "已关闭"
    if args.mine:
        return "指派给我 / 活跃"
    if args.reported_by_me:
        return "我呈报的 / 活跃"
    return "活跃"


def cmd_bug_show(odoo: Odoo, args):
    bid = _resolve_bug(odoo, args.id)
    r = odoo.read(BUG, [bid], [
        "bug_code", "name", "state", "severity", "priority", "resolution",
        "project_id", "task_id", "sprint_id", "found_version", "tag_ids",
        "reporter_id", "report_date", "assignee_id", "cc_user_ids",
        "verifier_id", "verify_date", "resolve_date", "reopen_count",
        "duplicate_of_id", "related_bug_ids", "effective_hours",
        "description", "note", "create_date", "write_date",
    ])[0]
    if args.json:
        print(json.dumps(r, ensure_ascii=False, default=str))
        return
    print(f"[{r.get('bug_code')}] {r['name']}")
    print(f"状态：{STATE.get(r['state'], r['state'])}" +
          (f"  处理结论：{RESOLUTION.get(r['resolution'], r['resolution'])}" if r.get("resolution") else ""))
    print(f"严重度：{SEVERITY.get(r.get('severity'), r.get('severity'))}   优先级：{PRIORITY.get(r.get('priority'), r.get('priority'))}")
    print(f"项目：{m2o_name(r.get('project_id'))}" +
          (f"   任务：{m2o_name(r.get('task_id'))}" if r.get("task_id") else "") +
          (f"   迭代：{m2o_name(r.get('sprint_id'))}" if r.get("sprint_id") else ""))
    if r.get("found_version"):
        print(f"发现版本：{r['found_version']}   标签：{', '.join(n for _, n in (r.get('tag_ids') or []))}")
    print(f"呈报人：{m2o_name(r.get('reporter_id'))} ({r.get('report_date') or '-'})" +
          f"   解决人：{m2o_name(r.get('assignee_id')) or '-'}")
    if r.get("resolve_date"):
        print(f"解决日期：{r['resolve_date']}   验收人：{m2o_name(r.get('verifier_id')) or '-'}   验收日期：{r.get('verify_date') or '-'}")
    if r.get("reopen_count"):
        print(f"⚠️  打回次数：{r['reopen_count']}")
    if r.get("duplicate_of_id"):
        print(f"重复于：{m2o_name(r['duplicate_of_id'])}")
    if r.get("related_bug_ids"):
        print(f"关联 Bug：{', '.join(m2o_name(b) for b in r['related_bug_ids'])}")
    if r.get("cc_user_ids"):
        print(f"抄送：{', '.join(m2o_name(u) for u in r['cc_user_ids'])}")
    print(f"累计工时：{hours(r.get('effective_hours'))}")
    if r.get("description") and r["description"].strip():
        import re
        plain = re.sub(r"<[^>]+>", " ", r["description"])
        plain = re.sub(r"\s+", " ", plain).strip()
        print(f"\n描述：{plain[:300]}{'…' if len(plain) > 300 else ''}")
    if r.get("note"):
        print(f"备注：{r['note']}")
    print(f"\n创建：{from_utc(r.get('create_date') or '', '%Y-%m-%d %H:%M')}   更新：{from_utc(r.get('write_date') or '', '%Y-%m-%d %H:%M')}")


def cmd_bug_update(odoo: Odoo, args):
    bid = _resolve_bug(odoo, args.id)
    vals = {}
    if args.title:
        vals["name"] = args.title
    if args.desc is not None:
        vals["description"] = _html(args.desc)
    if args.severity:
        vals["severity"] = args.severity
    if args.priority:
        vals["priority"] = _p(args.priority)
    if args.assignee:
        vals["assignee_id"] = _resolve(odoo, "res.users", args.assignee, "解决人")
    if args.project:
        vals["project_id"] = _resolve(odoo, "project.project", args.project, "项目")
    if args.task:
        vals["task_id"] = _resolve(odoo, "project.task", args.task, "任务")
    if args.sprint:
        vals["sprint_id"] = _resolve(odoo, SPRINT, args.sprint, "迭代")
    if args.found_version:
        vals["found_version"] = args.found_version
    if args.note is not None:
        vals["note"] = args.note
    if args.tags:
        # 追加标签（保留原有）
        cur = odoo.read(BUG, [bid], ["tag_ids"])[0]["tag_ids"]
        vals["tag_ids"] = [(6, 0, list(set(cur + _resolve_tags(odoo, args.tags))))]
    if not vals:
        raise OdooError("没有要更新的字段。")
    odoo.write(BUG, [bid], vals)
    print(f"✅ 已更新 Bug #{bid}：{', '.join(vals.keys())}")


def _bug_transition(method: str, word: str, needs_dup: bool = False):
    def runner(odoo: Odoo, args):
        ids = [_resolve_bug(odoo, x) for x in args.ids]
        if needs_dup:
            # 检查每个 bug 是否已设 duplicate_of_id
            for bid in ids:
                rec = odoo.read(BUG, [bid], ["duplicate_of_id"])[0]
                if not rec.get("duplicate_of_id"):
                    raise OdooError(
                        f"Bug #{bid} 还没设置「重复于」(duplicate_of_id)，无法标记重复。\n"
                        f"先用 bug-update {bid} --duplicate-of <主Bug> 设置，或改用 wontfix。"
                    )
        for bid in ids:
            odoo.execute_kw(BUG, method, [[bid]], {})
        if args.json:
            print(json.dumps({"ids": ids, "action": method}, ensure_ascii=False))
            return
        print(f"✅ 已{word} {len(ids)} 个 Bug：{', '.join('#' + str(i) for i in ids)}")
    return runner


def cmd_bug_delete(odoo: Odoo, args):
    ids = [_resolve_bug(odoo, x) for x in args.ids]
    try:
        odoo.unlink(BUG, ids)
    except OdooError as e:
        msg = str(e)
        if "不允许删除" in msg or "cannot be completed" in msg.lower():
            raise OdooError(
                f"❌ 删除失败：当前账号无「测试验收/管理员」权限。\n"
                f"   Odoo 限制：只有「测试验收 / 管理员」组可删除 Bug。\n"
                f"   替代做法：把 Bug 推进到 closed（reset → confirm → start → resolve → verify）。\n"
                f"   原始报错：{msg}"
            )
        raise
    print(f"✅ 已删除 {len(ids)} 个 Bug：{', '.join('#' + str(i) for i in ids)}")


# --------------------------------------------------------------------------- #
# Sprint
# --------------------------------------------------------------------------- #
def cmd_sprint_list(odoo: Odoo, args):
    domain = []
    if args.state:
        domain.append(("state", "=", args.state))
    if args.project:
        domain.append(("project_id", "=", _resolve(odoo, "project.project", args.project, "项目")))
    rows_data = odoo.search_read(
        SPRINT, domain,
        ["id", "name", "state", "project_id", "date_start", "date_end",
         "bug_count", "bug_closed_count", "progress"],
        order="date_start desc, id desc", limit=args.limit,
    )
    if args.json:
        print(json.dumps(rows_data, ensure_ascii=False, default=str))
        return
    SSTATE = {"planned": "📋计划", "active": "🚀进行", "done": "✅完成"}
    rows = []
    for r in rows_data:
        rows.append([
            r["id"], r["name"], SSTATE.get(r["state"], r["state"]),
            m2o_name(r.get("project_id")) or "-",
            r.get("date_start") or "-", r.get("date_end") or "-",
            f"{r.get('bug_closed_count', 0)}/{r.get('bug_count', 0)}",
            f"{r.get('progress', 0):.0f}%",
        ])
    print(render_table(rows, ["ID", "迭代", "状态", "项目", "开始", "结束", "已闭/总", "完成率"]))


def cmd_sprint_show(odoo: Odoo, args):
    sid = _resolve(odoo, SPRINT, args.id, "迭代")
    r = odoo.read(SPRINT, [sid], [
        "name", "state", "project_id", "date_start", "date_end", "description",
        "bug_count", "bug_closed_count", "progress",
    ])[0]
    if args.json:
        print(json.dumps(r, ensure_ascii=False, default=str))
        return
    SSTATE = {"planned": "📋计划", "active": "🚀进行", "done": "✅完成"}
    print(f"迭代：{r['name']}  ({SSTATE.get(r['state'], r['state'])})")
    print(f"项目：{m2o_name(r.get('project_id')) or '-'}   {r.get('date_start') or '?'} ~ {r.get('date_end') or '?'}")
    print(f"Bug：{r.get('bug_closed_count', 0)}/{r.get('bug_count', 0)} 已关闭   完成率 {r.get('progress', 0):.0f}%")
    if r.get("description"):
        print(f"说明：{r['description']}")
    # Bug 按状态分布
    dist = odoo.read_group(
        BUG, [["sprint_id", "=", sid]],
        ["state"], ["state"], lazy=False,
    )
    if dist:
        print("\nBug 状态分布：")
        for g in dist:
            st = g.get("state") or "-"
            cnt = g.get("state_count") or g.get("__count") or 0
            print(f"  {STATE.get(st, st):12s} {cnt}")


def cmd_sprint_add(odoo: Odoo, args):
    if not args.name:
        raise OdooError("--name 必填（迭代名称）。")
    vals = {"name": args.name}
    if args.project:
        vals["project_id"] = _resolve(odoo, "project.project", args.project, "项目")
    if args.start:
        vals["date_start"] = args.start
    if args.end:
        vals["date_end"] = args.end
    if args.desc:
        vals["description"] = args.desc
    sid = odoo.create(SPRINT, vals)
    if args.json:
        print(json.dumps({"id": sid}, ensure_ascii=False))
        return
    print(f"✅ 已建迭代 #{sid}：{args.name}")


def cmd_sprint_add_bugs(odoo: Odoo, args):
    sid = _resolve(odoo, SPRINT, args.id, "迭代")
    bids = [_resolve_bug(odoo, x) for x in args.bugs]
    odoo.write(BUG, bids, {"sprint_id": sid})
    print(f"✅ 已把 {len(bids)} 个 Bug 挂到迭代 #{sid}：{', '.join('#' + str(b) for b in bids)}")


def _sprint_transition(method: str, word: str):
    def runner(odoo: Odoo, args):
        sid = _resolve(odoo, SPRINT, args.id, "迭代")
        odoo.execute_kw(SPRINT, method, [[sid]], {})
        print(f"✅ 已{word}迭代 #{sid}")
    return runner


# --------------------------------------------------------------------------- #
# 标签
# --------------------------------------------------------------------------- #
def cmd_tag_list(odoo: Odoo, args):
    domain = [] if args.all else [("active", "=", True)]
    rows_data = odoo.search_read(TAG, domain, ["id", "name", "color", "active"], order="name")
    if args.json:
        print(json.dumps(rows_data, ensure_ascii=False, default=str))
        return
    rows = [[t["id"], t["name"], t.get("color") or 0, "✓" if t.get("active") else "✗"] for t in rows_data]
    print(render_table(rows, ["ID", "标签", "颜色", "启用"]))


def cmd_tag_add(odoo: Odoo, args):
    tid = odoo.create(TAG, {"name": args.name, "color": args.color})
    print(f"✅ 已建标签 #{tid}：{args.name}（颜色 {args.color}）")


# --------------------------------------------------------------------------- #
# 统计
# --------------------------------------------------------------------------- #
def cmd_stats(odoo: Odoo, args):
    by = args.by
    field_map = {
        "state": ("state", STATE),
        "severity": ("severity", SEVERITY),
        "priority": ("priority", PRIORITY),
        "resolution": ("resolution", RESOLUTION),
    }
    if by in field_map:
        fld, labels = field_map[by]
        groups = odoo.read_group(BUG, [], [fld], [fld], lazy=False)
        rows = []
        total = 0
        for g in sorted(groups, key=lambda x: x.get(fld) or "z"):
            k = g.get(fld) or "-"
            cnt = g.get(fld + "_count") or g.get("__count") or 0
            total += cnt
            rows.append([labels.get(k, k), cnt])
        rows.append(["合计", total])
        print(render_table(rows, [by, "Bug 数"]))
    elif by in ("project", "assignee", "reporter"):
        rel = {"project": "project_id", "assignee": "assignee_id", "reporter": "reporter_id"}[by]
        groups = odoo.formatted_read_group(BUG, [], rel, f"{rel}:count()")
        rows = []
        total = 0
        for g in sorted(groups, key=lambda x: -(x.get(f"{rel}:count()") or 0)):
            name = g.get(rel) or "（未指派）"
            cnt = g.get(f"{rel}:count()") or 0
            total += cnt
            rows.append([name, cnt])
        rows.append(["合计", total])
        print(render_table(rows, [by, "Bug 数"]))
    elif by == "sprint":
        groups = odoo.formatted_read_group(
            BUG, [], "sprint_id",
            "sprint_id:count(),state",
        )
        # 简化：按迭代计数
        sg = odoo.formatted_read_group(BUG, [], "sprint_id", "sprint_id:count()")
        rows = []
        total = 0
        for g in sorted(sg, key=lambda x: -(x.get("sprint_id:count()") or 0)):
            name = g.get("sprint_id") or "（无迭代）"
            cnt = g.get("sprint_id:count()") or 0
            total += cnt
            rows.append([name, cnt])
        rows.append(["合计", total])
        print(render_table(rows, ["迭代", "Bug 数"]))
    elif by == "tag":
        tg = odoo.formatted_read_group(BUG, [], "tag_ids", "tag_ids:count()")
        rows = []
        for g in sorted(tg, key=lambda x: -(x.get("tag_ids:count()") or 0)):
            name = g.get("tag_ids") or "（无标签）"
            cnt = g.get("tag_ids:count()") or 0
            rows.append([name, cnt])
        print(render_table(rows, ["标签", "Bug 数"]))
    else:
        raise OdooError(f"--by 不支持「{by}」。可选：state/severity/priority/resolution/project/assignee/reporter/sprint/tag")

    # 活跃/积压预警
    active = odoo.search_count(BUG, [["state", "in", list(ACTIVE_STATES)]])
    closed = odoo.search_count(BUG, [["state", "=", "closed"]])
    over_p1 = odoo.search_count(BUG, [
        ["state", "in", ("new", "confirmed")], ["priority", "in", ("p0", "p1")]
    ])
    print(f"\n活跃 {active} / 已关闭 {closed} / 总 {active + closed}")
    if over_p1:
        print(f"⚠️  {over_p1} 个 P0/P1 Bug 还在新建/已确认未处理，建议优先！")


# --------------------------------------------------------------------------- #
# argparse
# --------------------------------------------------------------------------- #
def build_parser():
    p = argparse.ArgumentParser(
        description="火一五 Odoo「测试验收」Bug/Sprint/标签管理",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    p.add_argument("--tools-md", help="凭据文件路径（默认 ~/.huo15/tools.md）")
    p.add_argument("--json", action="store_true", help="输出 JSON")
    sub = p.add_subparsers(dest="cmd", required=True)

    # bug-add
    a = sub.add_parser("bug-add", help="登记 Bug")
    a.add_argument("--title", required=True)
    a.add_argument("--project", required=True, help="所属项目（名字或 id）")
    a.add_argument("--severity", choices=list(SEVERITY), default="medium")
    a.add_argument("--priority", default="p2", help="p0-p3 或 0-3")
    a.add_argument("--desc", help="Bug 描述（复现步骤等）")
    a.add_argument("--assignee", help="解决人（名字或 我）")
    a.add_argument("--reporter", help="呈报人（默认当前用户）")
    a.add_argument("--task", help="关联任务")
    a.add_argument("--sprint", help="所属迭代")
    a.add_argument("--found-version", dest="found_version", help="发现版本")
    a.add_argument("--tags", help="标签，逗号分隔")
    a.add_argument("--cc", help="抄送人，逗号分隔")

    # bug-list
    li = sub.add_parser("bug-list", help="列 Bug")
    li.add_argument("--mine", action="store_true", help="指派给我的")
    li.add_argument("--reported-by-me", dest="reported_by_me", action="store_true", help="我呈报的")
    li.add_argument("--active", action="store_true", help="只看活跃（非 closed，默认即此）")
    li.add_argument("--closed", action="store_true", help="只看已关闭")
    li.add_argument("--all", action="store_true", help="全部状态（含已关闭）")
    li.add_argument("--state", choices=list(STATE))
    li.add_argument("--severity", choices=list(SEVERITY))
    li.add_argument("--priority", help="p0-p3 或 0-3")
    li.add_argument("--project")
    li.add_argument("--assignee")
    li.add_argument("--reporter")
    li.add_argument("--sprint")
    li.add_argument("--tag")
    li.add_argument("--search", help="标题关键词")
    li.add_argument("--order", default="auto")
    li.add_argument("--limit", type=int, default=80)

    # bug-show
    sh = sub.add_parser("bug-show", help="Bug 详情")
    sh.add_argument("id", help="Bug id / BUG-00001 / 标题关键词")

    # bug-update
    u = sub.add_parser("bug-update", help="修改 Bug")
    u.add_argument("id")
    u.add_argument("--title")
    u.add_argument("--desc")
    u.add_argument("--severity", choices=list(SEVERITY))
    u.add_argument("--priority")
    u.add_argument("--assignee")
    u.add_argument("--project")
    u.add_argument("--task")
    u.add_argument("--sprint")
    u.add_argument("--found-version", dest="found_version")
    u.add_argument("--note")
    u.add_argument("--tags", help="追加标签（逗号分隔，保留原标签）")
    u.add_argument("--duplicate-of", dest="duplicate_of", help="标记重复于（主 Bug）")

    # 状态流转（批量）
    for name, word, needs_dup in [
        ("confirm", "确认", False),
        ("start", "开始处理", False),
        ("resolve", "标记已解决", False),
        ("verify", "验收通过", False),
        ("reopen", "验收打回", False),
        ("wontfix", "不予处理", False),
        ("duplicate", "标记重复", True),
        ("reset", "重新打开", False),
    ]:
        sp = sub.add_parser(name, help=f"{word}（可批量，传 id/BUG-00001/标题）")
        sp.add_argument("ids", nargs="+")

    # bug-delete
    d = sub.add_parser("bug-delete", help="删除 Bug（仅「测试验收/管理员」可用）")
    d.add_argument("ids", nargs="+")

    # sprint
    sl = sub.add_parser("sprint-list", help="列迭代")
    sl.add_argument("--state", choices=["planned", "active", "done"])
    sl.add_argument("--project")
    sl.add_argument("--limit", type=int, default=50)

    ss = sub.add_parser("sprint-show", help="迭代详情")
    ss.add_argument("id")

    sa = sub.add_parser("sprint-add", help="建迭代")
    sa.add_argument("--name", required=True)
    sa.add_argument("--project")
    sa.add_argument("--start", help="开始日期 YYYY-MM-DD")
    sa.add_argument("--end", help="结束日期 YYYY-MM-DD")
    sa.add_argument("--desc")

    sab = sub.add_parser("sprint-add-bugs", help="把 Bug 挂到迭代")
    sab.add_argument("id", help="迭代 id 或名字")
    sab.add_argument("bugs", nargs="+", help="Bug id/BUG-00001/标题")

    for name, word in [
        ("sprint-start", "开始"), ("sprint-done", "完成"), ("sprint-reset", "重置")
    ]:
        sp = sub.add_parser(name, help=f"{word}迭代")
        sp.add_argument("id")

    # tag
    sub.add_parser("tag-list", help="列标签").add_argument("--all", action="store_true", help="含已停用")
    ta = sub.add_parser("tag-add", help="建标签")
    ta.add_argument("--name", required=True)
    ta.add_argument("--color", type=int, default=0)

    # stats
    st = sub.add_parser("stats", help="按维度统计")
    st.add_argument("--by", default="state",
                    choices=["state", "severity", "priority", "resolution",
                             "project", "assignee", "reporter", "sprint", "tag"])

    return p


def main(argv=None):
    args = build_parser().parse_args(argv if argv is not None else sys.argv[1:])
    try:
        odoo = Odoo(tools_md=args.tools_md)
        # bug 状态流转
        transitions = {
            "confirm": ("action_confirm", "确认"),
            "start": ("action_start", "开始处理"),
            "resolve": ("action_resolve", "标记已解决"),
            "verify": ("action_verify", "验收通过"),
            "reopen": ("action_reopen", "验收打回"),
            "wontfix": ("action_close_wontfix", "不予处理"),
            "duplicate": ("action_mark_duplicate", "标记重复"),
            "reset": ("action_reset", "重新打开"),
        }
        if args.cmd in transitions:
            method, word = transitions[args.cmd]
            needs_dup = args.cmd == "duplicate"
            _bug_transition(method, word, needs_dup)(odoo, args)
        elif args.cmd == "bug-add":
            cmd_bug_add(odoo, args)
        elif args.cmd == "bug-list":
            cmd_bug_list(odoo, args)
        elif args.cmd == "bug-show":
            cmd_bug_show(odoo, args)
        elif args.cmd == "bug-update":
            # duplicate-of 在 update 里处理
            if getattr(args, "duplicate_of", None):
                bid = _resolve_bug(odoo, args.id)
                dup_id = _resolve_bug(odoo, args.duplicate_of)
                odoo.write(BUG, [bid], {"duplicate_of_id": dup_id})
                print(f"✅ Bug #{bid} 标记重复于 {_resolve_bug(odoo, args.duplicate_of)}")
            cmd_bug_update(odoo, args)
        elif args.cmd == "bug-delete":
            cmd_bug_delete(odoo, args)
        elif args.cmd == "sprint-list":
            cmd_sprint_list(odoo, args)
        elif args.cmd == "sprint-show":
            cmd_sprint_show(odoo, args)
        elif args.cmd == "sprint-add":
            cmd_sprint_add(odoo, args)
        elif args.cmd == "sprint-add-bugs":
            cmd_sprint_add_bugs(odoo, args)
        elif args.cmd in ("sprint-start", "sprint-done", "sprint-reset"):
            smap = {"sprint-start": ("action_start", "开始"),
                    "sprint-done": ("action_done", "完成"),
                    "sprint-reset": ("action_reset", "重置")}
            method, word = smap[args.cmd]
            _sprint_transition(method, word)(odoo, args)
        elif args.cmd == "tag-list":
            cmd_tag_list(odoo, args)
        elif args.cmd == "tag-add":
            cmd_tag_add(odoo, args)
        elif args.cmd == "stats":
            cmd_stats(odoo, args)
    except OdooError as e:
        print(f"❌ {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
