#!/usr/bin/env python3
"""
全球快递物流查询脚本 — 由聚合数据 (juhe.cn) 提供数据支持
支持全球上千家快递公司的快递单号跟踪

用法:
    python express_track.py <快递单号> --com <公司名称或编号>
    python express_track.py SF1234567890 --com 顺丰 --sender-phone 1234
    python express_track.py SF1234567890 --com 顺丰 --receiver-phone 5678
    python express_track.py YT1234567890 --com yt
    python express_track.py --list              # 查看所有支持的快递公司
    python express_track.py --search 顺丰        # 搜索快递公司

注意:
    --com 为必填参数，接口不支持自动识别快递公司
    --com 支持中文名称（如：顺丰）或编号（如：sf），脚本会自动转换为编号后传给接口
    顺丰、中通、跨越等快递需提供 --sender-phone 或 --receiver-phone 其中一个（手机号后4位）

API Key 配置（任选其一，优先级从高到低）:
    1. 环境变量: export JUHE_EXPRESS_KEY=your_api_key
    2. 脚本同目录的 .env 文件: JUHE_EXPRESS_KEY=your_api_key
    3. 直接传参: python express_track.py --key your_api_key <快递单号> --com <公司>

免费申请 API Key: https://www.juhe.cn/docs/api/id/43
"""

import sys
import os
import json
import urllib.request
import urllib.parse
from pathlib import Path

API_URL = "https://v.juhe.cn/exp/index"
REGISTER_URL = "https://www.juhe.cn/docs/api/id/43"

COMPANY_LIST_PATH = Path(__file__).parent.parent / "references" / "express-company-list.json"

# status_detail 英文枚举 → 中文描述（接口返回的准确状态）
STATUS_DETAIL_MAP = {
    "PENDING":    ("待处理",   "⏳"),
    "NO_RECORD":  ("无记录",   "❓"),
    "ERROR":      ("查询错误", "❌"),
    "IN_TRANSIT": ("运输中",   "🚚"),
    "DELIVERING": ("派件中",   "🛵"),
    "SIGNED":     ("已签收",   "✅"),
    "REJECTED":   ("拒收退回", "↩️"),
    "PROBLEM":    ("疑难件",   "⚠️"),
    "INVALID":    ("无效单号", "🚫"),
    "TIMEOUT":    ("查询超时", "⏱️"),
    "FAILED":     ("投递失败", "❌"),
    "SEND_BACK":  ("退件中",   "🔄"),
    "TAKING":     ("已揽件",   "📦"),
}

# status 数字兜底映射（status_detail 优先）
STATUS_NUM_MAP = {
    "0": ("运输中",   "🚚"),
    "1": ("已揽件",   "📦"),
    "2": ("疑难件",   "⚠️"),
    "3": ("已签收",   "✅"),
    "4": ("退签",     "↩️"),
    "5": ("派件中",   "🛵"),
    "6": ("退回",     "🔄"),
}


def load_api_key(cli_key: str = None) -> str:
    if cli_key:
        return cli_key
    env_key = os.environ.get("JUHE_EXPRESS_KEY", "").strip()
    if env_key:
        return env_key
    env_file = Path(__file__).parent / ".env"
    if env_file.exists():
        for line in env_file.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line.startswith("JUHE_EXPRESS_KEY="):
                val = line.split("=", 1)[1].strip().strip('"').strip("'")
                if val:
                    return val
    return ""


def load_company_list() -> list:
    if not COMPANY_LIST_PATH.exists():
        return []
    try:
        data = json.loads(COMPANY_LIST_PATH.read_text(encoding="utf-8"))
        return data.get("result", [])
    except Exception:
        return []


def find_company(keyword: str, companies: list) -> dict | None:
    """按公司名称或编号查找，支持模糊匹配"""
    keyword_lower = keyword.lower().strip()

    # 精确匹配编号
    for c in companies:
        if c.get("no", "").lower() == keyword_lower:
            return c

    # 精确匹配名称
    for c in companies:
        if c.get("com", "") == keyword:
            return c

    # 模糊匹配名称（包含）
    matches = [c for c in companies if keyword_lower in c.get("com", "").lower()]
    if len(matches) == 1:
        return matches[0]
    if len(matches) > 1:
        return {"_ambiguous": True, "matches": matches}

    return None


def search_companies(keyword: str, companies: list) -> list:
    """搜索快递公司，返回匹配列表"""
    keyword_lower = keyword.lower().strip()
    return [
        c for c in companies
        if keyword_lower in c.get("com", "").lower()
        or keyword_lower in c.get("no", "").lower()
    ]


