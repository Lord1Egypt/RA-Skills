#!/usr/bin/env python3
"""
OW Seller 安装引导脚本 V2.2
按评标五维度引导卖家配置产品清单和企业资料

面向全球卖家 - 卖家自己选择发货区域（本国/全球/指定国家）

评标维度：
- 💰 价格竞争力 50% -> 提供产品定价策略
- 📜 真品证明 20% -> 提供企业资质、代理权、授权书
- 📸 商品展示 15% -> 上传图片视频
- 🚚 到货时间 5% -> 配置物流方式和发货区域
- 📋 交易记录 10% -> 提供店铺链接和历史交易
"""

import json
import sys
from pathlib import Path
from datetime import datetime

STATE_DIR = Path(__file__).parent.parent / "state"
CATALOG_FILE = STATE_DIR / "product_catalog.json"
REGION_FILE = STATE_DIR / "region_config.json"

# 国家/地区列表（供卖家选择）
COUNTRIES = {
    "亚洲": ["中国", "日本", "韩国", "新加坡", "马来西亚", "泰国", "越南", "印度", "印尼", "菲律宾"],
    "欧洲": ["英国", "法国", "德国", "意大利", "西班牙", "荷兰", "比利时", "瑞士", "奥地利", "瑞典"],
    "北美": ["美国", "加拿大", "墨西哥"],
    "南美": ["巴西", "阿根廷", "智利", "哥伦比亚"],
    "大洋洲": ["澳大利亚", "新西兰"],
    "非洲": ["南非", "埃及", "尼日利亚", "肯尼亚"],
    "中东": ["沙特", "阿联酋", "以色列", "土耳其"]
}

def print_header():
    print("""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║    💰 OW Seller - 发飙全球卖 | Global Selling System        ║
║                                                              ║
║    配置产品清单，让全球AI买家自动找到你                      ║
║    Configure products, let global AI buyers find you        ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
""")

def print_scoring_intro():
    print("""
📊 评标五维度 | 5-Dimension Scoring - 配置越完整，中标率越高

┌─────────────────────────────────────────────────────────────┐
│  维度          │ 权重  │ 你需要配置的内容                   │
├─────────────────────────────────────────────────────────────┤
│  💰 价格竞争力 │ 50%   │ 产品定价、成本、利润空间           │
│  📜 真品证明   │ 20%   │ 营业执照、代理权、授权书           │
│  📸 商品展示   │ 15%   │ 产品图片(最多3张)、视频(30秒)      │
│  🚚 到货时间   │ 5%    │ 物流方式、发货区域                 │
│  📋 交易记录   │ 10%   │ 店铺链接、历史成交                 │
└─────────────────────────────────────────────────────────────┘

⚠️  至少需要配置：产品类别
✅ 全部配置有利于：提高中标率，获得更多订单
""")

def get_input(prompt, default=None, required=False):
    """获取用户输入"""
    if default:
        prompt = f"{prompt} [{default}]: "
    else:
        prompt = f"{prompt}: "
    
    while True:
        value = input(prompt).strip()
        if value:
            return value
        if default:
            return default
        if not required:
            return ""
        print("❌ 此项为必填项，请输入")

def get_yes_no(prompt, default="n"):
    """获取是/否选择"""
    value = get_input(f"{prompt} (y/n)", default)
    return value.lower() == 'y'

def setup_basic_info():
    """配置卖家基本信息（全球视角）"""
    print("\n" + "="*60)
    print("📝 第一步：卖家基本信息 | Seller Information")
    print("="*60 + "\n")
    
    print("🌍 你来自哪个国家/地区？")
    print("   选择你的所在国家，系统会优先匹配本国买家")
    
    # 显示国家列表
    for region, countries in COUNTRIES.items():
        print(f"\n   【{region}】")
        for i, country in enumerate(countries, 1):
            print(f"      {i}. {country}")
    
    print("\n   或者直接输入国家名称（如：China、日本、Brazil）")
    
    seller_country = get_input("\n你的国家/地区", required=True)
    
    seller_id = get_input("卖家ID | Seller ID", f"seller-{datetime.now().strftime('%Y%m%d%H%M')}", required=True)
    seller_name = get_input("店铺/企业名称 | Shop/Company Name", required=True)
    contact = get_input("联系方式 | Contact (WeChat/Email/Phone)")
    
    return {
        "seller_id": seller_id,
        "seller_name": seller_name,
        "seller_country": seller_country,  # 卖家所在国家
        "contact": contact
    }

