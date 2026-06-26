#encoding: utf-8

from mquant_api import *
from mquant_struct import *
def timer_func(conetxt, interval, msg_type):
    """
    示例定时函数
    :param conetxt:
    :return:
    :remark:用户函数，可写可不写
    """
    open_orders = get_open_orders(only_this_inst=False)
    cancel_order_list = []
    for ord_id, order_item in open_orders.items():
        # 判断如果是限价单，则撤单
        if isinstance(order_item.style, LimitOrderStyle):
            item = batch_cancel_order_item()
            item.order_id=order_item.order_id
            cancel_order(order_item)
            cancel_order_list.append(item)
    if len(cancel_order_list) > 0:
        log.debug('开始批量撤单，数量：%d' % len(cancel_order_list))
        cancel_orders(cancel_order_list)
        log.debug('批量撤单结束')
    # print('enter timer func,inerval:%d'%interval)

def strategy_params():
    """
    策略可自定义运行参数，启动策略时会写入到context对象的run_params字段内
    :return:dict对象，key为参数名，value为一个包含参数默认值、参数描述（选填）的字典
    :remark:可选实现，参数由策略自由填写，自己解析
    """
    #示例如下：
    dict_params = {
       '撤单时间间隔':{'value':10}
       }
    return dict_params


def initialize(context):
    """
    策略初始化，启动策略时调用，用户可在初始化函数中订阅行情、设置标的、设置定时处理函数等
    该函数中允许读取文件，除此之外的其他函数禁止读取文件
    :param context:
    :return:
    :remark:必须实现
    """
    run_timely(timer_func, context.run_params['撤单时间间隔'])

def on_strategy_end(context):
    """
    策略结束时调用，用户可以在此函数中进行一些汇总分析、环境清理等工作
    :param context:
    :return:
    :remark:可选实现
    """
    pass