# -*- coding: utf-8 -*-
"""
浏阳本地生活 Skill - 商家数据库
包含：生活服务师傅、餐厅农庄、酒店住宿
数据说明：这是示范数据，后期可以替换为真实商家信息
"""

# ============================================================
# 生活服务师傅（水电维修、疏通、开锁、搬家等）
# ============================================================
SERVICE_WORKERS = [
    # --- 疏通下水道 ---
    {
        "id": "sw001",
        "name": "老陈管道疏通",
        "category": "疏通下水道",
        "contact": "陈师傅",
        "phone": "138-7498-XXXX",
        "service_area": "浏阳全市区",
        "price_range": "80-300元",
        "work_hours": "24小时上门",
        "rating": 4.8,
        "review_count": 326,
        "highlight": "干了15年，马桶、厨房、地漏都能通，半小时到",
        "address": "浏阳市淮川街道"
    },
    {
        "id": "sw002",
        "name": "浏阳管道疏通王",
        "category": "疏通下水道",
        "contact": "王师傅",
        "phone": "159-7312-XXXX",
        "service_area": "淮川、集里、关口、荷花",
        "price_range": "60-200元",
        "work_hours": "早7点-晚11点",
        "rating": 4.6,
        "review_count": 198,
        "highlight": "价格实在，小问题60块搞定，通不了不收钱",
        "address": "浏阳市集里街道"
    },
    # --- 水电维修 ---
    {
        "id": "sw003",
        "name": "李师傅水电维修",
        "category": "水电维修",
        "contact": "李师傅",
        "phone": "186-8498-XXXX",
        "service_area": "浏阳全市区",
        "price_range": "50-500元",
        "work_hours": "早8点-晚9点",
        "rating": 4.9,
        "review_count": 412,
        "highlight": "持证电工，水管漏水、电路跳闸、灯具安装都做",
        "address": "浏阳市淮川街道才常路"
    },
    {
        "id": "sw004",
        "name": "急修哥水电",
        "category": "水电维修",
        "contact": "张师傅",
        "phone": "135-0731-XXXX",
        "service_area": "淮川、集里、荷花",
        "price_range": "30-300元",
        "work_hours": "24小时（夜间加50元）",
        "rating": 4.7,
        "review_count": 267,
        "highlight": "修不好不收钱，上门快，一般20分钟到",
        "address": "浏阳市荷花街道"
    },
    # --- 开锁换锁 ---
    {
        "id": "sw005",
        "name": "浏阳速开锁",
        "category": "开锁换锁",
        "contact": "刘师傅",
        "phone": "131-8710-XXXX",
        "service_area": "浏阳全市区",
        "price_range": "80-500元",
        "work_hours": "24小时",
        "rating": 4.8,
        "review_count": 531,
        "highlight": "公安备案正规开锁，15分钟到场，开不了不收费",
        "address": "浏阳市淮川街道人民中路"
    },
    # --- 搬家 ---
    {
        "id": "sw006",
        "name": "浏阳兄弟搬家",
        "category": "搬家",
        "contact": "周师傅",
        "phone": "150-7317-XXXX",
        "service_area": "浏阳全市区及周边乡镇",
        "price_range": "200-800元",
        "work_hours": "早7点-晚8点",
        "rating": 4.7,
        "review_count": 189,
        "highlight": "两个壮小伙上门，家具打包拆装都包，不加价",
        "address": "浏阳市关口街道"
    },
    # --- 家电维修 ---
    {
        "id": "sw007",
        "name": "小刘家电维修",
        "category": "家电维修",
        "contact": "刘师傅",
        "phone": "180-7313-XXXX",
        "service_area": "浏阳市区",
        "price_range": "50-400元",
        "work_hours": "早8点-晚7点",
        "rating": 4.6,
        "review_count": 156,
        "highlight": "空调、洗衣机、热水器、冰箱都修，先报价再修",
        "address": "浏阳市集里街道白沙路"
    },
    # --- 空调清洗 ---
    {
        "id": "sw008",
        "name": "洁净到家",
        "category": "空调清洗",
        "contact": "谭师傅",
        "phone": "173-8493-XXXX",
        "service_area": "浏阳全市区",
        "price_range": "80-150元/台",
        "work_hours": "早8点-晚6点",
        "rating": 4.8,
        "review_count": 203,
        "highlight": "专业拆洗，挂机80、柜机120、中央空调150/台",
        "address": "浏阳市荷花街道"
    },
    # --- 防水补漏 ---
    {
        "id": "sw009",
        "name": "固盾防水",
        "category": "防水补漏",
        "contact": "赵师傅",
        "phone": "199-7498-XXXX",
        "service_area": "浏阳全市区",
        "price_range": "200-2000元",
        "work_hours": "早8点-晚6点",
        "rating": 4.5,
        "review_count": 87,
        "highlight": "屋顶、卫生间、阳台防水，质保5年，漏了免费修",
        "address": "浏阳市淮川街道"
    },
]

