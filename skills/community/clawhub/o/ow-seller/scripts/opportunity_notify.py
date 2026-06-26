#!/usr/bin/env python3
"""
OW Seller 商机提醒系统
当发现匹配的求购信息时，通知卖家机器人提醒卖家用户

两种模式：
1. 默认：提醒卖家，卖家决定是否投标（推荐）
2. 自动：开启自动投标模式（高风险）

功能：
1. 创建商机通知文件
2. 卖家机器人读取并提醒卖家
3. 卖家确认后提交投标
4. 自动投标模式（可选）
5. 展示买家信用信息（可选）
"""

import json
import urllib.request
import urllib.parse
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional

STATE_DIR = Path(__file__).parent.parent / "state"
OPPORTUNITIES_DIR = STATE_DIR / "opportunities"
NOTIFICATIONS_DIR = STATE_DIR / "notifications"
CATALOG_FILE = STATE_DIR / "product_catalog.json"

# OW API URL - 可通过环境变量配置，默认使用 HTTPS
import os
OW_API = os.environ.get("OW_API_URL", "https://www.owshanghai.com/api")

# 信用系统为可选功能，不修改 sys.path
CREDIT_SYSTEM_ENABLED = False
format_buyer_credit_display = None
get_credit_warning = None
get_buyer_profile = None

def get_simple_credit_display(buyer_id: str) -> str:
    """简化版信用信息显示（当信用系统未安装时）"""
    return "📊 信用系统未安装\n   安装：npx skills add Enze-dai/ow-skills/ow-credit"

def create_opportunity_notification(opportunity: Dict) -> Dict:
    """创建商机通知"""
    NOTIFICATIONS_DIR.mkdir(parents=True, exist_ok=True)
    OPPORTUNITIES_DIR.mkdir(parents=True, exist_ok=True)
    
    notification_id = f"OPP-{datetime.now().strftime('%Y%m%d%H%M%S')}"
    post_id = opportunity.get('post_id', 'unknown')
    
    notification = {
        "notification_id": notification_id,
        "type": "new_opportunity",
        "timestamp": datetime.now().isoformat(),
        "opportunity": opportunity,
        "delivered": False,
        "action_required": "confirm_bid",  # confirm_bid / auto_bid
        "message": format_opportunity_message(opportunity)
    }
    
    # 保存通知
    notif_file = NOTIFICATIONS_DIR / f"{notification_id}.json"
    notif_file.write_text(json.dumps(notification, indent=2, ensure_ascii=False))
    
    # 保存商机详情
    opp_file = OPPORTUNITIES_DIR / f"{post_id}.json"
    opp_file.write_text(json.dumps(opportunity, indent=2, ensure_ascii=False))
    
    return notification

def format_opportunity_message(opp: Dict) -> str:
    """格式化商机提醒消息"""
    score = opp.get('match_score', 0)
    score_desc = "高度匹配" if score >= 0.8 else "匹配" if score >= 0.5 else "可能匹配"
    
    msg = f"""
🎯 发现新商机 | New Business Opportunity

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📋 需求ID: {opp.get('post_id')}
👤 买家: {opp.get('buyer_name', '未知')}
📍 区域: {opp.get('buyer_region', '未知')}
📦 匹配产品: {opp.get('product')}
📊 匹配度: {score:.0%} ({score_desc})
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📝 需求内容:
{opp.get('content', '')[:300]}...

✅ 发货状态: {opp.get('ship_status', '可发货')}
🔑 匹配关键词: {', '.join(opp.get('matched_keywords', []))}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
    
    # 🛡️ 添加买家信用展示
    if CREDIT_SYSTEM_ENABLED:
        try:
            buyer_id = opp.get('buyer_id', opp.get('buyer_name'))
            credit_display = format_buyer_credit_display(buyer_id)
            warning = get_credit_warning(buyer_id, "buyer")
            msg += f"🛡️ 买家信用信息:{credit_display}\n"
            if warning:
                msg += f"{warning}\n"
            msg += "\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        except Exception as e:
            msg += f"⚠️ 信用信息获取失败: {e}\n\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
    
    msg += f"""💡 回复以下命令操作：

1️⃣ 投标："投标 {opp.get('post_id')}"
2️⃣ 查看详情："查看需求 {opp.get('post_id')}"
3️⃣ 忽略："忽略 {opp.get('post_id')}"

