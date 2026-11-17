#!/usr/bin/env python3
"""
企业被执行人信息（公示中及历史）查询脚本 — 由聚合数据 (juhe.cn) 提供数据支持
根据企业名称、统一社会信用代码、工商注册号或关键词查询被执行人记录

用法:
    python enterprise_executed.py --name 河北展发房地产开发有限公司
    python enterprise_executed.py --name 911309005661956791 --nametype 2
    python enterprise_executed.py --name 河北展发房地产开发有限公司 --need-his-data false

API Key 配置（任选其一，优先级从高到低）:
    1. 命令行参数：python enterprise_executed.py --key your_api_key --name 企业名称
    2. 环境变量：export JUHE_ENTERPRISE_EXECUTED_KEY=your_api_key
    3. 脚本同目录的 .env 文件：JUHE_ENTERPRISE_EXECUTED_KEY=your_api_key

申请 API Key: https://www.juhe.cn/docs/api/id/842
"""

import sys
import os
import json
import re
import urllib.request
import urllib.parse
from pathlib import Path

API_URL = "https://apis.juhe.cn/api_credit/query842"
REGISTER_URL = "https://www.juhe.cn/docs/api/id/842"
MAX_PAGE_SIZE = 200

NAMETYPE_NAME = "1"
NAMETYPE_CREDIT = "2"
NAMETYPE_REGNO = "3"
NAMETYPE_KEYWORD = "4"

NAMETYPE_LABELS = {
    NAMETYPE_NAME: "企业名称",
    NAMETYPE_CREDIT: "统一社会信用代码",
    NAMETYPE_REGNO: "工商注册号",
    NAMETYPE_KEYWORD: "关键词",
}

NAMETYPE_ALIASES = {
    "1": NAMETYPE_NAME,
    "name": NAMETYPE_NAME,
    "entname": NAMETYPE_NAME,
    "企业名称": NAMETYPE_NAME,
    "2": NAMETYPE_CREDIT,
    "credit": NAMETYPE_CREDIT,
    "creditno": NAMETYPE_CREDIT,
    "uscc": NAMETYPE_CREDIT,
    "统一社会信用代码": NAMETYPE_CREDIT,
    "信用代码": NAMETYPE_CREDIT,
    "3": NAMETYPE_REGNO,
    "regno": NAMETYPE_REGNO,
    "reg": NAMETYPE_REGNO,
    "注册号": NAMETYPE_REGNO,
    "工商注册号": NAMETYPE_REGNO,
    "4": NAMETYPE_KEYWORD,
    "keyword": NAMETYPE_KEYWORD,
    "关键词": NAMETYPE_KEYWORD,
}

IDCARD_PATTERN = re.compile(r"^[1-9]\d{5}(18|19|20)\d{2}(0[1-9]|1[0-2])(0[1-9]|[12]\d|3[01])\d{3}[\dXx]$")


def load_api_key(cli_key: str = None) -> str:
    if cli_key:
        return cli_key

    env_key = os.environ.get("JUHE_ENTERPRISE_EXECUTED_KEY", "").strip()
    if env_key:
        return env_key

    env_file = Path(__file__).parent / ".env"
    if env_file.exists():
        for line in env_file.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line.startswith("JUHE_ENTERPRISE_EXECUTED_KEY="):
                val = line.split("=", 1)[1].strip().strip('"').strip("'")
                if val:
                    return val
    return ""


def infer_nametype(name: str) -> str:
    value = (name or "").strip().upper()
    if re.match(r"^[0-9A-HJ-NPQRTUWXY]{18}$", value):
        return NAMETYPE_CREDIT
    if re.match(r"^\d{13,15}$", value):
        return NAMETYPE_REGNO
    return NAMETYPE_NAME


def normalize_nametype(raw: str, name: str) -> str:
    if raw:
        key = str(raw).strip().lower()
        if key in NAMETYPE_ALIASES:
            return NAMETYPE_ALIASES[key]
        print("错误：--nametype 仅支持 1(企业名称) / 2(统一社会信用代码) / 3(工商注册号) / 4(关键词)")
        sys.exit(1)
    return infer_nametype(name)


def parse_bool(raw: str, default: bool, flag: str) -> str:
    if raw is None or str(raw).strip() == "":
        return "true" if default else "false"
    key = str(raw).strip().lower()
    if key in ("true", "1", "yes", "y"):
        return "true"
    if key in ("false", "0", "no", "n"):
        return "false"
    print(f"错误：{flag} 仅支持 true / false")
    sys.exit(1)


def parse_positive_int(value: str, name: str, default: int) -> int:
    if value is None:
        return default
    try:
        parsed = int(value)
    except ValueError:
        print(f"错误：{name} 必须是整数")
        sys.exit(1)
    if parsed < 1:
        print(f"错误：{name} 必须大于等于 1")
        sys.exit(1)
    return parsed


def display_value(value) -> str:
    text = str(value or "").strip()
    return text if text else "-"


def mask_party_card(value: str) -> str:
    text = str(value or "").strip()
    if IDCARD_PATTERN.match(text):
        return text[:6] + "********" + text[-4:]
    return text or "-"


