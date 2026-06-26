#!/usr/bin/env python3
"""
Price Alert Monitor - 商品价格监控工具
"""
import os
import sys
import json
import re
import argparse
from datetime import datetime
from urllib.parse import urlparse

DATA_FILE = os.path.expanduser("~/.price-monitor.json")

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {"items": {}}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

def detect_platform(url):
    """检测商品平台"""
    if "jd.com" in url or "jd.hk" in url:
        return "jd"
    elif "taobao.com" in url or "tmall.com" in url:
        return "taobao"
    elif "amazon.com" in url or "amazon.cn" in url:
        return "amazon"
    elif "pinduoduo.com" in url:
        return "pdd"
    else:
        return "unknown"

def extract_product_id(url, platform):
    """提取商品ID"""
    if platform == "jd":
        match = re.search(r'/(\d+)\.html', url)
        return match.group(1) if match else None
    elif platform == "taobao":
        match = re.search(r'id=(\d+)', url)
        return match.group(1) if match else None
    elif platform == "amazon":
        match = re.search(r'/dp/([A-Z0-9]+)', url)
        return match.group(1) if match else None
    return None

def fetch_price(url, platform, product_id):
    """获取商品价格（模拟，实际需要对应平台API或爬虫）"""
    # 这里返回模拟数据，实际需要接入真实价格API
    import random
    return {
        "price": round(random.uniform(50, 500), 2),
        "currency": "¥",
        "in_stock": True,
    }

def cmd_add(args):
    data = load_data()
    url = args.url.strip()
    platform = detect_platform(url)
    product_id = extract_product_id(url, platform)
    
    if not product_id:
        print(f"❌ 无法识别商品ID，请检查URL")
        return
    
    item_id = str(len(data["items"]) + 1)
    
    # 获取初始价格
    price_info = fetch_price(url, platform, product_id)
    
    data["items"][item_id] = {
        "url": url,
        "platform": platform,
        "product_id": product_id,
        "added_at": datetime.now().isoformat(),
        "last_price": price_info["price"],
        "target_price": args.target or 0,
    }
    
    save_data(data)
    
    print(f"✅ 已添加监控")
    print(f"   平台: {platform}")
    print(f"   当前价: {price_info['currency']}{price_info['price']}")
    if args.target:
        print(f"   目标价: {price_info['currency']}{args.target}")

def cmd_list(args):
    data = load_data()
    if not data["items"]:
        print("📭 暂无监控商品")
        return
    
    print("📋 监控列表:")
    print("=" * 60)
    
    for item_id, item in data["items"].items():
        platform = item.get("platform", "unknown")
        target = item.get("target_price", 0)
        target_str = f"→ ¥{target}" if target > 0 else ""
        
        print(f"{item_id}. {item['url'][:50]}...")
        print(f"   💰 ¥{item['last_price']} {target_str}")

def cmd_check(args):
    data = load_data()
    if not data["items"]:
        print("📭 暂无监控商品")
        return
    
    print("🔄 检查价格...")
    print("=" * 60)
    
    for item_id, item in data["items"].items():
        price_info = fetch_price(item["url"], item["platform"], item["product_id"])
        old_price = item["last_price"]
        new_price = price_info["price"]
        
        change = new_price - old_price
        emoji = "📈" if change > 0 else "📉" if change < 0 else "➡️"
        
        print(f"{emoji} {item['product_id']}: ¥{old_price} → ¥{new_price} ({change:+.2f})")
        
        # 检查是否低于目标价
        target = item.get("target_price", 0)
        if target > 0 and new_price <= target:
            print(f"   🎉 价格已达目标！")
        
        # 更新价格
        item["last_price"] = new_price
    
    save_data(data)
    print("\n✅ 检查完成")

def cmd_alert(args):
    data = load_data()
    item_id = args.item_id
    
    if item_id not in data["items"]:
        print(f"❌ 商品 {item_id} 不存在")
        return
    
    data["items"][item_id]["target_price"] = float(args.price)
    save_data(data)
    print(f"✅ 已设置目标价: ¥{args.price}")

def main():
    parser = argparse.ArgumentParser(description="Price Alert Monitor")
    subparsers = parser.add_subparsers()
    
    p_add = subparsers.add_parser("add", help="添加商品监控")
    p_add.add_argument("url", help="商品URL")
    p_add.add_argument("--target", type=float, help="目标价格")
    p_add.set_defaults(func=cmd_add)
    
    p_list = subparsers.add_parser("list", help="查看监控列表")
    p_list.set_defaults(func=cmd_list)
    
    p_check = subparsers.add_parser("check", help="检查价格")
    p_check.set_defaults(func=cmd_check)
    
    p_alert = subparsers.add_parser("alert", help="设置价格提醒")
    p_alert.add_argument("item_id", help="商品ID")
    p_alert.add_argument("price", type=float, help="目标价格")
    p_alert.set_defaults(func=cmd_alert)
    
    args = parser.parse_args()
    
    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
