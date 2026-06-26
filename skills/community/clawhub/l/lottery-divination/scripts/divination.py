#!/usr/bin/env python3
"""
梅花易数彩票测算器 — Meihua Yishu Lottery Divination Engine

根据当前时间起卦，生成本卦、互卦、变卦，并映射为双色球/大乐透推荐号码。
采用「易数种子法」：将干支数+卦数组合为随机种子，保证号码不重复且在合法区间。
"""

import sys
import json
import hashlib
import random
from datetime import datetime

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 一、天干地支与农历近似映射
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

TIAN_GAN = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
DI_ZHI   = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]

# 先天八卦数 (乾1 兑2 离3 震4 巽5 坎6 艮7 坤8)
XIANTIAN = {1: "乾", 2: "兑", 3: "离", 4: "震", 5: "巽", 6: "坎", 7: "艮", 8: "坤"}

# 八卦符号 (用 Unicode 或三行表示)
GUA_SYMBOL = {
    "乾": "☰", "兑": "☱", "离": "☲", "震": "☳",
    "巽": "☴", "坎": "☵", "艮": "☶", "坤": "☷",
}

# 六十四卦名称查询表 (上卦, 下卦) -> 卦名
HEXAGRAM_NAMES = {
    ("乾","乾"): "乾为天",   ("乾","坤"): "天地否",   ("乾","震"): "天雷无妄", ("乾","巽"): "天风姤",
    ("乾","坎"): "天水讼",   ("乾","离"): "天火同人", ("乾","艮"): "天山遁",   ("乾","兑"): "天泽履",
    ("坤","乾"): "地天泰",   ("坤","坤"): "坤为地",   ("坤","震"): "地雷复",   ("坤","巽"): "地风升",
    ("坤","坎"): "地水师",   ("坤","离"): "地火明夷", ("坤","艮"): "地山谦",   ("坤","兑"): "地泽临",
    ("震","乾"): "雷天大壮", ("震","坤"): "雷地豫",   ("震","震"): "震为雷",   ("震","巽"): "雷风恒",
    ("震","坎"): "雷水解",   ("震","离"): "雷火丰",   ("震","艮"): "雷山小过", ("震","兑"): "雷泽归妹",
    ("巽","乾"): "风天小畜", ("巽","坤"): "风地观",   ("巽","震"): "风雷益",   ("巽","巽"): "巽为风",
    ("巽","坎"): "风水涣",   ("巽","离"): "风火家人", ("巽","艮"): "风山渐",   ("巽","兑"): "风泽中孚",
    ("坎","乾"): "水天需",   ("坎","坤"): "水地比",   ("坎","震"): "水雷屯",   ("坎","巽"): "水风井",
    ("坎","坎"): "坎为水",   ("坎","离"): "水火既济", ("坎","艮"): "水山蹇",   ("坎","兑"): "水泽节",
    ("离","乾"): "火天大有", ("离","坤"): "火地晋",   ("离","震"): "火雷噬嗑", ("离","巽"): "火风鼎",
    ("离","坎"): "火水未济", ("离","离"): "离为火",   ("离","艮"): "火山旅",   ("离","兑"): "火泽睽",
    ("艮","乾"): "山天大畜", ("艮","坤"): "山地剥",   ("艮","震"): "山雷颐",   ("艮","巽"): "山风蛊",
    ("艮","坎"): "山水蒙",   ("艮","离"): "山火贲",   ("艮","艮"): "艮为山",   ("艮","兑"): "山泽损",
    ("兑","乾"): "泽天夬",   ("兑","坤"): "泽地萃",   ("兑","震"): "泽雷随",   ("兑","巽"): "泽风大过",
    ("兑","坎"): "泽水困",   ("兑","离"): "泽火革",   ("兑","艮"): "泽山咸",   ("兑","兑"): "兑为泽",
}

# 五行属性
GUA_WUXING = {
    "乾": "金", "兑": "金", "离": "火", "震": "木",
    "巽": "木", "坎": "水", "艮": "土", "坤": "土",
}


def year_ganzhi(year: int) -> tuple[str, str, int, int]:
    """计算年干支（以立春为界的简化版本）"""
    gan_idx = (year - 4) % 10
    zhi_idx = (year - 4) % 12
    return TIAN_GAN[gan_idx], DI_ZHI[zhi_idx], gan_idx + 1, zhi_idx + 1


