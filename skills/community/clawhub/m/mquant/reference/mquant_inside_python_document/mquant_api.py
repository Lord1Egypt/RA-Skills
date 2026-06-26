#!/usr/bin/env python
# -*- coding: utf-8 -*-


from HTSAFuncImpl import *
from HTSACsvReader import *
from mquant_struct import *
from htstructdef import *

"""
日志接口
"""


class log(object):
    """
    category:日志接口
    category-desc:日志模块,与python的logging模块用法基本一致,支持自定义日志,将系统日志和用户策略日志分隔开,方便客户查看
    """

    @staticmethod
    def error(content, label=''):
        """
        brief:错误日志
        desc:记录错误日志,label不为空表示记录到label对应的自定义日志文件中,默认输出到MQuant界面及系统日志中
        :param content:日志内容
        :param label:日志标签,不同标签的日志会记录到对应的日志文件中
        :return:
        """
        return logImpl(LOG_LEVEL.ERROR, content, label)

    @staticmethod
    def warn(content, label=''):
        """
        brief:告警日志
        desc:记录告警日志,label不为空表示记录到label对应的自定义日志文件中,默认输出到MQuant界面及系统日志中
        :param content:日志内容
        :param label:日志标签,不同标签的日志会记录到对应的日志文件中
        :return:
        """
        return logImpl(LOG_LEVEL.WARNING, content, label)

    @staticmethod
    def info(content, label=''):
        """
        brief:运行信息日志
        desc:记录运行信息日志,label不为空表示记录到label对应的自定义日志文件中,默认输出到MQuant界面及系统日志中
        :param content:日志内容
        :param label:日志标签,不同标签的日志会记录到对应的日志文件中
        :return:
        """
        return logImpl(LOG_LEVEL.INFO, content, label)

    @staticmethod
    def debug(content, label=''):
        """
        brief:调试日志
        desc:记录调试日志,label不为空表示记录到label对应的自定义日志文件中,默认输出到MQuant界面及系统日志中
        :param content:日志内容
        :param label:日志标签,不同标签的日志会记录到对应的日志文件中
        :return:
        """
        return logImpl(LOG_LEVEL.DEBUG, content, label)

    @staticmethod
    def register_strategy_report_file(file_path, label):
        """
        brief:注册自定义日志文件
        desc:注册自定义日志文件,该接口实现将日志文件file_path和label绑定,后续写入日志时,只需要传入label就可以写入到对应的日志文件中。
            所有的日志输出接口，若需要指定日志文件，均需要注册后使用。
        :param file_path:文件路径,支持相对路径和绝对路径,相对路径为相对于软件根目录的路径,注意,一定要保证文件目录存在,否则写入文件会失败
        :param label:标签,相当于file_path的别名
        :return:None
        """
        register_strategy_report_file_impl(file_path, label)

    @staticmethod
    def set_log_level(log_level, lable=''):
        """
        brief:设置日志等级
        desc:设置日志文件记录日志等级,低于设置级别的日志不记录,仅支持控制策略日志,系统日志不受约束,默认等级为DEBUG
        :param log_level:LOG_LEVEL 类型
        :param label:日志标签,不同标签的日志级别设置互不影响
        :return:
        """
        return set_log_level_impl(log_level, lable)

    @staticmethod
    def set_console_log_level(log_level, lable=''):
        """
        brief:设置控制台日志等级
        desc:设置控制台日志等级,低于设置等级的日志不显示在控制台,仅支持控制策略日志,默认等级为DEBUG,调用此接口设置用户自定义日志的等级会自动开启控制台输出
        :param log_level:LOG_LEVEL 类型
        :param lable:日志标签,不同标签的日志级别设置互不影响
        :return:
        """
        return set_console_log_level_impl(log_level, lable)

    @staticmethod
    def enable_console_output(enable, label=''):
        """
        brief:设置控制台日志输出开关
        desc:设置控制台日志输出开关,系统日志（label为空）默认输出到控制台,用户自定义日志（label不为空）默认不允许
        :param enable: bool类型,True开启,False关闭
        :param label:日志标签,不同标签的日志级别设置互不影响
        :return:
        """
        enable_console_output_impl(enable, label)

    @staticmethod
    def clean_log_file(label):
        """
        brief:清空日志文件
        desc:清空指定label对应的日志文件中的全部内容
        :param label:日志标签
        :return:
        """
        clean_log_impl(label)

    @staticmethod
    def set_disp_log_level(log_level):
        """
        brief:设置界面日志等级
        desc:设置当前策略输出到matic界面的日志级别,默认为DEBUG
        :param log_level:LOG_LEVEL 类型
        :return:
        """
        set_disp_log_level_impl(log_level)

    @staticmethod
    def flush():
        """
        brief:强制输出缓冲区内容到日志文件
        desc:强制将缓存中的策略日志写入文件
        """
        flush_log_impl()

    @staticmethod
    def set_sys_log_level(log_level):
        """
        brief:设置系统日志级别
        desc:设置系统日志级别,默认为DEBUG
        :param log_level:LOG_LEVEL 类型
        :return:
        """
        set_sys_log_level_impl(log_level)



"""
行情接口
"""


def subscribe(security, frequency='tick'):
    """
    category:行情接口
    category-desc:行情接口,支持level-2实时行情、深市逐笔委托、沪深逐笔成交、分钟k的实时订阅推送,支持历史k线查询,包括1分钟、5分钟、15分钟、30分钟、60分钟、日线等各种粒度的k线数据
    brief:行情订阅
    desc:行情订阅,支持单标的和列表订阅,frequency参数为MarketDataType类的成员变量。
    :param security: 支持股票代码及股票代码列表,股票代码格式支持聚宽和mquant的股票代码格式
    :param frequency:MarketDataType类型,具体的类型及对应回调函数、数据类型如下：
                    1、MarketDataType.TICK：tick行情，回调函数handle_tick，数据类型Tick
                    2、MarketDataType.KLINE_1M：1分钟k线，回调函数handle_data，数据类型KLineDataPush
                    3、MarketDataType.RECORD_ORDER：逐笔委托，回调函数handle_order_record，数据类型RecordOrder
                    4、MarketDataType.RECORD_TRANSACTION：逐笔成交，回调函数handle_record_transaction，数据类型RecordTransaction
                    5、MarketDataType.FUND_FLOW：资金流向，回调函数handle_fund_flow，数据类型FundFlow
                    6、MarketDataType.ETF_ESTIMATE_INFO：ETF预估信息，回调函数handle_etf_estimate_info，数据类型EtfEstimateInfo
    :remark 注意,订阅ETF预估信息时,切记一定要在matic终端的“套利交易 -> ETF自助套利”界面将对应的ETF代码加入常用ETF列表,添加一次即可
    :return: 0：成功
    """
    if type(security) is type('a'):
        return subQuoteImpl([security], bool(True), frequency)
    return subQuoteImpl(security, bool(True), frequency)


def unsubscribe(security, frequency='tick'):
    """
    category:行情接口
    brief:取消订阅
    desc:取消订阅标的相关推送消息,与subscribe对应。
    :param security:支持股票代码及股票代码列表,股票代码格式支持聚宽和mquant的股票代码格式
    :param frequency:MarketDataType类型
    :return: 0：成功
    """
    if type(security) is type('a'):
        return subQuoteImpl([security], bool(False), frequency)
    return subQuoteImpl(security, bool(False), frequency)


def get_current_tick(security):
    """
    category:行情接口
    brief:获取最新行情
    desc:获取缓存中的最新行情,注意,必须策略订阅了目标标的的实时行情,且已经接收到实时行情推送后,调用此接口才能获取到数据
    :param security:标的代码, 支持股票、商品期货和股指期货。 不可以使用主力合约和指数合约代码。
    :return:security对应的最新tick对象,需要判断tick里面的代码是否=security,如果不相等,说明获取失败
    """
    tick = Tick()
    get_current_tick_impl(tick, security)
    return tick


def get_tick(symbol, start_time, end_time):
    """
	category:行情接口
	brief:历史tick查询数据
	desc:查询历史tick数据,仅支持level-1数据查询
    :param symbol: 标的
    :param start_time: 开始时间,datetime.datetime类型
    :param end_time:结束时间,datetime.datetime类型
    :return:返回列表,list<Tick>
    :remark:单次查询时间范围不可跨日
    """
    return get_tick_impl(symbol, start_time, end_time)


def get_kline_data_1d(symbol, start_date, end_date=None, fq='pre', sync=True, msg_type=-1, include_end_date=False):
    """
    category:行情接口
    brief:查询日K数据
    desc: 查询日k数据,返回KLineData对象,目前只支持前复权。
    :param symbol:证券代码,支持聚宽和MQuant两种格式
    :param start_date:开始日期,支持datetime对象格式、int格式和str格式,int示例格式：20180702,str格式支持yyyyMMddHHMMSS,其中HHMMSS可以不填写,不填写会用0补齐,
            例如2020090113、例如202009011310等等均是合法的
    :param end_date:结束日期,默认None为当前时间,支持格式同start_date
    :param fq:复权方式,默认为前复权,可选pre(前复权),None(不复权),post(后复权),目前只支持前复权
    :param sync:该参数已废弃，目前为同步查询
    :param msg_type:该参数已废弃
    :param include_end_date: 该参数已废弃,接口行为是包含结束时间
    :return:查询k线数据,返回KLineData对象
    """
    return get_kline_data_impl(symbol, start_date, end_date, fq, sync, msg_type, KLineDataType.KLINEData_1D,
                               include_end_date)


def get_kline_data_1d_from_init_date(symbol, days, init_date=None, fq=None, sync=True, msg_type=-1,
                                     date_type=DateType.NORMAL_DATE,
                                     security_exchange_type=SecurityExchangeType.UNKNOWN, include_init_date=False):
    """
    category:行情接口
    brief:查询N日日K数据
    desc: 查询N日日K数据,获取初始日期开始的days天的日k数据（N>0表示查询开始日期后N日的K线,N<0表示查询开始日期前N日的K线）,返回KLineData对象,支持按自然日和交易日查询,目前只支持前复权。
    :param symbol:证券代码,支持聚宽和MQuant两种格式
    :param days:int类型,大于0表示获取init_date之后days天的日k数据,小于0表示获取init_date之前days天的日k数据
    :param init_date:初始日期,支持datetime对象格式、int格式和str格式,int示例格式：20180702,str格式支持yyyyMMddHHMMSS,其中HHMMSS可以不填写,不填写会用0补齐,
            例如2020090113、例如202009011310等等均是合法的
    :param fq:复权方式,默认为前复权,可选pre(前复权),None(不复权),post(后复权),目前只支持前复权
    :param sync:该参数已废弃，目前为同步查询
    :param msg_type:该参数已废弃
    :param date_type:日期类型,DateType类型,主要区别在于days计算查询结束日期的方式,自然日包括交易日和非交易日
    :param security_exchange_type:代码交易市场,主要是区分港股代码,需要用户传入区分是港股市场还是沪深港通,SecurityExchangeType类型,如果传入SecurityExchangeType.UNKNOWN,取默认市场
    :param include_init_date:该参数已废弃,接口行为是包含开始及结束时间
    :return:查询k线数据,返回KLineData对象
    """
    return get_kline_data_from_init_date_impl(symbol, days, init_date, fq, sync, msg_type, KLineDataType.KLINEData_1D,
                                              date_type, security_exchange_type, include_init_date)


