"""
策略名称：强势ETF多因子轮动策略
描述：每周一调仓，综合动量+波动率+成交量对10只ETF打分，买入得分最高的TOP N
生成时间：2026-04-17
"""

import sys, os, io, math
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

from gm.api import *

# ============================================================
# 配置区
# ============================================================

# 10只ETF标的池（掘金symbol格式）
ETF_POOL = [
    'SHSE.513100',   # 纳指ETF
    'SHSE.513520',   # 日经ETF
    'SHSE.513500',   # 标普ETF
    'SHSE.513030',   # 德国ETF
    'SHSE.513080',   # 法国ETF
    'SHSE.513180',   # 恒生科技ETF
    'SZSE.159920',   # 恒生ETF
    'SHSE.518880',   # 黄金ETF
    'SHSE.551520',   # 原油ETF
    'SZSE.159985',   # 豆粕ETF
]

# ETF名称（用于日志显示）
ETF_NAMES = {
    'SHSE.513100': '纳指ETF',
    'SHSE.513520': '日经ETF',
    'SHSE.513500': '标普ETF',
    'SHSE.513030': '德国ETF',
    'SHSE.513080': '法国ETF',
    'SHSE.513180': '恒生科技',
    'SZSE.159920': '恒生ETF',
    'SHSE.518880': '黄金ETF',
    'SHSE.551520': '原油ETF',
    'SZSE.159985': '豆粕ETF',
}

FREQUENCY = '1d'
DATA_COUNT = 60                     # 回看数据天数（用于计算因子）

# 多因子参数
MOMENTUM_PERIOD = 20               # 动量：过去N天涨幅
VOL_LOOKBACK = 20                  # 波动率回看期
VOLUME_PERIOD = 5                  # 成交量动量：最近N日均量 vs 更早N日均量

TOP_N = 3                          # 持有得分最高的几只

# 调仓频率：每周一
REBALANCE_DAYOFWEEK = 1            # 0=周一(掘金中周一可能是0或1，运行时确认)

# 交易参数
ORDER_TYPE = OrderType_Market

# 回测参数
BACKTEST_START = '2024-06-01 09:30:00'
BACKTEST_END   = '2026-04-17 15:30:00'
INITIAL_CASH   = 1000000
COMMISSION     = 0.00025
SLIPPAGE       = 0.001

# ============================================================
# 因子计算函数
# ============================================================

def calc_momentum(close_prices):
    """动量因子：过去N天涨跌幅（收益率）"""
    if len(close_prices) < MOMENTUM_PERIOD + 1:
        return 0.0
    return (close_prices[-1] - close_prices[-MOMENTUM_PERIOD - 1]) / close_prices[-MOMENTUM_PERIOD - 1]


def calc_volatility(close_prices):
    """波动率因子（取负值，因为低波动更好）— 返回日收益率的标准差"""
    if len(close_prices) < VOL_LOOKBACK + 1:
        return 0.0
    returns = []
    for i in range(-VOL_LOOKBACK, 0):
        r = (close_prices[i] - close_prices[i - 1]) / close_prices[i - 1]
        returns.append(r)
    if len(returns) < 2:
        return 0.0
    mean_r = sum(returns) / len(returns)
    variance = sum((r - mean_r) ** 2 for r in returns) / (len(returns) - 1)
    vol = math.sqrt(variance)
    return vol  # 波动率越低越好，打分时取负


def calc_volume_trend(volumes):
    """成交量趋势因子：近期均量 / 远期均量 - 1（衡量资金关注度上升）"""
    if len(volumes) < VOLUME_PERIOD * 2:
        return 0.0
    recent_avg = sum(volumes[-VOLUME_PERIOD:]) / VOLUME_PERIOD
    earlier_avg = sum(volumes[-VOLUME_PERIOD * 2:-VOLUME_PERIOD]) / VOLUME_PERIOD
    if earlier_avg == 0:
        return 0.0
    return (recent_avg - earlier_avg) / earlier_avg