def setup_product():
    """配置单个产品"""
    print("\n" + "-"*60)
    print("📦 产品配置 | Product Configuration（按评标维度引导）")
    print("-"*60 + "\n")
    
    # 必填：产品类别
    print("【必填】产品基本信息")
    name = get_input("产品名称 | Product Name", required=True)
    category = get_input("产品类别 | Category (如：红酒、数码、服装)", required=True)
    
    product = {
        "product_id": f"PROD-{datetime.now().strftime('%Y%m%d%H%M%S')}",
        "name": name,
        "category": category,
        "active": True
    }
    
    # 可选：品牌和关键词
    brand = get_input("品牌 | Brand")
    if brand:
        product["brand"] = brand
    
    keywords_input = get_input("搜索关键词 | Keywords（逗号分隔，如：红酒,wine,葡萄酒）")
    if keywords_input:
        product["keywords"] = [k.strip() for k in keywords_input.split(",")]
    else:
        # 自动生成基础关键词
        product["keywords"] = [name, category]
        if brand:
            product["keywords"].append(brand)
    
    # 💰 价格竞争力 (50%)
    print("\n【💰 价格竞争力 - 权重50% | Price Competitiveness】")
    print("   配置价格信息可提高中标率")
    
    if get_yes_no("是否配置价格信息？| Configure pricing?", "y"):
        cost = get_input("成本价 | Cost (货币单位)", "0")
        try:
            product["cost"] = float(cost)
        except:
            product["cost"] = 0
        
        price_min = get_input("最低售价 | Min Price", str(int(product["cost"] * 1.1)))
        price_max = get_input("最高售价 | Max Price", str(int(product["cost"] * 2)))
        try:
            product["price_range"] = [float(price_min), float(price_max)]
        except:
            product["price_range"] = [product["cost"], product["cost"] * 2]
        
        stock = get_input("库存数量 | Stock", "10")
        try:
            product["stock"] = int(stock)
        except:
            product["stock"] = 10
        
        # 货币单位
        currency = get_input("货币单位 | Currency (CNY/USD/EUR/JPY)", "CNY")
        product["currency"] = currency
    
    # 📜 真品证明 (20%)
    print("\n【📜 真品证明 - 权重20% | Authenticity Proof】")
    print("   提供资质文件可大幅提高信任度")
    
    auth_docs = []
    if get_yes_no("有营业执照？| Have business license?", "y"):
        auth_docs.append("business_license")
        bl_url = get_input("营业执照图片链接 | License URL (optional)")
        if bl_url:
            auth_docs.append({"type": "business_license", "url": bl_url})
    
    if get_yes_no("有产品代理权/授权书？| Have agency/auth certificate?"):
        auth_docs.append("agency_cert")
        ag_url = get_input("证明链接 | Certificate URL (optional)")
        if ag_url:
            auth_docs.append({"type": "agency_cert", "url": ag_url})
    
    if get_yes_no("有质检报告/认证？| Have quality report/certification?"):
        auth_docs.append("quality_report")
    
    if auth_docs:
        product["auth_docs"] = auth_docs
    
    # 📸 商品展示 (15%)
    print("\n【📸 商品展示 - 权重15% | Product Display】")
    print("   图片视频让买家更放心")
    
    if get_yes_no("是否上传商品展示？| Upload product media?"):
        product["images"] = []
        for i in range(1, 4):
            img = get_input(f"图片{i}链接 | Image {i} URL (留空跳过)")
            if img:
                product["images"].append(img)
        
        video = get_input("视频链接 | Video URL (optional, max 30s)")
        if video:
            product["video"] = video
    
    # 📋 交易记录 (10%)
    print("\n【📋 交易记录 - 权重10% | Transaction History】")
    print("   店铺链接和成交记录提升信誉")
    
    shop_links = []
    if get_yes_no("是否提供店铺链接？| Provide shop links?", "y"):
        while True:
            platform = get_input("平台名称 | Platform (Amazon/eBay/Taobao/Shopify/留空结束)")
            if not platform:
                break
            shop_url = get_input("店铺链接 | Shop URL", required=True)
            shop_name = get_input("店铺名称 | Shop Name")
            shop_links.append({
                "platform": platform,
                "url": shop_url,
                "shop_name": shop_name if shop_name else f"{seller_name} {platform}"
            })
    
    if shop_links:
        product["shop_links"] = shop_links
    
    return product

