# -*- coding: utf-8 -*-
"""
lottery_core.py — 中国福利彩票 / 体育彩票 通用核心模块

提供:
  - GAME_CONFIG: 各彩种玩法配置(号码池、开奖时间、类型)
  - load_normalized(path): 读取归一化数据(JSON/CSV) -> records
  - 组合数 / 超几何分布 等数学辅助函数

归一化数据格式 (JSON):
{
  "game": "ssq",
  "source": "opencai",
  "records": [
     {"issue": "2024085", "date": "2024-07-28", "pools": {"red": [1,2,3,4,5,6], "blue": [9]}},
     ...
  ]
}
单池彩种使用 {"pools": {"main": [..]}}。
"""

import json
import csv
import math
import os
import sys

# ---------------------------------------------------------------------------
# 彩种配置
# kind: "dual" 多池(红蓝/前后/主特别) ; "single" 单池(数字型/快乐8)
# pools: 每个号码池的 min/max/count
# ---------------------------------------------------------------------------
GAME_CONFIG = {
    "ssq": {
        "name": "双色球", "org": "福彩", "kind": "dual",
        "draw": "每周二、四、日 21:15",
        "pools": {"red": {"min": 1, "max": 33, "count": 6},
                  "blue": {"min": 1, "max": 16, "count": 1}},
        "ticket": 2, "payout_ratio": 0.50,
    },
    "dlt": {
        "name": "大乐透", "org": "体彩", "kind": "dual",
        "draw": "每周一、三、六 21:25",
        "pools": {"front": {"min": 1, "max": 35, "count": 5},
                  "back": {"min": 1, "max": 12, "count": 2}},
        "ticket": 2, "payout_ratio": 0.50,
    },
    "qlc": {
        "name": "七乐彩", "org": "福彩", "kind": "dual",
        "draw": "每周一、三、五 21:30",
        "pools": {"main": {"min": 1, "max": 30, "count": 7},
                  "special": {"min": 1, "max": 30, "count": 1}},
        "ticket": 2, "payout_ratio": 0.50,
    },
    "kl8": {
        "name": "快乐8", "org": "福彩", "kind": "single",
        "draw": "每天 21:30",
        "pools": {"main": {"min": 1, "max": 80, "count": 20}},
        "ticket": 2, "payout_ratio": 0.58,
    },
    "fc3d": {
        "name": "福彩3D", "org": "福彩", "kind": "single",
        "draw": "每天 21:15",
        "pools": {"main": {"min": 0, "max": 9, "count": 3}},
        "ticket": 2, "payout_ratio": 0.53,
    },
    "pl3": {
        "name": "排列3", "org": "体彩", "kind": "single",
        "draw": "每天 21:25",
        "pools": {"main": {"min": 0, "max": 9, "count": 3}},
        "ticket": 2, "payout_ratio": 0.53,
    },
    "pl5": {
        "name": "排列5", "org": "体彩", "kind": "single",
        "draw": "每天 21:25",
        "pools": {"main": {"min": 0, "max": 9, "count": 5}},
        "ticket": 2, "payout_ratio": 0.50,
    },
    "qxc": {
        "name": "七星彩", "org": "体彩", "kind": "single",
        "draw": "每周二、五、日 21:25",
        "pools": {"main": {"min": 0, "max": 9, "count": 7}},
        "ticket": 2, "payout_ratio": 0.50,
    },
}

ALIASES = {
    "双色球": "ssq", "ssq": "ssq",
    "大乐透": "dlt", "dlt": "dlt",
    "七乐彩": "qlc", "qlc": "qlc",
    "快乐8": "kl8", "快乐八": "kl8", "kl8": "kl8",
    "3d": "fc3d", "福彩3d": "fc3d", "fc3d": "fc3d",
    "排列3": "pl3", "排三": "pl3", "pl3": "pl3",
    "排列5": "pl5", "排五": "pl5", "pl5": "pl5",
    "七星彩": "qxc", "qxc": "qxc",
}


def resolve_game(token):
    """将中文名 / 缩写解析为规范 game key。"""
    t = (token or "").strip().lower()
    if t in GAME_CONFIG:
        return t
    if t in ALIASES:
        return ALIASES[t]
    # 容错: 部分输入
    for k, v in ALIASES.items():
        if t and t in k.lower():
            return v
    raise KeyError("未知彩种: %s (支持: %s)" % (token, ", ".join(GAME_CONFIG.keys())))


def combinations(n, k):
    """C(n, k) 组合数。"""
    if k < 0 or k > n:
        return 0
    k = min(k, n - k)
    r = 1
    for i in range(1, k + 1):
        r = r * (n - k + i) // i
    return r


def hypergeom(N, K, n, k):
    """超几何概率: 总体 N, 成功 K, 抽取 n, 抽到 k 个成功的概率。"""
    return combinations(K, k) * combinations(N - K, n - k) / combinations(N, n)


# ---------------------------------------------------------------------------
# 数据加载
# ---------------------------------------------------------------------------
def load_normalized(path):
    """读取归一化数据。支持 .json 与 .csv。返回含 game/records 的 dict。"""
    if not os.path.exists(path):
        raise FileNotFoundError("数据文件不存在: %s" % path)
    ext = os.path.splitext(path)[1].lower()
    if ext == ".json":
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        records = data.get("records", [])
        game = data.get("game")
    elif ext == ".csv":
        records = []
        game = None
        with open(path, "r", encoding="utf-8-sig", newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                rec = {"issue": row.get("issue", ""), "date": row.get("date", "")}
                pools = {}
                if "numbers" in row:
                    pools["main"] = _split_nums(row["numbers"])
                for key in ("red", "blue", "front", "back", "main", "special"):
                    if key in row and row[key]:
                        pools[key] = _split_nums(row[key])
                if not pools and "n1" in row:
                    pools["main"] = [int(row["n%d" % i]) for i in range(1, 9)
                                     if ("n%d" % i) in row and row["n%d" % i]]
                rec["pools"] = pools
                if "game" in row:
                    game = row["game"]
                records.append(rec)
        data = {"game": game, "records": records}
    else:
        raise ValueError("不支持的文件类型: %s (用 .json 或 .csv)" % ext)
    if not records:
        raise ValueError("数据为空: %s" % path)
    return data


def _split_nums(s):
    out = []
    for part in str(s).replace(";", ",").replace("|", ",").split(","):
        part = part.strip()
        if part == "":
            continue
        try:
            out.append(int(part))
        except ValueError:
            continue
    return out


def ensure_sorted_ints(pools, game):
    """将各池号码转为去重排序的 int 列表, 便于统计。"""
    cfg = GAME_CONFIG[game]
    cleaned = {}
    for pname, pconf in cfg["pools"].items():
        nums = sorted(set(int(x) for x in pools.get(pname, [])))
        cleaned[pname] = nums
    return cleaned


if __name__ == "__main__":
    print("支持彩种:", ", ".join("%s(%s)" % (k, GAME_CONFIG[k]["name"]) for k in GAME_CONFIG))
    print("组合数示例: 双色球 =", combinations(33, 6) * 16,
          "  大乐透 =", combinations(35, 5) * combinations(12, 2))
