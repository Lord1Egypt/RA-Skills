#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Argala（门闩）行星干预模块 v1.0
Parashara体系的行星影响力锁定机制

Argala = "门闩/木栓"，指一颗行星通过特定宫位对另一颗行星产生
不可阻挡的干预影响。这是判断行星力量和结果表达的关键技法。

规则:
  - 主Argala: 2/4/11宫位产生正面干预
  - 副Argala: 5/8宫位（从第2宫起算）产生正面干预
  - Virodha Argala: 12/10/3宫位产生反向阻止
  - 更强Argala: 多颗行星在同一Argala位置则力量增强
"""
from typing import Dict, List

SIGNS = ['Aries','Taurus','Gemini','Cancer','Leo','Virgo',
         'Libra','Scorpio','Sagittarius','Capricorn','Aquarius','Pisces']
SIGN_LORDS = {'Aries':'Mars','Taurus':'Venus','Gemini':'Mercury','Cancer':'Moon',
    'Leo':'Sun','Virgo':'Mercury','Libra':'Venus','Scorpio':'Mars',
    'Sagittarius':'Jupiter','Capricorn':'Saturn','Aquarius':'Saturn','Pisces':'Jupiter'}

BENEFICS = ['Jupiter', 'Venus', 'Moon']
MALEFICS = ['Saturn', 'Mars', 'Sun', 'Rahu', 'Ketu']


def calc_argala(planet_sign_indices: Dict[str, int], asc_sign_idx: int) -> Dict:
    """
    计算所有行星的Argala和Virodha Argala
    
    参数:
        planet_sign_indices: {'Sun': 0, 'Moon': 3, ...} 行星所在星座索引
        asc_sign_idx: 上升星座索引
    
    返回: {
        planet_name: {
            'house': 宫位,
            'argala_from': [对哪些宫位有Argala],
            'argala_to': [被哪些行星Argala],
            'virodha_from': [被哪些行星阻止],
            'net_argala': 净Argala力量评估,
        }
    }
    """
    # 计算各行星宫位
    houses = {}
    for pname, si in planet_sign_indices.items():
        h = ((si - asc_sign_idx) % 12) + 1
        houses[pname] = h
    
    # 主Argala位置（从目标行星宫位起算）
    # 2宫=财富Argala, 4宫=幸福Argala, 11宫=收益Argala
    MAIN_ARGALA = [2, 4, 11]
    # 副Argala位置（特殊条件：需要无其他行星在相应Virodha位置）
    SUB_ARGALA = [5, 8]  # 第5宫=权力Argala(当2宫无Virodha), 第8宫(当4宫无Virodha)
    # Virodha Argala位置（反向阻止）
    VIRODHA = {2: 12, 4: 10, 11: 3, 5: 9, 8: 2}
    
    results = {}
    
    for target_p, target_h in houses.items():
        argala_on_target = []  # 作用于此行星的Argala
        virodha_on_target = []  # 作用于此行星的Virodha
        argala_by_target = []  # 此行星作用于其他位置的Argala
        
        # 检查哪些行星对此行星有Argala
        for source_p, source_h in houses.items():
            if source_p == target_p:
                continue
            rel = ((source_h - target_h) % 12) + 1
            
            # 主Argala检查
            if rel in MAIN_ARGALA:
                nature = 'benefic' if source_p in BENEFICS else 'malefic'
                strength = 'strong' if _is_strong_argala(source_p, rel) else 'normal'
                argala_on_target.append({
                    'source': source_p, 'house_from': rel,
                    'type': 'main', 'nature': nature, 'strength': strength,
                    'effect': _argala_effect(rel, nature),
                })
            
            # 副Argala检查
            elif rel in SUB_ARGALA:
                nature = 'benefic' if source_p in BENEFICS else 'malefic'
                argala_on_target.append({
                    'source': source_p, 'house_from': rel,
                    'type': 'sub', 'nature': nature, 'strength': 'conditional',
                    'effect': _argala_effect(rel, nature),
                })
            
            # Virodha检查
            for a_house, v_house in VIRODHA.items():
                if rel == v_house:
                    nature = 'benefic' if source_p in BENEFICS else 'malefic'
                    virodha_on_target.append({
                        'source': source_p, 'house_from': rel,
                        'blocks_argala_from': a_house,
                        'nature': nature,
                    })
        
        # 此行星对其他位置产生的Argala
        for rel_house in MAIN_ARGALA:
            target_house = ((target_h - 1 + rel_house - 1) % 12) + 1
            planets_there = [p for p, h in houses.items() if h == target_house]
            if planets_there:
                argala_by_target.append({
                    'argala_type': f'{rel_house}宫Argala',
                    'target_house': target_house,
                    'affects': planets_there,
                    'effect': _argala_effect(rel_house, 'benefic' if target_p in BENEFICS else 'malefic'),
                })
        
        # 净Argala评估
        benefic_argala = sum(1 for a in argala_on_target if a['nature'] == 'benefic')
        malefic_argala = sum(1 for a in argala_on_target if a['nature'] == 'malefic')
        benefic_virodha = sum(1 for v in virodha_on_target if v['nature'] == 'benefic')
        malefic_virodha = sum(1 for v in virodha_on_target if v['nature'] == 'malefic')
        
        net = (benefic_argala - malefic_virodha) - (malefic_argala - benefic_virodha)
        
        results[target_p] = {
            'house': target_h,
            'argala_on_this': argala_on_target,
            'virodha_on_this': virodha_on_target,
            'argala_by_this': argala_by_target,
            'net_score': net,
            'net_assessment': 'strongly_supported' if net >= 2 else 'supported' if net >= 1 
                else 'blocked' if net <= -2 else 'neutral',
        }
    
    return results


def _is_strong_argala(planet, house):
    """判断Argala是否特别强（有2+行星在同一位置）"""
    return False  # 需要宫位行星数信息，简化返回


def _argala_effect(house, nature):
    """Argala效果描述"""
    effects = {
        2: {'benefic': '财富和资源流入', 'malefic': '财务压力和资源消耗'},
        4: {'benefic': '幸福感、住所和内心平静增强', 'malefic': '家庭不和、住所问题'},
        11: {'benefic': '收益、愿望实现和社会认可', 'malefic': '损失、社会障碍'},
        5: {'benefic': '智慧、权力和创造力增强', 'malefic': '智力困扰、决策失误'},
        8: {'benefic': '隐藏资源和转化力量', 'malefic': '隐藏障碍和突发危机'},
    }
    return effects.get(house, {}).get(nature, '一般性影响')
