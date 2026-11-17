#!/usr/bin/env python3
"""
VIN 查车辆信息-精准版脚本 — 由聚合数据 (juhe.cn) 提供数据支持
通过 17 位车架号查询品牌、车系、车型、排量、排放标准等详细参数

用法:
    python vin_info.py --vin LBV21AF05MSZ88595

API Key 配置（任选其一，优先级从高到低）:
    1. 命令行参数：python vin_info.py --key your_api_key --vin LBV21AF05MSZ88595
    2. 环境变量：export JUHE_VIN_CAR_DETAIL_KEY=your_api_key
    3. 脚本同目录的 .env 文件：JUHE_VIN_CAR_DETAIL_KEY=your_api_key

申请 API Key: https://www.juhe.cn/docs/api/id/862
"""

import sys
import os
import json
import re
import urllib.request
import urllib.parse
from pathlib import Path

API_URL = "https://apis.juhe.cn/carinfo/vinInfo"
REGISTER_URL = "https://www.juhe.cn/docs/api/id/862"
VIN_PATTERN = re.compile(r"^[A-HJ-NPR-Z0-9]{17}$", re.I)

FIELD_GROUPS = [
    ("基本信息", [
        ("amMainBrandName", "一级品牌"),
        ("amBrandName", "二级品牌"),
        ("amSeriesName", "车系"),
        ("amVehicleName", "销售车型"),
        ("amYear", "年款"),
        ("amVinYear", "VIN出厂年份"),
        ("amGroupName", "车组"),
        ("vehCateNames", "车型大类"),
        ("vehCateOneNames", "一级分类"),
        ("vehCateTwoNames", "二级分类"),
        ("cfgLevel", "配置等级"),
        ("countriesName", "国别"),
        ("importFlag", "国产/进口"),
        ("marketDate", "上市日期"),
        ("stopDate", "停产日期"),
        ("price", "厂商指导价(元)"),
        ("purchasePrice", "新车市场价"),
    ]),
    ("动力与排放", [
        ("powerType", "动力类型"),
        ("displacement", "排量(L)"),
        ("power", "功率"),
        ("engineModel", "发动机型号"),
        ("engineDesc", "发动机描述"),
        ("airIntakeType", "进气形式"),
        ("fuelJetType", "燃油喷射"),
        ("roz", "燃油标号"),
        ("effluentStandard", "排放标准"),
        ("arrayType", "气缸排列"),
        ("valveNum", "气门数"),
        ("gearboxType", "变速器类型"),
        ("gearNum", "档位数"),
        ("drivenType", "驱动形式"),
    ]),
    ("车身尺寸", [
        ("bodyType", "车身结构"),
        ("vehicleSize", "外形尺寸(mm)"),
        ("wheelBase", "轴距(mm)"),
        ("trackFront", "前轮距(mm)"),
        ("trackRear", "后轮距(mm)"),
        ("fullWeight", "整备质量(kg)"),
        ("seats", "座位数"),
        ("doorNum", "车门数"),
        ("frontTyreSize", "前轮胎规格"),
        ("rearTyreSize", "后轮胎规格"),
        ("absFlag", "ABS"),
        ("chassisModel", "底盘号"),
        ("publicationNos", "公告号"),
    ]),
]


def load_api_key(cli_key: str = None) -> str:
    if cli_key:
        return cli_key

    env_key = os.environ.get("JUHE_VIN_CAR_DETAIL_KEY", "").strip()
    if env_key:
        return env_key

    env_file = Path(__file__).parent / ".env"
    if env_file.exists():
        for line in env_file.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line.startswith("JUHE_VIN_CAR_DETAIL_KEY="):
                val = line.split("=", 1)[1].strip().strip('"').strip("'")
                if val:
                    return val
    return ""


def normalize_vin(vin: str) -> str:
    return re.sub(r"[\s\-]", "", vin or "").upper()


def validate_vin(vin: str) -> bool:
    return bool(VIN_PATTERN.match(vin))


