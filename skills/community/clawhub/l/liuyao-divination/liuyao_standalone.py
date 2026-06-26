#!/usr/bin/env python3
"""
六爻预测Skill - 独立版本
包含所有必要的代码，无需依赖其他文件

使用方法：
    from liuyao_standalone import LiuyaoSkill

    skill = LiuyaoSkill()
    result = skill.divinate("问财运如何", "男")
    print(skill.format_text(result))
"""

import hashlib
import random
import datetime
from dataclasses import dataclass, field
from typing import List, Optional, Any
from enum import Enum, unique

# =============================================================================
# 枚举定义
# =============================================================================

@unique
class Sky(Enum):
    JIA = '甲'
    YI = '乙'
    BING = '丙'
    DING = '丁'
    WU = '戊'
    JI = '己'
    GENG = '庚'
    XIN = '辛'
    REN = '壬'
    GUI = '癸'


@unique
class Earth(Enum):
    ZI = '子'
    CHOU = '丑'
    YIN = '寅'
    MAO = '卯'
    CHEN = '辰'
    SI = '巳'
    WU = '午'
    WEI = '未'
    SHEN = '申'
    YOU = '酉'
    XU = '戌'
    HAI = '亥'


@unique
class Reps(Enum):
    GUAN = '官鬼'
    QI = '妻财'
    XIONG = '兄弟'
    FU = '父母'
    ZI = '子孙'


@unique
class Soul(Enum):
    LONG = '青龙'
    QUE = '朱雀'
    CHEN = '勾陈'
    SHE = '腾蛇'
    HU = '白虎'
    WU = '玄武'


@unique
class FortuneLevel(Enum):
    DA_JI = '大吉'
    JI = '吉'
    XIAO_JI = '小吉'
    PING = '平'
    XIAO_XIONG = '小凶'
    XIONG = '凶'
    DA_XIONG = '大凶'


# =============================================================================
# 数据模型
# =============================================================================

@dataclass
class YAO:
    """爻：六爻预测的基本单位"""
    essence: Optional[int] = None
    feature: Optional[int] = None
    ego: int = 0
    other: int = 0
    najia: Optional[List] = field(default_factory=list)
    representation: Optional[Any] = None
    soul: Optional[Any] = None


@dataclass
class GUA:
    """卦：由六爻组成的卦象"""
    yaos: List[YAO] = field(default_factory=lambda: [YAO() for _ in range(6)])

    def __post_init__(self):
        if len(self.yaos) != 6:
            raise ValueError(f"GUA must have exactly 6 yaos, got {len(self.yaos)}")


@dataclass
class XIANG:
    """象：包含本卦、变卦及预测信息的完整卦象"""
    base: GUA
    change: Optional[GUA] = None
    question: str = ''
    sex: str = ''
    origin: int = 0
    year: List = field(default_factory=list)
    month: List = field(default_factory=list)
    day: List = field(default_factory=list)
    hour: List = field(default_factory=list)
    lacks: List = field(default_factory=list)
    defects: List[Reps] = field(default_factory=list)
    fortune_result: Optional[FortuneLevel] = None
    fortune_description: str = ''

    @property
    def flag(self) -> int:
        return 1 if self.change is not None else 0

    @property
    def has_change(self) -> bool:
        return self.change is not None


# =============================================================================
# 起卦函数
# =============================================================================

