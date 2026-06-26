#!/usr/bin/env python3
"""
Stock Position Manager - 持仓管理系统 v1.0
基础功能：添加、查看、删除持仓，盈亏计算
"""

import json
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, Dict, List, Any

# 配置文件路径
MEMORY_DIR = Path("/Users/maxhou/Desktop/openclawmax/memory")
POSITIONS_FILE = MEMORY_DIR / "stock-positions.json"
TRADES_FILE = MEMORY_DIR / "stock-trades.json"


def load_json(filepath: Path) -> dict:
    """加载 JSON 文件"""
    if not filepath.exists():
        return {"version": "1.0", "positions": [], "summary": {}}
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_json(filepath: Path, data: dict):
    """保存 JSON 文件"""
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def generate_id(code: str, date: str) -> str:
    """生成持仓 ID"""
    return f"pos_{code}_{date.replace('-', '')}"


def calculate_holding_days(entry_date: str) -> int:
    """计算持有天数"""
    entry = datetime.strptime(entry_date, "%Y-%m-%d")
    today = datetime.now()
    return (today - entry).days


def calculate_take_profit_levels(entry_price: float) -> dict:
    """计算三档止盈位"""
    return {
        "level_1": round(entry_price * 1.08, 2),
        "level_2": round(entry_price * 1.15, 2),
        "level_3": round(entry_price * 1.25, 2)
    }


def calculate_stop_loss(entry_price: float) -> float:
    """计算止损位（保本下方1.8%）"""
    return round(entry_price * 0.982, 2)


def add_position(
    code: str,
    name: str,
    market: str,
    entry_price: float,
    shares: int,
    entry_date: Optional[str] = None,
    notes: str = ""
) -> dict:
    """
    添加新持仓
    
    示例:
        python3 position_manager.py add 600519 贵州茅台 A股 1800 100
    """
    if entry_date is None:
        entry_date = datetime.now().strftime("%Y-%m-%d")
    
    data = load_json(POSITIONS_FILE)
    
    # 检查是否已存在
    for pos in data["positions"]:
        if pos["code"] == code and pos["status"] == "holding":
            print(f"⚠️  {name}({code}) 已有持仓，请先卖出或加仓")
            return None
    
    # 计算策略参数
    take_profit = calculate_take_profit_levels(entry_price)
    stop_loss = calculate_stop_loss(entry_price)
    cost_basis = round(entry_price * shares, 2)
    holding_days = calculate_holding_days(entry_date)
    
    position = {
        "id": generate_id(code, entry_date),
        "code": code,
        "name": name,
        "market": market,
        "entry_price": entry_price,
        "shares": shares,
        "entry_date": entry_date,
        "holding_days": holding_days,
        "current_price": entry_price,  # 初始为成本价
        "market_value": cost_basis,
        "cost_basis": cost_basis,
        "unrealized_pnl": 0.0,
        "unrealized_pnl_pct": 0.0,
        "take_profit_1": take_profit["level_1"],
        "take_profit_2": take_profit["level_2"],
        "take_profit_3": take_profit["level_3"],
        "stop_loss": stop_loss,
        "strategy": "分批止盈",
        "status": "holding",
        "notes": notes
    }
    
    data["positions"].append(position)
    update_summary(data)
    save_json(POSITIONS_FILE, data)
    
    # 同时记录交易
    record_trade(code, name, "buy", entry_price, shares, notes)
    
    print(f"✅ 已添加持仓: {name}({code})")
    print(f"   成本: {entry_price}元 × {shares}股 = {cost_basis:.2f}元")
    print(f"   止盈位: {take_profit['level_1']} / {take_profit['level_2']} / {take_profit['level_3']}")
    print(f"   止损位: {stop_loss}元")
    
    return position


def record_trade(
    code: str,
    name: str,
    action: str,  # buy or sell
    price: float,
    shares: int,
    notes: str = ""
):
    """记录交易历史"""
    data = load_json(TRADES_FILE)
    
    amount = round(price * shares, 2)
    commission = round(amount * 0.001, 2) if action == "buy" else round(amount * 0.0015, 2)
    
    trade = {
        "id": f"trade_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
        "date": datetime.now().strftime("%Y-%m-%d"),
        "time": datetime.now().strftime("%H:%M:%S"),
        "code": code,
        "name": name,
        "action": action,
        "price": price,
        "shares": shares,
        "amount": amount,
        "fees": commission,
        "total_cost": round(amount + commission, 2) if action == "buy" else round(amount - commission, 2),
        "notes": notes
    }
    
    if "trades" not in data:
        data["trades"] = []
    data["trades"].append(trade)
    
    # 更新统计
    stats = data.get("statistics", {})
    stats["total_trades"] = stats.get("total_trades", 0) + 1
    if action == "buy":
        stats["buy_trades"] = stats.get("buy_trades", 0) + 1
    else:
        stats["sell_trades"] = stats.get("sell_trades", 0) + 1
    stats["total_commission"] = round(stats.get("total_commission", 0) + commission, 2)
    data["statistics"] = stats
    
    save_json(TRADES_FILE, data)