def score_etf(symbol, context):
    """对单只ETF计算综合得分"""
    try:
        data = context.data(symbol=symbol, frequency=FREQUENCY, count=DATA_COUNT)
        if data is None or len(data) < DATA_COUNT:
            return None

        close = data['close'].tolist()
        volume = data['volume'].tolist() if 'volume' in data.columns else [0] * len(close)

        # ---- 三个因子 ----
        momentum = calc_momentum(close)           # 涨幅越大越好
        volatility = calc_volatility(close)       # 越小越好（后面取反）
        volume_trend = calc_volume_trend(volume)  # 放量越好

        # ---- 归一化打分（简化版：直接加权）----
        # 动量权重 50%，反向波动率权重 25%，成交量趋势权重 25%
        vol_score = -volatility  # 反向：低波动得高分

        total_score = momentum * 50 + vol_score * 25 + volume_trend * 25

        return {
            'symbol': symbol,
            'name': ETF_NAMES.get(symbol, symbol),
            'score': round(total_score, 4),
            'momentum': round(momentum, 4),
            'volatility': round(volatility, 4),
            'volume_trend': round(volume_trend, 4),
            'price': close[-1],
        }
    except Exception as e:
        print(f'[因子计算异常] {symbol}: {e}')
        return None


# ============================================================
# 策略逻辑
# ============================================================

def init(context):
    print('=' * 60)
    print('  强势ETF多因子轮动策略启动')
    print(f'  标的池: {len(ETF_POOL)}只ETF')
    print(f'  因子: 动量({MOMENTUM_PERIOD}d) + 反向波动率 + 成交量趋势')
    print(f'  持仓: TOP {TOP_N}')
    print(f'  调仓: 每周{REBALANCE_DAYOFWEEK}')
    print('=' * 60)

    # 订阅所有ETF
    subscribe(symbols=','.join(ETF_POOL), frequency=FREQUENCY, count=DATA_COUNT)

    context.last_rebalance_date = None  # 上次调仓日期


def on_bar(context, bars):
    """每根K线触发 — 检查是否需要调仓"""
    # 获取当前日期（从bar数据中取）
    current_dt = None
    if bars:
        bar0 = bars[0]
        # bar 可能是 dict 或 DictLikeObject
        if isinstance(bar0, dict):
            current_dt = bar0.get('datetime') or bar0.get('bob')
        else:
            # 属性访问
            current_dt = getattr(bar0, 'datetime', None) or getattr(bar0, 'bob', None)

    if current_dt is None:
        return

    # 提取日期字符串
    date_str = str(current_dt)[:10] if current_dt else ''
    weekday = None
    try:
        # 掘金datetime格式: "2026-04-13 09:30:00"
        from datetime import datetime
        dt_obj = datetime.strptime(date_str, '%Y-%m-%d')
        weekday = dt_obj.weekday()  # 0=Monday
    except:
        pass

    # 只在周一调仓（weekday==0）
    if weekday != REBALANCE_DAYOFWEEK - 1:  # 用户说"周一"，weekday()中周一=0
        return

    # 避免同一天重复调仓
    if context.last_rebalance_date == date_str:
        return

    # 执行调仓
    _rebalance(context, date_str)