def setup_shipping_regions_global():
    """配置发货区域（全球卖家视角）"""
    print("\n" + "="*60)
    print("🚚 发货区域配置 | Shipping Regions")
    print("="*60 + "\n")
    
    print("🌍 选择你的发货范围：")
    print("   1. 本国发货 - 只发货到你所在的国家")
    print("   2. 区域发货 - 发货到指定国家或区域")
    print("   3. 全球发货 - 发货到全球任何国家")
    print("")
    
    choice = get_input("选择发货范围 (1/2/3)", "1")
    
    regions_config = {
        "ship_regions": {
            "mode": "",  # local/regional/global
            "enabled": [],
            "disabled": [],
            "countries": []
        }
    }
    
    if choice == "1":
        # 本国发货
        print("\n📍 本国发货模式")
        seller_country = get_input("确认你的国家 | Confirm your country", required=True)
        
        regions_config["ship_regions"]["mode"] = "local"
        regions_config["ship_regions"]["enabled"] = [seller_country]
        regions_config["ship_regions"]["countries"] = [seller_country]
        
        print(f"   ✅ 只匹配来自 {seller_country} 的买家")
        
    elif choice == "2":
        # 区域发货 - 选择指定国家
        print("\n📍 区域发货模式 - 选择可发货国家")
        
        regions_config["ship_regions"]["mode"] = "regional"
        
        enabled_countries = []
        
        for region, countries in COUNTRIES.items():
            print(f"\n   【{region}】")
            for country in countries:
                if get_yes_no(f"   发货到 {country}？| Ship to {country}?"):
                    enabled_countries.append(country)
        
        # 也可以手动输入其他国家
        print("\n   其他国家（输入国家名称，逗号分隔，留空跳过）")
        other_countries = get_input("   其他可发货国家")
        if other_countries:
            enabled_countries.extend([c.strip() for c in other_countries.split(",")])
        
        regions_config["ship_regions"]["enabled"] = enabled_countries
        regions_config["ship_regions"]["countries"] = enabled_countries
        
        # 排除的国家
        print("\n   是否有明确不发货的国家？")
        if get_yes_no("   配置不可发货国家？| Configure excluded countries?"):
            disabled = []
            for region, countries in COUNTRIES.items():
                for country in countries:
                    if country not in enabled_countries:
                        if get_yes_no(f"   明确排除 {country}？"):
                            disabled.append(country)
            regions_config["ship_regions"]["disabled"] = disabled
        
        print(f"\n   ✅ 可发货到 {len(enabled_countries)} 个国家")
        
    elif choice == "3":
        # 全球发货
        print("\n📍 全球发货模式")
        
        regions_config["ship_regions"]["mode"] = "global"
        regions_config["ship_regions"]["enabled"] = ["全球"]
        regions_config["ship_regions"]["countries"] = ["全球"]
        
        print("   ✅ 匹配来自任何国家的买家")
        
        # 仍然可以排除某些国家
        print("\n   是否有明确不发货的国家？")
        if get_yes_no("   配置不可发货国家？| Configure excluded countries?"):
            disabled = []
            other_disabled = get_input("   不可发货国家（逗号分隔）| Excluded countries")
            if other_disabled:
                disabled = [c.strip() for c in other_disabled.split(",")]
            regions_config["ship_regions"]["disabled"] = disabled
            print(f"   ❌ 排除 {len(disabled)} 个国家")
    
    # 物流方式
    print("\n【物流方式 | Logistics】")
    logistics_methods = []
    
    common_methods = ["DHL", "FedEx", "UPS", "顺丰", "EMS", "邮政", "本地快递"]
    for method in common_methods:
        if get_yes_no(f"使用 {method}？| Use {method}?"):
            logistics_methods.append(method)
    
    # 自定义物流
    print("\n   其他物流方式（逗号分隔，留空跳过）")
    other_methods = get_input("   其他物流")
    if other_methods:
        logistics_methods.extend([m.strip() for m in other_methods.split(",")])
    
    regions_config["logistics"] = {
        "methods": logistics_methods if logistics_methods else ["本地快递"],
        "default_delivery_days": 7  # 国际物流默认7天
    }
    
    return regions_config

