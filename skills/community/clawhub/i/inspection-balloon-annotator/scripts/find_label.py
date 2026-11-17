# -*- coding: utf-8 -*-
"""查标注文字坐标。用法: python find_label.py <labels.json> <关键词或正则> [--limit 15]
示例: python find_label.py labels.json "70.8"
打印匹配项的中心坐标(x,y)、文字、置信度, 方便手工建立 targets.json。
"""
import argparse, json, re, sys


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("labels"); ap.add_argument("pattern")
    ap.add_argument("--limit", type=int, default=15)
    a = ap.parse_args()
    d = json.load(open(a.labels, encoding="utf-8"))
    pat = re.compile(a.pattern)
    hits = [L for L in d["labels"] if pat.search(L["text"])]
    print(f'image_size={d.get("image_size")}  matches={len(hits)}')
    for L in hits[:a.limit]:
        print(f'  x={L["x"]:>7} y={L["y"]:>7}  w={L["w"]:>5} h={L["h"]:>5} '
              f'conf={L["conf"]}  ori={L["ori"]}  "{L["text"]}"')


if __name__ == "__main__":
    main()
