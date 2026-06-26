# -*- coding: utf-8 -*-
# 基础策略模板 - 适用于聚宽平台

from jqdata import *

def initialize(context):
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
                  type='stock')
    
    # 设置滑点
    set_slippage(PriceRelatedSlippage(0.00246))
    
    # 初始化全局变量
    g.security = '000001.XSHE'
    
    # 设置定时任务
    run_daily(market_open, time='9:30')

def market_open(context):
    """
    每日开盘运行函数
    """
    # 获取数据
    df = attribute_history(g.security, 20, '1d', ['close'])
    
    # 计算指标
    ma5 = df['close'].mean()
    current_price = get_current_data()[g.security].last_price
    
    # 交易逻辑
    if current_price > ma5 * 1.01:
        order_value(g.security, context.portfolio.available_cash)
        log.info(f"买入 {g.security}")
    elif current_price < ma5 * 0.99:
        order_target(g.security, 0)
        log.info(f"卖出 {g.security}")
