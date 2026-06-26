"""
lottery-helper/scripts/query.py
查询彩票开奖数据 from 17500.cn
"""
import urllib.request
import sys
import argparse

# 彩种中文名 → (内部代码, 方向)
API_MAP = {
    "双色球": ("ssq", "desc"),
    "大乐透": ("dlt", "desc"),
    "排列三": ("pl3", "desc"),
    "排列五": ("pl5", "desc"),
    "福彩3D": ("3d", "desc"),
    "北京快乐8": ("kl8", "desc"),
    "七乐彩": ("qlc", "desc"),
    "七星彩": ("qxc", "desc"),
}
REVERSE_MAP = {v[0]: k for k, v in API_MAP.items()}

# 内部代码 → API URL 代码（七乐彩/七星彩/3D 特殊）
_API_TO_URL = {"qlc": "7lc", "qxc": "7xc"}


def fetch_raw(code, direction="desc", max_chars=None, n=None):
    url_code = _API_TO_URL.get(code, code)
    url = f"https://data.17500.cn/{url_code}_{direction}.txt"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Accept": "text/plain, */*",
    }
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=20) as r:
        raw = r.read().decode("utf-8")
    lines = raw.strip().split("\n")
    if n is not None:
        lines = lines[:n]
    if max_chars:
        result, chars = [], 0
        for line in lines:
            if chars + len(line) > max_chars:
                break
            result.append(line)
            chars += len(line) + 1
        return result
    return lines


def _prize(parts, idx, label):
    """安全读取奖级字段，不存在或为空时返回None，0也是有效值。"""
    try:
        val = parts[idx].replace(',', '')
        return val if val not in ('-', '') else None
    except (IndexError, AttributeError):
        return None


def parse_line(code, line):
    """
    将一行原始数据解析为结构化字典。
    API 原始字段索引（已实测确认）：
      ssq  : 31字段 [0-30]  一等奖~六等奖+福运奖
      dlt  : 45字段 [0-44]  一等奖~九等奖+追加
      pl3  : 12字段 [0-11]  直选+组三+组六
      pl5  : 10字段 [0-9]   直选
      3d   : 17字段 [0-16]  直选（仅解析到[12]）
      kl8  : 102字段[0-101] 选十~选一各奖级
      qlc  : 26字段 [0-25]  奖池金额+一等奖~七等奖
      qxc  : 23字段 [0-22]  一等奖~六等奖
    """
    parts = line.split()
    if len(parts) < 2:
        return None

    result = {"code": code, "期号": parts[0], "日期": parts[1]}

    # ── 双色球 (31字段) ─────────────────────────────────────────
    # [0]期号 [1]日期 [2-7]红球 [8]蓝球 [9-14]出球顺序
    # [15]投注总额 [16]奖池金额
    # [17]一等奖注数 [18]一等奖金额 [19]二等奖注数 [20]二等奖金额
    # [21]三等奖注数 [22]三等奖金额 [23]四等奖注数 [24]四等奖金额
    # [25]五等奖注数 [26]五等奖金额 [27]六等奖注数 [28]六等奖金额
    # [29]福运奖注数 [30]福运奖金额
    if code == "ssq":
        result["红球"] = parts[2:8]
        result["蓝球"] = [parts[8]]
        result["号码"] = parts[2:8] + [parts[8]]
        if len(parts) > 16:
            result["投注总额"] = parts[15].replace(',', '')
            result["奖池金额"] = parts[16].replace(',', '')
        if len(parts) > 20:
            result["一等奖注数"] = _prize(parts, 17, "一等奖")
            result["一等奖金额"] = _prize(parts, 18, "一等奖")
            result["二等奖注数"] = _prize(parts, 19, "二等奖")
            result["二等奖金额"] = _prize(parts, 20, "二等奖")
        if len(parts) > 22:
            result["三等奖注数"] = _prize(parts, 21, "三等奖")
            result["三等奖金额"] = _prize(parts, 22, "三等奖")
            result["四等奖注数"] = _prize(parts, 23, "四等奖")
            result["四等奖金额"] = _prize(parts, 24, "四等奖")
            result["五等奖注数"] = _prize(parts, 25, "五等奖")
            result["五等奖金额"] = _prize(parts, 26, "五等奖")
            result["六等奖注数"] = _prize(parts, 27, "六等奖")
            result["六等奖金额"] = _prize(parts, 28, "六等奖")
            result["福运奖注数"] = _prize(parts, 29, "福运奖")
            result["福运奖金额"] = _prize(parts, 30, "福运奖")

    # ── 大乐透 (45字段) ─────────────────────────────────────────
    # [0]期号 [1]日期 [2-6]前区 [7-8]后区 [9-15]出球顺序(7个)
    # [16]投注总额 [17]奖池金额
    # [18]一等奖注数 [19]一等奖金额 [20]二等奖注数 [21]二等奖金额
    # [22]三等奖注数 [23]三等奖金额 [24]四等奖注数 [25]四等奖金额
    # [26]五等奖注数 [27]五等奖金额 [28]六等奖注数 [29]六等奖金额
    # [30]七等奖注数 [31]七等奖金额 [32]八等奖注数 [33]八等奖金额
    # [34]九等奖注数 [35]九等奖金额
    # [36-37]追加一等奖注数/金额 [38-39]追加二等奖 [40-41]追加三等奖
    # [42-43]追加四等奖 [44-45]追加五等奖（注：实际数据到44结束）
    elif code == "dlt":
        result["前区"] = parts[2:7]
        result["后区"] = parts[7:9]
        result["号码"] = parts[2:7] + parts[7:9]
        if len(parts) > 17:
            result["投注总额"] = parts[16].replace(',', '')
            result["奖池金额"] = parts[17].replace(',', '')
        if len(parts) > 21:
            result["一等奖注数"] = _prize(parts, 18, "一等奖")
            result["一等奖金额"] = _prize(parts, 19, "一等奖")
            result["二等奖注数"] = _prize(parts, 20, "二等奖")
            result["二等奖金额"] = _prize(parts, 21, "二等奖")
        if len(parts) > 23:
            result["三等奖注数"] = _prize(parts, 22, "三等奖")
            result["三等奖金额"] = _prize(parts, 23, "三等奖")
            result["四等奖注数"] = _prize(parts, 24, "四等奖")
            result["四等奖金额"] = _prize(parts, 25, "四等奖")
            result["五等奖注数"] = _prize(parts, 26, "五等奖")
            result["五等奖金额"] = _prize(parts, 27, "五等奖")
            result["六等奖注数"] = _prize(parts, 28, "六等奖")
            result["六等奖金额"] = _prize(parts, 29, "六等奖")
            result["七等奖注数"] = _prize(parts, 30, "七等奖")
            result["七等奖金额"] = _prize(parts, 31, "七等奖")
            result["八等奖注数"] = _prize(parts, 32, "八等奖")
            result["八等奖金额"] = _prize(parts, 33, "八等奖")
            result["九等奖注数"] = _prize(parts, 34, "九等奖")
            result["九等奖金额"] = _prize(parts, 35, "九等奖")
        if len(parts) > 37:
            result["追加一等奖注数"] = _prize(parts, 36, "追加一等奖")
            result["追加一等奖金额"] = _prize(parts, 37, "追加一等奖")
            result["追加二等奖注数"] = _prize(parts, 38, "追加二等奖")
            result["追加二等奖金额"] = _prize(parts, 39, "追加二等奖")

    # ── 排列三 (12字段) ─────────────────────────────────────────
    # [0]期号 [1]日期 [2]百 [3]十 [4]个 [5]投注总额
    # [6]直选注数 [7]直选金额 [8]组三注数 [9]组三金额 [10]组六注数 [11]组六金额
    elif code == "pl3":
        result["百"] = parts[2]
        result["十"] = parts[3]
        result["个"] = parts[4]
        result["号码"] = [parts[2], parts[3], parts[4]]
        if len(parts) > 5:
            result["投注总额"] = parts[5].replace(',', '')
            result["直选注数"] = _prize(parts, 6, "直选")
            result["直选金额"] = _prize(parts, 7, "直选")
            result["组三注数"] = _prize(parts, 8, "组三")
            result["组三金额"] = _prize(parts, 9, "组三")
            result["组六注数"] = _prize(parts, 10, "组六")
            result["组六金额"] = _prize(parts, 11, "组六")

    # ── 排列五 (10字段) ─────────────────────────────────────────
    # [0]期号 [1]日期 [2]万 [3]千 [4]百 [5]十 [6]个
    # [7]投注总额 [8]直选注数 [9]直选金额
    elif code == "pl5":
        result["万"] = parts[2]
        result["千"] = parts[3]
        result["百"] = parts[4]
        result["十"] = parts[5]
        result["个"] = parts[6]
        result["号码"] = list(parts[2:7])
        if len(parts) > 8:
            result["投注总额"] = parts[7].replace(',', '')
            result["直选注数"] = _prize(parts, 8, "直选")
            result["直选金额"] = _prize(parts, 9, "直选")

    # ── 福彩3D (17字段，仅解析前13字段) ──────────────────────────
    # [0]期号 [1]日期 [2]百 [3]十 [4]个 [5-9]出球顺序(5个) [10]投注总额
    # [11]直选注数 [12]直选金额 [13-16]组三/组六(省略)
    elif code == "3d":
        result["百"] = parts[2]
        result["十"] = parts[3]
        result["个"] = parts[4]
        result["号码"] = [parts[2], parts[3], parts[4]]
        if len(parts) > 10:
            result["投注总额"] = parts[10].replace(',', '')
            result["直选注数"] = _prize(parts, 11, "直选")
            result["直选金额"] = _prize(parts, 12, "直选")

    # ── 北京快乐8 (102字段) ──────────────────────────────────────
    # [0]期号 [1]日期 [2-21]20个号码 [22]投注总额 [23]奖池金额
    # [24-101] 选十(7对) 选九(7对) 选八(7对) 选七(7对)
    #           选六(6对) 选五(4对)
    elif code == "kl8":
        result["号码"] = parts[2:22]
        # 存为独立键，匹配 export FIELD_DEFS 的"码1"~"码20"
        for i in range(20):
            if 2 + i < len(parts):
                result[f"码{i+1}"] = parts[2 + i]
        if len(parts) > 23:
            result["投注总额"] = parts[22].replace(',', '')
            result["奖池金额"] = parts[23].replace(',', '')
        prize_map = [
            ("选十中十", 24), ("选十中九", 26), ("选十中八", 28),
            ("选十中七", 30), ("选十中六", 32), ("选十中五", 34), ("选十中零", 36),
            ("选九中九", 38), ("选九中八", 40), ("选九中七", 42),
            ("选九中六", 44), ("选九中五", 46), ("选九中四", 48), ("选九中零", 50),
            ("选八中八", 52), ("选八中七", 54), ("选八中六", 56),
            ("选八中五", 58), ("选八中四", 60), ("选八中三", 62), ("选八中零", 64),
            ("选七中七", 66), ("选七中六", 68), ("选七中五", 70),
            ("选七中四", 72), ("选七中三", 74), ("选七中二", 76), ("选七中零", 78),
            ("选六中六", 80), ("选六中五", 82), ("选六中四", 84),
            ("选六中三", 86), ("选六中二", 88), ("选六中一", 90),
            ("选五中五", 92), ("选五中四", 94), ("选五中三", 96),
            ("选五中二", 98), ("选五中一", 100),
        ]
        for name, idx in prize_map:
            if idx + 1 < len(parts):
                a = parts[idx].replace(',', '')
                b = parts[idx + 1].replace(',', '')
                # 只过滤空值和"-"，保留"0"（无人中奖是有效数据）
                result[f"{name}注数"] = a if a not in ('-', '') else None
                result[f"{name}奖金"] = b if b not in ('-', '') else None

    # ── 七乐彩 (26字段) ─────────────────────────────────────────
    # [0]期号 [1]日期 [2-8]基本号(7个) [9]特别码 [10]投注总额
    # [11]奖池金额
    # [12]一等奖注数 [13]一等奖金额
    # [14-15]二等奖注数金额 [16-17]三等奖注数金额 [18-19]四等奖注数金额
    # [20-21]五等奖注数金额 [22-23]六等奖注数金额 [24-25]七等奖注数金额
    elif code == "qlc":
        result["基本号"] = parts[2:9]
        result["特别码"] = parts[9]
        result["号码"] = parts[2:9] + [parts[9]]
        if len(parts) > 10:
            result["投注总额"] = parts[10].replace(',', '')
        if len(parts) > 11:
            result["奖池金额"] = parts[11].replace(',', '')
        if len(parts) > 13:
            result["一等奖注数"] = _prize(parts, 12, "一等奖")
            result["一等奖金额"] = _prize(parts, 13, "一等奖")
        # 二等奖~七等奖（注数金额交替）
        prize_map = [
            ("二等奖", 14, 15), ("三等奖", 16, 17), ("四等奖", 18, 19),
            ("五等奖", 20, 21), ("六等奖", 22, 23), ("七等奖", 24, 25),
        ]
        for name, i_cnt, i_amt in prize_map:
            if len(parts) > i_amt:
                result[f"{name}注数"] = _prize(parts, i_cnt, name)
                result[f"{name}金额"] = _prize(parts, i_amt, name)

    # ── 七星彩 (23字段) ─────────────────────────────────────────
    # 实测数据结构（从索引11开始）：
    # [11-12]一等奖注数金额 [13-14]二等奖注数金额 [15-16]三等奖注数金额
    # [17-18]四等奖注数金额 [19-20]五等奖注数金额 [21-22]六等奖注数金额
    # 注：API只返回23字段，无七等奖八等奖数据
    elif code == "qxc":
        result["号码"] = parts[2:9]
        result["位"] = parts[2:9]
        if len(parts) > 10:
            result["投注总额"] = parts[9].replace(',', '')
            result["奖池金额"] = parts[10].replace(',', '')
        prize_map = [
            ("一等奖", 11, 12), ("二等奖", 13, 14), ("三等奖", 15, 16),
            ("四等奖", 17, 18), ("五等奖", 19, 20), ("六等奖", 21, 22),
        ]
        for name, i_cnt, i_amt in prize_map:
            if len(parts) > i_amt:
                result[f"{name}注数"] = _prize(parts, i_cnt, name)
                result[f"{name}金额"] = _prize(parts, i_amt, name)

    return result


def format_draw(code, parsed):
    period = parsed.get("期号", "?")
    date = parsed.get("日期", "?")
    nums = parsed.get("号码", [])

    if code == "ssq":
        return f"{period} | {date} | 红球: {' '.join(parsed.get('红球', []))} | 蓝球: {parsed.get('蓝球', ['?'])[0]}"
    elif code == "dlt":
        return f"{period} | {date} | 前区: {' '.join(parsed.get('前区', []))} | 后区: {' '.join(parsed.get('后区', []))}"
    elif code in ("pl3", "3d"):
        return f"{period} | {date} | 开奖: {''.join(nums)}"
    elif code == "pl5":
        return f"{period} | {date} | 开奖: {''.join(nums)}"
    elif code == "kl8":
        return f"{period} | {date} | 20码: {' '.join(nums)}"
    elif code == "qlc":
        return f"{period} | {date} | 基本号: {' '.join(parsed.get('基本号', []))} | 特别码: {parsed.get('特别码', '?')}"
    elif code == "qxc":
        return f"{period} | {date} | 7位: {''.join(nums)}"
    return f"{period} | {date} | {nums}"


def get_latest(queries, n_each=1):
    results = {}
    for name, n in queries.items():
        if name not in API_MAP:
            print(f"[WARN] 未知彩种: {name}", file=sys.stderr)
            continue
        code, _ = API_MAP[name]
        try:
            lines = fetch_raw(code, "desc", n=n)
        except Exception as e:
            print(f"[ERROR] 获取{name}({code})失败: {e}", file=sys.stderr)
            continue
        records = []
        for line in lines:
            if not line.strip():
                continue
            parsed = parse_line(code, line)
            fmt = format_draw(code, parsed)
            records.append({"raw": line, "parsed": parsed, "formatted": fmt})
        results[name] = records
    return results


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="彩票开奖查询")
    parser.add_argument("--codes", default="双色球,大乐透",
                        help="彩种名称，逗号分隔")
    parser.add_argument("--periods", type=int, default=1, help="每种查询最近几期")
    args = parser.parse_args()
    queries = {}
    for name in args.codes.split(","):
        name = name.strip()
        # 支持内部代码（ssq/fc3d/kl8 等）自动转换为中文名
        if name in REVERSE_MAP:
            name = REVERSE_MAP[name]
        queries[name] = args.periods
    res = get_latest(queries)
    for name, records in res.items():
        for rec in records:
            print(f"[{name}] {rec['formatted']}")
