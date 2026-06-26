# encoding: utf-8

from mquant_api import *
from mquant_struct import *
import json
import os
import time
import threading
import shutil
from TradeDataDownload import TradeDataDownloader


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
        '算法文件路径': {
            'value': '.\\M-quant\\masterjyyqxm\\算法交易\\SMARTTWAP算法参数.csv',
            'desc': '算法参数文件路径，支持相对路径和绝对路径'},
        '启动时间': {'value': '09:30:00', 'desc': '启动后，策略会在初始化函数中一直堵塞等待，直到设定的时间再读取算法文件创建算法实例。如果当前时间大于设置的启动时间，则立即读取并创建实例'},
        # '批量创建': {'value': False, 'desc': '勾选批量创建时，从文件中读取到有多个标的，将会为每一只标的创建一个算法实例，默认创建一个多标的算法实例'},
        '单实例最大标的数': {'value': 300,
                     'desc': '单个算法实例最大能支持的标的数，算法平台单个实例最多支持300只标的，可以设置1-300，不在此范围内的整数将会失效，系统将采用默认一个实例最大300只标的来创建'},
        '交易数据落文件': {'value': True, 'desc': '是否需要将交易数据下载到文件中'},
        '仅下载MQuant订单': {'value': False, 'desc': '如果为False，表示下载勾选资金账号的所有订单，如果为True，则只下载inst_id不为空的订单'}
    }
    return json.dumps(dict_params)


def parser_algo_param_file(param_file):
    """
    解析算法参数文件
    :param param_file:
    :return:
    """
    with open(param_file, 'r', encoding='utf-8') as f:
        param_list = f.readlines()
        if len(param_list) < 4:
            log.error('不合法的算法参数文件，算法参数文件至少应该有4行，当前文件共{}行'.format(len(param_list)))
            return
        # 首先读取第一行标题
        # 资金账号,算法类型,开始时间,结束时间,交易方向,委托类型,最大市场占比,参与集合竞价比例,风格参数,涨停不卖跌停不买,备注
        general_algo_param_list = param_list[1].strip(',\n').split(',')
        #        print(param_list[1], general_algo_param_list)
        if len(general_algo_param_list) < 4:
            log.error('算法参数格式错误，算法基础参数至少应包含资金账号、算法类型、开始时间、结束时间,且以逗号分隔，当前算法基础参数为：{}'.format(param_list[1]))
            return

        fund_account = general_algo_param_list[0]
        algo_type = general_algo_param_list[1]
        if algo_type == 'AITWAP':
            algo_type = AlgoType.AITWAP
        elif algo_type == 'AIVWAP':
            algo_type = AlgoType.AIVWAP
        elif algo_type == 'SMARTTWAP':
            algo_type = AlgoType.SMARTTWAP
        else:
            log.error('暂不支持的算法类型[{}]，请与Matic技术支持联系'.format(algo_type))
            return

        g.algo_request_list['algo_type'] = algo_type
        g.algo_request_list['fund_account'] = fund_account
        g.algo_request_list['req_list'] = []
        algo_params_str_prefix = ','.join(general_algo_param_list[2:])

        cnt = 0
        algo_params_str = algo_params_str_prefix
        for param_line in param_list[3:]:
            if len(param_line) > 0:
                algo_params_str = algo_params_str + ';' + param_line.strip(',\n')
                cnt = cnt + 1
                if cnt == g.max_symbol_cnt_per_algo_inst:
                    g.algo_request_list['req_list'].append(algo_params_str)
                    algo_params_str = algo_params_str_prefix
                    cnt = 0

        if cnt > 0:
            g.algo_request_list['req_list'].append(algo_params_str)


