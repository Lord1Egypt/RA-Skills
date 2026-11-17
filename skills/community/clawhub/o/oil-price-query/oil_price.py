#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""中国油价查询"""

import json
import sys
import urllib.request
import urllib.parse

PROVINCE_MAP = {
    "北京": "北京市",
    "天津": "天津市",
    "河北": "河北省",
    "山西": "山西省",
    "内蒙古": "内蒙古自治区",
    "辽宁": "辽宁省",
    "吉林": "吉林省",
    "黑龙江": "黑龙江省",
    "上海": "上海市",
    "江苏": "江苏省",
    "浙江": "浙江省",
    "安徽": "安徽省",
    "福建": "福建省",
    "江西": "江西省",
    "山东": "山东省",
    "河南": "河南省",
    "湖北": "湖北省",
    "湖南": "湖南省",
    "广东": "广东省",
    "广西": "广西壮族自治区",
    "海南": "海南省",
    "重庆": "重庆市",
    "四川": "四川省",
    "贵州": "贵州省",
    "云南": "云南省",
    "西藏": "西藏自治区",
    "陕西": "陕西省",
    "甘肃": "甘肃省",
    "青海": "青海省",
    "宁夏": "宁夏回族自治区",
    "新疆": "新疆维吾尔自治区"
}

FUEL_MAP = {
    "89 号汽油": "89 号汽油",
    "92 号汽油": "92 号汽油",
    "95 号汽油": "95 号汽油",
    "98 号汽油": "98 号汽油",
    "0 号柴油": "0 号柴油",
    "-10 号柴油": "-10 号柴油",
    "89 号": "89 号汽油",
    "92 号": "92 号汽油",
    "95 号": "95 号汽油",
    "98 号": "98 号汽油",
    "0 号": "0 号柴油",
    "-10 号": "-10 号柴油",
    "汽油": "汽油",
    "柴油": "柴油",
}

def standardize_fuel_name(name):
    name = name.strip()
    
    # 按优先级顺序匹配（从最长到最短）
    # 这样可以确保 "92 号汽油" 优先匹配，而不是匹配到 "汽油"
    sorted_patterns = sorted(FUEL_MAP.keys(), key=len, reverse=True)
    for pattern in sorted_patterns:
        if pattern in name:
            return FUEL_MAP[pattern]
    
    return None

def get_province_name(province):
    province = province.strip()
    if province in PROVINCE_MAP.values():
        return province
    if province in PROVINCE_MAP:
        return PROVINCE_MAP[province]
    return province

def parse_oil_data(data_json):
    data = data_json.get("data")
    if not data:
        return None
    province = data.get("province", "未知")
    update_date = data.get("update_date", "未知")
    next_adjustment = data.get("next_adjustment", "未知")
    forecast = data.get("forecast", "")
    prices = data.get("prices", [])
    oil_data = {}
    for price_info in prices:
        fuel_name = price_info.get("name", "")
        fuel_type = standardize_fuel_name(fuel_name)
        price = price_info.get("price")
        unit = price_info.get("unit", "元/升")
        if fuel_type:
            # 使用标准名称作为键，但存储完整名称用于显示
            # FUEL_MAP 的 key 是完整名称，value 是标准名称
            display_name = fuel_name  # 使用 API 返回的完整名称
            oil_data[display_name] = {
                "name": fuel_name,
                "price": price,
                "unit": unit,
                "type": price_info.get("type", ""),
                "forecast": forecast
            }
    return {
        "province": get_province_name(province),
        "date": update_date,
        "next_date": next_adjustment,
        "oil_data": oil_data
    }

def format_output(data):
    province = data["province"]
    update_date = data["date"]
    next_date = data["next_date"]
    oil_data = data["oil_data"]
    print("")
    print("=" * 60)
    print("  中国油价查询 - " + province)
    print("  更新日期：" + update_date)
    print("  下次调整：" + next_date)
    print("=" * 60)
    print()
    # 按标准名称顺序输出
    fuel_types = sorted(oil_data.keys(), key=lambda x: FUEL_MAP.get(x, x))
    for fuel_type in fuel_types:
        fuel_info = oil_data[fuel_type]
        price = fuel_info.get("price")
        unit = fuel_info.get("unit", "元/升")
        display_name = FUEL_MAP.get(fuel_type, fuel_type)
        print("## " + display_name)
        print()
        if price is not None:
            price_str = str(round(float(price), 2)) + " " + unit if isinstance(price, (int, float)) else str(price) + " " + unit
            print(display_name + ":")
            print("  当前价格：" + price_str)
            if fuel_info.get("type"):
                print("  油品类型：" + fuel_info["type"])
        else:
            print(display_name + ": 暂无数据")
        print()
    if not oil_data:
        print("  暂无油价数据")
    print()
    print("=" * 60)
    print("  查询完成！")
    print("=" * 60)
    print()

def main():
    if len(sys.argv) < 2:
        print("=" * 60)
        print("  中国油价查询")
        print("=" * 60)
        print()
        print("用法：python3 oil_price.py <省份名称>")
        print()
        sys.exit(0)
    province_name = sys.argv[1]
    province_name = get_province_name(province_name)
    encoded_province = urllib.parse.quote(province_name)
    url = "https://v1.apizero.cn/api/oil-price?province=" + encoded_province
    print("正在查询 " + province_name + " 油价...")
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=15) as response:
            response_text = response.read().decode("utf-8")
            data_json = json.loads(response_text)
            if data_json.get("code") != 0:
                print("查询失败：" + data_json.get("msg", "未知错误"))
                sys.exit(1)
            result = parse_oil_data(data_json)
            if not result:
                print("无法解析油价数据")
                sys.exit(1)
            format_output(result)
    except Exception as e:
        print("错误：" + str(e))
        sys.exit(1)

if __name__ == "__main__":
    main()
