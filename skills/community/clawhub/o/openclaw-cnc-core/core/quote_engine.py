#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CNC 智能报价系统 - P0 报价引擎
版本：v1.2 (统一数据层集成)
功能：表面处理识别 + 成本计算 + RAG 历史修正 + 统一数据访问
"""

import json
import os
import logging
import sqlite3
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime
from enum import Enum

# 导入统一数据层
import sys
DATA_LAYER_PATH = os.path.expanduser("~/.openclaw/workspace/data")
if DATA_LAYER_PATH not in sys.path:
    sys.path.insert(0, DATA_LAYER_PATH)

try:
    from data_layer import get_data_layer, MaterialInfo, QuoteRecord
    UNIFIED_DATA_AVAILABLE = True
except ImportError:
    UNIFIED_DATA_AVAILABLE = False
    logging.warning("统一数据层不可用，使用本地配置")

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# ========== v3.2 新增：工艺难度系数 ==========
# 独立于几何复杂度，考虑材料特性和工艺约束
PROCESS_DIFFICULTY = {
    # 材料特性
    "material": {
        "钛合金TC4": 1.35,      # 刀具磨损极快，加工困难
        "钛合金TA1": 1.30,      # 纯钛，略软但仍难
        "不锈钢316": 1.20,      # 比304更难加工
        "不锈钢304": 1.10,      # 标准难度（已在K_Time体现，这里微调）
        "模具钢H13": 1.25,      # 硬度高，刀具损耗大
        "铜合金": 0.85,         # 软，易加工
        "黄铜": 0.80,           # 最易加工
        "铝合金6061": 0.90,     # 较易加工
        "铝合金7075": 1.05,     # 高强度铝，稍难
    },
    # 结构特性（几何相关但独立于复杂度）
    "structure": {
        "薄壁(<2mm)": 1.20,     # 易变形，需要小心
        "薄壁(<1mm)": 1.35,     # 极薄，难度大增
        "深孔(>5D)": 1.40,      # 排屑困难
        "深孔(>10D)": 1.60,     # 极深孔
        "细长轴(L/D>10)": 1.25, # 刚性差，易振动
        "异形腔": 1.15,         # 需要多轴联动
        "内螺纹": 1.10,         # 攻丝风险
        "外螺纹": 1.05,         # 相对简单
    },
    # 工艺约束
    "constraint": {
        "公差±0.01mm": 1.30,    # 超精密
        "公差±0.02mm": 1.20,    # 高精密
        "公差±0.05mm": 1.10,    # 精密
        "Ra<0.8": 1.15,         # 高光洁度要求
        "Ra<0.4": 1.25,         # 超高光洁度
        "同轴度<0.02": 1.20,    # 形位公差严格
    }
}


class DecisionFlag(Enum):
    """决策标志位"""
    NORMAL = "NORMAL"
    MANUAL_REVIEW_REQUIRED = "MANUAL_REVIEW_REQUIRED"
    PARTIAL_MATCH = "PARTIAL_MATCH"


@dataclass
class QuoteResult:
    """报价结果数据结构"""
    order_id: str
    customer: str
    material_cost: float
    machining_cost: float
    surface_cost: float
    total_price: float
    surface_type: str
    flag: DecisionFlag
    confidence: float
    reasoning: str
    created_at: str
    requires_manual_review: bool = False
    # v3.0-Plus 新增字段
    stock_info: dict = None  # 毛坯信息
    process_flow: str = ""   # Mermaid工艺流程图
    recommendations: list = None  # 工艺建议
    k_time: float = 1.0      # 应用的K_Time
    k_risk: float = 1.0      # 应用的K_Risk
    tool_wear_cost: float = 0.0  # 刀具损耗
    
    def to_dict(self) -> dict:
        """转换为字典 (用于 JSON 序列化)"""
        result = asdict(self)
        result['flag'] = self.flag.value
        return result


class LocalRuleEngine:
    """
    本地规则引擎 - 表面处理识别
    
    基于关键词匹配，支持多种匹配类型：
    - exact: 精确匹配 (权重 1.0)
    - partial: 部分匹配 (权重 0.7)
    - abbreviation: 缩写匹配 (权重 0.6)
    """
    
    KEYWORD_WEIGHTS = {
        "exact": 1.0,
        "partial": 0.7,
        "abbreviation": 0.6
    }
    
    def __init__(self, keywords_path: str):
        """
        初始化规则引擎
        
        Args:
            keywords_path: 关键词配置文件路径
        """
        self.keywords = self._load_keywords(keywords_path)
        logger.info(f"规则引擎初始化完成，加载了 {len(self.keywords)} 种表面处理类型")
    
    def _load_keywords(self, path: str) -> dict:
        """加载关键词配置"""
        if not os.path.exists(path):
            raise FileNotFoundError(f"关键词配置文件不存在：{path}")
        
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def recognize(self, text: str) -> Dict:
        """
        识别表面处理类型
        
        Args:
            text: 邮件原始文本
        
        Returns:
            {
                "surface_type": str,  # 识别结果
                "confidence": float,  # 置信度 0-1
                "matched_keywords": list,  # 匹配的关键词
                "match_details": list  # 详细匹配信息
            }
        """
        if not text:
            return {
                "surface_type": "UNKNOWN",
                "confidence": 0.0,
                "matched_keywords": [],
                "match_details": []
            }
        
        text_lower = text.lower()
        matches = []
        
        # 遍历所有表面处理类型和关键词
        for surface_type, keywords in self.keywords.items():
            for keyword_info in keywords:
                keyword = keyword_info["keyword"]
                weight_type = keyword_info["weight_type"]
                
                # 关键词匹配 (不区分大小写)
                if keyword.lower() in text_lower:
                    matches.append({
                        "surface_type": surface_type,
                        "keyword": keyword,
                        "weight_type": weight_type,
                        "weight": self.KEYWORD_WEIGHTS.get(weight_type, 0.5)
                    })
        
        if not matches:
            return {
                "surface_type": "UNKNOWN",
                "confidence": 0.0,
                "matched_keywords": [],
                "match_details": []
            }
        
        # 按表面处理类型分组统计得分
        type_scores = {}
        type_keywords = {}
        
        for match in matches:
            st = match["surface_type"]
            type_scores[st] = type_scores.get(st, 0) + match["weight"]
            
            if st not in type_keywords:
                type_keywords[st] = []
            type_keywords[st].append(match["keyword"])
        
        # 选出最高分的表面处理类型
        best_type = max(type_scores, key=type_scores.get)
        best_score = type_scores[best_type]
        
        # 置信度计算：归一化到 0-1 (假设最高可能得分为 3.0)
        # 多个关键词匹配会提高置信度
        confidence = min(best_score / 3.0, 1.0)
        
        # 如果有多个关键词匹配同一种类型，适当提升置信度
        keyword_count = len(type_keywords[best_type])
        if keyword_count > 1:
            confidence = min(confidence * (1 + 0.1 * (keyword_count - 1)), 1.0)
        
        return {
            "surface_type": best_type,
            "confidence": round(confidence, 3),
            "matched_keywords": type_keywords[best_type],
            "match_details": [m for m in matches if m["surface_type"] == best_type]
        }


class OpenClawQuoteEngine:
    """
    CNC 报价引擎 - P0 版本 + v3.0-Plus 增强
    
    核心功能:
    1. 材料费计算
    2. 加工费计算
    3. 表面处理费计算
    4. 异常检测与人工审核标记
    
    v3.0-Plus 增强:
    5. 知识库补偿因子 (K_Time, K_Risk)
    6. 刀具损耗附加费
    7. 毛坯自动计算
    8. Mermaid 工艺流程图
    """
    
    def __init__(self, config_dir: str, db_path: str = None):
        """
        初始化报价引擎
        
        Args:
            config_dir: 配置文件目录
            db_path: SQLite 数据库路径 (用于 RAG 和历史记录)
        """
        self.config_dir = config_dir
        
        # 加载配置
        self.rule_engine = LocalRuleEngine(
            os.path.join(config_dir, "surface_keywords.json")
        )
        self.surface_pricing = self._load_json("surface_pricing.json")
        self.material_pricing = self._load_json("material_pricing.json")
        self.machining_rules = self._load_json("machining_rules.json")
        
        # 初始化数据库 (RAG + 历史记录)
        if db_path is None:
            db_path = os.path.join(os.path.dirname(config_dir), "database", "risk_control.db")
        self.db_path = db_path
        self._init_database()
        
        # ========== v3.0-Plus 新增：延迟加载模块 ==========
        self._kb_bridge = None
        self._process_planner = None
        
        logger.info(f"报价引擎初始化完成 | 数据库：{self.db_path}")
    
    def _ensure_v3_modules(self):
        """延迟加载 v3.0-Plus 模块 (节省内存)"""
        if self._kb_bridge is None:
            try:
                from modules.knowledge_bridge import KnowledgeBridge
                kb_path = os.path.join(self.config_dir, "kb")
                self._kb_bridge = KnowledgeBridge(kb_path)
                logger.info("v3.0-Plus 知识库模块加载成功")
            except Exception as e:
                logger.warning(f"v3.0-Plus 知识库模块加载失败: {e}")
                self._kb_bridge = False  # 标记为不可用
        
        if self._process_planner is None:
            try:
                from modules.process_planner import ProcessPlanner
                self._process_planner = ProcessPlanner()
                logger.info("v3.0-Plus 工艺规划模块加载成功")
            except Exception as e:
                logger.warning(f"v3.0-Plus 工艺规划模块加载失败: {e}")
                self._process_planner = False  # 标记为不可用
    
    def _get_material_compensation(self, material: str) -> Dict:
        """
        获取材料补偿因子 (v3.0-Plus + 损耗系数)
        优先使用统一数据层，降级到本地配置
        
        Returns:
            {
                'K_Time': float,
                'K_Risk': float,
                'tool_cost_per_hour': float,
                'material_name': str,
                'density': float,
                'price_per_kg': float,
                'loss_factor': float,
                'waste_factor': float  # 新增：材料损耗系数
            }
        """
        # 优先使用统一数据层
        if UNIFIED_DATA_AVAILABLE:
            try:
                dl = get_data_layer()
                mat_info = dl.get_material(material)
                if mat_info:
                    logger.info(f"从统一数据层获取材料: {material} -> {mat_info.name}")
                    return {
                        'K_Time': mat_info.k_time,
                        'K_Risk': mat_info.k_risk,
                        'tool_cost_per_hour': mat_info.tool_wear_cost,
                        'material_name': mat_info.name,
                        'density': mat_info.density,
                        'price_per_kg': mat_info.price_per_kg,
                        'loss_factor': mat_info.loss_factor,
                        'waste_factor': mat_info.waste_factor  # 新增
                    }
            except Exception as e:
                logger.warning(f"统一数据层查询失败: {e}，降级到本地配置")
        
        # 降级：使用v3.0-Plus本地模块
        self._ensure_v3_modules()
        
        if self._kb_bridge:
            material_code = self._kb_bridge.resolve_material_code(material)
            factors = self._kb_bridge.get_compensation_factors(material_code)
            factors['waste_factor'] = 1.15  # 默认值
            return factors
        
        # 最终降级：默认值
        return {
            'K_Time': 1.0,
            'K_Risk': 1.0,
            'tool_cost_per_hour': 0.0,
            'material_name': material,
            'density': 2.7,
            'price_per_kg': 25.0,
            'loss_factor': 1.0,
            'waste_factor': 1.15
        }
    
    def _calculate_process_difficulty(self, order_data: dict) -> float:
        """
        计算工艺难度系数 (v3.2新增)
        
        独立于几何复杂度，考虑：
        1. 材料加工特性
        2. 结构约束（薄壁、深孔等）
        3. 工艺要求（公差、光洁度等）
        
        Returns:
            float: 工艺难度系数 (0.8-2.0)
        """
        process_difficulty = 1.0
        applied_factors = []
        
        # 1. 材料特性
        material = order_data.get("material", "")
        material_factor = 1.0
        
        for mat_key, factor in PROCESS_DIFFICULTY["material"].items():
            if mat_key in material:
                material_factor = factor
                applied_factors.append(f"材料:{mat_key}={factor:.2f}")
                break
        
        process_difficulty *= material_factor
        
        # 2. 结构特性
        # 检查薄壁
        wall_thickness = order_data.get("min_wall_thickness")
        if wall_thickness:
            if wall_thickness < 1.0:
                process_difficulty *= 1.35
                applied_factors.append(f"薄壁<{wall_thickness}mm=1.35")
            elif wall_thickness < 2.0:
                process_difficulty *= 1.20
                applied_factors.append(f"薄壁<{wall_thickness}mm=1.20")
        
        # 检查深孔（如果有孔径和深度信息）
        hole_depth_ratio = order_data.get("max_hole_depth_ratio", 0)
        if hole_depth_ratio > 10:
            process_difficulty *= 1.60
            applied_factors.append(f"深孔>{10}D=1.60")
        elif hole_depth_ratio > 5:
            process_difficulty *= 1.40
            applied_factors.append(f"深孔>{5}D=1.40")
        
        # 检查细长轴
        aspect_ratio = order_data.get("aspect_ratio", 0)
        if aspect_ratio > 10:
            process_difficulty *= 1.25
            applied_factors.append(f"细长轴L/D={aspect_ratio:.1f}=1.25")
        
        # 检查特征数量（孔、槽、螺纹）
        feature_count = order_data.get("hole_count", 0) + order_data.get("slot_count", 0)
        if feature_count > 20:
            process_difficulty *= 1.10
            applied_factors.append(f"特征多={feature_count}=1.10")
        
        # 3. 工艺约束 - 注意：公差已在tolerance_surcharge中计算，这里不再重复
        # 仅考虑光洁度要求（独立于公差）
        surface_roughness = order_data.get("surface_roughness")
        if surface_roughness:
            if surface_roughness < 0.4:
                process_difficulty *= 1.25
                applied_factors.append(f"Ra<{surface_roughness}=1.25")
            elif surface_roughness < 0.8:
                process_difficulty *= 1.15
                applied_factors.append(f"Ra<{surface_roughness}=1.15")
        
        # 设置上限，避免过度叠加
        MAX_PROCESS_DIFFICULTY = 2.0
        process_difficulty = min(process_difficulty, MAX_PROCESS_DIFFICULTY)
        
        if applied_factors:
            logger.info(f"v3.2 工艺难度: {' | '.join(applied_factors)} → 系数 {process_difficulty:.2f}")
        
        return process_difficulty
    
    def _init_database(self):
        """初始化数据库表结构 (如果不存在)"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 材料表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS materials (
                name TEXT PRIMARY KEY,
                density REAL,
                price_per_kg REAL,
                category TEXT
            )
        ''')
        
        # 历史报价表 (RAG 数据源)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS history (
                id INTEGER PRIMARY KEY,
                part_id TEXT,
                material TEXT,
                volume REAL,
                quantity INTEGER,
                final_price REAL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # 报价记录表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS quotes (
                id INTEGER PRIMARY KEY,
                part_id TEXT,
                material TEXT,
                quantity INTEGER,
                volume REAL,
                weight_kg REAL,
                material_cost REAL,
                machining_cost REAL,
                surface_cost REAL,
                total_price REAL,
                rag_factor REAL,
                status TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def _calculate_rag_factor(self, material: str, volume: float, quantity: int, 
                                complexity: str = None, tolerance: str = None) -> Tuple[float, Dict]:
        """
        计算 RAG 修正因子 (基于混合检索：规则+向量)
        
        v2.0 升级：使用 HybridRetriever 统一检索
        - 规则匹配：立即可用，基于材料/体积/数量区间匹配
        - 向量检索：需要API Key，语义相似度匹配
        - 自动降级：向量不可用时自动使用规则
        
        Args:
            material: 材料名称
            volume: 体积 (cm³)
            quantity: 数量
            complexity: 复杂度 (可选)
            tolerance: 公差等级 (可选)
        
        Returns:
            (RAG修正因子, 检索详情)
        """
        try:
            # 导入混合检索器
            from hybrid_retriever import HybridRetriever, RetrievalMode
            
            # 初始化检索器 (AUTO模式：优先向量，降级规则)
            retriever = HybridRetriever(mode=RetrievalMode.AUTO)
            
            # 执行检索
            result = retriever.retrieve(
                material=material,
                volume_cm3=volume,
                quantity=quantity,
                complexity=complexity,
                tolerance=tolerance
            )
            
            if not result.success or result.avg_unit_price is None:
                logger.debug("未找到相似历史报价，使用默认 RAG 因子 1.0")
                return 1.0, {"mode": result.mode_used, "cases": 0}
            
            # 计算参考价格与当前预估的比例
            # 注意：这里需要当前预估价格来计算比例
            # 目前返回历史平均价格，让调用方计算因子
            
            # 检索详情
            details = {
                "mode": result.mode_used,
                "cases": result.cases_count,
                "avg_unit_price": result.avg_unit_price,
                "price_range": [result.min_unit_price, result.max_unit_price],
                "confidence": result.confidence,
                "similar_cases": result.similar_cases[:3]
            }
            
            # RAG因子计算策略：
            # - 置信度高(>0.7)：历史价格权重更大
            # - 置信度中(0.5-0.7)：历史价格作为参考
            # - 置信度低(<0.5)：历史价格仅供参考，主要用规则
            
            if result.confidence >= 0.7:
                rag_factor = 0.85  # 历史价格权重 15%
            elif result.confidence >= 0.5:
                rag_factor = 0.92  # 历史价格权重 8%
            else:
                rag_factor = 0.97  # 历史价格权重 3%
            
            logger.info(f"RAG 修正[{result.mode_used}]：{result.cases_count}条案例，"
                       f"参考价¥{result.avg_unit_price}，置信度{result.confidence}，因子={rag_factor:.2f}")
            
            return rag_factor, details
            
        except ImportError:
            logger.warning("HybridRetriever 不可用，使用传统 RAG 方法")
            return self._calculate_rag_factor_legacy(material, volume, quantity)
        except Exception as e:
            logger.error(f"RAG 因子计算失败：{e}")
            return 1.0, {"error": str(e)}
    
    def _calculate_rag_factor_legacy(self, material: str, volume: float, quantity: int) -> Tuple[float, Dict]:
        """
        传统 RAG 方法 (备用)
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            volume_tolerance = volume * 0.5 if volume > 0 else 10
            cursor.execute('''
                SELECT final_price, volume, quantity
                FROM history
                WHERE material = ?
                AND volume BETWEEN ? AND ?
                AND quantity BETWEEN ? AND ?
                ORDER BY created_at DESC
                LIMIT 10
            ''', (
                material,
                max(0, volume - volume_tolerance),
                volume + volume_tolerance,
                max(1, quantity - 5),
                quantity + 5
            ))
            
            similar_quotes = cursor.fetchall()
            conn.close()
            
            if not similar_quotes:
                return 1.0, {"mode": "legacy", "cases": 0}
            
            avg_price = sum(q[0] for q in similar_quotes) / len(similar_quotes)
            
            return 1.0, {
                "mode": "legacy", 
                "cases": len(similar_quotes),
                "avg_unit_price": avg_price
            }
            
        except Exception as e:
            logger.error(f"传统 RAG 计算失败：{e}")
            return 1.0, {"error": str(e)}
    
    def _save_quote_record(self, order_data: dict, result: QuoteResult):
        """保存报价记录到数据库 (用于 RAG 训练) - v1.2 统一数据层版"""
        
        # 1. 保存到统一数据库
        if UNIFIED_DATA_AVAILABLE:
            try:
                dl = get_data_layer()
                record = QuoteRecord(
                    order_id=order_data.get('order_id', 'UNKNOWN'),
                    material=order_data.get('material', '未知'),
                    volume=order_data.get('volume_cm3', 0),
                    quantity=order_data.get('quantity', 1),
                    material_cost=result.material_cost,
                    machining_cost=result.machining_cost,
                    surface_cost=result.surface_cost,
                    total_price=result.total_price,
                    source=order_data.get('source', 'web')
                )
                dl.save_quote(record)
                logger.info(f"报价记录已保存到统一数据库：{order_data.get('order_id')}")
            except Exception as e:
                logger.warning(f"统一数据库保存失败: {e}")
        
        # 2. 同时保存到本地数据库 (兼容旧逻辑)
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO quotes (
                    part_id, material, quantity, volume, weight_kg,
                    material_cost, machining_cost, surface_cost,
                    total_price, rag_factor, status
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                order_data.get('part_name', order_data.get('order_id')),
                order_data.get('material', '未知'),
                order_data.get('quantity', 1),
                order_data.get('volume_cm3', 0),
                order_data.get('volume_cm3', 0) * 0.0078,  # 估算重量
                result.material_cost,
                result.machining_cost,
                result.surface_cost,
                result.total_price,
                1.0,  # RAG 因子
                'completed' if not result.requires_manual_review else 'pending_review'
            ))
            
            # 同时保存到历史表 (用于 RAG 检索)
            if not result.requires_manual_review:
                cursor.execute('''
                    INSERT INTO history (part_id, material, volume, quantity, final_price)
                    VALUES (?, ?, ?, ?, ?)
                ''', (
                    order_data.get('part_name', order_data.get('order_id')),
                    order_data.get('material', '未知'),
                    order_data.get('volume_cm3', 0),
                    order_data.get('quantity', 1),
                    result.total_price
                ))
            
            conn.commit()
            conn.close()
            logger.info(f"报价记录已保存：{order_data.get('order_id')}")
        
        except Exception as e:
            logger.error(f"保存报价记录失败：{e}")
    
    def _load_json(self, filename: str) -> dict:
        """加载 JSON 配置文件"""
        path = os.path.join(self.config_dir, filename)
        if not os.path.exists(path):
            raise FileNotFoundError(f"配置文件不存在：{path}")
        
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def calculate_quote(self, order_data: dict) -> QuoteResult:
        """
        计算报价 - 主入口
        
        Args:
            order_data: 订单数据
                {
                    "order_id": str,
                    "customer": str,
                    "material": str,  # 如 "铝 6061"
                    "volume_cm3": float,
                    "area_dm2": float,  # 表面积 (平方分米)
                    "quantity": int,
                    "machine_type": str,  # 如 "3 轴加工中心"
                    "complexity": str,  # 如 "中等"
                    "urgency": str,  # 如 "标准交期"
                    "raw_text": str,  # 原始邮件文本
                    "surface_color": str = None,  # 可选：颜色要求
                    "surface_type_hint": str = None  # 可选：表面处理提示
                }
        
        Returns:
            QuoteResult 报价结果
        """
        # ========== 步骤 1: 识别表面处理类型 ==========
        surface_result = self.rule_engine.recognize(order_data.get("raw_text", ""))
        surface_type = surface_result["surface_type"]
        surface_confidence = surface_result["confidence"]
        
        # ========== 步骤 2: 异常检测 - 关键风险控制点 ==========
        if surface_type == "UNKNOWN":
            # 🔴 未识别到表面处理类型，必须标记人工审核
            logger.warning(f"订单 {order_data.get('order_id')}: 表面处理类型未识别，标记人工审核")
            
            return QuoteResult(
                order_id=order_data.get("order_id", "UNKNOWN"),
                customer=order_data.get("customer", "未知客户"),
                material_cost=0,
                machining_cost=0,
                surface_cost=0,
                total_price=0,
                surface_type="UNKNOWN",
                flag=DecisionFlag.MANUAL_REVIEW_REQUIRED,
                confidence=0.0,
                reasoning="表面处理类型未识别，需人工审核",
                created_at=datetime.now().isoformat(),
                requires_manual_review=True
            )
        
        # ========== 步骤 3: 计算材料费 ==========
        material_cost_per_piece = self._calculate_material_cost(order_data)
        quantity = order_data.get("quantity", 1)
        material_cost = material_cost_per_piece * quantity  # 材料费 = 单件 × 数量
        
        # ========== 步骤 4: 计算加工费 ==========
        machining_cost_per_piece = self._calculate_machining_cost(order_data)
        
        # v3.2-GLM: 开机费全额计入单件基准价
        # 批量总价 = 单件基准价 × 数量 × 批量折扣
        # 不再把开机费单独处理，而是包含在单件基准价中
        machining_cost = machining_cost_per_piece * quantity
        
        # ========== v3.0-Plus: 获取知识库补偿因子 ==========
        material = order_data.get("material", "默认")
        compensation = self._get_material_compensation(material)
        k_time = compensation.get('K_Time', 1.0)
        k_risk = compensation.get('K_Risk', 1.0)
        
        # ========== v3.1: 复杂度和公差系数 ==========
        complexity = order_data.get('complexity', '中等')
        complexity_factor = {'中等': 1.0, '复杂': 1.8, '高复杂': 2.2}.get(complexity, 1.0)
        
        tolerance = order_data.get('tolerance', '普通')
        tolerance_surcharge = {'普通': 1.0, '精密': 1.15, '超精密': 1.30}.get(tolerance, 1.0)
        
        # ========== v3.2: 工艺难度系数 ==========
        process_difficulty = self._calculate_process_difficulty(order_data)
        
        # 应用工艺难度系数到加工费
        # 注意：K_Time和K_Risk已在_calculate_machining_cost中体现，这里只应用工艺难度
        adjusted_machining_cost = machining_cost * process_difficulty
        
        # 刀具损耗附加费
        machining_hours = self._estimate_machining_hours(order_data)
        tool_wear_cost = compensation.get('tool_cost_per_hour', 0.0) * machining_hours
        
        logger.info(f"v3.2 补偿: K_Time={k_time}, K_Risk={k_risk}, "
                   f"复杂度={complexity_factor}, 公差={tolerance_surcharge}, 工艺难度={process_difficulty:.2f}, "
                   f"加工费 {machining_cost:.2f} → {adjusted_machining_cost:.2f}, "
                   f"刀具损耗 ¥{tool_wear_cost:.2f}")
        
        # 使用调整后的加工费
        machining_cost = adjusted_machining_cost
        
        # ========== 步骤 5: 计算表面处理费 ==========
        surface_cost = self._calculate_surface_cost(
            surface_type=surface_type,
            area_dm2=order_data.get("area_dm2", 0),
            color=order_data.get("surface_color"),
            quantity=order_data.get("quantity", 1)
        )
        
        # ========== 步骤 6: 计算总价 (含刀具损耗) ==========
        subtotal = material_cost + machining_cost + surface_cost + tool_wear_cost
        
        # ========== v3.1 新增：风险溢价与管理费 ==========
        # 批量折扣
        batch_discount = self._get_batch_discount(order_data.get("quantity", 1))
        
        # v3.2修正：小件(体积<100cm³)不乘附加费，直接用基础价
        volume_cm3 = order_data.get("volume_cm3", 0)
        if volume_cm3 < 100:  # 小件
            # 小件：基础价 × 批量折扣
            total_price = subtotal * batch_discount
            logger.info(f"v3.2 小件报价: 基础价¥{subtotal:.2f} × 批量折扣{batch_discount:.1f} = ¥{total_price:.2f}")
        else:
            # 大件：基础价 × 附加费 × 批量折扣
            # 大型件风险溢价
            risk_premium = 0.0
            if volume_cm3 > 1000:
                risk_premium = 0.10
            if volume_cm3 > 2000:
                risk_premium = 0.15
            
            # 管理费
            management_fee = 0.08
            
            # 利润率
            profit_margin = 0.12
            
            total_price = subtotal * (1 + risk_premium + management_fee + profit_margin) * batch_discount
            logger.info(f"v3.1 大件附加费: 风险溢价={risk_premium*100:.0f}%, 管理费={management_fee*100:.0f}%, 利润率={profit_margin*100:.0f}%")
        logger.info(f"小计: ¥{subtotal:.2f} → 总价: ¥{total_price:.2f}")
        
        # 加急费用
        urgency_surcharge = self._get_urgency_surcharge(order_data.get("urgency", "标准交期"))
        total_price = total_price * urgency_surcharge
        
        # 最低订单金额检查
        min_order = self.machining_rules.get("minimum_order", {}).get("amount", 100)
        if total_price < min_order:
            total_price = min_order
        
        # ========== 步骤 7: 判断是否需要人工审核 ==========
        # 置信度低的情况也需要人工审核
        requires_manual_review = surface_confidence < 0.5
        flag = DecisionFlag.MANUAL_REVIEW_REQUIRED if requires_manual_review else DecisionFlag.NORMAL
        
        if requires_manual_review:
            logger.warning(
                f"订单 {order_data.get('order_id')}: "
                f"表面处理识别置信度低 ({surface_confidence:.2f})，标记人工审核"
            )
        
        # ========== v3.0-Plus 新增: 计算毛坯和工艺流程 ==========
        stock_info = None
        process_flow = ""
        recommendations = []
        
        if self._process_planner and not requires_manual_review:
            try:
                # 从订单数据提取零件尺寸
                volume_cm3 = order_data.get("volume_cm3", 100)
                area_dm2 = order_data.get("area_dm2", 20)
                
                # 估算零件尺寸 (假设立方体)
                side = (volume_cm3 * 1000) ** (1/3)  # mm
                part_dims = {
                    'L': order_data.get('length_mm', side * 1.2),
                    'W': order_data.get('width_mm', side * 0.8),
                    'H': order_data.get('height_mm', side * 0.5)
                }
                
                # 零件特征
                part_features = {
                    'is_complex': order_data.get('complexity', '中等') == '复杂',
                    'has_threads': False,  # 可从订单扩展
                    'has_surface': surface_cost > 0,
                    'surface_req': surface_type,
                    'tight_tolerance': False
                }
                
                plan_result = self._process_planner.plan_execution(
                    part_dims, part_features, compensation
                )
                
                stock_info = plan_result['stock_info']
                process_flow = plan_result['process_flow']
                recommendations = plan_result['recommendations']
                
            except Exception as e:
                logger.warning(f"工艺规划计算失败: {e}")
        
        # ========== 步骤 8: 构建报价结果 ==========
        reasoning_parts = [
            f"表面处理：{surface_type} (置信度：{surface_confidence:.2f})",
            f"匹配关键词：{', '.join(surface_result['matched_keywords'])}",
            f"材料费：¥{material_cost:.2f}",
            f"加工费：¥{machining_cost:.2f}",
            f"表面处理费：¥{surface_cost:.2f}",
        ]
        
        if batch_discount < 1.0:
            reasoning_parts.append(f"批量折扣：{batch_discount:.1f}折")
        if urgency_surcharge > 1.0:
            reasoning_parts.append(f"加急费用：x{urgency_surcharge}")
        
        return QuoteResult(
            order_id=order_data.get("order_id", "UNKNOWN"),
            customer=order_data.get("customer", "未知客户"),
            material_cost=round(material_cost, 2),
            machining_cost=round(machining_cost, 2),
            surface_cost=round(surface_cost, 2),
            total_price=round(total_price, 2),
            surface_type=surface_type,
            flag=flag,
            confidence=round(surface_confidence, 3),
            reasoning="; ".join(reasoning_parts),
            created_at=datetime.now().isoformat(),
            requires_manual_review=requires_manual_review,
            stock_info=stock_info,
            process_flow=process_flow,
            recommendations=recommendations,
            k_time=k_time,
            k_risk=k_risk,
            tool_wear_cost=round(tool_wear_cost, 2)
        )
    
    def _calculate_material_cost(self, order_data: dict) -> float:
        """
        计算材料费 (v1.2 统一数据层版 + 损耗系数)
        
        公式：材料费 = 材料单价 (元/kg) × 材料用量 (kg) × 损耗系数
        材料用量 = 体积 (cm³) × 密度 (g/cm³) / 1000
        
        优先使用统一数据层的 calculate_material_cost 函数
        """
        material = order_data.get("material", "默认")
        volume_cm3 = order_data.get("volume_cm3", 0)
        
        # 优先使用统一数据层的材料费计算函数
        if UNIFIED_DATA_AVAILABLE:
            try:
                from data_layer import calculate_material_cost
                cost = calculate_material_cost(volume_cm3, material)
                logger.info(f"材料费计算: {material} {volume_cm3}cm³ → ¥{cost:.2f}")
                return cost
            except Exception as e:
                logger.warning(f"统一数据层计算失败: {e}，使用本地计算")
        
        # 降级：本地计算
        compensation = self._get_material_compensation(material)
        density = compensation.get('density', 2.7)
        price_per_kg = compensation.get('price_per_kg', 25.0)
        waste_factor = compensation.get('waste_factor', 1.15)
        
        # 计算重量 (kg)
        weight_kg = volume_cm3 * density / 1000
        
        # 计算材料费 (含损耗系数)
        material_cost = price_per_kg * weight_kg * waste_factor
        
        logger.debug(f"材料费计算：{material} {volume_cm3}cm³ × {density}g/cm³ = {weight_kg}kg × ¥{price_per_kg}/kg × {waste_factor} = ¥{material_cost:.2f}")
        return material_cost
    
    def _parse_material(self, material: str) -> Tuple[str, str]:
        """
        解析材料字符串
        
        Args:
            material: 如 "铝 6061", "不锈钢 304", "45#钢"
        
        Returns:
            (材料类型，牌号)
        """
        material = material.strip()
        
        # 常见材料类型映射
        material_mapping = {
            "铝": "铝合金",
            "铝合金": "铝合金",
            "铝材": "铝合金",
            "不锈钢": "不锈钢",
            "钢": "碳钢",
            "碳钢": "碳钢",
            "45#钢": "碳钢",
            "黄铜": "黄铜",
            "铜": "紫铜",
            "紫铜": "紫铜",
            "abs": "ABS 塑料",
            "pom": "POM",
            "尼龙": "尼龙",
        }
        
        # 提取材料类型
        material_type = "默认"
        for key, value in material_mapping.items():
            if key in material:
                material_type = value
                break
        
        # 提取牌号
        grade = "默认"
        if "6061" in material:
            grade = "6061"
        elif "6063" in material:
            grade = "6063"
        elif "7075" in material:
            grade = "7075"
        elif "304" in material:
            grade = "304"
        elif "316" in material:
            grade = "316"
        elif "45#" in material or "45 号" in material:
            grade = "45#钢"
        elif "H59" in material:
            grade = "H59"
        elif "H62" in material:
            grade = "H62"
        
        return material_type, grade
    
    def _calculate_machining_cost(self, order_data: dict) -> float:
        """
        计算加工费 - 重构版 (v2.0)
        
        公式：加工费 = 固定开机费(全额计入单件) + 可变工时费
        
        关键改进：
        - 固定开机费全额计入单件基准价，不进行均摊
        - 这样才能完美拟合真实报价的陡峭下降曲线
        """
        volume_cm3 = order_data.get("volume_cm3", 0)
        area_dm2 = order_data.get("area_dm2", 0)
        machine_type = order_data.get("machine_type", "3轴加工中心")
        complexity = order_data.get("complexity", "中等")
        
        # 获取固定开机费 (核心参数)
        setup_cost = self.machining_rules.get("base_setup_cost", 180.0)
        
        # 获取机床时薪
        hourly_rates = self.machining_rules.get("hourly_rate", {})
        hourly_rate = hourly_rates.get(machine_type, hourly_rates.get("默认", 80))
        
        # 获取复杂度因子
        complexity_factors = self.machining_rules.get("complexity_factors", {})
        complexity_factor = complexity_factors.get(complexity, 1.0)
        
        # 估算加工时间 (分钟)
        time_config = self.machining_rules.get("machining_time_estimation", {})
        base_time = time_config.get("base_time_minutes", 30)
        volume_coeff = time_config.get("volume_coefficient", 0.5)
        area_coeff = time_config.get("area_coefficient", 0.02)
        
        machining_time_minutes = base_time + (volume_cm3 * volume_coeff) + (area_dm2 * area_coeff)
        machining_time_hours = machining_time_minutes / 60
        
        # 可变工时费
        variable_cost = machining_time_hours * hourly_rate * complexity_factor
        
        # 总加工费 = 固定开机费 + 可变工时费
        machining_cost = setup_cost + variable_cost
        
        logger.debug(
            f"加工费计算：开机费¥{setup_cost} + 工时费¥{variable_cost:.2f} ({machine_type} {complexity} {machining_time_minutes:.1f}分钟) → ¥{machining_cost:.2f}"
        )
        return machining_cost
    
    def _calculate_surface_cost(self, surface_type: str, area_dm2: float, 
                                 color: Optional[str] = None, quantity: int = 1) -> float:
        """
        计算表面处理费
        
        公式：表面处理费 = (基础单价 + 颜色附加 + 类型附加) × 面积 × 数量系数
        
        Args:
            surface_type: 表面处理类型
            area_dm2: 表面积 (平方分米)
            color: 颜色要求
            quantity: 数量
        """
        pricing = self.surface_pricing.get(surface_type)
        
        if not pricing:
            logger.warning(f"未知表面处理类型：{surface_type}")
            return 0.0
        
        base_price = pricing.get("base_price", 0)
        min_charge = pricing.get("min_charge", 0)
        
        # 颜色附加费
        color_surcharge = 0
        if color:
            color_surcharges = pricing.get("color_surcharge", {})
            # 模糊匹配颜色
            for color_key, surcharge in color_surcharges.items():
                if color_key in color or color in color_key:
                    color_surcharge = surcharge
                    break
        
        # 类型附加费 (简化处理，使用基础类型)
        type_surcharge = 0
        type_surcharges = pricing.get("type_surcharge", {})
        if type_surcharges:
            # 默认使用第一个 (通常是基础类型)
            type_surcharge = list(type_surcharges.values())[0] if type_surcharges else 0
        
        # 计算单件费用
        unit_price = base_price + color_surcharge + type_surcharge
        surface_cost = unit_price * area_dm2
        
        # 最低收费检查
        if surface_cost < min_charge:
            surface_cost = min_charge
        
        # 多件优惠 (第二件起 8 折)
        if quantity > 1:
            surface_cost = surface_cost + surface_cost * 0.8 * (quantity - 1)
        
        logger.debug(
            f"表面处理费计算：{surface_type} {area_dm2}dm² x{quantity} → ¥{surface_cost:.2f}"
        )
        return surface_cost
    
    def _get_batch_discount(self, quantity: int) -> float:
        """
        获取批量折扣系数 - 重构版 (v2.0)
        
        匹配真实折扣区间（字符串键兼容运营复制粘贴）
        新的折扣阶梯更符合CNC行业"起步门槛高、边际成本低"的特点
        """
        batch_rules = self.machining_rules.get("batch_discount", {})
        
        # 遍历所有折扣规则，解析区间
        for key, discount in batch_rules.items():
            key_clean = key.replace("件", "").strip()
            
            # 处理区间格式 (如 "3-5", "6-10")
            if "-" in key_clean and "以上" not in key_clean:
                try:
                    parts = key_clean.split("-")
                    min_q = int(parts[0])
                    max_q = int(parts[1])
                    if min_q <= quantity <= max_q:
                        return discount
                except (ValueError, IndexError):
                    continue
            
            # 处理"以上"格式 (如 "51件以上")
            elif "以上" in key_clean:
                try:
                    min_q = int(key_clean.replace("以上", ""))
                    if quantity >= min_q:
                        return discount
                except ValueError:
                    continue
        
        # 默认无折扣
        return 1.0
    
    def _get_urgency_surcharge(self, urgency: str) -> float:
        """获取加急费用系数"""
        surcharges = self.machining_rules.get("urgency_surcharge", {})
        return surcharges.get(urgency, surcharges.get("标准交期", 1.0))
    
    def _estimate_machining_hours(self, order_data: dict) -> float:
        """
        估算加工工时 (小时) - v3.0-Plus 新增
        
        公式: 基础时间 + 体积系数 × 体积 + 面积系数 × 面积
        """
        volume_cm3 = order_data.get("volume_cm3", 0)
        area_dm2 = order_data.get("area_dm2", 0)
        complexity = order_data.get("complexity", "中等")
        
        # 获取时间估算参数
        time_config = self.machining_rules.get("machining_time_estimation", {})
        base_time = time_config.get("base_time_minutes", 30)
        vol_coef = time_config.get("volume_coefficient", 0.5)
        area_coef = time_config.get("area_coefficient", 0.02)
        
        # 复杂度因子
        complexity_factors = self.machining_rules.get("complexity_factors", {})
        complexity_factor = complexity_factors.get(complexity, 1.0)
        
        # 计算工时 (分钟)
        total_minutes = base_time + volume_cm3 * vol_coef + area_dm2 * 10 * area_coef
        total_minutes *= complexity_factor
        
        # 转换为小时
        return total_minutes / 60.0


# ========== 测试代码 ==========

if __name__ == "__main__":
    # 测试报价引擎
    config_dir = os.path.join(os.path.dirname(__file__), "config")
    engine = OpenClawQuoteEngine(config_dir)
    
    # 测试订单 1 - 正常识别
    order1 = {
        "order_id": "TEST-001",
        "customer": "测试客户 A",
        "material": "铝 6061",
        "volume_cm3": 100,
        "area_dm2": 20,
        "quantity": 10,
        "machine_type": "3 轴加工中心",
        "complexity": "中等",
        "urgency": "标准交期",
        "raw_text": "需要阳极氧化处理，黑色，用于航空零件",
        "surface_color": "黑色"
    }
    
    result1 = engine.calculate_quote(order1)
    print("\n=== 测试订单 1 (正常识别) ===")
    print(json.dumps(result1.to_dict(), indent=2, ensure_ascii=False))
    
    # 测试订单 2 - UNKNOWN 情况
    order2 = {
        "order_id": "TEST-002",
        "customer": "测试客户 B",
        "material": "不锈钢 304",
        "volume_cm3": 50,
        "area_dm2": 10,
        "quantity": 5,
        "machine_type": "3 轴加工中心",
        "complexity": "简单",
        "urgency": "标准交期",
        "raw_text": "需要表面防护处理，具体要求待定",
    }
    
    result2 = engine.calculate_quote(order2)
    print("\n=== 测试订单 2 (UNKNOWN - 需人工审核) ===")
    print(json.dumps(result2.to_dict(), indent=2, ensure_ascii=False))
    
    # 测试订单 3 - 低置信度
    order3 = {
        "order_id": "TEST-003",
        "customer": "测试客户 C",
        "material": "铝 6061",
        "volume_cm3": 200,
        "area_dm2": 30,
        "quantity": 1,
        "machine_type": "3 轴加工中心",
        "complexity": "复杂",
        "urgency": "加急 (3 天)",
        "raw_text": "表面做氧化处理",  # 只匹配到"氧化"，置信度较低
    }
    
    result3 = engine.calculate_quote(order3)
    print("\n=== 测试订单 3 (低置信度 - 需人工审核) ===")
    print(json.dumps(result3.to_dict(), indent=2, ensure_ascii=False))