def get_kline_data(symbol, start_date, end_date=None, kline_type=KLineDataType.KLINEData_1M, fq='pre', sync=True,
                   msg_type=-1, include_end_date=False):
    """
    category:行情接口
    brief:查询K数据
    desc: 查询K线数据,包括1分钟、5分钟、15分钟、30分钟、60分钟K线及日K线,K线类型在KLineDataType中定义,目前只支持前复权。
    查询k线数据,如果k线数据已经准备好,则返回KLineData对象列表,否则返回None,目前支持日k和分钟k
    :param symbol:证券代码,支持聚宽和MQuant两种格式
    :param start_date:开始日期,支持datetime对象格式、int格式和str格式,int示例格式：20180702,str格式支持yyyyMMddHHMMSS,其中HHMMSS可以不填写,不填写会用0补齐,
            例如2020090113、例如202009011310等等均是合法的
    :param end_date:结束日期,默认None为当前时间,支持格式同start_date
    :param kline_type:k线数据类型,支持KLineDataType对象格式
    :param fq:复权方式,默认为前复权,可选pre(前复权),None(不复权),post(后复权),目前只支持前复权
    :param sync:该参数已废弃，目前为同步查询
    :param msg_type:该参数已废弃
    :param include_end_date:该参数已废弃，接口行为是包含结束时间
    :return:查询k线数据,返回KLineData对象
    """
    return get_kline_data_impl(symbol, start_date, end_date, fq, sync, msg_type, kline_type, include_end_date)


def get_kline_data_from_init_date(symbol, days, init_date=None, kline_type=KLineDataType.KLINEData_1M, fq=None,
                                  sync=True, msg_type=-1, date_type=DateType.NORMAL_DATE,
                                  security_exchange_type=SecurityExchangeType.UNKNOWN, include_init_date=False):
    """
    category:行情接口
    brief:查询后N日K数据
    desc: 查询前N日K线数据（N>0表示查询开始日期后N日的K线,N<0表示查询开始日期前N日的K线）,包括1分钟、5分钟、15分钟、30分钟、60分钟K线及日K线,K线类型在KLineDataType中定义,支持自然日和交易日查询,目前只支持前复权。
    获取初始日期开始的days天的k线数据
    :param symbol:证券代码,支持聚宽和MQuant两种格式
    :param days:int类型,大于0表示获取init_date之后days天的日k数据,小于0表示获取init_date之前days天的日k数据
    :param init_date:初始日期,支持datetime对象格式、int格式和str格式,int示例格式：20180702,str格式支持yyyyMMddHHMMSS,其中HHMMSS可以不填写,不填写会用0补齐,
            例如2020090113、例如202009011310等等均是合法的
    :param kline_type:k线数据类型,支持KLineDataType对象格式
    :param fq:复权方式,默认为前复权,可选pre(前复权),None(不复权),post(后复权),目前只支持前复权
    :param sync:该参数已废弃，目前为同步查询
    :param msg_type:该参数已废弃
    :param date_type:日期类型,DateType类型,主要区别在于days计算查询结束日期的方式,自然日包括交易日和非交易日
    :param security_exchange_type: 代码交易市场,主要是区分港股代码,需要用户传入区分是港股市场还是沪深港通,SecurityExchangeType类型,如果传入SecurityExchangeType.UNKNOWN,取默认市场
    :param include_init_date:该参数已废弃，接口行为是包含开始及结束时间
    :return: 查询k线数据,返回KLineData对象
    """
    return get_kline_data_from_init_date_impl(symbol, days, init_date, fq, sync, msg_type, kline_type, date_type,
                                              security_exchange_type, include_init_date)


"""
定时函数,目前支持日内的定时触发函数
"""

def run_timely(func, interval, start_time=None, stop_time=None, custom_params=''):
    """
    category:定时函数
    category-desc:定时函数
    brief:定时函数
    desc:定时函数,支持单次触发的定时信号和周期定时信号,目前时钟精度为秒。实盘模式为本机时钟,回测模式为行情时钟。
    定时运行函数,以秒为单位
    :param func: 回调函数, 形式为func(context, interval, custom_param),多个定时信号可共用一个回调函数（其中interval在单次定时信号时为起始时间start_time,周期定时信号时为间隔时间interval）
    :param interval: 间隔时间,单位为秒,interval=-1时,表示只在起始时间start_time发出一次定时信号(此时若start_time=None则判定为非法）
    :param start_time: 起始时间,格式为:"hh:mm:ss",比如 "10:00:01", "01:00:05"(精确到秒),None表示以订阅请求发起时间为开始时间
    :param stop_time: 结束时间,格式为:"hh:mm:ss",比如 "10:00:01", "01:00:05"(精确到秒),None表示没有结束时间
    :param custom_params: 用户自定义参数,字符串格式,定时信号触发时会通过回调函数返回，可用作定时器的标签
    :return:
    """
    run_timely_impl(func, interval, start_time, stop_time, custom_params)


def unschedule_all():
    """
    category:定时函数
    brief:取消所有定时信号
    desc:取消所有定时信号。
    取消所有定时运行函数
    :return:
    """
    return unschedule_all_impl()



"""
策略间通信
"""

def subscribe_custom_msg(custom_msg_type, func):
    """
    category:策略间通信
    category-desc:策略间通信,支持策略进程之间通过发布订阅自定义信号来进行通信
    brief:订阅自定义信号
    desc:订阅自定义信号,自定义信号类型custom_msg_type为10001-65536之间的int值,func为接收自定义信号的回调函数
    :param custom_msg_type:自定义信号类型,int类型,值应该在10001-65536之间
    :param func:回调函数,回调函数形式为func(context, custom_msg_type, msg_data),msg_data为发布者通过publish_custom_msg发布的str数据
    :return:
    """
    return subscribe_custom_msg_impl(custom_msg_type, func)


def unsubscribe_custom_msg(custom_msg_type):
    """
    category:策略间通信
    brief:取消订阅自定义信号
    desc:取消订阅自定义信号,自定义信号类型custom_msg_type为10001-65536之间的int值
    :param custom_msg_type:自定义信号类型,int类型,值应该在10001-65536之间
    :return:
    """
    return unsubscribe_custom_msg_impl(custom_msg_type)


def publish_custom_msg(custom_msg_type, msg_data):
    """
    category:策略间通信
    brief:发布自定义信号
    desc:发布自定义信号（初始化阶段禁止发布自定义信号）,自定义信号类型custom_msg_type为10001-65536之间的int值,msg_data为任意格式的字符串
    :param custom_msg_type:自定义信号,int类型,值应该在10001-65536之间
    :param msg_data: 自定义信号参数,str类型
    :return:
    """
    return publish_custom_msg_impl(custom_msg_type, msg_data)


"""
其他接口
"""

def get_symbol_list(exchange_type, security_type, security_sub_type=SecuritySubType.Ashares):
    """
    category:其他接口
    brief:获取证券代码列表
    desc:获取证券代码列表,支持获取指定市场、指定证券类型和子类型的证券代码列表,证券类型及证券子类型可以为空字符串,表示不作为限制条件。该接口的返回值可以直接传入subscribe接口来订阅实时行情。
    :param exchange_type:市场,类型为ExchangeType对象,仅支持一次获取一个市场的标的列表
    :param security_type:标的类型,类型为SecurityType对象,填空字符串表示不受该条件约束
    :param security_sub_type：标的子类型,类型为SecuritySubType对象,默认类型为A股（SecuritySubType.Ashares）,填空字符串表示不受该条件约束
    :return:成功返回证券代码列表，例如[601688.SH,600000.SH,...],失败返回None
    :remark: 用户可以调用此接口获取证券代码列表,然后调用subscribe函数订阅某个市场某类证券的全部行情
    """
    return get_symbol_list_impl(exchange_type, security_type, security_sub_type)


def get_symbol_detial(symbol):
    """
    category:其他接口
    brief:获取证券代码详情
    desc:获取证券代码详情,成功返回SecurityDetial对象,失败返回None。包含涨跌停价、昨收价、ST标志、流通股本等标的基础信息。
    :param symbol: 证券代码，例如601688.SH
    :return:成功返回SecurityDetial对象,失败返回None
    """
    return get_symbol_detial_impl(symbol)


def get_index_components(index_symbol):
    """
    category:其他接口
    brief:查询指数成分券
    desc:查询指定指数的成分券信息,包含成分券代码和样本数量
    :param index_symbol:指数代码
    :return:指数成分券列表,list<IndexComponent>
    """
    return get_index_components_impl(index_symbol)


def get_new_stock_purchase_Info(account_type):
    """
    category:其他接口
    brief:获取新股信息列表
    desc:获取新股信息列表
    :param account_type: 账户类型,AccountType类型
    :return:返回值为MResponseInfo类型,查询成功时MResponseInfo.data=list<NewStockDetailInfo>,失败时MResponseInfo.data=None
    """
    return get_new_stock_Info_impl(account_type)


def get_trade_dates(start_date=datetime.date.today(), end_date=datetime.date.today(), exchange=SecurityExchangeType.SH):
    """
    category:其他接口
    brief:获取指定范围内的交易日历信息。
    desc:获取指定范围内的交易日历信息。 支持本年度Matic交易日查询,年末跨年查询需待交易日历数据更新。此接口会限定最高频率,当前限频最高3s一次。
    :param start_date:查询开始时间,datetime.data类型
    :param end_date:查询结束时间,datetime.data类型
    :param exchange:交易日历对应市场,具体参见SecurityExchangeType
    :return:返回值为MResponseInfo类型,查询成功时MResponseInfo.data=list<datetime.date>,失败时MResponseInfo.data=None
    """
    return get_trade_dates_impl(start_date, end_date, exchange)


def unsubscribe_all():
    """
    category:其他接口
    brief:取消所有订阅
    desc:取消所有的订阅,涉及所有的推送数据,包括tick行情,逐笔委托、逐笔成交等。正常情况下,不建议使用。
    :return:
    """
    return unsubscribe_all_impl()


def get_sqlite_connection():
    """
    category:其他接口
    brief:获取内存数据库连接
    desc: 获取MQuant内置的sqlite内存数据库连接,返回HtDbConnection对象,在HTSADbAccess.py中定义。
    :return:HtDbConnection对象,在HTSADbAccess中定义
    """
    return getDbConnectionImpl()


def get_cur_time():
    """
    category:其他接口
    brief:获取当前时间
    desc: 获取当前时间,实盘模式下等同于datetime.datetime.now(),回测及行情回放模式下,返回根据行情计算出的当前时间
    :return:datetime.datetime对象
    """
    return get_cur_time_impl()


