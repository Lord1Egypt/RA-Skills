#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Avastha Calculator - 行星状态计算器
印度占星 Avastha（行星状态）系统

核心功能：
- Bala Avastha（年龄状态）：5种生命阶段
- Jagrat Avastha（警觉状态）：3种意识状态
- Deeptadi Avastha（情绪状态）：15种情绪/能量状态
- Lajjitadi Avastha（羞耻状态）：6种社会状态
- Shayanadi Avastha（姿态状态）：12种行为模式

参考文献：
- Brihat Parashara Hora Shastra (BPHS) Chapter 47-48
- Phaladeepika by Mantreswara
- Jataka Parijata by Vaidyanatha Dikshita
"""

from typing import Dict, List, Tuple
from enum import Enum

class BalaAvastha(Enum):
    """年龄状态（5种生命阶段）"""
    INFANT = "Infant"           # 婴儿期（0-6度）
    YOUNG = "Young"             # 少年期（6-12度）
    YOUTH = "Youth"             # 青年期（12-18度）
    OLD = "Old"                 # 老年期（18-24度）
    DEAD = "Dead"               # 死亡期（24-30度）

class JagratAvastha(Enum):
    """警觉状态（3种意识状态）"""
    AWAKE = "Awake"             # 清醒（Jagrat）
    DREAMING = "Dreaming"       # 梦境（Swapna）
    DEEP_SLEEP = "Deep Sleep"   # 深睡（Sushupti）

class DeeptadiAvastha(Enum):
    """情绪状态（15种）- Deeptadi Avastha"""
    DEEPTA = "Deepta"           # 光辉（Exalted）
    SWASTHA = "Swastha"         # 舒适（Own Sign）
    MUDITA = "Mudita"           # 快乐（Friend's Sign）
    SHANTA = "Shanta"           # 平静（Neutral Sign）
    DINA = "Dina"               # 沮丧（Enemy Sign）
    VIKALA = "Vikala"           # 残缺（Debilitated）
    KHALA = "Khala"             # 恶意（Combust）
    KOPA = "Kopa"               # 愤怒（Defeated in War）
    GARVITA = "Garvita"         # 骄傲（Victorious in War）
    KSHUDITA = "Kshudita"       # 饥饿（In Sandhi）
    TRUSHITA = "Trushita"       # 口渴（In Gandanta）
    MUDITA_SPECIAL = "Mudita"   # 特殊快乐（Aspected by Jupiter）
    KSHOBHITA = "Kshobhita"     # 激动（Aspected by Mars）
    LAJJITA = "Lajjita"         # 羞耻（Aspected by Saturn）
    GARVITA_SPECIAL = "Garvita" # 特殊骄傲（Aspected by Mercury）

class LajjitadiAvastha(Enum):
    """羞耻状态（6种社会状态）"""
    LAJJITA = "Lajjita"         # 羞耻（与敌对行星同宫）
    GARVITA = "Garvita"         # 骄傲（入庙）
    KSHUDITA = "Kshudita"       # 饥饿（在6/8/12宫）
    TRUSHITA = "Trushita"       # 口渴（在火象星座）
    MUDITA = "Mudita"           # 快乐（与友好行星同宫）
    KSHOBHITA = "Kshobhita"     # 激动（与火星同宫）

class ShayanadiAvastha(Enum):
    """姿态状态（12种行为模式）"""
    SHAYANA = "Shayana"         # 躺卧（在水象星座）
    UPAVESHANA = "Upaveshana"   # 坐着（在土象星座）
    NETRAPANI = "Netrapani"     # 手持武器（在火象星座）
    PRAKASHANA = "Prakashana"   # 显现（在风象星座）
    GAMANA = "Gamana"           # 行走（在双体星座）
    AGAMANA = "Agamana"         # 到来（在固定星座）
    SABHA = "Sabha"             # 集会（在变动星座）
    AGAMA = "Agama"             # 学习（在水星星座）
    BHOJANA = "Bhojana"         # 进食（在金星星座）
    NRITYALIPSA = "Nrityalipsa" # 舞蹈（在月亮星座）
    KAUTUKA = "Kautuka"         # 好奇（在木星星座）
    NIDRA = "Nidra"             # 睡眠（在土星星座）

class AvasthaCalculator:
    """行星状态计算器"""
    
    # 星座分类
    FIRE_SIGNS = ["Aries", "Leo", "Sagittarius"]
    EARTH_SIGNS = ["Taurus", "Virgo", "Capricorn"]
    AIR_SIGNS = ["Gemini", "Libra", "Aquarius"]
    WATER_SIGNS = ["Cancer", "Scorpio", "Pisces"]
    
    DUAL_SIGNS = ["Gemini", "Virgo", "Sagittarius", "Pisces"]
    FIXED_SIGNS = ["Taurus", "Leo", "Scorpio", "Aquarius"]
    MOVABLE_SIGNS = ["Aries", "Cancer", "Libra", "Capricorn"]
    
    # 行星主宰星座
    PLANET_SIGNS = {
        "Mercury": ["Gemini", "Virgo"],
        "Venus": ["Taurus", "Libra"],
        "Moon": ["Cancer"],
        "Jupiter": ["Sagittarius", "Pisces"],
        "Saturn": ["Capricorn", "Aquarius"],
        "Mars": ["Aries", "Scorpio"],
        "Sun": ["Leo"]
    }
    
    # 行星入庙/落陷度数
    EXALTATION = {
        "Sun": ("Aries", 10),
        "Moon": ("Taurus", 3),
        "Mars": ("Capricorn", 28),
        "Mercury": ("Virgo", 15),
        "Jupiter": ("Cancer", 5),
        "Venus": ("Pisces", 27),
        "Saturn": ("Libra", 20)
    }
    
    DEBILITATION = {
        "Sun": ("Libra", 10),
        "Moon": ("Scorpio", 3),
        "Mars": ("Cancer", 28),
        "Mercury": ("Pisces", 15),
        "Jupiter": ("Capricorn", 5),
        "Venus": ("Virgo", 27),
        "Saturn": ("Aries", 20)
    }
    
    def __init__(self):
        pass
    
    def calculate_all_avasthas(self, planet: str, sign: str, degree: float,
                               house: int, conjunctions: List[str] = None,
                               aspects: List[str] = None, is_combust: bool = False,
                               is_retrograde: bool = False) -> Dict[str, any]:
        """
        计算行星的所有Avastha状态
        
        Args:
            planet: 行星名
            sign: 所在星座
            degree: 星座内度数（0-30）
            house: 所在宫位（1-12）
            conjunctions: 合相的行星列表
            aspects: 相位的行星列表
            is_combust: 是否燃烧
            is_retrograde: 是否逆行
        
        Returns:
            所有Avastha状态的字典
        """
        result = {
            "planet": planet,
            "sign": sign,
            "degree": round(degree, 4),
            "house": house,
            "avasthas": {}
        }
        
        # 1. Bala Avastha（年龄状态）
        result["avasthas"]["Bala"] = self._calculate_bala_avastha(degree)
        
        # 2. Jagrat Avastha（警觉状态）
        result["avasthas"]["Jagrat"] = self._calculate_jagrat_avastha(planet, sign, house)
        
        # 3. Deeptadi Avastha（情绪状态）
        result["avasthas"]["Deeptadi"] = self._calculate_deeptadi_avastha(
            planet, sign, degree, is_combust, aspects
        )
        
        # 4. Lajjitadi Avastha（羞耻状态）
        result["avasthas"]["Lajjitadi"] = self._calculate_lajjitadi_avastha(
            planet, sign, house, conjunctions
        )
        
        # 5. Shayanadi Avastha（姿态状态）
        result["avasthas"]["Shayanadi"] = self._calculate_shayanadi_avastha(planet, sign)
        
        # 6. 综合解读
        result["interpretation"] = self._generate_interpretation(result["avasthas"])
        
        # 7. 补救建议
        result["remedies"] = self._generate_remedies(planet, result["avasthas"])
        
        return result
    
    def _calculate_bala_avastha(self, degree: float) -> Dict:
        """计算Bala Avastha（年龄状态）"""
        if degree < 6:
            state = BalaAvastha.INFANT
            strength = 0.2
            meaning = "婴儿期：行星力量微弱，潜力未开发，需要时间成长"
        elif degree < 12:
            state = BalaAvastha.YOUNG
            strength = 0.5
            meaning = "少年期：行星力量增长中，开始显现特质，但尚未成熟"
        elif degree < 18:
            state = BalaAvastha.YOUTH
            strength = 1.0
            meaning = "青年期：行星力量最强，充满活力，能够充分发挥作用"
        elif degree < 24:
            state = BalaAvastha.OLD
            strength = 0.7
            meaning = "老年期：行星力量开始衰退，经验丰富但活力下降"
        else:
            state = BalaAvastha.DEAD
            strength = 0.3
            meaning = "死亡期：行星力量极弱，难以发挥作用，需要补救"
        
        return {
            "state": state.value,
            "degree_range": f"{int(degree//6)*6}-{int(degree//6)*6+6}°",
            "strength": strength,
            "meaning": meaning
        }
    
    def _calculate_jagrat_avastha(self, planet: str, sign: str, house: int) -> Dict:
        """计算Jagrat Avastha（警觉状态）"""
        # 简化规则：
        # Awake: 在角宫（1,4,7,10）
        # Dreaming: 在续宫（2,5,8,11）
        # Deep Sleep: 在果宫（3,6,9,12）
        
        if house in [1, 4, 7, 10]:
            state = JagratAvastha.AWAKE
            meaning = "清醒状态：行星完全活跃，能够主动发挥作用，影响显著"
        elif house in [2, 5, 8, 11]:
            state = JagratAvastha.DREAMING
            meaning = "梦境状态：行星半活跃，作用不稳定，时强时弱"
        else:
            state = JagratAvastha.DEEP_SLEEP
            meaning = "深睡状态：行星不活跃，难以发挥作用，影响微弱"
        
        return {
            "state": state.value,
            "house": house,
            "meaning": meaning
        }
    
    def _calculate_deeptadi_avastha(self, planet: str, sign: str, degree: float,
                                    is_combust: bool, aspects: List[str] = None) -> Dict:
        """计算Deeptadi Avastha（情绪状态）"""
        aspects = aspects or []
        
        # 检查入庙/落陷
        if self._is_exalted(planet, sign, degree):
            state = DeeptadiAvastha.DEEPTA
            meaning = "光辉状态：行星处于最佳位置，能量充沛，带来积极结果"
        elif self._is_debilitated(planet, sign, degree):
            state = DeeptadiAvastha.VIKALA
            meaning = "残缺状态：行星处于最弱位置，能量受损，带来挑战"
        elif is_combust:
            state = DeeptadiAvastha.KHALA
            meaning = "恶意状态：行星被太阳燃烧，能量被压制，难以正常发挥"
        elif self._is_own_sign(planet, sign):
            state = DeeptadiAvastha.SWASTHA
            meaning = "舒适状态：行星在自己的星座，感觉自在，能够稳定发挥"
        elif self._is_friend_sign(planet, sign):
            state = DeeptadiAvastha.MUDITA
            meaning = "快乐状态：行星在友好星座，得到支持，能够良好发挥"
        elif self._is_enemy_sign(planet, sign):
            state = DeeptadiAvastha.DINA
            meaning = "沮丧状态：行星在敌对星座，受到压制，发挥受限"
        else:
            state = DeeptadiAvastha.SHANTA
            meaning = "平静状态：行星在中性星座，不强不弱，平稳发挥"
        
        # 检查相位影响
        aspect_effects = []
        if "Jupiter" in aspects:
            aspect_effects.append("木星相位：增加乐观和扩展性")
        if "Mars" in aspects:
            aspect_effects.append("火星相位：增加激情和冲动性")
        if "Saturn" in aspects:
            aspect_effects.append("土星相位：增加限制和责任感")
        if "Mercury" in aspects:
            aspect_effects.append("水星相位：增加智慧和沟通能力")
        
        return {
            "state": state.value,
            "meaning": meaning,
            "aspect_effects": aspect_effects
        }
    
    def _calculate_lajjitadi_avastha(self, planet: str, sign: str, house: int,
                                     conjunctions: List[str] = None) -> Dict:
        """计算Lajjitadi Avastha（羞耻状态）"""
        conjunctions = conjunctions or []
        
        # 简化规则
        if self._is_exalted(planet, sign, 15):  # 简化判断
            state = LajjitadiAvastha.GARVITA
            meaning = "骄傲状态：行星入庙，充满自信，能够展现最佳特质"
        elif house in [6, 8, 12]:
            state = LajjitadiAvastha.KSHUDITA
            meaning = "饥饿状态：行星在困难宫位，渴望满足，但难以获得"
        elif sign in self.FIRE_SIGNS:
            state = LajjitadiAvastha.TRUSHITA
            meaning = "口渴状态：行星在火象星座，能量过热，需要冷却"
        elif "Mars" in conjunctions:
            state = LajjitadiAvastha.KSHOBHITA
            meaning = "激动状态：与火星合相，能量激烈，容易冲动"
        elif any(self._is_enemy_planet(planet, conj) for conj in conjunctions):
            state = LajjitadiAvastha.LAJJITA
            meaning = "羞耻状态：与敌对行星同宫，感到不适，发挥受限"
        else:
            state = LajjitadiAvastha.MUDITA
            meaning = "快乐状态：与友好行星同宫，感到愉悦，能够良好发挥"
        
        return {
            "state": state.value,
            "meaning": meaning,
            "conjunctions": conjunctions
        }
    
    def _calculate_shayanadi_avastha(self, planet: str, sign: str) -> Dict:
        """计算Shayanadi Avastha（姿态状态）"""
        # 根据星座元素和类型判断
        if sign in self.WATER_SIGNS:
            state = ShayanadiAvastha.SHAYANA
            meaning = "躺卧姿态：行星在水象星座，处于休息状态，被动接受"
        elif sign in self.EARTH_SIGNS:
            state = ShayanadiAvastha.UPAVESHANA
            meaning = "坐着姿态：行星在土象星座，稳定扎根，缓慢行动"
        elif sign in self.FIRE_SIGNS:
            state = ShayanadiAvastha.NETRAPANI
            meaning = "持武器姿态：行星在火象星座，充满战斗力，主动出击"
        elif sign in self.AIR_SIGNS:
            state = ShayanadiAvastha.PRAKASHANA
            meaning = "显现姿态：行星在风象星座，灵活多变，善于表达"
        else:
            state = ShayanadiAvastha.GAMANA
            meaning = "行走姿态：行星处于移动状态，不断变化"
        
        # 根据行星主宰星座判断特殊状态
        for planet_name, signs in self.PLANET_SIGNS.items():
            if sign in signs:
                if planet_name == "Mercury":
                    state = ShayanadiAvastha.AGAMA
                    meaning = "学习姿态：在水星星座，专注于学习和沟通"
                elif planet_name == "Venus":
                    state = ShayanadiAvastha.BHOJANA
                    meaning = "进食姿态：在金星星座，享受物质和感官愉悦"
                elif planet_name == "Moon":
                    state = ShayanadiAvastha.NRITYALIPSA
                    meaning = "舞蹈姿态：在月亮星座，情感丰富，富有表现力"
                elif planet_name == "Jupiter":
                    state = ShayanadiAvastha.KAUTUKA
                    meaning = "好奇姿态：在木星星座，渴望探索和扩展"
                elif planet_name == "Saturn":
                    state = ShayanadiAvastha.NIDRA
                    meaning = "睡眠姿态：在土星星座，能量收缩，需要休息"
                break
        
        return {
            "state": state.value,
            "sign": sign,
            "meaning": meaning
        }
    
    def _is_exalted(self, planet: str, sign: str, degree: float) -> bool:
        """检查是否入庙"""
        if planet in self.EXALTATION:
            exalt_sign, exalt_degree = self.EXALTATION[planet]
            return sign == exalt_sign and abs(degree - exalt_degree) < 5
        return False
    
    def _is_debilitated(self, planet: str, sign: str, degree: float) -> bool:
        """检查是否落陷"""
        if planet in self.DEBILITATION:
            debil_sign, debil_degree = self.DEBILITATION[planet]
            return sign == debil_sign and abs(degree - debil_degree) < 5
        return False
    
    def _is_own_sign(self, planet: str, sign: str) -> bool:
        """检查是否在自己的星座"""
        return sign in self.PLANET_SIGNS.get(planet, [])
    
    def _is_friend_sign(self, planet: str, sign: str) -> bool:
        """检查是否在友好星座（简化版）"""
        # 这里需要完整的行星友好关系表，暂时简化
        return False
    
    def _is_enemy_sign(self, planet: str, sign: str) -> bool:
        """检查是否在敌对星座（简化版）"""
        # 这里需要完整的行星敌对关系表，暂时简化
        return False
    
    def _is_enemy_planet(self, planet1: str, planet2: str) -> bool:
        """检查两个行星是否敌对（简化版）"""
        # 这里需要完整的行星关系表，暂时简化
        enemies = {
            "Sun": ["Saturn", "Venus"],
            "Moon": ["Rahu", "Ketu"],
            "Mars": ["Mercury"],
            "Mercury": ["Moon"],
            "Jupiter": ["Mercury", "Venus"],
            "Venus": ["Sun", "Moon"],
            "Saturn": ["Sun", "Moon", "Mars"]
        }
        return planet2 in enemies.get(planet1, [])
    
    def _generate_interpretation(self, avasthas: Dict) -> str:
        """生成综合解读"""
        interpretation = "行星状态综合分析：\n\n"
        
        # Bala Avastha
        bala = avasthas["Bala"]
        interpretation += f"1. 年龄状态：{bala['state']}（{bala['degree_range']}）\n"
        interpretation += f"   {bala['meaning']}\n\n"
        
        # Jagrat Avastha
        jagrat = avasthas["Jagrat"]
        interpretation += f"2. 警觉状态：{jagrat['state']}（第{jagrat['house']}宫）\n"
        interpretation += f"   {jagrat['meaning']}\n\n"
        
        # Deeptadi Avastha
        deeptadi = avasthas["Deeptadi"]
        interpretation += f"3. 情绪状态：{deeptadi['state']}\n"
        interpretation += f"   {deeptadi['meaning']}\n"
        if deeptadi['aspect_effects']:
            interpretation += "   相位影响：\n"
            for effect in deeptadi['aspect_effects']:
                interpretation += f"   - {effect}\n"
        interpretation += "\n"
        
        # Lajjitadi Avastha
        lajjitadi = avasthas["Lajjitadi"]
        interpretation += f"4. 社会状态：{lajjitadi['state']}\n"
        interpretation += f"   {lajjitadi['meaning']}\n\n"
        
        # Shayanadi Avastha
        shayanadi = avasthas["Shayanadi"]
        interpretation += f"5. 行为模式：{shayanadi['state']}（{shayanadi['sign']}）\n"
        interpretation += f"   {shayanadi['meaning']}\n"
        
        return interpretation
    
    def _generate_remedies(self, planet: str, avasthas: Dict) -> List[str]:
        """生成补救建议"""
        remedies = []
        
        # 根据Bala Avastha
        bala_strength = avasthas["Bala"]["strength"]
        if bala_strength < 0.5:
            remedies.append(f"行星处于弱势年龄阶段，建议佩戴{planet}对应的宝石")
            remedies.append(f"在{planet}主管的日子进行布施和祈祷")
        
        # 根据Jagrat Avastha
        if avasthas["Jagrat"]["state"] == "Deep Sleep":
            remedies.append("行星处于深睡状态，建议通过冥想和咒语激活其能量")
        
        # 根据Deeptadi Avastha
        deeptadi_state = avasthas["Deeptadi"]["state"]
        if deeptadi_state in ["Vikala", "Khala", "Dina"]:
            remedies.append(f"行星处于{deeptadi_state}状态，需要特别补救")
            remedies.append(f"念诵{planet}的Beeja Mantra（种子咒）")
        
        return remedies


# 示例用法
if __name__ == "__main__":
    calculator = AvasthaCalculator()
    
    # 示例：太阳在白羊座15度，第10宫
    result = calculator.calculate_all_avasthas(
        planet="Sun",
        sign="Aries",
        degree=15.0,
        house=10,
        conjunctions=["Mercury"],
        aspects=["Jupiter", "Saturn"],
        is_combust=False,
        is_retrograde=False
    )
    
    print("="*60)
    print(f"{result['planet']} 在 {result['sign']} {result['degree']}° (第{result['house']}宫)")
    print("="*60)
    print(result['interpretation'])
    
    if result['remedies']:
        print("\n补救建议：")
        for i, remedy in enumerate(result['remedies'], 1):
            print(f"{i}. {remedy}")
