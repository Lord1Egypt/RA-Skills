# encoding: utf-8

from mquant_api import *
from mquant_struct import *
import json
import os
import time
import threading
import shutil
import datetime


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


class TradeDataDownloader(object):
    """
    数据下载类
    """

    def __init__(self):
        self.__context = None
        cur_date = datetime.datetime.strftime(datetime.datetime.now(), "%Y-%m-%d")
        self.__file_dir = 'D\\MQuantTradeData\\' + cur_date
        self.__custom_field_mutex = threading.Lock()
        self.__complete_section_mutex = threading.Lock()
        self.__order_custom_field = {}
        self.__complete_section = False
        self.__enable_custom_field = False
        self.__order_req_info = {}
        self.__account_type_info = {}
        self.__bak_file_num = 0
        self.__only_download_mquant_order = False

    def set_complete_section(self, flag):
        self.__complete_section = flag

    def set_enable_custom_field(self, flag):
        self.__enable_custom_field = flag

    def set_bak_file_num(self, num):
        self.__bak_file_num = num

    def set_context(self, context):
        self.__context = context
        fund_account_stock = context.get_fund_account_by_type(AccountType.normal)
        if fund_account_stock is not None and len(fund_account_stock) > 0:
            self.__account_type_info[fund_account_stock] = AccountType.normal

        fund_account_margin = context.get_fund_account_by_type(AccountType.margin)
        if fund_account_margin is not None and len(fund_account_margin) > 0:
            self.__account_type_info[fund_account_margin] = AccountType.margin

    def set_file_dir_path(self, dir_path):
        if not os.path.exists(dir_path):
            os.mkdir(dir_path)
        cur_date = datetime.datetime.strftime(datetime.datetime.now(), "%Y-%m-%d")
        self.__file_dir = dir_path + '\\' + cur_date
        if not os.path.exists(self.__file_dir):
            os.mkdir(self.__file_dir)

    def only_download_mquant_order(self, flag):
        self.__only_download_mquant_order = flag


    def get_order_file_path(self, fund_account):
        """
        获取订单文件路径
        :param fund_account:
        :return:
        """
        if fund_account is None:
            return ''
        if len(fund_account) == 0:
            return ''
        return self.__file_dir + '\\order_' + fund_account + '.csv'

    def get_execution_file_path(self, fund_account):
        """
        获取成交文件路径
        :param fund_account:
        :return:
        """
        if fund_account is None:
            return ''
        if len(fund_account) == 0:
            return ''
        return self.__file_dir + '\\execution_' + fund_account + '.csv'

    def get_fund_file_path(self, fund_account):
        """
        获取资金文件路径
        :param account_type:
        :return:
        """
        if fund_account is None:
            return ''
        if len(fund_account) == 0:
            return ''
        return self.__file_dir + '\\fund_' + fund_account + '.csv'

    def get_pos_file_path(self, fund_account):
        """
        获取持仓文件路径
        :param fund_account:
        :return:
        """
        if fund_account is None:
            return ''
        if len(fund_account) == 0:
            return ''
        return self.__file_dir + '\\position_' + fund_account + '.csv'

    def get_custom_field_file_path(self):
        """
        获取自定义字段文件路径
        :return:
        """
        return self.__file_dir + '\\custom_field.csv'

    def init_trade_files(self):
        """
        交易数据初始化
        :return:
        """
        self.init_custom_fields()
        self.init_order_files(AccountType.normal)
        self.init_order_files(AccountType.margin)
        self.init_execution_files(AccountType.normal)
        self.init_execution_files(AccountType.margin)
        self.init_fund_files(AccountType.normal)
        self.init_pos_files(AccountType.normal)
        self.init_fund_files(AccountType.margin)
        self.init_pos_files(AccountType.margin)

    def init_custom_fields(self):
        """
        初始化自定义字段
        :return:
        """
        if not self.__enable_custom_field:
            return
        custom_field_file_path = self.get_custom_field_file_path()
        if not os.path.exists(custom_field_file_path):
            with open(custom_field_file_path, 'w', encoding='utf-8') as f:
                f.write('订单号,自定义字段\n')
        else:
            # 将自定义字段信息都读取出来
            with open(custom_field_file_path, 'r', encoding='utf-8') as f:
                info_list = f.readlines()
                if len(info_list) > 0:
                    while not self.__custom_field_mutex.acquire():
                        time.sleep(0.01)
                    for line in info_list:
                        lst_item = line.rstrip('\n').split(',')
                        self.__order_custom_field[lst_item[0]] = lst_item[1]
                    self.__custom_field_mutex.release()

    def init_order_files(self, account_type):
        """
        初始化订单数据
        :param account_type:
        :return:
        """
        order_file = self.get_order_file_path(self.__context.get_fund_account_by_type(account_type))
        if len(order_file) == 0:
            return

        with open(order_file, 'w', encoding='utf-8') as f:
            f.write(
                '资金账号,委托时间,实例ID,证券代码,买卖方向,委托数量,委托价格,状态,价格类型,柜台委托编号,委托属性,委托类型,成交数量,成交金额,成交均价,撤单数量,废单原因,订单编号,自定义字段,算法实例ID,更新时间,市场,批次号\n')
            page_no = 1
            tmp_orders = []
            while True:
                ret_data = get_orders_ex(only_this_inst=False, page_no=page_no,
                                         account_type=account_type)  # 仅演示获取普通A股账号的订单信息，可根据自己的实际场景选择获取两融的,分页查询，每次获取1000条
                ord_list = ret_data[2]
                if ord_list is not None:
                    tmp_orders = tmp_orders + list(ord_list.values())
                    
                    if ret_data[1]:
                        break
                    page_no = page_no + 1
                else:
                    break
            tmp_orders = sorted(tmp_orders, key=lambda ord: str(ord.add_time) + str(ord.entrust_no))
