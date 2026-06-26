"""
策略名称：强势ETF动量轮动策略
描述：每周二调仓，20日动量筛选0~20%区间内的ETF，选前2~3名按动量比例分配仓位
生成时间：2026-04-17
"""

import sys, os, io, math
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

from gm.api import *

# ============================================================
# 配置区
# ============================================================

# ETF标的池（掘金symbol格式）
ETF_POOL = [
    'SZSE.159611',   # 富国中证绿色电力ETF
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
    'SHSE.562500',   # 机器人ETF
]

# ETF名称映射
ETF_NAMES = {
    'SZSE.159611': '绿色电力',
    'SZSE.159949': '创业板50',
    'SHSE.515070': 'AIETF',
    'SHSE.515880': '通信设备',
    'SHSE.512760': '半导体',
    'SHSE.517390': '卫星互联',
    'SHSE.513300': '纳斯达克100',
    'SHSE.518880': '黄金',
    'SHSE.588170': '科创半导体',
    'SZSE.159980': '有色',
    'SZSE.159267': '航天',
    'SZSE.159518': '石油',
    'SZSE.159512': '汽车',
    'SZSE.159698': '粮食',
    'SHSE.512630': '卫星广发',
    'SHSE.516520': '智能驾驶',
    'SZSE.159242': '人工智能',
    'SZSE.159326': '电网设备',
    'SHSE.513310': '中韩半导体',
    'SHSE.562500': '机器人',
}

FREQUENCY = '1d'
MOMENTUM_PERIOD = 20              # 20日动量
MOMENTUM_MIN = 0.0                # 动量下限（0%）
MOMENTUM_MAX = 0.20               # 动量上限（20%）
TOP_N = 3                         # 选前2~3名
REBALANCE_WEEKDAY = 1             # 周二（weekday()中周一=0，周二=1）
DATA_COUNT = 30                   # 订阅回看天数

# 回测参数
BACKTEST_START = '2026-01-02 09:30:00'
BACKTEST_END   = '2026-04-17 15:00:00'
INITIAL_CASH   = 1000000
COMMISSION     = 0.00025
SLIPPAGE       = 0.001

# ============================================================
# 动量计算
# ============================================================

def calc_momentum(symbol, context):
    """计算20日动量 = (当前价 - N日前价) / N日前价"""
    try:
        hist = context.data(symbol=symbol, frequency=FREQUENCY, count=MOMENTUM_PERIOD + 5)
        if hist is None or len(hist) < MOMENTUM_PERIOD + 1:
            return None

        close = hist['close']
        current_price = close.iloc[-1]
        start_price = close.iloc[-(MOMENTUM_PERIOD + 1)]
        momentum = (current_price - start_price) / start_price
        return {
            'symbol': symbol,
            'name': ETF_NAMES.get(symbol, symbol),
            'momentum': momentum,
            'price': current_price,
        }
    except Exception as e:
        print(f'  [calc_momentum error] {symbol}: {e}')
        return None


# ============================================================
# 策略逻辑
# ============================================================

def init(context):
    print('=' * 60)
    print('  Strong ETF Momentum Rotation Strategy')
    print(f'  Pool: {len(ETF_POOL)} ETFs')
    print(f'  Momentum: {MOMENTUM_PERIOD}d, range [{MOMENTUM_MIN:.0%} ~ {MOMENTUM_MAX:.0%}]')
    print(f'  Hold: TOP {TOP_N}')
    print(f'  Rebalance: Every Tuesday')
    print(f'  Period: {BACKTEST_START} ~ {BACKTEST_END}')
    print('=' * 60)

    subscribe(symbols=','.join(ETF_POOL), frequency=FREQUENCY, count=DATA_COUNT)
    context.last_rebalance_date = None


def on_bar(context, bars):
    """日线bar触发 — 检查是否周二调仓"""
    if not bars:
        return

    bar0 = bars[0]
    current_dt = None
    if isinstance(bar0, dict):
        current_dt = bar0.get('datetime') or bar0.get('bob')
    else:
        current_dt = getattr(bar0, 'datetime', None) or getattr(bar0, 'bob', None)

    if current_dt is None:
        return

    from datetime import datetime
    date_str = str(current_dt)[:10]
    try:
        dt_obj = datetime.strptime(date_str, '%Y-%m-%d')
        weekday = dt_obj.weekday()  # 0=Mon, 1=Tue
    except:
        return

    # 只在周二调仓
    if weekday != REBALANCE_WEEKDAY:
        return

    # 防同日重复
    if context.last_rebalance_date == date_str:
        return

    _rebalance(context, date_str)


