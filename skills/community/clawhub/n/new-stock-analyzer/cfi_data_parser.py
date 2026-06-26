#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
中财网(CFI)新股数据解析器
专门解析 https://newstock.cfi.cn/ 的新股数据
"""

import re
import logging
from datetime import datetime
from typing import Dict, List, Optional
import requests
from bs4 import BeautifulSoup

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class CFIDataParser:
    """中财网新股数据解析器"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Referer': 'https://www.cfi.cn/',
        })
        
        self.base_url = 'https://newstock.cfi.cn/'
    
    def fetch_new_stocks(self) -> List[Dict]:
        """获取中财网新股数据"""
        try:
            logger.info(f"访问中财网新股页面: {self.base_url}")
            response = self.session.get(self.base_url, timeout=15)
            response.raise_for_status()
            
            logger.info(f"页面获取成功，长度: {len(response.text)} 字符")
            
            # 解析页面
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 查找新股表格
            stocks = self._parse_new_stock_table(soup)
            
            # 如果没有找到，尝试其他解析方法
            if not stocks:
                stocks = self._parse_new_stocks_from_text(soup)
            
            logger.info(f"从中财网解析到 {len(stocks)} 只新股")
            return stocks
            
        except Exception as e:
            logger.error(f"中财网数据获取失败: {e}")
            return []
    
    def _parse_new_stock_table(self, soup: BeautifulSoup) -> List[Dict]:
        """解析新股表格"""
        stocks = []
        
        # 查找包含"即将发行的新股"的文本
        ipo_section = soup.find(string=re.compile(r'即将发行的新股'))
        if not ipo_section:
            logger.warning("未找到'即将发行的新股'部分")
            return []
        
        # 找到包含新股数据的表格
        table = None
        parent = ipo_section.parent
        
        # 向上查找表格
        for _ in range(5):
            if parent.name == 'table':
                table = parent
                break
            parent = parent.parent
        
        if not table:
            # 向下查找表格
            parent = ipo_section.parent
            for sibling in parent.find_next_siblings():
                if sibling.name == 'table':
                    table = sibling
                    break
        
        if not table:
            logger.warning("未找到新股表格")
            return []
        
        # 解析表格行
        rows = table.find_all('tr')
        logger.info(f"找到新股表格，行数: {len(rows)}")
        
        # 查找表头，确定列索引
        header_row = None
        for row in rows:
            cells = row.find_all(['td', 'th'])
            cell_texts = [cell.get_text(strip=True) for cell in cells]
            
            # 检查是否包含新股表头关键词
            header_keywords = ['股票名称', '新股申购日', '申购代码', '发行价']
            keyword_count = sum(1 for keyword in header_keywords if any(keyword in text for text in cell_texts))
            
            if keyword_count >= 2:
                header_row = cell_texts
                break
        
        if not header_row:
            logger.warning("未找到新股表头")
            return []
        
        logger.info(f"表头: {header_row}")
        
        # 确定各列索引
        col_indices = {}
        for i, header in enumerate(header_row):
            if '股票名称' in header:
                col_indices['name'] = i
            elif '新股申购日' in header or '申购日期' in header:
                col_indices['apply_date'] = i
            elif '申购代码' in header:
                col_indices['apply_code'] = i
            elif '发行价' in header or '发行价格' in header:
                col_indices['issue_price'] = i
            elif '发行量' in header or '发行量/股' in header:
                col_indices['issue_num'] = i
            elif '申购限额' in header:
                col_indices['apply_limit'] = i
        
        # 解析数据行
        for row in rows:
            cells = row.find_all(['td', 'th'])
            if len(cells) < 4:  # 至少需要4列数据
                continue
            
            cell_texts = [cell.get_text(strip=True) for cell in cells]
            
            # 跳过表头行
            if any(keyword in ' '.join(cell_texts) for keyword in ['股票名称', '新股申购日', '申购代码']):
                continue
            
            # 尝试解析股票数据
            stock = self._parse_stock_from_row(cell_texts, col_indices)
            if stock:
                stocks.append(stock)
        
        return stocks
    
    def _parse_stock_from_row(self, row_data: List[str], col_indices: Dict) -> Optional[Dict]:
        """从表格行解析股票数据"""
        try:
            # 提取股票名称和代码
            name_cell = row_data[col_indices.get('name', 0)] if col_indices.get('name') is not None else row_data[0]
            
            # 从名称中提取股票代码和名称
            name, code = self._extract_name_and_code(name_cell)
            if not name or not code:
                return None
            
            # 提取申购日期
            apply_date_cell = row_data[col_indices.get('apply_date', 1)] if col_indices.get('apply_date') is not None else row_data[1]
            apply_date = self._parse_apply_date(apply_date_cell)
            
            # 提取发行价格
            price_cell = row_data[col_indices.get('issue_price', 3)] if col_indices.get('issue_price') is not None else row_data[3]
            issue_price = self._parse_price(price_cell)
            
            # 提取申购代码
            apply_code_cell = row_data[col_indices.get('apply_code', 2)] if col_indices.get('apply_code') is not None else row_data[2]
            apply_code = self._parse_apply_code(apply_code_cell)
            
            # 提取发行数量
            issue_num_cell = row_data[col_indices.get('issue_num', 4)] if col_indices.get('issue_num') is not None else row_data[4]
            issue_num = self._parse_issue_num(issue_num_cell)
            
            # 提取申购限额
            apply_limit_cell = row_data[col_indices.get('apply_limit', 5)] if col_indices.get('apply_limit') is not None else row_data[5]
            apply_limit = self._parse_apply_limit(apply_limit_cell)
            
            # 推断市场类型
            market_type = self._infer_market_type(code, apply_code, name)
            
            stock = {
                'source': 'cfi',
                'code': code,
                'name': name,
                'apply_date': apply_date,
                'issue_price': issue_price,
                'apply_code': apply_code,
                'issue_num': issue_num,
                'apply_limit': apply_limit,
                'market_type': market_type,
                'raw_data': row_data,
            }
            
            return stock
            
        except Exception as e:
            logger.debug(f"解析行数据失败: {e}, 数据: {row_data}")
            return None
    
    def _extract_name_and_code(self, text: str) -> tuple:
        """从文本中提取股票名称和代码"""
        # 示例: "泰金新能(科)" 或 "宏明电子(创)" 或 "盛龙股份"
        
        # 先尝试提取代码
        code_match = re.search(r'[036]\d{5}', text)
        if code_match:
            code = code_match.group()
            # 从文本中移除代码得到名称
            name = re.sub(r'\([^)]*\)', '', text)  # 移除括号内容
            name = re.sub(r'[036]\d{5}', '', name)  # 移除代码
            name = name.strip()
            return name, code
        
        # 如果没有代码，尝试从申购代码推断
        return None, None
    
    def _parse_apply_date(self, text: str) -> str:
        """解析申购日期"""
        # 示例: "03月20日周五" 或 "03月16日今天"
        
        # 提取月份和日期
        date_match = re.search(r'(\d{1,2})月(\d{1,2})日', text)
        if date_match:
            month = date_match.group(1).zfill(2)
            day = date_match.group(2).zfill(2)
            year = datetime.now().year
            
            # 如果是"今天"，使用当前日期
            if '今天' in text:
                today = datetime.now()
                return today.strftime('%Y-%m-%d')
            
            return f"{year}-{month}-{day}"
        
        return ''
    
    def _parse_price(self, text: str) -> Optional[float]:
        """解析发行价格"""
        if not text or text == '待定' or text == '--':
            return None
        
        try:
            # 移除非数字字符
            price_text = re.sub(r'[^\d.]', '', text)
            if price_text:
                return float(price_text)
        except:
            pass
        
        return None
    
    def _parse_apply_code(self, text: str) -> str:
        """解析申购代码"""
        # 示例: "沪:787813" 或 "深:301683" 或 "北:920188"
        return text.strip()
    
    def _parse_issue_num(self, text: str) -> Optional[float]:
        """解析发行数量"""
        if not text or text == '--':
            return None
        
        try:
            # 处理单位: 万、亿
            if '亿' in text:
                num_text = re.sub(r'[^\d.]', '', text)
                return float(num_text) * 10000  # 转换为万股
            elif '万' in text:
                num_text = re.sub(r'[^\d.]', '', text)
                return float(num_text)
            else:
                # 假设是万股
                num_text = re.sub(r'[^\d.]', '', text)
                return float(num_text)
        except:
            return None
    
    def _parse_apply_limit(self, text: str) -> Optional[float]:
        """解析申购限额"""
        if not text or text == '--':
            return None
        
        try:
            # 处理单位: 万股
            if '万股' in text:
                num_text = re.sub(r'[^\d.]', '', text)
                return float(num_text) * 10000  # 转换为股
            elif '股' in text:
                num_text = re.sub(r'[^\d.]', '', text)
                return float(num_text)
        except:
            return None
    
    def _infer_market_type(self, code: str, apply_code: str, name: str) -> str:
        """推断市场类型"""
        # 根据代码前缀判断
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
        
        # 根据申购代码判断
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
        
        # 根据名称判断
        if '(科)' in name or '科创板' in name:
            return '科创板'
        elif '(创)' in name or '创业板' in name:
            return '创业板'
        elif '(北)' in name or '北交所' in name:
            return '北交所'
        
        return '未知'
    
    def _parse_new_stocks_from_text(self, soup: BeautifulSoup) -> List[Dict]:
        """从页面文本中解析新股数据（备用方法）"""
        stocks = []
        
        # 查找包含新股数据的文本块
        ipo_text_blocks = soup.find_all(string=re.compile(r'泰金新能|慧谷新材|盛龙股份|视涯科技|宏明电子|悦龙科技'))
        
        for text_block in ipo_text_blocks:
            # 提取周围的文本进行分析
            context = text_block
            for _ in range(3):
                context = str(context.parent)
            
            # 使用正则表达式提取新股信息
            ipo_pattern = r'([\u4e00-\u9fa5]+(?:\([科创北]\))?)\s+(\d{1,2}月\d{1,2}日[周今]*)\s+([沪深北]:[\d]+)\s+([\d.]+|待定)'
            matches = re.findall(ipo_pattern, context)
            
            for match in matches:
                name, date_str, apply_code, price_str = match
                
                # 提取股票代码
                code_match = re.search(r'(\d{6})', apply_code)
                code = code_match.group(1) if code_match else ''
                
                if code:
                    stock = {
                        'source': 'cfi_text',
                        'code': code,
                        'name': name,
                        'apply_date': self._parse_apply_date(date_str),
                        'issue_price': self._parse_price(price_str),
                        'apply_code': apply_code,
                        'market_type': self._infer_market_type(code, apply_code, name),
                    }
                    stocks.append(stock)
        
        return stocks
    
    def get_today_and_future_stocks(self) -> List[Dict]:
        """获取今天及未来的新股"""
        all_stocks = self.fetch_new_stocks()
        
        if not all_stocks:
            return []
        
        today = datetime.now().strftime('%Y-%m-%d')
        future_stocks = []
        
        for stock in all_stocks:
            apply_date = stock.get('apply_date', '')
            
            # 只保留今天及未来的股票
            if apply_date >= today:
                future_stocks.append(stock)
        
        # 按申购日期排序
        future_stocks.sort(key=lambda x: x.get('apply_date', ''))
        
        logger.info(f"获取到 {len(future_stocks)} 只今天及未来新股")
        return future_stocks


