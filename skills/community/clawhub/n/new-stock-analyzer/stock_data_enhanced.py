#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
增强版新股数据获取模块
提供详细的市场分类、时间信息和价格数据
"""

import json
import logging
import re
from datetime import datetime
from typing import Dict, List, Optional
import requests

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class EnhancedStockDataFetcher:
    """增强版新股数据获取器"""
    
    def __init__(self, cache_dir: str = "data/cache"):
        self.cache_dir = cache_dir
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        })
    
    def get_today_detailed_stocks(self) -> List[Dict]:
        """
        获取今日详细新股数据（包含市场分类、时间信息、价格等）
        
        Returns:
            详细新股数据列表
        """
        today = datetime.now().strftime('%Y-%m-%d')
        logger.info(f"获取今日({today})详细新股数据")
        
        # 从东方财富获取数据
        stocks = self._fetch_from_eastmoney_detailed(today)
        
        if not stocks:
            logger.warning("今日无新股数据")
            return []
        
        # 不再过滤没有发行价格的数据（避免错过重要新股）
        valid_stocks = stocks
        
        if not valid_stocks:
            logger.info(f"今日({today})无新股数据")
            return []
        
        # 增强数据：添加市场分类、格式化信息等
        enhanced_stocks = []
        for stock in valid_stocks:
            enhanced_stock = self._enhance_stock_data(stock)
            enhanced_stocks.append(enhanced_stock)
        
        logger.info(f"获取到 {len(enhanced_stocks)} 只今日有效新股数据")
        return enhanced_stocks
    
    def _fetch_from_eastmoney_detailed(self, date: str) -> List[Dict]:
        """从东方财富获取详细数据"""
        cache_file = f"{self.cache_dir}/eastmoney_detailed_{date}.json"
        
        # 检查缓存
        try:
            if self._check_cache_valid(cache_file, minutes=5):
                with open(cache_file, 'r', encoding='utf-8') as f:
                    cached_data = json.load(f)
                    logger.info(f"使用详细缓存数据: {cache_file}")
                    return cached_data
        except (FileNotFoundError, json.JSONDecodeError):
            pass
        
        # 东方财富新股申购API
        url = "http://datacenter-web.eastmoney.com/api/data/v1/get"
        params = {
            'reportName': 'RPTA_APP_IPOAPPLY',
            'columns': 'ALL',
            'pageNumber': '1',
            'pageSize': '100',
            'sortColumns': 'APPLY_DATE',
            'sortTypes': '-1',
            'source': 'WEB',
            'client': 'WEB',
        }
        
        try:
            logger.info(f"请求东方财富详细API: {url}")
            response = self.session.get(url, params=params, timeout=15)
            response.raise_for_status()
            data = response.json()
            
            if data.get('success'):
                result = data.get('result', {})
                raw_data = result.get('data', [])
                
                stocks = self._parse_eastmoney_detailed(raw_data, date)
                
                # 缓存数据
                self._save_cache(cache_file, stocks)
                logger.info(f"从东方财富获取到 {len(stocks)} 条详细新股数据")
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
    
    def _parse_eastmoney_detailed(self, raw_data: List[Dict], target_date: str) -> List[Dict]:
        """解析东方财富详细数据"""
        stocks = []
        
        for item in raw_data:
            try:
                apply_date = item.get('APPLY_DATE', '')
                if not apply_date.startswith(target_date):
                    continue
                
                # 获取市场信息
                market_code = item.get('MARKET_TYPE', '')
                market_name = self._get_market_name(market_code)
                
                stock = {
                    # 基本信息
                    'code': item.get('SECURITY_CODE', ''),
                    'name': item.get('SECURITY_NAME', ''),  # 证券简称
                    'full_name': item.get('SECURITY_NAME_FULL', ''),  # 公司全称
                    'abbr_name': item.get('SECURITY_NAME_ABBR', ''),  # 证券简称缩写
                    
                    # 市场分类
                    'market_code': market_code,
                    'market': market_name,
                    'market_type': self._get_market_type(market_code),
                    'exchange': self._get_exchange(market_code),
                    
                    # 时间信息
                    'apply_date': apply_date.split()[0] if apply_date else '',  # 申购日期
                    'listing_date': item.get('LISTING_DATE', ''),  # 上市日期
                    'lottery_date': item.get('LOTTERY_DATE', ''),  # 中签公布日期
                    
                    # 价格信息
                    'issue_price': item.get('ISSUE_PRICE'),  # 发行价格
                    'issue_pe': item.get('AFTER_ISSUE_PE'),  # 发行市盈率
                    'industry_pe': item.get('INDUSTRY_PE'),  # 行业市盈率
                    
                    # 申购信息
                    'apply_code': item.get('APPLY_CODE', ''),  # 申购代码
                    'online_apply_upper': item.get('ONLINE_APPLY_UPPER'),  # 申购上限(股)
                    'top_apply_marketcap': item.get('TOP_APPLY_MARKETCAP'),  # 顶格申购市值(万元)
                    
                    # 发行信息
                    'issue_num': item.get('ISSUE_NUM'),  # 发行数量(万股)
                    'total_raise_funds': item.get('TOTAL_RAISE_FUNDS'),  # 募集资金(亿元)
                    
                    # 公司信息
                    'main_business': item.get('MAIN_BUSINESS', ''),  # 主营业务
                    'industry': item.get('INDUSTRY', ''),  # 所属行业
                    
                    # 机构信息
                    'recommend_org': item.get('RECOMMEND_ORG', ''),  # 保荐机构
                    
                    # 元数据
                    'data_source': 'eastmoney_detailed',
                    'fetch_time': datetime.now().isoformat(),
                }
                
                # 清理空值
                stock = {k: v for k, v in stock.items() if v not in [None, '', 'null', 'NULL']}
                stocks.append(stock)
                
            except (KeyError, AttributeError) as e:
                logger.warning(f"解析数据项失败: {e}")
                continue
        
        return stocks
    
    def _enhance_stock_data(self, stock: Dict) -> Dict:
        """增强股票数据：添加分类、格式化等"""
        enhanced = stock.copy()
        
        # 0. 首先根据股票代码推断市场（最准确）
        code = enhanced.get('code', '')
        inferred_market = self._infer_market_from_code(code)
        
        # 如果API返回的市场信息不准确，使用推断的市场
        if inferred_market != '未知' and enhanced.get('market') == '未知市场':
            enhanced['market'] = inferred_market
        
        # 1. 市场分类增强
        enhanced['market_category'] = self._get_market_category(enhanced.get('market', ''))
        enhanced['exchange_name'] = self._get_exchange_name(enhanced.get('exchange', ''))
        
        # 2. 时间信息格式化
        enhanced['apply_date_formatted'] = self._format_date(enhanced.get('apply_date'))
        enhanced['listing_date_formatted'] = self._format_date(enhanced.get('listing_date'))
        enhanced['lottery_date_formatted'] = self._format_date(enhanced.get('lottery_date'))
        
        # 3. 价格信息格式化
        enhanced['issue_price_formatted'] = self._format_price(enhanced.get('issue_price'))
        enhanced['total_raise_formatted'] = self._format_money(enhanced.get('total_raise_funds'), unit='亿元')
        
        # 4. 申购信息格式化
        enhanced['apply_upper_formatted'] = self._format_number(enhanced.get('online_apply_upper'), unit='股')
        enhanced['issue_num_formatted'] = self._format_number(enhanced.get('issue_num'), unit='万股')
        
        # 5. 添加状态标签
        enhanced['status'] = self._get_stock_status(enhanced)
        
        # 6. 添加投资提示
        enhanced['investment_tips'] = self._generate_investment_tips(enhanced)
        
        # 7. 添加显示名称（合并多个名称）
        enhanced['display_name'] = self._get_display_name(enhanced)
        
        return enhanced
    
    def _get_display_name(self, stock: Dict) -> str:
        """获取显示名称（合并多个名称）"""
        name = stock.get('name', '')
        full_name = stock.get('full_name', '')
        abbr_name = stock.get('abbr_name', '')
        
        # 如果全称和简称不同，都显示
        if full_name and full_name != name:
            return f"{name} ({full_name})"
        elif abbr_name and abbr_name != name:
            return f"{name} ({abbr_name})"
        else:
            return name
    
    def _get_market_name(self, market_code: str) -> str:
        """根据市场代码获取市场名称"""
        # API返回的是中文文本，不是数字代码
        market_mapping = {
            '001': '沪市主板',
            '002': '深市主板',
            '003': '创业板',
            '004': '科创板',
            '005': '北交所',
            '069': '科创板',
            '070': '创业板',
            '科创板': '科创板',
            '创业板': '创业板',
            '北交所': '北交所',
            '非科创板': '创业板',  # 非科创板通常是创业板
            '沪市主板': '沪市主板',
            '深市主板': '深市主板',
        }
        return market_mapping.get(market_code, market_code if market_code else '未知市场')
    
    def _get_market_type(self, market_code: str) -> str:
        """获取市场类型"""
        if market_code in ['001', '002']:
            return '主板'
        elif market_code in ['003', '070']:
            return '创业板'
        elif market_code in ['004', '069']:
            return '科创板'
        elif market_code == '005':
            return '北交所'
        else:
            return '其他'
    
    def _get_exchange(self, market_code: str) -> str:
        """获取交易所"""
        if market_code in ['001', '004', '069']:
            return '上交所'
        elif market_code in ['002', '003', '070']:
            return '深交所'
        elif market_code == '005':
            return '北交所'
        else:
            return '未知'
    
    def _infer_market_from_code(self, code: str) -> str:
        """根据股票代码推断市场（最准确的方法）"""
        if not code or len(code) < 6:
            return '未知'
        
        prefix = code[:3]
        if prefix.startswith('60'):
            return '沪市主板'
        elif prefix.startswith('00'):
            return '深市主板'
        elif prefix.startswith('30'):
            return '创业板'
        elif prefix.startswith('68'):
            return '科创板'
        elif prefix.startswith('43') or prefix.startswith('83') or prefix.startswith('87'):
            return '北交所'
        elif prefix.startswith('92'):
            return '北交所'  # 92开头也是北交所
        else:
            return '未知'
    
    def _get_market_category(self, market: str) -> str:
        """获取市场分类"""
        if '沪市' in market or '上交所' in market or '沪市主板' in market:
            return '沪市'
        elif '深市' in market or '深交所' in market or '深市主板' in market:
            return '深市'
        elif '创业' in market:
            return '创业板'
        elif '科创' in market:
            return '科创板'
        elif '北交' in market:
            return '北交所'
        else:
            # 尝试从市场名称推断
            market_lower = market.lower()
            if '创业' in market_lower:
                return '创业板'
            elif '科创' in market_lower:
                return '科创板'
            elif '北交' in market_lower:
                return '北交所'
            else:
                return '其他'
    
    def _get_exchange_name(self, exchange: str) -> str:
        """获取交易所全称"""
        exchange_map = {
            '上交所': '上海证券交易所',
            '深交所': '深圳证券交易所',
            '北交所': '北京证券交易所',
        }
        return exchange_map.get(exchange, exchange)
    
    def _format_date(self, date_str: str) -> str:
        """格式化日期"""
        if not date_str:
            return '待定'
        
        try:
            if len(date_str) == 8 and date_str.isdigit():
                return f"{date_str[:4]}-{date_str[4:6]}-{date_str[6:8]}"
            elif 'T' in date_str:
                return date_str.split('T')[0]
            else:
                return date_str
        except:
            return date_str
    
    def _format_price(self, price) -> str:
        """格式化价格"""
        if price is None:
            return '待定'
        
        try:
            price_float = float(price)
            return f"{price_float:.2f}元"
        except:
            return str(price)
    
    def _format_money(self, amount, unit: str = '亿元') -> str:
        """格式化金额"""
        if amount is None:
            return '待定'
        
        try:
            amount_float = float(amount)
            return f"{amount_float:.2f}{unit}"
        except:
            return f"{amount}{unit}"
    
    def _format_number(self, number, unit: str = '') -> str:
        """格式化数量"""
        if number is None:
            return '待定'
        
        try:
            num_float = float(number)
            return f"{num_float:.0f}{unit}"
        except:
            return f"{number}{unit}"
    
    def _get_stock_status(self, stock: Dict) -> str:
        """获取股票状态"""
        today = datetime.now().strftime('%Y-%m-%d')
        apply_date = stock.get('apply_date')
        
        if apply_date == today:
            return '今日申购'
        elif apply_date and apply_date > today:
            return '即将申购'
        elif apply_date and apply_date < today:
            return '申购结束'
        else:
            return '未知'
    
    def _generate_investment_tips(self, stock: Dict) -> List[str]:
        """生成投资提示"""
        tips = []
        
        # 市场类型提示
        market = stock.get('market', '')
        if '科创' in market or '创业' in market:
            tips.append('科创板/创业板新股波动较大')
        elif '北交' in market:
            tips.append('北交所新股门槛较高')
        
        # 价格提示
        issue_price = stock.get('issue_price')
        if issue_price:
            try:
                price = float(issue_price)
                if price > 50:
                    tips.append('高价股，机构参与为主')
                elif price < 20:
                    tips.append('低价股，散户参与度高')
            except:
                pass
        
        # 规模提示
        issue_num = stock.get('issue_num')
        if issue_num:
            try:
                num = float(issue_num)
                if num > 20000:
                    tips.append('发行规模较大')
                elif num < 5000:
                    tips.append('发行规模较小，稀缺性高')
            except:
                pass
        
        return tips
    
    def _check_cache_valid(self, cache_file: str, minutes: int = 5) -> bool:
        """检查缓存是否有效"""
        try:
            import os
            import time
            if not os.path.exists(cache_file):
                return False
            
            file_mtime = os.path.getmtime(cache_file)
            current_time = time.time()
            cache_age = current_time - file_mtime
            
            return cache_age < (minutes * 60)
            
        except Exception as e:
            logger.warning(f"检查缓存失败: {e}")
            return False
    
    def _save_cache(self, cache_file: str, data: any):
        """保存数据到缓存"""
        try:
            import os
            os.makedirs(os.path.dirname(cache_file), exist_ok=True)
            with open(cache_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.error(f"保存缓存失败: {e}")
    
    def get_recent_stocks(self, days: int = 7) -> List[Dict]:
        """
        获取近期新股数据（包括未来几天）
        
        Args:
            days: 查询天数，默认7天（包括今天和未来6天）
            
        Returns:
            近期新股数据列表
        """
        from datetime import datetime, timedelta
        
        all_stocks = []
        today = datetime.now()
        
        for i in range(days):
            date = (today + timedelta(days=i)).strftime('%Y-%m-%d')
            logger.info(f"获取{date}新股数据")
            
            stocks = self._fetch_from_eastmoney_detailed(date)
            if stocks:
                # 不再过滤没有发行价格的数据（避免错过重要新股）
                all_stocks.extend(stocks)
        
        # 增强数据
        enhanced_stocks = []
        for stock in all_stocks:
            enhanced_stock = self._enhance_stock_data(stock)
            enhanced_stocks.append(enhanced_stock)
        
        # 按申购日期排序
        enhanced_stocks.sort(key=lambda x: x.get('apply_date', ''))
        
        logger.info(f"获取到 {len(enhanced_stocks)} 只近期新股数据")
        return enhanced_stocks
    
    def get_market_summary(self) -> Dict:
        """获取市场汇总信息"""
        stocks = self.get_today_detailed_stocks()
        
        summary = {
            'total_count': len(stocks),
            'by_market': {},
            'by_exchange': {},
            'price_range': {'min': None, 'max': None, 'avg': None},
            'raise_total': 0,
        }
        
        prices = []
        
        for stock in stocks:
            # 按市场统计
            market = stock.get('market', '未知')
            summary['by_market'][market] = summary['by_market'].get(market, 0) + 1
            
            # 按交易所统计
            exchange = stock.get('exchange', '未知')
            summary['by_exchange'][exchange] = summary['by_exchange'].get(exchange, 0) + 1
            
            # 价格统计
            price = stock.get('issue_price')
            if price:
                try:
                    prices.append(float(price))
                except:
                    pass
            
            # 募集资金统计
            raise_funds = stock.get('total_raise_funds')
            if raise_funds:
                try:
                    summary['raise_total'] += float(raise_funds)
                except:
                    pass
        
        # 计算价格范围
        if prices:
            summary['price_range']['min'] = min(prices)
            summary['price_range']['max'] = max(prices)
            summary['price_range']['avg'] = sum(prices) / len(prices)
        
        return summary


# ========== 测试代码 ==========

if __name__ == "__main__":
    print("=" * 60)
    print("增强版新股数据获取器测试")
    print("=" * 60)
    
    try:
        fetcher = EnhancedStockDataFetcher()
        
        print("\n1. 获取今日详细新股数据...")
        stocks = fetcher.get_today_detailed_stocks()
        
        if not stocks:
            print("❌ 未获取到新股数据")
        else:
            print(f"✅ 获取到 {len(stocks)} 只新股")
            
            # 显示第一只股票的详细信息
            if stocks:
                stock = stocks[0]
                print(f"\n2. 示例股票详细数据:")
                print(f"   代码: {stock.get('code')}")
                print(f"   名称: {stock.get('name')}")
                print(f"   市场: {stock.get('market')} ({stock.get('market_category')})")
                print(f"   交易所: {stock.get('exchange_name')}")
                print(f"   申购日期: {stock.get('apply_date_formatted')}")
                print(f"   上市日期: {stock.get('listing_date_formatted')}")
                print(f"   发行价格: {stock.get('issue_price_formatted')}")
                print(f"   发行市盈率: {stock.get('issue_pe')}")
                print(f"   行业市盈率: {stock.get('industry_pe')}")
                print(f"   发行数量: {stock.get('issue_num_formatted')}")
                print(f"   募集资金: {stock.get('total_raise_formatted')}")
                print(f"   申购上限: {stock.get('apply_upper_formatted')}")
                print(f"   状态: {stock.get('status')}")
                
                if stock.get('investment_tips'):
                    print(f"   投资提示: {', '.join(stock['investment_tips'])}")
        
        print("\n3. 市场汇总信息:")
        summary = fetcher.get_market_summary()
        print(f"   新股总数: {summary['total_count']}只")
        print(f"   募集资金总额: {summary['raise_total']:.2f}亿元")
        
        if summary['by_market']:
            print("   市场分布:")
            for market, count in summary['by_market'].items():
                print(f"     {market}: {count}只")
        
        print("\n" + "=" * 60)
        print("✅ 增强版数据获取器测试完成")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()