def format_money(value: str) -> str:
    text = str(value or "").strip()
    if not text:
        return "-"
    try:
        number = float(text.replace(",", ""))
        if number.is_integer():
            return f"{int(number):,}"
        return f"{number:,.2f}"
    except ValueError:
        return text


def is_current_status(status: str) -> bool:
    text = str(status or "")
    return "公示" in text and "不披露" not in text


def query_enterprise_executed(params: dict, api_key: str) -> dict:
    if not api_key:
        return {"success": False, "error": "未提供 API Key"}

    payload = {"key": api_key}
    for key, value in params.items():
        if value is None or str(value).strip() == "":
            continue
        payload[key] = str(value)

    data = urllib.parse.urlencode(payload).encode("utf-8")
    try:
        req = urllib.request.Request(API_URL, data=data, method="POST")
        req.add_header("Content-Type", "application/x-www-form-urlencoded")
        with urllib.request.urlopen(req, timeout=15) as resp:
            result = json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        return {"success": False, "error": f"网络请求失败：{e}"}

    if result.get("error_code") == 0:
        body = result.get("result") or {}
        items = body.get("data") or []
        for item in items:
            if isinstance(item, dict) and "partyCardNum" in item:
                item["partyCardNum"] = mask_party_card(item.get("partyCardNum"))
        current_count = sum(1 for item in items if is_current_status(item.get("caseStatus")))
        history_count = sum(1 for item in items if "不披露" in str(item.get("caseStatus") or ""))
        return {
            "success": True,
            "orderid": body.get("orderid", ""),
            "total_count": body.get("totalCount", 0),
            "total_page": body.get("totalPage", 0),
            "page_size": body.get("pageSize", 20),
            "page_index": body.get("pageIndex", 1),
            "query": {k: v for k, v in params.items() if v not in (None, "")},
            "current_count": current_count,
            "history_count": history_count,
            "items": items,
        }

    error_code = result.get("error_code", -1)
    reason = result.get("reason", "查询失败")
    hint = ""
    if error_code in (10001, 10002, 10003, 10009):
        hint = f"（请检查 API Key 是否正确，申请地址：{REGISTER_URL}）"
    elif error_code == 10012:
        hint = "（今日调用次数已用尽，请升级套餐）"
    elif error_code == 284201:
        hint = "（请检查 name / nametype：1=企业名称，2=统一社会信用代码，3=工商注册号，4=关键词）"
    elif error_code == 284202:
        hint = "（未找到被执行人记录，可核对企业全称、信用代码或注册号后重试）"
    elif error_code in (284203, 284204):
        hint = "（接口异常，请稍后重试）"
    return {"success": False, "error": f"{reason}{hint}", "error_code": error_code}


def format_result(result: dict) -> str:
    if not result["success"]:
        return f"❌ 查询失败：{result.get('error', '未知错误')}"

    items = result.get("items") or []
    query = result.get("query") or {}
    name = query.get("name") or "-"
    nametype = str(query.get("nametype") or "")
    type_label = NAMETYPE_LABELS.get(nametype, nametype or "未指定")
    his_data = "含已不披露" if str(query.get("isNeedHisData", "true")).lower() != "false" else "仅当前披露"

    lines = [
        "⚖️ 企业被执行人信息查询结果",
        "",
        f"查询条件：{name}（{type_label}，{his_data}）",
        f"共找到 {result.get('total_count', 0)} 条记录（第 {result.get('page_index', 1)}/{result.get('total_page') or 1} 页，本页 {len(items)} 条）",
        f"本页状态：公示中 {result.get('current_count', 0)} 条，已不披露 {result.get('history_count', 0)} 条",
    ]
    if not items:
        lines.extend(["", "当前页暂无被执行人记录。"])
        return "\n".join(lines)

    for idx, item in enumerate(items, 1):
        lines.extend([
            "",
            f"{idx}. [{display_value(item.get('caseStatus'))}] {display_value(item.get('pName'))}",
            f"   案号：{display_value(item.get('caseCode'))}",
            f"   执行法院：{display_value(item.get('execCourtName'))}",
            f"   执行标的：{format_money(item.get('execMoney'))}    立案：{display_value(item.get('caseCreateTime'))}",
            f"   主体标识：{mask_party_card(item.get('partyCardNum'))}",
            f"   采集：{display_value(item.get('inputTime'))}    更新：{display_value(item.get('updateTime'))}",
        ])
    return "\n".join(lines)


