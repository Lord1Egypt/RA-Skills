#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
accounting.py — 辉火套件ERP「会计 Accounting」（account.move / account.payment / account.journal / account.account）

字段坑（详见 references/odoo-accounting-api.md）：
  - account.move.state 只有 draft/posted/cancel（无 done）；move_type 区分发票(out_invoice)/账单(in_invoice)/退款(out_refund/in_refund)/日记账(entry)。
  - payment_state: not_paid/in_payment/paid/partial/reversed/blocked；invoicing_legacy 是旧版遗留。
  - 金额字段全 compute/store：amount_untaxed/amount_tax/amount_total/amount_residual（不可直接写，走 invoice_line_ids）。
  - 发票行用 invoice_line_ids（是 line_ids 的子集），行字段：product_id/name/quantity/price_unit/tax_ids/price_subtotal。
  - account.payment 创建需 payment_type(inbound收/outbound付)+partner_type(customer/supplier)+amount+partner_id+journal_id。
  - action_post 过账 = draft→posted（生成凭证行）；button_draft = 回草稿；button_cancel = 作废。
  - action_reverse 建反向发票（退款/信用票据）。

命令
  invoices  列出发票/账单  默认我的；--bills 供应商账单 / --draft 草稿 / --posted 已过账 / --unpaid 未付款 / --customer
  show      发票/账单详情 + 明细行
  add       建客户发票  --customer X --line "产品:数量[:单价]"（--line 可重复）
  bill      建供应商账单 --vendor X --line ...
  post      过账发票（draft→posted，生成凭证行）
  cancel    作废发票
  draft     回到草稿
  journals  列出账簿
  accounts  列出科目
  pay       登记付款  --partner X --amount N --type inbound|outbound --partner-type customer|supplier
  payments  列出付款

示例
  python3 accounting.py invoices --unpaid
  python3 accounting.py add --customer "某客户" --line "服务费:1:5000" --line "硬件:2:3000"
  python3 accounting.py bill --vendor "某供应商" --line "耗材:10:50"
  python3 accounting.py post 42
  python3 accounting.py pay --partner "某客户" --amount 5000 --type inbound --partner-type customer
  python3 accounting.py journals
  python3 accounting.py accounts --type income
