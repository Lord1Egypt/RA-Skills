"""
文件功能：K8sSkill核心模块包
主要类/函数：
    - Severity - 问题严重程度枚举
    - Failure - 故障详情数据类
    - AnalysisResult - 分析结果数据类
    - BaseAnalyzer - 分析器抽象基类
    - ResourceCache - 资源缓存管理器
    - 各类错误异常定义
作者：chenzc
创建时间：2026-04-03
最后修改：2026-04-03

LEARNING: 使用包结构组织代码，提高可维护性
IMPORTANT: 核心模块提供所有分析器的基础能力
"""

from .base import (
    Severity,
    Failure,
    AnalysisResult,
    BaseAnalyzer,
    ResourceCache,
    AnalyzerError,
    K8sConnectionError,
    ResourceNotFoundError,
    AnalysisFailedError,
    get_kubeconfig_path,
    verify_k8s_connection,
    K8S_AVAILABLE,
    PERF_CONFIG,
)

__all__ = [
    "Severity",
    "Failure",
    "AnalysisResult",
    "BaseAnalyzer",
    "ResourceCache",
    "AnalyzerError",
    "K8sConnectionError",
    "ResourceNotFoundError",
    "AnalysisFailedError",
    "get_kubeconfig_path",
    "verify_k8s_connection",
    "K8S_AVAILABLE",
    "PERF_CONFIG",
]