def query_express(
    tracking_no: str,
    company_code: str,
    api_key: str,
    sender_phone: str = "",
    receiver_phone: str = "",
) -> dict:
    """调用聚合数据 API 查询快递物流"""
    params = {
        "key": api_key,
        "com": company_code,
        "no": tracking_no,
    }
    if sender_phone:
        params["senderPhone"] = sender_phone
    if receiver_phone:
        params["receiverPhone"] = receiver_phone

    url = f"{API_URL}?{urllib.parse.urlencode(params)}"

    try:
        with urllib.request.urlopen(url, timeout=15) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        return {"success": False, "error": f"网络请求失败: {e}"}

    error_code = int(data.get("error_code", -1))
    result_code = str(data.get("resultcode", ""))

    if error_code == 0 and result_code == "200":
        return {"success": True, "result": data.get("result", {})}

    reason = data.get("reason", "查询失败")
    hint = ""
    if error_code in (10001, 10002, 10003):
        hint = f"\n   请检查 API Key 是否正确，免费申请：{REGISTER_URL}"
    elif error_code == 10012:
        hint = "\n   今日免费调用次数已用尽，请升级套餐"
    elif error_code == 204301:
        hint = "\n   快递公司编号错误，请用 --list 查看支持的公司列表"
    elif error_code == 204302:
        hint = "\n   运单号格式错误，请检查单号是否正确"
    elif error_code == 204303:
        hint = "\n   查询失败，请稍后重试"
    elif error_code == 204304:
        hint = "\n   暂时查不到该单号的物流信息"
    elif error_code == 204305:
        hint = "\n   该快递公司（顺丰/中通/跨越等）需要提供手机号后4位\n   请使用 --sender-phone <寄件人后4位> 或 --receiver-phone <收件人后4位>"

    return {
        "success": False,
        "error": f"{reason}{hint}",
        "error_code": error_code,
    }


def resolve_status(status_detail: str, status_num: str) -> tuple[str, str]:
    """优先用 status_detail 英文枚举解析状态，兜底用数字"""
    if status_detail:
        label, icon = STATUS_DETAIL_MAP.get(status_detail.upper(), (status_detail, "📋"))
        return label, icon
    label, icon = STATUS_NUM_MAP.get(str(status_num), (f"状态{status_num}", "📋"))
    return label, icon


def print_tracking_result(result: dict, tracking_no: str) -> None:
    """格式化输出物流跟踪信息"""
    company = result.get("company", "")
    com_code = result.get("com", "")
    status_num = str(result.get("status", ""))
    status_detail = result.get("status_detail", "")
    logs = result.get("list", [])

    status_label, status_icon = resolve_status(status_detail, status_num)

    print(f"\n{'─' * 56}")
    print(f"  {status_icon}  {company}（{com_code}）  单号: {tracking_no}")
    status_line = f"  状态: {status_label}"
    if status_detail:
        status_line += f"  [{status_detail}]"
    print(status_line)
    print(f"{'─' * 56}")

    if not logs:
        print("  （暂无物流轨迹信息）")
    else:
        for i, item in enumerate(logs):
            dt = item.get("datetime", "")
            remark = item.get("remark", "")
            zone = item.get("zone", "")
            prefix = "  ▶ " if i == 0 else "    "
            location = f"【{zone}】" if zone else ""
            print(f"{prefix}{dt}")
            print(f"      {location}{remark}")
            if i < len(logs) - 1:
                print()

    print(f"{'─' * 56}\n")


def print_company_list(companies: list, keyword: str = "") -> None:
    """输出快递公司列表（可筛选）"""
    if keyword:
        filtered = search_companies(keyword, companies)
        if not filtered:
            print(f"未找到包含 '{keyword}' 的快递公司")
            return
        title = f"搜索 '{keyword}' 的结果（共 {len(filtered)} 家）："
    else:
        filtered = companies
        title = f"支持的快递公司（共 {len(filtered)} 家）："

    print(f"\n{title}\n")

    col_width_com = max((len(c.get("com", "")) for c in filtered), default=4)
    col_width_com = max(col_width_com, 6)

    def cjk_len(s):
        return sum(2 if ord(ch) > 127 else 1 for ch in s)

    def pad(text, width):
        actual = cjk_len(str(text))
        return str(text) + " " * max(0, width - actual)

    header_com = "公司名称"
    header_no = "编号"
    w_com = max(cjk_len(header_com), max((cjk_len(c.get("com", "")) for c in filtered), default=0))
    w_no = max(cjk_len(header_no), max((cjk_len(c.get("no", "")) for c in filtered), default=0))

    sep = f"+-{'-' * w_com}-+-{'-' * w_no}-+"
    print(sep)
    print(f"| {pad(header_com, w_com)} | {pad(header_no, w_no)} |")
    print(sep)
    for c in filtered:
        print(f"| {pad(c.get('com', ''), w_com)} | {pad(c.get('no', ''), w_no)} |")
    print(sep)
    print()


