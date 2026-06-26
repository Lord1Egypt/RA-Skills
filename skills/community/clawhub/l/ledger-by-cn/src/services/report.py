"""
Report service - 报表统计服务。
"""
from typing import List, Dict, Optional

from src.db.connection import get_connection, get_db_path


def get_transactions(
    ledger_name: str,
    month: Optional[str] = None,
    db_path: str = None
) -> List[Dict]:
    """
    获取交易记录。
    
    Args:
        ledger_name: 账本名称
        month: 月份（YYYY-MM），为空则获取全部
        db_path: 数据库路径（可选）
    
    Returns:
        交易记录列表
    """
    if db_path is None:
        db_path = get_db_path(ledger_name)
    
    conn = get_connection(db_path)
    cursor = conn.cursor()
    
    # 获取账本 ID
    cursor.execute("SELECT id FROM ledgers WHERE name = ?", (ledger_name,))
    row = cursor.fetchone()
    if not row:
        conn.close()
        return []
    
    ledger_id = row['id']
    
    # 查询交易记录
    if month:
        # 格式化为 YYYY-MM%
        query_month = f"{month}%"
        cursor.execute(
            """SELECT id, date, amount, category, account, description, created_at
               FROM transactions 
               WHERE ledger_id = ? AND date LIKE ?
               ORDER BY date""",
            (ledger_id, query_month)
        )
    else:
        cursor.execute(
            """SELECT id, date, amount, category, account, description, created_at
               FROM transactions 
               WHERE ledger_id = ?
               ORDER BY date""",
            (ledger_id,)
        )
    
    transactions = []
    for row in cursor.fetchall():
        transactions.append({
            'id': row['id'],
            'date': row['date'],
            'amount': row['amount'],
            'category': row['category'],
            'account': row['account'],
            'description': row['description'],
            'created_at': row['created_at']
        })
    
    conn.close()
    return transactions


def get_monthly_summary(
    ledger_name: str,
    month: str,
    db_path: str = None
) -> Dict:
    """
    获取月度汇总。
    
    Args:
        ledger_name: 账本名称
        month: 月份（YYYY-MM）
        db_path: 数据库路径（可选）
    
    Returns:
        汇总数据字典
    """
    if db_path is None:
        db_path = get_db_path(ledger_name)
    
    conn = get_connection(db_path)
    cursor = conn.cursor()
    
    # 获取账本 ID
    cursor.execute("SELECT id FROM ledgers WHERE name = ?", (ledger_name,))
    row = cursor.fetchone()
    if not row:
        conn.close()
        return {
            'opening': 0,
            'income': 0,
            'expense': 0,
            'closing': 0,
            'transactions': []
        }
    
    ledger_id = row['id']
    
    # 获取期初结余（取最新的）
    cursor.execute(
        """SELECT amount FROM openings 
           WHERE ledger_id = ? AND month = ?
           ORDER BY created_at DESC LIMIT 1""",
        (ledger_id, month)
    )
    opening_row = cursor.fetchone()
    opening = opening_row['amount'] if opening_row else 0.0
    
    # 获取本月交易
    query_month = f"{month}%"
    cursor.execute(
        """SELECT id, date, amount, category, account, description, created_at
           FROM transactions 
           WHERE ledger_id = ? AND date LIKE ?
           ORDER BY date""",
        (ledger_id, query_month)
    )
    
    transactions = []
    income = 0.0
    expense = 0.0
    
    for row in cursor.fetchall():
        amount = row['amount']
        transactions.append({
            'id': row['id'],
            'date': row['date'],
            'amount': amount,
            'category': row['category'],
            'account': row['account'],
            'description': row['description'],
            'created_at': row['created_at']
        })
        
        if amount > 0:
            income += amount
        else:
            expense += amount
    
    closing = opening + income + expense
    
    conn.close()
    
    return {
        'opening': opening,
        'income': income,
        'expense': expense,
        'closing': closing,
        'transactions': transactions
    }


def get_ledger_date_range(ledger_name: str, db_path: str = None) -> Dict:
    """
    获取账本中交易记录的日期范围。
    
    Args:
        ledger_name: 账本名称
        db_path: 数据库路径（可选）
    
    Returns:
        包含最早和最新月份的字典，如 {'start': '2025-01', 'end': '2026-03'}
        如果没有交易记录返回 {'start': None, 'end': None}
    """
    if db_path is None:
        db_path = get_db_path(ledger_name)
    
    conn = get_connection(db_path)
    cursor = conn.cursor()
    
    # 获取账本 ID
    cursor.execute("SELECT id FROM ledgers WHERE name = ?", (ledger_name,))
    row = cursor.fetchone()
    if not row:
        conn.close()
        return {'start': None, 'end': None}
    
    ledger_id = row['id']
    
    # 查询最早和最新的日期
    cursor.execute(
        """SELECT MIN(date) as min_date, MAX(date) as max_date 
           FROM transactions WHERE ledger_id = ?""",
        (ledger_id,)
    )
    row = cursor.fetchone()
    conn.close()
    
    if not row or not row['min_date']:
        return {'start': None, 'end': None}
    
    # 返回完整日期（YYYY-MM-DD）
    return {'start': row['min_date'], 'end': row['max_date']}


def get_balance_trend(
    ledger_name: str,
    months: List[str],
    db_path: str = None
) -> List[Dict]:
    """
    获取余额趋势。
    
    Args:
        ledger_name: 账本名称
        months: 月份列表
        db_path: 数据库路径（可选）
    
    Returns:
        余额趋势列表
    """
    if db_path is None:
        db_path = get_db_path(ledger_name)
    
    conn = get_connection(db_path)
    cursor = conn.cursor()
    
    # 获取账本 ID
    cursor.execute("SELECT id FROM ledgers WHERE name = ?", (ledger_name,))
    row = cursor.fetchone()
    if not row:
        conn.close()
        return []
    
    ledger_id = row['id']
    
    # 获取所有期初结余
    cursor.execute(
        """SELECT month, amount FROM openings 
           WHERE ledger_id = ?
           ORDER BY created_at DESC""",
        (ledger_id,)
    )
    openings = {}
    for row in cursor.fetchall():
        if row['month'] not in openings:
            openings[row['month']] = row['amount']
    
    # 获取所有交易
    cursor.execute(
        """SELECT date, amount FROM transactions 
           WHERE ledger_id = ?
           ORDER BY date""",
        (ledger_id,)
    )
    all_transactions = cursor.fetchall()
    
    conn.close()
    
    # 计算每个月累计余额
    result = []
    cumulative_balance = 0.0
    
    for month in months:
        # 获取该月的期初结余
        opening = openings.get(month, 0.0)
        
        # 只在第一个月加上期初结余
        if month == months[0]:
            cumulative_balance = opening
        
        # 累加该月的所有交易
        month_prefix = f"{month}-"
        for trans in all_transactions:
            if trans['date'].startswith(month_prefix):
                cumulative_balance += trans['amount']
        
        result.append({
            'month': month,
            'balance': cumulative_balance
        })
    
    return result
