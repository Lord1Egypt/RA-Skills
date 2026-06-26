# encoding: utf-8

from mquant_api import *
from mquant_struct import *
import json


def timer_func(context, interval, custom_param):
    """
    示例定时函数
    :param context: Context对象
    :param interval:周期型定时函数，该字段为定时时间间隔，单位为秒；单次定时函数，该字段为触发时间，类型为str，格式为hh:mm:ss
    :param custom_param:用户注册定时器时传入的自定义参数
    :return:无
    :example:定时撤单
    # 通过interval判断是否是撤单定时器触发，这里也可利用custom_param来判断，适用于存在多个定时器共用定时回调函数的场景；如果是单个定时器独立的回调函数，则无需判断
    # context.run_params内支持用户在strategy_params回调函数中的自定义参数，这里示例中使用了'撤单时间间隔'参数
    if interval == int(context.run_params['撤单时间间隔']):
        open_orders = get_open_orders()
        cancel_order_list = []
        for ord_id, order_item in open_orders.items():
            # 按照订单号撤单
            item = batch_cancel_order_item()
            item.order_id=order_item.order_id
            cancel_order_list.append(item)
        if len(cancel_order_list) > 0:
            log.debug('开始批量撤单，数量：%d' % len(cancel_order_list))
            cancel_orders(cancel_order_list)
            log.debug('批量撤单结束')
    """
    pass


def strategy_params():
    """
    category:事件回调
    brief:策略运行参数定义
    desc: 策略运行参数定义，可选实现。
    策略可自定义运行参数，启动策略时，会在启动弹框中显示策略自定义的参数，客户在界面修改参数值，修改后的参数会写入到context对象的run_params字段内，客户可在策略程序中通过context对象获取策略运行参数。
    目前支持int、float、string、list、table、bool等类型的参数。
    :return:dict对象，key为参数名，value为一个包含参数默认值、参数描述（选填）的字典
    :remark:可选实现，参数由策略自由填写，由策略平台解析显示在运行参数设置界面上，支持编辑框、下拉列表、勾选框三种形式的参数
    :example:
        dict_params = {
       '证券代码':{'value':'601688.SH/000002.SZ','desc':'策略交易的标的代码'},		               #string类型，对应编辑框，'desc'字段可填写，也可不填写
       '委买价格':{'value':'17.50/27.5'},                                                        #string类型，对应编辑框
       '委卖价格':{'value':'18.50/28.0'},                                                        #string类型，对应编辑框
       '补单价格档位':{'value':['最新价','对手方一档','对手方二档','对手方3档','涨停价','跌停价']},  #list类型，对应下拉列表
       '使用持仓':{'value': True, 'desc':'买入篮子时是否使用持仓中已有的成分券额度'},                #bool类型，对应勾选框
       '撤单时间间隔':{'value':10}                                                                #int类型，对应编辑框
       }
        return json.dumps(dict_params)
    """
    pass