def register_backtest_symbols(symbols):
    """
    category:其他接口
    brief:注册回测标的
    desc: 注册回测标的列表,回测策略脚本必须在初始化阶段调用,实盘脚本调用无影响
    :param symbols 回测标的列表,支持单只标的'601688.SH',也支持列表格式['601688.SH','000002.SZ']
    :return: None
    """
    return register_backtest_symbols_impl(symbols)


def set_enable_order_reply(enable=False):
    """
    category:其他接口
    brief:设置接收下单类响应消息(全局)
    desc:开启后提供报、撤单响应发送给策略,回调函数为on_recv_order_reply。此接口为全局设置,开启后所有策略都将推送响应消息。
    :param enable:是否启用
    :return: 0成功，-1失败
    """
    return set_enable_order_reply_impl(enable)


def get_interproc_mutex(mutex_name):
    """
    category:其他接口
	brief:获取进程间互斥锁
	desc:获取进程间互斥锁
    :param mutex_name: 互斥锁名称
    :return:InterProcMutex 对象
    """
    return get_interproc_mutex_impl(mutex_name)




"""
普通交易
"""

def order_normal(order_request, account_type=AccountType.normal, batch_no=-1, last_batch_flag=0):
    """
    category:普通交易
    brief:统一报单接口
    desc: 提供统一报单接口,支持A股、两融、期货、期权报单,不包含ETF申赎、直接还款、备兑锁定解锁等
    :param last_batch_flag: 当前委托是否为batch_no对应的最后一笔委托, 0:不是, 1:是。目前保留不用
    :param batch_no:批次号,可以自定义批次号,需要保证同一资金账号下全局唯一,非必填,有效批次号为最大不超过2147483647的正整数
    :param account_type:账户类型,AccountType类型,默认为普通A股账户（AccountType.normal）
    :param order_request: 报单请求,单笔报单为OrderRequest类型,批量报单为list<OrderRequest>类型
    :return:Order对象或者None, 如果异步报单请求发送成功, 则返回Order对象, 失败则返回None,批量报单返回list<Order>或None,可使用batch_no作为透传字段
    """
    return order_normal_impl(order_request, account_type, batch_no, last_batch_flag)


def order(security, amount, style=None, side='long', pindex=0, msg_type=-1):
    """
    category:普通交易
    category-desc:股债基单笔报单接口,信用交易、期货、期权交易有专门的接口,初始化阶段禁止交易。
    brief:单笔报单（推荐使用order_normal）
    desc: 股债基单笔报单接口,支持限价单和多种市价单,买卖方向由amount的正负控制。mquant采用异步报单方式,order接口正常返回Order对象不代表订单已经报到后台或交易所,因此通过返回的order_id查询订单可能返回None
    :param security: 标的代码,支持M-Quant代码格式和聚宽代码格式
    :param amount:交易数量, 正数表示买入, 负数表示卖出
    :param style:参见OrderStyle, 支持限价LimitOrderStyle和市价MarketOrderStyle,None默认为MarketOrderStyle的最优五档即时成交剩余撤销(沪市深市均可),用户也可选择其他类型
    :param side:该参数已废弃
    :param pindex:该参数已废弃
    :param msg_type:该参数已废弃
    :return:Order对象或者None, 如果创建订单成功, 则返回Order对象, 失败则返回None
    """
    return order_impl(security, amount, style, side, pindex, msg_type)


def orders(orders, batch_no=-1, last_batch_flag=0, msg_type=-1):
    """
    category:普通交易
    brief:批量报单接口（推荐使用order_normal）
    desc: 支持股债基批量报单,支持自定义批次号,支持一个批次里面有不同买卖方向,不同订单类型的订单,支持按批次号撤单。
    :param orders:批量订单列表数据,list<batch_order_item>类型
    :param batch_no:批次号,可以自定义批次号,需要保证同一资金账号下全局唯一,非必填,有效批次号为最大不超过2147483647的正整数
    :param last_batch_flag:当前委托是否为batch_no对应的最后一笔委托, 0:不是, 1:是。目前保留不用
    :param msg_type:该参数已废弃
    :return:Order对象列表
    """
    return batch_order_impl(orders, batch_no, last_batch_flag, msg_type)


def cancel_order(order, batch_flag=0, account_type=AccountType.normal, msg_type=-1):
    """
    category:普通交易
    brief:单笔撤单接口
    desc: 单笔撤单接口,支持股、债、基、期货、期权、信用交易撤单。
    :param account_type:账户类型,AccountType类型,默认为普通A股账户（AccountType.normal）
    :param order:撤单对象参数，支持Order对象、str类型、int类型。根据batch_flag字段确定撤单方式。
    :param batch_flag: 0表示按照order_id撤单,1表示按照batch_no撤单,默认按照order_id撤单,期货暂不支持按批次号撤单。
    :param msg_type:该参数已废弃
    :return: Order对象或者None
    :remark: 期货暂不支持按批次号撤单
    """
    return cancel_order_impl(order, batch_flag, msg_type, account_type)


def cancel_orders(orders, account_type=AccountType.normal, msg_type=-1):
    """
    category:普通交易
    brief:批量撤单接口
    desc: 批量撤单接口,支持股、债、基、信用交易批量撤单,暂不支持期货、期权批量撤单。
    :param account_type:账户类型,AccountType类型,默认为普通A股账户（AccountType.normal）
    :param orders: batch_cancel_order_item列表
    :param msg_type:该参数已废弃
    :return: 返回list<Order>,失败为空列表,列表元素也可能是None
    :remark: 期货暂不支持按批次号撤单
    """
    return cancel_orders_impl(orders, msg_type, account_type)


def bond_convert_to_stock(convert_symbol, qty, account_type=AccountType.normal):
    """
    category:普通交易
    brief:债转股
    desc: 债转股
    :param convert_symbol: 转股代码
    :param qty: 数量,单位为张
    :param account_type:账户类型,AccountType类型,默认为普通A股账户（AccountType.normal）
    :return: Order对象或者None
    """
    return bond_convert_to_stock_impl(convert_symbol, qty, account_type)


def purchase_new_stock(orders, account_type):
    """
    category:普通交易
    brief:新股申购请求
    desc: 新股申购请求，批量报单接口
    :param orders:PurchasOrderRequest列表
    :param account_type: 账户类型,AccountType类型
    :return:Order对象列表
    """
    return purchase_new_stock_impl(orders, account_type)



"""
衍生品交易
"""

def get_future_contract_info(symbol, hedge_flag):
    """
    category:衍生品交易
    brief:获取期货合约
    desc:获取期货合约,成功返回FutureContractInfo对象,失败返回None。
    :param symbol:  期货合约代码
    :param hedge_flag: 投保标记,参见HedgeFlag中的定义
    :return:成功返回FutureContractInfo对象,失败返回None
    """
    return get_future_contract_info_impl(symbol, hedge_flag)


def order_future(security, amount, style=None, action=OrderAction.UNKNOWN, invest_type=HedgeFlag.SPECULATION,
                 close_direction=CloseDirection.DEFAULT):
    """
    category:衍生品交易
    category-desc:衍生品交易接口,包含期货、期权交易接口,期货合约查询等,初始化阶段禁止交易。
    brief:期货报单接口（推荐使用order_normal）
    desc: 支持期货开平仓交易,目前期货仅支持限价单。
    :param security:标的代码,支持M-Quant代码格式和聚宽代码格式
    :param amount:交易数量, 正数表示买入, 负数表示卖出
    :param style:参见OrderStyle,期货目前仅支持限价单LimitOrderStyle
    :param action: 开平标志,OrderAction类型
    :param invest_type: 投资类型,HedgeFlag类型,分为投机、套保、套利,默认为投机
    :param close_direction: 平仓方式,CloseDirection类型,默认为优先平老仓
    :return:Order对象或者None, 如果创建订单成功, 则返回Order对象, 失败则返回None
    """
    return order_future_impl(security, amount, style, action, invest_type, close_direction)


def orders_future(orders, batch_no=-1, last_batch_flag=0):
    """
    category:衍生品交易
    brief:期货批量报单接口（推荐使用order_normal）
    desc: 期货批量报单接口,暂不支持自定义批次号,也不支持按批次号撤单。
    :param orders:batch_order_item列表
    :param batch_no:可以自定义批次号,,需要保证同一资金账号下全局唯一,非必填,目前暂不支持
    :param last_batch_flag:该参数已废弃
    :return:返回list<Order>,失败为空列表,列表元素也可能是None
    """
    return batch_order_impl(orders, batch_no, last_batch_flag, account_type=AccountType.futures)


def order_option(security, amount, style=None, action=OrderAction.UNKNOWN, covered_flag=OptionCoveredFlag.UNKNOWN):
    """
    category:衍生品交易
    brief:期权报单接口（推荐使用order_normal）
    desc: 支持期权开平仓、备兑交易。
    :param security:标的代码,支持M-Quant代码格式
    :param amount:交易数量, 正数表示买入, 负数表示卖出
    :param style:参见OrderStyle, None代表MarketOrder
    :param action:开平标志,OrderAction类型
    :param covered_flag:备兑标志,OptionCoveredFlag类型
    :return:Order对象或者None, 如果创建订单成功, 则返回Order对象, 失败则返回None
    """
    return order_option_impl(security, amount, style, action, covered_flag)


def option_trans(security, amount):
    """
    category:衍生品交易
    brief:期权备兑证券锁定/解锁
    desc: 上交所期权要求备兑开仓前,要锁定标的券,备兑平仓后,要解锁标的券。
    :param security:标的券代码
    :param amount:锁定/解锁数据,amount>0表示锁定,amount<0表示解锁
    :return:Order对象或者None, 如果锁定/解锁成功, 则返回Order对象, 失败则返回None
    """
    return option_trans_impl(security, amount)


def combine_options(combo_option_req):
    """
    category:衍生品交易
    brief:期权组合创建
    desc:期权组合创建
    :param combo_option_order_id:组合创建/拆分请求,ComboOptionReq类型
    :return: MResponseInfo 对象,成功MResponseInfo.data = Order(),失败MResponseInfo.data=None
    """
    return combo_option_order(combo_option_req)


def split_option_combination(combo_option_req):
    """
    category:衍生品交易
    brief:期权组合拆分
    desc:期权组合拆分
    :param combo_option_req:组合创建/拆分请求,ComboOptionReq类型
    :return: MResponseInfo 对象,MResponseInfo 对象,成功MResponseInfo.data = Order(),失败MResponseInfo.data=None
    """
    return combo_option_order(combo_option_req)


def option_comb_exec_request(option_code_1, amount, security_exchange, option_code_2='', cl_order_id=''):
    """
    category:衍生品交易
    brief:期权组合行权请求
    desc:期权组合行权请求
    :param option_code_1:第一腿期权合约编码
    :param amount:数量
    :param security_exchange:市场，具体参见SecurityExchangeType
    :param option_code_2:第二腿期权合约编码
    :param cl_order_id:订单ID,无需填写,仅有特殊指定需求时使用,需注意避免重复,建议UUID
    :return:返回值为MResponseInfo类型（仅返回请求结果信息，MResponseInfo.data无数据）
    """
    return option_comb_exec_request_impl(option_code_1, amount, security_exchange, option_code_2, cl_order_id)



"""
融券交易
"""

