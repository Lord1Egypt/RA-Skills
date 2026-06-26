#!/usr/bin/env python3
"""发票查重技能 - 支持查重录入和查重记录查询"""

import argparse
import os
import sys

try:
    from common import is_error, post, validate_date
except ImportError:
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
    from common import is_error, post, validate_date


def enter(api_key: str, invoice_number: str, invoice_date: str,
          invoice_code: str = "", jshj: str = "") -> dict:
    payload = {"data": {"apiKey": api_key, "invoiceNumber": invoice_number,
                        "invoiceDate": invoice_date}}
    if invoice_code:
        payload["data"]["invoiceCode"] = invoice_code
    if jshj:
        payload["data"]["jshj"] = jshj
    return post("/api/jxplus/zxtSkill/repeat/enterSkillRepeatInvoice", payload)


def query(api_key: str, start_date: str = "", end_date: str = "",
          start_kprq_date: str = "", end_kprq_date: str = "",
          page_no: str = "1", page_size: str = "10") -> dict:
    payload = {"data": {"apiKey": api_key, "pageNo": page_no, "pageSize": page_size}}
    if start_date:
        payload["data"]["startDate"] = start_date
    if end_date:
        payload["data"]["endDate"] = end_date
    if start_kprq_date:
        payload["data"]["startKprqDate"] = start_kprq_date
    if end_kprq_date:
        payload["data"]["endKprqDate"] = end_kprq_date
    return post("/api/jxplus/zxtSkill/repeat/getRepeatInvoiceList", payload)


def fmt_enter(result: dict) -> str:
    err = is_error(result)
    if err:
        return err
    d = result.get("data", {})
    lines = [
        f"发票号码: {d.get('invoiceNumber', '-')}",
        f"发票代码: {d.get('invoiceCode') or '-'}",
        f"开票日期: {d.get('invoiceDate') or '-'}",
        f"价税合计: {d.get('jshj') or '-'}",
        f"重复类型: {d.get('repeatTypeName', '-')} ({d.get('repeatType', '-')})",
        f"采集时间: {d.get('collectTime', '-')}",
    ]
    return "\n".join(lines)


def fmt_query(result: dict) -> str:
    err = is_error(result)
    if err:
        return err
    d = result.get("data", {})
    total = d.get("total", "0")
    page = d.get("pageNo", "1")
    size = d.get("pageSize", "10")
    lines = [f"共 {total} 条记录 (第 {page} 页，每页 {size} 条)", "-" * 60]
    for i, item in enumerate(d.get("list", []), 1):
        lines.append(f"  [{i}] {item.get('invoiceNumber', '-')}")
        lines.append(f"      发票代码: {item.get('invoiceCode') or '-'}")
        lines.append(f"      开票日期: {item.get('invoiceDate', '-')}")
        lines.append(f"      价税合计: {item.get('jshj') or '-'}")
        lines.append(f"      重复类型: {item.get('repeatTypeName', '-')} ({item.get('repeatType', '-')})")
        lines.append(f"      采集时间: {item.get('collectTime', '-')}")
        if i < len(d.get("list", [])):
            lines.append("")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="发票查重技能")
    parser.add_argument("--api-key", default=os.environ.get("ZXT_API_KEY", ""),
                        help="apiKey，未传则读取环境变量 ZXT_API_KEY")
    sub = parser.add_subparsers(dest="action", required=True)

    p_enter = sub.add_parser("enter", help="查重录入")
    p_enter.add_argument("--invoice-number", required=True, help="发票号码")
    p_enter.add_argument("--invoice-date", required=True, help="开票日期 (YYYY-MM-DD)")
    p_enter.add_argument("--invoice-code", default="", help="发票代码")
    p_enter.add_argument("--jshj", default="", help="价税合计")

    p_query = sub.add_parser("query", help="查重记录查询")
    p_query.add_argument("--start-date", default="", help="采集日期开始 (YYYY-MM-DD)")
    p_query.add_argument("--end-date", default="", help="采集日期结束 (YYYY-MM-DD)")
    p_query.add_argument("--start-kprq-date", default="", help="开票日期开始 (YYYY-MM-DD)")
    p_query.add_argument("--end-kprq-date", default="", help="开票日期结束 (YYYY-MM-DD)")
    p_query.add_argument("--page-no", default="1", help="页码 (默认 1)")
    p_query.add_argument("--page-size", default="10", help="每页条数 (默认 10)")

    args = parser.parse_args()
    if not args.api_key:
        print("[错误] 缺少 apiKey。您需要完成以下三步，即可自动配置并执行技能：")
        print("")
        print("1. 注册账号")
        print("   访问中兴通简税Skill平台：https://skill.quandianfapiao.com/ 完成注册。")
        print("")
        print("2. 申请 apiKey")
        print("   登录后进入'技能中心'，复制您的 apiKey。")
        print("")
        print("3. 提供 apiKey")
        print("   将复制的 apiKey 发送给我，我将为您完成配置并立即执行技能。")
        sys.exit(1)

    if args.action == "enter":
        err = validate_date(args.invoice_date, "开票日期")
        if err:
            print(err)
            sys.exit(1)
        result = enter(args.api_key, args.invoice_number, args.invoice_date,
                       args.invoice_code, args.jshj)
        print(fmt_enter(result))
    elif args.action == "query":
        if args.start_date:
            err = validate_date(args.start_date, "采集日期开始")
            if err:
                print(err)
                sys.exit(1)
        if args.end_date:
            err = validate_date(args.end_date, "采集日期结束")
            if err:
                print(err)
                sys.exit(1)
        if args.start_kprq_date:
            err = validate_date(args.start_kprq_date, "开票日期开始")
            if err:
                print(err)
                sys.exit(1)
        if args.end_kprq_date:
            err = validate_date(args.end_kprq_date, "开票日期结束")
            if err:
                print(err)
                sys.exit(1)
        result = query(args.api_key, args.start_date, args.end_date,
                       args.start_kprq_date, args.end_kprq_date,
                       args.page_no, args.page_size)
        print(fmt_query(result))


if __name__ == "__main__":
    main()
