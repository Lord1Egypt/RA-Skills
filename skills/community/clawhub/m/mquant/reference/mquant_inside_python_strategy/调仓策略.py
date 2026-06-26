# encoding: utf-8

from mquant_api import *
from mquant_struct import *
import json
import csv
import time
import datetime
import os

def strategy_params():

    dict_params = {
        '文件路径': {'value': 'D:\\TestData\\testdata.csv', 'desc': '标的文件路径，建议填写绝对路径,如D:\\stock.csv'},  # 'desc'字段可填写，也可不填写
        '是否撤补单': {'value': True},
        '撤单时间间隔': {'value': 5, 'desc': '单位为秒，勾选了是否撤补单才有效'},
        '价格档位': {'value': ['市价单', '对手盘一档', '涨跌停买卖'], 'desc': '默认为市价单，类型为五档即成剩撤'},
        '最小委托数量':{'value': 100},
        '最大委托数量':{'value': 990000, 'desc':'单笔订单委托数量超过最大委托数量，会自动拆成多笔报单'},
        '委托数量向下取整': {'value': True, 'desc':'如果勾选数量向下取整，则会对订单数量按照最小委托数量的整数倍向下取整'}
    }
    return json.dumps(dict_params)


    
class OrderObject(object):
    def __init__(self):
      self.security=''
      self.market=''
      self.qty_list=[]       #考虑到拆单的场景,数量是一个数组
      self.side=0
      self.order_list=[]

    def set_qty(self, qty):
        """
        修正委托数量
        如果用户的委托数量不是最小委托数量的倍数，且用户设置了修正委托数量，则需要将委托数量向下取整
        如果用户的委托数量超过最大委托数量，则自动拆单
        """
        fix_qty = qty
        if qty < g.min_qty:
            log.info('标的[{}]委托数量[{}]小于最小委托数量，订单信息无效'.format(self.security, qty))
        if g.round_qty:
            if qty % g.min_qty != 0:
                fix_qty = qty - qty % g.min_qty
                log.info('标的[{}]原委托数量:{},修正委托数量:{}'.format(self.security, qty, fix_qty))
        while fix_qty > g.max_qty:
            if fix_qty - g.max_qty > g.min_qty:
                self.qty_list.append(g.max_qty)
                fix_qty = fix_qty - g.max_qty
                if fix_qty <= g.max_qty:
                    self.qty_list.append(fix_qty)
                    fix_qty = 0
                    break
            else:
                self.qty_list.append(g.min_qty)
                self.qty_list.append(fix_qty - g.min_qty)
                fix_qty = 0
        if fix_qty > 0:
            self.qty_list.append(fix_qty)
        
    def order_exec(self):
        """
        报单执行
        """
        symbol = self.security + "." + self.market
        for qty in self.qty_list:
            log.info('开始报单，标的：{}，数量：{}，价格类型：{}'.format(symbol, qty, g.price_level))
            order_style = None
            if g.price_level == '涨跌停买卖':
                symbol_detial = get_symbol_detial(symbol)
                if symbol_detial is not None:
                    if self.side == OrderSide.BUY:
                        order_style = LimitOrderStyle(symbol_detial.HighLimitPrice)
                    else:
                        order_style = LimitOrderStyle(symbol_detial.LowLimitPrice)
                else:
                    #如果获取标的详情信息错误，则报市价单，这是一种异常情况的处置方案，基本不会用到
                    log.info('获取标的{}基础信息失败,使用市价报单'.format(symbol))
                    pass
            elif g.price_level == '对手盘一档':
                tick = get_current_tick(symbol)
                if tick is None:
                    #从订阅到接收到行情推送需要时间，可能此时还未接收到行情推送，则缓存中没有tick信息
                    log.info('获取标的{}tick数据失败，等待2s继续获取'.format(symbol))
                    time.sleep(2)
                    tick = get_current_tick(symbol)
                if tick is None:
                    #如果获取标的详情信息错误，则报市价单，这是一种异常情况的处置方案，基本不会用到
                    log.info('获取标的{}tick数据失败,使用市价报单'.format(symbol))
                    pass
                else:
                    if self.side == OrderSide.BUY:
                        order_style = LimitOrderStyle(tick.a1_p)
                    else:
                        order_style = LimitOrderStyle(tick.b1_p)
                        
            if self.side == OrderSide.BUY:
                ord = order(symbol, qty, order_style)
                if ord is not None:
                    self.order_list.append(ord)
                else:
                    log.error('买入报单失败，返回None，标的：{}， 数量：{}'.format( symbol, qty))
            else:
                ord = order(symbol, -1 * qty, order_style)
                if ord is not None:
                    self.order_list.append(ord)
                else:
                    log.error('卖出报单失败，返回None，标的：{}， 数量：{}'.format( symbol, qty))
            
        if len(self.order_list) > 0:
            time=datetime.datetime.now() + datetime.timedelta(seconds=g.cancel_order_interval)
            run_timely(self.cancel_order,-1,time.strftime('%H:%M:%S'))

    def cancel_order(self, context, interval, msg_type):
        """
        撤单函数
        """
        #判断当前订单状态，如果未全成则撤单，如果报单已经废单了，完全没必要考虑撤补的情况，因为撤补还是会废单
        for ord in self.order_list:
            #查询订单
            order_dict = get_orders(ord.order_id)
            if order_dict is None or len(order_dict) == 0:
                log.error('未找到订单：{}对应的订单信息'.format(ord.order_id))
                continue
            order_info = order_dict.get(ord.order_id)
            if order_info is None:
                log.error('未找到订单：{}，查询返回的key：{}'.format(ord.order_id, order_dict.keys()))
                continue
            #撤单撤成功之后再补单，未收到撤单成交的消息不补单，避免超单
            if order_info.status == OrderStatus.new or order_info.status == OrderStatus.open:   #待报或已报，直接撤单
                cancel_order(order_info)
            elif order_info.status == OrderStatus.filled:     #部成状态，直接撤单
                cancel_order(order_info)
        
        self.order_list.clear()
                
        
    def is_valid(self):
        """
        订单参数合法性校验
        """
        if len(self.security) < 6:
            log.warn('不合法的标的：{}'.format(self.security))
            return False
        if len(self.market) <= 0:
            log.warn('不合法的市场，标的：{}，市场：{}'.format(self.security, self.market))
            return False
            
        if self.market not in ['SH','SZ']:
            log.warn('不合法的市场，标的：{}，市场：{}'.format(self.security, self.market))
            return False
            
        if len(self.qty_list) == 0:
            log.warn('不合法的订单数量，标的：{}，市场：{}'.format(self.security, self.market))
            return False
        if self.side == 1:
            self.side = OrderSide.BUY
        elif self.side == 2:
            self.side = OrderSide.SELL
        else:
            log.warn('不合法的订单方向，标的：{}，市场：{}，方向：{}'.format(self.security, self.market, self.side))
            return False
        return True
        