def order_secmatch(order_request, account_type=AccountType.margin):
    """
    category:融券交易
    brief:融券通报单接口
    desc: 融券通报单接口,注意该接口为同步报单请求,暂仅支持融入。仅支持单笔报单,交易前需要确保已签署风险揭示协议
    :param order_request: 报单请求,SecmatchOrderRequest类型
    :param account_type:账户类型,AccountType类型,默认为信用账号
    :return:返回值为MResponseInfo类型,成功时MResponseInfo.data为order_id(委托编号：转融通申请编号),失败时MResponseInfo.data=None
    """
    return order_secmatch_impl(order_request, account_type)


def cancel_secmatch(order_id, account_type=AccountType.margin):
    """
    category:融券交易
    brief:融券通撤单请求接口
    desc: 融券通撤单请求接口,仅支持单笔撤单
    :param order_id: 委托编号（转融通申请编号）,必填
    :param account_type:账户类型,AccountType类型,默认为信用账号
    :return:返回值为MResponseInfo类型,MResponseInfo.data=None无意义
    """
    return cancel_secmatch_impl(order_id, account_type)




"""
交易查询
"""

def get_open_orders(page_no=1, page_size=1000, only_this_inst=True, account_type=AccountType.normal, msg_type=-1,
                    inst_id=''):
    """
    category:交易查询
    category-desc:交易查询接口,包括委托、成交、持仓等查询接口
    brief:未完成订单查询
    desc: 获取未完成订单,不包含撤单订单。
    :param page_no:分页查询,页码
    :param page_size:每页数量,默认为1000, 建议在1000以内,-1表示查询符合条件的全部订单
    :param only_this_inst:是否只查询当前实例的订单,默认为True
    :param msg_type:该参数已废弃
    :param account_type: 账户类型,AccountType类型,默认为A股账户
    :param inst_id:如果only_this_inst=False,可以查询指定inst_id的订单信息,only_this_inst=True时无效
    :return:返回一个dict, key是order_id, value是Order对象
    """
    return get_open_orders_impl(page_no, page_size, only_this_inst, msg_type, account_type, inst_id)


def get_open_orders_ex(page_no=1, page_size=1000, only_this_inst=True, account_type=AccountType.normal, msg_type=-1,
                       inst_id=''):
    """
    category:交易查询
    category-desc:交易查询接口,包括委托、成交、持仓等查询接口
    brief:未完成订单查询
    desc: 获取未完成订单,不包含撤单订单。与get_open_orders功能相同,仅返回值形式不一样。
    :param page_no:分页查询,页码
    :param page_size:每页数量,默认为1000, 建议在1000以内,-1表示查询符合条件的全部订单
    :param only_this_inst:是否只查询当前实例的订单,默认为True
    :param msg_type:该参数已废弃
    :param account_type: 账户类型,AccountType类型,默认为A股账户
    :param inst_id:如果only_this_inst=False,可以查询指定inst_id的订单信息,only_this_inst=True时无效
    :return:返回一个tuple, [total_count, is_last, dict<order_id,Order>]
            total_count 订单总数
            is_last 是否最后一批，可用于判断分页查询结束
            dict<order_id,Order> 订单数据,key是order_id, value是Order对象
    """
    return get_open_orders_ex_impl(page_no, page_size, only_this_inst, msg_type, account_type, inst_id)


def get_orders(order_id='', security='', status=None, page_no=1, page_size=1000, only_this_inst=True, msg_type=-1,
               account_type=AccountType.normal, inst_id=''):
    """
    category:交易查询
    brief:订单查询
    desc: 按条件分页查询订单,不包含撤单订单。
    :param order_id:订单id,用于查询指定订单。默认为空，不指定。
    :param security:标的代码,用于查询指定标的的订单。默认为空，不指定。
    :param status:OrderStatus类型, 用于查询特定订单状态的订单。默认为None，不指定。
    :param page_no:分页查询,页码
    :param page_size:每页数量,默认为1000, 建议在1000以内,-1表示查询符合条件的全部订单
    :param only_this_inst:是否只查询当前实例的订单,默认为True
    :param msg_type:该参数已废弃
    :param account_type:账户类型,AccountType类型,默认为A股账户
    :param inst_id:如果only_this_inst=False,可以查询指定inst_id的订单信息,only_this_inst=True时无效
    :return:返回一个dict, key是order_id, value是Order对象
    """
    return get_orders_impl(order_id, security, status, page_no, page_size, only_this_inst, msg_type, account_type,
                           inst_id)


def get_orders_ex(order_id='', security='', status=None, page_no=1, page_size=1000, only_this_inst=True, msg_type=-1,
                  account_type=AccountType.normal, inst_id=''):
    """
    category:交易查询
    brief:订单查询（推荐）
    desc: 按条件分页查询订单,不包含撤单订单。
    :param order_id:订单id,用于查询指定订单。默认为空，不指定。
    :param security:标的代码,用于查询指定标的的订单。默认为空，不指定。
    :param status:OrderStatus类型, 用于查询特定订单状态的订单。默认为None，不指定。
    :param page_no:分页查询,页码
    :param page_size:每页数量,默认为1000, 建议在1000以内,-1表示查询符合条件的全部订单
    :param only_this_inst:是否只查询当前实例的订单,默认为True
    :param msg_type:该参数已废弃
    :param account_type:账户类型,AccountType类型,默认为A股账户
    :param inst_id:如果only_this_inst=False,可以查询指定inst_id的订单信息,only_this_inst=True时无效
    :return:返回一个tuple, [total_count, is_last, dict<order_id,Order>]
            total_count 订单总数
            is_last 是否最后一批，可用于判断分页查询结束
            dict<order_id,Order> 订单数据,key是order_id, value是Order对象
    """
    return get_orders_ex_impl(order_id, security, status, page_no, page_size, only_this_inst, msg_type, account_type,
                              inst_id)


def get_trades(order_id='', security='', page_no=1, page_size=1000, account_type=AccountType.normal,
               include_rejected_orders=False, include_withdraw_orders=True, only_this_inst=True, msg_type=-1,
               inst_id=''):
    """
    category:交易查询
    brief:成交查询
    desc: 按条件分页查询成交,page_size=-1表示查询满足条件的所有成交。此接口返回的数据以成交编号trade_id为key,在某些特殊情况下存在成交编号相同的场景（比如沪市自成交等）会导致数据缺失,建议使用get_trades_ex接口。
    :param order_id:订单id,用于查询指定订单。默认为空，不指定。
    :param security:标的代码,用于查询指定标的的订单。默认为空，不指定。
    :param page_no:分页查询,页码
    :param page_size:每页数量,默认为1000, 建议在1000以内,-1表示查询符合条件的全部成交
    :param include_rejected_orders: 该参数已废弃
    :param include_withdraw_order: 该参数已废弃
    :param only_this_inst:是否只查询当前实例的成交,默认为True
    :param msg_type:该参数已废弃
    :param account_type:账户类型,AccountType类型,默认为A股账户
    :param inst_id: 如果only_this_inst=False,可以查询指定inst_id的订单信息,only_this_inst=True时无效
    :return:返回一个dict, key是trade_id, value是Trade对象
    """
    return get_trades_impl(order_id, security, page_no, page_size, include_rejected_orders, include_withdraw_orders,
                           only_this_inst, msg_type, account_type, inst_id)


def get_trades_ex(order_id='', security='', page_no=1, page_size=1000, account_type=AccountType.normal,
                  include_rejected_orders=False, include_withdraw_orders=True, only_this_inst=True, msg_type=-1,
                  inst_id=''):
    """
    category:交易查询
    brief:成交查询（推荐）
    desc: 按条件分页查询成交,page_size=-1表示查询满足条件的所有成交。
    :param order_id:订单id,用于查询指定订单。默认为空，不指定。
    :param security:标的代码,用于查询指定标的的订单。默认为空，不指定。
    :param page_no:分页查询,页码
    :param page_size:每页数量,默认为1000, 建议在1000以内,-1表示查询符合条件的全部成交
    :param include_rejected_orders: 该参数已废弃
    :param include_withdraw_order: 该参数已废弃
    :param only_this_inst:是否只查询当前实例的成交,默认为True
    :param msg_type:该参数已废弃
    :param account_type:账户类型,AccountType类型,默认为A股账户
    :param inst_id: 如果only_this_inst=False,可以查询指定inst_id的订单信息,only_this_inst=True时无效
    :return:返回一个tuple, [total_count, is_last, list<Trade>]
            total_count 订单总数
            is_last 是否最后一批，可用于判断分页查询结束
            list<Trade> 订单数据,元素是Trade对象
    """
    return get_trades_ex_impl(order_id, security, page_no, page_size, include_rejected_orders, include_withdraw_orders,
                              only_this_inst, msg_type, account_type, inst_id)


def get_positions(account_type=AccountType.normal, symbol=''):
    """
    category:交易查询
    brief:持仓查询
    desc: 查询指定类型账号的所有持仓。此接口返回的数据以标的代码symbol为key,在多股东账号等特殊情况下存在symbol相同的场景会导致数据缺失,建议使用get_positions_ex接口。
    :param account_type:账户类型,AccountType类型,默认为A股账户
    :param symbol:标的代码,用于查询指定标的持仓。默认为空，不指定。
    :return:失败返回None,成功返回dict<symbol, Position>。指定symbol时,成功返回Position对象,失败返回None
    """
    return get_positions_impl(account_type, symbol)


def get_positions_ex(account_type=AccountType.normal, symbol=''):
    """
    category:交易查询
    brief:持仓查询（推荐）
    desc: 查询指定类型账号的所有持仓。
    :param account_type:账户类型,AccountType类型,默认为A股账户
    :param symbol:标的代码,用于查询指定标的持仓。默认为空，不指定。
    :return:失败返回None,成功返回list<Position>
    """
    return get_positions_ex_impl(account_type, symbol)


def query_position_from_counter(symbol='', account_type=AccountType.normal, action='1'):
    """
    category:交易查询
    brief:查询账号持仓
    desc:查询账号持仓。对于快速柜台账号可查询对应的集中柜台可划转持仓。
    :param symbol: 标的代码(非必填),可以用来查询指定标的的持仓,证券代码+市场后缀的格式,如600000.SH
    :param account_type: 账户类型,AccountType类型,默认为普通A股账户
    :param action:操作控制值,0-查询 当前柜台；1-查询 集中柜台（该参数仅快速柜台普通账号有效）
    :return:返回值为MResponseInfo类型,查询成功时MResponseInfo.data=list<Position> (其中closeable_amount即为可划转数量),失败时MResponseInfo.data=None
    """
    return query_position_from_counter_impl(symbol, account_type, action)


