#!/usr/bin/env python3.8
# -*- coding: utf-8 -*-
"""
hybrid_retriever.py - 混合检索器
版本: v1.0
功能: 统一接口，支持规则匹配和向量检索，优雅切换

架构：
┌─────────────────────────────────────────────┐
│              HybridRetriever                │
├─────────────────────────────────────────────┤
│  ┌─────────────┐    ┌─────────────────────┐ │
│  │ RuleMatcher │    │  VectorRetriever    │ │
│  │  (规则匹配)  │    │   (向量检索)         │ │
│  │   ✅ 可用    │    │   ⏳ 需要API Key    │ │
│  └─────────────┘    └─────────────────────┘ │
│           ↘                  ↙              │
│            └────────────────┘               │
│                    ↓                        │
│              统一结果返回                     │
└─────────────────────────────────────────────┘
"""

import os
import json
import logging
import sqlite3
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
from datetime import datetime

from case_retriever import CaseRetriever, QuoteCase

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("HybridRetriever")

WORKSPACE = Path("/home/admin/.openclaw/workspace")
DB_PATH = WORKSPACE / "data" / "training_quotes.db"
CONFIG_PATH = WORKSPACE / "data" / "retriever_config.json"


class RetrievalMode(Enum):
    """检索模式"""
    RULE_ONLY = "rule_only"           # 仅规则匹配
    VECTOR_ONLY = "vector_only"       # 仅向量检索
    HYBRID = "hybrid"                 # 混合模式（规则+向量加权）
    AUTO = "auto"                     # 自动选择（优先向量，降级规则）


@dataclass
class RetrievalResult:
    """检索结果"""
    success: bool
    mode_used: str                    # 实际使用的模式
    avg_unit_price: Optional[float]
    min_unit_price: Optional[float]
    max_unit_price: Optional[float]
    confidence: float
    cases_count: int
    similar_cases: List[Dict]
    error: Optional[str] = None
    
    def to_dict(self) -> Dict:
        return asdict(self)


class VectorRetriever:
    """向量检索器（需要API Key）"""
    
    def __init__(self, api_key: str = None, api_url: str = None, provider: str = "dashscope"):
        """
        初始化混合检索器

        Args:
            api_key: API密钥（可选）
            api_url: API地址（可选）
            provider: 服务提供商，支持: dashscope, openai, deepseek, zhipu, moonshot, local
        """
        from .config import APIAdapter

        self.adapter = APIAdapter(provider, api_key)
        self.api_key = self.adapter.api_key
        self.api_url = api_url or self.adapter.base_url
        self.available = False
        self._check_availability()
    
    def _check_availability(self) -> bool:
        """检查API是否可用"""
        if not self.api_key:
            logger.warning("向量检索: API Key未配置")
            return False
        
        try:
            import requests
            response = requests.post(
                f"{self.api_url}/embeddings",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "text-embedding-v2",
                    "input": "test"
                },
                timeout=5
            )
            if response.status_code == 200:
                self.available = True
                logger.info("向量检索: API可用 ✅")
                return True
            else:
                logger.warning(f"向量检索: API返回 {response.status_code}")
                return False
        except Exception as e:
            logger.warning(f"向量检索: API不可用 - {e}")
            return False
    
    def get_embedding(self, text: str) -> Optional[List[float]]:
        """获取文本向量"""
        if not self.available:
            return None
        
        try:
            import requests
            response = requests.post(
                f"{self.api_url}/embeddings",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "text-embedding-v2",
                    "input": text
                },
                timeout=30
            )
            if response.status_code == 200:
                return response.json()['data'][0]['embedding']
        except Exception as e:
            logger.error(f"获取向量失败: {e}")
        return None
    
    def retrieve(
        self,
        material: str,
        volume_cm3: float,
        quantity: int,
        complexity: str = None,
        tolerance: str = None,
        surface_treatment: str = None,
        limit: int = 5
    ) -> RetrievalResult:
        """向量检索（待实现）"""
        if not self.available:
            return RetrievalResult(
                success=False,
                mode_used="vector",
                avg_unit_price=None,
                min_unit_price=None,
                max_unit_price=None,
                confidence=0.0,
                cases_count=0,
                similar_cases=[],
                error="向量检索API不可用"
            )
        
        # TODO: 实现向量检索逻辑
        # 1. 构造查询文本
        # 2. 获取查询向量
        # 3. 在向量库中检索
        # 4. 返回结果
        
        return RetrievalResult(
            success=False,
            mode_used="vector",
            avg_unit_price=None,
            min_unit_price=None,
            max_unit_price=None,
            confidence=0.0,
            cases_count=0,
            similar_cases=[],
            error="向量检索功能待实现"
        )


