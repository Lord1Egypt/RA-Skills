#!/usr/bin/env python3
"""
银行卡三要素核验脚本 — 由聚合数据 (juhe.cn) 提供数据支持
验证银行卡号、姓名、身份证号三要素是否一致

用法:
    python verify_bankcard_three.py --bankcard 卡号 --realname 姓名 --idcard 身份证号
    python verify_bankcard_three.py --file data.csv   # 批量核验

API Key 配置（任选其一，优先级从高到低）:
    1. 环境变量: export JUHE_BANKCARD3_KEY=your_api_key
    2. 脚本同目录的 .env 文件: JUHE_BANKCARD3_KEY=your_api_key
    3. 直接传参: python verify_bankcard_three.py --key your_api_key ...

免费申请 API Key: https://www.juhe.cn/docs/api/id/207
"""

import sys
import os
import json
import re
import csv
import urllib.request
import urllib.parse
from pathlib import Path

API_URL = "http://v.juhe.cn/verifybankcard3/query"
REGISTER_URL = "https://www.juhe.cn/docs/api/id/207"


def load_api_key(cli_key: str = None) -> str:
    """按优先级加载 API Key"""
    if cli_key:
        return cli_key

    env_key = os.environ.get("JUHE_BANKCARD3_KEY", "").strip()
    if env_key:
        return env_key

    env_file = Path(__file__).parent / ".env"
    if env_file.exists():
        for line in env_file.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line.startswith("JUHE_BANKCARD3_KEY="):
                val = line.split("=", 1)[1].strip().strip('"').strip("'")
                if val:
                    return val

    return ""


def validate_bankcard(bankcard: str) -> str | None:
    """校验银行卡号格式，返回错误信息或 None"""
    if not bankcard:
        return "银行卡号不能为空"
    if not bankcard.isdigit():
        return "银行卡号必须为纯数字"
    if len(bankcard) < 15 or len(bankcard) > 19:
        return "银行卡号长度应为15-19位"
    return None


def validate_idcard(idcard: str) -> str | None:
    """校验身份证号格式，返回错误信息或 None"""
    if not idcard:
        return "身份证号不能为空"
    if not re.match(r'^\d{17}[\dXx]$', idcard):
        return "身份证号格式不正确（应为18位，最后一位可为X）"
    return None


def validate_realname(realname: str) -> str | None:
    """校验姓名，返回错误信息或 None"""
    if not realname or not realname.strip():
        return "姓名不能为空"
    return None


def mask_bankcard(bankcard: str) -> str:
    """银行卡号脱敏：保留前4后4"""
    if len(bankcard) <= 8:
        return bankcard
    return bankcard[:4] + "*" * (len(bankcard) - 8) + bankcard[-4:]


def mask_idcard(idcard: str) -> str:
    """身份证号脱敏：保留前4后4"""
    if len(idcard) <= 8:
        return idcard
    return idcard[:4] + "*" * (len(idcard) - 8) + idcard[-4:]


def verify(bankcard: str, realname: str, idcard: str, api_key: str) -> dict:
    """核验银行卡三要素"""
    bankcard = bankcard.strip()
    realname = realname.strip()
    idcard = idcard.strip().upper()

    # 本地参数校验
    err = validate_bankcard(bankcard)
    if err:
        return {"success": False, "bankcard": bankcard, "realname": realname, "idcard": idcard, "error": err}

    err = validate_idcard(idcard)
    if err:
        return {"success": False, "bankcard": bankcard, "realname": realname, "idcard": idcard, "error": err}

    err = validate_realname(realname)
    if err:
        return {"success": False, "bankcard": bankcard, "realname": realname, "idcard": idcard, "error": err}

    params = urllib.parse.urlencode({
        "key": api_key,
        "bankcard": bankcard,
        "realname": realname,
        "idcard": idcard,
    })
    url = f"{API_URL}?{params}"

    try:
        with urllib.request.urlopen(url, timeout=15) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        return {
            "success": False,
            "bankcard": bankcard,
            "realname": realname,
            "idcard": idcard,
            "error": f"网络请求失败: {e}",
        }

    if data.get("error_code") == 0:
        r = data.get("result", {})
        return {
            "success": True,
            "bankcard": r.get("bankcard", bankcard),
            "realname": r.get("realname", realname),
            "idcard": r.get("idcard", idcard),
            "res": str(r.get("res", "")),
            "message": r.get("message", ""),
            "jobid": r.get("jobid", ""),
        }

    error_code = data.get("error_code", -1)
    reason = data.get("reason", "核验失败")
    hint = ""
    if error_code in (10001, 10002):
        hint = f"（请检查 API Key 是否正确，免费申请：{REGISTER_URL}）"
    elif error_code == 10012:
        hint = "（请求次数超限，请升级套餐）"
    return {
        "success": False,
        "bankcard": bankcard,
        "realname": realname,
        "idcard": idcard,
        "error": f"{reason}{hint}",
        "error_code": error_code,
    }


