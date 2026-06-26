#!/usr/bin/env python3
"""
SQLite本地存储
"""
import json
import sqlite3
import logging
from pathlib import Path
from typing import List, Dict, Optional
from datetime import datetime


class SQLiteStorage:
    """SQLite存储"""
    
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.logger = logging.getLogger(__name__)
        self._init_db()
    
    def _init_db(self):
        """初始化数据库"""
        # 确保目录存在
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 创建表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS ipo_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                exchange TEXT NOT NULL,
                company_name TEXT,
                stock_code TEXT NOT NULL,
                application_status TEXT,
                expected_date TEXT,
                fundraising_amount TEXT,
                issue_price_range TEXT,
                update_time TEXT,
                source_url TEXT,
                source TEXT,
                create_time TEXT DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(exchange, stock_code)
            )
        ''')
        
        # 创建操作日志表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS operation_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                operation TEXT,
                exchange TEXT,
                stock_code TEXT,
                details TEXT,
                create_time TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def save_all(self, data: Dict[str, List[Dict]]):
        """保存所有数据"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        for exchange, ipo_list in data.items():
            for ipo in ipo_list:
                self._upsert(cursor, exchange, ipo)
        
        conn.commit()
        conn.close()
        
        self.logger.info(f"已保存 {sum(len(v) for v in data.values())} 条数据")
    
    def _upsert(self, cursor, exchange: str, ipo: Dict):
        """插入或更新"""
        cursor.execute('''
            INSERT OR REPLACE INTO ipo_data (
                exchange, company_name, stock_code, application_status,
                expected_date, fundraising_amount, issue_price_range,
                update_time, source_url, source
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            exchange,
            ipo.get('company_name', ''),
            ipo.get('stock_code', ''),
            ipo.get('application_status', ''),
            ipo.get('expected_date', ''),
            ipo.get('fundraising_amount', ''),
            ipo.get('issue_price_range', ''),
            ipo.get('update_time', ''),
            ipo.get('source_url', ''),
            ipo.get('source', '')
        ))
    
    def load_all(self) -> Dict[str, List[Dict]]:
        """加载所有数据"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT exchange, company_name, stock_code, application_status, expected_date, fundraising_amount, issue_price_range, update_time, source_url, source FROM ipo_data')
        
        rows = cursor.fetchall()
        conn.close()
        
        # 按交易所分组
        data = {}
        for row in rows:
            exchange = row[0]
            ipo = {
                'company_name': row[1],
                'stock_code': row[2],
                'application_status': row[3],
                'expected_date': row[4],
                'fundraising_amount': row[5],
                'issue_price_range': row[6],
                'update_time': row[7],
                'source_url': row[8],
                'source': row[9],
            }
            
            if exchange not in data:
                data[exchange] = []
            data[exchange].append(ipo)
        
        return data
    
    def load_by_exchange(self, exchange: str) -> List[Dict]:
        """按交易所加载"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT company_name, stock_code, application_status, expected_date,
                   fundraising_amount, issue_price_range, update_time, source_url, source
            FROM ipo_data WHERE exchange = ?
        ''', (exchange,))
        
        rows = cursor.fetchall()
        conn.close()
        
        return [
            {
                'company_name': row[0],
                'stock_code': row[1],
                'application_status': row[2],
                'expected_date': row[3],
                'fundraising_amount': row[4],
                'issue_price_range': row[5],
                'update_time': row[6],
                'source_url': row[7],
                'source': row[8],
            }
            for row in rows
        ]
    
    def log_operation(self, operation: str, exchange: str, stock_code: str, details: str = ''):
        """记录操作日志"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO operation_log (operation, exchange, stock_code, details)
            VALUES (?, ?, ?, ?)
        ''', (operation, exchange, stock_code, details))
        
        conn.commit()
        conn.close()


# 导出
__all__ = ['SQLiteStorage']
