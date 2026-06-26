"""
Neuro-α - 类脑分区AI助手
============================

Neuro-α 是一个模拟人脑分区架构的 AI 助手系统。

架构设计：
    左脑区（情绪感知）：情绪检测 → 共情生成 → 胶囊工厂
    右脑区（逻辑处理）：意图分类 → 逻辑解析 → 方案生成
    颞叶区（深度记忆）：短期记忆 → 长期记忆 → 向量检索
    前额叶区（执行控制）：权重分配 → 审核监控 → 融合输出
    边缘系统（关系维护）：关系管理 → 社交过滤 → 主动触发

核心模块：
    - core/input_processor.py: 输入处理器（主入口）
    - core/dream_process.py: 每日复盘
    
快速使用：
    >>> from NeuroAgent import process
    >>> result = process("今天工作好累啊")
    >>> print(result.response)
"""

__version__ = "5.1.0"
__author__ = "Neuro-α Team"

# 核心接口
from core.input_processor import InputProcessor, process, get_instance

# 复盘
from core.dream_process import DreamProcess, run_dream, get_instance as get_dream_instance

# 左脑
from left_brain.emotion_detector import EmotionDetector, detect_emotion, detect_subtext
from left_brain.empathy_generator import EmpathyGenerator, generate_empathy
from left_brain.capsule_factory import CapsuleFactory, should_create_capsule, create_capsule

# 右脑
from right_brain.intent_classifier import IntentClassifier, classify_intent
from right_brain.logic_parser import LogicParser, parse_task
from right_brain.solution_generator import SolutionGenerator, generate_solution

# 颞叶
from temporal.short_term_memory import ShortTermMemory
from temporal.long_term_memory import LongTermMemory
from temporal.vector_retriever import VectorRetriever

# 前额叶
from prefrontal.executor import PrefrontalExecutor, arbitrate
from prefrontal.monitor import Monitor as PrefrontalMonitor, monitor
from prefrontal.fusion_output import FusionOutput, fuse

# 边缘系统
from limbic.relationship_manager import RelationshipManager, record_interaction
from limbic.social_filter import SocialFilter, should_contact
from limbic.proactive_trigger import ProactiveTrigger, check_triggers


# ============ 快捷函数 ============
def quick_response(user_input: str, hour: int = None) -> str:
    """
    快速生成回复
    
    参数:
        user_input: 用户输入
        hour: 当前小时（可选，用于问候语生成）
    
    返回:
        str: 生成的回复
    """
    if hour is None:
        from datetime import datetime
        hour = datetime.now().hour
    
    processor = get_instance()
    result = processor.process(user_input, {"hour": hour})
    return result.response


def full_pipeline(user_input: str, context: dict = None) -> dict:
    """
    完整处理流程
    
    返回完整的处理结果，包括元数据
    """
    processor = get_instance()
    result = processor.process(user_input, context or {})
    return {
        "response": result.response,
        "capsules": result.capsules_to_save,
        "metadata": result.metadata
    }


# ============ 版本信息 ============
__all__ = [
    # 核心
    "InputProcessor",
    "process",
    "DreamProcess",
    "run_dream",
    
    # 左脑
    "EmotionDetector",
    "detect_emotion",
    "EmpathyGenerator",
    "generate_empathy",
    "CapsuleFactory",
    "should_create_capsule",
    "create_capsule",
    
    # 右脑
    "IntentClassifier",
    "classify_intent",
    "LogicParser",
    "parse_logic",
    "SolutionGenerator",
    "generate_solution",
    
    # 颞叶
    "ShortTermMemory",
    "LongTermMemory",
    "VectorRetriever",
    
    # 前额叶
    "PrefrontalExecutor",
    "execute",
    "PrefrontalMonitor",
    "monitor",
    "FusionOutput",
    "fuse",
    
    # 边缘
    "RelationshipManager",
    "record_interaction",
    "SocialFilter",
    "should_contact",
    "ProactiveTrigger",
    "check_triggers",
    
    # 快捷
    "quick_response",
    "full_pipeline",
]
