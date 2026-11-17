#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔔 刷牙提醒（Cron 用）— 早安 / 晚安 / 懶惰再提醒

- 早安刷牙提醒：預設 07:00-08:00（可設定）
- 晚安刷牙提醒：預設 20:00-21:00（可設定）
- 懶惰提醒：過了時間還沒刷 → 5 分鐘後再提醒一次（預設，可設定）
- 輸出：TTS 語音提醒文字（適合餵給 OpenClaw tts tool 朗讀）

資料檔：
    設定    ~/.bookshelf-plus/kids/brushing_config.json
    提醒狀態 ~/.bookshelf-plus/kids/brushing_reminder_state.json

用法：
    python3 brushing_cron.py --check morning --tts          # 早安檢查（cron 07:00）
    python3 brushing_cron.py --check evening --tts          # 晚安檢查（cron 20:00）
    python3 brushing_cron.py --check evening --lazy --tts   # 懶惰再提醒（cron 每 5 分鐘）
    python3 brushing_cron.py --config-get                   # 看目前設定
    python3 brushing_cron.py --morning 07:30 --evening 20:30  # 改時間
    python3 brushing_cron.py --cron-install                 # 印出 crontab 設定
    python3 brushing_cron.py --test                         # 測試（印範例提醒）
"""

import argparse
import datetime as dt
import json
import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)

try:
    import brushing_tracker as tracker
except Exception:
    tracker = None

DATA_DIR = os.path.expanduser("~/.bookshelf-plus/kids")
CONFIG_FILE = os.path.join(DATA_DIR, "brushing_config.json")
STATE_FILE = os.path.join(DATA_DIR, "brushing_reminder_state.json")

DEFAULT_CONFIG = {
    "morning": {"start": "07:00", "end": "08:00"},
    "evening": {"start": "20:00", "end": "21:00"},
    "lazy_minutes": 5,
    "kid_name": "寶貝",
}

RESET = "\033[0m"
BOLD = "\033[1m"
YELLOW = "\033[33m"


def _ensure():
    os.makedirs(DATA_DIR, exist_ok=True)


def load_config():
    _ensure()
    cfg = json.loads(json.dumps(DEFAULT_CONFIG))  # deep copy
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                user = json.load(f)
            if isinstance(user, dict):
                for k in cfg:
                    if k in user:
                        cfg[k] = user[k]
        except Exception:
            pass
    return cfg


def save_config(cfg):
    _ensure()
    tmp = CONFIG_FILE + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(cfg, f, ensure_ascii=False, indent=2)
    os.replace(tmp, CONFIG_FILE)


def load_state():
    if not os.path.exists(STATE_FILE):
        return {}
    try:
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data if isinstance(data, dict) else {}
    except Exception:
        return {}


def save_state(state):
    _ensure()
    tmp = STATE_FILE + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)
    os.replace(tmp, STATE_FILE)


def _parse(hhmm):
    h, m = hhmm.strip().split(":")
    return int(h), int(m)


def _in_window(now_t, start, end):
    return start <= now_t <= end


def make_reminder(kind, kid):
    """產生正向、零責怪的 TTS 提醒文字（小白語氣）。"""
    if kind == "morning":
        return (f"早安！小白兔小白來叫{kid}刷牙囉！刷刷刷，牙齒我最愛！✨ "
                f"刷完可以得到閃亮亮貼紙喔！")
    if kind == "evening":
        return (f"晚安～小白兔小白提醒{kid}：刷完牙才能聽睡前故事喔！"
                f"一起把牙齒刷得亮晶晶！⭐")
    # lazy：過了時間還沒刷，溫柔再提醒（零責怪）
    return (f"小白發現今天還沒刷牙耶！沒關係，現在刷也來得及！"
            f"小白在浴室等你，一起刷刷刷！💪 刷完有貼紙喔！")


def lazy_due(state, cfg, now):
    """懶惰提醒是否已過 lazy_minutes 的冷卻時間。"""
    last = state.get("last_lazy")
    if not last:
        return True
    try:
        last_dt = dt.datetime.fromisoformat(last)
        return (now - last_dt).total_seconds() >= int(cfg.get("lazy_minutes", 5)) * 60
    except Exception:
        return True


def cmd_check(args):
    now = dt.datetime.now()
    cfg = load_config()
    kid = args.kid or cfg["kid_name"]
    session = (args.check or "auto").lower()
    if session == "auto":
        session = "morning" if now.hour < 12 else "evening"

    win = cfg.get(session, DEFAULT_CONFIG.get(session, DEFAULT_CONFIG["evening"]))
    start, end = _parse(win["start"]), _parse(win["end"])
    now_t = (now.hour, now.minute)
    in_win = _in_window(now_t, start, end)

    session_label = "上午" if session == "morning" else "下午"
    brushed = False
    if tracker is not None:
        brushed = tracker.brushed_today(session=session_label)

    texts = []
    if not brushed:
        if in_win:
            if args.lazy:
                # 懶惰排程的每 5 分鐘一次：有冷卻，不吵人
                state = load_state()
                if lazy_due(state, cfg, now):
                    texts.append(make_reminder(session, kid))
                    state["last_lazy"] = now.isoformat(timespec="minutes")
                    save_state(state)
            else:
                texts.append(make_reminder(session, kid))
        elif now_t > end and args.lazy:
            # 過了時間還沒刷 → 5 分鐘後再提醒一次（有冷卻）
            state = load_state()
            if lazy_due(state, cfg, now):
                texts.append(make_reminder("lazy", kid))
                state["last_lazy"] = now.isoformat(timespec="minutes")
                save_state(state)

    if not texts:
        if not args.tts:
            print("✅ 今天已經刷過牙了（或時間未到），不需要提醒～")
        return 0

    for t in texts:
        if args.tts:
            print(t, flush=True)
        else:
            print(f"{YELLOW}🔔 刷牙提醒：{RESET}{BOLD}{t}{RESET}")
            print("TTS:", t)
    return 0


def cmd_config(args):
    cfg = load_config()
    if args.config_get:
        print(json.dumps(cfg, ensure_ascii=False, indent=2))
        return
    changed = False
    if args.morning:
        cfg["morning"]["start"] = args.morning
        changed = True
    if args.morning_end:
        cfg["morning"]["end"] = args.morning_end
        changed = True
    if args.evening:
        cfg["evening"]["start"] = args.evening
        changed = True
    if args.evening_end:
        cfg["evening"]["end"] = args.evening_end
        changed = True
    if args.kid:
        cfg["kid_name"] = args.kid
        changed = True
    if args.lazy_minutes:
        cfg["lazy_minutes"] = args.lazy_minutes
        changed = True
    if changed:
        save_config(cfg)
        print("✅ 已更新刷牙提醒設定：")
    print(json.dumps(cfg, ensure_ascii=False, indent=2))


def cmd_cron_install():
    py = sys.executable or "/usr/bin/python3"
    skill = os.path.dirname(SCRIPT_DIR)
    lines = [
        "請將以下內容加入 crontab（crontab -e）：",
        "",
        "# 🦷 快樂刷牙俠 — 早安刷牙提醒（每天 07:00）",
        f"0 7 * * * cd \"{skill}\" && \"{py}\" scripts/brushing_cron.py --check morning --tts",
        "",
        "# 🦷 快樂刷牙俠 — 晚安刷牙提醒（每天 20:00）",
        f"0 20 * * * cd \"{skill}\" && \"{py}\" scripts/brushing_cron.py --check evening --tts",
        "",
        "# 🦷 快樂刷牙俠 — 懶惰再提醒（20:05 起每 5 分鐘；刷過牙就不會吵）",
        f"5-59/5 20-21 * * * cd \"{skill}\" && \"{py}\" scripts/brushing_cron.py --check evening --lazy --tts",
        "",
        "提示：在 OpenClaw 環境中，建議用 qclaw-cron-skill 排程，"
        "把腳本輸出的 TTS 文字餵給 tts tool 朗讀。",
    ]
    print("\n".join(lines))


def cmd_test():
    print("🧪 刷牙提醒測試輸出（不寫入任何狀態）：")
    print()
    print("【早安提醒】")
    print(make_reminder("morning", "寶貝"))
    print()
    print("【晚安提醒】")
    print(make_reminder("evening", "寶貝"))
    print()
    print("【懶惰再提醒】")
    print(make_reminder("lazy", "寶貝"))
    print()
    print("【目前設定】")
    print(json.dumps(load_config(), ensure_ascii=False, indent=2))


def main():
    parser = argparse.ArgumentParser(
        description="🔔 刷牙提醒（Cron 用）— 早安 / 晚安 / 懶惰再提醒",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument("--check", choices=["morning", "evening", "auto"], default=None,
                        help="檢查並輸出提醒（未刷才提醒）")
    parser.add_argument("--lazy", action="store_true",
                        help="懶惰再提醒模式：未刷且時間已過 → 5 分鐘後再提醒一次")
    parser.add_argument("--kid", default=None, help="小朋友名字")
    parser.add_argument("--tts", action="store_true",
                        help="只輸出 TTS 朗讀文字（適合 cron）")
    parser.add_argument("--config-get", action="store_true", help="顯示目前設定")
    parser.add_argument("--morning", default=None, help="早安開始時間，如 07:00")
    parser.add_argument("--morning-end", default=None, help="早安結束時間，如 08:00")
    parser.add_argument("--evening", default=None, help="晚安開始時間，如 20:00")
    parser.add_argument("--evening-end", default=None, help="晚安結束時間，如 21:00")
    parser.add_argument("--lazy-minutes", type=int, default=None,
                        help="懶惰再提醒間隔分鐘（預設 5）")
    parser.add_argument("--cron-install", action="store_true", help="印出 crontab 設定")
    parser.add_argument("--test", action="store_true", help="測試：印出範例提醒文字")
    args = parser.parse_args()

    if args.test:
        cmd_test()
    elif args.cron_install:
        cmd_cron_install()
    elif args.config_get or args.morning or args.evening or args.morning_end or args.evening_end or args.lazy_minutes or args.kid:
        cmd_config(args)
    elif args.check:
        sys.exit(cmd_check(args))
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
