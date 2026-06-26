#!/usr/bin/env python3
"""
为所有旧账单添加时间戳
"""
import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from src.db.connection import get_connection, get_db_path
from datetime import datetime, timedelta


def add_timestamps_to_ledger(ledger_name):
    """为账本添加时间戳"""
    db_path = get_db_path(ledger_name)
    
    if not os.path.exists(db_path):
        print(f"  账本 '{ledger_name}' 不存在")
        return 0
    
    conn = get_connection(db_path)
    cursor = conn.cursor()
    
    # 获取所有交易，按日期和ID排序
    cursor.execute("""
        SELECT id, date, created_at 
        FROM transactions 
        ORDER BY date, id
    """)
    
    rows = cursor.fetchall()
    
    if not rows:
        print(f"  账本 '{ledger_name}' 无记录")
        conn.close()
        return 0
    
    # 按日期分组
    date_groups = {}
    for row in rows:
        trans_id = row['id']
        date = row['date']
        if date not in date_groups:
            date_groups[date] = []
        date_groups[date].append(trans_id)
    
    # 为每天生成时间戳（当天开始，每笔间隔1秒）
    count = 0
    
    for date, trans_ids in sorted(date_groups.items()):
        base_time = datetime.strptime(date, '%Y-%m-%d')
        
        for i, trans_id in enumerate(trans_ids):
            # 每笔间隔1秒
            timestamp = (base_time + timedelta(seconds=i)).strftime('%Y-%m-%dT%H:%M:%SZ')
            
            cursor.execute(
                "UPDATE transactions SET created_at = ? WHERE id = ?",
                (timestamp, trans_id)
            )
            count += 1
    
    conn.commit()
    conn.close()
    
    print(f"  账本 '{ledger_name}' 已更新 {count} 条记录")
    return count


def main():
    base_path = os.path.expanduser("~/.openclaw/skills_data/ledger")
    
    print("=" * 60)
    print("为旧账单添加时间戳")
    print("=" * 60)
    
    if not os.path.exists(base_path):
        print("错误: 账本目录不存在")
        return
    
    ledger_names = [d for d in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, d))]
    ledger_names.sort()
    
    total = 0
    for ledger_name in ledger_names:
        count = add_timestamps_to_ledger(ledger_name)
        total += count
    
    print("\n" + "=" * 60)
    print(f"完成! 共更新 {total} 条记录")
    print("=" * 60)


if __name__ == "__main__":
    main()
