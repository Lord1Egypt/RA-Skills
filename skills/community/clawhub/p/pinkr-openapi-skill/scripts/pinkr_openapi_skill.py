#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
pinkr_openapi_skill - 品氪 OpenApi 开放平台 skill
支持门店、导购、会员、订单、退单、库存、商品、积分、储值、卡券、销售等全链路CRM/SCRM数据同步与管理
"""

import os
import sys
import json
import re
import requests
from datetime import datetime

# 环境变量配置
PK_APPKEY = os.environ.get('PK_APPKEY')
PK_API_URL = os.environ.get('PK_API_URL', 'http://dev.openapi.pinkr.com')

# 输出目录配置
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'output')
PREFIX = 'pinkr_openapi_skill_'


# ============================================================
# 通用工具函数
# ============================================================

def check_appkey():
    """检查 APPKEY 是否配置"""
    if not PK_APPKEY:
        print("未找到 PK_APPKEY，请设置环境变量：")
        print("   export PK_APPKEY=your_appkey")
        return False
    return True


def ensure_output_dir():
    """确保输出目录存在"""
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR, exist_ok=True)


def save_result(query, text, data):
    """保存结果到文件"""
    ensure_output_dir()
    safe_query = re.sub(r'[^\w\u4e00-\u9fff]', '_', query)[:50]

    txt_file = os.path.join(OUTPUT_DIR, f"{PREFIX}{safe_query}.txt")
    with open(txt_file, 'w', encoding='utf-8') as f:
        f.write(text)

    json_file = os.path.join(OUTPUT_DIR, f"{PREFIX}{safe_query}.json")
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    return txt_file, json_file


def make_request(method, params=None):
    """发送 POST 请求到品氪 OpenAPI

    品氪 OpenAPI 统一使用表单方式提交：
    - method: API 接口名称
    - appid: 商户 appid
    - data:  请求数据实体 (JSON 格式字符串)
    - v:     API 协议版本，默认为 1
    """
    url = PK_API_URL
    form_data = {
        'method': method,
        'appid': PK_APPKEY,
        'data': json.dumps(params or {}, ensure_ascii=False),
        'v': '1'
    }

    try:
        response = requests.post(url, data=form_data, timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"请求失败: {str(e)}")
        return None


def is_success(data):
    """判断响应是否成功"""
    code = str(data.get('code', ''))
    return code in ['200', '1']


def format_error(data):
    """格式化错误信息"""
    code = data.get('code', '未知')
    message = data.get('message', '未知错误')
    return f"[{code}] {message}"


# ============================================================
# 响应格式化函数
# ============================================================

def format_common(data, action_name):
    """通用格式化（适用于上传类接口）"""
    if not is_success(data):
        return f"{action_name}失败: {format_error(data)}", data
    result = f"{action_name}成功\n"
    if data.get('data'):
        result += f"返回数据: {json.dumps(data['data'], ensure_ascii=False, indent=2)}\n"
    return result, data


def format_member_info(data):
    """格式化会员信息"""
    if not is_success(data):
        return f"查询失败: {format_error(data)}", data

    d = data.get('data', {})
    if not d:
        return "未找到会员信息", data

    result = "会员信息\n"
    result += "=" * 60 + "\n"
    result += f"  卡号:       {d.get('card_no', '-')}\n"
    result += f"  姓名:       {d.get('customer_name', '-')}\n"
    result += f"  手机号:     {d.get('phone', '-')}\n"
    result += f"  余额:       {d.get('remaining_amount', '-')}\n"
    result += f"  积分:       {d.get('remaining_bonus', '-')}\n"
    result += f"  开卡门店:   {d.get('open_card_store_no', '-')}\n"
    result += f"  开卡时间:   {d.get('open_card_time', '-')}\n"
    result += f"  绑定导购:   {d.get('bind_guide_no', '-')}\n"
    result += f"  关注状态:   {'已关注' if d.get('is_followed', -1) != -1 else '未关注'}\n"
    result += "=" * 60 + "\n"
    return result, data


def format_pinkr_member_list(data):
    """格式化品氪会员列表"""
    if not is_success(data):
        return f"查询失败: {format_error(data)}", data

    resp_data = data.get('data', {})
    members = resp_data.get('data', [])
    total = resp_data.get('total', 0)
    current_page = resp_data.get('current_page', 1)

    result = f"品氪会员列表 (第{current_page}页，共{total}条)\n"
    result += "=" * 80 + "\n"
    result += f"{'卡号':<18} {'姓名':<10} {'ERP卡号':<14} {'开卡门店':<10} {'是否激活'}\n"
    result += "-" * 80 + "\n"

    for m in members:
        card_no = m.get('pinkr_card_no', '-')
        name = m.get('customer_name', '-')
        erp = m.get('erp_card_no', '-')
        store = m.get('open_card_store_no', '-')
        active = '是' if m.get('is_import_active', 0) == 1 else '否'
        result += f"{card_no:<18} {name:<10} {erp:<14} {store:<10} {active}\n"

    result += "=" * 80 + "\n"
    result += f"共 {len(members)} 条记录\n"
    return result, data


def format_order_list(data):
    """格式化订单列表"""
    if not is_success(data):
        return f"查询失败: {format_error(data)}", data

    resp_data = data.get('data', {})
    orders = resp_data.get('data', [])
    total = resp_data.get('total', 0)

    result = f"订单列表 (共{total}条)\n"
    result += "=" * 100 + "\n"
    result += f"{'订单号':<18} {'会员卡号':<14} {'金额':<10} {'实付':<10} {'状态':<8} {'物流':<8} {'下单时间'}\n"
    result += "-" * 100 + "\n"

    status_map = {'-2': '已拆单', '1': '待发货', '2': '待付款', '4': '已发货'}

    for o in orders:
        order_no = o.get('order_no', '-')
        card = o.get('crm_card_no', '-')
        money = o.get('order_money', '-')
        fact = o.get('order_fact_money', '-')
        status = status_map.get(str(o.get('order_status', '')), str(o.get('order_status', '-')))
        express = o.get('express_name', '-') or '自提'
        order_time = o.get('order_time', '-')
        result += f"{order_no:<18} {card:<14} {str(money):<10} {str(fact):<10} {status:<8} {str(express):<8} {order_time}\n"

    result += "=" * 100 + "\n"
    result += f"共 {len(orders)} 条记录\n"
    return result, data


def format_order_goods(data):
    """格式化订单商品明细"""
    if not is_success(data):
        return f"查询失败: {format_error(data)}", data

    resp_data = data.get('data', {})
    order_no = resp_data.get('order_no', '-')
    goods_list = resp_data.get('order_goods', [])

    result = f"订单商品明细 (订单号: {order_no})\n"
    result += "=" * 90 + "\n"
    result += f"{'商品编号':<12} {'商品名称':<16} {'颜色':<8} {'尺码':<8} {'数量':<6} {'吊牌价':<8} {'实付金额'}\n"
    result += "-" * 90 + "\n"

    for g in goods_list:
        result += f"{g.get('goods_sn', '-'):<12} {g.get('goods_name', '-'):<16} " \
                  f"{g.get('color_code', '-'):<8} {g.get('size_code', '-'):<8} " \
                  f"{g.get('number', 0):<6} {g.get('goods_tag_price', 0):<8} {g.get('goods_fact_money', 0)}\n"

    result += "=" * 90 + "\n"
    return result, data


def format_refund_list(data):
    """格式化退单列表"""
    if not is_success(data):
        return f"查询失败: {format_error(data)}", data

    resp_data = data.get('data', {})
    refunds = resp_data.get('data', [])
    total = resp_data.get('total', 0)

    refund_status_map = {
        0: '申请退货', 1: '同意退货', 2: '关闭退货',
        3: '商家验收', 4: '卖家寄出', 5: '确认收货',
        6: '确认退款'
    }

    result = f"退单列表 (共{total}条)\n"
    result += "=" * 90 + "\n"
    result += f"{'退单号':<16} {'原订单号':<16} {'类型':<8} {'金额':<10} {'状态':<10} {'创建时间'}\n"
    result += "-" * 90 + "\n"

    for r in refunds:
        refund_no = r.get('refund_no', r.get('return_no', '-'))
        order_no = r.get('order_no', '-')
        refund_type = r.get('refund_type', r.get('return_type', '-'))
        money = r.get('refund_money', '-')
        status = refund_status_map.get(r.get('refund_status', 0), str(r.get('refund_status', '-')))
        created = r.get('created_at', '-')
        result += f"{refund_no:<16} {order_no:<16} {str(refund_type):<8} {str(money):<10} {status:<10} {created}\n"

    result += "=" * 90 + "\n"
    result += f"共 {len(refunds)} 条记录\n"
    return result, data


def format_storage_list(data):
    """格式化仓库列表"""
    if not is_success(data):
        return f"查询失败: {format_error(data)}", data

    resp_data = data.get('data', {})
    items = resp_data.get('data', resp_data) if isinstance(resp_data, dict) else resp_data
    if not isinstance(items, list):
        items = [resp_data] if resp_data else []

    result = "仓库清单\n"
    result += "=" * 40 + "\n"
    for s in items:
        result += f"  {s.get('storage_code', '-')} - {s.get('storage_name', '-')}\n"
    result += "=" * 40 + "\n"
    result += f"共 {len(items)} 个仓库\n"
    return result, data


def format_goods_list(data):
    """格式化商品列表"""
    if not is_success(data):
        return f"查询失败: {format_error(data)}", data

    resp_data = data.get('data', {})
    items = resp_data.get('data', resp_data) if isinstance(resp_data, dict) else resp_data
    if not isinstance(items, list):
        items = [resp_data] if resp_data else []

    result = "商品清单\n"
    result += "=" * 70 + "\n"
    result += f"{'商品代码':<14} {'商品名称':<20} {'SKU数量'}\n"
    result += "-" * 70 + "\n"

    for g in items:
        goods_sn = g.get('goods_sn', '-')
        goods_name = g.get('goods_name', '-')
        skus = g.get('skus', [])
        result += f"{goods_sn:<14} {goods_name:<20} {len(skus)}\n"

    result += "=" * 70 + "\n"
    result += f"共 {len(items)} 个商品\n"
    return result, data


def format_stock_list(data):
    """格式化库存列表"""
    if not is_success(data):
        return f"查询失败: {format_error(data)}", data

    resp_data = data.get('data', {})
    items = resp_data.get('data', resp_data) if isinstance(resp_data, dict) else resp_data
    if not isinstance(items, list):
        items = [resp_data] if resp_data else []

    result = "商品库存\n"
    result += "=" * 70 + "\n"
    result += f"{'商品款号':<14} {'颜色':<8} {'尺码':<8} {'仓库':<10} {'库存'}\n"
    result += "-" * 70 + "\n"

    for s in items:
        result += f"{s.get('goods_sn', '-'):<14} {s.get('color_code', '-'):<8} " \
                  f"{s.get('size_code', '-'):<8} {s.get('warehouse_code', s.get('storage_code', '-')):<10} " \
                  f"{s.get('stock_number', 0)}\n"

    result += "=" * 70 + "\n"
    result += f"共 {len(items)} 条记录\n"
    return result, data


def format_member_count(data):
    """格式化会员统计"""
    if not is_success(data):
        return f"查询失败: {format_error(data)}", data

    d = data.get('data', {})
    result = "会员统计数据\n"
    result += "=" * 40 + "\n"
    result += f"  总会员数:     {d.get('customer_count', 0)}\n"
    result += f"  关注会员数:   {d.get('followed_customer_count', 0)}\n"
    result += f"  开卡会员数:   {d.get('opened_card_customer_count', 0)}\n"
    result += f"  绑定会员数:   {d.get('bind_customer_count', 0)}\n"
    result += f"  消费会员数:   {d.get('consumed_customer_count', 0)}\n"
    result += f"  ERP激活数:    {d.get('from_erp_customer_count', 0)}\n"
    result += "=" * 40 + "\n"
    return result, data


def format_distribution_orders(data):
    """格式化分销订单"""
    if not is_success(data):
        return f"查询失败: {format_error(data)}", data

    resp_data = data.get('data', {})
    items = resp_data.get('data', [])
    total = resp_data.get('total', 0)

    status_map = {0: '冻结期', -1: '不结算(全额退款)', -2: '不结算(仅退款)',
                  1: '待结算', 2: '已结算', 3: '不分佣'}

    result = f"分销订单 (共{total}条)\n"
    result += "=" * 80 + "\n"
    result += f"{'订单号':<18} {'类型':<6} {'状态':<12} {'佣金比例':<8} {'收益':<10} {'订单金额'}\n"
    result += "-" * 80 + "\n"

    for o in items:
        order_no = o.get('order_no', '-')
        otype = o.get('type', '-')
        status = status_map.get(o.get('distribute_status', ''), str(o.get('distribute_status', '-')))
        ratio = o.get('distribute_ratio', '-')
        price = o.get('distribute_price', '-')
        money = o.get('order_money', '-')
        result += f"{order_no:<18} {str(otype):<6} {status:<12} {str(ratio):<8} {str(price):<10} {str(money)}\n"

    result += "=" * 80 + "\n"
    result += f"共 {len(items)} 条记录\n"
    return result, data


def format_tag_list(data):
    """格式化标签列表"""
    if not is_success(data):
        return f"查询失败: {format_error(data)}", data

    resp_data = data.get('data', {})
    items = resp_data.get('data', resp_data) if isinstance(resp_data, dict) else resp_data
    if not isinstance(items, list):
        items = [resp_data] if resp_data else []

    result = "标签列表\n"
    result += "=" * 40 + "\n"
    for t in items:
        cat = t.get('category_name', '')
        tag = t.get('tag_name', '')
        if cat:
            result += f"  [{cat}] {tag}\n"
        else:
            result += f"  {tag}\n"
    result += "=" * 40 + "\n"
    return result, data


def format_express_list(data):
    """格式化快递列表"""
    if not is_success(data):
        return f"查询失败: {format_error(data)}", data

    resp_data = data.get('data', {})
    items = resp_data.get('data', resp_data) if isinstance(resp_data, dict) else resp_data
    if not isinstance(items, list):
        items = [resp_data] if resp_data else []

    result = "支持的快递列表\n"
    result += "=" * 40 + "\n"
    for e in items:
        result += f"  {e.get('express_code', '-'):<10} {e.get('express_name', '-')}\n"
    result += "=" * 40 + "\n"
    result += f"共 {len(items)} 家快递公司\n"
    return result, data


# ============================================================
# 意图识别与参数解析
# ============================================================

# 意图关键词映射 (关键词 -> (method, formatter_name))
INTENT_MAP = {
    # 快递
    '快递': ('common.express.get', 'format_express_list'),

    # 门店
    '门店': ('store.upload', 'format_common'),

    # 导购
    '导购': ('guide.upload', 'format_common'),

    # 标签
    '标签分类': ('tag.category.upload', 'format_common'),
    '标签': ('tag.tag.upload', 'format_common'),
    '会员标签': ('tag.memberTag.upload', 'format_common'),
    '获取标签': ('tag.tag.get', 'format_tag_list'),

    # 订单
    '订单列表': ('order.order.get', 'format_order_list'),
    '订单商品': ('order.orderGoods.get', 'format_order_goods'),
    '发货': ('order.delivery.update', 'format_common'),
    '新增订单': ('order.order.add', 'format_common'),
    '订单仓库状态': ('order.storage.updateStatus', 'format_common'),

    # 退单
    '退货退款': ('refund.returnRefund.get', 'format_refund_list'),
    '退货状态': ('refund.returnRefund.status.update', 'format_common'),
    '退款单': ('refund.refund.get', 'format_refund_list'),
    '退款状态': ('refund.status.update', 'format_common'),
    '新增退货': ('refund.returnRefund.add', 'format_common'),

    # 库存
    '仓库清单': ('stock.storageList.get', 'format_storage_list'),
    '商品清单': ('stock.goodsList.get', 'format_goods_list'),
    '更新库存': ('stock.goodsStock.batchUpdate', 'format_common'),
    '获取库存': ('warehouse.goodsStock.get', 'format_stock_list'),

    # 商品
    '商品尺码': ('goods.size.upload', 'format_common'),
    '商品颜色': ('goods.color.upload', 'format_common'),
    '商品父属性': ('goods.attributeName.upload', 'format_common'),
    '商品子属性': ('goods.attributeValue.upload', 'format_common'),
    '上传商品': ('goods.goods.upload', 'format_common'),
    '商品价格': ('goods.price.upload', 'format_common'),
    '全量上传商品': ('goods.goods.fullUpload', 'format_common'),

    # 会员
    '会员信息': ('member.info.get', 'format_member_info'),
    '会员等级': ('member.level.update', 'format_common'),
    '更新会员': ('member.info.update', 'format_common'),
    '新增会员': ('member.add', 'format_common'),
    '品氪会员': ('pinkrMember.info.get', 'format_pinkr_member_list'),
    '收货地址': ('member.address.add', 'format_common'),

    # 积分
    '积分流水': ('integral.add', 'format_common'),

    # 储值
    '储值流水': ('deposit.add', 'format_common'),
    '储值卡绑定': ('deposit.card.bind', 'format_common'),

    # 卡券
    '核销卡券': ('coupon.status.batchUse', 'format_common'),

    # 销售
    '小票': ('sale.order.add', 'format_common'),

    # 营销数据
    '会员统计': ('data.member.count', 'format_member_count'),
    '目标管理': ('data.target.get', 'format_common'),
    '分组资料': ('data.member.group.groupInfo.get', 'format_common'),
    '分组类型': ('data.member.group.config.get', 'format_common'),
    '分组会员': ('data.member.group.get', 'format_common'),
    '标签资料': ('data.Tag.get', 'format_tag_list'),
    '标签会员': ('data.Tag.Member.get', 'format_common'),

    # 分销
    '分销订单': ('distribution.paidOrder.get', 'format_distribution_orders'),
}


def parse_query(query):
    """解析自然语言查询，识别意图和提取参数"""
    query_lower = query.lower()
    params = {}

    # ---- 查询类（优先匹配） ----

    # 快递列表
    if any(w in query for w in ['快递列表', '快递公司', '获取快递']):
        return 'common.express.get', None, 'format_express_list'

    # 获取标签资料
    if any(w in query for w in ['获取标签资料', '标签基础资料', '获取标签']):
        return 'tag.tag.get', None, 'format_tag_list'

    # 仓库清单
    if any(w in query for w in ['仓库清单', '仓库列表', '同步仓库']):
        return 'stock.storageList.get', None, 'format_storage_list'

    # 商品清单（库存同步）
    if any(w in query for w in ['商品清单', '同步商品清单', '商品列表']):
        return 'stock.goodsList.get', None, 'format_goods_list'

    # 获取库存
    if any(w in query for w in ['获取库存', '查询库存', '库存查询']):
        p = {}
        m = re.search(r'款号\s*(\S+)', query)
        if m:
            p['goods_sn'] = m.group(1)
        m = re.search(r'仓库\s*(\S+)', query)
        if m:
            p['storage_code'] = m.group(1)
        return 'warehouse.goodsStock.get', p or None, 'format_stock_list'

    # 会员信息查询
    if any(w in query for w in ['查询会员', '获取会员', '会员查询', '查看会员']) and '品氪' not in query:
        p = {}
        m = re.search(r'卡号\s*(\S+)', query)
        if m:
            p['card_no'] = m.group(1)
        m = re.search(r'手机\s*(\d{11})', query)
        if m:
            p['mobile'] = m.group(1)
        if not p:
            m = re.search(r'(\d{11})', query)
            if m:
                p['mobile'] = m.group(1)
        return 'member.info.get', p or None, 'format_member_info'

    # 品氪会员列表
    if any(w in query for w in ['品氪会员', '会员列表']):
        p = {}
        m = re.search(r'更新时间.*?(\d{4}-\d{2}-\d{2})', query)
        if m:
            p['update_time_start'] = m.group(1) + ' 00:00:00'
        return 'pinkrMember.info.get', p or None, 'format_pinkr_member_list'

    # 订单列表
    if any(w in query for w in ['订单列表', '查询订单', '获取订单', '我的订单']):
        p = {}
        m = re.search(r'订单状态\s*(\S+)', query)
        if m:
            p['order_status'] = m.group(1)
        m = re.search(r'订单号\s*(\S+)', query)
        if m:
            p['order_nos'] = m.group(1)
        return 'order.order.get', p or None, 'format_order_list'

    # 订单商品明细
    if any(w in query for w in ['订单商品', '商品明细', '订单详情']):
        m = re.search(r'订单号\s*(\S+)', query)
        if not m:
            m = re.search(r'(\w{10,})', query)
        p = {'order_no': m.group(1)} if m else {}
        return 'order.orderGoods.get', p, 'format_order_goods'

    # 退货退款单
    if any(w in query for w in ['退货退款', '退货单', '退货列表']):
        return 'refund.returnRefund.get', None, 'format_refund_list'

    # 退款单
    if any(w in query for w in ['退款单', '退款列表', '仅退款']):
        return 'refund.refund.get', None, 'format_refund_list'

    # 会员统计
    if any(w in query for w in ['会员统计', '会员数据', '会员概况']):
        return 'data.member.count', None, 'format_member_count'

    # 分销订单
    if any(w in query for w in ['分销订单', '付费订单', '分销列表']):
        p = {}
        m = re.search(r'分销状态\s*(\S+)', query)
        if m:
            p['distribute_status'] = int(m.group(1))
        return 'distribution.paidOrder.get', p or None, 'format_distribution_orders'

    # 目标管理
    if any(w in query for w in ['目标管理', '销售目标', '开卡目标']):
        return 'data.target.get', {'target_type': 1, 'page': 1}, 'format_common'

    # 分组资料
    if any(w in query for w in ['分组资料', '会员分组', '分组信息']):
        return 'data.member.group.groupInfo.get', {'type': 0}, 'format_common'

    # 分组类型
    if any(w in query for w in ['分组类型', '预设分组']):
        return 'data.member.group.config.get', None, 'format_common'

    # 标签资料（营销数据）
    if any(w in query for w in ['营销标签', '导购标签', '标签基础']):
        return 'data.Tag.get', {'tag_type': 'guide_tag'}, 'format_tag_list'

    # ---- 写入/上传类 ----

    # 上传门店
    if any(w in query for w in ['上传门店', '新增门店', '同步门店']):
        p = _extract_params(query, ['store_no', 'store_name', 'address', 'telephone', 'business_model'])
        return 'store.upload', p, 'format_common'

    # 上传导购
    if any(w in query for w in ['上传导购', '新增导购', '同步导购']):
        p = _extract_params(query, ['guide_no', 'guide_name', 'store_no', 'position', 'sex',
                                     'guide_status', 'phone', 'entry_date', 'birthday'])
        return 'guide.upload', p, 'format_common'

    # 上传标签分类
    if any(w in query for w in ['上传标签分类', '新增标签分类']):
        p = _extract_params(query, ['category_code', 'category_name'])
        return 'tag.category.upload', p, 'format_common'

    # 上传标签
    if any(w in query for w in ['上传标签', '新增标签']):
        p = _extract_params(query, ['category_code', 'tag_code', 'tag_name'])
        return 'tag.tag.upload', p, 'format_common'

    # 上传会员标签
    if any(w in query for w in ['上传会员标签', '更新会员标签']):
        p = _extract_params(query, ['card_no'])
        return 'tag.memberTag.upload', p, 'format_common'

    # 发货
    if any(w in query for w in ['发货', '更新发货', '确认发货']):
        p = _extract_params(query, ['order_no', 'channel_order_no', 'express_name',
                                     'express_code', 'express_no', 'is_split'])
        return 'order.delivery.update', p, 'format_common'

    # 新增订单（接收第三方）
    if any(w in query for w in ['新增订单', '接收订单', '同步订单', '创建订单']):
        return 'order.order.add', None, 'format_common'

    # 更新退货退款状态
    if any(w in query for w in ['同意退货', '确认收货', '确认退款', '关闭退货']):
        p = _extract_params(query, ['refund_no', 'refund_status'])
        if '同意退货' in query:
            p['refund_status'] = 1
        elif '关闭退货' in query:
            p['refund_status'] = 2
        elif '确认收货' in query:
            p['refund_status'] = 5
        elif '确认退款' in query:
            p['refund_status'] = 6
        return 'refund.returnRefund.status.update', p, 'format_common'

    # 同意退款
    if any(w in query for w in ['同意退款']):
        p = _extract_params(query, ['refund_no', 'refund_status'])
        p['refund_status'] = p.get('refund_status', 1)
        return 'refund.status.update', p, 'format_common'

    # 新增退货单
    if any(w in query for w in ['新增退货单', '接收退货']):
        return 'refund.returnRefund.add', None, 'format_common'

    # 更新库存
    if any(w in query for w in ['更新库存', '同步库存', '上传库存']):
        return 'stock.goodsStock.batchUpdate', None, 'format_common'

    # 上传商品尺码
    if any(w in query for w in ['上传尺码', '新增尺码', '商品尺码']):
        p = _extract_params(query, ['size_code', 'size_name', 'sort'])
        return 'goods.size.upload', p, 'format_common'

    # 上传商品颜色
    if any(w in query for w in ['上传颜色', '新增颜色', '商品颜色']):
        p = _extract_params(query, ['color_code', 'color_name'])
        return 'goods.color.upload', p, 'format_common'

    # 上传商品父属性
    if any(w in query for w in ['上传父属性', 'SPU父属性', '商品父属性']):
        p = _extract_params(query, ['attribute_name', 'attribute_name_code'])
        return 'goods.attributeName.upload', p, 'format_common'

    # 上传商品子属性
    if any(w in query for w in ['上传子属性', 'SPU子属性', '商品子属性']):
        p = _extract_params(query, ['attribute_name_code', 'attribute_value', 'attribute_value_code'])
        return 'goods.attributeValue.upload', p, 'format_common'

    # 上传商品
    if any(w in query for w in ['上传商品', '新增商品']) and '全量' not in query and '价格' not in query:
        return 'goods.goods.upload', None, 'format_common'

    # 上传商品价格
    if any(w in query for w in ['商品价格', '上传价格', '千店千面']):
        p = _extract_params(query, ['goods_sn', 'store_no', 'goods_tag_price',
                                     'mall_goods_real_price', 'goods_discount'])
        return 'goods.price.upload', p, 'format_common'

    # 全量上传商品
    if any(w in query for w in ['全量上传商品', '全量商品']):
        return 'goods.goods.fullUpload', None, 'format_common'

    # 更新会员等级
    if any(w in query for w in ['更新等级', '会员等级', '修改等级']):
        p = _extract_params(query, ['card_no', 'level_code'])
        return 'member.level.update', p, 'format_common'

    # 更新会员信息
    if any(w in query for w in ['更新会员', '修改会员']):
        p = _extract_params(query, ['card_no', 'customer_name', 'sex', 'mobile',
                                     'birthday', 'channel_card_no', 'bind_guide_no'])
        return 'member.info.update', p, 'format_common'

    # 新增会员
    if any(w in query for w in ['新增会员', '开卡', '注册会员']):
        return 'member.add', None, 'format_common'

    # 收货地址
    if any(w in query for w in ['收货地址', '新增地址']):
        p = _extract_params(query, ['card_no', 'customer_name', 'mobile',
                                     'province_name', 'city_name', 'area_name', 'address'])
        return 'member.address.add', p, 'format_common'

    # 积分流水
    if any(w in query for w in ['积分流水', '新增积分', '同步积分']):
        p = _extract_params(query, ['card_no', 'channel_card_no', 'channel_integral_no',
                                     'integral_code', 'integral', 'consume_no', 'change_time'])
        return 'integral.add', p, 'format_common'

    # 储值流水
    if any(w in query for w in ['储值流水', '新增储值', '同步储值']):
        p = _extract_params(query, ['card_no', 'channel_card_no', 'channel_deposit_no',
                                     'amount_type', 'amount', 'gift_amount', 'change_time'])
        return 'deposit.add', p, 'format_common'

    # 储值卡绑定
    if any(w in query for w in ['储值卡绑定', '绑定储值卡']):
        p = _extract_params(query, ['card_no', 'deposited_card_no', 'store_no'])
        return 'deposit.card.bind', p, 'format_common'

    # 核销卡券
    if any(w in query for w in ['核销卡券', '核销优惠券', '使用卡券']):
        m = re.findall(r'(\w+)', query)
        coupon_codes = [c for c in m if len(c) > 5]
        return 'coupon.status.batchUse', {'coupon_codes': coupon_codes}, 'format_common'

    # 小票
    if any(w in query for w in ['小票', '同步小票', '上传小票']):
        return 'sale.order.add', None, 'format_common'

    # 订单仓库状态
    if any(w in query for w in ['仓库状态', '转单']):
        p = _extract_params(query, ['order_no', 'status'])
        return 'order.storage.updateStatus', p, 'format_common'

    # 默认：显示帮助
    return None, None, None


def _extract_params(query, fields):
    """从查询文本中提取键值对参数

    支持格式: key=value, key:value, key=value1,value2
    """
    params = {}
    for field in fields:
        patterns = [
            rf'{field}\s*[=：:]\s*([^\s,，]+)',
            rf'{field}\s+([^\s,，]+)',
        ]
        for pattern in patterns:
            m = re.search(pattern, query, re.IGNORECASE)
            if m:
                val = m.group(1)
                # 数值类型转换
                if val.isdigit():
                    val = int(val)
                else:
                    try:
                        val = float(val)
                    except ValueError:
                        pass
                params[field] = val
                break
    return params


# ============================================================
# 主函数
# ============================================================

def print_help():
    """打印帮助信息"""
    help_text = """
