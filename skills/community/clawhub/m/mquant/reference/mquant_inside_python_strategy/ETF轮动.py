# encoding: utf-8
"""
策略描述

ETF套利原理：
ETF基金一级市场预估IOPV和二级市场价格存在价差
IOPV > 二级市场价格，折价套利：二级市场买入etf基金，一级市场赎回成分券，二级市场卖出成分券
IOPV < 二级市场价格，溢价套利：二级市场买入成分券，一级市场申购etf基金，二级市场卖出etf基金

瞬时套利策略逻辑：
1、订阅ETF一级市场IOPV，每次收到推送后用全局变量记录
2、订阅ETF二级市场价格，每次收到推送，比较IOPV和基金价格，若存在套利空间，则实行套利操作，否则直接返回
3、IOPV > 二级市场价格（折价套利）：执行折价套利step1，买入指定数量的etf基金
                                  将下单信息以 order_id：order 的形式存入order_dict
                                  记录当前执行步骤
    IOPV < 二级市场价格（溢价套利）：执行溢价套利step1，买入一篮子成分券
                                  每只成分券的下单信息均以 order_id：order 的形式存入order_dict
                                  记录当前执行步骤
4、接收订单回报信息，更新订单状态，若订单为成交、部撤、或已撤状态，则从order_id中删除这条订单，

    # 判断order_id是否为空，不为空表示有订单尚未完全成交，直接返回
    #                      为空则说明所有订单均已成交，根据当前执行步骤，选择执行下一步
    折价套利step2，赎回成分券，将下单信息存入order_dict，记录当前执行步骤，返回
    折价套利step3，赎回成分券，将下单信息存入order_dict，记录当前执行步骤，返回
    溢价套利step2，申购成分券，将下单信息存入order_dict，记录当前执行步骤，返回
    溢价套利step2，申购成分券，将下单信息存入order_dict，记录当前执行步骤，返回

5、定时撤单补单
    每个订单记录报单本机时间，订阅1s的定时信号，每次接收到定时信号则检查当前系统时间与订单时间的间隔，如果超过用户设定的定时撤单时间间隔（默认12s）则撤单
    为了提高效率，策略中将订单时间表顺序排列，每次从前向后取订单，取到第一条不满足撤单条件的订单为止
    撤单完成后，按照用户指定的价格档位进行补单操作（用户可以在参数中设置撤单立即补单，这样策略将不会等待撤单成交就会立即补单，此时可能会存在超单的风险）

    # 定时回调函数中，首先判断当前步骤，如果处于申购或赎回阶段，直接返回（申赎不能撤单）
    #                 若 cancel_order_list 为空，认为所有订单均未超时，直接返回
    #                 否则，*遍历 cancel_order_list，订单若同时存在于 cancel_order_list 和 order_dict，认为订单超时，根据当前步骤进行撤单和补单，补单的订单信息存入order_dict
    #                 将 order_dict 中所有订单id更新至 cancel_order_list
    #                 * 此处逻辑为 下单后至少15s还未成交，才执行撤单补单操作，由于下单时间随机，需要订单两次出现在order_dict中才认为订单超时，所以需要维护 cancel_order_list
"""

from mquant_api import *
from mquant_struct import *
import json
import datetime


def timer_func(conetxt, interval, msg_type):
    """
    示例定时函数
    1、interval == 6，定时发送行情假数据（用于测试）
    2、若当前套利步骤g.arbitrage_type为基金申赎，不能撤回，直接返回
    3、若当前套利步骤g.arbitrage_type为补单，直接返回（一个订单只执行一次撤补操作，补单的订单用市价下单，不再补单）
    3、g.cancel_order_list不为空，依次撤单补单，补单信息存入order_dict列表
    4、更新g.cancel_order_list
    :param conetxt:
    :return:
    :remark:用户函数
    """
    cancel_and_rebuild_orders()


def strategy_params():
    """
    策略可自定义运行参数，启动策略时会写入到context对象的run_params字段内
    :return:dict对象，key为参数名，value为一个包含参数默认值、参数描述（选填）的字典
    :remark:可选实现
    """
    # 示例如下：
    dict_params = {
        'ETF基金代码': {'value': '510050.SH', 'desc': '交易标的'},  # 'desc'字段可填写，也可不填写
        #        'ETF基金代码': {'value': '159901.SZ', 'desc': '交易标的'},  # 'desc'字段可填写，也可不填写
        '报单价格档位': {'value':['最新价', '对手方一档', '对手方二档', '对手方三档', '涨/跌停价']},
        '补单价格档位': {'value': ['最新价', '对手方一档', '对手方二档', '对手方三档', '涨/跌停价']},
        '套利预估金额': {'value': '1000'},  # 超过该金额，则进行套利操作
        '交易单位份数': {'value': 1, 'desc': '如50ETF，一个交易单位是900000份基金'},
        '撤单时间间隔': {'value': 10},
        '使用持仓':{'value': True, 'desc':'买入篮子时是否使用持仓中已有的成分券额度'}
    }
    return json.dumps(dict_params)


