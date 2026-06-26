import datetime
from abc import ABCMeta, abstractmethod
from enum import Enum


class MResponseInfo(object):
    """
    错误信息
    """

    def __init__(self):
        self.err_code = ''  # 错误码
        self.err_info = ''  # 错误信息
        self.inst_id = ''  # 实例ID
        self.custom_field = ''  # 自定义字段
        self.data = None  # 数据


class Position(object):
    """
    单只标的的持仓信息
    """

    def __init__(self):
        super(Position, self).__init__()
        self.security = ''  # 标的代码
        self.price = 0  # 最新行情价格
        self.avg_cost = 0  # 均价，废弃
        self.hold_cost = 0  # 持仓成本价
        self.init_time = 0  # 建仓时间，格式为 datetime.datetime,该字段目前保留
        self.transact_time = 0  # 最后交易时间，格式为 datetime.datetime,该字段目前保留
        self.total_amount = 0  # 总仓位
        self.closeable_amount = 0  # 可卖出的仓位
        self.locked_amount = 0  # 冻结仓位，期货、期权中包含多头冻结+空头冻结
        self.value = 0  # 标的价值，计算方法是: 股票基金市值=最新价*持仓数量，债券市值=（最新价+应计利息）*持仓数量，标准券市值=100*持仓数量
        self.side = OrderSide.UNKNOWN  # 废弃
        self.redemption_num = 0  # 可申赎数
        self.pindex = 0  # 废弃
        self.position_prop = PositionProp.LONG  # 仓位类型，股、债、基为多仓，期货分多仓和空仓
        self.init_amount = 0  # 期初数量，当日不变
        ###以下字段期货专用
        self.open_cost = 0  # 开仓均价，股票和hold_cost相同，期货=开仓成本/（总持仓*合约乘数）
        self.today_amount = 0  # 今天开的仓位，期货、期权支持
        self.old_amount = 0  # 昨持仓，期货、期权支持
        self.occupy_margin = 0  # 占用保证金
        # 开仓：交易前已占用保证金+开仓价*开仓数量*合约乘数*保证金比例；
        # 平仓：交易前已占用保证金—开仓价*平今仓数量*合约乘数*保证金比例—昨结算价*平昨仓数量*合约乘数*保证金比例
        self.close_pos_profit = 0  # 平仓盈亏（盯市），只有平仓的合约才会计入平仓盈亏,老仓采用昨结算价计算
        self.close_profit_by_trade = 0  # 平仓盈亏（逐笔）,只有平仓的合约才会计入平仓盈亏,老仓采用开仓价计算
        self.commission = 0  # 手续费
        self.contract_multiplier = 0  # 合约乘数,查询有值，推送不提供
        self.hedge_flag = HedgeFlag.UNKNOWN
        self.option_hold_type = OptionHoldType.DEFAULT  # 期权持仓类型
        self.fund_account = ''  # 资金账号
        self.stock_account = ''  # 股东账号，可用于区分多股东账号、沪港通、深港通场景
        self.security_exchange = SecurityExchangeType.UNKNOWN  # 市场，沪港通、深港通可通过市场区分
        self.income_balance = 0     # 盈亏金额，随行情变动，但无交易行为时行情变动并不会出发持仓推送，当日持仓全部卖出后，该字段会体现为标的最终的实现盈亏
        self.modify_time = None     # 更新时间,格式为 datetime.datetime


class AccountType(object):
    """
    账号属性
    """
    normal = 'stock'  # A股账号
    margin = 'stock_margin'  # 信用账号
    futures = 'futures'  # 期货
    open_fund = 'open_fund'  # 场外基金，暂不支持
    option = 'option'  # 期权
    metal = 'metal'  # 黄金
    unknown = 'unknown'  # 未知类型


class OrderSide(object):
    """
    交易方向定义
    """
    BUY = 'long'  # 买入
    SELL = 'short'  # 卖出
    UNKNOWN = ''  # 未知


class EntrustType(object):
    """
    委托类型，成交类型
    """
    entrust = '0'  # 委托
    cancelOrder = '2'  # 撤单
    creditFinancing = '6'  # 信用融资    卖券还款、融资买入
    creditMargin = '7'  # 信用融券      融券卖出、买券还券
    creditOpen = '8'  # 信用平仓
    creditTransactions = '9'  # 信用交易    担保品买卖

    # 以下仅报单中使用
    returnSecDirect = '10'  # 直接还券 (EntrustType.creditTransactions + EntrustProp.seculoan_restore)
    purchase = '11'  # 申购 (EntrustType.entrust + EntrustProp.purchase)

    UNKNOWN = ''


class EntrustProp(object):
    """
    委托属性
    """
    trade = '0'  # 买卖
    purchase = '3'  # 申购
    repurchase = '4'  # 回购，国债正逆回购使用此属性
    conversion = '7'  # 转股
    covered_transfer = '9'  # 备兑划转
    option_exercise = 'a'  # 期权行权
    redemption = 'N'  # ETF申赎
    pledge = 'f'  # 债券质押
    collteral_trans = 'R1'  # 担保品划转
    seculoan_restore = 'R3'  # 现券还券

    delivery = 'MJG'     # 交割申报(黄金交易所)
    neutral_pos = 'MZL'  # 中立仓(黄金交易所)

    UNKNOWN = ''


class ExchangeType(object):
    """
    交易所定义
    """
    SH = 'SH'  # 上海

    SZ = 'SZ'  # 深圳

    SHF = 'SHF'  # 上期

    CFFEX = 'CF'  # 中金

    ZCE = 'ZCE'  # 郑商

    DCE = 'DCE'  # 大商

    HK = 'HK'  # 港交所

    SI = 'SI'  # 申万

    BJ = "BJ"  # 北交所

    SGE = "SGE"  # 上海黄金交易所

    UNKNOWN = ''


class SecurityExchangeType(object):
    """
    证券交易市场
    """
    UNKNOWN = '-1'  # 未知

    SH = '1'  # #上交所

    SZ = '2'  # 深交所

    TZA = '9'  # 特转A

    TZB = 'A'  # 特转B

    YHJ = 'B'  # 银行间

    JJ = 'C'  # 基金

    SHB = 'D'  # 上海B

    HHK = 'G'  # 沪HK（沪港通南向）

    SZB = 'H'  # 深圳B

    HK = 'HK'  # 香港

    CFFEX = 'M'  # 中金所

    SHF = 'N'  # 上期所

    CZCE = 'O'  # 郑商所

    DCE = 'P'  # 大商所

    SZHK = 'S'  # 深HK（深港通南向）

    SSC = 'SSC'  # 沪股通（沪港通北向）

    SZC = 'SZC'  # 深股通（深港通北向）

    SGE = 'U'  # 上海黄金交易所


class MarketDataType(object):
    """
    行情类型定义
    """
    TICK = 'tick'  # tick行情（对应数据Tick）
    KLINE_1M = 'kline_1m'  # 1分钟k线（对应数据KLineDataPush）
    RECORD_ORDER = 'record_order'  # 逐笔委托（对应数据RecordOrder）
    RECORD_TRANSACTION = 'record_transaction'  # 逐笔成交（对应数据RecordTransaction）
    FUND_FLOW = 'fund_flow'  # 资金流向（对应数据FundFlow）
    ETF_ESTIMATE_INFO = 'etf_estimate_info' # ETF预估信息（对应数据EtfEstimateInfo）


class KLineDataType(object):
    """
    k线类型定义
    """
    KLINEData_1M = "kline_1m"  # 1分钟k线
    KLINEData_5M = "kline_5m"  # 5分钟线
    KLINEData_15M = "kline_15m"  # 15分钟线
    KLINEData_30M = "kline_30m"  # 30分钟线
    KLINEData_60M = "kline_60m"  # 60分钟线
    KLINEData_120M = "kline_120m"  # 120分钟线,暂不支持
    KLINEData_1D = "kline_1d"  # 日k线
    KLINEData_1W = "kline_1w"  # 周线,暂不支持
    KLINEData_15D = "kline_15d"  # 15日线，暂不支持
    KLINEData_1MON = "kline_1mon"  # 月线，暂不支持
    KLINEData_3MON = "kline_3mon"  # 3月线，暂不支持
    KLINEData_4MON = "kline_4mon"  # 4月线，暂不支持
    KLINEData_6MON = "kline_6mon"  # 半年线，暂不支持
    KLINEData_1Y = "kline_1y"  # 年线，暂不支持


class SecurityType(object):
    """
    标的类型定义
    """
    All = ""  # 所有标的

    IndexType = "1"  # 指数

    StockType = "2"  # 股票

    FundType = "3"  # 基金

    BondType = "4"  # 债券

    RepoType = "5"  # 回购

    WarrantType = "6"  # 权证，暂不支持

    OptionType = "7"  # 期权

    FuturesType = "8"  # 期货

    ForexType = "9"  # 外汇，暂不支持

    RateType = "10"  # 利率，暂不支持

    NmetalType = "11"  # 贵金属，暂不支持

    SpotType = "13"  # 现货

    UNKNOWN = "-1"


class SecuritySubType(object):
    """
    标的子类型
    """
    AsiaIndex = "01002"  # 亚洲指数

    InternationalIndex = "01003"  # 国际指数

    Systemclassificationindex = "01004"  # 系统分类指数

    Userclassificationindex = "01005"  # 用户分类指数

    Futuresindex = "01006"  # 期货指数

    Indexspot = "01007"  # 指数现货

    Ashares = "02001"  # A股（主板）

    ScienTechInnovateBoard = '02200'  # 科创板

    Smallandmediumstock = "02002"  # 中小板股

    Gemstock = "02003"  # 创业板股

    Strategicemergingboard = "02006"  # 战略新兴板

    Newthreeboard = "02007"  # 新三板

    MainboardofHongKongshares = "02008"  # 港股主板

    HongKongEquitygem = "02009"  # 港股创业板

    HongkonglistedNASDstock = "02010"  # 香港上市NASD股票

    Hongkongextendedplatestock = "02011"  # 香港扩展板块股票

    BjSelectedStock = "02022"  # 北交所精选层

    Preferredstock = "02100"  # 优先股

    Fund = "03001"  # 基金（封闭式）

    ListedopenfundLOF = "03003"  # 上市开放基金LOF

    TradingopenindexfundETF = "03004"  # 交易型开放式指数基金ETF

    Classificationsubfund = "03005"  # 分级子基金

    Extendedplatefund = "03006"  # 扩展板块基金(港)

    Redemptionfundonly = "03007"  # 仅申赎基金

    Governmentbonds = "04001"  # 政府债券（国债）

    Corporatebond = "04002"  # 企业债券

    Financialbond = "04003"  # 金融债券

    Corporatedebt = "04004"  # 公司债

    Convertiblebond = "04005"  # 可转债券

    Privatedebt = "04006"  # 私募债

    Exchangeableprivatedebt = "04007"  # 可交换私募债

    Securitiescompanysubordinateddebt = "04008"  # 证券公司次级债

    Securitiescompanyshorttermdebt = "04009"  # 证券公司短期债

    Exchangeablecorporatedebt = "04010"  # 可交换公司债

    Bondpreissue = "04011"  # 债券预发行

    Pledgetypetreasurybondrepurchase = "05001"  # 质押式国债回购

    Thecorporatebondpledgedrepo = "05002"  # 质押式企债回购

    Buybackofbuyoutbond = "05003"  # 买断式债券回购

    Bidrepurchase = "05004"  # 报价回购

    Stockoption = "07001"  # 个股期权

    ETFoption = "07002"  # ETF期权

    Indexfutures = "08001"  # 指数期货

    Commodityfutures = "08002"  # 商品期货

    Stockfutures = "08003"  # 股票期货

    Bondfutures = "08004"  # 债券期货

    Interbankinterestratefutures = "08005"  # 同业拆借利率期货

    ExchangeFundNoteFuturesExchangeFundpaperfutures = "08006"  # 外汇基金票据期货

    ExchangeForPhysicalsfuturesturntospot = "08007"  # 期货转现货


class SubPortfolioConfig(object):
    """
    仓位配置类（废弃）
    """

    def __init__(self, cash=0, type=AccountType.normal):
        """
        :param cash: 资金
        :param type: AccountType 类型
        """
        self.cash = cash
        self.type = type


