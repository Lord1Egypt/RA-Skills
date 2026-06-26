#!/usr/bin/env python3
"""梅花易数起卦 — 交互模式或命令行模式
用法:
  交互: python3 scripts/gua.py
  命令行: python3 scripts/gua.py <上卦> <下卦>
"""
import json
import os
import sys
from datetime import datetime

TABLE = [
    [],
    ["", "乾卦", "夬卦", "大有卦", "大壮卦", "小畜卦", "需卦",  "大畜卦", "泰卦"],
    ["", "履卦", "兑卦", "睽卦",   "归妹卦", "中孚卦", "节卦",  "损卦",   "临卦"],
    ["", "同人卦","革卦", "离卦",   "丰卦",   "家人卦", "既济卦","贲卦",   "明夷卦"],
    ["", "无妄卦","随卦", "噬嗑卦", "震卦",   "益卦",   "屯卦",  "颐卦",   "复卦"],
    ["", "姤卦", "大过卦","鼎卦",   "恒卦",   "巽卦",   "井卦",  "蛊卦",   "升卦"],
    ["", "讼卦", "困卦",  "未济卦", "解卦",   "涣卦",   "坎卦",  "蒙卦",   "师卦"],
    ["", "遁卦", "咸卦",  "旅卦",   "小过卦", "渐卦",   "蹇卦",  "艮卦",   "谦卦"],
    ["", "否卦", "萃卦",  "晋卦",   "豫卦",   "观卦",   "比卦",  "剥卦",   "坤卦"],
]

GUA_MAP = {1:"乾", 2:"兑", 3:"离", 4:"震", 5:"巽", 6:"坎", 7:"艮", 8:"坤"}
YAO_MAP = {1:"初爻", 2:"二爻", 3:"三爻", 4:"四爻", 5:"五爻", 6:"上爻"}

GUAS_JSON = os.path.join(os.path.dirname(__file__), "../references/guas.json")


def get_order(hour):
    thresholds = [1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23]
    for i, t in enumerate(thresholds):
        if hour < t:
            return i + 1
    return 1

def normalize(n):
    return 8 if n % 8 == 0 else n % 8

def get_yao(total):
    r = total % 6
    return YAO_MAP[6 if r == 0 else r]

def load_guas():
    with open(GUAS_JSON, encoding="utf-8") as f:
        return json.load(f)

def calc(up, down):
    hour = datetime.now().hour
    order = get_order(hour)
    up_idx, down_idx = normalize(up), normalize(down)
    yao_total = order + up_idx + down_idx
    gua_name = TABLE[down_idx][up_idx]
    guas = load_guas()
    url = guas.get(gua_name, "")
    return {
        "time": datetime.now().strftime("%H:%M:%S"),
        "order": order,
        "up_name": GUA_MAP[up_idx],
        "down_name": GUA_MAP[down_idx],
        "yao": get_yao(yao_total),
        "gua_name": gua_name,
        "url": url,
    }

def print_result(r, up, down):
    print(f"\n当前时间: {r['time']}  时序: {r['order']}")
    print(f"上卦: {r['up_name']}({up})  下卦: {r['down_name']}({down})")
    print(f"动爻: {r['yao']}")
    print(f"卦名: {r['gua_name']}")
    if r["url"]:
        print(f"详解: {r['url']}")

def read_gua(label):
    hint = "  ".join(f"{v}:{k}" for k, v in GUA_MAP.items())
    while True:
        raw = input(f"{label} ({hint}): ").strip()
        try:
            n = int(raw)
            if 1 <= n <= 64:
                return n
        except ValueError:
            pass
        print("  请输入 1~64 之间的整数")

def main():
    if len(sys.argv) == 3:
        try:
            up, down = int(sys.argv[1]), int(sys.argv[2])
        except ValueError:
            print("参数错误，用法: python3 scripts/gua.py <上卦> <下卦>")
            sys.exit(1)
    elif len(sys.argv) == 2:
        parts = sys.argv[1].split()
        if len(parts) != 2:
            print("参数错误，用法: python3 scripts/gua.py <上卦> <下卦>")
            sys.exit(1)
        try:
            up, down = int(parts[0]), int(parts[1])
        except ValueError:
            print("参数错误：上卦和下卦必须为整数")
            sys.exit(1)
    else:
        print("=== 梅花易数起卦 ===\n")
        up   = read_gua("上卦")
        down = read_gua("下卦")

    print_result(calc(up, down), up, down)

if __name__ == "__main__":
    main()