def setup_auto_match():
    """配置自动匹配"""
    print("\n" + "="*60)
    print("🤖 自动匹配配置 | Auto Matching")
    print("="*60 + "\n")
    
    print("⚡ 系统将自动搜索全球求购信息，匹配成功后通知你")
    print("   The system will auto-search global buyer requests")
    
    auto_match = {
        "enabled": True,
        "scan_interval_minutes": 30,
        "price_match_tolerance": 0.3,
        "keywords_weight": 0.6,
        "category_weight": 0.4,
        "min_match_score": 0.3,
        "notify_on_match": True,
        "auto_bid_enabled": False,
        "auto_bid_min_score": 0.8,
        "filter_by_region": True  # 按发货区域过滤
    }
    
    if get_yes_no("启用自动搜索匹配？| Enable auto matching?", "y"):
        interval = get_input("搜索间隔（分钟）| Scan interval (minutes)", "30")
        try:
            auto_match["scan_interval_minutes"] = int(interval)
        except:
            pass
        
        auto_match["enabled"] = True
    else:
        auto_match["enabled"] = False
    
    return auto_match

def run_setup():
    """执行完整安装引导"""
    print_header()
    print_scoring_intro()
    
    # 基本信息
    basic_info = setup_basic_info()
    
    # 产品清单
    products = []
    print("\n" + "="*60)
    print("📦 产品清单配置 | Product Catalog")
    print("="*60)
    
    while True:
        product = setup_product()
        products.append(product)
        
        if not get_yes_no("\n继续添加下一个产品？| Add another product? (y/n)"):
            break
    
    # 发货区域（全球视角）
    shipping_config = setup_shipping_regions_global()
    
    # 自动匹配
    auto_match = setup_auto_match()
    
    # 组装完整配置
    catalog = {
        "seller_id": basic_info["seller_id"],
        "seller_name": basic_info["seller_name"],
        "seller_country": basic_info["seller_country"],
        "contact": basic_info["contact"],
        "products": products,
        "ship_regions": shipping_config["ship_regions"],
        "logistics": shipping_config["logistics"],
        "auto_match": auto_match,
        "setup_completed": True,
        "setup_time": datetime.now().isoformat(),
        "version": "2.2.0"
    }
    
    # 保存
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    CATALOG_FILE.write_text(json.dumps(catalog, indent=2, ensure_ascii=False))
    
    # 保存区域配置
    region_config = {
        "seller_id": basic_info["seller_id"],
        "seller_name": basic_info["seller_name"],
        "seller_country": basic_info["seller_country"],
        "ship_regions": shipping_config["ship_regions"],
        "logistics": shipping_config["logistics"]
    }
    REGION_FILE.write_text(json.dumps(region_config, indent=2, ensure_ascii=False))
    
    # 完成提示
    mode = shipping_config["ship_regions"]["mode"]
    mode_desc = {
        "local": "本国发货",
        "regional": f"区域发货（{len(shipping_config['ship_regions']['countries'])}个国家）",
        "global": "全球发货"
    }
    
    print("\n" + "╔"+ "="*58 + "╗")
    print("║" + " "*58 + "║")
    print("║    ✅ 配置完成！你的产品清单已保存                        ║")
    print("║    Configuration complete!                                 ║")
    print("║" + " "*58 + "║")
    print("╚" + "="*58 + "╝")
    
    print(f"""
📊 配置摘要 | Configuration Summary：
   • 卖家ID: {basic_info['seller_id']}
   • 店铺名称: {basic_info['seller_name']}
   • 所在国家: {basic_info['seller_country']}
   • 产品数量: {len(products)}
   • 发货模式: {mode_desc.get(mode, mode)}
   • 自动匹配: {'已启用 | Enabled' if auto_match['enabled'] else '未启用 | Disabled'}

🚀 下一步 | Next Steps：
   1. 系统将每{auto_match['scan_interval_minutes']}分钟自动搜索匹配
   2. 发现商机时会自动通知你 | Auto-notify when opportunities found
   3. 你也可以手动搜索："搜索 [产品名] 求购信息"

💡 提高中标率 | Increase Win Rate：
   • 补充资质文件链接（真品证明+20%）
   • 上传商品图片视频（展示+15%）
   • 提供店铺成交记录（信誉+10%）

📁 配置文件位置 | Config Files：
   {CATALOG_FILE}
""")
    
    return catalog