###子仓位目前Matic并不支持######
class SubPortfolio(object):
    """
    某个仓位的资金，标的信息（废弃）
    """

    def __init__(self):
        self.inout_cash = 0  # 累计出入金, 当天银证转入/转出导致变化，证券买卖不会引发变化，暂不支持
        self.available_cash = 0  # 可用资金, 可用来购买证券的资金
        self.transferable_cash = 0  #: 可取资金, 即可以提现的资金, 不包括今日卖出证券所得资金
        self.locked_cash = 0  # 挂单锁住资金，暂不可用
        self.type = AccountType.normal  # 账户所属类型
        self.margin = 0  #:废弃
        self.positions = {}  # 等同于 long_positions
        self.long_positions = {}  # 多单的仓位, 一个dict, key是证券代码, value是Position对象
        self.short_positions = {}  # 空单的仓位, 一个dict, key是证券代码, value是Position对象,暂时不可用
        self.total_value = 0  #: 总资产, 包括现金, 保证金, 仓位的总价值, 可用来计算收益,A股可用
        self.returns = 0  # 总权益的累计收益,暂时不可用
        self.starting_cash = 0  # 初始资金, 暂时不可用
        self.total_liability = 0  #: 总负债, 等于融资负债、融券负债、利息总负债的总和,暂时不可用
        self.positions_value = 0  #: 持仓价值, 股票基金才有持仓价值, 期货为0,暂时不可用
        self.locked_cash_by_purchase = 0  # 基金申购未完成所冻结的金额,暂时不可用
        self.locked_cash_by_redeem = 0  # 基金赎回未到账的金额,暂时不可用
        self.locked_amount_by_redeem = 0  # 基金赎回时，冻结的份额,暂时不可用
        self.net_value = 0  #: 净资产, 等于总资产减去总负债,暂时不可用
        self.cash_liability = 0  #: 融资负债,暂时不可用
        self.sec_liability = 0  #: 融券负债,暂时不可用
        self.interest = 0  #: 利息总负债,暂时不可用
        self.maintenance_margin_rate = 0  #: 维持担保比例,暂时不可用
        self.frozen_cash = 0  # 新增字段，包含所有冻结的资金
        self.total_cash = 0  # 新增字段，当前资金
        self.settled_cash = 0  # 新增字段，期初资金
        self.market_value = 0  # 证券市值
        self.hk_available_cash = 0  # 港股可用资金

        # 以下字段为期货专用
        self.available_margin = 0  #: 可用保证金,期货、期权可用
        self.occupied_margin = 0  # 占用保证金，期货、期权可用
        self.pre_balance = 0  # 期初权益，期货可用
        self.current_balance = 0  # 客户权益，期货可用
        self.risk_level = 0  # 占用保证金/客户权益
        self.holding_profit = 0  # 盯市盈亏，以持仓成本计算的浮动盈亏
        self.close_pos_profit = 0  # 平仓盈亏（盯市），只有平仓的合约才会计入平仓盈亏,老仓采用昨结算价计算
        self.close_profit_by_trade = 0  # 平仓盈亏（逐笔）,只有平仓的合约才会计入平仓盈亏,老仓采用开仓价计算
        self.commission = 0  # 手续费
        self.frozen_commission = 0  # 冻结手续费
        self.freezed_deposit = 0  # 委托冻结保证金


# 此结构等同于SubPortfolio,废弃
class Portfolio(object):
    """
    仓位汇总信息（废弃）
    """

    def __init__(self):
        super(Portfolio, self).__init__()
        self.inout_cash = 0  # 累计出入金, 当天银证转入/转出导致变化，证券买卖不会引发变化
        self.available_cash = 0  # 可用资金, 可用来购买证券的资金
        self.transferable_cash = 0  # 可取资金, 即可以提现的资金, 不包括今日卖出证券所得资金，暂时不可用
        self.locked_cash = 0  # 挂单锁住资金，暂时不可用
        self.type = AccountType.normal  # 账户所属类型
        self.margin = 0  # 保证金，股票、基金保证金都为100%
        self.positions = {}  # 等同于 long_positions
        self.long_positions = {}  # 多单的仓位, 一个 dict, key 是证券代码, value 是 Position对象
        self.short_positions = {}  # 空单的仓位, 一个 dict, key 是证券代码, value 是 Position对象
        self.total_value = 0  # 总资产, 包括现金, 保证金, 仓位的总价值, 可用来计算收益,模拟交易暂不支持
        self.returns = 0  # 总权益的累计收益,暂时不可用
        self.starting_cash = 0  # 初始资金, 暂时不可用
        self.total_liability = 0  #: 总负债, 等于融资负债、融券负债、利息总负债的总和,暂时不可用
        self.positions_value = 0  # 持仓价值, 股票基金才有持仓价值, 期货为0，暂时不可用
        self.locked_cash_by_purchase = 0  # 基金申购未完成所冻结的金额,暂时不可用
        self.locked_cash_by_redeem = 0  # 基金赎回未到账的金额,暂时不可用
        self.locked_amount_by_redeem = 0  # 基金赎回时，冻结的份额,暂时不可用
        self.net_value = 0  #: 净资产, 等于总资产减去总负债,暂时不可用
        self.cash_liability = 0  #: 融资负债,暂时不可用
        self.sec_liability = 0  #: 融券负债,暂时不可用
        self.interest = 0  #: 利息总负债,暂时不可用
        self.maintenance_margin_rate = 0  #: 维持担保比例,暂时不可用
        self.frozen_cash = 0  # 新增字段，包含所有冻结的资金
        self.total_cash = 0  # 新增字段，资金总量，暂时不可用
        self.settled_cash = 0  # 新增字段，期初资金

        # 以下字段为期货专用
        self.available_margin = 0  #: 可用保证金,期货可用
        self.occupied_margin = 0  # 占用保证金，期货可用
        self.pre_balance = 0  # 期初权益，期货可用
        self.current_balance = 0  # 客户权益，期货可用
        self.risk_level = 0  # 占用保证金/客户权益
        self.holding_profit = 0  # 盯市盈亏，以持仓成本计算的浮动盈亏
        self.close_pos_profit = 0  # 平仓盈亏（盯市），只有平仓的合约才会计入平仓盈亏,老仓采用昨结算价计算
        self.close_profit_by_trade = 0  # 平仓盈亏（逐笔）,只有平仓的合约才会计入平仓盈亏,老仓采用开仓价计算
        self.commission = 0  # 手续费
        self.frozen_commission = 0  # 冻结手续费
        self.freezed_deposit = 0  # 委托冻结保证金


class Tick(object):
    """
    实时行情数据，里面的金额、价格单位都是元，数量都是股/张
    """

    def __init__(self):
        self.code = ''  # 标的的代码
        self.datetime = None  # tick时间
        self.current = 0  # 最新价
        self.open = 0  # 开盘价
        self.close = 0  # 收盘价
        self.pre_close = 0  # 昨收价
        self.high = 0  # 最高价
        self.low = 0  # 最低价
        self.volume = 0  # 截至到当前时刻的成交量
        self.amount = 0  # 截至到当前时刻的成交额
        self.position = 0  # 截至到当前时刻的持仓量，目前暂不可用
        self.bid_volume = 0  # 当前时刻的委买挂单总量
        self.ask_volume = 0  # 当前时刻的委卖挂单总量
        self.w_bid_price = 0  # 加权平均委买价格
        self.w_ask_price = 0  # 加权平均委卖价格
        # 涨跌停价
        self.high_limit = 0
        self.low_limit = 0
        self.trading_phase_code = TradingPhaseCode.StartBeforeOpen  # 行情状态，在TradingPhaseCode中定义
        self.num_trades = 0  # 成交笔数
        self.total_bid_number = 0  # 买入总笔数
        self.total_ask_number = 0  # 卖出总笔数
        # 十档盘口
        # 卖盘，挂单量
        self.a1_v = 0   # 卖1盘口挂单量
        self.a1_amount_list = []  # 卖一挂单数量列表，最多50
        self.a2_v = 0   # 卖2盘口挂单量
        self.a3_v = 0   # 卖3盘口挂单量
        self.a4_v = 0   # 卖4盘口挂单量
        self.a5_v = 0   # 卖5盘口挂单量
        self.a6_v = 0   # 卖6盘口挂单量
        self.a7_v = 0   # 卖7盘口挂单量
        self.a8_v = 0   # 卖8盘口挂单量
        self.a9_v = 0   # 卖9盘口挂单量
        self.a10_v = 0   # 卖10盘口挂单量
        # 卖盘，挂单价
        self.a1_p = 0   # 卖1价
        self.a2_p = 0   # 卖2价
        self.a3_p = 0   # 卖3价
        self.a4_p = 0   # 卖4价
        self.a5_p = 0   # 卖5价
        self.a6_p = 0   # 卖6价
        self.a7_p = 0   # 卖7价
        self.a8_p = 0   # 卖8价
        self.a9_p = 0   # 卖9价
        self.a10_p = 0   # 卖10价

        # 买盘，挂单量
        self.b1_v = 0   # 买1盘口挂单量
        self.b1_amount_list = []  # 买一挂单数量列表，最多50
        self.b2_v = 0   # 买2盘口挂单量
        self.b3_v = 0   # 买3盘口挂单量
        self.b4_v = 0   # 买4盘口挂单量
        self.b5_v = 0   # 买5盘口挂单量
        self.b6_v = 0   # 买6盘口挂单量
        self.b7_v = 0   # 买7盘口挂单量
        self.b8_v = 0   # 买8盘口挂单量
        self.b9_v = 0   # 买9盘口挂单量
        self.b10_v = 0   # 买10盘口挂单量
        # 买盘，挂单价
        self.b1_p = 0   # 买1价
        self.b2_p = 0   # 买2价
        self.b3_p = 0   # 买3价
        self.b4_p = 0   # 买4价
        self.b5_p = 0   # 买5价
        self.b6_p = 0   # 买6价
        self.b7_p = 0   # 买7价
        self.b8_p = 0   # 买8价
        self.b9_p = 0   # 买9价
        self.b10_p = 0   # 买10价

        # 买盘，委托笔数
        self.b1_nums = 0   # 买1委托笔数
        self.b2_nums = 0   # 买2委托笔数
        self.b3_nums = 0   # 买3委托笔数
        self.b4_nums = 0   # 买4委托笔数
        self.b5_nums = 0   # 买5委托笔数
        self.b6_nums = 0   # 买6委托笔数
        self.b7_nums = 0   # 买7委托笔数
        self.b8_nums = 0   # 买8委托笔数
        self.b9_nums = 0   # 买9委托笔数
        self.b10_nums = 0   # 买10委托笔数
        # 卖盘，委托笔数
        self.a1_nums = 0   # 卖1委托笔数
        self.a2_nums = 0   # 卖2委托笔数
        self.a3_nums = 0   # 卖3委托笔数
        self.a4_nums = 0   # 卖4委托笔数
        self.a5_nums = 0   # 卖5委托笔数
        self.a6_nums = 0   # 卖6委托笔数
        self.a7_nums = 0   # 卖7委托笔数
        self.a8_nums = 0   # 卖8委托笔数
        self.a9_nums = 0   # 卖9委托笔数
        self.a10_nums = 0   # 卖10委托笔数

        # 期货期权专用
        self.pre_open_interest = 0  # 昨持仓
        self.open_interest = 0  # 持仓总量
        self.pre_settle_price = 0  # 昨结算价
        self.settle_price = 0  # 今结算价
        self.pre_delta = 0  # 昨虚实度
        self.curr_delta = 0  # 今虚实度

        # 股债基
        self.withdraw_buy_num = 0  # 买入撤单笔数
        self.withdraw_buy_amount = 0  # 买入撤单数量
        self.withdraw_buy_money = 0  # 买入撤单金额
        self.withdraw_sell_num = 0  # 卖出撤单笔数
        self.withdraw_sell_amount = 0  # 卖出撤单数量
        self.withdraw_sell_money = 0  # 卖出撤单金额
        self.bid_trade_max_duration = 0  # 买入委托成交最大等待时间
        self.ask_trade_max_duration = 0  # 卖出委托成交最大等待时间
        self.num_bid_orders = 0  # 买方委托价位数
        self.num_ask_orders = 0  # 卖方委托价位数
        self.IOPV = 0  # IOPV(ETF)
        self.purchase_num = 0  # 申购笔数(ETF)
        self.purchase_amount = 0  # 申购数量(ETF)
        self.redemption_num = 0  # 赎回笔数(ETF)
        self.redemption_amount = 0  # 赎回数量(ETF)
        self.client_datetime = None  # 客户端接收tick时间

        self.last_px_type = 0             #LastPx对应的成交方式，取值：1-匹配成交；2-协商成交；3-点击成交；4-询价成交；5-竞买成交
        self.auction_last_px = 0          #匹配成交最新成交价
        self.auction_volume_trade = 0     #匹配成交成交量
        self.auction_value_trade = 0      #匹配成交成交金额

        self.push_type = 0             # 推送类型 0:正常推送，1：订阅时的本地最新缓存推送 2:订阅后行情服务给的查询返回（行情最新缓存）


