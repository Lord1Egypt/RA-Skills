# encoding: utf-8

from mquant_api import *
from mquant_struct import *
import json
import os
import time
import threading


def strategy_params():
    """
    category:事件回调
    brief:策略运行参数定义
    desc: 策略运行参数定义，可选实现。策略可自定义运行参数，启动策略时，会在启动弹框中显示策略自定义的参数，客户在界面修改参数值，修改后的参数会写入到context对象的run_params字段内，客户可在策略程序中通过context对象获取策略运行参数。目前支持int、float、string、list、table、bool类型的参数。

    :return:dict对象，key为参数名，value为一个包含参数默认值、参数描述（选填）的字典
    :remark:可选实现，参数由策略自由填写，由策略平台解析显示在界面上，支持编辑框、下拉列表、勾选框三种形式的参数，后续可根据需求进一步丰富
    :example:
        dict_params = {
       '证券代码':{'value':'601688.SH/000002.SZ','desc':'策略交易的标的代码'},                    #'desc'字段可填写，也可不填写，编辑框类型参数
       '委买价格':{'value':'17.50/27.5'},                                                        #编辑框类型参数
       '委卖价格':{'value':'18.50/28.0'},                                                        #编辑框类型参数
       '补单价格档位':{'value':['最新价','对手方一档','对手方二档','对手方3档','涨停价','跌停价']},  #下拉列表格式参数
       '使用持仓':{'value': True, 'desc':'买入篮子时是否使用持仓中已有的成分券额度'}                #bool类型参数
       '撤单时间间隔':{'value':10}                                                                #编辑框类型参数
       }
        return json.dumps(dict_params)
    """
    pass


def initialize(context):
    cur_date = datetime.datetime.strftime(datetime.datetime.now(), "%Y-%m-%d")  # 检查当日下载交易数据的文件夹是否存在，如果不存在，则创建
    cur_file_dir = 'D:\\MQuantTradeData\\' + cur_date
    if not os.path.exists(cur_file_dir):
        os.mkdir(cur_file_dir)

    g.cur_file_dir = cur_file_dir
    # 判断是否有A股、两融账号，如果有，则重写交易数据文件
    g.fund_account_stock = context.get_fund_account_by_type(AccountType.normal)
    g.fund_account_margin = context.get_fund_account_by_type(AccountType.margin)
    if g.fund_account_stock is None:
        g.fund_account_stock = ''
    if g.fund_account_margin is None:
        g.fund_account_margin = ''
    g.order_custom_field = {}  # 记录客户订单的自定义字段

    g.order_file_stock = cur_file_dir + '\\order_' + g.fund_account_stock + '.csv'
    g.execution_file_stock = cur_file_dir + '\\execution_' + g.fund_account_stock + '.csv'
    g.fund_file_stock = cur_file_dir + '\\fund_' + g.fund_account_stock + '.csv'
    g.position_file_stock = cur_file_dir + '\\position_' + g.fund_account_stock + '.csv'
    g.order_file_margin = cur_file_dir + '\\order_' + g.fund_account_margin + '.csv'
    g.execution_file_margin = cur_file_dir + '\\execution_' + g.fund_account_margin + '.csv'
    g.fund_file_margin = cur_file_dir + '\\fund_' + g.fund_account_margin + '.csv'
    g.position_file_margin = cur_file_dir + '\\position_' + g.fund_account_margin + '.csv'

    if len(g.fund_account_stock) > 0:
        init_trade_files(context, AccountType.normal, g.fund_account_stock, g.order_file_stock, g.execution_file_stock,
                         g.fund_file_stock,
                         g.position_file_stock)

    if len(g.fund_account_margin) > 0:
        init_trade_files(context, AccountType.margin, g.fund_account_margin, g.order_file_margin,
                         g.execution_file_margin, g.fund_file_margin,
                         g.position_file_margin)

    # 注册1s一次的定时函数，定时更新资金和持仓，每次全量更新，记录时间戳
    # run_timely(timer_func, 1)
    g.count = 0


