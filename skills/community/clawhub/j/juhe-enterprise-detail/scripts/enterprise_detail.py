#!/usr/bin/env python3
"""
企业信息精确查询脚本 — 由聚合数据 (juhe.cn) 提供数据支持
根据企业全名、注册号或统一社会信用代码精确查询详细工商信息

用法:
    python enterprise_detail.py --keyword 天聚地合（苏州）数据股份有限公司
    python enterprise_detail.py --keyword 9132059455117770X5

API Key 配置（任选其一，优先级从高到低）:
    1. 命令行参数：python enterprise_detail.py --key your_api_key --keyword 企业全名
    2. 环境变量：export JUHE_ENTERPRISE_DETAIL_KEY=your_api_key
    3. 脚本同目录的 .env 文件：JUHE_ENTERPRISE_DETAIL_KEY=your_api_key

申请 API Key: https://www.juhe.cn/docs/api/id/319
"""

import sys
import os
import json
import urllib.request
import urllib.parse
from pathlib import Path

API_URL = "https://japi.juhe.cn/enterprise/getDetailByName"
REGISTER_URL = "https://www.juhe.cn/docs/api/id/319"


def load_api_key(cli_key: str = None) -> str:
    if cli_key:
        return cli_key

    env_key = os.environ.get("JUHE_ENTERPRISE_DETAIL_KEY", "").strip()
    if env_key:
        return env_key

    env_file = Path(__file__).parent / ".env"
    if env_file.exists():
        for line in env_file.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line.startswith("JUHE_ENTERPRISE_DETAIL_KEY="):
                val = line.split("=", 1)[1].strip().strip('"').strip("'")
                if val:
                    return val
    return ""


def display_value(value) -> str:
    text = str(value or "").strip()
    return text if text and text != "-" else "-"


def query_enterprise_detail(keyword: str, api_key: str) -> dict:
    if not api_key:
        return {"success": False, "error": "未提供 API Key"}

    params = {"key": api_key, "keyword": keyword}
    data = urllib.parse.urlencode(params).encode("utf-8")
    try:
        req = urllib.request.Request(API_URL, data=data, method="POST")
        req.add_header("Content-Type", "application/x-www-form-urlencoded")
        with urllib.request.urlopen(req, timeout=15) as resp:
            result = json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        return {"success": False, "error": f"网络请求失败：{e}"}

    if result.get("error_code") == 0:
        payload = result.get("result") or {}
        data_obj = payload.get("data") or {}
        return {
            "success": True,
            "sign": payload.get("sign", ""),
            "keyword": keyword,
            "data": data_obj,
        }

    error_code = result.get("error_code", -1)
    reason = result.get("reason", "查询失败")
    hint = ""
    if error_code in (10001, 10002, 10003, 10009):
        hint = f"（请检查 API Key 是否正确，申请地址：{REGISTER_URL}）"
    elif error_code == 10012:
        hint = "（今日调用次数已用尽，请升级套餐）"
    elif error_code == 231901:
        hint = "（未找到匹配企业，请使用企业全称、注册号或统一社会信用代码）"
    elif error_code == 231908:
        hint = "（请检查 keyword 是否为空）"
    elif error_code in (231907, 231909):
        hint = "（接口异常，请稍后重试）"
    return {"success": False, "error": f"{reason}{hint}", "error_code": error_code}


def format_capi_items(items, amount_key: str, date_key: str) -> str:
    if not items:
        return "-"
    parts = []
    for item in items:
        amount = display_value(item.get(amount_key))
        invest_type = display_value(item.get("invest_type"))
        date = display_value(item.get(date_key))
        parts.append(f"{amount} / {invest_type} / {date}")
    return "；".join(parts)


