#!/usr/bin/env python3
"""
Family Finance Database Operations Script
"""

import sqlite3
import sys
import os
from datetime import datetime, timedelta

DB_PATH = os.path.join(os.path.dirname(__file__), '../db/finance.db')

def init_db():
    """初始化数据库，自动创建表结构（如果不存在）"""
    db_dir = os.path.dirname(DB_PATH)
    if db_dir and not os.path.exists(db_dir):
        os.makedirs(db_dir)
    
    conn = sqlite3.connect(DB_PATH)
    conn.executescript('''
        CREATE TABLE IF NOT EXISTS accounts (
            id TEXT PRIMARY KEY,
            ledger TEXT NOT NULL DEFAULT 'default',
            member TEXT,
            name TEXT NOT NULL,
            type TEXT NOT NULL,
            initial_balance REAL NOT NULL DEFAULT 0,
            budget REAL,
            remark TEXT
        );

        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            ledger TEXT NOT NULL DEFAULT 'default',
            account_id TEXT NOT NULL,
            type TEXT NOT NULL,
            amount REAL NOT NULL,
            category TEXT,
            description TEXT,
            FOREIGN KEY (account_id) REFERENCES accounts(id)
        );

        CREATE TABLE IF NOT EXISTS members (
            feishu_id TEXT PRIMARY KEY,
            nickname TEXT,
            ledger TEXT NOT NULL DEFAULT 'default',
            account_id TEXT,
            role TEXT NOT NULL DEFAULT '成员'
        );

        -- 如果 accounts 为空，插入默认账户
        INSERT OR IGNORE INTO accounts (id, ledger, name, type, initial_balance, budget)
        SELECT 'B001', 'default', '主收支账户', '资产', 0, NULL WHERE NOT EXISTS (SELECT 1 FROM accounts WHERE id = 'B001');
    ''')
    conn.commit()
    conn.close()

def get_db():
    # 首次访问时自动初始化数据库
    if not os.path.exists(DB_PATH):
        init_db()
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# ============ 账户操作 ============

def get_all_accounts():
    """获取所有账户"""
    conn = get_db()
    accounts = conn.execute('SELECT * FROM accounts ORDER BY id').fetchall()
    conn.close()
    return accounts

def get_account_by_id(account_id):
    """根据ID获取账户"""
    conn = get_db()
    account = conn.execute('SELECT * FROM accounts WHERE id = ?', (account_id,)).fetchone()
    conn.close()
    return account

def get_account_balance(account_id):
    """计算账户实时余额：初始余额 + 交易变动"""
    conn = get_db()
    acc = conn.execute('SELECT initial_balance FROM accounts WHERE id = ?', (account_id,)).fetchone()
    if not acc:
        conn.close()
        return None
    
    # 累加所有交易变动（包括转账，因为转账是账户真实资金流动）
    # 统计报表时再排除转账，避免重复计算
    result = conn.execute('''SELECT 
        SUM(CASE WHEN type = '收入' THEN amount ELSE -amount END) as change
        FROM transactions 
        WHERE account_id = ?''', (account_id,)).fetchone()
    
    change = result['change'] or 0
    conn.close()
    return acc['initial_balance'] + change

def add_transaction(date, ledger, account_id, trans_type, amount, category, description=''):
    """添加交易记录"""
    conn = get_db()
    conn.execute('''INSERT INTO transactions 
        (date, ledger, account_id, type, amount, category, description)
        VALUES (?, ?, ?, ?, ?, ?, ?)''',
        (date, ledger, account_id, trans_type, amount, category, description))
    conn.commit()
    conn.close()

# ============ 余额操作 ============

def get_balances():
    """获取所有账户余额"""
    accounts = get_all_accounts()
    result = []
    for acc in accounts:
        balance = get_account_balance(acc['id'])
        result.append({
            'id': acc['id'],
            'name': acc['name'],
            'type': acc['type'],
            'balance': balance,
            'budget': acc['budget']
        })
    return result

def print_balances():
    """打印所有账户余额"""
    balances = get_balances()
    print("\n{'='*50}")
    print(f"{'账户余额报表':^40}")
    print("=" * 50)
    total = 0
    for b in balances:
        print(f"{b['id']} {b['name']:<12} ¥{b['balance']:>10.2f}")
        total += b['balance']
    print("-" * 50)
    print(f"{'总计':<12} ¥{total:>10.2f}")
    print("=" * 50)

