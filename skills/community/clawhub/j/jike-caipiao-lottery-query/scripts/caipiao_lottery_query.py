#!/usr/bin/env python3
"""
即刻数据彩票查询 Skill 脚本。

功能说明：
1. 支持最新开奖、指定彩种指定期号详情、三位型彩票历史号码、三位型彩票冷热号统计。
2. 按 `--key`、环境变量、脚本目录 `.env` 的优先级读取 AppKey。
3. 分别调用 `/v1/caipiao/lottery/latest`、`/detail`、`/number_history`、`/number_stat` 接口。
4. 将开奖日期、期号、开奖号码、销售额、奖池、奖项和冷热号整理为适合 AI 客户端展示的文本。
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import unicodedata
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any

API_BASE_URL = os.environ.get("JIKE_API_BASE_URL", "https://api.jikeapi.cn").rstrip("/")
API_PATH_MAP = {
    "latest": "/v1/caipiao/lottery/latest",
    "detail": "/v1/caipiao/lottery/detail",
    "number-history": "/v1/caipiao/lottery/number_history",
    "number-stat": "/v1/caipiao/lottery/number_stat",
}
APPKEY_ENV_NAMES = ("JIKE_CAIPIAO_LOTTERY_QUERY_KEY", "JIKE_APPKEY")
REGISTER_URL = "https://www.jikeapi.cn/"
LOTTERY_TYPES = {
    "dlt": "大乐透",
    "pl3": "排列3",
    "pl5": "排列5",
    "qxc": "七星彩",
    "ssq": "双色球",
    "fc3d": "福彩3D",
    "qlc": "七乐彩",
    "kl8": "快乐8",
}
THREE_DIGIT_TYPES = {"pl3", "fc3d"}


def load_appkey(cli_key: str | None = None) -> str:
    """
    功能说明：
    1. 读取彩票查询需要的 AppKey。
    2. 优先使用命令行 `--key`，便于临时调试。
    3. 其次读取业务环境变量或通用 `JIKE_APPKEY`。
    4. 最后读取脚本目录 `.env` 文件。

    @param cli_key 命令行传入的 AppKey
    @return string AppKey，未找到时返回空字符串
    """
    if cli_key:
        return cli_key.strip()
    for env_name in APPKEY_ENV_NAMES:
        env_value = os.environ.get(env_name, "").strip()
        if env_value:
            return env_value
    env_file = Path(__file__).parent / ".env"
    if not env_file.exists():
        return ""
    for line in env_file.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        if key.strip() in APPKEY_ENV_NAMES:
            value = value.strip().strip('"').strip("'")
            if value:
                return value
    return ""


def parse_args(argv: list[str]) -> argparse.Namespace:
    """
    功能说明：
    1. 解析彩票查询子命令参数。
    2. `latest` 查询 8 种彩票最新开奖。
    3. `detail` 查询指定彩种和期号的开奖详情。
    4. `number-history` 和 `number-stat` 仅用于福彩3D、排列3。
    5. `--json` 支持放在子命令前或子命令后。

    @param argv 命令行参数列表
    @return argparse.Namespace 解析后的参数对象
    """
    json_output = "--json" in argv
    argv = [item for item in argv if item != "--json"]

    parser = argparse.ArgumentParser(description="彩票查询 - 即刻数据")
    parser.add_argument("--key", dest="cli_key", help="临时传入即刻数据 AppKey")
    parser.add_argument("--json", dest="json_output", action="store_true", help="输出 JSON")
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("latest", help="获取 8 种彩票最新开奖")

    detail_parser = subparsers.add_parser("detail", help="查询指定彩种指定期号的开奖详情")
    detail_parser.add_argument("--type", required=True, help="彩票类型，例如 ssq、dlt、pl3、fc3d")
    detail_parser.add_argument("--sn", required=True, help="期号，例如 2024001")

    history_parser = subparsers.add_parser("number-history", help="查询开奖号码历史出现记录，仅支持 pl3、fc3d")
    history_parser.add_argument("--type", required=True, help="彩票类型，仅支持 pl3 或 fc3d")
    history_parser.add_argument("--number", required=True, help="三位开奖号码，例如 666")

    stat_parser = subparsers.add_parser("number-stat", help="查询冷热号统计，仅支持 pl3、fc3d")
    stat_parser.add_argument("--type", required=True, help="彩票类型，仅支持 pl3 或 fc3d")

    args = parser.parse_args(argv)
    args.json_output = args.json_output or json_output
    return args


def normalize_type(type_value: str, only_three_digit: bool = False) -> str:
    """
    功能说明：
    1. 清理并小写彩票类型参数。
    2. `detail` 支持 8 种彩票类型。
    3. 历史号码和冷热号只支持福彩3D、排列3。

    @param type_value 用户输入的彩票类型
    @param only_three_digit 是否限制为三位型彩票
    @return string 合法的彩票类型标识
    @raises ValueError 类型不支持时抛出
    """
    value = type_value.strip().lower()
    allowed_types = THREE_DIGIT_TYPES if only_three_digit else set(LOTTERY_TYPES)
    if value not in allowed_types:
        names = "、".join(f"{key}({LOTTERY_TYPES[key]})" for key in sorted(allowed_types))
        raise ValueError(f"type 暂只支持: {names}")
    return value


def build_params(args: argparse.Namespace) -> dict[str, Any]:
    """
    功能说明：
    1. 根据彩票子命令构造接口参数。
    2. 最新开奖接口不需要业务参数。
    3. 开奖详情校验彩种和期号，期号按字符串传递以保留可能的前导零。
    4. 历史号码接口校验三位数字，冷热号接口校验三位型彩票类型。

    @param args argparse 解析结果
    @return dict 接口业务参数
    @raises ValueError 参数格式非法时抛出
    """
    if args.command == "latest":
        return {}
    if args.command == "detail":
        sn = args.sn.strip()
        if not re.fullmatch(r"\d{1,12}", sn):
            raise ValueError("sn 必须是 1 到 12 位数字期号，例如 2024001")
        return {"type": normalize_type(args.type), "sn": sn}
    if args.command == "number-history":
        number = args.number.strip()
        if not re.fullmatch(r"\d{3}", number):
            raise ValueError("number 必须是 3 位数字，例如 666")
        return {"type": normalize_type(args.type, True), "number": number}
    return {"type": normalize_type(args.type, True)}


def request_api(command: str, params: dict[str, Any], appkey: str) -> dict[str, Any]:
    """
    功能说明：
    1. 根据子命令选择彩票查询接口。
    2. 自动追加 appkey 参数，并使用 GET 方式请求即刻数据开放接口。
    3. 返回接口 JSON；HTTP、网络或解析异常时返回统一错误结构。

    @param command 子命令名称
    @param params 接口业务参数
    @param appkey 即刻数据 AppKey
    @return dict 接口返回或错误结构
    """
    url = f"{API_BASE_URL}{API_PATH_MAP[command]}?{urllib.parse.urlencode({**params, 'appkey': appkey})}"
    try:
        with urllib.request.urlopen(url, timeout=15) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        return {"code": exc.code, "message": f"接口请求失败: HTTP {exc.code}", "data": ""}
    except urllib.error.URLError as exc:
        return {"code": 500, "message": f"网络请求失败: {exc.reason}", "data": ""}
    except Exception as exc:
        return {"code": 500, "message": f"请求异常: {exc}", "data": ""}


def display_width(value: str) -> int:
    """
    功能说明：
    1. 计算终端展示宽度。
    2. 中文和全角字符按 2 个字符宽度处理。
    3. 用于彩票列表、奖项列表和冷热号列表表格对齐。

    @param value 待计算文本
    @return int 展示宽度
    """
    return sum(2 if unicodedata.east_asian_width(char) in ("F", "W") else 1 for char in value)


def truncate(value: Any, max_width: int = 34) -> str:
    """
    功能说明：
    1. 将长文本裁剪到指定展示宽度。
    2. 开奖号码和一等奖说明可能较长，列表展示时只保留摘要。
    3. 详情字段仍保留重点信息，避免终端输出过宽。

    @param value 原始值
    @param max_width 最大展示宽度
    @return string 裁剪后的文本
    """
    text = str(value or "-").replace("\n", " ").strip()
    current = 0
    chars = []
    for char in text:
        width = 2 if unicodedata.east_asian_width(char) in ("F", "W") else 1
        if current + width > max_width:
            chars.append("...")
            break
        chars.append(char)
        current += width
    return "".join(chars) or "-"


def pad_cell(value: Any, width: int) -> str:
    """
    功能说明：
    1. 将表格单元格内容转换为字符串。
    2. 根据中文展示宽度补齐空格。
    3. 保证不同彩种、号码和金额字段对齐。

    @param value 单元格内容
    @param width 目标展示宽度
    @return string 补齐后的文本
    """
    text = str(value or "-")
    return text + " " * max(width - display_width(text), 0)


def print_table(headers: list[str], rows: list[list[Any]]) -> None:
    """
    功能说明：
    1. 输出彩票查询表格。
    2. 自动计算每列展示宽度。
    3. 用于展示最新开奖、历史开奖、奖项列表和冷热号统计。

    @param headers 表头列表
    @param rows 表格数据列表
    @return void
    """
    widths = [display_width(header) for header in headers]
    for row in rows:
        for index, value in enumerate(row):
            widths[index] = max(widths[index], display_width(str(value or "-")))
    border = "+" + "+".join("-" * (width + 2) for width in widths) + "+"
    print(border)
    print("| " + " | ".join(pad_cell(header, widths[index]) for index, header in enumerate(headers)) + " |")
    print(border)
    for row in rows:
        print("| " + " | ".join(pad_cell(value, widths[index]) for index, value in enumerate(row)) + " |")
    print(border)


def print_latest_result(data: list[dict[str, Any]]) -> None:
    """
    功能说明：
    1. 输出 8 种彩票最新开奖列表。
    2. 展示彩种、类型标识、期号、开奖日期、星期、开奖号码和销售额。
    3. 开奖号码较长时进行摘要裁剪，避免表格过宽。

    @param data 最新开奖列表
    @return void
    """
    rows = []
    for item in data:
        rows.append([
            item.get("type_name"),
            item.get("type_abbr"),
            item.get("sn"),
            item.get("date"),
            item.get("week"),
            truncate(item.get("number"), 42),
            item.get("sales"),
        ])
    print_table(["彩种", "标识", "期号", "开奖日期", "星期", "开奖号码", "销售额"], rows)


def collect_prize_rows(data: dict[str, Any]) -> list[list[Any]]:
    """
    功能说明：
    1. 从开奖详情中提取奖项字段。
    2. 按 `p1` 到 `p12` 扫描金额、注数、总金额、说明字段。
    3. 不同彩种返回字段不完全一致，只展示接口实际返回的非空奖项。

    @param data 开奖详情数据
    @return list 奖项表格行
    """
    rows = []
    for index in range(1, 13):
        amount = data.get(f"p{index}_amount")
        count = data.get(f"p{index}_count")
        total_amount = data.get(f"p{index}_total_amount")
        content = data.get(f"p{index}_content") or data.get(f"p{index}_amount_remark")
        if amount or count or total_amount or content:
            rows.append([f"{index}等奖", amount or "-", count or "-", total_amount or "-", truncate(content, 40)])
    return rows


def print_detail_result(data: dict[str, Any]) -> None:
    """
    功能说明：
    1. 输出指定彩种指定期号的开奖详情。
    2. 先展示期号、日期、开奖号码、销售额、奖池、总奖金额。
    3. 再按奖项输出金额、注数、总金额和补充说明。

    @param data 开奖详情数据
    @return void
    """
    print(f"  期号:     {data.get('sn') or '-'}")
    print(f"  日期:     {data.get('date') or '-'} 星期{data.get('week') or '-'}")
    print(f"  开奖号码: {data.get('number') or '-'}")
    print(f"  销售额:   {data.get('sales') or '-'}")
    print(f"  奖池金额: {data.get('poolmoney') or '-'}")
    print(f"  总奖金额: {data.get('total_amount') or '-'}")
    prize_rows = collect_prize_rows(data)
    if prize_rows:
        print("\n  奖项明细:\n")
        print_table(["奖项", "单注奖金", "注数", "总金额", "说明"], prize_rows)
    if data.get("details_link"):
        print(f"\n  开奖公告: {data.get('details_link')}")
    if data.get("video_link"):
        print(f"  开奖视频: {data.get('video_link')}")


def print_number_history_result(data: dict[str, Any]) -> None:
    """
    功能说明：
    1. 输出三位开奖号码历史出现记录。
    2. 展示号码、历史出现次数和每期开奖期号。
    3. 历史列表按接口返回顺序展示。

    @param data 历史号码数据
    @return void
    """
    print(f"  开奖号码: {data.get('number') or '-'}")
    print(f"  出现次数: {data.get('frequency') or 0}")
    rows = []
    for item in data.get("history_list") or []:
        rows.append([item.get("sn"), item.get("date"), item.get("week")])
    if rows:
        print("\n  历史开奖列表:\n")
        print_table(["期号", "开奖日期", "星期"], rows)


def print_number_stat_result(data: dict[str, Any]) -> None:
    """
    功能说明：
    1. 输出三位型彩票冷热号统计。
    2. 展示最高、最低、平均历史开出次数。
    3. 分别输出冷门号码和热门号码列表。

    @param data 冷热号统计数据
    @return void
    """
    print(f"  最高开出次数: {data.get('max_frequency') or '-'}")
    print(f"  最低开出次数: {data.get('min_frequency') or '-'}")
    print(f"  平均开出次数: {data.get('avg_frequency') or '-'}")
    cold_rows = [[item.get("number"), item.get("frequency")] for item in data.get("cold_number") or []]
    hot_rows = [[item.get("number"), item.get("frequency")] for item in data.get("hot_number") or []]
    if hot_rows:
        print("\n  热门号码:\n")
        print_table(["号码", "历史开出次数"], hot_rows)
    if cold_rows:
        print("\n  冷门号码:\n")
        print_table(["号码", "历史开出次数"], cold_rows)


def print_text_result(command: str, payload: dict[str, Any]) -> int:
    """
    功能说明：
    1. 根据彩票子命令输出查询结果。
    2. 成功时调用对应的格式化输出方法。
    3. 失败时展示接口 message。
    4. 所有文本输出末尾提示仅供开奖数据查询，不构成投注建议。

    @param command 子命令名称
    @param payload 接口返回数据
    @return int 进程退出码
    """
    if int(payload.get("code", 0) or 0) != 200:
        print("\n彩票查询失败\n")
        print(f"  原因: {payload.get('message') or '查询失败'}")
        return 2

    print("\n彩票查询结果\n")
    data = payload.get("data") or ([] if command == "latest" else {})
    if command == "latest":
        print_latest_result(data)
    elif command == "detail":
        print_detail_result(data)
    elif command == "number-history":
        print_number_history_result(data)
    else:
        print_number_stat_result(data)
    print("\n  提示: 结果仅用于开奖数据查询，不构成投注建议。")
    return 0


def main() -> int:
    """
    功能说明：
    1. 解析命令行参数并校验业务参数。
    2. 读取 AppKey 后请求对应彩票接口。
    3. 根据 `--json` 决定输出接口原始 JSON 或格式化文本。

    @return int 进程退出码
    """
    args = parse_args(sys.argv[1:])
    try:
        params = build_params(args)
    except ValueError as exc:
        print(f"错误: {exc}")
        return 1
    appkey = load_appkey(args.cli_key)
    if not appkey:
        print("错误: 未找到 AppKey，请先配置环境变量 JIKE_CAIPIAO_LOTTERY_QUERY_KEY 或 JIKE_APPKEY")
        print(f"申请和查看 AppKey: {REGISTER_URL}")
        return 1
    payload = request_api(args.command, params, appkey)
    if args.json_output:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 0 if int(payload.get("code", 0) or 0) == 200 else 2
    return print_text_result(args.command, payload)


if __name__ == "__main__":
    raise SystemExit(main())