def format_result_line(result: dict) -> str:
    """格式化单条核验结果"""
    if not result["success"]:
        return f"❌ 核验失败: {result.get('error', '未知错误')}"

    res = result.get("res", "")
    if res == "1":
        return "💳 核验结果: 一致 ✓"
    elif res == "2":
        return f"💳 核验结果:  不一致 （{result.get('message', '未知')}）"
    else:
        return f"💳 核验结果: {result.get('message', '未知')}"

def main():
    args = sys.argv[1:]
    cli_key = None
    bankcard = None
    realname = None
    idcard = None
    file_path = None

    # 解析命令行参数
    i = 0
    while i < len(args):
        if args[i] == "--key" and i + 1 < len(args):
            cli_key = args[i + 1]
            i += 2
        elif args[i] == "--bankcard" and i + 1 < len(args):
            bankcard = args[i + 1]
            i += 2
        elif args[i] == "--realname" and i + 1 < len(args):
            realname = args[i + 1]
            i += 2
        elif args[i] == "--idcard" and i + 1 < len(args):
            idcard = args[i + 1]
            i += 2
        elif args[i] in ("-h", "--help"):
            print("用法:")
            print("  python verify_bankcard_three.py --bankcard 卡号 --realname 姓名 --idcard 身份证号")
            print("  python verify_bankcard_three.py --file data.csv")
            print()
            print("参数:")
            print("  --bankcard  银行卡号")
            print("  --realname  持卡人姓名")
            print("  --idcard    身份证号")
            print("  --file      CSV文件路径（批量核验，格式：银行卡号,姓名,身份证号）")
            print("  --key       API Key（也可通过环境变量或.env文件配置）")
            print()
            print(f"免费申请 API Key: {REGISTER_URL}")
            sys.exit(0)
        else:
            print(f"未知参数: {args[i]}")
            print("使用 --help 查看帮助")
            sys.exit(1)

    if not file_path and not (bankcard and realname and idcard):
        print("用法: python verify_bankcard_three.py --bankcard 卡号 --realname 姓名 --idcard 身份证号")
        print("      python verify_bankcard_three.py --file data.csv")
        print(f"\n免费申请 API Key: {REGISTER_URL}")
        sys.exit(1)

    api_key = load_api_key(cli_key)
    if not api_key:
        print("❌ 未找到 API Key，请通过以下方式之一配置：")
        print("   1. 环境变量: export JUHE_BANKCARD3_KEY=your_api_key")
        print("   2. .env 文件: 在脚本目录创建 .env，写入 JUHE_BANKCARD3_KEY=your_api_key")
        print("   3. 命令行参数: python verify_bankcard_three.py --key your_api_key ...")
        print(f"\n免费申请 Key: {REGISTER_URL}")
        sys.exit(1)

    # 单次核验模式
    result = verify(bankcard, realname, idcard, api_key)
    print(format_result_line(result))
    print()
    # 输出 JSON 时脱敏
    output = dict(result)
    output["bankcard"] = mask_bankcard(output.get("bankcard", ""))
    output["idcard"] = mask_idcard(output.get("idcard", ""))
    print(json.dumps(output, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
