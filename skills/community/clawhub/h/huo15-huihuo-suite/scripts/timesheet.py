#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
timesheet.py — 火一五 Odoo「工时单 / Timesheets」统计与报表

工时单 = account.analytic.line 且 project_id 非空（没有 is_timesheet 字段，详见
references/odoo-timesheet-api.md）。工时小时数字段是 unit_amount。

命令
  by-employee   按员工汇总工时（默认本月）
  by-project    按项目汇总工时
  by-month      按「员工 × 月」汇总（看趋势，默认今年）
  detail        某员工/项目的工时明细
  log           录一条工时（--project --hours，可选 --task/--date/--desc/--employee）

时间范围（各命令通用）
  --month 2026-06       指定某月（自动算月初到月末）
  --from 2026-06-01 --to 2026-06-30
  --year 2026
  缺省                  本月

筛选
  --employee 张三   --project 官网改版   --department 研发部

示例
  python3 timesheet.py by-employee --month 2026-06
  python3 timesheet.py by-employee --department 研发部 --from 2026-06-01 --to 2026-06-30
  python3 timesheet.py detail --employee 张三 --month 2026-06
"""

from __future__ import annotations

import argparse
import calendar
import json
import sys

from odoo_client import Odoo, OdooError
from odoo_utils import hours, m2o_name, render_table, today

MODEL = "account.analytic.line"
TS_BASE = [("project_id", "!=", False)]  # 「是工时单」基线


# --------------------------------------------------------------------------- #
def _period(args):
    """解析时间范围 -> (date_from, date_to, 标签)。"""
    if args.month:
        y, m = map(int, args.month.split("-"))
        last = calendar.monthrange(y, m)[1]
        return f"{y:04d}-{m:02d}-01", f"{y:04d}-{m:02d}-{last:02d}", args.month
    if args.year:
        y = int(args.year)
        return f"{y}-01-01", f"{y}-12-31", str(y)
    if args.date_from or args.date_to:
        return (args.date_from or "1970-01-01", args.date_to or today(),
                f"{args.date_from or '…'}~{args.date_to or '…'}")
    # 默认本月
    t = today()
    y, m = int(t[:4]), int(t[5:7])
    last = calendar.monthrange(y, m)[1]
    return f"{y:04d}-{m:02d}-01", f"{y:04d}-{m:02d}-{last:02d}", f"{y:04d}-{m:02d}(本月)"


def _domain(odoo: Odoo, args):
    d0, d1, label = _period(args)
    domain = list(TS_BASE) + [("date", ">=", d0), ("date", "<=", d1)]
    if getattr(args, "employee", None):
        domain.append(("employee_id", "=", _resolve_employee(odoo, args.employee)))
    if getattr(args, "project", None):
        from project import _resolve_project  # 复用解析
        domain.append(("project_id", "=", _resolve_project(odoo, args.project)))
    if getattr(args, "department", None):
        domain.append(("department_id.name", "ilike", args.department))
    return domain, label


def _resolve_employee(odoo: Odoo, ref) -> int:
    if str(ref).isdigit():
        return int(ref)
    res = odoo.name_search("hr.employee", ref, limit=1)
    if not res:
        raise OdooError(f"找不到员工「{ref}」。")
    return res[0][0]


def _sum_field(g: dict) -> float:
    for k in ("unit_amount:sum", "unit_amount"):
        if k in g:
            return g[k] or 0.0
    return 0.0


def _count(g: dict) -> int:
    for k in ("__count", "employee_id_count", "project_id_count"):
        if k in g:
            return g[k]
    return 0


# --------------------------------------------------------------------------- #
def _grouped_report(odoo, args, groupby, key_label, headers):
    domain, label = _domain(odoo, args)
    groups = odoo.read_group(
        MODEL, domain, ["unit_amount:sum"], groupby, lazy=False
    )
    rows, total = [], 0.0
    for g in groups:
        keys = [m2o_name(g.get(f.split(":")[0])) or "(未指定)" for f in groupby]
        amt = _sum_field(g)
        total += amt
        rows.append(keys + [hours(amt), _count(g)])
    rows.sort(key=lambda r: -float(str(r[-2]).rstrip("h") or 0))
    if args.json:
        print(json.dumps(
            [{"keys": r[:-2], "hours": r[-2], "count": r[-1]} for r in rows],
            ensure_ascii=False))
        return
    print(f"📊 工时汇总（{label}）—— {key_label}")
    print(render_table(rows, headers + ["工时", "条数"]))
    print(f"\n合计：{hours(total)}，{len(rows)} 组")


def cmd_by_employee(odoo, args):
    _grouped_report(odoo, args, ["employee_id"], "按员工", ["员工"])


def cmd_by_project(odoo, args):
    _grouped_report(odoo, args, ["project_id"], "按项目", ["项目"])


def cmd_by_month(odoo, args):
    if not (args.year or args.month or args.date_from):
        args.year = today()[:4]
    _grouped_report(odoo, args, ["employee_id", "date:month"], "按员工×月",
                    ["员工", "月份"])


def cmd_detail(odoo, args):
    domain, label = _domain(odoo, args)
    lines = odoo.search_read(
        MODEL, domain,
        ["date", "employee_id", "project_id", "task_id", "unit_amount", "name"],
        order="date asc, id asc", limit=args.limit,
    )
    if args.json:
        print(json.dumps(lines, ensure_ascii=False, default=str))
        return
    rows, total = [], 0.0
    for r in lines:
        total += r.get("unit_amount") or 0
        rows.append([
            r["date"], m2o_name(r.get("employee_id")) or "-",
            m2o_name(r.get("project_id")) or "-",
            m2o_name(r.get("task_id")) or "-",
            hours(r.get("unit_amount")),
            (r["name"][:30] if r.get("name") and r["name"] != "/" else ""),
        ])
    print(f"🧾 工时明细（{label}）")
    print(render_table(rows, ["日期", "员工", "项目", "任务", "工时", "说明"]))
    print(f"\n合计：{hours(total)}，{len(lines)} 条")


def cmd_log(odoo, args):
    from project import _resolve_project
    vals = {
        "project_id": _resolve_project(odoo, args.project),
        "unit_amount": args.hours,
        "name": args.desc or "/",
        "date": args.date or today(),
    }
    if args.task:
        vals["task_id"] = int(args.task) if str(args.task).isdigit() else \
            odoo.name_search("project.task", args.task, limit=1)[0][0]
    if args.employee:
        vals["employee_id"] = _resolve_employee(odoo, args.employee)
    lid = odoo.create(MODEL, vals)
    print(f"✅ 已录工时 #{lid}：{hours(args.hours)} @ {vals['date']}")


# --------------------------------------------------------------------------- #
def _add_period_args(sp):
    sp.add_argument("--month", help="YYYY-MM")
    sp.add_argument("--year")
    sp.add_argument("--from", dest="date_from", help="YYYY-MM-DD")
    sp.add_argument("--to", dest="date_to", help="YYYY-MM-DD")
    sp.add_argument("--employee", help="员工名/id")
    sp.add_argument("--project", help="项目名/id")
    sp.add_argument("--department", help="部门名")


def build_parser():
    p = argparse.ArgumentParser(description="火一五 Odoo 工时单统计")
    p.add_argument("--tools-md")
    p.add_argument("--json", action="store_true")
    sub = p.add_subparsers(dest="cmd", required=True)

    for name in ("by-employee", "by-project", "by-month"):
        sp = sub.add_parser(name, help=f"{name} 汇总")
        _add_period_args(sp)

    de = sub.add_parser("detail", help="工时明细")
    _add_period_args(de)
    de.add_argument("--limit", type=int, default=300)

    lg = sub.add_parser("log", help="录一条工时")
    lg.add_argument("--project", required=True)
    lg.add_argument("--hours", type=float, required=True)
    lg.add_argument("--task")
    lg.add_argument("--date", help="YYYY-MM-DD，默认今天")
    lg.add_argument("--desc")
    lg.add_argument("--employee", help="默认当前用户对应员工")
    return p


def main(argv=None):
    args = build_parser().parse_args(argv if argv is not None else sys.argv[1:])
    try:
        odoo = Odoo(tools_md=args.tools_md)
        dispatch = {
            "by-employee": cmd_by_employee, "by-project": cmd_by_project,
            "by-month": cmd_by_month, "detail": cmd_detail, "log": cmd_log,
        }
        dispatch[args.cmd](odoo, args)
    except OdooError as e:
        print(f"❌ {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