def initialize(context):
    """
    category:事件回调
    category-desc:MQuant的事件处理引擎会将交易系统内的各种事件以回调函数的形式通知给策略脚本，策略脚本根据自身的业务逻辑在对应的回调函数中进行相应处理
    brief:初始化
    desc: 策略初始化，必须实现。启动策略时调用，用户可在初始化函数中订阅行情、设置标的、设置定时处理函数等。该函数中允许读取文件，除此之外的其他函数禁止读取文件。注意，初始化阶段禁止交易。

    :param context: Context对象
    :return:无
    :remark:此回调函数必须实现
    :example:
    *****************************获取传入的策略运行参数******************************
    # 这里对应的获取用户在strategy_params中自定义的参数，实际值以运行参数界面修改设置为准
    g.security_list=context.run_params['证券代码'].strip('/').split('/')
    lst_buy_price = context.run_params['买入价格'].strip('/').split('/')
    lst_sell_price = context.run_params['卖出价格'].strip('/').split('/')
    g.buy_dict = dict(zip(g.security_list,lst_buy_price))
    g.sell_dict = dict(zip(g.security_list,lst_sell_price))

    *****************************订阅行情，支持tick、分钟k、逐笔委托、逐笔成交，用户按需订阅即可*****************************
    subscribe(g.security_list)                              #订阅tick，在handle_tick回调函数中接收实时tick推送
    subscribe(g.security_list, MarketDataType.KLINE_1M)     #订阅分钟k，在handle_data回调函数中接收实时分钟k推送
    subscribe(g.security_list, MarketDataType.RECORD_ORDER) #订阅逐笔委托数据，在handle_order_record回调函数中接收实时逐笔委托推送并处理
    subscribe(g.security_list, MarketDataType.RECORD_TRANSACTION)   #订阅逐笔成交数据，在handle_record_transaction回调函数中接收实时逐笔成交推送并处理
    ###特别注意，逐笔委托和逐笔成交数据量较大，如果订阅的标的数量较多时，需要考虑网络带宽和机器的处理能力
    ############网络带宽方面建议申请独享带宽
    ############机器处理能力方面，可以考虑将标的池分为多份，拆分为对应的多个策略实例执行（利用CPU的多核并发处理能力）

    *****************************读取外部文件*****************************
    #如果需要读取外部文件，只能在初始化函数中读取，正式运行过程中不允许读取
    #这里以读取ini配置为例
    configValue = read_ini_config('./configFile/usrCfg.ini', 'TEST', 'key1') #读取csv配置,如果需要读取csv配置，只能在初始化函数中读取，正式运行过程中不允许读取
    csv_reader = open_csv_file('./configFile/testCsv.csv')
    count = 0
    for row in csv_reader:
        count = count + 1
        if count > 10:
            break
        csv_reader.reset()
        print('第5行：', csv_reader.getRow(5))
    csv_reader.close()
    ###特别注意，为了方便用户使用，mquant提供了读取ini和csv格式配置文件的接口，用户也可以根据自己的使用习惯，选择python原生的或第三方库提供的文件读取方法读取外部文件
    ############文件读取操作只能在初始化阶段进行，其他阶段禁止以任何形式访问外部文件、网络、数据库、进程间通信等

    *****************************查询k线，目前支持1分钟、5分钟、15分钟、30分钟、60分钟、日k等k线类型，支持前复权、后复权和除权类型的数据*****************************
    *****************************查询k线，提供两种查询方式，（1）查询指定日期范围的k线，（2）查询指定日期前/后N天k线的数据*****************************
    *****************************支持查询当日k线数据，支持按自然日和交易日查询，返回KLineData类型*****************************
    # 查询000009.SZ的前30个交易日的前复权日K线数据
    klinedata = get_kline_data_from_init_date('000009.SZ',-30,kline_type=KLineDataType.KLINEData_1D,fq='pre', date_type=DateType.TRADE_DATE)
    # 查询000009.SZ从20191202到20191206期间所有交易日的前复权日K线数据
    klinedata = get_kline_data('000009.SZ',20191202,20191206,kline_type=KLineDataType.KLINEData_1D,fq='pre', date_type=DateType.TRADE_DATE)

    *****************************注册定时信号*****************************
    *****************************支持两种定时信号注册方式，（1）注册周期定时信号，（2）注册指定时间点触发的单次定时信号*****************************
    #注册在9:30-10:00之间每5s触发一次的周期定时信号，回调函数为timer_func（可任意指定）
    run_timely(timer_func, 5, '09:30:00', '10:00:00', 'period timer,interval:5'))  
    #注册10s后执行的单次定时函数，回调函数为timer_func（可任意指定）  
    time=datetime.datetime.now() + datetime.timedelta(seconds=10)
    run_timely(timer_func,-1,time.strftime('%H:%M:%S'),'one shot timer,time:{}'.format(time.strftime('%H:%M:%S')))  
    ###特别注意：周期定时信号的触发逻辑是在程序中有一个计数器，计数%周期=0时触发回调，由于这个计数器是全局的，注册请求提交后的第一次定时信号与注册请求提交的间隔时间会<=定时周期
    ############周期定时信号中的开始时间和结束时间可以不填写，此时周期定时信号会在策略生命周期内一直周期触发

    *****************************回测环境设置（需要回测模式，暂不支持）*****************************
    #如果使用回测，切记一定要调用register_backtest_symbols函数
    register_backtest_symbols(g.security_list)
    """
    pass


