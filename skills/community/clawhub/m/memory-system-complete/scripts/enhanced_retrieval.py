#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Enhanced Retrieval System
增强检索系统 - Clawvard Memory改进
"""

import sqlite3
import re
from typing import List, Dict, Optional, Tuple
from datetime import datetime, timedelta
from collections import defaultdict

class EnhancedRetrieval:
    """增强检索系统"""
    
    def __init__(self, db_path: str = None):
        if db_path is None:
            db_path = "memory/database/xiaozhi_memory.db"
        self.db_path = db_path
        self.conn = None
    
    def initialize(self) -> bool:
        """初始化检索系统"""
        try:
            self.conn = sqlite3.connect(self.db_path)
            self.conn.row_factory = sqlite3.Row
            return True
        except Exception as e:
            print(f"Error initializing retrieval system: {e}")
            return False
    
    def search(self, query: str, limit: int = 10, 
               min_importance: int = None,
               category: str = None,
               days_old: int = None) -> List[Dict]:
        """
        增强搜索
        
        Args:
            query: 搜索查询
            limit: 结果数量限制
            min_importance: 最小重要性
            category: 分类过滤
            days_old: 时间范围（天）
            
        Returns:
            搜索结果列表
        """
        cursor = self.conn.cursor()
        
        # 构建查询
        sql = "SELECT * FROM memories WHERE 1=1"
        params = []
        
        # 关键词搜索
        if query:
            keywords = self._extract_keywords(query)
            if keywords:
                conditions = []
                for keyword in keywords:
                    conditions.append("(title LIKE ? OR content LIKE ? OR tags LIKE ?)")
                    params.extend([f'%{keyword}%', f'%{keyword}%', f'%{keyword}%'])
                sql += " AND (" + " OR ".join(conditions) + ")"
        
        # 重要性过滤
        if min_importance:
            sql += " AND importance >= ?"
            params.append(min_importance)
        
        # 分类过滤
        if category:
            sql += " AND category = ?"
            params.append(category)
        
        # 时间过滤
        if days_old:
            cutoff_date = datetime.now() - timedelta(days=days_old)
            sql += " AND datetime(created_at) >= datetime(?)"
            params.append(cutoff_date.isoformat())
        
        # 排序和限制
        sql += " ORDER BY importance DESC, created_at DESC LIMIT ?"
        params.append(limit)
        
        cursor.execute(sql, params)
        
        results = []
        for row in cursor.fetchall():
            result = dict(row)
            if result['tags']:
                import json
                result['tags'] = json.loads(result['tags'])
            results.append(result)
        
        return results
    
    def _extract_keywords(self, query: str) -> List[str]:
        """提取关键词"""
        # 移除停用词
        stop_words = {'the', 'a', 'an', 'is', 'are', 'was', 'were', 'be', 'been', 
                     'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will',
                     'would', 'could', 'should', 'may', 'might', 'must', 'shall',
                     'can', 'need', 'dare', 'ought', 'used', 'to', 'of', 'in',
                     'for', 'on', 'with', 'at', 'by', 'from', 'as', 'into',
                     'through', 'during', 'before', 'after', 'above', 'below',
                     'between', 'under', 'again', 'further', 'then', 'once',
                     'here', 'there', 'when', 'where', 'why', 'how', 'all',
                     'each', 'few', 'more', 'most', 'other', 'some', 'such',
                     'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than',
                     'too', 'very', 'just', 'and', 'but', 'if', 'or', 'because',
                     'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with',
                     'about', 'against', 'between', 'into', 'through', 'during',
                     'before', 'after', 'above', 'below', 'to', 'from', 'up',
                     'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again',
                     'further', 'then', 'once'}
        
        # 分词
        words = re.findall(r'\b\w+\b', query.lower())
        
        # 过滤停用词和短词
        keywords = [word for word in words 
                   if word not in stop_words and len(word) > 2]
        
        return keywords
    
    def semantic_search(self, query: str, limit: int = 10) -> List[Dict]:
        """
        语义搜索（简化版，实际应该使用向量搜索）
        
        Args:
            query: 搜索查询
            limit: 结果数量限制
            
        Returns:
            搜索结果列表
        """
        # 这里简化为关键词搜索
        # 实际应该使用LanceDB进行向量搜索
        return self.search(query, limit=limit)
    
    def get_related_memories(self, memory_id: int, limit: int = 5) -> List[Dict]:
        """
        获取相关记忆
        
        Args:
            memory_id: 记忆ID
            limit: 结果数量限制
            
        Returns:
            相关记忆列表
        """
        cursor = self.conn.cursor()
        
        # 获取原记忆
        cursor.execute('SELECT * FROM memories WHERE id = ?', (memory_id,))
        original = cursor.fetchone()
        
        if not original:
            return []
        
        original = dict(original)
        
        # 提取关键词
        keywords = []
        if original['title']:
            keywords.extend(self._extract_keywords(original['title']))
        if original['content']:
            keywords.extend(self._extract_keywords(original['content']))
        
        if not keywords:
            return []
        
        # 搜索相关记忆
        sql = "SELECT * FROM memories WHERE id != ? AND ("
        params = [memory_id]
        
        conditions = []
        for keyword in keywords[:3]:  # 限制关键词数量
            conditions.append("(title LIKE ? OR content LIKE ?)")
            params.extend([f'%{keyword}%', f'%{keyword}%'])
        
        sql += " OR ".join(conditions) + ") ORDER BY importance DESC LIMIT ?"
        params.append(limit)
        
        cursor.execute(sql, params)
        
        results = []
        for row in cursor.fetchall():
            result = dict(row)
            if result['tags']:
                import json
                result['tags'] = json.loads(result['tags'])
            results.append(result)
        
        return results
    
    def get_trending_memories(self, days: int = 7, limit: int = 10) -> List[Dict]:
        """
        获取热门记忆（最近访问/更新）
        
        Args:
            days: 天数范围
            limit: 结果数量限制
            
        Returns:
            热门记忆列表
        """
        cursor = self.conn.cursor()
        
        cutoff_date = datetime.now() - timedelta(days=days)
        
        cursor.execute('''
            SELECT * FROM memories
            WHERE datetime(updated_at) >= datetime(?)
            ORDER BY importance DESC, updated_at DESC
            LIMIT ?
        ''', (cutoff_date.isoformat(), limit))
        
        results = []
        for row in cursor.fetchall():
            result = dict(row)
            if result['tags']:
                import json
                result['tags'] = json.loads(result['tags'])
            results.append(result)
        
        return results
    
    def get_statistics(self) -> Dict:
        """获取统计信息"""
        cursor = self.conn.cursor()
        
        # 总数
        cursor.execute('SELECT COUNT(*) FROM memories')
        total = cursor.fetchone()[0]
        
        # 按类型统计
        cursor.execute('''
            SELECT type, COUNT(*) as count
            FROM memories
            GROUP BY type
        ''')
        by_type = {row[0]: row[1] for row in cursor.fetchall()}
        
        # 按重要性统计
        cursor.execute('''
            SELECT importance, COUNT(*) as count
            FROM memories
            GROUP BY importance
        ''')
        by_importance = {row[0]: row[1] for row in cursor.fetchall()}
        
        # 按分类统计
        cursor.execute('''
            SELECT category, COUNT(*) as count
            FROM memories
            WHERE category IS NOT NULL
            GROUP BY category
        ''')
        by_category = {row[0]: row[1] for row in cursor.fetchall()}
        
        return {
            'total': total,
            'by_type': by_type,
            'by_importance': by_importance,
            'by_category': by_category
        }
    
    def close(self):
        """关闭连接"""
        if self.conn:
            self.conn.close()


if __name__ == "__main__":
    retrieval = EnhancedRetrieval()
    retrieval.initialize()
    
    # 测试搜索
    results = retrieval.search("python", limit=5)
    print(f"Found {len(results)} results")
    
    # 获取统计
    stats = retrieval.get_statistics()
    print(f"Statistics: {stats}")
    
    retrieval.close()
