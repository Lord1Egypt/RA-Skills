#!/usr/bin/env python3
"""
Ledger CLI - 命令行记账工具
"""
import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.services.ledger import (
    create_ledger,
    add_transaction,
    batch_add_transactions,
    set_opening_balance,
)
from src.services.report import (
    get_transactions,
    get_monthly_summary,
    get_balance_trend,
)
from src.db.connection import get_db_path
import tempfile


def main():
    # 使用临时数据库进行测试
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = os.path.join(tmpdir, "test_ledger.db")
        
        ledger_name = "test"
        
        print("=" * 50)
        print("账本测试演示")
        print("=" * 50)
        
        # 1. 创建账本
        print("\n1. 创建账本...")
        ledger_id = create_ledger(ledger_name, db_path)
        print(f"   账本 ID: {ledger_id}")
        
        # 2. 设置期初结余
        print("\n2. 设置期初结余 (2026-01: -15206)...")
        set_opening_balance(ledger_name, "2026-01", -15206.0, db_path)
        print("   期初结余已设置")
        
        # 3. 添加交易
        print("\n3. 添加交易...")
        transactions = [
            {"date": "2026-01-15", "amount": 5000.0, "category": "工资", "account": "银行卡"},
            {"date": "2026-02-10", "amount": -2000.0, "category": "房租", "account": "银行卡"},
            {"date": "2026-02-15", "amount": -50.0, "category": "餐饮", "account": "现金"},
            {"date": "2026-03-01", "amount": 5000.0, "category": "工资", "account": "银行卡"},
            {"date": "2026-03-05", "amount": -30.0, "category": "餐饮", "account": "现金"},
            {"date": "2026-03-10", "amount": -100.0, "category": "购物", "account": "银行卡"},
        ]
        count = batch_add_transactions(ledger_name, transactions, db_path)
        print(f"   已添加 {count} 笔交易")
        
        # 4. 查询月度汇总
        print("\n4. 查询 2026-03 月度汇总...")
        summary = get_monthly_summary(ledger_name, "2026-03", db_path)
        print(f"   期初: {summary['opening']}")
        print(f"   收入: {summary['income']}")
        print(f"   支出: {summary['expense']}")
        print(f"   期末: {summary['closing']}")
        print(f"   交易笔数: {len(summary['transactions'])}")
        
        # 5. 查询余额趋势
        print("\n5. 查询余额趋势 (2026-01 ~ 2026-03)...")
        trend = get_balance_trend(ledger_name, ["2026-01", "2026-02", "2026-03"], db_path)
        for item in trend:
            print(f"   {item['month']}: {item['balance']}")
        
        # 6. 打印所有交易
        print("\n6. 所有交易记录...")
        print(f"   {'日期':<12} {'分类':<8} {'金额':<10} {'账户':<8}")
        all_trans = get_transactions(ledger_name, None, db_path)
        print("   " + "-" * 40)
        for t in all_trans:
            print(f"   {t['date']:<12} {t['category']:<8} {t['amount']:<10} {t['account']:<8}")
        
        print("\n" + "=" * 50)
        print("测试完成!")
        print("=" * 50)


if __name__ == "__main__":
    main()
