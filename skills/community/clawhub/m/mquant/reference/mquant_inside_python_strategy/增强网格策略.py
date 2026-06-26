# encoding: utf-8
"""
@project = 内置策略
@file = 增强网格策略
@author = 011048
@create_time = 2019/11/1 10:11
"""

from mquant_api import *
from mquant_struct import *


def strategy_params():
    """
    策略可自定义运行参数，启动策略时会写入到context对象的run_params字段内
    :return:dict对象，key为参数名，value为一个包含参数默认值、参数描述（选填）的字典
    :remark:可选实现，参数由策略自由填写，自己解析
    :example:
    """
    dict_params = {
        '交易标的': {'value': '601688.SH/000002.SZ', 'desc': '策略交易的标的代码'},  # 'desc'字段可填写，也可不填写
        '基准价格': {'value': '17.50/26.70'},
        '单次买入数量': {'value': '500/500'},
        '单次卖出数量': {'value': '500/500'},
        '卖出监控涨幅': {'value': '0.06/0.06'},
        '卖出回落幅度': {'value': '0.01/0.01'},
        '买入监控跌幅': {'value': '0.06/0.06'},
        '买入上冲跌幅': {'value': '0.01/0.01'},
        '买入之前允许卖出': {'value': True}
    }
    return json.dumps(dict_params)


def initialize(context):
    """
    初始化函数
    :param context:
    :return:
    """

    # 记录参数
#    print(context.run_params)
    g.symbol_list = context.run_params['交易标的'].strip('/').split('/')
    g.baseline_price = context.run_params['基准价格'].strip('/').split('/')
    g.sell_monitor_range = context.run_params['卖出监控涨幅'].strip('/').split('/')
    g.sell_fall_range = context.run_params['卖出回落幅度'].strip('/').split('/')
    g.buy_monitor_range = context.run_params['买入监控跌幅'].strip('/').split('/')
    g.buy_rise_range = context.run_params['买入上冲跌幅'].strip('/').split('/')
    g.buy_qty_per = context.run_params['单次买入数量'].strip('/').split('/')
    g.sell_qty_per = context.run_params['单次卖出数量'].strip('/').split('/')
    g.sell_monitor_flag = {}
    g.buy_monitor_flag = {}
    # 达到监控涨跌幅后记录本次冲高或下探的最高/最低价格，每次收到新的tick，判断相比最高/最低价格是否回落/上升了指定幅度
    g.sell_range_highest_price = {}
    g.buy_range_lowest_price = {}
    for symbol in g.symbol_list:
        # 记录是否已经达到监控涨跌幅
        g.sell_monitor_flag[symbol] = False
        g.buy_monitor_flag[symbol] = False
        # 达到监控涨跌幅后记录本次冲高或下探的最高/最低价格，每次收到新的tick，判断相比最高/最低价格是否回落/上升了指定幅度
        g.sell_range_highest_price[symbol] = 0
        g.buy_range_lowest_price[symbol] = 0

    g.sell_flag = bool(int(context.run_params['买入之前允许卖出']))

    # 订阅股票行情
    subscribe(g.symbol_list)


def handle_tick(context, tick, msg_type):
    """
    行情处理函数，如果需要更快的行情，可以对接逐笔成交数据
    :param context:
    :param tick:
    :param msg_type:
    :return:
    """
    if tick.code not in g.symbol_list:
        print('收到非法行情数据:', tick.code)
    index = g.symbol_list.index(tick.code)
#    print(index, tick.code)
    
    baseline_price = float(g.baseline_price[index])
    # 记录最高最低价，报单之后需要将标的的最高最低价重置为基准价
    # g.buy_range_lowest_price[tick.code] = max(g.buy_range_lowest_price[tick.code], tick.current)
    # 如果价格在基准价上方，执行卖出逻辑
    if tick.current > baseline_price:
        if g.sell_flag:
            sell_func(context, tick, index, baseline_price)
    # 如果价格在基准价上方，执行买入逻辑
    else:
        buy_func(context, tick, index, baseline_price)


