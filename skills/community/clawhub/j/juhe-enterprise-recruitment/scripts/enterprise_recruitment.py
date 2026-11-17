#!/usr/bin/env python3
"""
企业招聘信息查询脚本 — 由聚合数据 (juhe.cn) 提供数据支持
根据企业全名、注册号或统一社会信用代码查询企业招聘职位信息

用法:
    python enterprise_recruitment.py --name 天聚地合（苏州）数据股份有限公司
    python enterprise_recruitment.py --name 9132059455117770X5 --nametype 3
    python enterprise_recruitment.py --name 天聚地合（苏州）数据股份有限公司 --page 2

API Key 配置（任选其一，优先级从高到低）:
    1. 命令行参数：python enterprise_recruitment.py --key your_api_key --name 企业全名
    2. 环境变量：export JUHE_ENTERPRISE_RECRUITMENT_KEY=your_api_key
    3. 脚本同目录的 .env 文件：JUHE_ENTERPRISE_RECRUITMENT_KEY=your_api_key

申请 API Key: https://www.juhe.cn/docs/api/id/852
"""

import sys
import os
import json
import re
import urllib.request
import urllib.parse
from pathlib import Path

API_URL = "https://apis.juhe.cn/api_credit/query852"
REGISTER_URL = "https://www.juhe.cn/docs/api/id/852"

NAMETYPE_NAME = "1"
NAMETYPE_REGNO = "2"
NAMETYPE_CREDIT = "3"

NAMETYPE_LABELS = {
    NAMETYPE_NAME: "企业名称",
    NAMETYPE_REGNO: "注册号",
    NAMETYPE_CREDIT: "统一社会信用代码",
}

NAMETYPE_ALIASES = {
    "1": NAMETYPE_NAME,
    "name": NAMETYPE_NAME,
    "entname": NAMETYPE_NAME,
    "企业名称": NAMETYPE_NAME,
    "2": NAMETYPE_REGNO,
    "regno": NAMETYPE_REGNO,
    "reg": NAMETYPE_REGNO,
    "注册号": NAMETYPE_REGNO,
    "3": NAMETYPE_CREDIT,
    "credit": NAMETYPE_CREDIT,
    "creditno": NAMETYPE_CREDIT,
    "uscc": NAMETYPE_CREDIT,
    "统一社会信用代码": NAMETYPE_CREDIT,
    "信用代码": NAMETYPE_CREDIT,
}

DESC_MAX_LEN = 160


def load_api_key(cli_key: str = None) -> str:
    """按优先级加载 API Key"""
    if cli_key:
        return cli_key

    env_key = os.environ.get("JUHE_ENTERPRISE_RECRUITMENT_KEY", "").strip()
    if env_key:
        return env_key

    env_file = Path(__file__).parent / ".env"
    if env_file.exists():
        for line in env_file.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line.startswith("JUHE_ENTERPRISE_RECRUITMENT_KEY="):
                val = line.split("=", 1)[1].strip().strip('"').strip("'")
                if val:
                    return val

    return ""


def infer_nametype(name: str) -> str:
    """根据输入内容推断 nametype"""
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
        print("错误：--nametype 仅支持 1(企业名称) / 2(注册号) / 3(统一社会信用代码)")
        sys.exit(1)
    return infer_nametype(name)


def truncate_text(text: str, max_len: int = DESC_MAX_LEN) -> str:
    value = (text or "").strip()
    if not value:
        return "-"
    compact = re.sub(r"\s+", " ", value)
    if len(compact) <= max_len:
        return compact
    return compact[:max_len].rstrip() + "…"