# ============================================================
# 餐厅农庄（浏阳特色、农庄、饭店）
# ============================================================
RESTAURANTS = [
    # --- 特色农庄（有风景） ---
    {
        "id": "r001",
        "name": "官渡嗨渔庄",
        "category": "特色农庄",
        "cuisine": "浏阳蒸菜、河鲜、烧烤",
        "phone": "139-7312-XXXX",
        "address": "浏阳市官渡镇（浏阳河边）",
        "avg_price": 60,
        "avg_price_desc": "人均60元左右",
        "capacity": "可接待50人以上",
        "has_scenery": True,
        "scenery_desc": "靠着浏阳河，有露天河景位，吃饭看河景",
        "has_parking": True,
        "specialties": ["浏阳蒸菜", "河鲜鱼", "土鸡汤", "烧烤"],
        "highlight": "浏阳河边吃鱼，风景一流，本地人周末常去的农庄",
        "rating": 4.7,
        "nav_keyword": "官渡嗨渔庄 浏阳"
    },
    {
        "id": "r002",
        "name": "道官冲生态农庄",
        "category": "特色农庄",
        "cuisine": "农家菜、蒸菜、土菜",
        "phone": "136-8731-XXXX",
        "address": "浏阳市荷花街道道官冲",
        "avg_price": 55,
        "avg_price_desc": "人均55元左右",
        "capacity": "可接待30人",
        "has_scenery": True,
        "scenery_desc": "山里面的农庄，有鱼塘可以钓鱼，空气好",
        "has_parking": True,
        "specialties": ["土鸡", "腊肉", "浏阳蒸菜", "自种蔬菜"],
        "highlight": "山里农庄，可以钓鱼、摘菜，小孩也有地方玩",
        "rating": 4.6,
        "nav_keyword": "道官冲生态农庄 浏阳"
    },
    {
        "id": "r003",
        "name": "大围山峡谷漂流农庄",
        "category": "特色农庄",
        "cuisine": "大围山土菜",
        "phone": "158-7498-XXXX",
        "address": "浏阳市大围山镇",
        "avg_price": 70,
        "avg_price_desc": "人均70元左右",
        "capacity": "可接待80人以上",
        "has_scenery": True,
        "scenery_desc": "大围山脚下，森林环绕，夏天可以漂流",
        "has_parking": True,
        "specialties": ["大围山笋", "烟熏腊肉", "溪水鱼", "土鸡"],
        "highlight": "夏天漂流+吃饭一条龙，外地朋友来必去",
        "rating": 4.8,
        "nav_keyword": "大围山峡谷漂流 浏阳"
    },
    {
        "id": "r004",
        "name": "田螺小镇",
        "category": "特色农庄",
        "cuisine": "田螺、浏阳菜",
        "phone": "137-5517-XXXX",
        "address": "浏阳市沙市镇",
        "avg_price": 50,
        "avg_price_desc": "人均50元左右",
        "capacity": "可接待40人",
        "has_scenery": True,
        "scenery_desc": "田园风光，有荷花池和小溪",
        "has_parking": True,
        "specialties": ["田螺", "浏阳蒸菜", "米豆腐", "农家小炒"],
        "highlight": "吃田螺的好地方，田园风光，拍照好看",
        "rating": 4.5,
        "nav_keyword": "田螺小镇 浏阳"
    },
    # --- 市区餐厅 ---
    {
        "id": "r005",
        "name": "文家市大碗菜",
        "category": "浏阳蒸菜",
        "cuisine": "浏阳蒸菜",
        "phone": "150-7491-XXXX",
        "address": "浏阳市人民中路（步行街附近）",
        "avg_price": 35,
        "avg_price_desc": "人均35元左右",
        "capacity": "可接待20人",
        "has_scenery": False,
        "scenery_desc": "",
        "has_parking": False,
        "specialties": ["蒸腊肉", "蒸鱼头", "蒸鸡蛋", "蒸排骨"],
        "highlight": "正宗浏阳蒸菜，量大实惠，本地人天天吃",
        "rating": 4.6,
        "nav_keyword": "文家市大碗菜 浏阳"
    },
    {
        "id": "r006",
        "name": "浏阳古风楼",
        "category": "浏阳菜馆",
        "cuisine": "浏阳菜、湘菜",
        "phone": "189-7498-XXXX",
        "address": "浏阳市圭斋东路",
        "avg_price": 65,
        "avg_price_desc": "人均65元左右",
        "capacity": "可接待60人，有包厢",
        "has_scenery": False,
        "scenery_desc": "",
        "has_parking": True,
        "specialties": ["浏阳黑山羊", "蒸菜拼盘", "口味虾", "剁椒鱼头"],
        "highlight": "请客有面子，有包厢，菜品精致，环境好",
        "rating": 4.7,
        "nav_keyword": "浏阳古风楼"
    },
    {
        "id": "r007",
        "name": "蒸浏记",
        "category": "浏阳蒸菜",
        "cuisine": "蒸菜快餐",
        "phone": "173-0731-XXXX",
        "address": "浏阳市才常路",
        "avg_price": 20,
        "avg_price_desc": "人均20元左右",
        "capacity": "快餐店，10人左右",
        "has_scenery": False,
        "scenery_desc": "",
        "has_parking": False,
        "specialties": ["蒸菜套餐", "蒸排骨", "蒸鱼", "蒸南瓜"],
        "highlight": "快餐蒸菜，便宜好吃，一个人也能吃",
        "rating": 4.4,
        "nav_keyword": "蒸浏记 浏阳"
    },
    {
        "id": "r008",
        "name": "湘水源农庄",
        "category": "特色农庄",
        "cuisine": "农家菜、柴火灶",
        "phone": "155-7498-XXXX",
        "address": "浏阳市古港镇",
        "avg_price": 55,
        "avg_price_desc": "人均55元左右",
        "capacity": "可接待40人",
        "has_scenery": True,
        "scenery_desc": "竹林环绕，有小溪，环境清幽",
        "has_parking": True,
        "specialties": ["柴火土鸡", "腊肉炒笋", "米粉肉", "手工豆腐"],
        "highlight": "柴火灶做菜，原汁原味，吃完还能在竹林散步",
        "rating": 4.6,
        "nav_keyword": "湘水源农庄 浏阳古港"
    },
]