def get_lunar_info(dt: datetime.datetime) -> dict:
    """
    简化的公历转农历/八字信息
    当 lunar_python 不可用时使用
    """
    # 简化版的天干地支计算
    # 天干：甲1乙2丙3丁4戊5己6庚7辛8壬9癸10
    # 地支：子1丑2寅3卯4辰5巳6午7未8申9酉10戌11亥12

    year_gan = ['庚', '辛', '壬', '癸', '甲', '乙', '丙', '丁', '戊', '己']
    year_zhi = ['申', '酉', '戌', '亥', '子', '丑', '寅', '卯', '辰', '巳', '午', '未']

    month_gan = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸',
                 '甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸']
    month_zhi = ['寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥', '子', '丑']

    day_gan_cycle = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸']
    day_zhi_cycle = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥']

    hour_gan_map = {
        '甲': ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸', '甲', '乙'],
        '乙': ['丙', '丁', '戊', '己', '庚', '辛', '壬', '癸', '甲', '乙', '丙', '丁'],
        '丙': ['戊', '己', '庚', '辛', '壬', '癸', '甲', '乙', '丙', '丁', '戊', '己'],
        '丁': ['庚', '辛', '壬', '癸', '甲', '乙', '丙', '丁', '戊', '己', '庚', '辛'],
        '戊': ['壬', '癸', '甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸'],
        '己': ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸', '甲', '乙'],
        '庚': ['丙', '丁', '戊', '己', '庚', '辛', '壬', '癸', '甲', '乙', '丙', '丁'],
        '辛': ['戊', '己', '庚', '辛', '壬', '癸', '甲', '乙', '丙', '丁', '戊', '己'],
        '壬': ['庚', '辛', '壬', '癸', '甲', '乙', '丙', '丁', '戊', '己', '庚', '辛'],
        '癸': ['壬', '癸', '甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸'],
    }
    hour_zhi = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥']

    # 计算年柱（简化）
    year_idx = (dt.year - 1984) % 60
    year_gan_idx = year_idx % 10
    year_zhi_idx = year_idx % 12

    # 计算月柱
    month_gan_idx = (year_idx % 10 * 2 + dt.month + 1) % 10
    month_zhi_idx = (dt.month + 1) % 12

    # 计算日柱（简化）
    base_date = datetime.date(1900, 1, 1)
    current_date = dt.date()
    days_diff = (current_date - base_date).days
    day_gan_idx = days_diff % 10
    day_zhi_idx = days_diff % 12

    # 计算时柱
    hour_index = dt.hour // 2
    day_gan = day_gan_cycle[day_gan_idx]
    hour_gan_list = hour_gan_map.get(day_gan, hour_gan_map['甲'])
    hour_gan = hour_gan_list[hour_index]
    hour_z = hour_zhi[hour_index]

    # 计算旬空
    xun_kong_map = {
        '甲子': ['戌', '亥'], '甲戌': ['申', '酉'], '甲申': ['午', '未'],
        '甲午': ['辰', '巳'], '甲辰': ['寅', '卯'], '甲寅': ['子', '丑'],
    }
    ganzhi = day_gan_cycle[day_gan_idx] + day_zhi_cycle[day_zhi_idx]
    for key, value in xun_kong_map.items():
        if ganzhi.startswith(key[0]):
            xun_kong = value
            break
    else:
        xun_kong = ['子', '丑']

    return {
        'year': [Sky(year_gan[year_gan_idx]), Earth(year_zhi[year_zhi_idx])],
        'month': [Sky(month_gan[month_gan_idx]), Earth(month_zhi[month_zhi_idx])],
        'day': [Sky(day_gan_cycle[day_gan_idx]), Earth(day_zhi_cycle[day_zhi_idx])],
        'hour': [Sky(hour_gan), Earth(hour_z)],
        'lacks': [Earth(xun_kong[0]), Earth(xun_kong[1])],
    }


def try_lunar_python(dt: datetime.datetime) -> dict:
    """尝试使用 lunar_python，失败则使用简化版"""
    try:
        from lunar_python import Solar
        lunar = Solar.fromYmdHms(dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second).getLunar()
        date = lunar.getEightChar()

        def match_sky_enum(s: str) -> Sky:
            return Sky(s)

        def match_earth_enum(e: str) -> Earth:
            return Earth(e)

        return {
            'year': [match_sky_enum(date.getYear()[0]), match_earth_enum(date.getYear()[1])],
            'month': [match_sky_enum(date.getMonth()[0]), match_earth_enum(date.getMonth()[1])],
            'day': [match_sky_enum(date.getDay()[0]), match_earth_enum(date.getDay()[1])],
            'hour': [match_sky_enum(date.getTime()[0]), match_earth_enum(date.getTime()[1])],
            'lacks': [match_earth_enum(date.getDayXunKong()[0]), match_earth_enum(date.getDayXunKong()[1])],
        }
    except ImportError:
        return get_lunar_info(dt)


def initialization(question: str, sex: str) -> XIANG:
    """初始化起卦"""
    yaos_base = [YAO() for _ in range(6)]
    random_res = get_random_list(question, sex)

    for i in range(6):
        transfer(yaos_base[i], random_res[i])

    base = GUA(yaos=yaos_base)
    xiang = XIANG(base=base, question=question, sex=sex)
    set_date(xiang)
    return xiang


