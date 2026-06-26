#encoding: utf-8
"""
策略描述
根据前一个交易日的收盘价、最高价和最低价数据通过一定方式计算出六个价位，从大到小依次为：
突破买入价（Bbreak,阻力位3)、观察卖出价(Ssetup，阻力位2)、反转卖出价(Senter，阻力位1)
反转买入价(Benter，支撑位1)、观察买入价(Bsetup，支撑位2)、突破卖出价(Sbreak，支撑位3)。
以此来形成当前交易日盘中交易的触发条件。
交易规则：
反转:
持多单，当日内最高价超过观察卖出价后，盘中价格出现回落，且进一步跌破反转卖出价构成的支撑线时，采取反转策略，即在该点位反手做空；
持空单，当日内最低价低于观察买入价后，盘中价格出现反弹，且进一步超过反转买入价构成的阻力线时，采取反转策略，即在该点位反手做多；
突破:
在空仓的情况下，如果盘中价格超过突破买入价，则采取趋势策略，即在该点位开仓做多；
在空仓的情况下，如果盘中价格跌破突破卖出价，则采取趋势策略，即在该点位开仓做空；

本策略做了适当调整，主要是弱化了当前仓位的限制
"""
from mquant_api import *
from mquant_struct import *

def strategy_params():
    dict_params = {
       '证券代码':{'value':'601688.SH/000002.SZ','desc':'策略交易的标的代码'},		#'desc'字段可填写，也可不填写
        '单次卖出最大数量':{'value':1000,'desc':'满足卖出条件时单次卖出最大数量'},
        '单次卖出最小数量':{'value':100,'desc':'满足卖出条件时单次卖出最小数量'},
        '单次卖出仓位比例':{'value':0.2, 'desc':'满足卖出条件时的单次卖出数量占可卖数量的比例'},
        '单次买入最大数量': {'value': 1000, 'desc': '满足买入条件时单次买入最大数量'},
        '单次买入最小数量': {'value': 100, 'desc': '满足买入条件时单次买入最小数量'},
        '单次买入仓位比例': {'value': 0.2, 'desc': '满足买入条件时的单次买入数量占可卖数量的比例'},   #考虑到T+0
    }
    return dict_params

def calcu_fix_params(code,klinedata):
    """
    根据k线计算6个固定价位
    """
    print('查询返回k线数据：', klinedata.data)
    if klinedata is not None and len(klinedata.data['date']) >= 1:
        
        pivot = (klinedata.data['high'][0] + klinedata.data['low'][0] + klinedata.data['close'][0])/3
        
        #三个阻力位
        g.fix_params_dict[code]['resistance_level_3'] = klinedata.data['high'][0] + 2 * (pivot-klinedata.data['low'][0])
        g.fix_params_dict[code]['resistance_level_2'] = pivot + klinedata.data['high'][0] - klinedata.data['low'][0]
        g.fix_params_dict[code]['resistance_level_1'] = 2*pivot-klinedata.data['low'][0]
        
        #三个支撑位
        g.fix_params_dict[code]['support_level_3'] = klinedata.data['low'][0] + 2 * (klinedata.data['high'][0]-pivot)
        g.fix_params_dict[code]['support_level_2'] = pivot - (klinedata.data['high'][0] - klinedata.data['low'][0])
        g.fix_params_dict[code]['support_level_1'] = 2*pivot-klinedata.data['high'][0]
        g.fix_params_dict[code]['ready_flag'] = True
#        print(g.fix_params_dict)
    
