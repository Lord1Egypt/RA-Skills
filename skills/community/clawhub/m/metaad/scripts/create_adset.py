#!/usr/bin/env python3
"""
创建 Meta 广告组 (Ad Set)
包含受众定位、预算、排期等设置
"""

from meta_api import api_post, get_ad_account_id

# 优化目标映射
OPTIMIZATION_GOALS = {
    "impressions": "IMPRESSIONS",
    "reach": "REACH",
    "link_clicks": "LINK_CLICKS",
    "landing_page_views": "LANDING_PAGE_VIEWS",
    "conversions": "OFFSITE_CONVERSIONS",
    "value": "VALUE",
    "thruplay": "THRUPLAY",
    "app_installs": "APP_INSTALLS",
}

# 计费方式映射
BILLING_EVENTS = {
    "impressions": "IMPRESSIONS",
    "clicks": "LINK_CLICKS",
    "thruplay": "THRUPLAY",
}


def create_adset(
    campaign_id,
    name,
    daily_budget,
    targeting,
    optimization_goal="conversions",
    billing_event="impressions",
    bid_amount=None,
    status="PAUSED",
    start_time=None,
    end_time=None
):
    """
    创建广告组
    
    Args:
        campaign_id: 所属广告系列 ID
        name: 广告组名称
        daily_budget: 日预算（单位：分，如 50刀 = 5000）
        targeting: 受众定位字典
        optimization_goal: 优化目标
        billing_event: 计费事件
        bid_amount: 出价金额（可选）
        status: 状态
        start_time: 开始时间 (ISO 8601 格式)
        end_time: 结束时间 (ISO 8601 格式)
    
    Returns:
        dict: 包含 adset_id 的字典
    """
    account_id = get_ad_account_id()
    
    # 标准化参数
    if optimization_goal.lower() in OPTIMIZATION_GOALS:
        optimization_goal = OPTIMIZATION_GOALS[optimization_goal.lower()]
    
    if billing_event.lower() in BILLING_EVENTS:
        billing_event = BILLING_EVENTS[billing_event.lower()]
    
    params = {
        "campaign_id": campaign_id,
        "name": name,
        "daily_budget": daily_budget,
        "targeting": targeting,
        "optimization_goal": optimization_goal,
        "billing_event": billing_event,
        "status": status,
    }
    
    if bid_amount:
        params["bid_amount"] = bid_amount
    if start_time:
        params["start_time"] = start_time
    if end_time:
        params["end_time"] = end_time
    
    result = api_post(f"{account_id}/adsets", params)
    
    adset_id = result.get('id')
    print(f"✅ 广告组创建成功")
    print(f"   名称: {name}")
    print(f"   日预算: ${daily_budget/100:.2f}")
    print(f"   ID: {adset_id}")
    
    return {
        "adset_id": adset_id,
        "name": name,
        "daily_budget": daily_budget
    }


def build_targeting(
    countries=None,
    regions=None,
    age_min=None,
    age_max=None,
    genders=None,
    interests=None,
    custom_audiences=None,
    excluded_custom_audiences=None
):
    """
    构建受众定位参数
    
    Args:
        countries: 国家代码列表，如 ["US", "CA"]
        regions: 地区列表
        age_min: 最小年龄
        age_max: 最大年龄
        genders: 性别 [1=男, 2=女]
        interests: 兴趣列表
        custom_audiences: 自定义受众 ID 列表
        excluded_custom_audiences: 排除的自定义受众 ID 列表
    
    Returns:
        dict: targeting 参数
    """
    targeting = {
        "geo_locations": {}
    }
    
    if countries:
        targeting["geo_locations"]["countries"] = countries
    if regions:
        targeting["geo_locations"]["regions"] = regions
    
    if age_min:
        targeting["age_min"] = age_min
    if age_max:
        targeting["age_max"] = age_max
    if genders:
        targeting["genders"] = genders
    
    if interests:
        targeting["interests"] = [{"id": i} if isinstance(i, str) and i.isdigit() else i for i in interests]
    
    if custom_audiences:
        targeting["custom_audiences"] = [{"id": aid} for aid in custom_audiences]
    
    if excluded_custom_audiences:
        targeting["excluded_custom_audiences"] = [{"id": aid} for aid in excluded_custom_audiences]
    
    return targeting


if __name__ == "__main__":
    import sys
    import json
    
    if len(sys.argv) < 4:
        print("用法: python create_adset.py <campaign_id> <名称> <日预算(分)> [targeting_json]")
        print("示例: python create_adset.py 123456789 '美国女性25-45' 5000 '{\"countries\":[\"US\"],\"age_min\":25,\"age_max\":45,\"genders\":[2]}'")
        exit(1)
    
    campaign_id = sys.argv[1]
    name = sys.argv[2]
    daily_budget = int(sys.argv[3])
    
    if len(sys.argv) > 4:
        targeting = json.loads(sys.argv[4])
    else:
        # 默认定位
        targeting = build_targeting(
            countries=["US"],
            age_min=25,
            age_max=45,
            genders=[2]  # 女性
        )
    
    print(f"=== 创建广告组 ===\n")
    
    try:
        result = create_adset(
            campaign_id=campaign_id,
            name=name,
            daily_budget=daily_budget,
            targeting=targeting
        )
        print(f"\n广告组 ID: {result['adset_id']}")
    except Exception as e:
        print(f"❌ 创建失败: {e}")
