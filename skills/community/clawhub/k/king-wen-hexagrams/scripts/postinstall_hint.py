import json

from session_state import configure_stdout, read_state


def has_profile(state: dict) -> bool:
    profile = state.get("profile")
    if not isinstance(profile, dict):
        return False
    return bool(profile.get("lunar_birthday")) and bool(profile.get("gender"))


def main() -> None:
    configure_stdout()
    state = read_state()

    print("King Wen Hexagrams 已安装。")
    print()

    if has_profile(state):
        print("已检测到命主资料，你可以直接开始问卦或设置每日运势。")
        print("查看当前状态：python scripts/session_state.py --show")
        print("如需更新资料：python scripts/init_profile.py")
        print()
        print("当前已保存摘要：")
        print(json.dumps(state, ensure_ascii=False, indent=2))
        return

    print("建议先完成一次命主资料初始化，再开始正式问卦。")
    print("推荐命令：npm run init-profile")
    print("或：python scripts/init_profile.py")
    print()
    print("首次启用建议话术：")
    print(
        "在正式起卦前，我先替你立一个命主小档。"
        "这样以后问卦、续问与每日运势都会更连贯。"
        "若你愿意，先告诉我两项：农历生日与性别；"
        "若还记得出生时辰，也可一并补上。"
        "若你不想提供，我们也可以直接起卦。"
    )
    print()
    print("更多说明见：onboarding.md")


if __name__ == "__main__":
    main()