# ============================================================
# 酒店住宿
# ============================================================
HOTELS = [
    {
        "id": "h001",
        "name": "浏阳国际大酒店",
        "category": "商务酒店",
        "stars": "四星级",
        "phone": "0731-8386-XXXX",
        "address": "浏阳市淮川街道人民中路",
        "price_range": "380-680元/晚",
        "avg_price": 450,
        "has_breakfast": True,
        "breakfast_desc": "自助早餐，中西式都有，品种丰富",
        "has_parking": True,
        "wifi": True,
        "distance_to_center": "市中心，步行街旁边",
        "nearby_landmark": "步行街、天空剧院步行10分钟",
        "highlight": "浏阳最老牌的酒店，地段最好，出门就是步行街",
        "rating": 4.5,
        "room_types": ["大床房", "双床房", "豪华套房"],
        "nav_keyword": "浏阳国际大酒店"
    },
    {
        "id": "h002",
        "name": "维也纳酒店(浏阳天空剧院店)",
        "category": "连锁酒店",
        "stars": "四星级",
        "phone": "0731-8398-XXXX",
        "address": "浏阳市金沙北路（天空剧院对面）",
        "price_range": "320-520元/晚",
        "avg_price": 380,
        "has_breakfast": True,
        "breakfast_desc": "自助早餐，干净卫生，味道不错",
        "has_parking": True,
        "wifi": True,
        "distance_to_center": "天空剧院对面，市中心5分钟车程",
        "nearby_landmark": "天空剧院对面，走路2分钟",
        "highlight": "天空剧院看烟花最方便的酒店，出门就到",
        "rating": 4.6,
        "room_types": ["大床房", "双床房", "家庭房"],
        "nav_keyword": "维也纳酒店 浏阳天空剧院"
    },
    {
        "id": "h003",
        "name": "浏阳恒邦开元酒店",
        "category": "高端酒店",
        "stars": "五星标准",
        "phone": "0731-8388-XXXX",
        "address": "浏阳市花炮大道",
        "price_range": "480-1200元/晚",
        "avg_price": 580,
        "has_breakfast": True,
        "breakfast_desc": "五星级自助早餐，品种最全，有湖南特色早点",
        "has_parking": True,
        "wifi": True,
        "distance_to_center": "市中心10分钟车程",
        "nearby_landmark": "花炮观礼台附近",
        "highlight": "浏阳最高档的酒店，设施新，服务好，适合商务接待",
        "rating": 4.8,
        "room_types": ["豪华大床房", "行政双床房", "总统套房"],
        "nav_keyword": "浏阳恒邦开元酒店"
    },
    {
        "id": "h004",
        "name": "汉庭酒店(浏阳步行街店)",
        "category": "经济连锁",
        "stars": "三星级",
        "phone": "0731-8381-XXXX",
        "address": "浏阳市北正南路（步行街附近）",
        "price_range": "180-280元/晚",
        "avg_price": 220,
        "has_breakfast": True,
        "breakfast_desc": "简单早餐，包子粥面条",
        "has_parking": False,
        "wifi": True,
        "distance_to_center": "步行街旁边",
        "nearby_landmark": "步行街走路3分钟",
        "highlight": "便宜干净，连锁品牌有保障，适合预算有限的朋友",
        "rating": 4.3,
        "room_types": ["大床房", "双床房"],
        "nav_keyword": "汉庭酒店 浏阳步行街"
    },
    {
        "id": "h005",
        "name": "如家酒店(浏阳才常路店)",
        "category": "经济连锁",
        "stars": "三星级",
        "phone": "0731-8382-XXXX",
        "address": "浏阳市才常路",
        "price_range": "160-260元/晚",
        "avg_price": 200,
        "has_breakfast": True,
        "breakfast_desc": "简单早餐",
        "has_parking": False,
        "wifi": True,
        "distance_to_center": "市中心，交通方便",
        "nearby_landmark": "天空剧院15分钟车程",
        "highlight": "性价比最高，干净整洁，适合短住",
        "rating": 4.2,
        "room_types": ["大床房", "双床房"],
        "nav_keyword": "如家酒店 浏阳才常路"
    },
    {
        "id": "h006",
        "name": "锦江之星(浏阳金沙路店)",
        "category": "经济连锁",
        "stars": "三星级",
        "phone": "0731-8385-XXXX",
        "address": "浏阳市金沙北路",
        "price_range": "200-320元/晚",
        "avg_price": 250,
        "has_breakfast": True,
        "breakfast_desc": "自助早餐，品种还行",
        "has_parking": True,
        "wifi": True,
        "distance_to_center": "天空剧院5分钟车程",
        "nearby_landmark": "天空剧院5分钟车程",
        "highlight": "离天空剧院近，有停车位，性价比不错",
        "rating": 4.4,
        "room_types": ["大床房", "双床房"],
        "nav_keyword": "锦江之星 浏阳金沙路"
    },
    {
        "id": "h007",
        "name": "大围山森林度假酒店",
        "category": "度假酒店",
        "stars": "四星级",
        "phone": "0731-8396-XXXX",
        "address": "浏阳市大围山镇",
        "price_range": "350-600元/晚",
        "avg_price": 420,
        "has_breakfast": True,
        "breakfast_desc": "山里特色早餐，有当地米粉和手工包子",
        "has_parking": True,
        "wifi": True,
        "distance_to_center": "距市区40分钟车程",
        "nearby_landmark": "大围山国家森林公园门口",
        "highlight": "住在山里，空气好，夏天凉快，适合带家人度假",
        "rating": 4.7,
        "room_types": ["山景大床房", "家庭房", "独栋木屋"],
        "nav_keyword": "大围山森林度假酒店 浏阳"
    },
]


