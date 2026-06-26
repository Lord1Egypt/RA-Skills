# encoding: utf-8

from mquant_api import *
from mquant_struct import *
import json
from datetime import datetime

# InsightSDK的安装及申请请参考以下网址或联系客户经理
# https://findata-insight.htsc.com:9151/insight_help/sdk/SDKDownload/

from insight_python.com.interface.mdc_gateway_base_define import GateWayServerConfig
from insight_python.com.insight import common, subscribe
from insight_python.com.insight.subscribe import *
from insight_python.com.insight.market_service import market_service
from insight_python.com.insight.query import *

# InsightSDK的回调
# ************************************处理数据订阅返回结果************************************
class insightmarketservice(market_service):

    def on_subscribe_tick(self, result):
        # pass
        print("接收到Tick数据：", result)
		# 具体字段可参考https://findata-insight.htsc.com:9151/insight_help/python_dataDictionary/stockData/StockTick/

    def on_subscribe_kline(self, result):
        # pass
        print("接收到KLine数据：", result)
		# 具体字段可参考https://findata-insight.htsc.com:9151/insight_help/python_dataDictionary/stockData/StockKLine/

    def on_subscribe_trans_and_order(self, result):
        # pass
		# data_type字段区分逐笔委托（order）、逐笔成交（transaction）
        print("接收到逐笔数据：", result)
		# 具体字段可参考https://findata-insight.htsc.com:9151/insight_help/python_dataDictionary/stockData/StockPen/

          
# ************************************初始化InsightSDK************************************    
def init_insight_sdk():
    print(common.get_version())    # (非必须)当前InsightSDK版本号
    
    # 登录
    markets = insightmarketservice()  # 回调
    user = "username"
    password = "password"
    # user        用户名
    # password    密码
    # login_log    登录日志，默认False
    result = common.login(markets, user, password, login_log=False)
#    result = common.loginSIT(markets, user, password, login_log=False)
    print(result)
    
    # 配置日志开关
    # open_trace trace    日志开关                True为打开日志False关闭日志
    # open_file_log        本地file日志开关     True为打开日志False关闭日志
    # open_cout_log        控制台日志开关        True为打开日志False关闭日志
    open_trace = False
    open_file_log = False
    open_cout_log = False
    common.config(open_trace, open_file_log, open_cout_log)



# ************************************行情订阅Demo************************************    
# 异步接口，返回函数在insightmarketservice
def subscribe_tick_by_type_demo():
    """
    根据证券类型订阅Tick数据
    :param query: 交易市场及对应的证券类型，元组类型，支持多市场多交易类型订阅，list类型 [(exchange1,security_type1),(exchange2,security_type2)]
    :param mode: 订阅方式 覆盖(coverage)， 新增（add）， 减少(decrease)， 取消(cancel)， 默认为coverage
    """

    query = [('XSHG', 'stock'), ('XSHE', 'stock')]
    mode = 'add'

    subscribe_tick_by_type(query=query, mode=mode)


def subscribe_kline_by_type_demo():
    """
    根据证券类型订阅K线数据
    :param query: 交易市场及对应的证券类型，元组类型，支持多市场多交易类型订阅，list类型 [(exchange1,security_type1),(exchange2,security_type2)]
    :param mode: 订阅方式  覆盖(coverage)， 新增（add）， 减少(decrease)， 取消(cancel)， 默认为coverage
    :param frequency: 频率，list类型，秒K（15s），分钟K（‘1min’）
    """

    query = [('XSHG', 'stock'), ('XSHE', 'stock')]
    mode = 'add'
    frequency = ["15s", "1min"]

    subscribe_kline_by_type(query=query, frequency=frequency, mode=mode)


def subscribe_trans_and_order_by_type_demo():
    """
    根据证券类型订阅逐笔数据
    :param query: 交易市场，支持多市场查询，list类型 [(exchange1,security_type1),(exchange2,security_type2)]
    :param mode: 订阅方式 覆盖(coverage)， 新增（add）， 减少(decrease)， 取消(cancel)， 默认为coverage
    """

    query = [('XSHG', 'stock'), ('XSHE', 'stock')]
    mode = 'coverage'

    subscribe_trans_and_order_by_type(query=query, mode=mode)
    
    
def subscribe_tick_by_id_demo():
    """
    根据证券ID订阅Tick数据
    :param htsc_code: 华泰证券ID，支持多ID查询，list类型
    :param mode: 订阅方式 覆盖(coverage)， 新增（add）， 减少(decrease)， 取消(cancel)， 默认为coverage
    """

    htsc_code = ['601688.SH', '603980.SH']
    mode = 'add'

    subscribe_tick_by_id(htsc_code=htsc_code, mode=mode)


