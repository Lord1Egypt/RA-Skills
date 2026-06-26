"""
策略名称：强势ETF动量轮动策略
描述：每周二调仓，从20只ETF中筛选20日动量在0~20%之间的前10只，
      选动量前2~3名，按动量比例分配仓位
生成时间：2026-04-17
"""

import sys, os, io, math
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

from gm.api import *
from datetime import datetime

# ============================================================
# 配置区
# ============================================================

# ETF标的池（掘金symbol格式）
ETF_POOL = [
    'SZSE.159611',   # 富国中证绿色电力ETF
    'SZSE.562500',   # 机器人ETF
    'SZSE.159949',   # 创业板50ETF
    'SHSE.515070',   # 华夏人工智能ETF
    'SHSE.515880',   # 国泰通信设备ETF
    'SHSE.512760',   # 国泰半导体ETF
    'SHSE.517390',   # 卫星互联网ETF
    'SHSE.513300',   # 纳斯达克100ETF
    'SHSE.518880',   # 黄金ETF
    'SHSE.588170',   # 科创半导体
    'SZSE.159980',   # 有色ETF
    'SZSE.159267',   # 航天ETF
    'SZSE.159518',   # 石油ETF
    'SZSE.159512',   # 汽车ETF
    'SZSE.159698',   # 粮食ETF
    'SHSE.512630',   # 卫星ETF广发
    'SHSE.516520',   # 智能驾驶ETF
    'SZSE.159242',   # 人工智能
    'SZSE.159326',   # 电网设备ETF
    'SHSE.513310',   # 中韩半导体ETF
]

# ETF名称映射
ETF_NAMES = {
    'SZSE.159611': '绿色电力',
    'SZSE.562500': '机器人',
    'SZSE.159949': '创业板50',
    'SHSE.515070': 'AIETF',
    'SHSE.515880': '通信设备',
    'SHSE.512760': '半导体',
    'SHSE.517390': '卫星互联',
    'SHSE.513300': '纳斯达克',
    'SHSE.518880': '黄金ETF',
    'SHSE.588170': '科创半导体',
    'SZSE.159980': '有色ETF',
    'SZSE.159267': '航天ETF',
    'SZSE.159518': '石油ETF',
    'SZSE.159512': '汽车ETF',
    'SZSE.159698': '粮食ETF',
    'SHSE.512630': '卫星广发',
    'SHSE.516520': '智能驾驶',
    'SZSE.159242': '人工智能',
    'SZSE.159326': '电网设备',
    'SHSE.513310': '中韩半导体',
}

# 动量参数
MOMENTUM_PERIOD = 20                # 动量回看天数
MOMENTUM_MIN = 0.0                  # 动量下限（0%）
MOMENTUM_MAX = 0.20                 # 动量上限（20%）
CANDIDATE_COUNT = 10                # 从动量在0~20%的ETF中取前N只
TOP_N = 3                           # 最终持有动量前N名

# 调仓参数
REBALANCE_WEEKDAY = 1               # 周二（0=周一, 1=周二）

# 数据参数
FREQUENCY = '1d'
DATA_COUNT = MOMENTUM_PERIOD + 30   # 多拉一些数据确保够用

# 交易参数
ORDER_TYPE = OrderType_Market

# 回测参数
BACKTEST_START = '2024-01-01 09:30:00'
BACKTEST_END   = '2026-04-17 15:30:00'
INITIAL_CASH   = 1000000
COMMISSION     = 0.00025
SLIPPAGE       = 0.001


# ============================================================
# 动量计算
# ============================================================

def calc_momentum(context, symbol):
    """
    计算20日动量: (当前价 - N天前价) / N天前价
    返回 (momentum, current_price) 或 (None, None)
    """
    try:
        hist = context.data(symbol=symbol, frequency=FREQUENCY, count=DATA_COUNT)
        if hist is None or len(hist) < MOMENTUM_PERIOD + 1:
            return None, None

        current_price = hist['close'].iloc[-1]
        start_price = hist['close'].iloc[-(MOMENTUM_PERIOD + 1)]
        momentum = (current_price - start_price) / start_price
        return momentum, current_price
    except Exception as e:
        print(f'  [calc_momentum error] {symbol}: {e}')
        return None, None


# ============================================================
# 策略逻辑
# ============================================================

