#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
IPO数据验证器 - 专门验证即将申购的新股数据
使用多个数据源交叉验证
"""

import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import requests
from bs4 import BeautifulSoup

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class IPODDataValidator:
    """IPO数据验证器（专门针对即将申购的新股）"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'application/json, text/html, */*',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        })
        
        # 专门针对即将申购新股的API
        self.data_sources = {
            'eastmoney_ipo': {
                'name': '东方财富-新股申购',
                'url': 'http://datacenter-web.eastmoney.com/api/data/v1/get',
                'params': {
                    'reportName': 'RPTA_APP_IPOAPPLY',
                    'columns': 'ALL',
                    'pageNumber': '1',
                    'pageSize': '100',
                    'sortColumns': 'APPLY_DATE',
                    'sortTypes': '-1',
                    'source': 'WEB',
                    'client': 'WEB',
                },
                'parser': self._parse_eastmoney_ipo,
            },
            'eastmoney_calendar': {
                'name': '东方财富-新股日历',
                'url': 'https://datacenter-web.eastmoney.com/api/data/v1/get',
                'params': {
                    'reportName': 'RPT_IPO_CALENDAR',
                    'columns': 'ALL',
                    'pageNumber': '1',
                    'pageSize': '100',
                    'sortColumns': 'APPLY_DATE',
                    'sortTypes': '-1',
                    'source': 'WEB',
                    'client': 'WEB',
                },
                'parser': self._parse_eastmoney_calendar,
            },
        }
    
    def _parse_eastmoney_ipo(self, data: Dict) -> List[Dict]:
        """解析东方财富新股申购数据"""
        stocks = []
        today = datetime.now().strftime('%Y-%m-%d')
        
        raw_data = data.get('result', {}).get('data', [])
        for item in raw_data:
            try:
                apply_date = item.get('APPLY_DATE', '')
                if not apply_date:
                    continue
                
                apply_date_str = apply_date[:10]
                
                # 只获取今天及未来的数据
                if apply_date_str < today:
                    continue
                
                stock = {
                    'source': 'eastmoney_ipo',
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
                    'status': '即将申购' if apply_date_str > today else '今日申购',
                }
                
                stocks.append(stock)
                
            except Exception as e:
                logger.warning(f"解析东方财富IPO数据失败: {e}")
                continue
        
        return stocks
    
    def _parse_eastmoney_calendar(self, data: Dict) -> List[Dict]:
        """解析东方财富新股日历数据"""
        stocks = []
        today = datetime.now().strftime('%Y-%m-%d')
        
        raw_data = data.get('result', {}).get('data', [])
        for item in raw_data:
            try:
                apply_date = item.get('APPLY_DATE', '')
                if not apply_date:
                    continue
                
                apply_date_str = apply_date[:10]
                
                # 只获取今天及未来的数据
                if apply_date_str < today:
                    continue
                
                stock = {
                    'source': 'eastmoney_calendar',
                    'code': item.get('SECURITY_CODE', ''),
                    'name': item.get('SECURITY_NAME', ''),
                    'apply_date': apply_date_str,
                    'issue_price': item.get('ISSUE_PRICE'),
                    'market_type': item.get('MARKET_TYPE', ''),
                    'issue_num': item.get('ISSUE_NUM'),
                    'total_raise': item.get('TOTAL_RAISE_FUNDS'),
                    'status': '即将申购' if apply_date_str > today else '今日申购',
                }
                
                stocks.append(stock)
                
            except Exception as e:
                logger.warning(f"解析东方财富日历数据失败: {e}")
                continue
        
        return stocks
    
    def fetch_from_source(self, source_key: str) -> List[Dict]:
        """从指定数据源获取数据"""
        source_config = self.data_sources.get(source_key)
        if not source_config:
            logger.error(f"未知数据源: {source_key}")
            return []
        
        try:
            logger.info(f"请求{source_config['name']}...")
            response = self.session.get(
                source_config['url'],
                params=source_config['params'],
                timeout=15
            )
            response.raise_for_status()
            
            data = response.json()
            if not data.get('success'):
                logger.error(f"{source_config['name']}返回失败: {data.get('message')}")
                return []
            
            # 使用对应的解析器
            stocks = source_config['parser'](data)
            logger.info(f"从{source_config['name']}获取到 {len(stocks)} 只即将申购新股")
            
            return stocks
            
        except Exception as e:
            logger.error(f"{source_config['name']}数据获取失败: {e}")
            return []
    
    def fetch_all_sources(self) -> Dict[str, List[Dict]]:
        """从所有数据源获取数据"""
        results = {}
        
        for source_key in self.data_sources.keys():
            data = self.fetch_from_source(source_key)
            results[source_key] = data
        
        return results
    
    def compare_and_validate(self, data_by_source: Dict[str, List[Dict]]) -> Dict:
        """比较和验证数据"""
        validation_result = {
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'sources_count': len(data_by_source),
            'data_by_source': {},
            'validation': {
                'total_unique_stocks': 0,
                'common_stocks': [],
                'data_consistency': 0.0,
                'data_quality': '未知',
                'recommendations': [],
                'warnings': [],
            },
        }
        
        # 统计各数据源
        for source, stocks in data_by_source.items():
            validation_result['data_by_source'][source] = {
                'count': len(stocks),
                'stocks': [{'code': s['code'], 'name': s['name'], 'apply_date': s['apply_date']} for s in stocks[:10]],
            }
        
        # 如果没有至少两个数据源，无法验证
        if len(data_by_source) < 2:
            validation_result['validation']['warnings'].append('数据源不足，无法进行有效验证')
            return validation_result
        
        # 提取股票代码
        stock_sets = {}
        for source, stocks in data_by_source.items():
            codes = set(s['code'] for s in stocks if s.get('code'))
            stock_sets[source] = codes
        
        # 计算唯一股票总数
        all_codes = set()
        for codes in stock_sets.values():
            all_codes.update(codes)
        
        validation_result['validation']['total_unique_stocks'] = len(all_codes)
        
        # 计算共同股票
        common_codes = set.intersection(*stock_sets.values())
        validation_result['validation']['common_stocks'] = list(common_codes)
        
        # 计算数据一致性
        if all_codes:
            consistency = len(common_codes) / len(all_codes) * 100
            validation_result['validation']['data_consistency'] = consistency
            
            if consistency >= 80:
                validation_result['validation']['data_quality'] = '优秀'
            elif consistency >= 60:
                validation_result['validation']['data_quality'] = '良好'
            elif consistency >= 40:
                validation_result['validation']['data_quality'] = '一般'
            else:
                validation_result['validation']['data_quality'] = '较差'
        else:
            validation_result['validation']['data_quality'] = '无数据'
        
        # 生成推荐
        if common_codes:
            validation_result['validation']['recommendations'].append(
                f"发现 {len(common_codes)} 只股票在多个数据源中一致，数据可靠性高"
            )
        
        # 检查数据差异
        for source, codes in stock_sets.items():
            other_codes = set()
            for other_source, other_codes_set in stock_sets.items():
                if other_source != source:
                    other_codes.update(other_codes_set)
            
            unique_codes = codes - other_codes
            if unique_codes:
                validation_result['validation']['warnings'].append(
                    f"{self.data_sources[source]['name']} 有 {len(unique_codes)} 只独有股票"
                )
        
        # 检查关键信息一致性
        for code in common_codes:
            stock_info_by_source = {}
            
            for source, stocks in data_by_source.items():
                for stock in stocks:
                    if stock.get('code') == code:
                        stock_info_by_source[source] = stock
                        break
            
            # 检查申购日期一致性
            apply_dates = set()
            for source, info in stock_info_by_source.items():
                apply_date = info.get('apply_date')
                if apply_date:
                    apply_dates.add(apply_date)
            
            if len(apply_dates) > 1:
                validation_result['validation']['warnings'].append(
                    f"股票 {code} 在不同数据源的申购日期不一致: {', '.join(apply_dates)}"
                )
        
        return validation_result
    
    def get_validated_stocks(self, data_by_source: Dict[str, List[Dict]]) -> List[Dict]:
        """获取验证后的股票数据"""
        validated_stocks = []
        
        # 优先使用IPO申购数据
        ipo_data = data_by_source.get('eastmoney_ipo', [])
        
        if not ipo_data:
            logger.warning("IPO申购数据为空，尝试使用日历数据")
            for source, data in data_by_source.items():
                if data:
                    ipo_data = data
                    break
        
        if not ipo_data:
            return []
        
        # 标记数据验证状态
        stock_sets = {}
        for source, stocks in data_by_source.items():
            codes = set(s['code'] for s in stocks if s.get('code'))
            stock_sets[source] = codes
        
        # 计算共同股票
        common_codes = set.intersection(*stock_sets.values()) if len(stock_sets) >= 2 else set()
        
        for stock in ipo_data:
            code = stock.get('code')
            if not code:
                continue
            
            validated_stock = stock.copy()
            
            # 添加验证标记
            if code in common_codes:
                validated_stock['validation_status'] = '已验证（多数据源一致）'
                validated_stock['reliability'] = '高'
            else:
                # 检查是否在其他数据源也存在
                in_other_sources = False
                for source, codes in stock_sets.items():
                    if source != 'eastmoney_ipo' and code in codes:
                        in_other_sources = True
                        break
                
                if in_other_sources:
                    validated_stock['validation_status'] = '部分验证'
                    validated_stock['reliability'] = '中'
                else:
                    validated_stock['validation_status'] = '未验证（仅单一数据源）'
                    validated_stock['reliability'] = '低'
            
            validated_stocks.append(validated_stock)
        
        # 按申购日期排序
        validated_stocks.sort(key=lambda x: x.get('apply_date', ''))
        
        return validated_stocks
    
    def run_validation(self) -> Dict:
        """运行完整验证流程"""
        logger.info("开始IPO数据验证...")
        
        # 1. 从所有数据源获取数据
        data_by_source = self.fetch_all_sources()
        
        # 2. 比较和验证数据
        validation_result = self.compare_and_validate(data_by_source)
        
        # 3. 获取验证后的股票数据
        validated_stocks = self.get_validated_stocks(data_by_source)
        validation_result['validated_stocks'] = {
            'count': len(validated_stocks),
            'stocks': validated_stocks[:20],  # 只保留前20只
        }
        
        return validation_result