def get_random_list(question: str, sex: str) -> list[int]:
    """根据问题、性别和当前时间生成随机数列表"""
    my_string = question + sex + str(datetime.datetime.now())
    my_bytes = str.encode(my_string)
    my_hash = hashlib.sha256(my_bytes).hexdigest()
    seed = int(my_hash, 16)
    random.seed(seed)
    random_list = [random.randint(0, 10000) % 4 for _ in range(6)]
    return random_list


def transfer(y: YAO, integer: int) -> None:
    """
    将随机数转换为爻的属性
    0: 老阴 (阴爻变爻)  1: 少阴 (阴爻静爻)
    2: 少阳 (阳爻静爻)  3: 老阳 (阳爻变爻)
    """
    match integer:
        case 0:
            y.essence = 0
            y.feature = 0
        case 1:
            y.essence = 0
            y.feature = 1
        case 2:
            y.essence = 1
            y.feature = 1
        case 3:
            y.essence = 1
            y.feature = 0


def set_date(xiang: XIANG) -> None:
    """设置八字信息"""
    current = datetime.datetime.now()
    info = try_lunar_python(current)
    xiang.year = info['year']
    xiang.month = info['month']
    xiang.day = info['day']
    xiang.hour = info['hour']
    xiang.lacks = info['lacks']


# =============================================================================
# 核心算法
# =============================================================================

def deriveChange(xiang: XIANG) -> None:
    """根据本卦推导变卦"""
    has_change = any(yao.feature == 0 for yao in xiang.base.yaos)

    if has_change:
        change = GUA()
        xiang.change = change
        for i in range(len(xiang.base.yaos)):
            if xiang.base.yaos[i].feature == 0:
                change.yaos[i].feature = 0
                change.yaos[i].essence = (xiang.base.yaos[i].essence + 1) % 2
            else:
                change.yaos[i].feature = 1
                change.yaos[i].essence = xiang.base.yaos[i].essence


def seekForEgo(xiang: XIANG) -> None:
    """寻找世爻和应爻的位置"""
    base = xiang.base
    yaos = base.yaos

    sun = yaos[2].essence == yaos[5].essence
    human = yaos[1].essence == yaos[4].essence
    earth = yaos[0].essence == yaos[3].essence

    position_map = {
        (True, True, True): (5, 2),
        (False, False, False): (2, 5),
        (True, False, False): (1, 4),
        (False, True, True): (4, 1),
        (False, False, True): (3, 0),
        (True, True, False): (0, 3),
        (False, True, False): (3, 0),
    }

    ego_idx, other_idx = position_map.get((sun, human, earth), (3, 0))
    yaos[ego_idx].ego = 1
    yaos[other_idx].other = 1


def matchSkyandEarth(xiang: XIANG) -> None:
    """为本卦（及变卦）纳甲"""
    base = xiang.base
    innerMatch(base)
    outerMatch(base)
    if xiang.flag == 1:
        change = xiang.change
        innerMatch(change)
        outerMatch(change)


def innerMatch(g: GUA) -> None:
    """内卦三爻纳甲"""
    yaos = g.yaos
    trigram_value = sum(yaos[i].essence * (2 ** i) for i in range(3))
    starting_point = getStartingPoint(trigram_value, 0)
    jia = sort(starting_point, trigram_value)
    for i in range(3):
        yaos[i].najia = jia[i]


def outerMatch(g: GUA) -> None:
    """外卦三爻纳甲"""
    yaos = g.yaos
    trigram_value = sum(yaos[i].essence * (2 ** (i - 3)) for i in range(3, 6))
    starting_point = getStartingPoint(trigram_value, 1)
    jia = sort(starting_point, trigram_value)
    for i in range(3):
        yaos[i + 3].najia = jia[i]


def getStartingPoint(sum_val: int, in_or_out: int) -> list[Sky, Earth]:
    match sum_val:
        case 0:
            return [Sky.YI, Earth.WEI] if in_or_out == 0 else [Sky.GUI, Earth.CHOU]
        case 1:
            return [Sky.GENG, Earth.ZI] if in_or_out == 0 else [Sky.GENG, Earth.WU]
        case 2:
            return [Sky.WU, Earth.YIN] if in_or_out == 0 else [Sky.WU, Earth.SHEN]
        case 3:
            return [Sky.DING, Earth.SI] if in_or_out == 0 else [Sky.DING, Earth.HAI]
        case 4:
            return [Sky.BING, Earth.CHEN] if in_or_out == 0 else [Sky.BING, Earth.XU]
        case 5:
            return [Sky.JI, Earth.MAO] if in_or_out == 0 else [Sky.JI, Earth.YOU]
        case 6:
            return [Sky.XIN, Earth.CHOU] if in_or_out == 0 else [Sky.XIN, Earth.WEI]
        case 7:
            return [Sky.JIA, Earth.ZI] if in_or_out == 0 else [Sky.REN, Earth.WU]
        case _:
            raise ValueError(f"Invalid trigram value: {sum_val}, expected 0-7")


