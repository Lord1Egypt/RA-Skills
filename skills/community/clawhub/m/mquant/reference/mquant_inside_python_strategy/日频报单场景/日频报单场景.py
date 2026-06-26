# encoding: utf-8

from mquant_api import *
from mquant_struct import *
import json
import csv
import time
import datetime
import os
from OrderMgr import *


def strategy_params():
    dict_params = {
        '是否撤补单': {'value': True},  # 注意，市价单不可撤
        '撤单时间间隔': {'value': 5, 'desc': '单位为秒，勾选了是否撤补单才有效'},
        '价格档位': {'value': ['对手盘一档', '市价单', '涨跌停买卖'], 'desc': '默认为市价单，类型为五档即成剩撤'},
        '最小委托数量': {'value': 100},
        '最大委托数量': {'value': 990000, 'desc': '单笔订单委托数量超过最大委托数量，会自动拆成多笔报单'}
        # '委托数量向下取整': {'value': True, 'desc': '如果勾选数量向下取整，则会对订单数量按照最小委托数量的整数倍向下取整'}
    }
    return json.dumps(dict_params)


# 继承OrderObject订单对象，并重新实现废单处理部分逻辑
class TC_OrderObject(OrderObject):
    """
    调仓单笔订单管理类
    """

    def __init__(self):
        super(TC_OrderObject, self).__init__()
        self.set_order_qty_range(g.min_qty, g.max_qty)  # 设置合法的数量范围，默认为100-900000
        # 如果资金、持仓不足，则循环等待，直到资金持仓充足再报单
        self.set_loop_check(try_count=10)  # 设置循环检查次数，默认一直循环检查
        self.set_check_fund()  # 设置买入资金校验，默认不校验
        self.set_check_position()  # 设置卖出持仓校验，默认不校验
        # self.set_high_limit_forbidden()   #设置涨停不卖,默认不限制
        # self.set_low_limit_forbidden()    #设置跌停不买,默认不限制
        # self.set_chg_forbidden(-1.0,5.0, 3.0,6.0)  #设置涨跌幅限制,默认不限制
        # self.set_price_precision(2)        #设置价格精度，默认为2位小数
        self.set_qty_precision(1)  # 设置数量精度，默认为100，如果不设置会导致零股卖出不了
        if g.reorder_flag:
            self.set_cancel_order_interval(g.cancel_order_interval, try_count=5)  # 设置定时撤单时间间隔
            self.register_status_callback(self.on_status_change)    #注册订单管理对象状态变化回调

    # 虚函数重载，提供报单价格，如果需要文件传入价格，直接在该函数中返回LimitOrderStyle(price)即可，但是指定价格时撤补单逻辑实际是没有意义的
    def get_style(self):
        """
        实现报单价格
        :return:
        """
        # 处理价格类型
        # 涨跌停价格最好从实时行情中获取，从静态信息中获取存在一定的风险
        if g.price_level == '涨跌停买卖':
            if self.high_limit_price < 0.001:
                tick = get_current_tick(self.symbol)
                count = 0
                while tick.code != self.symbol:
                    time.sleep(1)
                    tick = get_current_tick(self.symbol)
                    count = count + 1
                    if count >= 3:
                        break
                if tick.code != self.symbol:
                    symbol_detial = get_symbol_detial(self.symbol)
                    if symbol_detial is not None:
                        self.high_limit_price = symbol_detial.HighLimitPrice
                        self.low_limit_price = symbol_detial.LowLimitPrice
                    else:
                        # 如果获取标的详情信息错误，则报市价单，这是一种异常情况的处置方案，基本不会用到
                        log.info('获取标的{}基础信息失败,使用市价报单'.format(self.symbol))
                        return MarketOrderStyle()
                else:
                    self.high_limit_price = tick.high_limit
                    self.low_limit_price = tick.low_limit

            if self.side == OrderSide.BUY:  # 买入
                return LimitOrderStyle(self.high_limit_price)
            else:
                return LimitOrderStyle(self.low_limit_price)

        elif g.price_level == '对手盘一档':
            tick = get_current_tick(self.symbol)
            count = 0
            while tick.code != self.symbol:
                # 从订阅到接收到行情推送需要时间，可能此时还未接收到行情推送，则缓存中没有tick信息
                log.info('获取标的{}tick数据失败，等待2s继续获取'.format(self.symbol))
                time.sleep(1)
                tick = get_current_tick(self.symbol)
                count = count + 1
                if count >= 3:
                    break
            #            print(tick.__dict__)
            if tick.code != self.symbol:
                # 如果获取标的详情信息错误，则报市价单，这是一种异常情况的处置方案，基本不会用到
                log.info('获取标的{}tick数据失败,使用市价报单'.format(self.symbol))
                return MarketOrderStyle()
            else:
                if self.side == OrderSide.BUY:
                    return LimitOrderStyle(tick.a1_p)
                else:
                    return LimitOrderStyle(tick.b1_p)
        return MarketOrderStyle()

    def check_param(self, security, market, side, qty):
        """
        订单参数合法性校验
        """
        if len(security) < 6:
            log.warn('不合法的标的：{}'.format(security))
            return False
        if len(market) <= 0:
            log.warn('不合法的市场，标的：{}，市场：{}'.format(security, market))
            return False

        if market not in ['SH', 'SZ']:
            log.warn('不合法的市场，标的：{}，市场：{}'.format(security, market))
            return False

        if side == 1:
            self.side = OrderSide.BUY
        elif side == 2:
            self.side = OrderSide.SELL
        else:
            log.warn('不合法的订单方向，标的：{}，市场：{}，方向：{}'.format(security, market, side))
            return False

        self.symbol = security + '.' + market
        self.set_qty(qty)
        if len(self.qty_list) <= 0:
            log.warn('不合法的订单数量，标的：{}，市场：{}，数量：{}'.format(security, market, qty))
            return False

        return True

    def on_status_change(self, status):
        """
        当订单处理完成时，应该补单
        :param status:
        :return:
        """
        if status == OrderObjStatus.stop:
            self.rebuild_order()

    def rebuild_order(self):
        """
        补单，只对撤单部分补单，废单部分不补单
        :return:
        """
        cancelled_qty = self.cancelled_qty()
        if cancelled_qty > 0 and cancelled_qty > self.min_qty:
            new_order_obj = TC_OrderObject()
            new_order_obj.side = self.side
            new_order_obj.symbol = self.symbol
            new_order_obj.set_qty(cancelled_qty)
            new_order_obj.order()


