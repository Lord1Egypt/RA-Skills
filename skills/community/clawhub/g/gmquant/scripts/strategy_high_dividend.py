"""
策略名称：高红利+低波 Smart Beta 策略
描述：每季度调仓，综合股息率(60%) + 反向波动率(40%)对沪深300成分股打分，
       持有得分最高的TOP N只，等权分配仓位
生成时间：2026-04-17

选股逻辑：
  1. 用 get_dividend 获取过去12个月的每股分红总额
  2. 用 history/history_n 获取股价计算年化波动率
  3. 综合得分 = 股息率 * 60% + (-波动率) * 40%
  4. 选 TOP N 只等权持有
"""

import sys, os, io, math
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

from gm.api import *

# ============================================================
# 配置区
# ============================================================

# 标的池 — 沪深300成分股（用指数代码代表，init时展开）
INDEX_SYMBOL = 'SHSE.000300'   # 沪深300指数

FREQUENCY = '1d'
DATA_COUNT = 120                # 回看数据天数（用于计算因子）

# 因子参数
DIVIDEND_LOOKBACK_DAYS = 365   # 分红回看期（近1年）
VOL_LOOKBACK = 20              # 波动率日频回看期（月度）
ANNUAL_FACTOR = 245            # 年化交易日数

TOP_N = 10                     # 持有只数

# 调仓频率 — 季度（3/6/9/12月第一个交易日）
REBALANCE_MONTHS = [3, 6, 9, 12]

# 交易参数
ORDER_TYPE = OrderType_Market

# 回测参数
BACKTEST_START = '2023-01-01 09:30:00'
BACKTEST_END   = '2026-04-17 15:30:00'
INITIAL_CASH   = 1000000
COMMISSION     = 0.00025
SLIPPAGE       = 0.001


# ============================================================
# 工具函数
# ============================================================

def get_hs300_symbols(context):
    """获取沪深300当前成分股列表"""
    try:
        # 用 get_history_symbol 或 index_weight 获取成分股
        # 方式1: 通过 index_weight 接口
        from datetime import datetime, timedelta
        ref_date = (context.now - timedelta(days=1)).strftime('%Y-%m-%d') if hasattr(context, 'now') else '2026-01-01'

        weights = index_weight(index_symbol=INDEX_SYMBOL, date=ref_date)
        if weights and len(weights) > 0:
            symbols = [w['symbol'] if isinstance(w, dict) else w.symbol for w in weights]
            print(f'  从 {INDEX_SYMBOL} 获取到 {len(symbols)} 只成分股')
            return symbols
    except Exception as e:
        print(f'  [WARN] index_weight 失败: {e}，尝试备用方式')

    # 备用方式：硬编码常见高红利标的池
    fallback_pool = [
        'SHSE.600519', 'SZSE.000858', 'SHSE.601318', 'SHSE.600036',
        'SHSE.601398', 'SZSE.002594', 'SHSE.600276', 'SZSE.000333',
        'SHSE.600585', 'SHSE.601088', 'SHSE.600900', 'SHSE.601166',
        'SHSE.600887', 'SZSE.002304', 'SHSE.601888', 'SZSE.000651',
        'SHSE.601288', 'SHSE.600104', 'SHSE.600016', 'SHSE.600019',
        'SHSE.601006', 'SHSE.601628', 'SZSE.001979', 'SHSE.600309',
        'SZSE.000002', 'SHSE.600000', 'SHSE.601668', 'SHSE.601988',
        'SHSE.600028', 'SHSE.600031', 'SZSE.000063', 'SHSE.601618',
        'SHSE.600085', 'SZSE.000895', 'SHSE.601939', 'SHSE.600372',
        'SHSE.600690', 'SHSE.603160', 'SHSE.600887', 'SZSE.002142',
        'SHSE.601012', 'SHSE.600050', 'SHSE.600104', 'SZSE.002493',
        'SHSE.601888', 'SHSE.600011', 'SZSE.000568', 'SHSE.600115',
        'SHSE.600109', 'SZSE.000538', 'SHSE.600153', 'SHSE.600196',
    ]
    print(f'  使用备用股票池: {len(fallback_pool)} 只')
    return fallback_pool


def calc_dividend_yield(symbol, context):
    """
    计算滚动股息率 TTM
    = 过去12个月每股分红总额 / 当前股价 * 100%
    """
    try:
        # 确定查询日期范围
        if hasattr(context, 'now') and context.now is not None:
            end_dt = context.now.strftime('%Y-%m-%d')
            start_dt = (context.now.replace(year=context.now.year - 1)).strftime('%Y-%m-%d')
        else:
            end_dt = BACKTEST_END[:10]
            start_dt = '2023-01-01'

        div_data = get_dividend(symbol=symbol, start_date=start_dt, end_date=end_dt, df=True)
        if div_data is None or len(div_data) == 0:
            return None

        total_cash_div = div_data['cash_div'].sum()
        if total_cash_div <= 0:
            return 0.0

        # 获取最新股价
        price_data = history_n(symbol=symbol, frequency='1d', count=1,
                               fields='close', adjust=ADJUST_PREV, df=True)
        if price_data is None or len(price_data) == 0:
            return None
        latest_price = price_data['close'].iloc[0]
        if latest_price <= 0:
            return None

        yield_rate = total_cash_div / latest_price * 100  # 百分比
        return yield_rate

    except Exception as e:
        print(f'    [股息计算] {symbol}: {e}')
        return None


