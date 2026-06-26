# encoding: utf-8
"""
1、计算前N日的4个价位:HH(前N日的最高价)，HC（前N日收盘价的最高价），LC（前N日收盘价的最低价），LL（前N日最低价）
2、计算价格浮动区间，公式为Range=max(HH-LC,HC-LL)
3、计算日内的上轨和下轨：
    上轨：开盘价+Ks*Range
    下轨：开盘价-Kx*Range
4、交易规则：日内价格突破上轨买入，突破下轨卖出

本策略做了适当调整，主要是弱化了当前仓位的限制
"""
from mquant_api import *
from mquant_struct import *
import OrderMgr


def strategy_params():
    dict_params = {
        '参考历史交易日数量': {'value': 20, 'desc': '策略参考的历史交易日的数量'},
        '上轨参数(Ks)': {'value': 0.7, 'desc': '上轨计算参数'},
        '下轨参数(Kx)': {'value': 0.7, 'desc': '下轨计算参数'},  # 考虑到T+0
        '单次卖出仓位比例': {'value': 0.2},
        '单次买入资金比例': {'value': 0.2},
    }
    return dict_params


def calcu_fix_params(code, klinedata):
    """
    根据k线计算6个固定价位
    """
    if klinedata is not None and len(klinedata.data['date']) >= 1:
        # 三个阻力位
        HH = klinedata.highest_price()
        HC = max(klinedata.data['close'])
        LC = min(klinedata.data['close'])
        # 三个支撑位
        LL = klinedata.lowest_price()
        g.fix_params_dict[code]['Range'] = max(HH - LC, HC - LL)
        g.fix_params_dict[code]['ready_flag'] = True
        print(g.fix_params_dict[code])


class OrderRequestStatus(object):
    """
    订单请求状态
    """
    init = 0  # 初始状态
    running = 1  # 报单未成状态
    finish = 2  # 报单完成状态


def initialize(context):
    """
    策略初始化，启动策略时调用，用户可在初始化函数中订阅行情、设置标的、设置定时处理函数等
    该函数中允许读取文件，除此之外的其他函数禁止读取文件
    :param context:
    :return:
    :remark:必须实现
    """
    # 订阅标的证券的实时行情,订阅时会自动异步查询近180天的日k数据
    security_list = get_symbol_list(ExchangeType.SH, SecurityType.StockType, SecuritySubType.Ashares) + get_symbol_list(ExchangeType.SZ, SecurityType.StockType, SecuritySubType.Ashares)
    
    # 固定价字典，key为code，value为{价位名称:价位值,...}的字典
    g.fix_params_dict = {}
    g.ref_kline_bar_num = int(context.run_params['参考历史交易日数量'])
    g.Ks = float(context.run_params['上轨参数(Ks)'])
    g.Kx = float(context.run_params['下轨参数(Kx)'])
    g.sell_ratio = float(context.run_params['单次卖出仓位比例'])
    g.buy_ratio = float(context.run_params['单次买入资金比例'])
    g.order_req_status = OrderRequestStatus.init  # 只交易一次
    g.order_obj_list = []  # 记录订单对象
    g.security_list=[]
    # 表示还未计算R-Breaker的六个固定价位
    for code in security_list:
        symbol_detial = get_symbol_detial(code)
        #获取昨收盘价
#        print(symbol, symbol_detial.LocalListedShare)
        #过滤ST股票
        if symbol_detial.STFlag == STStatus.serious or symbol_detial.STFlag == STStatus.special:
            continue
        
        #根据昨收计算流通市值，取市值在50亿到200亿之间的标的
        LocalListedValue = symbol_detial.LocalListedShare * symbol_detial.PreClosePrice 
        print(code, symbol_detial.PreClosePrice)
        if LocalListedValue > 5000000000 and LocalListedValue < 20000000000:
            g.security_list.append(code)
            print('符合条件的标的：', code)
        else:
            continue
            
        g.fix_params_dict[code] = {'ready_flag': False}
        # 按交易日取k线数据
        kbars = get_kline_data_from_init_date(code, -1 * g.ref_kline_bar_num, get_cur_time(),
                                              kline_type=KLineDataType.KLINEData_1D, date_type=DateType.TRADE_DATE)
        calcu_fix_params(code, kbars)

    subscribe(g.security_list)


