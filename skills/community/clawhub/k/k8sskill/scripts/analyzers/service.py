"""
文件功能：Service分析器模块
主要类/函数：ServiceAnalyzer - 分析Service状态
作者：chenzc
创建时间：2026-04-03
最后修改：2026-04-03

LEARNING: 检测端点缺失、选择器匹配问题
IMPORTANT: Service与Pod的关联性检查
"""

from typing import List
from kubernetes.client.exceptions import ApiException
try:
    from ..core import BaseAnalyzer, AnalysisResult, Failure, Severity
except ImportError:
    from core import BaseAnalyzer, AnalysisResult, Failure, Severity


class ServiceAnalyzer(BaseAnalyzer):
    """
    Service分析器 - 基于SRE最佳实践设计
    
    检测能力：
    - 端点(Endpoints)缺失
    - 选择器匹配问题
    - 端口配置
    
    使用示例：
    >>> analyzer = ServiceAnalyzer()
    >>> results = analyzer.analyze(namespace="production")
    """
    
    @property
    def resource_kind(self) -> str:
        return "Service"
    
    def _do_analyze(self, namespace: str, label_selector: str) -> List[AnalysisResult]:
        """执行Service分析"""
        results = []
        v1 = self.client.CoreV1Api()
        
        services = self._list_resources_paginated(
            list_func=v1.list_service_for_all_namespaces,
            cache_key="services",
            namespace=namespace,
            label_selector=label_selector
        )
        
        for svc in services:
            if namespace and svc.metadata.namespace != namespace:
                continue
            
            if not svc.spec or not svc.spec.selector:
                continue
            
            failures = self._analyze_service(svc, v1)
            if failures:
                result = self._create_result(
                    svc,
                    failures,
                    type=svc.spec.type if svc.spec else "Unknown",
                    selector=svc.spec.selector if svc.spec else {},
                    ports=[p.port for p in svc.spec.ports] if svc.spec and svc.spec.ports else []
                )
                results.append(result)
        
        self._logger.info(f"分析完成: {len(results)} 个Service发现问题")
        return results
    
    def _analyze_service(self, svc, v1) -> List[Failure]:
        """分析单个Service"""
        failures = []
        
        try:
            endpoints = v1.read_namespaced_endpoints(
                name=svc.metadata.name,
                namespace=svc.metadata.namespace,
                _request_timeout=self._timeout
            )
            
            # 检查是否有可用端点
            has_endpoints = False
            if endpoints.subsets:
                for subset in endpoints.subsets:
                    if getattr(subset, 'addresses', None):
                        has_endpoints = True
                        break
            
            if not has_endpoints:
                selector_str = ", ".join([f"{k}={v}" for k, v in svc.spec.selector.items()])
                failures.append(Failure(
                    text=f"Service端点为空，选择器: {selector_str}",
                    severity=Severity.WARNING,
                    reason="NoEndpoints",
                    suggestion=f"1. 检查Pod标签是否匹配选择器\n2. 查看Pod状态: kubectl get pods -l {selector_str}\n3. 验证Pod是否通过健康检查"
                ))
                
        except ApiException as e:
            if e.status == 404:
                failures.append(Failure(
                    text="Service没有对应的Endpoints资源",
                    severity=Severity.WARNING,
                    reason="EndpointsNotFound",
                    suggestion="检查Service配置和Pod标签"
                ))
        
        return failures