def initialize(context):
    """
    策略初始化，启动策略时调用，用户可在初始化函数中订阅行情、设置标的、设置定时处理函数等 该函数中允许读取文件，除此之外的其他函数禁止读取文件
    注意，初始化阶段禁止交易
    :param context:
    :return:
    :remark:必须实现
    """
    print(context.run_params)
    g.file_path = context.run_params['文件路径'].strip('/')
    g.cancel_order_interval = int(context.run_params['撤单时间间隔'])
    g.price_level = context.run_params['价格档位']
    g.reorder_flag = bool(int(context.run_params['是否撤补单']))
    g.min_qty = int(context.run_params['最小委托数量'])
    g.max_qty = int(context.run_params['最大委托数量'])
    g.round_qty = bool(int(context.run_params['委托数量向下取整']))
    
    file_ready = False
    g.order_list = []
    while not file_ready:
#        print('begin check', os.path.exists(g.file_path))
        if not os.path.exists(g.file_path):
            time.sleep(1)
            continue

        csv_file = open(g.file_path, 'r', newline='')
        reader = csv.DictReader(csv_file)
        for row in reader:
            if row['last'] == 'True':
                file_ready = True
                break
        csv_file.close()
        if file_ready == False:
            print(file_ready)
            time.sleep(1)

    csv_file = open(g.file_path, 'r', newline='')
    reader = csv.DictReader(csv_file)
    symbol_list = []
    for row in reader:
        #读取csv文件，将订单信息存储下来，用户可根据自己的实际情况改写
        log.info('读取文件订单信息：{}'.format(row))
        order_info = OrderObject()
        order_info.security = row['security']           #证券代码
        order_info.market = row['market']               #交易市场，上海为SH，深圳为SZ
        order_info.set_qty(int(row['qty']))                #订单数量
        order_info.side = int(row['side'])              #买卖方向，1为买入，2为卖出
        if order_info.is_valid():
            g.order_list.append(order_info)
            symbol_list.append(order_info.security + "." + order_info.market)
    #订阅实时行情，方便报单的时候能获取到指定的价格
    if len(symbol_list) > 0:
        subscribe(symbol_list)

def on_strategy_start(context):
    """
    策略正式启动回调
    :param context:
    :return:
    :remark: 初始化函数返回后立即调用，在该回调函数中允许交易，不允许读取外部文件，可选实现
    """
    log.info('开始报单')
    for order_obj in g.order_list:
        order_obj.order_exec()
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

def handle_order_report(context, ord, msg_type):
    """
    订单回报处理函数
    :param ord:Order对象
    :param msg_type 消息类型，透传字段，调用查询接口时传入可获得协程并发
    :return:
    :remark:可选实现
    """
    if ord.status == OrderStatus.canceled:
        #判断需要补单的数量
        log.info('开始补单，标的：{}，补单数量：{}'.format(ord.symbol, ord.amount - ord.filled))
        if ord.amount - ord.filled < g.min_qty:
            log.info('补单数量小于最小数量，不执行补单')
            return
        symbol_info = ord.symbol.split('.')
        if len(symbol_info) != 2:
            log.error('标的代码{}非法，不执行补单'.format(ord.symbol))
            return
            
        order_info = OrderObject()
        order_info.security = symbol_info[0]           #证券代码
        order_info.market = symbol_info[1]              #交易市场，上海为SH，深圳为SZ
        order_info.set_qty(ord.amount - ord.filled)                #订单数量
        order_info.side = ord.side              #买卖方向，1为买入，2为卖出
        order_info.order_exec()

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
    pass