def init(context):
    print('=' * 70)
    print('  [ETF Momentum Rotation Strategy]')
    print(f'  Pool: {len(ETF_POOL)} ETFs')
    print(f'  Momentum: {MOMENTUM_PERIOD}d, range [{MOMENTUM_MIN:.0%} ~ {MOMENTUM_MAX:.0%}]')
    print(f'  Select: top {CANDIDATE_COUNT} in range -> hold top {TOP_N}')
    print(f'  Rebalance: every Tuesday (weekday={REBALANCE_WEEKDAY})')
    print(f'  Position: proportional to momentum')
    print('=' * 70)

    # 订阅所有ETF日线
    subscribe(symbols=','.join(ETF_POOL), frequency=FREQUENCY, count=DATA_COUNT)

    context.last_rebalance_date = None


def on_bar(context, bars):
    """日线K线回调 — 检查是否周二调仓"""

    # 从bar取当前日期
    current_dt = None
    if bars:
        bar0 = bars[0]
        if isinstance(bar0, dict):
            current_dt = bar0.get('datetime') or bar0.get('bob')
        else:
            current_dt = getattr(bar0, 'datetime', None) or getattr(bar0, 'bob', None)

    if current_dt is None:
        return

    date_str = str(current_dt)[:10]

    # 判断星期几
    try:
        dt_obj = datetime.strptime(date_str, '%Y-%m-%d')
        weekday = dt_obj.weekday()  # 0=Monday, 1=Tuesday
    except:
        return

    # 只在周二触发
    if weekday != REBALANCE_WEEKDAY:
        return

    # 防止同一天重复调仓
    if context.last_rebalance_date == date_str:
        return

    # 执行调仓
    _rebalance(context, date_str)


def _rebalance(context, date_str):
    """核心调仓逻辑"""
    print(f'\n{"="*70}')
    print(f'  [REBALANCE] {date_str} (Tuesday)')
    print(f'{"="*70}')

    # ---- Step 1: 计算所有ETF的20日动量 ----
    momentum_list = []
    for symbol in ETF_POOL:
        mom, price = calc_momentum(context, symbol)
        if mom is not None:
            momentum_list.append({
                'symbol': symbol,
                'name': ETF_NAMES.get(symbol, symbol),
                'momentum': mom,
                'price': price,
            })

    if not momentum_list:
        print('  [WARN] No valid momentum data, skip rebalance')
        return

    # 按动量降序排列
    momentum_list.sort(key=lambda x: x['momentum'], reverse=True)

    # ---- Step 2: 打印完整排行榜 ----
    print(f'\n  {"Rank":>4} | {"ETF":^10} | {"Momentum":>10} | {"Price":>8} | {"InRange":>8}')
    print(f'  {"-"*55}')
    for i, item in enumerate(momentum_list):
        in_range = MOMENTUM_MIN <= item['momentum'] <= MOMENTUM_MAX
        flag = '  YES' if in_range else '  -'
        print(f'  {i+1:>4} | {item["name"]:^10} | {item["momentum"]:>9.2%} | {item["price"]:>8.3f} |{flag}')

    # ---- Step 3: 筛选动量在0%~20%之间的ETF ----
    candidates = [item for item in momentum_list
                  if MOMENTUM_MIN <= item['momentum'] <= MOMENTUM_MAX]

    # 从符合条件的ETF中取前CANDIDATE_COUNT只（动量从高到低）
    candidates = candidates[:CANDIDATE_COUNT]

    if not candidates:
        print('\n  [WARN] No ETF in momentum range [0%, 20%], clear all positions')
        _clear_all_positions()
        context.last_rebalance_date = date_str
        return

    print(f'\n  ETFs in momentum range [0%, 20%]: {len(candidates)}')

    # ---- Step 4: 从候选中选动量前TOP_N名 ----
    targets = candidates[:TOP_N]

    print(f'\n  --- Target Holdings (Top {TOP_N}) ---')
    for i, t in enumerate(targets):
        print(f'  {i+1}. {t["name"]} ({t["symbol"]}) momentum={t["momentum"]:.2%} price={t["price"]:.3f}')

    # ---- Step 5: 按动量比例分配仓位 ----
    target_symbols = set(t['symbol'] for t in targets)

    # 先卖出不在目标列表中的持仓
    _sell_non_targets(target_symbols)

    # 按动量比例分配资金
    _allocate_by_momentum(context, targets)

    # 记录调仓日期
    context.last_rebalance_date = date_str

    # 打印账户摘要
    _print_account_summary()