def update_summary(data: dict):
    """更新持仓汇总统计"""
    positions = [p for p in data.get("positions", []) if p.get("status") == "holding"]
    
    total_cost = sum(p["cost_basis"] for p in positions)
    total_market_value = sum(p.get("market_value", p["cost_basis"]) for p in positions)
    total_pnl = total_market_value - total_cost
    total_pnl_pct = round((total_pnl / total_cost) * 100, 2) if total_cost > 0 else 0
    
    data["summary"] = {
        "total_positions": len(positions),
        "total_cost": round(total_cost, 2),
        "total_market_value": round(total_market_value, 2),
        "total_unrealized_pnl": round(total_pnl, 2),
        "total_return_pct": total_pnl_pct,
        "last_updated": datetime.now().strftime("%Y-%m-%dT%H:%M:%S+08:00")
    }
    data["last_updated"] = datetime.now().strftime("%Y-%m-%dT%H:%M:%S+08:00")


def list_positions():
    """列出所有持仓"""
    data = load_json(POSITIONS_FILE)
    positions = [p for p in data.get("positions", []) if p.get("status") == "holding"]
    
    if not positions:
        print("📭 当前没有持仓")
        return
    
    print("\n" + "=" * 80)
    print("📊 持仓总览")
    print("=" * 80)
    print(f"{'股票':<10} {'名称':<10} {'成本价':>8} {'现价':>8} {'数量':>8} {'市值':>10} {'盈亏':>10} {'盈亏%':>8}")
    print("-" * 80)
    
    for pos in positions:
        pnl_str = f"{pos.get('unrealized_pnl', 0):+.2f}"
        pnl_pct_str = f"{pos.get('unrealized_pnl_pct', 0):+.2f}%"
        emoji = "🟢" if pos.get('unrealized_pnl', 0) >= 0 else "🔴"
        print(f"{pos['code']:<10} {pos['name']:<10} {pos['entry_price']:>8.2f} "
              f"{pos.get('current_price', pos['entry_price']):>8.2f} {pos['shares']:>8} "
              f"{pos.get('market_value', pos['cost_basis']):>10.0f} "
              f"{emoji}{pnl_str:>8} {pnl_pct_str:>8}")
    
    print("-" * 80)
    summary = data.get("summary", {})
    print(f"合计: {summary.get('total_positions', 0)} 只标的 | "
          f"总市值: {summary.get('total_market_value', 0):.2f} | "
          f"总成本: {summary.get('total_cost', 0):.2f} | "
          f"总盈亏: {summary.get('total_unrealized_pnl', 0):+.2f} ({summary.get('total_return_pct', 0):+.2f}%)")
    print("=" * 80 + "\n")


def view_position(code: str):
    """查看单个持仓详情"""
    data = load_json(POSITIONS_FILE)
    position = next((p for p in data.get("positions", []) if p["code"] == code and p["status"] == "holding"), None)
    
    if not position:
        print(f"❌ 未找到持仓: {code}")
        return
    
    print("\n" + "=" * 60)
    print(f"📈 {position['name']} ({position['code']}) 持仓详情")
    print("=" * 60)
    print(f"市场: {position['market']}")
    print(f"建仓日期: {position['entry_date']} (已持有 {position['holding_days']} 天)")
    print(f"\n【持仓成本】")
    print(f"  成本价: {position['entry_price']:.2f}元")
    print(f"  持股数: {position['shares']} 股")
    print(f"  总成本: {position['cost_basis']:.2f}元")
    print(f"\n【当前状况】")
    print(f"  当前价: {position.get('current_price', position['entry_price']):.2f}元")
    print(f"  市值: {position.get('market_value', position['cost_basis']):.2f}元")
    print(f"  浮动盈亏: {position.get('unrealized_pnl', 0):+.2f}元 ({position.get('unrealized_pnl_pct', 0):+.2f}%)")
    print(f"\n【止盈策略】")
    print(f"  第一档: {position['take_profit_1']:.2f}元 (+8%) - 减仓1/3")
    print(f"  第二档: {position['take_profit_2']:.2f}元 (+15%) - 减仓1/3")
    print(f"  第三档: {position['take_profit_3']:.2f}元 (+25%) - 清仓或留底仓")
    print(f"\n【止损策略】")
    print(f"  止损位: {position['stop_loss']:.2f}元 (-1.8%)")
    if position.get('notes'):
        print(f"\n【备注】")
        print(f"  {position['notes']}")
    print("=" * 60 + "\n")