def parse_args(args: list) -> dict:
    result = {
        "cli_key": None,
        "tracking_no": None,
        "company": None,
        "sender_phone": None,
        "receiver_phone": None,
        "list": False,
        "search": None,
        "error": None,
    }

    i = 0
    positional = []

    while i < len(args):
        arg = args[i]
        if arg == "--key":
            if i + 1 < len(args):
                result["cli_key"] = args[i + 1]
                i += 2
            else:
                result["error"] = "错误: --key 后需要提供 API Key 值"
                return result
        elif arg in ("--com", "--company"):
            if i + 1 < len(args):
                result["company"] = args[i + 1]
                i += 2
            else:
                result["error"] = "错误: --com 后需要提供快递公司名称或编号"
                return result
        elif arg == "--sender-phone":
            if i + 1 < len(args):
                result["sender_phone"] = args[i + 1]
                i += 2
            else:
                result["error"] = "错误: --sender-phone 后需要提供寄件人手机号后4位"
                return result
        elif arg == "--receiver-phone":
            if i + 1 < len(args):
                result["receiver_phone"] = args[i + 1]
                i += 2
            else:
                result["error"] = "错误: --receiver-phone 后需要提供收件人手机号后4位"
                return result
        elif arg == "--list":
            result["list"] = True
            i += 1
        elif arg == "--search":
            if i + 1 < len(args):
                result["search"] = args[i + 1]
                i += 2
            else:
                result["error"] = "错误: --search 后需要提供搜索关键词"
                return result
        else:
            positional.append(arg)
            i += 1

    if positional:
        result["tracking_no"] = positional[0]

    return result


def main():
    args = sys.argv[1:]

    if not args:
        print("用法: python express_track.py <快递单号> --com <公司名称或编号>")
        print("      python express_track.py YT1234567890 --com 圆通")
        print("      python express_track.py SF1234567890 --com sf --sender-phone 1234")
        print("      python express_track.py SF1234567890 --com sf --receiver-phone 5678")
        print("      python express_track.py --list              # 查看所有支持的快递公司")
        print("      python express_track.py --search 顺丰        # 搜索快递公司编号")
        print()
        print("选项:")
        print("  --com <名称/编号>      【必填】快递公司，支持中文名称（顺丰）或编号（sf），脚本自动转为编号")
        print("  --sender-phone <4位>   寄件人手机号后4位（顺丰/中通/跨越等必填其一）")
        print("  --receiver-phone <4位> 收件人手机号后4位（顺丰/中通/跨越等必填其一）")
        print("  --list                 列出所有支持的快递公司及编号")
        print("  --search <关键词>      搜索快递公司编号")
        print()
        print(f"免费申请 API Key: {REGISTER_URL}")
        sys.exit(1)

    parsed = parse_args(args)
    if parsed["error"]:
        print(parsed["error"])
        sys.exit(1)

    companies = load_company_list()

    if parsed["list"]:
        print_company_list(companies)
        sys.exit(0)

    if parsed["search"]:
        print_company_list(companies, parsed["search"])
        sys.exit(0)

    if not parsed["tracking_no"]:
        print("错误: 请提供快递单号")
        print("用法: python express_track.py <快递单号> --com <公司名称或编号>")
        sys.exit(1)

    if not parsed["company"]:
        print("错误: --com 为必填参数，接口不支持自动识别快递公司")
        print("用法: python express_track.py <快递单号> --com <公司名称或编号>")
        print("示例: python express_track.py SF1234567890 --com 顺丰")
        print("      python express_track.py YT1234567890 --com yt")
        print("\n使用 --search <关键词> 搜索快递公司编号，例如: --search 顺丰")
        sys.exit(1)

    tracking_no = parsed["tracking_no"]
    sender_phone = parsed.get("sender_phone") or ""
    receiver_phone = parsed.get("receiver_phone") or ""

    found = find_company(parsed["company"], companies)
    if found is None:
        print(f"❌ 未找到快递公司 '{parsed['company']}'")
        print(f"   使用 --search <关键词> 搜索，或 --list 查看所有支持的公司")
        sys.exit(1)
    if found.get("_ambiguous"):
        matches = found["matches"]
        print(f"⚠️  '{parsed['company']}' 匹配到多家公司，请使用编号精确指定：\n")
        for m in matches[:10]:
            print(f"   {m['com']}  →  编号: {m['no']}")
        if len(matches) > 10:
            print(f"   ... 共 {len(matches)} 家，请缩小关键词范围")
        sys.exit(1)
    company_code = found["no"]
    company_name = found["com"]

    api_key = load_api_key(parsed["cli_key"])
    if not api_key:
        print("❌ 未找到 API Key，请通过以下方式之一配置：")
        print("   1. 环境变量: export JUHE_EXPRESS_KEY=your_api_key")
        print("   2. .env 文件: 在脚本目录创建 .env，写入 JUHE_EXPRESS_KEY=your_api_key")
        print("   3. 命令行参数: python express_track.py --key your_api_key <快递单号> --com <公司>")
        print(f"\n免费申请 Key: {REGISTER_URL}")
        sys.exit(1)

    print(f"\n📦 查询单号: {tracking_no}  快递公司: {company_name}（{company_code}）")

    result = query_express(
        tracking_no=tracking_no,
        company_code=company_code,
        api_key=api_key,
        sender_phone=sender_phone,
        receiver_phone=receiver_phone,
    )

    if not result["success"]:
        print(f"❌ 查询失败: {result['error']}")
        sys.exit(1)

    print_tracking_result(result["result"], tracking_no)


if __name__ == "__main__":
    main()