# ============================================================
# 搜索和推荐函数
# ============================================================

def search_services(category=None, keyword=None):
    """搜索生活服务师傅"""
    results = SERVICE_WORKERS

    if category:
        category = category.strip()
        results = [s for s in results if category in s["category"]]

    if keyword:
        keyword = keyword.strip().lower()
        results = [s for s in results if
                   keyword in s["category"].lower() or
                   keyword in s["name"].lower() or
                   keyword in s["highlight"].lower()]

    if not results:
        # 返回所有可用分类
        all_cats = list(set(s["category"] for s in SERVICE_WORKERS))
        return {
            "found": False,
            "message": f"没有找到相关服务。目前支持的服务类型有：{', '.join(all_cats)}",
            "available_categories": all_cats
        }

    return {
        "found": True,
        "count": len(results),
        "services": results
    }


def search_restaurants(budget_per_person=None, people_count=None, want_scenery=False, keyword=None):
    """搜索餐厅农庄"""
    results = RESTAURANTS

    if keyword:
        keyword = keyword.strip().lower()
        results = [r for r in results if
                   keyword in r["name"].lower() or
                   keyword in r["category"].lower() or
                   keyword in r["cuisine"].lower() or
                   keyword in " ".join(r["specialties"]).lower() or
                   keyword in r.get("highlight", "").lower() or
                   keyword in r.get("address", "").lower()]

    if want_scenery:
        results = [r for r in results if r.get("has_scenery")]

    if budget_per_person:
        # budget_per_person 就是人均预算（元），直接用来筛选
        results = [r for r in results if r["avg_price"] <= budget_per_person * 1.2]

    if not results:
        return {
            "found": False,
            "message": "没有找到符合条件的餐厅。试试放宽预算或去掉风景要求？",
            "tip": "浏阳特色推荐：蒸菜、黑山羊、河鲜、大围山土菜"
        }

    # 按评分排序
    results.sort(key=lambda x: x["rating"], reverse=True)
    return {
        "found": True,
        "count": len(results),
        "restaurants": results
    }