def month_ganzhi_approx(year: int, month: int) -> tuple[str, str, int, int]:
    """
    近似月干支。
    注意：严格来说需要节气精算，这里用公历月份近似映射。
    月地支固定：正月寅、二月卯 ... 十二月丑
    """
    zhi_idx = (month + 1) % 12  # 1月→寅(2), 2月→卯(3), ...
    # 月天干 = (年干 * 2 + 月数) % 10 的简化公式
    year_gan_idx = (year - 4) % 10
    gan_idx = (year_gan_idx * 2 + month) % 10
    return TIAN_GAN[gan_idx], DI_ZHI[zhi_idx], gan_idx + 1, zhi_idx + 1


def day_number_in_year(year: int, month: int, day: int) -> int:
    """当年第几天"""
    return (datetime(year, month, day) - datetime(year, 1, 1)).days + 1


def hour_dizhi(hour: int) -> tuple[str, int]:
    """时辰地支: 23-1子, 1-3丑, ... """
    zhi_idx = ((hour + 1) // 2) % 12
    return DI_ZHI[zhi_idx], zhi_idx + 1


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 二、梅花易数核心起卦
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def to_gua_num(n: int) -> int:
    """将数字映射到 1-8 的先天八卦数"""
    r = n % 8
    return 8 if r == 0 else r


def get_yao_lines(gua_name: str) -> list[int]:
    """返回卦的三爻列表 (从下到上), 1=阳, 0=阴"""
    yao_map = {
        "乾": [1,1,1], "兑": [1,1,0], "离": [1,0,1], "震": [0,0,1],
        "巽": [1,1,0], "坎": [0,1,0], "艮": [1,0,0], "坤": [0,0,0],
    }
    # 巽的正确爻: 下阳中阳上阴 → [1,1,0]
    yao_map["巽"] = [0,1,1]  # 从下到上: 阴阳阳
    yao_map["兑"] = [0,1,1]  # 兑: 从下到上 阳阳阴 → wait
    # 标准先天八卦爻 (从下到上):
    yao_map = {
        "乾": [1,1,1],  # ☰ 三阳
        "兑": [0,1,1],  # ☱ 上缺
        "离": [1,0,1],  # ☲ 中虚
        "震": [1,0,0],  # ☳ 仰盂
        "巽": [0,1,1],  # ☴ wait, 巽是下断
        "坎": [0,1,0],  # ☵ 中满
        "艮": [0,0,1],  # ☶ 覆碗
        "坤": [0,0,0],  # ☷ 三阴
    }
    # 再修正一下标准的:
    # 乾 ☰ = 111, 兑 ☱ = 011 (下阴中阳上阳? 不对)
    # 国际通用从下到上:
    # 乾=111, 兑=110, 离=101, 震=001, 巽=011, 坎=010, 艮=100, 坤=000
    # 但传统从上到下读: 乾=☰三连, 兑=☱上缺
    # 我们用从下到上(初爻→三爻):
    yao_map = {
        "乾": [1,1,1],
        "兑": [1,1,0],
        "离": [1,0,1],
        "震": [0,0,1],
        "巽": [1,1,0],  # No!
        "坎": [0,1,0],
        "艮": [1,0,0],
        "坤": [0,0,0],
    }
    # OK let me be precise. 从底到顶 (初爻=index0, 上爻=index2):
    # 乾 ≡≡≡ = [1,1,1]
    # 兑 ≡≡-- = 底阳中阳上阴? No. 兑☱ 上面缺口 = 底阳中阳上阴 = [1,1,0]
    # 离 ≡--≡ = [1,0,1]
    # 震 --≡-- NO. 震☳ = 底下一阳 = [1,0,0]
    # 巽 ☴ = 底下一阴 = [0,1,1]
    # 坎 ☵ = [0,1,0]
    # 艮 ☶ = 顶上一阳 = [0,0,1]
    # 坤 = [0,0,0]
    yao_map = {
        "乾": [1,1,1],
        "兑": [1,1,0],
        "离": [1,0,1],
        "震": [1,0,0],
        "巽": [0,1,1],
        "坎": [0,1,0],
        "艮": [0,0,1],
        "坤": [0,0,0],
    }
    return yao_map[gua_name]


def yao_to_gua(yao: list[int]) -> str:
    """三爻列表 -> 卦名"""
    for name, y in [("乾",[1,1,1]),("兑",[1,1,0]),("离",[1,0,1]),("震",[1,0,0]),
                    ("巽",[0,1,1]),("坎",[0,1,0]),("艮",[0,0,1]),("坤",[0,0,0])]:
        if yao == y:
            return name
    return "坤"


def meihua_qigua(now: datetime) -> dict:
    """
    梅花易数·时间起卦法

    规则:
    - 上卦 = (年数 + 月数 + 日数) % 8
    - 下卦 = (年数 + 月数 + 日数 + 时辰数) % 8
    - 动爻 = (年数 + 月数 + 日数 + 时辰数) % 6
    - 互卦 = 六爻中 2,3,4 爻为下卦, 3,4,5 爻为上卦
    - 变卦 = 动爻阴阳互换
    """
    year, month, day, hour = now.year, now.month, now.day, now.hour

    # 干支数
    _, _, year_gan_n, year_zhi_n = year_ganzhi(year)
    _, _, month_gan_n, month_zhi_n = month_ganzhi_approx(year, month)
    hour_zhi_name, hour_zhi_n = hour_dizhi(hour)

    year_num = year_zhi_n       # 用年地支数
    month_num = month_zhi_n     # 用月地支数 (简化: 用月份数也可)
    day_num = day               # 日数
    hour_num = hour_zhi_n       # 时辰地支数

    # ---- 起卦 ----
    upper_raw = year_num + month_num + day_num
    lower_raw = upper_raw + hour_num
    dong_yao_raw = lower_raw

    upper_n = to_gua_num(upper_raw)
    lower_n = to_gua_num(lower_raw)
    dong_yao = dong_yao_raw % 6
    if dong_yao == 0:
        dong_yao = 6

    upper_name = XIANTIAN[upper_n]
    lower_name = XIANTIAN[lower_n]

    # ---- 六爻组装 (从下到上: 1-3为下卦, 4-6为上卦) ----
    six_yao = get_yao_lines(lower_name) + get_yao_lines(upper_name)
    # six_yao[0]=初爻, six_yao[5]=上爻

    # ---- 互卦 (2,3,4爻为下, 3,4,5爻为上, 爻编号从1开始) ----
    hu_lower_yao = six_yao[1:4]   # 2,3,4 爻
    hu_upper_yao = six_yao[2:5]   # 3,4,5 爻
    hu_lower_name = yao_to_gua(hu_lower_yao)
    hu_upper_name = yao_to_gua(hu_upper_yao)

    # ---- 变卦 (动爻翻转) ----
    bian_yao = six_yao.copy()
    bian_yao[dong_yao - 1] = 1 - bian_yao[dong_yao - 1]
    bian_lower_yao = bian_yao[0:3]
    bian_upper_yao = bian_yao[3:6]
    bian_lower_name = yao_to_gua(bian_lower_yao)
    bian_upper_name = yao_to_gua(bian_upper_yao)

    # ---- 卦名 ----
    ben_gua_name = HEXAGRAM_NAMES.get((upper_name, lower_name), f"{upper_name}上{lower_name}下")
    hu_gua_name  = HEXAGRAM_NAMES.get((hu_upper_name, hu_lower_name), f"{hu_upper_name}上{hu_lower_name}下")
    bian_gua_name = HEXAGRAM_NAMES.get((bian_upper_name, bian_lower_name), f"{bian_upper_name}上{bian_lower_name}下")

    return {
        "time_info": {
            "datetime": now.strftime("%Y年%m月%d日 %H:%M"),
            "year_ganzhi": f"{year_ganzhi(year)[0]}{year_ganzhi(year)[1]}年",
            "hour_dizhi": f"{hour_zhi_name}时",
            "numbers": f"年数{year_num} + 月数{month_num} + 日数{day_num} + 时数{hour_num}",
        },
        "ben_gua": {
            "upper": upper_name, "lower": lower_name,
            "upper_n": upper_n, "lower_n": lower_n,
            "name": ben_gua_name,
            "symbol": f"{GUA_SYMBOL[upper_name]}{GUA_SYMBOL[lower_name]}",
            "wuxing": f"上{GUA_WUXING[upper_name]}下{GUA_WUXING[lower_name]}",
        },
        "dong_yao": dong_yao,
        "hu_gua": {
            "upper": hu_upper_name, "lower": hu_lower_name,
            "name": hu_gua_name,
            "symbol": f"{GUA_SYMBOL[hu_upper_name]}{GUA_SYMBOL[hu_lower_name]}",
        },
        "bian_gua": {
            "upper": bian_upper_name, "lower": bian_lower_name,
            "name": bian_gua_name,
            "symbol": f"{GUA_SYMBOL[bian_upper_name]}{GUA_SYMBOL[bian_lower_name]}",
        },
        # 用于种子生成的原始数字
        "_seed_nums": {
            "upper_n": upper_n, "lower_n": lower_n,
            "dong_yao": dong_yao,
            "year_num": year_num, "month_num": month_num,
            "day_num": day_num, "hour_num": hour_num,
        },
    }


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 三、易数种子法 — 卦象映射为彩票号码
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def generate_seed(seed_nums: dict) -> int:
    """
    将卦象数字组合成稳定的随机种子。
    同一秒内起卦，结果完全一致（天机不可泄两次）。
    """
    seed_str = "|".join(str(seed_nums[k]) for k in sorted(seed_nums.keys()))
    return int(hashlib.sha256(seed_str.encode()).hexdigest(), 16) % (2**32)


def pick_numbers(seed: int, count: int, pool_max: int, pool_min: int = 1) -> list[int]:
    """用给定种子从 [pool_min, pool_max] 中不重复抽取 count 个号码"""
    rng = random.Random(seed)
    pool = list(range(pool_min, pool_max + 1))
    rng.shuffle(pool)
    return sorted(pool[:count])


def generate_lottery(lottery_type: str, seed_nums: dict) -> dict:
    """
    生成彩票推荐号码。

    双色球 (ssq): 红球 6 个 (1-33) + 蓝球 1 个 (1-16)
    大乐透 (dlt): 前区 5 个 (1-35) + 后区 2 个 (1-12)
    """
    base_seed = generate_seed(seed_nums)

    if lottery_type == "ssq":
        red = pick_numbers(base_seed, 6, 33)
        # 蓝球用不同的种子偏移，避免相关性
        blue = pick_numbers(base_seed ^ 0xB10EBA11, 1, 16)
        return {
            "type": "双色球",
            "type_code": "ssq",
            "red_balls": red,
            "blue_ball": blue[0],
            "format": f"红球: {' '.join(f'{n:02d}' for n in red)}  |  蓝球: {blue[0]:02d}",
        }
    elif lottery_type == "dlt":
        front = pick_numbers(base_seed, 5, 35)
        back = pick_numbers(base_seed ^ 0xDA1E0000, 2, 12)
        return {
            "type": "大乐透",
            "type_code": "dlt",
            "front_zone": front,
            "back_zone": back,
            "format": f"前区: {' '.join(f'{n:02d}' for n in front)}  |  后区: {' '.join(f'{n:02d}' for n in back)}",
        }
    else:
        raise ValueError(f"未知彩票类型: {lottery_type}，请使用 'ssq' 或 'dlt'")


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 四、入口
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def main():
    if len(sys.argv) < 2:
        print("用法: python divination.py <ssq|dlt> [YYYY-MM-DD-HH]", file=sys.stderr)
        sys.exit(1)

    lottery_type = sys.argv[1].lower()
    if lottery_type not in ("ssq", "dlt"):
        print(f"错误: 彩票类型必须为 ssq 或 dlt，收到: {lottery_type}", file=sys.stderr)
        sys.exit(1)

    # 可选：手动指定时间（用于测试）
    if len(sys.argv) >= 3:
        parts = sys.argv[2].split("-")
        now = datetime(int(parts[0]), int(parts[1]), int(parts[2]), int(parts[3]))
    else:
        now = datetime.now()

    # 起卦
    gua = meihua_qigua(now)

    # 生成号码
    lottery = generate_lottery(lottery_type, gua["_seed_nums"])

    # 输出 JSON
    result = {
        "divination": gua,
        "lottery": lottery,
    }
    # 去掉内部种子数据
    del result["divination"]["_seed_nums"]

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