def on_strategy_start(context):
    """
    category:事件回调
    category-desc:MQuant的事件处理引擎会将交易系统内的各种事件以回调函数的形式通知给策略脚本，策略脚本根据自身的业务逻辑在对应的回调函数中进行相应处理
    brief:策略启动回调
    desc:策略启动回调，可选实现。策略初始化结束后，会立即调用此回调函数，策略在此回调函数中可以进行交易等处理，不可读取外部文件、网络等。

    :param context: Context对象
    :return: 无
    :remark: 初始化函数返回后立即调用，在该回调函数中允许交易，不允许读取外部文件，可选实现
    """
    pass


def handle_tick(context, tick, msg_type):
    """
    category:事件回调
    brief:TICK行情回调
    desc:TICK行情回调，可选实现。调用subscribe订阅TICK行情后，在此函数中接收实时TICK行情推送。回测模式下，如果选择TICK级回测，回测行情也在此回调函数中接收处理。

    :param context: Context对象
    :param tick: Tick对象
    :param msg_type: 消息类型，暂不启用
    :return: 无
    :remark:可选实现
    """
    pass


def handle_data(context, kline_data):
    """
    category:事件回调
    brief:K线行情回调
    desc:K线行情回调，可选实现。调用subscribe订阅K线行情后，在此函数中接收实时K线行情推送。回测模式下，如果选择分钟K或者日K回测，回测行情也在此回调函数中接收处理。

    :param context: Context对象
    :param kline_data: KLineDataPush类型，回测模式下分钟k和日k都通过该函数接收推送
    :return:无
    :remark:可选实现
    """
    pass


def handle_order_record(context, order_record, msg_type):
    """
    category:事件回调
    brief:逐笔委托回调
    desc:逐笔委托回调，可选实现。调用subscribe订阅逐笔委托行情后，在此函数中接收实时的逐笔委托行情推送。回测模式不支持逐笔数据订阅。
    :param context: Context对象
    :param order_record: 逐笔委托数据，RecordOrder对象
    :param msg_type: 消息类型，暂不启用
    :return:无
    :remark:可选实现
    """
    pass


def handle_record_transaction(context, record_transaction, msg_type):
    """
    category:事件回调
    brief:逐笔成交回调
    desc:逐笔成交回调，可选实现。调用subscribe订阅逐笔成交行情后，在此函数中接收实时的逐笔成交行情推送。回测模式不支持逐笔数据订阅。
    :param context: Context对象
    :param record_transaction: 逐笔成交数据，RecordTransaction对象
    :param msg_type: 消息类型，暂不启用
    :return:无
    :remark:可选实现
    """
    pass


def handle_order_report(context, ord, msg_type):
    """
    category:事件回调
    brief:订单回报函数
    desc:订单回报函数，可选实现。策略报单后，只要订单状态改变，都会进入订单回报函数，策略可以在此函数中判断订单状态并决定后续操作，只要当前策略报单的订单回报都会通过此函数通知给策略。回测模式下，订单回报也在此函数中处理。
    如果需要处理策略对应资金账号的所有订单（包含非本策略下单场景），则需要在运行时勾选“账号级交易推送”
    :param context: Context对象
    :param ord: Order对象
    :param msg_type: 消息类型，暂不启用
    :return:无
    :remark:可选实现
    """
    pass


def handle_execution_report(context, execution, msg_type):
    """
    category:事件回调
    brief:成交回报函数
    desc:成交回报函数，可选实现。策略报单后，只要订单产生成交（可能分多笔成交），都会进入成交回报函数，策略可以在此函数中获取本次成交信息（成交价格、数量、金额等），只要当前策略报单的成交回报都会通过此函数通知给策略。回测模式下，成交回报也在此函数中处理。
    如果需要处理策略对应资金账号的所有成交（包含非本策略下单场景），则需要在运行时勾选“账号级交易推送”
    :param context: Context对象
    :param execution:Trade对象
    :param msg_type: 消息类型，暂不启用
    :return:无
    """
    pass


