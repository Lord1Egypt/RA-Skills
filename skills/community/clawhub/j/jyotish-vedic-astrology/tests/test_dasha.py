#!/usr/bin/env python3
"""
Jyotish Engine 单元测试
覆盖: Dasha 计算、尊严等级判定、Yoga 格局识别

运行方式:
  cd yinduzhanxing
  python3 -m pytest tests/ -v
  # 或
  python3 -m unittest discover tests/
"""

import unittest
import sys
import os
from datetime import datetime

# 确保可以导入 scripts/ 下的模块
SCRIPT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'scripts')
sys.path.insert(0, SCRIPT_DIR)
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT_DIR)

from jyotish_engine import (
    cmd_dasha, _get_dignity_level, cmd_yoga,
    EXALTATION, DEBILITATION, SIGN_LORDS, MOOLATRIKONA,
    DASHA_ORDER, DASHA_YEARS, NAKSHATRA_LIST, SIGNS,
)


class TestDignityLevel(unittest.TestCase):
    """测试尊严等级判定 (_get_dignity_level)"""

    def test_exalted(self):
        """太阳在白羊座 = Exalted"""
        self.assertEqual(_get_dignity_level('Sun', 'Aries'), 'EXALTED')

    def test_debilitated(self):
        """太阳在天秤座 = Debilitated"""
        self.assertEqual(_get_dignity_level('Sun', 'Libra'), 'DEBILITATED')

    def test_own_sign(self):
        """太阳在狮子座 = Own Sign"""
        self.assertEqual(_get_dignity_level('Sun', 'Leo'), 'OWN_SIGN')

    def test_moolatrikona_in_range(self):
        """火星在白羊座 0-12° = Moolatrikona"""
        self.assertEqual(_get_dignity_level('Mars', 'Aries', 5.0), 'MOOLATRIKONA')

    def test_moolatrikona_out_of_range(self):
        """火星在白羊座 12°+ = Own Sign (不是 Moolatrikona)"""
        self.assertEqual(_get_dignity_level('Mars', 'Aries', 15.0), 'OWN_SIGN')

    def test_friend(self):
        """月亮在 Aries（火星的星座，月亮是火星的朋友）"""
        # Mars 的 PERMANENT_FRIENDS 包含 Moon，所以 Moon 在 Mars 的星座是 Friend
        # 但这里测的是 Moon 在 Aries: Aries lord = Mars, Moon in PERMANENT_FRIENDS['Mars'] = yes
        self.assertEqual(_get_dignity_level('Moon', 'Aries'), 'FRIEND')

    def test_enemy(self):
        """金星在 Aries（火星的星座，金星是火星的敌人 → 但实际看 Aries lord(Mars) 的朋友表里没有 Venus → 不是 Friend）
        Venus 在 PERMANENT_ENEMIES['Mars'] 吗？不在。看 Sun 的: Venus in PERMANENT_ENEMIES['Sun'].
        测试：Venus 在 Cancer（Moon 的星座），PERMANENT_FRIENDS['Moon'] = ['Sun', 'Mercury']，不包含 Venus
        PERMANENT_ENEMIES['Moon'] = []，所以 Venus 在 Cancer = NEUTRAL
        """
        # 测一个明确的 Enemy: Venus 在 Aries（Mars 守护，Venus 不在 Mars 的 friends 也不在 enemies）
        # Venus 在 Scorpio（Mars 守护）：同上
        # 更好的例子: Saturn 在 Leo（Sun 守护，Saturn 在 PERMANENT_ENEMIES['Sun']）
        self.assertEqual(_get_dignity_level('Saturn', 'Leo'), 'ENEMY')

    def test_neutral(self):
        """木星在 Gemini（Mercury 守护），Jupiter 不在 Mercury 的 friends 也不在 enemies"""
        # PERMANENT_FRIENDS['Mercury'] = ['Sun', 'Venus']
        # PERMANENT_ENEMIES['Mercury'] = ['Moon']
        self.assertEqual(_get_dignity_level('Jupiter', 'Gemini'), 'NEUTRAL')

    def test_all_exaltation_signs(self):
        """验证所有行星的入旺星座"""
        expected = {
            'Sun': 'Aries', 'Moon': 'Taurus', 'Mars': 'Capricorn',
            'Mercury': 'Virgo', 'Jupiter': 'Cancer', 'Venus': 'Pisces', 'Saturn': 'Libra'
        }
        for planet, sign in expected.items():
            result = _get_dignity_level(planet, sign)
            self.assertEqual(result, 'EXALTED', f"{planet} in {sign} should be EXALTED, got {result}")

    def test_all_debilitation_signs(self):
        """验证所有行星的落陷星座"""
        expected = {
            'Sun': 'Libra', 'Moon': 'Scorpio', 'Mars': 'Cancer',
            'Mercury': 'Pisces', 'Jupiter': 'Capricorn', 'Venus': 'Virgo', 'Saturn': 'Aries'
        }
        for planet, sign in expected.items():
            result = _get_dignity_level(planet, sign)
            self.assertEqual(result, 'DEBILITATED', f"{planet} in {sign} should be DEBILITATED, got {result}")