# ============ 统计报表 ============

def get_monthly_stats(ledger='default', year_month=None):
    """月度收支统计"""
    if not year_month:
        year_month = datetime.now().strftime('%Y-%m')
    
    conn = get_db()
    
    # 统计支出（排除转账）
    expenses = conn.execute('''SELECT category, SUM(amount) as total
        FROM transactions 
        WHERE ledger = ? AND type = '支出' AND date LIKE ? AND category != '转账'
        GROUP BY category ORDER BY total DESC''', (ledger, f'{year_month}%')).fetchall()
    
    # 统计收入（排除转账）
    income = conn.execute('''SELECT category, SUM(amount) as total
        FROM transactions 
        WHERE ledger = ? AND type = '收入' AND date LIKE ? AND category != '转账'
        GROUP BY category ORDER BY total DESC''', (ledger, f'{year_month}%')).fetchall()
    
    conn.close()
    
    return {
        'year_month': year_month,
        'expenses': expenses,
        'income': income
    }

def print_monthly_stats(ledger='default', year_month=None):
    """打印月度报表"""
    stats = get_monthly_stats(ledger, year_month)
    
    print(f"\n{'='*50}")
    print(f"{stats['year_month']} 月度收支报表".center(40))
    print("=" * 50)
    
    print("\n【收入】")
    total_income = 0
    for item in stats['income']:
        print(f"  {item['category']:<10} ¥{item['total']:>10.2f}")
        total_income += item['total']
    print(f"  {'收入合计':<10} ¥{total_income:>10.2f}")
    
    print("\n【支出】")
    total_expense = 0
    for item in stats['expenses']:
        print(f"  {item['category']:<10} ¥{item['total']:>10.2f}")
        total_expense += item['total']
    print(f"  {'支出合计':<10} ¥{total_expense:>10.2f}")
    
    print("-" * 50)
    balance = total_income - total_expense
    print(f"  {'本月结余':<10} ¥{balance:>10.2f}")
    print("=" * 50)

# ============ 快速记账 ============

def quick_add(ledger, account_name_or_id, trans_type, amount, category, description=''):
    """快速记账：账户名自动转ID"""
    conn = get_db()
    
    # 自动查找账户ID
    account = conn.execute(
        'SELECT id FROM accounts WHERE name = ? OR id = ?',
        (account_name_or_id, account_name_or_id)
    ).fetchone()
    
    if not account:
        # 尝试模糊匹配
        account = conn.execute(
            'SELECT id FROM accounts WHERE name LIKE ?',
            (f'%{account_name_or_id}%',)
        ).fetchone()
    
    conn.close()
    
    if not account:
        print(f"❌ 账户 '{account_name_or_id}' 不存在")
        return False
    
    date = datetime.now().strftime('%Y-%m-%d')
    add_transaction(date, ledger, account['id'], trans_type, float(amount), category, description)
    print(f"✅ 已添加: [{ledger}] {date} {account['id']} {trans_type} ¥{float(amount):.2f} ({category})")
    return True

# ============ 主程序 ============

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("用法: python3 finance_db.py <命令> [参数]")
        print("命令:")
        print("  -b, --balances          查看所有账户余额")
        print("  -s, --stats [YYYY-MM]   月度统计报表")
        print("  --add 账本 账户 类型 金额 分类 描述  添加交易")
        sys.exit(1)
    
    cmd = sys.argv[1]
    
    if cmd in ['-b', '--balances']:
        print_balances()
    
    elif cmd in ['-s', '--stats']:
        ym = sys.argv[2] if len(sys.argv) > 2 else None
        print_monthly_stats('default', ym)
    
    elif cmd == '--add':
        if len(sys.argv) < 7:
            print("❌ 参数不足: --add 账本 账户 类型 金额 分类 描述")
            sys.exit(1)
        _, _, ledger, account, trans_type, amount, category, *desc = sys.argv
        desc = desc[0] if desc else ''
        quick_add(ledger, account, trans_type, float(amount), category, desc)
    
    else:
        print(f"❌ 未知命令: {cmd}")