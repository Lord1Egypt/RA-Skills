#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Special Lagnas Calculator - 特殊上升点计算器
印度占星特殊上升点（Bhava/Hora/Ghati/Arudha/Upapada Lagna）

核心功能：
- Bhava Lagna（宫位上升）：反映物质层面的实际状况
- Hora Lagna（时辰上升）：财富和物质收益的指示器
- Ghati Lagna（Ghati上升）：基于Ghati单位的精确上升点
- Arudha Lagna（映像上升）：公众形象和社会地位
- Upapada Lagna（配偶映像上升）：配偶和婚姻的公众形象
"""

from typing import Dict, Tuple
from datetime import datetime, timedelta

class SpecialLagnasCalculator:
    """特殊上升点计算器"""
    
    SIGNS = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
             "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]
    
    def __init__(self):
        pass
    
    def calculate_all_lagnas(self, asc_degree: float, sun_degree: float, 
                            moon_degree: float, birth_time: datetime,
                            sunrise_time: datetime) -> Dict[str, Dict]:
        """
        计算所有特殊上升点
        
        Args:
            asc_degree: 上升点度数（0-360）
            sun_degree: 太阳度数（0-360）
            moon_degree: 月亮度数（0-360）
            birth_time: 出生时间
            sunrise_time: 当天日出时间
        
        Returns:
            所有特殊上升点的字典
        """
        result = {}
        
        # 1. Bhava Lagna
        result["Bhava_Lagna"] = self.calculate_bhava_lagna(asc_degree, sun_degree, moon_degree)
        
        # 2. Hora Lagna
        result["Hora_Lagna"] = self.calculate_hora_lagna(asc_degree, sun_degree, birth_time, sunrise_time)
        
        # 3. Ghati Lagna
        result["Ghati_Lagna"] = self.calculate_ghati_lagna(asc_degree, birth_time, sunrise_time)
        
        # 4. Arudha Lagna (需要1宫主星位置)
        # 注意：这里需要额外的行星位置信息，暂时返回占位符
        result["Arudha_Lagna"] = {"note": "Requires 1st house lord position"}
        
        # 5. Upapada Lagna (需要12宫主星位置)
        result["Upapada_Lagna"] = {"note": "Requires 12th house lord position"}
        
        return result
    
    def calculate_bhava_lagna(self, asc_degree: float, sun_degree: float, 
                              moon_degree: float) -> Dict:
        """
        计算Bhava Lagna（宫位上升）
        
        公式：Bhava Lagna = Asc + (Sun - Moon)
        
        含义：
        - 反映物质层面的实际状况
        - 显示真实的生活环境和物质条件
        - 与上升点的差异揭示表象与实质的差距
        """
        # 计算太阳-月亮的度数差
        sun_moon_diff = sun_degree - moon_degree
        
        # 如果差值为负，加360度
        if sun_moon_diff < 0:
            sun_moon_diff += 360
        
        # 计算Bhava Lagna
        bhava_lagna = (asc_degree + sun_moon_diff) % 360
        
        # 转换为星座和度数
        sign_index = int(bhava_lagna // 30)
        sign_degree = bhava_lagna % 30
        
        return {
            "degree": round(bhava_lagna, 4),
            "sign": self.SIGNS[sign_index],
            "sign_degree": round(sign_degree, 4),
            "formula": "Asc + (Sun - Moon)",
            "meaning": "物质层面的实际状况，真实的生活环境"
        }
    
    def calculate_hora_lagna(self, asc_degree: float, sun_degree: float,
                            birth_time: datetime, sunrise_time: datetime) -> Dict:
        """
        计算Hora Lagna（时辰上升）
        
        公式：Hora Lagna = Asc + (出生时间距日出的Hora数 × 15度)
        
        含义：
        - 财富和物质收益的指示器
        - 显示金钱来源和财富积累方式
        - 与2宫（财富宫）密切相关
        """
        # 计算出生时间距日出的小时数
        time_diff = birth_time - sunrise_time
        hours_from_sunrise = time_diff.total_seconds() / 3600
        
        # 计算Hora数（每个Hora = 1小时）
        hora_count = hours_from_sunrise
        
        # 计算Hora Lagna（每个Hora推进15度）
        hora_lagna = (asc_degree + (hora_count * 15)) % 360
        
        # 转换为星座和度数
        sign_index = int(hora_lagna // 30)
        sign_degree = hora_lagna % 30
        
        return {
            "degree": round(hora_lagna, 4),
            "sign": self.SIGNS[sign_index],
            "sign_degree": round(sign_degree, 4),
            "hours_from_sunrise": round(hours_from_sunrise, 2),
            "formula": "Asc + (Hora数 × 15°)",
            "meaning": "财富和物质收益的指示器"
        }
    
    def calculate_ghati_lagna(self, asc_degree: float, birth_time: datetime,
                             sunrise_time: datetime) -> Dict:
        """
        计算Ghati Lagna（Ghati上升）
        
        公式：Ghati Lagna = Asc + (Ghati数 × 6度)
        
        Ghati单位：
        - 1 Ghati = 24分钟
        - 1天 = 60 Ghati
        - 每个Ghati推进6度（360度 / 60 Ghati = 6度）
        
        含义：
        - 基于Ghati单位的精确上升点
        - 用于精确的时间矫正和事件预测
        - 在Prashna（问事占星）中特别重要
        """
        # 计算出生时间距日出的分钟数
        time_diff = birth_time - sunrise_time
        minutes_from_sunrise = time_diff.total_seconds() / 60
        
        # 计算Ghati数（1 Ghati = 24分钟）
        ghati_count = minutes_from_sunrise / 24
        
        # 计算Ghati Lagna（每个Ghati推进6度）
        ghati_lagna = (asc_degree + (ghati_count * 6)) % 360
        
        # 转换为星座和度数
        sign_index = int(ghati_lagna // 30)
        sign_degree = ghati_lagna % 30
        
        return {
            "degree": round(ghati_lagna, 4),
            "sign": self.SIGNS[sign_index],
            "sign_degree": round(sign_degree, 4),
            "ghati_count": round(ghati_count, 2),
            "formula": "Asc + (Ghati数 × 6°)",
            "meaning": "基于Ghati单位的精确上升点，用于精确预测"
        }
    
    def calculate_arudha_lagna(self, asc_degree: float, first_lord_degree: float) -> Dict:
        """
        计算Arudha Lagna（映像上升/AL）
        
        公式：
        1. 计算1宫主星距离上升点的宫位数（A）
        2. 从1宫主星再数A个宫位，得到AL
        3. 特殊规则：如果AL落在1宫或7宫，则从该位置再数10个宫位
        
        含义：
        - 公众形象和社会地位
        - 他人如何看待你
        - 外在表现与内在本质的差异
        """
        # 计算上升点和1宫主星的星座
        asc_sign = int(asc_degree // 30)
        lord_sign = int(first_lord_degree // 30)
        
        # 计算1宫主星距离上升点的宫位数
        distance = (lord_sign - asc_sign) % 12
        if distance == 0:
            distance = 12
        
        # 从1宫主星再数相同的宫位数
        al_sign = (lord_sign + distance - 1) % 12
        
        # 应用1/7宫例外规则
        if al_sign == asc_sign or al_sign == (asc_sign + 6) % 12:
            al_sign = (al_sign + 9) % 12  # 再数10个宫位（索引+9）
        
        # 计算AL的度数（使用1宫主星的度数）
        al_degree = (al_sign * 30 + (first_lord_degree % 30)) % 360
        
        return {
            "degree": round(al_degree, 4),
            "sign": self.SIGNS[al_sign],
            "sign_degree": round(al_degree % 30, 4),
            "distance_from_asc": distance,
            "formula": "从1宫主星数相同宫位数（1/7宫例外）",
            "meaning": "公众形象和社会地位，他人如何看待你"
        }
    
    def calculate_upapada_lagna(self, asc_degree: float, twelfth_lord_degree: float) -> Dict:
        """
        计算Upapada Lagna（配偶映像上升/UL）
        
        公式：
        1. 计算12宫主星距离12宫的宫位数（A）
        2. 从12宫主星再数A个宫位，得到UL
        3. 特殊规则：如果UL落在12宫或6宫，则从该位置再数10个宫位
        
        含义：
        - 配偶的公众形象
        - 婚姻在社会中的表现
        - 配偶的社会地位和声誉
        """
        # 计算12宫的起始度数
        asc_sign = int(asc_degree // 30)
        twelfth_house_sign = (asc_sign + 11) % 12
        
        # 计算12宫主星的星座
        lord_sign = int(twelfth_lord_degree // 30)
        
        # 计算12宫主星距离12宫的宫位数
        distance = (lord_sign - twelfth_house_sign) % 12
        if distance == 0:
            distance = 12
        
        # 从12宫主星再数相同的宫位数
        ul_sign = (lord_sign + distance - 1) % 12
        
        # 应用12/6宫例外规则
        if ul_sign == twelfth_house_sign or ul_sign == (twelfth_house_sign + 6) % 12:
            ul_sign = (ul_sign + 9) % 12  # 再数10个宫位
        
        # 计算UL的度数
        ul_degree = (ul_sign * 30 + (twelfth_lord_degree % 30)) % 360
        
        return {
            "degree": round(ul_degree, 4),
            "sign": self.SIGNS[ul_sign],
            "sign_degree": round(ul_degree % 30, 4),
            "distance_from_12th": distance,
            "formula": "从12宫主星数相同宫位数（12/6宫例外）",
            "meaning": "配偶的公众形象和婚姻的社会表现"
        }
    
    def format_output(self, lagnas: Dict) -> str:
        """格式化输出所有特殊上升点"""
        lines = ["=" * 60, "Special Lagnas Calculation", "=" * 60, ""]
        
        for lagna_name, data in lagnas.items():
            lines.append(f"{lagna_name}:")
            if "note" in data:
                lines.append(f"  {data['note']}")
            else:
                lines.append(f"  Position: {data['sign']} {data['sign_degree']:.2f}° ({data['degree']:.2f}°)")
                lines.append(f"  Formula: {data['formula']}")
                lines.append(f"  Meaning: {data['meaning']}")
            lines.append("")
        
        lines.append("=" * 60)
        return "\n".join(lines)


def main():
    """命令行接口"""
    import argparse
    from datetime import datetime
    
    parser = argparse.ArgumentParser(description="Calculate Special Lagnas")
    parser.add_argument("--asc", type=float, required=True, help="Ascendant degree (0-360)")
    parser.add_argument("--sun", type=float, required=True, help="Sun degree (0-360)")
    parser.add_argument("--moon", type=float, required=True, help="Moon degree (0-360)")
    parser.add_argument("--birth-time", type=str, help="Birth time (YYYY-MM-DD HH:MM:SS)")
    parser.add_argument("--sunrise-time", type=str, help="Sunrise time (YYYY-MM-DD HH:MM:SS)")
    parser.add_argument("--first-lord", type=float, help="1st house lord degree (for AL)")
    parser.add_argument("--twelfth-lord", type=float, help="12th house lord degree (for UL)")
    
    args = parser.parse_args()
    
    calc = SpecialLagnasCalculator()
    
    # 解析时间
    birth_time = datetime.strptime(args.birth_time, "%Y-%m-%d %H:%M:%S") if args.birth_time else datetime.now()
    sunrise_time = datetime.strptime(args.sunrise_time, "%Y-%m-%d %H:%M:%S") if args.sunrise_time else birth_time.replace(hour=6, minute=0, second=0)
    
    # 计算所有特殊上升点
    lagnas = calc.calculate_all_lagnas(args.asc, args.sun, args.moon, birth_time, sunrise_time)
    
    # 如果提供了1宫主星位置，计算AL
    if args.first_lord is not None:
        lagnas["Arudha_Lagna"] = calc.calculate_arudha_lagna(args.asc, args.first_lord)
    
    # 如果提供了12宫主星位置，计算UL
    if args.twelfth_lord is not None:
        lagnas["Upapada_Lagna"] = calc.calculate_upapada_lagna(args.asc, args.twelfth_lord)
    
    # 输出结果
    print(calc.format_output(lagnas))


if __name__ == "__main__":
    main()