# ========== 测试代码 ==========

if __name__ == "__main__":
    print("=" * 60)
    print("IPO数据验证器 - 专门验证即将申购的新股")
    print("=" * 60)
    
    try:
        validator = IPODDataValidator()
        
        print("\n1. 运行验证流程...")
        result = validator.run_validation()
        
        print(f"\n2. 数据源统计:")
        for source, info in result['data_by_source'].items():
            source_name = validator.data_sources[source]['name']
            print(f"   {source_name}: {info['count']} 只新股")
            if info['stocks']:
                stocks_display = []
            for s in info['stocks'][:3]:
                stocks_display.append(f"{s['name']}({s['code']})")
            print(f"     示例: {', '.join(stocks_display)}")
        
        print(f"\n3. 验证结果:")
        validation = result['validation']
        print(f"   唯一股票总数: {validation['total_unique_stocks']}")
        print(f"   共同股票数: {len(validation['common_stocks'])}")
        print(f"   数据一致性: {validation['data_consistency']:.1f}%")
        print(f"   数据质量: {validation['data_quality']}")
        
        if validation['common_stocks']:
            print(f"   共同股票: {', '.join(validation['common_stocks'][:10])}")
        
        if validation['recommendations']:
            print(f"\n4. 推荐:")
            for rec in validation['recommendations']:
                print(f"   ✅ {rec}")
        
        if validation['warnings']:
            print(f"\n5. 警告:")
            for warning in validation['warnings']:
                print(f"   ⚠️ {warning}")
        
        print(f"\n6. 验证后股票数据 ({result['validated_stocks']['count']} 只):")
        validated_stocks = result['validated_stocks']['stocks']
        for i, stock in enumerate(validated_stocks[:10], 1):
            print(f"   {i}. {stock.get('name', '未知')}({stock.get('code', '未知')})")
            print(f"      申购日期: {stock.get('apply_date', '未知')}")
            print(f"      发行价格: {stock.get('issue_price', '未知') or '待定'}")
            print(f"      市场类型: {stock.get('market_type', '未知')}")
            print(f"      验证状态: {stock.get('validation_status', '未知')}")
            print(f"      可靠性: {stock.get('reliability', '未知')}")
            print()
        
        print("\n" + "=" * 60)
        print("✅ IPO数据验证完成")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ 验证失败: {e}")
        import traceback
        traceback.print_exc()