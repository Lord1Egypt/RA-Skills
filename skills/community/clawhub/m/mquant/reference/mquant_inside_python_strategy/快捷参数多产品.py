# encoding: utf-8

from mquant_api import *
from mquant_struct import *
import json
import os
import time
import threading
import shutil
custom_field_mutex = threading.Lock()


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
    dict_params = {
       '自定义字段':{'value':['支持','不支持'],'desc':'下拉列表，是否支持自定义字段，默认支持'},
       '策略类型':{'value':['主策略','子策略'],'desc':'主策略负责接收消息，发现不是当前策略资金账号的，则通过消息分发出去，子策略接收到消息后再进行处理'},
       '备份文件数量':{'value':0, 'desc':'备份文件数量，0表示不留备份'},
       '废单字段补全':{'value':False}
       }
    return json.dumps(dict_params)

def on_recv_custom_params(context, msg_type, custom_msg):
    """
    接收策略间消息
    """
    on_recv_fast_params(custom_msg)
#    split_index = custom_msg.find("&")
#    if split_index == -1:
#        log.error('invalid msg:{}'.format(custom_msg))
#    else:
#        fund_account = custom_msg[0:split_index]
#        if fund_account != g.fund_account_stock and fund_account != g.fund_account_margin:
#            return
#        on_recv_fast_params(custom_msg[split_index + 1:])

def initialize(context):
    if context.run_params['自定义字段'] == '支持':
        g.enable_custom_field = True
    else:
        g.enable_custom_field = False
    
    if context.run_params['策略类型'] == '子策略':
        g.sub_strategy = True
    else:
        g.sub_strategy = False
    
    g.bak_file_num = int(context.run_params['备份文件数量'])
    g.complete_section=bool(context.run_params['废单字段补全'])
    g.order_info = {}
#    print(context.run_params, g.enable_custom_field)
    # 主策略才注册参数窗口
    if not g.sub_strategy:
        register_fast_param_wnd("FastMsgWnd")  # 注册快速参数窗口
        
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
    g.custom_field_file = cur_file_dir + '\\custom_field.csv'
    g.account_type_info = {}
    if len(g.fund_account_stock) > 0:
        init_trade_files(context, AccountType.normal, g.fund_account_stock, g.order_file_stock, g.execution_file_stock,
                         g.fund_file_stock,
                         g.position_file_stock)
        g.account_type_info[g.fund_account_stock] = AccountType.normal

    if len(g.fund_account_margin) > 0:
        init_trade_files(context, AccountType.margin, g.fund_account_margin, g.order_file_margin,
                         g.execution_file_margin, g.fund_file_margin,
                         g.position_file_margin)
        g.account_type_info[g.fund_account_margin] = AccountType.margin


    # 注册1s一次的定时函数，定时更新资金和持仓，每次全量更新，记录时间戳
    # run_timely(timer_func, 1)
    g.count = 0
    if g.sub_strategy:
        subscribe_custom_msg(12000, on_recv_custom_params)


def get_bak_file(origin_file, subfix=0):
    """
    获取备份文件名
    """
#    print(origin_file, subfix, g.bak_file_num)
    if subfix > g.bak_file_num:
        return ""
    pos = origin_file.find('.csv')
    if pos > 0:
        prefix = origin_file[:pos]
        file_bak = prefix + '_bak' + str(subfix) + '.csv'
        print(file_bak)
        if os.path.exists(file_bak):
            return get_bak_file(origin_file, subfix + 1)
        else:
            return file_bak
    return ""


def bak_trade_files(order_file, execution_file, fund_file, pos_file):
    """
    文件备份
    """
    
    if os.path.exists(order_file):
        ord_bak_file = get_bak_file(order_file)
        if len(ord_bak_file) > 0:
            shutil.copy(order_file, ord_bak_file)
            
    if os.path.exists(execution_file):
        exec_bak_file = get_bak_file(execution_file)
        if len(exec_bak_file) > 0:
            shutil.copy(execution_file, exec_bak_file)
         

