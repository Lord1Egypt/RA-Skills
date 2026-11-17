# -*- coding: utf-8 -*-
"""
万豪酒店技能 - ClawHub版
3个工具：search_marriott_hotels / get_marriott_hotel_info / search_marriott_packages
数据源：飞猪MCP via fliggy-proxy SCF代理
纯标准库实现
"""
import os
import json
import urllib.request
import urllib.error
import sys

# ===== 代理配置 =====
PROXY_URL = "https://1439498936-6sysdjjt99.ap-guangzhou.tencentscf.com"
PROXY_TOKEN = os.environ.get("PROXY_TOKEN", "")
def _request(api_type, params, timeout=30):
    """调用fliggy-proxy统一请求函数"""
    body = json.dumps({"type": api_type, "params": params}, ensure_ascii=False)
    req = urllib.request.Request(
        PROXY_URL,
        data=body.encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "X-Proxy-Token": PROXY_TOKEN,
        },
        method="POST",
    )
    try:
        resp = urllib.request.urlopen(req, timeout=timeout)
        data = json.loads(resp.read().decode("utf-8"))
        if data.get("status") == "error":
            return {"success": False, "error": data.get("message", "未知错误")}
        return {"success": True, "data": data.get("data", {})}
    except urllib.error.HTTPError as e:
        err_body = e.read().decode("utf-8")[:200]
        return {"success": False, "error": f"HTTP {e.code}: {err_body}"}
    except Exception as e:
        return {"success": False, "error": str(e)}


def search_marriott_hotels(destName, checkInDate=None, checkOutDate=None,
                           keyword=None, maxPrice=None, sort=None, limit=10):
    """
    搜索万豪集团旗下酒店
    参数:
        destName: 目的地城市/区域（必填），如"上海""深圳""三亚"
        checkInDate: 入住日期 YYYY-MM-DD
        checkOutDate: 退房日期 YYYY-MM-DD
        keyword: 关键词，如"万豪""JW""丽思卡尔顿"
        maxPrice: 最高价格（整数）
        sort: 排序方式 rate_desc/price_asc/price_desc/distance_asc
        limit: 返回数量，默认10
    """
    params = {"destName": destName}
    if checkInDate:
        params["checkInDate"] = checkInDate
    if checkOutDate:
        params["checkOutDate"] = checkOutDate
    if keyword:
        params["keyWords"] = keyword
    if maxPrice:
        params["maxPrice"] = int(maxPrice)
    if sort:
        params["sort"] = sort

    result = _request("search_marriott_hotels", params, timeout=30)
    if not result["success"]:
        return f"搜索失败: {result['error']}"

    items = (result.get("data") or {}).get("itemList", [])
    if not items:
        return f"未找到{destName}的万豪酒店，建议调整搜索条件"

    # 限制返回数量
    items = items[:limit]

    lines = []
    lines.append(f"🏨 {destName}万豪酒店搜索结果（{len(items)}家）\n")

    for i, item in enumerate(items, 1):
        name = item.get("name", "")
        price = item.get("price", "")
        star = item.get("star", "")
        address = item.get("address", "")
        poi = item.get("nearbyPoi", "")
        deco = item.get("decorationTime", "")
        url = item.get("detailUrl", "")
        shid = item.get("shid", "")

        lines.append(f"{i}. {name}")
        lines.append(f"   💰 {price}  ⭐ {star}")
        if address:
            lines.append(f"   📍 {address}")
        if poi:
            lines.append(f"   🚇 {poi}")
        if deco:
            lines.append(f"   🏗 装修: {deco}")
        if url:
            lines.append(f"   🔗 [点击预订]({url})")
        lines.append(f"   🆔 shid:{shid}")
        lines.append("")

    lines.append("💡 输入shid可查询酒店详情（交通/设施/政策/房型），输入关键词可查万豪套餐")
    return "\n".join(lines)


