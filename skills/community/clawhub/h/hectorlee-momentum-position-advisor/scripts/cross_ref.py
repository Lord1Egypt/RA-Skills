"""
量价收敛形态交叉引用 V1.0
封装 volume-price-screener 的检测与评分，供 momentum-position-advisor 融合使用。

融合逻辑：
  - 量价收敛命中 → 动量信号增强（蓄力+趋势=共振）
  - 量价收敛背离预警 → 动量卖出信号强化
  - 量价收敛未命中 → 纯动量驱动，无额外影响
"""

import os
import sys
from typing import List, Dict, Optional, Tuple

_SCREENER_DIR = os.path.expanduser('~/.workbuddy/skills/volume-price-screener/scripts')
if _SCREENER_DIR not in sys.path:
    sys.path.insert(0, _SCREENER_DIR)


def get_vp_result(kline: List[dict], code: str = '', params: dict = None) -> Optional[dict]:
    """
    调用 volume-price-screener 的 detect_pattern + scoring，
    返回统一格式的结果字典。
    
    返回 None 表示未命中任何量价收敛形态。
    
    返回格式:
    {
        'hit': True/False,
        'variant': 'A'/'B'/'C'/'D'/'R',
        'label': '标准横盘'/'高位平台'/'回踩确认'/'突破延续'/'底部反转',
        'variant_icon': 'A'/'B'/'C'/'D'/'R',
        'score': 68,            # 0-100
        'tier': 'standard',     # 'strong' (>=80) / 'standard' (60-79) / 'watch' (<60)
        'anchor_date': '2026-07-20',
        'surge_pct': 9.4,       # 放量日涨幅
        'volume_ratio': 2.3,    # 量比
        'shrink_days': 5,       # 缩量天数
        'shrink_depth': 0.35,   # 缩量深度
        'warning': None,        # 背离预警，如 '横盘期放量滞涨（出货嫌疑）'
        'detail': '...',        # 一行摘要
    }
    """
    try:
        from pattern_detect import detect_pattern, Bar
        from scoring import score_pattern
    except ImportError:
        return None
    
    if len(kline) < 20:
        return None
    
    # 转换为 Bar 对象
    bars = []
    for k in kline:
        bars.append(Bar(
            date=k['date'],
            open=k['open'],
            high=k['high'],
            low=k['low'],
            close=k['close'],
            volume=k['volume'],
            turnover=k.get('turnover'),
        ))
    
    # 检测形态
    p = params or {}
    result = detect_pattern(bars, code, p)
    
    if result is None or not result.pattern_variant:
        return None
    
    # 评分
    score_data = score_pattern(result)
    score = score_data.total if hasattr(score_data, 'total') else 0
    warning = score_data.warning if hasattr(score_data, 'warning') else None
    
    # 分级
    if score >= 80:
        tier = 'strong'
    elif score >= 60:
        tier = 'standard'
    else:
        tier = 'watch'
    
    # 变体图标映射
    icon_map = {'A': 'A', 'B': 'B', 'C': 'C', 'D': 'D', 'R': 'R'}
    
    return {
        'hit': True,
        'variant': result.pattern_variant,
        'label': result.pattern_label,
        'variant_icon': icon_map.get(result.pattern_variant, '?'),
        'score': score,
        'tier': tier,
        'anchor_date': result.anchor_date,
        'surge_pct': round(result.surge_pct, 1),
        'volume_ratio': round(result.volume_ratio, 1),
        'shrink_days': result.shrink_days,
        'shrink_depth': round(result.shrink_depth, 2),
        'warning': warning,
        'detail': (
            f"V{result.pattern_variant} {result.pattern_label} "
            f"放量日{result.anchor_date} 量比{result.volume_ratio:.1f}x "
            f"缩量{result.shrink_days}日 得分{score}"
        ),
    }


def compute_fusion_bonus(vp_result: Optional[dict], momentum_decision: str) -> Tuple[int, str]:
    """
    计算量价收敛对动量评分的融合加成。
    
    返回: (bonus_points, reason_string)
    
    规则:
      - 量价收敛强形态(>=80分) + 动量持有 → +12 (共振，最理想)
      - 量价收敛标准形态(>=60分) + 动量持有 → +8 (双重确认)
      - 量价收敛关注形态(<60分) + 动量持有 → +3 (略有加分)
      - 量价收敛命中 + 动量减仓 → +5 (回调蓄力，减仓不急)
      - 量价收敛命中 + 动量卖出 → +5 (趋势初期回踩，关注假跌破)
      - 量价收敛背离预警 → -8 (强化卖出)
      - 量价收敛未命中 + 动量持有 → 0 (纯动量，无附加)
      - 量价收敛未命中 + 动量卖出/减仓 → 0
    """
    if vp_result is None:
        return 0, "量价收敛形态未命中，纯动量驱动"
    
    score = vp_result.get('score', 0)
    tier = vp_result.get('tier', 'watch')
    warning = vp_result.get('warning')
    label = vp_result.get('label', '')
    
    # 背离预警 → 扣分
    if warning:
        return -8, f"量价收敛预警: {warning}（动量信号强化）"
    
    if momentum_decision in ('hold', 'hold_buy'):
        if tier == 'strong':
            return 12, f"量价共振: {label} {score}分（强势蓄力+动量趋势，最优信号）"
        elif tier == 'standard':
            return 8, f"量价共振: {label} {score}分（蓄力确认+动量持有，双重确认）"
        else:
            return 3, f"量价关注: {label} {score}分（弱蓄力信号，略加分）"
    
    elif momentum_decision in ('reduce', 'reduce_watch'):
        if score >= 60:
            return 5, f"量价收敛: {label} {score}分（回调蓄力中，减仓不必过急）"
        else:
            return 0, f"量价弱信号: {label} {score}分（维持减仓判断）"
    
    elif momentum_decision == 'sell':
        if score >= 60:
            return 5, f"量价收敛: {label} {score}分（趋势初期回踩？关注是否假跌破）"
        else:
            return 2, f"量价弱蓄力: {label} {score}分（卖出信号为主，蓄力不足以逆转）"
    
    return 0, ""


def format_vp_summary(vp_result: Optional[dict]) -> str:
    """格式化为一行摘要"""
    if vp_result is None:
        return "[volume-price] no convergence pattern -> pure momentum"
    
    v = vp_result
    tier_icon = {'strong': '[STRONG]', 'standard': '[OK]', 'watch': '[WEAK]'}
    icon = tier_icon.get(v.get('tier', 'watch'), '[?]')
    warning = f" WARN:{v['warning']}" if v.get('warning') else ""
    
    return (
        f"[volume-price] {icon} V{v['variant']} {v['label']} "
        f"{v['score']}pts "
        f"anchor={v['anchor_date']} "
        f"vol={v['volume_ratio']}x shrink={v['shrink_days']}d"
        f"{warning}"
    )