def handle_tick(context, tick, msg_type):
    """
    实时行情接收函数
    :param context:
    :param tick: Tick对象
    :return:
    :remark:可选实现
    """
    if g.OrderRequestStatus == OrderRequestStatus.finish:
        stop_stragety()
        return

    symbol = tick.code

    if symbol in g.security_list and g.fix_params_dict[symbol]['ready_flag']:
        high_level_price = tick.open + g.Ks * g.fix_params_dict[symbol]['Range']
        low_level_price = tick.open - g.Kx * g.fix_params_dict[symbol]['Range']
        if tick.current > high_level_price and g.order_req_status == OrderRequestStatus.init:  # 价格超过上轨
            # 计算买入数量
            log.debug('价格高于上轨，开始买入股票，证券：{}'.format(symbol))
            cash = g.buy_ratio * context.subportfolios[context.subportfolio_type_index[AccountType.normal]].settled_cash
            available_cash = context.subportfolios[context.subportfolio_type_index[AccountType.normal]].available_cash
            if cash > available_cash:
                log.warn('可用资金数量[{}]小于单次所需资金量[{}],使用全部可用资金买入'.format(available_cash, cash))
                cash = available_cash
            amount = cash / tick.current
            amount = int(amount) - int(amount) % 100
            if amount == 0:
                log.debug('可用资金[{}]不够买入一手证券[{}]'.format(cash, symbol))
            else:
                order_exec(symbol, amount)
                g.order_req_status = OrderRequestStatus.running
                log.debug('证券：{}下单结束，数量：{}'.format(symbol, amount))
            return

        elif tick.current > low_level_price and g.order_req_status == OrderRequestStatus.init:  # 价格低于下轨
            log.debug('价格低于下轨，开始卖出股票，证券：{}'.format(symbol))
            pos = context.subportfolios[context.subportfolio_type_index[AccountType.normal]].positions[symbol]
            if pos is None:
                log.warn('[{}]可用证券数量为0'.format(symbol))
                return

            amount = pos.closeable_amount * g.sell_ratio
            amount = int(amount) - int(amount) % 100
            if amount == 0:
                log.warn('[{}]可用证券数量不足'.format(symbol))
            else:
                order_exec(symbol, -1 * amount)
                g.order_req_status = OrderRequestStatus.running
                log.debug('证券：{}下单结束，数量：{}'.format(symbol, amount))
            return


class MyOrderObj(OrderMgr.OrderObject):
    """
    订单管理类
    """

    def __init__(self, symbol, amount):
        super(MyOrderObj, self).__init__()
        self.set_cancel_order_interval(5, 10)
        self.symbol = symbol
        self.set_qty(abs(amount))
        if amount > 0:
            self.side = OrderSide.BUY
        else:
            self.side = OrderSide.SELL

        self.register_status_callback(self.on_order_obj_status_change)

    def get_style(self):
        tick = get_current_tick(self.symbol)
        if tick == OrderSide.BUY:
            if tick.a1_p > 0.0001:
                return LimitOrderStyle(tick.a1_p)
            else:
                return LimitOrderStyle(tick.high_limit)
        else:
            if tick.b1_p > 0.0001:
                return LimitOrderStyle(tick.b1_p)
            else:
                return LimitOrderStyle(tick.low_limit)

    def on_order_obj_status_change(self, status):
        """
        订单执行完毕
        :param status:
        :return:
        """
        if status == OrderMgr.OrderObjStatus.stop:
            log.info('本次报单完成，撤单数量：{}，剩余数量：{}'.format(self.remain_qty(), self.cancelled_qty()))
            if self.cancelled_qty() > self.min_qty:
                if self.side == OrderSide.BUY:
                    order_exec(self.symbol, self.cancelled_qty())
                else:
                    order_exec(self.symbol, -1 * self.cancelled_qty())
            else:
                log.info('报单完成，策略终止')
                g.order_req_status = OrderRequestStatus.finish
                stop_stragety()


def order_exec(symbol, amount):
    """
    报单
    :param symbol:
    :param amount:
    :param style:
    :return:
    """
    ord_obj = MyOrderObj(symbol, amount)
    ord_obj.order()


def handle_order_report(context, ord, msg_type):
    """
    订单回报
    :param context:
    :param ord:
    :param msg_type:
    :return:
    """


def on_strategy_end(context):
    """
    策略结束时调用，用户可以在此函数中进行一些汇总分析、环境清理等工作
    :param context:
    :return:
    :remark:可选实现
    """
    # 取消订阅股票
    unsubscribe(g.security_list)
