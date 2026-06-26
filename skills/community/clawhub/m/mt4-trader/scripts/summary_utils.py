# -*- coding: utf-8 -*-
"""
持仓汇总核心逻辑 - 共享模块
供 position_summary.py 和 position_summary_cron.py 共用
"""
import logging

logger = logging.getLogger(__name__)


def build_position_summary(raw_positions_response):
    """
    从 MT4 持仓响应中构建汇总文本。

    Args:
        raw_positions_response: MT4Client.get_positions() 的返回结果

    Returns:
        (summary_text, count, total_pl) 三元组。
        异常时返回 (错误信息, 0, 0.0)
    """
    try:
        count = raw_positions_response.get('count', 0)
        positions = raw_positions_response.get('positions', [])

        if count == 0 or not positions:
            return "✅ 当前无持仓。", 0, 0.0

        lines = [f"📊 **订单汇总**（共{count}单）\n"]

        symbols = {}
        total_pl = 0.0

        for p in positions:
            sym = p.get('symbol', '?')
            ptype = p.get('type', 'buy')
            lots = p.get('lots', 0)
            profit = p.get('profit', 0.0)

            if sym not in symbols:
                symbols[sym] = {
                    'buy': {'lots': 0, 'count': 0, 'pl': 0},
                    'sell': {'lots': 0, 'count': 0, 'pl': 0}
                }
            symbols[sym][ptype]['lots'] += lots
            symbols[sym][ptype]['count'] += 1
            symbols[sym][ptype]['pl'] += profit
            total_pl += profit

        for sym, data in symbols.items():
            buy_lots = data['buy']['lots']
            sell_lots = data['sell']['lots']
            net = buy_lots - sell_lots
            if net > 0:
                net_str = f"净多{net:.2f}"
            elif net < 0:
                net_str = f"净空{abs(net):.2f}"
            else:
                net_str = "持平"
            lines.append(
                f"**{sym}**: 多{buy_lots:.2f}手({data['buy']['count']}单) / "
                f"空{sell_lots:.2f}手({data['sell']['count']}单) → {net_str}"
            )

        lines.append(f"\n**总盈亏**: ${total_pl:.2f}")
        return '\n'.join(lines), count, total_pl

    except Exception as e:
        logger.exception("构建持仓汇总时出错")
        return f"❌ 构建汇总失败: {e}", 0, 0.0