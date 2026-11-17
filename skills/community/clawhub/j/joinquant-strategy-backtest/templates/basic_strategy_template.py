"""
聚宽策略基础模板
适用场景：等权调仓策略，可作为新策略的起点

使用方法：
1. 复制此文件到聚宽策略编辑器
2. 修改 g.stock_pool 来源（指数成分股/自定义列表/多因子筛选）
3. 修改 g.position_ratio 控制仓位
4. 修改 rebalance 函数中的调仓逻辑
"""

# ===== 策略参数 =====
# 在 initialize 中设置的全局变量

def initialize(context):
    """策略初始化 — 回测开始时调用一次"""
    # --- 回测配置 ---
    set_benchmark('000300.XSHG')          # 基准：沪深300
    set_commission(PerTrade(
        buy_cost=0.0003,                   # 买入佣金万3
        sell_cost=0.0013,                  # 卖出佣金万3+印花税千1
        min_cost=5                          # 最低佣金5元
    ))
    set_slippage(FixedSlippage(0.02))      # 固定滑点2分
    set_option('use_real_price', True)     # 使用真实价格
    set_option('avoid_future_data', True)  # 避免未来数据

    # --- 全局变量 ---
    g.stock_pool = []                      # 股票池
    g.position_ratio = 0.8                 # 目标总仓位（占总资产）
    g.rebalance_day = 5                    # 每月调仓日（第N个交易日）
    g.day_count = 0                        # 交易日计数器

    # --- 定时任务 ---
    run_daily(before_market_open, time='before_open')   # 盘前：更新股票池
    run_daily(market_open, time='09:30')                 # 开盘：执行交易
    run_daily(after_market_close, time='after_close')    # 盘后：记录日志

    log.info('=== 策略初始化完成 ===')


def before_market_open(context):
    """盘前准备 — 每个交易日开盘前调用"""
    # 更新股票池：取沪深300成分股
    g.stock_pool = get_index_stocks('000300.XSHG')

    # 过滤停牌股票
    current_data = get_current_data()
    g.stock_pool = [s for s in g.stock_pool if not current_data[s].paused]

    g.day_count += 1
    log.info(f'第{g.day_count}个交易日 | 股票池: {len(g.stock_pool)}只 | 可用资金: {context.portfolio.available_cash:.0f}')


def market_open(context):
    """开盘交易 — 每月第N个交易日调仓"""
    # 判断是否为调仓日
    if g.day_count % 20 != g.rebalance_day % 20:  # 简化：每20个交易日调仓
        return

    log.info('>>> 开始调仓 <<<')

    # Step 1: 清仓不在股票池中的持仓
    for stock in list(context.portfolio.positions.keys()):
        if stock not in g.stock_pool:
            order_target(stock, 0)
            log.info(f'清仓: {stock}')

    # Step 2: 等权配置股票池中的股票
    if g.stock_pool:
        weight = g.position_ratio / len(g.stock_pool)
        for stock in g.stock_pool:
            # 跳过停牌
            current_data = get_current_data()
            if current_data[stock].paused:
                continue
            order_target_percent(stock, weight)

    log.info(f'>>> 调仓完成 | 持仓{len(context.portfolio.positions)}只 <<<')


def after_market_close(context):
    """盘后记录 — 每个交易日收盘后调用"""
    total_value = context.portfolio.total_value
    returns = context.portfolio.returns
    positions_count = len(context.portfolio.positions)

    log.info(
        f'日终 | 总资产: {total_value:.0f} | '
        f'累计收益: {returns*100:.2f}% | '
        f'持仓数: {positions_count}'
    )