class TestDashaCalculation(unittest.TestCase):
    """测试 Dasha 时间线计算"""

    def _make_dasha_args(self, moon_lon, birthdate, today=None):
        """构造 cmd_dasha 参数"""
        today = today or '2026-05-04'
        return type('Args', (), {
            'moon_lon': moon_lon,
            'nakshatra': None,
            'pada': None,
            'birthdate': birthdate,
            'today': today,
        })()

    def test_first_md_shows_balance(self):
        """第一个 MD 的 years 字段显示 balance，full_years 显示完整年数"""
        # 月亮在 Ardra (Rahu 主宰, 18年), 月亮黄经 73° → Ardra 范围 66.67-80°
        args = self._make_dasha_args(73.0, '1990-01-15')
        result = cmd_dasha(args)
        timeline = result.get('timeline', [])
        self.assertTrue(len(timeline) > 0, "Timeline should not be empty")
        first_md = timeline[0]
        # Ardra 主宰 Rahu
        self.assertEqual(first_md['lord'], 'Rahu')
        # years (展示值) 应该 < 18（balance）
        self.assertLess(first_md['years'], 18, f"First MD display years should be < 18, got {first_md['years']}")
        # full_years 应该 = 18
        self.assertEqual(first_md['full_years'], 18)
        # 应该有 is_balance 和 balance_years
        self.assertTrue(first_md.get('is_balance', False))
        self.assertIsNotNone(first_md.get('balance_years'))

    def test_timeline_date_chain_continuous(self):
        """验证时间线日期链条连续：每个 MD 的 start = 上一个 MD 的 end"""
        args = self._make_dasha_args(100.0, '1990-01-15')
        result = cmd_dasha(args)
        timeline = result.get('timeline', [])
        self.assertTrue(len(timeline) >= 2, "Need at least 2 MDs")
        for i in range(1, len(timeline)):
            self.assertEqual(timeline[i]['start'], timeline[i-1]['end'],
                f"MD{i} start should equal MD{i-1} end: {timeline[i]['start']} != {timeline[i-1]['end']}")

    def test_first_md_ends_at_birth_plus_remaining(self):
        """验证第一个 MD 的 end 日期 = birth + remaining 年（核心正确性）
        原始代码的数学等价性：end = (birth - elapsed) + full_years = birth + remaining
        """
        args = self._make_dasha_args(45.0, '1990-06-15', '2026-01-01')
        result = cmd_dasha(args)
        timeline = result.get('timeline', [])
        first = timeline[0]
        birth = datetime.strptime('1990-06-15', '%Y-%m-%d')
        end = datetime.strptime(first['end'], '%Y-%m-%d')
        # end - birth 应该 ≈ balance_years
        actual_years = (end - birth).days / 365.25
        balance = first.get('balance_years', first['years'])
        self.assertAlmostEqual(actual_years, balance, delta=0.1,
            msg=f"First MD end should be birth+{balance}y, got {actual_years:.2f}y")

    def test_dasha_order_correct(self):
        """验证 Dasha 顺序遵循 Ketu→Venus→Sun→Moon→Mars→Rahu→Jupiter→Saturn→Mercury"""
        # 用月亮在 Ashwini (Ketu 主宰) 的位置
        args = self._make_dasha_args(5.0, '1990-01-15')  # Ashwini
        result = cmd_dasha(args)
        timeline = result.get('timeline', [])
        if len(timeline) >= 9:
            actual_order = [d['lord'] for d in timeline]
            self.assertEqual(actual_order, DASHA_ORDER,
                f"Dasha order should be {DASHA_ORDER}, got {actual_order}")

    def test_nakshatra_moon_lon_mapping(self):
        """验证月亮黄经正确映射到 Nakshatra"""
        # Revati: 346.67° - 360°
        args = self._make_dasha_args(350.0, '1990-01-15')
        result = cmd_dasha(args)
        self.assertEqual(result.get('moon_nakshatra'), 'Revati')

    def test_antardasha_in_current_dasha(self):
        """验证当前 Dasha 包含 Antardasha 信息"""
        args = self._make_dasha_args(100.0, '1990-01-15', '2026-05-04')
        result = cmd_dasha(args)
        current = result.get('current_dasha')
        if current:
            self.assertIn('antardasha', current, "Current dasha should have antardasha")
            ad = current['antardasha']
            self.assertTrue(len(ad) > 0, "Antardasha should not be empty")

    def test_barack_oboma_dasha(self):
        """已知案例: Obama 月亮在 Rohini (约 35°59' → 实际 Krittika, 用 45° 测 Rohini)"""
        # Krittika: 26.67° - 40°, Rohini: 40° - 53.33°
        # 35.98° 在 Krittika 范围，用 45° 测 Rohini
        args = self._make_dasha_args(45.0, '1961-08-04', '2024-01-01')
        result = cmd_dasha(args)
        self.assertEqual(result['moon_nakshatra'], 'Rohini')
        # Rohini 主宰 Moon，所以第一个 MD 应该是 Moon
        timeline = result.get('timeline', [])
        if timeline:
            self.assertEqual(timeline[0]['lord'], 'Moon')


