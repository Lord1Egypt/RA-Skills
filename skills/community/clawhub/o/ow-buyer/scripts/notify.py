#!/usr/bin/env python3
"""
OW Buyer 中标提醒系统
当卖家投标并被确认中标后，通知买家机器人提醒买家用户

功能：
1. 监控投标状态变化
2. 当有新投标时，通知买家机器人
3. 当评标完成并列出前三时，通知买家机器人
4. 当买家确认中标时，通知买家机器人最终结果
5. 展示卖家信用信息（可选功能）
"""

import json
import pathlib
from datetime import datetime
from typing import Dict, Any

STATE_DIR = pathlib.Path(__file__).resolve().parent.parent / "state"
BIDS_DIR = STATE_DIR / "bids"
REQUIREMENTS_DIR = STATE_DIR / "requirements"
NOTIFICATIONS_DIR = STATE_DIR / "notifications"

# 信用系统为可选功能，不修改 sys.path
CREDIT_SYSTEM_ENABLED = False
format_seller_credit_display = None
get_credit_warning = None
format_buyer_credit_display = None

def get_simple_credit_display(seller_id: str) -> str:
    """简化版信用信息显示（当信用系统未安装时）"""
    return "📊 信用系统未安装\n   安装：npx skills add Enze-dai/ow-skills/ow-credit"

# 买家机器人通知配置
BUYER_BOT_CONFIG = {
    "notify_on_new_bid": True,      # 有新投标时通知
    "notify_on_evaluation": True,   # 评标完成时通知
    "notify_on_winner": True,       # 确认中标时通知
    "min_bids_to_notify": 1,        # 至少几个投标才通知
    "notification_method": "local"  # local/webhook/message
}

def create_notification(req_id: str, notification_type: str, data: Dict) -> Dict:
    """创建买家机器人通知"""
    NOTIFICATIONS_DIR.mkdir(parents=True, exist_ok=True)
    
    notification = {
        "notification_id": f"NOTIF-{datetime.now().strftime('%Y%m%d%H%M%S')}",
        "req_id": req_id,
        "type": notification_type,
        "timestamp": datetime.now().isoformat(),
        "data": data,
        "delivered": False,
        "delivered_at": None
    }
    
    # 保存通知
    notif_file = NOTIFICATIONS_DIR / f"{req_id}_{notification_type}.json"
    notif_file.write_text(json.dumps(notification, indent=2, ensure_ascii=False))
    
    return notification

def format_new_bid_notification(req_id: str, bid: Dict) -> str:
    """格式化新投标通知"""
    msg = f"""
🔔 新投标提醒 | New Bid Received

需求ID: {req_id}
投标ID: {bid['bid_id']}
供应商: {bid['supplier']['name']}
报价: ¥{bid['price']['amount']}
承诺到货: {bid['delivery']['time_days']}天

💡 已收到投标，等待更多投标后开始评标...
"""
    
    # 🛡️ 添加卖家信用展示
    if CREDIT_SYSTEM_ENABLED:
        try:
            seller_id = bid["supplier"].get("agent_id", bid["supplier"]["name"])
            credit_display = format_seller_credit_display(seller_id)
            warning = get_credit_warning(seller_id, "seller")
            msg += f"\n─── 🛡️ 卖家信用信息 ───{credit_display}"
            if warning:
                msg += f"\n{warning}\n"
        except Exception as e:
            msg += f"\n⚠️ 信用信息获取失败: {e}\n"
    
    return msg

