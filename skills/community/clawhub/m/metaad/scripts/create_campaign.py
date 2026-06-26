#!/usr/bin/env python3
"""
创建 Meta 广告系列 (Campaign)
"""

from meta_api import api_post, get_ad_account_id

# 广告系列目标映射
CAMPAIGN_OBJECTIVES = {
    "awareness": "BRAND_AWARENESS",           # 品牌知名度
    "reach": "REACH",                        # 覆盖人数
    "traffic": "TRAFFIC",                    # 流量
    "engagement": "ENGAGEMENT",              # 互动率
    "app_installs": "APP_INSTALLS",          # 应用安装
    "video_views": "VIDEO_VIEWS",            # 视频观看量
    "lead_generation": "LEAD_GENERATION",    # 潜在客户开发
    "conversions": "CONVERSIONS",            # 转化量
    "catalog_sales": "CATALOG_SALES",        # 目录促销
    "messages": "MESSAGES",                  # 消息互动
}


def create_campaign(name, objective="conversions", status="PAUSED", special_ad_categories=None):
    """
    创建广告系列
    
    Args:
        name: 广告系列名称
        objective: 广告目标 (见 CAMPAIGN_OBJECTIVES)
        status: 状态 (ACTIVE/PAUSED)
        special_ad_categories: 特殊广告类别 (如 CREDIT, EMPLOYMENT, HOUSING)
    
    Returns:
        dict: 包含 campaign_id 的字典
    """
    account_id = get_ad_account_id()
    
    # 标准化目标
    if objective.lower() in CAMPAIGN_OBJECTIVES:
        objective = CAMPAIGN_OBJECTIVES[objective.lower()]
    
    params = {
        "name": name,
        "objective": objective,
        "status": status,
        "special_ad_categories": special_ad_categories or []
    }
    
    result = api_post(f"{account_id}/campaigns", params)
    
    campaign_id = result.get('id')
    print(f"✅ 广告系列创建成功")
    print(f"   名称: {name}")
    print(f"   目标: {objective}")
    print(f"   ID: {campaign_id}")
    
    return {
        "campaign_id": campaign_id,
        "name": name,
        "objective": objective
    }


def list_objectives():
    """列出可用的广告目标"""
    print("=== 可用的广告目标 ===")
    for key, value in CAMPAIGN_OBJECTIVES.items():
        print(f"  {key:20} -> {value}")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("用法: python create_campaign.py <广告系列名称> [目标] [状态]")
        print("示例: python create_campaign.py '夏季促销' conversions PAUSED")
        print("\n可用目标:")
        list_objectives()
        exit(1)
    
    name = sys.argv[1]
    objective = sys.argv[2] if len(sys.argv) > 2 else "conversions"
    status = sys.argv[3] if len(sys.argv) > 3 else "PAUSED"
    
    print(f"=== 创建广告系列 ===\n")
    
    try:
        result = create_campaign(name, objective, status)
        print(f"\n广告系列 ID: {result['campaign_id']}")
    except Exception as e:
        print(f"❌ 创建失败: {e}")
