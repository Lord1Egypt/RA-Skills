#!/usr/bin/env python3
"""
接收并存储投标
验证投标格式并保存到本地
收到新投标时自动通知买家机器人
展示卖家信用信息（可选功能）
"""

import json
import pathlib
from datetime import datetime

STATE_DIR = pathlib.Path(__file__).resolve().parent.parent / "state"
BIDS_DIR = STATE_DIR / "bids"

# 信用系统为可选功能，不修改 sys.path
CREDIT_SYSTEM_ENABLED = False
get_seller_profile = None
format_seller_credit_display = None
get_credit_warning = None

def get_simple_credit_display(seller_id: str) -> str:
    """简化版信用信息显示（当信用系统未安装时）"""
    return "📊 信用系统未安装\n   安装：npx skills add Enze-dai/ow-skills/ow-credit"

def validate_bid(bid: dict) -> tuple[bool, str]:
    """验证投标格式"""
    required = ["bid_id", "req_id", "supplier", "price", "delivery"]
    
    for field in required:
        if field not in bid:
            return False, f"缺少必填字段：{field}"
    
    if "name" not in bid.get("supplier", {}):
        return False, "缺少供应商名称"
    
    if "amount" not in bid.get("price", {}):
        return False, "缺少投标价格"
    
    if "time_days" not in bid.get("delivery", {}):
        return False, "缺少到货时间"
    
    return True, "验证通过"

def receive_bid(bid_json: str, notify_buyer: bool = True) -> dict:
    """接收并存储投标"""
    try:
        bid = json.loads(bid_json)
    except json.JSONDecodeError as e:
        return {"error": f"JSON 格式错误：{e}"}
    
    # 验证
    valid, msg = validate_bid(bid)
    if not valid:
        return {"error": msg}
    
    req_id = bid["req_id"]
    bid_id = bid["bid_id"]
    
    # 保存
    bid_dir = BIDS_DIR / req_id
    bid_dir.mkdir(parents=True, exist_ok=True)
    
    bid_file = bid_dir / f"{bid_id}.json"
    bid["received_at"] = datetime.now().isoformat()
    bid_file.write_text(json.dumps(bid, indent=2, ensure_ascii=False))
    
    result = {
        "success": True,
        "bid_id": bid_id,
        "req_id": req_id,
        "supplier": bid["supplier"]["name"],
        "price": bid["price"]["amount"]
    }
    
    # 🔔 通知买家机器人（新投标提醒）
    if notify_buyer:
        try:
            from notify import notify_on_new_bid
            notification = notify_on_new_bid(req_id, bid)
            if notification.get("delivered"):
                result["notification_sent"] = True
                result["notification_type"] = "new_bid"
        except Exception as e:
            result["notification_error"] = str(e)
    
    # 🛡️ 获取卖家信用信息
    if CREDIT_SYSTEM_ENABLED:
        try:
            seller_id = bid["supplier"].get("agent_id", bid["supplier"]["name"])
            result["seller_credit"] = format_seller_credit_display(seller_id)
            result["seller_credit_warning"] = get_credit_warning(seller_id, "seller")
        except Exception as e:
            result["credit_error"] = str(e)
    
    return result

def list_bids(req_id: str) -> list:
    """列出某需求的所有投标"""
    bid_dir = BIDS_DIR / req_id
    if not bid_dir.exists():
        return []
    
    bids = []
    for bid_file in bid_dir.glob("*.json"):
        bid = json.loads(bid_file.read_text())
        bids.append(bid)
    
    return bids

def main():
    if len(sys.argv) < 2:
        print("用法：python receive.py <bid_json>")
        print("   或：python receive.py list <req_id>")
        sys.exit(1)
    
    if sys.argv[1] == "list" and len(sys.argv) > 2:
        req_id = sys.argv[2]
        bids = list_bids(req_id)
        print(f"需求 {req_id} 共有 {len(bids)} 个投标:")
        for bid in bids:
            print(f"  - {bid['bid_id']}: {bid['supplier']['name']} ¥{bid['price']['amount']}")
    else:
        bid_json = sys.argv[1]
        result = receive_bid(bid_json)
        if "error" in result:
            print(f"❌ {result['error']}")
        else:
            print(f"✅ 投标已接收: {result['supplier']} - ¥{result['price']}")
            if result.get("notification_sent"):
                print(f"🔔 已通知买家机器人")

if __name__ == "__main__":
    main()