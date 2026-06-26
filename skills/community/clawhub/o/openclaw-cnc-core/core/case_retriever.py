#!/usr/bin/env python3.8
# -*- coding: utf-8 -*-
"""
case_retriever.py - 历史案例检索器
版本: v1.0
功能: 基于规则匹配检索相似历史报价案例
"""

import sqlite3
import json
import logging
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("CaseRetriever")

WORKSPACE = Path("/home/admin/.openclaw/workspace")
DB_PATH = WORKSPACE / "data" / "training_quotes.db"
PARAMS_PATH = WORKSPACE / "data" / "optimized_params_v2.json"


@dataclass
class QuoteCase:
    """报价案例数据结构"""
    record_id: str
    material: str
    volume_cm3: float
    quantity: int
    complexity: str
    tolerance: str
    surface_treatment: str
    unit_price: float
    total_price: float
    material_cost: float
    machining_cost: float
    similarity_score: float = 0.0


class CaseRetriever:
    """历史案例检索器"""
    
    def __init__(self, db_path: str = None, params_path: str = None):
        self.db_path = db_path or str(DB_PATH)
        self.params_path = params_path or str(PARAMS_PATH)
        self.params = self._load_params()
        
    def _load_params(self) -> dict:
        """加载优化参数"""
        try:
            with open(self.params_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            logger.warning(f"参数文件不存在: {self.params_path}")
            return {}
    
    def retrieve_similar_cases(
        self,
        material: str,
        volume_cm3: float,
        quantity: int,
        complexity: str = None,
        tolerance: str = None,
        surface_treatment: str = None,
        limit: int = 5
    ) -> List[QuoteCase]:
        """
        检索相似历史案例
        
        Args:
            material: 材料名称
            volume_cm3: 体积(cm³)
            quantity: 数量
            complexity: 复杂度
            tolerance: 公差等级
            surface_treatment: 表面处理
            limit: 返回案例数量
            
        Returns:
            相似案例列表
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 构建查询条件
        conditions = []
        params = []
        
        # 1. 材料必须匹配
        conditions.append("material = ?")
        params.append(material)
        
        # 2. 体积范围 (±50%)
        if volume_cm3 > 0:
            vol_min = volume_cm3 * 0.5
            vol_max = volume_cm3 * 1.5
            conditions.append("volume_cm3 BETWEEN ? AND ?")
            params.extend([vol_min, vol_max])
        
        # 3. 数量范围 (同一区间)
        qty_range = self._get_quantity_range(quantity)
        qty_min, qty_max = self._get_quantity_bounds(qty_range)
        conditions.append("quantity BETWEEN ? AND ?")
        params.extend([qty_min, qty_max])
        
        # 构建SQL
        sql = f"""
            SELECT 
                record_id, material, volume_cm3, quantity,
                complexity, tolerance, surface_treatment,
                real_unit_price, real_total_price,
                real_material_cost, real_machining_cost
            FROM training_quotes
            WHERE {' AND '.join(conditions)}
            ORDER BY ABS(volume_cm3 - ?) + ABS(quantity - ?) * 0.1
            LIMIT ?
        """
        params.extend([volume_cm3, quantity, limit])
        
        cursor.execute(sql, params)
        rows = cursor.fetchall()
        conn.close()
        
        # 转换为案例对象
        cases = []
        for row in rows:
            case = QuoteCase(
                record_id=row[0],
                material=row[1],
                volume_cm3=row[2],
                quantity=row[3],
                complexity=row[4] or '中等',
                tolerance=row[5] or '普通',
                surface_treatment=row[6] or '',
                unit_price=row[7],
                total_price=row[8],
                material_cost=row[9],
                machining_cost=row[10]
            )
            # 计算相似度分数
            case.similarity_score = self._calculate_similarity(
                case, volume_cm3, quantity, complexity, tolerance
            )
            cases.append(case)
        
        logger.info(f"检索到 {len(cases)} 条相似案例")
        return cases
    
    def _get_quantity_range(self, quantity: int) -> str:
        """获取数量区间"""
        if quantity <= 5:
            return '1-5'
        elif quantity <= 10:
            return '6-10'
        elif quantity <= 20:
            return '11-20'
        elif quantity <= 50:
            return '21-50'
        elif quantity <= 100:
            return '51-100'
        else:
            return '100+'
    
    def _get_quantity_bounds(self, qty_range: str) -> Tuple[int, int]:
        """获取数量区间边界"""
        bounds = {
            '1-5': (1, 5),
            '6-10': (6, 10),
            '11-20': (11, 20),
            '21-50': (21, 50),
            '51-100': (51, 100),
            '100+': (101, 10000)
        }
        return bounds.get(qty_range, (1, 10000))
    
    def _calculate_similarity(
        self,
        case: QuoteCase,
        target_volume: float,
        target_quantity: int,
        target_complexity: str,
        target_tolerance: str
    ) -> float:
        """
        计算相似度分数 (0-1)
        
        体积权重 40%, 数量权重 30%, 复杂度权重 20%, 公差权重 10%
        """
        score = 0.0
        
        # 体积相似度 (40%)
        if target_volume > 0 and case.volume_cm3 > 0:
            vol_diff = abs(case.volume_cm3 - target_volume) / target_volume
            vol_score = max(0, 1 - vol_diff)
            score += vol_score * 0.4
        
        # 数量相似度 (30%)
        if target_quantity > 0 and case.quantity > 0:
            qty_diff = abs(case.quantity - target_quantity) / target_quantity
            qty_score = max(0, 1 - qty_diff)
            score += qty_score * 0.3
        
        # 复杂度匹配 (20%)
        if target_complexity and case.complexity == target_complexity:
            score += 0.2
        
        # 公差匹配 (10%)
        if target_tolerance and case.tolerance == target_tolerance:
            score += 0.1
        
        return round(score, 3)
    
    def get_reference_price(
        self,
        material: str,
        volume_cm3: float,
        quantity: int,
        complexity: str = None,
        tolerance: str = None
    ) -> Dict:
        """
        获取参考价格
        
        Returns:
            {
                'avg_unit_price': 平均单价,
                'min_unit_price': 最低单价,
                'max_unit_price': 最高单价,
                'avg_total_price': 平均总价,
                'cases_count': 案例数量,
                'confidence': 置信度 (0-1)
            }
        """
        cases = self.retrieve_similar_cases(
            material=material,
            volume_cm3=volume_cm3,
            quantity=quantity,
            complexity=complexity,
            tolerance=tolerance,
            limit=10
        )
        
        if not cases:
            return {
                'avg_unit_price': None,
                'min_unit_price': None,
                'max_unit_price': None,
                'avg_total_price': None,
                'cases_count': 0,
                'confidence': 0.0
            }
        
        unit_prices = [c.unit_price for c in cases if c.unit_price > 0]
        total_prices = [c.total_price for c in cases if c.total_price > 0]
        similarity_scores = [c.similarity_score for c in cases]
        
        # 加权平均 (相似度越高权重越大)
        if unit_prices and similarity_scores:
            total_weight = sum(similarity_scores)
            if total_weight > 0:
                weighted_price = sum(p * s for p, s in zip(unit_prices, similarity_scores)) / total_weight
            else:
                weighted_price = sum(unit_prices) / len(unit_prices)
        else:
            weighted_price = 0
        
        # 置信度计算
        confidence = min(1.0, len(cases) / 5) * (sum(similarity_scores) / len(similarity_scores) if similarity_scores else 0)
        
        return {
            'avg_unit_price': round(weighted_price, 2),
            'min_unit_price': round(min(unit_prices), 2) if unit_prices else None,
            'max_unit_price': round(max(unit_prices), 2) if unit_prices else None,
            'avg_total_price': round(sum(total_prices) / len(total_prices), 2) if total_prices else None,
            'cases_count': len(cases),
            'confidence': round(confidence, 2),
            'similar_cases': [
                {
                    'record_id': c.record_id,
                    'quantity': c.quantity,
                    'unit_price': c.unit_price,
                    'similarity': c.similarity_score
                }
                for c in cases[:3]
            ]
        }


# 测试代码
if __name__ == "__main__":
    retriever = CaseRetriever()
    
    # 测试检索
    print("=== 测试案例检索 ===")
    result = retriever.get_reference_price(
        material="AL6061",
        volume_cm3=100,
        quantity=10,
        complexity="简单",
        tolerance="普通"
    )
    
    print(f"\n参考价格:")
    print(f"  平均单价: ¥{result['avg_unit_price']}")
    print(f"  价格区间: ¥{result['min_unit_price']} - ¥{result['max_unit_price']}")
    print(f"  置信度: {result['confidence']}")
    print(f"  案例数量: {result['cases_count']}")
    
    if result['similar_cases']:
        print(f"\n相似案例:")
        for case in result['similar_cases']:
            print(f"  - {case['record_id'][:30]}... | {case['quantity']}件 | ¥{case['unit_price']} | 相似度{case['similarity']}")