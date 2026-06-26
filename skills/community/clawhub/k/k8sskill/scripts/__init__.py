"""
文件功能：K8sSkill脚本模块包 - 重构后的清晰结构
主要类/函数：
    # 核心基础
    - Severity - 问题严重程度枚举
    - Failure - 故障详情数据类
    - AnalysisResult - 分析结果数据类
    - BaseAnalyzer - 分析器抽象基类
    
    # 分析器编排
    - AnalyzerOrchestrator - 分析器编排器
    - analyze_cluster - 快速分析函数
    
    # 工作负载分析器
    - PodAnalyzer - Pod分析器
    - DeploymentAnalyzer - Deployment分析器
    - ServiceAnalyzer - Service分析器
    - StatefulSetAnalyzer - StatefulSet分析器
    - JobAnalyzer - Job分析器
    - CronJobAnalyzer - CronJob分析器
    - ReplicaSetAnalyzer - ReplicaSet分析器
    - HPAAnalyzer - HPA分析器
    
    # 存储和网络分析器
    - PVCAnalyzer - PVC分析器
    - IngressAnalyzer - Ingress分析器
    - GatewayAnalyzer - Gateway分析器
    - HTTPRouteAnalyzer - HTTPRoute分析器
    - NetworkPolicyAnalyzer - NetworkPolicy分析器
    
    # 集群分析器
    - NodeAnalyzer - Node分析器
    - EventAnalyzer - Event分析器
    - StorageAnalyzer - Storage分析器
    - SecurityAnalyzer - Security分析器
    - WebhookAnalyzer - Webhook分析器
    
    # 配置分析器
    - ConfigMapAnalyzer - ConfigMap分析器
    - SecretAnalyzer - Secret分析器
    - PDBAnalyzer - PDB分析器

作者：chenzc
创建时间：2026-04-03
最后修改：2026-04-03

LEARNING: 重构后的清晰模块化结构
IMPORTANT: 每个分析器独立，通过编排器统一管理

使用示例：
    # 方式1：使用编排器（推荐）
    # 在 scripts/ 目录下执行
    from orchestrator import AnalyzerOrchestrator
    
    orchestrator = AnalyzerOrchestrator()
    results = orchestrator.analyze("检查Pod问题", namespace="default")
    report = orchestrator.format_report(results)
    print(report)
    
    # 方式2：使用便捷函数
    # 在 scripts/ 目录下执行
    from orchestrator import analyze_cluster
    
    report = analyze_cluster("检查集群问题", namespace="production")
    print(report)
    
    # 方式3：单独使用分析器
    # 在 scripts/ 目录下执行
    from analyzers import PodAnalyzer
    
    analyzer = PodAnalyzer()
    results = analyzer.analyze(namespace="default")
    for result in results:
        print(f"{result.name}: {len(result.failures)} issues")
"""

# 核心基础
try:
    from .core import (
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
    from .orchestrator import AnalyzerOrchestrator, analyze_cluster
    from .analyzers import (
        PodAnalyzer,
        DeploymentAnalyzer,
        ServiceAnalyzer,
        StatefulSetAnalyzer,
        JobAnalyzer,
        CronJobAnalyzer,
        ReplicaSetAnalyzer,
        HPAAnalyzer,
        PVCAnalyzer,
        IngressAnalyzer,
        GatewayAnalyzer,
        HTTPRouteAnalyzer,
        NetworkPolicyAnalyzer,
        NodeAnalyzer,
        EventAnalyzer,
        StorageAnalyzer,
        SecurityAnalyzer,
        WebhookAnalyzer,
        ConfigMapAnalyzer,
        SecretAnalyzer,
        PDBAnalyzer,
    )
except ImportError:
    # 直接运行时的回退导入
    from core import (
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
    from orchestrator import AnalyzerOrchestrator, analyze_cluster
    from analyzers import (
        PodAnalyzer,
        DeploymentAnalyzer,
        ServiceAnalyzer,
        StatefulSetAnalyzer,
        JobAnalyzer,
        CronJobAnalyzer,
        ReplicaSetAnalyzer,
        HPAAnalyzer,
        PVCAnalyzer,
        IngressAnalyzer,
        GatewayAnalyzer,
        HTTPRouteAnalyzer,
        NetworkPolicyAnalyzer,
        NodeAnalyzer,
        EventAnalyzer,
        StorageAnalyzer,
        SecurityAnalyzer,
        WebhookAnalyzer,
        ConfigMapAnalyzer,
        SecretAnalyzer,
        PDBAnalyzer,
    )

__version__ = "1.0.0"
__all__ = [
    # 版本
    "__version__",
    
    # 核心基础
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
    
    # 分析器编排
    "AnalyzerOrchestrator",
    "analyze_cluster",
    
    # 工作负载分析器
    "PodAnalyzer",
    "DeploymentAnalyzer",
    "ServiceAnalyzer",
    "StatefulSetAnalyzer",
    "JobAnalyzer",
    "CronJobAnalyzer",
    "ReplicaSetAnalyzer",
    "HPAAnalyzer",
    
    # 存储和网络分析器
    "PVCAnalyzer",
    "IngressAnalyzer",
    "GatewayAnalyzer",
    "HTTPRouteAnalyzer",
    "NetworkPolicyAnalyzer",
    
    # 集群分析器
    "NodeAnalyzer",
    "EventAnalyzer",
    "StorageAnalyzer",
    "SecurityAnalyzer",
    "WebhookAnalyzer",
    
    # 配置分析器
    "ConfigMapAnalyzer",
    "SecretAnalyzer",
    "PDBAnalyzer",
]
