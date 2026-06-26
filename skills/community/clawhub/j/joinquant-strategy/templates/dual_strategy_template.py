# -*- coding: utf-8 -*-
# 双策略模板 - 支持多子账户管理

from jqdata import *

def initialize(context):
    """
    初始化函数
    """
    # 基础设置
    set_benchmark('000300.XSHG')
    set_option('use_real_price', True)
    
    # 设置多子账户
    g.strategy1_proportion = 0.5  # 策略1资金比例
    g.strategy2_proportion = 0.5  # 策略2资金比例
    
    subportfolios = [
        SubPortfolioConfig(context.portfolio.starting_cash * g.strategy1_proportion, 'stock'),
        SubPortfolioConfig(context.portfolio.starting_cash * g.strategy2_proportion, 'stock'),
    ]
    set_subportfolios(subportfolios)
    
    # 初始化策略
    _init_strategies(context)
    
    # 设置定时任务
    run_daily(strategy1_trade, time='10:00')
    run_daily(strategy2_trade, time='10:30')
    run_daily(after_market_close, time='15:30')

def _init_strategies(context):
    """
    初始化策略对象
    """
    g.strategies = {
        'strategy1': BaseStrategy(context, 0, '策略1'),
        'strategy2': BaseStrategy(context, 1, '策略2')
    }

class BaseStrategy:
    """策略基类"""
    def __init__(self, context, subportfolio_index, name):
        self.subportfolio_index = subportfolio_index
        self.name = name
        self.initial_cash = context.portfolio.subportfolios[subportfolio_index].total_value
        
    def order_target_value(self, context, security, target_value):
        """封装下单函数"""
        return order_target_value_send(context, self.subportfolio_index, 
                                       security, target_value)
    
    def after_market_close(self, context):
        """收盘后处理"""
        sub = context.portfolio.subportfolios[self.subportfolio_index]
        ret = (sub.total_value / self.initial_cash - 1) * 100
        record(**{self.name + '收益率': ret})

def strategy1_trade(context):
    """
    策略1交易逻辑
    """
    strategy = g.strategies['strategy1']
    # 策略1逻辑：动量策略
    stocks = ['600000.XSHG', '600519.XSHG']
    for stock in stocks:
        df = attribute_history(stock, 20, '1d', ['close'])
        if len(df) >= 20:
            returns = (df['close'][-1] - df['close'][0]) / df['close'][0]
            if returns > 0.05:
                sub = context.portfolio.subportfolios[0]
                strategy.order_target_value(context, stock, sub.available_cash)
                log.info(f'策略1买入 {stock}')

def strategy2_trade(context):
    """
    策略2交易逻辑
    """
    strategy = g.strategies['strategy2']
    # 策略2逻辑：均值回归策略
    stocks = ['000001.XSHE', '000858.XSHE']
    for stock in stocks:
        df = attribute_history(stock, 60, '1d', ['close'])
        if len(df) >= 60:
            returns = (df['close'][-1] - df['close'][0]) / df['close'][0]
            if returns < -0.1:
                sub = context.portfolio.subportfolios[1]
                strategy.order_target_value(context, stock, sub.available_cash)
                log.info(f'策略2买入 {stock}')

def after_market_close(context):
    """
    收盘后处理
    """
    for strategy in g.strategies.values():
        strategy.after_market_close(context)
