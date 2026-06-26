#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tajika/Varshaphala年运盘模块 v1.0
太阳返照盘分析系统

支持:
  - Muntha（年度上升点移动）
  - Varshaphala计算（太阳回到出生位置时的星盘）
  - Mudda Dasha（年度大运）
  - Tajika Yoga（年度特殊格局）
  - Tri-Pataka（三旗系统）
  -年度Lord（Year Lord）
"""
from typing import Dict, List, Optional
from datetime import datetime
import math

SIGNS = ['Aries','Taurus','Gemini','Cancer','Leo','Virgo',
         'Libra','Scorpio','Sagittarius','Capricorn','Aquarius','Pisces']
SIGN_LORDS = {'Aries':'Mars','Taurus':'Venus','Gemini':'Mercury','Cancer':'Moon',
    'Leo':'Sun','Virgo':'Mercury','Libra':'Venus','Scorpio':'Mars',
    'Sagittarius':'Jupiter','Capricorn':'Saturn','Aquarius':'Saturn','Pisces':'Jupiter'}


def calc_muntha(birth_asc_idx: int, age: int) -> Dict:
    """
    Muntha计算：年度上升点
    从出生上升星座开始，每年前进一个星座
    
    参数:
        birth_asc_idx: 出生上升星座索引（0=Aries）
        age: 当前年龄（整数）
    """
    muntha_idx = (birth_asc_idx + age) % 12
    muntha_sign = SIGNS[muntha_idx]
    lord = SIGN_LORDS[muntha_sign]
    
    # Muntha落在的宫位（从本命盘上升算起）
    # 需要本命盘上升来计算
    
    return {
        'muntha_sign': muntha_sign,
        'muntha_sign_idx': muntha_idx,
        'muntha_lord': lord,
        'age': age,
        'interpretation': _muntha_interp(muntha_sign, lord),
    }


def calc_year_lord(birth_asc_idx: int, age: int) -> Dict:
    """
    Year Lord（年度守护星）
    基于Muntha位置确定该年的守护行星
    
    规则:
      - Muntha落在某星座→该星座守护星为Year Lord
      - Muntha的2/5/9/11宫的守护星为辅助
    """
    muntha_idx = (birth_asc_idx + age) % 12
    muntha_sign = SIGNS[muntha_idx]
    year_lord = SIGN_LORDS[muntha_sign]
    
    # 辅助星（2/5/9/11宫主）
    aux_houses = [2, 5, 9, 11]
    aux_lords = []
    for h in aux_houses:
        h_sign_idx = (muntha_idx + h - 1) % 12
        h_sign = SIGNS[h_sign_idx]
        aux_lords.append({'house': h, 'sign': h_sign, 'lord': SIGN_LORDS[h_sign]})
    
    return {
        'age': age,
        'year_lord': year_lord,
        'muntha_sign': muntha_sign,
        'auxiliary_lords': aux_lords,
        'year_theme': _year_theme(year_lord),
    }


def calc_varshaphala(birth_datetime: datetime, 
                     target_year: int,
                     birth_lon: float, birth_lat: float,
                     birth_tz: float) -> Dict:
    """
    Varshaphala（太阳返照盘）计算
    
    原理: 太阳回到出生时精确位置的时刻，重新起盘
    这个新的上升星座和行星配置代表该年的运势
    
    参数:
        birth_datetime: 出生时间
        target_year: 目标年份
        birth_lon/lat: 出生经纬度
        birth_tz: 出生时区
    """
    # 简化版：用Muntha + Year Lord + 基本Tajika规则
    # 完整版需要Swiss Ephemeris计算太阳精确返照时间
    
    # 出生上升（需要传入，这里用简化版）
    age = target_year - birth_datetime.year
    
    return {
        'target_year': target_year,
        'age': age,
        'note': 'Varshaphala完整计算需要Swiss Ephemeris精确返照时间',
        'components': {
            'muntha': calc_muntha(0, age),  # 需要实际出生上升
            'year_lord': calc_year_lord(0, age),
        }
    }


def calc_mudda_dasha(asc_sign_idx: int, 
                     varsha_lord: str,
                     birth_month: int) -> Dict:
    """
    Mudda Dasha（年度大运）
    基于Varshaphala上升的12个月大运系统
    
    规则: 从年度守护星开始，按Vimshottari顺序排列
    每个大运按比例分配12个月
    """
    DASHA_ORDER = ["Ketu","Venus","Sun","Moon","Mars","Rahu","Jupiter","Saturn","Mercury"]
    DASHA_YEARS = {"Ketu":7,"Venus":20,"Sun":6,"Moon":10,"Mars":7,"Rahu":18,"Jupiter":16,"Saturn":19,"Mercury":17}
    
    start_idx = DASHA_ORDER.index(varsha_lord) if varsha_lord in DASHA_ORDER else 0
    
    sequence = []
    remaining_months = 12.0
    
    for i in range(9):
        lord = DASHA_ORDER[(start_idx + i) % 9]
        years = DASHA_YEARS[lord]
        months = years * 12.0 / 120.0  # 按比例分配
        
        if months > remaining_months:
            months = remaining_months
        remaining_months -= months
        
        sequence.append({
            'lord': lord,
            'months': round(months, 2),
            'order': i + 1,
        })
        
        if remaining_months <= 0:
            break
    
    return {
        'varsha_lord': varsha_lord,
        'dasha_sequence': sequence,
        'total_months': 12,
    }


def calc_tri_pataka(planet_lons: Dict[str, float], 
                    varsha_lord: str,
                    muntha_sign_idx: int) -> Dict:
    """
    Tri-Pataka（三旗系统）
    Tajika占星中判断年度吉凶的重要技法
    
    三旗:
      1. Dasha Lord（大运守护星）的强度
      2. Muntha Lord（Muntha守护星）的强度  
      3. Year Lord（年度守护星）的强度
    
    三者都强→大吉年；三者都弱→凶年
    """
    muntha_lord = SIGN_LORDS.get(SIGNS[muntha_sign_idx], '')
    
    # 评估各守护星强度（简化版）
    def _strength(planet, lons):
        if planet not in lons:
            return 'unknown'
        lon = lons[planet]
        si = int(lon / 30) % 12
        # 简化：在角宫(1/4/7/10)=强，三方(5/9)=中，其他=弱
        house_from_asc = ((si - muntha_sign_idx) % 12) + 1
        if house_from_asc in (1, 4, 7, 10): return 'strong'
        if house_from_asc in (5, 9): return 'moderate'
        return 'weak'
    
    dl_strength = _strength(varsha_lord, planet_lons)
    ml_strength = _strength(muntha_lord, planet_lons)
    yl_strength = _strength(varsha_lord, planet_lons)
    
    strong_count = sum(1 for s in [dl_strength, ml_strength, yl_strength] if s == 'strong')
    weak_count = sum(1 for s in [dl_strength, ml_strength, yl_strength] if s == 'weak')
    
    if strong_count >= 2: verdict = 'excellent'
    elif weak_count >= 2: verdict = 'challenging'
    else: verdict = 'mixed'
    
    return {
        'dasha_lord': {'planet': varsha_lord, 'strength': dl_strength},
        'muntha_lord': {'planet': muntha_lord, 'strength': ml_strength},
        'year_lord': {'planet': varsha_lord, 'strength': yl_strength},
        'verdict': verdict,
        'interpretation': {
            'excellent': '三旗中两旗以上强旺，年度运势极佳',
            'mixed': '三旗力量参差不齐，年度运势起伏',
            'challenging': '三旗中两旗以上衰弱，年度运势挑战较大',
        }.get(verdict, ''),
    }


def _muntha_interp(sign, lord):
    """Muntha在12星座的基本解读"""
    interps = {
        'Aries': '年度主题：新开始、冒险、独立行动',
        'Taurus': '年度主题：财务稳定、物质积累、感官享受',
        'Gemini': '年度主题：学习、沟通、多元发展',
        'Cancer': '年度主题：家庭、情感、内在安全感',
        'Leo': '年度主题：创造力、领导力、自我表达',
        'Virgo': '年度主题：健康、服务、细节完善',
        'Libra': '年度主题：关系、合作、美学追求',
        'Scorpio': '年度主题：转化、深层变革、隐藏事物',
        'Sagittarius': '年度主题：远方旅行、哲学、高等教育',
        'Capricorn': '年度主题：事业成就、社会地位、长期规划',
        'Aquarius': '年度主题：社交网络、创新、人道主义',
        'Pisces': '年度主题：灵性成长、隐退、创意灵感',
    }
    return interps.get(sign, '')


def _year_theme(lord):
    """年度守护星主题"""
    themes = {
        'Sun': '权威、政府、父亲、领导力',
        'Moon': '公众、母亲、情感、直觉',
        'Mars': '行动、竞争、房地产、手术',
        'Mercury': '沟通、商业、学习、旅行',
        'Jupiter': '智慧、子女、宗教、财富',
        'Venus': '爱情、艺术、奢侈品、婚姻',
        'Saturn': '纪律、长寿、建筑、责任',
    }
    return themes.get(lord, '')
