#!/usr/bin/env python3
"""发票识别技能 - 通过上传发票文件进行 OCR 识别"""

import argparse
import os
import sys

try:
    from common import fmt_invoice_basic, fmt_items, is_error, post_file
except ImportError:
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
    from common import fmt_invoice_basic, fmt_items, is_error, post_file


def ocr(api_key: str, file_path: str) -> dict:
    if not os.path.isfile(file_path):
        return {"status": "-1", "message": f"文件不存在: {file_path}"}
    ext = os.path.splitext(file_path)[1].lower()
    if ext not in (".pdf", ".ofd", ".jpeg", ".jpg", ".png", ".xml"):
        return {"status": "-1", "message": f"不支持的文件类型: {ext}，仅支持 pdf/ofd/jpeg/jpg/png/xml"}
    return post_file("/api/jxplus/zxtSkill/discern/invoiceDiscern", api_key, file_path)


def fmt_result(result: dict) -> str:
    err = is_error(result)
    if err:
        return err
    d = result.get("data", {})
    lines = ["识别结果:"]
    lines.extend(fmt_invoice_basic(d))
    lines.extend([
        f"  收款人: {d.get('payee') or '-'}",
        f"  复核人: {d.get('reviewer') or '-'}",
        f"  开票人: {d.get('invoicer') or '-'}",
        f"  机器编号: {d.get('machineNo') or '-'}",
        f"  校验码: {d.get('checkCode') or '-'}",
        f"  密码区: {d.get('passwordArea') or '-'}",
        f"  备注: {d.get('remark') or '-'}",
    ])
    items = d.get("item") or d.get("items")
    if items:
        lines.append("  明细项目:")
        lines.extend(fmt_items(items))
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="发票识别技能")
    parser.add_argument("--api-key", default=os.environ.get("ZXT_API_KEY", ""),
                        help="apiKey，未传则读取环境变量 ZXT_API_KEY")
    sub = parser.add_subparsers(dest="action", required=True)

    p_ocr = sub.add_parser("ocr", help="上传发票文件进行识别")
    p_ocr.add_argument("--file", required=True, help="发票文件路径 (pdf/ofd/jpeg/jpg/png/xml)")

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

    if args.action == "ocr":
        result = ocr(args.api_key, args.file)
        print(fmt_result(result))


if __name__ == "__main__":
    main()