def init_trade_files(context, account_type, fund_account, order_file, execution_file, fund_file, pos_file):
    # 委托
    if g.bak_file_num > 0:
        bak_trade_files(order_file, execution_file, fund_file, pos_file)
       
    if not os.path.exists(g.custom_field_file):
        with open(g.custom_field_file, 'w', encoding='utf-8') as f:
            f.write('订单号,自定义字段\n')
    else:
        # 将自定义字段信息都读取出来
        with open(g.custom_field_file, 'r', encoding='utf-8') as f:
            info_list = f.readlines()
            if len(info_list) > 0:
                while not custom_field_mutex.acquire():
                    time.sleep(0.01)
                for line in info_list:
                    lst_item = line.rstrip('\n').split(',')
                    g.order_custom_field[lst_item[0]] = lst_item[1]
                custom_field_mutex.release()
                
                        
    
    with open(order_file, 'w', encoding='utf-8') as f:
        f.write('资金账号,委托时间,实例ID,证券代码,买卖方向,委托数量,委托价格,状态,价格类型,柜台委托编号,委托属性,委托类型,成交数量,成交金额,撤单数量,废单原因,订单编号,自定义字段\n')
        page_no = 1
        while True:
            ret_data = get_orders_ex(only_this_inst=False, page_no=page_no,account_type=account_type)  # 仅演示获取普通A股账号的订单信息，可根据自己的实际场景选择获取两融的,分页查询，每次获取1000条
            ord_list = ret_data[2]
            if ord_list is not None:
                ord_list = sorted(ord_list.values(), key=lambda ord: str(ord.add_time) + str(ord.entrust_no))
                for ord in ord_list:
                    f.write(get_order_str(ord))
                if ret_data[1]:
                    break
                page_no = page_no + 1
            else:
                break
    # 成交
    with open(execution_file, 'w', encoding='utf-8') as f:
        f.write('资金账号,成交时间,实例ID,证券代码,买卖方向,成交价格,成交数量,成交金额,成交类型,柜台委托编号,柜台成交编号,订单编号,自定义字段\n')
        page_no = 1
        while True:
            ret_data = get_trades_ex(only_this_inst=False,page_no=page_no,page_size=1000,
                                        account_type=account_type)  # 仅演示获取普通A股账号的订单信息，可根据自己的实际场景选择获取两融的
            
            execution_list = ret_data[2]
            if execution_list is not None:
                print('查询成交返回：', len(execution_list))
                execution_list = sorted(execution_list,
                                        key=lambda execution: str(execution.time) + str(execution.trade_id))

                for execution in execution_list:
                    f.write(get_execution_str(execution))
                
                if ret_data[1]:
                    break
                page_no = page_no + 1
            else:
                break
    # 资金
    with open(fund_file, 'w', encoding='utf-8') as f:
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
    with open(fund_file, 'a', encoding='utf-8') as f:
        context.set_current_account_type(account_type)
        fund_account = context.get_fund_account_by_type(account_type)
        fund_str = '{},{},{},{}\n'.format(datetime.datetime.now(), fund_account, context.portfolio.settled_cash,
                                          context.portfolio.available_cash)
        f.write(fund_str)


def write_pos_info(context, account_type, pos_file):
    with open(pos_file, 'w', encoding='utf-8') as f:
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