def subscribe_kline_by_id_demo():
    """
    根据证券ID订阅K线数据
    :param htsc_code: 华泰证券ID，支持多ID订阅，list类型
    :param mode: 订阅方式 覆盖(coverage)， 新增（add）， 减少(decrease)， 取消(cancel)， 默认为coverage
    :param frequency: 频率，list类型，秒K（15s），分钟K（‘1min’）
    """

    htsc_code = ['601688.SH', '000001.SZ']
    mode = 'add'
    frequency = ["15s", "1min"]

    subscribe_kline_by_id(htsc_code=htsc_code, frequency=frequency, mode=mode)


def subscribe_trans_and_order_by_id_demo():
    """
    根据证券ID订阅逐笔数据
    :param htsc_code: 华泰证券ID，支持多ID订阅，list类型
    :param mode: 订阅方式
    """

    htsc_code = ['601688.SH', '603980.SH']
    mode = 'add'

    subscribe_trans_and_order_by_id(htsc_code=htsc_code, mode=mode)
    
    
# ************************************行情查询Demo************************************    
def get_kline_demo():
    """
    查询证券的分钟K，日K，周K，月K数据
    :param htsc_code: 华泰证券代码，支持多个code查询，列表类型
    :param time: 时间范围，list类型，开始结束时间为datetime
    :param frequency: 频率，分钟K（‘1min’，’5min’，’15min’，’60min’），日K（‘daily’），周K（‘weekly’），月K（‘monthly’）
    :param fq: 复权，默认前复权”pre”，后复权为”post”，不复权“none”
    :return:pandas.DataFrame
    """

    time_start_date = "2023-08-16 15:10:11"
    time_end_date = "2024-08-18 11:20:50"
    time_start_date = datetime.strptime(time_start_date, '%Y-%m-%d %H:%M:%S')
    time_end_date = datetime.strptime(time_end_date, '%Y-%m-%d %H:%M:%S')

    # time_start_date = "2021-01-14"
    # time_end_date = "2022-10-20"
    # time_start_date = datetime.strptime(time_start_date, '%Y-%m-%d')
    # time_end_date = datetime.strptime(time_end_date, '%Y-%m-%d')

    result = get_kline(htsc_code=["510050.SH", "601688.SH"], time=[time_start_date, time_end_date],
                       frequency="daily", fq="none")
    print("查询KLine数据结果：", result)
    
    
def get_tick_demo():
    """
    查询tick数据
    :param htsc_code: 华泰证券ID（沪深市场标的）
    :param trading_day: 时间范围
    :param security_type: 证券类型（stock,index,fund,bond,option）
    :return: pandas.DataFrame
    """

    htsc_code = '600000.SH'
    security_type = 'stock'

    # htsc_code = '000001.SH'
    # security_type = 'index'

    # htsc_code = '501000.SH'
    # security_type = 'fund'

    # htsc_code = '010504.SH'
    # security_type = 'bond'
    #
    # htsc_code = '10004679.SH'
    # security_type = 'option'

    start_date = "2024-09-10"
    end_date = "2024-09-12"
    start_date = datetime.strptime(start_date, '%Y-%m-%d')
    end_date = datetime.strptime(end_date, '%Y-%m-%d')

    result = get_tick(htsc_code=htsc_code,
                      security_type=security_type,
                      trading_day=[start_date, end_date])
    print("查询Tick数据结果：", result)
    
    
