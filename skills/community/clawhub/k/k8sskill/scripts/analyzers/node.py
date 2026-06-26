"""
文件功能：Node分析器模块
主要类/函数：NodeAnalyzer - 分析集群节点状态
作者：chenzc
创建时间：2026-04-03
最后修改：2026-04-03

LEARNING: 检测节点就绪状态、资源压力
IMPORTANT: 节点是集群基础设施，关注整体健康
"""

from typing import List
try:
    from ..core import BaseAnalyzer, AnalysisResult, Failure, Severity
except ImportError:
    from core import BaseAnalyzer, AnalysisResult, Failure, Severity


class NodeAnalyzer(BaseAnalyzer):
    """
    节点分析器 - 基于SRE最佳实践设计
    
    检测能力：
    - 节点就绪状态（NodeReady）
    - 内存压力（MemoryPressure）
    - 磁盘压力（DiskPressure）
    - PID压力（PIDPressure）
    - 网络不可用（NetworkUnavailable）
    
    使用示例：
    >>> analyzer = NodeAnalyzer()
    >>> results = analyzer.analyze()
    >>> for r in results:
    ...     print(f"节点 {r.name} 状态异常")
    """
    
    # 标准节点条件类型
    KNOWN_CONDITIONS = {
        "Ready", "MemoryPressure", "DiskPressure",
        "PIDPressure", "NetworkUnavailable"
    }
    
    PRESSURE_SUGGESTIONS = {
        "MemoryPressure": "1. 驱逐低优先级Pod\n2. 增加节点内存\n3. 检查内存泄漏",
        "DiskPressure": "1. 清理镜像和日志\n2. 增加节点磁盘\n3. 配置日志轮转",
        "PIDPressure": "1. 检查进程泄漏\n2. 增加节点PID限制\n3. 重启问题Pod",
        "NetworkUnavailable": "1. 检查网络插件\n2. 验证CNI配置\n3. 检查节点网络"
    }
    
    @property
    def resource_kind(self) -> str:
        return "Node"
    
    def _do_analyze(self, namespace: str, label_selector: str) -> List[AnalysisResult]:
        """执行Node分析（namespace参数被忽略，节点是集群级别资源）"""
        results = []
        v1 = self.client.CoreV1Api()
        
        nodes = v1.list_node(label_selector=label_selector if label_selector else None)
        
        for node in nodes.items:
            failures = self._analyze_node(node)
            if failures:
                status = node.status
                allocatable = getattr(status, 'allocatable', {}) if status else {}
                capacity = getattr(status, 'capacity', {}) if status else {}
                node_info = getattr(status, 'node_info', None)
                
                conditions = []
                if status and status.conditions:
                    conditions = [
                        {"type": c.type, "status": c.status, "reason": getattr(c, 'reason', '')}
                        for c in status.conditions
                    ]
                
                result = self._create_result(
                    node,
                    failures,
                    conditions=conditions,
                    allocatable_cpu=allocatable.get('cpu', 'N/A'),
                    allocatable_memory=allocatable.get('memory', 'N/A'),
                    capacity_pods=capacity.get('pods', 'N/A'),
                    kubelet_version=getattr(node_info, 'kubelet_version', 'N/A') if node_info else 'N/A'
                )
                results.append(result)
        
        self._logger.info(f"分析完成: {len(results)} 个Node发现问题")
        return results
    
    def _analyze_node(self, node) -> List[Failure]:
        """分析单个节点"""
        failures = []
        status = node.status
        
        if not status or not status.conditions:
            return failures
        
        for condition in status.conditions:
            condition_type = condition.type
            condition_status = condition.status
            
            # NodeReady特殊处理
            if condition_type == "Ready":
                if condition_status != "True":
                    failures.append(Failure(
                        text=f"节点未就绪: {getattr(condition, 'reason', 'Unknown')} - {getattr(condition, 'message', 'No message')}",
                        severity=Severity.CRITICAL,
                        reason="NotReady",
                        suggestion="1. 检查kubelet状态\n2. 查看节点事件\n3. 检查网络连接"
                    ))
            
            # 跳过EtcdIsVoter（k3s特殊条件）
            elif condition_type == "EtcdIsVoter":
                continue
            
            # 其他标准条件
            elif condition_type in self.KNOWN_CONDITIONS:
                if condition_status == "True":
                    suggestion = self.PRESSURE_SUGGESTIONS.get(
                        condition_type,
                        "检查节点资源使用情况"
                    )
                    failures.append(Failure(
                        text=f"节点存在压力: {condition_type} - {getattr(condition, 'message', 'No message')}",
                        severity=Severity.WARNING,
                        reason=condition_type,
                        suggestion=suggestion
                    ))
            
            # 未知条件类型
            else:
                if condition_status in ["True", "Unknown"]:
                    failures.append(Failure(
                        text=f"节点未知条件: {condition_type}={condition_status} - {getattr(condition, 'message', 'No message')}",
                        severity=Severity.INFO,
                        reason="UnknownCondition",
                        suggestion="检查节点条件和集群版本兼容性"
                    ))
        
        return failures
