#!/usr/bin/env python3
"""物流查询助手 - 支持多家快递公司物流追踪"""

import argparse
import asyncio
import json
import os
import re
import sqlite3
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Dict

import aiohttp

# 安全存储
try:
    from security import SecureStorage
except ImportError:
    print("请安装加密库: pip install cryptography")
    sys.exit(1)

secure_storage = SecureStorage(app_name="logistics")

# 配置
CONFIG_DIR = Path.home() / ".openclaw" / "data" / "logistics"
DB_FILE = CONFIG_DIR / "logistics.db"
CONFIG_DIR.mkdir(parents=True, exist_ok=True)

# 快递公司配置
CARRIERS = {
    'sf': {'name': '顺丰速运', 'pattern': r'^[A-Z]{2}\d{10,}$|^[0-9]{12,15}$'},
    'zto': {'name': '中通快递', 'pattern': r'^7(5|6|7)\d{10}$|^(7|5|6)\d{13}$|^(3|4)\d{12}$|^ZT\d{12}$'},
    'yto': {'name': '圆通速递', 'pattern': r'^[A-Z]{2}\d{10}$|^YT\d{12}$|^\d{10}$|^\d{12}$'},
    'sto': {'name': '申通快递', 'pattern': r'^(77|88|33|44)\d{11}$|^STO\d{10}$|^\d{12}$'},
    'yunda': {'name': '韵达速递', 'pattern': r'^(10|11|12|13|14|15|16|17|18|19)\d{11}$|^YD\d{12}$'},
    'best': {'name': '百世快递', 'pattern': r'^(50|51|52|53|54|55|56|57|58|59)\d{11}$|^\d{14}$'},
    'jd': {'name': '京东物流', 'pattern': r'^JD[A-Z0-9]{10,15}$|^JD\d{12}$|^\d{13}$'},
    'ems': {'name': '邮政EMS', 'pattern': r'^[A-Z]{2}\d{9}[A-Z]{2}$|^10\d{11}$|^11\d{11}$'},
    'deppon': {'name': '德邦快递', 'pattern': r'^DPK\d{10,}$|^\d{8,12}$'},
    'jt': {'name': '极兔速递', 'pattern': r'^JT\d{12}$|^80\d{11}$|^\d{15}$'},
    'cainiao': {'name': '菜鸟裹裹', 'pattern': r'^\d{13,20}$'},
    'danniao': {'name': '丹鸟物流', 'pattern': r'^DN\d{12}$|^\d{13}$'},
}


@dataclass
class TrackingEvent:
    """物流事件"""
    time: str
    description: str
    location: str
    status: str


@dataclass
class TrackingResult:
    """查询结果"""
    tracking_number: str
    carrier_code: str
    carrier_name: str
    status: str  # pending, in_transit, delivered, exception
    events: List[TrackingEvent]
    estimated_delivery: Optional[str] = None
    last_updated: Optional[str] = None