品氪 OpenApi 开放平台 Skill - 使用说明
==========================================

用法: python pinkr_openapi_skill.py <操作描述>

支持的操作:
  查询类:
    查询会员 卡号=xxx / 手机=xxx     获取会员信息
    品氪会员                         获取品氪会员列表
    会员统计                         获取会员统计数据
    订单列表 [订单状态=1]             获取订单列表
    订单商品 订单号=xxx              获取订单商品明细
    退货退款 / 退款单                获取退单列表
    快递列表                         获取快递公司列表
    仓库清单                         获取仓库清单
    商品清单                         获取商品清单
    获取库存 [款号=xxx]              获取商品库存
    获取标签                         获取标签资料
    分销订单                         获取分销订单
    目标管理                         获取目标管理
    分组资料 / 分组类型              获取会员分组信息
    营销标签                         获取营销标签资料

  写入类:
    上传门店 store_no=xxx store_name=xxx
    上传导购 guide_no=xxx guide_name=xxx store_no=xxx
    发货 order_no=xxx express_name=xxx express_code=xxx express_no=xxx
    同意退货 refund_no=xxx
    确认收货 refund_no=xxx
    同意退款 refund_no=xxx
    上传商品尺码 size_code=xxx size_name=xxx
    上传商品颜色 color_code=xxx color_name=xxx
    上传商品 (需JSON参数)
    更新库存 (需JSON参数)
    积分流水 card_no=xxx integral_code=xxx integral=100
    储值流水 card_no=xxx amount_type=0 amount=100
    核销卡券 coupon_code1,coupon_code2
    小票 (需JSON参数)
    更新会员 card_no=xxx
    更新等级 card_no=xxx level_code=xxx
    新增会员 (需JSON参数)
    收货地址 card_no=xxx customer_name=xxx mobile=xxx

  环境变量:
    PK_APPKEY    品氪开放平台分配的 APPKEY
    PK_API_URL   API 基础地址 (默认: http://dev.openapi.pinkr.com)
"""
    print(help_text)


def main():
    """主函数"""
    if not check_appkey():
        sys.exit(1)

    # 获取查询文本
    query = ' '.join(sys.argv[1:]) if len(sys.argv) > 1 else ''

    if not query or query in ('help', '--help', '-h', '帮助'):
        print_help()
        sys.exit(0)

    # 解析意图
    method, params, formatter_name = parse_query(query)

    if not method:
        print(f"无法识别的操作: {query}")
        print("使用 --help 查看支持的操作列表")
        sys.exit(1)

    # 发送请求
    data = make_request(method, params)
    if data is None:
        sys.exit(1)

    # 格式化输出
    formatter = globals().get(formatter_name, format_common)
    action_name = query[:30]
    if formatter == format_common:
        result_text, _ = formatter(data, action_name)
    else:
        result_text, _ = formatter(data)

    print(result_text)
    save_result(query, result_text, data)


if __name__ == '__main__':
    main()