def initialize(context):
    """
    策略初始化，启动策略时调用，用户可在初始化函数中订阅行情、设置标的、设置定时处理函数等 该函数中允许读取文件，除此之外的其他函数禁止读取文件
    注意，初始化阶段禁止交易
    :param context:
    :return:
    :remark:必须实现
    """
    # 用户根据自己实际文件存放路径来指定路径前缀，批量固化的策略批次序号从0开始，一批固化的策略批次序号依次+1递增
    g.file_path = "D:\\TestData\\testdata" + str(context.get_batch_index()) + ".csv"
    print(context.run_params)
    print('监控文件：',g.file_path) 
    g.cancel_order_interval = int(context.run_params['撤单时间间隔'])
    g.price_level = context.run_params['价格档位']
    g.reorder_flag = bool(int(context.run_params['是否撤补单']))
    g.min_qty = int(context.run_params['最小委托数量'])
    g.max_qty = int(context.run_params['最大委托数量'])
    # g.round_qty = bool(int(context.run_params['委托数量向下取整']))

    file_ready = False
    g.order_list = []
    g.strategy_end = False
    while not file_ready and not g.strategy_end:
        #        print('begin check', os.path.exists(g.file_path))
        if not os.path.exists(g.file_path):
            time.sleep(0.1)    #10ms重新检查一次，用户可以根据自己的实际情况，调长或者调短这个时间间隔
            continue

        csv_file = open(g.file_path, 'r', newline='')
        reader = csv.DictReader(csv_file)
        for row in reader:
            if row['last'] == 'True':
                file_ready = True
                break
        csv_file.close()
        if not file_ready:
            print(file_ready)
            time.sleep(0.1)    #10ms重新检查一次，用户可以根据自己的实际情况，调长或者调短这个时间间隔

    if g.strategy_end:
        return
    csv_file = open(g.file_path, 'r', newline='')
    reader = csv.DictReader(csv_file)
    symbol_list = []
    for row in reader:
        # 读取csv文件，将订单信息存储下来，用户可根据自己的实际情况改写
        log.info('读取文件订单信息：{}'.format(row))
        order_info = TC_OrderObject()
        if order_info.check_param(row['security'], row['market'], int(row['side']), int(row['qty'])):
            g.order_list.append(order_info)
            symbol_list.append(order_info.symbol)
        # 非法的订单信息需要用户自行手动处理
    # 订阅实时行情，方便报单的时候能获取到指定的价格
    if len(symbol_list) > 0:
        subscribe(symbol_list)


def on_strategy_start(context):
    """
    策略正式启动回调
    :param context:
    :return:
    :remark: 初始化函数返回后立即调用，在该回调函数中允许交易，不允许读取外部文件，可选实现
    """
    log.info('开始报单,数量：{}'.format(len(g.order_list)))
    for order_obj in g.order_list:
        order_obj.order()
    log.info('报单结束')


def handle_tick(context, tick, msg_type):
    """
    实时行情接收函数
    :param context:
    :param tick: Tick对象
    :param msg_type 消息类型，暂不启用
    :return:
    :remark:可选实现
    """
    pass


#    print('recv tick',tick.__dict__)


def handle_order_report(context, ord, msg_type):
    """
    订单回报处理函数
    :param ord:Order对象
    :param msg_type 消息类型，透传字段，调用查询接口时传入可获得协程并发
    :return:
    :remark:可选实现
    """
    # 判断如果废单且查不到相应的订单信息，说明订单未报到柜台就废单了，此时应该考虑是否补单
    if ord.status == OrderStatus.rejected:
        ord_info = get_orders(ord.order_id)
        if ord_info is None:
            log.warn('订单{}废单且未报到柜台，请手工检查并处理'.format(ord.order_id))


def on_strategy_params_change(params, path):
    """
    监控界面修改策略实例参数回调
    :param params:参数，支持任意形式的文本参数
    :param path:如果传入的是参数文件，path为文件路径，否则path为空字符串
    :return:
    :remark:可选实现
    """
    pass


def on_strategy_end(context):
    """
    策略结束时调用，用户可以在此函数中进行一些汇总分析、环境清理等工作
    :param context:
    :return:
    :remark:可选实现
    """
    log.info('strategy end')
    g.strategy_end = True