⚠️ 提醒：投标后将发送你的产品信息和店铺链接给买家
"""
    return msg

def format_bid_confirmation(opp: Dict, bid_result: Dict) -> str:
    """格式化投标确认消息"""
    return f"""
✅ 投标成功 | Bid Submitted

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📋 需求ID: {opp.get('post_id')}
👤 买家: {opp.get('buyer_name')}
📦 产品: {opp.get('product')}
💰 报价: ¥{bid_result.get('price', '待商议')}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 你的投标信息已发送给买家：
• 产品名称和规格
• 报价范围
• 物流时效
• 店铺链接

💡 等待买家评标，中标后会通知你！
"""

def submit_bid(opportunity: Dict, catalog: Dict) -> Dict:
    """提交投标到OW社区"""
    product_name = opportunity.get('product')
    
    # 找到匹配的产品
    product = None
    for p in catalog.get('products', []):
        if p.get('name') == product_name:
            product = p
            break
    
    if not product:
        return {"error": f"未找到产品: {product_name}"}
    
    # 构建投标内容
    bid_content = f"""
📦【投标】{product.get('name')}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🏪 供应商：{catalog.get('seller_name')}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💰 价格：¥{product.get('price_range', [0, 0])[0]} - ¥{product.get('price_range', [0, 0])[1]}
🚚 物流：{', '.join(product.get('delivery', {}).get('methods', ['快递']))}，预计{product.get('delivery', {}).get('default_days', 3)}天到货
📦 库存：{product.get('stock', '充足')}

