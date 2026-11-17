#!/usr/bin/env python3
"""
企业工商-异常经营信息查询脚本 — 由聚合数据 (juhe.cn) 提供数据支持
根据企业全名、注册号或统一社会信用代码查询经营异常名录记录

用法:
    python enterprise_abnormal.py --name 苏州瀚海知识产权代理有限公司
    python enterprise_abnormal.py --name 9132059455117770X5 --nametype 3
    python enterprise_abnormal.py --name 苏州瀚海知识产权代理有限公司 --pub-status 1

API Key 配置（任选其一，优先级从高到低）:
    1. 命令行参数：python enterprise_abnormal.py --key your_api_key --name 企业全名
    2. 环境变量：export JUHE_ENTERPRISE_ABNORMAL_KEY=your_api_key
    3. 脚本同目录的 .env 文件：JUHE_ENTERPRISE_ABNORMAL_KEY=your_api_key

申请 API Key: https://www.juhe.cn/docs/api/id/841
"""

import sys
import os
import json
import re
import urllib.request
import urllib.parse
from pathlib import Path

API_URL = "https://apis.juhe.cn/api_credit/query841"
REGISTER_URL = "https://www.juhe.cn/docs/api/id/841"

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

PUB_STATUS_ALL = "0"
PUB_STATUS_CURRENT = "1"

PUB_STATUS_LABELS = {
    PUB_STATUS_ALL: "全部",
    PUB_STATUS_CURRENT: "仅当前公示",
}

PUB_STATUS_ALIASES = {
    "0": PUB_STATUS_ALL,
    "all": PUB_STATUS_ALL,
    "全部": PUB_STATUS_ALL,
    "1": PUB_STATUS_CURRENT,
    "current": PUB_STATUS_CURRENT,
    "公示": PUB_STATUS_CURRENT,
    "当前": PUB_STATUS_CURRENT,
    "公示中": PUB_STATUS_CURRENT,
}

DISABLED_CURRENT = "0"
DISABLED_HISTORY = "1"


def load_api_key(cli_key: str = None) -> str:
    """按优先级加载 API Key"""
    if cli_key:
        return cli_key

    env_key = os.environ.get("JUHE_ENTERPRISE_ABNORMAL_KEY", "").strip()
    if env_key:
        return env_key

    env_file = Path(__file__).parent / ".env"
    if env_file.exists():
        for line in env_file.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line.startswith("JUHE_ENTERPRISE_ABNORMAL_KEY="):
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


def normalize_pub_status(raw: str) -> str:
    if raw is None or str(raw).strip() == "":
        return PUB_STATUS_ALL
    key = str(raw).strip().lower()
    if key in PUB_STATUS_ALIASES:
        return PUB_STATUS_ALIASES[key]
    print("错误：--pub-status 仅支持 0(全部) / 1(仅当前公示)")
    sys.exit(1)


def display_status(disabled: str) -> str:
    value = str(disabled).strip()
    if value == DISABLED_CURRENT:
        return "当前公示"
    if value == DISABLED_HISTORY:
        return "历史公示"
    return value or "-"


