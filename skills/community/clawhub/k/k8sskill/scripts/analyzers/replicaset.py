"""
文件功能：ReplicaSet分析器模块
主要类/函数：ReplicaSetAnalyzer - 分析ReplicaSet状态
作者：chenzc
创建时间：2026-04-03
最后修改：2026-04-03

LEARNING: 检测ReplicaSet副本创建失败
IMPORTANT: ReplicaSet通常由Deployment管理
"""

from typing import List
try:
    from ..core import BaseAnalyzer, AnalysisResult, Failure, Severity
except ImportError:
    from core import BaseAnalyzer, AnalysisResult, Failure, Severity


class ReplicaSetAnalyzer(BaseAnalyzer):
    """
    ReplicaSet分析器 - 基于SRE最佳实践设计
    
    检测能力：
    - ReplicaSet副本数为0
    - ReplicaFailure条件（FailedCreate）
    
    使用示例：
    >>> analyzer = ReplicaSetAnalyzer()
    >>> results = analyzer.analyze(namespace="production")
    """
    
    @property
    def resource_kind(self) -> str:
        return "ReplicaSet"
    
    def _do_analyze(self, namespace: str, label_selector: str) -> List[AnalysisResult]:
        """执行ReplicaSet分析"""
        results = []
        apps_v1 = self.client.AppsV1Api()
        
        replicasets = self._list_resources_paginated(
            list_func=apps_v1.list_replica_set_for_all_namespaces,
            cache_key="replicasets",
            namespace=namespace,
            label_selector=label_selector
        )
        
        for rs in replicasets:
            if namespace and rs.metadata.namespace != namespace:
                continue
            
            failures = self._analyze_replicaset(rs)
            if failures:
                status = rs.status
                
                result = self._create_result(
                    rs,
                    failures,
                    replicas=getattr(getattr(rs, 'spec', None), 'replicas', 0),
                    available_replicas=getattr(status, 'available_replicas', 0) if status else 0,
                    ready_replicas=getattr(status, 'ready_replicas', 0) if status else 0
                )
                results.append(result)
        
        self._logger.info(f"分析完成: {len(results)} 个ReplicaSet发现问题")
        return results
    
    def _analyze_replicaset(self, rs) -> List[Failure]:
        """分析单个ReplicaSet"""
        failures = []
        status = rs.status
        
        if not status:
            return failures
        
        # 检查副本数是否为0但有期望副本
        replicas = getattr(rs.spec, 'replicas', 0) if rs.spec else 0
        if replicas > 0 and status.replicas == 0:
            # 检查ReplicaFailure条件
            conditions = getattr(status, 'conditions', []) or []
            for condition in conditions:
                if condition.type == "ReplicaFailure" and condition.reason == "FailedCreate":
                    failures.append(Failure(
                        text=f"ReplicaSet创建副本失败: {condition.message}",
                        severity=Severity.CRITICAL,
                        reason="ReplicaFailure",
                        suggestion="1. 检查资源配额\n2. 查看Pod创建事件\n3. 检查节点资源"
                    ))
                    break
        
        return failures
