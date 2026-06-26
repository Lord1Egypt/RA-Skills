#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
多数据源新股数据验证器
使用东方财富、同花顺等多个数据源交叉验证新股数据准确性
"""

import json
import time
import logging
import re
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import requests
from bs4 import BeautifulSoup

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class MultiSourceValidator:
    """多数据源验证器"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'application/json, text/html, */*',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Referer': 'https://data.eastmoney.com/',
        })
        
        # 数据源配置（专注于即将申购的新股）
        self.data_sources = {
            'eastmoney': {
                'name': '东方财富-新股申购',
                'priority': 1,
                'enabled': True,
            },
            'cfi': {
                'name': '中财网-新股页面',
                'priority': 2,
                'enabled': True,
            },
        }
    
    def fetch_from_eastmoney(self) -> List[Dict]:
        """从东方财富获取新股数据（主数据源）"""
        try:
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
            
            logger.info("请求东方财富API...")
            response = self.session.get(url, params=params, timeout=15)
            response.raise_for_status()
            
            data = response.json()
            if not data.get('success'):
                logger.error(f"东方财富API返回失败: {data.get('message')}")
                return []
            
            raw_data = data.get('result', {}).get('data', [])
            logger.info(f"从东方财富获取到 {len(raw_data)} 条新股数据")
            
            # 解析数据
            stocks = []
            today = datetime.now().strftime('%Y-%m-%d')
            
            for item in raw_data:
                try:
                    apply_date = item.get('APPLY_DATE', '')
                    if not apply_date:
                        continue
                    
                    # 只获取今天及未来的数据
                    apply_date_str = apply_date[:10]
                    if apply_date_str < today:
                        continue
                    
                    stock = {
                        'source': 'eastmoney',
                        'code': item.get('SECURITY_CODE', ''),
                        'name': item.get('SECURITY_NAME', ''),
                        'full_name': item.get('SECURITY_NAME_FULL', ''),
                        'apply_date': apply_date_str,
                        'issue_price': item.get('ISSUE_PRICE'),
                        'market_type': item.get('MARKET_TYPE', ''),
                        'issue_num': item.get('ISSUE_NUM'),
                        'total_raise': item.get('TOTAL_RAISE_FUNDS'),
                        'industry_pe': item.get('INDUSTRY_PE'),
                        'apply_code': item.get('APPLY_CODE', ''),
                        'online_apply_upper': item.get('ONLINE_APPLY_UPPER'),
                        'listing_date': item.get('LISTING_DATE', ''),
                        'lottery_date': item.get('LOTTERY_DATE', ''),
                    }
                    
                    stocks.append(stock)
                    
                except Exception as e:
                    logger.warning(f"解析东方财富数据失败: {e}")
                    continue
            
            return stocks
            
        except Exception as e:
            logger.error(f"东方财富数据获取失败: {e}")
            return []
    
    def fetch_from_sina(self) -> List[Dict]:
        """从新浪财经获取新股数据"""
        try:
            # 新浪财经新股数据API
            url = "https://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/Market_Center.getHQNodeData"
            params = {
                'page': '1',
                'num': '100',
                'sort': 'symbol',
                'asc': '1',
                'node': 'new_stock',
            }
            
            logger.info("请求新浪财经API...")
            response = self.session.get(url, params=params, timeout=15)
            response.raise_for_status()
            
            # 新浪返回的是JSONP格式，需要提取JSON
            content = response.text
            if content.startswith('(') and content.endswith(')'):
                content = content[1:-1]
            
            try:
                data = json.loads(content)
                logger.info(f"从新浪财经获取到 {len(data)} 条新股数据")
                
                stocks = []
                today = datetime.now().strftime('%Y-%m-%d')
                
                for item in data:
                    try:
                        # 新浪数据字段可能不同，需要适配
                        stock = {
                            'source': 'sina',
                            'code': item.get('symbol', '').replace('sh', '').replace('sz', ''),
                            'name': item.get('name', ''),
                            'apply_date': today,  # 新浪可能不提供申购日期
                            'issue_price': item.get('open'),  # 可能用开盘价代替发行价
                            'market_type': self._infer_market_from_code(item.get('symbol', '')),
                        }
                        
                        stocks.append(stock)
                        
                    except Exception as e:
                        logger.warning(f"解析新浪数据失败: {e}")
                        continue
                
                return stocks
                
            except json.JSONDecodeError:
                logger.error("新浪财经数据格式错误")
                return []
            
        except Exception as e:
            logger.error(f"新浪财经数据获取失败: {e}")
            return []
    
    def fetch_from_cfi(self) -> List[Dict]:
        """从中财网获取新股数据"""
        try:
            from cfi_simple_parser import CFISimpleParser
            
            logger.info("请求中财网新股数据...")
            parser = CFISimpleParser()
            stocks = parser.fetch_and_parse()
            
            logger.info(f"从中财网获取到 {len(stocks)} 只新股")
            return stocks
            
        except Exception as e:
            logger.error(f"中财网数据获取失败: {e}")
            return []
    
    def _infer_market_from_code(self, code: str) -> str:
        """根据股票代码推断市场"""
        if not code:
            return '未知'
        
        code_str = str(code)
        if code_str.startswith('30'):
            return '创业板'
        elif code_str.startswith('68'):
            return '科创板'
        elif code_str.startswith('00'):
            return '深市主板'
        elif code_str.startswith('60'):
            return '沪市主板'
        elif code_str.startswith('43') or code_str.startswith('83') or code_str.startswith('87') or code_str.startswith('92'):
            return '北交所'
        else:
            return '未知'
    
    def fetch_all_sources(self) -> Dict[str, List[Dict]]:
        """从所有数据源获取数据"""
        results = {}
        
        # 东方财富（主数据源）
        if self.data_sources['eastmoney']['enabled']:
            eastmoney_data = self.fetch_from_eastmoney()
            results['eastmoney'] = eastmoney_data
            logger.info(f"东方财富: {len(eastmoney_data)} 只新股")
        
        # 中财网（验证数据源）
        if self.data_sources['cfi']['enabled']:
            cfi_data = self.fetch_from_cfi()
            results['cfi'] = cfi_data
            logger.info(f"中财网: {len(cfi_data)} 只新股")
        
        return results
    
    def compare_data_sources(self, data_by_source: Dict[str, List[Dict]]) -> Dict:
        """比较不同数据源的数据"""
        comparison = {
            'total_by_source': {},
            'common_stocks': [],
            'unique_by_source': {},
            'conflicts': [],
            'summary': {},
        }
        
        # 统计各数据源数量
        for source, stocks in data_by_source.items():
            comparison['total_by_source'][source] = len(stocks)
        
        # 如果没有至少两个数据源，无法比较
        if len(data_by_source) < 2:
            logger.warning("数据源不足，无法进行有效比较")
            return comparison
        
        # 提取股票代码集合
        stock_sets = {}
        for source, stocks in data_by_source.items():
            codes = set()
            for stock in stocks:
                code = stock.get('code')
                if code:
                    codes.add(code)
            stock_sets[source] = codes
        
        # 找出共同股票
        all_codes = set()
        for codes in stock_sets.values():
            all_codes.update(codes)
        
        common_codes = set.intersection(*stock_sets.values()) if stock_sets else set()
        comparison['common_stocks'] = list(common_codes)
        
        # 找出各数据源独有的股票
        for source, codes in stock_sets.items():
            other_codes = set()
            for other_source, other_codes_set in stock_sets.items():
                if other_source != source:
                    other_codes.update(other_codes_set)
            
            unique_codes = codes - other_codes
            comparison['unique_by_source'][source] = list(unique_codes)
        
        # 检查数据冲突（同一股票在不同数据源信息不一致）
        for code in common_codes:
            stock_info_by_source = {}
            
            for source, stocks in data_by_source.items():
                for stock in stocks:
                    if stock.get('code') == code:
                        stock_info_by_source[source] = stock
                        break
            
            # 比较关键信息
            if len(stock_info_by_source) >= 2:
                conflicts = self._check_stock_conflicts(code, stock_info_by_source)
                if conflicts:
                    comparison['conflicts'].append({
                        'code': code,
                        'conflicts': conflicts,
                        'info_by_source': stock_info_by_source,
                    })
        
        # 生成摘要
        comparison['summary'] = {
            'total_sources': len(data_by_source),
            'total_unique_stocks': len(all_codes),
            'common_stocks_count': len(common_codes),
            'consistency_rate': len(common_codes) / len(all_codes) * 100 if all_codes else 0,
            'data_quality': self._assess_data_quality(comparison),
        }
        
        return comparison
    
    def _check_stock_conflicts(self, code: str, stock_info_by_source: Dict[str, Dict]) -> List[str]:
        """检查股票信息冲突"""
        conflicts = []
        
        # 收集所有数据源的信息
        names = set()
        prices = set()
        apply_dates = set()
        
        for source, info in stock_info_by_source.items():
            name = info.get('name')
            price = info.get('issue_price')
            apply_date = info.get('apply_date')
            
            if name:
                names.add(name)
            if price:
                prices.add(str(price))
            if apply_date:
                apply_dates.add(apply_date)
        
        # 检查冲突
        if len(names) > 1:
            conflicts.append(f"名称不一致: {', '.join(names)}")
        
        if len(prices) > 1:
            conflicts.append(f"价格不一致: {', '.join(prices)}")
        
        if len(apply_dates) > 1:
            conflicts.append(f"申购日期不一致: {', '.join(apply_dates)}")
        
        return conflicts
    
    def _assess_data_quality(self, comparison: Dict) -> str:
        """评估数据质量"""
        summary = comparison.get('summary', {})
        consistency = summary.get('consistency_rate', 0)
        
        if consistency >= 80:
            return '优秀'
        elif consistency >= 60:
            return '良好'
        elif consistency >= 40:
            return '一般'
        else:
            return '较差'
    
    def get_recommended_data(self, data_by_source: Dict[str, List[Dict]], comparison: Dict) -> List[Dict]:
        """获取推荐数据（基于数据源比较）"""
        recommended = []
        
        # 优先使用东方财富数据（主数据源）
        eastmoney_data = data_by_source.get('eastmoney', [])
        
        if not eastmoney_data:
            logger.warning("东方财富无数据，尝试使用其他数据源")
            # 使用第一个有数据的数据源
            for source, data in data_by_source.items():
                if data:
                    return data
            return []
        
        # 如果有数据冲突，进行标记
        conflicts_by_code = {}
        for conflict in comparison.get('conflicts', []):
            code = conflict['code']
            conflicts_by_code[code] = conflict['conflicts']
        
        # 处理推荐数据
        for stock in eastmoney_data:
            code = stock.get('code')
            
            # 复制股票数据
            recommended_stock = stock.copy()
            
            # 添加数据质量标记
            if code in conflicts_by_code:
                recommended_stock['data_quality'] = '有冲突'
                recommended_stock['conflicts'] = conflicts_by_code[code]
            else:
                # 检查是否在其他数据源也存在
                in_other_sources = False
                for source, data in data_by_source.items():
                    if source != 'eastmoney':
                        for other_stock in data:
                            if other_stock.get('code') == code:
                                in_other_sources = True
                                break
                
                if in_other_sources:
                    recommended_stock['data_quality'] = '已验证'
                else:
                    recommended_stock['data_quality'] = '仅东方财富'
            
            recommended.append(recommended_stock)
        
        return recommended
    
    def validate_and_report(self) -> Dict:
        """执行验证并生成报告"""
        logger.info("开始多数据源验证...")
        
        # 1. 从所有数据源获取数据
        data_by_source = self.fetch_all_sources()
        
        # 2. 比较数据源
        comparison = self.compare_data_sources(data_by_source)
        
        # 3. 获取推荐数据
        recommended_data = self.get_recommended_data(data_by_source, comparison)
        
        # 4. 生成报告
        report = {
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'data_by_source': {k: len(v) for k, v in data_by_source.items()},
            'comparison': comparison,
            'recommended_data_count': len(recommended_data),
            'recommended_data': recommended_data,
        }
        
        return report