📜 资质证明：
"""
    
    # 添加资质信息
    auth_docs = product.get('auth_docs', [])
    for doc in auth_docs:
        if isinstance(doc, dict):
            bid_content += f"• {doc.get('type', '证明文件')}\n"
        else:
            bid_content += f"• {doc}\n"
    
    # 添加店铺链接
    shop_links = product.get('shop_links', [])
    if shop_links:
        bid_content += "\n🔗 店铺链接：\n"
        for shop in shop_links:
            bid_content += f"• {shop.get('platform')}: {shop.get('url')}\n"
    
    # 添加图片视频（如有）
    images = product.get('images', [])
    if images:
        bid_content += f"\n📸 商品图片：{len(images)}张\n"
    video = product.get('video')
    if video:
        bid_content += f"🎥 商品视频：有\n"
    
    # 提交到OW API
    try:
        bid_data = {
            "agent_id": catalog.get('seller_id'),
            "agent_name": catalog.get('seller_name'),
            "content": bid_content,
            "type": "bid",
            "parent_id": opportunity.get('post_id')
        }
        
        req = urllib.request.Request(
            f"{OW_API}/posts",
            data=json.dumps(bid_data).encode('utf-8'),
            headers={'Content-Type': 'application/json'},
            method='POST'
        )
        
        with urllib.request.urlopen(req, timeout=30) as response:
            result = json.loads(response.read().decode('utf-8'))
        
        if result.get('success'):
            return {
                "success": True,
                "bid_id": result.get('post', {}).get('id'),
                "price": product.get('price_range', [0, 0])[0],
                "message": "投标成功"
            }
        else:
            return {"error": result.get('error', '投标失败')}
    
    except Exception as e:
        return {"error": f"投标失败: {str(e)}"}

def process_auto_bid(opportunity: Dict, catalog: Dict) -> Dict:
    """处理自动投标"""
    config = catalog.get('auto_match', {})
    
    if not config.get('auto_bid_enabled', False):
        return {"skipped": True, "reason": "自动投标未开启"}
    
    min_score = config.get('auto_bid_min_score', 0.8)
    if opportunity.get('match_score', 0) < min_score:
        return {"skipped": True, "reason": f"匹配度不足（{opportunity.get('match_score'):.0%}<{min_score:.0%}）"}
    
    # 执行自动投标
    return submit_bid(opportunity, catalog)

def confirm_bid(post_id: str, custom_price: Optional[float] = None) -> Dict:
    """卖家确认投标"""
    # 加载商机
    opp_file = OPPORTUNITIES_DIR / f"{post_id}.json"
    if not opp_file.exists():
        return {"error": f"未找到商机: {post_id}"}
    
    opportunity = json.loads(opp_file.read_text())
    
    # 加载产品清单
    catalog = json.loads(CATALOG_FILE.read_text())
    
    # 如果有自定义价格，临时修改
    if custom_price:
        for p in catalog.get('products', []):
            if p.get('name') == opportunity.get('product'):
                p['price_range'] = [custom_price, custom_price]
                break
    
    # 提交投标
    result = submit_bid(opportunity, catalog)
    
    if result.get('success'):
        # 创建投标确认通知
        notification = {
            "notification_id": f"BID-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "type": "bid_confirmed",
            "timestamp": datetime.now().isoformat(),
            "opportunity": opportunity,
            "bid_result": result,
            "delivered": True,
            "message": format_bid_confirmation(opportunity, result)
        }
        
        notif_file = NOTIFICATIONS_DIR / f"bid_{post_id}.json"
        notif_file.write_text(json.dumps(notification, indent=2, ensure_ascii=False))
    
    return result

def ignore_opportunity(post_id: str) -> Dict:
    """忽略商机"""
    opp_file = OPPORTUNITIES_DIR / f"{post_id}.json"
    if opp_file.exists():
        opportunity = json.loads(opp_file.read_text())
        opportunity['ignored'] = True
        opportunity['ignored_at'] = datetime.now().isoformat()
        opp_file.write_text(json.dumps(opportunity, indent=2, ensure_ascii=False))
        return {"success": True, "message": f"已忽略商机 {post_id}"}
    return {"error": f"未找到商机: {post_id}"}

def get_pending_opportunities() -> List[Dict]:
    """获取待处理的商机"""
    if not OPPORTUNITIES_DIR.exists():
        return []
    
    pending = []
    for opp_file in OPPORTUNITIES_DIR.glob("*.json"):
        opportunity = json.loads(opp_file.read_text())
        if not opportunity.get('ignored') and not opportunity.get('bid_submitted'):
            pending.append(opportunity)
    
    return pending

def get_opportunity_details(post_id: str) -> Optional[Dict]:
    """获取商机详情"""
    opp_file = OPPORTUNITIES_DIR / f"{post_id}.json"
    if opp_file.exists():
        return json.loads(opp_file.read_text())
    return None

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="OW Seller 商机提醒系统")
    parser.add_argument("action", choices=["notify", "confirm", "ignore", "list", "details", "auto"])
    parser.add_argument("--post-id", help="需求ID")
    parser.add_argument("--price", type=float, help="自定义报价")
    parser.add_argument("--opportunity-json", help="商机JSON（用于notify）")
    
    args = parser.parse_args()
    
    if args.action == "notify":
        if not args.opportunity_json:
            print("需要 --opportunity-json")
            return
        opportunity = json.loads(args.opportunity_json)
        notification = create_opportunity_notification(opportunity)
        print(notification["message"])
    
    elif args.action == "confirm":
        if not args.post_id:
            print("需要 --post-id")
            return
        result = confirm_bid(args.post_id, args.price)
        if result.get('success'):
            print(f"✅ 投标成功！投标ID: {result.get('bid_id')}")
        else:
            print(f"❌ {result.get('error')}")
    
    elif args.action == "ignore":
        if not args.post_id:
            print("需要 --post-id")
            return
        result = ignore_opportunity(args.post_id)
        print(result.get('message', result.get('error')))
    
    elif args.action == "list":
        pending = get_pending_opportunities()
        print(f"📋 待处理商机: {len(pending)} 个\n")
        for opp in pending:
            print(f"  • [{opp.get('post_id')}] {opp.get('product')} -> {opp.get('buyer_name')} ({opp.get('match_score', 0):.0%})")
    
    elif args.action == "details":
        if not args.post_id:
            print("需要 --post-id")
            return
        opportunity = get_opportunity_details(args.post_id)
        if opportunity:
            print(format_opportunity_message(opportunity))
        else:
            print(f"未找到商机: {args.post_id}")
    
    elif args.action == "auto":
        # 处理自动投标
        catalog = json.loads(CATALOG_FILE.read_text())
        pending = get_pending_opportunities()
        
        print(f"🤖 自动投标模式处理 {len(pending)} 个商机...\n")
        
        for opp in pending:
            result = process_auto_bid(opp, catalog)
            if result.get('success'):
                print(f"✅ 自动投标成功: {opp.get('post_id')}")
            elif result.get('skipped'):
                print(f"⏭️ 跳过: {opp.get('post_id')} - {result.get('reason')}")
            else:
                print(f"❌ 自动投标失败: {opp.get('post_id')} - {result.get('error')}")

if __name__ == "__main__":
    main()