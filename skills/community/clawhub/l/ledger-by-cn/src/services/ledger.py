"""
Ledger service - 账本和交易管理服务。
"""
import os
import sqlite3
from typing import List, Dict, Optional
from datetime import datetime, timedelta

from src.db.connection import init_db, get_connection, get_db_path


def create_ledger(name: str, db_path: str = None) -> int:
    """
    创建新账本。
    
    Args:
        name: 账本名称
        db_path: 数据库路径（可选）
    
    Returns:
        新创建的账本 ID
    
    Raises:
        Exception: 如果账本已存在
    """
    if db_path is None:
        db_path = get_db_path(name)
    
    conn = init_db(db_path)
    cursor = conn.cursor()
    
    try:
        cursor.execute("INSERT INTO ledgers (name) VALUES (?)", (name,))
        conn.commit()
        ledger_id = cursor.lastrowid
        return ledger_id
    except sqlite3.IntegrityError:
        raise Exception(f"账本 '{name}' 已存在")
    finally:
        conn.close()


def get_ledger_id(name: str, db_path: str = None) -> Optional[int]:
    """
    获取账本 ID。
    
    Args:
        name: 账本名称
        db_path: 数据库路径（可选）
    
    Returns:
        账本 ID，如果不存在则返回 None
    """
    if db_path is None:
        db_path = get_db_path(name)
    
    # 确保数据库文件存在
    if not os.path.exists(db_path):
        return None
    
    conn = get_connection(db_path)
    cursor = conn.cursor()
    
    cursor.execute("SELECT id FROM ledgers WHERE name = ?", (name,))
    row = cursor.fetchone()
    conn.close()
    
    return row['id'] if row else None


def add_transaction(
    ledger_name: str,
    transaction: Dict,
    db_path: str = None
) -> int:
    """
    添加单笔交易。
    
    Args:
        ledger_name: 账本名称
        transaction: 交易数据，包含 date, amount, category, account, description
        db_path: 数据库路径（可选）
    
    Returns:
        新创建的交易 ID
    """
    if db_path is None:
        db_path = get_db_path(ledger_name)
    
    conn = init_db(db_path)
    cursor = conn.cursor()
    
    # 获取账本 ID
    cursor.execute("SELECT id FROM ledgers WHERE name = ?", (ledger_name,))
    row = cursor.fetchone()
    if not row:
        conn.close()
        raise Exception(f"账本 '{ledger_name}' 不存在")
    
    ledger_id = row['id']
    
    # 生成时间戳（如果未提供）
    created_at = transaction.get('created_at')
    if not created_at:
        created_at = datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
    
    # 插入交易记录
    cursor.execute(
        """INSERT INTO transactions 
           (ledger_id, date, amount, category, account, description, created_at) 
           VALUES (?, ?, ?, ?, ?, ?, ?)""",
        (
            ledger_id,
            transaction.get('date'),
            transaction.get('amount', 0),
            transaction.get('category', '其他'),
            transaction.get('account', '现金'),
            transaction.get('description', ''),
            created_at
        )
    )
    conn.commit()
    trans_id = cursor.lastrowid
    conn.close()
    
    return trans_id


def batch_add_transactions(
    ledger_name: str,
    transactions: List[Dict],
    db_path: str = None
) -> int:
    """
    批量添加交易。
    
    Args:
        ledger_name: 账本名称
        transactions: 交易列表
        db_path: 数据库路径（可选）
    
    Returns:
        添加的交易数量
    """
    if db_path is None:
        db_path = get_db_path(ledger_name)
    
    conn = init_db(db_path)
    cursor = conn.cursor()
    
    # 获取账本 ID
    cursor.execute("SELECT id FROM ledgers WHERE name = ?", (ledger_name,))
    row = cursor.fetchone()
    if not row:
        conn.close()
        raise Exception(f"账本 '{ledger_name}' 不存在")
    
    ledger_id = row['id']
    
    count = 0
    for trans in transactions:
        cursor.execute(
            """INSERT INTO transactions 
               (ledger_id, date, amount, category, account, description) 
               VALUES (?, ?, ?, ?, ?, ?)""",
            (
                ledger_id,
                trans.get('date'),
                trans.get('amount', 0),
                trans.get('category', '其他'),
                trans.get('account', '现金'),
                trans.get('description', '')
            )
        )
        count += 1
    
    conn.commit()
    conn.close()
    
    return count


def set_opening_balance(
    ledger_name: str,
    month: str,
    amount: float,
    db_path: str = None
) -> bool:
    """
    设置期初结余。
    
    Args:
        ledger_name: 账本名称
        month: 月份（YYYY-MM）
        amount: 期初金额
        db_path: 数据库路径（可选）
    
    Returns:
        是否设置成功
    """
    if db_path is None:
        db_path = get_db_path(ledger_name)
    
    conn = init_db(db_path)
    cursor = conn.cursor()
    
    # 获取账本 ID
    cursor.execute("SELECT id FROM ledgers WHERE name = ?", (ledger_name,))
    row = cursor.fetchone()
    if not row:
        conn.close()
        raise Exception(f"账本 '{ledger_name}' 不存在")
    
    ledger_id = row['id']
    
    # 使用 INSERT OR REPLACE 来更新或插入
    cursor.execute(
        """INSERT OR REPLACE INTO openings (ledger_id, month, amount, created_at)
           VALUES (?, ?, ?, ?)""",
        (ledger_id, month, amount, datetime.now().isoformat())
    )
    conn.commit()
    conn.close()
    
    return True
