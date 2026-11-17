#!/usr/bin/env python3
"""
企业列表查询脚本 — 由聚合数据 (juhe.cn) 提供数据支持
根据企业名称关键字、注册号或统一社会信用代码查询企业列表

用法:
    python enterprise_list.py --keyword 天聚地合
    python enterprise_list.py --keyword 天聚地合（苏州）数据股份有限公司 --page 1 --size 20

API Key 配置（任选其一，优先级从高到低）:
    1. 命令行参数：python enterprise_list.py --key your_api_key --keyword 天聚地合
    2. 环境变量：export JUHE_ENTERPRISE_LIST_KEY=your_api_key
    3. 脚本同目录的 .env 文件：JUHE_ENTERPRISE_LIST_KEY=your_api_key

申请 API Key: https://www.juhe.cn/docs/api/id/192
"""

import sys
import os
import json
import urllib.request
import urllib.parse
from pathlib import Path

API_URL = "https://japi.juhe.cn/enterprise/simpleList"
REGISTER_URL = "https://www.juhe.cn/docs/api/id/192"
MAX_PAGE_SIZE = 20


def load_api_key(cli_key: str = None) -> str:
    """按优先级加载 API Key"""
    if cli_key:
        return cli_key

    env_key = os.environ.get("JUHE_ENTERPRISE_LIST_KEY", "").strip()
    if env_key:
        return env_key

    env_file = Path(__file__).parent / ".env"
    if env_file.exists():
        for line in env_file.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line.startswith("JUHE_ENTERPRISE_LIST_KEY="):
                val = line.split("=", 1)[1].strip().strip('"').strip("'")
                if val:
                    return val

    return ""


def query_enterprise_list(
    keyword: str,
    page_num: int = 1,
    page_size: int = 20,
    api_key: str = None,
) -> dict:
    """根据关键字查询企业列表"""
    if not api_key:
        return {"success": False, "error": "未提供 API Key"}

    params = {
        "key": api_key,
        "keyword": keyword,
        "pageNum": str(page_num),
        "pageSize": str(page_size),
    }

    data = urllib.parse.urlencode(params).encode("utf-8")

    try:
        req = urllib.request.Request(API_URL, data=data, method="POST")
        req.add_header("Content-Type", "application/x-www-form-urlencoded")
        with urllib.request.urlopen(req, timeout=10) as resp:
            result = json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        return {"success": False, "error": f"网络请求失败：{e}"}

    if result.get("error_code") == 0:
        payload = result.get("result") or {}
        data_obj = payload.get("data") or {}
        items = data_obj.get("items") or []
        return {
            "success": True,
            "total": data_obj.get("total", 0),
            "num": data_obj.get("num", len(items)),
            "page_num": page_num,
            "page_size": page_size,
            "keyword": keyword,
            "items": items,
            "sign": payload.get("sign", ""),
        }

    error_code = result.get("error_code", -1)
    reason = result.get("reason", "查询失败")
    hint = ""
    if error_code in (10001, 10002, 10003, 10009):
        hint = f"（请检查 API Key 是否正确，申请地址：{REGISTER_URL}）"
    elif error_code == 10012:
        hint = "（今日调用次数已用尽，请升级套餐）"
    elif error_code == 219201:
        hint = "（未找到匹配企业，可尝试更完整的名称、注册号或统一社会信用代码）"
    elif error_code == 219208:
        hint = "（请检查 keyword 是否为空，pageSize 是否超过 20）"

    return {"success": False, "error": f"{reason}{hint}", "error_code": error_code}


def format_result(result: dict) -> str:
    """格式化查询结果"""
    if not result["success"]:
        return f"❌ 查询失败：{result.get('error', '未知错误')}"

    items = result.get("items") or []
    total = result.get("total", 0)
    num = result.get("num", len(items))
    page_num = result.get("page_num", 1)

    lines = []
    lines.append("🏢 企业列表查询结果")
    lines.append("")
    lines.append(f"关键词：{result.get('keyword', '')}")
    lines.append(f"共找到 {total} 家企业（第 {page_num} 页，本页 {num} 条）")

    if not items:
        lines.append("")
        lines.append("当前页暂无企业记录。")
        return "\n".join(lines)

    for idx, item in enumerate(items, 1):
        name = item.get("name") or "-"
        oper_name = item.get("oper_name") or "-"
        start_date = item.get("start_date") or "-"
        reg_no = item.get("reg_no") or "-"
        credit_no = item.get("credit_no") or "-"
        ent_id = item.get("id") or "-"

        lines.append("")
        lines.append(f"{idx}. {name}")
        lines.append(f"   法人：{oper_name}")
        lines.append(f"   成立日期：{start_date}")
        lines.append(f"   注册号：{reg_no}")
        lines.append(f"   统一社会信用代码：{credit_no}")
        lines.append(f"   企业编号：{ent_id}")

    return "\n".join(lines)


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


def main():
    args = sys.argv[1:]
    cli_key = None
    keyword = None
    page_num = "1"
    page_size = "20"

    i = 0
    while i < len(args):
        if args[i] == "--key" and i + 1 < len(args):
            cli_key = args[i + 1]
            i += 2
        elif args[i] == "--keyword" and i + 1 < len(args):
            keyword = args[i + 1]
            i += 2
        elif args[i] in ("--page", "--pageNum") and i + 1 < len(args):
            page_num = args[i + 1]
            i += 2
        elif args[i] in ("--size", "--pageSize") and i + 1 < len(args):
            page_size = args[i + 1]
            i += 2
        elif args[i] in ("--help", "-h"):
            print("用法：python enterprise_list.py --keyword 企业名称 [--page 页码] [--size 条数] [--key API_KEY]")
            print("")
            print("选项:")
            print("  --keyword KEYWORD  企业名称关键字 / 注册号 / 统一社会信用代码（必填）")
            print("  --page PAGE        页码，默认 1")
            print("  --size SIZE        每页条数，最大 20，默认 20")
            print("  --key KEY          API Key（可选，可用环境变量配置）")
            print("  --help, -h         显示帮助信息")
            print("")
            print("示例:")
            print("  python enterprise_list.py --keyword 天聚地合")
            print("  python enterprise_list.py --keyword 天聚地合（苏州）数据股份有限公司 --page 1 --size 10")
            print("  python enterprise_list.py --keyword 9132059455117770X5")
            print("")
            print(f"申请 API Key: {REGISTER_URL}")
            sys.exit(0)
        else:
            i += 1

    if not keyword or not str(keyword).strip():
        print("错误：缺少必填参数 --keyword")
        print("使用 --help 查看用法")
        sys.exit(1)

    page_num_int = parse_positive_int(page_num, "--page", 1)
    page_size_int = parse_positive_int(page_size, "--size", 20)
    if page_size_int > MAX_PAGE_SIZE:
        print(f"错误：--size 最大为 {MAX_PAGE_SIZE}")
        sys.exit(1)

    api_key = load_api_key(cli_key)
    if not api_key:
        print("❌ 未找到 API Key，请通过以下方式之一配置：")
        print("   1. 环境变量：export JUHE_ENTERPRISE_LIST_KEY=your_api_key")
        print("   2. .env 文件：在脚本目录创建 .env，写入 JUHE_ENTERPRISE_LIST_KEY=your_api_key")
        print("   3. 命令行参数：python enterprise_list.py --key your_api_key --keyword 天聚地合")
        print(f"\n申请 Key: {REGISTER_URL}")
        sys.exit(1)

    result = query_enterprise_list(
        keyword.strip(),
        page_num_int,
        page_size_int,
        api_key,
    )
    print(format_result(result))
    print("")
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