# ========== 测试代码 ==========

if __name__ == "__main__":
    print("=" * 60)
    print("中财网(CFI)新股数据解析器")
    print("=" * 60)
    
    try:
        parser = CFIDataParser()
        
        print("\n1. 获取中财网新股数据...")
        stocks = parser.get_today_and_future_stocks()
        
        if not stocks:
            print("❌ 未获取到新股数据")
        else:
            print(f"✅ 获取到 {len(stocks)} 只新股")
            
            print("\n2. 新股数据详情:")
            for i, stock in enumerate(stocks, 1):
                print(f"{i}. {stock.get('name', '未知')}({stock.get('code', '未知')})")
                print(f"   申购日期: {stock.get('apply_date', '未知')}")
                print(f"   发行价格: {stock.get('issue_price', '未知') or '待定'}")
                print(f"   申购代码: {stock.get('apply_code', '未知')}")
                print(f"   市场类型: {stock.get('market_type', '未知')}")
                
                if stock.get('issue_num'):
                    print(f"   发行数量: {stock.get('issue_num')}万股")
                if stock.get('apply_limit'):
                    print(f"   申购限额: {stock.get('apply_limit')}股")
                
                print()
        
        print("\n3. 与东方财富数据对比:")
        print("   需要结合东方财富数据进行交叉验证")
        
        print("\n" + "=" * 60)
        print("✅ 中财网数据解析完成")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ 解析失败: {e}")
        import traceback
        traceback.print_exc()