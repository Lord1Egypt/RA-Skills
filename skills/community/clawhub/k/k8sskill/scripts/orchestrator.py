"""
文件功能：K8sSkill分析器编排器
主要类/函数：AnalyzerOrchestrator - 协调多个分析器执行诊断
作者：chenzc
创建时间：2026-04-03
最后修改：2026-04-03

LEARNING: 使用编排器模式统一管理多个分析器
IMPORTANT: 支持意图识别和动态分析器加载
"""

from typing import List, Dict, Any, Optional, Type
from datetime import datetime
import logging

try:
    # 尝试相对导入（作为包的一部分时）
    from .core import BaseAnalyzer, AnalysisResult, Severity
    from .analyzers import (
        PodAnalyzer, DeploymentAnalyzer, ServiceAnalyzer,
        StatefulSetAnalyzer, JobAnalyzer, CronJobAnalyzer,
        ReplicaSetAnalyzer, HPAAnalyzer, PVCAnalyzer,
        NodeAnalyzer, IngressAnalyzer, EventAnalyzer,
        ConfigMapAnalyzer, SecretAnalyzer, NetworkPolicyAnalyzer,
        PDBAnalyzer, StorageAnalyzer, SecurityAnalyzer,
        GatewayAnalyzer, HTTPRouteAnalyzer, WebhookAnalyzer,
    )
except ImportError:
    # 回退到绝对导入（直接运行时）
    from core import BaseAnalyzer, AnalysisResult, Severity
    from analyzers import (
        PodAnalyzer, DeploymentAnalyzer, ServiceAnalyzer,
        StatefulSetAnalyzer, JobAnalyzer, CronJobAnalyzer,
        ReplicaSetAnalyzer, HPAAnalyzer, PVCAnalyzer,
        NodeAnalyzer, IngressAnalyzer, EventAnalyzer,
        ConfigMapAnalyzer, SecretAnalyzer, NetworkPolicyAnalyzer,
        PDBAnalyzer, StorageAnalyzer, SecurityAnalyzer,
        GatewayAnalyzer, HTTPRouteAnalyzer, WebhookAnalyzer,
    )

logger = logging.getLogger(__name__)


