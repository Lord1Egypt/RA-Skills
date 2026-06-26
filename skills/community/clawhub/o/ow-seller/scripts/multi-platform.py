#!/usr/bin/env python3
"""
OW Seller 多平台搜索与发布脚本
搜索全球多个平台的求购信息，同时发布商品信息
使用 urllib 无需外部 CLI 依赖
"""

import json
import os
import sys
import urllib.request
from datetime import datetime
from pathlib import Path

# 平台配置
import os
PLATFORMS = {
    "ow": {
        "name": "OW社区",
        "search_api": os.environ.get("OW_API_URL", "https://www.owshanghai.com/api/posts") + "?type=request",
        "publish_api": os.environ.get("OW_API_URL", "https://www.owshanghai.com/api/posts"),
        "type": "api"
    },
    "wechat_mp": {
        "name": "微信公众号",
        "skill": "social-media-publish",
        "type": "skill"
    },
    "wechat_moments": {
        "name": "微信朋友圈",
        "skill": "social-media-publish",
        "type": "skill"
    },
    "wechat_channels": {
        "name": "微信视频号",
        "skill": "social-media-publish",
        "type": "skill"
    },
    "douyin": {
        "name": "抖音",
        "skill": "douyin-publish",
        "type": "skill"
    },
    "xiaohongshu": {
        "name": "小红书",
        "skill": "social-media-publish",
        "type": "skill"
    },
    "weibo": {
        "name": "微博",
        "skill": "social-media-publish",
        "type": "skill"
    },
    "twitter": {
        "name": "推特",
        "skill": "social-media-publish",
        "type": "skill"
    },
    "facebook": {
        "name": "Facebook",
        "skill": "social-media-publish",
        "type": "skill"
    },
    "baidu": {
        "name": "百度",
        "skill": "social-media-publish",
        "type": "skill"
    },
    "google": {
        "name": "谷歌",
        "skill": "social-media-publish",
        "type": "skill"
    }
}

def search_ow_requests(keyword):
    """搜索OW社区的求购信息（使用 urllib，无需 curl）"""
    try:
        url = os.environ.get("OW_API_URL", "https://www.owshanghai.com/api/posts") + "?type=request&limit=50"
        with urllib.request.urlopen(url, timeout=30) as response:
            data = json.loads(response.read().decode('utf-8'))
        
        if data.get("success"):
            posts = data.get("posts", [])
            # 过滤包含关键词的帖子
            matched = []
            for post in posts:
                content = post.get("content", "").lower()
                if keyword.lower() in content:
                    matched.append({
                        "platform": "OW社区",
                        "post_id": post.get("id"),
                        "agent_name": post.get("agent_name"),
                        "content": post.get("content", "")[:200],
                        "created_at": post.get("created_at")
                    })
            return matched
        return []
    except Exception as e:
        return [{"error": str(e), "platform": "OW社区"}]

def search_platform(platform, keyword):
    """搜索指定平台的求购信息"""
    platform_names = {
        "douyin": "抖音",
        "xiaohongshu": "小红书",
        "weibo": "微博",
        "twitter": "推特",
        "facebook": "Facebook",
        "baidu": "百度",
        "google": "谷歌"
    }
    
    return {
        "platform": platform_names.get(platform, platform),
        "action": "manual_search",
        "keyword": keyword,
        "instruction": f"请手动在{platform_names.get(platform, platform)}搜索：{keyword}"
    }

def multi_platform_search(keyword, platforms=None):
    """多平台搜索求购信息"""
    
    if platforms is None or "all" in [p.lower() for p in platforms]:
        platforms = list(PLATFORMS.keys())
    
    results = []
    
    for platform in platforms:
        platform = platform.lower().strip()
        
        if platform not in PLATFORMS:
            continue
        
        if platform == "ow":
            result = search_ow_requests(keyword)
            results.extend(result)
        else:
            result = search_platform(platform, keyword)
            results.append(result)
    
    return results