def proc_split_order_algo_msg(algo_type, fund_account, params):
    """
    处理算法创建消息
    """
    print('recv algo params', params, fund_account)
    params_list = params.split(";")
    if len(params_list) < 2:
        log.error('不合法的算法参数，算法类型：{}，参数：{}'.format(algo_type, params))
        return

    algo_base_params_list = params_list[0].split(',')
    if len(algo_base_params_list) < 9 and (algo_type == AlgoType.AITWAP or algo_type == AlgoType.AIVWAP):
        log.error(
            "算法基础参数格式不合法，请按照'开始时间(yyyy-MM-dd hh:mm:ss),结束时间(yyyy-MM-dd hh:mm:ss),交易方向(1：买入，2：卖出),委托类型,最大市场占比,参与集合竞价比例,风格参数,涨停不卖跌停不买,备注'传入算法基础参数")
        return

    elif len(algo_base_params_list) < 13 and algo_type == AlgoType.SMARTTWAP:
        log.error(
            "算法基础参数格式不合法，请按照'开始时间(yyyy-MM-dd hh:mm:ss),结束时间(yyyy-MM-dd hh:mm:ss),交易方向(1：买入，2：卖出),委托类型,最大市场占比,单笔最小委托数量,单笔最大委托数量,撤单模式,委托间隔,撤单时间,委托档位,涨跌停委托控制,备注'传入算法基础参数")
        return

    split_algo_param = SplitOrderAlgoParam()
    split_algo_param.algo_type = algo_type

    try:
        split_algo_param.start_time = datetime.datetime.strptime(algo_base_params_list[0], '%Y-%m-%d %H:%M:%S')
    except Exception as e:
        log.error('开始时间[{}]格式非法，请按照yyyy-MM-dd hh:mm:ss格式填写'.format(algo_base_params_list[0]))
        return

    try:
        split_algo_param.end_time = datetime.datetime.strptime(algo_base_params_list[1], '%Y-%m-%d %H:%M:%S')
    except Exception as e:
        log.error('结束时间[{}]格式非法，请按照yyyy-MM-dd hh:mm:ss格式填写'.format(algo_base_params_list[1]))
        return

    side = algo_base_params_list[2]
    if side == '1':
        split_algo_param.order_side = OrderSide.BUY
    elif side == '2':
        split_algo_param.order_side = OrderSide.SELL
    else:
        log.error('算法参数错误，非法的订单方向：{}'.format(side))
        return

    split_algo_param.entrust_type = algo_base_params_list[3]
    split_algo_param.max_market_ratio = float(algo_base_params_list[4])

    if algo_type == AlgoType.AITWAP or algo_type == AlgoType.AIVWAP:
        split_algo_param.call_auction_ratio = float(algo_base_params_list[5])
        split_algo_param.style = int(algo_base_params_list[6])
        if algo_base_params_list[7] == '0':
            split_algo_param.forbidden_limit = False
        elif algo_base_params_list[7] == '1':
            split_algo_param.forbidden_limit = True
        else:
            log.warn('警告，算法参数【涨停不卖跌停不买】值【{}】有误，该参数将会被设置为【否】'.format(algo_base_params_list[7]))

        split_algo_param.remark = algo_base_params_list[8]
    elif algo_type == AlgoType.SMARTTWAP:

        split_algo_param.min_order_qty = int(algo_base_params_list[5])
        split_algo_param.max_order_qty = int(algo_base_params_list[6])
        split_algo_param.withdraw_type = int(algo_base_params_list[7])
        split_algo_param.entrust_interval = int(algo_base_params_list[8])
        split_algo_param.withdraw_interval = int(algo_base_params_list[9])
        split_algo_param.entrust_price_level = int(algo_base_params_list[10])
        if algo_base_params_list[11] == '0':
            split_algo_param.limit_price_entrust_forbidden = False
        elif algo_base_params_list[11] == '1':
            split_algo_param.limit_price_entrust_forbidden = True
        else:
            log.warn('警告，算法参数【涨跌停委托控制】值【{}】有误，该参数将会被设置为【是】'.format(algo_base_params_list[11]))
        split_algo_param.remark = algo_base_params_list[12]
        pass

    # 算法订单列表
    for ord_str in params_list[1:]:
        order_param_list = ord_str.split(',')
        if len(order_param_list) < 3:
            log.error("不合法的算法证券信息:{},请按照'证券代码,数量,限价价格'格式填写".format(ord_str))
            continue
        symbol = order_param_list[0]
        qty = int(order_param_list[1])
        limit_price = float(order_param_list[2])

        order_item = AlgoOrderInfo()
        order_item.symbol = symbol
        order_item.amount = qty
        order_item.limit_price = limit_price
        split_algo_param.order_list.append(order_item)

        if len(split_algo_param.order_list) == 300:
            print('create algo instance')
            rsp = AlgoTradeHandler.start_split_order_algo_instance(g.account_type_info[fund_account], split_algo_param)
            log.info('创建算法[{}]返回：{},{}'.format(algo_type, rsp.inst_id, rsp.err_info))
            split_algo_param.order_list.clear()

    print('create algo instance')
    rsp = AlgoTradeHandler.start_split_order_algo_instance(g.account_type_info[fund_account], split_algo_param)
    log.info('创建算法[{}]返回：{},{}'.format(algo_type, rsp.inst_id, rsp.err_info))


