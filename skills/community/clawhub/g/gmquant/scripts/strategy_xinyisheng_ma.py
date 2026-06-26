"""
策略名称：双均线交叉策略（新易盛 300502）
描述：MA5 上穿 MA20 买入，下穿卖出
生成时间：2026-04-17
"""

import sys, os, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

from gm.api import *

# ============================================================
# 配置区
# ============================================================
SYMBOLS = 'SZSE.300502'              # 新易盛
FREQUENCY = '1d'                      # 日线
COUNT = 20                            # 滑窗大小

ORDER_TYPE = OrderType_Market         # 市价单
POSITION_PCT = 0.95                   # 仓位占比

BACKTEST_START = '2024-06-01 09:30:00'
BACKTEST_END   = '2026-04-17 15:30:00'
INITIAL_CASH   = 1000000
COMMISSION     = 0.00025
SLIPPAGE       = 0.001

# ============================================================
# 策略逻辑
# ============================================================

def init(context):
    print('=== 双均线策略启动（新易盛 300502）===')
    print(f'标的: {SYMBOLS} | 周期: {FREQUENCY}')
    subscribe(symbols=SYMBOLS, frequency=FREQUENCY, count=COUNT)
    context.last_signal = {}


def on_bar(context, bars):
    for bar in bars:
        _handle_bar(context, bar['symbol'])


def _handle_bar(context, symbol):
    data = context.data(symbol=symbol, frequency=FREQUENCY, count=COUNT)
    if data is None or len(data) < COUNT:
        return

    close = data['close'].tolist()
    current_price = close[-1]

    ma5 = sum(close[-5:]) / 5
    ma20 = sum(close[-20:]) / 20

    prev_ma5 = sum(close[-6:-1]) / 5 if len(close) >= 6 else ma5
    prev_close_list = close[14:34] if len(close) >= 35 else close[-20:]
    prev_ma20 = sum(prev_close_list) / len(prev_close_list)

    golden_cross = (prev_ma5 <= prev_ma20) and (ma5 > ma20)
    death_cross = (prev_ma5 >= prev_ma20) and (ma5 < ma20)

    position = get_position()
    pos = None
    if position:
        for p in position:
            sym = p.get('symbol') if isinstance(p, dict) else (p.symbol if hasattr(p, 'symbol') else None)
            if sym == symbol:
                pos = p
                break

    cash_info = get_cash()

    if golden_cross and not pos:
        order_val = cash_info.available * POSITION_PCT
        volume = int(order_val / current_price / 100) * 100
        if volume > 0:
            order_volume(symbol, volume,
                         side=OrderSide_Buy,
                         position_effect=PositionEffect_Open,
                         order_type=ORDER_TYPE)
            print(f'[买入] {symbol} 价格={current_price:.2f} 数量={volume} MA5={ma5:.2f} MA20={ma20:.2f}')

    elif death_cross and pos:
        order_target_volume(symbol, 0,
                            position_side=PositionSide_Long,
                            order_type=ORDER_TYPE)
        print(f'[卖出] {symbol} 价格={current_price:.2f} MA5={ma5:.2f} MA20={ma20:.2f}')

    context.last_signal[symbol] = {'price': current_price, 'ma5': round(ma5, 2), 'ma20': round(ma20, 2)}


def handle_error(context, error_code, error_msg, **kwargs):
    print(f'[ERROR] {error_code}: {error_msg}')


if __name__ == '__main__':
    TOKEN = os.environ.get('GM_TOKEN', '') or ''
    MODE = os.environ.get('GM_RUN_MODE', 'backtest')
    STRATEGY_ID = os.environ.get('GM_STRATEGY_ID', '') or 'ma_xinyisheng_demo'
    START = os.environ.get('GM_BACKTEST_START', BACKTEST_START)
    END = os.environ.get('GM_BACKTEST_END', BACKTEST_END)
    CASH = float(os.environ.get('GM_INITIAL_CASH', str(INITIAL_CASH)))

    mode = MODE_LIVE if MODE.lower() in ('live', 'realtime') else MODE_BACKTEST

    run(
        strategy_id=STRATEGY_ID,
        filename='strategy_xinyisheng_ma',
        mode=mode,
        token=TOKEN,
        backtest_start_time=START,
        backtest_end_time=END,
        backtest_initial_cash=CASH,
        backtest_commission_ratio=COMMISSION,
        backtest_slippage_ratio=SLIPPAGE,
        backtest_adjust=ADJUST_PREV,
    )
