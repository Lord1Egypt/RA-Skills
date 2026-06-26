#!/usr/bin/env python3
"""
去重工具 - 基于股票代码+交易所唯一键
"""
from typing import List, Dict, Set


class Deduplicator:
    """去重器"""
    
    @staticmethod
    def deduplicate(ipo_list: List[Dict]) -> List[Dict]:
        """
        去重
        
        规则：同一交易所下，股票代码唯一
        """
        seen: Set[str] = set()
        result = []
        
        for ipo in ipo_list:
            # 生成唯一键：交易所_股票代码
            exchange = ipo.get('exchange', '')
            stock_code = ipo.get('stock_code', '')
            
            key = f"{exchange}_{stock_code}"
            
            if stock_code and key not in seen:
                seen.add(key)
                result.append(ipo)
        
        return result
    
    @staticmethod
    def merge_lists(lists: List[List[Dict]]) -> List[Dict]:
        """合并多个列表并去重"""
        all_data = []
        for lst in lists:
            all_data.extend(lst)
        return Deduplicator.deduplicate(all_data)
    
    @staticmethod
    def filter_valid(ipo_list: List[Dict]) -> List[Dict]:
        """过滤有效数据（必须有股票代码）"""
        return [ipo for ipo in ipo_list if ipo.get('stock_code')]


# 导出
__all__ = ['Deduplicator']
