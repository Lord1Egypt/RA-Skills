#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
hr.py — 辉火套件ERP「人力资源 HR」（员工/部门/考勤/请假/报销）

字段坑（详见 references/odoo-hr-api.md）：
  - hr.employee: name 通过 resource_id.name 关联(store=True)；user_id 关联系统用户。
  - 部门用 complete_name（层级名 "总部/研发部"），非 name。
  - 考勤 hr.attendance: check_in/check_out 是 Datetime/UTC；worked_hours 是 compute 不可直接写。
  - 考勤签到/签退走 hr.employee._attendance_action_change（不是 hr.attendance.create）。
  - 请假 hr.leave: state=confirm/refuse/validate1/validate/cancel；建假用 request_date_from/to(Date)非 date_from/to(Datetime,computed)。
  - 请假 number_of_days 是 compute（由 request_date_from/to + resource_calendar 算），不可直接写。
  - 请假审批走 action_approve（validate1→validate 或 confirm→validate）；拒绝 action_refuse。
  - 报销 hr.expense: state=draft/submitted/approved/posted/in_payment/paid/refused。
  - 报销 v19 无 sheet（hr.expense.sheet 已废弃），直接在 hr.expense 上操作。
  - 报销 action_submit(draft→submitted) → action_approve(submitted→approved) → action_post(approved→posted,建凭证)。

命令
  employees   列出员工   默认在职；--department 部门 / --job 岗位
  emp-show    员工详情
  departments 列出部门（含层级名和人数）
  attendance  查考勤  --employee X --from --to（默认今天）
  check-in    签到（当前用户关联的员工）
  check-out   签退
  leaves      列出请假  --employee / --department / --pending
  leave-add   建请假  --employee X --type 假期类型 --from --to
  leave-approve  批准请假
  leave-refuse   拒绝请假
  expenses    列出报销  --employee / --draft / --submitted / --approved
  expense-add    建报销  --employee X --product 产品 --qty 1 --amount 100
  expense-submit 提交报销（draft→submitted）
  expense-approve 批准报销（submitted→approved）
  expense-post   过账报销（approved→posted，建会计凭证）

示例
  python3 hr.py employees --department 研发部
  python3 hr.py attendance --employee 张三 --from 2026-08-01 --to 2026-08-31
  python3 hr.py check-in
  python3 hr.py leave-add --employee 张三 --type "年假" --from 2026-08-10 --to 2026-08-12
  python3 hr.py leave-approve 42
  python3 hr.py expense-add --employee 张三 --product "办公用品" --qty 1 --amount 200
  python3 hr.py expense-submit 42