def init_trade_files(context, account_type, fund_account, order_file, execution_file, fund_file, pos_file):
    # 委托
    with open(order_file, 'w') as f:
        f.write('资金账号,委托时间,实例ID,证券代码,买卖方向,委托数量,委托价格,状态,价格类型,柜台委托编号,委托属性,委托类型,成交数量,成交金额,撤单数量,废单原因,订单编号\n')
        ord_list = get_orders(only_this_inst=False, account_type=account_type)  # 仅演示获取普通A股账号的订单信息，可根据自己的实际场景选择获取两融的

        if ord_list is not None:
            ord_list = sorted(ord_list.values(), key=lambda ord: str(ord.add_time) + str(ord.entrust_no))

            for ord in ord_list:
                f.write(get_order_str(ord))
    # 成交
    with open(execution_file, 'w') as f:
        f.write('资金账号,成交时间,实例ID,证券代码,买卖方向,成交价格,成交数量,成交金额,成交类型,柜台委托编号,柜台成交编号,订单编号\n')
        execution_list = get_trades(only_this_inst=False,
                                    account_type=account_type)  # 仅演示获取普通A股账号的订单信息，可根据自己的实际场景选择获取两融的

        if execution_list is not None:
            execution_list = sorted(execution_list.values(),
                                    key=lambda execution: str(execution.time) + str(execution.trade_id))
            for execution in execution_list:
                f.write(get_execution_str(execution))
    # 资金
    with open(fund_file, 'w') as f:
        f.write('记录时间,资金账号,期初资金,可用资金\n')
        context.set_current_account_type(account_type)
        fund_str = '{},{},{},{}\n'.format(datetime.datetime.now(), fund_account, context.portfolio.settled_cash,
                                          context.portfolio.available_cash)
        f.write(fund_str)
    # 持仓
    write_pos_info(context, account_type, pos_file)


def handle_tick(context, tick, msg_type):
    """
    category:事件回调
    brief:TICK行情回调
    desc:TICK行情回调，可选实现。调用subscribe订阅TICK行情后，在此函数中接收实时TICK行情推送。回测模式下，如果选择TICK级回测，回测行情也在此回调函数中接收处理。

    实时行情接收函数
    :param context:
    :param tick: Tick对象
    :param msg_type 消息类型，暂不启用
    :return:
    :remark:可选实现
    """
    pass


def write_fund_info(context, account_type, fund_file):
    with open(fund_file, 'a') as f:
        context.set_current_account_type(account_type)
        fund_account = context.get_fund_account_by_type(account_type)
        fund_str = '{},{},{},{}\n'.format(datetime.datetime.now(), fund_account, context.portfolio.settled_cash,
                                          context.portfolio.available_cash)
        f.write(fund_str)


def write_pos_info(context, account_type, pos_file):
    with open(pos_file, 'w') as f:
        f.write('资金账号,证券代码,当前持仓,可用持仓,期初持仓\n')
        fund_account = context.get_fund_account_by_type(account_type)
        pos_list = get_positions_ex(account_type)
        if pos_list is not None:
            for pos in pos_list:
                pos_str = '{},{},{},{},{}\n'.format(fund_account, pos.security, pos.total_amount, pos.closeable_amount,
                                                    pos.init_amount)
                f.write(pos_str)


def transfer_order_side(side):
    if side == OrderSide.BUY:
        return 1
    elif side == OrderSide.SELL:
        return 2
    else:
        return -1


def transfer_price_type(style):
    if isinstance(style, LimitOrderStyle) or isinstance(style, MarketOrderStyle):
        return style.get_order_style()
    else:
        return 'a'


def get_entrust_price(style):
    if isinstance(style, LimitOrderStyle) or isinstance(style, MarketOrderStyle):
        return style.get_limited_price()
    else:
        return 0


def get_order_str(ord):
    if ord.status is None:
        log.debug(ord.order_id)

    cancel_info = ord.cancel_info.replace(",", ";").replace("\n", "")
    order_info = '{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}\n'.format(ord.fund_account, ord.add_time,
                                                                               ord.inst_id, ord.symbol,
                                                                               transfer_order_side(ord.side),
                                                                               ord.amount,
                                                                               get_entrust_price(ord.style),
                                                                               ord.status.value,
                                                                               transfer_price_type(ord.style),
                                                                               ord.entrust_no, ord.entrust_prop,
                                                                               ord.entrust_type,
                                                                               ord.filled, ord.business_balance,
                                                                               ord.withdraw_amount,
                                                                               cancel_info, ord.order_id)
    return order_info


def get_execution_str(execution):
    '资金账号,成交时间,实例ID,证券代码,买卖方向,成交价格,成交数量,成交金额,成交类型,柜台委托编号,柜台成交编号'
    execution_info = '{},{},{},{},{},{},{},{},{},{},{},{}\n'.format(execution.fund_account, execution.time,
                                                                    execution.inst_id, execution.symbol,
                                                                    transfer_order_side(execution.side),
                                                                    execution.price,
                                                                    execution.amount,
                                                                    execution.business_balance,
                                                                    execution.real_type,
                                                                    execution.entrust_no, execution.trade_id,
                                                                    execution.order_id)
    return execution_info


