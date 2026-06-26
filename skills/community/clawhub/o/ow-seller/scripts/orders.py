#!/usr/bin/env python3
"""
OWS - 订单管理与发货跟进
处理中标订单、发货通知、收款确认
"""

import json
import pathlib
from datetime import datetime

STATE_DIR = pathlib.Path(__file__).resolve().parent.parent / "state"
ORDERS_DIR = STATE_DIR / "orders"
BIDS_DIR = STATE_DIR / "bids"

def load_order(order_id):
    """加载订单"""
    order_file = ORDERS_DIR / f"{order_id}.json"
    if order_file.exists():
        return json.loads(order_file.read_text())
    return None

def save_order(order):
    """保存订单"""
    ORDERS_DIR.mkdir(parents=True, exist_ok=True)
    order_file = ORDERS_DIR / f"{order['order_id']}.json"
    order_file.write_text(json.dumps(order, indent=2, ensure_ascii=False))

def create_order_from_bid(bid_id, buyer_info):
    """从中标投标创建订单"""
    bid_file = BIDS_DIR / f"{bid_id}.json"
    if not bid_file.exists():
        return {"error": f"未找到投标 {bid_id}"}
    
    bid = json.loads(bid_file.read_text())
    
    order = {
        "order_id": f"ORD-{datetime.now().strftime('%Y%m%d-%H%M%S')}",
        "bid_id": bid_id,
        "status": "pending",
        "created_at": datetime.now().isoformat(),
        "item": bid.get("item", "商品"),
        "buyer": buyer_info,
        "supplier": bid["supplier"],
        "amount": bid["price"]["amount"],
        "delivery_address": buyer_info.get("address", "待确认"),
        "shipping": None,
        "payment": None
    }
    
    save_order(order)
    return order

def confirm_order(order_id):
    """确认订单"""
    order = load_order(order_id)
    if not order:
        return {"error": f"未找到订单 {order_id}"}
    
    order["status"] = "confirmed"
    order["confirmed_at"] = datetime.now().isoformat()
    save_order(order)
    
    return {
        "success": True,
        "order_id": order_id,
        "message": "订单已确认，准备发货"
    }

def ship_order(order_id, tracking_number, carrier="顺丰快递"):
    """发货"""
    order = load_order(order_id)
    if not order:
        return {"error": f"未找到订单 {order_id}"}
    
    order["shipping"] = {
        "carrier": carrier,
        "tracking_number": tracking_number,
        "shipped_at": datetime.now().isoformat()
    }
    order["status"] = "shipped"
    save_order(order)
    
    return {
        "success": True,
        "order_id": order_id,
        "tracking_number": tracking_number,
        "message": f"订单已发货，快递单号：{tracking_number}"
    }

def confirm_payment(order_id, payment_method, transaction_id):
    """确认收款"""
    order = load_order(order_id)
    if not order:
        return {"error": f"未找到订单 {order_id}"}
    
    order["payment"] = {
        "method": payment_method,
        "transaction_id": transaction_id,
        "paid_at": datetime.now().isoformat()
    }
    order["status"] = "paid"
    save_order(order)
    
    return {
        "success": True,
        "order_id": order_id,
        "amount": order["amount"],
        "message": f"已收到付款 ¥{order['amount']}"
    }

def complete_order(order_id):
    """完成订单"""
    order = load_order(order_id)
    if not order:
        return {"error": f"未找到订单 {order_id}"}
    
    order["status"] = "completed"
    order["completed_at"] = datetime.now().isoformat()
    save_order(order)
    
    return {
        "success": True,
        "order_id": order_id,
        "message": "订单已完成"
    }

def list_orders(status=None):
    """列出订单"""
    if not ORDERS_DIR.exists():
        return []
    
    orders = []
    for order_file in ORDERS_DIR.glob("*.json"):
        order = json.loads(order_file.read_text())
        if status is None or order.get("status") == status:
            orders.append(order)
    
    return sorted(orders, key=lambda x: x["created_at"], reverse=True)

def format_orders(orders):
    """格式化订单列表"""
    if not orders:
        return "暂无订单"
    
    output = f"📦 订单列表 ({len(orders)} 个)\n\n"
    
    for order in orders:
        status_emoji = {
            "pending": "⏳",
            "confirmed": "✅",
            "shipped": "🚚",
            "paid": "💰",
            "completed": "🎉"
        }.get(order["status"], "❓")
        
        output += f"{status_emoji} {order['order_id']}\n"
        output += f"   商品：{order.get('item', '未知')}\n"
        output += f"   金额：¥{order['amount']}\n"
        output += f"   状态：{order['status']}\n"
        output += f"   时间：{order['created_at']}\n\n"
    
    return output

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="订单管理")
    parser.add_argument("action", choices=["list", "confirm", "ship", "payment", "complete"])
    parser.add_argument("--order-id", "-o", help="订单 ID")
    parser.add_argument("--tracking", "-t", help="快递单号")
    parser.add_argument("--carrier", "-c", default="顺丰快递", help="快递公司")
    parser.add_argument("--method", "-m", help="支付方式")
    parser.add_argument("--tx-id", help="交易号")
    parser.add_argument("--status", "-s", help="订单状态筛选")
    
    args = parser.parse_args()
    
    if args.action == "list":
        orders = list_orders(args.status)
        print(format_orders(orders))
    
    elif args.action == "confirm":
        if not args.order_id:
            print("❌ 请指定订单 ID")
            return
        result = confirm_order(args.order_id)
        print(f"✅ {result['message']}")
    
    elif args.action == "ship":
        if not args.order_id or not args.tracking:
            print("❌ 请指定订单 ID 和快递单号")
            return
        result = ship_order(args.order_id, args.tracking, args.carrier)
        print(f"✅ {result['message']}")
    
    elif args.action == "payment":
        if not args.order_id or not args.method:
            print("❌ 请指定订单 ID 和支付方式")
            return
        result = confirm_payment(args.order_id, args.method, args.tx_id or "")
        print(f"✅ {result['message']}")
    
    elif args.action == "complete":
        if not args.order_id:
            print("❌ 请指定订单 ID")
            return
        result = complete_order(args.order_id)
        print(f"✅ {result['message']}")

if __name__ == "__main__":
    main()