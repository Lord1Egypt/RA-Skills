# -*- coding: utf-8 -*-
# 动量ETF策略 - 基于聚宽平台

from jqdata import *

class MomentumETFStrategy:
    def __init__(self):
        """初始化策略参数"""
        # ETF池
        self.etf_list = [
            '510050.XSHG',  # 上证50ETF
            '510300.XSHG',  # 沪深300ETF
            '510500.XSHG',  # 中证500ETF
            '510880.XSHG',  # 红利ETF
            '512880.XSHG',  # 银行ETF
            '512660.XSHG',  # 券商ETF
            '512400.XSHG',  # 有色金属ETF
            '512200.XSHG',  # 医药ETF
            '512100.XSHG',  # 中证1000ETF
            '512000.XSHG'   # 计算机ETF
        ]
        # 策略参数
        self.initial_cash = 1000000  # 初始资金
        self.rebalance_period = 21  # 调仓周期（21个交易日，约1个月）
        self.lookback_period = 63  # 动量计算周期（63个交易日，约3个月）
        self.top_n = 3  # 选择表现最好的前3个ETF
    
    def initialize(self, context):
        """
        初始化函数，整个策略生命周期只执行一次
        """
        # 设置基准
        set_benchmark('000300.XSHG')
        # 开启动态复权
        set_option('use_real_price', True)
        # 设置手续费
        set_order_cost(OrderCost(open_tax=0, close_tax=0.001,
                                 open_commission=0.0003, close_commission=0.0003,
                                 close_today_commission=0, min_commission=5), 
                      type='fund')
        
        # 初始化策略参数
        context.etf_list = self.etf_list
        context.initial_cash = self.initial_cash
        context.rebalance_period = self.rebalance_period
        context.lookback_period = self.lookback_period
        context.top_n = self.top_n
        context.trade_count = 0
        
        # 设置定时任务
        run_daily(self.handle_daily, time='9:30')
        
        # 输出日志
        log.info('动量ETF策略初始化完成')
    
    def handle_daily(self, context):
        """
        每日交易逻辑
        """
        context.trade_count += 1
        
        # 达到调仓周期时进行调仓
        if context.trade_count % context.rebalance_period == 0:
            self.rebalance(context)
    
    def rebalance(self, context):
        """
        调仓逻辑：选择动量最强的ETF进行配置
        """
        # 计算每个ETF的动量
        etf_momentum = {}
        for etf in context.etf_list:
            # 使用聚宽特有函数获取历史数据
            df = attribute_history(etf, context.lookback_period, '1d', ['close'])
            if len(df) >= context.lookback_period:
                # 计算动量（收益率）
                momentum = (df['close'][-1] - df['close'][0]) / df['close'][0]
                etf_momentum[etf] = momentum
        
        # 按动量排序，选择表现最好的前N个ETF
        if etf_momentum:
            sorted_etfs = sorted(etf_momentum.items(), key=lambda x: x[1], reverse=True)
            selected_etfs = [item[0] for item in sorted_etfs[:context.top_n]]
            
            # 卖出不在选择列表中的ETF
            for etf in list(context.portfolio.positions.keys()):
                if etf not in selected_etfs:
                    order_target(etf, 0)
                    log.info(f'卖出 {etf}')
            
            # 等权买入选择的ETF
            cash_per_etf = context.portfolio.available_cash / len(selected_etfs)
            for etf in selected_etfs:
                # 检查ETF是否可交易
                current_data = get_current_data()
                if etf in current_data and not current_data[etf].paused:
                    order_value(etf, cash_per_etf)
                    log.info(f'买入 {etf}，金额 {cash_per_etf}，动量 {etf_momentum[etf]:.2%}')
    
    def on_strategy_end(self, context):
        """
        策略结束时执行
        """
        # 计算策略收益
        total_returns = (context.portfolio.total_value - context.initial_cash) / context.initial_cash
        log.info(f'动量ETF策略结束，总收益：{total_returns:.2%}')

# 策略入口
if __name__ == '__main__':
    # 创建策略实例
    strategy = MomentumETFStrategy()
    
    # 运行策略
    run_strategy(
        initialize=strategy.initialize,
        handle_data=strategy.handle_daily,
        start_date='2020-01-01',
        end_date='2023-12-31',
        capital_base=strategy.initial_cash,
        frequency='daily'
    )
