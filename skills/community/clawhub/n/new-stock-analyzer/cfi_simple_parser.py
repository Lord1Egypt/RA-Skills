#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
中财网新股数据简单解析器
直接从页面文本中提取新股数据
"""

import re
import logging
from datetime import datetime
from typing import Dict, List
import requests

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class CFISimpleParser:
    """中财网新股数据简单解析器"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        })
        
        self.base_url = 'https://newstock.cfi.cn/'
    
    def fetch_and_parse(self) -> List[Dict]:
        """获取并解析中财网新股数据"""
        try:
            logger.info(f"访问中财网: {self.base_url}")
            response = self.session.get(self.base_url, timeout=15)
            response.raise_for_status()
            
            content = response.text
            logger.info(f"页面获取成功，长度: {len(content)} 字符")
            
            # 直接使用正则表达式提取新股数据
            stocks = self._extract_stocks_from_text(content)
            
            # 过滤今天及未来的新股
            today = datetime.now().strftime('%Y-%m-%d')
            future_stocks = [s for s in stocks if s.get('apply_date', '') >= today]
            
            # 按申购日期排序
            future_stocks.sort(key=lambda x: x.get('apply_date', ''))
            
            logger.info(f"提取到 {len(future_stocks)} 只今天及未来新股")
            return future_stocks
            
        except Exception as e:
            logger.error(f"中财网数据获取失败: {e}")
            return []
    
    def _extract_stocks_from_text(self, content: str) -> List[Dict]:
        """从页面文本中提取新股数据"""
        stocks = []
        
        # 查找新股表格区域
        # 先找到"即将发行的新股"部分
        ipo_start = content.find('即将发行的新股')
        if ipo_start == -1:
            logger.warning("未找到'即将发行的新股'部分")
            return []
        
        # 提取新股表格区域（大约2000字符）
        ipo_section = content[ipo_start:ipo_start + 2000]
        
        # 使用正则表达式匹配新股行
        # 模式: 股票名称(市场) 申购日期 申购代码 发行价 发行量 申购限额
        stock_pattern = r'([\u4e00-\u9fa5]+(?:\([科创北]\))?)\s+(\d{1,2}月\d{1,2}日[周今]*)\s+([沪深北]:[\d]+)\s+([\d.]+|待定)\s+([\d.]+[万亿]*)\s+([\d.]+[万股]*)'
        
        matches = re.findall(stock_pattern, ipo_section)
        
        for match in matches:
            name, date_str, apply_code, price_str, issue_num_str, apply_limit_str = match
            
            # 提取股票代码
            code_match = re.search(r'(\d{6})', apply_code)
            if not code_match:
                continue
            
            code = code_match.group(1)
            
            # 解析数据
            stock = {
                'source': 'cfi',
                'code': code,
                'name': name,
                'apply_date': self._parse_date(date_str),
                'issue_price': self._parse_price(price_str),
                'apply_code': apply_code,
                'issue_num': self._parse_issue_num(issue_num_str),
                'apply_limit': self._parse_apply_limit(apply_limit_str),
                'market_type': self._infer_market_type(code, apply_code, name),
            }
            
            stocks.append(stock)
        
        # 如果没有匹配到，尝试更宽松的匹配
        if not stocks:
            logger.info("尝试宽松匹配...")
            stocks = self._extract_stocks_loose(content)
        
        return stocks
    
    def _extract_stocks_loose(self, content: str) -> List[Dict]:
        """宽松匹配新股数据"""
        stocks = []
        
        # 匹配股票名称和代码
        # 查找类似 "泰金新能(科)03月20日周五沪:787813待定" 的模式
        loose_pattern = r'([\u4e00-\u9fa5]+(?:\([科创北]\))?)(\d{1,2}月\d{1,2}日[周今]*)([沪深北]:\d+)([\d.]+|待定)'
        
        matches = re.findall(loose_pattern, content)
        
        for match in matches:
            name, date_str, apply_code, price_str = match
            
            # 提取股票代码
            code_match = re.search(r'(\d{6})', apply_code)
            if not code_match:
                continue
            
            code = code_match.group(1)
            
            stock = {
                'source': 'cfi_loose',
                'code': code,
                'name': name,
                'apply_date': self._parse_date(date_str),
                'issue_price': self._parse_price(price_str),
                'apply_code': apply_code,
                'market_type': self._infer_market_type(code, apply_code, name),
            }
            
            stocks.append(stock)
        
        return stocks
    
    def _parse_date(self, date_str: str) -> str:
        """解析日期"""
        # 示例: "03月20日周五" 或 "03月16日今天"
        
        date_match = re.search(r'(\d{1,2})月(\d{1,2})日', date_str)
        if date_match:
            month = date_match.group(1).zfill(2)
            day = date_match.group(2).zfill(2)
            year = datetime.now().year
            
            if '今天' in date_str:
                today = datetime.now()
                return today.strftime('%Y-%m-%d')
            
            return f"{year}-{month}-{day}"
        
        return ''
    
    def _parse_price(self, price_str: str):
        """解析价格"""
        if not price_str or price_str == '待定':
            return None
        
        try:
            return float(price_str)
        except:
            return None
    
    def _parse_issue_num(self, issue_num_str: str):
        """解析发行数量"""
        if not issue_num_str:
            return None
        
        try:
            # 处理单位
            if '亿' in issue_num_str:
                num = re.sub(r'[^\d.]', '', issue_num_str)
                return float(num) * 10000  # 亿转换为万股
            elif '万' in issue_num_str:
                num = re.sub(r'[^\d.]', '', issue_num_str)
                return float(num)
            else:
                num = re.sub(r'[^\d.]', '', issue_num_str)
                return float(num)
        except:
            return None
    
    def _parse_apply_limit(self, apply_limit_str: str):
        """解析申购限额"""
        if not apply_limit_str:
            return None
        
        try:
            if '万股' in apply_limit_str:
                num = re.sub(r'[^\d.]', '', apply_limit_str)
                return float(num) * 10000  # 转换为股
            elif '股' in apply_limit_str:
                num = re.sub(r'[^\d.]', '', apply_limit_str)
                return float(num)
            else:
                num = re.sub(r'[^\d.]', '', apply_limit_str)
                return float(num)
        except:
            return None
    
    def _infer_market_type(self, code: str, apply_code: str, name: str) -> str:
        """推断市场类型"""
        if code.startswith('30'):
            return '创业板'
        elif code.startswith('68'):
            return '科创板'
        elif code.startswith('00'):
            return '深市主板'
        elif code.startswith('60'):
            return '沪市主板'
        elif code.startswith('92'):
            return '北交所'
        
        if apply_code:
            if apply_code.startswith('沪:'):
                if '787' in apply_code:
                    return '科创板'
                else:
                    return '沪市主板'
            elif apply_code.startswith('深:'):
                if '300' in apply_code or '301' in apply_code:
                    return '创业板'
                else:
                    return '深市主板'
            elif apply_code.startswith('北:'):
                return '北交所'
        
        if '(科)' in name or '科创板' in name:
            return '科创板'
        elif '(创)' in name or '创业板' in name:
            return '创业板'
        elif '(北)' in name or '北交所' in name:
            return '北交所'
        
        return '未知'


# ========== 测试代码 ==========

if __name__ == "__main__":
    print("=" * 60)
    print("中财网新股数据简单解析器")
    print("=" * 60)
    
    try:
        parser = CFISimpleParser()
        
        print("\n1. 获取中财网新股数据...")
        stocks = parser.fetch_and_parse()
        
        if not stocks:
            print("❌ 未获取到新股数据")
        else:
            print(f"✅ 获取到 {len(stocks)} 只新股")
            
            print("\n2. 新股数据详情:")
            for i, stock in enumerate(stocks, 1):
                print(f"{i}. {stock['name']}({stock['code']})")
                print(f"   申购日期: {stock['apply_date']}")
                print(f"   发行价格: {stock['issue_price'] or '待定'}")
                print(f"   申购代码: {stock['apply_code']}")
                print(f"   市场类型: {stock['market_type']}")
                
                if stock.get('issue_num'):
                    print(f"   发行数量: {stock['issue_num']}万股")
                if stock.get('apply_limit'):
                    print(f"   申购限额: {stock['apply_limit']}股")
                
                print()
        
        print("\n" + "=" * 60)
        print("✅ 中财网数据解析完成")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ 解析失败: {e}")
        import traceback
        traceback.print_exc()