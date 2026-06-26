import argparse
import json
from typing import Optional

from session_state import (
    configure_stdout,
    ensure_daily_fortune_bucket,
    ensure_profile_bucket,
    read_state,
    write_state,
)


def prompt_yes_no(question: str, default: bool = False) -> bool:
    default_hint = "Y/n" if default else "y/N"
    raw = input(f"{question}[{default_hint}]：").strip().lower()
    if not raw:
        return default
    return raw in {"y", "yes", "是"}


def prompt_value(label: str, current: str | None = None, optional: bool = False) -> Optional[str]:
    current_hint = f"（当前：{current}）" if current else ""
    optional_hint = "，可留空跳过" if optional else ""
    raw = input(f"{label}{current_hint}{optional_hint}：").strip()
    if raw:
        return raw
    if current:
        return current
    return None


def should_enable_daily_fortune(current_time: str | None = None) -> bool:
    return prompt_yes_no("是否同时设置每日运势时间？", default=bool(current_time))


def quote_message(raw: str) -> str:
    return raw.replace("\\", "\\\\").replace('"', '\\"')


def build_cron_command(state: dict) -> str | None:
    profile = state.get("profile")
    daily_fortune = state.get("daily_fortune")
    if not isinstance(profile, dict) or not isinstance(daily_fortune, dict):
        return None

    daily_time = daily_fortune.get("time")
    timezone = daily_fortune.get("timezone") or "Asia/Shanghai"
    lunar_birthday = profile.get("lunar_birthday")
    gender = profile.get("gender")
    if not daily_time or not lunar_birthday or not gender:
        return None

    if ":" not in daily_time:
        return None

    hour_text, minute_text = daily_time.split(":", 1)
    if not hour_text.isdigit() or not minute_text.isdigit():
        return None

    hour = int(hour_text)
    minute = int(minute_text)
    if hour < 0 or hour > 23 or minute < 0 or minute > 59:
        return None

    birth_hour = profile.get("birth_hour") or "未提供"
    cron_expr = f"{minute} {hour} * * *"
    message = (
        "请启用 king-wen-hexagrams 技能，为我生成今日运势。"
        f"命主资料如下：农历生日={lunar_birthday}；性别={gender}；出生时辰={birth_hour}。"
        "请结合今天的日期，起一卦看当日气机，只输出：今日卦势、气机偏向、宜、忌、一句收束。"
        "口吻保持庄重、简洁、克制，不要夸张渲染神秘。"
    )
    return (
        "openclaw cron add \\\n"
        '  --name "文王每日运势" \\\n'
        f'  --cron "{cron_expr}" \\\n'
        f'  --tz "{timezone}" \\\n'
        '  --session isolated \\\n'
        f'  --message "{quote_message(message)}" \\\n'
        "  --announce"
    )


def main() -> None:
    configure_stdout()
    parser = argparse.ArgumentParser(description="初始化命主资料与每日运势设置。")
    parser.add_argument("--lunar-birthday", help="命主农历生日，例如 农历二零零一年三月初八。")
    parser.add_argument("--gender", help="命主性别，例如 男、女。")
    parser.add_argument("--birth-hour", help="出生时辰，例如 子时。")
    parser.add_argument("--daily-time", help="每日运势时间，例如 07:30。")
    parser.add_argument("--timezone", help="时区，例如 Asia/Shanghai。")
    parser.add_argument(
        "--skip-daily-fortune",
        action="store_true",
        help="只初始化命主资料，不设置每日运势。",
    )
    args = parser.parse_args()

    state = read_state()
    profile = ensure_profile_bucket(state)
    daily_fortune = ensure_daily_fortune_bucket(state)

    print("为你立一个命主小档，后面问卦与每日运势都会更连贯一些。")
    print("默认只需两项：农历生日、性别；出生时辰与每日运势时间都可稍后再补。")
    print()

    if args.lunar_birthday is not None:
        profile["lunar_birthday"] = args.lunar_birthday
    elif not profile.get("lunar_birthday"):
        value = prompt_value("请输入农历生日")
        if value:
            profile["lunar_birthday"] = value

    if args.gender is not None:
        profile["gender"] = args.gender
    elif not profile.get("gender"):
        value = prompt_value("请输入性别")
        if value:
            profile["gender"] = value

    if args.birth_hour is not None:
        profile["birth_hour"] = args.birth_hour
    else:
        value = prompt_value("如愿意可补出生时辰", profile.get("birth_hour"), optional=True)
        if value:
            profile["birth_hour"] = value

    enable_daily_fortune = False
    if args.skip_daily_fortune:
        enable_daily_fortune = False
    elif args.daily_time or args.timezone:
        enable_daily_fortune = True
    else:
        enable_daily_fortune = should_enable_daily_fortune(daily_fortune.get("time"))

    if enable_daily_fortune:
        if args.daily_time is not None:
            daily_fortune["time"] = args.daily_time
        else:
            value = prompt_value("请输入每日运势时间", daily_fortune.get("time"), optional=True)
            if value:
                daily_fortune["time"] = value

        if args.timezone is not None:
            daily_fortune["timezone"] = args.timezone
        else:
            value = prompt_value("请输入时区", daily_fortune.get("timezone") or "Asia/Shanghai", optional=True)
            if value:
                daily_fortune["timezone"] = value

    write_state(state)

    print()
    print("初始化完成，当前保存状态如下：")
    print(json.dumps(state, ensure_ascii=False, indent=2))

    cron_command = build_cron_command(state)
    if cron_command and prompt_yes_no("是否需要继续配置每日运势 cron？", default=False):
        print()
        print("可直接参考下面这条 OpenClaw 命令：")
        print(cron_command)
    elif cron_command:
        print()
        print("如果你之后想接入每日运势 cron，可查看：daily-fortune.md")


if __name__ == "__main__":
    main()
