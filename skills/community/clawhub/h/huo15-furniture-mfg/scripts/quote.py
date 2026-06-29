#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
quote.py — 非标定制报价草稿（确认制）

把客户口头的"1.8 米床垫换乳胶面料做两张"变成系统里的草稿报价单：
产品行支持非标尺寸（cm）与主料，写入 sale_product_custom 的定制字段；
可一键带品牌档案（product.brand：Logo / 付款码 / 收发货地址 / 条款）。
只建/改 **draft 草稿**，不确认、不通知——业务员后续在系统里完善并走正式流程。

命令（默认 dry-run 预览，--yes 执行）
  draft --customer <客户名> --line "<产品>:<数量>[:<长>*<宽>*<高>[:<主料>]]" [--line ...]
        [--brand <品牌名>] [--note "备注"] [--yes]
  edit <SO单号> [--set N:数量[:单价[:折扣]]]... [--add 产品:数量[:长*宽*高[:主料]]]...
        [--del N]... [--yes]              # 不带操作参数 = 列出当前行
  drop <SO单号> [--yes]                   # 删除草稿报价单（仅 draft 可删）

示例
  python3 quote.py draft --customer 李梦 --line "山隐主垫-舒睡版:1:2000*2200*280:进口乳胶" --brand HeySleep
  python3 quote.py edit SO-260613-001 --set 1:2:1580 --add "山隐顶垫:1" --yes
  python3 quote.py drop SO-260613-001 --yes
