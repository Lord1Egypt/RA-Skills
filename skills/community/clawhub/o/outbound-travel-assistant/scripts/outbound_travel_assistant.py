#!/usr/bin/env python3
"""出境游旅行助手 - Outbound Travel Assistant
11个工具覆盖从签证到退税的完整出境需求
RG代理5个(机票/酒店/座位/行李/房型) + 本地数据4个(签证/安全/插头/紧急) + 计算+API 2个(退税/汇率)
"""
import json
import os
import sys
import urllib.request
import urllib.error

PROXY_URL = "https://1439498936-460a7b6oqn.ap-guangzhou.tencentscf.com"
PROXY_TOKEN = os.environ.get("PROXY_TOKEN", "")

# ============================================================
# 第一组：RG代理工具 (5个)
# ============================================================

def _call_proxy(api_type, params=None):
    """通过RG云端代理调用API"""
    headers = {"Content-Type": "application/json"}
    if PROXY_TOKEN:
        headers["Authorization"] = f"Bearer {PROXY_TOKEN}"
    body = json.dumps({"type": api_type, "params": params or {}})
    req = urllib.request.Request(
        PROXY_URL,
        data=body.encode("utf-8"),
        headers=headers,
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return data
    except urllib.error.HTTPError as e:
        detail = ""
        try:
            detail = e.read().decode("utf-8", errors="replace")
        except Exception:
            pass
        return {"error": f"HTTP {e.code}", "detail": detail}
    except Exception as e:
        return {"error": str(e)}


def _fmt_duration(minutes):
    """格式化飞行时长"""
    if not minutes:
        return ""
    try:
        m = int(minutes)
        return f"{m // 60}h{m % 60}m"
    except (ValueError, TypeError):
        return str(minutes)


def search_flights(origin="", destination="", date="", **kwargs):
    """搜索国际机票"""
    if not origin or not destination or not date:
        return json.dumps({"error": "请提供origin(出发城市)、destination(到达城市)、date(日期YYYY-MM-DD)"}, ensure_ascii=False)
    result = _call_proxy("flight", {"origin": origin, "destination": destination, "date": date})
    if "error" in result:
        return json.dumps(result, ensure_ascii=False)
    flights = result.get("flightInformationList", [])
    if not flights:
        return json.dumps({"message": f"未找到{origin}→{destination}({date})的航班", "raw": result}, ensure_ascii=False)
    output = []
    for f in flights[:10]:
        segs = f.get("fromSegments", [])
        seg_info = ""
        if segs:
            s = segs[0]
            seg_info = f"{s.get('flightNumber','')} {s.get('depAirport','')}→{s.get('arrAirport','')} {_fmt_duration(s.get('duration',''))} 出发{s.get('depTime','')} 到达{s.get('arrTime','')}"
        output.append({
            "routingId": f.get("routingId", ""),
            "carrier": f.get("validatingCarrier", ""),
            "segment": seg_info,
            "price": f.get("totalAdultPrice", ""),
            "score": f.get("fromSmartValueScore", ""),
            "bookingUrl": f.get("bookingUrl", ""),
        })
    return json.dumps({"count": len(flights), "flights": output}, ensure_ascii=False, indent=2)


def search_hotels(city="", checkin="", checkout="", **kwargs):
    """搜索酒店"""
    if not city or not checkin or not checkout:
        return json.dumps({"error": "请提供city(城市)、checkin(入住日期)、checkout(离店日期)"}, ensure_ascii=False)
    result = _call_proxy("hotel_search", {"city": city, "checkin": checkin, "checkout": checkout})
    if "error" in result:
        return json.dumps(result, ensure_ascii=False)
    hotels = result.get("hotelInformationList", [])
    if not hotels:
        return json.dumps({"message": f"未找到{city}({checkin}~{checkout})的酒店", "raw": result}, ensure_ascii=False)
    output = []
    for h in hotels[:10]:
        output.append({
            "hotelId": h.get("hotelId", ""),
            "name": h.get("name", ""),
            "starRating": h.get("starRating", ""),
            "lowestPrice": h.get("price", {}).get("lowestPrice", ""),
            "address": h.get("address", ""),
            "amenities": h.get("hotelAmenities", [])[:5],
            "bookingUrl": h.get("bookingUrl", ""),
        })
    return json.dumps({"count": len(hotels), "hotels": output}, ensure_ascii=False, indent=2)


def flight_seats(flight_number="", date="", **kwargs):
    """查询航班座位布局和选座价格"""
    if not flight_number:
        return json.dumps({"error": "请提供flight_number(航班号)"}, ensure_ascii=False)
    result = _call_proxy("flight_seats", {"flight_number": flight_number, "date": date})
    return json.dumps(result, ensure_ascii=False, indent=2)


def flight_baggage(flight_number="", date="", **kwargs):
    """查询航班行李额度和额外费用"""
    if not flight_number:
        return json.dumps({"error": "请提供flight_number(航班号)"}, ensure_ascii=False)
    result = _call_proxy("flight_baggage", {"flight_number": flight_number, "date": date})
    return json.dumps(result, ensure_ascii=False, indent=2)


def hotel_detail(hotel_id="", checkin="", checkout="", **kwargs):
    """查看酒店房型价格和退改政策"""
    if not hotel_id:
        return json.dumps({"error": "请提供hotel_id(酒店ID)"}, ensure_ascii=False)
    result = _call_proxy("hotel_detail", {"hotel_id": hotel_id, "checkin": checkin, "checkout": checkout})
    if "error" in result:
        return json.dumps(result, ensure_ascii=False)
    rooms = result.get("roomRatePlans", [])
    if not rooms:
        return json.dumps({"message": "未找到房型信息", "raw": result}, ensure_ascii=False)
    output = []
    for r in rooms:
        policies = r.get("cancellationPolicies", [])
        policy_desc = "; ".join([p.get("description", "") for p in policies]) if policies else "请咨询酒店"
        output.append({
            "roomName": r.get("roomName", ""),
            "totalPrice": r.get("totalPrice", ""),
            "mealPlan": r.get("mealPlan", ""),
            "cancellationPolicy": policy_desc,
            "bookingUrl": r.get("bookingUrl", ""),
        })
    return json.dumps({"rooms": output}, ensure_ascii=False, indent=2)


# ============================================================
# 第二组：本地数据工具 (4个)
# ============================================================

# ---------- 签证数据库 ----------
VISA_DB = {
    "日本": {"en": "Japan", "visa_types": {"tourism": {"type": "需提前申请", "max_stay": 15, "visa_fee": 200, "processing_time": 5, "entry_count": "单次", "notes": "单次短期滞在签证15天。3年多次需年收入20万+或近3年内2次赴日记录；5年多次需年收入50万+。"}, "business": {"type": "需提前申请", "max_stay": 90, "visa_fee": 200, "processing_time": 5, "entry_count": "单次", "notes": "需日方邀请函、身元保证书、滞在日程表。"}, "transit": {"type": "过境免签", "max_stay": 3, "visa_fee": 0, "processing_time": 0, "entry_count": "单次", "notes": "经日本转机可享72小时过境免签(Shore Pass)。"}}, "photo_spec": "4.5×4.5cm，白底", "checklist_tips": "单次签证核心：在职证明+银行流水(余额建议5万+)+行程单。多次签证核心：高收入证明+纳税记录+旧签证。"},
    "韩国": {"en": "South Korea", "visa_types": {"tourism": {"type": "需提前申请", "max_stay": 30, "visa_fee": 195, "processing_time": 5, "entry_count": "单次", "notes": "有过OECD国家签证记录可简化材料。济州岛免签30天。"}, "business": {"type": "需提前申请", "max_stay": 90, "visa_fee": 195, "processing_time": 5, "entry_count": "单次", "notes": "需韩方邀请函、事业者登录证明、纳税证明。"}, "transit": {"type": "过境免签", "max_stay": 3, "visa_fee": 0, "processing_time": 0, "entry_count": "单次", "notes": "经韩国转机前往美/加/澳/新/欧，持确认续程机票可免签72小时。"}}, "photo_spec": "3.5×4.5cm，白底", "checklist_tips": "有美/日/加/澳/新签证或永居可申请多次简化。首次申请需：护照+照片+申请表+在职证明+银行流水+身份证复印件。"},
    "泰国": {"en": "Thailand", "visa_types": {"tourism": {"type": "免签", "max_stay": 30, "visa_fee": 0, "processing_time": 0, "entry_count": "单次", "notes": "2024年3月1日起永久互免签证。护照有效期需6个月以上，需出示返程机票和酒店确认单。免签停留30天，可延期30天。"}, "business": {"type": "免签", "max_stay": 30, "visa_fee": 0, "processing_time": 0, "entry_count": "单次", "notes": "商务活动免签停留30天，正式工作需办理Non-B签证。"}}, "photo_spec": "3.5×4.5cm白底(如需办非免签类型)", "checklist_tips": "免签入境需准备：返程机票、酒店预订单、足够资金证明(1万泰铢/人或2万泰铢/家庭)"},
    "新加坡": {"en": "Singapore", "visa_types": {"tourism": {"type": "需提前申请", "max_stay": 30, "visa_fee": 153, "processing_time": 3, "entry_count": "多次", "notes": "必须通过授权旅行社/航空公司在线申请，不接受个人直接递签。电子签审批后邮件发送。"}, "transit": {"type": "过境免签", "max_stay": 4, "visa_fee": 0, "processing_time": 0, "entry_count": "单次", "notes": "持有效澳/加/德/日/新(西兰)/瑞/英/美签证，经新加坡转机可享96小时免签(VFTF)。"}}, "photo_spec": "4.0×5.2cm，白底", "checklist_tips": "新加坡签证必须通过授权旅行社代办。核心材料：护照+照片+申请表+在职证明+银行流水+往返机票+酒店预订。"},
    "越南": {"en": "Vietnam", "visa_types": {"tourism": {"type": "电子签", "max_stay": 90, "visa_fee": 25, "processing_time": 3, "entry_count": "单次", "notes": "2023年8月起电子签有效期延长至90天。也可办落地签(25美元)但建议提前办电子签更省时。", "evisa_url": "https://evisa.xuatnhapcanh.gov.vn/"}}, "photo_spec": "4.0×6.0cm，白底", "checklist_tips": "电子签在线申请最快，3个工作日。落地签需准备：护照照片+签证费25美元+入境批文。"},
    "马来西亚": {"en": "Malaysia", "visa_types": {"tourism": {"type": "免签", "max_stay": 30, "visa_fee": 0, "processing_time": 0, "entry_count": "单次", "notes": "2023年12月1日起对中国公民免签30天。需填写MDAC电子入境卡(出发前3天内)，出示返程机票和酒店确认。"}, "business": {"type": "需提前申请", "max_stay": 30, "visa_fee": 200, "processing_time": 5, "entry_count": "单次", "notes": "商务访问需马方邀请函，正式工作需办就业签证。"}}, "photo_spec": "3.5×5.0cm白底(如需办签证类型)", "checklist_tips": "免签入境需：MDAC电子入境卡+返程机票+酒店预订+足够资金。MDAC必须出发前3天在线填写。"},
    "印度尼西亚": {"en": "Indonesia", "visa_types": {"tourism": {"type": "落地签/电子签", "max_stay": 30, "visa_fee": 35, "processing_time": 0, "entry_count": "单次", "notes": "VOA落地签35美元，可延期30天。电子签e-VOA提前申请更方便。", "evisa_url": "https://molina.imigrasi.go.id/"}}, "photo_spec": "4.0×6.0cm白底(如需办其他类型)", "checklist_tips": "落地签最方便，需护照+返程机票+签证费35美元。e-VOA提前在线申请省排队时间。"},
    "柬埔寨": {"en": "Cambodia", "visa_types": {"tourism": {"type": "电子签/落地签", "max_stay": 30, "visa_fee": 30, "processing_time": 3, "entry_count": "单次", "notes": "电子签和落地签均可。电子签e-visa在线申请3天出签。落地签在口岸办理需30美元现金+照片。", "evisa_url": "https://www.evisa.gov.kh/"}}, "photo_spec": "4.0×6.0cm，白底", "checklist_tips": "落地签最方便，但旺季排队久。建议电子签提前办。"},
    "菲律宾": {"en": "Philippines", "visa_types": {"tourism": {"type": "需提前申请", "max_stay": 30, "visa_fee": 167, "processing_time": 5, "entry_count": "单次", "notes": "需在使领馆递签。有美/日/加/澳/申根有效签证可免签7天(需从第三国入境)。"}}, "photo_spec": "3.5×4.5cm，白底", "checklist_tips": "核心材料：护照+照片+申请表+在职证明+银行流水+往返机票+酒店预订。有发达国家签证可免签7天。"},
    "印度": {"en": "India", "visa_types": {"tourism": {"type": "电子签", "max_stay": 30, "visa_fee": 25, "processing_time": 4, "entry_count": "单次", "notes": "e-Tourist Visa在线申请，30天单次入境。也有1年/5年多次电子签选项。", "evisa_url": "https://indianvisaonline.gov.in/evisa/tvoa.html"}, "business": {"type": "电子签", "max_stay": 365, "visa_fee": 80, "processing_time": 4, "entry_count": "多次", "notes": "e-Business Visa，1年多次入境，每次停留180天。"}}, "photo_spec": "5.0×5.0cm，白底，JPEG格式上传", "checklist_tips": "电子签全程在线办理，需上传照片+护照首页扫描件。注意照片格式要求严格。"},
    "沙特阿拉伯": {"en": "Saudi Arabia", "visa_types": {"tourism": {"type": "电子签", "max_stay": 90, "visa_fee": 80, "processing_time": 1, "entry_count": "多次", "notes": "电子签在线申请，即时出签，1年多次入境每次90天。也可落地签但费用更高。", "evisa_url": "https://visa.visitsaudi.com/"}}, "photo_spec": "无需(电子签上传)", "checklist_tips": "电子签非常方便，在线即时出签。注意沙特文化禁忌，入境需遵守当地法规。"},
    "美国": {"en": "United States", "visa_types": {"tourism": {"type": "需提前申请", "max_stay": 180, "visa_fee": 1250, "processing_time": 15, "entry_count": "多次", "notes": "B1/B2签证10年多次入境，每次停留最长6个月。需面签。EVUS登记后才能入境。"}, "business": {"type": "需提前申请", "max_stay": 180, "visa_fee": 1250, "processing_time": 15, "entry_count": "多次", "notes": "B1/B2商务旅游签证10年多次。需面签。"}, "transit": {"type": "需提前申请", "max_stay": 29, "visa_fee": 1250, "processing_time": 15, "entry_count": "多次", "notes": "美国没有过境免签，转机也需签证。C型过境签证或B1/B2均可。"}}, "photo_spec": "5.0×5.0cm，白底，不可戴眼镜", "checklist_tips": "美签核心：DS-160表+面签+签证费。面签重点：证明无移民倾向(稳定工作+资产+家庭联系)。通过后需EVUS登记(免费)。"},
    "加拿大": {"en": "Canada", "visa_types": {"tourism": {"type": "需提前申请", "max_stay": 180, "visa_fee": 850, "processing_time": 20, "entry_count": "多次", "notes": "临时居民签证(TRV)，通常给到护照有效期。也可申请eTA(需持美签)。"}}, "photo_spec": "3.5×4.5cm，白底", "checklist_tips": "加拿大签核心：资金证明(6个月银行流水)+在职证明+行程单。持有效美签可简化申请。"},
    "墨西哥": {"en": "Mexico", "visa_types": {"tourism": {"type": "免签(有条件)", "max_stay": 180, "visa_fee": 0, "processing_time": 0, "entry_count": "多次", "notes": "持有效美/加/日/英/申根签证可免签180天。无上述签证需申请墨西哥签证。"}}, "photo_spec": "3.5×4.5cm白底(如需办签)", "checklist_tips": "有美/加/日/英/申根签证直接免签，最方便。无上述签证需办墨西哥签证，建议先办美签。"},
    "英国": {"en": "United Kingdom", "visa_types": {"tourism": {"type": "需提前申请", "max_stay": 180, "visa_fee": 1150, "processing_time": 15, "entry_count": "多次", "notes": "标准访客签证6个月多次入境。2年/5年/10年长期签证可选，费用递增。UKVI在线申请+VFS递签。"}, "business": {"type": "需提前申请", "max_stay": 180, "visa_fee": 1150, "processing_time": 15, "entry_count": "多次", "notes": "商务访客签证，允许会议/考察/培训等，不允许工作。"}}, "photo_spec": "3.5×4.5cm，白底", "checklist_tips": "英国签核心：银行流水(6个月，余额建议10万+)+在职证明+行程单。资金证明最重要，切忌临时大额转入。2年签性价比高。"},
    "法国": {"en": "France", "visa_types": {"tourism": {"type": "需提前申请(申根)", "max_stay": 90, "visa_fee": 615, "processing_time": 10, "entry_count": "多次", "notes": "申根签证，可在26个申根国通行。需在主要停留国或首入国使领馆申请。France-Visas在线填表+TLScontact预约递签。"}, "business": {"type": "需提前申请(申根)", "max_stay": 90, "visa_fee": 615, "processing_time": 10, "entry_count": "多次", "notes": "商务申根签证，需法方邀请函+公司担保信。"}}, "photo_spec": "3.5×4.5cm，白底，不可微笑", "checklist_tips": "申根签核心：行程单+酒店预订+往返机票+保险(3万欧元)+银行流水(余额建议5万+)+在职证明。法国签相对容易，是申根热门首签国。"},
    "德国": {"en": "Germany", "visa_types": {"tourism": {"type": "需提前申请(申根)", "max_stay": 90, "visa_fee": 615, "processing_time": 10, "entry_count": "多次", "notes": "申根签证。通过VFS Global递签。德国审核较严，建议材料充分。"}}, "photo_spec": "3.5×4.5cm，白底", "checklist_tips": "德国签审核严格，银行流水要稳定(切忌临时大额存入)，在职证明需详细。"},
    "意大利": {"en": "Italy", "visa_types": {"tourism": {"type": "需提前申请(申根)", "max_stay": 90, "visa_fee": 615, "processing_time": 10, "entry_count": "多次", "notes": "申根签证。通过VFS Global递签。意大利签相对容易，出签率较高。"}}, "photo_spec": "3.5×4.5cm，白底", "checklist_tips": "意大利签出签率较高，材料与法国申根类似。旺季(5-9月)预约紧张，提前2-3个月申请。"},
    "西班牙": {"en": "Spain", "visa_types": {"tourism": {"type": "需提前申请(申根)", "max_stay": 90, "visa_fee": 615, "processing_time": 10, "entry_count": "多次", "notes": "申根签证。通过BLS International递签。"}}, "photo_spec": "3.5×4.5cm，白底", "checklist_tips": "西班牙签材料与申根标准一致。注意BLS预约有时紧张。"},
    "瑞士": {"en": "Switzerland", "visa_types": {"tourism": {"type": "需提前申请(申根)", "max_stay": 90, "visa_fee": 615, "processing_time": 10, "entry_count": "多次", "notes": "申根签证。通过TLScontact递签。非EU但属申根区。"}}, "photo_spec": "3.5×4.5cm，白底", "checklist_tips": "瑞士虽非EU但属申根区。材料与申根标准一致。"},
    "荷兰": {"en": "Netherlands", "visa_types": {"tourism": {"type": "需提前申请(申根)", "max_stay": 90, "visa_fee": 615, "processing_time": 10, "entry_count": "多次", "notes": "申根签证。通过VFS Global递签。"}}, "photo_spec": "3.5×4.5cm，白底", "checklist_tips": "荷兰申根签标准流程，审核适中。"},
    "希腊": {"en": "Greece", "visa_types": {"tourism": {"type": "需提前申请(申根)", "max_stay": 90, "visa_fee": 615, "processing_time": 10, "entry_count": "多次", "notes": "申根签证。希腊签出签率较高。"}}, "photo_spec": "3.5×4.5cm，白底", "checklist_tips": "希腊签出签率较高，是申根签热门选择。"},
    "葡萄牙": {"en": "Portugal", "visa_types": {"tourism": {"type": "需提前申请(申根)", "max_stay": 90, "visa_fee": 615, "processing_time": 10, "entry_count": "多次", "notes": "申根签证。葡萄牙签出签率较高。"}}, "photo_spec": "3.5×4.5cm，白底", "checklist_tips": "葡萄牙签出签率较高，适合首次申根。"},
    "捷克": {"en": "Czech Republic", "visa_types": {"tourism": {"type": "需提前申请(申根)", "max_stay": 90, "visa_fee": 615, "processing_time": 10, "entry_count": "多次", "notes": "申根签证。通过VFS Global递签。"}}, "photo_spec": "3.5×4.5cm，白底", "checklist_tips": "捷克申根签标准流程。布拉格是热门旅游目的地。"},
    "爱尔兰": {"en": "Ireland", "visa_types": {"tourism": {"type": "需提前申请", "max_stay": 90, "visa_fee": 600, "processing_time": 15, "entry_count": "单次", "notes": "短期停留签证。持英国签证可使用BIVS互免计划入境爱尔兰。"}}, "photo_spec": "3.5×4.5cm，白底", "checklist_tips": "如果有英国签证(标注BIVS)，可免签入境爱尔兰。单独申请爱尔兰签材料与英国类似。"},
    "澳大利亚": {"en": "Australia", "visa_types": {"tourism": {"type": "电子签", "max_stay": 90, "visa_fee": 960, "processing_time": 15, "entry_count": "多次", "notes": "访客签证600类(Subclass 600)，可在线申请ImmiAccount。1年/3年多次可选。", "evisa_url": "https://online.immi.gov.au/"}}, "photo_spec": "3.5×4.5cm，白底", "checklist_tips": "澳签核心：在线申请ImmiAccount+资金证明+在职证明+行程单。电调概率较高，确保信息一致。"},
    "新西兰": {"en": "New Zealand", "visa_types": {"tourism": {"type": "电子签", "max_stay": 90, "visa_fee": 1200, "processing_time": 20, "entry_count": "多次", "notes": "访客签证，可在线申请。5年多次签证可选(需满足条件)。", "evisa_url": "https://www.immigration.govt.nz/"}}, "photo_spec": "3.5×4.5cm，白底", "checklist_tips": "新西兰签核心：在线申请+资金证明+在职证明。审核较严格，材料需真实完整。"},
    "阿联酋": {"en": "UAE", "visa_types": {"tourism": {"type": "免签", "max_stay": 30, "visa_fee": 0, "processing_time": 0, "entry_count": "单次", "notes": "2018年起对中国公民免签30天，可延期。迪拜/阿布扎比等均可免签入境。"}}, "photo_spec": "无需(免签)", "checklist_tips": "免签入境需：护照有效期6个月以上+返程机票。停留可延期一次(30天)。"},
    "土耳其": {"en": "Turkey", "visa_types": {"tourism": {"type": "电子签", "max_stay": 30, "visa_fee": 50, "processing_time": 1, "entry_count": "单次", "notes": "e-Visa在线申请，即时出签。需持有效OECD国家签证或居留许可。", "evisa_url": "https://www.evisa.gov.tr/"}}, "photo_spec": "无需(电子签)", "checklist_tips": "电子签非常方便，前提是持有有效的OECD国家(美/加/澳/新/申根/英/日/韩)签证或居留。"},
    "俄罗斯": {"en": "Russia", "visa_types": {"tourism": {"type": "需提前申请", "max_stay": 30, "visa_fee": 350, "processing_time": 7, "entry_count": "单次", "notes": "需俄罗斯邀请函。团队游可免签15天(需旅行社组织)。电子签仅限远东/加里宁格勒等部分地区。"}}, "photo_spec": "3.5×4.5cm，白底", "checklist_tips": "核心材料：护照+照片+邀请函+申请表+保险。个人旅游签需俄方旅行社邀请函。团队游免签最方便。"},
    "巴西": {"en": "Brazil", "visa_types": {"tourism": {"type": "需提前申请", "max_stay": 90, "visa_fee": 1050, "processing_time": 15, "entry_count": "多次", "notes": "旅游签证90天多次入境。需在巴西驻华使领馆递签。2024年对中国实行电子签政策。"}}, "photo_spec": "5.0×7.0cm，白底", "checklist_tips": "巴西签证材料较多：护照+照片+申请表+在职证明+银行流水+往返机票+酒店预订+行程单。照片尺寸特殊(5×7cm)。"},
    "埃及": {"en": "Egypt", "visa_types": {"tourism": {"type": "落地签/电子签", "max_stay": 30, "visa_fee": 25, "processing_time": 0, "entry_count": "单次", "notes": "落地签25美元，需准备：酒店预订+返程机票+2000美元现金或等值。电子签也可在线申请。", "evisa_url": "https://visa2egypt.gov.eg/"}}, "photo_spec": "无需(落地签)", "checklist_tips": "落地签最方便，但需携带2000美元现金(有时会查)。电子签提前办更省心。"},
    "南非": {"en": "South Africa", "visa_types": {"tourism": {"type": "需提前申请", "max_stay": 90, "visa_fee": 550, "processing_time": 10, "entry_count": "多次", "notes": "需在南非签证中心递签。审核周期较长，建议提前1个月申请。"}}, "photo_spec": "3.5×4.5cm，白底", "checklist_tips": "南非签材料较多：护照+照片+申请表+在职证明+银行流水+往返机票+酒店预订+黄热病疫苗接种证明(如从疫区来)。"},
    "以色列": {"en": "Israel", "visa_types": {"tourism": {"type": "需提前申请", "max_stay": 90, "visa_fee": 200, "processing_time": 10, "entry_count": "单次", "notes": "需在以色列驻华使领馆递签。持有效美/申根签证可简化部分材料。"}}, "photo_spec": "5.0×5.0cm，白底", "checklist_tips": "以色列签证材料：护照+照片+申请表+在职证明+银行流水+行程单+往返机票。注意以色列签证可能影响部分阿拉伯国家入境。"},
}

VISA_ALIAS = {
    "日本": "日本", "Japan": "日本", "japan": "日本", "东京": "日本", "大阪": "日本",
    "韩国": "韩国", "南韩": "韩国", "South Korea": "韩国", "首尔": "韩国", "釜山": "韩国",
    "泰国": "泰国", "Thailand": "泰国", "曼谷": "泰国", "清迈": "泰国", "普吉": "泰国",
    "新加坡": "新加坡", "Singapore": "新加坡",
    "越南": "越南", "Vietnam": "越南", "河内": "越南", "胡志明": "越南",
    "马来西亚": "马来西亚", "Malaysia": "马来西亚", "吉隆坡": "马来西亚",
    "印尼": "印度尼西亚", "印度尼西亚": "印度尼西亚", "Indonesia": "印度尼西亚", "巴厘岛": "印度尼西亚",
    "美国": "美国", "USA": "美国", "纽约": "美国", "洛杉矶": "美国",
    "加拿大": "加拿大", "Canada": "加拿大", "多伦多": "加拿大",
    "英国": "英国", "UK": "英国", "伦敦": "英国", "英格兰": "英国",
    "法国": "法国", "France": "法国", "巴黎": "法国",
    "德国": "德国", "Germany": "德国", "柏林": "德国", "慕尼黑": "德国",
    "意大利": "意大利", "Italy": "意大利", "罗马": "意大利", "米兰": "意大利",
    "西班牙": "西班牙", "Spain": "西班牙", "巴塞罗那": "西班牙",
    "澳大利亚": "澳大利亚", "澳洲": "澳大利亚", "Australia": "澳大利亚", "悉尼": "澳大利亚",
    "新西兰": "新西兰", "New Zealand": "新西兰", "奥克兰": "新西兰",
    "阿联酋": "阿联酋", "迪拜": "阿联酋", "UAE": "阿联酋",
    "土耳其": "土耳其", "Turkey": "土耳其", "伊斯坦布尔": "土耳其",
    "俄罗斯": "俄罗斯", "Russia": "俄罗斯", "莫斯科": "俄罗斯",
    "巴西": "巴西", "Brazil": "巴西", "里约": "巴西",
    "墨西哥": "墨西哥", "Mexico": "墨西哥", "坎昆": "墨西哥",
    "埃及": "埃及", "Egypt": "埃及", "开罗": "埃及",
    "南非": "南非", "South Africa": "南非", "开普敦": "南非",
    "瑞士": "瑞士", "Switzerland": "瑞士", "苏黎世": "瑞士",
    "荷兰": "荷兰", "Netherlands": "荷兰", "阿姆斯特丹": "荷兰",
    "希腊": "希腊", "Greece": "希腊", "雅典": "希腊",
    "葡萄牙": "葡萄牙", "Portugal": "葡萄牙", "里斯本": "葡萄牙",
    "捷克": "捷克", "Czech": "捷克", "布拉格": "捷克",
    "爱尔兰": "爱尔兰", "Ireland": "爱尔兰", "都柏林": "爱尔兰",
    "以色列": "以色列", "Israel": "以色列",
    "印度": "印度", "India": "印度",
    "柬埔寨": "柬埔寨", "Cambodia": "柬埔寨", "暹粒": "柬埔寨",
    "菲律宾": "菲律宾", "Philippines": "菲律宾", "马尼拉": "菲律宾",
    "沙特": "沙特阿拉伯", "沙特阿拉伯": "沙特阿拉伯", "Saudi Arabia": "沙特阿拉伯",
}

# ---------- 安全指数数据库 ----------
SAFETY_DB = {
    "日本": {"overall": 9.2, "crime": 9.5, "terror": 9.0, "natural": 7.0, "health": 9.0, "traffic": 8.5, "level": "极安全", "risks": ["地震风险（东京/大阪位于地震带）", "台风季6-10月", "夏季高温中暑"], "tips": ["日本是全球最安全国家之一", "紧急电话110(警察)/119(急救)"], "advisory": "无需特别注意，正常旅行即可"},
    "韩国": {"overall": 8.8, "crime": 8.5, "terror": 8.0, "natural": 8.5, "health": 9.0, "traffic": 8.5, "level": "极安全", "risks": ["朝韩边境局势偶有紧张", "台风季7-9月"], "tips": ["韩国治安良好", "紧急电话112(警察)/119(急救)"], "advisory": "无需特别注意，避开DMZ附近区域即可"},
    "泰国": {"overall": 6.8, "crime": 6.5, "terror": 6.0, "natural": 7.0, "health": 6.5, "traffic": 5.5, "level": "较安全", "risks": ["南部三府恐怖袭击", "交通事故率高", "旅游景点扒窃", "登革热"], "tips": ["主要旅游区安全", "远离南部边境三府", "紧急电话191(警察)/1669(急救)"], "advisory": "旅游区安全，避开南部边境地区，注意交通安全"},
    "新加坡": {"overall": 9.5, "crime": 9.5, "terror": 8.5, "natural": 9.0, "health": 9.5, "traffic": 9.5, "level": "极安全", "risks": ["极低风险", "偶有暴雨"], "tips": ["全球最安全城市之一", "紧急电话999(警察)/995(急救)"], "advisory": "极度安全，正常旅行"},
    "越南": {"overall": 6.5, "crime": 6.0, "terror": 7.5, "natural": 6.5, "health": 6.0, "traffic": 5.0, "level": "较安全", "risks": ["飞车抢夺(胡志明)", "交通事故率高", "食品安全"], "tips": ["背包前背/手机握紧", "喝瓶装水", "紧急电话113(警察)/115(急救)"], "advisory": "旅游区较安全，注意随身物品和交通安全"},
    "马来西亚": {"overall": 7.0, "crime": 6.5, "terror": 6.5, "natural": 7.5, "health": 7.0, "traffic": 6.0, "level": "较安全", "risks": ["东马沙巴沿海绑架风险", "吉隆坡扒窃"], "tips": ["西马安全", "紧急电话999"], "advisory": "西马安全，东马沿海地区注意安全"},
    "印度尼西亚": {"overall": 6.0, "crime": 6.0, "terror": 5.5, "natural": 5.5, "health": 5.5, "traffic": 5.0, "level": "较安全", "risks": ["地震/火山活动", "交通事故", "登革热/疟疾"], "tips": ["巴厘岛主旅游区安全", "注意火山预警", "紧急电话110(警察)/118(急救)"], "advisory": "巴厘岛等旅游区安全，注意自然灾害预警"},
    "柬埔寨": {"overall": 6.0, "crime": 5.5, "terror": 7.0, "natural": 7.0, "health": 5.0, "traffic": 4.5, "level": "较安全", "risks": ["飞车抢夺", "地雷区(偏远地区)", "医疗条件有限"], "tips": ["暹粒/金边主城区安全", "紧急电话117(警察)/119(急救)"], "advisory": "主要旅游区安全，偏远地区注意地雷和医疗条件"},
    "菲律宾": {"overall": 5.5, "crime": 5.0, "terror": 5.0, "natural": 5.5, "health": 5.5, "traffic": 4.5, "level": "注意安全", "risks": ["南部棉兰老岛恐怖袭击/绑架", "台风频发", "马尼拉扒窃/抢劫"], "tips": ["长滩/巴拉望/宿务等旅游区安全", "避开棉兰老岛西部", "紧急电话911"], "advisory": "主要旅游区安全，避开南部高风险地区"},
    "印度": {"overall": 5.0, "crime": 4.5, "terror": 5.0, "natural": 6.0, "health": 4.5, "traffic": 3.5, "level": "注意安全", "risks": ["女性安全风险", "交通安全极差", "食物/水污染"], "tips": ["女性避免夜间独行", "只喝瓶装水", "紧急电话100(警察)/102(急救)"], "advisory": "需高度注意安全，女性旅行者尤其需要防范"},
    "美国": {"overall": 6.5, "crime": 5.5, "terror": 6.0, "natural": 7.0, "health": 7.5, "traffic": 6.5, "level": "较安全", "risks": ["枪击事件(偶发)", "大城市特定区域犯罪率高", "医疗费用极高"], "tips": ["避开高犯罪率区域", "务必购买旅行保险", "紧急电话911"], "advisory": "旅游区安全，需注意特定区域和枪支安全"},
    "加拿大": {"overall": 8.0, "crime": 8.0, "terror": 8.0, "natural": 7.5, "health": 8.5, "traffic": 8.0, "level": "安全", "risks": ["冬季极端严寒", "野生动物(郊区)"], "tips": ["加拿大整体很安全", "紧急电话911"], "advisory": "很安全，注意冬季极端天气"},
    "英国": {"overall": 7.5, "crime": 6.5, "terror": 6.0, "natural": 8.5, "health": 8.5, "traffic": 8.0, "level": "较安全", "risks": ["伦敦扒窃", "恐怖袭击风险", "偶有骚乱/抗议"], "tips": ["伦敦注意随身物品", "紧急电话999/112"], "advisory": "整体安全，大城市注意防盗"},
    "法国": {"overall": 7.0, "crime": 6.0, "terror": 5.5, "natural": 8.5, "health": 8.5, "traffic": 7.5, "level": "较安全", "risks": ["巴黎扒窃/抢劫(地铁/景点)", "恐怖袭击风险", "罢工频繁影响交通"], "tips": ["地铁注意随身物品", "紧急电话17(警察)/15(急救)/112"], "advisory": "整体安全，巴黎需注意扒窃，关注恐袭预警"},
    "德国": {"overall": 7.8, "crime": 7.0, "terror": 6.5, "natural": 9.0, "health": 9.0, "traffic": 8.0, "level": "安全", "risks": ["恐怖袭击风险", "大型车站扒窃"], "tips": ["德国整体很安全", "火车站注意随身物品", "紧急电话110(警察)/112(急救)"], "advisory": "很安全，注意火车站防盗"},
    "意大利": {"overall": 7.0, "crime": 5.5, "terror": 7.0, "natural": 7.5, "health": 8.5, "traffic": 5.5, "level": "较安全", "risks": ["罗马/米兰/那不勒斯扒窃严重", "交通事故"], "tips": ["景点周围注意吉普赛人团伙", "贵重物品贴身携带", "紧急电话112/113(警察)/118(急救)"], "advisory": "整体安全，但扒窃非常普遍需高度警惕"},
    "西班牙": {"overall": 7.0, "crime": 6.0, "terror": 6.5, "natural": 8.0, "health": 8.5, "traffic": 7.0, "level": "较安全", "risks": ["巴塞罗那/马德里扒窃严重", "恐怖袭击风险"], "tips": ["兰布拉大道特别小心", "紧急电话112"], "advisory": "整体安全，扒窃严重需注意"},
    "瑞士": {"overall": 9.0, "crime": 8.5, "terror": 8.0, "natural": 8.0, "health": 9.5, "traffic": 9.0, "level": "极安全", "risks": ["极低风险", "雪崩(滑雪区)", "高山反应"], "tips": ["全球最安全国家之一", "紧急电话117(警察)/144(急救)/112"], "advisory": "极度安全，正常旅行"},
    "荷兰": {"overall": 7.8, "crime": 7.0, "terror": 7.0, "natural": 8.5, "health": 8.5, "traffic": 8.0, "level": "安全", "risks": ["阿姆斯特丹扒窃/自行车盗", "偶有恐袭风险"], "tips": ["注意随身物品", "紧急电话112"], "advisory": "整体很安全，注意阿姆斯特丹防盗"},
    "希腊": {"overall": 7.0, "crime": 6.5, "terror": 7.0, "natural": 7.0, "health": 7.5, "traffic": 6.0, "level": "较安全", "risks": ["雅典扒窃", "夏季高温/山火", "岛屿交通"], "tips": ["景点注意随身物品", "紧急电话100(警察)/166(急救)/112"], "advisory": "整体安全，注意扒窃和高温"},
    "葡萄牙": {"overall": 7.8, "crime": 7.0, "terror": 8.0, "natural": 8.0, "health": 8.0, "traffic": 7.0, "level": "安全", "risks": ["里斯本扒窃", "夏季山火"], "tips": ["整体较安全", "紧急电话112"], "advisory": "整体安全，注意里斯本扒窃"},
    "捷克": {"overall": 7.8, "crime": 7.0, "terror": 7.5, "natural": 8.5, "health": 8.0, "traffic": 7.0, "level": "安全", "risks": ["布拉格扒窃", "偶有出租车宰客"], "tips": ["布拉格景点注意随身物品", "紧急电话158(警察)/155(急救)/112"], "advisory": "整体安全，注意布拉格扒窃"},
    "爱尔兰": {"overall": 8.0, "crime": 7.0, "terror": 8.0, "natural": 8.5, "health": 8.0, "traffic": 7.5, "level": "安全", "risks": ["都柏林扒窃", "偶有骚乱"], "tips": ["整体安全", "紧急电话999/112"], "advisory": "整体安全，注意都柏林防盗"},
    "澳大利亚": {"overall": 8.0, "crime": 7.5, "terror": 8.0, "natural": 7.5, "health": 8.5, "traffic": 7.5, "level": "安全", "risks": ["海洋生物(鲨鱼/水母)", "紫外线极强", "山火(夏季)"], "tips": ["海滩只在红旗/黄旗之间游泳", "涂防晒SPF50+", "紧急电话000"], "advisory": "很安全，注意海洋安全和防晒"},
    "新西兰": {"overall": 8.5, "crime": 8.5, "terror": 9.0, "natural": 7.0, "health": 8.5, "traffic": 7.5, "level": "极安全", "risks": ["地震", "山路交通", "紫外线强"], "tips": ["全球最安全国家之一", "紧急电话111"], "advisory": "极度安全，注意地震和山路驾驶"},
    "阿联酋": {"overall": 8.5, "crime": 9.0, "terror": 7.5, "natural": 9.0, "health": 8.5, "traffic": 7.0, "level": "安全", "risks": ["高温(夏季50°C+)", "严格的法律法规"], "tips": ["迪拜/阿布扎比极度安全", "注意法律差异", "紧急电话999"], "advisory": "非常安全，注意遵守当地法律"},
    "土耳其": {"overall": 6.0, "crime": 6.0, "terror": 5.0, "natural": 6.5, "health": 7.0, "traffic": 5.0, "level": "较安全", "risks": ["恐怖袭击风险(伊斯坦布尔/安卡拉)", "叙利亚边境局势", "地震带"], "tips": ["旅游区安全", "远离叙利亚边境", "紧急电话155(警察)/112(急救)"], "advisory": "旅游区安全，注意恐袭风险和边境地区"},
    "俄罗斯": {"overall": 5.5, "crime": 5.5, "terror": 5.0, "natural": 7.0, "health": 6.0, "traffic": 5.0, "level": "注意安全", "risks": ["恐怖袭击风险", "种族歧视(偶发)", "交通事故", "冬季极端严寒"], "tips": ["莫斯科/圣彼得堡旅游区安全", "夜间避免偏僻区域", "紧急电话102(警察)/103(急救)/112"], "advisory": "大城市旅游区安全，需注意恐怖袭击风险"},
    "巴西": {"overall": 5.0, "crime": 4.0, "terror": 7.0, "natural": 7.0, "health": 5.5, "traffic": 5.0, "level": "注意安全", "risks": ["暴力犯罪率高(里约/圣保罗)", "贫民窟(favela)危险", "登革热/寨卡"], "tips": ["旅游区白天安全", "绝不进入贫民窟", "不佩戴贵重首饰", "紧急电话190(警察)/192(急救)"], "advisory": "需高度注意安全，避免进入危险区域"},
    "墨西哥": {"overall": 5.5, "crime": 4.5, "terror": 6.0, "natural": 7.0, "health": 6.0, "traffic": 5.0, "level": "注意安全", "risks": ["毒品相关暴力(边境城市)", "绑架风险(部分州)", "交通事故", "食品安全"], "tips": ["坎昆/墨西哥城旅游区安全", "避开边境高风险州", "紧急电话911", "旅游警察078"], "advisory": "主要旅游区安全，避开边境和毒品活动区域"},
    "埃及": {"overall": 5.0, "crime": 5.5, "terror": 4.5, "natural": 7.0, "health": 5.0, "traffic": 4.0, "level": "注意安全", "risks": ["恐怖袭击(西奈半岛)", "性骚扰(女性)", "交通事故"], "tips": ["开罗/卢克索/红海度假村旅游区安全", "避开西奈半岛北部", "紧急电话122(警察)/123(急救)"], "advisory": "旅游区有安全保障，需注意性骚扰和交通安全"},
    "南非": {"overall": 5.0, "crime": 4.0, "terror": 6.5, "natural": 7.0, "health": 5.5, "traffic": 5.0, "level": "注意安全", "risks": ["暴力犯罪率高(约堡/开普敦部分区域)", "劫车风险", "HIV/AIDS高发"], "tips": ["旅游区白天安全", "不开车窗给乞丐", "紧急电话10111(警察)/10177(急救)"], "advisory": "需高度注意安全，避免夜间外出和进入危险区域"},
    "以色列": {"overall": 6.0, "crime": 7.0, "terror": 4.5, "natural": 7.5, "health": 8.5, "traffic": 7.0, "level": "较安全", "risks": ["恐怖袭击/火箭弹(偶发)", "巴以冲突影响", "特拉维夫扒窃"], "tips": ["特拉维夫/耶路撒冷旅游区有安保", "关注安全预警", "紧急电话100(警察)/101(急救)"], "advisory": "旅游区有安保，需密切关注安全局势"},
    "沙特阿拉伯": {"overall": 7.0, "crime": 8.0, "terror": 6.5, "natural": 8.5, "health": 7.5, "traffic": 5.5, "level": "较安全", "risks": ["极端高温", "严格法律法规", "交通事故"], "tips": ["利雅得/吉达安全", "注意法律差异(酒精/着装)", "紧急电话999"], "advisory": "治安良好，需严格遵守当地法律和文化规范"},
}

# ---------- 插头电压数据库 ----------
PLUG_DB = {
    "日本": {"plugs": ["A", "B"], "voltage": "100V", "frequency": "50/60Hz", "note": "东部50Hz(东京)，西部60Hz(大阪)，电压全球最低100V", "adapter": "需美标转换器，中国两脚扁插可插A型，三脚需转换器", "need_adapter": True},
    "韩国": {"plugs": ["C", "F"], "voltage": "220V", "frequency": "60Hz", "note": "欧标C/F型，与中国插头不同", "adapter": "需欧标转换器(德标)，中国三脚插头无法插入", "need_adapter": True},
    "泰国": {"plugs": ["A", "B", "C", "O"], "voltage": "220V", "frequency": "50Hz", "note": "新旧标准混杂，A/C型都可插入", "adapter": "中国两脚扁插可直接使用，三脚部分酒店需转换器", "need_adapter": False},
    "新加坡": {"plugs": ["G"], "voltage": "230V", "frequency": "50Hz", "note": "英标G型", "adapter": "需英标转换器(三脚方头)", "need_adapter": True},
    "越南": {"plugs": ["A", "B", "C"], "voltage": "220V", "frequency": "50Hz", "note": "美标和欧标混用", "adapter": "中国两脚扁插可插A型，部分需转换器", "need_adapter": False},
    "马来西亚": {"plugs": ["G"], "voltage": "240V", "frequency": "50Hz", "note": "英标G型为主", "adapter": "需英标转换器", "need_adapter": True},
    "印度尼西亚": {"plugs": ["C", "F"], "voltage": "230V", "frequency": "50Hz", "note": "欧标为主，巴厘岛酒店有万能插座", "adapter": "需欧标转换器", "need_adapter": True},
    "美国": {"plugs": ["A", "B"], "voltage": "120V", "frequency": "60Hz", "note": "美标A/B型，电压120V需注意", "adapter": "中国两脚扁插可插A型，但电压不同注意宽电压设备", "need_adapter": True},
    "加拿大": {"plugs": ["A", "B"], "voltage": "120V", "frequency": "60Hz", "note": "美标，与美国相同", "adapter": "同美国，注意电压120V", "need_adapter": True},
    "英国": {"plugs": ["G"], "voltage": "230V", "frequency": "50Hz", "note": "英标G型，与内地完全不同", "adapter": "需英标转换器", "need_adapter": True},
    "法国": {"plugs": ["C", "E"], "voltage": "230V", "frequency": "50Hz", "note": "法标E型，C型两脚也可插", "adapter": "需欧标转换器(法标)", "need_adapter": True},
    "德国": {"plugs": ["C", "F"], "voltage": "230V", "frequency": "50Hz", "note": "德标F型(舒柯)，C型两脚也可插", "adapter": "需欧标转换器(德标)", "need_adapter": True},
    "意大利": {"plugs": ["C", "F", "L"], "voltage": "230V", "frequency": "50Hz", "note": "意标L型(三脚一字)，C/F型也常见", "adapter": "需欧标转换器(意标L型特殊)", "need_adapter": True},
    "西班牙": {"plugs": ["C", "F"], "voltage": "230V", "frequency": "50Hz", "note": "德标F型为主", "adapter": "需欧标转换器(德标)", "need_adapter": True},
    "澳大利亚": {"plugs": ["I"], "voltage": "230V", "frequency": "50Hz", "note": "澳标I型(与中标形状相同)", "adapter": "中国三脚插头可直接使用(形状相同)", "need_adapter": False},
    "新西兰": {"plugs": ["I"], "voltage": "230V", "frequency": "50Hz", "note": "澳标I型", "adapter": "中国三脚插头可直接使用", "need_adapter": False},
    "阿联酋": {"plugs": ["C", "D", "G"], "voltage": "230V", "frequency": "50Hz", "note": "英标G型为主，迪拜酒店有万能插座", "adapter": "需英标转换器", "need_adapter": True},
    "土耳其": {"plugs": ["C", "F"], "voltage": "230V", "frequency": "50Hz", "note": "德标为主", "adapter": "需欧标转换器(德标)", "need_adapter": True},
    "俄罗斯": {"plugs": ["C", "F"], "voltage": "220V", "frequency": "50Hz", "note": "德标为主", "adapter": "需欧标转换器(德标)", "need_adapter": True},
    "巴西": {"plugs": ["C", "N"], "voltage": "127/240V", "frequency": "60Hz", "note": "电压因城市而异！圣保罗127V/里约127V/巴西利亚240V", "adapter": "需万能转换器，注意电压因城市不同", "need_adapter": True},
    "墨西哥": {"plugs": ["A", "B"], "voltage": "127V", "frequency": "60Hz", "note": "美标为主，部分老建筑电压不稳", "adapter": "同美国，注意电压127V", "need_adapter": True},
    "埃及": {"plugs": ["C", "F"], "voltage": "220V", "frequency": "50Hz", "note": "德标为主", "adapter": "需欧标转换器(德标)", "need_adapter": True},
    "南非": {"plugs": ["C", "D", "M", "N"], "voltage": "230V", "frequency": "50Hz", "note": "M型(大三脚)为主，新建筑N型增多", "adapter": "需南非专用转换器(大三脚)", "need_adapter": True},
    "瑞士": {"plugs": ["C", "J"], "voltage": "230V", "frequency": "50Hz", "note": "瑞士标J型，与邻国不同", "adapter": "需瑞士专用转换器(J型)", "need_adapter": True},
    "荷兰": {"plugs": ["C", "F"], "voltage": "230V", "frequency": "50Hz", "note": "德标为主", "adapter": "需欧标转换器(德标)", "need_adapter": True},
    "希腊": {"plugs": ["C", "F"], "voltage": "230V", "frequency": "50Hz", "note": "德标为主", "adapter": "需欧标转换器(德标)", "need_adapter": True},
    "葡萄牙": {"plugs": ["C", "F"], "voltage": "230V", "frequency": "50Hz", "note": "德标为主", "adapter": "需欧标转换器(德标)", "need_adapter": True},
    "捷克": {"plugs": ["C", "E"], "voltage": "230V", "frequency": "50Hz", "note": "法标为主", "adapter": "需欧标转换器(法标)", "need_adapter": True},
    "爱尔兰": {"plugs": ["G"], "voltage": "230V", "frequency": "50Hz", "note": "英标", "adapter": "需英标转换器", "need_adapter": True},
    "以色列": {"plugs": ["C", "H"], "voltage": "230V", "frequency": "50Hz", "note": "以色列标H型", "adapter": "需以色列专用转换器(H型)", "need_adapter": True},
    "印度": {"plugs": ["C", "D", "M"], "voltage": "230V", "frequency": "50Hz", "note": "D型(粗三脚)和M型为主", "adapter": "需印度标转换器(D/M型)", "need_adapter": True},
    "柬埔寨": {"plugs": ["A", "B", "C"], "voltage": "230V", "frequency": "50Hz", "note": "美标欧标混用", "adapter": "中国两脚扁插可插A型", "need_adapter": False},
    "菲律宾": {"plugs": ["A", "B", "C"], "voltage": "220V", "frequency": "60Hz", "note": "美标为主", "adapter": "中国两脚扁插可插A型", "need_adapter": False},
    "沙特阿拉伯": {"plugs": ["A", "B", "G"], "voltage": "230V", "frequency": "60Hz", "note": "多种标准混用，酒店以G型为主", "adapter": "建议带英标转换器", "need_adapter": True},
}

# ---------- 紧急求助数据库 ----------
EMERGENCY_DB = {
    "日本": {"police": "110", "ambulance": "119", "fire": "119", "note": "报警110，消防急救119"},
    "韩国": {"police": "112", "ambulance": "119", "fire": "119"},
    "泰国": {"police": "191", "ambulance": "1669", "tourist_police": "1155", "note": "旅游警察1155可中文服务"},
    "新加坡": {"police": "999", "ambulance": "995", "fire": "995"},
    "越南": {"police": "113", "ambulance": "115", "fire": "114"},
    "马来西亚": {"police": "999", "ambulance": "999", "fire": "994", "tourist_police": "03-2149 6590"},
    "印度尼西亚": {"police": "110", "ambulance": "118", "fire": "113"},
    "柬埔寨": {"police": "117", "ambulance": "119", "tourist_police": "012-942 484"},
    "菲律宾": {"police": "117", "ambulance": "911", "fire": "117"},
    "印度": {"police": "100", "ambulance": "102", "fire": "101", "women_helpline": "1091"},
    "沙特阿拉伯": {"police": "999", "ambulance": "997", "fire": "998"},
    "美国": {"police": "911", "ambulance": "911", "fire": "911", "note": "统一911"},
    "加拿大": {"police": "911", "ambulance": "911", "fire": "911"},
    "英国": {"police": "999", "ambulance": "999", "fire": "999", "non_emergency": "101"},
    "法国": {"police": "17", "ambulance": "15", "fire": "18", "eu_emergency": "112"},
    "德国": {"police": "110", "ambulance": "112", "fire": "112"},
    "意大利": {"police": "113", "ambulance": "118", "fire": "115", "carabinieri": "112"},
    "西班牙": {"police": "091", "ambulance": "061", "fire": "080", "eu_emergency": "112"},
    "瑞士": {"police": "117", "ambulance": "144", "fire": "118", "eu_emergency": "112"},
    "荷兰": {"police": "112", "ambulance": "112", "fire": "112", "non_emergency": "0900-8844"},
    "希腊": {"police": "100", "ambulance": "166", "fire": "199", "eu_emergency": "112"},
    "葡萄牙": {"police": "112", "ambulance": "112", "fire": "112"},
    "捷克": {"police": "158", "ambulance": "155", "fire": "150", "unified": "112"},
    "爱尔兰": {"police": "999", "ambulance": "999", "fire": "999", "eu_emergency": "112"},
    "澳大利亚": {"police": "000", "ambulance": "000", "fire": "000", "note": "统一000"},
    "新西兰": {"police": "111", "ambulance": "111", "fire": "111"},
    "阿联酋": {"police": "999", "ambulance": "998", "fire": "997"},
    "土耳其": {"police": "155", "ambulance": "112", "fire": "110", "tourist_police": "0212-527 4503"},
    "俄罗斯": {"police": "102", "ambulance": "103", "fire": "101", "unified": "112"},
    "巴西": {"police": "190", "ambulance": "192", "fire": "193"},
    "墨西哥": {"police": "911", "ambulance": "911", "fire": "911", "tourist_police": "078"},
    "埃及": {"police": "122", "ambulance": "123", "tourist_police": "126"},
    "南非": {"police": "10111", "ambulance": "10177", "cellphone": "112"},
    "以色列": {"police": "100", "ambulance": "101", "fire": "102"},
}

EMBASSY_DB = {
    "日本": {"name": "中国驻日本大使馆", "phone": "+81-3-34033380", "duty": "+81-3-34033380", "consulates": [{"city": "大阪", "phone": "+81-6-64459481"}, {"city": "名古屋", "phone": "+81-52-9321098"}, {"city": "札幌", "phone": "+81-11-5635563"}, {"city": "福冈", "phone": "+81-92-7520088"}]},
    "韩国": {"name": "中国驻韩国大使馆", "phone": "+82-2-7381038", "duty": "+82-2-7550572", "consulates": [{"city": "釜山", "phone": "+82-51-7430725"}, {"city": "济州", "phone": "+82-64-7228803"}]},
    "泰国": {"name": "中国驻泰国大使馆", "phone": "+66-2-2450088", "duty": "+66-2-2457010", "consulates": [{"city": "清迈", "phone": "+66-53-280380"}, {"city": "宋卡", "phone": "+66-74-322034"}]},
    "新加坡": {"name": "中国驻新加坡大使馆", "phone": "+65-64750165", "duty": "+65-64750165"},
    "马来西亚": {"name": "中国驻马来西亚大使馆", "phone": "+60-3-21428495", "duty": "+60-3-21636812", "consulates": [{"city": "槟城", "phone": "+60-4-2634488"}, {"city": "古晋", "phone": "+60-82-453344"}]},
    "越南": {"name": "中国驻越南大使馆", "phone": "+84-24-38453736", "duty": "+84-24-38453736", "consulates": [{"city": "胡志明市", "phone": "+84-28-38292457"}, {"city": "岘港", "phone": "+84-236-3821655"}]},
    "印度尼西亚": {"name": "中国驻印度尼西亚大使馆", "phone": "+62-21-5764139", "duty": "+62-21-5764139", "consulates": [{"city": "泗水", "phone": "+62-31-5675383"}, {"city": "登巴萨(巴厘岛)", "phone": "+62-361-285017"}]},
    "柬埔寨": {"name": "中国驻柬埔寨大使馆", "phone": "+855-12-901923", "duty": "+855-12-901923"},
    "菲律宾": {"name": "中国驻菲律宾大使馆", "phone": "+63-2-88442148", "duty": "+63-2-88442148"},
    "印度": {"name": "中国驻印度大使馆", "phone": "+91-11-26112345", "duty": "+91-11-26112345", "consulates": [{"city": "孟买", "phone": "+91-22-66320803"}]},
    "美国": {"name": "中国驻美国大使馆", "phone": "+1-202-4952216", "duty": "+1-202-4952216", "consular": "+1-202-8551555", "consulates": [{"city": "纽约", "phone": "+1-212-2449392"}, {"city": "旧金山", "phone": "+1-415-8525924"}, {"city": "洛杉矶", "phone": "+1-213-8068088"}, {"city": "芝加哥", "phone": "+1-312-8059838"}]},
    "加拿大": {"name": "中国驻加拿大大使馆", "phone": "+1-613-7893434", "duty": "+1-613-7893434", "consulates": [{"city": "多伦多", "phone": "+1-416-9647260"}, {"city": "温哥华", "phone": "+1-604-7365188"}]},
    "英国": {"name": "中国驻英国大使馆", "phone": "+44-20-72994049", "duty": "+44-20-72994049", "consulates": [{"city": "曼彻斯特", "phone": "+44-161-2247473"}, {"city": "爱丁堡", "phone": "+44-131-3373220"}]},
    "法国": {"name": "中国驻法国大使馆", "phone": "+33-1-49521950", "duty": "+33-1-49521950", "consulates": [{"city": "马赛", "phone": "+33-4-91320000"}, {"city": "里昂", "phone": "+33-4-78946400"}]},
    "德国": {"name": "中国驻德国大使馆", "phone": "+49-30-275880", "duty": "+49-30-27588221", "consulates": [{"city": "汉堡", "phone": "+49-40-82276013"}, {"city": "慕尼黑", "phone": "+49-89-17301618"}, {"city": "法兰克福", "phone": "+49-69-75085500"}]},
    "意大利": {"name": "中国驻意大利大使馆", "phone": "+39-06-96524200", "duty": "+39-06-96524200", "consulates": [{"city": "米兰", "phone": "+39-02-5694069"}, {"city": "佛罗伦萨", "phone": "+39-055-5058188"}]},
    "西班牙": {"name": "中国驻西班牙大使馆", "phone": "+34-91-5194242", "duty": "+34-91-5194242", "consulates": [{"city": "巴塞罗那", "phone": "+34-93-2541199"}]},
    "澳大利亚": {"name": "中国驻澳大利亚大使馆", "phone": "+61-2-62734780", "duty": "+61-2-62283948", "consulates": [{"city": "悉尼", "phone": "+61-2-85958002"}, {"city": "墨尔本", "phone": "+61-3-98043271"}, {"city": "珀斯", "phone": "+61-8-92220333"}]},
    "新西兰": {"name": "中国驻新西兰大使馆", "phone": "+64-4-4721382", "duty": "+64-4-4721382", "consulates": [{"city": "奥克兰", "phone": "+64-9-5268682"}]},
    "阿联酋": {"name": "中国驻阿联酋大使馆", "phone": "+971-2-4434276", "duty": "+971-2-4434276", "consulates": [{"city": "迪拜", "phone": "+971-4-3944733"}]},
    "土耳其": {"name": "中国驻土耳其大使馆", "phone": "+90-312-4360628", "duty": "+90-312-4360628", "consulates": [{"city": "伊斯坦布尔", "phone": "+90-212-2992188"}]},
    "俄罗斯": {"name": "中国驻俄罗斯大使馆", "phone": "+7-495-9561168", "duty": "+7-495-9561168", "consulates": [{"city": "圣彼得堡", "phone": "+7-812-7146230"}, {"city": "哈巴罗夫斯克", "phone": "+7-4212-302590"}, {"city": "伊尔库茨克", "phone": "+7-3952-781442"}]},
    "巴西": {"name": "中国驻巴西大使馆", "phone": "+55-61-21958200", "duty": "+55-61-99631988", "consulates": [{"city": "圣保罗", "phone": "+55-11-30626165"}, {"city": "里约热内卢", "phone": "+55-21-32376612"}]},
    "埃及": {"name": "中国驻埃及大使馆", "phone": "+20-2-27361219", "duty": "+20-2-27361219"},
    "南非": {"name": "中国驻南非大使馆", "phone": "+27-12-4316500", "duty": "+27-12-4316500", "consulates": [{"city": "约翰内斯堡", "phone": "+27-11-8835073"}, {"city": "开普敦", "phone": "+27-21-6740059"}]},
    "以色列": {"name": "中国驻以色列大使馆", "phone": "+972-3-5442639", "duty": "+972-3-5442639"},
}

EMERGENCY_GUIDES = {
    "passport_lost": {"name": "护照丢失", "steps": ["1. 立即报警获取报案记录", "2. 联系中国驻当地使领馆领保电话", "3. 准备材料：护照复印件/照片+报案记录+证件照2张+申请表", "4. 前往使领馆办理旅行证(1-4工作日，加急可当天)", "5. 通知旅行保险公司报案"], "tips": ["出国前拍下护照信息页存手机和云端", "旅行证可替代护照回国，不可用于第三国签证", "外交部全球领保热线：+86-10-12308"]},
    "flight_cancel": {"name": "航班取消/延误", "steps": ["1. 确认航班最新状态", "2. 了解权利：航司原因→免费改签+可能补偿；天气原因→免费改签无额外补偿", "3. 立即通过航司APP/柜台改签", "4. 如需过夜：航司原因航司提供住宿；天气原因通常自理", "5. 联系旅行保险报案(延误4小时起赔)"], "tips": ["EU261条款：从EU出发航班取消/延误3h+可获€250-600补偿", "保留所有票据和截图用于理赔"]},
    "medical": {"name": "突发疾病/受伤", "steps": ["1. 拨打当地急救电话", "2. 说明情况：I need help, I'm at [地址], [症状]", "3. 联系保险公司24小时救援热线", "4. 前往保险公司合作医院(如自费就医保留所有单据)", "5. 保留理赔材料：病历+收据+处方+诊断书"], "tips": ["欧美医疗费极贵：美国急诊$2000+起，务必确认保险覆盖", "出国前准备：常用药+英文说明书、过敏史英文卡片"]},
    "theft": {"name": "被盗/被抢", "steps": ["1. 确保人身安全，不要与劫匪对抗", "2. 报警获取报案记录(保险理赔必须)", "3. 挂失银行卡和手机", "4. 如护照被盗参考「护照丢失」流程", "5. 48小时内联系保险公司报案"], "tips": ["常见被盗场景：巴黎地铁、罗马景点、巴塞罗那兰布拉大道", "防盗：贵重物品分放、背包前背、酒店保险箱存护照原件"]},
    "natural_disaster": {"name": "自然灾害/极端天气", "steps": ["1. 关注官方预警", "2. 前往安全地带：地震→空旷地 台风→室内远离窗 洪水→高处 海啸→内陆高处", "3. 联系使领馆报平安", "4. 调整行程联系航司/酒店", "5. 保险理赔(自然灾害通常在承保范围)"], "tips": ["下载当地应急APP：日本Yurekuru Call(地震预警)", "外交部领事直通车微信公众号可接收安全提醒"]},
    "traffic": {"name": "交通事故", "steps": ["1. 确保安全+检查伤情", "2. 报警(海外事故必须报警，无交警报告保险可能拒赔)", "3. 记录现场：拍照+对方信息+目击者联系方式", "4. 联系租车公司(如适用)", "5. 联系保险理赔"], "tips": ["海外自驾务必购买全险(含第三者责任险)", "部分国家靠左行驶(泰国/澳/新/英/日/印度)"]},
    "legal": {"name": "法律纠纷/被捕", "steps": ["1. 保持冷静配合执法，不要签署看不懂的文件", "2. 要求联系中国使领馆(领事探视权)", "3. 聘请当地律师(使领馆可提供律师名单)", "4. 通知家人安排律师费", "5. 了解当地法律(常见陷阱：新加坡禁口香糖、阿联酋公共场所禁酒)"], "tips": ["不要替陌生人携带行李或包裹", "使领馆不能：干预司法、支付律师费、安排保释金"]},
}

# ---------- 退税数据库 ----------
TAX_REFUND_DB = {
    "日本": {"currency": "JPY", "symbol": "¥", "vat_rate": 10, "min_purchase": 5000, "refund_rate": 10, "deduction": 0, "method": "免税店直接免税", "notes": "同日同店满5000日元即可免税。消耗品需密封不可拆封直到离境。", "steps": ["购物时出示护照", "店员直接扣除税金", "消耗品密封包装不可拆封直到离境", "离境时海关可能查验"]},
    "韩国": {"currency": "KRW", "symbol": "₩", "vat_rate": 10, "min_purchase": 15000, "refund_rate": 8.5, "deduction": 1.5, "method": "免税店直接免税/市区退税/机场退税", "notes": "满15000韩元即可退税，手续费约1-2%。首尔市区有自助退税机。", "steps": ["免税店直接免税", "普通店索要退税单", "机场自助退税机或柜台退税", "或市区退税点办理"]},
    "泰国": {"currency": "THB", "symbol": "฿", "vat_rate": 7, "min_purchase": 2000, "refund_rate": 5.5, "deduction": 1.5, "method": "机场退税", "notes": "同店同日消费满2000泰铢可开退税单，退税手续费100泰铢。", "steps": ["购物时索取PP10退税表", "同日同店累计满2000铢", "离境时先海关盖章", "过安检后退税柜台领钱"]},
    "新加坡": {"currency": "SGD", "symbol": "S$", "vat_rate": 9, "min_purchase": 100, "refund_rate": 7.5, "deduction": 1.5, "method": "eTRS电子退税/机场退税", "notes": "GST从8%升至9%(2024年)。eTRS电子退税系统便捷。", "steps": ["购物时出示护照，开具eTRS单", "樟宜机场自助退税机扫描", "选择退款方式(信用卡/支付宝/现金)", "贵重物品海关可能查验"]},
    "法国": {"currency": "EUR", "symbol": "€", "vat_rate": 20, "min_purchase": 100, "refund_rate": 12, "deduction": 8, "method": "PABLO电子退税/机场退税", "notes": "税率20%为欧洲最高之一，退税后实际到手约12%。满100欧元即可退税。", "steps": ["购物时索要退税单(PABLO)", "机场PABLO自助机扫描", "过安检后退税柜台领钱", "或选择信用卡/支付宝退款"]},
    "意大利": {"currency": "EUR", "symbol": "€", "vat_rate": 22, "min_purchase": 154, "refund_rate": 13, "deduction": 9, "method": "机场退税/市区退税", "notes": "税率22%欧盟最高，实际到手约13%。", "steps": ["购物时索要退税单", "机场海关盖章", "过安检后Global Blue/Planet柜台退税", "市区退税点可提前拿到现金"]},
    "德国": {"currency": "EUR", "symbol": "€", "vat_rate": 19, "min_purchase": 50, "refund_rate": 11, "deduction": 8, "method": "机场退税", "notes": "起退点低(50欧)，适合小额购物退税。", "steps": ["购物时索要Tax Free单", "机场海关盖章", "过安检后退税柜台办理"]},
    "西班牙": {"currency": "EUR", "symbol": "€", "vat_rate": 21, "min_purchase": 90, "refund_rate": 12, "deduction": 9, "method": "DIVA电子退税/机场退税", "notes": "税率21%，DIVA电子退税在马德里/巴塞罗那可用。", "steps": ["购物时索要退税单", "DIVA自助机扫描或海关盖章", "过安检后退税柜台办理"]},
    "英国": {"currency": "GBP", "symbol": "£", "vat_rate": 20, "min_purchase": 0, "refund_rate": 0, "deduction": 0, "method": "已取消退税", "notes": "英国已于2021年取消离境退税。国际旅客在英国购物不再享受VAT退税。", "steps": ["英国已无退税政策"]},
    "瑞士": {"currency": "CHF", "symbol": "CHF", "vat_rate": 8.1, "min_purchase": 300, "refund_rate": 5.5, "deduction": 2.6, "method": "机场退税", "notes": "税率低(8.1%)，起退点高(300CHF)。瑞士非欧盟，与欧盟国家分开退税。", "steps": ["购物时索要退税单", "瑞士海关盖章(非欧盟海关)", "过安检后退税柜台办理"]},
    "阿联酋": {"currency": "AED", "symbol": "د.إ", "vat_rate": 5, "min_purchase": 250, "refund_rate": 4.0, "deduction": 1.0, "method": "Planet退税/机场退税", "notes": "税率仅5%，退税金额有限但流程简单。", "steps": ["购物时索要退税单", "机场自助机扫描Planet退税单", "选择退款方式"]},
    "澳大利亚": {"currency": "AUD", "symbol": "A$", "vat_rate": 10, "min_purchase": 300, "refund_rate": 8.5, "deduction": 1.5, "method": "TRS机场退税", "notes": "离境前60天内同一商家消费满300澳元可退GST。TRS支持网上预申报。", "steps": ["购物时保留发票", "TRS网上预申报(app)", "机场TRS柜台出示商品和发票", "退到信用卡/澳洲银行账户"]},
    "美国": {"currency": "USD", "symbol": "$", "vat_rate": 0, "min_purchase": 0, "refund_rate": 0, "deduction": 0, "method": "无退税", "notes": "美国没有联邦VAT退税政策。国际旅客无法退消费税。部分州(如Oregon)本身无消费税。", "steps": ["美国无退税政策"]},
    "加拿大": {"currency": "CAD", "symbol": "C$", "vat_rate": 5, "min_purchase": 0, "refund_rate": 0, "deduction": 5, "method": "已取消退税", "notes": "加拿大2007年取消访客退税计划。", "steps": ["加拿大已无退税政策"]},
    "俄罗斯": {"currency": "RUB", "symbol": "₽", "vat_rate": 20, "min_purchase": 10000, "refund_rate": 12, "deduction": 8, "method": "tax free退税", "notes": "俄罗斯2018年起实行Tax Free退税，需在同店消费满10000卢布。", "steps": ["在同店消费满10000卢布", "索要Tax Free退税单", "离境时海关盖章", "退税柜台办理"]},
    "土耳其": {"currency": "TRY", "symbol": "₺", "vat_rate": 20, "min_purchase": 100, "refund_rate": 12, "deduction": 8, "method": "Global Blue/Planet退税", "notes": "税率20%，实际到手约12%。满100里拉即可退税。", "steps": ["购物时索要退税单", "机场海关盖章", "过安检后退税柜台办理"]},
}

# ============================================================
# 工具函数
# ============================================================

def _resolve_visa_dest(dest):
    """解析签证目的地"""
    if dest in VISA_DB:
        return dest
    if dest in VISA_ALIAS:
        mapped = VISA_ALIAS[dest]
        if mapped in VISA_DB:
            return mapped
    for key in VISA_DB:
        if dest in key or key in dest:
            return key
    for key, data in VISA_DB.items():
        if data.get("en", "").lower() == dest.lower():
            return key
    return ""

def _resolve_safety_dest(dest):
    """解析安全目的地"""
    if dest in SAFETY_DB:
        return dest
    for key in SAFETY_DB:
        if dest in key or key in dest:
            return key
    return ""

def _resolve_plug_dest(dest):
    """解析插头目的地"""
    if dest in PLUG_DB:
        return dest
    for key in PLUG_DB:
        if dest in key or key in dest:
            return key
    return ""

def _resolve_emergency_dest(dest):
    """解析紧急求助目的地"""
    if dest in EMERGENCY_DB:
        return dest
    if dest in VISA_ALIAS:
        mapped = VISA_ALIAS[dest]
        if mapped in EMERGENCY_DB:
            return mapped
    for key in EMERGENCY_DB:
        if dest in key or key in dest:
            return key
    return ""

def _resolve_tax_dest(dest):
    """解析退税目的地"""
    if dest in TAX_REFUND_DB:
        return dest
    for key in TAX_REFUND_DB:
        if dest in key or key in dest:
            return key
    return ""

def _resolve_emergency_type(etype):
    """匹配紧急场景类型"""
    keywords = {
        "passport_lost": ["护照", "passport", "丢护照", "证件丢", "旅行证"],
        "flight_cancel": ["航班", "flight", "取消", "cancel", "延误", "delay"],
        "medical": ["疾病", "medical", "生病", "医院", "急救", "受伤", "中暑"],
        "theft": ["被盗", "theft", "被偷", "抢劫", "robbery", "钱包"],
        "natural_disaster": ["台风", "地震", "洪水", "海啸", "自然灾害", "极端天气"],
        "traffic": ["车祸", "accident", "交通事故", "撞车", "自驾"],
        "legal": ["被捕", "arrest", "拘留", "法律", "legal", "律师"],
    }
    best = None
    best_score = 0
    for scenario, kws in keywords.items():
        score = sum(1 for kw in kws if kw in etype.lower())
        if score > best_score:
            best_score = score
            best = scenario
    return best


# ============================================================
# 工具6: check_visa
# ============================================================
def check_visa(destination="", purpose="tourism", **kwargs):
    """签证查询"""
    if not destination:
        return json.dumps({"error": "请提供destination(目的地)"}, ensure_ascii=False)
    dest_key = _resolve_visa_dest(destination)
    if not dest_key:
        return json.dumps({"error": f"未找到「{destination}」的签证信息", "supported": list(VISA_DB.keys())}, ensure_ascii=False)
    data = VISA_DB[dest_key]
    purpose_data = data["visa_types"].get(purpose, data["visa_types"].get("tourism", {}))
    result = {
        "destination": dest_key,
        "destination_en": data.get("en", ""),
        "purpose": purpose,
        "visa_type": purpose_data.get("type", ""),
        "max_stay": f"{purpose_data.get('max_stay', 'N/A')}天",
        "visa_fee": f"¥{purpose_data.get('visa_fee', 0)}" if purpose_data.get('visa_fee', 0) > 0 else "免费",
        "processing_time": f"{purpose_data.get('processing_time', 0)}个工作日" if purpose_data.get('processing_time', 0) > 0 else "无需等待",
        "entry_count": purpose_data.get("entry_count", ""),
        "notes": purpose_data.get("notes", ""),
        "evisa_url": purpose_data.get("evisa_url", ""),
        "photo_spec": data.get("photo_spec", ""),
        "checklist_tips": data.get("checklist_tips", ""),
        "disclaimer": "⚠️ 签证政策随时变动，请以目的地使领馆最新公告为准",
    }
    return json.dumps(result, ensure_ascii=False, indent=2)


# ============================================================
# 工具7: check_safety
# ============================================================
def check_safety(destination="", **kwargs):
    """目的地安全评级"""
    if not destination:
        return json.dumps({"error": "请提供destination(目的地)"}, ensure_ascii=False)
    dest_key = _resolve_safety_dest(destination)
    if not dest_key:
        return json.dumps({"error": f"未找到「{destination}」的安全评级", "supported": list(SAFETY_DB.keys())}, ensure_ascii=False)
    d = SAFETY_DB[dest_key]
    result = {
        "destination": dest_key,
        "overall_score": d["overall"],
        "level": d["level"],
        "dimensions": {
            "犯罪安全": d["crime"],
            "恐怖袭击": d["terror"],
            "自然灾害": d["natural"],
            "健康卫生": d["health"],
            "交通安全": d["traffic"],
        },
        "risks": d["risks"],
        "tips": d["tips"],
        "advisory": d["advisory"],
        "disclaimer": "数据来源：Global Peace Index/US DOS/FCDO等，仅供参考",
    }
    return json.dumps(result, ensure_ascii=False, indent=2)


# ============================================================
# 工具8: check_plug
# ============================================================
def check_plug(destination="", **kwargs):
    """插头电压查询"""
    if not destination:
        return json.dumps({"error": "请提供destination(目的地)"}, ensure_ascii=False)
    dest_key = _resolve_plug_dest(destination)
    if not dest_key:
        return json.dumps({"error": f"未找到「{destination}」的插头信息", "supported": list(PLUG_DB.keys())}, ensure_ascii=False)
    d = PLUG_DB[dest_key]
    result = {
        "destination": dest_key,
        "plug_types": d["plugs"],
        "voltage": d["voltage"],
        "frequency": d["frequency"],
        "note": d["note"],
        "need_adapter": d["need_adapter"],
        "adapter_recommendation": d["adapter"],
    }
    return json.dumps(result, ensure_ascii=False, indent=2)


# ============================================================
# 工具9: emergency_help
# ============================================================
def emergency_help(destination="", emergency_type="", **kwargs):
    """紧急求助"""
    if not destination and not emergency_type:
        return json.dumps({"error": "请提供destination(目的地)或emergency_type(紧急类型)"}, ensure_ascii=False)
    result = {}
    # 目的地紧急电话
    if destination:
        dest_key = _resolve_emergency_dest(destination)
        if dest_key:
            numbers = EMERGENCY_DB[dest_key]
            result["destination"] = dest_key
            result["emergency_numbers"] = numbers
            # 使领馆
            if dest_key in EMBASSY_DB:
                emb = EMBASSY_DB[dest_key]
                result["embassy"] = {
                    "name": emb["name"],
                    "duty_phone": emb.get("duty", emb["phone"]),
                    "consulates": emb.get("consulates", []),
                }
        else:
            result["emergency_numbers"] = f"未找到「{destination}」的紧急电话"
    # 紧急场景指南
    if emergency_type:
        etype = _resolve_emergency_type(emergency_type)
        if etype and etype in EMERGENCY_GUIDES:
            guide = EMERGENCY_GUIDES[etype]
            result["scenario"] = guide["name"]
            result["steps"] = guide["steps"]
            result["tips"] = guide["tips"]
        elif emergency_type in EMERGENCY_GUIDES:
            guide = EMERGENCY_GUIDES[emergency_type]
            result["scenario"] = guide["name"]
            result["steps"] = guide["steps"]
            result["tips"] = guide["tips"]
        else:
            result["scenario"] = f"未识别场景「{emergency_type}」"
            result["available_types"] = list(EMERGENCY_GUIDES.keys())
    # 始终附带全球领保热线
    result["global_hotline"] = "+86-10-12308 / +86-10-65612308"
    return json.dumps(result, ensure_ascii=False, indent=2)


# ============================================================
# 工具10: calc_tax_refund
# ============================================================
def calc_tax_refund(destination="", amount="", currency="", **kwargs):
    """退税计算"""
    if not destination or not amount:
        return json.dumps({"error": "请提供destination(目的地)和amount(购物金额)"}, ensure_ascii=False)
    dest_key = _resolve_tax_dest(destination)
    if not dest_key:
        # 尝试从签证数据库匹配
        dest_key = _resolve_visa_dest(destination)
        if dest_key and dest_key in TAX_REFUND_DB:
            pass
        else:
            return json.dumps({"error": f"未找到「{destination}」的退税信息", "supported": list(TAX_REFUND_DB.keys())}, ensure_ascii=False)
    c = TAX_REFUND_DB[dest_key]
    # 无退税国家
    if c["refund_rate"] == 0:
        return json.dumps({
            "destination": dest_key,
            "status": "no_refund",
            "message": c["notes"],
            "method": c["method"],
        }, ensure_ascii=False, indent=2)
    try:
        amt = float(amount)
    except (ValueError, TypeError):
        return json.dumps({"error": "金额必须为数字"}, ensure_ascii=False)
    local_amount = amt
    vat_amount = local_amount * c["vat_rate"] / 100
    fee = local_amount * c["deduction"] / 100
    refund = local_amount * c["refund_rate"] / 100
    is_eligible = local_amount >= c["min_purchase"]
    result = {
        "destination": dest_key,
        "currency": c["currency"],
        "purchase_amount": local_amount,
        "vat_rate": f"{c['vat_rate']}%",
        "vat_amount": round(vat_amount, 2),
        "refund_rate": f"{c['refund_rate']}%",
        "deduction_fee": round(fee, 2),
        "actual_refund": round(refund, 2),
        "is_eligible": is_eligible,
        "min_purchase": c["min_purchase"],
        "method": c["method"],
        "steps": c["steps"],
        "notes": c["notes"],
        "disclaimer": "退税金额为估算，实际以退税公司为准",
    }
    if not is_eligible:
        result["gap"] = c["min_purchase"] - local_amount
        result["message"] = f"未达到起退金额{c['min_purchase']}{c['symbol']}，还差{result['gap']:.0f}{c['symbol']}"
    return json.dumps(result, ensure_ascii=False, indent=2)


# ============================================================
# 工具11: exchange_rate
# ============================================================
def exchange_rate(from_currency="", to_currency="", amount="1", **kwargs):
    """实时汇率换算"""
    if not from_currency or not to_currency:
        return json.dumps({"error": "请提供from_currency(源币种)和to_currency(目标币种)，如USD, CNY, JPY等"}, ensure_ascii=False)
    try:
        amt = float(amount)
    except (ValueError, TypeError):
        return json.dumps({"error": "amount必须为数字"}, ensure_ascii=False)
    url = f"https://open.er-api.com/v6/latest/{from_currency.upper()}"
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        return json.dumps({"error": f"汇率查询失败: {e}"}, ensure_ascii=False)
    if data.get("result") != "success":
        return json.dumps({"error": "汇率API返回错误", "raw": data}, ensure_ascii=False)
    rates = data.get("rates", {})
    to_upper = to_currency.upper()
    if to_upper not in rates:
        return json.dumps({"error": f"不支持目标币种{to_upper}", "available": list(rates.keys())[:20]}, ensure_ascii=False)
    rate = rates[to_upper]
    converted = round(amt * rate, 4)
    result = {
        "from": from_currency.upper(),
        "to": to_upper,
        "rate": rate,
        "amount": amt,
        "converted": converted,
        "update_time": data.get("time_last_update_utc", ""),
        "disclaimer": "汇率实时波动，换算结果仅供参考",
    }
    return json.dumps(result, ensure_ascii=False, indent=2)


# ============================================================
# 工具注册表和主入口
# ============================================================
TOOLS = {
    "search_flights": search_flights,
    "search_hotels": search_hotels,
    "flight_seats": flight_seats,
    "flight_baggage": flight_baggage,
    "hotel_detail": hotel_detail,
    "check_visa": check_visa,
    "check_safety": check_safety,
    "check_plug": check_plug,
    "emergency_help": emergency_help,
    "calc_tax_refund": calc_tax_refund,
    "exchange_rate": exchange_rate,
}


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"用法: python outbound_travel_assistant.py <tool_name> [key=value ...]")
        print(f"可用工具: {', '.join(TOOLS.keys())}")
        sys.exit(1)
    tool_name = sys.argv[1]
    if tool_name not in TOOLS:
        print(f"未知工具: {tool_name}")
        print(f"可用工具: {', '.join(TOOLS.keys())}")
        sys.exit(1)
    kwargs = {}
    for arg in sys.argv[2:]:
        if "=" in arg:
            k, v = arg.split("=", 1)
            kwargs[k] = v
    print(TOOLS[tool_name](**kwargs))
