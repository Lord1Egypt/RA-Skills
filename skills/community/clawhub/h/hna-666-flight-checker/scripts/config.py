#!/usr/bin/env python3
"""
配置文件：目的地列表、城市映射等
"""

# 目的地字典：三字码 -> 中文名
DESTINATIONS = {
    "HAK": "海口", "XIY": "西安", "KMG": "昆明", "CKG": "重庆",
    "XMN": "厦门"
}
# DESTINATIONS = {
#    "HAK": "海口", "YYA": "岳阳", "XNN": "西宁", "INC": "银川",
#    "LHW": "兰州", "XIY": "西安", "KMG": "昆明", "CKG": "重庆",
#    "CTU": "成都", "WNZ": "温州", "UYN": "榆林", "JHG": "西双版纳",
#    "YIH": "宜昌", "ERL": "二连浩特", "AQG": "安庆", "FOC": "福州",
#    "XMN": "厦门", "HRB": "哈尔滨", "DLC": "大连"
# }
# 查询页面 URL
QUERY_URL = "https://m.hnair.com/hnams/plusMember/ableAirlineQuery"