def format_result(result: dict) -> str:
    if not result["success"]:
        return f"❌ 查询失败：{result.get('error', '未知错误')}"

    data = result.get("data") or {}
    lines = [
        "📋 企业信息精确查询结果",
        "",
        f"企业名称：{display_value(data.get('name'))}",
        f"经营状态：{display_value(data.get('status'))}",
        f"企业类型：{display_value(data.get('econ_kind'))}",
        f"法定代表人：{display_value(data.get('oper_name'))}",
        f"成立日期：{display_value(data.get('start_date'))}",
        f"注册资本：{display_value(data.get('regist_capi_new') or data.get('regist_capi'))} {display_value(data.get('currency_unit')).replace('-', '').strip()}".rstrip(),
        f"统一社会信用代码：{display_value(data.get('credit_no'))}",
        f"注册号：{display_value(data.get('reg_no'))}",
        f"组织机构号：{display_value(data.get('org_no'))}",
        f"登记机关：{display_value(data.get('belong_org'))}",
        f"省份：{display_value(data.get('province'))}",
        f"地址：{display_value(data.get('address') or data.get('addresses'))}",
        f"营业期限：{display_value(data.get('term_start'))} 至 {display_value(data.get('term_end'))}",
        f"核准日期：{display_value(data.get('check_date'))}",
        f"注销日期：{display_value(data.get('end_date'))}",
        f"经营范围：{display_value(data.get('scope'))}",
    ]

    employees = data.get("employees") or []
    lines.append("")
    lines.append(f"主要人员（{len(employees)}）")
    if employees:
        for idx, item in enumerate(employees, 1):
            lines.append(f"   {idx}. {display_value(item.get('name'))}  {display_value(item.get('job_title'))}")
    else:
        lines.append("   无")

    partners = data.get("partners") or []
    lines.append("")
    lines.append(f"股东信息（{len(partners)}）")
    if partners:
        for idx, item in enumerate(partners, 1):
            should = format_capi_items(item.get("should_capi_items") or [], "shoud_capi", "should_capi_date")
            real = format_capi_items(item.get("real_capi_items") or [], "real_capi", "real_capi_date")
            lines.append(f"   {idx}. {display_value(item.get('name'))}（{display_value(item.get('stock_type'))}）")
            lines.append(f"      认缴：{should}")
            lines.append(f"      实缴：{real}")
    else:
        lines.append("   无")

    branches = data.get("branches") or data.get("brances") or []
    lines.append("")
    lines.append(f"分支机构（{len(branches)}）")
    if branches:
        for idx, item in enumerate(branches, 1):
            lines.append(f"   {idx}. {display_value(item.get('name'))}")
    else:
        lines.append("   无")

    changes = data.get("changerecords") or []
    lines.append("")
    lines.append(f"变更记录（{len(changes)}）")
    if changes:
        for idx, item in enumerate(changes, 1):
            lines.append(f"   {idx}. {display_value(item.get('change_date'))}  {display_value(item.get('change_item'))}")
            lines.append(f"      变更前：{display_value(item.get('before_content'))}")
            lines.append(f"      变更后：{display_value(item.get('after_content'))}")
    else:
        lines.append("   无")

    abnormals = data.get("abnormal_items") or []
    lines.append("")
    lines.append(f"经营异常（{len(abnormals)}）")
    if abnormals:
        for idx, item in enumerate(abnormals, 1):
            lines.append(f"   {idx}. 列入：{display_value(item.get('in_date'))}  {display_value(item.get('in_reason'))}")
            lines.append(f"      移出：{display_value(item.get('out_date'))}  {display_value(item.get('out_reason'))}")
    else:
        lines.append("   无")

    return "\n".join(lines)


def main():
    args = sys.argv[1:]
    cli_key = None
    keyword = None

    i = 0
    while i < len(args):
        if args[i] == "--key" and i + 1 < len(args):
            cli_key = args[i + 1]
            i += 2
        elif args[i] in ("--keyword", "--name") and i + 1 < len(args):
            keyword = args[i + 1]
            i += 2
        elif args[i] in ("--help", "-h"):
            print("用法：python enterprise_detail.py --keyword 企业全名 [--key API_KEY]")
            print("")
            print("选项:")
            print("  --keyword KEYWORD  企业全名 / 注册号 / 统一社会信用代码（必填）")
            print("  --key KEY          API Key（可选，可用环境变量配置）")
            print("  --help, -h         显示帮助信息")
            print("")
            print("示例:")
            print("  python enterprise_detail.py --keyword 天聚地合（苏州）数据股份有限公司")
            print("  python enterprise_detail.py --keyword 9132059455117770X5")
            print("")
            print(f"申请 API Key: {REGISTER_URL}")
            sys.exit(0)
        else:
            i += 1

    if not keyword or not str(keyword).strip():
        print("错误：缺少必填参数 --keyword")
        print("使用 --help 查看用法")
        sys.exit(1)

    api_key = load_api_key(cli_key)
    if not api_key:
        print("❌ 未找到 API Key，请通过以下方式之一配置：")
        print("   1. 环境变量：export JUHE_ENTERPRISE_DETAIL_KEY=your_api_key")
        print("   2. .env 文件：在脚本目录创建 .env，写入 JUHE_ENTERPRISE_DETAIL_KEY=your_api_key")
        print("   3. 命令行参数：python enterprise_detail.py --key your_api_key --keyword 企业全名")
        print(f"\n申请 Key: {REGISTER_URL}")
        sys.exit(1)

    result = query_enterprise_detail(keyword.strip(), api_key)
    print(format_result(result))
    print("")
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
