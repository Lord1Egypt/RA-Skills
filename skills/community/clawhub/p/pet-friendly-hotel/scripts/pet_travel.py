#!/usr/bin/env python3
"""宠物出行助手 — 中国宠物出行全攻略
Tools: check_pet_flight / check_pet_train / pet_travel_docs
"""

import json
import sys

# ============================================================
# 航空宠物政策数据库
# ============================================================
AIRLINE_PET_DB = {
    "国航": {
        "en": "Air China", "code": "CA",
        "cabin_pet": False,
        "cabin_note": "国航目前不允许宠物进客舱",
        "cargo_pet": True,
        "cargo_note": "可办理宠物托运(随机托运)，需提前申请",
        "weight_limit": "含航空箱≤32kg(部分航班≤8kg小型宠物)",
        "size_limit": "航空箱尺寸：长×宽×高≤100cm(各边之和)，且能放入货舱",
        "fee": "按逾重行李收费：经济舱全价×1.5%/kg，最低收费¥350起",
        "breed_restrictions": [
            "短鼻犬禁运：巴哥、法斗、英斗、西施、拳师犬、北京犬等",
            "短鼻猫禁运：波斯猫、异国短毛猫、喜马拉雅猫等",
            "怀孕期/哺乳期/8周龄以下禁运",
            "攻击性犬种禁运：比特犬、藏獒等"
        ],
        "temperature_restrictions": "高温季节(夏季)部分航线暂停托运，地面温度>29℃可能拒运",
        "required_docs": ["动物检疫合格证明", "宠物疫苗本(狂犬疫苗≥21天≤1年)", "航空箱标识牌"],
        "booking_tips": [
            "必须提前24-72小时申请，经航司同意后方可办理",
            "每架航班限托运宠物数量有限(通常2-4只)，先到先得",
            "值机前需到货运站办理检疫查验",
            "建议选择直达航班，避免中转风险"
        ]
    },
    "南航": {
        "en": "China Southern", "code": "CZ",
        "cabin_pet": False,
        "cabin_note": "南航目前不允许宠物进客舱",
        "cargo_pet": True,
        "cargo_note": "可办理宠物托运(随机托运)，需提前申请",
        "weight_limit": "含航空箱≤32kg",
        "size_limit": "航空箱三边之和≤158cm",
        "fee": "按逾重行李收费，约¥350-800不等(视航线和重量)",
        "breed_restrictions": [
            "短鼻犬/猫禁运（同国航）",
            "6月龄以下禁运",
            "怀孕/哺乳期禁运"
        ],
        "temperature_restrictions": "夏季高温可能暂停托运，具体以航司通知为准",
        "required_docs": ["动物检疫合格证明", "狂犬疫苗证明(≥21天≤1年)", "航空箱"],
        "booking_tips": [
            "提前24小时以上致电95539申请",
            "每航班限运2-3只宠物",
            "部分机型不支持宠物托运(如ARJ21等小型机)"
        ]
    },
    "东航": {
        "en": "China Eastern", "code": "MU",
        "cabin_pet": False,
        "cabin_note": "东航目前不允许宠物进客舱(服务犬除外)",
        "cargo_pet": True,
        "cargo_note": "可办理宠物随机托运",
        "weight_limit": "含航空箱≤32kg",
        "size_limit": "航空箱三边之和≤158cm",
        "fee": "按逾重行李费率收取，约¥350-800",
        "breed_restrictions": [
            "短鼻犬/猫禁运",
            "8周龄以下禁运",
            "怀孕/哺乳期禁运"
        ],
        "temperature_restrictions": "高温季节限制托运",
        "required_docs": ["动物检疫合格证明", "狂犬疫苗证明", "航空箱"],
        "booking_tips": [
            "提前48小时致电95530申请",
            "上海浦东/虹桥有专门的宠物托运柜台",
            "建议选早班或晚班机避开高温"
        ]
    },
    "海航": {
        "en": "Hainan Airlines", "code": "HU",
        "cabin_pet": True,
        "cabin_note": "海航是国内少数允许宠物进客舱的航司！需提前申请，仅限猫和小型犬",
        "cargo_pet": True,
        "cargo_note": "同时支持客舱携带和托运",
        "weight_limit": "客舱：含包袋≤5kg | 托运：含航空箱≤32kg",
        "size_limit": "客舱：宠物包长×宽×高≤35×28×24cm | 托运：三边之和≤158cm",
        "fee": "客舱：¥800/航段 | 托运：按逾重行李收费约¥350-800",
        "breed_restrictions": [
            "客舱仅限猫和小型犬(不含短鼻品种)",
            "托运短鼻犬/猫禁运",
            "6月龄以下/怀孕/哺乳期禁运"
        ],
        "temperature_restrictions": "夏季高温托运限制，客舱不受影响",
        "required_docs": ["动物检疫合格证明", "狂犬疫苗证明", "宠物健康证明", "客舱需额外签署责任书"],
        "booking_tips": [
            "客舱宠物位非常紧俏，建议提前7天以上申请",
            "每航班客舱限2只宠物",
            "客舱宠物需装在专用软包内，全程不得放出",
            "目前仅部分航线支持客舱宠物，预订时确认"
        ]
    },
    "川航": {
        "en": "Sichuan Airlines", "code": "3U",
        "cabin_pet": False,
        "cabin_note": "川航目前不允许宠物进客舱",
        "cargo_pet": True,
        "cargo_note": "可办理宠物随机托运",
        "weight_limit": "含航空箱≤32kg",
        "size_limit": "航空箱三边之和≤158cm",
        "fee": "按逾重行李费率收取",
        "breed_restrictions": ["短鼻犬/猫禁运", "怀孕/哺乳期禁运"],
        "temperature_restrictions": "夏季高温限制",
        "required_docs": ["动物检疫合格证明", "狂犬疫苗证明"],
        "booking_tips": [
            "提前24小时申请",
            "成都双流机场宠物托运手续较完善"
        ]
    },
    "春秋航空": {
        "en": "Spring Airlines", "code": "9C",
        "cabin_pet": False,
        "cabin_note": "春秋航空不允许宠物进客舱",
        "cargo_pet": True,
        "cargo_note": "可办理宠物托运，但收费相对较高",
        "weight_limit": "含航空箱≤32kg",
        "size_limit": "航空箱三边之和≤158cm",
        "fee": "按逾重行李收费，春秋费率较高",
        "breed_restrictions": ["短鼻犬/猫禁运"],
        "temperature_restrictions": "夏季高温限制",
        "required_docs": ["动物检疫合格证明", "狂犬疫苗证明"],
        "booking_tips": [
            "提前24小时申请",
            "廉价航空托运费用较高，建议对比其他航司"
        ]
    },
    "吉祥航空": {
        "en": "Juneyao Airlines", "code": "HO",
        "cabin_pet": False,
        "cabin_note": "吉祥航空不允许宠物进客舱",
        "cargo_pet": True,
        "cargo_note": "可办理宠物随机托运",
        "weight_limit": "含航空箱≤32kg",
        "size_limit": "航空箱三边之和≤158cm",
        "fee": "按逾重行李收费",
        "breed_restrictions": ["短鼻犬/猫禁运"],
        "temperature_restrictions": "夏季高温限制",
        "required_docs": ["动物检疫合格证明", "狂犬疫苗证明"],
        "booking_tips": ["提前24小时申请"]
    },
    "厦航": {
        "en": "XiamenAir", "code": "MF",
        "cabin_pet": False,
        "cabin_note": "厦航不允许宠物进客舱",
        "cargo_pet": True,
        "cargo_note": "可办理宠物托运",
        "weight_limit": "含航空箱≤32kg",
        "size_limit": "航空箱三边之和≤158cm",
        "fee": "按逾重行李收费",
        "breed_restrictions": ["短鼻犬/猫禁运"],
        "temperature_restrictions": "夏季高温限制",
        "required_docs": ["动物检疫合格证明", "狂犬疫苗证明"],
        "booking_tips": ["提前24小时申请", "厦门/福州出发宠物托运手续较便捷"]
    },
    "深航": {
        "en": "Shenzhen Airlines", "code": "ZH",
        "cabin_pet": False,
        "cabin_note": "深航不允许宠物进客舱",
        "cargo_pet": True,
        "cargo_note": "可办理宠物随机托运",
        "weight_limit": "含航空箱≤32kg",
        "size_limit": "航空箱三边之和≤158cm",
        "fee": "按逾重行李收费",
        "breed_restrictions": ["短鼻犬/猫禁运"],
        "temperature_restrictions": "夏季高温限制",
        "required_docs": ["动物检疫合格证明", "狂犬疫苗证明"],
        "booking_tips": ["提前24小时申请", "深圳宝安机场宠物托运流程较规范"]
    },
    "山航": {
        "en": "Shandong Airlines", "code": "SC",
        "cabin_pet": False,
        "cabin_note": "山航不允许宠物进客舱",
        "cargo_pet": True,
        "cargo_note": "可办理宠物托运",
        "weight_limit": "含航空箱≤32kg",
        "size_limit": "航空箱三边之和≤158cm",
        "fee": "按逾重行李收费",
        "breed_restrictions": ["短鼻犬/猫禁运"],
        "temperature_restrictions": "夏季高温限制",
        "required_docs": ["动物检疫合格证明", "狂犬疫苗证明"],
        "booking_tips": ["提前24小时申请"]
    },
}

