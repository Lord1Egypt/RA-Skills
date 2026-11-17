#!/usr/bin/env python3
"""
自然人对外投资任职查询脚本 — 由聚合数据 (juhe.cn) 提供数据支持
根据姓名、身份证号（可选手机号）查询自然人对外投资和任职信息

用法:
    python person_invest.py --name 张三 --idcard 110101199001011234
    python person_invest.py --name 张三 --idcard 110101199001011234 --mobile 13800138000

API Key 配置（任选其一，优先级从高到低）:
    1. 命令行参数：python person_invest.py --key your_api_key --name 张三 --idcard 身份证号
    2. 环境变量：export JUHE_PERSON_INVEST_KEY=your_api_key
    3. 脚本同目录的 .env 文件：JUHE_PERSON_INVEST_KEY=your_api_key

申请 API Key: https://www.juhe.cn/docs/api/id/320
"""

import sys
import os
import json
import re
import urllib.request
import urllib.parse
from pathlib import Path

API_URL = "https://apis.juhe.cn/personinvest/query"
REGISTER_URL = "https://www.juhe.cn/docs/api/id/320"

RELATIONSHIP_LABELS = {
    "lp": "法人",
    "tm": "高管",
    "sh": "股东",
}


def load_api_key(cli_key: str = None) -> str:
    """按优先级加载 API Key"""
    if cli_key:
        return cli_key

    env_key = os.environ.get("JUHE_PERSON_INVEST_KEY", "").strip()
    if env_key:
        return env_key

    env_file = Path(__file__).parent / ".env"
    if env_file.exists():
        for line in env_file.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line.startswith("JUHE_PERSON_INVEST_KEY="):
                val = line.split("=", 1)[1].strip().strip('"').strip("'")
                if val:
                    return val

    return ""


def validate_mobile(mobile: str) -> bool:
    """验证手机号格式"""
    return bool(re.match(r"^1[3-9]\d{9}$", mobile))


def validate_idcard(idcard: str) -> bool:
    """验证身份证号格式"""
    if len(idcard) != 18:
        return False
    pattern = r"^[1-9]\d{5}(18|19|20)\d{2}(0[1-9]|1[0-2])(0[1-9]|[12]\d|3[01])\d{3}[\dXx]$"
    return bool(re.match(pattern, idcard))


def mask_mobile(mobile: str) -> str:
    if len(mobile) != 11:
        return mobile
    return mobile[:3] + "****" + mobile[-4:]


def mask_name(name: str) -> str:
    if not name:
        return "-"
    if len(name) <= 1:
        return name + "*"
    return name[0] + "*" * (len(name) - 1)


def mask_idcard(idcard: str) -> str:
    if len(idcard) != 18:
        return idcard
    return idcard[:6] + "********" + idcard[-4:]


def format_relationships(values) -> str:
    if not values:
        return "-"
    if isinstance(values, str):
        values = [values]
    labels = [RELATIONSHIP_LABELS.get(str(item).strip().lower(), str(item)) for item in values]
    return "、".join(labels) if labels else "-"


def query_person_invest(
    name: str,
    idcard: str,
    mobile: str = None,
    api_key: str = None,
) -> dict:
    """查询自然人对外投资任职信息"""
    if not api_key:
        return {"success": False, "error": "未提供 API Key"}

    params = {
        "key": api_key,
        "name": name,
        "idcard": idcard,
    }
    if mobile:
        params["mobile"] = mobile

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
        relation_counts = {"lp": 0, "tm": 0, "sh": 0}
        for item in items:
            relations = item.get("relationship") or []
            if isinstance(relations, str):
                relations = [relations]
            for rel in relations:
                key = str(rel).strip().lower()
                if key in relation_counts:
                    relation_counts[key] += 1
        return {
            "success": True,
            "orderid": payload.get("orderid", ""),
            "name": name,
            "idcard": idcard,
            "mobile": mobile or "",
            "total_count": len(items),
            "lp_count": relation_counts["lp"],
            "tm_count": relation_counts["tm"],
            "sh_count": relation_counts["sh"],
            "items": items,
        }

    error_code = result.get("error_code", -1)
    reason = result.get("reason", "查询失败")
    hint = ""
    if error_code in (10001, 10002, 10003, 10009):
        hint = f"（请检查 API Key 是否正确，申请地址：{REGISTER_URL}）"
    elif error_code == 10012:
        hint = "（今日调用次数已用尽，请升级套餐）"
    elif error_code == 232001:
        hint = "（网络超时，请稍后重试）"
    elif error_code == 232002:
        hint = "（请检查 name / idcard 是否为空）"
    elif error_code == 232003:
        hint = "（姓名格式错误，请重新输入）"
    elif error_code == 232004:
        hint = "（身份证号格式错误，请输入 18 位有效身份证号）"
    elif error_code == 232005:
        hint = "（手机号格式错误，请输入 11 位有效手机号）"
    elif error_code == 232006:
        hint = "（未找到对外投资或任职记录）"
    elif error_code == 232008:
        hint = "（查询失败，请稍后重试）"

    return {"success": False, "error": f"{reason}{hint}", "error_code": error_code}


def display_value(value: str) -> str:
    text = (value or "").strip()
    return text if text else "-"