def query_enterprise_recruitment(
    name: str,
    nametype: str,
    page_index: int = 1,
    api_key: str = None,
) -> dict:
    """查询企业招聘信息"""
    if not api_key:
        return {"success": False, "error": "未提供 API Key"}

    params = {
        "key": api_key,
        "name": name,
        "nametype": nametype,
        "pageIndex": str(page_index),
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
        items = payload.get("data") or []
        return {
            "success": True,
            "orderid": payload.get("orderid", ""),
            "total_count": payload.get("totalCount", 0),
            "total_page": payload.get("totalPage", 0),
            "page_size": payload.get("pageSize", 20),
            "page_index": payload.get("pageIndex", page_index),
            "name": name,
            "nametype": nametype,
            "items": items,
        }

    error_code = result.get("error_code", -1)
    reason = result.get("reason", "查询失败")
    hint = ""
    if error_code in (10001, 10002, 10003, 10009):
        hint = f"（请检查 API Key 是否正确，申请地址：{REGISTER_URL}）"
    elif error_code == 10012:
        hint = "（今日调用次数已用尽，请升级套餐）"
    elif error_code == 285201:
        hint = "（请检查 name / nametype 是否正确：1=企业名称，2=注册号，3=统一社会信用代码）"
    elif error_code == 285202:
        hint = "（未找到招聘记录，可核对企业全称、注册号或信用代码后重试）"
    elif error_code in (285203, 285204):
        hint = "（接口异常，请稍后重试）"

    return {"success": False, "error": f"{reason}{hint}", "error_code": error_code}


def format_result(result: dict) -> str:
    """格式化查询结果"""
    if not result["success"]:
        return f"❌ 查询失败：{result.get('error', '未知错误')}"

    items = result.get("items") or []
    total_count = result.get("total_count", 0)
    total_page = result.get("total_page", 0)
    page_index = result.get("page_index", 1)
    nametype = str(result.get("nametype", NAMETYPE_NAME))
    type_label = NAMETYPE_LABELS.get(nametype, nametype)

    lines = []
    lines.append("💼 企业招聘信息查询结果")
    lines.append("")
    lines.append(f"查询条件：{result.get('name', '')}（{type_label}）")
    lines.append(f"共找到 {total_count} 条招聘（第 {page_index}/{total_page or 1} 页，本页 {len(items)} 条）")

    if not items:
        lines.append("")
        lines.append("当前页暂无招聘记录。")
        return "\n".join(lines)

    for idx, item in enumerate(items, 1):
        position = item.get("position") or "-"
        salary = item.get("salary") or "-"
        workplace = item.get("workplace") or "-"
        education = item.get("education") or "-"
        work_years = item.get("workYears") or "-"
        recruit_num = item.get("recruitNum") or "-"
        position_type = item.get("positionType") or "-"
        position_label = item.get("positionLabel") or "-"
        enterprise_name = item.get("enterpriseName") or "-"
        enterprise_type = item.get("enterpriseType") or "-"
        enterprise_size = item.get("enterpriseSize") or "-"
        source = item.get("source") or "-"
        publish_date = item.get("punlishDate") or "-"
        valid_date = item.get("validDate") or "-"
        url = item.get("url") or "-"
        description = truncate_text(item.get("description") or "")

        lines.append("")
        lines.append(f"{idx}. {position}")
        lines.append(f"   薪资：{salary}    地点：{workplace}")
        lines.append(f"   学历：{education}    经验：{work_years}    人数：{recruit_num}")
        lines.append(f"   类型：{position_type}    标签：{position_label}")
        lines.append(f"   企业：{enterprise_name}（{enterprise_type} / {enterprise_size}）")
        lines.append(f"   来源：{source}    发布：{publish_date}    有效期至：{valid_date}")
        lines.append(f"   描述：{description}")
        lines.append(f"   链接：{url}")

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
    name = None
    nametype = None
    page_index = "1"

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
        elif args[i] in ("--help", "-h"):
            print("用法：python enterprise_recruitment.py --name 企业全名 [--nametype 1|2|3] [--page 页码] [--key API_KEY]")
            print("")
            print("选项:")
            print("  --name NAME        企业全名 / 注册号 / 统一社会信用代码（必填）")
            print("  --nametype TYPE    1=企业名称，2=注册号，3=统一社会信用代码（可省略，脚本自动识别）")
            print("  --page PAGE        页码，默认 1，每页 20 条")
            print("  --key KEY          API Key（可选，可用环境变量配置）")
            print("  --help, -h         显示帮助信息")
            print("")
            print("示例:")
            print("  python enterprise_recruitment.py --name 天聚地合（苏州）数据股份有限公司")
            print("  python enterprise_recruitment.py --name 9132059455117770X5 --nametype 3")
            print("  python enterprise_recruitment.py --name 天聚地合（苏州）数据股份有限公司 --page 2")
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
    nametype_value = normalize_nametype(nametype, name)
    page_index_int = parse_positive_int(page_index, "--page", 1)

    api_key = load_api_key(cli_key)
    if not api_key:
        print("❌ 未找到 API Key，请通过以下方式之一配置：")
        print("   1. 环境变量：export JUHE_ENTERPRISE_RECRUITMENT_KEY=your_api_key")
        print("   2. .env 文件：在脚本目录创建 .env，写入 JUHE_ENTERPRISE_RECRUITMENT_KEY=your_api_key")
        print("   3. 命令行参数：python enterprise_recruitment.py --key your_api_key --name 企业全名")
        print(f"\n申请 Key: {REGISTER_URL}")
        sys.exit(1)

    result = query_enterprise_recruitment(
        name,
        nametype_value,
        page_index_int,
        api_key,
    )
    print(format_result(result))
    print("")
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