def _sell_non_targets(target_symbols):
    """卖出不在目标列表中的持仓"""
    positions = get_position()
    if not positions:
        return

    for p in positions:
        if isinstance(p, dict):
            sym = p.get('symbol', '')
            vol = p.get('volume', 0) or p.get('long_volume', 0)
        else:
            sym = getattr(p, 'symbol', '')
            vol = getattr(p, 'volume', 0) or getattr(p, 'long_volume', 0)

        if not sym or sym not in ETF_NAMES:
            continue

        if sym not in target_symbols and vol > 0:
            try:
                order_target_volume(sym, 0,
                                    position_side=PositionSide_Long,
                                    order_type=ORDER_TYPE)
                name = ETF_NAMES.get(sym, sym)
                print(f'  [SELL] {name} ({sym}) - close position')
            except Exception as e:
                print(f'  [SELL FAIL] {sym}: {e}')


def _allocate_by_momentum(context, targets):
    """
    按动量比例分配仓位
    动量越高的ETF分配越多资金
    """
    if not targets:
        return

    # 计算动量权重（动量可能为0，需要+小偏移避免除零）
    momentums = [max(t['momentum'], 0.001) for t in targets]
    total_momentum = sum(momentums)

    # 获取可用资金（先卖出后应该有新资金）
    cash_info = get_cash()
    available = cash_info.available

    print(f'\n  Available cash: {available:,.0f}')

    for i, target in enumerate(targets):
        sym = target['symbol']
        name = target['name']
        price = target['price']
        mom = target['momentum']

        # 动量比例分配
        weight = momentums[i] / total_momentum
        allocated = available * weight

        # 计算股数（ETF最小100股）
        if price <= 0:
            continue
        volume = int(allocated / price / 100) * 100

        if volume >= 100:
            try:
                order_target_volume(sym, volume,
                                    position_side=PositionSide_Long,
                                    order_type=ORDER_TYPE)
                print(f'  [BUY] {name} ({sym}) | mom={mom:.2%} | weight={weight:.1%} | alloc={allocated:,.0f} | vol={volume} x {price:.3f}')
            except Exception as e:
                print(f'  [BUY FAIL] {sym}: {e}')
        else:
            print(f'  [SKIP] {name}: volume={volume} < 100, not enough cash')


def _clear_all_positions():
    """清空所有ETF持仓"""
    positions = get_position()
    if not positions:
        return
    for p in positions:
        if isinstance(p, dict):
            sym = p.get('symbol', '')
        else:
            sym = getattr(p, 'symbol', '')
        if sym and sym in ETF_NAMES:
            try:
                order_target_volume(sym, 0,
                                    position_side=PositionSide_Long,
                                    order_type=ORDER_TYPE)
                name = ETF_NAMES.get(sym, sym)
                print(f'  [SELL] {name} ({sym}) - clear all')
            except Exception as e:
                print(f'  [SELL FAIL] {sym}: {e}')


def _print_account_summary():
    """打印账户摘要"""
    cash_info = get_cash()
    nav = cash_info.nav if hasattr(cash_info, 'nav') else 0
    available = cash_info.available if hasattr(cash_info, 'available') else 0
    print(f'\n  Account: NAV={nav:,.0f} | Available={available:,.0f}')
    print(f'{"="*70}\n')


def on_tick(context, tick):
    pass


def handle_error(context, error_code, error_msg, **kwargs):
    print(f'[ERROR] {error_code}: {error_msg}')


# ============================================================
# 启动入口
# ============================================================
if __name__ == '__main__':
    TOKEN = os.environ.get('GM_TOKEN', '') or ''
    MODE = os.environ.get('GM_RUN_MODE', 'backtest')
    STRATEGY_ID = os.environ.get('GM_STRATEGY_ID', '') or 'etf_momentum_rotation'
    START = os.environ.get('GM_BACKTEST_START', BACKTEST_START)
    END = os.environ.get('GM_BACKTEST_END', BACKTEST_END)
    CASH = float(os.environ.get('GM_INITIAL_CASH', str(INITIAL_CASH)))

    mode = MODE_LIVE if MODE.lower() in ('live', 'realtime') else MODE_BACKTEST

    run(
        strategy_id=STRATEGY_ID,
        filename='strategy_etf_momentum_rotation',
        mode=mode,
        token=TOKEN,
        backtest_start_time=START,
        backtest_end_time=END,
        backtest_initial_cash=CASH,
        backtest_commission_ratio=COMMISSION,
        backtest_slippage_ratio=SLIPPAGE,
        backtest_adjust=ADJUST_PREV,
    )
