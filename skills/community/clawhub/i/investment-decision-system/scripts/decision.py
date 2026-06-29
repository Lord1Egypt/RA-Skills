"""
Investment Decision System - Decision Engine
INVEST 六维决策框架: Intent, Numbers, Value, Edge, Safety, Timing
"""

import json


# ---- INVEST Framework ----

INVEST_DIMENSIONS = {
    'intent': {
        'name': '意图 (Intent)',
        'weight': 0.15,
        'description': '投资目标是否清晰？这笔交易与你的整体策略一致吗？',
        'questions': [
            '你的投资目标是什么？（增值/收息/保值/投机）',
            '这笔交易是否符合你的投资目标？',
            '你期望的回报率是多少？预期持有多久？',
            '如果这笔交易亏损50%，你的生活会受影响吗？',
        ],
        'scoring_guide': {
            '0-3': '目标模糊，纯跟风或情绪驱动',
            '4-6': '有大致方向，但缺乏具体计划',
            '7-8': '目标明确，与整体策略一致',
            '9-10': '目标极为清晰，有完整的投资论点和退出计划',
        }
    },
    'numbers': {
        'name': '数字 (Numbers)',
        'weight': 0.20,
        'description': '关键财务数据和技术指标是否支持你的判断？',
        'questions': [
            'PE/PB/PS 估值水平如何？与历史区间和同行比较？',
            'ROE/ROA 盈利能力如何？是否有改善趋势？',
            '营收和利润增长率如何？现金流健康吗？',
            '技术面：趋势、支撑/阻力、成交量是否配合？',
        ],
        'scoring_guide': {
            '0-3': '缺乏关键数据支持，凭感觉决策',
            '4-6': '看过一些数据，但分析不深入',
            '7-8': '多维度数据交叉验证，逻辑自洽',
            '9-10': '全面深入的数据分析，量化模型支持',
        }
    },
    'value': {
        'name': '价值 (Value)',
        'weight': 0.20,
        'description': '当前价格是否低于内在价值？安全边际够吗？',
        'questions': [
            '你估计的内在价值是多少？用什么方法估算的？',
            '当前价格相对于内在价值的折扣（安全边际）是多少？',
            '公司的护城河是什么？可持续吗？',
            '最差情况下，这个资产值多少钱？',
        ],
        'scoring_guide': {
            '0-3': '没有估值概念，只看价格涨跌',
            '4-6': '有粗略估值，但安全边际不足',
            '7-8': '估值合理，有足够安全边际',
            '9-10': '深度低估，安全边际充裕，护城河清晰',
        }
    },
    'edge': {
        'name': '优势 (Edge)',
        'weight': 0.10,
        'description': '你比别人多知道什么？你的信息或分析优势在哪？',
        'questions': [
            '你对这个行业/公司有什么独特的了解？',
            '你的信息优势是什么？（行业经验、专业背景、独特数据源）',
            '市场中大多数人对这个资产的看法与你不同在哪？',
            '如果所有人都知道这个信息，价格已经反映了吗？',
        ],
        'scoring_guide': {
            '0-3': '没有信息优势，和大众认知一致',
            '4-6': '有一些行业了解，但优势不显著',
            '7-8': '有明显的认知差或信息优势',
            '9-10': '深度行业洞察，信息不对称明显，大众尚未认知',
        }
    },
    'safety': {
        'name': '安全 (Safety)',
        'weight': 0.20,
        'description': '风险控制是否到位？止损、仓位、分散化是否合理？',
        'questions': [
            '这笔交易的最大可能亏损是多少？你能承受吗？',
            '止损位设在哪里？基于什么逻辑？',
            '这笔交易占你总资产的比例是否合理？',
            '你的投资组合是否足够分散？有没有集中度风险？',
            '如果出现黑天鹅事件，你的应对方案是什么？',
        ],
        'scoring_guide': {
            '0-3': '没有止损计划，仓位过重或过于集中',
            '4-6': '有止损但执行不严格，仓位基本合理',
            '7-8': '止损明确，仓位控制良好，组合分散',
            '9-10': '完善的风控体系，压力测试充分，极端情景有预案',
        }
    },
    'timing': {
        'name': '时机 (Timing)',
        'weight': 0.15,
        'description': '现在是合适的入场/出场时机吗？',
        'questions': [
            '当前市场处于什么周期阶段？（牛市/熊市/震荡）',
            '技术面上是否出现买入/卖出信号？',
            '有没有即将发生的重大事件影响？（财报、政策、行业变化）',
            '你是分批建仓还是一次性买入？为什么？',
            '如果错过这个时机，你会后悔吗？为什么现在必须行动？',
        ],
        'scoring_guide': {
            '0-3': '追涨杀跌，FOMO驱动，没有时机判断',
            '4-6': '粗略判断时机，但缺乏系统分析',
            '7-8': '时机选择有逻辑支撑，分批操作',
            '9-10': '精准把握周期节点，左侧/右侧策略清晰',
        }
    },
}