def initialize(context):
    """
    策略初始化，启动策略时调用，用户可在初始化函数中订阅行情、设置标的、设置定时处理函数等
    该函数中允许读取文件，除此之外的其他函数禁止读取文件
    1、订阅二级市场基金价格和ETF预估IOPV
    2、设置定时器定时撤单补单
    :param context:
    :return:
    :remark:必须实现
    """
    # 查询获取ETF基础信息及成分券信息
    print('参数信息', context.run_params)
    etfFundSymbol = context.run_params['ETF基金代码'].strip('/')
    g.etfHandler = HtEtfHandler(etfFundSymbol)
    g.etfInfo = g.etfHandler.getEtfInfo()
    if g.etfInfo.etf_fund_symbol != etfFundSymbol:
        log.error('获取ETF基础信息失败，ETF基金代码:%s' % etfFundSymbol)
        return

    g.etfConstituentInfoList = g.etfHandler.getEtfConstituentList()
    if len(g.etfConstituentInfoList) == 0:
        log.error('获取ETF成分券信息失败，ETF基金代码:%s' % etfFundSymbol)
        return

    g.etfConstituentSymbols = g.etfHandler.getEtfConstituentSymbols()
    print(g.etfConstituentSymbols)

    g.amount = int(context.run_params['交易单位份数'])
    g.symbol = etfFundSymbol
    g.arbitrage_estimate_amount = float(context.run_params['套利预估金额'])
    g.cancel_time_interval = int(context.run_params['撤单时间间隔'])
    g.rebuild_order_level = context.run_params['补单价格档位']
    g.order_level = context.run_params['报单价格档位']
    print('补单价格挡位：',g.rebuild_order_level)
    g.use_position = bool(int(context.run_params['使用持仓']))
    print('使用持仓', g.use_position)

    g.ETF_IOPV = 0  # ETF一级市场预估IOPV
    g.current_price = 0  # ETF二级市场价格
    g.arbitrage_type = ''  # 当前套利类型和执行步骤记录

    g.order_dict = {}  # 存放未完成订单列表
    log.debug('订阅ETF基金二级市场实时行情')
    subscribe(etfFundSymbol)  # 订阅ETF基金二级市场实时行情
    log.debug('订阅ETF基金一级市场预估信息')
    subscribe(etfFundSymbol, 'etf_estimate_info')  # 订阅ETF基金一级市场预估信息
    # g.cancel_order_list = []  # 存放上一次调用定时回调函数时，未完成的订单
    run_timely(timer_func, 1)  # 注册一个定时函数，用于判断超时订单，撤单精度设置为1s，每1s检查一次订单是否应该撤回并补单
    # run_timely(timer_func, 6)  # 测试使用，定时调用行情推送接口
    # print('fund account', context.get_fund_account_by_type('stock'))


def handle_order_report(context, ord, msg_type):
    """
    订单回报处理函数，非必填
    接收订单回报，如果订单为已成、部撤、已撤或废单，从order_list中移除，订单为废单，应该提示用户，由用户确定是否补单

    判断order_dict是否为空，不为空则直接返回，为空则根据标识，继续执行套利操作的下一步
        折价套利step2，赎回成分券，将下单信息存入order_list，记录当前执行步骤，返回
        折价套利step3，卖出成分券
        溢价套利step2，申购基金，将基金的订单信息存储在order_list中，记录当前执行步骤，返回
        溢价套利step3，卖出基金
    :param ord:Order对象
    :return:
    """
    #判断是否为申赎成交，如果是，则进行下一步
    print('handle_order_report', ord.symbol, ord.status, ord.entrust_prop)
    if ord.entrust_prop == 'N' and ord.status == OrderStatus.held:
        if ord.side == 'long':
            g.arbitrage_type='premium_step2'
        elif ord.side == 'short':
            g.arbitrage_type = 'discount_step2'
    # 判断如果g.order_dict为空，则进行下一步操作
        check_and_excute_next_step()
        return
    
    if len(g.order_dict) == 0:
        return
    #