def record_order(order_id, symbol, side, amount, price, price_type):
#    print('record', price, price_type)
    if not g.complete_section:
        return
    while not custom_field_mutex.acquire():
        time.sleep(0.01)
    if len(order_id) > 0:
        g.order_info[order_id] = {'symbol':symbol, 'side':side, 'amount':amount, 'price':price, 'price_type':price_type, 'time':datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    custom_field_mutex.release()
    
def get_order_ext_info(order_id):
    if not g.complete_section:
        return
    while not custom_field_mutex.acquire():
        time.sleep(0.01)
    if len(order_id) > 0 and g.order_info.get(order_id) is not None:
        ext_order_info = g.order_info[order_id]
        custom_field_mutex.release()
        return ext_order_info
#        g.order_info[order_id] = {'symbol':symbol, 'side':side, 'amount':amount, 'price':price, 'price_type':price_type}
    custom_field_mutex.release()
            
                            
def get_custom_field_str(ord, push_msg=False):
    """
    获取自定义字段
    """
    if not g.enable_custom_field:
        return ""
    # 排除非MQuant报单
    if ord.inst_id is None or len(ord.inst_id) == 0 :
#        print('not mquant order:', ord.order_id)
        return ""
    # 排除算法报单
    if ord.algo_inst_id is not None and len(ord.algo_inst_id) > 0:
        return ""
  
    while not custom_field_mutex.acquire():
        time.sleep(0.01)

    custom_field = g.order_custom_field.get(ord.order_id)
    custom_field_mutex.release()
    count = 0
    if push_msg: 
        while custom_field is None:
            time.sleep(0.01)
            while not custom_field_mutex.acquire():
                time.sleep(0.01)
            custom_field = g.order_custom_field.get(ord.order_id)
            custom_field_mutex.release()
            count = count + 1
            if count > 10:
                custom_field = ''
                log.warn('尝试获取100次订单的用户自定义字段失败，订单id：{}'.format(ord.order_id))
                break
    elif custom_field is None:
        custom_field = ''
    return custom_field

def get_custom_field_str_from_execution(execution):
    if not g.enable_custom_field:
        return ""
    if execution.inst_id is None or len(execution.inst_id) == 0 :
#        print('not mquant order:', ord.order_id)
        return ""
    if execution.algo_inst_id is not None and len(execution.algo_inst_id) > 0:
        return ""
  
    while not custom_field_mutex.acquire():
        time.sleep(0.01)

    custom_field = g.order_custom_field.get(execution.order_id)
    custom_field_mutex.release()
    if custom_field is None:
        custom_field = ''
    return custom_field

def record_custom_field(order_id, custom_field):
    """
    记录自定义字段
    """
    if not g.enable_custom_field:
        return 
    while not custom_field_mutex.acquire():
        time.sleep(0.01)
    g.order_custom_field[order_id] = custom_field
    custom_field_mutex.release()
    
    # 将自定义字段写入文件
    try:
        with open(g.custom_field_file, 'a', encoding='utf-8') as f:
#            print('record custom field:', order_id, custom_field)
            f.write('{},{}\n'.format(order_id, custom_field))
    except Exception as e:
        print(e)


def get_order_str(ord, push_msg=False):
    custom_field = ''
#    if push_msg:
    custom_field = get_custom_field_str(ord, push_msg)
#    print(ord.order_id, ord.status, ord.fund_account)
    if ord.status is None:
        log.debug(ord.order_id)
    cancel_info = ord.cancel_info
    if len(ord.cancel_info) > 0:
        cancel_info = ord.cancel_info.replace(",",";").replace("\r\n","")
        cancel_info = cancel_info.replace(",",";").replace("\n","")
    if (len(ord.symbol) == 0 or ord.status == OrderStatus.rejected) and g.complete_section:
        ord_ext_info = get_order_ext_info(ord.order_id)
        if ord_ext_info is not None:
            ord.symbol = ord_ext_info['symbol']
            ord.amount = ord_ext_info['amount']
            price = ord_ext_info['price']
            ord.side = ord_ext_info['side']
            ord.add_time = ord_ext_info['time']
            price_type = ord_ext_info['price_type']
            if str(price_type) == "1":
                ord.style = LimitOrderStyle(price)
            else:
                ord.style = MarketOrderStyle(price_type, price)
        
    order_info = '{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}\n'.format(ord.fund_account, ord.add_time,
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
                                                                                  cancel_info, ord.order_id,
                                                                                  custom_field)
    return order_info


def get_execution_str(execution, push_msg=False):
    custom_field = get_custom_field_str_from_execution(execution)
    #'资金账号,成交时间,实例ID,证券代码,买卖方向,成交价格,成交数量,成交金额,成交类型,柜台委托编号,柜台成交编号,订单编号,自定义字段'
    execution_info = '{},{},{},{},{},{},{},{},{},{},{},{},{}\n'.format(execution.fund_account, execution.time,
                                                                    execution.inst_id, execution.symbol,
                                                                    transfer_order_side(execution.side),
                                                                    execution.price,
                                                                    execution.amount,
                                                                    execution.business_balance,
                                                                    execution.real_type,
                                                                    execution.entrust_no, execution.trade_id,
                                                                    execution.order_id,
                                                                    custom_field)

    return execution_info


def write_order_to_csv(ord):
    file_path = g.cur_file_dir + '\\order_' + ord.fund_account + '.csv'
    if not os.path.exists(file_path):
        log.error("订单文件{}不存在，无法更新订单信息".format(file_path))
        return
    with open(file_path, 'a', encoding='utf-8') as f:
        # 字段：资金账号、委托时间、实例ID、证券代码、买卖方向、委托数量、委托价格、价格类型、柜台委托编号、委托属性、委托类型、成交数量、成交金额、撤单数量、状态、废单原因、自定义字段
        f.write(get_order_str(ord, True))


def write_execution_to_csv(execution):
    # 成交留待客户自行实现
    file_path = g.cur_file_dir + '\\execution_' + execution.fund_account + '.csv'
    if not os.path.exists(file_path):
        log.error("成交文件{}不存在，无法更新订单信息".format(file_path))
        return
    with open(file_path, 'a', encoding='utf-8') as f:
        # 字段：资金账号、委托时间、实例ID、证券代码、买卖方向、委托数量、委托价格、价格类型、柜台委托编号、委托属性、委托类型、成交数量、成交金额、撤单数量、状态、废单原因
        f.write(get_execution_str(execution,True))


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
    try:
        write_order_to_csv(ord)
    except:
        pass


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
    try:
        write_execution_to_csv(execution)
    except:
        pass


def on_fund_update(context, fund_info):
    """
    category:事件回调
    brief:资金推送
    desc:资金推送函数，可选实现。
    :param context:
    :param fund_info: FundUpdateInfo 类对象
    :return:
    """
    try:
        fund_account = fund_info.fund_account
        fund_str = '记录时间,资金账号,期初资金,可用资金\n' + '{},{},{},{}\n'.format(datetime.datetime.now(), fund_account,
                                                                    context.portfolio.settled_cash,
                                                                    context.portfolio.available_cash)
        #    print(fund_info.__dict__, fund_str)
        fund_file = g.cur_file_dir + "\\fund_" + fund_account + ".csv"
        with open(fund_file, 'w', encoding='utf-8', buffering=len(fund_str) + 1) as f:
            f.write(fund_str)
    except:
        pass


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
    try:
        fund_account = pos_info.fund_account
        pos_file = g.cur_file_dir + "\\position_" + fund_account + ".csv"
        pos_str = '资金账号,证券代码,当前持仓,可用持仓,期初持仓\n'

        account_type = g.account_type_info[fund_account]
        pos_list = get_positions_ex(account_type)
        if pos_list is not None:
            for pos in pos_list:
                pos_str = pos_str + (
                    '{},{},{},{},{}\n'.format(fund_account, pos.security, pos.total_amount, pos.closeable_amount,
                                              pos.init_amount))

        with open(pos_file, 'w', encoding='utf-8', buffering=len(pos_str) + 1) as f:
            f.write(pos_str)
    except:
        pass


def on_recv_fast_params(params):
    #    log.debug('recv params:{}'.format(params))
    # 解析报撤单参数，多条订单用;分隔，一条订单内的不同字段用,分隔，可以修改脚本文件实现自定义
    # 报单参数格式为:
    # "资金账号&类型(0：报单),账号类型(AccountType),证券代码(带市场，如601688.SH),委托方向(1：买入，2：卖出),委托价格,
    # 价格类型(限价单：1，市价单，参考MarketOrderStyle),委托数量,委托类型(EntrustType),委托属性(EntrustProp),用户自定义字段(选填),
    # 头寸类型(融券卖出、买券还券、直接还券选填，如果不填写默认为普通头寸，PositionType),合约编号(买券还券、卖券还款、直接还券、直接还款选填，不填按默认顺序归还)"
    # 注意，选填字段之后如果还有字段需要填入，前面选填的字段也必须占位
    # 撤单参数格式为：
    # "资金账号&类型(1：撤单),账号类型(AccountType),订单编号"

#    print('recv params',params)
    pos = params.find("&")
    if pos <= 0:
        log.error('非法的参数:{}'.format(params))
        return
    fund_account = params[:pos]
#    print('fund_account',fund_account)
    if fund_account != g.fund_account_stock and fund_account != g.fund_account_margin:
        if not g.sub_strategy:
            publish_custom_msg(12000, params)
        return
    
    order_list = params[pos+1:].split(';')
#    print('order_list',order_list)

#    print('recv params:', params)
    for ord_str in order_list:
        params_list = ord_str.split(',')
        if len(params_list) < 3:
            log.error('非法的参数：{}'.format(ord_str))
            continue
        else:
            
            op_type = params_list[0]
            account_type = params_list[1]
#            print(op_type, account_type)
            if account_type != AccountType.normal and account_type != AccountType.margin:
                log.error('不支持的账号类型：{}'.format(account_type))
                continue

            if op_type == '0':  # 报单
                #                print('111111')
                # 用户自定义字段
                if len(params_list) < 9:
                    log.error('报单参数不足9个必传字段：{}'.format(ord_str))
                    continue
                entrust_prop = params_list[8]

                if entrust_prop != EntrustProp.trade and entrust_prop != EntrustProp.redemption:
                    log.error('不支持的委托属性：{}'.format(entrust_prop))
                    continue
                symbol = params_list[2]
                if len(symbol) != 9:
                    log.error('不支持的证券代码：{}'.format(symbol))
                    continue

                side = params_list[3]
                if side == '1':
                    side = OrderSide.BUY
                elif side == '2':
                    side = OrderSide.SELL
                else:
                    log.error('非法的订单方向：{}'.format(side))
                    continue

                price_type = params_list[5]
                price = float(params_list[4])
                if price_type == "1":
                    if price <= 0:
                        log.error('限价单非法的委托价格：{}'.format(params_list[4]))
                        continue
                    style = LimitOrderStyle(price)
                else:
                    style = MarketOrderStyle(price_type, price)

                qty = int(params_list[6])

                if qty <= 0:
                    log.error('非法的订单数量：{}'.format(params_list[6]))
                    continue

                custom_field = ''
                if len(params_list) >= 10:
                    custom_field = params_list[9]

                if account_type == AccountType.normal:
                    if entrust_prop == EntrustProp.redemption:  # ETF申赎
                        etfHandler = HtEtfHandler(symbol)
                        if side == OrderSide.BUY:
                            ord = etfHandler.etf_purchase_redemption(qty, style, side)
                        else:
                            ord = etfHandler.etf_purchase_redemption(-1 * qty, style, side)
                            
                        if ord is not None:
                            record_custom_field(ord.order_id, custom_field)
                            record_order(ord.order_id, symbol, side, qty, 1.0, 1)
                    else:
                        item = OrderRequest()
                        item.symbol = symbol
                        item.amount = qty
                        item.side = side
                        item.style = style
                        
                        ord = order_normal(item, account_type)
                        if ord is not None:
                            record_custom_field(ord.order_id, custom_field)
                            record_order(ord.order_id, symbol, side, qty, 1.0, 1)
                        
                else:
                    item = OrderRequest()
                    item.symbol = symbol
                    item.amount = qty
                    item.side = side
                    item.style = style
                    item.entrust_type = params_list[7]
                    contract_no = ''
                    position_type = PositionType.normal
                    if len(params_list) >= 11:
                        if int(params_list[10]) == PositionType.vip.value:
                            position_type = PositionType.vip
                    item.position_type = position_type

                    if len(params_list) >= 12:
                        contract_no = params_list[11]
                        item.contract_no = contract_no
                        
                    ord = order_normal(item, account_type)
                    if ord is not None:
                        record_custom_field(ord.order_id, custom_field)
                        record_order(ord.order_id, symbol, side, qty, 1.0, 1)


            elif op_type == '1':  # 撤单
                orig_order_id = params_list[2]
                if len(orig_order_id) <= 0:
                    log.error('被撤订单号为空，撤单失败，参数：{}'.format(ord_str))
                    continue
                
                cancel_order(orig_order_id,account_type=account_type)
            else:
                log.error("非法的操作类型：{}".format(op_type))
                continue



def on_strategy_params_change(params, path):
    """
    category:事件回调
    brief:参数修改回调
    desc:参数修改回调，可选实现。用户在策略执行监控界面的实例列表中，点击参数修改按钮修改实例参数时，参数信息会通过此回调通知给策略，支持修改策略启动参数值或者传入参数文件。

    监控界面修改策略实例参数回调
    :param params:参数，支持任意形式的文本参数
    :param path:如果传入的是参数文件，path为文件路径，否则path为空字符串
    :return:
    :remark:可选实现
    """
    pass


def handle_etf_estimate_info(context, etf_estimate_info, msg_type):
    """
    实时ETF预估信息接收函数
    :param context:上下文
    :param etf_estimate_info: EtfEstimateInfo对象
    :param msg_type 保留字段
    :return:
    :remark:可选实现
    """
    pass


def on_strategy_ready_stop(context):
    """
    category:事件回调
    brief:策略准备结束回调
    desc:策略准备结束回调，可选实现。停止策略时，会先调用此回调，调用结束后，再调用on_strategy_end回调。该回调中允许交易，不允许与外部系统交互，策略可选择在此回调函数中撤掉在途订单。
    :param context:
    :return:
    """
    pass


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