def on_fund_update(context, fund_info):
    """
    category:事件回调
    brief:资金推送
    desc:资金推送函数，可选实现。当账号对应的资金变化时，会主动推送资金信息，相对于成交有一定的延迟。
    :param context: Context对象
    :param fund_info: FundUpdateInfo 类对象
    :return:无
    """
    pass


def on_position_update(context, pos_info):
    """
    category:事件回调
    brief:持仓推送
    desc:持仓推送函数，可选实现。当账号对应的持仓变化时，会主动推送持仓信息，相对于成交有一定的延迟。
    :param context: Context对象
    :param pos_info: Position类对象
    :return:无
    """
    pass


def handle_fund_flow(context, fund_flow):
    """
    category:事件回调
    brief:实时资金流向推送
    desc:实时资金流向推送函数，可选实现。
    :param context: Context对象
    :param fund_flow:资金流向数据，FundFlow类型
    :return:无
    """
    pass


def on_strategy_params_change(params, path):
    """
    category:事件回调
    brief:参数修改回调
    desc:参数修改回调，可选实现。用户在策略执行监控界面的实例列表中，点击参数修改按钮修改实例参数时，参数信息会通过此回调通知给策略，支持修改策略启动参数值或者传入参数文件。

    :param params:参数，支持任意形式的文本参数
    :param path:如果传入的是参数文件，path为文件路径，否则path为空字符串
    :return:无
    :remark:可选实现
    """
    pass


def on_rsp_user_params(context, json_params, wnd_title):
    """
    category:事件回调
    brief:请求用户参数异步响应
    desc:策略调用get_user_params在界面弹出一个参数框（异步模式），用户修改参数后，点击确定，修改后的参数将通过此回调函数回传给策略
    使用场景示例：当用户策略逻辑处理中，需要在某个条件触发的时候，期望能够通过参数交互窗口进行指定数据的设置交互，则应该调用get_user_params弹出自定义的参数设置窗口，等待用户进行干预设置。设置后的参数会通过此回调函数通知策略。
    :param context: Context对象
    :param json_params: 设置参数，具体由用户通过get_user_params设置的json_params_template有关
    :param wnd_title: 界面弹窗的窗口名称
    :return:无
    :remark:可选实现
    """
    pass


def on_request_user_params_template(context, params):
    """
    category:事件回调
    brief:触发弹出用户参数设置窗口
    desc:用户在策略执行监控实例列表界面点击手工干预按钮，将会触发此回调函数，策略可以在此回调函数中获取用户参数，也可不实现
    :param context: Context对象
    :param params: 保留字段
    :return:无
    :remark:可选实现
    :example:
    # 可以结合get_user_params和on_rsp_user_params一起来实现主动的人工干预
    # 以下是一个持仓止损的干预参数示例
    param_template = {"left_layout":{"name":"操作表格","ui_type":"table","check_box":True,"columns":[{"name":"","ui_type":"check_box"},
    {"name":"证券代码","ui_type":"code_edit"},{"name":"持仓数量","ui_type":"line_edit","editable":"0"},
    {"name":"可用数量","ui_type":"line_edit","editable":"0"},{"name":"持仓均价","ui_type":"line_edit","editable":"0"},{"name":"止损价","ui_type":"line_edit"}],
    "rows":[[0,"600000.SH",5400,1800,29.15,29.15],[0,"000001.SZ",3800,3000,18.15,18.15]]}}
    get_user_params(json.dumps(param_template), "test111")
    # 这里就相当于在策略执行监控实例列表界面点击手工干预按钮，则主动弹出了参数设置窗口，在设置完成后，可在on_rsp_user_params中进行对应后续逻辑的处理
    """
    pass


