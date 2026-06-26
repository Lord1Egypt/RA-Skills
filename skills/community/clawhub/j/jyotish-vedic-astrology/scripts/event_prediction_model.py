#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
事件预测模型 v5.0 — 三层验证法（全功能版）
第一层：静态星盘分析（Yoga、宫位、行星聚集、Vivah Saham、Ashtakavarga）
第二层：Dasha激活（Vimshottari + Chara Dasha with Antardasha）
第三层：过境触发（Double Transit PAC+D9、Transit LL/7L、行星聚集、Vivah Saham激活）

v5.0 重大升级：所有分析函数从空壳升级为真实逻辑，接入 jyotish_engine 的全部计算能力
"""

from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


# ============================================================================
# 数据结构
# ============================================================================

class EventType(Enum):
    """事件类型"""
    MARRIAGE = "marriage"
    CAREER = "career"
    WEALTH = "wealth"
    HEALTH = "health"
    EDUCATION = "education"
    CHILDREN = "children"
    TRAVEL = "travel"
    SPIRITUAL = "spiritual"


class RiskLevel(Enum):
    """风险等级"""
    LOW = "低"
    MEDIUM = "中"
    HIGH = "高"
    CRITICAL = "极高"


class Confidence(Enum):
    """置信度（三级）"""
    HIGH = "高"      # 多层验证确认
    MEDIUM = "中"    # 两层验证
    LOW = "低"       # 单层信号或未经验证


@dataclass
class Prediction:
    """预测结果"""
    event_type: EventType
    description: str
    probability: float  # 0-100
    risk_level: RiskLevel
    confidence: Confidence = Confidence.LOW
    timing: Optional[str] = None
    timing_windows: List[Dict] = field(default_factory=list)
    key_factors: List[str] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)
    dasha_signals: List[str] = field(default_factory=list)
    transit_signals: List[str] = field(default_factory=list)
    method: str = "三层验证法 v5.0"


# ============================================================================
# 常量
# ============================================================================

SIGNS = ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo',
         'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces']

SIGN_LORDS = {
    'Aries': 'Mars', 'Taurus': 'Venus', 'Gemini': 'Mercury', 'Cancer': 'Moon',
    'Leo': 'Sun', 'Virgo': 'Mercury', 'Libra': 'Venus', 'Scorpio': 'Mars',
    'Sagittarius': 'Jupiter', 'Capricorn': 'Saturn', 'Aquarius': 'Saturn', 'Pisces': 'Jupiter',
}

# 事件→宫位映射
EVENT_HOUSES = {
    EventType.MARRIAGE: [7, 2, 11, 5],
    EventType.CAREER: [10, 6, 9, 11],
    EventType.WEALTH: [2, 11, 5, 9],
    EventType.HEALTH: [6, 8, 12, 1],
    EventType.EDUCATION: [4, 5, 9, 2],
    EventType.CHILDREN: [5, 9, 2, 11],
    EventType.TRAVEL: [3, 9, 12, 7],
    EventType.SPIRITUAL: [9, 12, 8, 4],
}

# 事件→ Karaka 映射
EVENT_KARAKAS = {
    EventType.MARRIAGE: ['Venus', 'Jupiter', '7L'],
    EventType.CAREER: ['Sun', 'Mercury', 'Saturn', '10L'],
    EventType.WEALTH: ['Jupiter', 'Venus', 'Mercury', '2L'],
    EventType.HEALTH: ['Saturn', 'Moon', '6L'],
    EventType.EDUCATION: ['Mercury', 'Jupiter', '4L'],
    EventType.CHILDREN: ['Jupiter', '5L'],
    EventType.TRAVEL: ['Mercury', 'Rahu', '9L'],
    EventType.SPIRITUAL: ['Jupiter', 'Saturn', 'Ketu', '9L'],
}

# Vimshottari Dasha 行星
DASHA_PLANETS = ['Ketu', 'Venus', 'Sun', 'Moon', 'Mars', 'Rahu', 'Jupiter', 'Saturn', 'Mercury']
DASHA_YEARS = {
    'Ketu': 7, 'Venus': 20, 'Sun': 6, 'Moon': 10, 'Mars': 7,
    'Rahu': 18, 'Jupiter': 16, 'Saturn': 19, 'Mercury': 17,
}

# Graha Drishti 相位
PLANET_ASPECTS = {
    'Sun': [7], 'Moon': [7], 'Mars': [4, 7, 8], 'Mercury': [7],
    'Jupiter': [5, 7, 9], 'Venus': [7], 'Saturn': [3, 7, 10],
    'Rahu': [5, 7, 9], 'Ketu': [5, 7, 9],
}


# ============================================================================
# 预测引擎
# ============================================================================

class EventPredictionModel:
    """事件预测模型 v5.0 — 全功能三层验证法"""

    def __init__(self, chart_data: Dict, dasha_data: Optional[Dict] = None,
                 transit_data: Optional[Dict] = None,
                 congregation_data: Optional[Dict] = None,
                 vivah_saham_data: Optional[Dict] = None,
                 chara_dasha_data: Optional[Dict] = None,
                 double_transit_data: Optional[Dict] = None,
                 ll7l_data: Optional[Dict] = None):
        self.chart = chart_data
        self.dasha = dasha_data or {}
        self.transit = transit_data or {}
        self.congregation = congregation_data or {}
        self.vivah_saham = vivah_saham_data or {}
        self.chara_dasha = chara_dasha_data or {}
        self.double_transit = double_transit_data or {}
        self.ll7l = ll7l_data or {}
        self.predictions = []

        # 预计算 ascendant 索引
        asc_sign = self.chart.get('ascendant', {}).get('sign', 'Aries')
        self.asc_idx = SIGNS.index(asc_sign) if asc_sign in SIGNS else 0

        # 预计算宫主星
        self.house_lords = {}
        for i in range(12):
            h_sign = SIGNS[(self.asc_idx + i) % 12]
            self.house_lords[i + 1] = SIGN_LORDS.get(h_sign, '')

        # 预计算行星宫位
        self.planet_houses = {}
        for pn, pd in self.chart.get('planets', {}).items():
            if isinstance(pd, dict) and 'house' in pd:
                self.planet_houses[pn] = pd['house']

        # 预计算行星经度（度数精确）
        self.planet_lons = {}
        for pn, pd in self.chart.get('planets', {}).items():
            if isinstance(pd, dict) and 'degree' in pd:
                self.planet_lons[pn] = pd['degree']

    def predict_all_events(self) -> List[Prediction]:
        """预测所有类型的事件"""
        predictions = []
        for evt_type in EventType:
            pred = self.predict_event(evt_type)
            if pred:
                predictions.append(pred)
        self.predictions = predictions
        return predictions

    def predict_event(self, evt_type: EventType) -> Optional[Prediction]:
        """预测单个事件类型（核心方法）"""
        # ── 第一层：静态星盘分析 ──
        static = self._layer1_static(evt_type)

        # ── 第二层：Dasha激活 ──
        dasha_signals = self._layer2_dasha(evt_type)

        # ── 第三层：过境触发 ──
        transit_signals = self._layer3_transit(evt_type)

        # ── 综合概率 ──
        probability = self._calc_probability(static, dasha_signals, transit_signals)
        risk = self._assess_risk(static, evt_type)

        # ── 置信度判定 ──
        layer_count = sum([
            1 if static['total_signals'] > 0 else 0,
            1 if len(dasha_signals) > 0 else 0,
            1 if len(transit_signals) > 0 else 0,
        ])
        if layer_count >= 3:
            confidence = Confidence.HIGH
        elif layer_count >= 2:
            confidence = Confidence.MEDIUM
        else:
            confidence = Confidence.LOW

        # ── 时间窗预测 ──
        timing_windows = self._calc_timing_windows(evt_type, dasha_signals, transit_signals)

        # ── 关键因素汇总 ──
        key_factors = []
        for s in static['signals']:
            key_factors.append(f"[静态] {s}")
        for s in dasha_signals:
            key_factors.append(f"[Dasha] {s}")
        for s in transit_signals:
            key_factors.append(f"[Transit] {s}")

        # ── 建议 ──
        recommendations = self._gen_recommendations(evt_type, static, dasha_signals, transit_signals)

        # ── 时间描述 ──
        timing = self._describe_timing(timing_windows, dasha_signals, transit_signals)

        return Prediction(
            event_type=evt_type,
            description=evt_type.value,
            probability=probability,
            risk_level=risk,
            confidence=confidence,
            timing=timing,
            timing_windows=timing_windows,
            key_factors=key_factors,
            recommendations=recommendations,
            dasha_signals=dasha_signals,
            transit_signals=transit_signals,
        )

    # ========================================================================
    # 第一层：静态星盘分析
    # ========================================================================

    def _layer1_static(self, evt_type: EventType) -> Dict:
        """第一层：全面静态分析"""
        result = {'signals': [], 'total_signals': 0, 'details': {}}
        target_houses = EVENT_HOUSES.get(evt_type, [])
        target_karakas = EVENT_KARAKAS.get(evt_type, [])

        # 1. 宫位强旺检查（主宫+辅助宫）
        for h in target_houses:
            h_lord = self.house_lords.get(h, '')
            if h_lord and self.planet_houses.get(h_lord) in target_houses:
                result['signals'].append(f'{h}宫主{h_lord}落入相关宫位({self.planet_houses[h_lord]}宫)')

            # 检查主宫有无吉星落陷/受克
            for pn, ph in self.planet_houses.items():
                if ph == h and pn in target_karakas:
                    pd = self.chart.get('planets', {}).get(pn, {})
                    status = pd.get('status', '')
                    # 支持"擢升(Exalted)"、"落陷(Debilitated)"、"入庙(Own Sign)"等中英混合格式
                    status_lower = status.lower() if status else ''
                    if 'exalted' in status_lower or '擢升' in status:
                        result['signals'].append(f'Karaka {pn}在{h}宫擢升')
                    elif 'own' in status_lower or '入庙' in status:
                        result['signals'].append(f'Karaka {pn}在{h}宫入庙')
                    elif 'debilitated' in status_lower or '落陷' in status:
                        result['signals'].append(f'Karaka {pn}在{h}宫落陷(负面)')

        # 2. 行星聚集分析（使用 congregation_data）
        if self.congregation.get('congregations'):
            for c in self.congregation['congregations']:
                ch = c.get('house', 0)
                if ch in target_houses:
                    strength_label = {'strong': '吉星主导', 'mixed': '吉凶混合', 'malefic_heavy': '凶星主导'}
                    s = strength_label.get(c['strength'], c['strength'])
                    result['signals'].append(
                        f"行星聚集: {c['planets']}聚于{ch}宫({s})，"
                        f"影响{','.join(c.get('impact', []))}")

        # 3. Vivah Saham（婚姻事件特有）
        if evt_type == EventType.MARRIAGE and self.vivah_saham:
            vs = self.vivah_saham
            if vs.get('saham_lon'):
                sahams_house = vs.get('saham_house', 0)
                if sahams_house in [7, 1, 5, 9]:
                    result['signals'].append(
                        f"Vivah Saham在{sahams_house}宫({vs['saham_sign']}) "
                        f"{vs['saham_deg_in_sign']:.1f}°，婚姻敏感点高度相关")
                # 本命行星与 Saham 的合相
                for cj in vs.get('natal_conjuncts', []):
                    result['signals'].append(
                        f"本命{cj['planet']}与Vivah Saham合相({cj['diff_deg']}°)")

        # 4. Ashtakavarga 检查（如果数据可用）
        av_data = self.transit.get('ashtakavarga') or self.dasha.get('ashtakavarga')
        if av_data and isinstance(av_data, dict):
            for h in target_houses[:2]:  # 只检查前两个主宫
                sav = av_data.get('bhinnashtakavarga', {}).get(str(h), {}).get('total', 0)
                if sav and sav >= 28:
                    result['signals'].append(f'Ashtakavarga: {h}宫SAV={sav}(≥28，强)')
                elif sav and sav <= 18:
                    result['signals'].append(f'Ashtakavarga: {h}宫SAV={sav}(≤18，弱)')

        result['total_signals'] = len(result['signals'])
        return result

    # ========================================================================
    # 第二层：Dasha 激活
    # ========================================================================

    def _layer2_dasha(self, evt_type: EventType) -> List[str]:
        """第二层：Dasha 激活分析（Vimshottari + Chara）"""
        signals = []
        target_houses = EVENT_HOUSES.get(evt_type, [])
        target_karakas = EVENT_KARAKAS.get(evt_type, [])

        # ── 2a. Vimshottari Dasha ──
        if self.dasha:
            # 适配 full-reading 输出格式：current_dasha.lord + current_dasha.antardasha[]
            md_lord = ''
            ad_lord = ''

            # 方式1：current_dasha 格式（full-reading输出）
            current_md = self.dasha.get('current_dasha')
            if current_md and isinstance(current_md, dict):
                md_lord = current_md.get('lord', '')
                # 从 antardasha 列表中找 is_current=True 的
                for ad in current_md.get('antardasha', []):
                    if ad.get('is_current'):
                        ad_lord = ad.get('lord', '')
                        break
            else:
                # 方式2：current_mahadasha / current_antardasha 格式
                md_lord = self.dasha.get('current_mahadasha', {}).get('lord', '')
                ad_lord = self.dasha.get('current_antardasha', {}).get('lord', '')

            if md_lord:
                md_house = self.planet_houses.get(md_lord, 0)
                # MD 主星是否关联目标宫位
                if md_house in target_houses:
                    signals.append(f'当前Vimshottari MD {md_lord}在{md_house}宫(目标宫位)')

                # MD 主星是否就是目标 Karaka
                if md_lord in [k for k in target_karakas if not k.endswith('L')]:
                    signals.append(f'当前MD {md_lord}是{evt_type.value}的Karaka')

                # MD 主星是否是目标宫的宫主星
                for h in target_houses:
                    if self.house_lords.get(h) == md_lord:
                        signals.append(f'当前MD {md_lord}是{h}宫主(目标宫)')

            if ad_lord:
                ad_house = self.planet_houses.get(ad_lord, 0)
                if ad_house in target_houses:
                    signals.append(f'当前AD {ad_lord}在{ad_house}宫(目标宫位)')

                for h in target_houses:
                    if self.house_lords.get(h) == ad_lord:
                        signals.append(f'当前AD {ad_lord}是{h}宫主(目标宫)')

                # MD+AD 组合信号（高权重）
                if md_lord and ad_lord:
                    md_house2 = self.planet_houses.get(md_lord, 0)
                    if ad_house in target_houses and md_house2 in target_houses:
                        signals.append(f'★ MD+AD双激活目标宫位({md_lord}+{ad_lord})')

        # ── 2b. Chara Dasha (Jaimini) ──
        if self.chara_dasha:
            # 适配实际格式：dasha_sequence[] 或 dasha_list[]
            cd_list = self.chara_dasha.get('dasha_sequence') or self.chara_dasha.get('dasha_list', [])
            if cd_list:
                # 当前 Chara Mahadasha（第一个条目）
                current_cd = cd_list[0] if cd_list else {}
                cd_sign = current_cd.get('sign', '')
                cd_lord = current_cd.get('lord', '') or SIGN_LORDS.get(cd_sign, '')
                cd_house = self.planet_houses.get(cd_lord, 0)

                if cd_house in target_houses:
                    signals.append(f'当前Chara Dasha {cd_sign}({cd_lord})在{cd_house}宫(目标宫)')

                # Chara Antardasha
                antardashas = current_cd.get('antardashas') or current_cd.get('antardasha', [])
                if antardashas:
                    current_ad = antardashas[0] if antardashas else {}
                    ad_sign = current_ad.get('sign', '')
                    ad_lord_name = current_ad.get('lord', '') or SIGN_LORDS.get(ad_sign, '')
                    ad_h = self.planet_houses.get(ad_lord_name, 0)
                    if ad_h in target_houses:
                        signals.append(f'Chara AD {ad_sign}({ad_lord_name})在{ad_h}宫(目标宫)')

        return signals

    # ========================================================================
    # 第三层：过境触发
    # ========================================================================

    def _layer3_transit(self, evt_type: EventType) -> List[str]:
        """第三层：过境触发分析"""
        signals = []
        target_houses = EVENT_HOUSES.get(evt_type, [])
        event_house = target_houses[0] if target_houses else 7  # 主宫

        # ── 3a. Double Transit PAC + D9 (KN Rao) ──
        if self.double_transit:
            dt = self.double_transit
            dt_list = dt.get('double_transit', [])
            for item in dt_list:
                layer = item.get('layer', '')
                strength = item.get('strength', '')
                # 检查是否命中目标宫
                target = item.get('target', '')
                # 解析 target 中的宫号
                import re
                nums = re.findall(r'(\d+)宫', target)
                for n in nums:
                    if int(n) == event_house:
                        label = '★' if strength == 'strong' else '◇'
                        signals.append(
                            f'{label} Double Transit PAC [{layer}层]: '
                            f'Jupiter+Saturn同时PAC到{event_house}宫({strength})')

            # 汇总
            d1_j = dt.get('d1', {}).get('jupiter', {})
            d1_s = dt.get('d1', {}).get('saturn', {})
            if d1_j or d1_s:
                j_targets = list(d1_j.keys()) if isinstance(d1_j, dict) else []
                s_targets = list(d1_s.keys()) if isinstance(d1_s, dict) else []
                for t in j_targets:
                    nums = re.findall(r'(\d+)宫', t)
                    for n in nums:
                        if int(n) == event_house:
                            signals.append(f'Transit Jupiter PAC到{event_house}宫D1层')
                for t in s_targets:
                    nums = re.findall(r'(\d+)宫', t)
                    for n in nums:
                        if int(n) == event_house:
                            signals.append(f'Transit Saturn PAC到{event_house}宫D1层')

        # ── 3b. Transit LL/7L (婚姻特有) ──
        if evt_type == EventType.MARRIAGE and self.ll7l:
            ll7l = self.ll7l
            # P5: Transit LL PAC natal 7L / Transit 7L PAC natal LL
            p5_signals = ll7l.get('p5', [])
            for s in p5_signals:
                signals.append(f'Transit LL/7L P5: {s}')

            # P8: Transit LL in 7H / Transit 7L in Lagna
            p8_signals = ll7l.get('p8', [])
            for s in p8_signals:
                signals.append(f'Transit LL/7L P8: {s}')

            # Parivartana
            pariv = ll7l.get('parivartana', [])
            if pariv:
                for p in pariv:
                    signals.append(f'Transit LL/7L Parivartana: {p}')

        # ── 3c. Vivah Saham 过境激活（婚姻特有）──
        if evt_type == EventType.MARRIAGE and self.vivah_saham:
            vs_activations = self.vivah_saham.get('transit_activations', [])
            for act in vs_activations:
                signals.append(f'Vivah Saham过境激活: {act}')

        # ── 3d. 基础过境分析（从 transit_data 中提取）──
        if self.transit:
            # Jupiter 过境目标宫
            jup_house = self.transit.get('jupiter', {}).get('house', 0)
            if jup_house in target_houses:
                signals.append(f'Jupiter过境{jup_house}宫(目标宫)')

            # Saturn 过境目标宫
            sat_house = self.transit.get('saturn', {}).get('house', 0)
            if sat_house in target_houses:
                signals.append(f'Saturn过境{sat_house}宫(目标宫)')

            # Rahu/Ketu 过境
            rahu_house = self.transit.get('rahu', {}).get('house', 0)
            ketu_house = self.transit.get('ketu', {}).get('house', 0)
            for rn, rh in [('Rahu', rahu_house), ('Ketu', ketu_house)]:
                if rh in target_houses:
                    signals.append(f'{rn}过境{rh}宫(目标宫)')

            # Sade Sati（Moon 过境相关）
            sade_sati = self.transit.get('sade_sati', {})
            if sade_sati and evt_type in [EventType.CAREER, EventType.HEALTH, EventType.MARRIAGE]:
                phase = sade_sati.get('phase', '')
                if phase:
                    signals.append(f'Sade Sati {phase}期（影响情绪和决策）')

        return signals

    # ========================================================================
    # 概率、风险、时间窗计算
    # ========================================================================

    def _calc_probability(self, static: Dict, dasha: List, transit: List) -> float:
        """综合概率计算"""
        base = 30.0  # 基线概率

        # 静态信号
        static_score = min(static['total_signals'] * 5, 25)
        base += static_score

        # Dasha 信号
        dasha_score = min(len(dasha) * 8, 30)
        base += dasha_score
        # MD+AD 双激活加分
        if any('★' in s for s in dasha):
            base += 10

        # Transit 信号
        transit_score = min(len(transit) * 6, 25)
        base += transit_score
        # Double Transit strong 加分
        if any('★' in s for s in transit):
            base += 15

        return min(100, max(0, round(base, 1)))

    def _assess_risk(self, static: Dict, evt_type: EventType) -> RiskLevel:
        """风险评估"""
        if evt_type == EventType.HEALTH:
            # 健康事件特殊处理（高信号 = 高风险）
            if static['total_signals'] >= 3:
                return RiskLevel.CRITICAL
            elif static['total_signals'] >= 2:
                return RiskLevel.HIGH
            return RiskLevel.LOW
        else:
            if static['total_signals'] >= 4:
                return RiskLevel.HIGH
            elif static['total_signals'] >= 2:
                return RiskLevel.MEDIUM
            return RiskLevel.LOW

    def _calc_timing_windows(self, evt_type: EventType, dasha: List, transit: List) -> List[Dict]:
        """计算时间窗"""
        windows = []

        # 从 Dasha 提取时间信息
        if self.dasha:
            md_info = self.dasha.get('current_mahadasha', {})
            if md_info.get('start') and md_info.get('end'):
                windows.append({
                    'type': 'Vimshottari MD',
                    'period': f"{md_info.get('start', '?')} ~ {md_info.get('end', '?')}",
                    'source': md_info.get('lord', '?'),
                    'weight': 0.6,
                })

        # 从 Chara Dasha 提取
        if self.chara_dasha:
            cd_list = self.chara_dasha.get('dasha_list', [])
            if cd_list:
                cd = cd_list[0]
                start = cd.get('start_year', 0)
                end = cd.get('end_year', 0)
                if start:
                    windows.append({
                        'type': 'Chara Dasha',
                        'period': f"{start} ~ {end}" if end else f"{start}起",
                        'source': cd.get('sign', '?'),
                        'weight': 0.4,
                    })

        return windows

    def _describe_timing(self, windows, dasha, transit) -> str:
        """生成时间描述"""
        parts = []
        if windows:
            for w in windows:
                parts.append(f"{w['type']}({w['period']})")
        if dasha:
            parts.append(f"{len(dasha)}个Dasha信号")
        if transit:
            parts.append(f"{len(transit)}个Transit信号")
        if not parts:
            return "无明确时间窗"
        return " | ".join(parts)

    def _gen_recommendations(self, evt_type, static, dasha, transit) -> List[str]:
        """生成建议"""
        recs = []
        if evt_type == EventType.MARRIAGE:
            if len(dasha) >= 2 and len(transit) >= 1:
                recs.append("Dasha+Transit双重激活，婚姻事件窗已开，积极把握")
            elif len(dasha) >= 1:
                recs.append("Dasha激活中，等待Transit触发确认")
            if any('落陷' in s for s in static['signals']):
                recs.append("相关Karaka落陷，建议补救措施")
        elif evt_type == EventType.CAREER:
            if len(dasha) >= 2 and len(transit) >= 1:
                recs.append("事业突破事件窗已开，抓住机遇")
            recs.append("持续关注10宫主Dasha和Jupiter/Saturn过境10宫")
        elif evt_type == EventType.HEALTH:
            if any('受克' in s or '落陷' in s for s in static['signals']):
                recs.append("有健康警示信号，建议定期体检")
            recs.append("注意Saturn过境6/8/12宫期间的身体健康")
        elif evt_type == EventType.WEALTH:
            if any('★' in s for s in transit):
                recs.append("Double Transit激活财富宫，投资/商业机会窗口")
        if not recs:
            recs.append("保持观察，等待多层信号确认")
        return recs


# ============================================================================
# 报告生成
# ============================================================================

def generate_prediction_report(model: EventPredictionModel) -> str:
    """生成预测报告"""
    if not model.predictions:
        model.predict_all_events()

    lines = []
    lines.append("=" * 60)
    lines.append("事件预测报告 — 三层验证法 v5.0")
    lines.append("=" * 60)
    lines.append("")

    # 置信度分布
    high_count = sum(1 for p in model.predictions if p.confidence == Confidence.HIGH)
    med_count = sum(1 for p in model.predictions if p.confidence == Confidence.MEDIUM)
    low_count = sum(1 for p in model.predictions if p.confidence == Confidence.LOW)

    lines.append(f"分析范围: {len(model.predictions)} 类事件")
    lines.append(f"置信度: 高={high_count}, 中={med_count}, 低={low_count}")
    lines.append("")

    for pred in model.predictions:
        conf_icon = {'高': '⭐', '中': '◆', '低': '○'}.get(pred.confidence.value, '○')
        lines.append(f"{conf_icon}【{pred.event_type.value}】置信度:{pred.confidence.value} 概率:{pred.probability:.0f}% 风险:{pred.risk_level.value}")
        if pred.timing:
            lines.append(f"  时间窗: {pred.timing}")
        for f in pred.key_factors[:5]:  # 最多显示5个
            lines.append(f"  - {f}")
        for r in pred.recommendations[:3]:
            lines.append(f"  → {r}")
        lines.append("")

    return "\n".join(lines)


if __name__ == "__main__":
    # 测试示例
    test_chart = {
        'ascendant': {'sign': 'Leo', 'degree': 130.5},
        'planets': {
            'Sun': {'house': 1, 'sign': 'Leo', 'degree': 132.0, 'status': 'own_sign'},
            'Moon': {'house': 7, 'sign': 'Aquarius', 'degree': 312.0, 'status': ''},
            'Mars': {'house': 4, 'sign': 'Scorpio', 'degree': 222.0, 'status': 'own_sign'},
            'Mercury': {'house': 1, 'sign': 'Leo', 'degree': 145.0, 'status': ''},
            'Jupiter': {'house': 3, 'sign': 'Libra', 'degree': 192.0, 'status': 'debilitated'},
            'Venus': {'house': 12, 'sign': 'Cancer', 'degree': 97.0, 'status': ''},
            'Saturn': {'house': 7, 'sign': 'Aquarius', 'degree': 325.0, 'status': 'own_sign'},
            'Rahu': {'house': 10, 'sign': 'Taurus', 'degree': 60.0, 'status': ''},
            'Ketu': {'house': 4, 'sign': 'Scorpio', 'degree': 240.0, 'status': ''},
        }
    }

    model = EventPredictionModel(test_chart)
    print(generate_prediction_report(model))