class HybridRetriever:
    """混合检索器"""
    
    def __init__(
        self,
        mode: RetrievalMode = RetrievalMode.AUTO,
        config_path: str = None
    ):
        self.mode = mode
        self.config_path = config_path or str(CONFIG_PATH)
        
        # 初始化检索器
        self.rule_retriever = CaseRetriever()
        self.vector_retriever = VectorRetriever()
        
        # 加载配置
        self.config = self._load_config()
        
        logger.info(f"混合检索器初始化完成，模式: {mode.value}")
        logger.info(f"  规则匹配: ✅ 可用")
        logger.info(f"  向量检索: {'✅ 可用' if self.vector_retriever.available else '❌ 不可用'}")
    
    def _load_config(self) -> Dict:
        """加载配置"""
        default_config = {
            "mode": self.mode.value,
            "rule_weight": 0.5,        # 混合模式下规则权重
            "vector_weight": 0.5,      # 混合模式下向量权重
            "fallback_to_rule": True,  # 向量失败时降级到规则
            "min_confidence": 0.3      # 最低置信度阈值
        }
        
        try:
            if Path(self.config_path).exists():
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    saved_config = json.load(f)
                    default_config.update(saved_config)
        except Exception as e:
            logger.warning(f"加载配置失败: {e}")
        
        return default_config
    
    def _save_config(self):
        """保存配置"""
        try:
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.error(f"保存配置失败: {e}")
    
    def set_mode(self, mode: RetrievalMode):
        """切换检索模式"""
        self.mode = mode
        self.config["mode"] = mode.value
        self._save_config()
        logger.info(f"检索模式已切换为: {mode.value}")
    
    def retrieve(
        self,
        material: str,
        volume_cm3: float,
        quantity: int,
        complexity: str = None,
        tolerance: str = None,
        surface_treatment: str = None,
        limit: int = 5
    ) -> RetrievalResult:
        """
        检索相似案例
        
        根据配置的模式自动选择检索方式：
        - RULE_ONLY: 仅使用规则匹配
        - VECTOR_ONLY: 仅使用向量检索
        - HYBRID: 两种方式加权融合
        - AUTO: 优先向量，不可用时降级规则
        """
        
        if self.mode == RetrievalMode.RULE_ONLY:
            return self._rule_retrieve(
                material, volume_cm3, quantity, 
                complexity, tolerance, surface_treatment, limit
            )
        
        elif self.mode == RetrievalMode.VECTOR_ONLY:
            return self.vector_retriever.retrieve(
                material, volume_cm3, quantity,
                complexity, tolerance, surface_treatment, limit
            )
        
        elif self.mode == RetrievalMode.HYBRID:
            return self._hybrid_retrieve(
                material, volume_cm3, quantity,
                complexity, tolerance, surface_treatment, limit
            )
        
        else:  # AUTO
            # 优先尝试向量检索
            if self.vector_retriever.available:
                result = self.vector_retriever.retrieve(
                    material, volume_cm3, quantity,
                    complexity, tolerance, surface_treatment, limit
                )
                if result.success:
                    return result
            
            # 降级到规则匹配
            if self.config.get("fallback_to_rule", True):
                logger.info("向量检索不可用，降级到规则匹配")
                return self._rule_retrieve(
                    material, volume_cm3, quantity,
                    complexity, tolerance, surface_treatment, limit
                )
            
            return RetrievalResult(
                success=False,
                mode_used="none",
                avg_unit_price=None,
                min_unit_price=None,
                max_unit_price=None,
                confidence=0.0,
                cases_count=0,
                similar_cases=[],
                error="无可用的检索方式"
            )
    
    def _rule_retrieve(
        self,
        material: str,
        volume_cm3: float,
        quantity: int,
        complexity: str,
        tolerance: str,
        surface_treatment: str,
        limit: int
    ) -> RetrievalResult:
        """规则匹配检索"""
        try:
            result = self.rule_retriever.get_reference_price(
                material=material,
                volume_cm3=volume_cm3,
                quantity=quantity,
                complexity=complexity,
                tolerance=tolerance
            )
            
            return RetrievalResult(
                success=True,
                mode_used="rule",
                avg_unit_price=result['avg_unit_price'],
                min_unit_price=result['min_unit_price'],
                max_unit_price=result['max_unit_price'],
                confidence=result['confidence'],
                cases_count=result['cases_count'],
                similar_cases=result.get('similar_cases', [])
            )
        except Exception as e:
            logger.error(f"规则检索失败: {e}")
            return RetrievalResult(
                success=False,
                mode_used="rule",
                avg_unit_price=None,
                min_unit_price=None,
                max_unit_price=None,
                confidence=0.0,
                cases_count=0,
                similar_cases=[],
                error=str(e)
            )
    
    def _hybrid_retrieve(
        self,
        material: str,
        volume_cm3: float,
        quantity: int,
        complexity: str,
        tolerance: str,
        surface_treatment: str,
        limit: int
    ) -> RetrievalResult:
        """混合检索（规则+向量加权）"""
        rule_result = self._rule_retrieve(
            material, volume_cm3, quantity,
            complexity, tolerance, surface_treatment, limit
        )
        
        vector_result = self.vector_retriever.retrieve(
            material, volume_cm3, quantity,
            complexity, tolerance, surface_treatment, limit
        )
        
        # 如果向量不可用，直接返回规则结果
        if not vector_result.success:
            rule_result.mode_used = "hybrid (rule only)"
            return rule_result
        
        # 加权融合
        rule_weight = self.config.get("rule_weight", 0.5)
        vector_weight = self.config.get("vector_weight", 0.5)
        
        if rule_result.avg_unit_price and vector_result.avg_unit_price:
            hybrid_price = (
                rule_result.avg_unit_price * rule_weight +
                vector_result.avg_unit_price * vector_weight
            )
        else:
            hybrid_price = rule_result.avg_unit_price or vector_result.avg_unit_price
        
        return RetrievalResult(
            success=True,
            mode_used="hybrid",
            avg_unit_price=round(hybrid_price, 2) if hybrid_price else None,
            min_unit_price=min(
                filter(lambda x: x is not None,
                       [rule_result.min_unit_price, vector_result.min_unit_price]),
                default=None
            ),
            max_unit_price=max(
                filter(lambda x: x is not None,
                       [rule_result.max_unit_price, vector_result.max_unit_price]),
                default=None
            ),
            confidence=max(rule_result.confidence, vector_result.confidence),
            cases_count=max(rule_result.cases_count, vector_result.cases_count),
            similar_cases=rule_result.similar_cases[:3] + vector_result.similar_cases[:2]
        )
    
    def get_status(self) -> Dict:
        """获取检索器状态"""
        return {
            "mode": self.mode.value,
            "rule_retriever": {
                "available": True,
                "status": "✅ 可用"
            },
            "vector_retriever": {
                "available": self.vector_retriever.available,
                "status": "✅ 可用" if self.vector_retriever.available else "❌ 需要API Key"
            },
            "config": self.config
        }