#    
    if g.order_dict.get(ord.order_id) is not None:
        if ord.status == OrderStatus.held or ord.status == OrderStatus.canceled or ord.status == OrderStatus.rejected or ord.status == OrderStatus.pending_cancel:
            g.order_dict.pop(ord.order_id)
        elif ord.status == OrderStatus.filled:
            g.order_dict[ord.order_id].filled = ord.filled
    check_and_excute_next_step()


def get_order_price(symbol, order_side, order_level):
    """
    获取补单价格
    :param order_side:
    :param symbol:
    :return:
    """
    tickData = get_current_tick(symbol)
    # print('从行情中获取订单价格', tickData.code, tickData.close, tickData.current, tickData.a1_p)
    if tickData.code == symbol:
        print('获取到行情，按照指定价格档位下单，symbol:',symbol)
        if order_level == '最新价':
            if tickData.current > 0:
                # print('获取到订单价格', tickData.current)
                return tickData.current
            else:
                # print('获取到订单价格', tickData.close)
                return tickData.close
            
        elif order_level == '对手方一档':
            if order_side == 'long':
                return tickData.a1_p
            else:
                return tickData.b1_p
        elif order_level == '对手方二档':
            if order_side == 'long':
                return tickData.a2_p
            else:
                return tickData.b2_p
        elif order_level == '对手方三档':
            if order_side == 'long':
                return tickData.a3_p
            else:
                return tickData.b3_p
        elif order_level == '涨/跌停价':
            if order_side == 'long':
                return tickData.high_limit  # 以涨停价买
            else:
                return tickData.low_limit  # 以跌停价卖
    else:
        # 如果没取到行情，按照涨停价下单
        print('未获取到行情，按照涨/跌停价格下单, symbol:', symbol)
        eftConstituentInfo = g.etfHandler.getEftConstituentInfo(symbol)
        if eftConstituentInfo is not None:
            if order_side == 'long':
                print('订单价格：', eftConstituentInfo.high_limit_px)
                return eftConstituentInfo.high_limit_px  # 以涨停价买
            else:
                print('订单价格：', eftConstituentInfo.low_limit_px)
                return eftConstituentInfo.low_limit_px  # 以跌停价卖
        else:
            print('未获取到订单价格，代码', symbol)
            return 1.0


def cancel_and_rebuild_orders():
    """
    撤单补单函数，由定时器驱动，精度为1s
    由于python本身的dict不排序，g.order_dict中的订单顺序是按照时间顺序排列的，因此从前向后遍历订单，找到第一个不满足撤单条件的订单即可不在查找
    :return:
    """
    # 为了提高性能，此处不等待撤单成交，直接进行补单操作，可能导致超单现象
    lstCancelOrders = []
    lstOrders = []
    for item in g.order_dict.values():
        #如果是已报待撤和部成待撤状态的订单，不再做撤补操作
        if item.status == OrderStatus.pending_cancel:
            continue
        if (datetime.datetime.now() - item.create_time).seconds < g.cancel_time_interval:
            break
            
        print('对订单[%s]进行撤补单，symbol:%s，原单数量：%d,成交数量:%d' % (item.order_id, item.security, item.amount, item.filled), datetime.datetime.now(), item.create_time)
        cancel_order_item = batch_cancel_order_item()
        cancel_order_item.order_id = item.order_id
        lstCancelOrders.append(cancel_order_item)

        order_item = batch_order_item()
        order_item.security = item.security
        if item.side == 'long':
            order_item.amount = item.amount - item.filled
        else:
            order_item.amount = -(item.amount - item.filled)

        order_item.style = LimitOrderStyle(get_order_price(item.security, item.side, g.rebuild_order_level))
        lstOrders.append(order_item)
        
    # 撤单,原单依然保留在g.order_dict中，直到收到已报待撤或者已撤的状态推送
    if len(lstCancelOrders) > 0:
        cancel_orders(lstCancelOrders)
    # 补单
#    print('开始补单操作，数量:%d', len(lstOrders))
    if len(lstOrders) > 0:
        lstRetOrders = orders(lstOrders)
#        print('补单返回数量:%d', len(lstRetOrders))
        for item in lstRetOrders:
#            print('补单订单号', item.order_id)
            g.order_dict[item.order_id] = item
#        print('order dict size:', len(g.order_dict))


def trade_constituents(side='long'):
    """
    成分券买卖接口，停牌不交易、涨停不卖，跌停不买、必须现金替代的不买
    :return:
    """
    lstOrders = []
    for etfConstituentInfo in g.etfConstituentInfoList:
        # 订单取对手盘一档报单