def format_evaluation_notification(req_id: str, result: Dict) -> str:
    """格式化评标完成通知"""
    top3 = result.get('top3', [])
    
    msg = f"""
📊 评标完成提醒 | Evaluation Complete

需求ID: {req_id}
投标总数: {result['total_bids']}
评标时间: {result['evaluated_at']}

🏆 前三名供应商：

"""
    
    medals = ["🏆", "🥈", "🥉"]
    for i, bid in enumerate(top3):
        medal = medals[i] if i < 3 else "📌"
        msg += f"{medal} 第{i+1}名：{bid['supplier']} | 综合得分 {bid['total_score']}\n"
        msg += f"   ├─ 价格：¥{bid['price']} (得分 {bid['price_score']:.1f}/50)\n"
        msg += f"   ├─ 真品：{len(bid.get('auth_docs', []))}项 (得分 {bid['auth_score']:.1f}/20)\n"
        msg += f"   ├─ 时效：{bid['delivery_days']}天 (得分 {bid['delivery_score']:.1f}/5)\n"
        msg += f"   └─ 信誉：{bid['reputation'].get('total_transactions', 0)}笔 (得分 {bid['reputation_score']:.1f}/10)\n"
        
        # 🛡️ 添加信用展示
        if CREDIT_SYSTEM_ENABLED:
            try:
                seller_id = bid.get('supplier_id', bid['supplier'])
                profile = get_seller_profile(seller_id) if 'get_seller_profile' in dir() else None
                if profile and profile.get('transaction_count', 0) >= 3:
                    credit_score = profile.get('信用分', 0)
                    level = profile.get('信用等级', ('', '', ''))[0] if profile.get('信用等级') else ''
                    msg += f"   🛡️ 信用：{level} ({credit_score}分)\n"
            except:
                pass
        
        msg += "\n"
    
    msg += """
⚠️ 请确认中标供应商，回复：
   "确认中标 REQ-xxx 第1名"
   或查看详情："查看投标详情 REQ-xxx"
"""
    
    return msg

def format_winner_notification(req_id: str, winner: Dict) -> str:
    """格式化中标确认通知"""
    return f"""
🎉 中标确认提醒 | Winner Confirmed

需求ID: {req_id}
中标供应商: {winner['supplier']}
中标价格: ¥{winner['price']}
综合得分: {winner['total_score']}

🔗 下一步：
1. 点击店铺链接下单：{winner.get('shop_url', '待提供')}
2. 或回复："获取店铺链接"
3. 完成交易后："确认收货 REQ-xxx"

💡 提醒：实际交易在卖家店铺进行，本平台仅匹配供应商
"""

def notify_on_new_bid(req_id: str, bid: Dict) -> Dict:
    """有新投标时通知买家机器人"""
    if not BUYER_BOT_CONFIG["notify_on_new_bid"]:
        return {"skipped": True, "reason": "新投标通知未启用"}
    
    # 检查投标数量
    bid_dir = BIDS_DIR / req_id
    if bid_dir.exists():
        bid_count = len(list(bid_dir.glob("*.json")))
        if bid_count < BUYER_BOT_CONFIG["min_bids_to_notify"]:
            return {"skipped": True, "reason": f"投标数量不足（{bid_count}<{BUYER_BOT_CONFIG['min_bids_to_notify']}）"}
    
    notification = create_notification(req_id, "new_bid", bid)
    
    # 格式化通知内容
    notification["message"] = format_new_bid_notification(req_id, bid)
    
    # 标记为已交付（买家机器人会读取这个文件）
    notification["delivered"] = True
    notification["delivered_at"] = datetime.now().isoformat()
    
    notif_file = NOTIFICATIONS_DIR / f"{req_id}_new_bid.json"
    notif_file.write_text(json.dumps(notification, indent=2, ensure_ascii=False))
    
    return notification

def notify_on_evaluation(req_id: str, result: Dict) -> Dict:
    """评标完成时通知买家机器人"""
    if not BUYER_BOT_CONFIG["notify_on_evaluation"]:
        return {"skipped": True, "reason": "评标通知未启用"}
    
    notification = create_notification(req_id, "evaluation", result)
    
    # 格式化通知内容
    notification["message"] = format_evaluation_notification(req_id, result)
    
    # 标记为已交付
    notification["delivered"] = True
    notification["delivered_at"] = datetime.now().isoformat()
    
    notif_file = NOTIFICATIONS_DIR / f"{req_id}_evaluation.json"
    notif_file.write_text(json.dumps(notification, indent=2, ensure_ascii=False))
    
    return notification

def notify_on_winner(req_id: str, winner: Dict) -> Dict:
    """确认中标时通知买家机器人"""
    if not BUYER_BOT_CONFIG["notify_on_winner"]:
        return {"skipped": True, "reason": "中标通知未启用"}
    
    notification = create_notification(req_id, "winner", winner)
    
    # 格式化通知内容
    notification["message"] = format_winner_notification(req_id, winner)
    
    # 标记为已交付
    notification["delivered"] = True
    notification["delivered_at"] = datetime.now().isoformat()
    
    notif_file = NOTIFICATIONS_DIR / f"{req_id}_winner.json"
    notif_file.write_text(json.dumps(notification, indent=2, ensure_ascii=False))
    
    # 同时更新需求状态
    req_file = REQUIREMENTS_DIR / f"{req_id}.json"
    if req_file.exists():
        req = json.loads(req_file.read_text())
        req["status"] = "winner_confirmed"
        req["winner"] = winner
        req["winner_confirmed_at"] = datetime.now().isoformat()
        req_file.write_text(json.dumps(req, indent=2, ensure_ascii=False))
    
    return notification