class AnalyzerOrchestrator:
    """
    分析器编排器 - 协调所有分析器执行诊断
    
    功能：
    - 意图识别：将自然语言映射到分析器
    - 协调分析：调用多个分析器执行诊断
    - 结果汇总：整合和格式化分析结果
    
    使用示例：
    >>> orchestrator = AnalyzerOrchestrator()
    >>> 
    >>> # 分析所有资源
    >>> results = orchestrator.analyze("检查集群问题")
    >>> 
    >>> # 仅分析Pod
    >>> results = orchestrator.analyze("Pod为什么崩溃", namespace="default")
    >>> 
    >>> # 打印报告
    >>> print(orchestrator.format_report(results))
    """
    
    # 意图关键词映射表
    INTENT_MAP = {
        "pod": ["pod", "容器", "container", "重启", "crash", "oom", "崩溃"],
        "deployment": ["deployment", "部署", "rollout", "发布", "更新"],
        "service": ["service", "服务", "访问", "连通", "endpoint"],
        "statefulset": ["statefulset", "sts", "有状态", "数据库", "kafka", "redis", "mysql"],
        "job": ["job", "任务", "批处理", "batchjob", "一次性任务"],
        "cronjob": ["cronjob", "定时任务", "定时器", "schedule", "cron"],
        "replicaset": ["replicaset", "rs", "副本集", "副本"],
        "hpa": ["hpa", "自动伸缩", "扩缩容", "autoscale", "horizontal"],
        "pvc": ["pvc", "存储", "volume", "磁盘", "持久化", "storage", "claim"],
        "node": ["node", "节点", "机器", "服务器", "宿主机", "worker", "master"],
        "ingress": ["ingress", "域名", "路由", "gateway", "入口"],
        "event": ["event", "事件", "日志", "警告", "warning", "log"],
        "configmap": ["configmap", "cm", "配置", "配置项", "config"],
        "secret": ["secret", "密钥", "证书", "tls", "docker-registry"],
        "networkpolicy": ["networkpolicy", "网络策略", "防火墙", "网络隔离"],
        "pdb": ["pdb", "poddisruptionbudget", "中断预算", "驱逐保护"],
        "storage": ["storage", "storageclass", "pv", "持久卷", "存储类"],
        "security": ["security", "安全", "特权", "root", "serviceaccount"],
        "gateway": ["gateway", "网关", "gatewayapi"],
        "httproute": ["httproute", "路由", "http路由"],
        "webhook": ["webhook", "准入控制器", "validatingwebhook", "mutatingwebhook"],
        "all": ["所有", "全部", "集群", "cluster", "整体", "问题"]
    }
    
    # 分析器注册表
    ANALYZER_REGISTRY: Dict[str, Type[BaseAnalyzer]] = {
        "pod": PodAnalyzer,
        "deployment": DeploymentAnalyzer,
        "service": ServiceAnalyzer,
        "statefulset": StatefulSetAnalyzer,
        "job": JobAnalyzer,
        "cronjob": CronJobAnalyzer,
        "replicaset": ReplicaSetAnalyzer,
        "hpa": HPAAnalyzer,
        "pvc": PVCAnalyzer,
        "node": NodeAnalyzer,
        "ingress": IngressAnalyzer,
        "event": EventAnalyzer,
        "configmap": ConfigMapAnalyzer,
        "secret": SecretAnalyzer,
        "networkpolicy": NetworkPolicyAnalyzer,
        "pdb": PDBAnalyzer,
        "storage": StorageAnalyzer,
        "security": SecurityAnalyzer,
        "gateway": GatewayAnalyzer,
        "httproute": HTTPRouteAnalyzer,
        "webhook": WebhookAnalyzer,
    }
    
    def __init__(self, analyzer_types: Optional[List[str]] = None):
        """
        初始化编排器
        
        参数说明：
        - analyzer_types: [Optional[List[str]]] 要加载的分析器类型列表，
                         None表示加载所有分析器
        """
        self._logger = logging.getLogger(self.__class__.__name__)
        self._analyzers: Dict[str, BaseAnalyzer] = {}
        
        # 加载分析器
        types_to_load = analyzer_types or list(self.ANALYZER_REGISTRY.keys())
        for analyzer_type in types_to_load:
            self._load_analyzer(analyzer_type)
    
    def _load_analyzer(self, analyzer_type: str):
        """加载指定类型的分析器"""
        if analyzer_type in self._analyzers:
            return
        
        analyzer_class = self.ANALYZER_REGISTRY.get(analyzer_type)
        if not analyzer_class:
            self._logger.warning(f"未知的分析器类型: {analyzer_type}")
            return
        
        try:
            self._analyzers[analyzer_type] = analyzer_class()
            self._logger.info(f"已加载分析器: {analyzer_type}")
        except Exception as e:
            self._logger.error(f"加载分析器 {analyzer_type} 失败: {e}")
    
    def register_analyzer(self, name: str, analyzer: BaseAnalyzer):
        """
        注册自定义分析器
        
        参数说明：
        - name: [str] 分析器名称
        - analyzer: [BaseAnalyzer] 分析器实例
        """
        self._analyzers[name] = analyzer
        self._logger.info(f"已注册分析器: {name}")
    
    def parse_intent(self, query: str) -> List[str]:
        """
        解析用户意图，识别需要执行的分析类型
        
        参数说明：
        - query: [str] 用户自然语言输入
        
        返回说明：
        - [List[str]] 需要执行的分析器类型列表
        
        示例：
        >>> orchestrator.parse_intent("检查Pod为什么崩溃")
        ['pod']
        >>> orchestrator.parse_intent("服务和部署有什么问题")
        ['service', 'deployment']
        """
        query_lower = query.lower()
        detected = []
        
        for analyzer_type, keywords in self.INTENT_MAP.items():
            for keyword in keywords:
                if keyword in query_lower:
                    detected.append(analyzer_type)
                    break
        
        # 默认执行全部分析
        if not detected or "all" in detected:
            return list(self._analyzers.keys())
        
        # 过滤掉未加载的分析器
        return [d for d in detected if d in self._analyzers]
    
    def analyze(
        self,
        query: str,
        namespace: str = "",
        label_selector: str = ""
    ) -> Dict[str, List[AnalysisResult]]:
        """
        执行分析（主入口）
        
        参数说明：
        - query: [str] 用户自然语言查询
        - namespace: [str] 目标命名空间
        - label_selector: [str] 标签选择器
        
        返回说明：
        - [Dict[str, List[AnalysisResult]]] 按分析器分类的结果
        
        示例：
        >>> results = orchestrator.analyze("检查Pod问题", namespace="production")
        >>> for analyzer_type, result_list in results.items():
        ...     print(f"{analyzer_type}: {len(result_list)} issues")
        """
        analyzer_types = self.parse_intent(query)
        results = {}
        errors = {}
        
        for analyzer_type in analyzer_types:
            analyzer = self._analyzers.get(analyzer_type)
            if not analyzer:
                continue
            
            try:
                result_list = analyzer.analyze(namespace, label_selector)
                if result_list:
                    results[analyzer_type] = result_list
            except Exception as e:
                error_msg = f"分析器 {analyzer_type} 执行失败: {e}"
                self._logger.error(error_msg, exc_info=True)
                errors[analyzer_type] = str(e)
        
        if errors:
            results["_errors"] = errors
        
        return results
    
    def format_report(self, results: Dict[str, List[AnalysisResult]], format_type: str = "markdown") -> str:
        """
        格式化分析报告
        
        参数说明：
        - results: [Dict] 分析结果
        - format_type: [str] 输出格式 (markdown/json)
        
        返回说明：
        - [str] 格式化后的报告
        """
        if format_type == "markdown":
            return self._format_markdown(results)
        elif format_type == "json":
            return self._format_json(results)
        else:
            return str(results)
    
    def _format_json(self, results: Dict[str, List[AnalysisResult]]) -> str:
        """格式化为JSON报告"""
        import json
        json_results = {}
        
        for k, v in results.items():
            if k == "_errors":
                json_results["errors"] = v
            elif isinstance(v, list):
                json_results[k] = [
                    {
                        "kind": r.kind,
                        "name": r.name,
                        "namespace": r.namespace,
                        "failures": [
                            {
                                "text": f.text,
                                "severity": f.severity.value,
                                "reason": f.reason,
                                "suggestion": f.suggestion
                            }
                            for f in r.failures
                        ],
                        "details": r.details
                    }
                    for r in v
                ]
        
        return json.dumps(json_results, indent=2, ensure_ascii=False)
    
    def _format_markdown(self, results: Dict[str, List[AnalysisResult]]) -> str:
        """格式化为Markdown报告"""
        lines = []
        lines.append("# K8sSkill 诊断报告\n")
        lines.append(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        
        errors = results.get("_errors", {})
        if errors:
            lines.append("\n## [ERROR] 分析过程错误\n")
            lines.append("以下分析器执行失败，请检查集群连接或权限：\n")
            for analyzer_type, error_msg in errors.items():
                lines.append(f"- **{analyzer_type}**: {error_msg}\n")
            lines.append("\n---\n")
        
        total_issues = sum(len(r) for r in results.values() if isinstance(r, list))
        if total_issues == 0 and not errors:
            lines.append("\n[OK] **未发现明显问题**\n")
            return "\n".join(lines)
        elif total_issues == 0:
            lines.append("\n[INFO] **未发现资源问题**（但存在分析错误）\n")
            return "\n".join(lines)
        
        lines.append(f"\n## 汇总\n")
        lines.append(f"发现问题资源: **{total_issues}** 个\n")
        
        # 统计严重程度
        critical = 0
        warning = 0
        for key, result_list in results.items():
            if key == "_errors":
                continue
            if not isinstance(result_list, list):
                continue
            for result in result_list:
                critical += result.critical_count
                warning += sum(1 for f in result.failures if f.severity == Severity.WARNING)
        
        if critical > 0:
            lines.append(f"[CRITICAL] 严重: **{critical}**\n")
        if warning > 0:
            lines.append(f"[WARNING] 警告: **{warning}**\n")
        
        lines.append("\n---\n")
        
        # 详细结果
        for analyzer_type, result_list in results.items():
            if analyzer_type == "_errors":
                continue
            if not isinstance(result_list, list) or not result_list:
                continue
            
            lines.append(f"\n## {analyzer_type.upper()} 分析结果\n")
            
            for result in result_list:
                status = "[CRITICAL]" if result.critical_count > 0 else "[WARNING]" if result.has_issues else "[OK]"
                lines.append(f"\n### {status} {result.kind}: `{result.name}`\n")
                lines.append(f"**命名空间:** {result.namespace}\n")
                
                if result.parent_object:
                    lines.append(f"**父资源:** {result.parent_object}\n")
                
                lines.append(f"\n**问题详情:**\n")
                for failure in result.failures:
                    severity_mark = "[CRITICAL]" if failure.severity == Severity.CRITICAL else "[WARNING]" if failure.severity == Severity.WARNING else "[INFO]"
                    lines.append(f"\n{severity_mark} **{failure.reason}**\n")
                    lines.append(f"> {failure.text}\n")
                    if failure.suggestion:
                        lines.append(f"\n**建议:**\n")
                        lines.append(f"```\n{failure.suggestion}\n```\n")
        
        return "\n".join(lines)


# 便捷函数
def analyze_cluster(query: str = "检查集群问题", namespace: str = "") -> str:
    """
    快速分析集群并返回Markdown报告
    
    参数说明：
    - query: [str] 分析查询
    - namespace: [str] 命名空间
    
    返回说明：
    - [str] Markdown格式的分析报告
    
    使用示例：
    >>> report = analyze_cluster("检查Pod为什么崩溃", "production")
    >>> print(report)
    """
    orchestrator = AnalyzerOrchestrator()
    results = orchestrator.analyze(query, namespace)
    return orchestrator.format_report(results, "markdown")