def generate_product_content(product_name, specs, price, shop_link, platform):
    """根据平台生成适配的商品发布内容"""
    
    templates = {
        "ow": {
            "content": f"【供应】{product_name}\n\n规格：{specs}\n价格：{price}\n店铺：{shop_link}\n\n有意者请联系！",
            "type": "offer"
        },
        "wechat_mp": {
            "title": f"【供应】{product_name}",
            "content": f"商品名称：{product_name}\n\n规格参数：\n{specs}\n\n💰 价格：{price}\n\n✅ 正品保证\n✅ 快速发货\n✅ 售后无忧\n\n🔗 购买链接：{shop_link}\n\n欢迎咨询购买！",
            "type": "图文消息"
        },
        "wechat_moments": {
            "content": f"✨ {product_name}\n\n{specs}\n\n💰 价格：{price}\n\n正品保证，欢迎咨询！\n\n👉 购买链接私信获取"
        },
        "wechat_channels": {
            "title": f"出售{product_name}",
            "content": f"✨ {product_name}\n\n{specs}\n💰 价格：{price}\n\n正品保证，购买链接在主页！#好物推荐 #{product_name}"
        },
        "douyin": {
            "title": f"出售{product_name}",
            "content": f"✨ {product_name}\n\n{specs}\n💰 价格：{price}\n\n👉 购买链接在主页\n\n#好物推荐 #{product_name} #购物分享",
            "tags": ["好物推荐", "购物", product_name]
        },
        "xiaohongshu": {
            "title": f"🛍️ {product_name} | 性价比之选",
            "content": f"姐妹们看过来！\n\n{specs}\n\n💰 价格：{price}\n\n✅ 正品保证\n✅ 发货快\n✅ 售后无忧\n\n🔗 店铺链接在主页\n\n#好物推荐 #购物分享 #{product_name}",
            "tags": ["好物推荐", "购物", product_name]
        },
        "weibo": {
            "content": f"【出售】{product_name}\n\n{specs}\n💰 价格：{price}\n\n👉 店铺：{shop_link}\n\n#好物推荐# #{product_name}#"
        },
        "twitter": {
            "content": f"🛒 Selling: {product_name}\n\n{specs}\n💰 Price: {price}\n\nShop: {shop_link}\n\n#selling #{product_name.replace(' ', '')}"
        },
        "facebook": {
            "content": f"🛒 FOR SALE\n\nProduct: {product_name}\n\n{specs}\n\n💰 Price: {price}\n\n✅ Authentic guarantee\n✅ Fast shipping\n\nShop link: {shop_link}\n\n#forsale #shopping"
        },
        "baidu": {
            "title": f"出售{product_name}，价格{price}",
            "content": f"本店销售{product_name}，{specs}。价格：{price}。正品保证，发货迅速，欢迎咨询购买。店铺链接：{shop_link}"
        },
        "google": {
            "content": f"Product: {product_name}\nSpecs: {specs}\nPrice: {price}\nShop: {shop_link}"
        }
    }
    
    return templates.get(platform, {"content": f"{product_name} - {price}"})

def publish_to_ow(product_name, specs, price, shop_link, agent_id, agent_name):
    """发布商品信息到OW社区（使用 urllib，无需 curl）"""
    content_data = generate_product_content(product_name, specs, price, shop_link, "ow")
    
    payload = {
        "agent_id": agent_id or "ow-seller",
        "agent_name": agent_name or "OW Seller",
        "content": content_data["content"],
        "type": content_data["type"]
    }
    
    try:
        data = json.dumps(payload, ensure_ascii=False).encode('utf-8')
        req = urllib.request.Request(
            PLATFORMS["ow"]["publish_api"],
            data=data,
            headers={"Content-Type": "application/json"},
            method="POST"
        )
        
        with urllib.request.urlopen(req, timeout=30) as response:
            result = json.loads(response.read().decode('utf-8'))
        
        if result.get("success"):
            return {"success": True, "platform": "OW社区", "post_id": result.get("post_id")}
        return {"success": False, "platform": "OW社区", "error": result.get("error")}
    except Exception as e:
        return {"success": False, "platform": "OW社区", "error": str(e)}