#        print('开始检查成分券：', etfConstituentInfo.symbol)
        if etfConstituentInfo.suspend_flag:  # 停牌不交易
            continue
        elif etfConstituentInfo.cash_replace_flag == 2 and side == 'long':  # 示例程序中暂不考虑跨市场，必须现金替代的不买
            continue
        tickData = get_current_tick(etfConstituentInfo.symbol)
        if tickData.code == etfConstituentInfo.symbol:
            if side == 'long' and abs(tickData.current - tickData.low_limit) < 0.001:  # 跌停不买
                continue
            elif side == 'short' and abs(tickData.current - tickData.high_limit) < 0.001:  # 涨停不卖
                continue
        else:
            print('未获取到成分券行情，成分券代码:', etfConstituentInfo.symbol)
        
        item = batch_order_item()
        item.security = etfConstituentInfo.symbol
        if side == 'long':
            item.amount = etfConstituentInfo.sample_size * g.amount
        else:
            item.amount = -1 * etfConstituentInfo.sample_size * g.amount

        # 判断是否使用持仓
        if side == 'long':
            if g.use_position:
                position = context.portfolio.positions[item.security]
                if position is not None:
                    item.amount -= position.redemption_num
                    if item.amount <= 0:
#                        print('持仓数量足够，无需买入成分券:', item.security)
                        continue
#        print('报单：',item.security)
        item.style = LimitOrderStyle(get_order_price(etfConstituentInfo.symbol, side, g.order_level))
        lstOrders.append(item)
    if len(lstOrders) > 0:
        lstRetOrders = orders(lstOrders)
        for item in lstRetOrders:
            g.order_dict[item.order_id] = item
    else:
        check_and_excute_next_step()

def check_and_excute_next_step():
    """
    检查并执行下一步操作，目前通过成交驱动
    :return:
    """
    # 如果订单列表里面还有未完成的订单，不执行下一步操作
    if len(g.order_dict) != 0:
        return

    if g.arbitrage_type == 'discount_step1':
        log.debug('step1-end ETF基金买入成功')
        print('\n')
        log.debug('step2 赎回成分券')
#        g.arbitrage_type = 'discount_step2'
        print(-1 * g.amount, type(g.amount))
        order2 = g.etfHandler.etf_purchase_redemption(-1 * g.amount)
        #赎回操作不可撤销，不放入订单列表，通过类型判断是否为赎回成交
#        g.order_dict[order2.order_id] = order2

    elif g.arbitrage_type == 'discount_step2':
        log.debug('step2-end 赎回成功')
        print('\n')
        log.debug('step3 卖出成分券')
        trade_constituents('short')
        g.arbitrage_type = 'discount_step3'

    elif g.arbitrage_type == 'discount_step3':
        log.debug('step3-end 成分券卖出成功')
        print('\n')
        log.debug('折价套利操作结束')
        print('\n')
        g.arbitrage_type = 'end'
    elif g.arbitrage_type == 'premium_step1':
        log.debug('step1-end 买入成分券成功')
        print('\n')
        log.debug('step2 申购ETF基金')
        order2 = g.etfHandler.etf_purchase_redemption(g.amount)
        #        print('申购：order_id = ', order2.order_id, '------------------------------')
        #申购操作不可撤销，不放入订单列表，通过类型判断是否为申购成交
#        g.order_dict[order2.order_id] = order2
    elif g.arbitrage_type == 'premium_step2':
        log.debug('step2-end ETF基金申购成功')
        print('\n')
        log.debug('step3 卖出ETF基金')
        order3 = order(g.symbol, -g.amount * g.etfInfo.report_unit, LimitOrderStyle(g.current_price))
        g.order_dict[order3.order_id] = order3
        g.arbitrage_type = 'premium_step3'
    elif g.arbitrage_type == 'premium_step3':
        log.debug('step3-end ETF基金卖出成功')
        print('\n')
        log.debug('溢价套利操作结束')
        print('\n')
        g.arbitrage_type = 'end'
    else:
        pass


def handle_tick(context, tick, msg_type):
    """
    实时行情接收函数
    1、接收基金的实时行情数据
    2、若没有接收到IOPV数据或套利步骤标识没有初始化，直接返回
    3、IOPV > price，执行折价套利操作第一步：买入etf基金，g.arbitrage_type中记录当前步骤
    4、IOPV < price, 执行溢价套利操作第一步：买入成分券，g.arbitrage_type中记录当前步骤
    :param context:
    :param tick: Tick对象
    :return:
    :remark:可选实现
    """
    print('recv tick data', tick.code, tick.current, tick.code, g.symbol, g.ETF_IOPV, g.arbitrage_type)
    if tick.code != g.symbol:
        # tickData = get_current_tick(tick.code)
        # print('代码行情:',tickData.code)
        return
    # tickData = get_current_tick(tick.code)
    # print('代码行情111:',tickData.code)
    g.current_price = tick.current
    
    trigger_trade()
    
    