class KLineData(object):
    """
    日k线数据
    """

    def __init__(self):  # 数据，key包含'open', 'close', 'high', 'low', 'volume', 'money'，对应的value都是list
        self.data = {
            'date': [],
            # 'time': [],
            'open': [],
            'close': [],
            'high': [],
            'low': [],
            'volume': [],
            'money': [],
            'open_interest': [],  # 期权期货持仓量
            'settle_price': [],  # 期权期货结算价
            'pre_close': [],  # 前收盘价,预留字段,暂不提供
        }
        self.symbol = ''  # 证券代码

    def is_ready(self):
        """
        brief:数据是否准备好
        :return:是否准备就绪，bool类型
        """
        if len(self.symbol) > 6:
            return True
        return False

    def highest_price(self):
        """
        brief:获取当前K线数据中的最高价
        :return:最高价
        """
        return max(self.data['high'])

    def lowest_price(self):
        """
        brief:获取当前K线数据中的最低价
        :return:最低价
        """
        return min(self.data['low'])

    def avg_money(self):
        """
        brief:获取当前K线数据中的平均成交金额
        :return:平均成交金额
        """
        if len(self.data['money']) == 0:
            return 0
        return sum(self.data['money']) / len(self.data['money'])

    def avg_volume(self):
        """
        brief:获取当前K线数据中的平均成交量
        :return:平均成交量
        """
        if len(self.data['volume']) == 0:
            return 0
        return sum(self.data['volume']) / len(self.data['volume'])

    def avg_close_price(self):
        """
        brief:获取当前K线数据中的平均收盘价
        :return:平均收盘价
        """
        if len(self.data['close']) == 0:
            return 0
        return sum(self.data['close']) / len(self.data['close'])


#
class KLineDataPush(object):
    """
    k线数据，推送时的k线数据结构
    """

    def __init__(self):
        self.datetime = None  # 时间，datetime.datetime类型
        self.open = 0  # k线周期内的开盘价
        self.close = 0  # k线周期内的收盘价
        self.high = 0  # k线周期内的最高价
        self.low = 0  # k线周期内的最低价
        self.total_volume = 0  # k线周期内的成交总量
        self.total_money = 0  # k线周期内的总成交金额
        self.num_trades = 0  # k线周期内的总成交笔数
        self.data_type = KLineDataType.KLINEData_1M  # k线数据类型
        self.symbol = ''  # 证券代码


class EtfEstimateInfo(object):
    def __init__(self):
        self.code = ''  # 标的代码
        self.datetime = None  # ETF时间，实时传入
        self.IOPV = 0  # 最新价计算的IOPV
        # 在系统设置-ETF套利设置-利润设置，可自定义篮子市值价格取值
        self.DIOPVS1 = 0  # 指定档位计算的IOPV(溢价利润篮子取值设置)
        self.DIOPVB1 = 0  # 指定档位计算的IOPV(折价利润篮子取值设置)
        self.premium = 0  # 溢价套利预估利润(溢价利润篮子取值设置)
        self.discount = 0  # 折价套利预估利润(折价利润篮子取值设置)
        # self.IOPV_Ori = 0  # 交易所提供的IOPV （待上线）


class RecordOrder(object):
    def __init__(self):
        self.code = ''  # 标的代码
        self.datetime = None  # 行情时间
        self.side = OrderSide.BUY  # 买卖方向
        self.order_type = -1  # 委托类别
        #  -1 无效，
        # 1 市价
        # 2 限价
        # 3 本方最优
        # 4	对手方最优
        # 5 即时成交剩余撤销委托记录
        # 6 最优五档即时成交剩余撤销委托记录
        # 7 全额成交或撤销委托记录
        # 8 意向委托
        # 9	定价委托
        # 10 撤销委托
        # 11 产品状态订单
        # 12 债券现券交易点击成交逐笔委托
        # 13 债券现券交易意向申报逐笔委托
        # 14 债券现券交易竞买成交逐笔委托
        # 15 债券现券交易匹配成交大额逐笔委托
        self.price = 0.0  # 委托价格
        self.amount = 0  # 委托数量
        self.order_index = 0  # 委托编号
        self.order_no = 0  # 原始订单号（上交所在新增、删除订单时用以标识订单的唯一编号）
        self.appl_seq_num = 0  # 逐笔数据序号
        self.channel_no = 0  # 交易所原始频道代码


class RecordTransaction(object):
    def __init__(self):
        self.code = ''  # 标的代码
        self.datetime = None  # 行情时间
        self.trade_type = 0  # 成交类别
        # 0	交易业务成交记录
        # 1 交易业务撤单回报记录
        # 2	即时成交剩余撤销委托”未能成交部分或其他原因的自动撤单回报记录
        # 3 ETF基金申购/赎回成功回报记录或ETF基金申购/赎回成功证券给付明细回报记录 
        # 4	ETF基金申购/赎回撤单报记录
        # 5 最优五档即时成交剩余撤销委托”未能成交部分的自动撤单或其他原因的自动撤单回报记录
        # 6 全额成交或撤销委托”未能成交时的自动撤单或其他原因自动撤单回报记
        # 7 本方最优价格委托的撤单回报记录
        # 8	对手方最优价格委托的撤单回报记录
        # 9	ETF基金申购/赎回成功允许/必须现金替代明细回报记录
        self.side = OrderSide.BUY  # OrderSide 类型
        self.price = 0.0  # 成交价格
        self.amount = 0  # 成交数量
        self.business_balance = 0.0  # 成交金额
        self.trade_buy_no = 0  # 买方委托序号
        self.trade_sell_no = 0  # 卖方委托序号
        self.trade_index = 0    # 成交编号
        self.appl_seq_num = 0  # 逐笔数据序号
        self.channel_no = 0  # 交易所原始频道代码


class OrderStyle(metaclass=ABCMeta):
    """
    订单类型
    """

    @abstractmethod
    def get_order_style(self):
        """
        brief:获取当前订单类型
        :return:订单类型
        """
        pass

    @abstractmethod
    def get_limited_price(self):
        """
        brief:获取当前（保护）限价价格
        :return:限价价格
        """
        pass


class MarketOrderStyle(OrderStyle):
    """
    市价单,默认为五档即成剩撤
    北交所或者沪市的股票、基金在市价时需要填写保护限价，通过limit_price指定
    """

    def __init__(self, type='a', limit_price=1.0):
        """
        :param type:
            "2"最新价,暂不提供使用
            "3"涨停价,暂不提供使用
            "4"跌停价,暂不提供使用
            "5"买1,暂不提供使用
            "6"#/买2,暂不提供使用
            "7"#/买3,暂不提供使用
            "8"#/买4,暂不提供使用
            "9"#/买5,暂不提供使用
            "10"#/买6,暂不提供使用
            "11"#/买7,暂不提供使用
            "12"#/买8,暂不提供使用
            "13"#/买9,暂不提供使用
            "14"#/买10,暂不提供使用
            "15"#/卖1,暂不提供使用
            "16"#/卖2,暂不提供使用
            "17"#/卖3,暂不提供使用
            "18"#/卖4,暂不提供使用
            "19"#/卖5,暂不提供使用
            "20"#/卖6,暂不提供使用
            "21"#/卖7,暂不提供使用
            "22"#/卖8,暂不提供使用
            "23"#/卖9,暂不提供使用
            "24"#/卖10,暂不提供使用
            "25"#/"买:卖1/卖:买1",暂不提供使用
            "26"#/"买:卖2/卖:买2",暂不提供使用
            "27"#/"买:卖3/卖:买3",暂不提供使用
            "28"#/"买:卖4/卖:买4",暂不提供使用
            "29"#/"买:卖5/卖:买5",暂不提供使用
            "30"#/"买:买1/卖:买1",暂不提供使用
            "31"#/"买:买2/卖:买2",暂不提供使用
            "32"#/"买:买3/卖:买3",暂不提供使用
            "33"#/"买:买4/卖:买4",暂不提供使用
            "34"#/"买:买5/卖:买5",暂不提供使用
            "35"#/买:卖1/卖:卖1,暂不提供使用
            "36"#/买:卖2/卖:卖2,暂不提供使用
            "37"#/买:卖3/卖:卖3,暂不提供使用
            "38"#/买:卖4/卖:卖4,暂不提供使用
            "39"#/买:卖5/卖:卖5,暂不提供使用
            "40"#/买/卖:最新价,暂不提供使用
            "a"#/上交所五档即成剩撤
            "b"#/上交所五档即成剩转限价
            "a"#/深交所五档即成剩撤（深市期权五档即成剩撤）
            "c"#/深交所即成剩撤（深市期权即成剩撤）
            "d"#/沪深交易所对手最优
            "e"#/沪深交易所本方最优
            "f"#/深交所全额成交或撤（深市期权全额成交或撤）
            "l"#/中金所五档即成剩撤
            "PFP"#/盘后固定价（科创板）
            "0" #/增强限价盘
            "2" #/竞价限价盘
            "OPA" 沪深期权限价全额成交或撤销
            ######以下价格类型为上海期权独有########
            "OPB" 即时成交剩余撤销
            "OPC" 市价全额成交或撤销
            "OPD" 市价剩余转限价


        """
        self.__type = type
        self.limit_price = limit_price

    def get_order_style(self):
        return self.__type

    def get_limited_price(self):
        return self.limit_price


class LimitOrderStyle(OrderStyle):
    """
    限价单
    """

    def __init__(self, limit_price):
        self.limit_price = limit_price

    def get_order_style(self):
        #限价单
        return '1'

    def get_limited_price(self):
        return self.limit_price


class batch_order_item(object):
    """
    批次下单的单个订单对象
    批次下单允许一个批次里面存在不同订单类型，不同买卖方向的订单
    """

    def __init__(self):
        """
        :param security: 标的代码
        :param amount:交易数量, 正数表示买入, 负数表示卖出
        :param style:参见OrderStyle, 支持限价LimitOrderStyle和市价MarketOrderStyle
        :param side:该参数已废弃，买卖或者开平方向通过amount的正负判定
        :param action: 开平标志,OrderAction类型
        :param invest_type: 投资类型,HedgeFlag类型,分为投机、套保、套利
        :param close_direction: 平仓方式,CloseDirection类型,默认为优先平老仓
        :param pindex:该参数已废弃
        """
        self.security = ''
        self.amount = 0
        self.style = None
        self.side = ''
        self.action = OrderAction.UNKNOWN
        self.invest_type = HedgeFlag.UNKNOWN
        self.close_direction = CloseDirection.DEFAULT
        self.pindex = 0


class batch_cancel_order_item(object):
    """
    批量撤单的单个订单信息
    """

    def __init__(self):
        """
        :param order_id: 原始订单的order_id,batch_flag=0有效
        :param batch_no: 批次号，batch_flag=1有效
        :param batch_flag: 0表示按照order_id撤单，1表示按照批次号撤单，默认按照order_id撤单
        """
        self.order_id = ''
        self.batch_no = ''
        self.batch_flag = 0


class OrderStatus(Enum):
    """
    订单状态
    """
    # 待报：订单新创建未委托，用于盘前/隔夜单，订单在开盘时变为 open 状态开始撮合
    new = 8

    # 已报：订单未完成, 无任何成交
    open = 0

    # 部成：订单未完成, 部分成交
    filled = 1

    # 已撤/部撤：订单完成, 已撤销, 可能有成交, Order订单对象中需要看 Order.filled 字段
    canceled = 2

    # 废单：订单完成, 已拒绝，Order订单对象中具体原因参见 Order.cancel_info 字段
    rejected = 3

    # 已成：订单完成, 全部成交, Order订单对象中此时 Order.filled 等于 Order.amount
    held = 4

    # 已报待撤/部成待撤：订单取消中，只有实盘会出现，回测/模拟不会出现这个状态
    pending_cancel = 9

    # 回购到期交收
    repo_settle = 10

    # 确认(新股确认、期权行权确认、场外首期交收等场景)
    confirmed = 11

    # 撤废
    cancel_failed = 12

    # 不确定的
    unknown = -1