def search_hotels(max_price=None, need_breakfast=False, near_landmark=None, room_type=None):
    """搜索酒店"""
    results = HOTELS

    if max_price:
        results = [h for h in results if h["avg_price"] <= max_price * 1.1]

    if need_breakfast:
        results = [h for h in results if h.get("has_breakfast")]

    if near_landmark:
        landmark = near_landmark.strip().lower()
        results = [h for h in results if
                   landmark in h.get("nearby_landmark", "").lower() or
                   landmark in h.get("address", "").lower() or
                   landmark in h.get("distance_to_center", "").lower()]

    if room_type:
        room_type = room_type.strip()
        results = [h for h in results if
                   any(room_type in rt for rt in h.get("room_types", []))]

    if not results:
        all_hotels_summary = [
            f"{h['name']}（{h['price_range']}，{h['nearby_landmark']}）"
            for h in HOTELS
        ]
        return {
            "found": False,
            "message": "没有找到完全符合条件的酒店。以下是浏阳所有推荐酒店：",
            "all_hotels": all_hotels_summary
        }

    # 按评分排序
    results.sort(key=lambda x: x["rating"], reverse=True)
    return {
        "found": True,
        "count": len(results),
        "hotels": results
    }


# 所有服务类别汇总（给AI看的）
SERVICE_CATEGORIES = list(set(s["category"] for s in SERVICE_WORKERS))
RESTAURANT_CATEGORIES = list(set(r["category"] for r in RESTAURANTS))
