# encoding: utf-8
#################################订单管理对象###########################
"""
提供单笔普通订单的订单管理对象，支持数量、价格检查、大单拆分、定时撤单、资金/持仓检查等，具体的使用示例参考内置策略中的“调仓策略.py”
注意事项：
如果订单废单，该笔订单监控将会直接终止，由用户自行处理
如果设置了定时撤单，那么订单状态非已撤、部撤、已成、废单时，会在指定次数内一直循环撤单，直到撤成，默认不定时撤单
如果设置了校验资金和持仓，则资金不足会等待指定的时间重新检查，重试次数和时间间隔由用户设定，持仓不足也会等待指定的时间重新检查，默认不检查资金和持仓
如果订单监控状态为stop时，可以查看剩余未成数量（可能包含未委托数量）和已撤数量
"""
from mquant_api import *
from mquant_struct import *
from abc import abstractmethod


class OrderObjStatus(object):
    """
    对象状态
    """
    init = 0  # 初始状态
    running = 1  # 运行中,包括撤单监控中
    stop = 2  # 已停止


class OrderObject(object):
    """
    单笔订单的订单管理类，支持参数合法性检查、自动拆单、超时自动撤单
    支持设置如果资金、持仓不足，则每隔指定时间检查一次资金持仓是否已经满足要求，满足时再报单
    """

    def __init__(self):
        self.symbol = ''
        self.qty_list = []  # 考虑到拆单的场景,数量是一个数组
        self.side = OrderSide.UNKNOWN  # 交易方向
        self.order_list = {}  # 订单列表，单只标的拆单后形成的订单列表
        self.status = OrderObjStatus.init  # 订单管理对象状态
        self.__remain_order_qty = 0  # 剩余数量，委托数量-已成数量，只有设置了有效的撤单时间间隔，补单才是有意义的，status为OrderObjStatus.stop时才可查看
        self.__cancelled_order_qty = 0  # 已撤数量，只有设置了有效的撤单时间间隔，补单才是有意义的，status为OrderObjStatus.stop时才可查看

        self.qty = 0
        # 特别注意，未报到柜台的废单不会体现在补单数量中，这部分用户可自行修改代码，通过接收订单回报来进行管理
        self.max_qty = 900000  # 最大委托数量，默认90w，柜台最大不能超过100w，报单数量超过最大委托数量，会自动拆单
        self.min_qty = 100  # 最小委托数量，报单数量一定要超过最小委托数量才能报单
        self.__price_precision = 2  # 价格精度，默认为普通A股的价格精度2，基金、债券的价格精度会有不同
        self.__qty_precision = 100  # 数量精度，默认为普通A股的数量精度100，报单数量一定要是__qty_precision的整数倍才能正常报单
        self.__cancel_order_interval_secs = 0  # 撤单时间间隔，为0表示不撤单
        self.__status_callback_func = None
        self.__loop_check_interval_secs = 2  # 资金持仓不足时循环检查的时间间隔
        self.__loop_check_flag = False  # 资金持仓不足时循环检查标志，默认不循环检查，报单时不检查资金和持仓
        self.high_limit_price = 0  # 涨停价
        self.low_limit_price = 0  # 跌停价
        self.__cancel_order_try_count = -1        #撤单重试次数，-1表示无限次
        self.__loop_check_try_count = -1          #资金持仓不足时的重试次数，-1表示无限次

    def on_order_report_event(self, ord):
        """
        接收报单推送
        :param ord:
        :return:
        """
        if self.order_list.get(ord.order_id) is None:
            return False
        #判断订单已经到最终状态，则停止监控，如果是部撤状态，记录撤单数量，也可终止
        if ord.status == OrderStatus.canceled:
            log.info('订单已撤销，不再监控，订单id：{}， 订单状态：{}， 委托时间：{},已撤数量：{}'.format(ord.order_id, ord.status.value,
                                                                           ord.add_time,
                                                                           ord.withdraw_amount))
            self.__cancelled_order_qty = self.__cancelled_order_qty + ord.withdraw_amount
            self.__remain_order_qty = self.__remain_order_qty - (ord.amount - ord.withdraw_amount)
            self.order_list.pop(ord.order_id)
        elif ord.status == OrderStatus.rejected:
            log.info('订单已废单，不再监控，订单id：{}，  委托时间：{}, 委托数量：{}'.format(ord.order_id, order_info.add_time, ord.amount))
            self.order_list.pop(ord.order_id)
        elif ord.status == OrderStatus.held:
            log.info('订单已完成，不再监控，订单id：{}， 订单状态：{}， 委托时间：{}'.format(ord.order_id, ord.status.value,
                                                                   ord.add_time))
            self.__remain_order_qty = self.__remain_order_qty - ord.amount
            self.order_list.pop(ord.order_id)

        # 还有订单状态未定，则间隔撤单时间后继续撤单，直到所有订单状态都达到最终状态为止
        if self.__cancel_order_interval_secs > 0 and len(self.order_list) > 0:
            pass
        else:
            if len(self.qty_list) == 0:
                self.__set_status(OrderObjStatus.stop)
        return True

    def cancelled_qty(self):
        """
        已撤数量
        :return:
        """
        return self.__cancelled_order_qty

    def remain_qty(self):
        """
        剩余未成交数量
        :return:
        """
        return self.__remain_order_qty

    def set_order_qty_range(self, min_qty, max_qty):
        """
        设置订单数量范围
        :param min_qty:
        :param max_qty:
        :return:
        """
        self.max_qty = max_qty
        self.min_qty = min_qty

    def set_price_precision(self, precision):
        """
        设置价格精度
        :param precision:
        :return:
        """
        self.__price_precision = precision

    def set_qty_precision(self, precision):
        """
        设置数量精度
        :param precision:
        :return:
        """
        self.__qty_precision = precision

    def set_cancel_order_interval(self, cancel_interval_secs, try_count = -1):
        """
        设置撤单时间间隔，
        :param cancel_interval_secs:
        :param price_level:
        :return:
        """
        if cancel_interval_secs >= 0:
            self.__cancel_order_interval_secs = cancel_interval_secs
            self.__cancel_order_try_count = try_count
        else:
            log.warn('设置撤单时间间隔失败，参数不合法：{}'.format(cancel_interval_secs))

    def set_loop_check_when_fund_or_position_dissatisfy(self, interval_secs=2, try_count = -1):
        """
        设置当资金或持仓不足时，循环检查，满足条件再报单
        :param interval_secs:
        :return:
        """
        if interval_secs > 0:
            self.__loop_check_flag = True
            self.__loop_check_interval_secs = interval_secs
            self.__loop_check_try_count = try_count

    def set_order_param(self, symbol, qty, side):
        """
        报单接口，返回订单列表 list类型
        :return:
        """
        if len(symbol) < 6:
            log.warn('不合法的标的：{}'.format(symbol))
            self.__set_status(OrderObjStatus.stop)
            return False

        self.symbol = symbol
        self.set_qty(qty)
        if len(self.qty_list) == 0:
            log.warn('不合法的订单数量，证券代码：{},数量：{}'.format(self.symbol, qty))
            self.__set_status(OrderObjStatus.stop)
            return False

        if side in [OrderSide.BUY, OrderSide.SELL]:
            self.side = side
        else:
            log.warn('不合法的订单方向，证券代码：{},数量：{}，方向：{}'.format(self.symbol, qty, side))
            self.__set_status(OrderObjStatus.stop)
            return False

        self.__set_status(OrderObjStatus.running)
        
        return True

    def register_status_callback(self, func):
        """
        注册状态变化回调
        :param func:
        :return:
        """
        self.__status_callback_func = func

    def order(self):
        """
        报单接口，返回订单列表 list类型
        :param symbol:标的
        :param qty:数量
        :param style:价格，包括市价单和限价单，市价单不做处理，限价单会检查价格精度，如果价格精度不正确，会截断报单
        :return:
        """
        self.__order_exec()
        return self.order_list.values()

    def set_qty(self, qty):
        """
        修正委托数量
        数量超过最大委托数量，则拆单，数量小于最小委托数量，则报单失败，数量不满足数量精度要求，则下取整
        """
        self.qty = qty
        self.__remain_order_qty = qty
        fix_qty = qty
        if qty < self.min_qty:
            log.warn('标的[{}]委托数量[{}]小于最小委托数量[{}]，订单信息无效'.format(self.symbol, qty, self.min_qty))
            return None

        if qty % self.__qty_precision != 0:
            fix_qty = qty - qty % g.__qty_precision
            log.info('标的[{}]原委托数量:{},修正后委托数量:{}'.format(self.symbol, qty, fix_qty))

        while fix_qty > self.max_qty:
            if fix_qty - self.max_qty > self.min_qty:
                self.qty_list.append(self.max_qty)
                fix_qty = fix_qty - self.max_qty
                if fix_qty <= self.max_qty:
                    self.qty_list.append(fix_qty)
                    fix_qty = 0
                    break
            else:
                self.qty_list.append(self.min_qty)
                self.qty_list.append(fix_qty - self.min_qty)
                fix_qty = 0
        if fix_qty > 0:
            self.qty_list.append(fix_qty)

    @abstractmethod
    def get_style(self):
        """
        订单价格，默认为市价单，使用者可根据自己的情况选择实现
        :return:
        """
        return MarketOrderStyle()

    def __get_style(self):
        """
        获取订单价格，限价单会检查价格精度，如果价格精度超过设置的价格精度，将会直接截断
        :return:
        """
        style = self.get_style()
        if isinstance(style, LimitOrderStyle):
            style = LimitOrderStyle(round(style.limit_price, self.__price_precision))
        return style

    def __check_fund(self, qty):
        """
        校验资金，注意，资金有1.5-2s的延迟，取到的资金不一定是柜台真实的资金
        :param qty:
        :return:
        """
        if self.__get_style() is None or isinstance(self.__get_style(), MarketOrderStyle):
            # 买入按涨停价控资金
            if self.high_limit_price < 0.0001:
                symbol_detial = get_symbol_detial(self.symbol)
                if symbol_detial is None:
                    log.warn('获取标的{}的涨停价失败，不校验资金，直接报单'.format(self.symbol))
                    return True
                else:
                    self.high_limit_price = symbol_detial.HighLimitPrice
                    self.low_limit_price = symbol_detial.LowLimitPrice
            available_cash = context.portfolio.available_cash
            if qty * self.high_limit_price > available_cash:
                log.warn('标的{}买入{}股资金不足，需要资金：{}，可用资金：{}'.format(self.symbol, qty, qty * self.high_limit_price,
                                                                available_cash))
                return False
        elif isinstance(self.__get_style(), LimitOrderStyle):
            price = self.__get_style().limit_price
            available_cash = context.portfolio.available_cash
            if qty * price > available_cash:
                log.warn('标的{}买入{}股资金不足，需要资金：{}，可用资金：{}'.format(self.symbol, qty, qty * price,
                                                                available_cash))
                return False
        return True

    def __check_pos(self, qty):
        """
        检查持仓是否足够
        :param qty:
        :return:
        """
        pos_info = context.portfolio.positions[self.symbol]
        if pos_info is None:
            log.info('获取标的{}的持仓失败，继续等待报单'.format(self.symbol))
            return False
        elif pos_info.closeable_amount < qty:
            log.info('标的{}的可用持仓不足，报单数量：{}， 可用持仓：{}'.format(self.symbol, qty, pos_info.closeable_amount))
            return False
        else:
            return True

    def __order_exec(self):
        """
        报单执行
        """
        symbol = self.symbol
        qty_list = self.qty_list[:]
        self.qty_list.clear()
        for qty in qty_list:
            log.info('开始报单，标的：{}，数量：{}，价格类型：{}'.format(symbol, qty, self.__get_style()))

            if self.side == OrderSide.BUY:
                if self.__loop_check_flag and not self.__check_fund(qty):
                    # 资金不足，循环检测，满足条件再报单
                    self.qty_list.append(qty)
                    continue
                ord = order(symbol, qty, self.__get_style())
                if ord is not None:
                    self.order_list[ord.order_id] = ord
                else:
                    log.error('买入报单失败，标的：{}， 数量：{}'.format(symbol, qty))
            else:
                if self.__loop_check_flag and not self.__check_pos(qty):
                    # 持仓不足，循环检测，满足条件再报单
                    self.qty_list.append(qty)
                    continue

                ord = order(symbol, -1 * qty, self.__get_style())
                if ord is not None:
                    self.order_list[ord.order_id] = ord
                else:
                    log.error('卖出报单失败，标的：{}， 数量：{}'.format(symbol, qty))

        self.__set_status(OrderObjStatus.running)
        # 如果有部分订单未通过资金持仓检查，则注册定时器，定时检查
        if len(self.qty_list) > 0:
            time = datetime.datetime.now() + datetime.timedelta(seconds=self.__loop_check_interval_secs)
            run_timely(self.__loop_check_and_reorder, -1, time.strftime('%H:%M:%S'))

        # 如果有报出去的订单，且要求定时撤单，则注册定时器定时撤单
        if self.__cancel_order_interval_secs > 0 and len(self.order_list) > 0:
            time = datetime.datetime.now() + datetime.timedelta(seconds=self.__cancel_order_interval_secs)
            run_timely(self.__cancel_order, -1, time.strftime('%H:%M:%S'))
        else:
            if len(self.qty_list) == 0:
                self.__set_status(OrderObjStatus.stop)

    def __loop_check_and_reorder(self, context, interval, msg_type):
        """
        不满足资金持仓检查的订单重新报单
        :param context:
        :param interval:
        :param msg_type:
        :return:
        """
        if self.__loop_check_try_count == -1:
            log.debug('重新检查资金持仓是否满足条件并报单，标的：{}'.format(self.symbol))
            self.__order_exec()
            
        elif self.__loop_check_try_count - 1 > 0:
            log.debug('重新检查资金持仓是否满足条件并报单，标的：{}，剩余次数:{}'.format(self.symbol, self.__loop_check_try_count - 1))
            self.__loop_check_try_count = self.__loop_check_try_count - 1
            self.__order_exec()
        else:
            log.debug('检查资金持仓是否满足条件并报单达到设定的次数，停止检查，标的：{}'.format(self.symbol))
            if self.__cancel_order_interval_secs <= 0 or len(self.order_list) == 0:
                self.__set_status(OrderObjStatus.stop)

    def __cancel_order(self, context, interval, msg_type):
        """
        撤单函数
        """
        if self.__cancel_order_try_count <= 1 and self.__cancel_order_try_count != -1:
            log.debug('撤单达到设定的次数，停止撤单，标的：{}'.format(self.symbol))
            if not self.__loop_check_flag or len(self.qty_list) == 0:
                self.__set_status(OrderObjStatus.stop)
            return
        
        elif self.__cancel_order_try_count != -1:
            log.debug('开始撤单，标的：{}，剩余次数:{}'.format(self.symbol, self.__cancel_order_try_count - 1))
            self.__cancel_order_try_count = self.__cancel_order_try_count - 1
            
        # 判断当前订单状态，如果未全成则定时循环撤单，直到订单达到最终状态（已成、已撤、部撤、废单），达到最终状态的订单不再定时撤单
        for ord in self.order_list.values():
            # 查询订单
            order_dict = get_orders(ord.order_id)
            if order_dict is None or len(order_dict) == 0:
                log.error('未找到订单：{}对应的订单信息'.format(ord.order_id))
                continue
            order_info = order_dict.get(ord.order_id)
            if order_info is None:
                log.error('未找到订单：{}，查询返回的key：{}'.format(ord.order_id, order_dict.keys()))
                continue
            # 撤单撤成功之后再补单，未收到撤单成交的消息不补单，避免超单
            if order_info.status in [OrderStatus.new, OrderStatus.open, OrderStatus.filled]:  # 待报、已报、部成，直接撤单
                log.info(
                    '开始撤单，订单id：{}， 订单状态：{}， 委托时间：{}'.format(ord.order_id, order_info.status.value, order_info.add_time))
                cancel_order(order_info)
            elif order_info.status == OrderStatus.canceled:
                log.info('订单已撤销，不再监控，订单id：{}， 订单状态：{}， 委托时间：{},已撤数量：{}'.format(ord.order_id, order_info.status.value,
                                                                               order_info.add_time,
                                                                               order_info.withdraw_amount))
                self.__cancelled_order_qty = self.__cancelled_order_qty + order_info.withdraw_amount
                self.__remain_order_qty = self.__remain_order_qty - (order_info.amount - order_info.withdraw_amount)
                self.order_list.pop(ord.order_id)
            elif order_info.status == OrderStatus.rejected:
                log.info('订单已废单，不再监控，订单id：{}，  委托时间：{}, 委托数量：{}'.format(ord.order_id, order_info.add_time, ord.amount))
                self.order_list.pop(ord.order_id)
            elif order_info.status == OrderStatus.held:
                log.info('订单已完成，不再监控，订单id：{}， 订单状态：{}， 委托时间：{}'.format(ord.order_id, order_info.status.value,
                                                                       order_info.add_time))
                self.__remain_order_qty = self.__remain_order_qty - order_info.amount
                self.order_list.pop(ord.order_id)

        # 还有订单状态未定，则间隔撤单时间后继续撤单，直到所有订单状态都达到最终状态为止
        if self.__cancel_order_interval_secs > 0 and len(self.order_list) > 0:
            time = datetime.datetime.now() + datetime.timedelta(seconds=self.__cancel_order_interval_secs)
            run_timely(self.__cancel_order, -1, time.strftime('%H:%M:%S'))
        else:
            if len(self.qty_list) == 0:
                self.__set_status(OrderObjStatus.stop)

    def __set_status(self, status):
        """
        设置状态
        :param status:
        :return:
        """
        self.status = status
        if self.__status_callback_func is not None:
            self.__status_callback_func(status)