# 航司别名
AIRLINE_ALIAS = {
    "国航": "国航", "中国国航": "国航", "Air China": "国航", "CA": "国航",
    "南航": "南航", "中国南航": "南航", "China Southern": "南航", "CZ": "南航",
    "东航": "东航", "中国东航": "东航", "China Eastern": "东航", "MU": "东航",
    "海航": "海航", "海南航空": "海航", "Hainan Airlines": "海航", "HU": "海航",
    "川航": "川航", "四川航空": "川航", "Sichuan Airlines": "川航", "3U": "川航",
    "春秋": "春秋航空", "春秋航空": "春秋航空", "Spring Airlines": "春秋航空", "9C": "春秋航空",
    "吉祥": "吉祥航空", "吉祥航空": "吉祥航空", "Juneyao Airlines": "吉祥航空", "HO": "吉祥航空",
    "厦航": "厦航", "厦门航空": "厦航", "XiamenAir": "厦航", "MF": "厦航",
    "深航": "深航", "深圳航空": "深航", "Shenzhen Airlines": "深航", "ZH": "深航",
    "山航": "山航", "山东航空": "山航", "Shandong Airlines": "山航", "SC": "山航",
}

# ============================================================
# 铁路宠物政策
# ============================================================
TRAIN_PET_POLICY = {
    "高铁": {
        "policy": "❌ 不可携带宠物上车",
        "detail": "根据《铁路旅客运输规程》，高铁/动车禁止旅客随身携带活体动物(导盲犬除外)",
        "exceptions": "导盲犬可随视障旅客乘车，需持有效证件",
    },
    "动车": {
        "policy": "❌ 不可携带宠物上车",
        "detail": "同高铁政策，动车同样禁止携带活体动物",
        "exceptions": "导盲犬可随视障旅客乘车",
    },
    "普速": {
        "policy": "❌ 不可携带宠物上车(可办理行李车托运)",
        "detail": "普通列车同样不允许旅客随身携带宠物，但可通过行李车办理宠物托运(需提前办理)",
        "exceptions": "导盲犬可随视障旅客乘车",
    },
    "通用": {
        "alternatives": [
            {
                "method": "铁路行李车托运",
                "detail": "部分普速列车有行李车，可办理宠物托运。需动物检疫证明+宠物箱，费用约¥2-3/kg。需提前到站办理，仅限有行李车的车次。",
                "suitable_for": "普速列车长途出行"
            },
            {
                "method": "宠物专车/顺风车",
                "detail": "滴滴/哈啰等平台的宠物专车服务，或宠物顺风车，可携带宠物同行。费用比普通打车高20-50%。",
                "suitable_for": "中短途(500km以内)"
            },
            {
                "method": "自驾出行",
                "detail": "最灵活的宠物出行方式，可随时照顾宠物。注意：高速服务区可遛狗，但需牵绳。",
                "suitable_for": "中短途(800km以内)"
            },
            {
                "method": "航空托运",
                "detail": "适合长途出行，但需办理检疫证明，费用较高。夏季高温可能限制。",
                "suitable_for": "800km以上长途"
            },
            {
                "method": "宠物托运公司",
                "detail": "专业宠物托运公司提供门到门服务，价格较高(¥500-2000+)但省心。",
                "suitable_for": "不随行/异地搬迁"
            }
        ],
        "tips": [
            "高铁/动车确实不允许带宠物，不要抱有侥幸心理",
            "宠物铁路托运仅限有行李车的普速列车，且需提前确认车次",
            "宠物托运途中无法照顾，短鼻犬/猫风险较高",
            "自驾是最推荐的宠物出行方式，可随时停车照顾"
        ]
    }
}

