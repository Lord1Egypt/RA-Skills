#!/usr/bin/env python3
"""
差异计算引擎 - 对比新旧数据，判断新增/更新
优化版：使用hash快速比对，提高效率
"""
import logging
import hashlib
from typing import Dict, List, Set
from datetime import datetime


class DiffEngine:
    """差异计算引擎"""
    
    # 用于生成hash的关键字段
    KEY_FIELDS = [
        'stock_code',
        'company_name', 
        'application_status',
        'expected_date',
        'fundraising_amount',
        'issue_price_range'
    ]
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def _compute_hash(self, item: Dict) -> str:
        """
        计算数据项的hash值
        
        使用关键字段生成hash，用于快速比对是否有变化
        """
        # 提取关键字段值
        key_values = []
        for field in self.KEY_FIELDS:
            value = item.get(field, '') or ''
            key_values.append(str(value).strip())
        
        # 生成hash
        content = '|'.join(key_values)
        return hashlib.md5(content.encode('utf-8')).hexdigest()
    
    def _compute_content_hash(self, item: Dict) -> str:
        """
        计算完整内容的hash（用于去重）
        """
        # 按字段排序后生成hash，确保一致性
        sorted_fields = sorted(item.items())
        content = str(sorted_fields)
        return hashlib.md5(content.encode('utf-8')).hexdigest()
    
    def compute_diff(self, old_data: Dict[str, List[Dict]], new_data: Dict[str, List[Dict]]) -> Dict:
        """
        计算差异（优化版：使用hash快速比对）
        
        Args:
            old_data: 上次数据 {'板块名': [IPO列表]}
            new_data: 新数据 {'板块名': [IPO列表]}
        
        Returns:
            差异报告
        """
        result = {
            'has_changes': False,
            'added': [],      # 新增
            'updated': [],    # 更新
            'removed': [],   # 删除（下市/撤回）
            'summary': {},
        }
        
        # ========== 步骤1: 构建old数据的hash索引（O(n)）==========
        old_hashes: Dict[str, Dict] = {}  # {exchange: {hash: item}}
        old_codes: Dict[str, Set[str]] = {}  # {exchange: {stock_codes}}
        
        for exchange, old_list in old_data.items():
            old_hashes[exchange] = {}
            old_codes[exchange] = set()
            
            for item in old_list:
                stock_code = item.get('stock_code')
                if stock_code:
                    old_codes[exchange].add(stock_code)
                    # 计算hash用于快速比对
                    item_hash = self._compute_hash(item)
                    item['_content_hash'] = item_hash
                    old_hashes[exchange][item_hash] = item
        
        # ========== 步骤2: 遍历新数据，查找新增和更新（O(m)）==========
        # 构建stock_code到hash的映射，实现O(1)查找
        old_code_to_hash: Dict[str, Dict] = {}  # {exchange: {stock_code: {hash: item}}}
        
        for exchange, old_hash_map in old_hashes.items():
            old_code_to_hash[exchange] = {}
            for item_hash, old_item in old_hash_map.items():
                stock_code = old_item.get('stock_code')
                if stock_code:
                    old_code_to_hash[exchange][stock_code] = old_item
        
        for exchange, new_list in new_data.items():
            old_list = old_data.get(exchange, [])
            old_code_map = old_code_to_hash.get(exchange, {})
            old_code_set = old_codes.get(exchange, set())
            
            added_count = 0
            updated_count = 0
            
            for new_item in new_list:
                stock_code = new_item.get('stock_code')
                
                if not stock_code:
                    continue
                
                # 计算新数据的hash
                new_hash = self._compute_hash(new_item)
                new_item['_content_hash'] = new_hash
                
                if stock_code not in old_code_set:
                    # 新增：股票代码在旧数据中不存在
                    new_item['change_type'] = '新增'
                    new_item['change_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    result['added'].append({
                        'exchange': exchange,
                        'data': new_item
                    })
                    added_count += 1
                else:
                    # 股票代码存在，使用O(1) hash查找检查内容是否有变化
                    found_old = old_code_map.get(stock_code)
                    
                    if found_old:
                        old_hash = found_old.get('_content_hash', '')
                        if old_hash and old_hash != new_hash:
                            # 有更新
                            new_item['change_type'] = '更新'
                            new_item['change_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                            new_item['old_status'] = found_old.get('application_status')
                            new_item['old_fundraising'] = found_old.get('fundraising_amount')
                            new_item['old_price_range'] = found_old.get('issue_price_range')
                            result['updated'].append({
                                'exchange': exchange,
                                'data': new_item
                            })
                            updated_count += 1
            
            result['summary'][exchange] = {
                'added': added_count,
                'updated': updated_count,
                'total': len(new_list)
            }
        
        # ========== 步骤3: 检查删除（利用已有的code set，O(n)）==========
        for exchange, old_list in old_data.items():
            new_list = new_data.get(exchange, [])
            new_codes = {item['stock_code'] for item in new_list if item.get('stock_code')}
            
            for old_item in old_list:
                stock_code = old_item.get('stock_code')
                if stock_code and stock_code not in new_codes:
                    old_item['change_type'] = '删除'
                    result['removed'].append({
                        'exchange': exchange,
                        'data': old_item
                    })
        
        # 判断是否有变化
        result['has_changes'] = bool(result['added'] or result['updated'] or result['removed'])
        
        # 记录日志
        if result['has_changes']:
            self.logger.info(
                f"发现变化: 新增{len(result['added'])}条, 更新{len(result['updated'])}条, 删除{len(result['removed'])}条"
            )
        else:
            self.logger.info("无变化")
        
        return result
    
    def compute_diff_fast(self, old_data: Dict[str, List[Dict]], new_data: Dict[str, List[Dict]]) -> Dict:
        """
        极速版差异计算（仅比较stock_code是否存在）
        
        适用于只需要知道新增/删除，不关心内容变化的场景
        """
        result = {
            'has_changes': False,
            'added': [],
            'removed': [],
            'summary': {},
        }
        
        # 构建旧数据的股票代码集合
        old_codes: Dict[str, Set[str]] = {}
        for exchange, old_list in old_data.items():
            old_codes[exchange] = {item['stock_code'] for item in old_list if item.get('stock_code')}
        
        # 查找新增
        for exchange, new_list in new_data.items():
            old_code_set = old_codes.get(exchange, set())
            added = 0
            
            for new_item in new_list:
                stock_code = new_item.get('stock_code')
                if stock_code and stock_code not in old_code_set:
                    new_item['change_type'] = '新增'
                    new_item['change_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    result['added'].append({
                        'exchange': exchange,
                        'data': new_item
                    })
                    added += 1
            
            result['summary'][exchange] = {
                'added': added,
                'total': len(new_list)
            }
        
        # 查找删除
        for exchange, old_list in old_data.items():
            new_list = new_data.get(exchange, [])
            new_codes = {item['stock_code'] for item in new_list if item.get('stock_code')}
            
            for old_item in old_list:
                stock_code = old_item.get('stock_code')
                if stock_code and stock_code not in new_codes:
                    old_item['change_type'] = '删除'
                    result['removed'].append({
                        'exchange': exchange,
                        'data': old_item
                    })
        
        result['has_changes'] = bool(result['added'] or result['removed'])
        
        return result
    
    def _has_update(self, old_item: Dict, new_item: Dict) -> bool:
        """
        检查是否有实质更新（保留用于兼容性）
        """
        # 使用hash快速比对
        old_hash = self._compute_hash(old_item)
        new_hash = self._compute_hash(new_item)
        return old_hash != new_hash


# 导出
__all__ = ['DiffEngine']