def timer_func(context, interval, custom_param):
    """
    示例定时函数
    :param context:
    :param interval 周期型定时函数，该字段为定时时间间隔，单位为秒；单次定时函数，该字段为触发时间，类型为str，格式为hh:mm:ss
    :param custom_param 用户注册定时器时传入的自定义参数
    :return:
    :remark:用户函数，可写可不写
    :example:定时撤单
    if interval == int(context.run_params['撤单时间间隔']):
        open_orders = get_open_orders(msg_type)
        cancel_order_list = []
        for ord_id, order_item in open_orders.items():
        # 判断如果是限价单，则撤单
            item = batch_cancel_order_item()
            item.order_id=order_item.order_id
            cancel_order(order_item)
            cancel_order_list.append(item)
        if len(cancel_order_list) > 0:
            log.debug('开始批量撤单，数量：%d' % len(cancel_order_list))
            cancel_orders(cancel_order_list)
            log.debug('批量撤单结束')
    """
    print("定时函数", interval, datetime.now().strftime('%Y-%m-%d %H:%M:%S %f'))


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
       '使用持仓':{'value': True, 'desc':'买入篮子时是否使用持仓中已有的成分券额度'},                #bool类型参数
       '撤单时间间隔':{'value':10}                                                                #编辑框类型参数
       }
        return json.dumps(dict_params)
    """
    pass


def initialize(context):
    """
    category:事件回调
    category-desc:MQuant的事件处理引擎会将交易系统内的各种事件以回调函数的形式通知给策略脚本，策略脚本根据自身的业务逻辑在对应的回调函数中进行相应处理
    brief:初始化
    desc: 策略初始化，必须实现。启动策略时调用，用户可在初始化函数中订阅行情、设置标的、设置定时处理函数等 该函数中允许读取文件，除此之外的其他函数禁止读取文件。注意，初始化阶段禁止交易。
    """

    # 初始化Insight_SDK
    init_insight_sdk()
    
# 订阅接口调用测试，实际使用时按需参考下列各Demo函数中的使用方法
    subscribe_tick_by_id_demo()
#    subscribe_tick_by_type_demo()
#    subscribe_kline_by_id_demo()
#    subscribe_kline_by_type_demo()
#    subscribe_trans_and_order_by_id_demo()
#    subscribe_trans_and_order_by_type_demo()


# 说明：如果使用Insight_SDK查询数据，需要pandas的版本0.25.0以上，具体可以在“策略工具”菜单查看版本信息。
#       若版本较低，可手动进行删除后，重新安装，目前python3.6.2下最新pandas版本1.1.5
# 查询接口测试,其余数据查询示例可参考Insight网站说明。
#    get_tick_demo()
#    get_kline_demo()

    # 因为此处insightSDK订阅接口存在一定的耗时，如果是多次调用接口进行订阅，可能存在后面的订阅还未完成，前面订阅已经开始推送回调了，在回调处理中需要注意此时策略还未初始化完成，避免引发处理上的问题。
    # 按实际需要进行启动定时器等，这里建议在订阅之后开启定时器，否则可能会因为订阅的耗时导致定时器事件阻塞积压
    run_timely(timer_func, 5)


def on_strategy_start(context):
    """
    category:事件回调
    category-desc:MQuant的事件处理引擎会将交易系统内的各种事件以回调函数的形式通知给策略脚本，策略脚本根据自身的业务逻辑在对应的回调函数中进行相应处理
    brief:策略启动回调
    desc:策略启动回调，可选实现。策略初始化结束后，会立即调用此回调函数，策略在此回调函数中可以进行交易，不可读取外部文件、网络等。

    策略正式启动回调
    :param context:
    :return:
    :remark: 初始化函数返回后立即调用，在该回调函数中允许交易，不允许读取外部文件，可选实现
    """
    pass


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
	# 使用InsightSDK模式下，订阅的tick数据应该在insightmarketservice的on_subscribe_tick回调函数中处理


def handle_data(context, kline_data):
    """
    category:事件回调
    brief:K线行情回调
    desc:K线行情回调，可选实现。调用subscribe订阅1分钟K线行情后，在此函数中接收实时的分钟K线行情推送。回测模式下，如果选择分钟K或者日K回测，回测行情也在此回调函数中接收处理。
    k线数据接收函数，包含实时分钟k，回测模式下的分钟k和日k
    :param context:
    :param kline_data:KLineDataPush类型，回测模式下分钟k和日k都通过该函数接收推送
    :return:
    :remark:可选实现
    """
    pass
	# 使用InsightSDK模式下，订阅的K线数据应该在insightmarketservice的on_subscribe_kline回调函数中处理


def handle_order_record(context, order_record, msg_type):
    """
    category:事件回调
    brief:逐笔委托回调
    desc:逐笔委托回调，可选实现。调用subscribe订阅逐笔委托行情后，在此函数中接收实时的逐笔委托行情推送。回测模式不支持逐笔数据订阅。
    处理逐笔委托
    :param context: Context对象
    :param order_record: 逐笔委托数据，RecordOrder对象
    :param msg_type:
    :return:
    :remark:可选实现
    """
    pass
	# 使用InsightSDK模式下，订阅的逐笔数据应该在insightmarketservice的on_subscribe_trans_and_order回调函数中处理


def handle_record_transaction(context, record_transaction, msg_type):
    """
    category:事件回调
    brief:逐笔成交回调
    desc:逐笔成交回调，可选实现。调用subscribe订阅逐笔成交行情后，在此函数中接收实时的逐笔成交行情推送。回测模式不支持逐笔数据订阅。
    处理逐笔成交
    :param context: Context对象
    :param record_transaction: 逐笔成交数据，RecordTransaction对象
    :param msg_type: 保留
    :return:
    :remark:可选实现
    """
    pass
	# 使用InsightSDK模式下，订阅的逐笔数据应该在insightmarketservice的on_subscribe_trans_and_order回调函数中处理
	

def on_strategy_ready_stop(context):
    """
    category:事件回调
    brief:策略准备结束回调
    desc:策略准备结束回调，可选实现。停止策略时，会先调用此回调，调用结束后，再调用on_strategy_end回调。该回调中允许交易，不允许与外部系统交互，策略可选择在此回调函数中撤掉在途订单。
    :param context:
    :return:
    """
    
    # 退出释放资源，可以在on_strategy_ready_stop或者on_strategy_end进行调用
	print("开始释放InsightSDK资源", datetime.now().strftime('%Y-%m-%d %H:%M:%S %f'))
    if GateWayServerConfig.IsRealTimeData:
        subscribe.sync()
    common.fini()
	print("完成释放InsightSDK资源", datetime.now().strftime('%Y-%m-%d %H:%M:%S %f'))


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