def calc_volatility(symbol):
    """计算年化波动率（%）— 基于日线收益率标准差 * sqrt(245)"""
    try:
        data = history_n(symbol=symbol, frequency='1d', count=DATA_COUNT,
                         fields='close', adjust=ADJUST_PREV, df=True)
        if data is None or len(data) < VOL_LOOKBACK + 1:
            return None

        closes = data['close'].tolist()
        returns = []
        for i in range(1, len(closes)):
            if closes[i - 1] > 0:
                r = (closes[i] - closes[i - 1]) / closes[i - 1]
                returns.append(r)

        if len(returns) < VOL_LOOKBACK:
            return None

        mean_r = sum(returns[-VOL_LOOKBACK:]) / VOL_LOOKBACK
        var = sum((r - mean_r) ** 2 for r in returns[-VOL_LOOKUP:]) / (VOL_LOOKBACK - 1)
        vol_annual = math.sqrt(var) * math.sqrt(ANNUAL_FACTOR) * 100  # 年化百分比
        return vol_annual

    except Exception as e:
        return None


def score_stock(symbol, context):
    """对单只股票计算 Smart Beta 综合得分"""
    # 计算两个因子
    div_yield = calc_dividend_yield(symbol, context)
    volatility = calc_volatility(symbol)

    if div_yield is None or volatility is None:
        return None

    # Smart Beta 打分：
    #   红利因子权重 60%（越高越好）
    #   低波因子权重 40%（波动率越低越好，取负值）
    vol_score = -volatility  # 反向波动率
    total_score = div_yield * 0.6 + vol_score * 0.4

    return {
        'symbol': symbol,
        'div_yield': round(div_yield, 2),
        'volatility': round(volatility, 2),
        'score': round(total_score, 2),
    }


# ============================================================
# 策略主逻辑
# ============================================================

def init(context):
    print('=' * 60)
    print('  高红利+低波 Smart Beta 策略启动')
    print(f'  选股池: {INDEX_SYMBOL}(沪深300)')
    print(f'  因子: 红利(TTM,60%) + 低波(40%)')
    print(f'  持仓: TOP {TOP_N} 只等权')
    print(f'  调仓: 季度({REBALANCE_MONTHS})')
    print('=' * 60)

    # 获取成分股列表
    context.stock_pool = get_hs300_symbols(context)

    # 订阅行情（订阅所有成分股的日线）
    subscribe(symbols=','.join(context.stock_pool), frequency=FREQUENCY, count=DATA_COUNT)

    context.last_rebalance_yearmonth = None  # 上次调仓年月 "YYYY-MM"
    context.rebalance_count = 0


def on_bar(context, bars):
    """每根K线触发 — 检查是否为季度调仓日"""
    current_dt = None
    if bars:
        bar0 = bars[0]
        if isinstance(bar0, dict):
            current_dt = bar0.get('datetime') or bar0.get('bob')
        else:
            current_dt = getattr(bar0, 'datetime', None) or getattr(bar0, 'bob', None)

    if current_dt is None:
        return

    date_str = str(current_dt)[:10]  # "YYYY-MM-DD"

    # 提取月份
    try:
        from datetime import datetime
        dt_obj = datetime.strptime(date_str, '%Y-%m-%d')
        month = dt_obj.month
        yearmonth = f'{dt_obj.year}-{dt_obj.month:02d}'
    except:
        return

    # 只在指定月份调仓
    if month not in REBALANCE_MONTHS:
        return

    # 避免同月重复调仓
    if context.last_rebalance_yearmonth == yearmonth:
        return

    _rebalance(context, date_str, yearmonth)