class Order(object):
    """
    委托订单对象
    """

    def __init__(self):
        """
        以下字段除标注'下单立即返回'字样之外，均需要调用查询订单接口（get_open_orders、get_orders等）查询才会填充
        """
        self.status = OrderStatus.new  # 状态, 随着订单执行状态改变，包含在订单执行回报中，在OrderStatus中定义
        self.add_time = None  # 订单创建时间, datetime.datetime对象，为后台创建时间，包含在订单执行回报中
        self.amount = 0  # 下单数量, 不管是买还是卖, 都是正数，下单立即返回，包含在订单执行回报中
        self.filled = 0  # 已经成交的股票数量, 正数，包含在订单执行回报中
        self.security = ''  # 股票代码，同下单请求的security参数，下单立即返回，包含在订单执行回报中
        self.order_id = ''  # 订单ID，为M-Quant系统内部生成的订单id，非委托编号，下单/撤单立即返回，包含在订单执行回报中
        self.price = 0.0  # 平均成交价格, 已经成交的股票的平均成交价格(一个订单可能分多次成交)，包含在订单执行回报中
        self.avg_cost = 0.0  # 同price
        self.side = ''  # 买卖方向，OrderSide类型，下单立即返回，包含在订单执行回报中
        self.action = OrderAction.UNKNOWN  # 开平行为，OrderAction类型，期货有效
        self.invest_type = HedgeFlag.UNKNOWN  # 投资类型，HedgeFlag类型，报单立即返回，期货有效
        self.close_direction = CloseDirection.DEFAULT  # 平仓类型，CloseDirection类型，报单立即返回，期货有效

        self.batch_no = -1  # 批次号，包含在订单执行回报中
        self.orig_order_id = ''  # 原始订单号，撤单订单有效，目前保留字段，撤单接口的返回值中该字段有效
        self.symbol = ''  # 证券代码，M-Quant格式，包含在订单执行回报中
        self.entrust_price = 0  # 委托价格，下单立即返回，包含在订单执行回报中
        self.style = None  # 订单类型（LimitOrderStyle或MarketOrderStyle），下单立即返回，包含在订单执行回报中
        self.cancel_info = ''  # 废单原因，废单有效
        self.withdraw_amount = 0  # 撤单数量，包含在订单执行回报中
        self.business_balance = 0  # 已成交金额，包含在订单执行回报中
        self.clear_balance = 0  # 成交费用，目前保留字段
        self.create_time = datetime.datetime.now()  # 内部字段，不提供使用
        self.entrust_prop = EntrustProp.trade  # 委托属性，包含在订单执行回报中，在EntrustProp中定义
        self.entrust_type = EntrustType.entrust  # 委托类型，包含在订单执行回报中，在EntrustType中定义
        self.algo_inst_id = None  # 算法实例ID，由MQuant启动的算法实例相关订单中有此字段，包含在订单执行回报中
        self.error_code = None  # 错误码
        self.inst_id = None  # Mquant实例ID，仅查询订单返回
        self.trader_name = None  # 交易员名
        self.entrust_no = ''  # 柜台委托编号
        self.covered_flag = OptionCoveredFlag.UNKNOWN  # 期权备兑标志，期权有效，在OptionCoveredFlag中定义
        self.last_amount = 0  # 本次成交数量，仅推送有效
        self.last_price = 0.0  # 本次成交价格，仅推送有效
        self.fund_account = ''  # 资金账号
        self.security_exchange = SecurityExchangeType.UNKNOWN  # 市场，主要用于港股通，在SecurityExchangeType中定义
        # 债券协商交易字段
        self.settlement_type = SettleType.UNKNOWN     # 深圳协商交易结算方式，在SettleType中定义
        self.counter_trader = ''    # 沪深协商交易对手方交易员
        self.counter_party = ''     # 深圳协商交易对手主体
        self.agreement_no = ''      # 沪深协商交易约定号
        # 期权组合字段
        self.option_comb_id = ''  # 期权组合编码
        # 超级ETF
        self.etf_portfolio_no = ''  # 超级ETF组合编号
        # 上海黄金交易所
        self.list_SGEETF_detail = None  # ETF申购的成分明细，list<HtSGEEtfConInfo>


class Trade(object):
    """
    成交订单对象
    """

    def __init__(self):
        self.time = None  # 成交时间, datetime.datetime对象，查询及推送返回
        self.amount = 0  # 成交数量，查询及推送返回
        self.price = 0.0  # 成交价格，查询及推送返回
        self.trade_id = ''  # 柜台成交编号，查询及推送返回
        self.order_id = ''  # 订单id，查询及推送返回

        self.security = ''  # 股票代码，下单立即返回，查询及推送返回
        self.symbol = ''  # 同security
        self.real_type = 0  # 成交类型，EntrustType中定义，查询及推送返回
        self.business_balance = 0  # 成交金额，查询及推送返回
        self.cost_balance = 0  # 成交费用，目前保留字段
        self.orig_order_id = -1  # 原始订单号，撤单订单有效，目前保留字段
        self.side = ''  # 委托方向,OrderSide类型，查询及推送返回
        self.algo_inst_id = None  # 算法实例ID，由MQuant启动的算法实例相关订单中有此字段，包含在订单执行回报中
        self.inst_id = None  # Mquant实例ID，仅查询成交返回
        self.trader_name = None  # 交易员，查询及推送返回
        self.action = OrderAction.UNKNOWN  # 开平行为，OrderAction类型，期货有效
        self.invest_type = HedgeFlag.UNKNOWN  # 投资类型，HedgeFlag类型，报单立即返回，期货有效
        self.close_direction = CloseDirection.DEFAULT  # 平仓类型，CloseDirection类型，报单立即返回，期货有效
        self.entrust_no = ''  # 柜台委托编号
        self.style = None  # 订单类型
        self.fund_account = ''  # 资金账号
        self.security_exchange = SecurityExchangeType.UNKNOWN  # 市场，主要用于港股通，在SecurityExchangeType中定义
        self.entrust_prop = EntrustProp.trade  # 委托属性，包含在订单执行回报中，在EntrustProp中定义
        self.entrust_type = EntrustType.entrust # 委托类型，包含在订单执行回报中，在EntrustType中定义
        # 债券协商交易字段
        self.counter_trader = ''  # 沪深协商交易对手方交易员
        self.counter_party = ''  # 深圳协商交易对手主体
        self.agreement_no = ''  # 沪深协商交易约定号
        # 期权组合字段
        self.option_comb_id = ''  # 期权组合编码
        # 超级ETF
        self.etf_portfolio_no = ''  # 超级ETF组合编号
        # 上海黄金交易所
        self.list_SGEETF_detail = None  # ETF赎回的成分明细，list<HtSGEEtfConInfo>


class SecmatchOrderStatus(Enum):
    """
    融券通委托订单状态
    """
    # 未成交
    unfilled = 0
    # 部分成交
    partially_filled = 1
    # 全部成交
    filled = 2
    # 已撤销
    canceled = 3
    # 已报证金
    new = 4
    # 保证金废单
    reject = 5
    # 不确定的
    unknown = -1


class SecmatchTradeStatus(Enum):
    """
    融券通成交订单状态
    """
    # 成交
    filled = 1
    # 预撮合
    prematch = 2
    # 意向
    intention = 3
    # 撤单
    canceled = 4
    # 部分成交
    partially_filled = 5
    # 未成交
    unfilled = 6
    # 不确定的
    unknown = -1

class SecmatchOrder(object):
    """
    融券通委托订单对象
    """

    def __init__(self):
        self.fund_account = ''  # 资金账号
        self.symbol = ''    # 证券代码
        self.exchange = SecurityExchangeType.UNKNOWN    # 市场，在SecurityExchangeType中定义
        self.trade_date = None     # 交易日期,datetime.date类型，表示委托所属的交易日
        self.create_time = None    # 委托时间,datetime.datetime类型
        self.order_id = ''   # 委托编号
        self.entrust_type = ''   # 委托类型，1 - 出借，2 - 融入
        self.order_qty = 0  # 委托数量
        self.apply_rate = 0.0   # 委托利率
        self.secmatch_ord_status = SecmatchOrderStatus.unknown    # 委托状态，在SecmatchOrderStatus中定义
        self.deal_qty = 0   # 成交数量
        self.intention_qty = 0  # 预成交量
        self.agreement_no = ''   # 约定号
        self.term = 0   # 合约期限（天数）
        self.exp_date = None   # 到期日,datetime.date类型
        self.entrust_prop = ''  # 委托属性


class SecmatchTrade(object):
    """
    融券通成交订单对象
    """

    def __init__(self):
        self.fund_account = ''  # 资金账号
        self.symbol = ''    # 证券代码
        self.deal_time = None    # 成交时间,datetime.datetime类型
        self.entrust_type = ''   # 委托类型，1 - 出借，2 - 融入
        self.order_id = ''  # 委托编号
        self.exec_id = ''  # 成交编号
        self.order_qty = 0  # 委托数量
        self.apply_rate = 0.0  # 委托利率
        self.deal_rate = 0.0    # 成交利率
        self.deal_qty = 0  # 成交数量
        self.intention_qty = 0  # 预成交数量
        self.term = 0  # 合约期限（天数）
        self.secmatch_ord_status = SecmatchTradeStatus.unknown  # 成交状态，在SecmatchTradeStatus中定义


class SecmatchCompact(object):
    """
    融入合约对象
    """

    def __init__(self):
        self.fund_account = ''  # 资金账号
        self.symbol = ''  # 证券代码
        self.start_date = None  # 起始日期,datetime.date类型
        self.valid_date = None  # 有效日期,datetime.date类型
        self.compact_id = ''  # 合约编号
        self.compact_state = ''  # 合约状态，0-未归还、1-部分归还、2-提前了结、3-到期了结、4-逾期了结
        self.compact_qty = 0  # 合约数量
        self.compact_balance = 0.0  # 合约金额
        self.fsmp_used_rate = 0.0  # 使用费率
        self.fine_rate = 0.0  # 违约金率，罚息利率
        self.postphone_times = 0  # 展期次数
        self.fsmp_occuped_rate = 0.0  # 成交利率
        self.fsmp_comgroup_id = ''  # 资券组合编号
        self.trans_apply_id = ''  # 资券平台申请号
        self.return_date = None  # 归还日,datetime.date类型
        self.used_amount = 0  # 已使用数量
        self.begin_compact_amount = 0  # 期初合约数量
        self.return_amount = 0  # 当日归还数量
        self.compact_interest = 0.0  # 合约利息金额
        self.compact_fine_interest = 0.0  # 合约罚息金额
        self.occuped_integra = 0.0  # 占用利息积数
        self.fine_integra = 0.0  # 罚息积数
        self.repaid_integra = 0.0  # 已还利息
        self.repaid_fine_integra = 0.0  # 归还罚息
        self.post_pone_amount = 0  # 已展期数量
        self.pre_interest = 0.0  # 预计利息
        self.days_left = 0  # 合约到期剩余时间
        self.orig_end_date = None  # 原合约到期日,datetime.date类型
        self.orig_compact_no = ''  # 原合约编号
        self.fsmp_compact_type = 0  # 资券合约类型，0-当日成交合约、1-权益补偿合约、2-调账合约、3-内部合约、4-内部权益补偿合约
        self.post_pone_status = 0  # 展期状态，0-未申请 1-待审核 2-审核通过 3-审核不通过 4-已撤销
        self.defer_end_date = None  # 展期后到期日,datetime.date类型


class BondNegotiateExecID(object):
    """
    债券协商交易执行编号对象
    """

    def __init__(self):
        self.symbol = ''  # 证券代码
        self.side = OrderSide.UNKNOWN  # 买卖方向，OrderSide类型
        self.price = 0.0  # 委托价格
        self.amount = 0  # 委托数量
        self.agreement_no = ''  # 约定号
        self.counter_trader = ''  # 发起方交易员
        self.counter_party = ''  # 发起方主体
        self.counter_account_name = ''  # 发起方账号名称
        self.exec_id = ''  # 执行编号


class CurrencyType(Enum):
    CNY = '0'   # 人民币
    USD = '1'   # 美元
    HKD = '2'   # 港元


class BankTransferStatement(object):
    """
    银行转账流水对象
    """

    def __init__(self):
        self.entrust_time = None    # 委托时间,datetime.datetime类型
        self.bank_name = ''         # 银行名称
        self.operate = ''           # 操作，（'0':未知，'1':银行转存，2':银行转取）
        self.occur_balance = 0.0    # 发生金额
        self.money_type = ''        # 货币单位，参见CurrencyType定义
        self.remark = ''            # 备注
        self.entrust_status = ''    # 委托状态（'0':未报，'1':已报'，2':成功，'3':作废，'4':待撤，'5':撤消，'7':待冲正，'8':已冲正，'A':待报，'P':正报，'Q':已确认，其他未知）
        self.serial_no = 0          # 序列号