def get_pending_notifications() -> list:
    """获取待处理的通知"""
    NOTIFICATIONS_DIR.mkdir(parents=True, exist_ok=True)
    
    pending = []
    for notif_file in NOTIFICATIONS_DIR.glob("*.json"):
        notification = json.loads(notif_file.read_text())
        if not notification.get("delivered", False):
            pending.append(notification)
    
    return pending

def mark_notification_delivered(notification_id: str):
    """标记通知为已交付"""
    for notif_file in NOTIFICATIONS_DIR.glob("*.json"):
        notification = json.loads(notif_file.read_text())
        if notification.get("notification_id") == notification_id:
            notification["delivered"] = True
            notification["delivered_at"] = datetime.now().isoformat()
            notif_file.write_text(json.dumps(notification, indent=2, ensure_ascii=False))
            return True
    return False

def confirm_winner(req_id: str, rank: int = 1) -> Dict:
    """确认中标供应商"""
    # 加载评标结果
    result_file = REQUIREMENTS_DIR / f"{req_id}_result.json"
    if not result_file.exists():
        return {"error": f"未找到评标结果：{req_id}"}
    
    result = json.loads(result_file.read_text())
    top3 = result.get("top3", [])
    
    if not top3:
        return {"error": "没有投标记录"}
    
    if rank > len(top3):
        return {"error": f"无效排名：{rank}（只有{len(top3)}个投标）"}
    
    winner = top3[rank - 1]
    
    # 创建中标通知
    notification = notify_on_winner(req_id, winner)
    
    return {
        "success": True,
        "req_id": req_id,
        "winner": winner,
        "notification": notification
    }

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="OW Buyer 中标提醒系统")
    parser.add_argument("action", choices=["new-bid", "evaluate", "confirm", "pending", "list"])
    parser.add_argument("--req-id", help="需求ID")
    parser.add_argument("--bid-json", help="投标JSON")
    parser.add_argument("--rank", type=int, default=1, help="中标排名（默认第1名）")
    
    args = parser.parse_args()
    
    if args.action == "new-bid":
        if not args.req_id or not args.bid_json:
            print("需要 --req-id 和 --bid-json")
            return
        bid = json.loads(args.bid_json)
        result = notify_on_new_bid(args.req_id, bid)
        print(result.get("message", "通知已创建"))
    
    elif args.action == "evaluate":
        if not args.req_id:
            print("需要 --req-id")
            return
        # 先执行评标
        from evaluate import evaluate_bids
        result = evaluate_bids(args.req_id)
        if "error" in result:
            print(f"❌ {result['error']}")
            return
        # 通知买家机器人
        notification = notify_on_evaluation(args.req_id, result)
        print(notification.get("message", "评标通知已创建"))
    
    elif args.action == "confirm":
        if not args.req_id:
            print("需要 --req-id")
            return
        result = confirm_winner(args.req_id, args.rank)
        if "error" in result:
            print(f"❌ {result['error']}")
        else:
            print(result["notification"].get("message", "中标确认通知已创建"))
    
    elif args.action == "pending":
        pending = get_pending_notifications()
        print(f"待处理通知: {len(pending)} 个")
        for n in pending:
            print(f"  - {n['notification_id']}: {n['type']} ({n['req_id']})")
    
    elif args.action == "list":
        NOTIFICATIONS_DIR.mkdir(parents=True, exist_ok=True)
        notifications = []
        for notif_file in NOTIFICATIONS_DIR.glob("*.json"):
            notifications.append(json.loads(notif_file.read_text()))
        print(f"所有通知: {len(notifications)} 个")
        for n in notifications:
            status = "✅" if n.get("delivered") else "⏳"
            print(f"  {status} {n['type']}: {n['req_id']} ({n['timestamp']})")

if __name__ == "__main__":
    main()