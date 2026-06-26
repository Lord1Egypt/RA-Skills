#!/usr/bin/env python3
"""
一键创建完整的 Meta 广告
串联 Campaign -> Ad Set -> Ad 的创建流程
"""

import json
from pathlib import Path
from datetime import datetime, timedelta

from config_manager import get_config
from upload_media import upload_images_batch
from create_campaign import create_campaign
from create_adset import create_adset, build_targeting
from create_ad import create_ad, build_creative


def create_full_ad(
    product_name,
    daily_budget,
    targeting_config,
    ad_config,
    campaign_name=None,
    objective="conversions",
    status="PAUSED"
):
    """
    一键创建完整广告
    
    Args:
        product_name: 产品名称
        daily_budget: 日预算（美元）
        targeting_config: 受众配置
            {
                "countries": ["US"],
                "age_min": 25,
                "age_max": 45,
                "genders": [2],  # 1=男, 2=女
                "interests": []
            }
        ad_config: 广告配置
            {
                "page_id": "YOUR_PAGE_ID",
                "message": "广告文案",
                "headline": "标题",
                "images": ["path/to/image1.jpg"],
                "link_url": "https://example.com",
                "call_to_action": "SHOP_NOW"
            }
        campaign_name: 广告系列名称（可选，默认使用产品名）
        objective: 广告目标
        status: 初始状态
    
    Returns:
        dict: 完整的广告结构信息
    """
    
    print("=" * 50)
    print("🚀 开始创建完整 Meta 广告")
    print("=" * 50)
    
    # 1. 上传素材
    print("\n📤 Step 1: 上传素材")
    print("-" * 30)
    
    images = ad_config.get("images", [])
    if images:
        uploaded_images = upload_images_batch(images)
        image_hashes = [img["hash"] for img in uploaded_images if img]
        if not image_hashes:
            raise Exception("素材上传失败，无法继续创建广告")
    else:
        image_hashes = []
    
    # 2. 创建 Campaign
    print("\n📋 Step 2: 创建广告系列")
    print("-" * 30)
    
    campaign_name = campaign_name or f"{product_name} - {datetime.now().strftime('%Y-%m-%d')}"
    campaign = create_campaign(
        name=campaign_name,
        objective=objective,
        status=status
    )
    
    # 3. 创建 Ad Set
    print("\n🎯 Step 3: 创建广告组")
    print("-" * 30)
    
    targeting = build_targeting(
        countries=targeting_config.get("countries", ["US"]),
        age_min=targeting_config.get("age_min"),
        age_max=targeting_config.get("age_max"),
        genders=targeting_config.get("genders"),
        interests=targeting_config.get("interests")
    )
    
    adset = create_adset(
        campaign_id=campaign["campaign_id"],
        name=f"{product_name} - AdSet",
        daily_budget=int(daily_budget * 100),  # 转换为分
        targeting=targeting,
        status=status
    )
    
    # 4. 创建 Ad
    print("\n📝 Step 4: 创建广告")
    print("-" * 30)
    
    results = []
    for i, image_hash in enumerate(image_hashes):
        creative = build_creative(
            name=f"{product_name} - Creative {i+1}",
            page_id=ad_config["page_id"],
            message=ad_config["message"],
            headline=ad_config.get("headline"),
            description=ad_config.get("description"),
            call_to_action=ad_config.get("call_to_action", "SHOP_NOW"),
            image_hash=image_hash,
            link_url=ad_config.get("link_url"),
            display_link=ad_config.get("display_link")
        )
        
        ad = create_ad(
            adset_id=adset["adset_id"],
            name=f"{product_name} - Ad {i+1}",
            creative=creative,
            status=status
        )
        results.append(ad)
    
    # 汇总
    print("\n" + "=" * 50)
    print("✅ 广告创建完成！")
    print("=" * 50)
    
    summary = {
        "campaign": campaign,
        "adset": adset,
        "ads": results,
        "images_uploaded": len(image_hashes),
        "status": status
    }
    
    print(f"\n📊 创建摘要:")
    print(f"   广告系列: {campaign['name']} (ID: {campaign['campaign_id']})")
    print(f"   广告组: {adset['name']} (ID: {adset['adset_id']})")
    print(f"   日预算: ${daily_budget}")
    print(f"   广告数量: {len(results)}")
    print(f"   初始状态: {status}")
    
    if status == "PAUSED":
        print(f"\n💡 提示: 广告已创建但处于暂停状态，请在 Meta 广告管理器中审核后启用")
    
    return summary


def create_from_json(config_path):
    """从 JSON 配置文件创建广告"""
    with open(config_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
    
    return create_full_ad(
        product_name=config["product_name"],
        daily_budget=config["daily_budget"],
        targeting_config=config["targeting"],
        ad_config=config["ad"],
        campaign_name=config.get("campaign_name"),
        objective=config.get("objective", "conversions"),
        status=config.get("status", "PAUSED")
    )


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("用法:")
        print("  方式1 - 使用配置文件: python create_full_ad.py <config.json>")
        print("  方式2 - 使用示例配置: python create_full_ad.py --example")
        print("\n示例配置文件格式:")
        print(json.dumps({
            "product_name": "夏季连衣裙",
            "daily_budget": 50,
            "campaign_name": "夏季促销2024",
            "objective": "conversions",
            "status": "PAUSED",
            "targeting": {
                "countries": ["US"],
                "age_min": 25,
                "age_max": 45,
                "genders": [2]
            },
            "ad": {
                "page_id": "YOUR_PAGE_ID",
                "message": "限时优惠！夏季新款连衣裙5折起，快来选购！",
                "headline": "夏季大促",
                "images": ["image1.jpg", "image2.jpg"],
                "link_url": "https://yourstore.com/summer-sale",
                "call_to_action": "SHOP_NOW"
            }
        }, indent=2, ensure_ascii=False))
        exit(1)
    
    if sys.argv[1] == "--example":
        # 创建示例配置文件
        example = {
            "product_name": "示例产品",
            "daily_budget": 50,
            "campaign_name": "示例广告系列",
            "objective": "conversions",
            "status": "PAUSED",
            "targeting": {
                "countries": ["US"],
                "age_min": 25,
                "age_max": 45,
                "genders": [2]
            },
            "ad": {
                "page_id": "YOUR_PAGE_ID",
                "message": "限时优惠！快来选购！",
                "headline": "大促活动",
                "images": ["image1.jpg"],
                "link_url": "https://example.com",
                "call_to_action": "SHOP_NOW"
            }
        }
        example_path = "ad_config_example.json"
        with open(example_path, 'w', encoding='utf-8') as f:
            json.dump(example, f, indent=2, ensure_ascii=False)
        print(f"✅ 示例配置文件已创建: {example_path}")
        print("请修改配置文件中的 YOUR_PAGE_ID 和图片路径，然后运行:")
        print(f"  python create_full_ad.py {example_path}")
    else:
        config_path = sys.argv[1]
        if not Path(config_path).exists():
            print(f"❌ 配置文件不存在: {config_path}")
            exit(1)
        
        try:
            result = create_from_json(config_path)
            print(f"\n🎉 全部完成！")
        except Exception as e:
            print(f"\n❌ 创建失败: {e}")
            import traceback
            traceback.print_exc()
