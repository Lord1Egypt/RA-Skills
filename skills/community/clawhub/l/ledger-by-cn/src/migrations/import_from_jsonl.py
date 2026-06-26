#!/usr/bin/env python3
"""
账本迁移脚本 - 将 JSONL 格式迁移到 SQLite
"""
import sys
import os
import json

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from src.services.ledger import create_ledger, add_transaction, set_opening_balance
from src.db.connection import get_db_path


def get_ledger_path(ledger_name):
    """获取账本目录路径"""
    base_path = os.path.expanduser("~/.openclaw/skills_data/ledger")
    return os.path.join(base_path, ledger_name)


def load_transactions_from_jsonl(ledger_path):
    """从 JSONL 文件加载交易记录"""
    jsonl_file = os.path.join(ledger_path, "transactions.jsonl")
    transactions = []
    
    if os.path.exists(jsonl_file):
        with open(jsonl_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:
                    try:
                        trans = json.loads(line)
                        transactions.append(trans)
                    except json.JSONDecodeError:
                        print(f"   警告: 跳过无法解析的行: {line[:50]}...")
    
    return transactions


def migrate_ledger(ledger_name):
    """迁移单个账本"""
    ledger_path = get_ledger_path(ledger_name)
    
    print(f"\n迁移账本: {ledger_name}")
    print(f"  路径: {ledger_path}")
    
    # 检查账本目录是否存在
    if not os.path.exists(ledger_path):
        print(f"  错误: 账本目录不存在")
        return False
    
    # 创建账本
    try:
        ledger_id = create_ledger(ledger_name)
        print(f"  账本 ID: {ledger_id}")
    except Exception as e:
        print(f"  错误: 创建账本失败 - {e}")
        return False
    
    # 加载并导入交易记录
    transactions = load_transactions_from_jsonl(ledger_path)
    print(f"  找到 {len(transactions)} 笔交易记录")
    
    # 导入所有交易（包括期初结余作为普通支出）
    imported_count = 0
    for trans in transactions:
        try:
            add_transaction(ledger_name, {
                'date': trans.get('date'),
                'amount': trans.get('amount'),
                'category': trans.get('category', '其他'),
                'account': trans.get('account', '现金'),
                'description': trans.get('description', '')
            })
            imported_count += 1
        except Exception as e:
            print(f"   警告: 导入交易失败 - {e}")
    
    print(f"  已导入 {imported_count} 笔交易")
    
    return True


def main():
    base_path = os.path.expanduser("~/.openclaw/skills_data/ledger")
    
    print("=" * 60)
    print("账本迁移工具 - JSONL -> SQLite")
    print("=" * 60)
    
    # 获取所有账本目录
    if not os.path.exists(base_path):
        print(f"错误: 账本目录不存在: {base_path}")
        return
    
    ledger_names = []
    for item in os.listdir(base_path):
        item_path = os.path.join(base_path, item)
        if os.path.isdir(item_path):
            ledger_names.append(item)
    
    ledger_names.sort()
    print(f"\n找到 {len(ledger_names)} 个账本: {ledger_names}")
    
    # 迁移每个账本
    for ledger_name in ledger_names:
        migrate_ledger(ledger_name)
    
    print("\n" + "=" * 60)
    print("迁移完成!")
    print("=" * 60)
    
    # 显示每个账本的数据库位置
    print("\n数据库文件位置:")
    for ledger_name in ledger_names:
        db_path = get_db_path(ledger_name)
        print(f"  {ledger_name}: {db_path}")


if __name__ == "__main__":
    main()