def _rebalance(context, date_str, yearmonth):
    """执行一次季度调仓"""
    context.rebalance_count += 1
    print(f'\n{"="*70}')
    print(f'  📊 第{context.rebalance_count}次调仓 | 日期: {date_str} | 年月: {yearmonth}')
    print(f'{"="*70}')

    pool = context.stock_pool
    print(f'  扫描 {len(pool)} 只股票...')

    # ---- 1. 对每只股票打分 ----
    scores = []
    for i, symbol in enumerate(pool):
        result = score_stock(symbol, context)
        if result and result['score'] is not None:
            scores.append(result)
        # 每50只打一次进度
        if (i + 1) % 50 == 0:
            print(f'    已扫描 {i + 1}/{len(pool)}, 有效评分: {len(scores)}')

    if not scores:
        print('  [WARN] 所有股票都无法计算分数，跳过本次调仓')
        return

    # ---- 2. 排序 ----
    scores.sort(key=lambda x: x['score'], reverse=True)

    # ---- 3. 打印 TOP 20 排行榜 ----
    print(f'\n  {"排名":^4}| {"代码":^14}| {"股息率":^8}| {"年化波":^8}| {"得分":^8}| {"入选":^4}')
    print(f'  {"-"*56}')
    for i, s in enumerate(scores[:20]):
        mark = ' ✅' if i < TOP_N else ''
        print(f'  {i+1:^4}| {s["symbol"]:^14}| {s["div_yield"]:^8.2f}%| {s["volatility"]:^8.2f}%| {s["score"]:^8.2f}{mark}')

    # ---- 4. 选出 TOP N ----
    target_symbols = set(s['symbol'] for s in scores[:TOP_N])
    print(f'\n  🎯 本季持仓 ({TOP_N}只):')
    top_names = []
    for s in scores[:TOP_N]:
        info = f'    {s["symbol"]} | 股息{s["div_yield"]:.2f}% | 波动{s["volatility"]:.2f}%'
        print(info)
        top_names.append(s['symbol'])

    # ---- 5. 获取当前持仓并执行调仓 ----
    all_positions = get_position()
    current_held = set()
    if all_positions:
        for p in all_positions:
            sym = p.get('symbol') if isinstance(p, dict) else (p.symbol if hasattr(p, 'symbol') else None)
            if sym:
                current_held.add(sym)

    # 先卖出不在目标中的持仓
    to_sell = current_held - target_symbols
    if to_sell:
        print(f'\n  🔻 卖出 ({len(to_sell)}只):')
        for sym in to_sell:
            try:
                order_target_volume(sym, 0,
                                    position_side=PositionSide_Long,
                                    order_type=ORDER_TYPE)
                print(f'      卖出 {sym}')
            except Exception as e:
                print(f'      [失败] {sym}: {e}')
    else:
        print(f'\n  无需卖出')

    # 买入/调整目标持仓（等权）
    cash_info = get_cash()
    available = cash_info.available

    if available > 0 and target_symbols:
        per_stock_amount = available / len(target_symbols)
        print(f'  可用资金: {available:,.0f}元, 每只分配: {per_stock_amount:,.0f}元')

        bought = 0
        for sym in target_symbols:
            name = sym
            try:
                # 获取最新价
                price_data = history_n(symbol=sym, frequency='1d', count=1,
                                       fields='close', adjust=ADJUST_PREV, df=True)
                if price_data is None or len(price_data) == 0:
                    continue
                price = price_data['close'].iloc[0]

                volume = int(per_stock_amount / price / 100) * 100
                if volume >= 100:
                    order_target_volume(sym, volume,
                                        position_side=PositionSide_Long,
                                        order_type=ORDER_TYPE)
                    print(f'  🟢 {name} | {volume}股 × {price:.2f}元 ≈ {volume*price:,.0f}元')
                    bought += 1
                elif volume > 0:
                    order_target_volume(sym, 100,
                                        position_side=PositionSide_Long,
                                        order_type=ORDER_TYPE)
                    print(f'  🟡 {name} | 100股 × {price:.2f}元（资金不足，最低买入）')
                    bought += 1
            except Exception as e:
                print(f'  [下单失败] {name}: {e}')

        print(f'  成功买入 {bought}/{len(target_symbols)} 只')

    # ---- 6. 记录调仓状态 ----
    context.last_rebalance_yearmonth = yearmonth

    # 打印账户摘要
    cash_info = get_cash()
    nav = cash_info.nav
    pnl = cash_info.pnl
    fpnl = cash_info.fpnl
    print(f'\n  💰 总资产: {nav:,.0f}元 | 已实现盈亏: {pnl:+,.0f}元 | 浮动盈亏: {fpnl:+,.0f}元')
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
    STRATEGY_ID = os.environ.get('GM_STRATEGY_ID', '') or 'high_dividend_v1'
    START = os.environ.get('GM_BACKTEST_START', BACKTEST_START)
    END = os.environ.get('GM_BACKTEST_END', BACKTEST_END)
    CASH = float(os.environ.get('GM_INITIAL_CASH', str(INITIAL_CASH)))

    mode = MODE_LIVE if MODE.lower() in ('live', 'realtime') else MODE_BACKTEST

    run(
        strategy_id=STRATEGY_ID,
        filename='strategy_high_dividend',
        mode=mode,
        token=TOKEN,
        backtest_start_time=START,
        backtest_end_time=END,
        backtest_initial_cash=CASH,
        backtest_commission_ratio=COMMISSION,
        backtest_slippage_ratio=SLIPPAGE,
        backtest_adjust=ADJUST_PREV,
    )