def get_secmatch_orders(symbol='', status=None, start_date=datetime.date.today(), end_date=None, entrust_prop='', account_type=AccountType.margin):
    """
    category:交易查询
    brief:融券通订单查询
    desc: 按条件查询融券通订单。
    注意,如果查询当日委托,应该只传start_date,如果start_date和end_date都传当日,则16:00-20:00下单的委托将不会被查询到（16:00-20:00下单的委托属于T+1日的委托）
    :param symbol: 标的代码(非必填),可以用来查询指定标的的所有订单,证券代码+市场后缀的格式,如600000.SH
    :param status: 状态SecmatchOrderStatus类型(非必填), 查询特定订单状态的所有订单
    :param start_date: 查询开始日期(必填),默认为当前日期
    :param end_date: 查询结束日期(非必填),不传结束日期,等于是查>=开始日期的所有订单
    :param entrust_prop: 委托属性: 0-非特殊策略 1-长期限策略 ,不填写默认为0
    :param account_type: 账号类型,AccountType类型,默认为信用账号
    :return:返回值为MResponseInfo类型,成功时MResponseInfo.data为dict, key是order_id, value是SecmatchOrder对象,失败时MResponseInfo.data=None
    """
    return get_secmatch_orders_impl(symbol, status, start_date, end_date, entrust_prop, account_type)


def get_secmatch_trades(symbol='', start_date=datetime.date.today(), end_date=None, entrust_prop='', account_type=AccountType.margin):
    """
    category:交易查询
    brief:融券通成交查询
    desc: 按条件查询融券通成交。
    :param symbol: 标的代码(非必填),可以用来查询指定标的的所有订单,证券代码+市场后缀的格式,如600000.SH
    :param start_date: 查询开始日期(必填),默认为当前日期
    :param end_date: 查询结束日期(非必填),不传结束日期,等于是查>=开始日期的所有订单
    :param entrust_prop: 委托属性: 0-非特殊策略 1-长期限策略 ,不填写默认为0
    :param account_type: 账号类型,AccountType类型,默认为信用账号
    :return:返回值为MResponseInfo类型,成功时MResponseInfo.data为list<SecmatchTrade>,失败时MResponseInfo.data=None
    """
    return get_secmatch_trades_impl(symbol, start_date, end_date, entrust_prop, account_type)


def get_secmatch_compacts(symbol='', compact_id='', account_type=AccountType.margin):
    """
    category:交易查询
    brief:融入合约查询
    desc: 按条件查询融入合约。
    :param symbol: 标的代码(非必填),可以用来查询指定标的的所有订单,证券代码+市场后缀的格式,如600000.SH
    :param compact_id: 合约编号(非必填)
    :param account_type: 账号类型,AccountType类型,默认为信用账号
    :return:返回值为MResponseInfo类型,成功时MResponseInfo.data为list<SecmatchCompact>,失败时MResponseInfo.data=None
    """
    return get_secmatch_compacts_impl(symbol, compact_id, account_type)


def get_bond_negotiate_exec_id(order_request, account_type=AccountType.normal):
    """
    category:交易查询
    brief:债券协商交易执行编号查询
    desc: 按条件查询债券协商交易执行编号。深市协商确认/拒绝需要用到该编号。
    :param order_request: 格式同报单请求,OrderRequest类型,仅需填写协商交易相关字段
    :param account_type:账户类型,AccountType类型,默认为普通A股账户
    :return:返回值为MResponseInfo类型,成功时MResponseInfo.data为list<BondNegotiateExecID>,失败时MResponseInfo.data=None
    """
    return get_bond_negotiate_exec_id_impl(order_request, account_type)


def get_bank_transfer_statement(start_date=datetime.date.today(), end_date=None, account_type=AccountType.normal):
    """
    category:交易查询
    brief:银行转账流水查询
    desc: 按条件查询银行转账流水。
    :param start_date: 查询开始日期(必填),默认为当前日期
    :param end_date: 查询结束日期(非必填),不传结束日期,等于是查从开始日期到当前日期的所有流水
    :param account_type:账户类型,AccountType类型,默认为普通A股账户
    :return:返回值为MResponseInfo类型,成功时MResponseInfo.data为list<BankTransferStatement>,失败时MResponseInfo.data=None
    """
    return get_bank_transfer_statement_impl(start_date, end_date, account_type)


def get_fund_info(account_type=AccountType.normal):
    """
    category:交易查询
    brief:获取账户资金信息
    desc:查询指定账户的资金信息
    :param account_type:账户类型,AccountType类型,默认为普通A股账户
    :return:资金信息,成功返回FundUpdateInfo对象,失败返回None
    """
    return get_fund_info_impl(account_type)


def get_fund_info_from_counter(account_type=AccountType.normal):
    """
    category:交易查询
    brief:从柜台查询获取账户资金
    desc:从柜台查询获取账户资金，目前限制至少间隔10s查询一次。
    :param account_type:账户类型,AccountType类型,默认为普通A股账户
    :return:资金信息,返回值为QueryFundRsp类型,成功时QueryFundRsp.fund_info为FundInfoCounter对象,失败返回None
    """
    return get_fund_info_from_counter_impl(account_type)


def get_combo_option_strategy_list():
    """
    category:交易查询
    brief:获取组合期权策略信息
    desc:获取组合期权策略信息
    :return:返回值为MResponseInfo类型,查询成功时MResponseInfo.data=list<ComboOptionStrategyInfo>,失败时MResponseInfo.data=None
    """
    return get_combo_option_strategy_list_impl()


def get_account_combo_option_positions():
    """
    category:交易查询
    brief:获取期权组合持仓
    desc:获取期权组合持仓
    :return:返回值为MResponseInfo类型,查询成功时MResponseInfo.data=list<ComboOptionPosInfo>,失败时MResponseInfo.data=None
    """
    return get_account_combo_option_positions_impl()


"""
划转调拨
"""


def transter_position(symbol, qty, account_type=AccountType.normal, action='0'):
    """
    category:划转调拨
    brief:证券划转
    desc:证券划转，目前仅支持快速柜台账号，支持 快速柜台 和 集中柜台 间的持仓划转。接口query_position_from_counter可查询可划转持仓。
    :param symbol: 标的代码(非必填),可以用来查询指定标的的持仓,证券代码+市场后缀的格式,如600000.SH
    :param qty: 划转数量
    :param account_type: 账户类型,AccountType类型,默认为普通A股账户
    :param action:操作控制值,0-冻结（从 集中 划拨持仓到 快速）；1-解冻（从 快速 划拨持仓到 集中）
    :return:返回值为MResponseInfo类型,划拨成功时MResponseInfo.err_code='0',失败时MResponseInfo.error_info包含错误信息
    """
    return transter_position_impl(symbol, qty, account_type, action)


def transter_fund(amount, account_type=AccountType.normal, action='0'):
    """
    category:划转调拨
    brief:资金调拨
    desc:资金调拨，目前仅支持快速柜台账号，支持 快速柜台 和 集中柜台 间的资金调拨
    :param amount: 调拨金额
    :param account_type: 账户类型,AccountType类型,默认为普通A股账户
    :param action:操作控制值,0-转入（从 集中 划拨到 快速）；1-转出（从 快速 划拨到 集中）
    :return:返回值为MResponseInfo类型,查询成功时MResponseInfo.err_code='0',失败时MResponseInfo.error_info包含错误信息
    """
    return transter_fund_impl(amount, account_type, action)


def query_transter_fund_info(account_type=AccountType.normal, action='0'):
    """
    category:划转调拨
    brief:查询调拨资金详细信息
    desc:查询调拨资金详细信息，目前仅支持快速柜台账号，从 快速柜台 和 集中柜台 间的可调拨资金详情（总资金/可调资金/可取资金等）
    :param account_type: 账户类型,AccountType类型,默认为普通A股账户
    :param action: 操作控制值,0-查询 快速柜台；1-查询 集中柜台
    :return:返回值为MResponseInfo类型,查询成功时MResponseInfo.data=FundInfoCounter资金信息对象 ,失败时MResponseInfo.data=None
            FundInfoCounter中仅以下数据有效：
            fund_balance    # 总资金余额
            enable_balance  # 可用资金
            fetch_balance   # 可取金额（仅集中柜台支持）
    """
    return query_transter_fund_info_impl(account_type, action)


def transter_fund_to_normal_account(fund_account_dest, amount, password):
    """
    category:划转调拨
    brief:同名划转到普通账号
    desc:同名划转到普通账号，集中信用账号资金同名划转到集中普通账号，主要用于银证转出。对于快速柜台信用账号出金，需要先transter_fund资金调拨到集中柜台，在通过此接口划转到集中普通账号，最后进行银证转账。
    :param fund_account_dest: 转入资金账户，必须是当前信用账号对应的同名下的普通账号。字符串格式，如“123456”
    :param amount: 划转金额。数字格式(int/float)，如1000.00
    :param password: 资金密码，转出账号对应的资金密码，这里即为信用账号对应的密码。字符串格式，如“888888”
    :return:返回值为MResponseInfo类型,划拨成功时MResponseInfo.err_code='0',失败时MResponseInfo.error_info包含错误信息
    """
    return transter_fund_to_normal_account_impl(fund_account_dest, amount, password)


"""
外部数据访问
"""


def read_ini_config(path, section, key, buf_len=1024):
    """
    category:外部数据访问
    category-desc:外部数据访问,仅允许初始化阶段访问外部数据
    brief:读取ini文件
    desc: 读取指定路径的ini文件的指定section下指定key的值。仅允许在initialize函数中使用。
    :param path:ini配置文件路径,支持相对路径
    :param section:ini文件section
    :param key:ini文件key
    :param buf_len:缓冲区长度
    :return:读取的数据，字符串类型
    """
    return getIniConfigImpl(path, section, key, buf_len)


def open_csv_file(path, encodeing='utf-8'):
    """
    category:外部数据访问
    brief:读取csv文件
    desc: 读取指定路径的csv文件,返回CsvReader操作对象,用户使用该对象读取csv文件。
    获取csv读取对象,目前只支持utf-8编码的csv文件
    :param path:csv文件路径
    :param encodeing:编码方式
    :return:CsvReader对象,在HTSACsvReader.py中定义
    """
    return CsvReader(path, encodeing)


def exec_py(py_file_path, params='', python_interpreter_path='', cmd_run=False):
    """
    category:外部数据访问
    brief:执行外部脚本
    desc: 同步执行外部python脚本,支持使用用户本地的python环境。
    :param py_file_path: python文件路径,建议全路径
    :param params: 脚本执行参数
    :param python_interpreter_path:python解释器路径,要带上python.exe,默认为空,表示使用mquant内置解释器
    :param cmd_run: 是否直接通过cmd执行
    :return:
    """
    return exec_py_impl(py_file_path, params, python_interpreter_path, cmd_run)


"""
策略控制
"""


def stop_stragety(inst_id=''):
    """
    category:策略控制
    category-desc:策略控制,包含通过接口停止策略、创建新策略实例
    brief:停止实例
    desc: 停止策略实例。如果策略创建了算法实例,调用此接口不会自动停止算法实例,需要策略主动调用停止算法实例接口停止。
    :param inst_id:如果为空,表示停止当前实例,如果不为空,表示停止指定实例id的实例
    :return: 成功返回0,失败返回-1
    """
    return stop_stragety_impl(inst_id)