def write_order_to_csv(ord):
    file_path = g.cur_file_dir + '\\order_' + ord.fund_account + '.csv'
    if not os.path.exists(file_path):
        log.error("订单文件{}不存在，无法更新订单信息".format(file_path))
        return
    with open(file_path, 'a') as f:
        # 字段：资金账号、委托时间、实例ID、证券代码、买卖方向、委托数量、委托价格、价格类型、柜台委托编号、委托属性、委托类型、成交数量、成交金额、撤单数量、状态、废单原因、自定义字段
        f.write(get_order_str(ord))


def write_execution_to_csv(execution):
    # 成交留待客户自行实现
    file_path = g.cur_file_dir + '\\execution_' + execution.fund_account + '.csv'
    if not os.path.exists(file_path):
        log.error("成交文件{}不存在，无法更新订单信息".format(file_path))
        return
    with open(file_path, 'a') as f:
        # 字段：资金账号、委托时间、实例ID、证券代码、买卖方向、委托数量、委托价格、价格类型、柜台委托编号、委托属性、委托类型、成交数量、成交金额、撤单数量、状态、废单原因
        f.write(get_execution_str(execution))


def handle_order_report(context, ord, msg_type):
    """
    category:事件回调
    brief:订单回报函数
    desc:订单回报函数，可选实现。策略报单后，只要订单状态改变，都会进入订单回报函数，策略可以在此函数中判断订单状态并决定后续操作，只要当前策略报单的订单回报会通过此函数通知给策略。回测模式下，订单回报也在此函数中处理。
    订单回报处理函数
    :param ord:Order对象
    :param msg_type 消息类型，透传字段，调用查询接口时传入可获得协程并发
    :return:
    :remark:可选实现
    """
    # print(ord.__dict__)
    write_order_to_csv(ord)


def handle_execution_report(context, execution, msg_type):
    """
    category:事件回调
    brief:成交回报函数
    desc:成交回报函数，可选实现。策略报单后，只要订单产生成交（可能分多笔成交），都会进入成交回报函数，策略可以在此函数中获取本次成交信息（成交价格、数量、金额等），只要当前策略报单的成交回报会通过此函数通知给策略。回测模式下，成交回报也在此函数中处理。
    成交回报
    :param context:
    :param execution:Trade对象
    :param msg_type:
    :return:
    """
    write_execution_to_csv(execution)


def on_fund_update(context, fund_info):
    """
    category:事件回调
    brief:资金推送
    desc:资金推送函数，可选实现。
    :param context:
    :param fund_info: FundUpdateInfo 类对象
    :return:
    """
    fund_account = fund_info.fund_account
    fund_str = '记录时间,资金账号,期初资金,可用资金\n' + '{},{},{},{}\n'.format(datetime.datetime.now(), fund_account,
                                                                context.portfolio.settled_cash,
                                                                context.portfolio.available_cash)
    #    print(fund_info.__dict__, fund_str)
    fund_file = g.cur_file_dir + "\\fund_" + fund_account + ".csv"
    with open(fund_file, 'w', buffering=len(fund_str) + 1) as f:
        f.write(fund_str)


def on_position_update(context, pos_info):
    """
    category:事件回调
    brief:持仓推送
    desc:持仓推送函数，可选实现。
    :param context:
    :param pos_info: Position类对象
    :return:
    """
    #    print('recv pos update:', pos_info.__dict__)
    fund_account = pos_info.fund_account
    pos_file = g.cur_file_dir + "\\position_" + fund_account + ".csv"
    pos_str = '资金账号,证券代码,当前持仓,可用持仓,期初持仓\n'

    if fund_account.startswith('9'):
        account_type = AccountType.margin
    else:
        account_type = AccountType.normal

    pos_list = get_positions_ex(account_type)
    if pos_list is not None:
        for pos in pos_list:
            pos_str = pos_str + (
                '{},{},{},{},{}\n'.format(fund_account, pos.security, pos.total_amount, pos.closeable_amount,
                                          pos.init_amount))

    with open(pos_file, 'w', buffering=len(pos_str) + 1) as f:
        f.write(pos_str)


def on_strategy_end(context):
    """
    category:事件回调
    brief:策略结束回调
    desc:策略结束回调，可选实现。策略实例终止时，MQuant会调用此回调函数通知策略进行一些数据保存、环境清理等工作，待策略的处理工作结束后再结束策略进程。特别注意，如果直接关闭策略进程，可能导致此函数未执行完毕进程就已经关闭，建议通过策略执行监控界面或者通过stop_strategy API终止策略。
    策略结束时调用，用户可以在此函数中进行一些汇总分析、环境清理等工作
    :param context:
    :return:
    :remark:可选实现
    """
    pass
