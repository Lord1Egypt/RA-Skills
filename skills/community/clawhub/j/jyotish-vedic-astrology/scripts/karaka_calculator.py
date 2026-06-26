#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Karaka Calculator - Jaimini Chara Karaka System
印度占星 Karaka（象征星）计算器

支持两种模式：
1. BPHS标准模式（8-Karaka）：Sun > Moon > Mars > Mercury > Jupiter > Venus > Saturn > Rahu
2. Jagannatha Hora兼容模式（7-Karaka + Rahu限制）：Rahu只能是Matrukaraka(MK)

核心功能：
- 计算7大Chara Karaka（可变象征星）
- 支持8-Karaka系统（包含Rahu）
- 自动识别Karaka模式
- 提供详细的度数排序和Karaka分配
"""

import sys
from typing import Dict, List, Tuple, Optional
from enum import Enum

class KarakaMode(Enum):
    """Karaka计算模式"""
    BPHS_8_KARAKA = "bphs"  # 标准BPHS 8-Karaka系统
    JH_COMPATIBLE = "jh"     # Jagannatha Hora兼容模式（Rahu限制在MK）
    BPHS_7_KARAKA = "bphs7" # 标准BPHS 7-Karaka系统（不含Rahu）

class KarakaType(Enum):
    """7大Chara Karaka类型"""
    ATMAKARAKA = "AK"      # 灵魂象征星（最高度数）
    AMATYAKARAKA = "AmK"   # 事业象征星（第二高）
    BHRATRUKARAKA = "BK"   # 兄弟象征星（第三高）
    MATRUKARAKA = "MK"     # 母亲象征星（第四高）
    PUTRAKARAKA = "PK"     # 子女象征星（第五高）
    GNATIKARAKA = "GK"     # 敌人/疾病象征星（第六高）
    DARAKARAKA = "DK"      # 配偶象征星（最低度数）
    EXTRA_KARAKA = "XK"    # 额外象征星（仅在8-Karaka系统中）

class KarakaCalculator:
    """Karaka计算器"""
    
    SEVEN_PLANETS = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]
    EIGHT_PLANETS = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu"]
    
    def __init__(self, mode: KarakaMode = KarakaMode.BPHS_8_KARAKA):
        self.mode = mode
        
    def calculate_karaka(self, planet_positions: Dict[str, float]) -> Dict[str, any]:
        """
        计算Chara Karaka
        
        Args:
            planet_positions: 行星位置字典 {行星名: 黄道度数}
        
        Returns:
            Karaka分配结果字典
        """
        result = {
            "mode": self.mode.value,
            "karakas": {},
            "sorted_planets": [],
            "warnings": []
        }
        
        # 1. 提取有效行星
        valid_planets = self._extract_valid_planets(planet_positions, result)
        if not valid_planets:
            result["warnings"].append("No valid planets found")
            return result
        
        # 2. 转换为星座内度数（0-30度）
        sign_degrees = {p: d % 30.0 for p, d in valid_planets.items()}
        
        # 3. 按度数排序（降序）
        sorted_planets = sorted(sign_degrees.items(), key=lambda x: x[1], reverse=True)
        result["sorted_planets"] = [(p, round(d, 4)) for p, d in sorted_planets]
        
        # 4. 分配Karaka
        result["karakas"] = self._assign_karakas(sorted_planets, result)
        
        # 5. 验证
        self._validate_karakas(result)
        
        return result
    
    def _extract_valid_planets(self, positions: Dict[str, float], result: Dict) -> Dict[str, float]:
        """提取有效行星"""
        valid = {}
        planets = self.SEVEN_PLANETS if self.mode == KarakaMode.BPHS_7_KARAKA else self.EIGHT_PLANETS
        
        for planet in planets:
            if planet in positions:
                valid[planet] = positions[planet]
            else:
                result["warnings"].append(f"Missing planet: {planet}")
        
        return valid
    
    def _assign_karakas(self, sorted_planets: List[Tuple[str, float]], result: Dict) -> Dict:
        """分配Karaka"""
        karakas = {}
        
        if self.mode == KarakaMode.JH_COMPATIBLE:
            # JH模式：强制Rahu为MK
            rahu_idx = next((i for i, (p, _) in enumerate(sorted_planets) if p == "Rahu"), None)
            if rahu_idx is not None and rahu_idx != 3:
                result["warnings"].append(f"JH Mode: Rahu forced to MK (was rank {rahu_idx + 1})")
                adjusted = [p for p in sorted_planets if p[0] != "Rahu"]
                adjusted.insert(3, sorted_planets[rahu_idx])
                sorted_planets = adjusted
        
        # 分配Karaka
        karaka_types = [
            ("AK", "灵魂象征星"),
            ("AmK", "事业象征星"),
            ("BK", "兄弟象征星"),
            ("MK", "母亲象征星"),
            ("PK", "子女象征星"),
            ("GK", "敌人/疾病象征星"),
        ]
        
        if self.mode == KarakaMode.BPHS_8_KARAKA:
            karaka_types.append(("XK", "额外象征星"))
        
        karaka_types.append(("DK", "配偶象征星"))
        
        for i, (planet, degree) in enumerate(sorted_planets[:len(karaka_types)]):
            code, name = karaka_types[i]
            karakas[code] = {
                "planet": planet,
                "sign_degree": round(degree, 4),
                "name": name,
                "rank": i + 1
            }
        
        return karakas
    
    def _validate_karakas(self, result: Dict):
        """验证Karaka分配"""
        expected = 7 if self.mode != KarakaMode.BPHS_8_KARAKA else 8
        if len(result["karakas"]) != expected:
            result["warnings"].append(f"Expected {expected} Karakas, got {len(result['karakas'])}")
    
    def format_output(self, result: Dict) -> str:
        """格式化输出"""
        lines = ["=" * 60, "Chara Karaka Calculation", "=" * 60]
        lines.append(f"Mode: {result['mode'].upper()}\n")
        
        lines.append("Karaka Assignment:")
        for code, data in result['karakas'].items():
            lines.append(f"  {code:4s} = {data['planet']:10s} ({data['sign_degree']:6.2f}°) - {data['name']}")
        
        if result['warnings']:
            lines.append("\nWarnings:")
            for w in result['warnings']:
                lines.append(f"  ⚠️  {w}")
        
        lines.append("=" * 60)
        return "\n".join(lines)


def main():
    """命令行接口"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Calculate Jaimini Chara Karaka")
    parser.add_argument("--mode", choices=["bphs", "jh", "bphs7"], default="bphs")
    parser.add_argument("--planets", type=str, help="Format: Sun:45.5,Moon:120.3,...")
    parser.add_argument("--json", action="store_true")
    
    args = parser.parse_args()
    
    # 解析行星位置
    if args.planets:
        positions = {}
        for pair in args.planets.split(","):
            planet, degree = pair.split(":")
            positions[planet.strip()] = float(degree.strip())
    else:
        # 示例数据
        positions = {
            "Sun": 45.5, "Moon": 120.3, "Mars": 200.1,
            "Mercury": 50.8, "Jupiter": 180.5, "Venus": 90.2,
            "Saturn": 250.7, "Rahu": 150.4
        }
        print("Using example data\n")
    
    # 计算
    mode_map = {"bphs": KarakaMode.BPHS_8_KARAKA, "jh": KarakaMode.JH_COMPATIBLE, "bphs7": KarakaMode.BPHS_7_KARAKA}
    calc = KarakaCalculator(mode=mode_map[args.mode])
    result = calc.calculate_karaka(positions)
    
    # 输出
    if args.json:
        import json
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(calc.format_output(result))


if __name__ == "__main__":
    main()