def start_strategy(strategy_file, run_params='', instance_name='', show_params=False):
    """
    category:策略控制
    brief:创建策略实例
    desc: 创建一个新的策略实例,至少间隔5分钟才能创建一次
    创建策略实例,允许带参启动,参数会直接传给新启动的实例,不会做任何额外处理，新启动的实例会继承父实例的资金账号。
    :param strategy_file: 策略文件路径,支持绝对路径或相对路径,相对路径为相对用户目录下的文件路径（Matic安装路径\\M-quant\\用户名）
    :param run_params: 启动参数,最长4096字节,可以为空
    :param instance_name: 实例名，可选参数,如果未填写默认生成
    :param show_params: 是否显示窗口，可选参数,如果未填写默认不弹窗
    :return: 成功返回实例ID,失败返回空字符串
    """
    return start_strategy_impl(strategy_file, run_params, instance_name, show_params)


def set_instance_remark(remark):
    """
    category:策略控制
    brief:设置策略实例的备注信息
    desc:设置策略实例的备注信息
    :param remark: 实例备注，字符串类型，长度不超过200
    :return:无
    """
    set_instance_remark_impl(remark)




"""
人工干预
"""

def get_user_params(json_params_template, wnd_title, sync=False):
    """
    category:人工干预
    category-desc:实现策略和交易员之间的双向互动
    brief:获取用户输入参数
    desc:根据请求参数中传入的模板生成操作界面,用户可以修改表格中的参数,点击确定,即可将修改后的参数返回给策略,支持同步和异步两种方式,异步通过on_rsp_user_params回调返回给策略
    :param json_params_template: 参数模板,例如,下方为一个持仓止损的示例：
        {"left_layout":{"name":"操作表格","ui_type":"table","columns":[{"name":"","ui_type":"check_box"},
                                                                        {"name":"证券代码","ui_type":"code_edit"},
                                                                        {"name":"持仓数量","ui_type":"line_edit","editable":"0"},
                                                                        {"name":"可用数量","ui_type":"line_edit","editable":"0"},
                                                                        {"name":"持仓均价","ui_type":"line_edit","editable":"0"},
                                                                        {"name":"止损价","ui_type":"line_edit"}],
                                                            "rows":[[0,"601688.SH",5400,1800,29.15,29.15],[0,"000001.SZ",3800,3000,18.15,18.15]]}}
    目前支持的ui_type控件类型
    "tab_widget": Tab选项卡窗口
    "table": 表格
    "check_box": 勾选框
    "code_edit": 代码筛选框
    "line_edit": 编辑框
    "combobox": 下拉选择框
    
    :param wnd_title:界面弹窗的窗口名称
    :param sync:是否同步,默认为异步,要注意同步模式会阻塞接收线程
    :return:同步返回用户修改后的参数,异步返回空字符串（由回调on_rsp_user_params返回）
    """
    return get_user_params_impl(json_params_template, wnd_title, sync)


def play_sound(wav_file=''):
    """
    category:人工干预
    brief:播放音频
    desc:播放传入的音频文件,如果传入为空,则播放系统默认的音频文件
    :param wav_file:声音文件,如果为空,则使用系统自带的声音
    :return:成功,返回当前音频的唯一ID,停止音频时需要传入,失败返回空字符串
    """
    return play_sound_impl(wav_file)


def stop_sound(sound_id):
    """
    category:人工干预
    brief:停止播放音频
    desc:停止播放指定sound_id的音频,sound_id为play_sound接口的返回值
    :param sound_id:音频的唯一ID,为play_sound接口成功后的返回值
    :return:无
    """
    stop_sound_impl(sound_id)


def message_box(title, msg, sync=False, width=200, height=200):
    """
    category:人工干预
	brief:弹出模态框，用于用户自定义的提示功能
    desc:弹出MessageBox,分为同步和异步弹出,同步弹出时,返回值为True（点击确定）或者False（点击取消或关闭）
    :param title:弹框标题
    :param msg:弹框内容，str类型
    :param sync:是否同步,默认为异步,要注意同步模式会阻塞接收线程
    :return:sync=True时,点击确定返回True,点击取消返回False,sync=False时固定返回False
    """
    return message_box_impl(title, msg, sync, width, height)



"""
手工干预
"""

def register_fast_param_wnd(wnd_title):
    """
    category:手工干预
    brief:注册常驻参数窗口。使用方法请参考手工干预Ex示例策略。
    desc:注册一个常驻的参数输入窗口,用户在窗口中输入参数后,通过点击发送并清空或者用F8快捷键即可将参数发送给策略,策略响应回调函数为on_recv_fast_params,只允许在初始化函数中调用
    :param wnd_title:窗口名称
    :return: 0成功，-1失败
    """
    return register_fast_param_wnd_impl(wnd_title)


def register_fast_param_wnd_super(reg_params):
    """
    category:手工干预
    brief:注册常驻参数窗口。窗口全局唯一,可通过此接口追加注册。使用方法请参考手工干预Super示例策略。
    desc:注册一个常驻的参数输入窗口,用户在窗口中输入参数后,通过点击发送并清空或者用F8快捷键即可将参数发送给策略,策略响应回调函数为on_recv_fast_params,只允许在初始化函数中调用
    :param reg_params:注册参数，dict类型。支持的参数key包括：
    'account_list': list列表，资金账号。
    'download_order_mode': int类型，下载订单的范围,0-MQuant级别订单，1-资金账号级别订单。
    'download_all_data_time': str类型，全量下载所有数据时间，hh:mm:ss格式。
    :return: 0成功，-1失败
    """
    return register_fast_param_wnd_super_impl(reg_params)






class HtEtfHandler(object):
    """
    ETF处理类,与ETF相关的操作及数据获取通过此类实现
    category:ETF申赎
    category-desc:ETF申赎,支持查询ETF清单数据,支持ETF申赎
    """

    def __init__(self, etfFundSymbol):
        """
        brief:构造函数
        :param etfFundSymbol: etf基金代码
        """
        self.etf_fund_symbol = etfFundSymbol  # etf基金代码
        self.etf_constituent_list = {}  # eft成分券列表,key为成分券证券代码
        self.etf_info = HtEtfInfo()  # etf信息

    def getEtfInfo(self):
        """
        brief:查询ETF基础信息
        desc: 查询ETF基础信息,包括申赎代码、申赎单位基金份额、预估现金差额、最大现金替代比例等。
        :return:HtEtfInfo对象,失败返回None
        """
        if self.etf_info.etf_fund_symbol == '':
            self.etf_info = get_etf_info_impl(self.etf_fund_symbol)
        return self.etf_info

    def getEtfConstituentList(self):
        """
        brief:查询ETF成分券信息
        desc: 查询ETF成分券信息,包括成分券代码、样本数量、现金替代金额、是否必须现金替代等
        :return:成分券信息列表，list<HtEtfConstituentInfo>
        """
        if len(self.etf_constituent_list) == 0:
            self.etf_constituent_list = get_etf_constituent_list_impl(self.etf_fund_symbol)
        return self.etf_constituent_list.values()

    def getEtfConstituentSymbols(self):
        """
        brief:查询ETF成分券列表
        desc: 查询ETF成分券列表
        :return:ETF成分券的证券代码列表,list<str>
        """
        if len(self.etf_constituent_list) == 0:
            self.etf_constituent_list = get_etf_constituent_list_impl(self.etf_fund_symbol)
        return self.etf_constituent_list.keys()

    def getEftConstituentInfo(self, constituentSymbol):
        """
        brief:查询ETF指定成分券信息
        desc: 查询ETF指定成分券信息
        :param constituentSymbol:成分券代码
        :return:HtEtfConstituentInfo类对象
        """
        if len(self.etf_constituent_list) == 0:
            self.etf_constituent_list = get_etf_constituent_list_impl(self.etf_fund_symbol)
        return self.etf_constituent_list.get(constituentSymbol)


    def etf_purchase_redemption(self, amount, style=None, side='long', pindex=0, msg_type=-1):
        """
        brief:ETF申赎
        desc: ETF基金申赎接口
        :param amount:基金申赎数量, 正数表示申购, 负数表示赎回
        :param style:该参数已废弃
        :param side:该参数已废弃
        :param pindex:该参数已废弃
        :param msg_type:该参数已废弃
        :return:Order对象或者None, 如果创建订单成功, 则返回Order对象, 失败则返回None
        """
        return etf_purchase_redemption_impl(self.etf_fund_symbol, amount, style, side, pindex, msg_type)