class LogisticsClient:
    """物流查询客户端"""
    
    # 使用快递100 API (示例，实际使用时需要申请API Key)
    API_BASE = "https://api.kuaidi100.com"
    
    def __init__(self):
        self.db = self._init_db()
        self.session: Optional[aiohttp.ClientSession] = None
    
    def _init_db(self) -> sqlite3.Connection:
        """初始化数据库"""
        conn = sqlite3.connect(str(DB_FILE))
        cursor = conn.cursor()
        
        # 查询历史表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tracking_number TEXT NOT NULL,
                carrier_code TEXT,
                carrier_name TEXT,
                status TEXT,
                result TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # 订阅表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS subscriptions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tracking_number TEXT NOT NULL UNIQUE,
                carrier_code TEXT,
                last_status TEXT,
                notify_enabled BOOLEAN DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        return conn
    
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    def detect_carrier(self, tracking_number: str) -> Optional[str]:
        """智能识别快递公司"""
        for code, config in CARRIERS.items():
            if re.match(config['pattern'], tracking_number.upper()):
                return code
        return None
    
    async def query(self, tracking_number: str, carrier_code: Optional[str] = None) -> TrackingResult:
        """查询物流信息"""
        # 自动识别快递公司
        if not carrier_code:
            carrier_code = self.detect_carrier(tracking_number)
            if not carrier_code:
                raise ValueError(f"无法识别单号 {tracking_number} 的快递公司，请手动指定")
        
        carrier_name = CARRIERS.get(carrier_code, {}).get('name', '未知快递')
        
        # 模拟查询结果（实际使用时调用真实API）
        # 这里返回模拟数据作为示例
        result = TrackingResult(
            tracking_number=tracking_number,
            carrier_code=carrier_code,
            carrier_name=carrier_name,
            status="in_transit",
            events=[
                TrackingEvent(
                    time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    description="快件已到达【北京顺义集散中心】",
                    location="北京市",
                    status="in_transit"
                ),
                TrackingEvent(
                    time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    description="快件已从【上海虹桥集散中心】发出",
                    location="上海市",
                    status="in_transit"
                ),
            ],
            last_updated=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
        
        # 保存到历史记录
        self._save_history(result)
        
        return result
    
    async def batch_query(self, tracking_numbers: List[str]) -> List[TrackingResult]:
        """批量查询"""
        tasks = []
        for number in tracking_numbers:
            carrier = self.detect_carrier(number)
            tasks.append(self.query(number, carrier))
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        return [r for r in results if not isinstance(r, Exception)]
    
    def _save_history(self, result: TrackingResult):
        """保存查询历史"""
        cursor = self.db.cursor()
        cursor.execute('''
            INSERT INTO history (tracking_number, carrier_code, carrier_name, status, result)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            result.tracking_number,
            result.carrier_code,
            result.carrier_name,
            result.status,
            json.dumps(result.__dict__, default=lambda x: x.__dict__ if hasattr(x, '__dict__') else str(x))
        ))
        self.db.commit()
    
    def get_history(self, limit: int = 10, search: Optional[str] = None) -> List[dict]:
        """获取查询历史"""
        cursor = self.db.cursor()
        
        if search:
            cursor.execute('''
                SELECT * FROM history 
                WHERE tracking_number LIKE ? 
                ORDER BY created_at DESC LIMIT ?
            ''', (f'%{search}%', limit))
        else:
            cursor.execute('''
                SELECT * FROM history 
                ORDER BY created_at DESC LIMIT ?
            ''', (limit,))
        
        columns = [description[0] for description in cursor.description]
        results = []
        for row in cursor.fetchall():
            results.append(dict(zip(columns, row)))
        return results
    
    def subscribe(self, tracking_number: str, carrier_code: Optional[str] = None):
        """订阅物流提醒"""
        if not carrier_code:
            carrier_code = self.detect_carrier(tracking_number) or 'unknown'
        
        cursor = self.db.cursor()
        cursor.execute('''
            INSERT OR REPLACE INTO subscriptions (tracking_number, carrier_code, last_status)
            VALUES (?, ?, ?)
        ''', (tracking_number, carrier_code, 'pending'))
        self.db.commit()
        return True
    
    def unsubscribe(self, tracking_number: str):
        """取消订阅"""
        cursor = self.db.cursor()
        cursor.execute('DELETE FROM subscriptions WHERE tracking_number = ?', (tracking_number,))
        self.db.commit()
        return True
    
    def get_subscriptions(self) -> List[dict]:
        """获取所有订阅"""
        cursor = self.db.cursor()
        cursor.execute('SELECT * FROM subscriptions ORDER BY created_at DESC')
        columns = [description[0] for description in cursor.description]
        results = []
        for row in cursor.fetchall():
            results.append(dict(zip(columns, row)))
        return results
    
    def format_result(self, result: TrackingResult) -> str:
        """格式化查询结果"""
        lines = [
            f"📦 {result.carrier_name} ({result.tracking_number})",
            f"状态: {self._format_status(result.status)}",
            f"更新时间: {result.last_updated or '未知'}",
            "",
            "物流轨迹:",
        ]
        
        for event in result.events:
            lines.append(f"  [{event.time}] {event.location} - {event.description}")
        
        return "\n".join(lines)
    
    def _format_status(self, status: str) -> str:
        """格式化状态"""
        status_map = {
            'pending': '⏳ 待发货',
            'in_transit': '🚚 运输中',
            'delivered': '✅ 已签收',
            'exception': '⚠️ 异常',
        }
        return status_map.get(status, status)


def print_carriers():
    """打印支持的快递公司"""
    print("支持的快递公司:\n")
    print(f"{'代码':<10} {'名称':<15}")
    print("-" * 30)
    for code, config in CARRIERS.items():
        print(f"{code:<10} {config['name']:<15}")


def print_history(client: LogisticsClient, limit: int = 10, search: Optional[str] = None):
    """打印查询历史"""
    history = client.get_history(limit, search)
    if not history:
        print("暂无查询记录")
        return
    
    print(f"最近 {len(history)} 条查询记录:\n")
    print(f"{'单号':<20} {'快递公司':<12} {'状态':<10} {'查询时间':<20}")
    print("-" * 70)
    
    for record in history:
        print(f"{record['tracking_number']:<20} {record['carrier_name']:<12} "
              f"{record['status']:<10} {record['created_at']:<20}")


def print_subscriptions(client: LogisticsClient):
    """打印订阅列表"""
    subs = client.get_subscriptions()
    if not subs:
        print("暂无订阅")
        return
    
    print(f"共 {len(subs)} 个订阅:\n")
    print(f"{'单号':<20} {'快递公司':<12} {'最后状态':<12} {'订阅时间':<20}")
    print("-" * 70)
    
    for sub in subs:
        carrier_name = CARRIERS.get(sub['carrier_code'], {}).get('name', sub['carrier_code'])
        print(f"{sub['tracking_number']:<20} {carrier_name:<12} "
              f"{sub['last_status']:<12} {sub['created_at']:<20}")


def print_privacy_info():
    """打印隐私信息"""
    info = secure_storage.get_storage_info()
    print("存储信息:\n")
    print(f"存储目录: {info['base_dir']}")
    print(f"文件数量: {info['total_files']}\n")
    
    if info['files']:
        print("文件列表:")
        for f in info['files']:
            print(f"  - {f['name']} ({f['size']} bytes, 权限: {f['permissions']})")


async def main():
    parser = argparse.ArgumentParser(description='物流查询助手')
    subparsers = parser.add_subparsers(dest='command', help='可用命令')
    
    # 单号查询
    query_parser = subparsers.add_parser('query', help='查询单个快递')
    query_parser.add_argument('tracking_number', help='快递单号')
    query_parser.add_argument('--carrier', '-c', help='快递公司代码')
    
    # 批量查询
    batch_parser = subparsers.add_parser('batch', help='批量查询')
    batch_parser.add_argument('tracking_numbers', nargs='+', help='快递单号列表')
    
    # 历史记录
    history_parser = subparsers.add_parser('history', help='查询历史')
    history_parser.add_argument('--limit', '-l', type=int, default=10, help='显示数量')
    history_parser.add_argument('--search', '-s', help='搜索单号')
    
    # 订阅
    sub_parser = subparsers.add_parser('subscribe', help='订阅物流提醒')
    sub_parser.add_argument('tracking_number', help='快递单号')
    sub_parser.add_argument('--carrier', '-c', help='快递公司代码')
    
    # 取消订阅
    unsub_parser = subparsers.add_parser('unsubscribe', help='取消订阅')
    unsub_parser.add_argument('tracking_number', help='快递单号')
    
    # 订阅列表
    subparsers.add_parser('subscriptions', help='查看所有订阅')
    
    # 快递公司列表
    subparsers.add_parser('carriers', help='查看支持的快递公司')
    
    # 隐私控制
    privacy_parser = subparsers.add_parser('privacy', help='隐私控制')
    privacy_parser.add_argument('action', choices=['info', 'clear', 'export'], 
                                help='info: 查看信息, clear: 清除数据, export: 导出备份')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    # 显示快递公司列表
    if args.command == 'carriers':
        print_carriers()
        return
    
    # 隐私控制
    if args.command == 'privacy':
        if args.action == 'info':
            print_privacy_info()
        elif args.action == 'clear':
            secure_storage.clear_all()
            print("✅ 已清除所有个人数据")
        elif args.action == 'export':
            info = secure_storage.get_storage_info()
            export_file = CONFIG_DIR / 'privacy_export.json'
            with open(export_file, 'w') as f:
                json.dump(info, f, indent=2)
            print(f"✅ 已导出到: {export_file}")
        return
    
    # 初始化客户端
    async with LogisticsClient() as client:
        # 单号查询
        if args.command == 'query':
            try:
                result = await client.query(args.tracking_number, args.carrier)
                print(client.format_result(result))
            except Exception as e:
                print(f"❌ 查询失败: {e}")
        
        # 批量查询
        elif args.command == 'batch':
            results = await client.batch_query(args.tracking_numbers)
            for result in results:
                print(client.format_result(result))
                print("\n" + "="*50 + "\n")
        
        # 历史记录
        elif args.command == 'history':
            print_history(client, args.limit, args.search)
        
        # 订阅
        elif args.command == 'subscribe':
            if client.subscribe(args.tracking_number, args.carrier):
                print(f"✅ 已订阅 {args.tracking_number} 的物流提醒")
        
        # 取消订阅
        elif args.command == 'unsubscribe':
            if client.unsubscribe(args.tracking_number):
                print(f"✅ 已取消 {args.tracking_number} 的订阅")
        
        # 订阅列表
        elif args.command == 'subscriptions':
            print_subscriptions(client)


if __name__ == '__main__':
    asyncio.run(main())