def remove_position(code: str, sell_price: Optional[float] = None):
    """
    删除/清仓持仓
    
    示例:
        python3 position_manager.py remove 600089
        python3 position_manager.py remove 600089 --price 31.50
    """
    data = load_json(POSITIONS_FILE)
    position = next((p for p in data.get("positions", []) if p["code"] == code and p["status"] == "holding"), None)
    
    if not position:
        print(f"❌ 未找到持仓: {code}")
        return
    
    name = position["name"]
    shares = position["shares"]
    
    if sell_price:
        # 计算实际盈亏
        realized_pnl = round((sell_price - position["entry_price"]) * shares, 2)
        realized_pnl_pct = round((sell_price / position["entry_price"] - 1) * 100, 2)
        print(f"💰 卖出 {name}({code}) {shares}股 @ {sell_price}元")
        print(f"   实现盈亏: {realized_pnl:+.2f}元 ({realized_pnl_pct:+.2f}%)")
        
        # 记录交易
        record_trade(code, name, "sell", sell_price, shares, "清仓")
    else:
        print(f"🗑️  删除持仓记录: {name}({code})")
    
    # 标记为已卖出
    position["status"] = "sold"
    position["exit_date"] = datetime.now().strftime("%Y-%m-%d")
    if sell_price:
        position["exit_price"] = sell_price
        position["realized_pnl"] = realized_pnl
        position["realized_pnl_pct"] = realized_pnl_pct
    
    update_summary(data)
    save_json(POSITIONS_FILE, data)
    print(f"✅ 已完成")


def update_price(code: str, current_price: float):
    """更新当前股价"""
    data = load_json(POSITIONS_FILE)
    position = next((p for p in data.get("positions", []) if p["code"] == code and p["status"] == "holding"), None)
    
    if not position:
        print(f"❌ 未找到持仓: {code}")
        return
    
    position["current_price"] = current_price
    position["market_value"] = round(current_price * position["shares"], 2)
    position["unrealized_pnl"] = round(position["market_value"] - position["cost_basis"], 2)
    position["unrealized_pnl_pct"] = round((position["unrealized_pnl"] / position["cost_basis"]) * 100, 2)
    position["holding_days"] = calculate_holding_days(position["entry_date"])
    
    update_summary(data)
    save_json(POSITIONS_FILE, data)
    
    print(f"✅ 已更新 {position['name']}({code}) 股价: {current_price}元")
    print(f"   当前盈亏: {position['unrealized_pnl']:+.2f}元 ({position['unrealized_pnl_pct']:+.2f}%)")


def main():
    if len(sys.argv) < 2:
        print("""
Stock Position Manager - 持仓管理

用法:
  python3 position_manager.py list              # 列出所有持仓
  python3 position_manager.py view <code>       # 查看持仓详情
  python3 position_manager.py add <code> <name> <market> <price> <shares> [date] [notes]
                                                # 添加持仓
  python3 position_manager.py remove <code> [--price <price>]
                                                # 删除/清仓持仓
  python3 position_manager.py update <code> <price>
                                                # 更新当前股价

示例:
  python3 position_manager.py add 600519 贵州茅台 A股 1800 100
  python3 position_manager.py view 600089
  python3 position_manager.py remove 600089 --price 31.50
  python3 position_manager.py update 600089 30.50
        """)
        return
    
    command = sys.argv[1]
    
    if command == "list":
        list_positions()
    
    elif command == "view" and len(sys.argv) >= 3:
        view_position(sys.argv[2])
    
    elif command == "add" and len(sys.argv) >= 7:
        code = sys.argv[2]
        name = sys.argv[3]
        market = sys.argv[4]
        price = float(sys.argv[5])
        shares = int(sys.argv[6])
        date = sys.argv[7] if len(sys.argv) > 7 else None
        notes = sys.argv[8] if len(sys.argv) > 8 else ""
        add_position(code, name, market, price, shares, date, notes)
    
    elif command == "remove" and len(sys.argv) >= 3:
        code = sys.argv[2]
        sell_price = None
        if "--price" in sys.argv:
            idx = sys.argv.index("--price")
            if idx + 1 < len(sys.argv):
                sell_price = float(sys.argv[idx + 1])
        remove_position(code, sell_price)
    
    elif command == "update" and len(sys.argv) >= 4:
        update_price(sys.argv[2], float(sys.argv[3]))
    
    else:
        print("❌ 未知命令或参数不足，运行时不带参数查看帮助")


if __name__ == "__main__":
    main()
