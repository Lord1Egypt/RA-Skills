#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
order_api.py — 小递查查「在线下单」接口层

对应官网页面：https://xdccy.com/send/SellerDelivery.aspx
页面 JS 里与下单相关的四个接口（已从 /dist/js/config.js 与页面内联脚本逆向得到）：

  POST /UserInfo/GetAccountBalanceInfo   账户余额（下单前判断钱够不够）
  POST /AddressLib/GetDefaultAddr        默认寄件人地址簿（免重复填写发件信息）
  POST /ToDoorOrder/GetAccessibleList    可取件时间段 + 超区校验（下单必填取件时间）
  POST /ToDoorOrder/PlaceOrder           提交订单（真正扣款）

共同约定：
  Content-Type: application/x-www-form-urlencoded
  Headers: auth = localStorage.userToken（网页登录 token）
  嵌套对象按 jQuery 的 $.param 规则序列化：Sender[ProvinceName]=广东省

统一返回值： (data, err)
  data —— 接口 Data 字段（dict / list），失败时为 None
  err  —— None 表示成功；"AUTH" 表示登录失效；其余为可读错误串
"""

import json
import random
import time
import urllib.error
import urllib.parse
import urllib.request

API_HOST = "https://api.xdccy.com"
PAGE_URL = "https://xdccy.com/send/SellerDelivery.aspx"

EP_BALANCE = "/UserInfo/GetAccountBalanceInfo"
EP_DEFAULT_ADDR = "/AddressLib/GetDefaultAddr"
EP_ACCESSIBLE = "/ToDoorOrder/GetAccessibleList"
EP_PLACE_ORDER = "/ToDoorOrder/PlaceOrder"
EP_FREIGHT = "/ToDoorOrder/GetFreightPredictList"
EP_ADDRESS_ANALYSIS = "/ToDoorOrder/AddressAnalysis"

# 寄件管理 / 工单（对应 https://xdccy.com/send/DeliveryManage.aspx 与根目录下的
# /AddWorkOrder.html、/WorkOrderManage.html，接口名取自 /dist/js/config.js?v=19881）
EP_SEARCH_ORDER_LIST = "/ToDoorOrder/SearchOrderList"
EP_ORDER_DETAIL = "/ToDoorOrder/GetOrderDetail"
EP_CANCEL_ORDER = "/ToDoorOrder/CancelOrder"
EP_WORK_ORDER_LIST = "/ToDoorOrder/GetWorkOrderList"
EP_WORK_ORDER_DETAIL = "/ToDoorOrder/GetWorkOrderDetail"
EP_WORK_ORDER_CATEGORY = "/ToDoorOrder/GetWorkOrderCategoryList"
EP_WORK_ORDER_ADD = "/ToDoorOrder/AddWorkOrder"
EP_WAYBILL_INTERCEPT = "/ToDoorOrder/WaybillIntercept"

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0 Safari/537.36")

# 支付类型（页面 GoBuy 里写死 PayType=1，注释说明了取值含义）
PAY_TYPES = {
    1: "现付（余额支付）",
    2: "到付",
    3: "月结",
    4: "第三方付",
}
DEFAULT_PAY_TYPE = 1

# 快递公司别名 → 接口实际编码。
# 接口的 ShipperCode 未必是常见缩写（顺丰是 shunfeng 而非 SF，申通是 shentong 而非 STO），
# 客户口头说的是「顺丰」「圆通」，所以这里做一层归一化，免得必须背编码。
SHIPPER_ALIASES = {
    "jt": "jtexpress", "jtexpress": "jtexpress", "极兔": "jtexpress",
    "极兔快递": "jtexpress",
    "yto": "yuantong", "yuantong": "yuantong", "圆通": "yuantong",
    "圆通速递": "yuantong",
    "yd": "yunda", "yunda": "yunda", "韵达": "yunda", "韵达快递": "yunda",
    "sto": "shentong", "shentong": "shentong", "申通": "shentong",
    "申通快递": "shentong",
    "sf": "shunfeng", "shunfeng": "shunfeng", "顺丰": "shunfeng",
    "顺丰速递": "shunfeng", "顺丰速运": "shunfeng",
    "jd": "jd", "京东": "jd", "京东快递": "jd",
    "zhiixuan": "kuaidi100zhixuan", "zhixuan": "kuaidi100zhixuan",
    "智选": "kuaidi100zhixuan", "小递智选": "kuaidi100zhixuan",
    "快递100智选": "kuaidi100zhixuan",
    "zto": "zto", "中通": "zto", "中通快递": "zto",
    "ems": "ems", "邮政": "ems", "邮政快递": "ems", "中国邮政": "ems",
    "htky": "huitongkuaidi", "汇通": "huitongkuaidi", "百世": "huitongkuaidi",
}


def match_shipper(rows, want):
    """按「编码 / 别名 / 中文名」在报价结果里找渠道。

    兼容三種写法：接口编码（shunfeng）、通用缩写（SF）、中文名（顺丰）。
    返回 (item, err)；找不到时 item 为 None（由调用方列出可选渠道）。
    """
    if not want:
        return None, None
    w = str(want).strip().lower()
    code = SHIPPER_ALIASES.get(w, w)
    for r in rows:                                    # 1) 编码精确匹配
        if (r.get("shipper_code") or "").lower() == code:
            return r, None
    for r in rows:                                    # 2) 中文名包含
        if w and w in (r.get("shipper_name") or "").lower():
            return r, None
    for r in rows:                                    # 3) 编码互相包含
        c = (r.get("shipper_code") or "").lower()
        if c and (c in w or w in c):
            return r, None
    return None, None


# --------------------------------------------------------------------------- #
# 底层请求
# --------------------------------------------------------------------------- #
def post_form(token, path, payload, timeout=30):
    """向 xdccy 接口 POST 表单。

    payload 支持嵌套 dict（会被 flatten 成 a[b] 形式）。
    返回 (data, err)：err 为 None 表示 Code==200。
    """
    url = API_HOST + path
    body = urllib.parse.urlencode(flatten(payload)).encode("utf-8")
    req = urllib.request.Request(url, data=body, method="POST", headers={
        "Content-Type": "application/x-www-form-urlencoded",
        "auth": token or "",
        "User-Agent": UA,
        "Referer": PAGE_URL,
        "Origin": "https://xdccy.com",
    })
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            text = r.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as e:
        if e.code == 401:
            return None, "AUTH"
        try:
            detail = e.read().decode("utf-8", errors="replace")[:300]
        except Exception:
            detail = ""
        return None, f"HTTP {e.code}：{detail}"
    except urllib.error.URLError as e:
        return None, f"网络异常：{e.reason}"
    except Exception as e:  # pragma: no cover
        return None, f"请求异常：{e}"

    try:
        res = json.loads(text)
    except ValueError:
        return None, f"响应不是 JSON：{text[:200]}"
    if str(res.get("Code")) != "200":
        # 页面失败分支优先展示 DebugMsg，其次 Message
        msg = res.get("DebugMsg") or res.get("Message") or "未知原因"
        return None, f"接口返回 Code={res.get('Code')}：{msg}"
    return res.get("Data"), None


def flatten(payload, prefix=""):
    """把嵌套 dict 压成 jQuery $.param 风格的扁平键。

    {"Sender": {"Name": "张三"}} → {"Sender[Name]": "张三"}
    bool → "true"/"false"（jQuery 的行为）；None 会被跳过。
    """
    out = {}
    for k, v in (payload or {}).items():
        key = f"{prefix}[{k}]" if prefix else str(k)
        if isinstance(v, dict):
            out.update(flatten(v, key))
        elif isinstance(v, bool):
            out[key] = "true" if v else "false"
        elif v is None:
            continue
        else:
            out[key] = str(v)
    return out


# --------------------------------------------------------------------------- #
# 各接口封装
# --------------------------------------------------------------------------- #
def get_balance(token, timeout=30):
    """账户余额。返回 (data_dict, err)。data 关键字段：
    AvailableAmount 可用余额 / TotalAmount 总额 / OrderProductType 产品类型。
    """
    return post_form(token, EP_BALANCE, {}, timeout)


def get_default_addr(token, timeout=30):
    """默认寄件人地址。返回 (data_dict, err)。字段：FullName/MobilePhone/Province/City/Area/Address。"""
    return post_form(token, EP_DEFAULT_ADDR, {}, timeout)


def get_accessible_list(token, sender, receiver, shipper_code, timeout=30):
    """可取件时间段（兼超区校验）。

    sender/receiver 为 region.resolve() 的结果（province/city/area）。
    返回 (slots, err)，slots 为 [{"StartTime":..., "EndTime":..., "EndFetchTime":...}, ...]。
    接口两种返回形态都要兼容：Data 直接是数组，或 Data.BookableTime 是数组。
    """
    payload = {
        "ShipperType": "2",          # 页面 OrderingTime 里写死 2（标快）
        "Receiver[ProvinceName]": receiver["province"],
        "Receiver[CityName]": receiver["city"],
        "Receiver[ExpAreaName]": receiver["area"],
        "Receiver[Address]": "-",    # 页面这里传固定 "-"，不传真实地址
        "Sender[ProvinceName]": sender["province"],
        "Sender[CityName]": sender["city"],
        "Sender[ExpAreaName]": sender["area"],
        "Sender[Address]": "-",
        "ShipperCode": shipper_code,
    }
    data, err = post_form(token, EP_ACCESSIBLE, payload, timeout)
    if err:
        return None, err
    if isinstance(data, dict):
        raw = data.get("BookableTime")
        if raw is None:
            raw = data.get("Data")
    else:
        raw = data
    slots = []
    for it in (raw or []):
        if not isinstance(it, dict):
            continue
        slots.append({
            "start": (it.get("StartTime") or "").strip(),
            "end": (it.get("EndTime") or "").strip(),
            "end_fetch": (it.get("EndFetchTime") or "").strip(),
        })
    return slots, None


def place_order(token, payload, timeout=30):
    """提交订单（真实扣款）。payload 为 build_order_payload() 的产物。"""
    return post_form(token, EP_PLACE_ORDER, payload, timeout)


def analysis_address(token, text, timeout=30):
    """地址识别：把一整段「姓名+电话+地址」拆成结构化字段。

    对应官网 https://xdccy.com/send/AddrRecognition.html 的 AddrRecognitionV2()，
    接口就是同一个。请求只有一个参数 Content（用户粘贴的原始文本）。

    成功返回 (fields, err)；fields 含
      name / phone / province / city / area / street / address / full_address
    其中 full_address = StreetName + Address（与页面拼接方式一致）。

    空文本直接本地返回，不发请求：接口对空串会返回 Code=500。
    """
    if not text or not text.strip():
        return None, "输入为空"
    data, err = post_form(token, EP_ADDRESS_ANALYSIS, {"Content": text}, timeout)
    if err:
        return None, err
    return normalize_analysis(data), None


def normalize_analysis(data):
    """把 AddressAnalysis 的返回规整成统一字段。

    页面里的两段逻辑都要照顾到：
      1. 直辖市的 ProvinceName 可能返回裸名（"北京"），页面此时补一个「市」；
      2. 直筒子市（如东莞）没有区县，ExpAreaName 会回落成 CityName。
    """
    get = lambda k: (data.get(k) or "").strip()
    province = get("ProvinceName")
    if province in ("北京", "天津", "上海", "重庆") and not province.endswith("市"):
        province += "市"
    street = get("StreetName")
    address = get("Address")
    return {
        "name": get("Name"),
        "phone": get("Mobile"),
        "province": province,
        "city": get("CityName"),
        "area": get("ExpAreaName"),
        "street": street,
        "address": address,
        "full_address": (street + address).strip(),
    }


# --------------------------------------------------------------------------- #
# 参数构造
# --------------------------------------------------------------------------- #
def gen_platform_order_code():
    """生成平台订单号：与页面 orderCode() 完全一致 —— 'KDN' + 毫秒时间戳 + 6 位随机数。"""
    rnd = "".join(str(random.randint(0, 9)) for _ in range(6))
    return f"KDN{int(time.time() * 1000)}{rnd}"


def build_party(region_dict, name, phone):
    """构造收/寄件人参数块。

    手机号判定与页面一致：11 位且不含 '-' 走 Mobile，否则走 Tel（座机/带分机号）。
    """
    party = {
        "ProvinceName": region_dict["province"],
        "CityName": region_dict["city"],
        "ExpAreaName": region_dict["area"],
        "Address": (region_dict.get("address") or "").strip(),
        "Name": (name or "").strip(),
    }
    p = (phone or "").strip()
    if len(p) == 11 and "-" not in p:
        party["Mobile"] = p
    else:
        party["Tel"] = p
    return party


def build_order_payload(sender_region, receiver_region,
                        sender_name, sender_phone,
                        receiver_name, receiver_phone,
                        shipper_code, weight, pay_amount,
                        goods_name, start_date, end_date,
                        quantity=1, pay_type=DEFAULT_PAY_TYPE,
                        remark="", platform_order_code=None,
                        save_sender=False, save_receiver=False):
    """构造 PlaceOrder 的完整请求体（字段与页面 GoBuy() 一一对应）。"""
    return {
        "PlatFormOrderCode": platform_order_code or gen_platform_order_code(),
        "ShipperCode": shipper_code,
        "Quantity": quantity,
        "PayType": pay_type,
        "PayAmount": pay_amount,
        "Weight": weight,
        "Sender": build_party(sender_region, sender_name, sender_phone),
        "Receiver": build_party(receiver_region, receiver_name, receiver_phone),
        "StartDate": start_date,
        "EndDate": end_date,
        "GoodsName": goods_name,
        "Remark": remark or "",
        "SaveSender": bool(save_sender),
        "SaveReceiver": bool(save_receiver),
    }


# --------------------------------------------------------------------------- #
# 状态字典
#
# 数字码的中文含义写在页面内联脚本里（DeliveryManage.aspx 的 parseData），
# 接口本身只返回数字，所以这里照抄一份，列表才读得懂。
# --------------------------------------------------------------------------- #
ORDER_STATUS = {
    1: "下单成功", 2: "分配网点", 3: "分配快递员", 4: "已取件", 5: "已揽件",
    6: "已取消", 7: "在途中", 8: "已签收", 9: "已赔付", 10: "下单失败",
}
LOGISTICS_STATUS = {1: "待揽件", 2: "已揽件", 3: "在途中", 4: "派件中", 5: "已签收"}
PAY_STATUS = {1: "已冻结", 2: "已解冻", 3: "已扣款", 4: "已退款"}
WORK_ORDER_STATUS = {0: "待处理", 1: "已处理", 2: "已关闭"}

# 订单行操作栏（barDemo）里「取消订单」只对 OrderStatus 为这三个值显示，
#  Beyond 取件之后就取消了，接口也会拒绝。
CANCELABLE_ORDER_STATUS = (1, 2, 3)

WORK_ORDER_TYPE_NAME = {
    1: "虚假揽件", 2: "快递员服务态度差", 3: "重量/运费异常", 5: "超时揽件",
    6: "包裹破损", 8: "丢件", 10: "物流长时间未更新", 11: "轨迹签收实际未收到货",
    13: "快递员私下收费", 14: "收到后少件", 15: "包裹收到错件", 16: "其他",
    18: "更改收件信息", 19: "拦截", 20: "核实退回",
}


def fmt_order_status(code):
    """订单状态数字 → 中文。"""
    return ORDER_STATUS.get(_as_int(code), "-")


def fmt_logistics_status(order_status, logistics_status):
    """物流状态数字 → 中文。

    页面逻辑：OrderStatus 属于「已取件/已揽件及之后」（>=4 且不是 6/10）时
    才用 LogisticsStatus 映射，否则一律显示 '-'（例如刚下单还没分配快递员）。
    """
    os_ = _as_int(order_status)
    ls = _as_int(logistics_status)
    if os_ is not None and os_ >= 4 and os_ != 6 and os_ != 10:
        return LOGISTICS_STATUS.get(ls, "-")
    return "-"


def fmt_pay_status(code):
    return PAY_STATUS.get(_as_int(code), "-")


def fmt_work_order_status(code):
    return WORK_ORDER_STATUS.get(_as_int(code), "-")


def _as_int(v):
    """把 '3' / 3 / '3.0' 这类值安全转成 int；转不了返回 None。"""
    if v is None or v == "":
        return None
    try:
        n = int(float(str(v).strip()))
    except (ValueError, TypeError):
        return None
    return n


def can_cancel(order):
    """该订单是否可取消（对应页面 barDemo 里「取消订单」的显示条件）。"""
    return _as_int(order.get("OrderStatus")) in CANCELABLE_ORDER_STATUS


# --------------------------------------------------------------------------- #
# 取件时间段挑选
# --------------------------------------------------------------------------- #
def _parse_slot_time(text):
    """把 '2026-10-05 09:00:00' 解析成 time.struct_time；无法解析返回 None。"""
    s = (text or "").strip().replace("/", "-")
    for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M"):
        try:
            return time.strptime(s, fmt)
        except (ValueError, TypeError):
            continue
    return None


def pick_slot(slots, index=None, now=None):
    """从可取件时间段里挑一个。

    index  —— 1 起的序号（对应 --pickup）；不传则自动选「最早且尚未开始」的那一段。
    now    —— 用于测试注入的当前时间（struct_time 或 epoch 秒）。
    返回 (slot, err)。
    """
    if not slots:
        return None, "该渠道暂无可取件时间段（可能超出揽收范围）"
    if index is not None:
        if index < 1 or index > len(slots):
            return None, f"取件时间段序号 {index} 超出范围（共 {len(slots)} 段）"
        return slots[index - 1], None

    # 页面逻辑：上门取件产品（OrderProductType=1）提交前会再次校验所选时间是否已过期，
    # 过期就重新拉时间段。这里直接跳过已开始的时段，避免提交即失败。
    now_epoch = time.mktime(now) if isinstance(now, time.struct_time) else (
        now if now is not None else time.time())
    for s in slots:
        st = _parse_slot_time(s.get("start"))
        if st is None:
            continue
        if time.mktime(st) + 60 >= now_epoch:
            return s, None
    return slots[0], None


def fmt_slot(slot):
    """把时间段渲染成人类可读文案：今天 09:00-20:00 / 10-08 09:00-20:00。"""
    if not slot:
        return "-"
    st = _parse_slot_time(slot.get("start"))
    et = _parse_slot_time(slot.get("end"))
    if not st or not et:
        return f"{slot.get('start')} ~ {slot.get('end')}"
    # 与页面一致：按「今天/明天/后天 + 时:分-时:分」描述，超过后天直接给日期
    today0 = time.mktime(time.strptime(time.strftime("%Y-%m-%d"), "%Y-%m-%d"))
    diff = int((time.mktime(st) - today0) // 86400)
    prefix = {0: "今天", 1: "明天", 2: "后天"}.get(diff, time.strftime("%m-%d", st))
    return f"{prefix} {time.strftime('%H:%M', st)}-{time.strftime('%H:%M', et)}"


# --------------------------------------------------------------------------- #
# 寄件订单：列表 / 详情 / 取消
#
# 页面：https://xdccy.com/send/DeliveryManage.aspx
#   SearchOrderList  结果在 res.Data.ResultList（分页信息 TotalCount/TotalPage/PageSize）
#   CancelOrder      请求 { "OrderCode": "..." }，直接调就是真的取消，无预览态
# 注意：页面表格声明了 contentType: 'application/json'，但接口用表单同样能绑上
#       标量字段，本项目只用标量筛选条件，继续走 post_form 一套。
# --------------------------------------------------------------------------- #
def search_order_list(token, keyword=None, shipper_code=None, logistics_status=None,
                      order_status=None, pay_status=None, receiver_name=None,
                      receiver_mobile=None, start_time=None, end_time=None,
                      page_index=1, page_size=50, timeout=30):
    """我的寄件列表。返回 (rows, total, err)。

    ⚠️ 坑（实测）：接口**不认** PageIndex / PageSize，无论传 1 还是 200，
        都固定返回「最近 15 条」（TotalCount 仍是全量 65）。所以想看更多只能
        靠筛选条件收窄范围，别指望翻页——脚本里的一页条数只是客户端截断。
    """
    payload = {
        "PageIndex": page_index,
        "PageSize": page_size,
        "OrderCode": keyword or "",
        "LogisticsCode": keyword or "",   # 运单号也按订单号那栏输，接口会两边都查
        "ShipperCode": shipper_code or "",
        "LogisticsStatus": logistics_status if logistics_status is not None else "",
        "OrderStatus": order_status if order_status is not None else "",
        "PayStatus": pay_status if pay_status is not None else "",
        "ReceiverName": receiver_name or "",
        "ReceiverMobile": receiver_mobile or "",
        "StartTime": start_time or "",
        "EndTime": end_time or "",
    }
    data, err = post_form(token, EP_SEARCH_ORDER_LIST, payload, timeout)
    if err:
        return None, 0, err
    rows = (data or {}).get("ResultList") or []
    total = (data or {}).get("TotalCount") or 0
    return rows, total, None


def fmt_order_row(order):
    """把列表行规整成展示用的 dict。

    注意：列表接口里 Sender/Receiver 的手机号做了脱敏（131****9237），
    要拿完整号码得再调 GetOrderDetail。
    """
    receiver = order.get("Receiver") or {}
    sender = order.get("Sender") or {}
    cost = order.get("PredictCost")
    try:
        cost = float(cost) if cost not in (None, "") else 0.0
    except (TypeError, ValueError):
        cost = 0.0
    return {
        "order_code": order.get("OrderCode") or "",
        "platform_order_code": order.get("PlatFormOrderCode") or "",
        "logistics_code": order.get("LogisticsCode") or "",
        "shipper": order.get("ShipperName") or "-",
        "order_status": fmt_order_status(order.get("OrderStatus")),
        "order_status_code": _as_int(order.get("OrderStatus")),
        "logistics_status": fmt_logistics_status(order.get("OrderStatus"),
                                                order.get("LogisticsStatus")),
        "pay_status": fmt_pay_status(order.get("PayStatus")),
        "predict_cost": cost,
        "receiver": receiver.get("FullName") or "-",
        "receiver_mobile": receiver.get("Mobile") or "-",
        "receiver_address": receiver.get("Address") or "-",
        "sender": sender.get("FullName") or "-",
        "create_time": order.get("CreateTime") or "-",
        "cancelable": can_cancel(order),
    }


def get_order_detail(token, order_code, timeout=30):
    """订单详情：含未脱敏的寄/收件人信息与取消原因。返回 (data, err)。"""
    data, err = post_form(token, EP_ORDER_DETAIL, {"OrderCode": order_code}, timeout)
    return data, err


def cancel_order(token, order_code, timeout=30):
    """取消寄件（真实生效，不可预览）。

    页面 CancelOrder() 就这一个参数 OrderCode。返回值语义：
      (data, err)，data 非 None 即成功。
    """
    if not order_code or not str(order_code).strip():
        return None, "订单号为空"
    return post_form(token, EP_CANCEL_ORDER, {"OrderCode": str(order_code).strip()}, timeout)


# --------------------------------------------------------------------------- #
# 工单：类型列表 / 列表 / 详情 / 提交
#
# 页面：/AddWorkOrder.html（type 3 = 工单反馈）、/WorkOrderManage.html（列表）
# --------------------------------------------------------------------------- #
# 页面 workOrderTypeMap 的副本：categoryCode → 该类型额外要填什么。
# 后端只喂分类树（GetWorkOrderCategoryList），要不要「反馈重量/商品价值/新收件信息/截图」
# 是前端根据这张表控制必填的，所以技能包里也得留一份，否则提交会被后端拒。
WORK_ORDER_RULES = {
    3:     {"need_weight": True,  "need_value": False, "need_image": True, "name": "重量/运费异常"},
    585696: {"need_weight": False, "need_value": True,  "need_image": True, "name": "包裹收到错件"},
    585698: {"need_weight": False, "need_value": True,  "need_image": True, "name": "收到后少件"},
    6:     {"need_weight": False, "need_value": True,  "need_image": True, "name": "包裹破损"},
    13:    {"need_weight": False, "need_value": False, "need_image": True, "name": "快递员私下收费"},
    5:     {"need_weight": False, "need_value": False, "need_image": True, "name": "超时揽件"},
    1:     {"need_weight": False, "need_value": False, "need_image": True, "name": "虚假揽件"},
    8:     {"need_weight": False, "need_value": True,  "need_image": True, "name": "丢件"},
    11:    {"need_weight": False, "need_value": False, "need_image": True, "name": "轨迹签收实际未收到货"},
    2:     {"need_weight": False, "need_value": False, "need_image": True, "name": "快递员服务态度差"},
    10:    {"need_weight": False, "need_value": False, "need_image": True, "name": "物流长时间未更新"},
    401:   {"need_weight": False, "need_value": False, "need_image": True, "name": "拦截"},
    678679: {"need_weight": False, "need_value": False, "need_image": True, "name": "核实退回"},
    # 接口分类树里没有、页面手工补的一档（快递100 secondType=18）
    18:   {"need_weight": False, "need_value": False, "need_image": True,
           "need_new_address": True, "name": "更改收件信息"},
}


def get_work_order_categories(token, timeout=30):
    """工单分类树。返回 (grouped, err)。

    grouped 形如 [{"group": "投诉", "code": 993, "items": [{"code": 2, "name": "..."}]}, ...]
    请求体是空的 {}，跟页面 GetWorkOrderCategoryList() 一致。
    """
    data, err = post_form(token, EP_WORK_ORDER_CATEGORY, {}, timeout)
    if err:
        return None, err
    groups = []
    for g in (data or []):
        items = []
        for c in (g.get("Children") or []):
            items.append({"code": _as_int(c.get("CategoryCode")), "name": c.get("CategoryName") or ""})
        groups.append({"code": _as_int(g.get("CategoryCode")),
                       "group": g.get("CategoryName") or "", "items": items})
    return groups, None


def flatten_work_order_categories(groups):
    """把分类树拍平成 [{code, name, group}]，方便展示和按名匹配。"""
    out = []
    for g in (groups or []):
        for it in g.get("items") or []:
            out.append({"code": it["code"], "name": it["name"], "group": g["group"]})
    return out


def match_work_order_category(categories, want):
    """按编码/中文名/关键词找工单类型。

    支持 '2'、'投诉/快递员服务态度差'、'丢件' 三种写法。
    找不到返回 (None, err)。
    """
    flat = flatten_work_order_categories(categories) if categories else []
    flat.append({"code": 18, "name": "更改收件信息", "group": "其他"})  # 接口不返回，手工补
    if not want:
        return None, "未指定工单类型"
    w = str(want).strip()
    for it in flat:
        if str(it["code"]) == w:
            return it, None
    for it in flat:
        if w in it["name"]:
            return it, None
    if "/" in w:                                   # 支持 '投诉/快递员服务态度差'
        leaf = w.split("/")[-1].strip()
        for it in flat:
            if leaf and leaf in it["name"]:
                return it, None
    names = "、".join(it["name"] for it in flat)
    return None, f"找不到工单类型「{want}」，可用：{names}"


def work_order_rule(code):
    """取某工单类型的附加校验规则（WORK_ORDER_RULES）。"""
    return WORK_ORDER_RULES.get(_as_int(code), {})


def search_work_orders(token, status=None, page_index=1, page_size=50, timeout=30):
    """工单列表。status 传 '' 或 None 查全部。返回 (rows, total, err)。

    列表行字段：WorkOrderCode / OrderCode / LogisticsCode / ShipperName /
    WorkOrderType / WorkOrderName / WorkOrderContent / WorkOrderStatus /
    ReplyContent / ReplyDateTime / CreateTime / OrderImages
    """
    payload = {
        "PageIndex": page_index,
        "PageSize": page_size,
        "WorkOrderStatus": status if status not in (None, "") else "",
    }
    data, err = post_form(token, EP_WORK_ORDER_LIST, payload, timeout)
    if err:
        return None, 0, err
    rows = (data or {}).get("ResultList") or []
    total = (data or {}).get("TotalCount") or 0
    return rows, total, None


def fmt_work_order_row(row):
    """工单列表行 → 展示用 dict。"""
    code = _as_int(row.get("WorkOrderType"))
    return {
        "work_order_code": row.get("WorkOrderCode") or "",
        "order_code": row.get("OrderCode") or "-",
        "logistics_code": row.get("LogisticsCode") or "-",
        "shipper": row.get("ShipperName") or "-",
        "type_code": code,
        "type_name": row.get("WorkOrderName") or WORK_ORDER_TYPE_NAME.get(code, "-"),
        "status": fmt_work_order_status(row.get("WorkOrderStatus")),
        "content": (row.get("WorkOrderContent") or "").strip(),
        "reply": (row.get("ReplyContent") or "").strip() or "-",
        "create_time": row.get("CreateTime") or "-",
        "reply_time": row.get("ReplyDateTime") or "-",
    }


def get_work_order_detail(token, work_order_id, timeout=30):
    """工单详情。

    ⚠️ 坑：接口校验的是**内部自增 ID**（列表行里的 ID 字段），不是 WorkOrderCode。
        传 '260918000015' 会报「工单ID不能为空」，传 819 才成功。
    返回 (data, err)，data 里另有 WorkOrderReplyList（历史回复）。
    """
    return post_form(token, EP_WORK_ORDER_DETAIL, {"ID": work_order_id}, timeout)


def build_work_order_payload(order_code, work_type, content, link_man, mobile_phone,
                             source_page=1, tel_weight="", modity_value="",
                             new_receiver_name="", new_receiver_phone="",
                             new_receiver_address="", images=None):
    """构造工单提交体，字段与页面 getData() 一一对应。

    type=3（工单反馈）走 AddWorkOrder；type=1/2（拦截转寄/退回）走
    WaybillIntercept，那条链路额外要 MonthCode 与新地址，见
    build_intercept_payload()。
    """
    name = (link_man or "").strip()
    phone = (mobile_phone or "").strip()
    payload = {
        "OrderCode": (order_code or "").strip(),
        "Type": 3,
        "WorkOrderType": _as_int(work_type),
        "WorkOrderContent": (content or "").strip(),
        "LinkMan": name,
        "MobilePhone": phone,
        # Reason 是页面拼的固定说明串，后端据此回联系
        "Reason": f"我是{name},电话：{phone},如有疑问请联系我。" if phone else "如有疑问请联系我。",
        "Role": "1",          # 发起方：1-寄方
        "PayMode": 4,         # 1-寄付 2-到付 3-转第三方月结 4-寄付月结
        "SourcePage": source_page,
        # 页面是数组（jQuery 序列化成 ImageNameList[]=x），这里没有图片上传能力，
        # 给空数组保持形状一致：json.dumps([]) == '[]'
        "ImageNameList": json.dumps(images or []),
    }
    rule = work_order_rule(work_type)
    if rule.get("need_weight"):
        payload["TelWeight"] = (tel_weight or "").strip()
    if rule.get("need_value"):
        payload["ModityValue"] = (modity_value or "").strip()
    if rule.get("need_new_address"):
        payload["NewReceiverName"] = (new_receiver_name or "").strip()
        payload["NewReceiverPhone"] = (new_receiver_phone or "").strip()
        payload["NewReceiverAddress"] = (new_receiver_address or "").strip()
        # 页面会把新收件信息并进 WorkOrderContent 一起提交（secondType=18）
        extra = (f"【更改后收件信息】姓名：{payload['NewReceiverName']}，"
                 f"电话：{payload['NewReceiverPhone']}，"
                 f"地址：{payload['NewReceiverAddress']}")
        base = payload["WorkOrderContent"]
        payload["WorkOrderContent"] = (base + "\n" + extra) if base else extra
    return payload


def build_intercept_payload(order_code, intercept_type, month_code, link_man, mobile_phone,
                            province="", city="", area="", address=""):
    """构造拦截转寄(1)/拦截退回(2)的提交体。

    这两类不走 AddWorkOrder，走 WaybillIntercept，且**必须**带月结号（页面
    #div_MonthCode 是必填），type=1 还要带新收件地址。
    """
    name = (link_man or "").strip()
    payload = {
        "OrderCode": (order_code or "").strip(),
        "Type": _as_int(intercept_type) or 2,
        "MonthCode": (month_code or "").strip(),
        "LinkMan": name,
        "MobilePhone": (mobile_phone or "").strip(),
        "Reason": f"我是{name},电话：{mobile_phone},如有疑问请联系我。",
        "Role": "1",
        "PayMode": 4,
        "SourcePage": 1,
        "ImageNameList": json.dumps([]),
    }
    if _as_int(intercept_type) == 1:
        payload["NewAddress"] = {
            "ProvinceName": province, "CityName": city,
            "ExpAreaName": area, "Address": (address or "").strip(),
        }
    return payload


def validate_work_order(payload):
    """提交前的本地校验，复刻页面 verifyData()。

    返回 (warnings, fatal)：fatal 非空就不要提交（接口多半也会拒）。
    """
    warnings, fatal = [], []
    if not payload.get("OrderCode"):
        fatal.append("请输订单号")
    if not payload.get("LinkMan"):
        fatal.append("请输入姓名")
    if not payload.get("MobilePhone"):
        fatal.append("请输入手机号码")
    else:
        p = str(payload["MobilePhone"]).strip()
        if not (len(p) == 11 and p.isdigit()):
            warnings.append(f"联系方式「{p}」不是常见手机号，工单可能联系不到你")

    rule = work_order_rule(payload.get("WorkOrderType"))
    if payload.get("Type") == 3:
        if not payload.get("WorkOrderType"):
            fatal.append("请选择工单类型")
        elif not (payload.get("WorkOrderContent") or "").strip():
            fatal.append("请输入问题描述")
    else:
        if not (payload.get("MonthCode") or "").strip():
            fatal.append("请输入月结号（快递公司需要验证身份）")
    if rule.get("need_weight") and not (payload.get("TelWeight") or "").strip():
        fatal.append("该工单类型需填写反馈重量")
    if rule.get("need_value") and not (payload.get("ModityValue") or "").strip():
        fatal.append("该工单类型需填写商品价值")
    if rule.get("need_new_address"):
        for key, label in (("NewReceiverName", "新收件人姓名"),
                           ("NewReceiverPhone", "新收件人电话"),
                           ("NewReceiverAddress", "新收件地址")):
            if not (payload.get(key) or "").strip():
                fatal.append(f"请输入{label}")
    return warnings, fatal


def add_work_order(token, payload, timeout=30):
    """提交工单（type=3）。真正的写入操作，调用前请先把 validate_work_order 跑过。"""
    return post_form(token, EP_WORK_ORDER_ADD, payload, timeout)


def intercept_waybill(token, payload, timeout=30):
    """提交运单拦截（type=1 转寄 / type=2 退回）。"""
    return post_form(token, EP_WAYBILL_INTERCEPT, payload, timeout)