def evaluate_decision(scores, decision_type='buy'):
    """
    Evaluate an INVEST decision with given scores.

    Args:
        scores: dict with keys intent_score, numbers_score, value_score,
                edge_score, safety_score, timing_score (each 0-10)
        decision_type: 'buy', 'sell', or 'hold'

    Returns:
        dict with total_score, recommendation, dimension_details, action_items
    """
    dim_keys = ['intent_score', 'numbers_score', 'value_score',
                'edge_score', 'safety_score', 'timing_score']
    dim_map = {
        'intent_score': 'intent',
        'numbers_score': 'numbers',
        'value_score': 'value',
        'edge_score': 'edge',
        'safety_score': 'safety',
        'timing_score': 'timing',
    }

    total = 0
    dimensions_detail = []

    for key in dim_keys:
        dim_name = dim_map[key]
        dim_info = INVEST_DIMENSIONS[dim_name]
        score = scores.get(key, 0) or 0
        weight = dim_info['weight']
        weighted = score * weight
        total += weighted

        level = 'danger'
        if score >= 7:
            level = 'good'
        elif score >= 4:
            level = 'warning'

        dimensions_detail.append({
            'key': dim_name,
            'name': dim_info['name'],
            'score': score,
            'weight': weight,
            'weighted': round(weighted, 2),
            'level': level,
        })

    total = round(total, 1)

    # Recommendation
    if total >= 7.0:
        recommendation = 'STRONG_CONFIDENCE'
        label = '强烈推荐 / 信心充足'
        color = '#22c55e'
        icon = '✅'
    elif total >= 5.0:
        recommendation = 'CAUTIOUS'
        label = '谨慎推荐 / 可考虑'
        color = '#eab308'
        icon = '⚠️'
    elif total >= 3.0:
        recommendation = 'WAIT'
        label = '建议等待 / 减少仓位'
        color = '#f97316'
        icon = '⏸️'
    else:
        recommendation = 'AVOID'
        label = '不建议 / 应回避'
        color = '#ef4444'
        icon = '❌'

    # Weakest dimensions
    sorted_dims = sorted(dimensions_detail, key=lambda x: x['score'])
    weakest = [d for d in sorted_dims if d['score'] < 5]

    # Action items based on weak dimensions
    action_items = []
    for dim in weakest:
        dm = INVEST_DIMENSIONS[dim['key']]
        action_items.append({
            'dimension': dim['name'],
            'score': dim['score'],
            'suggestion': f"加强{dim['name']}维度分析: {dm['questions'][0]}",
            'priority': 'P0' if dim['score'] <= 2 else 'P1' if dim['score'] <= 4 else 'P2',
        })

    return {
        'total_score': total,
        'recommendation': recommendation,
        'label': label,
        'color': color,
        'icon': icon,
        'dimensions': dimensions_detail,
        'weakest_dimensions': [d['name'] for d in weakest],
        'action_items': action_items,
        'decision_type': decision_type,
    }