# ============================================================
# 宠物证件办理
# ============================================================
PET_DOCS = {
    "domestic": {
        "required_docs": [
            {
                "name": "动物检疫合格证明",
                "detail": "到当地动物卫生监督所(或农业农村局指定窗口)办理",
                "validity": "一般3-5天有效，出发前最近办理",
                "cost": "免费或¥10-30",
                "process": [
                    "1. 携带宠物+疫苗本到指定兽医站/动物卫生监督所",
                    "2. 工作人员现场查验宠物健康状态",
                    "3. 核对狂犬疫苗信息(需≥21天≤1年)",
                    "4. 出具《动物检疫合格证明》"
                ]
            },
            {
                "name": "宠物疫苗本(狂犬疫苗)",
                "detail": "需在正规宠物医院接种并在疫苗本上登记",
                "validity": "狂犬疫苗需≥21天且≤1年(以出发日计算)",
                "cost": "¥50-120/针",
                "process": [
                    "1. 到正规宠物医院接种狂犬疫苗",
                    "2. 医院在疫苗本上盖章+登记批号",
                    "3. 等待21天以上方可出行",
                    "注意：疫苗本信息需与检疫证明一致"
                ]
            },
            {
                "name": "航空箱/宠物包",
                "detail": "托运需硬质航空箱，客舱需软质宠物包",
                "requirements": [
                    "硬质航空箱：牢固、防逃逸、底部防漏、有饮水器",
                    "软质宠物包(客舱)：透气、防水、可放入前排座椅下方",
                    "箱内铺好尿垫，放熟悉物品(如主人的旧T恤)减少焦虑"
                ]
            }
        ],
        "timeline": "建议提前3-4周开始准备：\n- 提前4周：确认狂犬疫苗在有效期(如过期需重新接种+等21天)\n- 提前1-2周：预订机票并申请宠物托运/客舱位\n- 出发前1-3天：办理动物检疫合格证明\n- 出发当天：提前2-3小时到机场办理手续",
        "tips": [
            "检疫证明有效期短(3-5天)，不要提前太久办",
            "狂犬疫苗必须≥21天才能出行，刚打的不行",
            "航空箱建议提前让宠物适应(在家放几天让它习惯)",
            "出发前4-6小时断食，2小时断水，防止晕车呕吐",
            "夏季尽量避免中午航班，货舱温度可能过高"
        ]
    },
    "international": {
        "required_docs": [
            {
                "name": "宠物护照/国际健康证书",
                "detail": "到海关指定的宠物出入境检疫机构办理",
                "validity": "各国要求不同，一般7-10天有效",
                "cost": "¥200-500"
            },
            {
                "name": "狂犬疫苗证明+抗体滴度检测",
                "detail": "大多数国家要求狂犬疫苗≥30天且≤1年，部分要求抗体滴度检测(RNATT)",
                "validity": "抗体检测需提前3-4个月(采血→等结果→等等待期)",
                "cost": "抗体检测¥500-1000"
            },
            {
                "name": "微芯片(ISO 11784/11785)",
                "detail": "国际出行必须植入ISO标准微芯片(15位数字)",
                "validity": "永久有效",
                "cost": "¥100-300"
            },
            {
                "name": "入境许可证",
                "detail": "部分国家(如澳大利亚/新西兰/日本等)需提前申请入境许可",
                "validity": "各国不同",
                "cost": "各国不同"
            },
            {
                "name": "目的地国家额外要求",
                "detail": "各国要求差异大，需逐一确认",
                "examples": {
                    "日本": "需提前40天申请进口许可+出发前12小时内健康检查",
                    "澳大利亚": "极度严格，需提前7个月准备，强制隔离10天",
                    "新西兰": "类似澳大利亚，需提前数月申请",
                    "新加坡": "需进口许可+隔离(如来自非指定国家)",
                    "泰国": "相对宽松，需健康证明+疫苗记录",
                    "欧盟": "需宠物护照+微芯片+狂犬疫苗+抗体检测(部分国家)",
                    "美国": "需健康证明+狂犬疫苗证明，无隔离要求",
                    "加拿大": "需健康证明+狂犬疫苗证明，无隔离要求",
                    "韩国": "需健康证明+狂犬疫苗+微芯片",
                    "中国香港": "需进口许可+隔离(视来源地)"
                }
            }
        ],
        "timeline": "建议提前6-8个月开始准备(澳大利亚/新西兰等严格国家)或3-4个月(普通国家)：\n- 提前6个月：确认目的地国家入境要求\n- 提前4个月：植入微芯片+接种狂犬疫苗+抗体检测\n- 提前2个月：申请入境许可(如需)\n- 提前1个月：预订有氧舱航班\n- 出发前1周：办理国际健康证书\n- 出发当天：提前3小时到机场",
        "tips": [
            "宠物出国手续比人还复杂，务必提前规划",
            "澳大利亚/新西兰是宠物入境最严格的国家，建议找专业代理",
            "不是所有航班都有有氧舱(宠物货舱)，预订时必须确认",
            "转机可能需要在转机国重新检疫，建议直飞",
            "短鼻犬/猫多数航司不允许托运，国际出行更受限"
        ]
    }
}