def _rebalance(context, date_str):
    """执行周二战仓"""
    print(f'\n{"="*60}')
    print(f'  Rebalance Day: {date_str} (Tue)')
    print(f'{"="*60}')

    # ---- 1. 计算所有ETF的20日动量 ----
    momentum_list = []
    for symbol in ETF_POOL:
        result = calc_momentum(symbol, context)
        if result is not None:
            momentum_list.append(result)

    if not momentum_list:
        print('  [WARN] No momentum data available, skip')
        return

    # ---- 2. 筛选动量在 0%~20% 之间的ETF ----
    filtered = [m for m in momentum_list if MOMENTUM_MIN <= m['momentum'] <= MOMENTUM_MAX]

    # 按动量降序排列
    filtered.sort(key=lambda x: x['momentum'], reverse=True)

    # ---- 3. 打印完整排行 ----
    print(f'\n  {"Rank":^4} | {"ETF":^10} | {"Momentum":^10} | {"Price":^8} | {"In Range":^8}')
    print(f'  {"-"*56}')
    for i, m in enumerate(momentum_list):
        in_range = 'Y' if MOMENTUM_MIN <= m['momentum'] <= MOMENTUM_MAX else 'N'
        selected_mark = ' <<<' if (m in filtered and filtered.index(m) < TOP_N) else ''
        print(f'  {i+1:^4} | {m["name"]:^10} | {m["momentum"]:>9.2%} | {m["price"]:>8.3f} | {in_range:^8}{selected_mark}')

    # ---- 4. 选出前2~3名 ----
    if not filtered:
        print('\n  [INFO] No ETF with momentum in [0%, 20%], hold cash')
        # 全部清仓
        _close_all_positions(context)
        context.last_rebalance_date = date_str
        return

    candidates = filtered[:TOP_N]
    print(f'\n  Selected ({len(candidates)} ETFs):')
    for c in candidates:
        print(f'    {c["name"]} ({c["symbol"]}) momentum={c["momentum"]:.2%} price={c["price"]:.3f}')

    target_symbols = set(c['symbol'] for c in candidates)

    # ---- 5. 先卖掉不在目标中的持仓 ----
    _close_non_target(context, target_symbols)

    # ---- 6. 按动量比例分配仓位 ----
    # 动量比例: 每只ETF的动量占所有候选ETF动量之和的比例
    total_momentum = sum(c['momentum'] for c in candidates)
    if total_momentum <= 0:
        # 如果动量总和为0或负（不太可能在0~20%范围），等权分配
        weights = {c['symbol']: 1.0 / len(candidates) for c in candidates}
    else:
        weights = {c['symbol']: c['momentum'] / total_momentum for c in candidates}

    print(f'\n  Weights:')
    for c in candidates:
        w = weights[c['symbol']]
        print(f'    {c["name"]}: {w:.1%} (momentum={c["momentum"]:.2%})')

    # 使用 order_target_percent 按总资产比例调仓
    # 注意: order_target_percent(symbol, percent, position_side, order_type)
    for c in candidates:
        sym = c['symbol']
        w = weights[sym]
        try:
            order_target_percent(
                symbol=sym,
                percent=w,
                position_side=PositionSide_Long,
                order_type=OrderType_Market
            )
            print(f'  ORDER: {c["name"]} -> {w:.1%} of NAV')
        except Exception as e:
            print(f'  [ORDER FAIL] {c["name"]}: {e}')

    # 记录调仓日
    context.last_rebalance_date = date_str
    print(f'{"="*60}\n')


def _close_all_positions(context):
    """清仓所有ETF持仓"""
    for symbol in ETF_POOL:
        try:
            pos = context.account().position(symbol=symbol, side=PositionSide_Long)
            if pos and hasattr(pos, 'volume') and pos.volume > 0:
                order_target_volume(symbol, 0, position_side=PositionSide_Long, order_type=OrderType_Market)
                print(f'  CLOSE ALL: {ETF_NAMES.get(symbol, symbol)} ({symbol})')
        except:
            pass


def _close_non_target(context, target_symbols):
    """卖出不在目标列表中的持仓"""
    for symbol in ETF_POOL:
        if symbol in target_symbols:
            continue
        try:
            pos = context.account().position(symbol=symbol, side=PositionSide_Long)
            if pos and hasattr(pos, 'volume') and pos.volume > 0:
                order_target_volume(symbol, 0, position_side=PositionSide_Long, order_type=OrderType_Market)
                print(f'  SELL: {ETF_NAMES.get(symbol, symbol)} ({symbol}) all {pos.volume}sh')
        except:
            pass


def on_tick(context, tick):
    pass


def on_backtest_finished(context, indicator):
    """回测结束，打印绩效"""
    print('\n' + '=' * 60)
    print('  BACKTEST RESULTS')
    print('=' * 60)
    if indicator:
        # indicator 可能是 dict 或对象
        if isinstance(indicator, dict):
            for k, v in indicator.items():
                print(f'  {k}: {v}')
        else:
            for attr in dir(indicator):
                if not attr.startswith('_'):
                    val = getattr(indicator, attr)
                    if not callable(val):
                        print(f'  {attr}: {val}')
    print('=' * 60)


def handle_error(context, error_code, error_msg, **kwargs):
    print(f'[ERROR] {error_code}: {error_msg}')


# ============================================================
# 启动入口
# ============================================================
if __name__ == '__main__':
    TOKEN = os.environ.get('GM_TOKEN', '') or ''
    STRATEGY_ID = os.environ.get('GM_STRATEGY_ID', '')
    START = os.environ.get('GM_BACKTEST_START', BACKTEST_START)
    END = os.environ.get('GM_BACKTEST_END', BACKTEST_END)
    CASH = float(os.environ.get('GM_INITIAL_CASH', str(INITIAL_CASH)))

    print(f'Running backtest with strategy_id={STRATEGY_ID}')
    print(f'Period: {START} ~ {END}')
    print(f'Initial cash: {CASH:,.0f}')

    run(
        strategy_id=STRATEGY_ID,
        filename='strategy_etf_momentum',
        mode=MODE_BACKTEST,
        token=TOKEN,
        backtest_start_time=START,
        backtest_end_time=END,
        backtest_initial_cash=CASH,
        backtest_commission_ratio=COMMISSION,
        backtest_slippage_ratio=SLIPPAGE,
        backtest_adjust=ADJUST_PREV,
    )