class MarginTradeHandler(object):
    """
    信用交易处理类
    category:信用交易
    category-desc:信用交易,支持融资买入、融券卖出、担保品买卖、买券还券、卖券还款、直接还款,支持查询信用资产、担保品列表、融资融券标的列表、信用合约、账户可融券标的额度、账户实时可交易的标的数量
    """
    __impl = HtMarginTradeHandler()


    @staticmethod
    def margincash_open(security, amount, style=None, pindex=0, batch_no=-1, msg_type=-1):
        """
        brief:融资买入
        desc: 融资买入
        :param security: 标的代码,支持单标的和多标的,多标的用list传入
        :param amount: 交易数量,应与security对应，多标时用list传入
        :param style:参见OrderStyle, 支持限价LimitOrderStyle和市价MarketOrderStyle,None默认为MarketOrderStyle的最优五档即时成交剩余撤销(沪市深市均可),用户也可选择其他类型
        :param pindex:该参数已废弃
        :param batch_no:批次号,可以自定义批次号,需要保证同一资金账号下全局唯一,非必填,有效批次号为最大不超过2147483647的正整数
        :param msg_type:该参数已废弃
        :return:list<Order>对象或者None, 如果创建委托成功, 则返回list<Order>对象, 失败则返回None
        """
        return margincash_open_impl(security, amount, style, pindex, batch_no, msg_type)

    @staticmethod
    def margincash_close(security, amount, contract_no='', style=None, pindex=0, batch_no=-1, msg_type=-1):
        """
        brief:卖券还款
        desc: 卖券还款
        :param security:标的代码,支持单标的和多标的,多标的用list传入
        :param amount:交易数量,应与security对应，多标时用list传入
        :param contract_no: 合约编号,如果为空,表示按照默认顺序归还
        :param style:参见OrderStyle, 支持限价LimitOrderStyle和市价MarketOrderStyle,None默认为MarketOrderStyle的最优五档即时成交剩余撤销(沪市深市均可),用户也可选择其他类型
        :param pindex:该参数已废弃
        :param batch_no:批次号,可以自定义批次号,需要保证同一资金账号下全局唯一,非必填,有效批次号为最大不超过2147483647的正整数
        :param msg_type:该参数已废弃
        :return:list<Order>对象或者None, 如果创建委托成功, 则返回list<Order>对象, 失败则返回None
        """
        return margincash_close_impl(security, amount, contract_no, style, pindex, batch_no, msg_type)

    @staticmethod
    def marginsec_open(security, amount, position_type=PositionType.normal, style=None, pindex=0, batch_no=-1,
                       msg_type=-1):
        """
        brief:融券卖出
        desc: 融券卖出,不支持市价单
        :param security:标的代码,支持单标的和多标的,多标的用list传入
        :param amount:交易数量,应与security对应，多标时用list传入
        :param position_type:头寸类型,PositionType类型，支持普通头寸和专项头寸,默认为普通头寸（PositionType.normal）
        :param style:参见OrderStyle, 支持限价LimitOrderStyle
        :param pindex:该参数已废弃
        :param batch_no:批次号,可以自定义批次号,需要保证同一资金账号下全局唯一,非必填,有效批次号为最大不超过2147483647的正整数
        :param msg_type:该参数已废弃
        :return:list<Order>对象或者None, 如果创建委托成功, 则返回list<Order>对象, 失败则返回None
        """
        return marginsec_open_impl(security, amount, position_type, style, pindex, batch_no, msg_type)

    @staticmethod
    def marginsec_close(security, amount, contract_no='', position_type=PositionType.normal, style=None, pindex=0,
                        batch_no=-1, msg_type=-1):
        """
        brief:买券还券
        desc: 买券还券
        :param security:标的代码,支持单标的和多标的,多标的用list传入
        :param amount:交易数量,应与security对应，多标时用list传入
        :param contract_no:合约编号,如果为空,表示按照默认顺序归还
        :param position_type: 头寸类型,PositionType类型，支持普通头寸和专项头寸,默认为普通头寸（PositionType.normal）
        :param style:参见OrderStyle, 支持限价LimitOrderStyle和市价MarketOrderStyle,None默认为MarketOrderStyle的最优五档即时成交剩余撤销(沪市深市均可),用户也可选择其他类型
        :param pindex:该参数已废弃
        :param batch_no:批次号,可以自定义批次号,需要保证同一资金账号下全局唯一,非必填,有效批次号为最大不超过2147483647的正整数
        :param msg_type:该参数已废弃
        :return:list<Order>对象或者None, 如果创建委托成功, 则返回list<Order>对象, 失败则返回None
        """
        return marginsec_close_impl(security, amount, position_type, contract_no, style, pindex, batch_no, msg_type)

    @staticmethod
    def marginsec_direct_refund(security, amount, position_type=PositionType.normal, contract_no='', pindex=0,
                                batch_no=-1, msg_type=-1):
        """
        brief:直接还券
        desc: 直接还券
        :param security: 标的代码,支持单标的和多标的,多标的用list传入
        :param amount:数量,应与security对应，多标时用list传入
        :param position_type:头寸类型,PositionType类型，支持普通头寸和专项头寸,默认为普通头寸（PositionType.normal）
        :param contract_no: 合约编号,如果为空,表示按照默认顺序归还
        :param pindex:该参数已废弃
        :param batch_no:批次号,可以自定义批次号,需要保证同一资金账号下全局唯一,非必填,有效批次号为最大不超过2147483647的正整数
        :param msg_type:该参数已废弃
        :return:list<Order>对象或者None, 如果创建委托成功, 则返回list<Order>对象, 失败则返回None
        """
        return marginsec_direct_refund_impl(security, amount, position_type, contract_no, pindex, batch_no, msg_type)

    @staticmethod
    def margincash_direct_refund(value, contract_no='', pindex=0, msg_type=-1):
        """
        brief:直接还款
        desc: 直接还款
        :param value:  还款金额
        :param contract_no:合约编号,如果为空,表示按照默认顺序归还
        :param pindex:该参数已废弃
        :param msg_type:该参数已废弃
        :return:MResponseInfo对象
        """
        return margincash_direct_refund_impl(value, contract_no, pindex, msg_type)

    @staticmethod
    def margin_trade(security, amount, style=None, pindex=0, batch_no=-1, msg_type=-1):
        """
        brief:担保品交易
        desc: 普通信用交易,即担保品买卖
        :param security: 标的代码,支持单标的和多标的,多标的用list传入
        :param amount: 数量,应与security对应，多标时用list传入,数量<0表示卖出
        :param style: 参见OrderStyle, 支持限价LimitOrderStyle和市价MarketOrderStyle,None默认为MarketOrderStyle的最优五档即时成交剩余撤销(沪市深市均可),用户也可选择其他类型
        :param pindex:该参数已废弃
        :param batch_no:批次号,可以自定义批次号,需要保证同一资金账号下全局唯一,非必填,有效批次号为最大不超过2147483647的正整数
        :param msg_type:该参数已废弃
        :return:list<Order>对象或者None, 如果创建委托成功, 则返回list<Order>对象, 失败则返回None
        """
        return margin_trade_impl(security, amount, style, pindex, batch_no, msg_type)

    @staticmethod
    def get_margincash_stocks():
        """
        brief:查询融资标的
        desc: 获取融资标的列表,返回list<str>
        :return:返回上交所、深交所最近一次披露的的可融资标的列表的list。
        """
        return MarginTradeHandler.__impl.get_margincash_stocks()

    @staticmethod
    def get_marginsec_stocks():
        """
        brief:查询融券标的
        desc: 获取融券标的列表
        :return:返回可融券标的列表，list<str>。
        """
        return MarginTradeHandler.__impl.get_marginsec_stocks()

    @staticmethod
    def get_margin_symbol_list(symbol=''):
        """
        brief:从柜台查询两融标的数据(账号相关)
        desc: 查询两融标的数据,此接口直接从柜台查询,会限定最高频率,当前限频最高10s一次
        :param symbol: 指定查询的标的,非必填。为空时则为查询全部。
        :return: 查询成功,返回MarginSymbolRsp类对象
        """
        return MarginTradeHandler.__impl.get_margin_symbol_list_from_counter(symbol)

    @staticmethod
    def get_margin_contract(contract_no=''):
        """
        brief:查询信用合约
        desc: 查询信用合约,支持查询所有合约或者按照合约编号查询单笔合约
        :param contract_no:合约编号
        :return: 查询成功,返回dict<contract_no,MarginContract>
        """
        rsp = MarginTradeHandler.__impl.get_margin_contract(contract_no)
        return rsp.margin_contract_list

    @staticmethod
    def get_margin_contract_ex(contract_no=''):
        """
        brief:查询信用合约
        desc: 查询信用合约,支持查询所有合约或者按照合约编号查询单笔合约
        :param contract_no:合约编号
        :return: 返回MarginContractRsp对象
        """
        return MarginTradeHandler.__impl.get_margin_contract(contract_no)

    @staticmethod
    def get_margin_assert():
        """
        brief:查询信用资产
        desc: 查询信用资产。信用资产非实时更新,会定时从柜台同步,目前更新时间间隔为1分钟。
        :return: 查询成功,返回MarginAssert类对象,失败返回None
        """
        return MarginTradeHandler.__impl.get_margin_assert()

    @staticmethod
    def get_assure_security_list():
        """
        brief:查询担保券列表
        desc: 查询担保券列表
        :return:担保券列表，dict<symbol,discount_ratio>，其中key为证券代码，vlaue为折算比例
        """
        return MarginTradeHandler.__impl.get_assure_security_list()

    @staticmethod
    def get_margin_security_info(symbol='', position_type=PositionType.undefine):
        """
        brief:查询账户可融券信息
        desc: 查询账户可融券信息
        :param symbol:指定查询的代码,不指定则查询全部
        :param position_type:指定的头寸类型,默认查询全部
        :return:list<MarginSecurityInfo>或者None
        """
        return MarginTradeHandler.__impl.get_margin_security_info(symbol, position_type)

    @staticmethod
    def get_margin_security_info_ex(symbol='', position_type=PositionType.undefine):
        """
        brief:查询账户可融券信息
        desc: 查询账户可融券信息,与get_margin_security_info功能一致,返回结果符合标准结构,支持错误信息处理。
        :param symbol:指定查询的代码,不指定则查询全部
        :param position_type:指定的头寸类型,默认查询全部
        :return:返回MarginSecurityInfoRsp对象
        """
        return MarginTradeHandler.__impl.get_margin_security_info_ex(symbol, position_type)

    @staticmethod
    def get_avaliable_qty_for_trade(symbol, entrust_type, side, style=None, position_prop=PositionType.normal):
        """
        brief:查询大约可交易数量
        desc: 查询大约可交易数量,后台会根据输入条件实时计算大约可交易数量,为了避免对柜台造成太大压力,目前限制至少间隔3s查询一次。
        :param symbol:标的
        :param entrust_type:委托类型,EntrustType类型,必填
        :param side:交易方向,OrderSide类型,必填
        :param style:参见OrderStyle, 支持限价LimitOrderStyle和市价MarketOrderStyle,None默认为MarketOrderStyle的最优五档即时成交剩余撤销(沪市深市均可),用户也可选择其他类型
        :param position_prop:头寸类型,PositionType类型，支持普通头寸和专项头寸,默认为普通头寸（PositionType.normal）
        :return:返回指定条件交易的最大可交易数量
        :return qty, error_info: 1）请求失败,qty为'',error_info为原因；2）请求成功,qty为整数,error_info为''
        """
        return MarginTradeHandler.__impl.get_avaliable_qty_for_trade(symbol, entrust_type, side, style, position_prop)

    @staticmethod
    def get_collateral_transferable_qty_for_trade(side, symbol, security_account, counter_party_fund_account, counter_party_security_account):
        """
        brief:查询担保品交存/提取可用数量
        desc: 查询担保品交存/提取可用数量
        :param side: 划转方向,数值类型,必传。1：普通->信用，2：信用->普通
        :param symbol: 标的
        :param security_account: 信用股东账号
        :param counter_party_fund_account: 普通资金账号
        :param counter_party_security_account: 普通股东账号
        :return qty, error_info: 1）请求失败,qty为'',error_info为原因；2）请求成功,qty为整数,error_info为''
        """
        return MarginTradeHandler.__impl.get_collateral_transferable_qty_for_trade(side,
                                                                                   symbol,
                                                                                   security_account,
                                                                                   counter_party_fund_account,
                                                                                   counter_party_security_account)

    @staticmethod
    def get_margin_asset_from_counter():
        """
        brief:从柜台查询信用资产
        desc: 查询信用资产,成功返回MarginAssert 类对象,失败返回None。
        :return: 查询成功,返回MarginAssetRsp类对象,此接口直接从柜台查询,会限定最高频率,当前限频最高10s一次
        """
        return MarginTradeHandler.__impl.get_margin_assert_from_counter()