def query_enterprise_abnormal(
    name: str,
    nametype: str,
    page_index: int = 1,
    pub_status: str = PUB_STATUS_ALL,
    api_key: str = None,
) -> dict:
    """查询企业经营异常信息"""
    if not api_key:
        return {"success": False, "error": "未提供 API Key"}

    params = {
        "key": api_key,
        "name": name,
        "nametype": nametype,
        "pageIndex": str(page_index),
        "pubStatus": str(pub_status),
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
        current_count = sum(1 for item in items if str(item.get("disabled", "")).strip() == DISABLED_CURRENT)
        history_count = sum(1 for item in items if str(item.get("disabled", "")).strip() == DISABLED_HISTORY)
        return {
            "success": True,
            "orderid": payload.get("orderid", ""),
            "total_count": payload.get("totalCount", 0),
            "total_page": payload.get("totalPage", 0),
            "page_size": payload.get("pageSize", 20),
            "page_index": payload.get("pageIndex", page_index),
            "name": name,
            "nametype": nametype,
            "pub_status": pub_status,
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
    elif error_code == 284101:
        hint = "（请检查 name / nametype：企业全名至少 4 个字；1=企业名称，2=注册号，3=统一社会信用代码）"
    elif error_code == 284102:
        hint = "（未找到经营异常记录，可核对企业全称、注册号或信用代码后重试）"
    elif error_code in (284103, 284104):
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
    pub_status = str(result.get("pub_status", PUB_STATUS_ALL))
    pub_label = PUB_STATUS_LABELS.get(pub_status, pub_status)
    current_count = result.get("current_count", 0)
    history_count = result.get("history_count", 0)

    lines = []
    lines.append("⚠️ 企业工商-异常经营信息查询结果")
    lines.append("")
    lines.append(f"查询条件：{result.get('name', '')}（{type_label}，{pub_label}）")
    lines.append(f"共找到 {total_count} 条记录（第 {page_index}/{total_page or 1} 页，本页 {len(items)} 条）")
    lines.append(f"本页状态：当前公示 {current_count} 条，历史公示 {history_count} 条")

    if not items:
        lines.append("")
        lines.append("当前页暂无经营异常记录。")
        return "\n".join(lines)

    for idx, item in enumerate(items, 1):
        ent_name = item.get("name") or "-"
        reg_no = item.get("reg_no") or "-"
        province = item.get("province") or "-"
        in_reason = item.get("in_reason") or "-"
        in_date = item.get("in_date") or "-"
        out_reason = item.get("out_reason") or "-"
        out_date = item.get("out_date") or "-"
        department = item.get("department") or "-"
        status = display_status(item.get("disabled"))

        lines.append("")
        lines.append(f"{idx}. [{status}] {ent_name}")
        lines.append(f"   注册号：{reg_no}    省份：{province}")
        lines.append(f"   列入时间：{in_date}")
        lines.append(f"   列入原因：{in_reason}")
        lines.append(f"   移出时间：{out_date}")
        lines.append(f"   移出原因：{out_reason}")
        lines.append(f"   决定机关：{department}")

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
    pub_status = None

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
        elif args[i] in ("--pub-status", "--pubStatus") and i + 1 < len(args):
            pub_status = args[i + 1]
            i += 2
        elif args[i] in ("--help", "-h"):
            print("用法：python enterprise_abnormal.py --name 企业全名 [--nametype 1|2|3] [--page 页码] [--pub-status 0|1] [--key API_KEY]")
            print("")
            print("选项:")
            print("  --name NAME            企业全名 / 注册号 / 统一社会信用代码（必填，企业全名至少 4 个字）")
            print("  --nametype TYPE        1=企业名称，2=注册号，3=统一社会信用代码（可省略，脚本自动识别）")
            print("  --page PAGE            页码，默认 1，每页 20 条")
            print("  --pub-status STATUS    0=全部（默认），1=仅当前公示")
            print("  --key KEY              API Key（可选，可用环境变量配置）")
            print("  --help, -h             显示帮助信息")
            print("")
            print("示例:")
            print("  python enterprise_abnormal.py --name 苏州瀚海知识产权代理有限公司")
            print("  python enterprise_abnormal.py --name 9132059455117770X5 --nametype 3")
            print("  python enterprise_abnormal.py --name 苏州瀚海知识产权代理有限公司 --pub-status 1")
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
    if nametype_value == NAMETYPE_NAME and len(name) < 4:
        print("错误：按企业名称查询时，--name 至少 4 个字")
        sys.exit(1)

    page_index_int = parse_positive_int(page_index, "--page", 1)
    pub_status_value = normalize_pub_status(pub_status)

    api_key = load_api_key(cli_key)
    if not api_key:
        print("❌ 未找到 API Key，请通过以下方式之一配置：")
        print("   1. 环境变量：export JUHE_ENTERPRISE_ABNORMAL_KEY=your_api_key")
        print("   2. .env 文件：在脚本目录创建 .env，写入 JUHE_ENTERPRISE_ABNORMAL_KEY=your_api_key")
        print("   3. 命令行参数：python enterprise_abnormal.py --key your_api_key --name 企业全名")
        print(f"\n申请 Key: {REGISTER_URL}")
        sys.exit(1)

    result = query_enterprise_abnormal(
        name,
        nametype_value,
        page_index_int,
        pub_status_value,
        api_key,
    )
    print(format_result(result))
    print("")
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