def quick_setup():
    """快速配置（只配置必填项 - 全球视角）"""
    print_header()
    
    print("⚡ 快速配置模式 - 只配置必要信息\n")
    
    print("🌍 你来自哪个国家/地区？| Your country/region")
    seller_country = get_input("国家/地区", required=True)
    
    seller_name = get_input("店铺/企业名称 | Shop name", required=True)
    category = get_input("产品类别 | Category (如：红酒、数码、服装)", required=True)
    
    # 发货范围快速选择
    print("\n📍 发货范围 | Shipping scope：")
    print("   1. 本国 | Local (only your country)")
    print("   2. 全球 | Global (worldwide)")
    ship_choice = get_input("选择 (1/2)", "1")
    
    ship_mode = "local" if ship_choice == "1" else "global"
    ship_countries = [seller_country] if ship_mode == "local" else ["全球"]
    
    catalog = {
        "seller_id": f"seller-{datetime.now().strftime('%Y%m%d%H%M%S')}",
        "seller_name": seller_name,
        "seller_country": seller_country,
        "products": [
            {
                "product_id": f"PROD-{datetime.now().strftime('%Y%m%d%H%M%S')}",
                "name": category,
                "category": category,
                "keywords": [category],
                "active": True
            }
        ],
        "ship_regions": {
            "mode": ship_mode,
            "enabled": ship_countries,
            "disabled": [],
            "countries": ship_countries
        },
        "logistics": {
            "methods": ["本地快递"],
            "default_delivery_days": 7
        },
        "auto_match": {
            "enabled": True,
            "scan_interval_minutes": 30,
            "min_match_score": 0.3,
            "notify_on_match": True,
            "filter_by_region": True
        },
        "setup_completed": True,
        "setup_time": datetime.now().isoformat(),
        "version": "2.2.0"
    }
    
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    CATALOG_FILE.write_text(json.dumps(catalog, indent=2, ensure_ascii=False))
    
    print(f"\n✅ 快速配置完成！| Quick setup complete!")
    print(f"   店铺: {seller_name}")
    print(f"   国家: {seller_country}")
    print(f"   类别: {category}")
    print(f"   发货: {'本国' if ship_mode == 'local' else '全球'}")
    print(f"\n💡 后续可运行完整配置补充更多信息，提高中标率")
    
    return catalog

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="OW Seller 安装引导 | Setup Wizard")
    parser.add_argument("--quick", action="store_true", help="快速配置模式 | Quick setup")
    args = parser.parse_args()
    
    if args.quick:
        quick_setup()
    else:
        run_setup()