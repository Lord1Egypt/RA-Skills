"""
文件功能：StatefulSet分析器模块
主要类/函数：StatefulSetAnalyzer - 分析StatefulSet状态
作者：chenzc
创建时间：2026-04-03
最后修改：2026-04-03

LEARNING: 检测Headless Service、StorageClass依赖
IMPORTANT: StatefulSet的特殊性：有序部署、稳定网络标识
"""

from typing import List
from kubernetes.client.exceptions import ApiException
try:
    from ..core import BaseAnalyzer, AnalysisResult, Failure, Severity
except ImportError:
    from core import BaseAnalyzer, AnalysisResult, Failure, Severity


class StatefulSetAnalyzer(BaseAnalyzer):
    """
    StatefulSet分析器 - 基于SRE最佳实践设计
    
    检测能力：
    - Headless Service不存在
    - StorageClass不存在
    - Pod未就绪
    - 副本数不匹配
    
    使用示例：
    >>> analyzer = StatefulSetAnalyzer()
    >>> results = analyzer.analyze(namespace="database")
    """
    
    @property
    def resource_kind(self) -> str:
        return "StatefulSet"
    
    def _do_analyze(self, namespace: str, label_selector: str) -> List[AnalysisResult]:
        """执行StatefulSet分析"""
        results = []
        apps_v1 = self.client.AppsV1Api()
        
        statefulsets = self._list_resources_paginated(
            list_func=apps_v1.list_stateful_set_for_all_namespaces,
            cache_key="statefulsets",
            namespace=namespace,
            label_selector=label_selector
        )
        
        core_v1 = self.client.CoreV1Api()
        storage_v1 = self.client.StorageV1Api()
        
        for sts in statefulsets:
            if namespace and sts.metadata.namespace != namespace:
                continue
            
            failures = self._analyze_statefulset(sts, core_v1, storage_v1)
            if failures:
                result = self._create_result(
                    sts,
                    failures,
                    replicas=getattr(getattr(sts, 'spec', None), 'replicas', 0),
                    service_name=getattr(getattr(sts, 'spec', None), 'service_name', ''),
                    volume_claim_templates=len(getattr(getattr(sts, 'spec', None), 'volume_claim_templates', []) or [])
                )
                results.append(result)
        
        self._logger.info(f"分析完成: {len(results)} 个StatefulSet发现问题")
        return results
    
    def _analyze_statefulset(self, sts, core_v1, storage_v1) -> List[Failure]:
        """分析单个StatefulSet"""
        failures = []
        spec = sts.spec
        status = sts.status
        
        if not spec:
            return failures
        
        # 检查Headless Service
        service_name = spec.service_name
        if service_name:
            try:
                core_v1.read_namespaced_service(
                    name=service_name,
                    namespace=sts.metadata.namespace
                )
            except ApiException as e:
                if e.status == 404:
                    failures.append(Failure(
                        text=f"StatefulSet使用的Service '{service_name}' 不存在",
                        severity=Severity.CRITICAL,
                        reason="ServiceNotFound",
                        suggestion=f"1. 创建Headless Service: {service_name}\n2. 检查Service名称配置"
                    ))
        
        # 检查StorageClass
        if spec.volume_claim_templates:
            for template in spec.volume_claim_templates:
                sc_name = getattr(getattr(template, 'spec', None), 'storage_class_name', None)
                if sc_name:
                    try:
                        storage_v1.read_storage_class(name=sc_name)
                    except ApiException as e:
                        if e.status == 404:
                            failures.append(Failure(
                                text=f"StatefulSet使用的StorageClass '{sc_name}' 不存在",
                                severity=Severity.WARNING,
                                reason="StorageClassNotFound",
                                suggestion="1. 创建StorageClass\n2. 或使用默认StorageClass"
                            ))
        
        # 检查副本状态
        desired = spec.replicas or 0
        available = getattr(status, 'available_replicas', 0) or 0
        if desired > 0 and available != desired:
            failures.append(Failure(
                text=f"StatefulSet副本未就绪: {available}/{desired}",
                severity=Severity.WARNING,
                reason="ReplicasNotReady",
                suggestion="1. 查看Pod状态\n2. 检查Pod事件"
            ))
        
        return failures