"""

from __future__ import annotations

import argparse
import sys

from actions import _confirm_gate, resolve_record
from odoo_client import Odoo, OdooError
from odoo_utils import m2o_name, money, qty


def _parse_line(spec: str, odoo: Odoo) -> dict:
    """'产品关键词:数量[:长*宽*高[:主料]]' → 订单行 vals + 预览信息。"""
    parts = [p.strip() for p in spec.split(":")]
    if len(parts) < 2:
        raise OdooError(f"行格式错误：{spec!r}（至少要 产品:数量）")
    kw, qty_s = parts[0], parts[1]
    try:
        quantity = float(qty_s)
    except ValueError:
        raise OdooError(f"数量不是数字：{qty_s!r}（行 {spec!r}）")

    hits = odoo.search_read(
        "product.product",
        ["&", ["sale_ok", "=", True],
         "|", ["name", "ilike", kw], ["default_code", "ilike", kw]],
        ["name", "list_price", "uom_id"], limit=5)
    if not hits:
        raise OdooError(f"找不到可售产品：{kw}")
    prod = hits[0]

    vals = {"product_id": prod["id"], "product_uom_qty": quantity}
    desc = []
    if len(parts) >= 3 and parts[2]:
        dims = parts[2].replace("×", "*").replace("x", "*").replace("X", "*").split("*")
        if len(dims) != 3:
            raise OdooError(f"尺寸格式错误：{parts[2]!r}（应为 长*宽*高，单位 cm）")
        try:
            l, w, h = (float(d) for d in dims)
        except ValueError:
            raise OdooError(f"尺寸不是数字：{parts[2]!r}")
        vals.update(custom_length=l, custom_width=w, custom_height=h,
                    is_custom_product=True)
        desc.append(f"非标 {qty(l)}×{qty(w)}×{qty(h)}cm")
    if len(parts) >= 4 and parts[3]:
        vals["custom_material"] = parts[3]
        desc.append(f"主料 {parts[3]}")
    return {"vals": vals, "product": prod, "qty": quantity,
            "candidates": hits[1:], "desc": "、".join(desc)}


def _resolve_brand(odoo: Odoo, name: str) -> dict | None:
    """品牌名 → product.brand 记录（sale_brand_extension，后端现成）。"""
    if not name:
        return None
    bs = odoo.search_read("product.brand", [["name", "ilike", name]],
                          ["name", "company_name"], limit=3)
    if not bs:
        avail = [b["name"] for b in odoo.search_read("product.brand", [], ["name"], limit=10)]
        raise OdooError(f"找不到品牌：{name}（可用：{'、'.join(avail)}）")
    return bs[0]


def cmd_draft(args):
    odoo = Odoo()
    partners = odoo.name_search("res.partner", args.customer, limit=5)
    if not partners:
        raise OdooError(f"找不到客户：{args.customer}")
    pid, pname = partners[0]
    lines = [_parse_line(spec, odoo) for spec in args.line]
    brand = _resolve_brand(odoo, args.brand)

    print("🧾 将要执行：创建草稿报价单（draft，不确认不通知）")
    print(f"   客户: {pname}"
          + (f"（同名还有: {', '.join(p[1] for p in partners[1:])}）" if len(partners) > 1 else ""))
    if brand:
        print(f"   品牌档案: {brand['name']}（带 {brand.get('company_name') or ''} 抬头/付款码/地址/条款）")
    for ln in lines:
        extra = f" | {ln['desc']}" if ln["desc"] else ""
        print(f"   行: {ln['product']['name']} × {qty(ln['qty'])}"
              f"（目录价 {money(ln['product']['list_price'])}）{extra}")
        if ln["candidates"]:
            print(f"      产品同名候选: {', '.join(c['name'] for c in ln['candidates'])}"
                  "（如匹配错请换更精确的关键词重跑）")
    if args.note:
        print(f"   备注: {args.note}")
    _confirm_gate(args.yes)

    vals = {"partner_id": pid,
            "order_line": [(0, 0, ln["vals"]) for ln in lines]}
    if brand:
        vals["brand_id"] = brand["id"]
    if args.note:
        vals["note"] = args.note
    so_id = odoo.create("sale.order", vals)
    so = odoo.read("sale.order", [so_id], ["name", "amount_total"])[0]
    print(f"✅ 草稿报价单已创建：{so['name']}（合计 {money(so['amount_total'])}，状态=报价单）")
    print(f"   改行：python3 quote.py edit {so['name']}    误建可撤：python3 quote.py drop {so['name']} --yes")


def cmd_edit(args):
    odoo = Odoo()
    model, rec = resolve_record(odoo, args.ref)
    if model != "sale.order":
        raise OdooError(f"{rec['name']} 不是销售单。")
    cur = odoo.read("sale.order", [rec["id"]], ["state", "amount_total"])[0]
    if cur["state"] != "draft":
        raise OdooError(f"{rec['name']} 状态为 {cur['state']}，只能编辑 draft 草稿报价。")
    cur_lines = odoo.search_read(
        "sale.order.line",
        [["order_id", "=", rec["id"]], ["display_type", "=", False]],
        ["product_id", "product_uom_qty", "price_unit", "discount"], order="sequence,id")

    # 无操作参数 → 列出当前行供参考
    if not (args.set or args.add or args.dele):
        print(f"📋 {rec['name']}（{m2o_name(rec.get('partner_id'))}，{money(cur['amount_total'])}）当前报价行：")
        for idx, l in enumerate(cur_lines, 1):
            d = f" -{qty(l['discount'])}%" if l.get("discount") else ""
            print(f"  {idx}. {m2o_name(l['product_id'])} × {qty(l['product_uom_qty'])} @ {money(l['price_unit'])}{d}")
        print("编辑：--set N:数量[:单价[:折扣]] / --add 产品:数量[:长*宽*高[:主料]] / --del N")
        return

    cmds, ops = [], []
    for spec in (args.set or []):
        parts = spec.split(":")
        n = int(parts[0])
        if not (1 <= n <= len(cur_lines)):
            raise OdooError(f"行号 {n} 超范围（1~{len(cur_lines)}）")
        line = cur_lines[n - 1]
        vals, chg = {}, []
        if len(parts) >= 2 and parts[1]:
            vals["product_uom_qty"] = float(parts[1]); chg.append(f"数量→{parts[1]}")
        if len(parts) >= 3 and parts[2]:
            vals["price_unit"] = float(parts[2]); chg.append(f"单价→{money(float(parts[2]))}")
        if len(parts) >= 4 and parts[3]:
            vals["discount"] = float(parts[3]); chg.append(f"折扣→{parts[3]}%")
        if not vals:
            raise OdooError(f"--set {spec!r} 没给任何新值")
        cmds.append((1, line["id"], vals))
        ops.append(f"改第{n}行 {m2o_name(line['product_id'])}：{'，'.join(chg)}")
    for n_s in (args.dele or []):
        n = int(n_s)
        if not (1 <= n <= len(cur_lines)):
            raise OdooError(f"行号 {n} 超范围（1~{len(cur_lines)}）")
        line = cur_lines[n - 1]
        cmds.append((2, line["id"], False))
        ops.append(f"删第{n}行 {m2o_name(line['product_id'])}")
    for spec in (args.add or []):
        ln = _parse_line(spec, odoo)
        cmds.append((0, 0, ln["vals"]))
        ops.append(f"加行 {ln['product']['name']} × {qty(ln['qty'])}"
                   + (f" | {ln['desc']}" if ln["desc"] else ""))

    print(f"✏️ 将要执行：编辑草稿报价 {rec['name']}（现合计 {money(cur['amount_total'])}）")
    for op in ops:
        print("   ·", op)
    _confirm_gate(args.yes)
    odoo.write("sale.order", rec["id"], {"order_line": cmds})
    after = odoo.read("sale.order", [rec["id"]], ["amount_total"])[0]
    print(f"✅ 已编辑，新合计 {money(after['amount_total'])}")


def cmd_drop(args):
    odoo = Odoo()
    model, rec = resolve_record(odoo, args.ref)
    if model != "sale.order":
        raise OdooError(f"{rec['name']} 不是销售单。")
    cur = odoo.read("sale.order", [rec["id"]], ["state", "amount_total"])[0]
    if cur["state"] != "draft":
        raise OdooError(f"{rec['name']} 状态为 {cur['state']}，只允许删除 draft 草稿。")
    print(f"🗑 将要执行：删除草稿报价单 {rec['name']}（{m2o_name(rec.get('partner_id'))}，"
          f"{money(cur['amount_total'])}）")
    _confirm_gate(args.yes)
    odoo.unlink("sale.order", rec["id"])
    print("✅ 已删除。")


def build_parser():
    p = argparse.ArgumentParser(description="非标定制报价草稿（确认制）")
    sub = p.add_subparsers(dest="cmd", required=True)
    d = sub.add_parser("draft", help="创建草稿报价单")
    d.add_argument("--customer", required=True)
    d.add_argument("--line", action="append", required=True,
                   help='产品:数量[:长*宽*高[:主料]]，可重复')
    d.add_argument("--brand", help="品牌档案名（带 Logo/付款码/地址/条款）")
    d.add_argument("--note")
    d.add_argument("--yes", action="store_true")
    e = sub.add_parser("edit", help="编辑草稿报价行")
    e.add_argument("ref")
    e.add_argument("--set", action="append", help="N:数量[:单价[:折扣]]，可重复")
    e.add_argument("--add", action="append", help="产品:数量[:长*宽*高[:主料]]，可重复")
    e.add_argument("--del", dest="dele", action="append", help="行号，可重复")
    e.add_argument("--yes", action="store_true")
    r = sub.add_parser("drop", help="删除草稿报价单")
    r.add_argument("ref")
    r.add_argument("--yes", action="store_true")
    return p


def main(argv=None):
    args = build_parser().parse_args(argv)
    try:
        {"draft": cmd_draft, "edit": cmd_edit, "drop": cmd_drop}[args.cmd](args)
    except OdooError as e:
        print(f"❌ {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
