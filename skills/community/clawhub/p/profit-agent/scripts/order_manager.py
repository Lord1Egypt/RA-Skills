#!/usr/bin/env python3
"""Profit Agent — 订单管理/利润优化引擎"""
import json, os, sys, uuid
from datetime import datetime, timedelta

DATA_DIR = os.path.expanduser("~/.openclaw/workspace/state/orders")
os.makedirs(DATA_DIR, exist_ok=True)

class OrderManager:
    def __init__(self):
        self.orders = self._load_all()
    
    def _load_all(self):
        orders = []
        for f in os.listdir(DATA_DIR):
            if f.endswith(".json"):
                with open(os.path.join(DATA_DIR, f)) as fp:
                    orders.append(json.load(fp))
        return orders
    
    def _save(self, order):
        path = os.path.join(DATA_DIR, f"{order['id']}.json")
        with open(path, "w") as f:
            json.dump(order, f, indent=2)
    
    def create_order(self, name, desc, cost=0, price=0):
        order = {
            "id": uuid.uuid4().hex[:12],
            "name": name,
            "description": desc,
            "cost": cost,
            "price": price,
            "status": "draft",
            "created": datetime.now().isoformat(),
            "metrics": {}
        }
        if price > 0:
            order["metrics"] = {
                "revenue": price,
                "cost": cost,
                "profit": price - cost,
                "margin_pct": round((price - cost) / price * 100, 1) if price > 0 else 0
            }
        self._save(order)
        self.orders.append(order)
        return order
    
    def calculate_margin(self, cost, price):
        return {"profit": price - cost, "margin_pct": round((price - cost) / price * 100, 1) if price > 0 else 0}
    
    def report(self):
        if not self.orders:
            print("⚠️  无订单记录")
            return
        total_revenue = sum(o.get("metrics", {}).get("revenue", o.get("price", 0)) for o in self.orders)
        total_cost = sum(o.get("metrics", {}).get("cost", o.get("cost", 0)) for o in self.orders)
        total_profit = total_revenue - total_cost
        
        print(f"=== 💰 利润报告: {datetime.now().strftime('%Y-%m-%d %H:%M')} ===")
        print(f"   订单总数: {len(self.orders)}")
        print(f"   总收入: ¥{total_revenue:.2f}")
        print(f"   总成本: ¥{total_cost:.2f}")
        print(f"   总利润: ¥{total_profit:.2f}")
        if total_revenue > 0:
            print(f"   利润率: {round(total_profit/total_revenue*100,1)}%")
        print()
        for o in self.orders:
            m = o.get("metrics", {})
            print(f"  {o['id']} {o['name']}: ¥{m.get('profit','?')} ({m.get('margin_pct','?')}%) [{o['status']}]")

def main():
    mgr = OrderManager()
    args = sys.argv[1:]
    
    if "--new-order" in args:
        idx = args.index("--new-order")
        name = args[idx+1] if idx+1 < len(args) else "服务订单"
        price = int(args[idx+2]) if idx+2 < len(args) else 299
        cost = int(args[idx+3]) if idx+3 < len(args) else 50
        o = mgr.create_order(name, f"客户下单: {name}", cost=cost, price=price)
        print(f"✅ 订单已创建: {o['id']}")
        print(f"   名称: {name}")
        print(f"   金额: ¥{price} | 成本: ¥{cost} | 利润: ¥{price-cost}")
        print(f"   状态: draft (待收款)")
        print(f"   收款码: assets/wechat_pay_qr.png")
    
    elif "--confirm" in args:
        idx = args.index("--confirm")
        oid = args[idx+1] if idx+1 < len(args) else ""
        if not oid:
            print("请指定订单ID: --confirm <order_id>")
            return
        found = None
        for o in mgr.orders:
            if o['id'] == oid:
                found = o
                break
        if found:
            found['status'] = 'paid'
            found['paid_at'] = datetime.now().isoformat()
            mgr._save(found)
            print(f"✅ 订单 {oid} 已标记为已收款!")
            print(f"   金额: ¥{found['price']}")
            print(f"   利润: ¥{found['price'] - found['cost']}")
        else:
            print(f"❌ 未找到订单: {oid}")
    
    elif "--simulate" in args:
        print("=== 📈 利润模拟 ===")
        for price in [99, 199, 299, 499]:
            m = mgr.calculate_margin(cost=50, price=price)
            print(f"  定价 ¥{price:>3} → 利润 ¥{m['profit']:>3} | 利润率 {m['margin_pct']:>5.1f}%")
        for price in [99, 199, 299, 499]:
            m = mgr.calculate_margin(cost=100, price=price)
            print(f"  定价 ¥{price:>3} → 利润 ¥{m['profit']:>3} | 利润率 {m['margin_pct']:>5.1f}%")
    
    elif "--report" in args:
        mgr.report()
    
    elif "--list" in args:
        print(f"=== 📋 订单列表 ({len(mgr.orders)} 笔) ===")
        for o in mgr.orders:
            status_icon = "✅" if o['status'] == 'paid' else "📝"
            print(f"  {status_icon} {o['id'][:8]}... ¥{o['price']} [{o['status']}] {o['name']}")
    
    else:
        print("📌 码行者订单系统")
        print("用法:")
        print("  --new-order <名称> <金额> [成本]   创建新订单")
        print("  --confirm <id>                    确认微信收款")
        print("  --list                            查看所有订单")
        print("  --report                          利润报告")
        print("  --simulate                        利润模拟")

if __name__ == "__main__":
    main()