def trigger_trade():
    
    if g.ETF_IOPV == 0 or g.arbitrage_type != '':
        return
        
    if g.ETF_IOPV > g.current_price and g.discount_estimated_amount > g.arbitrage_estimate_amount:
        # 折价套利操作
        print('当前一级市场ETF预估IOPV：', g.ETF_IOPV)
        print('当前二级市场ETF基金价格：', g.current_price)
        print('\n')
        log.debug('开始执行折价套利操作')
        print('\n')
        log.debug('step1 买入ETF基金')
        g.arbitrage_type = 'discount_step1'
        if g.use_position:      #判断是否使用持仓
            position = context.portfolio.positions[g.symbol]
            if position is not None:
                amount = g.amount * g.etfInfo.report_unit - position.redemption_num
                if amount > 0:
                    retOrder = order(g.symbol, amount, LimitOrderStyle(g.current_price))
                    g.order_dict[retOrder.order_id] = retOrder
                else:
                    g.arbitrage_type = 'discount_step2'
                    print('ETF基金持仓已经足够，无需买入基金,开始赎回成分券')
                    order2 = g.etfHandler.etf_purchase_redemption(-1 * g.amount)
            else:
                print('未获取到etf持仓信息，全量买入etf基金')
                retOrder = order(g.symbol, g.amount * g.etfInfo.report_unit, LimitOrderStyle(g.current_price))
                g.order_dict[retOrder.order_id] = retOrder
        else:
            retOrder = order(g.symbol, g.amount * g.etfInfo.report_unit, LimitOrderStyle(g.current_price))
            g.order_dict[retOrder.order_id] = retOrder

    elif g.ETF_IOPV < g.current_price and g.premium_estimated_amount > g.arbitrage_estimate_amount:
        # 溢价套利操作
        print('当前一级市场ETF预估IOPV：', g.ETF_IOPV)
        print('当前二级市场ETF基金价格：', g.current_price)
        print('\n')
        log.debug('开始执行溢价套利操作')
        print('\n')
        log.debug('step1 买入成分券')
        # 可以使用篮子买入接口，也可以获取所有成分券，根据样本数量买入，前一种简单，但是需要配合ETF交易界面上的设置来做一些类似涨停不买、跌停不卖、使用持仓等
        # 后一种比较灵活，可以根据自己的策略来设置
        # 示例策略中采用后一种
        g.arbitrage_type = 'premium_step1'
        trade_constituents('long')
        # 篮子买入接口示例
        # order1 = basket_order(g.symbol, 1)
        # for tmp in order1:
        #     tmp_order = Order()
        #     tmp_order.order_id = tmp['cl_ord_id']
        #     tmp_order.amount = float(tmp['entrust_amount'])
        #     tmp_order.security = tmp['security_symbol']
        #     tmp_order.symbol = tmp['security_symbol']
        #     g.order_dict[tmp_order.order_id] = tmp_order
        #            log.debug('买入成分券: order_id=' + tmp_order.order_id + '  symbol=' + tmp_order.symbol + '  security=' + tmp_order.security + '  amount=%d' % (tmp_order.amount))

    else:
        pass


def handle_etf_estimate_info(context, etf_estimate_info, msg_type):
    """
    实时ETF预估信息接收函数
    :type etf_estimate_info: EtfEstimateInfo
    :param context:
    :param etf_estimate_info: EtfEstimateInfo对象
    :return:
    :remark:可选实现
    """
    # 保存当前IOPV
#    print('handle_etf_estimate_info', etf_estimate_info.code, etf_estimate_info.IOPV, etf_estimate_info.premium, etf_estimate_info.discount)
    g.ETF_IOPV = etf_estimate_info.IOPV
    g.premium_estimated_amount = etf_estimate_info.premium
    g.discount_estimated_amount = etf_estimate_info.discount
    trigger_trade()

#    print('ETF预估信息：', g.ETF_IOPV, etf_estimate_info.premium, etf_estimate_info)

def on_strategy_end(context):
    """
    策略结束时调用，用户可以在此函数中进行一些汇总分析、环境清理等工作
    :param context:
    :return:
    :remark:可选实现
    """
    print('on_strategy_end')