def sort(starting_point: list, trigram_value: int) -> list:
    jia1 = [starting_point[0]]
    jia2 = [starting_point[0]]
    jia = [starting_point, jia1, jia2]

    earth = starting_point[1]
    enum = list(Earth.__members__.values())
    starting_index = enum.index(earth)

    if trigram_value in [1, 2, 4, 7]:
        e1 = (starting_index + 2) % 12
        e2 = (starting_index + 4) % 12
    else:
        e1 = (starting_index - 2) % 12
        e2 = (starting_index - 4) % 12

    earth1 = Earth(enum[e1])
    earth2 = Earth(enum[e2])
    jia1.append(earth1)
    jia2.append(earth2)
    return jia


def seekForReps(xiang: XIANG) -> None:
    """寻找六亲关系"""
    xiang.origin = seekForOrigin(xiang.base)

    palace_element_map = {
        7: 0, 3: 0,  # 乾、兑属金
        2: 1,        # 坎属水
        4: 2, 0: 2,  # 艮、坤属土
        1: 3, 6: 3,  # 震、巽属木
        5: 4         # 离属火
    }
    element = palace_element_map.get(xiang.origin, 0)

    for yao in xiang.base.yaos:
        findReps(element, yao)
    if xiang.flag == 1:
        for yao in xiang.change.yaos:
            findReps(element, yao)


def seekForOrigin(g: GUA) -> int:
    """寻找卦宫"""
    yaos = g.yaos
    tian = yaos[2].essence == yaos[5].essence
    ren = yaos[1].essence == yaos[4].essence
    di = yaos[0].essence == yaos[3].essence

    if tian and ren and di:
        return sum(yaos[i].essence * (2 ** i) for i in range(3))

    if tian and not ren and di:
        return sum(yaos[i].essence * (2 ** i) for i in range(3))

    ego_pos = next((i for i, y in enumerate(yaos) if y.ego == 1), 0)

    if ego_pos <= 2:
        return sum(yaos[i + 3].essence * (2 ** i) for i in range(3))
    else:
        return sum((1 - yaos[i].essence) * (2 ** i) for i in range(3))


def _get_earth_element(earth: Earth) -> int:
    """获取地支对应的五行：金0木3水1火4土2"""
    element_map = {
        Earth.SHEN: 0, Earth.YOU: 0,
        Earth.YIN: 3, Earth.MAO: 3,
        Earth.ZI: 1, Earth.HAI: 1,
        Earth.SI: 4, Earth.WU: 4,
        Earth.CHEN: 2, Earth.XU: 2, Earth.CHOU: 2, Earth.WEI: 2,
    }
    return element_map.get(earth, 2)


def _is_generating(from_elem: int, to_elem: int) -> bool:
    generating = {0: 1, 1: 3, 3: 4, 4: 2, 2: 0}
    return generating.get(from_elem) == to_elem


def _is_overcoming(from_elem: int, to_elem: int) -> bool:
    overcoming = {0: 3, 3: 2, 2: 1, 1: 4, 4: 0}
    return overcoming.get(from_elem) == to_elem


def findReps(element: int, yao: YAO) -> None:
    """确定单个爻的六亲"""
    if not yao.najia or len(yao.najia) < 2:
        yao.representation = Reps.XIONG
        return

    earth = yao.najia[1]
    earth_element = _get_earth_element(earth)

    if earth_element == element:
        yao.representation = Reps.XIONG
    elif _is_generating(earth_element, element):
        yao.representation = Reps.FU
    elif _is_generating(element, earth_element):
        yao.representation = Reps.ZI
    elif _is_overcoming(earth_element, element):
        yao.representation = Reps.GUAN
    elif _is_overcoming(element, earth_element):
        yao.representation = Reps.QI
    else:
        yao.representation = Reps.XIONG


def seekForDefects(xiang: XIANG) -> None:
    """找出本卦中缺失的六亲"""
    found = {y.representation for y in xiang.base.yaos}
    all_reps = {Reps.FU, Reps.GUAN, Reps.XIONG, Reps.ZI, Reps.QI}
    xiang.defects = list(all_reps - found)


