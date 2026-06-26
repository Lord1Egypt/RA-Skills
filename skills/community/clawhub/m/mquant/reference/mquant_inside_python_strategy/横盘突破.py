#encoding: utf-8
"""
策略描述
横盘突破在过去N（可调整）根K线的高低点围绕中轴上下0.5%（可调整）的范围内波动时；
上轨＝过去N根K线的最高价；下轨＝过去N根K线的最低价；
当价格突破上轨，买入开仓；当价格跌穿下轨，卖出开仓。
"""
from mquant_api import *
from mquant_struct import *

def strategy_params():
    """
    策略可自定义运行参数，启动策略时会写入到context对象的run_params字段内
    :return:dict对象，key为参数名，value为一个包含参数默认值、参数描述（选填）的字典
    :remark:可选实现，参数由策略自由填写，自己解析
    :example:
        dict_params = {
       '证券代码':{'value':'601688.SH/000002.SZ','desc':'策略交易的标的代码'},		#'desc'字段可填写，也可不填写
       '委买价格':{'value':'17.50/27.5'},
       '委卖价格':{'value':'18.50/28.0'},
       '撤单时间间隔':{'value':10}
       }
        return dict_params
    """
    #示例如下：
    dict_params = {
       '证券代码':{'value':'601688.SH/000002.SZ','desc':'策略交易的标的代码'},		#'desc'字段可填写，也可不填写
       '参考日k数量':{'value':30, 'desc':'用作参考的日k数量N'},
       '波动区间':{'value':0.005, 'desc':'前N个交易日的波动范围'},
       'k线数量不够视为非法':{'value':True}
       }
    return dict_params

def calcu_fix_params(code,klinedata):
    """
    根据k线计算输入证券是否满足横盘突破条件，并计算前N日的最高点、最低点和中间点
    """
    g.fix_params_dict[code]['is_valid'] = False
    if klinedata is not None and len(klinedata.data['date']) > 0:
        if len(klinedata.data['date']) < g.kline_bar_num and g.ignore_sufficient_symbol:
            log.warn('证券[%s]查询获取到的k线数据仅[%d]条，证券将不会被纳入交易范围'%(code, len(klinedata.data['date'])))
        else:
            g.fix_params_dict[code]['high_level'] = klinedata.highest_price()        #上轨
            g.fix_params_dict[code]['low_level'] = klinedata.lowest_price()            #下轨
            g.fix_params_dict[code]['base_line'] = (g.fix_params_dict[code]['high_level'] + g.fix_params_dict[code]['low_level'])/2
            #判断过去N个交易日的最高、最低价是否都在中轴线一定范围内波动
            wave = (g.fix_params_dict[code]['high_level']-g.fix_params_dict[code]['base_line'])/g.fix_params_dict[code]['base_line']
            if wave > g.wave_range:
                log.info('证券[%s]不满足横盘突破条件，波动幅度[%s]大于设置的幅度范围[%s]' %(code,wave,g.wave_range))
                return
            g.fix_params_dict[code]['is_valid'] = True
        

def initialize(context):
    """
    策略初始化，启动策略时调用，用户可在初始化函数中订阅行情、设置标的、设置定时处理函数等
    该函数中允许读取文件，除此之外的其他函数禁止读取文件
    :param context:
    :return:
    :remark:必须实现
    """
    g.security_list=context.run_params['证券代码'].strip('/').split('/')
    g.fix_params_dict = {}
    g.kline_bar_num = int(context.run_params['参考日k数量'])
    g.wave_range = float(context.run_params['波动区间'])
    g.ignore_sufficient_symbol = bool(int(context.run_params['k线数量不够视为非法']))
    
    for code in g.security_list:
        g.fix_params_dict[code] = {}
        calcu_fix_params(code,get_kline_data_1d_from_init_date(code,-g.kline_bar_num,datetime.datetime.now(),sync=True))

    subscribe(g.security_list)

def handle_tick(context, tick, msg_type):
    """
    实时行情接收函数
    :param context:
    :param tick: Tick对象
    :return:
    :remark:可选实现
    :example:
    symbol = normalize_code_jq_to_mquant(tick.code)
    if symbol in g.security_list:
        if float(g.buy_dict[symbol]) > tick.current:
            log.debug('开始买入证券：%s' % symbol)
            #市价买入
            order(symbol, 1000)
        elif float(g.sell_dict[symbol]) < tick.current:
            log.debug('开始卖出证券：%s' % symbol)
            #限价卖出
            order(symbol, -1000, LimitOrderStyle(float(g.sell_dict[symbol])))
    """
    symbol = normalize_code_jq_to_mquant(tick.code)
    if symbol in g.security_list and g.fix_params_dict[symbol]['is_valid']:
        if tick.current > g.fix_params_dict[symbol]['high_level']:
            log.info('开始买入股票[%s]', symbol)
            order(symbol,1000)
        elif tick.current < g.fix_params_dict[symbol]['low_level']:
            log.info('开始卖出股票[%s]', symbol)
            order(symbol,-1000)
    

def on_strategy_end(context):
    """
    策略结束时调用，用户可以在此函数中进行一些汇总分析、环境清理等工作
    :param context:
    :return:
    :remark:可选实现
    """
    pass