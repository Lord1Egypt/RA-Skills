#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Erbing 大脑 - 四策略检索系统
基于 Memori 架构的四种检索策略
"""
import sqlite3
import json
import re
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple
from pathlib import Path
import sys

class FourStrategyRetrieval:
    """四策略检索系统"""

    def __init__(self, db_path: str = None):
        """
        初始化四策略检索系统

        Args:
            db_path: SQLite数据库路径
        """
        if db_path is None:
            db_path = "memory/database/xiaozhi_memory.db"
        self.db_path = db_path

    # ==================== 策略 1: 按需归因检索 ====================
    def retrieve_by_attribution(self, query: str, entity_id: str = None, process_id: str = None) -> List[Dict]:
        """
        策略 1: 按需归因检索
        根据 Entity/Process/Session 三层归因，按需查询，不遍历全部

        参数:
            query: 搜索关键词
            entity_id: 实体 ID（可选）
            process_id: 过程 ID（可选）

        返回:
            相关记忆列表
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        # 构建三层归因查询
        sql = """
            SELECT * FROM memories
            WHERE (title LIKE ? OR content LIKE ? OR tags LIKE ?)
        """
        params = [f"%{query}%", f"%{query}%", f"%{query}%"]

        # 添加归因过滤（如果有）
        if entity_id:
            sql += " AND (tags LIKE ? OR content LIKE ?)"
            params.extend([f"%{entity_id}%", f"%{entity_id}%"])

        if process_id:
            sql += " AND (tags LIKE ? OR content LIKE ?)"
            params.extend([f"%{process_id}%", f"%{process_id}%"])

        # 按重要性排序
        sql += " ORDER BY importance DESC, created_at DESC LIMIT 20"

        cursor.execute(sql, params)
        results = [dict(row) for row in cursor.fetchall()]
        conn.close()

        return results

    # ==================== 策略 2: 时间衰减检索 ====================
    def retrieve_by_time_decay(self, query: str, half_life_days: int = 30, limit: int = 10) -> List[Dict]:
        """
        策略 2: 时间衰减检索
        最近的记忆权重更高，遵循指数衰减

        参数:
            query: 搜索关键词
            half_life_days: 半衰期（天），默认30天
            limit: 返回数量

        返回:
            按时间衰减权重排序的记忆列表
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        # 计算 decay_factor = exp(-ln(2) * days / half_life)
        # 使用 SQLite 的数学函数
        sql = """
            SELECT *,
                   importance * exp(-0.693 * CAST((julianday('now') - julianday(created_at)) AS REAL) / ?) AS decay_score
            FROM memories
            WHERE title LIKE ? OR content LIKE ? OR tags LIKE ?
            ORDER BY decay_score DESC
            LIMIT ?
        """

        cursor.execute(sql, (half_life_days, f"%{query}%", f"%{query}%", f"%{query}%", limit))
        results = [dict(row) for row in cursor.fetchall()]
        conn.close()

        return results

    # ==================== 策略 3: 重要性优先检索 ====================
    def retrieve_by_importance(self, min_importance: int = 7, limit: int = 15) -> List[Dict]:
        """
        策略 3: 重要性优先检索
        优先返回高重要性记忆，用于关键决策

        参数:
            min_importance: 最低重要性阈值（1-10）
            limit: 返回数量

        返回:
            高重要性记忆列表
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        sql = """
            SELECT * FROM memories
            WHERE importance >= ?
            ORDER BY importance DESC, created_at DESC
            LIMIT ?
        """

        cursor.execute(sql, (min_importance, limit))
        results = [dict(row) for row in cursor.fetchall()]
        conn.close()

        return results

    # ==================== 策略 4: 向量语义检索 ====================
    def retrieve_by_semantic(self, query: str, limit: int = 10) -> List[Dict]:
        """
        策略 4: 向量语义检索
        使用 LanceDB 进行向量相似度搜索，支持语义联想

        参数:
            query: 查询文本
            limit: 返回数量

        返回:
            语义相似的记忆列表
        """
        # 简化版本：使用关键词搜索
        # 完整版本需要集成 LanceDB
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        sql = """
            SELECT * FROM memories
            WHERE title LIKE ? OR content LIKE ?
            ORDER BY importance DESC
            LIMIT ?
        """

        cursor.execute(sql, (f"%{query}%", f"%{query}%", limit))
        results = [dict(row) for row in cursor.fetchall()]
        conn.close()

        return results

    # ==================== 组合策略：智能检索 ====================
    def smart_retrieve(self, query: str, mode: str = "balanced") -> Dict[str, List[Dict]]:
        """
        智能检索：组合四种策略

        参数:
            query: 搜索关键词
            mode: 检索模式
                - "balanced": 平衡模式（默认），四种策略均衡
                - "importance": 重要性优先
                - "recent": 时效性优先
                - "semantic": 语义优先

        返回:
            包含四种策略结果的字典
        """
        results = {}

        if mode == "balanced":
            # 平衡模式：每种策略取少量
            results["attribution"] = self.retrieve_by_attribution(query)[:5]
            results["time_decay"] = self.retrieve_by_time_decay(query)[:5]
            results["importance"] = self.retrieve_by_importance()[:5]
            results["semantic"] = self.retrieve_by_semantic(query)[:5]

        elif mode == "importance":
            # 重要性优先：主要用重要性检索
            results["importance"] = self.retrieve_by_importance(min_importance=8, limit=10)
            results["attribution"] = self.retrieve_by_attribution(query)[:3]

        elif mode == "recent":
            # 时效性优先：主要用时间衰减
            results["time_decay"] = self.retrieve_by_time_decay(query, half_life_days=7, limit=10)
            results["semantic"] = self.retrieve_by_semantic(query)[:3]

        elif mode == "semantic":
            # 语义优先：主要用向量检索
            results["semantic"] = self.retrieve_by_semantic(query, limit=10)
            results["attribution"] = self.retrieve_by_attribution(query)[:3]

        # 去重合并
        all_ids = set()
        unique_results = []
        for strategy_name, items in results.items():
            for item in items:
                if item["id"] not in all_ids:
                    all_ids.add(item["id"])
                    item["_strategy"] = strategy_name
                    unique_results.append(item)

        return {
            "by_strategy": results,
            "merged": sorted(unique_results, key=lambda x: x.get("importance", 5), reverse=True)
        }

    # ==================== 辅助方法 ====================
    def get_context_for_generation(self, query: str, max_tokens: int = 4000) -> str:
        """
        为生成获取上下文：智能选择最相关的记忆

        参数:
            query: 当前查询
            max_tokens: 最大 token 数（估算）

        返回:
            格式化的上下文字符串
        """
        # 智能检索
        smart_results = self.smart_retrieve(query, mode="balanced")
        merged = smart_results["merged"]

        # 构建上下文
        context_parts = []
        current_length = 0

        for mem in merged[:20]:  # 最多20条
            # 格式化记忆
            mem_text = f"[{mem['type']}] {mem['title']}\n{mem['content'][:500]}\n"
            mem_length = len(mem_text) // 4  # 粗略估算 token

            if current_length + mem_length > max_tokens:
                break

            context_parts.append(mem_text)
            current_length += mem_length

        return "\n---\n".join(context_parts)