def seekForSouls(xiang: XIANG) -> None:
    """寻找六神位置"""
    sky = xiang.day[0]

    origin_soul = Soul.WU
    if sky in [Sky.JIA, Sky.YI]:
        origin_soul = Soul.LONG
    elif sky in [Sky.BING, Sky.DING]:
        origin_soul = Soul.QUE
    elif sky == Sky.WU:
        origin_soul = Soul.CHEN
    elif sky == Sky.JI:
        origin_soul = Soul.SHE
    elif sky in [Sky.GENG, Sky.XIN]:
        origin_soul = Soul.HU

    enum = list(Soul.__members__.values())
    starting_index = enum.index(origin_soul)
    yaos = xiang.base.yaos

    for i in range(6):
        yaos[i].soul = Soul(enum[(starting_index + i) % 6])


def judgeFortune(xiang: XIANG) -> None:
    """判断卦象的吉凶"""
    score = 0
    reasons = []

    if xiang.change is not None:
        score -= 5
        reasons.append("有变爻，事情有变动")

    ego_yao = next((y for y in xiang.base.yaos if y.ego == 1), None)
    if ego_yao:
        if ego_yao.representation == Reps.FU:
            score += 5
            reasons.append("世爻临父母，得庇护")
        elif ego_yao.representation == Reps.QI:
            score += 8
            reasons.append("世爻临妻财，财运亨通")
        elif ego_yao.representation == Reps.GUAN:
            score -= 3
            reasons.append("世爻临官鬼，多忧愁")
        elif ego_yao.representation == Reps.ZI:
            score += 6
            reasons.append("世爻临子孙，万事无忧")
        elif ego_yao.representation == Reps.XIONG:
            score -= 5
            reasons.append("世爻临兄弟，主消耗")

    yongshen = _getYongShen(xiang)
    if yongshen:
        if ego_yao and ego_yao.representation == yongshen:
            score += 10
            reasons.append(f"用神{yongshen.value}持世，大吉")
        else:
            yongshen_present = any(y.representation == yongshen for y in xiang.base.yaos)
            if yongshen_present:
                score += 5
                reasons.append(f"卦中有{yongshen.value}，凡事可成")
            else:
                score -= 8
                reasons.append(f"卦中不见{yongshen.value}，难求")

    if len(xiang.defects) == 0:
        score += 3
        reasons.append("六亲俱全，万事顺遂")
    else:
        score -= 3
        if yongshen and yongshen in xiang.defects:
            score -= 10
            reasons.append(f"用神{yongshen.value}不上卦，大凶")
        else:
            reasons.append(f"缺{xiang.defects[0].value if xiang.defects else '六亲'}，略有不足")

    if ego_yao and ego_yao.soul:
        soul_scores = {
            Soul.LONG: 5, Soul.QUE: -2, Soul.CHEN: -1,
            Soul.SHE: -3, Soul.HU: -5, Soul.WU: -3,
        }
        score += soul_scores.get(ego_yao.soul, 0)
        if soul_scores.get(ego_yao.soul, 0) > 0:
            reasons.append(f"世爻临{ego_yao.soul.value}，多吉庆")
        elif soul_scores.get(ego_yao.soul, 0) < 0:
            reasons.append(f"世爻临{ego_yao.soul.value}，需谨慎")

    is_inner_pure = all(y.essence == xiang.base.yaos[0].essence for y in xiang.base.yaos[:3])
    is_outer_pure = all(y.essence == xiang.base.yaos[3].essence for y in xiang.base.yaos[3:])
    if is_inner_pure and is_outer_pure:
        score += 8
        reasons.append("八纯之卦，根气深厚")

    xiang.fortune_result = _getFortuneLevel(score)
    xiang.fortune_description = "；".join(reasons) if reasons else "平卦，凡事守旧为宜"


def _getYongShen(xiang: XIANG) -> Reps:
    """根据所占事项确定用神"""
    question = xiang.question.lower()

    if any(kw in question for kw in ['财', '钱', '金', '婚', '妻', '利', '得', '失', '买卖', '生意', '经营']):
        return Reps.QI
    if any(kw in question for kw in ['官', '职', '考', '名', '病', '灾', '鬼', '盗', '工作', '提拔']):
        return Reps.GUAN
    if any(kw in question for kw in ['父', '母', '屋', '房', '车', '书', '印', '文', '师', '学', '试']):
        return Reps.FU
    if any(kw in question for kw in ['子', '孙', '儿', '女', '药', '医', '行', '解', '乐']):
        return Reps.ZI
    if any(kw in question for kw in ['兄', '弟', '友', '朋', '合', '竞', '赛', '比']):
        return Reps.XIONG
    return Reps.QI


