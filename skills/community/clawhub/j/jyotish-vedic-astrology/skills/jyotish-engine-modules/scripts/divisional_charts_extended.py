#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Divisional Charts Extended - D2-D60完整分盘宫位图计算器
印度占星 Shodasavarga（16分盘）+ 扩展分盘系统

核心功能：
- 计算D1-D60所有分盘的行星位置
- 生成每个分盘的12宫位行星分布图
- 支持BPHS标准算法
- 提供分盘上升点计算
- 输出可视化宫位图数据

参考文献：
- Brihat Parashara Hora Shastra (BPHS) Chapter 6
- Phaladeepika by Mantreswara
- Jataka Parijata by Vaidyanatha Dikshita
"""

from typing import Dict, List, Tuple
from enum import Enum

class VargaType(Enum):
    """分盘类型枚举"""
    D1 = (1, "Rashi", "本命盘")
    D2 = (2, "Hora", "财富")
    D3 = (3, "Drekkana", "兄弟姐妹")
    D4 = (4, "Chaturthamsa", "财产/运气")
    D5 = (5, "Panchamsa", "名声/权力")
    D6 = (6, "Shashthamsa", "健康/敌人")
    D7 = (7, "Saptamsa", "子女")
    D8 = (8, "Ashtamsa", "突发事件")
    D9 = (9, "Navamsa", "配偶/灵性")
    D10 = (10, "Dasamsa", "事业")
    D11 = (11, "Rudramsa", "破坏/转化")
    D12 = (12, "Dwadasamsa", "父母")
    D16 = (16, "Shodasamsa", "交通工具/舒适")
    D20 = (20, "Vimsamsa", "灵性修行")
    D24 = (24, "Chaturvimsamsa", "教育/学习")
    D27 = (27, "Bhamsa", "力量/弱点")
    D30 = (30, "Trimsamsa", "不幸/困难")
    D40 = (40, "Khavedamsa", "吉凶效果")
    D45 = (45, "Akshavedamsa", "全面判断")
    D60 = (60, "Shashtiamsa", "前世业力")
    
    def __init__(self, division: int, name: str, meaning: str):
        self.division = division
        self.varga_name = name
        self.meaning = meaning

class DivisionalChartsCalculator:
    """分盘计算器"""
    
    SIGNS = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
             "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]
    
    # 星座分类
    MOVABLE_SIGNS = [0, 3, 6, 9]      # Aries, Cancer, Libra, Capricorn
    FIXED_SIGNS = [1, 4, 7, 10]       # Taurus, Leo, Scorpio, Aquarius
    DUAL_SIGNS = [2, 5, 8, 11]        # Gemini, Virgo, Sagittarius, Pisces
    
    ODD_SIGNS = [0, 2, 4, 6, 8, 10]   # 奇数星座
    EVEN_SIGNS = [1, 3, 5, 7, 9, 11]  # 偶数星座
    
    def __init__(self):
        pass
    
    def calculate_all_vargas(self, planet_positions: Dict[str, float],
                            asc_degree: float) -> Dict[str, Dict]:
        """
        计算所有分盘的行星位置
        
        Args:
            planet_positions: {行星名: 黄道度数(0-360)}
            asc_degree: 上升点黄道度数(0-360)
        
        Returns:
            {分盘名: {
                "planets": {行星名: {"sign": 星座, "degree": 度数, "house": 宫位}},
                "ascendant": {"sign": 星座, "degree": 度数},
                "house_chart": [宫位1的行星列表, 宫位2的行星列表, ...]
            }}
        """
        results = {}
        
        # 计算所有分盘
        for varga_type in VargaType:
            varga_result = self._calculate_single_varga(
                varga_type, planet_positions, asc_degree
            )
            results[varga_type.varga_name] = varga_result
        
        return results
    
    def _calculate_single_varga(self, varga_type: VargaType,
                                planet_positions: Dict[str, float],
                                asc_degree: float) -> Dict:
        """计算单个分盘"""
        division = varga_type.division
        
        # 计算分盘上升点
        varga_asc = self._calculate_varga_position(asc_degree, division)
        varga_asc_sign = int(varga_asc // 30)
        varga_asc_degree = varga_asc % 30
        
        # 计算所有行星的分盘位置
        varga_planets = {}
        for planet, degree in planet_positions.items():
            varga_pos = self._calculate_varga_position(degree, division)
            varga_sign = int(varga_pos // 30)
            varga_degree = varga_pos % 30
            
            # 计算宫位（从上升点开始）
            house = ((varga_sign - varga_asc_sign) % 12) + 1
            
            varga_planets[planet] = {
                "sign": self.SIGNS[varga_sign],
                "sign_index": varga_sign,
                "degree": round(varga_degree, 4),
                "house": house,
                "absolute_degree": round(varga_pos, 4)
            }
        
        # 生成宫位图（12个宫位，每个宫位包含的行星列表）
        house_chart = [[] for _ in range(12)]
        for planet, data in varga_planets.items():
            house_chart[data["house"] - 1].append(planet)
        
        return {
            "division": division,
            "name": varga_type.varga_name,
            "meaning": varga_type.meaning,
            "ascendant": {
                "sign": self.SIGNS[varga_asc_sign],
                "sign_index": varga_asc_sign,
                "degree": round(varga_asc_degree, 4)
            },
            "planets": varga_planets,
            "house_chart": house_chart
        }
    
    def _calculate_varga_position(self, degree: float, division: int) -> float:
        """
        计算分盘位置（BPHS标准算法）
        
        Args:
            degree: 黄道度数(0-360)
            division: 分盘数(2-60)
        
        Returns:
            分盘中的黄道度数(0-360)
        """
        # 获取星座索引和星座内度数
        sign_index = int(degree // 30)
        sign_degree = degree % 30
        
        # 根据不同分盘使用不同算法
        if division == 2:
            return self._calculate_d2(sign_index, sign_degree)
        elif division == 3:
            return self._calculate_d3(sign_index, sign_degree)
        elif division == 4:
            return self._calculate_d4(sign_index, sign_degree)
        elif division == 5:
            return self._calculate_d5(sign_index, sign_degree)
        elif division == 6:
            return self._calculate_d6(sign_index, sign_degree)
        elif division == 7:
            return self._calculate_d7(sign_index, sign_degree)
        elif division == 8:
            return self._calculate_d8(sign_index, sign_degree)
        elif division == 9:
            return self._calculate_d9(sign_index, sign_degree)
        elif division == 10:
            return self._calculate_d10(sign_index, sign_degree)
        elif division == 11:
            return self._calculate_d11(sign_index, sign_degree)
        elif division == 12:
            return self._calculate_d12(sign_index, sign_degree)
        elif division == 16:
            return self._calculate_d16(sign_index, sign_degree)
        elif division == 20:
            return self._calculate_d20(sign_index, sign_degree)
        elif division == 24:
            return self._calculate_d24(sign_index, sign_degree)
        elif division == 27:
            return self._calculate_d27(sign_index, sign_degree)
        elif division == 30:
            return self._calculate_d30(sign_index, sign_degree)
        elif division == 40:
            return self._calculate_d40(sign_index, sign_degree)
        elif division == 45:
            return self._calculate_d45(sign_index, sign_degree)
        elif division == 60:
            return self._calculate_d60(sign_index, sign_degree)
        else:
            # 通用算法（适用于其他分盘）
            return self._calculate_generic_varga(sign_index, sign_degree, division)
    
    def _calculate_d2(self, sign_index: int, sign_degree: float) -> float:
        """D2 Hora - 财富分盘"""
        # 奇数星座：0-15度→Leo，15-30度→Cancer
        # 偶数星座：0-15度→Cancer，15-30度→Leo
        if sign_index in self.ODD_SIGNS:
            if sign_degree < 15:
                return 4 * 30 + sign_degree * 2  # Leo
            else:
                return 3 * 30 + (sign_degree - 15) * 2  # Cancer
        else:
            if sign_degree < 15:
                return 3 * 30 + sign_degree * 2  # Cancer
            else:
                return 4 * 30 + (sign_degree - 15) * 2  # Leo
    
    def _calculate_d3(self, sign_index: int, sign_degree: float) -> float:
        """D3 Drekkana - 兄弟姐妹分盘"""
        # 每个星座分为3个10度区间
        # 第1个10度→本星座，第2个10度→第5个星座，第3个10度→第9个星座
        drekkana = int(sign_degree // 10)
        offset = [0, 4, 8][drekkana]
        varga_sign = (sign_index + offset) % 12
        varga_degree = (sign_degree % 10) * 3
        return varga_sign * 30 + varga_degree
    
    def _calculate_d4(self, sign_index: int, sign_degree: float) -> float:
        """D4 Chaturthamsa - 财产/运气分盘"""
        # 每个星座分为4个7.5度区间
        part = int(sign_degree // 7.5)
        varga_sign = (sign_index + part * 3) % 12
        varga_degree = (sign_degree % 7.5) * 4
        return varga_sign * 30 + varga_degree
    
    def _calculate_d7(self, sign_index: int, sign_degree: float) -> float:
        """D7 Saptamsa - 子女分盘"""
        # 每个星座分为7个约4.286度区间
        part = int(sign_degree // (30/7))
        if sign_index in self.ODD_SIGNS:
            varga_sign = (sign_index + part) % 12
        else:
            varga_sign = (sign_index + 6 + part) % 12
        varga_degree = (sign_degree % (30/7)) * 7
        return varga_sign * 30 + varga_degree
    
    def _calculate_d9(self, sign_index: int, sign_degree: float) -> float:
        """D9 Navamsa - 配偶/灵性分盘（最重要的分盘）"""
        # 每个星座分为9个3.333度区间
        part = int(sign_degree // (30/9))
        
        # 根据星座类型确定起始点
        if sign_index in self.MOVABLE_SIGNS:
            start = sign_index  # 从本星座开始
        elif sign_index in self.FIXED_SIGNS:
            start = (sign_index + 8) % 12  # 从第9个星座开始
        else:  # DUAL_SIGNS
            start = (sign_index + 4) % 12  # 从第5个星座开始
        
        varga_sign = (start + part) % 12
        varga_degree = (sign_degree % (30/9)) * 9
        return varga_sign * 30 + varga_degree
    
    def _calculate_d10(self, sign_index: int, sign_degree: float) -> float:
        """D10 Dasamsa - 事业分盘"""
        # 每个星座分为10个3度区间
        part = int(sign_degree // 3)
        if sign_index in self.ODD_SIGNS:
            varga_sign = (sign_index + part) % 12
        else:
            varga_sign = (sign_index + 8 + part) % 12
        varga_degree = (sign_degree % 3) * 10
        return varga_sign * 30 + varga_degree
    
    def _calculate_d12(self, sign_index: int, sign_degree: float) -> float:
        """D12 Dwadasamsa - 父母分盘"""
        # 每个星座分为12个2.5度区间
        part = int(sign_degree // 2.5)
        varga_sign = (sign_index + part) % 12
        varga_degree = (sign_degree % 2.5) * 12
        return varga_sign * 30 + varga_degree
    
    def _calculate_d16(self, sign_index: int, sign_degree: float) -> float:
        """D16 Shodasamsa - 交通工具/舒适分盘"""
        # 每个星座分为16个1.875度区间
        part = int(sign_degree // 1.875)
        if sign_index in self.MOVABLE_SIGNS:
            start = sign_index
        elif sign_index in self.FIXED_SIGNS:
            start = (sign_index + 4) % 12
        else:
            start = (sign_index + 8) % 12
        varga_sign = (start + part) % 12
        varga_degree = (sign_degree % 1.875) * 16
        return varga_sign * 30 + varga_degree
    
    def _calculate_d20(self, sign_index: int, sign_degree: float) -> float:
        """D20 Vimsamsa - 灵性修行分盘"""
        # 每个星座分为20个1.5度区间
        part = int(sign_degree // 1.5)
        if sign_index in self.MOVABLE_SIGNS:
            start = sign_index
        elif sign_index in self.FIXED_SIGNS:
            start = (sign_index + 8) % 12
        else:
            start = (sign_index + 4) % 12
        varga_sign = (start + part) % 12
        varga_degree = (sign_degree % 1.5) * 20
        return varga_sign * 30 + varga_degree
    
    def _calculate_d24(self, sign_index: int, sign_degree: float) -> float:
        """D24 Chaturvimsamsa - 教育/学习分盘"""
        # 每个星座分为24个1.25度区间
        part = int(sign_degree // 1.25)
        if sign_index in self.ODD_SIGNS:
            varga_sign = (4 + part) % 12  # 从Leo开始
        else:
            varga_sign = (3 + part) % 12  # 从Cancer开始
        varga_degree = (sign_degree % 1.25) * 24
        return varga_sign * 30 + varga_degree
    
    def _calculate_d27(self, sign_index: int, sign_degree: float) -> float:
        """D27 Bhamsa - 力量/弱点分盘"""
        # 每个星座分为27个1.111度区间
        part = int(sign_degree // (30/27))
        if sign_index in self.ODD_SIGNS:
            start = sign_index
        else:
            start = (sign_index + 8) % 12
        varga_sign = (start + part) % 12
        varga_degree = (sign_degree % (30/27)) * 27
        return varga_sign * 30 + varga_degree
    
    def _calculate_d30(self, sign_index: int, sign_degree: float) -> float:
        """D30 Trimsamsa - 不幸/困难分盘（特殊算法）"""
        # D30使用特殊的不等分算法
        # 奇数星座：Mars(5°), Saturn(5°), Jupiter(8°), Mercury(7°), Venus(5°)
        # 偶数星座：Venus(5°), Mercury(7°), Jupiter(8°), Saturn(5°), Mars(5°)
        
        if sign_index in self.ODD_SIGNS:
            if sign_degree < 5:
                varga_sign = 0  # Aries (Mars)
                varga_degree = sign_degree * 6
            elif sign_degree < 10:
                varga_sign = 10  # Aquarius (Saturn)
                varga_degree = (sign_degree - 5) * 6
            elif sign_degree < 18:
                varga_sign = 8  # Sagittarius (Jupiter)
                varga_degree = (sign_degree - 10) * 3.75
            elif sign_degree < 25:
                varga_sign = 2  # Gemini (Mercury)
                varga_degree = (sign_degree - 18) * 4.286
            else:
                varga_sign = 1  # Taurus (Venus)
                varga_degree = (sign_degree - 25) * 6
        else:
            if sign_degree < 5:
                varga_sign = 1  # Taurus (Venus)
                varga_degree = sign_degree * 6
            elif sign_degree < 12:
                varga_sign = 2  # Gemini (Mercury)
                varga_degree = (sign_degree - 5) * 4.286
            elif sign_degree < 20:
                varga_sign = 8  # Sagittarius (Jupiter)
                varga_degree = (sign_degree - 12) * 3.75
            elif sign_degree < 25:
                varga_sign = 10  # Aquarius (Saturn)
                varga_degree = (sign_degree - 20) * 6
            else:
                varga_sign = 0  # Aries (Mars)
                varga_degree = (sign_degree - 25) * 6
        
        return varga_sign * 30 + varga_degree
    
    def _calculate_d40(self, sign_index: int, sign_degree: float) -> float:
        """D40 Khavedamsa - 吉凶效果分盘"""
        # 每个星座分为40个0.75度区间
        part = int(sign_degree // 0.75)
        if sign_index in self.MOVABLE_SIGNS:
            start = sign_index
        elif sign_index in self.FIXED_SIGNS:
            start = (sign_index + 8) % 12
        else:
            start = (sign_index + 4) % 12
        varga_sign = (start + part) % 12
        varga_degree = (sign_degree % 0.75) * 40
        return varga_sign * 30 + varga_degree
    
    def _calculate_d45(self, sign_index: int, sign_degree: float) -> float:
        """D45 Akshavedamsa - 全面判断分盘"""
        # 每个星座分为45个0.667度区间
        part = int(sign_degree // (30/45))
        if sign_index in self.ODD_SIGNS:
            start = sign_index
        else:
            start = (sign_index + 8) % 12
        varga_sign = (start + part) % 12
        varga_degree = (sign_degree % (30/45)) * 45
        return varga_sign * 30 + varga_degree
    
    def _calculate_d60(self, sign_index: int, sign_degree: float) -> float:
        """D60 Shashtiamsa - 前世业力分盘（最精细的分盘）"""
        # 每个星座分为60个0.5度区间
        part = int(sign_degree // 0.5)
        varga_sign = (sign_index + part) % 12
        varga_degree = (sign_degree % 0.5) * 60
        return varga_sign * 30 + varga_degree
    
    def _calculate_d5(self, sign_index: int, sign_degree: float) -> float:
        """D5 Panchamsa - 名声/权力分盘"""
        part = int(sign_degree // 6)
        if sign_index in self.ODD_SIGNS:
            varga_sign = (sign_index + part) % 12
        else:
            varga_sign = (sign_index + 8 + part) % 12
        varga_degree = (sign_degree % 6) * 5
        return varga_sign * 30 + varga_degree
    
    def _calculate_d6(self, sign_index: int, sign_degree: float) -> float:
        """D6 Shashthamsa - 健康/敌人分盘"""
        part = int(sign_degree // 5)
        if sign_index in self.ODD_SIGNS:
            varga_sign = (sign_index + part) % 12
        else:
            varga_sign = (sign_index + 6 + part) % 12
        varga_degree = (sign_degree % 5) * 6
        return varga_sign * 30 + varga_degree
    
    def _calculate_d8(self, sign_index: int, sign_degree: float) -> float:
        """D8 Ashtamsa - 突发事件分盘"""
        part = int(sign_degree // 3.75)
        if sign_index in self.ODD_SIGNS:
            varga_sign = (sign_index + part) % 12
        else:
            varga_sign = (sign_index + 8 + part) % 12
        varga_degree = (sign_degree % 3.75) * 8
        return varga_sign * 30 + varga_degree
    
    def _calculate_d11(self, sign_index: int, sign_degree: float) -> float:
        """D11 Rudramsa - 破坏/转化分盘"""
        part = int(sign_degree // (30/11))
        if sign_index in self.ODD_SIGNS:
            varga_sign = (sign_index + part) % 12
        else:
            varga_sign = (sign_index + 8 + part) % 12
        varga_degree = (sign_degree % (30/11)) * 11
        return varga_sign * 30 + varga_degree
    
    def _calculate_generic_varga(self, sign_index: int, sign_degree: float, division: int) -> float:
        """通用分盘算法（适用于其他分盘）"""
        part = int(sign_degree // (30/division))
        varga_sign = (sign_index + part) % 12
        varga_degree = (sign_degree % (30/division)) * division
        return varga_sign * 30 + varga_degree
    
    def generate_house_chart_ascii(self, house_chart: List[List[str]]) -> str:
        """
        生成ASCII格式的宫位图
        
        Args:
            house_chart: 12个宫位的行星列表
        
        Returns:
            ASCII格式的宫位图字符串
        """
        # 北印度风格宫位图（菱形）
        chart = f"""
        ┌─────────┬─────────┬─────────┐
        │  12     │   1     │   2     │
        │ {self._format_planets(house_chart[11]):7} │ {self._format_planets(house_chart[0]):7} │ {self._format_planets(house_chart[1]):7} │
        ├─────────┼─────────┼─────────┤
        │  11     │         │   3     │
        │ {self._format_planets(house_chart[10]):7} │   ASC   │ {self._format_planets(house_chart[2]):7} │
        ├─────────┼─────────┼─────────┤
        │  10     │   9     │   4     │
        │ {self._format_planets(house_chart[9]):7} │ {self._format_planets(house_chart[8]):7} │ {self._format_planets(house_chart[3]):7} │
        ├─────────┼─────────┼─────────┤
        │   9     │   8     │   5     │
        │ {self._format_planets(house_chart[8]):7} │ {self._format_planets(house_chart[7]):7} │ {self._format_planets(house_chart[4]):7} │
        ├─────────┼─────────┼─────────┤
        │   8     │   7     │   6     │
        │ {self._format_planets(house_chart[7]):7} │ {self._format_planets(house_chart[6]):7} │ {self._format_planets(house_chart[5]):7} │
        └─────────┴─────────┴─────────┘
        """
        return chart
    
    def _format_planets(self, planets: List[str]) -> str:
        """格式化行星列表为简写"""
        if not planets:
            return "       "
        
        # 行星简写
        abbrev = {
            "Sun": "Su", "Moon": "Mo", "Mars": "Ma", "Mercury": "Me",
            "Jupiter": "Ju", "Venus": "Ve", "Saturn": "Sa",
            "Rahu": "Ra", "Ketu": "Ke"
        }
        
        short = [abbrev.get(p, p[:2]) for p in planets]
        return " ".join(short)[:7].ljust(7)


# 示例用法
if __name__ == "__main__":
    calculator = DivisionalChartsCalculator()
    
    # 示例数据：行星位置（黄道度数）
    planet_positions = {
        "Sun": 15.5,        # Aries 15.5°
        "Moon": 125.3,      # Leo 5.3°
        "Mars": 285.7,      # Capricorn 15.7°
        "Mercury": 25.2,    # Aries 25.2°
        "Jupiter": 95.8,    # Cancer 5.8°
        "Venus": 335.4,     # Pisces 5.4°
        "Saturn": 245.6,    # Sagittarius 5.6°
        "Rahu": 185.9,      # Libra 5.9°
        "Ketu": 5.9         # Aries 5.9°
    }
    
    asc_degree = 10.0  # Aries 10°
    
    # 计算所有分盘
    all_vargas = calculator.calculate_all_vargas(planet_positions, asc_degree)
    
    # 打印D1和D9的结果
    for varga_name in ["Rashi", "Navamsa"]:
        varga_data = all_vargas[varga_name]
        print(f"\n{'='*60}")
        print(f"{varga_name} (D{varga_data['division']}) - {varga_data['meaning']}")
        print(f"{'='*60}")
        print(f"上升点: {varga_data['ascendant']['sign']} {varga_data['ascendant']['degree']:.2f}°")
        print(f"\n行星位置:")
        for planet, data in varga_data['planets'].items():
            print(f"  {planet:10} → {data['sign']:12} {data['degree']:6.2f}° (第{data['house']}宫)")
        
        print(f"\n宫位图:")
        print(calculator.generate_house_chart_ascii(varga_data['house_chart']))
