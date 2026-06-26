#!/usr/bin/env python3
"""
OW Seller 自动搜索匹配脚本 V2.5
全球卖家版本 - 卖家自己选择发货区域（本国/全球/指定国家）
信用系统为可选功能

功能：
1. 搜索OW社区求购信息
2. 智能匹配产品清单
3. 区域匹配 - 根据卖家配置的发货范围筛选买家
4. 通知卖家新商机
5. 展示买家信用（可选）

发货模式：
- local: 本国发货，只匹配本国买家
- regional: 区域发货，匹配指定国家买家
- global: 全球发货，匹配任何国家买家
"""

import json
import urllib.request
import re
from datetime import datetime
from pathlib import Path

STATE_DIR = Path(__file__).parent.parent / "state"
CATALOG_FILE = STATE_DIR / "product_catalog.json"
REGION_FILE = STATE_DIR / "region_config.json"
MATCH_LOG_FILE = STATE_DIR / "match_log.json"

# OW API URL - 可通过环境变量配置，默认使用 HTTPS
import os
OW_API = os.environ.get("OW_API_URL", "https://www.owshanghai.com/api/posts") + "?type=request&limit=50"

# 信用系统为可选功能，不修改 sys.path
CREDIT_SYSTEM_ENABLED = False
format_buyer_credit_display = None
get_credit_warning = None
get_buyer_profile = None

def get_simple_credit_display(buyer_id: str) -> str:
    """简化版信用信息显示（当信用系统未安装时）"""
    return "📊 信用系统未安装\n   安装：npx skills add Enze-dai/ow-skills/ow-credit"

# IP区域映射（简化版）
IP_REGION_MAP = {
    # 中国IP前缀 -> 区域
    "202": "中国", "203": "中国", "210": "中国", "211": "中国",
    "218": "中国", "219": "中国", "220": "中国", "221": "中国",
    "222": "中国", "58": "中国", "59": "中国", "60": "中国",
    "61": "中国", "116": "中国", "117": "中国", "118": "中国",
    "119": "中国", "120": "中国", "121": "中国", "122": "中国",
    "123": "中国", "124": "中国", "125": "中国",
    
    # 香港
    "203.186": "香港", "218.102": "香港",
    
    # 台湾
    "61.216": "台湾", "61.217": "台湾", "61.218": "台湾",
    
    # 海外主要国家
    "8": "美国", "12": "美国", "13": "美国", "14": "美国",
    "23": "美国", "24": "美国", "26": "美国", "27": "美国",
    "50": "美国", "51": "美国", "52": "美国", "53": "美国",
    "54": "美国", "64": "美国", "65": "美国", "66": "美国",
    "67": "美国", "68": "美国", "69": "美国", "70": "美国",
    "71": "美国", "72": "美国", "73": "美国", "74": "美国",
    
    "153": "日本", "150": "日本",
    "133": "韩国", "147": "韩国",
    "62": "欧洲", "80": "欧洲", "81": "欧洲", "82": "欧洲",
    "83": "欧洲", "84": "欧洲", "85": "欧洲", "86": "欧洲",
    "87": "欧洲", "88": "欧洲", "89": "欧洲", "90": "欧洲",
    "91": "欧洲", "92": "欧洲", "93": "欧洲", "94": "欧洲",
    "95": "欧洲",
}

def load_catalog():
    """加载产品清单"""
    with open(CATALOG_FILE, 'r') as f:
        return json.load(f)

def save_catalog(catalog):
    """保存产品清单"""
    with open(CATALOG_FILE, 'w') as f:
        json.dump(catalog, f, ensure_ascii=False, indent=2)

def load_region_config():
    """加载区域配置"""
    if REGION_FILE.exists():
        try:
            with open(REGION_FILE, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"加载区域配置失败: {e}")
    # 默认配置
    return {
        "ship_regions": {
            "enabled": ["中国-全国"],
            "disabled": [],
            "international": {"enabled": False, "countries": []}
        }
    }