# 宠物友好酒店通用信息
PET_FRIENDLY_HOTEL_TIPS = {
    "search_keywords": ["宠物友好", "可带宠物", "pet-friendly", "可带狗"],
    "chain_hotels": [
        {"name": "亚朵酒店", "policy": "部分门店允许携带小型宠物(≤10kg)，需提前确认，可能收清洁费¥100-200"},
        {"name": "全季酒店", "policy": "部分门店宠物友好，需提前电话确认"},
        {"name": "桔子酒店", "policy": "部分门店允许携带宠物"},
        {"name": "民宿/客栈", "policy": "民宿宠物友好度最高，预订时筛选'可带宠物'标签"},
    ],
    "tips": [
        "预订前务必电话确认宠物政策，线上标注可能过时",
        "大多数酒店对宠物体重有限制(通常≤10kg或≤5kg)",
        "部分酒店收取宠物清洁费(¥100-300/晚)",
        "入住时宠物需全程牵绳/装笼，不得单独留在房间",
        "建议带尿垫+食盆+熟悉玩具，减少宠物焦虑"
    ]
}

# 短鼻犬猫品种列表(航司禁运)
SHORT_NOSE_BREEDS = {
    "dog": [
        "巴哥犬(Pug)", "法国斗牛犬(French Bulldog)", "英国斗牛犬(English Bulldog)",
        "西施犬(Shih Tzu)", "北京犬(Pekingese)", "拳师犬(Boxer)",
        "波士顿梗(Boston Terrier)", "查理王小猎犬(Cavalier King Charles Spaniel)",
        "日本�的(Japanese Chin)", "拉萨犬(Lhasa Apso)",
        "松狮犬(Chow Chow)", "拉萨阿普索犬"
    ],
    "cat": [
        "波斯猫(Persian)", "异国短毛猫(Exotic Shorthair)", "喜马拉雅猫(Himalayan)",
        "缅甸猫(Burmese)", "苏格兰折耳猫(Scottish Fold)"
    ]
}