def main():
    """测试四策略检索"""
    retrieval = FourStrategyRetrieval()

    print("="*60)
    print("四策略检索系统 - 测试")
    print("="*60)

    # 测试查询
    test_query = "Erbing-1B"

    print(f"\n测试查询: {test_query}\n")

    # 策略 1: 按需归因
    print("策略 1: 按需归因检索")
    print("-" * 40)
    results = retrieval.retrieve_by_attribution(test_query)
    for r in results[:3]:
        print(f"  - [{r['type']}] {r['title']} (importance: {r['importance']})")

    # 策略 2: 时间衰减
    print("\n策略 2: 时间衰减检索")
    print("-" * 40)
    results = retrieval.retrieve_by_time_decay(test_query, half_life_days=30)
    for r in results[:3]:
        print(f"  - [{r['type']}] {r['title']} (decay_score: {r.get('decay_score', 'N/A'):.2f})")

    # 策略 3: 重要性优先
    print("\n策略 3: 重要性优先检索")
    print("-" * 40)
    results = retrieval.retrieve_by_importance(min_importance=8)
    for r in results[:5]:
        print(f"  - [{r['type']}] {r['title']} (importance: {r['importance']})")

    # 策略 4: 向量语义
    print("\n策略 4: 向量语义检索")
    print("-" * 40)
    results = retrieval.retrieve_by_semantic(test_query)
    for r in results[:3]:
        print(f"  - [{r['type']}] {r['title']} (score: {r.get('_score', 'N/A')})")

    # 智能检索
    print("\n智能检索（组合模式）")
    print("-" * 40)
    smart = retrieval.smart_retrieve(test_query, mode="balanced")
    print(f"  总计合并: {len(smart['merged'])} 条记忆")
    for strategy, items in smart["by_strategy"].items():
        print(f"  - {strategy}: {len(items)} 条")


if __name__ == "__main__":
    main()
