"""
文件功能：Ingress分析器模块
主要类/函数：IngressAnalyzer - 分析Ingress配置
作者：chenzc
创建时间：2026-04-03
最后修改：2026-04-03

LEARNING: 检测IngressClass、后端Service、TLS证书问题
IMPORTANT: Ingress是入口流量管理，关注配置完整性
"""

from typing import List
from kubernetes.client.exceptions import ApiException
try:
    from ..core import BaseAnalyzer, AnalysisResult, Failure, Severity
except ImportError:
    from core import BaseAnalyzer, AnalysisResult, Failure, Severity


class IngressAnalyzer(BaseAnalyzer):
    """
    Ingress分析器 - 基于SRE最佳实践设计
    
    检测能力：
    - IngressClass未指定或不存在
    - 后端Service不存在
    - TLS证书Secret不存在
    
    使用示例：
    >>> analyzer = IngressAnalyzer()
    >>> results = analyzer.analyze(namespace="production")
    """
    
    @property
    def resource_kind(self) -> str:
        return "Ingress"
    
    def _do_analyze(self, namespace: str, label_selector: str) -> List[AnalysisResult]:
        """执行Ingress分析"""
        results = []
        networking_v1 = self.client.NetworkingV1Api()
        
        ingresses = self._list_resources_paginated(
            list_func=networking_v1.list_ingress_for_all_namespaces,
            cache_key="ingresses",
            namespace=namespace,
            label_selector=label_selector
        )
        
        for ingress in ingresses:
            if namespace and ingress.metadata.namespace != namespace:
                continue
            
            failures = self._analyze_ingress(ingress)
            if failures:
                spec = ingress.spec
                
                result = self._create_result(
                    ingress,
                    failures,
                    class_name=getattr(spec, 'ingress_class_name', None) if spec else None,
                    rules_count=len(getattr(spec, 'rules', []) or []) if spec else 0,
                    tls_count=len(getattr(spec, 'tls', []) or []) if spec else 0
                )
                results.append(result)
        
        self._logger.info(f"分析完成: {len(results)} 个Ingress发现问题")
        return results
    
    def _analyze_ingress(self, ingress) -> List[Failure]:
        """分析单个Ingress"""
        failures = []
        spec = ingress.spec
        metadata = ingress.metadata
        
        if not spec:
            return failures
        
        networking_v1 = self.client.NetworkingV1Api()
        core_v1 = self.client.CoreV1Api()
        
        # 检查IngressClass
        ingress_class_name = spec.ingress_class_name
        
        # 从注解获取（旧方式）
        if not ingress_class_name and metadata.annotations:
            ingress_class_name = metadata.annotations.get("kubernetes.io/ingress.class")
        
        if not ingress_class_name:
            failures.append(Failure(
                text="Ingress未指定IngressClass",
                severity=Severity.WARNING,
                reason="NoIngressClass",
                suggestion="1. 设置spec.ingressClassName\n2. 或添加注解kubernetes.io/ingress.class"
            ))
        else:
            # 检查IngressClass是否存在
            try:
                networking_v1.read_ingress_class(ingress_class_name)
            except ApiException as e:
                if e.status == 404:
                    failures.append(Failure(
                        text=f"Ingress使用的IngressClass '{ingress_class_name}' 不存在",
                        severity=Severity.CRITICAL,
                        reason="IngressClassNotFound",
                        suggestion=f"1. 创建IngressClass '{ingress_class_name}'\n2. 或更正为存在的IngressClass"
                    ))
        
        # 检查后端Service
        if spec.rules:
            for rule in spec.rules:
                http = getattr(rule, 'http', None)
                if http and http.paths:
                    for path in http.paths:
                        backend = getattr(path, 'backend', None)
                        service = getattr(backend, 'service', None)
                        if service and service.name:
                            try:
                                core_v1.read_namespaced_service(
                                    name=service.name,
                                    namespace=metadata.namespace
                                )
                            except ApiException as e:
                                if e.status == 404:
                                    failures.append(Failure(
                                        text=f"Ingress引用的Service '{service.name}' 不存在",
                                        severity=Severity.CRITICAL,
                                        reason="ServiceNotFound",
                                        suggestion=f"1. 创建Service '{service.name}'\n2. 或更正Ingress中的service名称"
                                    ))
        
        # 检查TLS Secret
        if spec.tls:
            for tls in spec.tls:
                if tls.secret_name:
                    try:
                        core_v1.read_namespaced_secret(
                            name=tls.secret_name,
                            namespace=metadata.namespace
                        )
                    except ApiException as e:
                        if e.status == 404:
                            failures.append(Failure(
                                text=f"Ingress使用的TLS证书Secret '{tls.secret_name}' 不存在",
                                severity=Severity.WARNING,
                                reason="TLSSecretNotFound",
                                suggestion=f"1. 创建Secret '{tls.secret_name}'\n2. 或使用cert-manager自动管理"
                            ))
        
        return failures