def buy_func(context, tick, index, baseline_price):
    """
    买入逻辑
    :param baseline_price:
    :param context:
    :param tick:
    :param index:
    :return:
    """
    buy_monitor_range = float(g.buy_monitor_range[index])
    
    log.info(str.format('当前价格[{}]在基准价[{}]下方，判断是否触及下跌监控线：[{}]', tick.current, baseline_price, buy_monitor_range))
    if not g.buy_monitor_flag[tick.code]:
        fall_range = (baseline_price - tick.current) / tick.pre_close
        if fall_range >= buy_monitor_range:
            log.info(str.format('当前价格[{}]触及下跌监控线：[{}],开始监控', tick.current, buy_monitor_range))
            g.buy_monitor_flag[tick.code] = True
            g.buy_range_lowest_price[tick.code] = min(g.buy_range_lowest_price[tick.code], tick.current)
        else:
            return
    else:
        # 已经处于监控中，判断是否满足报单条件
        if g.buy_range_lowest_price[tick.code] > tick.current:  # 还在下跌
            g.buy_range_lowest_price[tick.code] = tick.current
        else:
            rise_range = (tick.current - g.buy_range_lowest_price[tick.code]) / tick.pre_close
            if str(rise_range) >= g.buy_rise_range[index]:  # 满足买入报单条件
                log.info(str.format('满足买入报单条件，标的[{}]，当前价格[{}]，区间最低价格[{}]，昨收盘价[{}]', tick.code, tick.current,
                                    g.buy_range_lowest_price[tick.code], tick.pre_close))
                buy_qty = int(g.buy_qty_per[index])
                price = round(tick.a1_p, 2)
                g.baseline_price[index] = price
                # 判断资金是否足够，如果不够，不买入，但是基准价设置为预期报单价
                available_cash = context.portfolio.available_cash
                if available_cash < buy_qty * price:
                    log.warn(str.format('标的[{}]可用资金[{}]不足，不买入，基准价调整为报单价格[{}]', tick.code, available_cash, g.baseline_price[index]))
                    return

                log.info(str.format('买入报单，标的：[{}], 价格:[{}]，数量：[{}]', tick.code, price, buy_qty))
                order(tick.code, buy_qty, LimitOrderStyle(price))
                g.sell_flag = True


def sell_func(context, tick, index, baseline_price):
    """
    卖出逻辑
    :param baseline_price:
    :param index:
    :param context:
    :param tick:
    :return:
    """
    sell_monitor_range = float(g.sell_monitor_range[index])
#    print(g.sell_monitor_range,index)
    log.info(str.format('当前价格[{}]在基准价[{}]上方，判断是否触及上涨监控线：[{}]', tick.current, baseline_price, sell_monitor_range))
    if not g.sell_monitor_flag[tick.code]:
        rise_range = (tick.current - baseline_price) / tick.pre_close
        if rise_range >= sell_monitor_range:
            log.info(str.format('当前价格[{}]触及上涨监控线：[{}],开始监控', tick.current, sell_monitor_range))
            g.sell_monitor_flag[tick.code] = True
            g.sell_range_highest_price[tick.code] = max(g.sell_range_highest_price[tick.code], tick.current)
        else:
            return
    else:
        # 已经处于监控中，判断是否满足报单条件
        if g.sell_range_highest_price[tick.code] < tick.current:  # 还在上涨
            g.sell_range_highest_price[tick.code] = tick.current
        else:
            fall_range = (g.sell_range_highest_price[tick.code] - tick.current) / tick.pre_close
            if str(fall_range) >= g.sell_fall_range[index]:  # 满足卖出报单条件
                log.info(str.format('满足卖出报单条件，标的[{}]，当前价格[{}]，区间最高价格[{}]，昨收盘价[{}]', tick.code, tick.current,
                                    g.sell_range_highest_price[tick.code], tick.pre_close))
                sell_qty = int(g.sell_qty_per[index])
                g.baseline_price[index] = round(tick.b1_p, 2)
                # 判断持仓是否可用，如果不可用，将g.sell_flag设置为false，并返回
                pos = context.portfolio.positions[tick.code]
                if pos is None:
                    log.warn(str.format('标的[{}]可卖持仓[{}]不足，不卖出，基准价调整为报单价格[{}]', tick.code, 0, g.baseline_price[index]))
                    return
                elif pos.closeable_amount < sell_qty:
                    log.warn(str.format('标的[{}]可卖持仓[{}]不足，不卖出，基准价调整为报单价格[{}]', tick.code, pos.closeable_amount,
                                        g.baseline_price[index]))
                    return
                log.info(str.format('卖出报单，标的：[{}], 价格:[{}]，数量：[{}]', tick.code, round(tick.b1_p, 2), sell_qty))
                order(tick.code, -1 * sell_qty, LimitOrderStyle(round(tick.b1_p, 2)))
