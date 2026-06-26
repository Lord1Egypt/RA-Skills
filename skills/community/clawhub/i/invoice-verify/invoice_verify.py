#!/usr/bin/env python3
"""发票查验技能 - 支持按票面查验和按文件查验"""

import argparse
import os
import sys

try:
    from common import fmt_invoice_basic, fmt_items, is_error, post, post_file, validate_date
except ImportError:
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
    from common import fmt_invoice_basic, fmt_items, is_error, post, post_file, validate_date


def inspect(api_key: str, invoice_number: str, invoice_date: str,
            jejym: str, invoice_code: str = "") -> dict:
    payload = {"data": {"apiKey": api_key, "invoiceNumber": invoice_number,
                        "invoiceDate": invoice_date, "jejym": jejym}}
    if invoice_code:
        payload["data"]["invoiceCode"] = invoice_code
    return post("/api/jxplus/zxtSkill/inspection/queryInspectionInvoice", payload)


def inspect_file(api_key: str, file_path: str) -> dict:
    if not os.path.isfile(file_path):
        return {"status": "-1", "message": f"文件不存在: {file_path}"}
    ext = os.path.splitext(file_path)[1].lower()
    if ext not in (".pdf", ".ofd", ".xml", ".jpg", ".png"):
        return {"status": "-1", "message": f"不支持的文件类型: {ext}，仅支持 pdf/ofd/xml/jpg/png"}
    return post_file("/api/jxplus/zxtSkill/inspection/queryInspectionFile", api_key, file_path)


def query_record(api_key: str, kprq_start: str = "", kprq_end: str = "",
                 invoice_number: str = "", invoice_code: str = "",
                 fplx_list: list = None, page_no: str = "1",
                 page_size: str = "10", cysj_start: str = "", cysj_end: str = "") -> dict:
    payload = {"data": {"apiKey": api_key, "pageNo": page_no, "pageSize": page_size}}
    if kprq_start:
        payload["data"]["kprqStart"] = kprq_start
    if kprq_end:
        payload["data"]["kprqEnd"] = kprq_end
    if cysj_start:
        payload["data"]["cysjStart"] = cysj_start
    if cysj_end:
        payload["data"]["cysjEnd"] = cysj_end
    if invoice_number:
        payload["data"]["invoiceNumber"] = invoice_number
    if invoice_code:
        payload["data"]["invoiceCode"] = invoice_code
    if fplx_list:
        payload["data"]["fplxList"] = fplx_list
    return post("/api/jxplus/zxtSkill/inspection/queryInspectionRecord", payload)


def fmt_record(result: dict) -> str:
    err = is_error(result)
    if err:
        return err
    d = result.get("data", {})
    total = d.get("total", "0")
    page = d.get("pageNo", "1")
    size = d.get("pageSize", "10")
    lines = [f"共 {total} 条查验记录 (第 {page} 页，每页 {size} 条)", "-" * 60]
    for i, item in enumerate(d.get("list", []), 1):
        lines.append(f"  [{i}] {item.get('invoiceNumber', '-')}")
        lines.append(f"      发票代码: {item.get('invoiceCode') or '-'}")
        lines.append(f"      发票类型: {item.get('fplxName', '-')} ({item.get('fplx', '-')})")
        lines.append(f"      开票日期: {item.get('kprq', '-')}")
        lines.append(f"      价税合计: {item.get('jshj', '-')}")
        lines.append(f"      销售方: {item.get('xsfMc', '-')}")
        lines.append(f"      查验时间: {item.get('cysj') or '-'}")
        lines.append(f"      查验状态: {item.get('cyztName', '-')} ({item.get('cyzt', '-')})")
        if i < len(d.get("list", [])):
            lines.append("")
    return "\n".join(lines)


def fmt_invoice(d: dict) -> list:
    lines = fmt_invoice_basic(d)
    lines.extend([
        f"  发票状态: {d.get('fpStatus', '-')}",
        f"  备注: {d.get('remark') or '-'}",
    ])
    items = d.get("items")
    if items:
        lines.append("  明细项目:")
        lines.extend(fmt_items(items))
    return lines


