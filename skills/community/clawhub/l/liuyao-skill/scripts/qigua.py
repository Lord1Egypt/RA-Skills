#!/usr/bin/env python3
import argparse
import json
import random
import sys
from datetime import datetime
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
ASSETS_DIR = SCRIPT_DIR.parent / "assets"


def load_gua_data():
    with open(ASSETS_DIR / "gua-data.json", encoding="utf-8") as f:
        data = json.load(f)
    data["lookup"] = {key: entry["name"] for key, entry in data["hexagrams"].items()}
    return data


# Lines are generated and stored from bottom to top, so these bit strings
# follow the same order: first bit = 初爻, third bit = 三爻.
TRIGRAM_NAMES = {
    "111": "qian",
    "000": "kun",
    "100": "zhen",
    "011": "xun",
    "010": "kan",
    "101": "li",
    "001": "gen",
    "110": "dui",
}

TRIGRAM_DISPLAY = {
    "qian": "乾",
    "kun": "坤",
    "zhen": "震",
    "xun": "巽",
    "kan": "坎",
    "li": "离",
    "gen": "艮",
    "dui": "兑",
}

YAO_TYPE_MAP = {
    0: {"type": "老阴", "symbol": "--", "moving": True, "yang": False},
    1: {"type": "少阳", "symbol": "—", "moving": False, "yang": True},
    2: {"type": "少阴", "symbol": "--", "moving": False, "yang": False},
    3: {"type": "老阳", "symbol": "—", "moving": True, "yang": True},
}


def yao_label(position, is_yang):
    yin_yang = "九" if is_yang else "六"
    if position == 1:
        return f"初{yin_yang}"
    elif position == 6:
        return f"上{yin_yang}"
    else:
        pos_names = {2: "二", 3: "三", 4: "四", 5: "五"}
        return f"{yin_yang}{pos_names[position]}"


def coin_back_count(rng=None):
    """Return the number of backs among three simulated coins."""
    rng = rng or random
    return sum(rng.randint(0, 1) for _ in range(3))


def shicao_change(stalks, change_index, rng=None):
    # Model the classic yarrow-stalk line probabilities directly:
    # first change removes 5/9 with 3:1 odds, later changes remove 4/8 evenly.
    rng = rng or random
    if change_index == 0:  # noqa: SIM108
        removed = 5 if rng.random() < 0.75 else 9
    else:
        removed = 4 if rng.random() < 0.5 else 8
    return stalks - removed


def shicao_line_value(rng=None):
    stalks = 49
    for change_index in range(3):
        stalks = shicao_change(stalks, change_index, rng)
    return stalks // 4


def yao_to_trigram_bit(yao_info):
    return "1" if yao_info["yang"] else "0"


def get_trigram_key(yaos):
    if len(yaos) != 3:
        raise ValueError("每个卦必须包含3个爻")
    if any(not isinstance(y.get("yang"), bool) for y in yaos):
        raise ValueError("爻数据缺少有效的 yang 布尔值")
    bits = "".join(yao_to_trigram_bit(y) for y in yaos)
    return TRIGRAM_NAMES[bits]


def get_hexagram_name(gua_data, upper_key, lower_key):
    lookup_key = f"{upper_key}_{lower_key}"
    try:
        return gua_data["lookup"][lookup_key]
    except KeyError as exc:
        raise ValueError(f"无法识别卦象：{lookup_key}") from exc


def divine_coin(rng=None):
    yaos = []
    for i in range(6):
        backs = coin_back_count(rng)
        yao_info = dict(YAO_TYPE_MAP[backs])
        yao_info["position"] = i + 1
        yao_info["label"] = yao_label(i + 1, yao_info["yang"])
        yaos.append(yao_info)
    return yaos


def divine_manual(inputs):
    if len(inputs) != 6:
        raise ValueError("需要输入6个数字（每个0-3）")
    yaos = []
    for i, v in enumerate(inputs):
        if v not in (0, 1, 2, 3):
            raise ValueError(f"第{i + 1}个输入 {v} 无效，必须是0-3")
        yao_info = dict(YAO_TYPE_MAP[v])
        yao_info["position"] = i + 1
        yao_info["label"] = yao_label(i + 1, yao_info["yang"])
        yaos.append(yao_info)
    return yaos


def divine_shicao(rng=None):
    value_to_input = {6: 0, 7: 1, 8: 2, 9: 3}
    yaos = []
    for i in range(6):
        value = shicao_line_value(rng)
        yao_info = dict(YAO_TYPE_MAP[value_to_input[value]])
        yao_info["position"] = i + 1
        yao_info["label"] = yao_label(i + 1, yao_info["yang"])
        yao_info["shicao_value"] = value
        yaos.append(yao_info)
    return yaos