"""

from __future__ import annotations

import argparse
import json
import sys

from odoo_client import Odoo, OdooError
from odoo_utils import from_utc, m2o_name, render_table, today

AM = "account.move"       # 发票/账单/日记账
AML = "account.move.line"  # 凭证行
AJ = "account.journal"    # 账簿
AA = "account.account"    # 会计科目
AP = "account.payment"    # 付款

MOVE_TYPE = {
    "out_invoice": "客户发票",
    "in_invoice": "供应商账单",
    "out_refund": "客户退款",
    "in_refund": "供应商退款",
    "entry": "日记账",
    "out_receipt": "销售收据",
    "in_receipt": "采购收据",
}

STATE = {"draft": "草稿", "posted": "已过账", "cancel": "已作废"}

PAY_STATE = {
    "not_paid": "未付款",
    "in_payment": "付款中",
    "paid": "已付款",
    "partial": "部分付款",
    "reversed": "已冲销",
    "blocked": "已阻止",
    "invoicing_legacy": "遗留",
}

PAY_STATE_LABEL = {
    "draft": "草稿",
    "in_process": "处理中",
    "paid": "已付款",
    "canceled": "已取消",
    "rejected": "已拒绝",
}

JOURNAL_TYPE = {
    "sale": "销售",
    "purchase": "采购",
    "cash": "现金",
    "bank": "银行",
    "credit": "信用卡",
    "general": "通用",
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


def _parse_lines(odoo: Odoo, specs: list) -> list:
    """解析 "产品:数量[:单价]" 格式的发票行。"""
    cmds = []
    for spec in specs:
        parts = [p.strip() for p in spec.split(":")]
        vals = {"product_id": _resolve(odoo, "product.product", parts[0], "产品"),
                "quantity": float(parts[1]) if len(parts) > 1 and parts[1] else 1.0}
        if len(parts) > 2 and parts[2]:
            vals["price_unit"] = float(parts[2])
        cmds.append((0, 0, vals))
    return cmds


# --------------------------------------------------------------------------- #
# 发票 / 账单
# --------------------------------------------------------------------------- #
def cmd_invoices(odoo: Odoo, args):
    uid = odoo.ensure_uid()
    domain = [("move_type", "in", ("out_invoice", "in_invoice", "out_refund", "in_refund"))]
    if args.bills:
        domain.append(("move_type", "in", ("in_invoice", "in_refund")))
    elif args.invoices_only:
        domain.append(("move_type", "in", ("out_invoice", "out_refund")))
    if args.draft:
        domain.append(("state", "=", "draft"))
    elif args.posted:
        domain.append(("state", "=", "posted"))
    if args.unpaid:
        domain.append(("payment_state", "in", ("not_paid", "partial")))
    if args.partner:
        domain.append(("partner_id", "=", _resolve(odoo, "res.partner", args.partner, "客户/供应商")))
    if not args.all:
        domain.append(("create_uid", "=", uid))
    moves = odoo.search_read(
        AM, domain,
        ["name", "move_type", "partner_id", "state", "amount_total",
         "amount_residual", "payment_state", "invoice_date", "invoice_date_due"],
        order="date desc, name desc", limit=args.limit)
    if args.json:
        print(json.dumps(moves, ensure_ascii=False, default=str))
        return
    rows, total, residual = [], 0.0, 0.0
    for m in moves:
        total += m.get("amount_total") or 0
        residual += m.get("amount_residual") or 0
        rows.append([
            m["id"], m.get("name") or "-",
            MOVE_TYPE.get(m.get("move_type"), m.get("move_type") or "-"),
            m2o_name(m.get("partner_id")) or "-",
            _money(m.get("amount_total")),
            _money(m.get("amount_residual")),
            PAY_STATE.get(m.get("payment_state"), m.get("payment_state") or "-"),
            m.get("invoice_date") or "-",
        ])
    print(render_table(rows, ["ID", "单号", "类型", "客户/供应商", "总额", "待付", "付款状态", "日期"]))
    print(f"\n共 {len(moves)} 张，总额 {_money(total)}，待付 {_money(residual)}")


def cmd_show(odoo: Odoo, args):
    m = odoo.read(AM, [args.id], [
        "name", "move_type", "partner_id", "state", "payment_state",
        "amount_untaxed", "amount_tax", "amount_total", "amount_residual",
        "invoice_date", "invoice_date_due", "journal_id", "invoice_line_ids",
        "ref", "narration", "date"])
    if not m:
        raise OdooError(f"会计凭证 #{args.id} 不存在。")
    m = m[0]
    mt = MOVE_TYPE.get(m.get("move_type"), m.get("move_type") or "-")
    print(f"📄 {mt} {m.get('name') or '-'}（#{args.id}）  [{STATE.get(m.get('state'), m.get('state') or '-')}]")
    print(f"   客户/供应商：{m2o_name(m.get('partner_id')) or '-'}")
    print(f"   账簿：{m2o_name(m.get('journal_id')) or '-'}   日期：{m.get('invoice_date') or m.get('date') or '-'}   到期：{m.get('invoice_date_due') or '-'}")
    print(f"   参考：{m.get('ref') or '-'}")
    print(f"   未税 {_money(m.get('amount_untaxed'))} + 税 {_money(m.get('amount_tax'))} = 总额 {_money(m.get('amount_total'))}   待付 {_money(m.get('amount_residual'))}")
    print(f"   付款状态：{PAY_STATE.get(m.get('payment_state'), m.get('payment_state') or '-')}")
    if m.get("invoice_line_ids"):
        lines = odoo.read(AML, m["invoice_line_ids"], [
            "product_id", "name", "quantity", "price_unit", "price_subtotal", "tax_ids"])
        rows = []
        for ln in lines:
            tax_names = ",".join(m2o_name(t) for t in (ln.get("tax_ids") or []))
            rows.append([
                m2o_name(ln.get("product_id"))[:16] or "-",
                (ln.get("name") or "")[:30],
                ln.get("quantity") or 0,
                _money(ln.get("price_unit")),
                _money(ln.get("price_subtotal")),
                tax_names[:12],
            ])
        print("\n   明细行：")
        for line in render_table(rows, ["产品", "描述", "数量", "单价", "小计", "税"]).splitlines():
            print("   " + line)


def cmd_add(odoo: Odoo, args):
    """建客户发票（out_invoice）。"""
    partner_id = _resolve(odoo, "res.partner", args.customer, "客户")
    vals = {
        "move_type": "out_invoice",
        "partner_id": partner_id,
        "invoice_line_ids": _parse_lines(odoo, args.line),
    }
    if args.date:
        vals["invoice_date"] = args.date
    mid = odoo.create(AM, vals)
    m = odoo.read(AM, [mid], ["name", "amount_total"])[0]
    print(f"✅ 已建客户发票 {m.get('name') or '-'}（#{mid}），总额 {_money(m.get('amount_total'))}")


def cmd_bill(odoo: Odoo, args):
    """建供应商账单（in_invoice）。"""
    partner_id = _resolve(odoo, "res.partner", args.vendor, "供应商")
    vals = {
        "move_type": "in_invoice",
        "partner_id": partner_id,
        "invoice_line_ids": _parse_lines(odoo, args.line),
    }
    if args.date:
        vals["invoice_date"] = args.date
    mid = odoo.create(AM, vals)
    m = odoo.read(AM, [mid], ["name", "amount_total"])[0]
    print(f"✅ 已建供应商账单 {m.get('name') or '-'}（#{mid}），总额 {_money(m.get('amount_total'))}")


def cmd_post(odoo: Odoo, args):
    """过账发票/账单（draft→posted，生成凭证行）。"""
    odoo.execute_kw(AM, "action_post", [[args.id]])
    print(f"✅ 会计凭证 #{args.id} 已过账（draft→posted，已生成凭证行）")


def cmd_cancel(odoo: Odoo, args):
    """作废发票/账单。"""
    odoo.execute_kw(AM, "button_cancel", [[args.id]])
    print(f"✅ 会计凭证 #{args.id} 已作废")


def cmd_draft(odoo: Odoo, args):
    """回到草稿。"""
    odoo.execute_kw(AM, "button_draft", [[args.id]])
    print(f"✅ 会计凭证 #{args.id} 已回到草稿")


# --------------------------------------------------------------------------- #
# 账簿 / 科目
# --------------------------------------------------------------------------- #
def cmd_journals(odoo: Odoo, args):
    domain = []
    if args.type:
        domain.append(("type", "=", args.type))
    journals = odoo.search_read(
        AJ, domain,
        ["name", "code", "type", "active"],
        order="sequence, type, code", limit=args.limit)
    if args.json:
        print(json.dumps(journals, ensure_ascii=False, default=str))
        return
    rows = []
    for j in journals:
        rows.append([
            j["id"], j.get("name") or "-", j.get("code") or "-",
            JOURNAL_TYPE.get(j.get("type"), j.get("type") or "-"),
            "✅" if j.get("active") else "❌",
        ])
    print(render_table(rows, ["ID", "名称", "代码", "类型", "启用"]))


def cmd_accounts(odoo: Odoo, args):
    domain = []
    if args.type:
        domain.append(("account_type", "=", args.type))
    if args.active_only:
        domain.append(("active", "=", True))
    accounts = odoo.search_read(
        AA, domain,
        ["code", "name", "account_type", "reconcile", "active"],
        order="code", limit=args.limit)
    if args.json:
        print(json.dumps(accounts, ensure_ascii=False, default=str))
        return
    rows = []
    for a in accounts:
        rows.append([
            a["id"], a.get("code") or "-", (a.get("name") or "")[:24],
            a.get("account_type") or "-",
            "✅" if a.get("reconcile") else "-",
            "✅" if a.get("active") else "❌",
        ])
    print(render_table(rows, ["ID", "代码", "名称", "类型", "可对账", "启用"]))


# --------------------------------------------------------------------------- #
# 付款
# --------------------------------------------------------------------------- #
def cmd_pay(odoo: Odoo, args):
    """登记付款。"""
    partner_id = _resolve(odoo, "res.partner", args.partner, "客户/供应商")
    # 找付款账簿（bank/cash 类型）
    journals = odoo.search_read(
        AJ, [("type", "in", ("bank", "cash")), ("active", "=", True)],
        ["name", "type"], limit=1)
    if not journals:
        raise OdooError("找不到可用的付款账簿（bank/cash），请先在系统中创建银行或现金账簿。")
    journal_id = journals[0]["id"]

    vals = {
        "payment_type": args.type,
        "partner_type": args.partner_type,
        "partner_id": partner_id,
        "amount": args.amount,
        "journal_id": journal_id,
        "date": args.date or today(),
    }
    if args.memo:
        vals["memo"] = args.memo
    pid = odoo.create(AP, vals)
    # 过账付款
    odoo.execute_kw(AP, "action_post", [[pid]])
    p = odoo.read(AP, [pid], ["name", "amount", "state"])[0]
    print(f"✅ 已登记并过账付款 {p.get('name') or '-'}（#{pid}），金额 {_money(p.get('amount'))}，状态 {PAY_STATE_LABEL.get(p.get('state'), p.get('state') or '-')}")


def cmd_payments(odoo: Odoo, args):
    uid = odoo.ensure_uid()
    domain = []
    if args.draft:
        domain.append(("state", "=", "draft"))
    elif args.paid:
        domain.append(("state", "=", "paid"))
    if args.partner:
        domain.append(("partner_id", "=", _resolve(odoo, "res.partner", args.partner, "客户/供应商")))
    if not args.all:
        domain.append(("create_uid", "=", uid))
    payments = odoo.search_read(
        AP, domain,
        ["name", "partner_id", "amount", "state", "payment_type", "partner_type", "date"],
        order="date desc, name desc", limit=args.limit)
    if args.json:
        print(json.dumps(payments, ensure_ascii=False, default=str))
        return
    rows, total = [], 0.0
    for p in payments:
        total += p.get("amount") or 0
        ptype = "收款" if p.get("payment_type") == "inbound" else "付款"
        rows.append([
            p["id"], p.get("name") or "-",
            m2o_name(p.get("partner_id")) or "-",
            _money(p.get("amount")), ptype,
            PAY_STATE_LABEL.get(p.get("state"), p.get("state") or "-"),
            p.get("date") or "-",
        ])
    print(render_table(rows, ["ID", "单号", "客户/供应商", "金额", "类型", "状态", "日期"]))
    print(f"\n共 {len(payments)} 笔，金额合计 {_money(total)}")


# --------------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------------- #
def build_parser():
    p = argparse.ArgumentParser(description="辉火套件ERP 会计（发票/账单/科目/付款）")
    p.add_argument("--tools-md")
    p.add_argument("--json", action="store_true")
    sub = p.add_subparsers(dest="cmd", required=True)

    # 发票/账单列表
    li = sub.add_parser("invoices", help="列出发票/账单")
    li.add_argument("--bills", action="store_true", help="只看供应商账单")
    li.add_argument("--invoices-only", action="store_true", help="只看客户发票")
    li.add_argument("--draft", action="store_true", help="只看草稿")
    li.add_argument("--posted", action="store_true", help="只看已过账")
    li.add_argument("--unpaid", action="store_true", help="只看未付款")
    li.add_argument("--partner", help="按客户/供应商筛选（名字或 id）")
    li.add_argument("--all", action="store_true", help="看全部（默认只看我的）")
    li.add_argument("--limit", type=int, default=80)

    # 详情
    sh = sub.add_parser("show", help="发票/账单详情")
    sh.add_argument("id", type=int)

    # 建发票
    ad = sub.add_parser("add", help="建客户发票")
    ad.add_argument("--customer", required=True)
    ad.add_argument("--line", action="append", required=True, help='"产品:数量[:单价]"，可重复')
    ad.add_argument("--date", help="发票日期 YYYY-MM-DD")

    # 建账单
    bl = sub.add_parser("bill", help="建供应商账单")
    bl.add_argument("--vendor", required=True)
    bl.add_argument("--line", action="append", required=True, help='"产品:数量[:单价]"，可重复')
    bl.add_argument("--date", help="账单日期 YYYY-MM-DD")

    # 状态操作
    for name, hlp in [("post", "过账"), ("cancel", "作废"), ("draft", "回草稿")]:
        sp = sub.add_parser(name, help=hlp)
        sp.add_argument("id", type=int)

    # 账簿
    jn = sub.add_parser("journals", help="列出账簿")
    jn.add_argument("--type", choices=list(JOURNAL_TYPE.keys()))
    jn.add_argument("--limit", type=int, default=50)

    # 科目
    ac = sub.add_parser("accounts", help="列出会计科目")
    ac.add_argument("--type", help="按类型筛选（如 income/expense/asset_cash/liability_payable）")
    ac.add_argument("--active-only", action="store_true")
    ac.add_argument("--limit", type=int, default=100)

    # 付款
    py = sub.add_parser("pay", help="登记付款")
    py.add_argument("--partner", required=True, help="客户/供应商（名字或 id）")
    py.add_argument("--amount", type=float, required=True)
    py.add_argument("--type", choices=["inbound", "outbound"], default="inbound",
                     help="inbound=收款 / outbound=付款")
    py.add_argument("--partner-type", choices=["customer", "supplier"], default="customer")
    py.add_argument("--date", help="付款日期 YYYY-MM-DD")
    py.add_argument("--memo", help="备注")

    # 付款列表
    ps = sub.add_parser("payments", help="列出付款")
    ps.add_argument("--draft", action="store_true")
    ps.add_argument("--paid", action="store_true")
    ps.add_argument("--partner", help="按客户/供应商筛选")
    ps.add_argument("--all", action="store_true")
    ps.add_argument("--limit", type=int, default=80)

    return p


def main(argv=None):
    args = build_parser().parse_args(argv if argv is not None else sys.argv[1:])
    try:
        odoo = Odoo(tools_md=args.tools_md)
        dispatch = {
            "invoices": cmd_invoices, "show": cmd_show,
            "add": cmd_add, "bill": cmd_bill,
            "post": cmd_post, "cancel": cmd_cancel, "draft": cmd_draft,
            "journals": cmd_journals, "accounts": cmd_accounts,
            "pay": cmd_pay, "payments": cmd_payments,
        }
        dispatch[args.cmd](odoo, args)
    except OdooError as e:
        print(f"❌ {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