def handle_etf_estimate_info(context, etf_estimate_info, msg_type):
    """
    category:事件回调
    brief:实时ETF预估信息接收函数
    desc:实时ETF预估信息接收函数,需要在ETF常用列表中增加对应代码，并在策略中通过subscribe订阅
    :param context: Context对象
    :param etf_estimate_info: EtfEstimateInfo对象
    :param msg_type: 消息类型，暂不启用
    :return:无
    :remark:可选实现
    """
    pass


def market_open(context, trade_date):
    """
    category:事件回调
    brief:开盘信号
    desc:开盘信号，可选实现。回测模式下，回测周期内的每个交易日开始时，都会发送一个开盘信号给策略，策略在此回调函数中进行每日初始化操作。注意，仅回测模式有效。
    开盘信号，回测专用，在该回调中进行每日初始化操作，例如查询数据，处理静态数据等，日k回测在该回调函数中报单时，订单在当日撮合，在handle_data中报单时，订单在下一个交易日撮合
    :param context: Context对象
    :param trade_date:当前交易日
    :return:无
    :remark:可选实现
    """
    pass


def market_close(context, trade_date):
    """
    category:事件回调
    brief:收盘信号
    desc:收盘信号，可选实现。回测模式下，回测周期内的每个交易日结束时，都会发送一个收盘信号给策略，策略在此回调函数中进行每日日终操作。注意，仅回测模式有效。
    收盘信号,回测专用
    :param context: Context对象
    :param trade_date: 交易日
    :return:无
    :remark:可选实现
    """
    pass


def on_strategy_ready_stop(context):
    """
    category:事件回调
    brief:策略准备结束回调
    desc:策略准备结束回调，可选实现。停止策略时，会先调用此回调，调用结束后，再调用on_strategy_end回调。该回调中允许交易，不允许与外部系统交互，比如策略可按需选择在此回调函数中撤掉在途订单等。
    :param context: Context对象
    :return:无
    :remark:可选实现
    """
    pass


def on_strategy_end(context):
    """
    category:事件回调
    brief:策略结束回调
    desc:策略结束回调，可选实现。策略实例终止时，MQuant会调用此回调函数通知策略进行一些数据保存、环境清理等工作，待策略的处理工作结束后再结束策略进程。特别注意，如果直接关闭策略进程，可能导致此函数未执行完毕进程就已经关闭，建议通过策略执行监控界面或者通过stop_strategy API终止策略。
    策略结束时调用，用户可以在此函数中进行一些汇总分析、环境清理等工作
    :param context: Context对象
    :return:无
    :remark:可选实现
    """
    pass


def on_recv_order_reply(context, order_reply):
    """
    category:事件回调
    brief:报撤单异步响应
    desc:报撤单异步响应，可选实现。必须调用set_enable_order_reply(True)开启响应消息推送后，才可收到响应。set_enable_order_reply是全局开关，任何一个实例调用此接口设置后，其他实例都会受影响。
    可以按策略逻辑需要，在此处理一些报单异常错误
    :param context: Context对象
    :param order_reply: OrderReply对象
    :return:无
    :remark:可选实现
    """
    pass

def on_system_msg(context, error_code, error_msg):
    """
    category:事件回调
    brief:系统消息
    desc:系统消息,可选实现。当客户端出现网络断线重连等场景，会通过此回调函数通知策略。
    目前支持的系统消息
    1、error_code：0，error_msg：insight gateway reconnected，行情网络重连成功
    2、error_code：-1，error_msg：insight gateway is connecting，行情网络正在重连
    3、error_code：0，error_msg：trade gateway reconnected，交易网络重连成功
    4、error_code：-1，error_msg：trade gateway is connecting，交易网络正在重连
    5、error_code：0，error_msg：insight grpc gateway reconnected，行情查询网络重连成功
    6、error_code：-1，error_msg：insight grpc gateway is connecting，行情查询网络正在重连
    7、error_code：0，error_msg：xinfo gateway reconnected，资讯网络重连成功
    8、error_code：-1，error_msg：xinfo gateway is connecting，资讯网络正在重连
    :param context: Context对象
    :param error_code: 错误码
    :param error_msg: 错误信息
    :return:无
    :remark:可选实现
    """
    pass