def initialize(context):
    """
    策略初始化，启动策略时调用，用户可在初始化函数中订阅行情、设置标的、设置定时处理函数等
    该函数中允许读取文件，除此之外的其他函数禁止读取文件
    :param context:
    :return:
    :remark:必须实现
    """
    #订阅标的证券的实时行情,订阅时会自动异步查询近180天的日k数据
    g.security_list=context.run_params['证券代码'].strip('/').split('/')
    #固定价字典，key为code，value为{价位名称:价位值,...}的字典
    g.fix_params_dict = {}
    g.max_sell_amount = int(context.run_params['单次卖出最大数量'])
    g.min_sell_amount = int(context.run_params['单次卖出最小数量'])
    g.sell_ratio = float(context.run_params['单次卖出仓位比例'])
    g.max_buy_amount = float(context.run_params['单次买入最大数量'])
    g.min_buy_amount = float(context.run_params['单次买入最小数量'])
    g.buy_ratio = float(context.run_params['单次买入仓位比例'])
    #表示还未计算R-Breaker的六个固定价位
    for code in g.security_list:
        g.fix_params_dict[code] = {}
        g.fix_params_dict[code]['ready_flag'] = False
        calcu_fix_params(code,get_kline_data_1d_from_init_date(code,-1,datetime.datetime.now(),sync=True))

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
#    print('recv tick msg, code:%s' % tick.code)
    symbol = normalize_code_jq_to_mquant(tick.code)
    
    if symbol in g.security_list and g.fix_params_dict[symbol]['ready_flag']:
    #当日内最高价超过观察卖出价(阻力位2)后，盘中价格出现回落，且进一步跌破反转卖出价（阻力位1）构成的支撑线时，采取反转策略，即在该点位（反手、开仓）做空
        if tick.high > g.fix_params_dict[symbol]['resistance_level_2']:     #盘中最高超过阻力位2
            if tick.current < g.fix_params_dict[symbol]['resistance_level_1']:  #回跌到低于阻力位1
                #计算卖出数量
                log.debug('满足条件1，开始卖出证券：%s' % symbol)
                enable_amount = context.subportfolios[context.subportfolio_type_index['stock']].long_positions[symbol].closeable_amount
                if enable_amount < 100:
                    order(symbol,-1 * enable_amount)
                    log.debug('证券：%s可用数量不足100股，全部卖出，数量：%d' % (symbol, amount))
                else:
                    amount = min(max(g.sell_ratio * enable_amount,g.min_sell_amount),g.max_sell_amount)
                    amount = int(amount)/100 * 100
                    if amount < 100:
                        log.debug('可用证券数量不足' % (symbol, amount))
                    else:
                        order(symbol,-1 * amount)
                        log.debug('证券：%s卖出结束，数量：%d' % (symbol, amount))
                    return

    #当日内最低价低于观察买入价(支撑位2)后，盘中价格出现反弹，且进一步超过反转买入价（支撑位1）构成的阻力线时，采取反转策略，即在该点位（反手、开仓）做多；
        elif tick.low < g.fix_params_dict[symbol]['support_level_2']:
            if tick.current > g.fix_params_dict[symbol]['support_level_1']:
                # order(symbol, -1 * context.portfolio.positions[symbol].closeable_amount)  # 全部卖出
                log.debug('满足条件2，开始下单，证券：%s' % symbol)
                amount = min(max(g.buy_ratio * context.subportfolios[context.subportfolio_type_index['stock']].long_positions[symbol].closeable_amount,g.min_buy_amount), g.max_buy_amount)
                if amount < 0:
                    log.debug('可用证券数量不足' % (symbol, amount))
                else:
                    order(symbol, amount)
                    log.debug('证券：%s下单结束，数量：%d' % (symbol, amount))
                return
        
        #在空仓的情况下，如果盘中价格超过突破买入价(阻力位3)，则采取趋势策略，即在该点位开仓做多；(不考虑空仓情况)
        elif tick.current > g.fix_params_dict[symbol]['resistance_level_3']:
            log.debug('满足条件3，开始下单，证券：%s' % symbol)
            amount = min(max(g.buy_ratio * context.subportfolios[context.subportfolio_type_index['stock']].long_positions[symbol].closeable_amount,g.min_buy_amount), g.max_buy_amount)
            if amount < 0:
                log.debug('可用证券数量不足' % (symbol, amount))
            else:
                order(symbol, amount)
                log.debug('证券：%s下单结束，数量：%d' % (symbol, amount))
            return
        #在空仓的情况下，如果盘中价格跌破突破卖出价，则采取趋势策略，即在该点位开仓做空。
        elif tick.current < g.fix_params_dict[symbol]['support_level_3']:
            log.debug('满足条件4，开始下单，证券：%s' % symbol)
            enable_amount = context.subportfolios[context.subportfolio_type_index['stock']].long_positions[symbol].closeable_amount
            log.debug('获取可用数量结束：%d' % enable_amount)
            #            print('可用数量：',enable_amount)
            amount = min(max(g.buy_ratio * enable_amount,g.min_buy_amount), g.max_buy_amount)
            log.debug('计算下单数量：%d' % amount)
            if amount < 0:
                log.debug('可用证券数量不足' % (symbol, amount))
            else:
                order(symbol, amount)
                log.debug('证券：%s下单结束，数量：%d' % (symbol, amount))
            return

def on_strategy_end(context):
    """
    策略结束时调用，用户可以在此函数中进行一些汇总分析、环境清理等工作
    :param context:
    :return:
    :remark:可选实现
    """
    #取消订阅股票
    unsubscribe(g.security_list)