def publish_product(product_name, specs, price, shop_link, platforms=None, agent_id=None, agent_name=None):
    """多平台发布商品信息"""
    
    if platforms is None or "all" in [p.lower() for p in platforms]:
        platforms = list(PLATFORMS.keys())
    
    results = []
    
    for platform in platforms:
        platform = platform.lower().strip()
        
        if platform not in PLATFORMS:
            continue
        
        if platform == "ow":
            result = publish_to_ow(product_name, specs, price, shop_link, agent_id, agent_name)
        else:
            content = generate_product_content(product_name, specs, price, shop_link, platform)
            platform_names = {
                "douyin": "抖音",
                "xiaohongshu": "小红书",
                "weibo": "微博",
                "twitter": "推特",
                "facebook": "Facebook",
                "baidu": "百度"
            }
            result = {
                "success": True,
                "platform": platform_names.get(platform, platform),
                "action": "manual_publish",
                "content": content,
                "instruction": f"请使用 {PLATFORMS[platform]['skill']} 技能发布到{platform_names.get(platform, platform)}"
            }
        
        results.append(result)
    
    return results

def main():
    if len(sys.argv) < 2:
        print("用法:")
        print("  搜索: python multi-platform.py search <关键词> [平台1,平台2,...]")
        print("  发布: python multi-platform.py publish <商品名> <规格> <价格> <店铺链接> [平台1,平台2,...]")
        print()
        print("平台: ow, douyin, xiaohongshu, weibo, twitter, facebook, baidu, google, all")
        sys.exit(1)
    
    action = sys.argv[1]
    
    if action == "search":
        if len(sys.argv) < 3:
            print("请提供搜索关键词")
            sys.exit(1)
        
        keyword = sys.argv[2]
        platforms = sys.argv[3].split(",") if len(sys.argv) > 3 else ["ow"]
        
        print(f"\n🔍 开始多平台搜索求购信息...")
        print(f"   关键词: {keyword}")
        print(f"   平台: {', '.join(platforms)}")
        print()
        
        results = multi_platform_search(keyword, platforms)
        
        print("=" * 50)
        print(f"📊 搜索结果: 找到 {len([r for r in results if not r.get('error')])} 条信息")
        print("=" * 50)
        
        for result in results:
            if result.get("post_id"):
                print(f"\n📍 [{result['platform']}] 帖子#{result['post_id']}")
                print(f"   用户: {result.get('agent_name', 'Unknown')}")
                print(f"   内容: {result.get('content', '')[:100]}...")
            elif result.get("instruction"):
                print(f"\n📍 [{result['platform']}]")
                print(f"   指令: {result['instruction']}")
    
    elif action == "publish":
        if len(sys.argv) < 6:
            print("请提供商品名称、规格、价格、店铺链接")
            sys.exit(1)
        
        product_name = sys.argv[2]
        specs = sys.argv[3]
        price = sys.argv[4]
        shop_link = sys.argv[5]
        platforms = sys.argv[6].split(",") if len(sys.argv) > 6 else ["ow"]
        
        print(f"\n📤 开始多平台发布商品信息...")
        print(f"   商品: {product_name}")
        print(f"   规格: {specs}")
        print(f"   价格: {price}")
        print(f"   店铺: {shop_link}")
        print(f"   平台: {', '.join(platforms)}")
        print()
        
        results = publish_product(product_name, specs, price, shop_link, platforms)
        
        success_count = sum(1 for r in results if r.get("success"))
        
        print("=" * 50)
        print(f"📊 发布结果: {success_count}/{len(results)} 平台成功")
        print("=" * 50)
        
        for result in results:
            status = "✅" if result.get("success") else "❌"
            print(f"{status} {result.get('platform', 'Unknown')}")
            if result.get("post_id"):
                print(f"   帖子ID: {result['post_id']}")
            if result.get("instruction"):
                print(f"   指令: {result['instruction']}")
    
    else:
        print(f"未知操作: {action}")
        print("支持的操作: search, publish")
        sys.exit(1)

if __name__ == "__main__":
    main()