# 测试代码
if __name__ == "__main__":
    print("=" * 60)
    print("混合检索器测试")
    print("=" * 60)
    
    # 初始化
    retriever = HybridRetriever(mode=RetrievalMode.AUTO)
    
    # 显示状态
    print("\n【检索器状态】")
    status = retriever.get_status()
    print(json.dumps(status, indent=2, ensure_ascii=False))
    
    # 测试检索
    print("\n【测试检索】")
    print("输入: AL6061, 100cm³, 10件, 简单, 普通")
    
    result = retriever.retrieve(
        material="AL6061",
        volume_cm3=100,
        quantity=10,
        complexity="简单",
        tolerance="普通"
    )
    
    print(f"\n检索结果:")
    print(f"  模式: {result.mode_used}")
    print(f"  成功: {result.success}")
    print(f"  平均单价: ¥{result.avg_unit_price}")
    print(f"  价格区间: ¥{result.min_unit_price} - ¥{result.max_unit_price}")
    print(f"  置信度: {result.confidence}")
    print(f"  案例数量: {result.cases_count}")
    
    if result.similar_cases:
        print(f"\n  相似案例:")
        for case in result.similar_cases[:3]:
            print(f"    - {case}")
    
    # 切换模式测试
    print("\n【切换模式测试】")
    retriever.set_mode(RetrievalMode.RULE_ONLY)
    print(f"当前模式: {retriever.mode.value}")