def _getFortuneLevel(score: int) -> FortuneLevel:
    if score >= 20:
        return FortuneLevel.DA_JI
    elif score >= 10:
        return FortuneLevel.JI
    elif score >= 5:
        return FortuneLevel.XIAO_JI
    elif score >= -4:
        return FortuneLevel.PING
    elif score >= -10:
        return FortuneLevel.XIAO_XIONG
    elif score >= -15:
        return FortuneLevel.XIONG
    else:
        return FortuneLevel.DA_XIONG


# =============================================================================
# Skill 主类
# =============================================================================

class LiuyaoSkill:
    """六爻预测Skill主类 - 独立版本"""

    PALACE_NAMES = {
        0: "坤宫", 1: "震宫", 2: "坎宫", 3: "兑宫",
        4: "艮宫", 5: "离宫", 6: "巽宫", 7: "乾宫"
    }

    TRIGRAM_NAMES = {
        0: "坤", 1: "震", 2: "坎", 3: "兑",
        4: "艮", 5: "离", 6: "巽", 7: "乾"
    }

    def __init__(self):
        self.xiang = None

    def divinate(self, question: str, sex: str = "男") -> dict:
        """执行六爻预测"""
        self.xiang = initialization(question, sex)
        deriveChange(self.xiang)
        seekForEgo(self.xiang)
        matchSkyandEarth(self.xiang)
        seekForReps(self.xiang)
        seekForDefects(self.xiang)
        seekForSouls(self.xiang)
        judgeFortune(self.xiang)
        return self._format_result()

    def _format_result(self) -> dict:
        """格式化预测结果为字典"""
        x = self.xiang

        base_yaos = []
        for i in range(5, -1, -1):
            yao = x.base.yaos[i]
            line_type = "⚊" if yao.essence == 1 else "⚋"
            if yao.feature == 0:
                line_type += " ○" if yao.essence == 1 else " ×"

            base_yaos.append({
                'position': ['上爻', '五爻', '四爻', '三爻', '二爻', '初爻'][5-i],
                'index': i + 1,
                'line': line_type,
                'essence': '阳' if yao.essence == 1 else '阴',
                'feature': '老' if yao.feature == 0 else '少',
                'najia': yao.najia,
                'representation': yao.representation.value if yao.representation else None,
                'soul': yao.soul.value if yao.soul else None,
                'is_ego': yao.ego == 1,
                'is_other': yao.other == 1,
            })

        change_yaos = None
        if x.change:
            change_yaos = []
            for i in range(5, -1, -1):
                yao = x.change.yaos[i]
                line_type = "⚊" if yao.essence == 1 else "⚋"
                change_yaos.append({
                    'position': ['上爻', '五爻', '四爻', '三爻', '二爻', '初爻'][5-i],
                    'index': i + 1,
                    'line': line_type,
                    'representation': yao.representation.value if yao.representation else None,
                })

        inner_trigram = sum(x.base.yaos[i].essence * (2 ** i) for i in range(3))
        outer_trigram = sum(x.base.yaos[i].essence * (2 ** (i - 3)) for i in range(3, 6))

        ego_pos = next((i+1 for i, y in enumerate(x.base.yaos) if y.ego == 1), 0)
        other_pos = next((i+1 for i, y in enumerate(x.base.yaos) if y.other == 1), 0)

        year_str = f"{x.year[0].value}{x.year[1].value}" if len(x.year) >= 2 and hasattr(x.year[0], 'value') else \
                   f"{x.year[0]}{x.year[1]}" if len(x.year) >= 2 else ""
        month_str = f"{x.month[0].value}{x.month[1].value}" if len(x.month) >= 2 and hasattr(x.month[0], 'value') else \
                    f"{x.month[0]}{x.month[1]}" if len(x.month) >= 2 else ""
        day_str = f"{x.day[0].value}{x.day[1].value}" if len(x.day) >= 2 and hasattr(x.day[0], 'value') else \
                  f"{x.day[0]}{x.day[1]}" if len(x.day) >= 2 else ""
        hour_str = f"{x.hour[0].value}{x.hour[1].value}" if len(x.hour) >= 2 and hasattr(x.hour[0], 'value') else \
                   f"{x.hour[0]}{x.hour[1]}" if len(x.hour) >= 2 else ""

        lacks_str = "".join([e.value for e in x.lacks if hasattr(e, 'value')]) if x.lacks else ""
        if not lacks_str and x.lacks:
            lacks_str = "".join([str(e) for e in x.lacks])
        defects_str = [d.value for d in x.defects] if x.defects else []

        return {
            'question': x.question,
            'sex': x.sex,
            'date': {'year': year_str, 'month': month_str, 'day': day_str, 'hour': hour_str},
            'lacks': lacks_str,
            'base_gua': {
                'name': f"{self.TRIGRAM_NAMES.get(outer_trigram, '未知')}{self.TRIGRAM_NAMES.get(inner_trigram, '未知')}",
                'inner': self.TRIGRAM_NAMES.get(inner_trigram, '未知'),
                'outer': self.TRIGRAM_NAMES.get(outer_trigram, '未知'),
                'yaos': base_yaos,
            },
            'change_gua': {'yaos': change_yaos} if change_yaos else None,
            'palace': self.PALACE_NAMES.get(x.origin, '未知'),
            'ego_position': ego_pos,
            'other_position': other_pos,
            'defects': defects_str,
            'fortune': {
                'level': x.fortune_result.value if x.fortune_result else None,
                'description': x.fortune_description,
            },
            'has_change': x.has_change,
        }

    def format_text(self, result: dict = None) -> str:
        """将结果格式化为易读的文本格式"""
        if result is None:
            result = self._format_result()

        lines = []
        lines.append("=" * 60)
        lines.append("【六爻预测结果】")
        lines.append("=" * 60)
        lines.append("")
        lines.append(f"占卜问题：{result['question']}")
        lines.append(f"卦主性别：{result['sex']}")
        lines.append("")
        d = result['date']
        lines.append(f"日期：{d['year']}年 {d['month']}月 {d['day']}日 {d['hour']}时")
        lines.append(f"旬空：{result['lacks'] or '无'}")
        lines.append("")
        lines.append("-" * 60)
        lines.append("【本卦】")
        lines.append(f"卦名：{result['base_gua']['name']}")
        lines.append(f"外卦（上）：{result['base_gua']['outer']}，内卦（下）：{result['base_gua']['inner']}")
        lines.append("")
        lines.append("爻象（从上至下）：")
        for yao in result['base_gua']['yaos']:
            mark = " 【世】" if yao['is_ego'] else " 【应】" if yao['is_other'] else ""
            najia_str = f"{yao['najia'][0].value}{yao['najia'][1].value}" if yao['najia'] and len(yao['najia']) >= 2 else ""
            line = f"  {yao['position']}：{yao['line']:8} {najia_str:6} {yao['representation'] or '':4} {yao['soul'] or '':4}{mark}"
            lines.append(line)
        lines.append("")

        if result['change_gua']:
            lines.append("-" * 60)
            lines.append("【变卦】")
            for yao in result['change_gua']['yaos']:
                lines.append(f"  {yao['position']}：{yao['line']:8} {yao['representation'] or ''}")
            lines.append("")

        lines.append("-" * 60)
        lines.append("【卦象分析】")
        lines.append(f"卦宫：{result['palace']}")
        lines.append(f"世爻：第{result['ego_position']}爻")
        lines.append(f"应爻：第{result['other_position']}爻")
        if result['defects']:
            lines.append(f"缺失六亲：{', '.join(result['defects'])}")
        else:
            lines.append("六亲：齐全")
        lines.append("")
        lines.append("=" * 60)
        lines.append(f"【吉凶判断】{result['fortune']['level']}")
        lines.append("=" * 60)
        lines.append(result['fortune']['description'])

        return "\n".join(lines)


def main():
    """命令行入口"""
    import argparse
    parser = argparse.ArgumentParser(description='六爻预测工具')
    parser.add_argument('question', nargs='?', default='占问前程', help='所占事项')
    parser.add_argument('--sex', '-s', default='男', help='卦主性别（男/女）')
    args = parser.parse_args()

    skill = LiuyaoSkill()
    result = skill.divinate(args.question, args.sex)
    print(skill.format_text(result))


if __name__ == "__main__":
    main()