def calculate_position_size(capital, risk_per_trade_pct, entry_price, stop_loss_price, max_position_pct=20):
    """
    Calculate optimal position size using fixed fractional method.

    Args:
        capital: Total available capital
        risk_per_trade_pct: Max % of capital to risk on this trade (e.g., 2)
        entry_price: Planned entry price
        stop_loss_price: Stop loss price
        max_position_pct: Maximum position size as % of capital

    Returns:
        dict with shares, position_value, position_pct, risk_amount, risk_reward
    """
    risk_amount = capital * (risk_per_trade_pct / 100)
    risk_per_share = abs(entry_price - stop_loss_price)

    if risk_per_share <= 0:
        return {
            'error': '止损价必须与入场价不同',
            'shares': 0, 'position_value': 0, 'position_pct': 0,
            'risk_amount': risk_amount, 'risk_reward': 0,
        }

    shares_by_risk = int(risk_amount / risk_per_share)
    position_value = shares_by_risk * entry_price
    position_pct = position_value / capital * 100

    # Cap at max position
    max_value = capital * (max_position_pct / 100)
    if position_value > max_value:
        shares_by_risk = int(max_value / entry_price)
        position_value = shares_by_risk * entry_price
        position_pct = position_value / capital * 100

    # Risk/reward (assuming take profit at 2x risk by default)
    take_profit_price = entry_price + (entry_price - stop_loss_price) * 2
    risk_reward = 2.0

    return {
        'shares': max(shares_by_risk, 0),
        'position_value': round(position_value, 2),
        'position_pct': round(position_pct, 1),
        'risk_amount': round(risk_amount, 2),
        'risk_per_share': round(risk_per_share, 2),
        'entry_price': entry_price,
        'stop_loss_price': stop_loss_price,
        'suggested_take_profit': round(take_profit_price, 2),
        'risk_reward': risk_reward,
        'capital': capital,
    }


def format_decision_report(evaluation, position_sizing=None):
    """Format a decision evaluation into a readable text report."""
    lines = []
    lines.append("=" * 60)
    lines.append("  INVEST 投资决策评估报告")
    lines.append("=" * 60)
    lines.append(f"  综合评分: {evaluation['total_score']}/10   {evaluation['icon']} {evaluation['label']}")
    lines.append(f"  决策类型: {evaluation['decision_type']}")
    lines.append("-" * 60)
    lines.append("  六维评分明细:")
    for dim in evaluation['dimensions']:
        bar = '█' * dim['score'] + '░' * (10 - dim['score'])
        lines.append(f"  {dim['name']:12s} [{bar}] {dim['score']}/10 (权重 {dim['weight']*100:.0f}%)")
    lines.append("-" * 60)

    if evaluation['weakest_dimensions']:
        lines.append(f"  ⚡ 薄弱维度: {', '.join(evaluation['weakest_dimensions'])}")
        lines.append("")
        lines.append("  改进建议:")
        for item in evaluation['action_items']:
            lines.append(f"  [{item['priority']}] {item['suggestion']}")

    if position_sizing and 'error' not in position_sizing:
        lines.append("-" * 60)
        lines.append("  仓位计算:")
        lines.append(f"  可用资金: ¥{position_sizing['capital']:,.2f}")
        lines.append(f"  建议股数: {position_sizing['shares']} 股")
        lines.append(f"  仓位价值: ¥{position_sizing['position_value']:,.2f}")
        lines.append(f"  仓位占比: {position_sizing['position_pct']}%")
        lines.append(f"  风险金额: ¥{position_sizing['risk_amount']:,.2f}")
        lines.append(f"  每股风险: ¥{position_sizing['risk_per_share']:.2f}")
        lines.append(f"  止损价: ¥{position_sizing['stop_loss_price']:.2f}")
        lines.append(f"  建议止盈: ¥{position_sizing['suggested_take_profit']:.2f}")
        lines.append(f"  风险回报比: 1:{position_sizing['risk_reward']}")

    lines.append("=" * 60)

    return '\n'.join(lines)


if __name__ == '__main__':
    # Quick test
    scores = {
        'intent_score': 7,
        'numbers_score': 6,
        'value_score': 8,
        'edge_score': 5,
        'safety_score': 7,
        'timing_score': 6,
    }
    result = evaluate_decision(scores)
    sizing = calculate_position_size(100000, 2, 50, 46)
    print(format_decision_report(result, sizing))