def get_region_from_ip(ip_address):
    """根据IP地址判断区域"""
    if not ip_address:
        return "未知"
    
    # 提取IP前缀
    ip_prefix = ip_address.split('.')[0]
    
    # 直接匹配
    if ip_prefix in IP_REGION_MAP:
        base_region = IP_REGION_MAP[ip_prefix]
        
        # 进一步判断是否港澳台
        if base_region == "中国":
            # 检查是否港澳台特殊IP段
            for prefix, region in IP_REGION_MAP.items():
                if ip_address.startswith(prefix) and region in ["香港", "台湾", "澳门"]:
                    return region
            return "中国"
        
        return base_region
    
    # 默认判断
    try:
        prefix_num = int(ip_prefix)
        if prefix_num >= 1 and prefix_num <= 126:
            return "美国/欧洲"  # 北美/欧洲常见
        elif prefix_num >= 200 and prefix_num <= 223:
            return "中国"  # 中国常见段
    except:
        pass
    
    return "海外"

def can_ship_to_region(buyer_region, region_config, seller_country=None):
    """判断是否可发货到买家区域（全球卖家视角）"""
    ship_regions = region_config.get("ship_regions", {})
    mode = ship_regions.get("mode", "local")  # local/regional/global
    
    enabled = ship_regions.get("enabled", [])
    disabled = ship_regions.get("disabled", [])
    countries = ship_regions.get("countries", [])
    
    # 检查是否在禁发列表
    for dis in disabled:
        if buyer_region in dis or dis in buyer_region:
            return False, f"不可发货到 {buyer_region} | Cannot ship to {buyer_region}"
    
    # 根据发货模式判断
    if mode == "global":
        # 全球发货模式 - 接受所有买家（除非在禁发列表）
        return True, f"全球发货，可发货到 {buyer_region} | Global shipping"
    
    elif mode == "local":
        # 本国发货模式 - 只接受本国买家
        # 特殊处理：未知区域
        if buyer_region == "未知" or buyer_region == "Unknown":
            if ship_regions.get("allow_unknown_as_local", True):
                return True, f"本国发货，默认可发货（买家区域未知，视为本国）"
            return False, f"仅本国发货，买家区域未知"
        
        if buyer_region == seller_country:
            return True, f"本国发货，可发货到 {buyer_region}"
        # 检查enabled列表
        for en in enabled:
            if buyer_region in en or en in buyer_region:
                return True, f"可发货到 {buyer_region}"
        return False, f"仅本国发货，不可发货到 {buyer_region}"
    
    elif mode == "regional":
        # 区域发货模式 - 检查是否在指定国家列表
        # 特殊处理：未知区域
        if buyer_region == "未知" or buyer_region == "Unknown":
            if ship_regions.get("allow_unknown", False):
                return True, f"允许未知区域买家"
            return False, f"买家区域未知，无法判断发货范围"
        
        for country in countries:
            if buyer_region in country or country in buyer_region:
                return True, f"区域发货，可发货到 {buyer_region}"
        return False, f"不在发货范围内 | Not in shipping region"
    
    # 默认：检查enabled列表
    for en in enabled:
        if buyer_region in en or en in buyer_region:
            return True, f"可发货到 {buyer_region}"
    
    return False, f"不在发货范围内 | Not in shipping range"

def search_requests():
    """搜索求购信息"""
    try:
        with urllib.request.urlopen(OW_API, timeout=30) as response:
            data = json.loads(response.read().decode('utf-8'))
        if data.get('success'):
            return data.get('posts', [])
    except Exception as e:
        print(f"获取求购信息失败: {e}")
        return []