def main():
    args = sys.argv[1:]
    cli_key = None
    name = None
    nametype = None
    page_index = "1"
    page_size = "20"
    need_his_data = None
    his_name = None
    case_no = None
    case_no_fuzzy = None
    start = None
    end = None
    province = None
    city = None
    serial_no = None

    i = 0
    while i < len(args):
        if args[i] == "--key" and i + 1 < len(args):
            cli_key = args[i + 1]
            i += 2
        elif args[i] == "--name" and i + 1 < len(args):
            name = args[i + 1]
            i += 2
        elif args[i] in ("--nametype", "--type") and i + 1 < len(args):
            nametype = args[i + 1]
            i += 2
        elif args[i] in ("--page", "--pageIndex") and i + 1 < len(args):
            page_index = args[i + 1]
            i += 2
        elif args[i] in ("--size", "--pageSize") and i + 1 < len(args):
            page_size = args[i + 1]
            i += 2
        elif args[i] in ("--need-his-data", "--isNeedHisData") and i + 1 < len(args):
            need_his_data = args[i + 1]
            i += 2
        elif args[i] in ("--his-name", "--isRelationHisName") and i + 1 < len(args):
            his_name = args[i + 1]
            i += 2
        elif args[i] in ("--case-no", "--caseNo") and i + 1 < len(args):
            case_no = args[i + 1]
            i += 2
        elif args[i] in ("--case-no-fuzzy", "--isCaseNoFuzzy") and i + 1 < len(args):
            case_no_fuzzy = args[i + 1]
            i += 2
        elif args[i] in ("--start", "--caseCreateTimeStart") and i + 1 < len(args):
            start = args[i + 1]
            i += 2
        elif args[i] in ("--end", "--caseCreateTimeEnd") and i + 1 < len(args):
            end = args[i + 1]
            i += 2
        elif args[i] in ("--province", "--prov") and i + 1 < len(args):
            province = args[i + 1]
            i += 2
        elif args[i] == "--city" and i + 1 < len(args):
            city = args[i + 1]
            i += 2
        elif args[i] in ("--serial-no", "--serialNo") and i + 1 < len(args):
            serial_no = args[i + 1]
            i += 2
        elif args[i] in ("--help", "-h"):
            print("用法：python enterprise_executed.py --name 企业名称 [--nametype 1|2|3|4] [--page 页码] [--size 条数] [--key API_KEY]")
            print("")
            print("选项:")
            print("  --name NAME            企业名称 / 统一社会信用代码 / 工商注册号 / 关键词（必填）")
            print("  --nametype TYPE        1=企业名称，2=统一社会信用代码，3=工商注册号，4=关键词（可省略，脚本自动识别）")
            print("  --page PAGE            页码，默认 1")
            print("  --size SIZE            每页条数，默认 20，最大 200")
            print("  --need-his-data BOOL   是否包含已不披露数据，默认 true")
            print("  --his-name BOOL        是否关联曾用名，默认 false")
            print("  --case-no CASE         案号")
            print("  --case-no-fuzzy BOOL   案号是否模糊检索，默认 false")
            print("  --start DATE           立案时间起，yyyy-MM-dd")
            print("  --end DATE             立案时间止，yyyy-MM-dd")
            print("  --province NAME        省份")
            print("  --city NAME            城市")
            print("  --key KEY              API Key（可选，可用环境变量配置）")
            print("  --help, -h             显示帮助信息")
            print("")
            print("示例:")
            print("  python enterprise_executed.py --name 河北展发房地产开发有限公司")
            print("  python enterprise_executed.py --name 911309005661956791 --nametype 2")
            print("  python enterprise_executed.py --name 河北展发房地产开发有限公司 --need-his-data false")
            print("")
            print(f"申请 API Key: {REGISTER_URL}")
            sys.exit(0)
        else:
            i += 1

    if not name or not str(name).strip():
        print("错误：缺少必填参数 --name")
        print("使用 --help 查看用法")
        sys.exit(1)

    name = name.strip()
    page_size_int = parse_positive_int(page_size, "--size", 20)
    if page_size_int > MAX_PAGE_SIZE:
        print(f"错误：--size 最大为 {MAX_PAGE_SIZE}")
        sys.exit(1)

    api_key = load_api_key(cli_key)
    if not api_key:
        print("❌ 未找到 API Key，请通过以下方式之一配置：")
        print("   1. 环境变量：export JUHE_ENTERPRISE_EXECUTED_KEY=your_api_key")
        print("   2. .env 文件：在脚本目录创建 .env，写入 JUHE_ENTERPRISE_EXECUTED_KEY=your_api_key")
        print("   3. 命令行参数：python enterprise_executed.py --key your_api_key --name 企业名称")
        print(f"\n申请 Key: {REGISTER_URL}")
        sys.exit(1)

    params = {
        "name": name,
        "nametype": normalize_nametype(nametype, name),
        "pageIndex": parse_positive_int(page_index, "--page", 1),
        "pageSize": page_size_int,
        "isNeedHisData": parse_bool(need_his_data, True, "--need-his-data"),
        "isRelationHisName": parse_bool(his_name, False, "--his-name"),
        "caseNo": case_no.strip() if case_no else None,
        "isCaseNoFuzzy": parse_bool(case_no_fuzzy, False, "--case-no-fuzzy") if case_no_fuzzy is not None else None,
        "caseCreateTimeStart": start,
        "caseCreateTimeEnd": end,
        "province": province,
        "city": city,
        "serialNo": serial_no,
    }
    result = query_enterprise_executed(params, api_key)
    print(format_result(result))
    print("")
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
