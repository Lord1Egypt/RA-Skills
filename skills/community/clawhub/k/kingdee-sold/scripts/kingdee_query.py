#!/usr/bin/env python3
"""
金蝶ERP数据库查询工具
用于连接金蝶PostgreSQL数据库并执行常用查询
"""

import psycopg2
from psycopg2 import Error
import json
from datetime import datetime, date

# 数据库连接配置
DB_CONFIG = {
    'host': '111.198.79.26',
    'port': 5432,
    'user': 'cosmic',
    'password': 'Kd1234567890!',
    'database': 'yyzl202501',
}

class JSONEncoder(json.JSONEncoder):
    """处理日期时间类型的JSON编码器"""
    def default(self, obj):
        if isinstance(obj, (datetime, date)):
            return obj.isoformat()
        return super().default(obj)

class KingdeeDB:
    """金蝶数据库连接类"""
    
    def __init__(self, config=None):
        self.config = config or DB_CONFIG
        self.connection = None
        
    def connect(self):
        """建立数据库连接"""
        try:
            self.connection = psycopg2.connect(**self.config)
            print("✓ 数据库连接成功")
            return True
        except Error as e:
            print(f"✗ 数据库连接失败: {e}")
            return False
    
    def close(self):
        """关闭数据库连接"""
        if self.connection:
            self.connection.close()
            print("✓ 数据库连接已关闭")
    
    def execute_query(self, sql, params=None, limit=None):
        """执行查询并返回结果"""
        if not self.connection:
            print("✗ 请先建立数据库连接")
            return None
        
        try:
            cursor = self.connection.cursor()
            cursor.execute(sql, params or ())
            
            # 获取列名
            columns = [desc[0] for desc in cursor.description]
            
            # 获取数据
            if limit:
                rows = cursor.fetchmany(limit)
            else:
                rows = cursor.fetchall()
            
            cursor.close()
            
            # 转换为字典列表
            results = [dict(zip(columns, row)) for row in rows]
            
            print(f"✓ 查询成功，返回 {len(results)} 条记录")
            return results
            
        except Error as e:
            print(f"✗ 查询失败: {e}")
            return None
    
    def print_results(self, results, max_rows=20):
        """打印查询结果"""
        if not results:
            print("(无数据)")
            return
        
        if len(results) > max_rows:
            print(f"显示前 {max_rows} 条，共 {len(results)} 条:")
            display = results[:max_rows]
        else:
            display = results
        
        # 打印表头
        if display:
            columns = list(display[0].keys())
            print(" | ".join(columns))
            print("-+-".join(["-" * len(c) for c in columns]))
            
            for row in display:
                values = [str(row[c])[:50] for c in columns]
                print(" | ".join(values))
    
    def to_json(self, results, indent=2):
        """转换为JSON格式"""
        return json.dumps(results, cls=JSONEncoder, indent=indent, ensure_ascii=False)


# 常用查询函数
def query_purchase_orders(db, start_date='2025-01-01', limit=100):
    """查询采购订单"""
    sql = """
    SELECT fid, fnumber, fdate, fsupplierid, famount_lc, fdocumentstatus
    FROM t_po_purorder
    WHERE fdate >= %s
    ORDER BY fdate DESC
    LIMIT %s
    """
    return db.execute_query(sql, (start_date, limit))


def query_sales_orders(db, start_date='2025-01-01', limit=100):
    """查询销售订单"""
    sql = """
    SELECT fid, fnumber, fdate, fcustid, famount_lc, fdocumentstatus
    FROM t_sal_saleorder
    WHERE fdate >= %s
    ORDER BY fdate DESC
    LIMIT %s
    """
    return db.execute_query(sql, (start_date, limit))


def query_pay_bills(db, start_date='2025-01-01', limit=100):
    """查询付款单"""
    sql = """
    SELECT fid, fnumber, fdate, famount_lc, fpaytype, fdocumentstatus
    FROM t_ap_paybill
    WHERE fdate >= %s
    ORDER BY fdate DESC
    LIMIT %s
    """
    return db.execute_query(sql, (start_date, limit))


def describe_table(db, table_name):
    """查询表结构"""
    sql = """
    SELECT column_name, data_type, is_nullable
    FROM information_schema.columns
    WHERE table_name = %s AND table_schema = 'public'
    ORDER BY ordinal_position
    """
    return db.execute_query(sql, (table_name,))


def search_tables(db, keyword):
    """搜索表名"""
    sql = """
    SELECT table_name
    FROM information_schema.tables
    WHERE table_schema = 'public' AND table_name LIKE %s
    ORDER BY table_name
    """
    return db.execute_query(sql, (f'%{keyword}%',))


# 使用示例
if __name__ == '__main__':
    db = KingdeeDB()
    
    if db.connect():
        # 示例: 查询采购订单
        print("\n=== 采购订单 ===")
        results = query_purchase_orders(db, limit=10)
        db.print_results(results)
        
        # 示例: 查询表结构
        print("\n=== t_po_purorder 表结构 ===")
        columns = describe_table(db, 't_po_purorder')
        db.print_results(columns)
        
        db.close()