def calculate_match_score(content, product, config):
    """计算匹配分数"""
    score = 0
    matched_keywords = []
    
    content_lower = content.lower()
    
    # 关键词匹配
    keywords = product.get('keywords', [])
    keyword_count = len(keywords) if keywords else 1
    keyword_weight = config.get('keywords_weight', 0.6)
    
    for keyword in keywords:
        if keyword.lower() in content_lower:
            matched_keywords.append(keyword)
            score += keyword_weight / keyword_count
    
    # 类别匹配
    category = product.get('category', '')
    if category and category.lower() in content_lower:
        score += config.get('category_weight', 0.4)
    
    return score, matched_keywords

def run_match():
    """执行匹配（全球卖家视角）"""
    catalog = load_catalog()
    region_config = load_region_config()
    config = catalog.get('auto_match', {})
    
    # 获取卖家所在国家
    seller_country = catalog.get('seller_country', '') or region_config.get('seller_country', '')
    
    # 发货模式
    ship_mode = region_config.get('ship_regions', {}).get('mode', 'local')
    ship_countries = region_config.get('ship_regions', {}).get('countries', [])
    
    if not config.get('enabled', True):
        print("自动匹配未启用 | Auto matching disabled")
        return []
    
    print(f"\n🔍 [{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 开始搜索匹配...")
    print(f"   卖家: {catalog.get('seller_name')}")
    print(f"   所在国家: {seller_country}")
    print(f"   产品数: {len(catalog.get('products', []))}")
    
    # 显示发货模式
    if ship_mode == "global":
        print(f"   发货模式: 🌍 全球发货")
    elif ship_mode == "local":
        print(f"   发货模式: 📍 本国发货 ({seller_country})")
    else:
        print(f"   发货模式: 🌐 区域发货 ({len(ship_countries)} 个国家)")
    
    # 获取求购信息
    posts = search_requests()
    print(f"   求购信息: {len(posts)} 条 | Buyer requests")
    
    matches = []
    region_filtered = []
    seen_post_ids = set(m.get('post_id') for m in catalog.get('matches', []))
    
    for post in posts:
        post_id = post.get('id')
        content = post.get('content', '')
        
        # 获取买家IP区域（从post数据中提取）
        buyer_ip = post.get('buyer_ip', '') or post.get('ip', '')
        buyer_region = get_region_from_ip(buyer_ip)
        
        # 如果没有IP数据，尝试从内容推断区域
        if buyer_region == "未知":
            # 检查内容中的地区关键词
            region_keywords = {
                "上海": "中国-华东", "北京": "中国-华北", 
                "广州": "中国-华南", "深圳": "中国-华南",
                "成都": "中国-西南", "杭州": "中国-华东",
                "南京": "中国-华东", "武汉": "中国-华中",
                "香港": "香港", "台湾": "台湾", "澳门": "澳门",
                "美国": "美国", "日本": "日本", "韩国": "韩国"
            }
            for kw, region in region_keywords.items():
                if kw in content:
                    buyer_region = region
                    break
        
        for product in catalog.get('products', []):
            if not product.get('active', True):
                continue
            
            # 先检查区域匹配（全球卖家视角）
            can_ship, ship_reason = can_ship_to_region(buyer_region, region_config, seller_country)
            
            if not can_ship:
                region_filtered.append({
                    "post_id": post_id,
                    "product": product.get('name'),
                    "buyer_region": buyer_region,
                    "reason": ship_reason
                })
                continue  # 跳过不可发货区域
            
            # 产品匹配计算
            score, matched_keywords = calculate_match_score(content, product, config)
            
            if score >= config.get('min_match_score', 0.3):
                is_new = post_id not in seen_post_ids
                
                match_info = {
                    "post_id": post_id,
                    "buyer_name": post.get('agent_name'),
                    "buyer_id": post.get('agent_id'),
                    "buyer_ip": buyer_ip,
                    "buyer_region": buyer_region,
                    "content": content[:500],
                    "created_at": post.get('created_at'),
                    "product": product.get('name'),
                    "product_id": product.get('product_id'),
                    "match_score": round(score, 2),
                    "matched_keywords": matched_keywords,
                    "ship_status": ship_reason,
                    "is_new": is_new,
                    "notified_at": datetime.now().isoformat() if is_new else None
                }
                
                matches.append(match_info)
                
                if is_new:
                    print(f"\n🎯 发现新商机!")
                    print(f"   买家: {post.get('agent_name')}")
                    print(f"   区域: {buyer_region}")
                    print(f"   产品: {product.get('name')}")
                    print(f"   匹配分数: {round(score, 2)}")
                    print(f"   发货状态: ✅ {ship_reason}")
                    print(f"   关键词: {', '.join(matched_keywords)}")
                    
                    # 🛡️ 展示买家信用
                    if CREDIT_SYSTEM_ENABLED:
                        try:
                            buyer_id = post.get('agent_id', post.get('agent_name'))
                            credit_display = format_buyer_credit_display(buyer_id)
                            warning = get_credit_warning(buyer_id, "buyer")
                            print(f"\n   ─── 🛡️ 买家信用信息 ───")
                            for line in credit_display.strip().split('\n'):
                                print(f"   {line}")
                            if warning:
                                print(f"   {warning}")
                        except Exception as e:
                            print(f"   ⚠️ 信用信息获取失败: {e}")
                    
                    # 🔔 创建商机通知（提醒卖家机器人）
                    try:
                        from opportunity_notify import create_opportunity_notification
                        notification = create_opportunity_notification(match_info)
                        if notification.get('delivered', False):
                            print(f"\n   🔔 已通知卖家机器人")
                        
                        # 检查是否开启自动投标
                        if config.get('auto_bid_enabled', False):
                            from opportunity_notify import process_auto_bid
                            auto_result = process_auto_bid(match_info, catalog)
                            if auto_result.get('success'):
                                print(f"   🤖 自动投标成功！")
                            elif auto_result.get('skipped'):
                                print(f"   ⏭️ 自动投标跳过: {auto_result.get('reason')}")
                    except Exception as e:
                        print(f"   ⚠️ 通知创建失败: {e}")
    
    # 显示区域过滤统计
    if region_filtered:
        print(f"\n📍 区域过滤: {len(region_filtered)} 个需求因发货区域限制被排除")
        for rf in region_filtered[:3]:  # 只显示前3个
            print(f"   • {rf['product']} -> {rf['buyer_region']} ({rf['reason']})")
    
    # 更新匹配记录
    all_matches = catalog.get('matches', []) + matches
    unique_matches = {m['post_id']: m for m in all_matches}.values()
    catalog['matches'] = list(unique_matches)[-50:]
    catalog['last_scan'] = datetime.now().isoformat()
    
    save_catalog(catalog)
    
    new_count = sum(1 for m in matches if m.get('is_new'))
    print(f"\n📊 搜索完成:")
    print(f"   发现 {len(matches)} 个匹配（可发货区域）")
    print(f"   其中 {new_count} 个新商机")
    print(f"   排除 {len(region_filtered)} 个不可发货区域需求")
    
    return matches

def check_single_match(product_name):
    """检查单个产品的匹配情况"""
    catalog = load_catalog()
    region_config = load_region_config()
    
    posts = search_requests()
    
    print(f"\n🔍 搜索匹配: {product_name}")
    
    for post in posts:
        content = post.get('content', '')
        if product_name.lower() in content.lower():
            buyer_ip = post.get('buyer_ip', '') or post.get('ip', '')
            buyer_region = get_region_from_ip(buyer_ip)
            can_ship, reason = can_ship_to_region(buyer_region, region_config)
            
            print(f"\n📌 找到需求:")
            print(f"   ID: {post.get('id')}")
            print(f"   买家: {post.get('agent_name')}")
            print(f"   区域: {buyer_region}")
            print(f"   发货: {'✅ ' if can_ship else '❌ '}{reason}")
            print(f"   内容: {content[:200]}...")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="OW Seller 自动匹配")
    parser.add_argument("--product", help="检查单个产品匹配")
    args = parser.parse_args()
    
    if args.product:
        check_single_match(args.product)
    else:
        run_match()