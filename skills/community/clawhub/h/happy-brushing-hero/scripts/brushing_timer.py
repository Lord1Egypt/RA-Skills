#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🦷 快樂刷牙俠 — 互動式刷牙計時器（核心）

讓 2-6 歲孩子開心刷滿 2 分鐘的歡樂計時器：
- 大字彩色倒數（MM:SS）
- 每 30 秒輪播小鼓勵語（小白兔「小白」陪你刷）
- 三種模式：標準 / 故事 / 音樂
- 完成後：煙火慶祝 + 大聲祝賀 + 打卡 + 當日貼紙

用法：
    python3 brushing_timer.py                 # 標準模式，2 分鐘
    python3 brushing_timer.py --mode B        # 故事模式（刷牙聽故事）
    python3 brushing_timer.py --mode C        # 音樂模式（節奏刷刷刷）
    python3 brushing_timer.py --minutes 1     # 只刷 1 分鐘
    python3 brushing_timer.py --who 小寶      # 指定刷牙的小朋友
    python3 brushing_timer.py --tts           # 只輸出 TTS 朗讀文字（給 OpenClaw tts tool）
    python3 brushing_timer.py --test          # 測試模式（5 秒，不寫記錄）

風格紅線：超級正向歡樂、零責怪，絕不說「不刷牙會蛀牙」之類的威脅語。
"""

import argparse
import os
import random
import shutil
import subprocess
import sys
import threading
import time

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)

try:
    import brushing_tracker as tracker
    import brushing_reward as reward
except Exception:
    # 獨立執行時不強制依賴打卡/貼紙模組
    tracker = None
    reward = None

# ---------------- 色彩 ----------------
RESET = "\033[0m"
BOLD = "\033[1m"
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
MAGENTA = "\033[35m"
CYAN = "\033[36m"
WHITE = "\033[37m"
RAINBOW = [RED, YELLOW, GREEN, CYAN, BLUE, MAGENTA]


def paint(text, color=BOLD + WHITE):
    """包上 ANSI 顏色（純 TTS 模式不用）。"""
    return f"{color}{text}{RESET}"


def rainbow(text):
    return "".join(RAINBOW[i % len(RAINBOW)] + ch + RESET for i, ch in enumerate(text))


# ---------------- 大字倒數 ----------------
DIGITS = {
    "0": ["███", "█ █", "█ █", "█ █", "███"],
    "1": [" █ ", "██ ", " █ ", " █ ", "███"],
    "2": ["███", "  █", "███", "█  ", "███"],
    "3": ["███", "  █", "███", "  █", "███"],
    "4": ["█ █", "█ █", "███", "  █", "  █"],
    "5": ["███", "█  ", "███", "  █", "███"],
    "6": ["███", "█  ", "███", "█ █", "███"],
    "7": ["███", "  █", "  █", "  █", "  █"],
    "8": ["███", "█ █", "███", "█ █", "███"],
    "9": ["███", "█ █", "███", "  █", "███"],
    ":": ["   ", " █ ", "   ", " █ ", "   "],
}


def big_time(total_seconds):
    """把剩餘秒數渲染成 5 行大字（MM:SS），彩虹色。"""
    total_seconds = max(0, int(total_seconds))
    m, s = divmod(total_seconds, 60)
    text = f"{m:02d}:{s:02d}"
    rows = [""] * 5
    for i, ch in enumerate(text):
        color = RAINBOW[i % len(RAINBOW)]
        for r in range(5):
            rows[r] += color + DIGITS[ch][r] + RESET + " "
    return rows


def progress_bar(ratio, width=22):
    """進度條 + 表情符號。"""
    ratio = max(0.0, min(1.0, ratio))
    if ratio >= 1.0:
        return paint("🥳 刷 完 啦 ！ 超 級 棒 ！ 🥳", YELLOW)
    filled = int(ratio * width)
    bar = "█" * filled + "░" * (width - filled)
    if ratio < 0.25:
        face = "🐰"
    elif ratio < 0.5:
        face = "😊"
    elif ratio < 0.75:
        face = "😄"
    else:
        face = "🤩"
    return f"{face} [{paint(bar, GREEN)}] {int(ratio * 100)}%"


# ---------------- 小白的鼓勵語（每 30 秒輪播） ----------------
ENCOURAGEMENTS = [
    "很棒喔！上排牙齒刷乾淨了！✨",
    "下排牙齒也要刷到喔～ 🦷",
    "快完成了！最後刷刷舌頭～ 👅",
    "太厲害了！牙齒亮晶晶！⭐",
]

# ---------------- 故事模式：短篇故事 ----------------
STORIES = {
    "小白兔刷牙大冒險": [
        "從前從前，有一隻最愛刷牙的小白兔，名字叫做小白。小白每天起床第一件事，就是拿起小牙刷，對著鏡子大喊：「刷刷刷，牙齒我最愛！」✨",
        "這天早上，小白發現牙刷上有魔法泡泡！每一顆泡泡裡都住著一顆亮晶晶的小星星。小白刷一刷，星星就跳出來跳舞！⭐🕺",
        "刷刷上排牙齒，咕嚕咕嚕～泡泡變成彩虹橋！刷刷下排牙齒，咕嚕咕嚕～泡泡變成小汽車！小白笑得眼睛瞇成一條線！🌈",
        "最後，小白漱漱口，對著鏡子張開嘴巴：「啊～～」哇！每一顆牙齒都亮得像小燈泡！小白說：刷牙真是太好玩了，明天還要刷！🦷💡",
    ],
    "太空牙刷任務": [
        "今天晚上，小白要執行史上最酷的任務：太空刷牙任務！小白坐上牙刷火箭，咻——！飛到牙齒星球！🚀🦷",
        "牙齒星球上，住著好多好多髒髒的細菌怪獸！小白拿起泡泡槍，咕嚕咕嚕——泡泡把細菌怪獸通通包起來！🫧👾",
        "上排牙齒是高山，下排牙齒是山洞。小白左刷刷、右刷刷，把高山山洞都刷得亮晶晶！✨⛰️",
        "任務完成！小白對著鏡子比出勝利手勢：耶！牙齒星球得救了！回家睡覺前，小白說：明天還要再來刷牙！🌙💪",
    ],
    "小恐龍的亮晶晶牙齒": [
        "有一隻小恐龍，名字叫亮亮。亮亮最喜歡吃水果和點心，可是他不喜歡刷牙，牙齒變得黃黃的。🦕🍎",
        "有一天，亮亮碰到小白兔小白。小白說：「我教你一個魔法！刷牙的時候，牙齒會唱歌喔！」亮亮好好奇！🎵",
        "亮亮拿起牙刷，刷刷刷——哇！牙齒真的唱歌了！叮叮咚咚，像小鈴鐺一樣！亮亮開心極了！🔔🦷",
        "從那天起，亮亮每天刷牙，牙齒變得又白又亮，笑起來像一顆小太陽！小朋友，你也一起來刷吧！☀️😁",
    ],
}


def story_generator(title=None, part=None):
    """故事產生器：回傳 (故事名, 故事章節串列) 或指定章節文字。

    title: 故事名稱（模糊比對）；part: 章節編號（0 起）。都省略時隨機選故事。
    """
    if title:
        for key in STORIES:
            if title in key or key in title:
                story = STORIES[key]
                title = key
                break
        else:
            title = random.choice(list(STORIES.keys()))
            story = STORIES[title]
    else:
        title = random.choice(list(STORIES.keys()))
        story = STORIES[title]
    if part is not None:
        return title, story[part % len(story)]
    return title, story


# ---------------- 語音（macOS say，非阻塞） ----------------
def say_available():
    return sys.platform == "darwin" and shutil.which("say") is not None


def speak(text, rate=200):
    """用 macOS say 即時朗讀，不阻塞計時（fire-and-forget）。"""
    if not say_available():
        return
    try:
        subprocess.Popen(
            ["say", "-r", str(rate), text],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    except Exception:
        pass


# ---------------- 非阻塞按鍵（q = 提早結束） ----------------
def _read_key():
    if not sys.stdin.isatty():
        return None
    try:
        import select
        import termios
        import tty

        fd = sys.stdin.fileno()
        old = termios.tcgetattr(fd)
        try:
            tty.setcbreak(fd)
            if select.select([sys.stdin], [], [], 0)[0]:
                return sys.stdin.read(1)
            return None
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old)
    except Exception:
        return None


# ---------------- 畫面 ----------------
def clear_screen():
    if sys.stdout.isatty():
        print("\033[H\033[J", end="")
    else:
        print("\n" + "─" * 48)


def countdown_3_2_1():
    for n in ("3", "2", "1"):
        clear_screen()
        print()
        for row in DIGITS[n]:
            print(paint(row, YELLOW))
        print()
        time.sleep(0.6)
    clear_screen()


def beat_line(now_ts):
    """音樂模式的跳動音符列。"""
    notes = ["♪", "♫", "♬", "♩"]
    idx = int(now_ts * 3)
    return " ".join(
        RAINBOW[(idx + j) % len(RAINBOW)] + notes[(idx + j) % len(notes)] + RESET
        for j in range(6)
    )


# ---------------- 事件列（供主畫面重繪，避免被清屏吃掉） ----------------
_EVENTS = []
_EVENTS_LOCK = threading.Lock()


def add_event(text):
    with _EVENTS_LOCK:
        _EVENTS.append(text)
        if len(_EVENTS) > 3:
            del _EVENTS[0]


def get_events():
    with _EVENTS_LOCK:
        return list(_EVENTS)


def render(remaining, elapsed, duration, mode, tts_mode):
    """每秒重繪主畫面（純 TTS 模式不重繪，只靠 worker 出文字）。"""
    if tts_mode:
        return
    clear_screen()
    print(paint("🦷 快樂刷牙俠 · 小白陪你刷牙 🐰", CYAN))
    print()
    for row in big_time(remaining):
        print(row)
    print()
    print(progress_bar(elapsed / duration))
    if mode == "C":
        print(paint("🎵 音樂模式：", YELLOW) + beat_line(time.monotonic()) + paint(" 刷刷刷！", BOLD))
    elif mode == "B":
        print(paint("📖 故事模式：聽故事，刷亮亮！", BLUE))
    else:
        print(paint("✨ 標準模式：跟小白一起刷刷刷！", GREEN))
    for ev in get_events()[-2:]:
        print()
        print(ev)
    print()
    print(paint("（按 q 可提早結束）", CYAN))


# ---------------- 三個 worker 執行緒 ----------------
def encouragement_worker(stop, start, duration, offset, tts_mode, use_say, quick):
    """每 30 秒輪播一句小白的鼓勵語。"""
    if quick:
        marks = [1, 2, 3, 4]
    else:
        marks = list(range(30, int(duration) + 1, 30))
    for i, mark in enumerate(marks):
        if mark > duration:
            break
        if mark >= duration and not quick:
            mark = max(1, duration - 2)  # 最後一響在結束前 2 秒
        remaining = start + mark - time.monotonic()
        if remaining > 0 and stop.wait(remaining):
            return
        line = ENCOURAGEMENTS[(offset + i) % len(ENCOURAGEMENTS)]
        add_event(paint("🐰 小白說：", MAGENTA) + paint(line, BOLD + WHITE))
        if tts_mode:
            print(f"小白說：{line}", flush=True)
        if use_say:
            speak("小白說，" + line, 200)


def story_worker(stop, start, duration, tts_mode, use_say, quick):
    """故事模式：每 30 秒講一段故事（呼叫 story_generator）。"""
    title, story = story_generator()
    add_event(paint(f"📖 故事時間：《{title}》", CYAN))
    if tts_mode:
        print(f"故事時間：{title}", flush=True)
    if use_say:
        speak(f"故事時間，{title}", 190)
    if quick:
        marks = [1, 2, 3, 4]
    else:
        marks = list(range(30, int(duration) + 1, 30))
    for i, mark in enumerate(marks):
        if mark > duration:
            break
        remaining = start + mark - time.monotonic()
        if remaining > 0 and stop.wait(remaining):
            return
        chunk = story[i % len(story)]
        add_event(paint(f"📖 第 {i + 1} 章：", BLUE) + paint(chunk, BOLD + WHITE))
        if tts_mode:
            print(f"第 {i + 1} 章：{chunk}", flush=True)
        if use_say:
            speak(chunk, 190)


def music_worker(stop, duration, tts_mode, use_say, quick):
    """音樂模式：歡快節奏 + 偶爾的小白加油。"""
    cheers = [
        "刷刷刷！牙齒我最愛！✨",
        "跟著節奏！左刷刷右刷刷！🎵",
        "音樂好好聽，牙齒好乾淨！💃",
    ]
    last_speak = 0.0
    i = 0
    interval = 1.0 if quick else 0.5
    step = 2 if quick else 12
    while True:
        if stop.wait(interval):
            return
        i += 1
        now = time.monotonic()
        if use_say and now - last_speak >= 3.0:
            last_speak = now
            speak("刷刷刷，牙齒我最愛", 300)
        if i % step == 0:
            idx = (i // step - 1) % len(cheers)
            add_event(paint(f"🎵 {cheers[idx]}", CYAN))
            if tts_mode:
                print(cheers[idx], flush=True)


# ---------------- 煙火 + 完成慶祝 ----------------
def fireworks(seconds=2.0):
    frames = [
        [
            "      ✨      ",
            "   ✦   ✧   ✦  ",
            "🎆  *  *  *  🎆",
            "   ✧   ✦   ✧  ",
            "      ✨      ",
        ],
        [
            "   ✧   ✦   ✧  ",
            " ✨  *  *  * ✨ ",
            "  🎆  *  * 🎆  ",
            " ✦  *  *  *  ✦ ",
            "   ✧   ✦   ✧  ",
        ],
    ]
    end = time.monotonic() + seconds
    i = 0
    while time.monotonic() < end:
        clear_screen()
        print()
        for line in frames[i % len(frames)]:
            print(rainbow(line))
        print()
        i += 1
        time.sleep(0.25)


def finish(args, who, duration):
    """完成：煙火 + 大聲祝賀 + 星級 + 打卡 + 貼紙。"""
    if not args.tts:
        fireworks(1.2 if args.test else 2.0)
        print()
        print(paint("╔══════════════════════════════════════╗", YELLOW))
        print(paint("║  🎉 刷 牙 完 成 ！ 好 棒 棒 ！ 🎉  ║", YELLOW))
        print(paint("╚══════════════════════════════════════╝", YELLOW))
        print(paint("太 厲 害 了 ！ 牙 齒 亮 晶 晶 ！ ⭐", BOLD + WHITE))
        print()
    else:
        print("哇！刷牙完成！太厲害了！牙齒亮晶晶！", flush=True)

    stars = tracker.rate_duration(duration) if tracker else 5
    if not args.tts:
        print(paint("刷牙俠星級評價：", MAGENTA) + paint("⭐" * stars, YELLOW))
        print()

    if args.no_log or args.test:
        if not args.tts:
            print(paint("（測試模式：不寫打卡記錄、不發貼紙）", CYAN))
        return 0

    tts_tail = ""
    if tracker is not None:
        rec = tracker.record_brushing(who=who, duration=duration)
        streak = rec["streak"]
        if not args.tts:
            print(paint(f"📅 打卡成功！{who} 已連續刷牙 {streak} 天！", GREEN))
        tts_tail += f"打卡成功！已經連續刷牙 {streak} 天！"
    if reward is not None:
        st = reward.award_sticker(who=who)
        milestone = reward.milestone_text()
        if not args.tts:
            print()
            print(paint("🎁 獲得刷牙俠貼紙：", MAGENTA))
            print(paint(st["art"], BOLD + WHITE))
            print(paint(milestone, CYAN))
        tts_tail += f"獲得貼紙：{st['name']}！{milestone}"
    if args.tts and tts_tail:
        print(tts_tail, flush=True)
    return 0


# ---------------- 主流程 ----------------
def run(args):
    duration = 5 if args.test else args.minutes * 60
    who = args.who or "寶貝"
    mode = args.mode.upper()
    use_say = args.say and say_available()
    target_text = f"{duration} 秒" if duration < 60 else f"{duration // 60} 分鐘"

    # 鼓勵語輪播起點：依今天已刷次數偏移（每天輪法不同）
    offset = 0
    if tracker is not None and not args.test:
        try:
            offset = tracker.today_count() % len(ENCOURAGEMENTS)
        except Exception:
            offset = 0

    if args.tts:
        print(f"開始！{who} 今天要刷 {target_text}！小白陪你一起！刷刷刷！", flush=True)
    else:
        print(paint("🦷 快樂刷牙俠 · 小白陪你刷牙 🐰", CYAN))
        print(paint(f"👶 今天刷牙的是：{who}　　⏱ 目標 {target_text}", GREEN))
        if mode == "B":
            print(paint("📖 故事模式啟動！聽故事刷亮亮！", BLUE))
        elif mode == "C":
            print(paint("🎵 音樂模式啟動！跟著節奏刷刷刷！", YELLOW))
        print()
        countdown_3_2_1()

    stop = threading.Event()
    start = time.monotonic()
    threads = []

    t = threading.Thread(
        target=encouragement_worker,
        args=(stop, start, duration, offset, args.tts, use_say, args.test),
        daemon=True,
    )
    t.start()
    threads.append(t)

    if mode == "B":
        t = threading.Thread(
            target=story_worker,
            args=(stop, start, duration, args.tts, use_say, args.test),
            daemon=True,
        )
        t.start()
        threads.append(t)
    elif mode == "C":
        t = threading.Thread(
            target=music_worker,
            args=(stop, duration, args.tts, use_say, args.test),
            daemon=True,
        )
        t.start()
        threads.append(t)

    last_shown = None
    try:
        while True:
            elapsed = time.monotonic() - start
            remaining = duration - elapsed
            sec = int(remaining)
            if sec != last_shown:
                last_shown = sec
                render(remaining, elapsed, duration, mode, args.tts)
            if remaining <= 0:
                break
            if not args.test and not args.tts and _read_key() == "q":
                print("\n👋 小白說：沒關係，先休息一下，等一下再刷，小白等你喔～")
                stop.set()
                return 0
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("\n👋 小白說：沒關係！下次再一起刷滿 2 分鐘喔～")
        stop.set()
        return 0

    stop.set()
    for t in threads:
        t.join(timeout=0.5)
    return finish(args, who, duration)


def main():
    parser = argparse.ArgumentParser(
        description="🦷 快樂刷牙俠 — 互動式刷牙計時器（2 分鐘歡樂刷牙）",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument("--mode", choices=["A", "B", "C"], default="A",
                        help="A=標準（預設） B=故事模式 C=音樂模式")
    parser.add_argument("--minutes", type=int, default=2, help="刷牙目標分鐘數（預設 2）")
    parser.add_argument("--who", default=None, help="刷牙的小朋友名字（預設：寶貝）")
    parser.add_argument("--tts", action="store_true",
                        help="只輸出 TTS 朗讀文字（給 OpenClaw tts tool 用）")
    parser.add_argument("--say", action="store_true",
                        help="同時用 macOS say 即時朗讀（本機有音效）")
    parser.add_argument("--test", action="store_true",
                        help="測試模式：5 秒快速跑完，不寫打卡/貼紙")
    parser.add_argument("--no-log", action="store_true", help="不寫打卡記錄")
    args = parser.parse_args()
    sys.exit(run(args))


if __name__ == "__main__":
    main()
