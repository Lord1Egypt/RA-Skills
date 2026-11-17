#!/usr/bin/env python3
"""topic-factory.py — 心跳主題工廠（2026-08-22 設計）

每晚心跳時，AI諗新主題 → 用呢個 script 合併入 topic-rotation.json：
- 保留 rotation[index:]（未用嘅，buffer 唔浪費）
- 後面接新主題（agent 諗嗰啲）
- 補到 30 條為止（30 定 27 都得，buffer 多少之別）
- index 保持唔郁（仍然指住第一個未用嘅）

用法：
  python3 topic-factory.py show                 # 睇現狀（唔改嘢）
  python3 topic-factory.py refresh --new "主題A" "主題B" ...   # 合併新主題

零雲端、零 LLM：新主題由心跳時嘅 agent（AI）自己諗，script 只做 merge。
"""
import argparse
import datetime
import json
import os

BASE = os.environ.get("IDLE_PING_WS") or os.path.expanduser("~/.openclaw/workspace")
ROTATION = os.path.join(BASE, "curiosity", "topic-rotation.json")
TARGET = 30  # 30 或 27 都得，純粹 buffer 多少


def load():
    try:
        with open(ROTATION) as f:
            return json.load(f)
    except Exception:
        return {"version": 1, "description": "夜晚心跳主題輪換清單", "rotation": [], "index": 0, "updatedAt": ""}


def show():
    cfg = load()
    rotation = cfg.get("rotation", [])
    index = min(cfg.get("index", 0), len(rotation))
    print(f"總數: {len(rotation)}")
    print(f"index: {index}（下一條 = rotation[{index}]）")
    print(f"已用: {index} 條 | 未用: {len(rotation) - index} 條")
    if rotation:
        print("未用清單:")
        for i, t in enumerate(rotation[index:], start=index):
            print(f"  [{i}] {t}")


def refresh(new_topics):
    cfg = load()
    rotation = cfg.get("rotation", [])
    index = min(cfg.get("index", 0), len(rotation))
    unused = rotation[index:]  # 未用嘅保留

    merged = list(unused)
    for t in new_topics:
        t = t.strip()
        if t and t not in merged:
            merged.append(t)
    if len(merged) > TARGET:
        merged = merged[:TARGET]

    cfg["rotation"] = merged
    cfg["index"] = 0  # merged 頭一個 = 未用嘅第一條，crawler 由佢開始用（唔可以保持舊 index，會跳過保留主題）
    cfg["updatedAt"] = datetime.date.today().isoformat()
    tmp = ROTATION + ".tmp"
    with open(tmp, "w") as f:
        json.dump(cfg, f, ensure_ascii=False, indent=2)
    os.replace(tmp, ROTATION)

    print(f"refresh 完成: 保留 {len(unused)} 條未用 + 新加 {len(merged) - len(unused)} 條 → 共 {len(merged)} 條")
    print(f"index: {cfg['index']}（下一條 = rotation[{cfg['index']}]）")
    if len(merged) < TARGET:
        print(f"⚠️ 少過 {TARGET} 條（buffer 唔夠），下次心跳補多啲")
    elif len(unused) >= TARGET:
        print(f"ℹ️ 未用嘅已經有 {TARGET} 條，今次冇加新主題（buffer 滿，正常）")


def main():
    parser = argparse.ArgumentParser(description="心跳主題工廠：保留未用 + 補新主題到 30 條")
    parser.add_argument("action", choices=["show", "refresh"])
    parser.add_argument("--new", nargs="*", default=[], help="新主題（agent 諗嗰啲）")
    args = parser.parse_args()

    if args.action == "show":
        show()
    else:
        refresh(args.new)


if __name__ == "__main__":
    main()