def display_value(key: str, value) -> str:
    text = str(value or "").strip()
    if not text:
        return ""
    if key in ("price", "purchasePrice") and text.replace(".", "", 1).isdigit():
        try:
            number = float(text)
            if number.is_integer():
                return f"{int(number):,}"
            return f"{number:,.2f}"
        except ValueError:
            return text
    return text


def query_vin_info(vin: str, api_key: str) -> dict:
    if not api_key:
        return {"success": False, "error": "未提供 API Key"}

    params = {"key": api_key, "vin": vin}
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
        return {"success": True, **payload}

    error_code = result.get("error_code", -1)
    reason = result.get("reason", "查询失败")
    hint = ""
    if error_code in (10001, 10002, 10003, 10009):
        hint = f"（请检查 API Key 是否正确，申请地址：{REGISTER_URL}）"
    elif error_code == 10012:
        hint = "（今日调用次数已用尽，请升级套餐）"
    elif error_code == 286201:
        hint = "（车架号须为 17 位，且不含字母 I、O、Q）"
    elif error_code == 286204:
        hint = "（未找到该 VIN 对应车辆信息）"
    elif error_code in (286202, 286203):
        hint = "（接口异常，请稍后重试）"
    return {"success": False, "error": f"{reason}{hint}", "error_code": error_code}


def format_result(result: dict) -> str:
    if not result["success"]:
        return f"❌ 查询失败：{result.get('error', '未知错误')}"

    lines = ["🚗 VIN 查车辆信息（精准版）", ""]
    vin = result.get("vin") or "-"
    lines.append(f"VIN：{vin}")
    vehicle = result.get("amVehicleName") or "-"
    lines.append(f"车型：{vehicle}")

    for title, fields in FIELD_GROUPS:
        rows = []
        for key, label in fields:
            value = display_value(key, result.get(key))
            if value:
                rows.append(f"   {label}：{value}")
        if rows:
            lines.append("")
            lines.append(title)
            lines.extend(rows)
    return "\n".join(lines)


def main():
    args = sys.argv[1:]
    cli_key = None
    vin = None

    i = 0
    while i < len(args):
        if args[i] == "--key" and i + 1 < len(args):
            cli_key = args[i + 1]
            i += 2
        elif args[i] == "--vin" and i + 1 < len(args):
            vin = args[i + 1]
            i += 2
        elif args[i] in ("--help", "-h"):
            print("用法：python vin_info.py --vin 17位车架号 [--key API_KEY]")
            print("")
            print("选项:")
            print("  --vin VIN    17 位车架号（必填，不含 I/O/Q）")
            print("  --key KEY    API Key（可选，可用环境变量配置）")
            print("  --help, -h   显示帮助信息")
            print("")
            print("示例:")
            print("  python vin_info.py --vin LBV21AF05MSZ88595")
            print("")
            print(f"申请 API Key: {REGISTER_URL}")
            sys.exit(0)
        else:
            i += 1

    if not vin or not str(vin).strip():
        print("错误：缺少必填参数 --vin")
        print("使用 --help 查看用法")
        sys.exit(1)

    vin = normalize_vin(vin)
    if not validate_vin(vin):
        print(f"错误：VIN 码格式错误 '{vin}'，须为 17 位字母数字且不含 I、O、Q")
        sys.exit(1)

    api_key = load_api_key(cli_key)
    if not api_key:
        print("❌ 未找到 API Key，请通过以下方式之一配置：")
        print("   1. 环境变量：export JUHE_VIN_CAR_DETAIL_KEY=your_api_key")
        print("   2. .env 文件：在脚本目录创建 .env，写入 JUHE_VIN_CAR_DETAIL_KEY=your_api_key")
        print("   3. 命令行参数：python vin_info.py --key your_api_key --vin LBV21AF05MSZ88595")
        print(f"\n申请 Key: {REGISTER_URL}")
        sys.exit(1)

    result = query_vin_info(vin, api_key)
    print(format_result(result))
    print("")
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
