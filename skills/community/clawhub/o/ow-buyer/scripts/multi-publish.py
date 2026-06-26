#!/usr/bin/env python3
"""
OW Buyer 多平台发布脚本
将采购需求同步发布到多个平台
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
        "api": os.environ.get("OW_API_URL", "https://www.owshanghai.com/api/posts"),
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
        "name": "百度百家号",
        "skill": "social-media-publish",
        "type": "skill"
    },
    "google": {
        "name": "谷歌",
        "skill": "social-media-publish",
        "type": "skill"
    }
}

def generate_content(product, budget, platform):
    """根据平台生成适配的内容"""
    
    base_content = f"【求购】{product}\n预算：{budget}"
    
    templates = {
        "ow": {
            "content": f"求购：{product}，预算{budget}，有货的卖家请联系！",
            "type": "request"
        },
        "wechat_mp": {
            "title": f"【求购】{product}",
            "content": f"求购{product}，预算{budget}左右。\n\n要求：\n1. 正品保证\n2. 来源清晰\n3. 价格合理\n\n有货的商家请联系，长期合作优先！",
            "type": "图文消息"
        },
        "wechat_moments": {
            "content": f"【求购】{product}\n预算{budget}左右\n有靠谱渠道的朋友私信我！🙏"
        },
        "wechat_channels": {
            "title": f"求购{product}",
            "content": f"急求{product}！预算{budget}，有渠道的朋友私信！#求购 #采购"
        },
        "douyin": {
            "title": f"求购{product}",
            "content": f"急求{product}！预算{budget}，有渠道的朋友私信我！#求购 #采购",
            "tags": ["求购", "采购", "买东西"]
        },
        "xiaohongshu": {
            "title": f"📚 求购｜{product}",
            "content": f"姐妹们帮忙看看！想买{product}，预算{budget}左右，有靠谱渠道的求推荐！🙏\n\n#求购 #好物推荐 #购物分享",
            "tags": ["求购", "购物", "好物推荐"]
        },
        "weibo": {
            "content": f"【求购】{product}，预算{budget}，有货的商家私信！#求购# #采购#"
        },
        "twitter": {
            "content": f"🛒 Looking for: {product}\n💰 Budget: {budget}\nDM me if you have it! #procurement #buying"
        },
        "facebook": {
            "content": f"🛒 PROCUREMENT REQUEST\n\nProduct: {product}\nBudget: {budget}\n\nPlease DM if available!"
        },
        "baidu": {
            "title": f"求购{product}，预算{budget}",
            "content": f"本人在寻找{product}，预算{budget}左右，有正规渠道的商家请联系，要求质量保证、价格合理。"
        },
        "google": {
            "content": f"Procurement Request: {product} - Budget: {budget}"
        }
    }
    
    return templates.get(platform, {"content": base_content})

def publish_to_ow(product, budget, agent_id, agent_name):
    """发布到OW社区（使用 urllib，无需 curl）"""
    content_data = generate_content(product, budget, "ow")
    
    payload = {
        "agent_id": agent_id or "ow-buyer",
        "agent_name": agent_name or "OW Buyer",
        "content": content_data["content"],
        "type": content_data["type"]
    }
    
    try:
        data = json.dumps(payload, ensure_ascii=False).encode('utf-8')
        req = urllib.request.Request(
            PLATFORMS["ow"]["api"],
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

def publish_to_social(platform, product, budget):
    """发布到社交媒体平台"""
    content_data = generate_content(product, budget, platform)
    
    platform_names = {
        "douyin": "抖音",
        "xiaohongshu": "小红书",
        "weibo": "微博",
        "twitter": "推特",
        "facebook": "Facebook",
        "baidu": "百度百家号"
    }
    
    # 返回发布指令
    return {
        "success": True,
        "platform": platform_names.get(platform, platform),
        "action": "manual_publish",
        "content": content_data,
        "instruction": f"请使用 {PLATFORMS[platform]['skill']} 技能发布到{platform_names.get(platform, platform)}"
    }

def multi_publish(product, budget, platforms=None, agent_id=None, agent_name=None):
    """多平台发布"""
    
    if platforms is None or "all" in [p.lower() for p in platforms]:
        platforms = list(PLATFORMS.keys())
    
    results = []
    
    for platform in platforms:
        platform = platform.lower().strip()
        
        if platform not in PLATFORMS:
            results.append({
                "success": False,
                "platform": platform,
                "error": "不支持的平台"
            })
            continue
        
        if platform == "ow":
            result = publish_to_ow(product, budget, agent_id, agent_name)
        else:
            result = publish_to_social(platform, product, budget)
        
        results.append(result)
    
    return results

def main():
    if len(sys.argv) < 3:
        print("用法: python multi-publish.py <商品> <预算> [平台1,平台2,...] [agent_id] [agent_name]")
        print("平台: ow, douyin, xiaohongshu, weibo, twitter, facebook, baidu, google, all")
        sys.exit(1)
    
    product = sys.argv[1]
    budget = sys.argv[2]
    platforms = sys.argv[3].split(",") if len(sys.argv) > 3 else ["ow"]
    agent_id = sys.argv[4] if len(sys.argv) > 4 else "ow-buyer"
    agent_name = sys.argv[5] if len(sys.argv) > 5 else "OW Buyer"
    
    print(f"\n🛒 开始多平台发布采购需求...")
    print(f"   商品: {product}")
    print(f"   预算: {budget}")
    print(f"   平台: {', '.join(platforms)}")
    print()
    
    results = multi_publish(product, budget, platforms, agent_id, agent_name)
    
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
        if result.get("error"):
            print(f"   错误: {result['error']}")
    
    # 保存发布记录
    record = {
        "timestamp": datetime.now().isoformat(),
        "product": product,
        "budget": budget,
        "platforms": platforms,
        "results": results
    }
    
    record_file = Path(__file__).parent.parent / "state" / "multi-publish" / f"publish_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    record_file.parent.mkdir(parents=True, exist_ok=True)
    record_file.write_text(json.dumps(record, ensure_ascii=False, indent=2))
    
    print(f"\n📝 发布记录已保存: {record_file}")
    
    return success_count == len(results)

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)