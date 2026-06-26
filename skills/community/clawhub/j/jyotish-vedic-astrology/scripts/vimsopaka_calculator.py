#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Vimsopaka Bala Calculator - 分盘综合力量计算器
印度占星 Vimsopaka Bala（20分力量）系统

核心功能：
- 计算16种分盘（Shodasavarga）的行星尊严
- 根据BPHS权重系统计算Vimsopaka Bala
- 提供行星在各分盘的综合力量评分
- 支持Dasa Varga（10分盘）和Shodasavarga（16分盘）两种模式

参考文献：
- Brihat Parashara Hora Shastra (BPHS) Chapter 7
- B.V. Raman - "A Manual of Hindu Astrology"
"""

from typing import Dict, List, Tuple
from enum import Enum

class VargaType(Enum):
    """分盘类型"""
    D1 = "Rashi"           # 本命盘
    D2 = "Hora"            # 财富
    D3 = "Drekkana"        # 兄弟姐妹
    D4 = "Chaturthamsa"    # 财产/运气
    D7 = "Saptamsa"        # 子女
    D9 = "Navamsa"         # 配偶/灵性
    D10 = "Dasamsa"        # 事业
    D12 = "Dwadasamsa"     # 父母
    D16 = "Shodasamsa"     # 交通工具
    D20 = "Vimsamsa"       # 灵性修行
    D24 = "Chaturvimsamsa" # 教育/学习
    D27 = "Bhamsa"         # 力量/弱点
    D30 = "Trimsamsa"      # 不幸/困难
    D40 = "Khavedamsa"     # 吉凶效果
    D45 = "Akshavedamsa"   # 全面判断
    D60 = "Shashtiamsa"    # 前世业力

class DignityLevel(Enum):
    """行星尊严等级"""
    EXALTED = "Exalted"           # 入庙（最高）
    MOOLATRIKONA = "Moolatrikona" # 根本三角
    OWN_SIGN = "Own Sign"         # 自己的星座
    FRIEND = "Friend"             # 友好星座
    NEUTRAL = "Neutral"           # 中性星座
    ENEMY = "Enemy"               # 敌对星座
    DEBILITATED = "Debilitated"   # 落陷（最低）

class VimsopakaBalaCalculator:
    """Vimsopaka Bala计算器"""
    
    # BPHS标准权重系统（Shodasavarga - 16分盘）
    SHODASAVARGA_WEIGHTS = {
        VargaType.D1: 3.5,   # Rashi
        VargaType.D2: 1.0,   # Hora
        VargaType.D3: 1.0,   # Drekkana
        VargaType.D4: 0.5,   # Chaturthamsa
        VargaType.D7: 0.5,   # Saptamsa
        VargaType.D9: 3.5,   # Navamsa
        VargaType.D10: 0.5,  # Dasamsa
        VargaType.D12: 0.5,  # Dwadasamsa
        VargaType.D16: 2.0,  # Shodasamsa
        VargaType.D20: 0.5,  # Vimsamsa
        VargaType.D24: 0.5,  # Chaturvimsamsa
        VargaType.D27: 0.5,  # Bhamsa
        VargaType.D30: 1.0,  # Trimsamsa
        VargaType.D40: 0.5,  # Khavedamsa
        VargaType.D45: 0.5,  # Akshavedamsa
        VargaType.D60: 4.0   # Shashtiamsa
    }
    
    # Dasa Varga权重系统（10分盘 - 简化版）
    DASAVARGA_WEIGHTS = {
        VargaType.D1: 3.0,
        VargaType.D2: 1.5,
        VargaType.D3: 1.5,
        VargaType.D7: 1.5,
        VargaType.D9: 3.0,
        VargaType.D10: 1.5,
        VargaType.D12: 1.5,
        VargaType.D16: 1.5,
        VargaType.D30: 1.5,
        VargaType.D60: 5.0
    }
    
    # 尊严等级对应的Virupas（力量单位）
    DIGNITY_VIRUPAS = {
        DignityLevel.EXALTED: 20.0,
        DignityLevel.MOOLATRIKONA: 18.0,
        DignityLevel.OWN_SIGN: 15.0,
        DignityLevel.FRIEND: 10.0,
        DignityLevel.NEUTRAL: 7.5,
        DignityLevel.ENEMY: 5.0,
        DignityLevel.DEBILITATED: 2.0
    }
    
    # 力量等级分类（基于总分）
    STRENGTH_CATEGORIES = {
        "Parijatamsa": (18.0, 20.0),    # 极强（18-20）
        "Uttamamsa": (16.0, 18.0),      # 优秀（16-18）
        "Gopuramsa": (12.0, 16.0),      # 良好（12-16）
        "Simhasanamsa": (10.0, 12.0),   # 中等偏上（10-12）
        "Paravatamsa": (8.0, 10.0),     # 中等（8-10）
        "Devalokamsa": (6.0, 8.0),      # 中等偏下（6-8）
        "Brahmalokamsa": (4.0, 6.0),    # 较弱（4-6）
        "Airavata": (2.0, 4.0),         # 弱（2-4）
        "Vaiseshikamsa": (0.0, 2.0)     # 极弱（0-2）
    }
    
    def __init__(self, mode: str = "shodasavarga"):
        """
        初始化计算器
        
        Args:
            mode: "shodasavarga" (16分盘) 或 "dasavarga" (10分盘)
        """
        self.mode = mode
        self.weights = self.SHODASAVARGA_WEIGHTS if mode == "shodasavarga" else self.DASAVARGA_WEIGHTS
        
    def calculate_vimsopaka_bala(self, planet_vargas: Dict[str, Dict[VargaType, DignityLevel]]) -> Dict[str, Dict]:
        """
        计算所有行星的Vimsopaka Bala
        
        Args:
            planet_vargas: {行星名: {分盘类型: 尊严等级}}
        
        Returns:
            {行星名: {
                "total_score": 总分,
                "category": 力量等级,
                "varga_scores": {分盘: 得分},
                "interpretation": 解读
            }}
        """
        results = {}
        
        for planet, vargas in planet_vargas.items():
            planet_result = self._calculate_planet_vimsopaka(planet, vargas)
            results[planet] = planet_result
        
        return results
    
    def _calculate_planet_vimsopaka(self, planet: str, vargas: Dict[VargaType, DignityLevel]) -> Dict:
        """计算单个行星的Vimsopaka Bala"""
        varga_scores = {}
        total_weighted_score = 0.0
        total_weight = 0.0
        
        # 计算每个分盘的得分
        for varga_type, dignity in vargas.items():
            if varga_type in self.weights:
                # 获取尊严对应的Virupas
                virupas = self.DIGNITY_VIRUPAS.get(dignity, 0.0)
                
                # 获取分盘权重
                weight = self.weights[varga_type]
                
                # 计算加权得分
                weighted_score = virupas * weight
                
                varga_scores[varga_type.value] = {
                    "dignity": dignity.value,
                    "virupas": virupas,
                    "weight": weight,
                    "weighted_score": round(weighted_score, 2)
                }
                
                total_weighted_score += weighted_score
                total_weight += weight
        
        # 计算最终得分（归一化到20分制）
        if total_weight > 0:
            final_score = total_weighted_score / total_weight
        else:
            final_score = 0.0
        
        # 确定力量等级
        category = self._get_strength_category(final_score)
        
        # 生成解读
        interpretation = self._generate_interpretation(planet, final_score, category, varga_scores)
        
        return {
            "planet": planet,
            "total_score": round(final_score, 2),
            "category": category,
            "varga_scores": varga_scores,
            "interpretation": interpretation,
            "mode": self.mode
        }
    
    def _get_strength_category(self, score: float) -> str:
        """根据得分确定力量等级"""
        for category, (min_score, max_score) in self.STRENGTH_CATEGORIES.items():
            if min_score <= score < max_score:
                return category
        return "Vaiseshikamsa"  # 默认最低等级
    
    def _generate_interpretation(self, planet: str, score: float, category: str, varga_scores: Dict) -> str:
        """生成解读文本"""
        interpretation = f"{planet}的Vimsopaka Bala得分为{score:.2f}/20，属于{category}等级。\n\n"
        
        # 根据等级给出解读
        if score >= 16:
            interpretation += "这是极强的行星力量，表示该行星在生活中能够充分发挥其积极作用，带来显著的成果和成功。"
        elif score >= 12:
            interpretation += "这是良好的行星力量，表示该行星能够有效发挥作用，在其主管领域带来正面影响。"
        elif score >= 8:
            interpretation += "这是中等的行星力量，表示该行星的作用较为平衡，既有积极面也有挑战。"
        elif score >= 4:
            interpretation += "这是较弱的行星力量，表示该行星在发挥作用时会遇到一些困难和阻碍。"
        else:
            interpretation += "这是极弱的行星力量，表示该行星难以充分发挥其作用，需要通过补救措施来增强。"
        
        # 找出最强和最弱的分盘
        if varga_scores:
            sorted_vargas = sorted(varga_scores.items(), key=lambda x: x[1]['weighted_score'], reverse=True)
            strongest = sorted_vargas[0]
            weakest = sorted_vargas[-1]
            
            interpretation += f"\n\n最强分盘：{strongest[0]}（{strongest[1]['dignity']}，得分{strongest[1]['weighted_score']}）"
            interpretation += f"\n最弱分盘：{weakest[0]}（{weakest[1]['dignity']}，得分{weakest[1]['weighted_score']}）"
        
        return interpretation
    
    def compare_planets(self, results: Dict[str, Dict]) -> List[Tuple[str, float]]:
        """
        比较所有行星的力量，返回排序列表
        
        Args:
            results: calculate_vimsopaka_bala的返回结果
        
        Returns:
            [(行星名, 得分), ...] 按得分降序排列
        """
        planet_scores = [(planet, data["total_score"]) for planet, data in results.items()]
        return sorted(planet_scores, key=lambda x: x[1], reverse=True)
    
    def get_remedial_recommendations(self, planet: str, score: float) -> List[str]:
        """
        根据Vimsopaka Bala得分提供补救建议
        
        Args:
            planet: 行星名
            score: Vimsopaka Bala得分
        
        Returns:
            补救建议列表
        """
        recommendations = []
        
        if score < 8:  # 力量较弱，需要补救
            recommendations.append(f"建议佩戴{planet}对应的宝石来增强力量")
            recommendations.append(f"在{planet}主管的日子进行布施（Daan）")
            recommendations.append(f"念诵{planet}的咒语（Mantra）")
            recommendations.append(f"在{planet}主管的时辰进行重要活动")
            
            if score < 4:  # 极弱，需要额外补救
                recommendations.append(f"考虑进行{planet}的火祭仪式（Homa）")
                recommendations.append(f"在{planet}主管的日子断食")
        
        return recommendations


# 示例用法
if __name__ == "__main__":
    # 创建计算器（使用16分盘模式）
    calculator = VimsopakaBalaCalculator(mode="shodasavarga")
    
    # 示例数据：太阳在各分盘的尊严
    sun_vargas = {
        VargaType.D1: DignityLevel.EXALTED,
        VargaType.D2: DignityLevel.OWN_SIGN,
        VargaType.D3: DignityLevel.FRIEND,
        VargaType.D9: DignityLevel.MOOLATRIKONA,
        VargaType.D10: DignityLevel.FRIEND,
        VargaType.D12: DignityLevel.NEUTRAL,
        VargaType.D16: DignityLevel.OWN_SIGN,
        VargaType.D20: DignityLevel.FRIEND,
        VargaType.D30: DignityLevel.ENEMY,
        VargaType.D60: DignityLevel.EXALTED
    }
    
    # 计算所有行星的Vimsopaka Bala
    planet_vargas = {
        "Sun": sun_vargas
    }
    
    results = calculator.calculate_vimsopaka_bala(planet_vargas)
    
    # 打印结果
    for planet, data in results.items():
        print(f"\n{'='*60}")
        print(f"{planet} - Vimsopaka Bala分析")
        print(f"{'='*60}")
        print(f"总分：{data['total_score']}/20")
        print(f"等级：{data['category']}")
        print(f"\n{data['interpretation']}")
        
        # 如果需要补救
        remedies = calculator.get_remedial_recommendations(planet, data['total_score'])
        if remedies:
            print(f"\n补救建议：")
            for i, remedy in enumerate(remedies, 1):
                print(f"{i}. {remedy}")
