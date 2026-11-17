#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎁 刷牙俠貼紙收集 — 虛擬貼紙系統

每完成一次刷牙 = 獲得 1 張隨機刷牙俠貼紙（文字藝術，不用圖片）。
集滿 7 張 = 給爸媽的獎勵提示（不是自動化獎勵）。

資料檔：~/.bookshelf-plus/kids/brushing_stickers.json

用法：
    python3 brushing_reward.py --award 小寶   # 發一張貼紙
    python3 brushing_reward.py --list         # 看收集進度
    python3 brushing_reward.py --status       # 里程碑狀態
    python3 brushing_reward.py --hints        # 爸媽獎勵建議
"""

import datetime as dt
import json
import os
import random
import sys

DATA_DIR = os.path.expanduser("~/.bookshelf-plus/kids")
STICKER_FILE = os.path.join(DATA_DIR, "brushing_stickers.json")

# 20+ 款刷牙俠角色表情貼紙（文字藝術）
STICKERS = [
    {"id": 1, "name": "小白眨眨眼", "art": "🐰✨ 小白對你眨眨眼！\n ˶ᵔ ᵕ ᵔ˶"},
    {"id": 2, "name": "亮晶晶牙齒", "art": "🦷⭐ 每顆牙齒都在發光！\n ✨✦✨✦✨"},
    {"id": 3, "name": "彩虹泡泡", "art": "🫧🌈 刷牙泡泡變成彩虹！\n 🫧🫧🫧🫧🫧"},
    {"id": 4, "name": "星星閃閃", "art": "⭐🌟 你是最亮的小星星！\n ✨ ·:*¨¨*:· ✨"},
    {"id": 5, "name": "月亮晚安", "art": "🌙💤 刷完牙，月亮陪你睡！\n 🌙·˚ ˚·🌙"},
    {"id": 6, "name": "太陽早安", "art": "☀️😃 早安！牙齒亮得像太陽！\n ☀️☀️☀️☀️☀️"},
    {"id": 7, "name": "刷刷超人", "art": "💪🦸 刷刷超人出動！\n 卍 卍 卍"},
    {"id": 8, "name": "刷牙小舞者", "art": "💃🎵 邊刷邊跳舞！\n ♪ ♫ ♬ ♩ ♪"},
    {"id": 9, "name": "泡泡噴射器", "art": "🫧🚀 泡泡火箭發射！\n 💨💨💨💨💨"},
    {"id": 10, "name": "勝利小旗", "art": "🏁🎉 刷完啦！揮揮小旗！\n 🏁 🏁 🏁 🏁"},
    {"id": 11, "name": "愛心滿滿", "art": "❤️🥰 小白送你一顆大愛心！\n ❤️❤️❤️❤️❤️"},
    {"id": 12, "name": "恐龍亮亮", "art": "🦕✨ 小恐龍亮亮也說讚！\n 🦕˶ᵔ ᵕ ᵔ˶🦕"},
    {"id": 13, "name": "太空任務", "art": "🚀🌌 太空刷牙任務成功！\n ✨·˚ ˚·✨"},
    {"id": 14, "name": "鈴鐺叮噹", "art": "🔔🎶 牙齒唱歌叮叮咚！\n 🔔·♪·🔔·♪·🔔"},
    {"id": 15, "name": "小花朵朵", "art": "🌸🌼 刷牙開出小花朵！\n 🌸·🌼·🌸·🌼"},
    {"id": 16, "name": "糖果掰掰", "art": "🍬👋 糖果說明天見！\n 🍬👋🍬👋🍬"},
    {"id": 17, "name": "笑一個", "art": "😁🦷 露出亮晶晶的笑容！\n (◕‿◕)✨"},
    {"id": 18, "name": "超人披風", "art": "🦸♂️💫 小白飛過天空！\n 〜〜〜〜〜"},
    {"id": 19, "name": "小星星收集家", "art": "🌟🧺 收集好多小星星！\n 🌟·🌟·🌟·🌟"},
    {"id": 20, "name": "刷牙節奏王", "art": "🥁🎶 咚咚咚！刷牙節奏王！\n 🥁·♪·🥁·♪·🥁"},
    {"id": 21, "name": "小白兔跳跳", "art": "🐰🏃 小白開心跳跳跳！\n ˶ᵔ ᵕ ᵔ˶ ˶ᵔ ᵕ ᵔ˶"},
    {"id": 22, "name": "牙膏冰淇淋", "art": "🍦🦷 薄荷口味最清爽！\n ❄️❄️❄️❄️❄️"},
    {"id": 23, "name": "金幣閃亮", "art": "🪙✨ 刷牙金幣 +1！\n ✨🪙✨🪙✨"},
    {"id": 24, "name": "冠軍獎盃", "art": "🏆🎊 今日刷牙冠軍就是你！\n 🎊·🏆·🎊"},
]

# 集滿 7 張時給爸媽的獎勵建議（提示，非自動化）
PARENT_HINTS = [
    "🎁 集滿 7 張貼紙的獎勵建議（由爸媽決定，不是自動獎勵喔）：",
    "1️⃣ 一起挑一本新繪本，睡前多講 10 分鐘",
    "2️⃣ 帶去公園多玩 30 分鐘",
    "3️⃣ 把 7 張貼紙貼在「刷牙英雄榜」牆上，集滿 3 週換小玩具",
    "4️⃣ 讓寶貝自己選明天的早餐（健康選項內）",
    "5️⃣ 全家一起拍一張「亮晶晶牙齒」合照",
]


def _ensure():
    os.makedirs(DATA_DIR, exist_ok=True)


def load_store():
    _ensure()
    if not os.path.exists(STICKER_FILE):
        return {"stickers": [], "awarded": 0}
    try:
        with open(STICKER_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, dict):
            data.setdefault("stickers", [])
            data.setdefault("awarded", len(data["stickers"]))
            return data
        return {"stickers": [], "awarded": 0}
    except Exception:
        return {"stickers": [], "awarded": 0}


def save_store(store):
    _ensure()
    tmp = STICKER_FILE + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(store, f, ensure_ascii=False, indent=2)
    os.replace(tmp, STICKER_FILE)


def award_sticker(who="寶貝", date=None, sticker_id=None):
    """完成一次刷牙 → 獲得 1 張隨機貼紙。回傳貼紙資料。"""
    store = load_store()
    date = date or dt.date.today().isoformat()
    if sticker_id:
        s = next((x for x in STICKERS if x["id"] == sticker_id), None) or random.choice(STICKERS)
    else:
        s = random.choice(STICKERS)
    entry = {
        "date": date,
        "who": who,
        "sticker_id": s["id"],
        "name": s["name"],
        "art": s["art"],
    }
    store["stickers"].append(entry)
    store["awarded"] = len(store["stickers"])
    save_store(store)
    return entry


def collection(who=None):
    store = load_store()
    if who:
        return [e for e in store["stickers"] if e.get("who") == who]
    return store["stickers"]


def awarded_count():
    return len(collection())


def milestone_text(total=None, short=False):
    """里程碑提醒：集滿 7 張 = 爸媽獎勵提示；差 1-3 張給加油。"""
    total = awarded_count() if total is None else total
    toward = total % 7
    remaining = 7 - toward
    if total > 0 and toward == 0:
        return "🎉 集滿 7 張貼紙！爸媽可以給寶貝一個小獎勵喔！"
    if remaining <= 3:
        return f"💪 再刷 {remaining} 天就可以集滿一週 7 張貼紙了！"
    return "✨ 貼紙越蒐越多，小白為你加油！"


def status_text(who=None):
    total = awarded_count()
    toward = total % 7
    text = f"🎁 目前共收集 {total} 張刷牙俠貼紙，這週進度 {toward}/7。"
    if total > 0 and toward == 0:
        text += " 這一週集滿啦！" + milestone_text(total)
    else:
        text += " " + milestone_text(total)
    return text


if __name__ == "__main__":
    args = sys.argv[1:]
    if args and args[0] == "--award":
        who = args[1] if len(args) > 1 else "寶貝"
        st = award_sticker(who=who)
        print(f"🎁 {who} 獲得貼紙：{st['name']}")
        print(st["art"])
        print(milestone_text())
    elif args and args[0] == "--list":
        cols = collection()
        if not cols:
            print("📭 還沒有貼紙，快去刷一次牙吧！")
        else:
            print(f"📚 目前收集 {len(cols)} 張：")
            for e in cols:
                print(f"  [{e['date']}] {e['name']}（{e['who']}）")
    elif args and args[0] == "--status":
        print(status_text())
    elif args and args[0] == "--hints":
        print("\n".join(PARENT_HINTS))
    else:
        print(__doc__.strip())