def fmt_inspect(result: dict) -> str:
    err = is_error(result)
    if err:
        return err
    d = result.get("data", {})
    lines = ["查验结果:"]
    lines.extend(fmt_invoice(d))
    return "\n".join(lines)


def fmt_inspect_file(result: dict) -> str:
    err = is_error(result)
    if err:
        return err
    data = result.get("data", {})
    if isinstance(data, list):
        lines = [f"查验结果: 共 {len(data)} 张发票", "=" * 60]
        for i, d in enumerate(data, 1):
            lines.append(f"发票 {i}:")
            lines.extend(fmt_invoice(d))
            if i < len(data):
                lines.append("-" * 60)
        return "\n".join(lines)
    lines = ["查验结果:"]
    lines.extend(fmt_invoice(data))
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="发票查验技能")
    parser.add_argument("--api-key", default=os.environ.get("ZXT_API_KEY", ""),
                        help="apiKey，未传则读取环境变量 ZXT_API_KEY")
    sub = parser.add_subparsers(dest="action", required=True)

    p_inspect = sub.add_parser("inspect", help="按票面查验")
    p_inspect.add_argument("--invoice-number", required=True, help="发票号码")
    p_inspect.add_argument("--invoice-date", required=True, help="开票日期 (YYYY-MM-DD)")
    p_inspect.add_argument("--jejym", required=True, help="金额或校验码")
    p_inspect.add_argument("--invoice-code", default="", help="发票代码")

    p_file = sub.add_parser("file", help="按文件查验")
    p_file.add_argument("--file", required=True, help="发票文件路径 (pdf/ofd/xml/jpg/png)")

    p_record = sub.add_parser("record", help="查询查验记录")
    p_record.add_argument("--kprq-start", default="", help="开票日期开始 (YYYY-MM-DD)")
    p_record.add_argument("--kprq-end", default="", help="开票日期结束 (YYYY-MM-DD)")
    p_record.add_argument("--invoice-number", default="", help="发票号码")
    p_record.add_argument("--invoice-code", default="", help="发票代码")
    p_record.add_argument("--fplx", nargs="*", default=[], help="发票类型筛选（可多选）")
    p_record.add_argument("--page-no", default="1", help="页码 (默认 1)")
    p_record.add_argument("--page-size", default="10", help="每页条数 (默认 10)")
    p_record.add_argument("--cysj-start", default="", help="查验时间开始 (YYYY-MM-DD)")
    p_record.add_argument("--cysj-end", default="", help="查验时间结束 (YYYY-MM-DD)")

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

    if args.action == "inspect":
        err = validate_date(args.invoice_date, "开票日期")
        if err:
            print(err)
            sys.exit(1)
        result = inspect(args.api_key, args.invoice_number, args.invoice_date,
                         args.jejym, args.invoice_code)
        print(fmt_inspect(result))
    elif args.action == "file":
        result = inspect_file(args.api_key, args.file)
        print(fmt_inspect_file(result))
    elif args.action == "record":
        if args.kprq_start:
            err = validate_date(args.kprq_start, "开票日期开始")
            if err:
                print(err)
                sys.exit(1)
        if args.kprq_end:
            err = validate_date(args.kprq_end, "开票日期结束")
            if err:
                print(err)
                sys.exit(1)
        if args.cysj_start:
            err = validate_date(args.cysj_start, "查验时间开始")
            if err:
                print(err)
                sys.exit(1)
        if args.cysj_end:
            err = validate_date(args.cysj_end, "查验时间结束")
            if err:
                print(err)
                sys.exit(1)
        fplx_list = args.fplx if args.fplx else None
        result = query_record(args.api_key, args.kprq_start, args.kprq_end,
                              args.invoice_number, args.invoice_code,
                              fplx_list, args.page_no, args.page_size,
                              args.cysj_start, args.cysj_end)
        print(fmt_record(result))


if __name__ == "__main__":
    main()