def resolve_airline(name: str) -> str:
    """解析航司名称"""
    if name in AIRLINE_PET_DB:
        return name
    if name in AIRLINE_ALIAS:
        return AIRLINE_ALIAS[name]
    # 模糊匹配
    for key in AIRLINE_PET_DB:
        if key in name or name in key:
            return key
    for alias, mapped in AIRLINE_ALIAS.items():
        if alias in name or name in alias:
            return mapped
    return ""


def check_pet_flight(airline: str, pet_type: str = "cat", cabin_type: str = "both") -> dict:
    """工具1: 航空宠物政策查询"""
    airline_key = resolve_airline(airline)
    if not airline_key:
        return {
            "success": False,
            "error": f"未找到「{airline}」的宠物政策",
            "supported_airlines": list(AIRLINE_PET_DB.keys()),
            "suggestion": "请输入航司名称，如：国航、南航、东航、海航等"
        }
    
    data = AIRLINE_PET_DB[airline_key]
    
    result = {
        "success": True,
        "airline": airline_key,
        "airline_en": data["en"],
        "airline_code": data["code"],
        "pet_type": pet_type,
    }
    
    if cabin_type in ["both", "cabin"]:
        result["cabin_policy"] = {
            "allowed": data["cabin_pet"],
            "note": data["cabin_note"],
        }
        if data["cabin_pet"]:
            result["cabin_policy"]["weight_limit"] = data.get("weight_limit", "N/A").split("|")[0].strip() if "|" in data.get("weight_limit", "") else "含包袋≤5kg"
            result["cabin_policy"]["size_limit"] = data.get("size_limit", "N/A").split("|")[0].strip() if "|" in data.get("size_limit", "") else "≤35×28×24cm"
            result["cabin_policy"]["fee"] = data.get("fee", "N/A").split("|")[0].strip() if "|" in data.get("fee", "") else "¥800/航段"
    
    if cabin_type in ["both", "cargo"]:
        result["cargo_policy"] = {
            "allowed": data["cargo_pet"],
            "note": data["cargo_note"],
            "weight_limit": data["weight_limit"],
            "size_limit": data["size_limit"],
            "fee": data["fee"],
        }
    
    result["breed_restrictions"] = data["breed_restrictions"]
    result["temperature_restrictions"] = data["temperature_restrictions"]
    result["required_docs"] = data["required_docs"]
    result["booking_tips"] = data["booking_tips"]
    
    # 短鼻品种提示
    if pet_type == "dog":
        result["short_nose_warning"] = f"⚠️ 以下短鼻犬品种多数航司禁运：{', '.join(SHORT_NOSE_BREEDS['dog'][:6])}等"
    elif pet_type == "cat":
        result["short_nose_warning"] = f"⚠️ 以下短鼻猫品种多数航司禁运：{', '.join(SHORT_NOSE_BREEDS['cat'])}"
    
    # 海航特殊提示
    if data["cabin_pet"]:
        result["cabin_highlight"] = f"✅ {airline_key}允许宠物进客舱！这是国内少数支持客舱宠物的航司，建议优先选择"
    
    return result