# ========== 测试代码 ==========

if __name__ == "__main__":
    print("=" * 60)
    print("多数据源新股数据验证器")
    print("=" * 60)
    
    try:
        validator = MultiSourceValidator()
        
        print("\n1. 从所有数据源获取数据...")
        report = validator.validate_and_report()
        
        print(f"\n2. 数据源统计:")
        for source, count in report['data_by_source'].items():
            print(f"   {source}: {count} 只新股")
        
        print(f"\n3. 数据比较结果:")
        comparison = report['comparison']
        
        print(f"   唯一股票总数: {comparison['summary'].get('total_unique_stocks', 0)}")
        print(f"   共同股票数: {comparison['summary'].get('common_stocks_count', 0)}")
        print(f"   一致性率: {comparison['summary'].get('consistency_rate', 0):.1f}%")
        print(f"   数据质量: {comparison['summary'].get('data_quality', '未知')}")
        
        if comparison['common_stocks']:
            print(f"   共同股票代码: {', '.join(comparison['common_stocks'][:10])}")
        
        if comparison['unique_by_source']:
            print(f"\n4. 各数据源独有股票:")
            for source, codes in comparison['unique_by_source'].items():
                if codes:
                    print(f"   {source}: {len(codes)} 只 ({', '.join(codes[:5])})")
        
        if comparison['conflicts']:
            print(f"\n5. 数据冲突 ({len(comparison['conflicts'])} 处):")
            for conflict in comparison['conflicts'][:3]:  # 只显示前3个
                print(f"   股票 {conflict['code']}:")
                for c in conflict['conflicts']:
                    print(f"     - {c}")
        
        print(f"\n6. 推荐数据 ({report['recommended_data_count']} 只):")
        for i, stock in enumerate(report['recommended_data'][:5], 1):
            print(f"   {i}. {stock.get('name', '未知')}({stock.get('code', '未知')})")
            print(f"      申购日期: {stock.get('apply_date', '未知')}")
            print(f"      发行价格: {stock.get('issue_price', '未知')}")
            print(f"      市场类型: {stock.get('market_type', '未知')}")
            print(f"      数据质量: {stock.get('data_quality', '未知')}")
        
        print("\n" + "=" * 60)
        print("✅ 多数据源验证完成")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ 验证失败: {e}")
        import traceback
        traceback.print_exc()