"""

from __future__ import annotations

import argparse
import json
import sys

from odoo_client import Odoo, OdooError
from odoo_utils import from_utc, m2o_name, render_table, to_utc, today

EMP = "hr.employee"
DEPT = "hr.department"
ATT = "hr.attendance"
LEAVE = "hr.leave"
LEAVE_TYPE = "hr.leave.type"
EXPENSE = "hr.expense"

LEAVE_STATE = {
    "confirm": "待审批",
    "refuse": "已拒绝",
    "validate1": "待二审",
    "validate": "已批准",
    "cancel": "已取消",
}

EXPENSE_STATE = {
    "draft": "草稿",
    "submitted": "已提交",
    "approved": "已批准",
    "posted": "已入账",
    "in_payment": "付款中",
    "paid": "已付款",
    "refused": "已拒绝",
}


def _money(v) -> str:
    try:
        return f"{float(v or 0):,.2f}"
    except (TypeError, ValueError):
        return str(v)


def _resolve(odoo: Odoo, model: str, ref, label: str, args=None):
    if str(ref).isdigit():
        return int(ref)
    r = odoo.name_search(model, str(ref), args=args or [], limit=1)
    if not r:
        raise OdooError(f"找不到{label}「{ref}」。")
    return r[0][0]


def _resolve_employee(odoo: Odoo, ref, uid: int | None = None):
    """名字/id/「我」→ employee_id。"""
    if ref and str(ref).lower() == "我":
        if not uid:
            uid = odoo.ensure_uid()
        emps = odoo.search_read(EMP, [("user_id", "=", uid)], ["id", "name"], limit=1)
        if not emps:
            raise OdooError("当前登录用户没有关联的员工档案。")
        return emps[0]["id"]
    return _resolve(odoo, EMP, ref, "员工")


# --------------------------------------------------------------------------- #
# 员工 / 部门
# --------------------------------------------------------------------------- #
def cmd_employees(odoo: Odoo, args):
    domain = [("active", "=", True)]
    if args.department:
        dept_id = _resolve(odoo, DEPT, args.department, "部门")
        domain.append(("department_id", "child_of", dept_id))
    if args.job:
        domain.append(("job_id", "=", _resolve(odoo, "hr.job", args.job, "岗位")))
    if args.name:
        domain.append(("name", "ilike", args.name))
    emps = odoo.search_read(
        EMP, domain,
        ["name", "job_id", "department_id", "work_phone", "work_email",
         "user_id", "parent_id", "active"],
        order="name", limit=args.limit)
    if args.json:
        print(json.dumps(emps, ensure_ascii=False, default=str))
        return
    rows = []
    for e in emps:
        rows.append([
            e["id"], e.get("name") or "-",
            m2o_name(e.get("job_id")) or "-",
            m2o_name(e.get("department_id")) or "-",
            e.get("work_phone") or e.get("work_email") or "-",
            m2o_name(e.get("parent_id")) or "-",
        ])
    print(render_table(rows, ["ID", "姓名", "岗位", "部门", "电话/邮箱", "上级"]))


def cmd_emp_show(odoo: Odoo, args):
    e = odoo.read(EMP, [args.id], [
        "name", "job_id", "department_id", "work_phone", "work_email",
        "mobile_phone", "user_id", "parent_id", "coach_id", "active",
        "company_id", "work_location_type", "birthday", "private_phone",
        "private_email", "date_start"])
    if not e:
        raise OdooError(f"员工 #{args.id} 不存在。")
    e = e[0]
    print(f"👤 {e.get('name') or '-'}（#{args.id}）")
    print(f"   岗位：{m2o_name(e.get('job_id')) or '-'}   部门：{m2o_name(e.get('department_id')) or '-'}")
    print(f"   上级：{m2o_name(e.get('parent_id')) or '-'}   导师：{m2o_name(e.get('coach_id')) or '-'}")
    print(f"   工作电话：{e.get('work_phone') or '-'}   手机：{e.get('mobile_phone') or '-'}")
    print(f"   工作邮箱：{e.get('work_email') or '-'}")
    print(f"   入职日期：{e.get('date_start') or '-'}   生日：{e.get('birthday') or '-'}")
    print(f"   状态：{'在职' if e.get('active') else '离职'}")


def cmd_departments(odoo: Odoo, args):
    domain = [("active", "=", True)]
    depts = odoo.search_read(
        DEPT, domain,
        ["name", "complete_name", "manager_id", "parent_id", "total_employee"],
        order="complete_name", limit=args.limit)
    if args.json:
        print(json.dumps(depts, ensure_ascii=False, default=str))
        return
    rows = []
    for d in depts:
        rows.append([
            d["id"], d.get("complete_name") or d.get("name") or "-",
            m2o_name(d.get("manager_id")) or "-",
            m2o_name(d.get("parent_id")) or "-",
            d.get("total_employee") or 0,
        ])
    print(render_table(rows, ["ID", "部门", "负责人", "上级部门", "人数"]))


# --------------------------------------------------------------------------- #
# 考勤
# --------------------------------------------------------------------------- #
def cmd_attendance(odoo: Odoo, args):
    domain = []
    if args.employee:
        domain.append(("employee_id", "=", _resolve_employee(odoo, args.employee, odoo.ensure_uid())))
    if args.department:
        dept_id = _resolve(odoo, DEPT, args.department, "部门")
        domain.append(("employee_id.department_id", "child_of", dept_id))
    d_from = args.from_date or today()
    d_to = args.to_date or today()
    domain.append(("date", ">=", d_from))
    domain.append(("date", "<=", d_to))
    records = odoo.search_read(
        ATT, domain,
        ["employee_id", "check_in", "check_out", "worked_hours", "overtime_hours"],
        order="check_in desc", limit=args.limit)
    if args.json:
        print(json.dumps(records, ensure_ascii=False, default=str))
        return
    rows, total_hours = [], 0.0
    for r in records:
        wh = r.get("worked_hours") or 0
        total_hours += wh
        rows.append([
            r["id"], m2o_name(r.get("employee_id")) or "-",
            from_utc(r.get("check_in") or "", "%Y-%m-%d %H:%M") or "-",
            from_utc(r.get("check_out") or "", "%Y-%m-%d %H:%M") or "（未签退）",
            f"{wh:.1f}h",
            f"{r.get('overtime_hours') or 0:.1f}h" if r.get("overtime_hours") else "-",
        ])
    print(render_table(rows, ["ID", "员工", "签到", "签退", "工时", "加班"]))
    print(f"\n共 {len(records)} 条，合计 {total_hours:.1f}h")


def cmd_check_in(odoo: Odoo, args):
    uid = odoo.ensure_uid()
    emps = odoo.search_read(EMP, [("user_id", "=", uid)], ["id", "name"], limit=1)
    if not emps:
        raise OdooError("当前登录用户没有关联的员工档案，无法签到。")
    emp = emps[0]
    # _attendance_action_change 自动判断签到/签退
    result = odoo.execute_kw(EMP, "_attendance_action_change", [[emp["id"]]])
    # 判断是签到了还是签退了
    atts = odoo.search_read(
        ATT, [("employee_id", "=", emp["id"]), ("check_out", "=", False)],
        ["check_in"], order="check_in desc", limit=1)
    if atts:
        print(f"✅ {emp['name']} 已签到（{from_utc(atts[0].get('check_in') or '', '%H:%M')}）")
    else:
        print(f"✅ {emp['name']} 已签退")


def cmd_check_out(odoo: Odoo, args):
    uid = odoo.ensure_uid()
    emps = odoo.search_read(EMP, [("user_id", "=", uid)], ["id", "name"], limit=1)
    if not emps:
        raise OdooError("当前登录用户没有关联的员工档案，无法签退。")
    emp = emps[0]
    # 检查是否有未签退的记录
    open_atts = odoo.search_read(
        ATT, [("employee_id", "=", emp["id"]), ("check_out", "=", False)],
        ["id", "check_in"], limit=1)
    if not open_atts:
        print(f"ℹ️ {emp['name']} 当前没有待签退的考勤记录（可能已签退或未签到）")
        return
    # _attendance_action_change 会自动签退
    odoo.execute_kw(EMP, "_attendance_action_change", [[emp["id"]]])
    print(f"✅ {emp['name']} 已签退")


# --------------------------------------------------------------------------- #
# 请假
# --------------------------------------------------------------------------- #
def cmd_leaves(odoo: Odoo, args):
    uid = odoo.ensure_uid()
    domain = []
    if args.employee:
        domain.append(("employee_id", "=", _resolve_employee(odoo, args.employee, uid)))
    if args.department:
        dept_id = _resolve(odoo, DEPT, args.department, "部门")
        domain.append(("employee_id.department_id", "child_of", dept_id))
    if args.pending:
        domain.append(("state", "in", ("confirm", "validate1")))
    if not args.all and not args.employee:
        # 默认看当前用户关联员工的请假
        emps = odoo.search_read(EMP, [("user_id", "=", uid)], ["id"], limit=1)
        if emps:
            domain.append(("employee_id", "=", emps[0]["id"]))
        else:
            domain.append(("state", "in", ("confirm", "validate1")))
    leaves = odoo.search_read(
        LEAVE, domain,
        ["name", "employee_id", "holiday_status_id", "date_from", "date_to",
         "number_of_days", "state", "department_id"],
        order="date_from desc", limit=args.limit)
    if args.json:
        print(json.dumps(leaves, ensure_ascii=False, default=str))
        return
    rows = []
    for l in leaves:
        rows.append([
            l["id"],
            m2o_name(l.get("employee_id")) or "-",
            m2o_name(l.get("holiday_status_id")) or "-",
            from_utc(l.get("date_from") or "", "%Y-%m-%d %H:%M") or "-",
            from_utc(l.get("date_to") or "", "%Y-%m-%d %H:%M") or "-",
            f"{l.get('number_of_days') or 0:.1f}天",
            LEAVE_STATE.get(l.get("state"), l.get("state") or "-"),
        ])
    print(render_table(rows, ["ID", "员工", "类型", "开始", "结束", "天数", "状态"]))


def cmd_leave_add(odoo: Odoo, args):
    uid = odoo.ensure_uid()
    emp_id = _resolve_employee(odoo, args.employee, uid)
    type_id = _resolve(odoo, LEAVE_TYPE, args.type, "假期类型")
    vals = {
        "employee_id": emp_id,
        "holiday_status_id": type_id,
        "request_date_from": args.from_date,
        "request_date_to": args.to_date,
    }
    if args.reason:
        vals["notes"] = args.reason
    lid = odoo.create(LEAVE, vals)
    l = odoo.read(LEAVE, [lid], ["name", "number_of_days", "state"])[0]
    print(f"✅ 已建请假 {l.get('name') or '-'}（#{lid}），"
          f"{l.get('number_of_days') or 0:.1f}天，状态 {LEAVE_STATE.get(l.get('state'), l.get('state') or '-')}")


def cmd_leave_approve(odoo: Odoo, args):
    odoo.execute_kw(LEAVE, "action_approve", [[args.id]])
    l = odoo.read(LEAVE, [args.id], ["state"])[0]
    print(f"✅ 请假 #{args.id} 已批准（状态 → {LEAVE_STATE.get(l.get('state'), l.get('state') or '-')})")


def cmd_leave_refuse(odoo: Odoo, args):
    odoo.execute_kw(LEAVE, "action_refuse", [[args.id]])
    print(f"✅ 请假 #{args.id} 已拒绝")


# --------------------------------------------------------------------------- #
# 报销
# --------------------------------------------------------------------------- #
def cmd_expenses(odoo: Odoo, args):
    uid = odoo.ensure_uid()
    domain = []
    if args.employee:
        domain.append(("employee_id", "=", _resolve_employee(odoo, args.employee, uid)))
    if args.draft:
        domain.append(("state", "=", "draft"))
    elif args.submitted:
        domain.append(("state", "=", "submitted"))
    elif args.approved:
        domain.append(("state", "=", "approved"))
    if not args.all and not args.employee:
        emps = odoo.search_read(EMP, [("user_id", "=", uid)], ["id"], limit=1)
        if emps:
            domain.append(("employee_id", "=", emps[0]["id"]))
    expenses = odoo.search_read(
        EXPENSE, domain,
        ["name", "employee_id", "total_amount", "date", "state",
         "payment_mode", "product_id", "quantity"],
        order="date desc, id desc", limit=args.limit)
    if args.json:
        print(json.dumps(expenses, ensure_ascii=False, default=str))
        return
    rows, total = [], 0.0
    for e in expenses:
        total += e.get("total_amount") or 0
        pay_mode = "公司" if e.get("payment_mode") == "company_account" else "个人"
        rows.append([
            e["id"], (e.get("name") or "")[:20],
            m2o_name(e.get("employee_id")) or "-",
            _money(e.get("total_amount")),
            e.get("date") or "-",
            EXPENSE_STATE.get(e.get("state"), e.get("state") or "-"),
            pay_mode,
        ])
    print(render_table(rows, ["ID", "描述", "员工", "金额", "日期", "状态", "支付"]))
    print(f"\n共 {len(expenses)} 条，合计 {_money(total)}")


def cmd_expense_add(odoo: Odoo, args):
    uid = odoo.ensure_uid()
    emp_id = _resolve_employee(odoo, args.employee, uid)
    vals = {
        "employee_id": emp_id,
        "name": args.name or (args.product and f"报销：{args.product}") or "报销",
        "date": args.date or today(),
        "total_amount": args.amount,
    }
    if args.product:
        vals["product_id"] = _resolve(odoo, "product.product", args.product, "产品")
    if args.payment_mode:
        vals["payment_mode"] = args.payment_mode
    eid = odoo.create(EXPENSE, vals)
    e = odoo.read(EXPENSE, [eid], ["name", "total_amount", "state"])[0]
    print(f"✅ 已建报销 {e.get('name') or '-'}（#{eid}），金额 {_money(e.get('total_amount'))}，"
          f"状态 {EXPENSE_STATE.get(e.get('state'), e.get('state') or '-')}")


def cmd_expense_submit(odoo: Odoo, args):
    odoo.execute_kw(EXPENSE, "action_submit", [[args.id]])
    e = odoo.read(EXPENSE, [args.id], ["state"])[0]
    print(f"✅ 报销 #{args.id} 已提交（状态 → {EXPENSE_STATE.get(e.get('state'), e.get('state') or '-')})")


def cmd_expense_approve(odoo: Odoo, args):
    odoo.execute_kw(EXPENSE, "action_approve", [[args.id]])
    e = odoo.read(EXPENSE, [args.id], ["state"])[0]
    print(f"✅ 报销 #{args.id} 已批准（状态 → {EXPENSE_STATE.get(e.get('state'), e.get('state') or '-')})")


def cmd_expense_refuse(odoo: Odoo, args):
    odoo.execute_kw(EXPENSE, "action_refuse", [[args.id]])
    print(f"✅ 报销 #{args.id} 已拒绝")


def cmd_expense_post(odoo: Odoo, args):
    odoo.execute_kw(EXPENSE, "action_post", [[args.id]])
    e = odoo.read(EXPENSE, [args.id], ["state"])[0]
    print(f"✅ 报销 #{args.id} 已过账（状态 → {EXPENSE_STATE.get(e.get('state'), e.get('state') or '-')}，已生成会计凭证）")


# --------------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------------- #
def build_parser():
    p = argparse.ArgumentParser(description="辉火套件ERP 人力资源（员工/部门/考勤/请假/报销）")
    p.add_argument("--tools-md")
    p.add_argument("--json", action="store_true")
    sub = p.add_subparsers(dest="cmd", required=True)

    # 员工
    le = sub.add_parser("employees", help="列出员工")
    le.add_argument("--department", help="按部门筛选")
    le.add_argument("--job", help="按岗位筛选")
    le.add_argument("--name", help="按名字搜索")
    le.add_argument("--limit", type=int, default=100)

    es = sub.add_parser("emp-show", help="员工详情")
    es.add_argument("id", type=int)

    # 部门
    dp = sub.add_parser("departments", help="列出部门")
    dp.add_argument("--limit", type=int, default=100)

    # 考勤
    at = sub.add_parser("attendance", help="查考勤记录")
    at.add_argument("--employee", help="员工名字/id/我")
    at.add_argument("--department", help="按部门筛选")
    at.add_argument("--from", dest="from_date", help="开始日期 YYYY-MM-DD")
    at.add_argument("--to", dest="to_date", help="结束日期 YYYY-MM-DD")
    at.add_argument("--limit", type=int, default=200)

    ci = sub.add_parser("check-in", help="签到（当前用户）")
    co = sub.add_parser("check-out", help="签退（当前用户）")

    # 请假
    lv = sub.add_parser("leaves", help="列出请假")
    lv.add_argument("--employee", help="员工名字/id/我")
    lv.add_argument("--department", help="按部门筛选")
    lv.add_argument("--pending", action="store_true", help="只看待审批")
    lv.add_argument("--all", action="store_true", help="看全部")
    lv.add_argument("--limit", type=int, default=80)

    la = sub.add_parser("leave-add", help="建请假")
    la.add_argument("--employee", required=True, help="员工名字/id/我")
    la.add_argument("--type", required=True, help="假期类型（如 年假/病假/事假）")
    la.add_argument("--from", dest="from_date", required=True, help="开始日期 YYYY-MM-DD")
    la.add_argument("--to", dest="to_date", required=True, help="结束日期 YYYY-MM-DD")
    la.add_argument("--reason", help="请假原因")

    for name, hlp in [("leave-approve", "批准请假"), ("leave-refuse", "拒绝请假")]:
        sp = sub.add_parser(name, help=hlp)
        sp.add_argument("id", type=int)

    # 报销
    ex = sub.add_parser("expenses", help="列出报销")
    ex.add_argument("--employee", help="员工名字/id/我")
    ex.add_argument("--draft", action="store_true")
    ex.add_argument("--submitted", action="store_true")
    ex.add_argument("--approved", action="store_true")
    ex.add_argument("--all", action="store_true")
    ex.add_argument("--limit", type=int, default=80)

    ea = sub.add_parser("expense-add", help="建报销")
    ea.add_argument("--employee", required=True, help="员工名字/id/我")
    ea.add_argument("--product", help="产品（名字或 id）")
    ea.add_argument("--name", help="报销描述")
    ea.add_argument("--amount", type=float, required=True)
    ea.add_argument("--date", help="报销日期 YYYY-MM-DD")
    ea.add_argument("--payment-mode", choices=["own_account", "company_account"],
                     default="own_account", help="own_account=个人(报销) / company_account=公司")

    for name, hlp in [
        ("expense-submit", "提交报销"),
        ("expense-approve", "批准报销"),
        ("expense-refuse", "拒绝报销"),
        ("expense-post", "过账报销"),
    ]:
        sp = sub.add_parser(name, help=hlp)
        sp.add_argument("id", type=int)

    return p


def main(argv=None):
    args = build_parser().parse_args(argv if argv is not None else sys.argv[1:])
    try:
        odoo = Odoo(tools_md=args.tools_md)
        dispatch = {
            "employees": cmd_employees, "emp-show": cmd_emp_show,
            "departments": cmd_departments,
            "attendance": cmd_attendance, "check-in": cmd_check_in, "check-out": cmd_check_out,
            "leaves": cmd_leaves, "leave-add": cmd_leave_add,
            "leave-approve": cmd_leave_approve, "leave-refuse": cmd_leave_refuse,
            "expenses": cmd_expenses, "expense-add": cmd_expense_add,
            "expense-submit": cmd_expense_submit, "expense-approve": cmd_expense_approve,
            "expense-refuse": cmd_expense_refuse, "expense-post": cmd_expense_post,
        }
        dispatch[args.cmd](odoo, args)
    except OdooError as e:
        print(f"❌ {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