class EtfType(object):
    """
    ETF基金类型
    """
    singleMarket = "1"  # 单市场ETF
    crossBorder = "2"  # 跨境ETF
    crossMarket = "3"  # 跨市ETF
    currency = "4"  # 货币ETF
    bond = "5"  # 实物债券ETF
    commodity = "6"  # 商品ETF
    cashBond = "7"  # 现金债券ETF
    unknown = "-1"  # 未知


class EtfStatus(object):
    """
    ETF基金状态
    """
    forbidden = "0"  # 全部禁止
    allow = "1"  # 全部允许
    onlyAllowApplyBuy = "2"  # 仅允许申购
    onlyAllowRedemption = "3"  # 仅允许赎回
    unknown = "-1"  # 未知


class HtEtfConstituentInfo(object):
    """
    ETF成分券信息
    """

    def __init__(self):
        self.symbol = ''  # 成分券代码
        self.sample_size = 0  # 样本数量
        self.cash_replace_flag = 0  # 现金替代标志
        # 0-禁止替代
        # 1-允许替代
        # 2-必须替代
        # 3-非沪市退补现金替代
        # 4-非沪市必须现金替代
        # 5-非沪深退补现金替代
        # 6-非沪深必须现金替代
        self.deposit_ratio = 0  # 保证金率（溢价比率）
        self.replace_balance = 0  # 替代金额
        self.pre_close_px = 0  # 昨收价格（静态信息补充数据）
        self.high_limit_px = 0  # 涨停（静态信息补充数据）
        self.low_limit_px = 0  # 跌停价（静态信息补充数据）
        self.suspend_flag = False  # 停牌标志（静态信息补充数据）

        self.modify_time = ''  # 本地更新时间(datetime.datetime类型)，可用于校验成分数据是否正常更新，实际需要结合HtEtfInfo的T日日期判断数据有效性


class HtEtfInfo(object):
    """
    ETF信息
    """

    def __init__(self):
        super(HtEtfInfo, self).__init__()
        self.etf_fund_symbol = ''  # etf基金代码
        self.etf_symbol = ''  # etf申赎代码
        self.report_unit = 0  # 一个申赎单位的基金份额
        self.cash_balance = 0  # 预估现金差额
        self.max_cash_ratio = 0  # 最大现金替代比例
        self.pre_cash_componet = 0  # T-1日申购基准单位现金余额
        self.nav_percu = 0  # T-1日申购基准单位净值
        self.nav_pre = 0  # T-1日基金单位净值
        self.allot_max = 0  # 申购份额上限
        self.redeem_max = 0  # 赎回份额上限
        self.etf_type = EtfType.unknown  # ETF类型
        self.etf_status = EtfStatus.unknown  # ETF基金状态

        self.trade_date = ''  # T日日期(datetime.date类型)，可用于校验清单数据是否为当日最新数据


class HtSGEEtfConstituentInfo(object):
    """
    SGEETF成分券信息
    """

    def __init__(self):
        self.symbol = ''  # 成分券代码
        self.cash_balance = 0  # 现金差额（单位：元/千克）
        self.pre_cash_balance = 0  # T-1日现金差额（单位：元/千克）


class HtSGEEtfInfo(object):
    """
    SGEETF信息
    """

    def __init__(self):
        self.trade_date = ''  # 交易日(datetime.date类型)
        self.etf_fund_symbol = ''  # etf基金代码
        self.report_unit = 0  # 最小申购赎回单位（单位：份）
        self.weight_pre_unit = 0.0  # 每份ETF基金对应的合约数量（克）
        self.contract_qty = 0  # 合约数量（克）
        self.allot_max = 0  # 申购份额上限（单位：份）
        self.redeem_max = 0  # 赎回份额上限（单位：份）
        self.etf_status = EtfStatus.unknown  # ETF基金状态


class HtSGEEtfConInfo(object):
    """
    SGEETF申购时的成分券信息
    """

    def __init__(self):
        self.symbol = ''  # 成分券代码
        self.weight = 0.0  # 重量（单位：千克）


class Context(object, metaclass=ABCMeta):
    """
    上下文信息
    """
    def __init__(self):
        super(Context, self).__init__()
        self.subportfolios = [] # 该参数已废弃
        self.portfolio = None  # 该参数已废弃
        self.current_dt = None  # 参数已废弃
        self.previous_date = None  # 该参数已废弃
        self.universe = []  # 该参数已废弃
        self.run_params = {}  # 策略此次运行的参数, 字典类型，在回调函数strategy_params中可自定义
        self.cur_account_type = None  # 当前账户类型，AccountType类型

    def __getattribute__(self, item):
        """
        访问对象属性时，必定会调用该函数，可以在调用到该函数时动态获取对应的数据
        避免始终保持context中的数据为最新，导致持续的不必要的开销
        """
        return super(Context, self).__getattribute__(item)

    def set_current_account_type(self, account_type=AccountType.normal):
        """
        设置当前账户类型
        :param account_type: AccountType类型
        """
        self.cur_account_type = account_type

    def get_current_account_type(self):
        """
        获取当前账户类型
        :return:AccountType类型
        """
        return self.cur_account_type

    @abstractmethod
    def get_fund_account_by_type(self, account_type):
        """
        根据账号类型获取资金账号
        :param account_type: 账号类型，AccountType类型
        :return:资金账号，失败返回空字符串
        """
        pass

    @abstractmethod
    def get_batch_index(self):
        """
        批量固化的策略获取在固化批次中的序号
        :return: 序号，int类型
        """
        pass


class GlobalObj(object):
    """
    全局变量g
    """

    def __init__(self):
        """
        初始化时可进行一些现场恢复的工作
        """
        super(GlobalObj, self).__init__()


class MarginContractType(Enum):
    """
    信用合约类型
    """
    unknown = 0  # 未知类型
    finacing = 1  # 融资合约
    security = 2  # 融券合约


class PositionType(Enum):
    """
    头寸类型
    """
    undefine = -1  # 未知
    normal = 1  # 普通头寸
    vip = 2  # 专项头寸


class MarginContract(object):
    """
    信用交易合约,包含融资负债和融券负债
    """

    def __init__(self, contract_type=MarginContractType.unknown.value):
        self.symbol = ''  # 标的
        self.contract_type = contract_type  # 负债类型，在MarginContractType中定义
        self.unpaid_amount = 0  # 未还金额
        self.unpaid_qty = 0  # 未还数量
        self.unpaid_interest = 0  # 未还利息
        self.unpaid_fee = 0  # 未还费用
        self.paid_amount = 0  # 已还金额
        self.paid_qty = 0  # 已还数量
        self.paid_interest = 0  # 已还利息
        self.paid_fee = 0  # 已还费用
        self.total_liability = 0  # 总负债
        self.open_date = None  # 开仓日期，datetime.date类型
        self.deadline = None  # 归还截止日期,datetime.date类型
        self.contract_no = ''  # 合同编号
        self.position_type = 0  # 头寸类型（融券合约专用）,0-普通，1-专项
        self.interest = 0  # 利息,该参数已废弃，值等于unpaid_interest
        self.cost = 0  # 费用，该参数已废弃，值等于unpaid_fee


class MarginAssert(object):
    """
    信用资产信息, 后台系统定时从柜台同步，不保证实时性
    """

    def __init__(self):
        self.cash_asset = 0  # 现金资产
        self.security_market_value = 0  # 证券市值
        self.assure_asset = 0  # 担保资产
        self.total_liability = 0  # 总负债
        self.maintain_value = 0  # 个人维持担保比例
        self.available_margin = 0  # 可用保证金
        self.occupy_margin = 0  # 占用保证金
        self.collateral_available_money = 0  # 买担保品可用资金
        self.finance_available_money = 0  # 买融资标的可用资金
        self.security_available_fund = 0  # 买券还券可用资金
        self.cash_available_money = 0  # 现金还款可用资金
        self.finance_quota_capacity = 0  # 融资额度上限
        self.finance_available_quota = 0  # 融资可用额度
        self.finance_occupy_quota = 0  # 融资占用额度
        self.finance_occupy_margin = 0  # 融资占用保证金
        self.finance_compact_quota = 0  # 融资合约金额
        self.finance_compact_commission = 0  # 融资合约费用
        self.finance_compact_interest = 0  # 融资合约利息
        self.finance_market_value = 0  # 融资市值
        self.finance_compact_revenue = 0  # 融资合约收益
        self.security_loan_quota_capacity = 0  # 融券额度上限
        self.security_loan_available_quota = 0  # 融券可用额度
        self.security_loan_occupy_quota = 0  # 融券占用额度
        self.security_loan_occupy_margin = 0  # 融券占用保证金
        self.security_loan_compact_quota = 0  # 融券合约金额
        self.security_loan_compact_commission = 0  # 融券合约费用
        self.security_loan_compact_interest = 0  # 融券合约利息
        self.security_loan_market_value = 0  # 融券市值
        self.security_loan_compact_revenue = 0  # 融券合约收益
        self.transfer_asset = 0  # 可转出资产
        self.compact_total_interest = 0  # 合约总利息
        self.net_asset = 0  # 净资产
        self.withdraw_quota = 0  # 可取金额(暂不提供)
        self.security_loan_sell_balance = 0  # 融资卖出所得金


class MarginSymbol(object):
    """
    两融标的数据
    """

    def __init__(self):
        self.fund_account = 0  # 资金账号
        self.symbol = ''  # 证券代码
        self.symbol_name = ''  # 证券简称
        self.finance_ratio = 0.0  # 融资保证金比例
        self.loan_ratio = 0.0  # 融券保证金比例
        self.finance_state = ''  # 融资状态: 0-正常、1-暂停、2-作废
        self.loan_state = ''  # 融券状态: 0-正常、1-暂停、2-作废


class AlgoType(Enum):
    """
    算法类型
    """
    AIVWAP = 6
    """
    基于深度学习的VWAP执行算法,对应算法为AIVWAP
    """
    AITWAP = 14
    """
    基于深度学习的TWAP执行算法,对应算法为AITWAP
    """
    SMARTTWAP = 15
    """
    从AES迁移的TWAP算法，对应算法为SMARTTWAPTW
    """
    SMARTVWAP = 16
    """
    从AES迁移的VWAP算法，对应算法为SMARTVWAPTW
    """
    SMARTSNIPER = 17
    """
    对应算法为SMARTSNIPER
    """
    AIPAIR = 18
    """
    对应算法为AI调仓
    """

    AITWAPBASIC = 20
    """
    基础版AITWAP，该算法在“算法交易”菜单中“算法类型”展示为AITWAP,已废弃
    """
    AIVWAPBASIC = 21
    """
    基础版AIVWAP，该算法在“算法交易”菜单中“算法类型”展示为AIVWAP,已废弃
    """
    AIPAIRBASIC = 22
    """
    基础版AIPAIR，该算法在“算法交易”菜单中“算法类型”展示为AI调仓,已废弃
    """
    AITWAPPLUS = 23
    """
    升级版AITWAP，该算法在“算法交易”菜单中“算法类型”展示为AITWAP+,已废弃
    """
    AIVWAPPLUS = 24
    """
    升级版AIVWAP，该算法在“算法交易”菜单中“算法类型”展示为AIVWAP+,已废弃
    """
    AIPAIRPLUS = 25
    """
    升级版AIPAIR，该算法在“算法交易”菜单中“算法类型”展示为AI调仓+,已废弃
    """
    SUPERTWAP = 26
    """
    增强版TWAP，该算法在“算法交易”菜单中“算法类型”展示为SUPERTWAP
    """
    KF_TWAPPLUS = 27
    """
    KF_TWAPPLUS，该算法在“算法交易”菜单中“算法类型”展示为KF_TWAPPLUS
    """
    KF_VWAPPLUS = 28
    """
    KF_VWAPPLUS，该算法在“算法交易”菜单中“算法类型”展示为KF_VWAPPLUS
    """
    smarT_I = 29
    """
    T0策略，smarT_I，该策略在“smarT策略交易”菜单中“策略类型”展示为smarT_卡方
    """
    smarT_Y = 30
    """
    T0策略，smarT_Y，该策略在“smarT策略交易”菜单中“策略类型”展示为smarT_跃然
    """
    smarT_Q = 31    # 已下线
    """
    T0策略，smarT_Q，该策略在“smarT策略交易”菜单中“策略类型”展示为smarT_启能达
    """
    YR_TWAP = 32    # 已下线
    """
    YR_TWAP，该算法在“算法交易”菜单中“算法类型”展示为跃然_TWAP
    """
    YR_VWAP = 33    # 已下线
    """
    YR_VWAP，该算法在“算法交易”菜单中“算法类型”展示为跃然_VWAP
    """
    PursueHighLimitGY = 34
    """
    PursueHighLimitGY，该算法在“算法交易”菜单中“算法类型”展示为抢涨停_GY
    """
    ZC_SMART = 35    # 已下线
    """
    ZC_SMART，该算法在“算法交易”菜单中“算法类型”展示为自诚_算法
    """
    SUPERVWAP = 36
    """
    增强版VWAP，该算法在“算法交易”菜单中“算法类型”展示为SUPERVWAP
    """
    FT_TWAPPLUS = 37
    """
    FT_TWAPPLUS，该算法在“算法交易”菜单中“算法类型”展示为非凸_TWAPPLUS
    """
    FT_VWAPPLUS = 38
    """
    FT_VWAPPLUS，该算法在“算法交易”菜单中“算法类型”展示为非凸_VWAPPLUS
    """
    smarT_AOA = 39
    """
    T0策略，smarT_AOA，该策略在“smarT策略交易”菜单中“策略类型”展示为smarT_AOA
    """
    PursueHighLimitPLUS = 40
    """
    PursueHighLimitPLUS，该算法在“算法交易”菜单中“算法类型”展示为极速抢涨停算法+
    """
    DoubleConditionOrderPLUS = 41
    """
    DoubleConditionOrderPLUS，该算法在“算法交易”菜单中“算法类型”展示为双条件抢单算法+
    """
    smarT_F = 42
    """
    T0策略，smarT_F，该策略在“smarT策略交易”菜单中“策略类型”展示为smarT_非凸
    """
    smarT_J = 43
    """
    T0策略，smarT_J，该策略在“smarT策略交易”菜单中“策略类型”展示为smarT_靖戈
    """
    AIPOV = 44
    """
    AIPOV，该策略在“算法交易”菜单中“算法类型”展示为AIPOV
    """
    smarT_T = 45
    """
    T0策略，smarT_T，该策略在“smarT策略交易”菜单中“策略类型”展示为smarT_TL
    """
    UNKNOWN = 64