def check_pet_train(train_type: str = "all") -> dict:
    """工具2: 铁路宠物政策查询"""
    result = {
        "success": True,
        "summary": "🚄 中国铁路目前不允许旅客随身携带宠物乘车(导盲犬除外)"
    }
    
    if train_type == "all":
        result["policies"] = {}
        for ttype in ["高铁", "动车", "普速"]:
            result["policies"][ttype] = TRAIN_PET_POLICY[ttype]
    else:
        ttype = train_type if train_type in TRAIN_PET_POLICY else "通用"
        if ttype in ["高铁", "动车", "普速"]:
            result["policy"] = TRAIN_PET_POLICY[ttype]
    
    result["alternatives"] = TRAIN_PET_POLICY["通用"]["alternatives"]
    result["tips"] = TRAIN_PET_POLICY["通用"]["tips"]
    
    return result


def pet_travel_docs(travel_type: str = "domestic", destination: str = "", pet_type: str = "dog") -> dict:
    """工具3: 宠物出行证件办理指南"""
    if travel_type not in PET_DOCS:
        travel_type = "domestic"
    
    data = PET_DOCS[travel_type]
    
    result = {
        "success": True,
        "travel_type": "国内" if travel_type == "domestic" else "国际",
        "required_docs": data["required_docs"],
        "timeline": data["timeline"],
        "tips": data["tips"]
    }
    
    # 国际出行特殊处理
    if travel_type == "international" and destination:
        dest_docs = data["required_docs"][-1]  # 目的地国家额外要求
        dest_lower = destination.lower()
        examples = dest_docs.get("examples", {})
        
        # 匹配目的地
        matched = None
        for country in examples:
            if dest_lower in country.lower() or country.lower() in dest_lower:
                matched = country
                break
        
        if matched:
            result["destination_specific"] = {
                "country": matched,
                "requirements": examples[matched]
            }
        else:
            result["destination_note"] = f"「{destination}」的详细宠物入境要求未收录，请查询该国驻华使领馆或农业部官网获取最新规定"
    
    # 附加宠物友好酒店信息
    result["pet_hotel_tips"] = PET_FRIENDLY_HOTEL_TIPS
    
    return result


def main():
    """主入口"""
    if len(sys.argv) < 3:
        print(json.dumps({
            "error": "Usage: pet_travel.py <tool> <args_json>",
            "tools": ["check_pet_flight", "check_pet_train", "pet_travel_docs"]
        }, ensure_ascii=False))
        sys.exit(1)
    
    tool = sys.argv[1]
    try:
        args = json.loads(sys.argv[2])
    except json.JSONDecodeError:
        print(json.dumps({"error": "Invalid JSON arguments"}, ensure_ascii=False))
        sys.exit(1)
    
    if tool == "check_pet_flight":
        result = check_pet_flight(
            airline=args.get("airline", ""),
            pet_type=args.get("pet_type", "cat"),
            cabin_type=args.get("cabin_type", "both")
        )
    elif tool == "check_pet_train":
        result = check_pet_train(
            train_type=args.get("train_type", "all")
        )
    elif tool == "pet_travel_docs":
        result = pet_travel_docs(
            travel_type=args.get("travel_type", "domestic"),
            destination=args.get("destination", ""),
            pet_type=args.get("pet_type", "dog")
        )
    else:
        result = {"error": f"Unknown tool: {tool}", "available_tools": ["check_pet_flight", "check_pet_train", "pet_travel_docs"]}
    
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