class AlgoTradeHandler(object):
    """
    算法交易模块
    category:算法交易
    category-desc:对接华泰算法交易平台,提供TWAP、VWAP等算法能力,有需求可联系Matic技术支持
    """

    def __init__(self):
        pass

    @staticmethod
    def stop_instance(instId):
        """
        brief:停止算法实例
        desc: 停止算法实例,MQuant策略实例停止时,不会自动停止启动的算法实例,策略如果需要停止算法,需要主动调用该接口。注意,停止算法实例请求可能会执行失败,需要通过查询目标实例状态是否确实是已停止。
        :param instId:算法实例ID
        :return:CreateAlgoInstanceRsp 类型
        """
        return stop_instance_impl(instId)

    @staticmethod
    def pause_instance(instId):
        """
        brief:暂停算法实例
        desc: 暂停算法实例,注意,暂停算法实例请求可能会执行失败,需要通过查询目标实例状态是否确实是已暂停。
        :param instId:算法实例ID
        :return:CreateAlgoInstanceRsp 类型
        """
        return pause_instance_impl(instId)

    @staticmethod
    def resume_instance(instId):
        """
        brief:恢复算法实例
        desc: 恢复算法实例,注意,恢复算法实例请求可能会执行失败,需要通过查询目标实例状态是否确实是运行中。
        :param instId:算法实例ID
        :return:CreateAlgoInstanceRsp 类型
        """
        return resume_instance_impl(instId)

    @staticmethod
    def get_instance_info(instId):
        """
        brief:查询算法实例信息
        desc: 查询算法实例信息
        查询获取实例信息,包含实例状态、进度、标的进度等信息。当前仅提供查询接口,不提供推送接口。
        :param instId:算法实例ID
        :return:成功,返回AlgoInstanceInfo对象,失败返回None
        """
        return get_instance_info_impl(instId)

    @staticmethod
    def get_instance_id_list(algo_global_type=AlgoGlobalType.algo):
        """
        brief:查询算法实例列表
        desc: 查询当前用户的所有实例列表
        :return:算法实例ID列表，[inst_id1,inst_id2,...],失败返回None
        """
        return get_instance_id_list_impl(algo_global_type)

    @staticmethod
    def start_split_order_algo_instance(account_type, algo_params, async=False):
        """
        brief:创建算法实例（包含T0）
        desc: 创建算法实例，创建后立即启动
        算法的具体功能及参数说明,请参考算法介绍：https://inst.htsc.com/helpOnline
        :param account_type: 账户类型,AccountType类型
        :param algo_params: 算法参数,SplitOrderAlgoParam类型
        :param async: 算法创建方式，False：同步（默认） True：异步，该模式下返回值中无算法实例ID信息。
        :return:CreateAlgoInstanceRsp 类型,如果成功,返回实例ID,否则会返回错误信息
        :remark:创建算法单，特别是异步创建时，策略可能无法及时感知算法实例ID的情况，对于在此期间的对应算法订单无法判断为本策略订单，需要按使用场景考虑勾选“账号级交易推送”
                异步创建可能会遇到后台创建失败的场景，目前可通过get_instance_id_by_client_id来间接确认结果
        """
        return start_split_order_algo_instance_impl(account_type, algo_params, async)

    @staticmethod
    def get_instance_detial_from_service(inst_id, custom_field):
        """
        brief:查询算法实例详情信息
        desc: 查询算法实例详情信息
        :param inst_id: 算法实例ID
        :param custom_field:该参数已废弃
        :return:MResponseInfo类型,其中MResponseInfo.data为AlgoInstanceInfo类型
        """
        return get_algo_instance_detial_from_service_impl(inst_id, custom_field)

    @staticmethod
    def get_T0_instance_info(instId):
        """
        brief:查询T0算法实例信息
        desc: 查询T0算法实例信息,包含实例状态、进度、标的进度等信息
        :param instId: 算法实例ID
        :return:MResponseInfo类型,其中MResponseInfo.data为T0AlgoInstanceInfo对象
        """
        return get_T0_instance_info_impl(instId)

    @staticmethod
    def get_T0_instance_symbol_info(instId, symbol):
        """
        brief:查询T0算法实例标的进度信息
        desc: 查询T0算法实例标的进度信息
        :param instId: 实例ID
        :param symbol: 标的
        :return:MResponseInfo类型,其中MResponseInfo.data为T0AlgoSymbolInfo对象
        """
        return get_T0_instance_symbol_info_impl(instId, symbol)

    @staticmethod
    def get_T0_instance_performance(account_type, algo_type=None):
        """
        brief:查询资金账号T0绩效
        desc: 查询资金账号T0绩效
        :param account_type: 账户类型,AccountType类型
        :param algo_type: T0策略类型,AlgoType中的smarT系列。None则包含所有T0策略
        :return:MResponseInfo类型,其中MResponseInfo.data为T0AlgoPerformance对象
        """
        return get_T0_instance_performance_impl(account_type, algo_type)

    @staticmethod
    def get_instance_id_by_client_id(cl_inst_id):
        """
        brief:通过自定义实例ID查询对应的实例ID
        desc: 通过自定义实例ID查询对应的实例ID，以便于进一步查询实例信息
        :param cl_inst_id: 自定义实例ID
        :return:MResponseInfo类型
                查询成功时MResponseInfo.err_code='0'，MResponseInfo.data为实例ID，若实例ID为空则可能实例信息还未就绪，可重新尝试查询
                失败时MResponseInfo.err_code='-1'，MResponseInfo.error_info包含具体的创建错误信息,此时表示创建已失败
                失败时MResponseInfo.err_code='1',此时表示创建超时，存在超时但实际创建成功正常下单的可能，请尽快联系系统管理员确认后台真实状态，避免重复下单超单。
        """
        return get_instance_id_by_client_id_impl(cl_inst_id)



class HtSGEEtfHandler(object):
    """
    上海黄金交易所ETF处理类,与金交所ETF相关的操作及数据获取通过此类实现
    category:金交所ETF交易
    category-desc:金交所ETF交易,支持查询ETF清单数据,支持ETF买卖、申赎，支持现货合约买卖等,支持对于快速柜台的证券划转
    remark:1、HtSGEEtfHandler对象构建时，对应的ETF代码使用实际市场的格式，比如518880.SH
           2、order_normal、cancel_orders属于内置静态方法，无需构建HtSGEEtfHandler对象即可实际调用
           3、对于申赎报单，委托成交内的代码所属市场为上海黄金交易所，比如518880.SGE
           4、现货合约、ETF买卖均可直接使用order_normal、cancel_orders，需注意对应的AccountType类型
    """

    def __init__(self, etfFundSymbol):
        """
        brief:构造函数
        :param etfFundSymbol: etf基金代码，
        """
        self.etf_fund_symbol = etfFundSymbol  # etf基金代码
        self.etf_constituent_list = {}  # eft成分券列表,key为成分券证券代码
        self.etf_info = HtSGEEtfInfo()  # etf信息

    def getEtfInfo(self):
        """
        brief:查询ETF基础信息
        desc: 查询ETF基础信息,包括申赎单位基金份额、合约数量、申赎上限等。
        :return:HtSGEEtfInfo对象,失败返回None
        """
        if self.etf_info.etf_fund_symbol == '':
            self.etf_info = get_SGE_etf_info_impl(self.etf_fund_symbol)
        return self.etf_info

    def getEtfConstituentList(self):
        """
        brief:查询ETF成分券信息
        desc: 查询ETF成分券信息,包括成分券代码、现金差额等
        :return:成分券信息列表，list<HtSGEEtfConstituentInfo>
        """
        if len(self.etf_constituent_list) == 0:
            self.etf_constituent_list = get_SGE_etf_constituent_list_impl(self.etf_fund_symbol)
        return self.etf_constituent_list.values()

    def getEtfConstituentSymbols(self):
        """
        brief:查询ETF成分券列表
        desc: 查询ETF成分券列表
        :return:ETF成分券的证券代码列表,list<str>
        """
        if len(self.etf_constituent_list) == 0:
            self.etf_constituent_list = get_SGE_etf_constituent_list_impl(self.etf_fund_symbol)
        return self.etf_constituent_list.keys()

    def getEftConstituentInfo(self, constituentSymbol):
        """
        brief:查询ETF指定成分券信息
        desc: 查询ETF指定成分券信息
        :param constituentSymbol:成分券代码
        :return:HtSGEEtfConstituentInfo类对象
        """
        if len(self.etf_constituent_list) == 0:
            self.etf_constituent_list = get_SGE_etf_constituent_list_impl(self.etf_fund_symbol)
        return self.etf_constituent_list.get(constituentSymbol)

    def etf_purchase(self, amount, constituent_info, unit_no=''):
        """
        brief:ETF申购
        desc: ETF基金申购接口
        特别注意：申购时，柜台申购以成分总重量为准，所以constituent_info必须保证正确填写所期望申购ETF单位对应的总重量。
                例如1个单位的ETF要求3kg，则必须保证constituent_info中总重量为3kg，以此类推，2个单位则需要6kg。
        :param amount:基金申购数量（单位）, 需要注意N个单位，对应的成分需要按照合约数量*N凑足足够的数量
        :param constituent_info:基金对应成分信息，list<HtSGEEtfConInfo>
        :param unit_no:托管单元（席位号），在金交所做ETF申赎可以指定
        :return:Order对象,具体是否报单成功需要关注Order对象的error_code和cancel_info
        """
        return etf_purchase_SGE_impl(self.etf_fund_symbol, amount, constituent_info, unit_no)

    def etf_redemption(self, amount, unit_no=''):
        """
        brief:ETF赎回
        desc: ETF基金赎回接口
        :param amount:基金赎回数量（单位）
        :param unit_no:托管单元（席位号），在金交所做ETF申赎可以指定
        :return:Order对象,具体是否报单成功需要关注Order对象的error_code和cancel_info
        """
        return etf_redemption_SGE_impl(self.etf_fund_symbol, amount, unit_no)

    @staticmethod
    def order_normal(order_request, limit_price_type='0', account_type=AccountType.metal):
        """
        brief:统一报单接口
        desc: 提供统一报单接口,在原order_normal基础上，扩展支持金交所的现货交易
        :param order_request: 报单请求,单笔报单为OrderRequest类型,批量报单为list<OrderRequest>类型
        :param limit_price_type: 限价单子类型: '0':普通限价单，'1':限价FOK指令, '2':限价FAK指令。仅现货合约限价报单方式下有效
        :param account_type:账户类型,AccountType类型,默认为黄金账户（AccountType.metal）
        :return:Order对象或者None, 如果异步报单请求发送成功, 则返回Order对象, 失败则返回None,批量报单返回list<Order>或None,可使用batch_no作为透传字段
        :remark:现货延期交收合约（T+D）的说明如下
                1、支持买入开仓、卖出平仓、卖出开仓、买入平仓：
                    需要在报单请求中填写action（开/平）,交易方向依然使用side。
                    例如买入开仓side=OrderSide.BUY，action=OrderAction.OPEN
                    对应持仓Position中，通过option_hold_type来判断多空仓，具体参见OptionHoldType定义。（注意不可使用position_prop，该字段用于期货）
                2、支持交割/中立仓：
                    委托属性entrust_prop填写EntrustProp.delivery或EntrustProp.neutral_pos。交货（SELL）/收货（BUY）使用交易方向side字段。
                    例如交割收货申报side=OrderSide.BUY，entrust_prop=EntrustProp.delivery
        """
        return order_normal_SGE_impl(order_request, limit_price_type, account_type)

    @staticmethod
    def cancel_orders(orders, account_type=AccountType.metal):
        """
        brief:批量撤单接口
        desc: 批量撤单接口,在原cancel_orders基础上，扩展支持金交所的现货交易
        :param account_type:账户类型,AccountType类型,默认为黄金账户（AccountType.metal）
        :param orders: batch_cancel_order_item列表
        :return: 返回list<Order>,失败为空列表,列表元素也可能是None
        :remark: 期货暂不支持按批次号撤单
        """
        return cancel_orders_SGE_impl(orders, account_type)



