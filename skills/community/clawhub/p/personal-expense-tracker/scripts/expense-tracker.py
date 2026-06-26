#!/usr/bin/env python3
"""Expense Tracker - Personal expense tracking"""

import argparse
import json
import os
from datetime import datetime
from pathlib import Path

DATA_DIR = Path.home() / ".expense-tracker"
DATA_FILE = DATA_DIR / "expenses.json"

# Auto-categorization rules
CATEGORIES = {
    "food": ["早餐", "午餐", "晚餐", "吃饭", "餐厅", "外卖", "零食", "水果", "奶茶", "咖啡"],
    "transport": ["地铁", "公交", "打车", "滴滴", "加油", "停车", "高铁", "机票"],
    "shopping": ["超市", "购物", "衣服", "鞋子", "包", "化妆品", "淘宝", "京东", "拼多多"],
    "entertainment": ["电影", "游戏", "KTV", "旅游", "门票", "会员", "订阅"],
    "housing": ["房租", "水电", "物业", "宽带", "维修"]
}

def init_data():
    """Initialize data directory"""
    DATA_DIR.mkdir(exist_ok=True)
    if not DATA_FILE.exists():
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump([], f)

def load_expenses():
    """Load all expenses"""
    init_data()
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_expenses(expenses):
    """Save expenses"""
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(expenses, f, ensure_ascii=False, indent=2)

def auto_categorize(note):
    """Auto categorize based on keywords"""
    note_lower = note.lower()
    for category, keywords in CATEGORIES.items():
        for keyword in keywords:
            if keyword in note_lower:
                return category
    return "others"

def cmd_add(note, amount):
    """Add expense"""
    expenses = load_expenses()
    
    expense = {
        "id": len(expenses) + 1,
        "note": note,
        "amount": float(amount),
        "category": auto_categorize(note),
        "date": datetime.now().strftime("%Y-%m-%d"),
        "timestamp": datetime.now().isoformat()
    }
    
    expenses.append(expense)
    save_expenses(expenses)
    
    print(f"✅ 已记录: {note} - {amount}元")
    print(f"   分类: {expense['category']}")
    print(f"   日期: {expense['date']}")

def cmd_list():
    """List all expenses"""
    expenses = load_expenses()
    
    if not expenses:
        print("📭 暂无消费记录")
        return
    
    print("=" * 60)
    print("📋 消费记录")
    print("=" * 60)
    
    for e in expenses[-10:]:  # Show last 10
        print(f"   {e['date']} | {e['category']:12} | {e['amount']:6}元 | {e['note']}")
    
    if len(expenses) > 10:
        print(f"   ... 还有 {len(expenses) - 10} 条记录")
    
    print("-" * 60)
    print(f"   总计: {sum(e['amount'] for e in expenses)}元")

def cmd_stats():
    """Show monthly statistics"""
    expenses = load_expenses()
    
    if not expenses:
        print("📭 暂无消费记录")
        return
    
    # Filter current month
    current_month = datetime.now().strftime("%Y-%m")
    month_expenses = [e for e in expenses if e['date'].startswith(current_month)]
    
    if not month_expenses:
        print(f"📭 {current_month}月暂无消费记录")
        return
    
    # Calculate statistics
    total = sum(e['amount'] for e in month_expenses)
    category_stats = {}
    for e in month_expenses:
        cat = e['category']
        if cat not in category_stats:
            category_stats[cat] = {"count": 0, "amount": 0}
        category_stats[cat]["count"] += 1
        category_stats[cat]["amount"] += e['amount']
    
    # Display
    print("=" * 60)
    print(f"📊 {current_month}月消费统计")
    print("=" * 60)
    print(f"\n💰 总支出: {total:.2f}元")
    print(f"📝 笔数: {len(month_expenses)}笔")
    print(f"📊 日均: {total / 30:.2f}元")
    
    print(f"\n📈 分类占比:")
    print("-" * 60)
    
    # Sort by amount
    sorted_cats = sorted(category_stats.items(), key=lambda x: x[1]['amount'], reverse=True)
    
    for cat, stats in sorted_cats:
        percentage = stats['amount'] / total * 100
        bar = "█" * int(percentage / 5)
        print(f"   {cat:12} | {bar:20} | {stats['amount']:6.0f}元 ({percentage:.1f}%)")
    
    print("-" * 60)
    
    # Save sample data for reference
    sample_data = {
        "month": current_month,
        "total": total,
        "count": len(month_expenses),
        "by_category": category_stats
    }
    
    sample_file = Path(__file__).parent.parent / "data" / "sample.json"
    sample_file.parent.mkdir(exist_ok=True)
    with open(sample_file, 'w', encoding='utf-8') as f:
        json.dump(sample_data, f, ensure_ascii=False, indent=2)

def main():
    parser = argparse.ArgumentParser(description="Expense Tracker")
    subparsers = parser.add_subparsers(dest='command')
    
    # add command
    add_parser = subparsers.add_parser('add', help='Add expense')
    add_parser.add_argument('note', help='Expense description')
    add_parser.add_argument('amount', type=float, help='Amount')
    
    # list command
    subparsers.add_parser('list', help='List expenses')
    
    # stats command
    subparsers.add_parser('stats', help='Show statistics')
    
    args = parser.parse_args()
    
    if args.command == 'add':
        cmd_add(args.note, args.amount)
    elif args.command == 'list':
        cmd_list()
    elif args.command == 'stats':
        cmd_stats()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