def build_result(gua_data, yaos):
    if len(yaos) != 6:
        raise ValueError("六爻卦必须包含6个爻")
    positions = [y.get("position") for y in yaos]
    if positions != list(range(1, 7)):
        raise ValueError("爻位置必须按1到6排列")
    if any(not isinstance(y.get("moving"), bool) for y in yaos):
        raise ValueError("爻数据缺少有效的 moving 布尔值")

    lower_yaos = yaos[:3]
    upper_yaos = yaos[3:]

    lower_key = get_trigram_key(lower_yaos)
    upper_key = get_trigram_key(upper_yaos)

    ben_gua_name = get_hexagram_name(gua_data, upper_key, lower_key)

    bian_yaos = []
    for y in yaos:
        bian_yao = dict(y)
        if y["moving"]:
            bian_yao["yang"] = not y["yang"]
            bian_yao["symbol"] = "—" if bian_yao["yang"] else "--"
            bian_yao["type"] = "变爻"
            bian_yao["label"] = yao_label(y["position"], bian_yao["yang"])
        bian_yaos.append(bian_yao)

    bian_lower_key = get_trigram_key(bian_yaos[:3])
    bian_upper_key = get_trigram_key(bian_yaos[3:])
    bian_gua_name = get_hexagram_name(gua_data, bian_upper_key, bian_lower_key)

    moving_yao = [y["label"] for y in yaos if y["moving"]]

    result = {
        "ben_gua": {
            "name": ben_gua_name,
            "upper": TRIGRAM_DISPLAY.get(upper_key, upper_key),
            "lower": TRIGRAM_DISPLAY.get(lower_key, lower_key),
        },
        "bian_gua": {
            "name": bian_gua_name,
            "upper": TRIGRAM_DISPLAY.get(bian_upper_key, bian_upper_key),
            "lower": TRIGRAM_DISPLAY.get(bian_lower_key, bian_lower_key),
        },
        "yao_details": [
            {
                "position": y["position"],
                "type": y["type"],
                "symbol": y["symbol"],
                "moving": y["moving"],
                "label": y["label"],
                **({"shicao_value": y["shicao_value"]} if "shicao_value" in y else {}),
            }
            for y in yaos
        ],
        "moving_yao": moving_yao,
        "timestamp": datetime.now().astimezone().isoformat(timespec="seconds"),
    }
    return result


def print_visual(result):
    yaos = result["yao_details"]
    print(f"\n{'=' * 40}")
    print(f"本卦：{result['ben_gua']['name']}（上{result['ben_gua']['upper']} 下{result['ben_gua']['lower']}）")
    if result["moving_yao"]:
        print(f"变卦：{result['bian_gua']['name']}（上{result['bian_gua']['upper']} 下{result['bian_gua']['lower']}）")
    print(f"{'=' * 40}")
    print("卦象（自上而下显示）：")
    for y in reversed(yaos):
        marker = " ○动" if y["moving"] else ""
        print(f"  {y['label']}：{y['symbol']}{y['type']}{marker}")
    if result["moving_yao"]:
        print(f"\n动爻：{'、'.join(result['moving_yao'])}")
    else:
        print("\n无动爻（静卦）")
    print(f"{'=' * 40}\n")


def main():
    parser = argparse.ArgumentParser(description="周易起卦脚本")
    parser.add_argument(
        "--method",
        choices=["coin", "manual", "shicao"],
        default="coin",
        help="起卦方式：coin=铜钱法(默认), manual=手动输入, shicao=蓍草法",
    )
    parser.add_argument(
        "--input", type=str, default=None, help="手动输入模式：6个0-3的数字，逗号分隔（如 1,2,3,0,1,2）"
    )
    parser.add_argument("--json", action="store_true", help="仅输出JSON结果")
    parser.add_argument("--seed", type=int, default=None, help="设置随机种子，便于复现实验结果")
    args = parser.parse_args()

    # 默认使用 SystemRandom；显式 --seed 仅用于复现实验结果，不用于安全场景
    rng = random.Random(args.seed) if args.seed is not None else random.SystemRandom()

    gua_data = load_gua_data()

    if args.method == "coin":
        yaos = divine_coin(rng)
    elif args.method == "manual":
        if not args.input:
            print("错误：手动模式需要 --input 参数（6个0-3的数字，逗号分隔）", file=sys.stderr)
            sys.exit(1)
        try:
            inputs = [int(x.strip()) for x in args.input.split(",")]
        except ValueError:
            print("错误：输入格式不正确，需要6个0-3的数字，逗号分隔", file=sys.stderr)
            sys.exit(1)
        try:
            yaos = divine_manual(inputs)
        except ValueError as exc:
            print(f"错误：{exc}", file=sys.stderr)
            sys.exit(1)
    elif args.method == "shicao":
        yaos = divine_shicao(rng)

    result = build_result(gua_data, yaos)

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print_visual(result)
        print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
