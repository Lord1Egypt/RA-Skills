# ETF轮动策略模板

from jqdata import *

class ETFRotationStrategy:
    def __init__(self):
        # 策略参数
        self.etf_list = []  # ETF列表
        self.initial_cash = 1000000  # 初始资金
        self.trade_date = None  # 交易日期
        self.rebalance_period = 20  # 调仓周期（天）
        self.lookback_days = 60  # 回看天数
    
    def initialize(self, context):
        """初始化策略"""
        context.etf_list = self.etf_list
        context.initial_cash = self.initial_cash
        context.rebalance_period = self.rebalance_period
        context.lookback_days = self.lookback_days
        context.trade_count = 0  # 交易计数
        
        # 设置交易频率
        run_daily(self.handle_daily, time='9:30')
        
        # 输出日志
        log.info('ETF轮动策略初始化完成')
    
    def handle_daily(self, context):
        """每日交易逻辑"""
        context.trade_count += 1
        self.trade_date = context.current_dt
        
        # 达到调仓周期时进行调仓
        if context.trade_count % context.rebalance_period == 0:
            self.rebalance(context)
    
    def rebalance(self, context):
        """调仓逻辑"""
        # 计算每个ETF的收益率
        etf_returns = {}
        for etf in context.etf_list:
            # 获取历史数据
            df = get_price(etf, end_date=context.current_dt, count=context.lookback_days, frequency='daily')
            if len(df) < context.lookback_days:
                continue
            
            # 计算收益率
            returns = (df['close'][-1] - df['close'][0]) / df['close'][0]
            etf_returns[etf] = returns
        
        # 按收益率排序，选择表现最好的ETF
        if etf_returns:
            sorted_etfs = sorted(etf_returns.items(), key=lambda x: x[1], reverse=True)
            top_etf = sorted_etfs[0][0]
            
            # 卖出所有持仓
            for stock in list(context.portfolio.positions.keys()):
                order_target(stock, 0)
                log.info(f'卖出 {stock}')
            
            # 买入表现最好的ETF
            cash = context.portfolio.available_cash
            price = get_current_data()[top_etf].last_price
            if cash > 0 and price > 0:
                amount = int(cash / price)
                if amount > 0:
                    order(top_etf, amount)
                    log.info(f'买入 {top_etf}，数量 {amount}，收益率 {etf_returns[top_etf]:.2%}')
    
    def on_strategy_end(self, context):
        """策略结束时执行"""
        # 计算策略收益
        total_returns = (context.portfolio.total_value - context.initial_cash) / context.initial_cash
        log.info(f'ETF轮动策略结束，总收益：{total_returns:.2%}')

# 策略入口
if __name__ == '__main__':
    # 示例用法
    strategy = ETFRotationStrategy()
    # 可以在这里设置策略参数
    strategy.etf_list = ['510050.XSHG', '510300.XSHG', '510500.XSHG']  # 示例ETF
    
    # 运行策略
    run_strategy(
        initialize=strategy.initialize,
        handle_data=strategy.handle_daily,
        start_date='2020-01-01',
        end_date='2020-12-31',
        capital_base=strategy.initial_cash,
        frequency='daily'
    )
