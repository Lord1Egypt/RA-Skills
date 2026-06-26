"""
文件功能：Deployment分析器模块
主要类/函数：DeploymentAnalyzer - 分析Deployment状态
作者：chenzc
创建时间：2026-04-03
最后修改：2026-04-03

LEARNING: 检测滚动更新状态、副本可用性
IMPORTANT: 关注ProgressDeadlineExceeded等关键条件
"""

from typing import List
try:
    from ..core import BaseAnalyzer, AnalysisResult, Failure, Severity
except ImportError:
    from core import BaseAnalyzer, AnalysisResult, Failure, Severity


class DeploymentAnalyzer(BaseAnalyzer):
    """
    Deployment分析器 - 基于SRE最佳实践设计
    
    检测能力：
    - 滚动更新状态
    - 副本可用性
    - 资源配额问题
    
    使用示例：
    >>> analyzer = DeploymentAnalyzer()
    >>> results = analyzer.analyze(namespace="production")
    """
    
    @property
    def resource_kind(self) -> str:
        return "Deployment"
    
    def _do_analyze(self, namespace: str, label_selector: str) -> List[AnalysisResult]:
        """执行Deployment分析"""
        results = []
        apps_v1 = self.client.AppsV1Api()
        
        deployments = self._list_resources_paginated(
            list_func=apps_v1.list_deployment_for_all_namespaces,
            cache_key="deployments",
            namespace=namespace,
            label_selector=label_selector
        )
        
        for deploy in deployments:
            if namespace and deploy.metadata.namespace != namespace:
                continue
            
            failures = self._analyze_deployment(deploy)
            if failures:
                spec = deploy.spec
                status = deploy.status
                
                result = self._create_result(
                    deploy,
                    failures,
                    replicas=getattr(spec, 'replicas', 0) if spec else 0,
                    available_replicas=getattr(status, 'available_replicas', 0) if status else 0,
                    updated_replicas=getattr(status, 'updated_replicas', 0) if status else 0,
                    strategy=getattr(getattr(spec, 'strategy', None), 'type', 'Unknown') if spec else 'Unknown'
                )
                results.append(result)
        
        self._logger.info(f"分析完成: {len(results)} 个Deployment发现问题")
        return results
    
    def _analyze_deployment(self, deploy) -> List[Failure]:
        """分析单个Deployment"""
        failures = []
        spec = deploy.spec
        status = deploy.status
        
        if not spec or not status:
            return failures
        
        desired = getattr(spec, 'replicas', 0) or 0
        available = getattr(status, 'available_replicas', 0) or 0
        updated = getattr(status, 'updated_replicas', 0) or 0
        
        # 检查可用副本不足
        if available < desired:
            failures.append(Failure(
                text=f"可用副本不足: {available}/{desired}",
                severity=Severity.CRITICAL if available == 0 else Severity.WARNING,
                reason="UnavailableReplicas",
                suggestion="1. 检查Pod状态和事件\n2. 查看资源配额\n3. 检查节点资源"
            ))
        
        # 检查滚动更新进度
        strategy = getattr(getattr(spec, 'strategy', None), 'type', None)
        if updated < desired and strategy == "RollingUpdate":
            failures.append(Failure(
                text=f"滚动更新进行中: {updated}/{desired} 已更新",
                severity=Severity.INFO,
                reason="RollingUpdateInProgress",
                suggestion="等待更新完成或检查新Pod启动失败原因"
            ))
        
        # 检查条件
        if status.conditions:
            for condition in status.conditions:
                if condition.type == "Progressing" and condition.status == "False":
                    failures.append(Failure(
                        text=f"部署进度停滞: {condition.message or 'Unknown'}",
                        severity=Severity.WARNING,
                        reason="ProgressDeadlineExceeded",
                        suggestion="检查新ReplicaSet的Pod创建失败原因"
                    ))
        
        return failures