def _rebalance(context, date_str):
    """执行一次完整调仓"""
    print(f'\n{"="*60}')
    print(f'  📊 调仓日: {date_str} (周一)')
    print(f'{"="*60}')

    # ---- 1. 对所有ETF打分 ----
    scores = []
    for symbol in ETF_POOL:
        result = score_etf(symbol, context)
        if result is not None:
            scores.append(result)

    if not scores:
        print('[WARN] 所有ETF都无法计算分数，跳过本次调仓')
        return

    # 按得分降序排列
    scores.sort(key=lambda x: x['score'], reverse=True)

    # ---- 2. 打印排行榜 ----
    print(f'\n  {"排名":^4} | {"ETF名称":^10} | {"得分":^10} | {"动量":^10} | {"波动率":^10} | {"量比":^10} | {"价格":^8}')
    print(f'  {"-"*76}')
    for i, s in enumerate(scores):
        mark = ' ✅' if i < TOP_N else ''
        print(f'  {i+1:^4} | {s["name"]:^10} | {s["score"]:^10.4f} | {s["momentum"]:^10.2%} | {s["volatility"]:^10.4f} | {s["volume_trend"]:^10.2%} | {s["price"]:^8.3f}{mark}')

    # ---- 3. 选出 TOP N ----
    target_symbols = set(s['symbol'] for s in scores[:TOP_N])
    print(f'\n  🎯 本周持有: {", ".join([ETF_NAMES.get(s, s) for s in target_symbols])}')

    # ---- 4. 获取当前持仓 ----
    all_positions = get_position()
    current_held = set()
    if all_positions:
        for p in all_positions:
            sym = p.get('symbol') if isinstance(p, dict) else (p.symbol if hasattr(p, 'symbol') else None)
            if sym:
                current_held.add(sym)

    # ---- 5. 计算每只目标ETF的仓位金额（等权分配）----
    cash_info = get_cash()
    available = cash_info.available

    # 先卖出不在目标列表中的持仓
    to_sell = current_held - target_symbols
    if to_sell:
        for sym in to_sell:
            try:
                order_target_volume(sym, 0,
                                    position_side=PositionSide_Long,
                                    order_type=ORDER_TYPE)
                name = ETF_NAMES.get(sym, sym)
                print(f'  🔻 卖出: {name} ({sym})')
            except Exception as e:
                print(f'  [卖出失败] {sym}: {e}')

    # 再调整目标持仓为等权
    if available > 0 and target_symbols:
        per_etf_amount = available / len(target_symbols)

        for sym in target_symbols:
            name = ETF_NAMES.get(sym, sym)
            # 获取当前价格用于计算数量
            etf_data = context.data(symbol=sym, frequency=FREQUENCY, count=5)
            if etf_data is None or len(etf_data) == 0:
                continue
            price = etf_data['close'].iloc[-1]

            # ETF最小单位通常是100份（和股票一样）
            volume = int(per_etf_amount / price / 100) * 100
            if volume >= 100:
                try:
                    order_target_volume(sym, volume,
                                        position_side=PositionSide_Long,
                                        order_type=ORDER_TYPE)
                    print(f'  🟢 买入/持有: {name} {volume}份 × {price:.3f}元 ≈ {volume*price:.0f}元')
                except Exception as e:
                    print(f'  [下单失败] {sym}: {e}')
            else:
                print(f'  ⚠️ {name}: 计算份额不足100份({volume})，跳过')

    # ---- 6. 记录调仓日期 ----
    context.last_rebalance_date = date_str

    # 打印账户摘要
    cash_info = get_cash()
    print(f'\n  💰 可用资金: {cash_info.available:,.0f}元 | 总资产: {cash_info.nav + cash_info.available:,.0f}元')
    print(f'{"="*60}\n')


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
    STRATEGY_ID = os.environ.get('GM_STRATEGY_ID', '') or 'etf_rotation_demo'
    START = os.environ.get('GM_BACKTEST_START', BACKTEST_START)
    END = os.environ.get('GM_BACKTEST_END', BACKTEST_END)
    CASH = float(os.environ.get('GM_INITIAL_CASH', str(INITIAL_CASH)))

    mode = MODE_LIVE if MODE.lower() in ('live', 'realtime') else MODE_BACKTEST

    run(
        strategy_id=STRATEGY_ID,
        filename='strategy_etf_rotation',
        mode=mode,
        token=TOKEN,
        backtest_start_time=START,
        backtest_end_time=END,
        backtest_initial_cash=CASH,
        backtest_commission_ratio=COMMISSION,
        backtest_slippage_ratio=SLIPPAGE,
        backtest_adjust=ADJUST_PREV,
    )