class TestNakshatraMapping(unittest.TestCase):
    """测试 Nakshatra 映射"""

    def test_ashwini_start(self):
        """0° → Ashwini"""
        args = type('Args', (), {
            'moon_lon': 0.5, 'nakshatra': None, 'pada': None,
            'birthdate': '1990-01-01', 'today': '2026-01-01',
        })()
        result = cmd_dasha(args)
        self.assertEqual(result['moon_nakshatra'], 'Ashwini')

    def test_revati_end(self):
        """~359° → Revati"""
        args = type('Args', (), {
            'moon_lon': 359.0, 'nakshatra': None, 'pada': None,
            'birthdate': '1990-01-01', 'today': '2026-01-01',
        })()
        result = cmd_dasha(args)
        self.assertEqual(result['moon_nakshatra'], 'Revati')

    def test_jyeshtha(self):
        """~230° → Jyeshtha (226.67° - 240°)"""
        args = type('Args', (), {
            'moon_lon': 230.0, 'nakshatra': None, 'pada': None,
            'birthdate': '1990-01-01', 'today': '2026-01-01',
        })()
        result = cmd_dasha(args)
        self.assertEqual(result['moon_nakshatra'], 'Jyeshtha')


class TestYogaDetection(unittest.TestCase):
    """测试 Yoga 格局识别"""

    def _make_yoga_args(self, ascendant, planets_str):
        return type('Args', (), {
            'ascendant': ascendant,
            'planets': planets_str,
        })()

    def test_raja_yoga_detection(self):
        """测试 Raja Yoga 检测：角宫主+三方主同宫"""
        # Leo Ascendant: Kendra lords = Sun(1st), Mars(4th/Scorpio), Jupiter(7th/Pisces)
        # Trikona lords = Sun(1st), Jupiter(5th/Sagittarius)
        # 如果 Jupiter 和 Sun 都在某宫 → Raja Yoga
        args = self._make_yoga_args('Leo', 'Sun:Leo:1,Jupiter:Leo:1,Moon:Taurus:10,Mars:Scorpio:4')
        result = cmd_yoga(args)
        yogas = result.get('yogas', [])
        raja = [y for y in yogas if y['name'] == 'Raja Yoga']
        self.assertTrue(len(raja) > 0, "Should detect Raja Yoga when Sun+Jupiter in 1st house")

    def test_no_yoga_false_positive(self):
        """测试不满足条件时不产生 Yoga"""
        # 行星分散，不满足任何 Yoga
        args = self._make_yoga_args('Aries', 'Sun:Taurus:2,Moon:Gemini:3')
        result = cmd_yoga(args)
        yogas = result.get('yogas', [])
        self.assertEqual(len(yogas), 0, "Should not detect any Yoga with scattered planets")


if __name__ == '__main__':
    unittest.main()
