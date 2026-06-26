import argparse
import json
import sys
from pathlib import Path


STATE_PATH = Path.home() / ".openclaw" / "king-wen-session.json"


def configure_stdout() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")


def ensure_parent() -> None:
    STATE_PATH.parent.mkdir(parents=True, exist_ok=True)


def read_state() -> dict:
    if not STATE_PATH.exists():
        return {}
    return json.loads(STATE_PATH.read_text(encoding="utf-8"))


def write_state(data: dict) -> None:
    ensure_parent()
    STATE_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def ensure_profile_bucket(state: dict) -> dict:
    profile = state.get("profile")
    if not isinstance(profile, dict):
        profile = {}
        state["profile"] = profile
    return profile


def ensure_daily_fortune_bucket(state: dict) -> dict:
    daily_fortune = state.get("daily_fortune")
    if not isinstance(daily_fortune, dict):
        daily_fortune = {}
        state["daily_fortune"] = daily_fortune
    return daily_fortune


def main() -> None:
    configure_stdout()
    parser = argparse.ArgumentParser(description="查看或更新当前问事会话状态。")
    parser.add_argument("--show", action="store_true", help="显示当前状态。")
    parser.add_argument("--clear", action="store_true", help="清空当前状态。")
    parser.add_argument("--question", help="写入当前问题摘要。")
    parser.add_argument("--hexagram", type=int, help="写入当前本卦卦序。")
    parser.add_argument("--moving-lines", help="写入动爻，例如 2,5。")
    parser.add_argument("--lunar-birthday", help="写入命主农历生日，例如 癸酉年八月十五。")
    parser.add_argument("--gender", help="写入命主性别，例如 男 或 女。")
    parser.add_argument("--birth-hour", help="可选，写入命主时辰，例如 子时。")
    parser.add_argument("--daily-time", help="写入每日运势执行时间，例如 07:30。")
    parser.add_argument("--timezone", help="写入每日运势时区，例如 Asia/Shanghai。")
    args = parser.parse_args()

    if args.clear:
        if STATE_PATH.exists():
            STATE_PATH.unlink()
        print("已清空当前问事会话。")
        return

    state = read_state()

    if args.question:
        state["question"] = args.question
    if args.hexagram is not None:
        state["hexagram"] = args.hexagram
    if args.moving_lines:
        state["moving_lines"] = [int(part.strip()) for part in args.moving_lines.split(",") if part.strip()]
    if args.lunar_birthday:
        profile = ensure_profile_bucket(state)
        profile["lunar_birthday"] = args.lunar_birthday
    if args.gender:
        profile = ensure_profile_bucket(state)
        profile["gender"] = args.gender
    if args.birth_hour:
        profile = ensure_profile_bucket(state)
        profile["birth_hour"] = args.birth_hour
    if args.daily_time:
        daily_fortune = ensure_daily_fortune_bucket(state)
        daily_fortune["time"] = args.daily_time
    if args.timezone:
        daily_fortune = ensure_daily_fortune_bucket(state)
        daily_fortune["timezone"] = args.timezone

    if (
        args.question
        or args.hexagram is not None
        or args.moving_lines
        or args.lunar_birthday
        or args.gender
        or args.birth_hour
        or args.daily_time
        or args.timezone
    ):
        write_state(state)

    if args.show or state:
        print(json.dumps(state, ensure_ascii=False, indent=2))
    else:
        print("{}")


if __name__ == "__main__":
    main()