class AlgoGlobalType(Enum):
    """
    算法交易类型
    """
    algo = 0
    """
    普通算法
    """
    T0 = 6
    """
    T0类型算法（AlgoType中smarT系列）
    """

class AlgoEntrustProp(object):
    """
    算法委托属性
    """
    normal = '0'  # 普通A股交易
    credit = '9'  # 信用交易
    credit_financing = '6'  # 融资买入


class AlgoInstanceStatus(object):
    """
    算法实例状态
    """
    RUNNING = '0'  # 运行中
    PAUSE = '1'  # 暂停
    STOP = '2'  # 停止
    INIT = '3'  # 初始状态
    UNKNOWN = '4'  # 未知状态
    FINISH = '5'  # 已完成


class AlgoSymbolInfo(object):
    """
    标的的进度信息
    """

    def __init__(self):
        self.cum_qty = 0  # 累计成交总量
        self.order_qty = 0  # 委托总量
        self.avg_px = 0  # 成交均价
        self.cum_amount = 0  # 成交金额
        self.target_qty = 0  # 目标总量
        self.target_amount = 0.0  # 目标金额
        self.progress = 0  # 标的成交进度
        self.symbol = '' # 证券代码
        self.limit_price = 0.0  # 算法限价
        self.entrust_type = EntrustType.UNKNOWN # 委托类型，在EntrustType中定义
        self.order_side = OrderSide.UNKNOWN # 委托方向，在OrderSide中定义


class AlgoInstanceInfo(object):
    """
    算法实例信息
    """

    def __init__(self):
        self.inst_id = ''  # 实例ID
        self.status = AlgoInstanceStatus.UNKNOWN  # 实例状态，在AlgoInstanceStatus中定义
        self.symbol_info = []  # 标的的进度信息列表，元素类型为AlgoSymbolInfo对象
        self.progress = 0  # 实例成交进度
        self.is_final_progress = False  # 是否终态时查到进度，在True的状态下symbol_info中的进度信息为最终状态
        self.fund_account = ''  # 资金账户
        self.remark = ''  # 备注信息
        self.algo_type = AlgoType.UNKNOWN  # 算法类型，在AlgoType中定义
        self.cl_inst_id = ''  # 自定义实例ID


class T0AlgoSymbolInfo(object):
    """
    T0标的的绩效/进度信息
    """

    def __init__(self):
        self.inst_id = ''           # 实例ID
        self.symbol = ''            # 证券代码
        self.algo_type = AlgoType.UNKNOWN         # 策略类型，在AlgoType中定义
        self.target_qty = 0         # 目标数量
        self.target_amount = 0      # 目标总金额
        self.buy_qty = 0            # 买入总数量
        self.buy_avg = 0            # 买入均价
        self.buy_amount = 0         # 买入总金额
        self.sell_qty = 0           # 卖出总数量
        self.sell_avg = 0           # 卖出均价
        self.sell_amount = 0        # 卖出总金额
        self.achieve_profit = 0     # 预估实现盈亏
        self.open_qty = 0           # 敞口数量
        self.status = AlgoInstanceStatus.UNKNOWN    # 实例状态，在AlgoInstanceStatus中定义
        self.remark = ''  # 备注信息


class T0AlgoInstanceInfo(object):
    """
    T0算法实例信息
    """

    def __init__(self):
        self.inst_id = ''  # 实例ID
        self.fund_account = ''  # 资金账户
        self.symbol_info = []  # 标的的进度信息列表，元素类型为T0AlgoSymbolInfo对象
        self.is_final_progress = False  # 是否终态时查到进度，在True的状态下symbol_info中的进度信息为最终状态
        self.cl_inst_id = ''  # 自定义实例ID


class T0AlgoPerformance(object):
    """
    T0算法绩效信息
    """

    def __init__(self):
        self.fund_account = ''  # 资金账户
        self.algo_type = AlgoType.UNKNOWN     # 策略类型，在AlgoType中定义
        self.target_amount = 0  # 目标总金额
        self.buy_amount = 0  # 买入总金额
        self.sell_amount = 0  # 卖出总金额
        self.achieve_profit = 0  # 预估实现盈亏


class STStatus(object):
    """
    股票的ST标识
    """
    notst = 0  # 非ST标的
    special = 1  # ST
    serious = 2  # *ST


class TradingPhaseCode(object):
    StartBeforeOpen = "0"  # 开盘前，启动
    OpenAggregateAuction = "1"  # 开盘集合竞价
    AfterAggregateAuction = "2"  # 开盘集合竞价阶段结束到连续竞价阶段开始之前
    ContinuousAuction = "3"  # 连续竞价
    CloseAtNoon = "4"  # 中午休市
    CloseAggregateAuction = "5"  # 收盘集合竞价
    Closed = "6"  # 已闭市
    PostTrading = "7"  # 盘后交易
    TemporarilySuspended = "8"  # 临时停牌
    VolatilityInterrupted = "9"  # 波动性中断


class SecurityDetial(object):
    """
    证券详情
    """

    def __init__(self):
        self.symbol = ''        # 证券代码
        self.display_name = ''  # 中文名
        self.spell_name = ''  # 拼音简称
        self.start_date = None  # 上市日期, [datetime.date] 类型，暂不提供
        self.end_date = None  # 退市日期， [datetime.date] 类型, 如果没有退市则为2200-01-01，暂不提供
        self.security_type = None  # 证券类型，在SecurityType中定义
        self.security_sub_type = None  # 证券子类型，在SecuritySubType中定义
        self.STFlag = STStatus.notst  # ST标志，在STStatus中定义
        self.TradingPhaseCode = 0  # 股票状态，该参数已废弃，建议使用Tick中的trading_phase_code
        self.RoundLot = 100  # 单手股数，目前仅港股有效
        self.LocalTotalShare = 0  # 本市总股本
        self.LocalListedShare = 0  # 本市流通股本
        self.TotalCapital = 0   # 总股本
        self.NegotiateCapital = 0  # 流通股本
        self.TickSize = 0  # 价格精度，暂不可用
        self.HighLimitPrice = 0  # 涨停价
        self.LowLimitPrice = 0  # 跌停价
        self.PreClosePrice = 0  # 昨收盘价
        self.MarginTradingFlag = 0  # 融资融券标识，1表示支持融资融券，0表示不支持融资融券，暂不提供
        self.ContractMultiplier = 0  # 合约乘数，目前仅期权有效。金交所现货合约交易单位（克/手）
        self.IsSHHK = False     # 是否沪港通标的,港股有效
        self.IsSZHK = False     # 是否深港通标的,港股有效

        # 以下字段期权专用
        self.StrikePrice = 0  # 行权价格，期权有效
        self.StrikeDate = None  # 行权日期， 期权有效，yyyyMMdd格式
        self.PutOrCall = ''  # 认购('C')/认沽('P')，期权有效
        self.UnderlyingSymbol = ''  # 期权的基础证券代码，期权有效
        self.ExerciseType = ''  # 行权方式（'A'-美式，'E'-欧式 ，'B'-百慕大式），期权有效

        # 以下字段可转债专用
        self.ConvertSymbol = ''  # 转股代码
        self.ConvertPrice = 0.0  # 转股价格
        self.ConvertStartDate = ''  # 转股开始日期,yyyyMMdd
        self.ConvertEndDate = ''  # 转股结束日期,yyyyMMdd

        self.NetPrice = 0.0  # 债券估值(上一交易日)


class LOG_LEVEL(Enum):
    """
    日志级别
    """
    DEBUG = 0
    INFO = 1
    WARNING = 2
    ERROR = 3
    MAX_LEVEL = 4


class DateType(object):
    """
    日期类型
    """
    NORMAL_DATE = 0  # 自然日
    TRADE_DATE = 1  # 交易日


class PositionProp(object):
    """
    仓位属性
    """
    SHORT_FOR_SHORT = '0'  # 备兑持仓
    LONG = '1'  # 多仓
    SHORT = '2'  # 空仓
    UNKNOWN = ''  # 未知


class OrderAction(object):
    """
    订单行为，期货期权用
    """
    OPEN = '1'  # 开
    CLOSE = '2'  # 平
    EXERCISE = '3'  # 行权
    AUTO_EXERCISE = '4'  # 自动行权
    UNKNOWN = ''


class HedgeFlag(object):
    """
    期货投保标记
    """
    SPECULATION = '1'  # 投机
    HEDGING = '2'  # 套保
    ARBITRAGE = '3'  # 套利
    UNKNOWN = ''  # 未知


class CloseDirection(object):
    """
    平仓类型
    """
    DEFAULT = '0'  # 默认
    CLOSE_TODAY = '1'  # 平今仓
    CLOSE_OLD = '2'  # 平老仓
    FORCE_CLOSE = '3'  # 强平
    FORCE_OFF = '4'  # 强减
    LOCAL_FORCE_CLOSE = '5'  # 本地强平


class FutureContractInfo(object):
    """
    期货合约信息
    """

    def __init__(self):
        self.symbol = ''    # 证券代码
        self.price_step = 0  # 最小价格变动单位
        self.contract_multiplier = 0  # 合约乘数
        self.start_deliv_date = 0  # 开始交割日
        self.end_deliv_date = 0  # 结束交割日
        self.long_margin_ratio = 0  # 多头保证金率（按金额）
        self.short_margin_ratio = 0  # 空头保证金率（按金额）
        self.long_margin_ratio_amount = 0  # 多头保证金率（按手数）
        self.short_margin_ratio_amount = 0  # 空头保证金率（按手数）
        self.margin_ratio_flag = 1  # 保证金率模式，1-按金额，2-按手数
        self.market_max_buy_qty = 0  # 市价最大买入数量
        self.market_max_sell_qty = 0  # 市价最大卖出数量
        self.market_min_buy_qty = 0  # 市价最小买入数量
        self.market_min_sell_qty = 0  # 市价最小卖出数量
        self.max_buy_qty = 0  # 限价最大买入数量
        self.max_sell_qty = 0  # 限价最大卖出数量
        self.min_buy_qty = 0  # 限价最小买入数量
        self.min_sell_qty = 0  # 限价最小卖出数量


class OptionCoveredFlag(object):
    """
    期权备兑信息
    """
    UNCOVERED = '1'  # 非备兑
    COVERED = '2'  # 备兑
    UNKNOWN = ''  # 未知


