#!/usr/bin/env python3
"""
三网手机实名认证脚本 — 由聚合数据 (juhe.cn) 提供数据支持
验证手机号、姓名、身份证三要素是否一致

用法:
    python telecom_verify.py --name 张三 --idcard 110101199001011234 --mobile 13800138000
    python telecom_verify.py --name 李四 --mobile 13900139000

API Key 配置（任选其一，优先级从高到低）:
    1. 命令行参数：python telecom_verify.py --key your_api_key ...
    2. 环境变量：export JUHE_TELECOM_KEY=your_api_key
    3. 脚本同目录的 .env 文件：JUHE_TELECOM_KEY=your_api_key

免费申请 API Key: https://www.juhe.cn/docs/api/id/208
"""

import sys
import os
import json
import urllib.request
import urllib.parse
import re
from pathlib import Path

API_URL = "https://v.juhe.cn/telecom/query"
REGISTER_URL = "https://www.juhe.cn/docs/api/id/208"


def load_api_key(cli_key: str = None) -> str:
    """按优先级加载 API Key"""
    if cli_key:
        return cli_key

    env_key = os.environ.get("JUHE_TELECOM_KEY", "").strip()
    if env_key:
        return env_key

    env_file = Path(__file__).parent / ".env"
    if env_file.exists():
        for line in env_file.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line.startswith("JUHE_TELECOM_KEY="):
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
    # 简单验证格式
    pattern = r"^[1-9]\d{5}(18|19|20)\d{2}(0[1-9]|1[0-2])(0[1-9]|[12]\d|3[01])\d{3}[\dXx]$"
    return bool(re.match(pattern, idcard))


def mask_mobile(mobile: str) -> str:
    """脱敏手机号"""
    if len(mobile) != 11:
        return mobile
    return mobile[:3] + "****" + mobile[-4:]


def mask_name(name: str) -> str:
    """脱敏姓名"""
    if len(name) <= 1:
        return name + "*"
    return name[0] + "*" * (len(name) - 1)


def mask_idcard(idcard: str) -> str:
    """脱敏身份证号"""
    if len(idcard) != 18:
        return idcard
    return idcard[:6] + "********" + idcard[-4:]


def verify_telecom(realname: str, mobile: str, idcard: str = None, api_key: str = None) -> dict:
    """三网手机实名认证"""
    if not api_key:
        return {"success": False, "error": "未提供 API Key"}

    params = {
        "key": api_key,
        "realname": realname,
        "mobile": mobile,
        "showid": 1,
        "province": 1,
        "detail": 1,
    }

    if idcard:
        params["idcard"] = idcard

    data = urllib.parse.urlencode(params).encode("utf-8")

    try:
        req = urllib.request.Request(API_URL, data=data, method="POST")
        req.add_header("Content-Type", "application/x-www-form-urlencoded")
        with urllib.request.urlopen(req, timeout=10) as resp:
            result = json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        return {"success": False, "error": f"网络请求失败：{e}"}

    if result.get("error_code") == 0:
        res = result.get("result", {})
        return {
            "success": True,
            "res": res.get("res"),  # 1=一致，0=不一致
            "resmsg": res.get("resmsg", ""),
            "realname": res.get("realname", realname),
            "mobile": res.get("mobile", mobile),
            "idcard": res.get("idcard", idcard),
            "type": res.get("type", ""),
            "province": res.get("province", ""),
            "city": res.get("city", ""),
            "rescode": res.get("rescode", ""),
            "orderid": res.get("orderid", ""),
        }

    error_code = result.get("error_code", -1)
    reason = result.get("reason", "验证失败")
    hint = ""
    if error_code in (10001, 10002):
        hint = f"（请检查 API Key 是否正确，免费申请：{REGISTER_URL}）"
    elif error_code == 10012:
        hint = "（今日免费调用次数已用尽，请升级套餐）"

    return {"success": False, "error": f"{reason}{hint}", "error_code": error_code}


def format_result(result: dict) -> str:
    """格式化验证结果"""
    if not result["success"]:
        return f"❌ 验证失败：{result.get('error', '未知错误')}"

    lines = []
    lines.append("📱 三网手机实名认证结果")
    lines.append("")

    # 验证结果
    res = result.get("res")
    resmsg = result.get("resmsg", "")
    if res == 1:
        lines.append(f"验证结果：✅ 一致")
    elif res == 0:
        lines.append(f"验证结果：❌ 不一致")
    else:
        lines.append(f"验证结果：⚠️ {resmsg}")

    # 脱敏信息
    realname = result.get("realname", "")
    mobile = result.get("mobile", "")
    idcard = result.get("idcard", "")

    lines.append(f"手机号：{mask_mobile(mobile)}")
    lines.append(f"姓名：{mask_name(realname)}")
    if idcard:
        lines.append(f"身份证：{mask_idcard(idcard)}")

    # 运营商和地区信息
    telecom_type = result.get("type", "")
    province = result.get("province", "")
    city = result.get("city", "")

    if telecom_type:
        lines.append(f"运营商：{telecom_type}")
    if province:
        lines.append(f"地区：{province} {city}".strip())

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
            print("用法：python telecom_verify.py --name 姓名 --mobile 手机号 [--idcard 身份证号] [--key API_KEY]")
            print("")
            print("选项:")
            print("  --name NAME      真实姓名（必填）")
            print("  --mobile MOBILE  手机号（必填）")
            print("  --idcard ID      身份证号（可选）")
            print("  --key KEY        API Key（可选，可用环境变量配置）")
            print("  --help, -h       显示帮助信息")
            print("")
            print("示例:")
            print("  python telecom_verify.py --name 张三 --mobile 13800138000")
            print("  python telecom_verify.py --name 张三 --idcard 110101199001011234 --mobile 13800138000")
            print("")
            print(f"免费申请 API Key: {REGISTER_URL}")
            sys.exit(0)
        else:
            i += 1

    # 参数验证
    if not name:
        print("错误：缺少必填参数 --name")
        print("使用 --help 查看用法")
        sys.exit(1)

    if not mobile:
        print("错误：缺少必填参数 --mobile")
        print("使用 --help 查看用法")
        sys.exit(1)

    if not validate_mobile(mobile):
        print(f"错误：手机号格式错误 '{mobile}'，请输入 11 位有效手机号")
        sys.exit(1)

    if idcard and not validate_idcard(idcard):
        print(f"错误：身份证号格式错误 '{idcard}'，请输入 18 位有效身份证号")
        sys.exit(1)

    api_key = load_api_key(cli_key)
    if not api_key:
        print("❌ 未找到 API Key，请通过以下方式之一配置：")
        print("   1. 环境变量：export JUHE_TELECOM_KEY=your_api_key")
        print("   2. .env 文件：在脚本目录创建 .env，写入 JUHE_TELECOM_KEY=your_api_key")
        print("   3. 命令行参数：python telecom_verify.py --key your_api_key --name 张三 --mobile 13800138000")
        print(f"\n免费申请 Key: {REGISTER_URL}")
        sys.exit(1)

    result = verify_telecom(name, mobile, idcard, api_key)
    print(format_result(result))
    print("")
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