#            pre_time = None
            for ord in tmp_orders:
                if self.__only_download_mquant_order and (ord.inst_id is None or len(ord.inst_id) == 0):
                    continue
#                if pre_time is not None:
#                    if ord.add_time < pre_time:
#                        print('sort error', ord.add_time, pre_time)
#                pre_time = ord.add_time
#                log.debug('{}'.format(ord.add_time))
                f.write(self.get_order_str(ord))

    def init_execution_files(self, account_type):
        """
        初始化成交文件
        :param account_type:
        :return:
        """
        execution_file = self.get_execution_file_path(self.__context.get_fund_account_by_type(account_type))
        if len(execution_file) == 0:
            return
        with open(execution_file, 'w', encoding='utf-8') as f:
            f.write('资金账号,成交时间,实例ID,证券代码,买卖方向,成交价格,成交数量,成交金额,成交类型,柜台委托编号,柜台成交编号,订单编号,自定义字段,算法实例ID,更新时间,市场\n')
            page_no = 1
            tmp_execution_list = []
            while True:
                ret_data = get_trades_ex(only_this_inst=False, page_no=page_no, page_size=1000,
                                         account_type=account_type)  # 仅演示获取普通A股账号的订单信息，可根据自己的实际场景选择获取两融的

                execution_list = ret_data[2]
                if execution_list is not None:
                    print('查询成交返回：', len(execution_list))
                    tmp_execution_list = tmp_execution_list + execution_list
                    

                    if ret_data[1]:
                        break
                    page_no = page_no + 1
                else:
                    break
            tmp_execution_list = sorted(tmp_execution_list,
                                            key=lambda execution: str(execution.time) + str(execution.trade_id))

            for execution in tmp_execution_list:
                if self.__only_download_mquant_order and (execution.inst_id is None or len(execution.inst_id) == 0):
                    continue
                f.write(self.get_execution_str(execution))

    def init_fund_files(self, account_type):
        """
        初始化资金文件
        :return:
        """
        fund_account = self.__context.get_fund_account_by_type(account_type)
        fund_file = self.get_fund_file_path(fund_account)
        if len(fund_file) == 0:
            return
        with open(fund_file, 'w', encoding='utf-8') as f:
            f.write(self.get_fund_str(fund_account))

    def init_pos_files(self, account_type):
        """
        初始化持仓信息
        :return:
        """
        # 持仓
        self.write_pos_info(self.__context.get_fund_account_by_type(account_type))

    def get_bak_file(self, origin_file, subfix=0):
        """

        :param origin_file:
        :param subfix:
        :return:
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

    def bak_trade_files(self, order_file, execution_file, fund_file, pos_file):
        """

        :param order_file:
        :param execution_file:
        :param fund_file:
        :param pos_file:
        :return:
        """

        if os.path.exists(order_file):
            ord_bak_file = get_bak_file(order_file)
            if len(ord_bak_file) > 0:
                shutil.copy(order_file, ord_bak_file)

        if os.path.exists(execution_file):
            exec_bak_file = get_bak_file(execution_file)
            if len(exec_bak_file) > 0:
                shutil.copy(execution_file, exec_bak_file)


    def write_fund_info(self, context, account_type, fund_file):
        """
        写资金
        :param context:
        :param account_type:
        :param fund_file:
        :return:
        """
        with open(fund_file, 'a', encoding='utf-8') as f:
            context.set_current_account_type(account_type)
            fund_account = context.get_fund_account_by_type(account_type)
            fund_str = '{},{},{},{}\n'.format(datetime.datetime.now(), fund_account, context.portfolio.settled_cash,
                                              context.portfolio.available_cash)
            f.write(fund_str)

    def write_pos_info(self, fund_account):
        """
        写持仓
        :param account_type:
        :param pos_file:
        :return:
        """
        if fund_account is None or len(fund_account) == 0:
            return
        pos_file = self.get_pos_file_path(fund_account)
#        if not os.path.exists(pos_file):
#            log.error("持仓文件{}不存在，无法更新持仓信息".format(pos_file))
#            return
        pos_str = '资金账号,证券代码,当前持仓,可用持仓,期初持仓,持仓成本,当前市值,更新时间,市场\n'

        account_type = self.__account_type_info[fund_account]
        pos_list = get_positions_ex(account_type)
        if pos_list is not None:
            for pos in pos_list:
                pos_str = pos_str + '{},{},{},{},{},{},{},{},{}\n'.format(fund_account, pos.security, pos.total_amount,
                                                        pos.closeable_amount,
                                                        pos.init_amount,pos.hold_cost, pos.value,datetime.datetime.now(),pos.security_exchange)

        with open(pos_file, 'w', encoding='utf-8', buffering=len(pos_str) + 1) as f:
            f.write(pos_str)
        

    def record_order(self, order_id, symbol, side, amount, price, price_type):
        """
        记录订单请求
        :param order_id:
        :param symbol:
        :param side:
        :param amount:
        :param price:
        :param price_type:
        :return:
        """
        #    print('record', price, price_type)
        if not self.__complete_section:
            return
        while not self.__complete_section_mutex.acquire():
            time.sleep(0.001)
        if len(order_id) > 0:
            self.__order_req_info[order_id] = {'symbol': symbol, 'side': side, 'amount': amount, 'price': price,
                                               'price_type': price_type,
                                               'time': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        self.__complete_section_mutex.release()

    def get_order_ext_info(self, order_id):
        """
        获取订单请求信息
        :param order_id:
        :return:
        """
        if not self.__complete_section:
            return
        while not self.__complete_section_mutex.acquire():
            time.sleep(0.001)
        if len(order_id) > 0 and self.__order_req_info.get(order_id) is not None:
            ext_order_info = self.__order_req_info[order_id]
            self.__complete_section_mutex.release()
            return ext_order_info
        self.__complete_section_mutex.release()

    def get_custom_field_str(self, ord, push_msg=False):
        """
        获取自定义字段
        """
        if not self.__enable_custom_field:
            return ""
        # 排除非MQuant报单
        if ord.inst_id is None or len(ord.inst_id) == 0:
            #        print('not mquant order:', ord.order_id)
            return ""
        # 排除算法报单
        if ord.algo_inst_id is not None and len(ord.algo_inst_id) > 0:
            return ""

        while not self.__custom_field_mutex.acquire():
            time.sleep(0.01)

        custom_field = self.__order_custom_field.get(ord.order_id)
        self.__custom_field_mutex.release()
        count = 0
        if push_msg:
            while custom_field is None:
                time.sleep(0.01)
                while not self.__custom_field_mutex.acquire():
                    time.sleep(0.001)
                custom_field = self.__order_custom_field.get(ord.order_id)
                self.__custom_field_mutex.release()
                count = count + 1
                if count > 10:
                    custom_field = ''
                    log.warn('尝试获取100次订单的用户自定义字段失败，订单id：{}'.format(ord.order_id))
                    break
        elif custom_field is None:
            custom_field = ''
        return custom_field

    def get_custom_field_str_from_execution(self, execution):
        if not self.__enable_custom_field:
            return ""
        if execution.inst_id is None or len(execution.inst_id) == 0:
            #        print('not mquant order:', ord.order_id)
            return ""
        if execution.algo_inst_id is not None and len(execution.algo_inst_id) > 0:
            return ""

        while not self.__custom_field_mutex.acquire():
            time.sleep(0.001)

        custom_field = self.__order_custom_field.get(execution.order_id)
        self.__custom_field_mutex.release()
        if custom_field is None:
            custom_field = ''
        return custom_field

    def record_custom_field(self, order_id, custom_field):
        """
        记录自定义字段
        """
        if not self.__enable_custom_field:
            return
        while not self.__custom_field_mutex.acquire():
            time.sleep(0.001)
        self.__order_custom_field[order_id] = custom_field
        self.__custom_field_mutex.release()

        # 将自定义字段写入文件
        try:
            with open(self.get_custom_field_file_path(), 'a', encoding='utf-8') as f:
                #            print('record custom field:', order_id, custom_field)
                f.write('{},{}\n'.format(order_id, custom_field))
        except Exception as e:
            print(e)

    def get_order_str(self, ord, push_msg=False):
        """
        订单字符串
        :param ord:
        :param push_msg:
        :return:
        """
        custom_field = ''
        #    if push_msg:
        custom_field = self.get_custom_field_str(ord, push_msg)
        #    print(ord.order_id, ord.status, ord.fund_account)
        if ord.status is None:
            log.debug(ord.order_id)
        cancel_info = ord.cancel_info
        if len(ord.cancel_info) > 0:
            cancel_info = ord.cancel_info.replace(",", ";").replace("\r\n", "")
            cancel_info = cancel_info.replace(",", ";").replace("\n", "")
        if (len(ord.symbol) == 0 or ord.status == OrderStatus.rejected) and self.__complete_section:
            ord_ext_info = self.get_order_ext_info(ord.order_id)
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

        algo_inst_id = ord.algo_inst_id
        if algo_inst_id is None:
            algo_inst_id = ''
        order_info = '{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}\n'.format(ord.fund_account, ord.add_time,
                                                                                         ord.inst_id, ord.symbol,
                                                                                         transfer_order_side(ord.side),
                                                                                         ord.amount,
                                                                                         get_entrust_price(ord.style),
                                                                                         ord.status.value,
                                                                                         transfer_price_type(ord.style),
                                                                                         ord.entrust_no,
                                                                                         ord.entrust_prop,
                                                                                         ord.entrust_type,
                                                                                         ord.filled,
                                                                                         ord.business_balance,
                                                                                         ord.price,
                                                                                         ord.withdraw_amount,
                                                                                         cancel_info, ord.order_id,
                                                                                         custom_field, algo_inst_id,
                                                                                        datetime.datetime.now(),
                                                                                        ord.security_exchange,
                                                                                        ord.batch_no)
        return order_info

    def get_execution_str(self, execution, push_msg=False):
        """
        成交字符串
        :param push_msg:
        :return:
        """
        custom_field = self.get_custom_field_str_from_execution(execution)
        algo_inst_id = execution.algo_inst_id
        if algo_inst_id is None:
            algo_inst_id = ''
        # '资金账号,成交时间,实例ID,证券代码,买卖方向,成交价格,成交数量,成交金额,成交类型,柜台委托编号,柜台成交编号,订单编号,自定义字段'
        execution_info = '{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}\n'.format(execution.fund_account, execution.time,
                                                                              execution.inst_id, execution.symbol,
                                                                              transfer_order_side(execution.side),
                                                                              execution.price,
                                                                              execution.amount,
                                                                              execution.business_balance,
                                                                              execution.real_type,
                                                                              execution.entrust_no, execution.trade_id,
                                                                              execution.order_id,
                                                                              custom_field, algo_inst_id,
                                                                            datetime.datetime.now(),
                                                                            execution.security_exchange)

        return execution_info

    def get_fund_str(self, fund_account, fund_info=None):
        """
        获取资金串
        :param fund_account:
        :param fund_info:
        :return:
        """
        # if fund_info is None:
        #     fund_str = '记录时间,资金账号,期初资金,可用资金\n' + '{},{},{},{}\n'.format(
        #         datetime.datetime.now(),
        #         fund_account,
        #         self.__context.portfolio.settled_cash,
        #         self.__context.portfolio.available_cash)
        # else:
        #     fund_str = '记录时间,资金账号,期初资金,可用资金\n' + '{},{},{},{}\n'.format(
        #         datetime.datetime.now(),
        #         fund_account,
        #         fund_info.settled_cash,
        #         fund_info.available_cash)
        # return fund_str

        if fund_info is None:
            fund_str = '记录时间,资金账号,期初资金,可用资金,当前余额,冻结资金,可取资金,证券市值,总资产,港股可用资金\n' + '{},{},{},{},{},{},{},{},{},{}\n'.format(
                datetime.datetime.now(),
                fund_account,
                self.__context.portfolio.settled_cash,
                self.__context.portfolio.available_cash,
                self.__context.portfolio.total_cash,
                self.__context.portfolio.frozen_cash,
                self.__context.portfolio.transferable_cash,
                self.__context.portfolio.market_value,
                self.__context.portfolio.total_value,
                self.__context.portfolio.hk_available_cash)
        else:
            fund_str = '记录时间,资金账号,期初资金,可用资金,当前余额,冻结资金,可取资金,证券市值,总资产,港股可用资金\n' + '{},{},{},{},{},{},{},{},{},{}\n'.format(
                datetime.datetime.now(),
                fund_account,
                fund_info.settled_cash,
                fund_info.available_cash,
                fund_info.hold_cash,
                fund_info.frozen_cash,
                fund_info.transferable_cash,
                fund_info.market_value,
                fund_info.total_value,
                fund_info.hk_available_cash)
        return fund_str

    def write_order_to_csv(self, ord):
        """
        写订单
        :return:
        """
        file_path = self.get_order_file_path(ord.fund_account)
        if not os.path.exists(file_path):
            log.error("订单文件{}不存在，无法更新订单信息".format(file_path))
            return
        with open(file_path, 'a', encoding='utf-8') as f:
            # 字段：资金账号、委托时间、实例ID、证券代码、买卖方向、委托数量、委托价格、价格类型、柜台委托编号、委托属性、委托类型、成交数量、成交金额、撤单数量、状态、废单原因、自定义字段
            f.write(self.get_order_str(ord, True))

    def write_execution_to_csv(self, execution):
        """
        写成交
        :param execution:
        :return:
        """
        # 成交留待客户自行实现
        file_path = self.get_execution_file_path(execution.fund_account)
        if not os.path.exists(file_path):
            log.error("成交文件{}不存在，无法更新订单信息".format(file_path))
            return
        with open(file_path, 'a', encoding='utf-8') as f:
            # 字段：资金账号、委托时间、实例ID、证券代码、买卖方向、委托数量、委托价格、价格类型、柜台委托编号、委托属性、委托类型、成交数量、成交金额、撤单数量、状态、废单原因
            f.write(self.get_execution_str(execution, True))

    def on_order_update(self, ord):
        """
        订单推送
        :param ord:
        :return:
        """
        if self.__only_download_mquant_order and ( ord.inst_id is None or len(ord.inst_id) == 0):
            return 
        file_path = self.get_order_file_path(ord.fund_account)
        if not os.path.exists(file_path):
            log.error("订单文件{}不存在，无法更新订单信息".format(file_path))
            return
        with open(file_path, 'a', encoding='utf-8') as f:
            # 字段：资金账号、委托时间、实例ID、证券代码、买卖方向、委托数量、委托价格、价格类型、柜台委托编号、委托属性、委托类型、成交数量、成交金额、撤单数量、状态、废单原因、自定义字段
            f.write(self.get_order_str(ord, True))

    def on_execution_update(self, execution):
        """
        成交推送
        :param context:
        :param execution:
        :return:
        """
        if self.__only_download_mquant_order and ( execution.inst_id is None or len(execution.inst_id) == 0):
            return 
        self.write_execution_to_csv(execution)

    def on_fund_update(self, fund_info):
        """
        category:事件回调
        brief:资金推送
        desc:资金推送函数，可选实现。
        :param fund_info: FundUpdateInfo 类对象
        :return:
        """
        fund_file = self.get_fund_file_path(fund_info.fund_account)
        if not os.path.exists(fund_file):
            log.error("资金文件{}不存在，无法更新资金信息".format(fund_file))
            return
        fund_str = self.get_fund_str(fund_info.fund_account, fund_info)
        with open(fund_file, 'w', encoding='utf-8', buffering=len(fund_str) + 1) as f:
            f.write(fund_str)
    
    
    def on_position_update(self, pos_info):
        """
        category:事件回调
        brief:持仓推送
        desc:持仓推送函数，可选实现。
        :param pos_info: Position类对象
        :return:
        """
        self.write_pos_info(pos_info.fund_account)
        
