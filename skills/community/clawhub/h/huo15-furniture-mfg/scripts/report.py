#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
report.py — 单据 PDF 生成下载（合同 / 唛头 / 施工单等，发给客户或贴车间）

XML-RPC 渲染不了 QWeb 报表，本脚本走 web session：
  /web/session/authenticate 拿 session cookie → GET /report/pdf/<report_name>/<id>

命令
  list [--model sale|mo|picking|qc]      列出系统可用 PDF 报表
  pdf <单号> --report <别名> [-o 目录]    生成并下载 PDF，输出文件绝对路径

报表别名（test 库实测，huo15 定制模块提供）
  contract         销售合约·客户版（SO 或出库单）
  contract-seller  销售合约·买家版
  quote            标准报价单/订单 PDF（SO）
  label            包装唛头 A5（出库单或 MO）
  workorder        生产施工单（MO）
  delivery         交货单·自定义联次（出库单）
  也可直接传完整 report_name（如 huo15_product_label_a5.report_package_label）

示例
  python3 report.py pdf SO-260531-758 --report contract
  python3 report.py pdf MO-260604-643 --report label -o /tmp
  → 输出: ✅ /tmp/fmfg-reports/SO-260531-758-contract.pdf （AI 应把该文件直接发送给用户）
"""

from __future__ import annotations

import argparse
import http.cookiejar
import json
import re
import sys
import urllib.parse
import urllib.request
from pathlib import Path

from actions import resolve_record
from odoo_client import Odoo, OdooError

# 别名 → (适用模型集合, report_name 候选按序尝试)
ALIASES = {
    "contract": {
        "sale.order": "huo15_sale_contract_report.report_sale_contract_quotation",
        "stock.picking": "huo15_sale_contract_report.report_sale_contract",
    },
    "contract-seller": {
        "sale.order": "huo15_sale_contract_report.report_sale_contract_quotation_seller",
        "stock.picking": "huo15_sale_contract_report.report_sale_contract_seller",
    },
    "quote": {"sale.order": "sale.report_saleorder"},
    "label": {
        "stock.picking": "huo15_product_label_a5.report_package_label",
        "mrp.production": "huo15_product_label_a5.report_package_label",
    },
    "workorder": {"mrp.production": "huo15_product_label_a5.report_production_work_order"},
    "delivery": {"stock.picking": "huo15_product_label_a5.report_delivery_slip"},
}

DEFAULT_OUT = Path("/tmp/fmfg-reports")


class WebSession:
    """带 cookie 的 Odoo web 会话（只用于报表下载）。"""

    def __init__(self, odoo: Odoo):
        self.odoo = odoo
        jar = http.cookiejar.CookieJar()
        self.opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(jar))

    def authenticate(self):
        payload = {"jsonrpc": "2.0", "method": "call",
                   "params": {"db": self.odoo.db, "login": self.odoo.login,
                              "password": self.odoo.secret}}
        req = urllib.request.Request(
            f"{self.odoo.url}/web/session/authenticate",
            data=json.dumps(payload).encode(), headers={"Content-Type": "application/json"})
        with self.opener.open(req, timeout=60) as resp:
            data = json.loads(resp.read().decode())
        if data.get("error") or not (data.get("result") or {}).get("uid"):
            raise OdooError("web 会话认证失败：检查 login.py show 的账号密码。")

    def download_pdf(self, report_name: str, res_id: int) -> bytes:
        url = f"{self.odoo.url}/report/pdf/{urllib.parse.quote(report_name)}/{res_id}"
        with self.opener.open(url, timeout=120) as resp:
            blob = resp.read()
        if not blob.startswith(b"%PDF"):
            raise OdooError(
                f"返回内容不是 PDF（前 80 字节：{blob[:80]!r}）。"
                "常见原因：report_name 拼错 / 该模型无此报表 / 会话失效。")
        return blob


def cmd_list(args):
    odoo = Odoo()
    model_map = {"sale": "sale.order", "so": "sale.order", "mo": "mrp.production",
                 "picking": "stock.picking", "do": "stock.picking", "qc": "quality.check"}
    domain = [["report_type", "=", "qweb-pdf"]]
    if args.model:
        domain.append(["model", "=", model_map.get(args.model, args.model)])
    else:
        domain.append(["model", "in", ["sale.order", "stock.picking",
                                       "mrp.production", "quality.check"]])
    reps = odoo.search_read("ir.actions.report", domain,
                            ["name", "model", "report_name"], limit=60, order="model")
    for r in reps:
        print(f"{r['model']:16} | {r['name']:20} | {r['report_name']}")
    print("\n别名速查: " + ", ".join(ALIASES))


def cmd_pdf(args):
    odoo = Odoo()
    model, rec = resolve_record(odoo, args.ref)
    alias = args.report
    if alias in ALIASES:
        table = ALIASES[alias]
        if model not in table:
            raise OdooError(
                f"报表「{alias}」不适用于 {rec['name']}（{model}），"
                f"适用：{', '.join(table)}")
        report_name = table[model]
    elif "." in alias:
        report_name = alias
    else:
        raise OdooError(f"未知报表别名：{alias}（可用：{', '.join(ALIASES)}，或传完整 report_name）")

    out_dir = Path(args.out) if args.out else DEFAULT_OUT
    out_dir.mkdir(parents=True, exist_ok=True)
    safe_ref = re.sub(r"[^\w\-.]", "_", rec["name"])
    safe_alias = re.sub(r"[^\w\-.]", "_", alias.split(".")[-1])
    out_path = out_dir / f"{safe_ref}-{safe_alias}.pdf"

    sess = WebSession(odoo)
    sess.authenticate()
    blob = sess.download_pdf(report_name, rec["id"])
    out_path.write_bytes(blob)
    print(f"✅ {out_path}")
    print(f"   单据: {rec['name']} | 报表: {report_name} | {len(blob) / 1024:.0f} KB")
    print("   （AI：请把上面这个 PDF 文件直接作为文件消息发送给用户，不要发本地路径链接。）")


def build_parser():
    p = argparse.ArgumentParser(description="单据 PDF 生成下载")
    sub = p.add_subparsers(dest="cmd", required=True)
    l = sub.add_parser("list", help="列出可用报表")
    l.add_argument("--model", help="sale / mo / picking / qc 或完整模型名")
    d = sub.add_parser("pdf", help="生成并下载 PDF")
    d.add_argument("ref", help="单号（SO-/MO-/DO- 等）")
    d.add_argument("--report", required=True, help="别名或完整 report_name")
    d.add_argument("-o", "--out", help="输出目录（默认 /tmp/fmfg-reports）")
    return p


def main(argv=None):
    args = build_parser().parse_args(argv)
    try:
        {"list": cmd_list, "pdf": cmd_pdf}[args.cmd](args)
    except OdooError as e:
        print(f"❌ {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
