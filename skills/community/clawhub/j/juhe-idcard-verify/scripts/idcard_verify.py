#!/usr/bin/env python3
"""
身份证实名认证脚本 — 由聚合数据 (juhe.cn) 提供数据支持
验证姓名与身份证号是否一致

用法:
    python idcard_verify.py --name 张三 --idcard 110101199001011234

API Key 配置（任选其一，优先级从高到低）:
    1. 命令行参数：python idcard_verify.py --key your_api_key ...
    2. 环境变量：export JUHE_IDCARD_VERIFY_KEY=your_api_key
    3. 脚本同目录的 .env 文件：JUHE_IDCARD_VERIFY_KEY=your_api_key

免费申请 API Key: https://www.juhe.cn/docs/api/id/103
"""

import sys
import os
import json
import urllib.request
import urllib.parse
import re
from pathlib import Path

API_URL = "http://op.juhe.cn/idcard/query"
REGISTER_URL = "https://www.juhe.cn/docs/api/id/103"


def load_api_key(cli_key: str = None) -> str:
    """按优先级加载 API Key"""
    if cli_key:
        return cli_key

    env_key = os.environ.get("JUHE_IDCARD_VERIFY_KEY", "").strip()
    if env_key:
        return env_key

    env_file = Path(__file__).parent / ".env"
    if env_file.exists():
        for line in env_file.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line.startswith("JUHE_IDCARD_VERIFY_KEY="):
                val = line.split("=", 1)[1].strip().strip('"').strip("'")
                if val:
                    return val

    return ""


def validate_idcard(idcard: str) -> bool:
    """验证身份证号格式"""
    if len(idcard) != 18:
        return False
    pattern = r"^[1-9]\d{5}(18|19|20)\d{2}(0[1-9]|1[0-2])(0[1-9]|[12]\d|3[01])\d{3}[\dXx]$"
    return bool(re.match(pattern, idcard))


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


def verify_idcard(realname: str, idcard: str, api_key: str = None) -> dict:
    """身份证实名认证"""
    if not api_key:
        return {"success": False, "error": "未提供 API Key"}

    params = urllib.parse.urlencode({
        "key": api_key,
        "realname": realname,
        "idcard": idcard,
    })
    url = f"{API_URL}?{params}"

    try:
        with urllib.request.urlopen(url, timeout=10) as resp:
            result = json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        return {"success": False, "error": f"网络请求失败：{e}"}

    if result.get("error_code") == 0:
        res = result.get("result", {})
        return {
            "success": True,
            "res": res.get("res"),  # 1=一致，2=不一致
            "realname": res.get("realname", realname),
            "idcard": res.get("idcard", idcard),
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
    lines.append("🆔 身份证实名认证结果")
    lines.append("")

    res = result.get("res")
    if res == 1:
        lines.append("验证结果：✅ 一致")
    elif res == 2:
        lines.append("验证结果：❌ 不一致")
    else:
        lines.append(f"验证结果：⚠️ 未知结果 ({res})")

    realname = result.get("realname", "")
    idcard = result.get("idcard", "")
    orderid = result.get("orderid", "")

    lines.append(f"姓名：{mask_name(realname)}")
    lines.append(f"身份证：{mask_idcard(idcard)}")
    if orderid:
        lines.append(f"订单号：{orderid}")

    return "\n".join(lines)


def main():
    args = sys.argv[1:]
    cli_key = None
    name = None
    idcard = None

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
        elif args[i] in ("--help", "-h"):
            print("用法：python idcard_verify.py --name 姓名 --idcard 身份证号 [--key API_KEY]")
            print("")
            print("选项:")
            print("  --name NAME      真实姓名（必填）")
            print("  --idcard ID      身份证号（必填）")
            print("  --key KEY        API Key（可选，可用环境变量配置）")
            print("  --help, -h       显示帮助信息")
            print("")
            print("示例:")
            print("  python idcard_verify.py --name 张三 --idcard 110101199001011234")
            print("")
            print(f"免费申请 API Key: {REGISTER_URL}")
            sys.exit(0)
        else:
            i += 1

    if not name:
        print("错误：缺少必填参数 --name")
        print("使用 --help 查看用法")
        sys.exit(1)

    if not idcard:
        print("错误：缺少必填参数 --idcard")
        print("使用 --help 查看用法")
        sys.exit(1)

    if not validate_idcard(idcard):
        print(f"错误：身份证号格式错误 '{idcard}'，请输入 18 位有效身份证号")
        sys.exit(1)

    api_key = load_api_key(cli_key)
    if not api_key:
        print("❌ 未找到 API Key，请通过以下方式之一配置：")
        print("   1. 环境变量：export JUHE_IDCARD_VERIFY_KEY=your_api_key")
        print("   2. .env 文件：在脚本目录创建 .env，写入 JUHE_IDCARD_VERIFY_KEY=your_api_key")
        print("   3. 命令行参数：python idcard_verify.py --key your_api_key --name 张三 --idcard 110101199001011234")
        print(f"\n免费申请 Key: {REGISTER_URL}")
        sys.exit(1)

    result = verify_idcard(name, idcard, api_key)
    print(format_result(result))
    print("")
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
