#!/usr/bin/env python3
"""
星座引擎：识别星座原型并加载性格基因
"""

import json
from pathlib import Path
from typing import Dict, Optional


class ZodiacEngine:
    """星座原型引擎"""

    # 星座日期范围
    ZODIAC_DATES = {
        'aries': {'start': (3, 21), 'end': (4, 19)},
        'taurus': {'start': (4, 20), 'end': (5, 20)},
        'gemini': {'start': (5, 21), 'end': (6, 20)},
        'cancer': {'start': (6, 21), 'end': (7, 22)},
        'leo': {'start': (7, 23), 'end': (8, 22)},
        'virgo': {'start': (8, 23), 'end': (9, 22)},
        'libra': {'start': (9, 23), 'end': (10, 22)},
        'scorpio': {'start': (10, 23), 'end': (11, 21)},
        'sagittarius': {'start': (11, 22), 'end': (12, 21)},
        'capricorn': {'start': (12, 22), 'end': (1, 19)},
        'aquarius': {'start': (1, 20), 'end': (2, 18)},
        'pisces': {'start': (2, 19), 'end': (3, 20)}
    }

    # 星座基本信息
    ZODIAC_INFO = {
        'aries': {
            'element': 'fire',
            'mode': 'cardinal',
            'ruling_planet': 'mars',
            'symbol': '♈'
        },
        'taurus': {
            'element': 'earth',
            'mode': 'fixed',
            'ruling_planet': 'venus',
            'symbol': '♉'
        },
        'gemini': {
            'element': 'air',
            'mode': 'mutable',
            'ruling_planet': 'mercury',
            'symbol': '♊'
        },
        'cancer': {
            'element': 'water',
            'mode': 'cardinal',
            'ruling_planet': 'moon',
            'symbol': '♋'
        },
        'leo': {
            'element': 'fire',
            'mode': 'fixed',
            'ruling_planet': 'sun',
            'symbol': '♌'
        },
        'virgo': {
            'element': 'earth',
            'mode': 'mutable',
            'ruling_planet': 'mercury',
            'symbol': '♍'
        },
        'libra': {
            'element': 'air',
            'mode': 'cardinal',
            'ruling_planet': 'venus',
            'symbol': '♎'
        },
        'scorpio': {
            'element': 'water',
            'mode': 'fixed',
            'ruling_planet': 'pluto',
            'symbol': '♏'
        },
        'sagittarius': {
            'element': 'fire',
            'mode': 'mutable',
            'ruling_planet': 'jupiter',
            'symbol': '♐'
        },
        'capricorn': {
            'element': 'earth',
            'mode': 'cardinal',
            'ruling_planet': 'saturn',
            'symbol': '♑'
        },
        'aquarius': {
            'element': 'air',
            'mode': 'fixed',
            'ruling_planet': 'uranus',
            'symbol': '♒'
        },
        'pisces': {
            'element': 'water',
            'mode': 'mutable',
            'ruling_planet': 'neptune',
            'symbol': '♓'
        }
    }

    def __init__(self, prototypes_dir: Path):
        self.prototypes_dir = prototypes_dir

    def identify_zodiac(self, birthday: str) -> str:
        """根据生日识别星座"""
        try:
            year, month, day = map(int, birthday.split('-'))
        except:
            raise ValueError(f"Invalid birthday format: {birthday}. Expected YYYY-MM-DD")

        # 处理摩羯座跨年
        if month == 12 and day >= 22:
            return 'capricorn'
        elif month == 1 and day <= 19:
            return 'capricorn'

        # 其他星座
        for sign, dates in self.ZODIAC_DATES.items():
            start_month, start_day = dates['start']
            end_month, end_day = dates['end']

            if start_month == end_month:
                if month == start_month and start_day <= day <= end_day:
                    return sign
            else:
                if month == start_month and day >= start_day:
                    return sign
                elif month == end_month and day <= end_day:
                    return sign

        return 'unknown'

    def load_zodiac_prototype(self, zodiac_sign: str) -> Dict:
        """加载星座原型数据"""
        if zodiac_sign not in self.ZODIAC_INFO:
            raise ValueError(f"Unknown zodiac sign: {zodiac_sign}")

        # 基本信息
        info = self.ZODIAC_INFO[zodiac_sign]

        # 尝试加载详细原型数据
        prototype_file = self.prototypes_dir / f"{zodiac_sign}.md"
        if prototype_file.exists():
            # 这里简化处理，实际应该解析MD文件
            content = prototype_file.read_text(encoding='utf-8')
            # 简化的提取逻辑
            prototype = {
                'sign': zodiac_sign,
                'info': info,
                'has_detailed_data': True,
                'file_path': str(prototype_file)
            }
        else:
            # 使用默认模板
            prototype = {
                'sign': zodiac_sign,
                'info': info,
                'has_detailed_data': False,
                'core_drive': f"{zodiac_sign}的核心动机",
                'cognitive_filter': f"{zodiac_sign}的认知过滤器",
                'emotional_pattern': f"{zodiac_sign}的情感模式",
                'expression_style': f"{zodiac_sign}的表达风格"
            }

        return prototype

    def get_zodiac_compatibility(self, sign1: str, sign2: str) -> Dict:
        """获取两个星座的兼容性"""
        info1 = self.ZODIAC_INFO.get(sign1, {})
        info2 = self.ZODIAC_INFO.get(sign2, {})

        # 元素兼容性
        element_compatibility = self._get_element_compatibility(
            info1.get('element'),
            info2.get('element')
        )

        # 模式兼容性
        mode_compatibility = self._get_mode_compatibility(
            info1.get('mode'),
            info2.get('mode')
        )

        return {
            'sign1': sign1,
            'sign2': sign2,
            'element_compatibility': element_compatibility,
            'mode_compatibility': mode_compatibility,
            'overall_compatibility': self._calculate_overall_compatibility(
                element_compatibility,
                mode_compatibility
            )
        }

    def _get_element_compatibility(self, elem1: str, elem2: str) -> Dict:
        """元素兼容性分析"""
        compatible_elements = {
            'fire': ['fire', 'air'],
            'earth': ['earth', 'water'],
            'air': ['air', 'fire'],
            'water': ['water', 'earth']
        }

        if elem1 == elem2:
            return {'score': 0.9, 'type': 'same_element'}
        elif elem2 in compatible_elements.get(elem1, []):
            return {'score': 0.8, 'type': 'compatible'}
        else:
            return {'score': 0.3, 'type': 'challenging'}

    def _get_mode_compatibility(self, mode1: str, mode2: str) -> Dict:
        """模式兼容性分析"""
        if mode1 == mode2:
            return {'score': 0.7, 'type': 'same_mode'}
        else:
            return {'score': 0.8, 'type': 'different_mode'}

    def _calculate_overall_compatibility(self, element_compat: Dict, mode_compat: Dict) -> float:
        """计算总体兼容性"""
        element_score = element_compat['score']
        mode_score = mode_compat['score']
        return (element_score + mode_score) / 2


def main():
    import argparse

    parser = argparse.ArgumentParser(description='星座引擎')
    parser.add_argument('--birthday', help='生日 (YYYY-MM-DD)')
    parser.add_argument('--compatibility', nargs=2, metavar=('SIGN1', 'SIGN2'),
                       help='检查两个星座的兼容性')

    args = parser.parse_args()

    engine = ZodiacEngine(Path('./references/zodiac-prototypes'))

    if args.birthday:
        sign = engine.identify_zodiac(args.birthday)
        prototype = engine.load_zodiac_prototype(sign)
        print(f"星座: {sign}")
        print(f"信息: {json.dumps(prototype['info'], ensure_ascii=False, indent=2)}")

    if args.compatibility:
        sign1, sign2 = args.compatibility
        compatibility = engine.get_zodiac_compatibility(sign1, sign2)
        print(f"兼容性: {json.dumps(compatibility, ensure_ascii=False, indent=2)}")


if __name__ == '__main__':
    main()
