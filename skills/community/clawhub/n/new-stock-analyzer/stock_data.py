#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
新股数据获取模块
支持多数据源：东方财富（主）、同花顺（备）
"""

import json
import time
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import requests
from bs4 import BeautifulSoup

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class StockDataFetcher:
    """新股数据获取器"""
    
    def __init__(self, cache_dir: str = "data/cache"):
        self.cache_dir = cache_dir
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        })
    
    def fetch_from_eastmoney(self, date: str = None) -> List[Dict]:
        """
        从东方财富获取新股数据
        
        Args:
            date: 查询日期，格式YYYY-MM-DD，默认今日
            
        Returns:
            新股数据列表
        """
        if date is None:
            date = datetime.now().strftime('%Y-%m-%d')
        
        cache_file = f"{self.cache_dir}/eastmoney_{date}.json"
        
        # 检查缓存（5分钟内有效）
        try:
            if self._check_cache_valid(cache_file, minutes=5):
                with open(cache_file, 'r', encoding='utf-8') as f:
                    cached_data = json.load(f)
                    logger.info(f"使用缓存数据: {cache_file}")
                    return cached_data
        except (FileNotFoundError, json.JSONDecodeError):
            pass
        
        url = "http://datacenter-web.eastmoney.com/api/data/v1/get"
        params = {
            'reportName': 'RPTA_APP_IPOAPPLY',
            'columns': 'ALL',
            'pageNum': 1,
            'pageSize': 100,
            'sortColumns': 'APPLY_DATE',
            'sortTypes': '-1',
            # 移除filter参数，获取全部数据后在代码中过滤
        }
        
        headers = {
            'Referer': 'http://data.eastmoney.com/xg/xg/default.html',
        }
        
        try:
            logger.info(f"请求东方财富API: {url}")
            # 增加超时时间，添加重试机制
            for attempt in range(3):  # 重试3次
                try:
                    response = self.session.get(url, params=params, headers=headers, timeout=15)
                    response.raise_for_status()
                    break  # 成功则跳出重试循环
                except requests.exceptions.Timeout:
                    if attempt < 2:  # 前两次重试
                        logger.warning(f"API请求超时，第{attempt+1}次重试...")
                        import time
                        time.sleep(2)  # 等待2秒后重试
                    else:
                        raise  # 最后一次失败则抛出异常
            
            data = response.json()
            if data.get('success'):
                stocks = self._parse_eastmoney_data(data['result']['data'], date)
                
                # 缓存数据
                self._save_cache(cache_file, stocks)
                logger.info(f"从东方财富获取到 {len(stocks)} 条新股数据")
                return stocks
            else:
                logger.error(f"东方财富API返回错误: {data.get('message')}")
                return []
                
        except requests.RequestException as e:
            logger.error(f"东方财富API请求失败: {e}")
            return []
        except (KeyError, ValueError) as e:
            logger.error(f"东方财富数据解析失败: {e}")
            return []
    
    def fetch_from_ths(self, date: str = None) -> List[Dict]:
        """
        从同花顺获取新股数据（备用数据源）
        
        Args:
            date: 查询日期，格式YYYY-MM-DD，默认今日
            
        Returns:
            新股数据列表
        """
        if date is None:
            date = datetime.now().strftime('%Y-%m-%d')
        
        cache_file = f"{self.cache_dir}/ths_{date}.json"
        
        # 检查缓存
        try:
            if self._check_cache_valid(cache_file, minutes=5):
                with open(cache_file, 'r', encoding='utf-8') as f:
                    cached_data = json.load(f)
                    logger.info(f"使用同花顺缓存数据: {cache_file}")
                    return cached_data
        except (FileNotFoundError, json.JSONDecodeError):
            pass
        
        # 同花顺新股中心页面
        url = "http://data.10jqka.com.cn/ipo/xgsgyzq/"
        
        try:
            logger.info(f"请求同花顺页面: {url}")
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            stocks = self._parse_ths_data(soup, date)
            
            # 缓存数据
            self._save_cache(cache_file, stocks)
            logger.info(f"从同花顺获取到 {len(stocks)} 条新股数据")
            return stocks
            
        except requests.RequestException as e:
            logger.error(f"同花顺请求失败: {e}")
            return []
        except Exception as e:
            logger.error(f"同花顺数据解析失败: {e}")
            return []
    
    def get_today_new_stocks(self) -> List[Dict]:
        """
        获取今日可申购新股（主备数据源合并）
        
        Returns:
            今日新股列表
        """
        today = datetime.now().strftime('%Y-%m-%d')
        logger.info(f"获取今日({today})新股数据")
        
        # 优先使用东方财富数据
        eastmoney_stocks = self.fetch_from_eastmoney(today)
        
        if eastmoney_stocks:
            return eastmoney_stocks
        
        # 东方财富失败时使用同花顺
        logger.warning("东方财富数据获取失败，尝试同花顺")
        ths_stocks = self.fetch_from_ths(today)
        
        if ths_stocks:
            return ths_stocks
        
        logger.error("所有数据源均失败")
        return []
    
    def get_week_new_stocks(self) -> List[Dict]:
        """
        获取本周可申购新股
        
        Returns:
            本周新股列表
        """
        today = datetime.now()
        week_stocks = []
        
        for i in range(7):  # 未来7天
            date = (today + timedelta(days=i)).strftime('%Y-%m-%d')
            stocks = self.fetch_from_eastmoney(date)
            week_stocks.extend(stocks)
        
        # 按申购日期排序
        week_stocks.sort(key=lambda x: x.get('apply_date', ''))
        return week_stocks
    
    def _parse_eastmoney_data(self, raw_data: List[Dict], target_date: str) -> List[Dict]:
        """解析东方财富数据"""
        stocks = []
        
        for item in raw_data:
            try:
                apply_date = item.get('APPLY_DATE', '')
                if not apply_date.startswith(target_date):
                    continue
                
                stock = {
                    'code': item.get('SECURITY_CODE', ''),
                    'name': item.get('SECURITY_NAME', ''),
                    'apply_code': item.get('APPLY_CODE', ''),
                    'apply_date': apply_date.split()[0] if apply_date else '',
                    'listing_date': item.get('LISTING_DATE', ''),
                    'issue_price': item.get('ISSUE_PRICE'),
                    'predict_issue_price': item.get('PREDICT_ISSUE_PRICE'),
                    'issue_pe': item.get('AFTER_ISSUE_PE'),
                    'industry_pe': item.get('INDUSTRY_PE'),
                    'online_apply_upper': item.get('ONLINE_APPLY_UPPER'),  # 申购上限(股)
                    'top_apply_marketcap': item.get('TOP_APPLY_MARKETCAP'),  # 顶格申购市值(万元)
                    'market': item.get('MARKET', ''),
                    'main_business': item.get('MAIN_BUSINESS', ''),
                    'recommend_org': item.get('RECOMMEND_ORG', ''),  # 保荐机构
                    'underwriter_org': item.get('UNDERWRITER_ORG', ''),  # 主承销商
                    'issue_num': item.get('ISSUE_NUM'),  # 发行数量(万股)
                    'total_raise_funds': item.get('TOTAL_RAISE_FUNDS'),  # 募集资金(亿元)
                    'data_source': 'eastmoney',
                    'fetch_time': datetime.now().isoformat(),
                }
                
                # 清理空值
                stock = {k: v for k, v in stock.items() if v not in [None, '', 'null']}
                stocks.append(stock)
                
            except (KeyError, AttributeError) as e:
                logger.warning(f"解析东方财富数据项失败: {e}")
                continue
        
        return stocks
    
    def _parse_ths_data(self, soup: BeautifulSoup, target_date: str) -> List[Dict]:
        """解析同花顺数据（简化版）"""
        stocks = []
        
        # 同花顺页面结构可能变化，这里提供基本解析逻辑
        # 实际使用时需要根据页面结构调整
        
        try:
            # 查找新股表格
            tables = soup.find_all('table', class_='m-table')
            for table in tables:
                rows = table.find_all('tr')[1:]  # 跳过表头
                for row in rows:
                    cols = row.find_all('td')
                    if len(cols) >= 6:
                        stock = {
                            'code': cols[0].text.strip(),
                            'name': cols[1].text.strip(),
                            'apply_date': target_date,
                            'issue_price': self._parse_price(cols[2].text.strip()),
                            'apply_upper': self._parse_number(cols[3].text.strip()),
                            'market': cols[4].text.strip(),
                            'data_source': 'ths',
                            'fetch_time': datetime.now().isoformat(),
                        }
                        stocks.append(stock)
        except Exception as e:
            logger.error(f"解析同花顺表格失败: {e}")
        
        return stocks
    
    def _parse_price(self, text: str) -> Optional[float]:
        """解析价格文本"""
        try:
            # 移除非数字字符
            import re
            clean = re.sub(r'[^\d.]', '', text)
            return float(clean) if clean else None
        except:
            return None
    
    def _parse_number(self, text: str) -> Optional[int]:
        """解析数量文本"""
        try:
            import re
            clean = re.sub(r'[^\d]', '', text)
            return int(clean) if clean else None
        except:
            return None
    
    def _check_cache_valid(self, cache_file: str, minutes: int = 5) -> bool:
        """检查缓存是否有效"""
        try:
            import os
            from datetime import datetime, timedelta
            
            if not os.path.exists(cache_file):
                return False
            
            mtime = datetime.fromtimestamp(os.path.getmtime(cache_file))
            expire_time = mtime + timedelta(minutes=minutes)
            
            return datetime.now() < expire_time
        except:
            return False
    
    def _save_cache(self, cache_file: str, data: List[Dict]):
        """保存数据到缓存"""
        try:
            import os
            os.makedirs(os.path.dirname(cache_file), exist_ok=True)
            
            with open(cache_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.warning(f"缓存保存失败: {e}")


# 单例实例
fetcher = StockDataFetcher()


if __name__ == "__main__":
    # 测试代码
    print("测试数据获取模块...")
    
    # 测试今日新股
    today_stocks = fetcher.get_today_new_stocks()
    print(f"今日新股数量: {len(today_stocks)}")
    
    for stock in today_stocks[:3]:  # 显示前3只
        print(f"{stock.get('name')} ({stock.get('code')}) - 申购上限: {stock.get('online_apply_upper')}股")