def get_marriott_hotel_info(shid=None, hotelName=None, reviewKeyword=None):
    """
    查询万豪酒店详情（交通/景点/设施/政策/房型）
    参数:
        shid: 酒店ID（推荐，从搜索结果获取）
        hotelName: 酒店名称（备选定位方式）
        reviewKeyword: 评价关键词过滤
    """
    if not shid and not hotelName:
        return "请提供shid（从搜索结果获取）或hotelName"

    params = {}
    if shid:
        params["shid"] = int(shid)
    if hotelName:
        params["hotelName"] = hotelName
    if reviewKeyword:
        params["reviewKeyword"] = reviewKeyword

    result = _request("get_marriott_hotel_info", params, timeout=20)
    if not result["success"]:
        return f"查询失败: {result['error']}"

    items = (result.get("data") or {}).get("itemList", [])
    if not items:
        return "未找到酒店详情"

    item = items[0]
    hotel_info = item.get("hotelInfo", {})
    url = item.get("detailUrl", "")

    lines = []

    # 基础信息
    basic = hotel_info.get("酒店基础信息", {})
    name = basic.get("酒店名称", "")
    address = basic.get("酒店地址", "")
    level = basic.get("酒店等级", "")
    rooms_count = basic.get("房间数量", "")
    open_time = basic.get("开业时间", "")
    deco_time = basic.get("装修时间", basic.get("最新装修时间", ""))
    checkin_method = basic.get("入住方式", "")
    pool = basic.get("恒温泳池", "")

    lines.append(f"🏨 {name} 详情\n")
    lines.append(f"📍 地址: {address}")
    lines.append(f"⭐ 等级: {level}")
    if rooms_count:
        lines.append(f"🏠 房间数: {rooms_count}")
    if open_time:
        lines.append(f"📅 开业: {open_time}")
    if deco_time:
        lines.append(f"🏗 装修: {deco_time}")
    if pool:
        lines.append(f"🏊 恒温泳池: {pool}")
    if checkin_method:
        lines.append(f"🔑 入住方式: {checkin_method}")

    # 政策
    policy = hotel_info.get("酒店政策", {})
    if policy:
        lines.append("\n📋 酒店政策")
        checkin_out = policy.get("入离政策", "")
        if checkin_out:
            lines.append(f"  ⏰ {checkin_out}")
        breakfast = policy.get("早餐政策", "")
        if breakfast:
            lines.append(f"  🍳 早餐: {breakfast}")
        deposit = policy.get("押金政策", "")
        if deposit:
            lines.append(f"  💳 押金: {deposit}")
        pet = policy.get("宠物政策", "")
        if pet:
            lines.append(f"  🐾 宠物: {pet}")

    # 周边
    nearby = hotel_info.get("酒店周边", {})
    if nearby:
        lines.append("\n🗺 周边信息")
        for cat, info in nearby.items():
            if info:
                lines.append(f"  【{cat}】")
                # 截取前3个
                spots = info.split(";") if isinstance(info, str) else [info]
                for s in spots[:3]:
                    s = s.strip()
                    if s:
                        lines.append(f"    · {s}")

    # 设施
    facility = hotel_info.get("酒店设施", {})
    if facility:
        lines.append("\n🏢 酒店设施")
        for cat, info in facility.items():
            if info:
                lines.append(f"  【{cat}】{info}")

    # 房型
    room_layers = item.get("roomLayers", [])
    if room_layers:
        lines.append(f"\n🛏 房型（{len(room_layers)}种）")
        for r in room_layers[:6]:
            rname = r.get("name", "")
            hot = r.get("热门设施", "")
            bed = r.get("床政策", "")
            info_str = ""
            if hot:
                info_str += f" {hot}"
            if bed:
                info_str += f" | {bed}"
            lines.append(f"  · {rname}{info_str}")
        if len(room_layers) > 6:
            lines.append(f"  ...还有{len(room_layers) - 6}种房型")

    if url:
        lines.append(f"\n🔗 [点击预订]({url})")

    return "\n".join(lines)


def search_marriott_packages(keyword=None, hotelName=None,
                             provinceOrCity=None, sort=None, limit=10):
    """
    搜索万豪酒店套餐优惠（含早/连住/门票等打包产品）
    参数:
        keyword: 搜索关键词，如"上海""三亚度假"
        hotelName: 酒店名称
        provinceOrCity: 省份或城市
        sort: 排序方式
        limit: 返回数量，默认10
    """
    if not keyword and not hotelName and not provinceOrCity:
        return "请提供keyword、hotelName或provinceOrCity中的至少一个"

    params = {}
    if keyword:
        params["keyword"] = keyword
    if hotelName:
        params["hotelName"] = hotelName
    if provinceOrCity:
        params["provinceOrCity"] = provinceOrCity
    if sort:
        params["sortType"] = sort

    result = _request("search_marriott_packages", params, timeout=30)
    if not result["success"]:
        return f"搜索失败: {result['error']}"

    items = (result.get("data") or {}).get("itemList", [])
    if not items:
        kw = keyword or hotelName or provinceOrCity
        return f"未找到{kw}的万豪套餐"

    items = items[:limit]

    lines = []
    search_kw = keyword or hotelName or provinceOrCity or "万豪"
    lines.append(f"🎁 {search_kw}万豪套餐搜索结果（{len(items)}个）\n")

    for i, item in enumerate(items, 1):
        title = item.get("title", "")
        price = item.get("price", "")
        sell = item.get("sellPoint", "")
        benefit = item.get("benefit", "")
        url = item.get("detailUrl", "")

        lines.append(f"{i}. {title}")
        lines.append(f"   💰 {price}")
        if sell:
            # 清理sellPoint中的多余标点
            sell = sell.replace("。，", "；").replace(",,", "，")
            lines.append(f"   ✨ {sell[:150]}")
        if benefit:
            lines.append(f"   🏷 {benefit}")
        if url:
            lines.append(f"   🔗 [点击预订]({url})")
        lines.append("")

    lines.append("💡 套餐通常比单订更优惠，含早餐/门票/连住折扣等")
    return "\n".join(lines)


# ===== 命令行入口 =====
def main():
    if len(sys.argv) < 3:
        print("用法: python marriott_hotel.py <tool> <args_json>")
        print("  tool: search | detail | packages")
        print('  示例: python marriott_hotel.py search \'{"destName":"上海"}\'')
        return

    tool = sys.argv[1]
    try:
        args = json.loads(sys.argv[2])
    except json.JSONDecodeError:
        print(f"参数JSON解析失败: {sys.argv[2]}")
        return

    if tool == "search":
        print(search_marriott_hotels(**args))
    elif tool == "detail":
        print(get_marriott_hotel_info(**args))
    elif tool == "packages":
        print(search_marriott_packages(**args))
    else:
        print(f"未知工具: {tool}，可选: search / detail / packages")


if __name__ == "__main__":
    main()