class OptionHoldType(object):
    """
    期权持仓类型
    """
    DEFAULT = '0'
    RIGHT = '1'  # 权利仓
    COMPULSORY = '2'  # 义务仓
    COVERED = '3'  # 备兑仓

    LONG = '4'  # 空仓，用于现货延期交收合约
    SHORT = '6'  # 多仓，用于现货延期交收合约



class IndexComponent(object):
    """
    指数成分券信息
    """
    def __init__(self):
        self.symbol = ''    # 证券代码
        self.include_date = 0  # 进入日期，int类型，yyyyMMdd
        self.exclude_date = 0  # 退出日期，int类型，yyyyMMdd
        self.status = 0  # 最新状态，1-使用，0-停用


class FundUpdateInfo(object):
    """
    资金推送信息
    """

    def __init__(self):
        self.fund_account = ''  # 资金账号
        self.available_cash = 0  # 可用资金
        self.frozen_cash = 0  # 冻结资金
        self.total_value = 0  # 总资产
        self.settled_cash = 0  # 期初资金
        self.hold_cash = 0  # 当前资金余额
        self.market_value = 0  # 证券市值
        self.transferable_cash = 0  # 可取资金
        self.hk_available_cash = 0  # 港股可用资金
        # 以下字段为期货专用
        self.available_margin = 0  # 保证金余额
        self.occupied_margin = 0  # 占用保证金
        self.pre_balance = 0  # 期初权益
        self.current_balance = 0  # 客户权益
        self.risk_level = 0  # 风险度
        self.close_pos_profit = 0  # 平仓盈亏（盯市）
        self.close_profit_by_trade = 0  # 平仓盈亏（逐笔）
        self.commission = 0  # 手续费
        self.frozen_commission = 0  # 冻结手续费
        self.freezed_deposit = 0  # 委托冻结保证金
        # 两融字段
        self.total_liability_credit = 0  # 总负债
        self.available_margin_credit = 0  # 可用保证金
        self.collateral_available_money = 0  # 买担保品可用资金


class AlgoOrderInfo(object):
    """
    算法创建标的信息
    """

    def __init__(self):
        # 公共部分
        self.symbol = ''    # 证券代码
        self.amount = 0     # 目标数量
        self.security_exchange = SecurityExchangeType.UNKNOWN  # 证券市场，港股通必须填写，其他类型无需填写
        # 普通算法，smarT系列不需要
        self.limit_price = 0    # 算法限价
        self.side = OrderSide.UNKNOWN  # 仅AI调仓、自诚、跃然、非凸、卡方支持每只标的不同的交易方向，在OrderSide中定义
        self.entrust_type = EntrustType.entrust  # 仅AI调仓、自诚、跃然、非凸、卡方支持每只标的不同的委托类型，在EntrustType中定义

        # 以下为smarT系列参数
        self.buy_entrust_type = EntrustType.entrust  # 买入类型，在EntrustType中定义
        self.sell_entrust_type = EntrustType.entrust  # 卖出类型，在EntrustType中定义
        self.remark = ''  # 备注,T0算法

        self.enhanced_param = ''  # 增强参数（非凸算法专用，非必填）


class SplitOrderAlgoParam(object):
    """
    算法创建参数
    """

    def __init__(self):
        self.algo_type = AlgoType.UNKNOWN  # 算法类型，在AlgoType中定义
        self.start_time = None  # 开始时间,datetime.datetime类型
        self.end_time = None  # 结束时间，datetime.datetime类型
        self.order_side = OrderSide.BUY  # 交易方向，默认为买入，在OrderSide中定义
        self.entrust_type = EntrustType.entrust  # 委托类型（普通账号该字段无效，会被强制填入EntrustType.entrust），在EntrustType中定义
        self.max_market_ratio = 0.3  # 最大市场占比，默认0.3，当前总委托量不大于市场总成交金额*最大市场占比
        self.call_auction_ratio = 0  # 参与开盘集合竞价比例，0表示不参与，SMARTTWAP不支持
        self.style = 1  # 1-平稳，2-激进；该字段仅AI系列、SUPER系列、非凸系列算法支持
        self.forbidden_limit = False  # 是否涨停不卖跌停不买，默认为否，SMARTTWAP不支持
        self.call_auction_offset_ratio = 0  # 开盘集合竞价价格偏离比例，为0时，价格不进行偏离，该字段的取值范围为[0,1]
        self.order_list = []  # 标的信息列表，列表元素为AlgoOrderInfo类型
        self.remark = ''  # 备注

        # 以下字段仅AITWAP、AIVWAP、SUPERTWAP、SUPERVWAP支持
        self.call_close_auction_ratio = 0  # 收盘参与集合竞价比例，0表示不参与
        self.call_close_auction_offset_ratio = 0  # 收盘集合竞价价格偏离比例，为0时，价格不进行偏离，该字段的取值范围为[0,1]
        self.min_order_money = 0   # 单笔最小委托金额，A股默认是0；两融属性默认10000，其中融资买入、买券还券（专项）、融券卖出（专项）不能小于10000元，否则创建失败
        # 以下字段仅SMARTTWAP支持
        self.min_order_qty = 100  # 单笔最小量
        self.max_order_qty = 1000000  # 单笔最大委托量
        self.withdraw_type = 0  # 撤单模式，0-普通，1-自动
        self.entrust_interval = 30  # 委托间隔（s）
        self.withdraw_interval = 12  # 撤单时间间隔（s）
        self.entrust_price_level = 0  # 0 当前价格，1-5 买入对应卖出价1-5档, 卖出对应买入价1-5档，买入对应涨停价卖出对应跌停价档位无价格的用涨跌停价，SMARTSNIPER不支持当前价格，如果填写为0，系统会默认改为1
        self.limit_price_entrust_forbidden = True  # 该参数生效时，不允许以涨停价买入，不允许以跌停价卖出；该参数不生效时，不做涨跌停价格控制

        # 以下字段仅AI调仓支持
        self.trade_progress_deviation = 0.1  # 买卖进度差

        # 以下字段仅SMARTSNIPER支持
        self.swap_board_ratio = 0.5  # 扫盘比例

        # 以下字段目前仅KF支持
        self.up_limit = -1.0  # 涨幅限制 涨幅限制，单位为%，范围[-1,20]，小数位数不限制。填-1或者为空时，相当于此参数不使用
        self.down_limit = -1.0  # 跌幅限制 跌幅限制，单位为%，范围[-1,20]，小数位数不限制。填-1或者为空时，相当于此参数不使用
        self.after_action = False  # 过期后是否继续交易 True:到了结束时间，算法未完成全部交易，继续交易，直到闭市，不参与收盘集合竞价
        # 以下字段目前仅卡方算法、跃然算法、非凸算法支持
        self.limit_action = False  # 涨跌停是否继续交易 True:涨停可以卖、跌停可以买 False:涨停不卖、跌停不买

        # 以下为smarT系列参数
        self.expiration_date = None  # 截止日期，datetime.date类型
        # --以下字段目前仅启能达T0、跃然T0和跃然算法使用
        self.occupy_amount = 0.0  # 授权资金，启能达T0、跃然T0该参数必须大于0，建议不小于目标数量*前收盘价*5%；跃然算法为0或者空时，代表不限制

        # 是否允许部分标的创建成功，涉及两部分：1、客户端校验；2、算法后台校验
        # 对于算法后台本身的校验，情况如下
        # 【算法】    【模式】   【是否支持部分创建成功】
        # 卡方        多标      支持
        # 跃然        多标      不支持
        # 非凸        多标      支持
        # Super      多标      支持（参数控制，partial_success）
        # 其余算法及T0均不支持
        self.partial_success = 0  # 是否允许部分标的创建成功，仅SUPER算法支持（算法参数，非客户端校验）
        self.cl_partial_success = False  # 客户端是否允许部分标的创建成功(False:默认的是当客户端校验失败后整体失败，与算法本身无关。True：开启允许后，通过校验的部分会发起创建)

        # 以下字段目前仅抢涨停算法支持
        self.sell1_amount = 0.0  # 卖1盘口金额（抢涨停GY）
        self.order_amount = 0.0  # 委托金额
        self.sealed_order_amount = 0.0  # 封单金额（极速抢涨停算法+）
        self.sell_order_amount = 0.0  # 卖单金额（双条件抢单算法+）
        self.price_increase_threshold = 0.0  # 涨幅阈值（双条件抢单算法+）

        # 自定义实例ID目前支持卡方、非凸、跃然算法以及smarT系列(其余算法若使用，需注意在查询实例信息时，该字段会有延迟滞后)
        self.cl_inst_id = ''  # 自定义实例ID(最大支持64个字符,smarT_AOA不支持)，一般无需填写，仅有特殊指定需求时使用，需注意避免重复，建议UUID


class CreateAlgoInstanceRsp(object):
    """
    创建算法的响应
    """

    def __init__(self):
        self.inst_id = ''  # 实例ID（多个实例ID以;连接）
        self.err_code = 0  # 错误码，'0'表示成功，'1'表示超时，'-1'表示失败，'99'表示部分成功（Tips:超时需要通过算法交易界面人工检查算法实例是否创建成功，或者联系Matic技术支持）
        self.err_info = ''  # 错误信息


class NegotiateType(object):
    """
    协商交易类型
    """
    UNKNOWN = 0
    ORDER = 1       # 协商委托（沪市）
    INITIATE = 2    # 协商委托发起（深市）
    CONFIRM = 3     # 协商委托确认（深市）
    REJECT = 4      # 协商委托拒绝（深市）


class SettleType(object):
    """
    协商交易结算方式
    """
    MULTILATERALNETTING = '103'  # 多边净额
    REALTIMEGROSS = '104'  # 逐笔全额
    UNKNOWN = ''  # 未知


class OrderRequest(object):
    """
    报单请求
    """

    def __init__(self):
        self.symbol = ''  # 证券代码
        self.amount = 0  # 报单数量
        self.side = OrderSide.UNKNOWN  # 报单方向，OrderSide中定义
        self.style = None  # 订单类型，限价单用LimitOrderStyle，市价单用MarketOrderStyle（特别注意，港股通报单统一用MarketOrderStyle，需要填入报单价格，价格类型为竞价限价盘（"2"）和增强限价盘（"0"））
        self.entrust_type = EntrustType.entrust  # 委托类型，EntrustType中定义，默认为买卖委托，信用交易需要特别关注委托类型
        self.entrust_prop = EntrustProp.trade  # 委托属性，在EntrustProp中定义
        self.action = OrderAction.UNKNOWN  # 开平方向，OrderAction中定义，期权、期货需要填写
        self.invest_type = HedgeFlag.UNKNOWN  # 投资类型，HedgeFlag中定义，期货填写，包含投机、套保、套利
        self.close_direction = CloseDirection.DEFAULT  # 平仓类型，CloseDirection中定义，期货、期权平仓填写
        self.covered_flag = OptionCoveredFlag.UNKNOWN  # 备兑类型，OptionCoveredFlag中定义，期权备兑填写，其他不填
        self.position_type = PositionType.normal  # 头寸性质，PositionType中定义，融券卖出、买券还券、直接还券必填，其他不用填写
        self.contract_no = ''  # 信用合约编号，信用交易归还合约时选填，不填按默认顺序归还
        self.channel_type = 1  # 该字段已废弃
        self.security_exchange = SecurityExchangeType.UNKNOWN  # 证券市场，港股通必须填写，其他报单类型无效
        self.cl_order_id = ''   # 订单ID，一般无需填写，仅有特殊指定需求时使用，需注意避免重复，建议UUID

        # -------沪深协商交易专用字段-------------
        # 协商交易必填基础字段 symbol、amount、side、style(LimitOrderStyle)
        # 1、沪市协商NegotiateType.ORDER: counter_trader、agreement_no必填
        # 2、深市协商发起NegotiateType.INITIATE: counter_trader、settlement_type、counter_party、agreement_no必填
        # 3、深市协商确认/拒绝NegotiateType.CONFIRM/REJECT: settlement_type、ex_no必填，agreement_no选填
        # 4、深市执行编号查询使用接口get_bond_negotiate_exec_id：settlement_type、agreement_no必填
        self.negotiate_type = NegotiateType.UNKNOWN   # 协商交易类型，NegotiateType中定义
        self.counter_trader = ''    # 沪深协商交易对手方交易员
        self.agreement_no = ''      # 沪深协商交易约定号
        self.settlement_type = SettleType.UNKNOWN     # 深圳协商交易结算方式，SettleType中定义
        self.counter_party = ''     # 深圳协商交易对手主体
        self.ex_no = ''             # 深圳协商交易执行编号