def format_result(result: dict) -> str:
    """格式化查询结果"""
    if not result["success"]:
        return f"❌ 查询失败：{result.get('error', '未知错误')}"

    items = result.get("items") or []
    total_count = result.get("total_count", len(items))
    name = result.get("name", "")
    idcard = result.get("idcard", "")
    mobile = result.get("mobile", "")

    lines = []
    lines.append("👤 自然人对外投资任职查询结果")
    lines.append("")
    lines.append(f"查询人：{mask_name(name)}    身份证：{mask_idcard(idcard)}")
    if mobile:
        lines.append(f"手机号：{mask_mobile(mobile)}")
    lines.append(f"共找到 {total_count} 家关联企业")
    lines.append(
        f"关系统计：法人 {result.get('lp_count', 0)} 家，"
        f"高管 {result.get('tm_count', 0)} 家，"
        f"股东 {result.get('sh_count', 0)} 家"
    )

    if not items:
        lines.append("")
        lines.append("暂无对外投资或任职记录。")
        return "\n".join(lines)

    for idx, item in enumerate(items, 1):
        org_name = display_value(item.get("orgName"))
        legal_person = display_value(item.get("legalPersonName"))
        relation = format_relationships(item.get("relationship"))
        position = display_value(item.get("typeJoin"))
        status = display_value(item.get("regStatus"))
        org_type = display_value(item.get("companyOrgType"))
        credit_code = display_value(item.get("creditCode"))
        industry = display_value(item.get("industry"))
        reg_number = display_value(item.get("regNumber"))
        establish_time = display_value(item.get("estiblishTime"))
        capital = display_value(item.get("regCapital"))
        currency = display_value(item.get("regCapitalCurrency"))
        subscript_amt = display_value(item.get("subscriptAmt"))
        invest_date = display_value(item.get("investDate"))
        funded_ratio = display_value(item.get("fundedRatio"))
        base = display_value(item.get("base"))

        lines.append("")
        lines.append(f"{idx}. {org_name}")
        lines.append(f"   关系：{relation}    职务：{position}    状态：{status}")
        lines.append(f"   法人：{legal_person}    省份：{base}    成立：{establish_time}")
        lines.append(f"   类型：{org_type}    行业：{industry}")
        lines.append(f"   统一社会信用代码：{credit_code}")
        lines.append(f"   注册号：{reg_number}")
        lines.append(f"   注册资本：{capital}    币种：{currency}")
        lines.append(f"   认缴出资：{subscript_amt}    比例：{funded_ratio}    出资时间：{invest_date}")

    return "\n".join(lines)


def main():
    args = sys.argv[1:]
    cli_key = None
    name = None
    idcard = None
    mobile = None

    i = 0
    while i < len(args):
        if args[i] == "--key" and i + 1 < len(args):
            cli_key = args[i + 1]
            i += 2
        elif args[i] == "--name" and i + 1 < len(args):
            name = args[i + 1]
            i += 2
        elif args[i] == "--idcard" and i + 1 < len(args):
            idcard = args[i + 1]
            i += 2
        elif args[i] == "--mobile" and i + 1 < len(args):
            mobile = args[i + 1]
            i += 2
        elif args[i] in ("--help", "-h"):
            print("用法：python person_invest.py --name 姓名 --idcard 身份证号 [--mobile 手机号] [--key API_KEY]")
            print("")
            print("选项:")
            print("  --name NAME      真实姓名（必填）")
            print("  --idcard ID      身份证号（必填）")
            print("  --mobile MOBILE  手机号（可选）")
            print("  --key KEY        API Key（可选，可用环境变量配置）")
            print("  --help, -h       显示帮助信息")
            print("")
            print("示例:")
            print("  python person_invest.py --name 张三 --idcard 110101199001011234")
            print("  python person_invest.py --name 张三 --idcard 110101199001011234 --mobile 13800138000")
            print("")
            print(f"申请 API Key: {REGISTER_URL}")
            sys.exit(0)
        else:
            i += 1

    if not name or not str(name).strip():
        print("错误：缺少必填参数 --name")
        print("使用 --help 查看用法")
        sys.exit(1)

    if not idcard or not str(idcard).strip():
        print("错误：缺少必填参数 --idcard")
        print("使用 --help 查看用法")
        sys.exit(1)

    name = name.strip()
    idcard = idcard.strip()
    mobile = mobile.strip() if mobile else None

    if not validate_idcard(idcard):
        print(f"错误：身份证号格式错误 '{idcard}'，请输入 18 位有效身份证号")
        sys.exit(1)

    if mobile and not validate_mobile(mobile):
        print(f"错误：手机号格式错误 '{mobile}'，请输入 11 位有效手机号")
        sys.exit(1)

    api_key = load_api_key(cli_key)
    if not api_key:
        print("❌ 未找到 API Key，请通过以下方式之一配置：")
        print("   1. 环境变量：export JUHE_PERSON_INVEST_KEY=your_api_key")
        print("   2. .env 文件：在脚本目录创建 .env，写入 JUHE_PERSON_INVEST_KEY=your_api_key")
        print("   3. 命令行参数：python person_invest.py --key your_api_key --name 张三 --idcard 身份证号")
        print(f"\n申请 Key: {REGISTER_URL}")
        sys.exit(1)

    result = query_person_invest(name, idcard, mobile, api_key)
    print(format_result(result))
    print("")
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