def initialize(context):
    """
    初始化函数
    :param context:
    :return:
    """
    fund_account_stock = context.get_fund_account_by_type(AccountType.normal)
    g.account_type_info = {}
    if fund_account_stock is not None and len(fund_account_stock) > 0:
        g.account_type_info[fund_account_stock] = AccountType.normal

    fund_account_margin = context.get_fund_account_by_type(AccountType.margin)
    if fund_account_margin is not None and len(fund_account_margin) > 0:
        g.account_type_info[fund_account_margin] = AccountType.margin

    g.algo_params_file_path = context.run_params['算法文件路径']
    g.start_time = context.run_params['启动时间']
    g.max_symbol_cnt_per_algo_inst = int(context.run_params['单实例最大标的数'])
    if g.max_symbol_cnt_per_algo_inst <= 0:
        g.max_symbol_cnt_per_algo_inst = 300
    elif g.max_symbol_cnt_per_algo_inst > 300:
        g.max_symbol_cnt_per_algo_inst = 300

    #    print(g.algo_params_file_path)
    g.download_trade_data = False
    if context.run_params['交易数据落文件'] == '1':
        g.download_trade_data = True
    g.trade_data_downloader = None
    if g.download_trade_data:
        g.trade_data_downloader = TradeDataDownloader()
        g.trade_data_downloader.set_context(context)
        g.trade_data_downloader.set_file_dir_path('D:\\MQuantTradeData')
        g.trade_data_downloader.init_trade_files()

        if context.run_params['仅下载MQuant订单'] == '1':
            g.trade_data_downloader.only_download_mquant_order(True)
        else:
            g.trade_data_downloader.only_download_mquant_order(False)
    # print(g.batch_algo_flag, context.run_params)

    # 判断当前时间是否可以开始读文件，如果还不能开始，则阻塞等待
    cur_time = datetime.datetime.now().strftime('%H:%M:%S')
    g.algo_request_list = {}
    if len(g.algo_params_file_path) > 0:
        while cur_time < g.start_time:
            # print('等待设定时间', cur_time, start_time)
            time.sleep(1)
            cur_time = datetime.datetime.now().strftime('%H:%M:%S')
        #        print(g.algo_params_file_path)
        # 读取算法参数文件，并创建算法实例

        parser_algo_param_file(g.algo_params_file_path)


def on_strategy_start(context):
    """
    策略正式启动回调
    :param context:
    :return:
    :remark: 初始化函数返回后立即调用，在该回调函数中允许交易，不允许读取外部文件，可选实现
    """
    algo_type = g.algo_request_list.get('algo_type')
    if algo_type is None:
        return
    fund_account = g.algo_request_list.get('fund_account')
    if fund_account is None:
        return
    req_list = g.algo_request_list.get('req_list')
    if req_list is None:
        return
    for algo_request in req_list:
        proc_split_order_algo_msg(algo_type, fund_account, algo_request)


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
        if g.trade_data_downloader is not None:
            g.trade_data_downloader.on_order_update(ord)
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
        if g.trade_data_downloader is not None:
            g.trade_data_downloader.on_execution_update(execution)
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
        # print('recv fund update:', fund_info.__dict__)
        if g.trade_data_downloader is not None:
            g.trade_data_downloader.on_fund_update(fund_info)
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
    try:
        if g.trade_data_downloader is not None:
            g.trade_data_downloader.on_position_update(pos_info)
    except:
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