class SecmatchOrderRequest(object):
    """
    融券报单请求
    """

    def __init__(self):
        self.symbol = ''    # 证券代码（必填），6位证券代码+后缀
        self.entrust_type = '2'   # 委托类型（必填），1-出借，2-借入
        self.order_qty = 0  # 委托数量（必填），必须为正整数
        self.term = 0       # 合约期限（天数，必填），必须为正整数
        self.apply_rate = 0.0   # 申请利率（必填），例如利率为4.12%，需填写0.0412(最多支持四位小数)
        self.agreement_no = ''  # 约定号，委托方向为融入时选填，填入约定号则按约定申报配对，否则按非约定申报处理
        self.exp_date = None   # 委托有效日期，datetime.date类型，不传默认到期日是当日



class PurchasOrderRequest(object):
    """
    新股申购请求
    """

    def __init__(self):
        self.symbol = ''  # 申购代码
        self.amount = 0  # 报单数量
        self.sub_price = 0.0  # 发行价
        self.security_exchange = SecurityExchangeType.UNKNOWN  # 证券市场


class FundFlowDetial(object):
    """
    资金流向详情
    """

    def __init__(self):
        self.in_flow_value = 0.0  # 流入金额
        self.in_flow_qty = 0  # 流入股数
        self.out_flow_value = 0.0  # 流出金额
        self.out_flow_qty = 0  # 流出股数


class FundFlow(object):
    """
    资金流向数据
    """

    def __init__(self):
        self.symbol = ''    # 证券代码
        self.datetime = None  # 时间戳，datetime.datetime类型
        self.super_large_order = None  # 超大单 FundFlowDetial对象
        self.large_order = None  # 大单 FundFlowDetial对象
        self.middle_order = None  # 中单 FundFlowDetial对象
        self.small_order = None  # 小单 FundFlowDetial对象
        self.main_order = None  # 主力 FundFlowDetial对象


class OrderReply(object):
    """
    下单响应数据
    """

    def __init__(self):
        self.entrust_type = ''  # 类型
        self.error_code = ''  # 错误码
        self.fund_account = ''  # 资金账号
        self.order_id = ''  # 订单编号
        self.Origin_order_id = ''  # 原订单编号
        self.batch_no = -1  # 批次号
        self.algo_inst_id = ''  # 算法实例ID注
        self.inst_id = ''  # 实例ID
        self.error_info = ''  # 错误信息


class MarginAssetRsp(MResponseInfo):
    """
    查询信用资产返回值
    """

    def __init__(self):
        super(MarginAssetRsp, self).__init__()
        self.margin_asset = None  # 信用资产，MarginAssert对象


class MarginContractRsp(MResponseInfo):
    """
    查询信用合约响应
    """

    def __init__(self):
        super(MarginContractRsp, self).__init__()
        self.margin_contract_list = {}


class MarginSymbolRsp(MResponseInfo):
    """
    查询信用两融标的响应
    """

    def __init__(self):
        super(MarginSymbolRsp, self).__init__()
        self.margin_symbol_list = []  # 信用两融标的，MarginSymbol对象


class MarginSecurityInfo(object):
    """
    融券标的信息
    """

    def __init__(self):
        self.loan_available_qty = 0  # 融券可用额度
        self.loan_ratio = 0  # 融券保证金比例
        self.position_type = PositionType.undefine  # 头寸性质
        self.symbol = ''  # 标的
        self.loan_state = ''  # 融券状态: 0-正常、1-暂停、2-作废


class MarginSecurityInfoRsp(MResponseInfo):
    """
    查询账户可融券信息响应
    """
    def __init__(self):
        super(MarginSecurityInfoRsp, self).__init__()
        self.margin_security_info_list = []  # 信用两融标的，MarginSecurityInfo对象


class InterProcMutex(object):
    """
    进程间互斥锁，通过get_interproc_mutex可以获取进程间互斥锁
    """
    INFINITE = 0xFFFFFFFF

    def __init__(self, name):
        self.mutex = None
        self.name = name

    def lock(self, timeout_msecs=INFINITE):
        pass

    def unlock(self):
        pass

    def destory(self):
        pass


class ComboOptionAction(object):
    """
    期权组合动作
    """
    COMBINE = '1'  # 组合
    SPLIT = '2'  # 拆分
    DEFAULT = '0'  # 默认


class OptionType(object):
    """
    期权合约类型
    """
    PUT = 'P'  # 认沽
    CALL = 'C'  # 认购
    DEFAULT = ''


class ComboOptionStrategyType(object):
    """
    期权组合策略类型
    """
    KS = 'KS'  # 跨式空头策略
    KKS = 'KKS'  # 宽跨式空头策略
    ZBD = 'ZBD'  # 认购期权普通卖出开仓转备兑开仓
    ZXJ = 'ZXJ'  # 认购期权备兑开仓转普通卖出
    CNSJC = 'CNSJC'  # 认购牛市价差策略
    CXSJC = 'CXSJC'  # 认购熊市价差策略
    PNSJC = 'PNSJC'  # 认沽牛市价差策略
    PXSJC = 'PXSJC'  # 认沽熊市价差策略


class ComboOptionReq(object):
    """
    期权组合创建/拆分请求
    """

    def __init__(self):
        super(ComboOptionReq, self).__init__()
        self.combo_option_strategy_id = ''  # 组合策略编号，必填
        self.option_code_1 = ''  # 第一腿期权合约编码，必填
        self.option_hold_type_1 = OptionHoldType.DEFAULT  # 第一腿期权合约持仓类型，必填
        self.option_code_2 = ''  # 第二腿期权合约编码，必填
        self.option_hold_type_2 = OptionHoldType.DEFAULT  # 第二腿期权合约持仓类型，必填
        self.side = OrderSide.UNKNOWN  # 组合动作，必填，创建组合（买入：OrderSide.BUY），拆分组合（卖出：OrderSide.SELL）
        self.amount = 0  # 组合数量，必填
        self.security_exchange = SecurityExchangeType.UNKNOWN  # 市场
        self.combo_option_order_id = ''  # 拆分时必填，创建组合时不必填写
        self.cl_order_id = ''  # 订单ID，无需填写，仅有特殊指定需求时使用，需注意避免重复，建议UUID


class ComboOptionStrategyInfo(object):
    """
    期权组合策略信息
    """

    def __init__(self):
        self.exchange_type = SecurityExchangeType.UNKNOWN # 证券交易市场
        self.combo_option_strategy_id = ''  # 组合策略编码
        self.combo_option_strategy_name = ''  # 组合策略名称
        self.same_end_date = True  # 到期日是否相同
        self.same_underlying_symbol = True  # 标的证券是否相同
        self.same_unit = True  # 合约单位是否相同
        self.component_count = 0  # 成分合约个数
        self.option_type_1 = OptionType.DEFAULT  # 第一腿合约类型
        self.option_hold_type_1 = OptionHoldType.DEFAULT  # 第一腿合约持仓类型
        self.option_exercise_price_seq_1 = ''  # 第一腿合约行权价格顺序（用于标识构建期权组合时，第一腿和第二腿的顺序，特别是在两腿合约相同时，需要通过这个价格顺序来确定第一腿和第二腿的顺序）
        self.option_amount_1 = 0  # 第一腿合约数量
        self.option_type_2 = OptionType.DEFAULT  # 第二腿合约类型
        self.option_hold_type_2 = OptionHoldType.DEFAULT  # 第二腿合约持仓类型
        self.option_amount_2 = 0  # 第二腿合约数量
        self.option_exercise_price_seq_2 = ''  # 第二腿合约行权价格顺序
        self.near_split_days = 0  # 组合到期提前拆分天数
        self.remark = ''  # 备注


class ComboOptionPosInfo(object):
    """
    期权组合持仓信息
    """

    def __init__(self):
        self.fund_account = ''  # 资金账号
        self.exchange_type = SecurityExchangeType.UNKNOWN  # 证券交易市场
        self.option_account = ''  # 衍生品合约账户
        self.combo_option_id = ''  # 组合编码
        self.combo_option_strategy_id = ''  # 组合策略编码
        self.combo_option_strategy_name = ''  # 组合策略名称
        self.current_amount = 0  # 当前数量
        self.enable_amount = 0  # 可用数量
        self.real_comb_amount = 0  # 回报组合数量
        self.real_split_amount = 0  # 回报拆分数量
        self.entrust_split_amount = 0  # 委托拆分数量
        self.option_code_1 = ''  # 第一腿期权合约编码
        self.option_type_1 = OptionType.DEFAULT  # 第一腿合约类型
        self.option_name_1 = ''  # 第一腿期权合约简称
        self.option_hold_type_1 = OptionHoldType.DEFAULT  # 第一腿合约持仓类型
        self.option_amount_1 = 0  # 第一腿合约数量
        self.option_code_2 = ''  # 第二腿期权合约编码
        self.option_type_2 = OptionType.DEFAULT  # 第二腿合约类型
        self.option_name_2 = ''  # 第二腿期权合约简称
        self.option_hold_type_2 = OptionHoldType.DEFAULT  # 第二腿合约持仓类型
        self.option_amount_2 = 0  # 第二腿合约数量
        self.comb_bail_balance = 0  # 组合占用保证金
        self.split_comb_margin = 0  # 组合拆分后保证金
        self.comb_auto_split_date = ''  # 组合自动拆分日期


class NewStockDetailInfo(object):
    """
    新股信息
    """

    def __init__(self):
        self.fund_account = ''  # 资金账号
        self.subscription_code = ''  # 申购代码
        self.security_Id = ''  # 正股代码
        self.security_name = ''  # 证券名称
        self.exchange_type = SecurityExchangeType.UNKNOWN  # 市场
        self.sub_price = 0.0  # 发行价格
        self.security_type = SecurityType.UNKNOWN  # 证券类型, SecurityType类型
        self.max_sub_amount = 0  # 可申购额度，股票单位是股，债券单位是张
        # 如下为北交所新增
        self.issue_way = ''  # 发行方式，定价发行或者竞价发行（0询价发行 1定价发行 2竞价发行）
        self.min_sub_price = 0.0  # 北交所最小申购价格，定价发行时，最小申购价格等于最大申购价格
        self.max_sub_price = 0.0  # 北交所最大申购价格，定价发行时，最小申购价格等于最大申购价格
        self.min_sub_amount = 100  # 北交所最小申购额度，单位是股/张

        # self.total_fund_amount = 0.0  # 募集资金总额
        # self.issue_date = None  # 网上发行日，datetime.date类型
        # self.ration_offline_date = None  # 网下配售日，datetime.date类型
        # self.issue_count = 0  # 网上发行量
        # self.ration_count = 0  # 网下配售量
        # self.total_count = 0  # 总发行量
        # self.capital_need_max = 0.0  # 顶格申购需配市值
        # self.payin_date = None  # 中签缴款日，datetime.date类型


class FundInfoCounter(object):
    """
    资金信息,柜台查询
    """

    def __init__(self):
        self.current_balance = 0  # 当前余额
        self.begin_balance = 0  # 期初余额
        self.enable_balance = 0  # 可用资金
        self.foregift_balance = 0  # 禁取资金
        self.mortgage_balance = 0  # 禁取资产
        self.frozen_balance = 0  # 冻结资金
        self.unfrozen_balance = 0  # 解冻资金
        self.fetch_balance = 0  # 可取金额
        self.fetch_cash = 0  # 可取现金
        self.entrust_buy_balance = 0  # 委托买入金额
        self.market_value = 0  # 证券市值
        self.asset_balance = 0  # 资产值
        self.interest = 0  # 待入账利息
        self.integral_balance = 0  # 利息积数
        self.fine_integral = 0  # 罚息积数
        self.pre_interest = 0  # 预计利息
        self.pre_fine = 0  # 预计罚息
        self.pre_interest_tax = 0  # 预计利息税
        self.fund_balance = 0  # 总资金余额
        self.opfund_market_value = 0  # 开基市值
        self.rate_kind = 0  # 利率类别
        self.real_buy_balance = 0  # 回报买入金额
        self.realSell_balance = 0  # 回报卖出金额
        self.net_asset = 0  # 净资产
        self.prod_market_value = 0  # 多金融产品市值
        self.correct_balance = 0  # 资产修正金额


class QueryFundRsp(MResponseInfo):
    """
    柜台查询资金信息返回
    """

    def __init__(self):
        super(QueryFundRsp, self).__init__()
        self.fund_info = None  # 资金信息，FundInfoCounter对象