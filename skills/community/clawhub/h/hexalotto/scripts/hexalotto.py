#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HexaLotto V2.0 六爻奇门测彩 · 多彩种引擎
==========================================
支持双色球(SSQ)、大乐透(DLT)、六合彩(MARK6)三大彩种。
核心引擎通用六爻状态机，输出端按彩种路由差异化映射。

纯属娱乐与中国传统术数文化演示，不构成任何投资或博彩建议。
"""

import argparse
import json
import sys
from datetime import datetime, date

# ============================================================
# 第一部分：基础常量
# ============================================================

TIAN_GAN = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸']
DI_ZHI = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥']
SHENG_XIAO = ['鼠', '牛', '虎', '兔', '龙', '蛇', '马', '羊', '猴', '鸡', '狗', '猪']
ZHI_TO_XIAO = dict(zip(DI_ZHI, SHENG_XIAO))
XIAO_TO_ZHI = dict(zip(SHENG_XIAO, DI_ZHI))

ZHI_TO_WUXING = {
    '子': '水', '丑': '土', '寅': '木', '卯': '木',
    '辰': '土', '巳': '火', '午': '火', '未': '土',
    '申': '金', '酉': '金', '戌': '土', '亥': '水'
}

WUXING_SHENG = {'木': '火', '火': '土', '土': '金', '金': '水', '水': '木'}
WUXING_KE   = {'木': '土', '土': '水', '水': '火', '火': '金', '金': '木'}
WUXING_BEI_KE = {v: k for k, v in WUXING_KE.items()}
WUXING_MU = {'木': '未', '火': '戌', '金': '丑', '水': '辰', '土': '辰'}

LIU_HE = {
    '子': '丑', '丑': '子', '寅': '亥', '卯': '戌',
    '辰': '酉', '巳': '申', '午': '未', '未': '午',
    '申': '巳', '酉': '辰', '戌': '卯', '亥': '寅'
}

LIU_CHONG = {
    '子': '午', '午': '子', '丑': '未', '未': '丑',
    '寅': '申', '申': '寅', '卯': '酉', '酉': '卯',
    '辰': '戌', '戌': '辰', '巳': '亥', '亥': '巳'
}

XIANTIAN_GUA = {1: '乾', 2: '兑', 3: '离', 4: '震', 5: '巽', 6: '坎', 7: '艮', 8: '坤'}

GUA_XIANG = {
    '乾': (1, 1, 1), '兑': (0, 1, 1), '离': (1, 0, 1), '震': (0, 0, 1),
    '巽': (1, 1, 0), '坎': (0, 1, 0), '艮': (1, 0, 0), '坤': (0, 0, 0)
}

# 先天八卦数 -> 四象 (四象名, 阴阳值1阳0阴, 是否动爻)
SIXIANG_MAP = {
    1: ('老阳', 1, True),   2: ('少阴', 0, False),
    3: ('少阳', 1, False),  4: ('老阴', 0, True),
    5: ('老阳', 1, True),   6: ('少阳', 1, False),
    7: ('少阴', 0, False),  8: ('老阴', 0, True),
}

# 纳甲表
NAJIA_TABLE = {
    '乾': {'inner': ['子', '寅', '辰'], 'outer': ['午', '申', '戌'],
            'stem_inner': '甲', 'stem_outer': '壬', 'wuxing': '金'},
    '坤': {'inner': ['未', '巳', '卯'], 'outer': ['丑', '亥', '酉'],
            'stem_inner': '乙', 'stem_outer': '癸', 'wuxing': '土'},
    '震': {'inner': ['子', '寅', '辰'], 'outer': ['午', '申', '戌'],
            'stem_inner': '庚', 'stem_outer': '庚', 'wuxing': '木'},
    '巽': {'inner': ['丑', '亥', '酉'], 'outer': ['未', '巳', '卯'],
            'stem_inner': '辛', 'stem_outer': '辛', 'wuxing': '木'},
    '坎': {'inner': ['寅', '辰', '午'], 'outer': ['申', '戌', '子'],
            'stem_inner': '戊', 'stem_outer': '戊', 'wuxing': '水'},
    '离': {'inner': ['卯', '丑', '亥'], 'outer': ['酉', '未', '巳'],
            'stem_inner': '己', 'stem_outer': '己', 'wuxing': '火'},
    '艮': {'inner': ['辰', '午', '申'], 'outer': ['戌', '子', '寅'],
            'stem_inner': '丙', 'stem_outer': '丙', 'wuxing': '土'},
    '兑': {'inner': ['巳', '卯', '丑'], 'outer': ['亥', '酉', '未'],
            'stem_inner': '丁', 'stem_outer': '丁', 'wuxing': '金'},
}

# 64卦名
GUA_NAME_TABLE = {
    ('乾', '乾'): '乾为天', ('坤', '坤'): '坤为地',
    ('坎', '坎'): '坎为水', ('离', '离'): '离为火',
    ('震', '震'): '震为雷', ('巽', '巽'): '巽为风',
    ('艮', '艮'): '艮为山', ('兑', '兑'): '兑为泽',
    ('坎', '乾'): '水天需', ('乾', '坎'): '天水讼',
    ('坤', '坎'): '地水师', ('坎', '坤'): '水地比',
    ('巽', '乾'): '风天小畜', ('乾', '兑'): '天泽履',
    ('坤', '乾'): '地天泰', ('乾', '坤'): '天地否',
    ('离', '乾'): '火天大有', ('乾', '离'): '天火同人',
    ('坤', '艮'): '地山谦', ('震', '坤'): '雷地豫',
    ('兑', '震'): '泽雷随', ('艮', '巽'): '山风蛊',
    ('坤', '兑'): '地泽临', ('巽', '坤'): '风地观',
    ('离', '震'): '火雷噬嗑', ('艮', '离'): '山火贲',
    ('艮', '坤'): '山地剥', ('坤', '震'): '地雷复',
    ('乾', '震'): '天雷无妄', ('艮', '乾'): '山天大畜',
    ('艮', '震'): '山雷颐', ('兑', '巽'): '泽风大过',
    ('坎', '离'): '水火既济', ('离', '坎'): '火水未济',
    ('离', '兑'): '火泽睽', ('巽', '离'): '风火家人',
    ('艮', '坎'): '山水蒙', ('坎', '震'): '水雷屯',
    ('巽', '坎'): '风水涣', ('坎', '兑'): '水泽节',
    ('巽', '兑'): '风泽中孚', ('震', '艮'): '雷山小过',
    ('震', '离'): '雷火丰', ('离', '艮'): '火山旅',
    ('坎', '巽'): '水风井', ('震', '坎'): '雷水解',
    ('艮', '兑'): '山泽损', ('巽', '震'): '风雷益',
    ('兑', '乾'): '泽天夬', ('乾', '巽'): '天风姤',
    ('兑', '坤'): '泽地萃', ('坤', '巽'): '地风升',
    ('兑', '坎'): '泽水困', ('震', '巽'): '雷风恒',
    ('巽', '艮'): '风山渐', ('震', '兑'): '雷泽归妹',
    ('震', '乾'): '雷天大壮', ('乾', '艮'): '天山遁',
    ('离', '坤'): '火地晋', ('坤', '离'): '地火明夷',
    ('离', '巽'): '火风鼎', ('兑', '艮'): '泽山咸',
    ('坎', '艮'): '水山蹇',
}


# ============================================================
# 第二部分：彩种特码映射表
# ============================================================

# --- 双色球蓝球 (1~16) ---
# mod 12 循环叠加：子01,13  丑02,14  寅03,15  卯04,16  辰~亥 单对应
SSQ_BLUE_MAP = {
    '子': [1, 13], '丑': [2, 14], '寅': [3, 15], '卯': [4, 16],
    '辰': [5],     '巳': [6],     '午': [7],     '未': [8],
    '申': [9],     '酉': [10],    '戌': [11],    '亥': [12],
}

# --- 大乐透后区 (1~12) ---
# 1:1 绝对映射
DLT_BACK_MAP = {
    '子': [1],  '丑': [2],  '寅': [3],  '卯': [4],
    '辰': [5],  '巳': [6],  '午': [7],  '未': [8],
    '申': [9],  '酉': [10], '戌': [11], '亥': [12],
}

# --- 六合彩 动态生肖表 ---
MARK6_PRESET_TABLES = {
    2025: {
        '蛇': [1, 13, 25, 37, 49], '龙': [2, 14, 26, 38],
        '兔': [3, 15, 27, 39],     '虎': [4, 16, 28, 40],
        '牛': [5, 17, 29, 41],     '鼠': [6, 18, 30, 42],
        '猪': [7, 19, 31, 43],     '狗': [8, 20, 32, 44],
        '鸡': [9, 21, 33, 45],     '猴': [10, 22, 34, 46],
        '羊': [11, 23, 35, 47],    '马': [12, 24, 36, 48],
    },
    2026: {
        '马': [1, 13, 25, 37, 49], '蛇': [2, 14, 26, 38],
        '龙': [3, 15, 27, 39],     '兔': [4, 16, 28, 40],
        '虎': [5, 17, 29, 41],     '牛': [6, 18, 30, 42],
        '鼠': [7, 19, 31, 43],     '猪': [8, 20, 32, 44],
        '狗': [9, 21, 33, 45],     '鸡': [10, 22, 34, 46],
        '猴': [11, 23, 35, 47],    '羊': [12, 24, 36, 48],
    },
}

def _build_mark6_year_table(year):
    """动态生成六合彩某年的生肖号码对照表(1-49)"""
    tai_sui_idx = (year - 4) % 12
    table = {}
    for num in range(1, 50):
        xiao_idx = (tai_sui_idx - (num - 1)) % 12
        xiao = SHENG_XIAO[xiao_idx]
        table.setdefault(xiao, []).append(num)
    return table

def get_mark6_map(year):
    """获取六合彩当年 地支->号码 映射"""
    if year in MARK6_PRESET_TABLES:
        return {XIAO_TO_ZHI.get(x, '?'): ns for x, ns in MARK6_PRESET_TABLES[year].items()}
    xiao_table = _build_mark6_year_table(year)
    return {XIAO_TO_ZHI.get(x, '?'): ns for x, ns in xiao_table.items()}

# --- V1 兼容：红球/前区映射（报告参考用） ---
SSQ_RED_MAP = {
    '子': [1, 13, 25],  '丑': [2, 14, 26], '寅': [3, 15, 27], '卯': [4, 16, 28],
    '辰': [5, 17, 29],  '巳': [6, 18, 30], '午': [7, 19, 31], '未': [8, 20, 32],
    '申': [9, 21, 33],  '酉': [10, 22],    '戌': [11, 23],    '亥': [12, 24],
}
DLT_FRONT_MAP = {
    '子': [1, 13, 25],  '丑': [2, 14, 26], '寅': [3, 15, 27], '卯': [4, 16, 28],
    '辰': [5, 17, 29],  '巳': [6, 18, 30], '午': [7, 19, 31], '未': [8, 20, 32],
    '申': [9, 21, 33],  '酉': [10, 22, 34],'戌': [11, 23, 35],'亥': [12, 24],
}


# ============================================================
# 第三部分：干支历法
# ============================================================

REF_DATE = date(2000, 1, 7)
REF_DAY_GANZHI_IDX = 16  # 庚辰

def ganzhi_from_idx(idx):
    idx = idx % 60
    return TIAN_GAN[idx % 10] + DI_ZHI[idx % 12]

def day_ganzhi(target_date):
    if isinstance(target_date, str):
        target_date = datetime.strptime(target_date, '%Y-%m-%d').date()
    delta = (target_date - REF_DATE).days
    idx = (REF_DAY_GANZHI_IDX + delta) % 60
    return ganzhi_from_idx(idx), idx

def year_ganzhi(year):
    idx = (year - 4) % 60
    return ganzhi_from_idx(idx), idx

def month_ganzhi(year, month):
    month_zhi_map = {1:1, 2:2, 3:3, 4:4, 5:5, 6:6, 7:7, 8:8, 9:9, 10:10, 11:11, 12:0}
    zhi_idx = month_zhi_map[month]
    year_gan_idx = (year - 4) % 10
    month_gan_base = {0:2, 5:2, 1:4, 6:4, 2:6, 7:6, 3:8, 8:8, 4:0, 9:0}
    base = month_gan_base[year_gan_idx]
    gan_idx = (base + (zhi_idx - 2)) % 10
    return TIAN_GAN[gan_idx] + DI_ZHI[zhi_idx], zhi_idx

def hour_ganzhi(day_gan_idx, hour):
    hour_zhi_idx = ((hour + 1) // 2) % 12
    day_gan = day_gan_idx % 10
    hour_gan_base = {0:0, 5:0, 1:2, 6:2, 2:4, 7:4, 3:6, 8:6, 4:8, 9:8}
    gan_idx = (hour_gan_base[day_gan] + hour_zhi_idx) % 10
    return TIAN_GAN[gan_idx] + DI_ZHI[hour_zhi_idx], hour_zhi_idx

def calc_xunkong(day_gz_idx):
    xun_start = (day_gz_idx // 10) * 10
    start_zhi = xun_start % 12
    kong1 = (start_zhi + 10) % 12
    kong2 = (start_zhi + 11) % 12
    return DI_ZHI[kong1], DI_ZHI[kong2]


# ============================================================
# 第四部分：多彩种输入适配器
# ============================================================

LOTTERY_NAMES = {'ssq': '双色球', 'dlt': '大乐透', 'mark6': '六合彩'}

def adapt_input(raw_numbers, lottery_type, target_date=None, dlt_strategy='A'):
    """
    将不同彩种的原始输入适配为统一的6个起卦数字。
    SSQ:   6个红球 -> 直接使用
    MARK6: 6个平码 -> 直接使用
    DLT:   5个前区 -> 策略A(求和) 或 策略B(干支借位)
    """
    if lottery_type in ('ssq', 'mark6'):
        if len(raw_numbers) != 6:
            raise ValueError(f"{LOTTERY_NAMES[lottery_type]}需要恰好6个平码/红球")
        return raw_numbers, "直接使用6个平码/红球起卦"

    elif lottery_type == 'dlt':
        if len(raw_numbers) == 6:
            return raw_numbers, "大乐透已提供6个号码，直接使用"
        if len(raw_numbers) != 5:
            raise ValueError("大乐透需要5个前区号码（系统自动补第6爻）")

        if dlt_strategy == 'A':
            sixth = sum(raw_numbers)
            note = f"策略A求和衍生：第6爻={'+'.join(map(str, raw_numbers))}={sixth}"
            return raw_numbers + [sixth], note
        else:
            if target_date is None:
                target_date = date.today()
            _, gz_idx = day_ganzhi(target_date)
            sixth = (gz_idx % 60) + 1
            note = f"策略B干支借位：第6爻取日柱{ganzhi_from_idx(gz_idx)}代数={sixth}"
            return raw_numbers + [sixth], note

    raise ValueError(f"不支持的彩种：{lottery_type}")


# ============================================================
# 第五部分：起卦与排盘
# ============================================================

def numbers_to_yao(numbers):
    if len(numbers) != 6:
        raise ValueError("需要恰好6个起卦数字")
    yaos = []
    for i, n in enumerate(numbers):
        mod8 = n % 8 or 8
        gua_name = XIANTIAN_GUA[mod8]
        sixiang_name, yinyang, is_dong = SIXIANG_MAP[mod8]
        changed = (1 - yinyang) if is_dong else yinyang
        yaos.append({
            'pos': i, 'number': n, 'mod8': mod8,
            'gua_name': gua_name, 'sixiang': sixiang_name,
            'yinyang': yinyang, 'is_dong': is_dong, 'changed_yy': changed,
        })
    return yaos

def build_hexagram(yaos):
    lower_lines = tuple(y['yinyang'] for y in yaos[:3])
    upper_lines = tuple(y['yinyang'] for y in yaos[3:])
    changed_lower = tuple(y['changed_yy'] for y in yaos[:3])
    changed_upper = tuple(y['changed_yy'] for y in yaos[3:])

    def lines_to_gua(lines):
        for name, pattern in GUA_XIANG.items():
            if pattern == lines:
                return name
        return '未知'

    lg, ug = lines_to_gua(lower_lines), lines_to_gua(upper_lines)
    clg, cug = lines_to_gua(changed_lower), lines_to_gua(changed_upper)
    return {
        'lower_gua': lg, 'upper_gua': ug,
        'ben_gua_name': GUA_NAME_TABLE.get((ug, lg), f'{ug}上{lg}下'),
        'changed_lower_gua': clg, 'changed_upper_gua': cug,
        'bian_gua_name': GUA_NAME_TABLE.get((cug, clg), f'{cug}上{clg}下'),
        'has_dong': any(y['is_dong'] for y in yaos),
    }

def assign_najia(yaos, hexagram):
    lower, upper = hexagram['lower_gua'], hexagram['upper_gua']
    cl, cu = hexagram['changed_lower_gua'], hexagram['changed_upper_gua']
    ld, ud = NAJIA_TABLE[lower], NAJIA_TABLE[upper]
    cld, cud = NAJIA_TABLE[cl], NAJIA_TABLE[cu]

    for i in range(3):
        yaos[i]['najia_zhi'] = ld['inner'][i]
        yaos[i]['najia_gan'] = ld['stem_inner']
        yaos[i]['najia_wuxing'] = ZHI_TO_WUXING[ld['inner'][i]]
    for i in range(3):
        yaos[i+3]['najia_zhi'] = ud['outer'][i]
        yaos[i+3]['najia_gan'] = ud['stem_outer']
        yaos[i+3]['najia_wuxing'] = ZHI_TO_WUXING[ud['outer'][i]]

    for i in range(3):
        if yaos[i]['is_dong']:
            yaos[i]['bian_zhi'] = cld['inner'][i]
            yaos[i]['bian_wuxing'] = ZHI_TO_WUXING[cld['inner'][i]]
        else:
            yaos[i]['bian_zhi'] = yaos[i]['bian_wuxing'] = None
    for i in range(3):
        if yaos[i+3]['is_dong']:
            yaos[i+3]['bian_zhi'] = cud['outer'][i]
            yaos[i+3]['bian_wuxing'] = ZHI_TO_WUXING[cud['outer'][i]]
        else:
            yaos[i+3]['bian_zhi'] = yaos[i+3]['bian_wuxing'] = None
    return yaos


# ============================================================
# 第六部分：断卦引擎（通用核心）
# ============================================================

def get_wuxing_relation(source_wx, target_wx):
    if source_wx == target_wx: return '同'
    if WUXING_SHENG.get(source_wx) == target_wx: return '生'
    if WUXING_KE.get(source_wx) == target_wx: return '克'
    if WUXING_SHENG.get(target_wx) == source_wx: return '被生'
    if WUXING_KE.get(target_wx) == source_wx: return '被克'
    return '无'

def evaluate_wang_shuai(yao_wx, month_zhi, day_zhi):
    month_wx, day_wx = ZHI_TO_WUXING[month_zhi], ZHI_TO_WUXING[day_zhi]
    def _state(rel):
        if rel in ('同', '生'): return '旺'
        if rel == '被生': return '相'
        if rel == '被克': return '休'
        if rel == '克': return '囚'
        return '死'
    m = _state(get_wuxing_relation(month_wx, yao_wx))
    d = _state(get_wuxing_relation(day_wx, yao_wx))
    smap = {'旺': 2, '相': 1, '休': 0, '囚': -1, '死': -2}
    total = smap.get(m, 0) + smap.get(d, 0)
    if total >= 3:   o = '极旺'
    elif total >= 1:  o = '偏旺'
    elif total == 0:  o = '平衡'
    elif total >= -2: o = '偏衰'
    else:             o = '极衰'
    return m, d, o, total

def check_special_states(yao, month_zhi, day_zhi, kong1, kong2, all_yaos):
    zhi = yao['najia_zhi']
    yao_wx = yao['najia_wuxing']
    st = []
    if zhi in (kong1, kong2):            st.append('旬空')
    if LIU_CHONG.get(month_zhi) == zhi:  st.append('月破')
    if LIU_CHONG.get(day_zhi) == zhi:    st.append('日冲')
    if LIU_HE.get(day_zhi) == zhi:       st.append('日合')
    if LIU_HE.get(month_zhi) == zhi:     st.append('月合')

    mu_zhi = WUXING_MU.get(yao_wx)
    if mu_zhi == day_zhi:
        st.append('入日墓')
    for other in all_yaos:
        if other['is_dong'] and other.get('bian_zhi') == mu_zhi:
            st.append('入动变墓'); break

    # V2 新增：动变关系（回头生、回头克、化合绊）
    if yao['is_dong'] and yao.get('bian_wuxing'):
        bwx = yao['bian_wuxing']
        rel = get_wuxing_relation(bwx, yao_wx)
        if rel == '生': st.append('回头生')
        elif rel == '克': st.append('回头克')
        if yao.get('bian_zhi') and LIU_HE.get(yao['bian_zhi']) == zhi:
            st.append('化合绊')

    for other in all_yaos:
        if other['is_dong'] and other['pos'] != yao['pos']:
            if LIU_HE.get(other['najia_zhi']) == zhi:
                st.append('被动爻合'); break
    return st

def find_yingqi(yao, month_zhi, day_zhi, kong1, kong2, all_yaos):
    zhi = yao['najia_zhi']
    yao_wx = yao['najia_wuxing']
    is_dong = yao['is_dong']
    states = yao.get('special_states', [])
    strength = yao.get('strength_score', 0)
    R, RS = [], []

    # A: 静爻衰败 -> 逢值逢冲
    if not is_dong and strength <= 0:
        R.append(zhi); RS.append(f'静爻偏衰，逢值({zhi})')
        ch = LIU_CHONG.get(zhi)
        if ch: R.append(ch); RS.append(f'静爻偏衰，逢冲({ch})')

    # B: 动爻合绊 -> 冲破
    if is_dong and ('被动爻合' in states or '化合绊' in states):
        he = LIU_HE.get(zhi)
        if he:
            ch = LIU_CHONG.get(he)
            if ch: R.append(ch); RS.append(f'合绊，冲破({ch})')
        R.append(zhi); RS.append(f'合绊，逢值({zhi})')

    # C: 入墓 -> 冲墓
    if '入日墓' in states or '入动变墓' in states:
        mu = WUXING_MU.get(yao_wx)
        if mu:
            ch = LIU_CHONG.get(mu)
            if ch: R.append(ch); RS.append(f'入墓，冲墓({ch})')
            R.append(mu); RS.append(f'入墓，临墓值({mu})')

    # D: 太旺 -> 墓之、克之
    if is_dong and strength >= 3:
        mu = WUXING_MU.get(yao_wx)
        if mu: R.append(mu); RS.append(f'太旺，入墓({mu})')
        ke_wx = WUXING_BEI_KE.get(yao_wx)
        if ke_wx:
            for z in DI_ZHI:
                if ZHI_TO_WUXING[z] == ke_wx:
                    R.append(z); RS.append(f'太旺，克制({z}/{ke_wx})'); break

    # E: 旬空 -> 出空
    if '旬空' in states:
        R.append(zhi); RS.append(f'旬空，出空填实({zhi})')
        ch = LIU_CHONG.get(zhi)
        if ch: R.append(ch); RS.append(f'旬空，冲空({ch})')

    # F: 月破 -> 逢值
    if '月破' in states and not R:
        R.append(zhi); RS.append(f'月破，逢值填实({zhi})')

    # G: 回头克 -> 寻生扶
    if '回头克' in states and not R:
        for wx_src, wx_dst in WUXING_SHENG.items():
            if wx_dst == yao_wx:
                for z in DI_ZHI:
                    if ZHI_TO_WUXING[z] == wx_src:
                        R.append(z); RS.append(f'回头克，寻生扶({z}/{wx_src})'); break
                break

    # Fallback 动爻
    if is_dong and not R:
        he = LIU_HE.get(zhi)
        if he: R.append(he); RS.append(f'动爻，逢合({he})')
        R.append(zhi); RS.append(f'动爻，逢值({zhi})')

    # Fallback 静爻
    if not is_dong and not R:
        R.append(zhi); RS.append(f'静爻，逢值({zhi})')
        ch = LIU_CHONG.get(zhi)
        if ch: R.append(ch); RS.append(f'静爻，逢冲({ch})')

    seen = set(); ur, urs = [], []
    for r, rs in zip(R, RS):
        if r not in seen: seen.add(r); ur.append(r); urs.append(rs)
    return ur, urs


def run_divination_engine(yaos, month_zhi, day_zhi, kong1, kong2):
    for yao in yaos:
        m, d, o, s = evaluate_wang_shuai(yao['najia_wuxing'], month_zhi, day_zhi)
        yao['month_state'], yao['day_state'] = m, d
        yao['overall_strength'], yao['strength_score'] = o, s
        states = check_special_states(yao, month_zhi, day_zhi, kong1, kong2, yaos)
        if '回头生' in states: yao['strength_score'] += 1
        if '回头克' in states: yao['strength_score'] -= 1
        yao['special_states'] = states

    for yao in yaos:
        recs, reasons = find_yingqi(yao, month_zhi, day_zhi, kong1, kong2, yaos)
        yao['yingqi_zhi'] = recs
        yao['yingqi_reasons'] = reasons
    return yaos


# ============================================================
# 第七部分：评分 + 差异化输出路由
# ============================================================

def score_yingqi(yaos):
    zhi_scores = {}
    for yao in yaos:
        w = 3 if yao['is_dong'] else 1
        sp = yao.get('special_states', [])
        if '旬空' in sp: w += 2
        if '入日墓' in sp or '入动变墓' in sp: w += 2
        if '被动爻合' in sp or '化合绊' in sp: w += 1
        if '月破' in sp: w += 1
        if '回头克' in sp: w += 1
        for zhi in yao.get('yingqi_zhi', []):
            zhi_scores[zhi] = zhi_scores.get(zhi, 0) + w
    return sorted(zhi_scores.items(), key=lambda x: -x[1])


def get_main_number_map(lottery_type, year):
    """获取主号（红球/前区/平码）映射表"""
    if lottery_type == 'ssq':
        return SSQ_RED_MAP, 33, '红球', 6
    elif lottery_type == 'dlt':
        return DLT_FRONT_MAP, 35, '前区', 5
    elif lottery_type == 'mark6':
        return get_mark6_map(year), 49, '平码', 6
    return SSQ_RED_MAP, 33, '号码', 6


def get_special_map(lottery_type, year):
    """获取特殊球映射表及参数"""
    if lottery_type == 'ssq':
        return SSQ_BLUE_MAP, 1, '蓝球', '双色球蓝球（01~16）'
    elif lottery_type == 'dlt':
        return DLT_BACK_MAP, 2, '后区', '大乐透后区（01~12）'
    elif lottery_type == 'mark6':
        return get_mark6_map(year), 1, '特码/特肖', f'六合彩特码（01~49, {year}年生肖表）'
    return SSQ_BLUE_MAP, 1, '特殊球', '特殊球'


def build_main_picks(ranked, lottery_type, year):
    """
    V1 逻辑：从权重排序的地支中，选出主号推荐。
    返回: top_zhi, core_numbers, selected, top_xiao
    """
    main_map, max_num, _, need_count = get_main_number_map(lottery_type, year)
    top5 = [z for z, _ in ranked[:5]]

    core_nums = []
    for z in top5:
        for n in main_map.get(z, []):
            if 1 <= n <= max_num and n not in core_nums:
                core_nums.append(n)
    core_nums.sort()

    # 精选：每个高权重地支取一个代表号码，补齐到 need_count
    selected = []
    for z in top5:
        for n in main_map.get(z, []):
            if n not in selected and 1 <= n <= max_num:
                selected.append(n)
                break
    for n in core_nums:
        if len(selected) >= need_count:
            break
        if n not in selected:
            selected.append(n)
    selected.sort()

    top_xiao = [ZHI_TO_XIAO.get(z, '?') for z in top5]
    return top5, core_nums, selected, top_xiao


def build_special_picks(ranked, lottery_type, year):
    """
    V2 新增：特殊球推荐。
    返回: top_zhi, top_numbers, all_candidates, mode_label
    """
    sp_map, pick, _, mode_label = get_special_map(lottery_type, year)
    top_zhi = [z for z, _ in ranked[:pick]]
    top_numbers = []
    for z in top_zhi:
        top_numbers.extend(sp_map.get(z, []))
    all_cand = {z: sp_map.get(z, []) for z, _ in ranked}
    return top_zhi, sorted(top_numbers), all_cand, mode_label


# ============================================================
# 第八部分：报告生成
# ============================================================

POS_NAMES = ['初爻', '二爻', '三爻', '四爻', '五爻', '上爻']

def format_yao_line(yao):
    name = POS_NAMES[yao['pos']]
    sym = '▬▬▬' if yao['yinyang'] == 1 else '▬ ▬'
    dong = ' ○' if yao['is_dong'] and yao['yinyang'] == 1 else \
           ' ✕' if yao['is_dong'] and yao['yinyang'] == 0 else '  '
    gz = f"{yao['najia_gan']}{yao['najia_zhi']}"
    wx = yao['najia_wuxing']
    bian = ''
    if yao['is_dong'] and yao.get('bian_zhi'):
        bian = f" -> {yao['bian_zhi']}({yao['bian_wuxing']})"
    st = ''
    if yao.get('special_states'):
        st = f" 【{'、'.join(yao['special_states'])}】"
    strength = f"{yao.get('month_state','?')}/{yao.get('day_state','?')}={yao.get('overall_strength','?')}"
    return f"  {name} {sym}{dong}  {gz}({wx}) {strength}{bian}{st}"


def generate_report(yaos, hexagram, date_info, lottery_type, adapt_note, year):
    L = []
    lname = LOTTERY_NAMES.get(lottery_type, lottery_type)
    main_map, max_num, main_label, need_count = get_main_number_map(lottery_type, year)
    sp_map_obj, sp_pick, sp_label, sp_mode = get_special_map(lottery_type, year)

    L.append("=" * 62)
    L.append("     六爻奇门测彩 · HexaLotto V2.0 推演报告")
    L.append("=" * 62)
    L.append("")
    L.append(f"  起卦日期：{date_info['date_str']}")
    L.append(f"  日    柱：{date_info['day_gz']}    月柱：{date_info['month_gz']}")
    L.append(f"  月    建：{date_info['month_zhi']}({ZHI_TO_WUXING[date_info['month_zhi']]})")
    L.append(f"  日    建：{date_info['day_zhi']}({ZHI_TO_WUXING[date_info['day_zhi']]})")
    L.append(f"  旬    空：{date_info['kong1']} {date_info['kong2']}")
    L.append(f"  彩    种：{lname}")
    L.append(f"  起卦号码：{' '.join(str(y['number']).zfill(2) for y in yaos)}")
    L.append(f"  适配说明：{adapt_note}")
    L.append("")

    # 卦象
    L.append("─" * 42)
    L.append(f"  本  卦：{hexagram['ben_gua_name']}")
    L.append(f"         （{hexagram['upper_gua']}上 {hexagram['lower_gua']}下）")
    if hexagram['has_dong']:
        L.append(f"  变  卦：{hexagram['bian_gua_name']}")
        L.append(f"         （{hexagram['changed_upper_gua']}上 {hexagram['changed_lower_gua']}下）")
    else:
        L.append("  变  卦：六爻安静（按静而逢值逢冲处理）")
    L.append("─" * 42)
    L.append("")

    # 排盘
    L.append("  【六爻排盘】（上 -> 下）")
    L.append("  " + "─" * 58)
    for i in range(5, -1, -1):
        L.append(format_yao_line(yaos[i]))
    L.append("")

    # 断卦分析
    L.append("─" * 42)
    L.append("  【断卦分析 · 应期推算】")
    L.append("─" * 42)
    for yao in yaos:
        if yao['yingqi_zhi']:
            dm = "【动】" if yao['is_dong'] else "【静】"
            L.append(f"\n  {POS_NAMES[yao['pos']]} {dm} ({yao['najia_gan']}{yao['najia_zhi']}/{yao['najia_wuxing']})：")
            for r in yao['yingqi_reasons']:
                L.append(f"    -> {r}")
    L.append("")

    # 加权排序
    ranked = score_yingqi(yaos)

    # ================================================================
    #  第一部分：主号推荐（V1 逻辑保留）
    # ================================================================
    top5, core_nums, selected, top_xiao = build_main_picks(ranked, lottery_type, year)
    main_nmap = {z: main_map.get(z, []) for z, _ in ranked}

    L.append("=" * 62)
    L.append(f"  【{main_label}推荐】（按权重排序）")
    L.append("=" * 62)
    L.append("")
    L.append(f"  应期地支  ->  生肖  ->  {main_label}候选               权重")
    L.append("  " + "─" * 52)
    for zhi, score in ranked:
        xiao = ZHI_TO_XIAO.get(zhi, '?')
        nums = main_nmap.get(zhi, [])
        ns = ', '.join(str(n).zfill(2) for n in nums if 1 <= n <= max_num) if nums else '—'
        star = '★' if zhi in top5 else '  '
        L.append(f"  {star} {zhi}      ->  {xiao}    ->  {ns:<28s} ({score}分)")

    L.append("")
    L.append(f"  ★ 核心生肖：{'、'.join(top_xiao)}")
    L.append(f"  ★ 候选号码池：{' '.join(str(n).zfill(2) for n in core_nums)}")
    L.append(f"  ★ 精选{main_label}（{len(selected)}个）：{' '.join(str(n).zfill(2) for n in selected)}")
    L.append("")

    # ================================================================
    #  第二部分：特殊球推荐（V2 新增）
    # ================================================================
    sp_top_zhi, sp_top_nums, sp_all_cand, sp_mode_label = build_special_picks(ranked, lottery_type, year)
    sp_top_xiao = [ZHI_TO_XIAO.get(z, '?') for z in sp_top_zhi]

    L.append("=" * 62)
    L.append(f"  【{sp_label}推荐】· {sp_mode_label}")
    L.append("=" * 62)
    L.append("")
    L.append(f"  应期地支  ->  生肖  ->  {sp_label}候选               权重")
    L.append("  " + "─" * 52)
    for zhi, score in ranked:
        xiao = ZHI_TO_XIAO.get(zhi, '?')
        nums = sp_all_cand.get(zhi, [])
        ns = ', '.join(str(n).zfill(2) for n in nums) if nums else '—'
        star = '★' if zhi in sp_top_zhi else '  '
        L.append(f"  {star} {zhi}      ->  {xiao}    ->  {ns:<28s} ({score}分)")

    L.append("")
    L.append("  " + "━" * 52)
    sp_str = ' '.join(str(n).zfill(2) for n in sp_top_nums)

    if lottery_type == 'mark6':
        L.append(f"  ★ 推算特肖：【{'、'.join(sp_top_xiao)}】")
        L.append(f"  ★ 特码候选：{sp_str}")
    elif lottery_type == 'dlt':
        L.append(f"  ★ 推算后区（{sp_pick}个）：{sp_str}")
        L.append(f"  ★ 对应生肖：{'、'.join(sp_top_xiao)}")
    elif lottery_type == 'ssq':
        L.append(f"  ★ 推算蓝球：{sp_str}")
        L.append(f"  ★ 对应生肖：{'、'.join(sp_top_xiao)}")
        if len(sp_top_nums) > 1:
            L.append(f"    （该地支双对应，{len(sp_top_nums)}个蓝球备选）")
    L.append("  " + "━" * 52)

    # ================================================================
    #  综合推荐摘要
    # ================================================================
    L.append("")
    L.append("=" * 62)
    L.append("  【综合推荐摘要】")
    L.append("=" * 62)
    if lottery_type == 'ssq':
        L.append(f"  红球：{' '.join(str(n).zfill(2) for n in selected)}")
        L.append(f"  蓝球：{sp_str}")
    elif lottery_type == 'dlt':
        L.append(f"  前区：{' '.join(str(n).zfill(2) for n in selected)}")
        L.append(f"  后区：{sp_str}")
    elif lottery_type == 'mark6':
        L.append(f"  平码：{' '.join(str(n).zfill(2) for n in selected)}")
        L.append(f"  特肖：【{'、'.join(sp_top_xiao)}】 -> {sp_str}")

    L.append("")
    L.append("─" * 62)
    L.append("  ⚠ 免责声明：本推演纯属娱乐与传统文化演示，")
    L.append("    不构成任何投资或博彩建议。彩票中奖完全依靠随机概率。")
    L.append("─" * 62)

    summary = {
        'lottery_type': lottery_type, 'lottery_name': lname,
        # V1: 主号
        'main_label': main_label,
        'main_recommended_zhi': top5,
        'main_recommended_xiao': top_xiao,
        'main_candidate_numbers': core_nums,
        'main_selected': selected,
        # V2: 特殊球
        'special_label': sp_label,
        'special_mode': sp_mode_label,
        'special_recommended_zhi': sp_top_zhi,
        'special_recommended_xiao': sp_top_xiao,
        'special_recommended_numbers': sp_top_nums,
        # 共用
        'all_ranked_zhi': [(z, s) for z, s in ranked],
    }
    return '\n'.join(L), summary


# ============================================================
# 第九部分：主入口
# ============================================================

def run(raw_numbers, target_date=None, lottery_type='ssq',
        dlt_strategy='A', output_json=False):
    if target_date is None:
        target_date = date.today()
    elif isinstance(target_date, str):
        target_date = datetime.strptime(target_date, '%Y-%m-%d').date()

    year = target_date.year
    numbers, adapt_note = adapt_input(raw_numbers, lottery_type, target_date, dlt_strategy)

    day_gz, day_gz_idx = day_ganzhi(target_date)
    year_gz, _ = year_ganzhi(year)
    month_gz, _ = month_ganzhi(year, target_date.month)
    now = datetime.now()
    hour_gz, _ = hour_ganzhi(day_gz_idx, now.hour)
    day_zhi, month_zhi = day_gz[1], month_gz[1]
    kong1, kong2 = calc_xunkong(day_gz_idx)

    date_info = {
        'date_str': target_date.strftime('%Y年%m月%d日'),
        'year_gz': year_gz, 'month_gz': month_gz,
        'day_gz': day_gz, 'hour_gz': hour_gz,
        'day_zhi': day_zhi, 'month_zhi': month_zhi,
        'kong1': kong1, 'kong2': kong2,
    }

    yaos = numbers_to_yao(numbers)
    hexagram = build_hexagram(yaos)
    yaos = assign_najia(yaos, hexagram)
    yaos = run_divination_engine(yaos, month_zhi, day_zhi, kong1, kong2)
    report, summary = generate_report(yaos, hexagram, date_info, lottery_type, adapt_note, year)

    if output_json:
        out = {
            'date_info': date_info, 'adapt_note': adapt_note,
            'hexagram': hexagram,
            'yaos': [{
                'pos': y['pos'], 'number': y['number'],
                'sixiang': y['sixiang'], 'is_dong': y['is_dong'],
                'najia': f"{y['najia_gan']}{y['najia_zhi']}",
                'wuxing': y['najia_wuxing'],
                'bian_zhi': y.get('bian_zhi'),
                'bian_wuxing': y.get('bian_wuxing'),
                'month_state': y.get('month_state'),
                'day_state': y.get('day_state'),
                'overall': y.get('overall_strength'),
                'strength_score': y.get('strength_score'),
                'special_states': y.get('special_states', []),
                'yingqi_zhi': y.get('yingqi_zhi', []),
                'yingqi_reasons': y.get('yingqi_reasons', []),
            } for y in yaos],
            'summary': {
                'lottery_type': summary['lottery_type'],
                'lottery_name': summary['lottery_name'],
                'main': {
                    'label': summary['main_label'],
                    'recommended_zhi': summary['main_recommended_zhi'],
                    'recommended_xiao': summary['main_recommended_xiao'],
                    'candidate_numbers': summary['main_candidate_numbers'],
                    'selected': summary['main_selected'],
                },
                'special': {
                    'label': summary['special_label'],
                    'mode': summary['special_mode'],
                    'recommended_zhi': summary['special_recommended_zhi'],
                    'recommended_xiao': summary['special_recommended_xiao'],
                    'recommended_numbers': summary['special_recommended_numbers'],
                },
                'all_ranked_zhi': summary['all_ranked_zhi'],
            },
        }
        return json.dumps(out, ensure_ascii=False, indent=2, default=str)
    return report


def main():
    parser = argparse.ArgumentParser(
        description='HexaLotto V2.0 六爻奇门测彩 · 多彩种引擎',
        epilog='⚠ 免责声明：本工具纯属娱乐，不构成任何投资建议。'
    )
    parser.add_argument('--numbers', '-n', required=True,
                        help='平码/红球，空格分隔。SSQ/MARK6=6个，DLT=5个(自动补)或6个')
    parser.add_argument('--date', '-d', default=None,
                        help='起卦日期 (YYYY-MM-DD)，默认今天')
    parser.add_argument('--type', '-t', default='ssq',
                        choices=['ssq', 'dlt', 'mark6'],
                        help='彩种：ssq=双色球, dlt=大乐透, mark6=六合彩')
    parser.add_argument('--dlt-strategy', '-s', default='A',
                        choices=['A', 'B'],
                        help='大乐透第6爻策略：A=求和衍生, B=干支借位')
    parser.add_argument('--json', '-j', action='store_true',
                        help='JSON格式输出')
    args = parser.parse_args()

    try:
        numbers = [int(x) for x in args.numbers.strip().split()]
    except (ValueError, AttributeError):
        print("错误：号码必须为整数，空格分隔", file=sys.stderr)
        sys.exit(1)

    print(run(numbers, args.date, args.type, args.dlt_strategy, args.json))


if __name__ == '__main__':
    main()
