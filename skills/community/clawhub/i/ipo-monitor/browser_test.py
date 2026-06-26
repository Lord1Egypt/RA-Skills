#!/usr/bin/env python3
"""
IPO监控 V2 - 浏览器抓取测试
使用真实浏览器方式抓取IPO数据
"""
import sys
import os
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List
import json

# 添加当前目录到路径
sys.path.insert(0, str(Path(__file__).parent))

from config import Config


class BrowserIPOFetcher:
    """使用浏览器抓取IPO数据"""
    
    # 交易所URL配置
    EXCHANGES = {
        "上交所": "https://www.sse.com.cn/listing/renewal/ipo/",
        "深交所": "https://www.szse.cn/listing/projectdynamic/ipo/",
        "北交所": "https://www.bse.cn/audit/project_news.html",
    }
    
    def __init__(self, config):
        self.config = config
        self.logger = logging.getLogger('browser_ipo')
        
        # 设置日志
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
    
    def fetch_sse(self, browser) -> List[Dict]:
        """抓取上交所IPO数据"""
        self.logger.info("抓取上交所IPO数据...")
        
        url = self.EXCHANGES["上交所"]
        
        # 打开页面
        result = browser.action(action="open", url=url)
        tab_id = result.get("targetId")
        
        # 等待加载
        browser.action(
            action="snapshot",
            targetId=tab_id,
            loadState="networkidle",
            timeoutMs=30000
        )
        
        # 获取快照
        snapshot = browser.action(action="snapshot", targetId=tab_id)
        
        # 解析数据
        return self._parse_sse(snapshot)
    
    def _parse_sse(self, snapshot: Dict) -> List[Dict]:
        """解析上交所快照"""
        results = []
        
        # snapshot包含aria树结构
        # 查找表格
        def find_table(node):
            if isinstance(node, dict):
                if node.get('role') == 'table' or node.get('role') == 'grid':
                    return node
                for v in node.values():
                    result = find_table(v)
                    if result:
                        return result
            elif isinstance(node, list):
                for item in node:
                    result = find_table(item)
                    if result:
                        return result
            return None
        
        # 简化：直接解析aria树中的表格数据
        # 从snapshot的结构中提取表格行
        rows = self._extract_table_rows(snapshot)
        
        for row in rows:
            # 跳过表头
            if row.get('isHeader'):
                continue
            
            cells = row.get('cells', [])
            if len(cells) >= 9:
                ipo_info = {
                    'company_name': cells[0].get('text', ''),
                    'board': cells[1].get('text', ''),  # 板块
                    'stock_code': '',  # 上交所没有股票代码
                    'exchange': '上交所',
                    'application_status': cells[2].get('text', ''),  # 审核状态
                    'province': cells[3].get('text', ''),  # 注册地
                    'industry': cells[4].get('text', ''),  # 行业分类
                    'sponsor': cells[5].get('text', ''),  # 保荐机构
                    'law_firm': cells[6].get('text', ''),  # 律师事务所
                    'accounting_firm': cells[7].get('text', ''),  # 会计师事务所
                    'update_date': cells[8].get('text', ''),  # 更新日期
                    'accept_date': cells[9].get('text', '') if len(cells) > 9 else '',  # 受理日期
                    'update_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'source_url': self.EXCHANGES["上交所"],
                    'source': '上交所',
                }
                
                if ipo_info['company_name']:
                    results.append(ipo_info)
        
        self.logger.info(f"上交所: 获取 {len(results)} 条记录")
        return results
    
    def _extract_table_rows(self, snapshot: Dict) -> List[Dict]:
        """从快照中提取表格行"""
        rows = []
        
        def traverse(node, parent=None):
            if not isinstance(node, dict):
                return
            
            role = node.get('role', '')
            
            # 查找行
            if role in ['row', 'rowgroup']:
                row_data = {'cells': [], 'isHeader': role == 'rowgroup'}
                
                # 获取单元格
                children = node.get('children', [])
                for child in children:
                    if isinstance(child, dict):
                        cell_text = child.get('name', '') or child.get('text', '')
                        if cell_text:
                            row_data['cells'].append({'text': cell_text})
                
                if row_data['cells']:
                    rows.append(row_data)
            
            # 递归遍历
            children = node.get('children', [])
            for child in children:
                traverse(child, node)
        
        # 从snapshot的root开始遍历
        root = snapshot.get('root', {})
        traverse(root)
        
        return rows


def test_browser_fetch(browser):
    """测试浏览器抓取"""
    config = Config()
    fetcher = BrowserIPOFetcher(config)
    
    # 抓取上交所
    data = fetcher.fetch_sse(browser)
    
    print("\n" + "=" * 60)
    print("上交所IPO数据抓取结果:")
    print("=" * 60)
    
    for i, item in enumerate(data[:10], 1):
        print(f"{i}. {item.get('company_name')}")
        print(f"   板块: {item.get('board')} | 状态: {item.get('application_status')}")
        print(f"   注册地: {item.get('province')} | 行业: {item.get('industry')}")
        print(f"   更新日期: {item.get('update_date')}")
        print()
    
    print(f"共 {len(data)} 条记录")
    print("=" * 60)
    
    return data


if __name__ == '__main__':
    print("需要通过OpenClaw的browser工具调用")
    print("请在OpenClaw中运行此模块")
