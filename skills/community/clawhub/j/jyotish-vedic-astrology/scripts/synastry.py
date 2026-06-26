#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
synastry.py — 合盘分析模块
Ashta Koota 36分制 + Mangal Dosha + Papasamya + Dasha兼容性

依赖: swisseph (可选，用于从出生数据直接计算)
"""

import math

SIGNS = ['Aries','Taurus','Gemini','Cancer','Leo','Virgo',
         'Libra','Scorpio','Sagittarius','Capricorn','Aquarius','Pisces']

# 27 Nakshatras: (name, lord, yoni)
NAK27 = [
    ("Ashwini",0),("Bharani",1),("Krittika",2),("Rohini",3),("Mrigashira",4),
    ("Ardra",5),("Punarvasu",6),("Pushya",7),("Ashlesha",8),("Magha",0),
    ("Purva Phalguni",1),("Uttara Phalguni",2),("Hasta",3),("Chitra",4),
    ("Swati",5),("Vishakha",6),("Anuradha",7),("Jyeshtha",8),("Mula",0),
    ("Purva Ashadha",1),("Uttara Ashadha",2),("Shravana",3),("Dhanishta",4),
    ("Shatabhisha",5),("Purva Bhadrapada",6),("Uttara Bhadrapada",7),("Revati",8),
]
# Gana: Deva(0)=0,1,6,7,14; Manushya(1)=2,4,8,10,12,15,18,20,22; Rakshasa(2)=3,5,9,11,13,16,17,19,21,23,24,25,26
GANA_MAP = [0,0,1,2,1,2,0,0,1,2,1,2,1,2,0,1,2,2,2,2,1,2,1,2,2,2,2]
# Yoni: 14种动物配对
YONI_MAP = [0,1,2,3,4,5,6,7,2,0,1,8,3,4,5,6,7,8,9,1,8,3,10,4,5,6,11]
YONI_NAME = ['Horse','Elephant','Sheep','Serpent','Dog','Cat','Rat','Cow','Buffalo',
             'Tiger','Lion','Fish','?','?']
# Nadi: 3种 (Vata=0, Pitta=1, Kapha=2)
NADI_MAP = [0,1,2,0,1,2,0,1,2,0,1,2,0,1,2,0,1,2,0,1,2,0,1,2,0,1,2]
# Varna: 4种种姓 (Brahmin=3, Kshatriya=2, Vaishya=1, Shudra=0)
VARNA_MAP = [0,2,1,3,0,2,1,3,0,2,1,3,0,2,1,3,0,2,1,3,0,2,1,3,0,2,1]
# Vashya: sign-based
VASHYA_SIGN = [0,1,2,3,0,1,2,3,0,1,2,3]  # 0=quadruped,1=biped,2=insect,3=water

# Dasha years for Vimshottari
DASHA_YEARS = {"Ketu":7,"Venus":20,"Sun":6,"Moon":10,"Mars":7,"Rahu":18,"Jupiter":16,"Saturn":19,"Mercury":17}
DASHA_ORDER = ["Ketu","Venus","Sun","Moon","Mars","Rahu","Jupiter","Saturn","Mercury"]

def _nak_idx(lon):
    """黄经→Nakshatra索引(0-26)"""
    return int(lon / (360/27)) % 27

def _sign_idx(lon):
    return int(lon / 30) % 12

# ============================================================================
# Ashta Koota 8维度评分
# ============================================================================
def _calc_varna(n1, n2):
    """Varna Koota (1分) - 精神兼容"""
    v1, v2 = VARNA_MAP[n1], VARNA_MAP[n2]
    if v2 >= v1: return {'score':1,'max':1,'v1':v1,'v2':v2,'note':'女方种姓≥男方，吉'}
    return {'score':0,'max':1,'v1':v1,'v2':v2,'note':'女方种姓<男方，不吉'}

def _calc_vashya(s1, s2):
    """Vashya Koota (2分) - 控制力"""
    v1, v2 = VASHYA_SIGN[s1], VASHYA_SIGN[s2]
    if v1 == v2: return {'score':2,'max':2,'note':'同Vashya，满分'}
    # 互补对
    pairs = {(0,3),(3,0),(1,2),(2,1)}
    if (v1,v2) in pairs: return {'score':1,'max':2,'note':'互补Vashya，半分'}
    return {'score':0,'max':2,'note':'Vashya不合'}

def _calc_tara(n1, n2):
    """Tara Koota (3分) - 星宿距离吉凶"""
    diff = (n2 - n1) % 9
    auspicious = {0,2,4,6,8}  # Janma,Sampat,Kshema,Pratyak,Sadhana → 2,4,6,8,0 mod9
    # 好Tara: Sampat(2),Kshema(4),Sadhana(6),Priya(8)
    good = {2,4,6,8}
    if diff in good: return {'score':3,'max':3,'diff':diff,'note':'吉Tara'}
    if diff == 0: return {'score':2,'max':3,'diff':diff,'note':'中性Tara(Janma)'}
    return {'score':0,'max':3,'diff':diff,'note':'凶Tara'}

def _calc_yoni(n1, n2):
    """Yoni Koota (4分) - 生理兼容"""
    y1, y2 = YONI_MAP[n1], YONI_MAP[n2]
    if y1 == y2: return {'score':4,'max':4,'note':'同Yoni，满分'}
    # 敌对Yoni
    enemy = {(0,5),(5,0),(2,4),(4,2),(3,2),(2,3)}
    if (y1,y2) in enemy: return {'score':0,'max':4,'note':'敌对Yoni'}
    # 友好Yoni
    friendly = {(0,7),(7,0),(1,8),(8,1),(6,9),(9,6)}
    if (y1,y2) in friendly: return {'score':3,'max':4,'note':'友好Yoni'}
    return {'score':1,'max':4,'note':'中性Yoni'}

def _calc_graha_maitri(lord1, lord2):
    """Graha Maitri Koota (5分) - 行星友谊"""
    # 行星友谊表
    friends = {'Sun':['Moon','Mars','Jupiter'],'Moon':['Sun','Mercury'],
               'Mars':['Sun','Moon','Jupiter'],'Mercury':['Sun','Venus'],
               'Jupiter':['Sun','Moon','Mars'],'Venus':['Mercury','Saturn'],
               'Saturn':['Mercury','Venus'],'Rahu':['Venus','Saturn'],
               'Ketu':['Venus','Saturn']}
    enemies = {'Sun':['Saturn','Venus'],'Moon':['Mercury'],'Mars':['Mercury','Saturn'],
               'Mercury':['Mars','Jupiter','Saturn'],'Jupiter':['Mercury','Venus'],
               'Venus':['Sun','Moon','Mars'],'Saturn':['Sun','Moon','Mars'],
               'Rahu':['Sun','Moon','Mars'],'Ketu':['Sun','Moon','Mars']}
    if lord1 == lord2: return {'score':5,'max':5,'note':'同主星，满分'}
    l2_friends = friends.get(lord2,[])
    l2_enemies = enemies.get(lord2,[])
    if lord1 in l2_friends: return {'score':4,'max':5,'note':f'{lord1}是{lord2}的友星'}
    if lord1 in l2_enemies: return {'score':0,'max':5,'note':f'{lord1}是{lord2}的敌星'}
    return {'score':2,'max':5,'note':f'{lord1}对{lord2}中性'}

def _calc_gana(n1, n2):
    """Gana Koota (6分) - 气质类型"""
    g1, g2 = GANA_MAP[n1], GANA_MAP[n2]
    gana_name = {0:'Deva(天神)',1:'Manushya(人类)',2:'Rakshasa(罗刹)'}
    if g1 == g2: return {'score':6,'max':6,'g1':gana_name[g1],'g2':gana_name[g2],'note':'同Gana，满分'}
    # Deva+Manushya
    combo = {g1,g2}
    if combo == {0,1}: return {'score':5,'max':6,'g1':gana_name[g1],'g2':gana_name[g2],'note':'天神+人类，良好'}
    if combo == {1,2}: return {'score':2,'max':6,'g1':gana_name[g1],'g2':gana_name[g2],'note':'人类+罗刹，较差'}
    # Deva+Rakshasa
    return {'score':1,'max':6,'g1':gana_name[g1],'g2':gana_name[g2],'note':'天神+罗刹，很差'}

def _calc_bhakuta(n1, n2):
    """Bhakuta Koota (7分) - 情感+经济"""
    diff = (n2 - n1) % 9
    # 满分组合
    full = {1,3,5,7}
    if diff in full: return {'score':7,'max':7,'diff':diff,'note':'吉Bhakuta，满分'}
    if diff == 0: return {'score':4,'max':7,'diff':diff,'note':'中性Bhakuta'}
    return {'score':0,'max':7,'diff':diff,'note':'凶Bhakuta，零分'}

def _calc_nadi(n1, n2):
    """Nadi Koota (8分) - 生命力/健康"""
    na1, na2 = NADI_MAP[n1], NADI_MAP[n2]
    nadi_name = {0:'Vata(风)',1:'Pitta(胆汁)',2:'Kapha(粘液)'}
    if na1 == na2:
        return {'score':0,'max':8,'n1':nadi_name[na1],'n2':nadi_name[na2],
                'note':'同Nadi=不吉（传统认为影响后代健康）'}
    return {'score':8,'max':8,'n1':nadi_name[na1],'n2':nadi_name[na2],
            'note':'不同Nadi=吉，互补生命力'}

# ============================================================================
# 合盘主函数
# ============================================================================
def calc_synastry(person1: dict, person2: dict) -> dict:
    """
    计算两人的完整合盘分析

    person1/person2 格式:
    {
        'moon_lon': float,      # 月亮黄经(恒星黄道)
        'mars_lon': float,      # 火星黄经(恒星黄道) (可选)
        'asc_lon': float,       # 上升黄经(恒星黄道) (可选)
        'nakshatra_lord': str,  # 月亮Nakshatra主星 (可选，自动计算)
        'gender': str,          # 'M' or 'F' (影响Varna方向)
    }

    返回: 完整合盘报告 dict
    """
    m1 = person1.get('moon_lon', 0)
    m2 = person2.get('moon_lon', 0)
    n1 = _nak_idx(m1)
    n2 = _nak_idx(m2)
    s1 = _sign_idx(m1)
    s2 = _sign_idx(m2)

    # Nakshatra主星
    lords = ['Ketu','Venus','Sun','Moon','Mars','Rahu','Jupiter','Saturn','Mercury']
    lord1 = person1.get('nakshatra_lord') or lords[n1 % 9]
    lord2 = person2.get('nakshatra_lord') or lords[n2 % 9]

    # Ashta Koota 8维度
    varna = _calc_varna(n1, n2)
    vashya = _calc_vashya(s1, s2)
    tara = _calc_tara(n1, n2)
    yoni = _calc_yoni(n1, n2)
    graha = _calc_graha_maitri(lord1, lord2)
    gana = _calc_gana(n1, n2)
    bhakuta = _calc_bhakuta(n1, n2)
    nadi = _calc_nadi(n1, n2)

    kootas = [
        ('Varna(精神)', varna), ('Vashya(控制)', vashya), ('Tara(星宿距离)', tara),
        ('Yoni(生理)', yoni), ('Graha Maitri(行星友谊)', graha),
        ('Gana(气质)', gana), ('Bhakuta(情感经济)', bhakuta), ('Nadi(生命力)', nadi),
    ]

    total = sum(k[1]['score'] for k in kootas)
    max_total = sum(k[1]['max'] for k in kootas)
    pct = round(total / max_total * 100, 1) if max_total else 0

    # 综合判定
    verdict = _compatibility_verdict(total, pct)

    # Mangal Dosha 检查
    dosha1 = _check_mangal_dosha(person1)
    dosha2 = _check_mangal_dosha(person2)
    mangal_note = _dosha_match(dosha1, dosha2)

    # Papasamya (双方凶星抵消度)
    papasamya = _calc_papasamya(person1, person2)

    return {
        'method': 'Ashta Koota 36分制 + Mangal Dosha + Papasamya',
        'version': '3.7',
        'person1': {'moon_nakshatra': NAK27[n1][0], 'nak_idx': n1, 'moon_sign': SIGNS[s1]},
        'person2': {'moon_nakshatra': NAK27[n2][0], 'nak_idx': n2, 'moon_sign': SIGNS[s2]},
        'kootas': {k:v for k,v in kootas},
        'total_score': total,
        'max_score': max_total,
        'percentage': pct,
        'verdict': verdict,
        'mangal_dosha': {'person1': dosha1, 'person2': dosha2, 'compatibility': mangal_note},
        'papasamya': papasamya,
        'recommendations': _generate_recommendations(total, pct, kootas, mangal_note),
    }


def _compatibility_verdict(score, pct):
    """综合判定"""
    if pct >= 75: return {'level':'极佳','color':'绿色','cn':'强烈推荐，天然契合'}
    if pct >= 60: return {'level':'良好','color':'蓝绿','cn':'推荐，小问题可化解'}
    if pct >= 45: return {'level':'一般','color':'黄色','cn':'需要努力调和'}
    if pct >= 30: return {'level':'较差','color':'橙色','cn':'不推荐，阻力较大'}
    return {'level':'很差','color':'红色','cn':'强烈不推荐，冲突严重'}


def _check_mangal_dosha(person):
    """Mangal Dosha（火星凶相）检查"""
    mars_lon = person.get('mars_lon')
    if mars_lon is None:
        return {'has_dosha': None, 'note': '缺少火星数据'}
    mars_house = person.get('mars_house')
    mars_sign = _sign_idx(mars_lon) if mars_house is None else None

    # 需要计算火星在第几宫（相对于上升）
    asc_lon = person.get('asc_lon')
    if asc_lon is not None and mars_house is None:
        asc_si = _sign_idx(asc_lon)
        mars_si = _sign_idx(mars_lon)
        mars_house = ((mars_si - asc_si) % 12) + 1

    if mars_house is None:
        return {'has_dosha': None, 'note': '缺少上升数据，无法确定宫位'}

    # Mangal Dosha: 火星在1/2/4/7/8/12宫
    dosha_houses = {1, 2, 4, 7, 8, 12}
    has = mars_house in dosha_houses

    # 强度分级
    severity = '无'
    if has:
        if mars_house in {7, 8}:
            severity = '强'
        elif mars_house in {1, 2}:
            severity = '中'
        else:
            severity = '轻'

    return {
        'has_dosha': has,
        'severity': severity if has else '无',
        'mars_house': mars_house,
        'note': f'火星在第{mars_house}宫' + ('→有Mangal Dosha' if has else '→无Mangal Dosha'),
    }


def _dosha_match(dosha1, dosha2):
    """双方Mangal Dosha匹配"""
    d1 = dosha1.get('has_dosha')
    d2 = dosha2.get('has_dosha')
    if d1 is None or d2 is None:
        return {'status':'数据不足','note':'缺少一方火星数据'}
    if d1 and d2:
        return {'status':'双Dosha匹配','note':'双方都有Mangal Dosha，互相抵消→可接受'}
    if d1 and not d2:
        return {'status':'仅一方Dosha','note':'仅Person1有Dosha，Person2需有足够力量承受'}
    if not d1 and d2:
        return {'status':'仅一方Dosha','note':'仅Person2有Dosha，Person1需有足够力量承受'}
    return {'status':'双方无Dosha','note':'双方均无Mangal Dosha→理想'}


def _calc_papasamya(p1, p2):
    """Papasamya - 双方凶星点数抵消"""
    # 简化版：检查太阳/火星/土星/北交点在凶宫(6/8/12)的情况
    def _count_papa(person):
        count = 0
        for key in ['sun_house','mars_house','saturn_house','rahu_house']:
            h = person.get(key)
            if h and h in {6, 8, 12}:
                count += 1
        return count

    c1 = _count_papa(p1)
    c2 = _count_papa(p2)
    diff = abs(c1 - c2)

    if diff == 0:
        balance = '均衡'
        note = '双方凶星负担相当，Papasamya良好'
    elif diff == 1:
        balance = '轻微失衡'
        note = '一方凶星负担略重，可接受'
    else:
        balance = '明显失衡'
        note = '双方凶星负担差异较大，需注意'

    return {'person1_papa': c1, 'person2_papa': c2, 'difference': diff,
            'balance': balance, 'note': note}


def _generate_recommendations(score, pct, kootas, mangal_note):
    """生成建议"""
    recs = []

    # 低分维度警告
    for name, data in kootas:
        if data['score'] < data['max'] * 0.3:
            recs.append(f"⚠ {name}得分低({data['score']}/{data['max']})：{data['note']}")

    # Nadi特别警告
    nadi_score = kootas[7][1]['score']  # Nadi是第8个
    if nadi_score == 0:
        recs.append("🔴 Nadi Koota零分！传统认为同Nadi婚姻可能影响后代健康，建议咨询专业占星师")
        recs.append("化解方案：Nadi Dosha Pooja、佩戴对应宝石、或寻找Nadi不同的伴侣")

    # Mangal Dosha建议
    if mangal_note.get('status') == '仅一方Dosha':
        recs.append("⚠ 一方有Mangal Dosha：建议找有Dosha的伴侣匹配，或进行Mangal Dosha化解仪式")
        recs.append("化解方案：Kumbh Vivah（与陶罐结婚仪式）、在28岁后结婚、或匹配有Dosha的对象")

    # 总分建议
    if pct >= 60:
        recs.append(f"✅ 总分{pct}%，在可接受范围内。建议深入了解彼此价值观和生活目标")
    elif pct >= 45:
        recs.append(f"⚠ 总分{pct}%，需要双方更多努力和理解。建议进行详细的合盘咨询")
    else:
        recs.append(f"❌ 总分{pct}%，传统认为阻力较大。强烈建议咨询专业占星师后再做决定")

    return recs


# ============================================================================
# Dasha 兼容性分析
# ============================================================================
def calc_dasha_compatibility(dasha1: list, dasha2: list, start_year: int) -> dict:
    """
    分析两人Dasha时间线的兼容性

    dasha1/dasha2: [{'lord':'Venus','start':'1990-01-01','end':'2010-01-01','years':20}, ...]
    start_year: 分析起始年份
    """
    from datetime import datetime

    periods = []
    conflicts = []
    harmonies = []

    # 行星兼容性
    friends = {'Sun':['Moon','Mars','Jupiter'],'Moon':['Sun','Mercury'],
               'Mars':['Sun','Moon','Jupiter'],'Mercury':['Sun','Venus'],
               'Jupiter':['Sun','Moon','Mars'],'Venus':['Mercury','Saturn'],
               'Saturn':['Mercury','Venus'],'Rahu':['Venus','Saturn'],'Ketu':['Venus','Saturn']}

    for d1 in dasha1:
        for d2 in dasha2:
            # 检查时间重叠
            try:
                s1 = datetime.strptime(d1['start'],'%Y-%m-%d')
                e1 = datetime.strptime(d1['end'],'%Y-%m-%d')
                s2 = datetime.strptime(d2['start'],'%Y-%m-%d')
                e2 = datetime.strptime(d2['end'],'%Y-%m-%d')
            except:
                continue

            overlap_start = max(s1, s2)
            overlap_end = min(e1, e2)
            if overlap_start >= overlap_end:
                continue
            if overlap_start.year < start_year:
                continue

            lord1 = d1.get('lord','')
            lord2 = d2.get('lord','')

            # 判断关系
            l2_friends = friends.get(lord2, [])
            rel = '中性'
            if lord1 == lord2:
                rel = '同步'
            elif lord1 in l2_friends:
                rel = '友好'
            elif lord1 in ['Rahu','Ketu'] or lord2 in ['Rahu','Ketu']:
                rel = '变化'
            else:
                rel = '紧张'

            period_info = {
                'period': f"{overlap_start.strftime('%Y-%m')} ~ {overlap_end.strftime('%Y-%m')}",
                'person1_dasha': lord1,
                'person2_dasha': lord2,
                'relationship': rel,
            }
            periods.append(period_info)

            if rel in ('紧张','变化'):
                conflicts.append(period_info)
            elif rel in ('同步','友好'):
                harmonies.append(period_info)

    return {
        'method': 'Dasha时间线兼容性',
        'periods_analyzed': len(periods),
        'conflicts': conflicts[:5],
        'harmonies': harmonies[:5],
        'conflict_count': len(conflicts),
        'harmony_count': len(harmonies),
        'assessment': '和谐' if len(harmonies) > len(conflicts) * 1.5 else
                      ('一般' if len(harmonies) >= len(conflicts) else '紧张'),
    }


# ============================================================================
# CLI 入口
# ============================================================================
if __name__ == '__main__':
    import json
    import sys

    # 示例用法
    if len(sys.argv) > 1 and sys.argv[1] == 'test':
        p1 = {'moon_lon': 45.5, 'mars_lon': 120.3, 'asc_lon': 150.0, 'gender': 'M'}
        p2 = {'moon_lon': 200.7, 'mars_lon': 30.1, 'asc_lon': 60.0, 'gender': 'F'}
        result = calc_synastry(p1, p2)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print("Usage: python synastry.py test")
        print("  test - 运行示例测试")
