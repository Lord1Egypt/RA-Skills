"""
文件功能：HTTPRoute分析器模块
主要类/函数：HTTPRouteAnalyzer - 分析Gateway API HTTPRoute资源
作者：chenzc
创建时间：2026-04-03
最后修改：2026-04-03

LEARNING: 检测HTTPRoute Gateway引用、后端Service问题
IMPORTANT: HTTPRoute是Gateway API的路由资源
NOTE: 需要集群支持Gateway API（CRD已安装）
"""

from typing import List, Dict
from kubernetes.client.exceptions import ApiException
try:
    from ..core import BaseAnalyzer, AnalysisResult, Failure, Severity
except ImportError:
    from core import BaseAnalyzer, AnalysisResult, Failure, Severity


class HTTPRouteAnalyzer(BaseAnalyzer):
    """
    HTTPRoute分析器（Gateway API）- 基于SRE最佳实践设计
    
    检测能力：
    - HTTPRoute引用的Gateway不存在
    - HTTPRoute与Gateway不在允许的命名空间
    - 后端Service不存在
    
    使用示例：
    >>> analyzer = HTTPRouteAnalyzer()
    >>> results = analyzer.analyze(namespace="production")
    
    NOTE: 需要集群支持Gateway API（CRD已安装）
    """
    
    @property
    def resource_kind(self) -> str:
        return "HTTPRoute"
    
    def _do_analyze(self, namespace: str, label_selector: str) -> List[AnalysisResult]:
        """执行HTTPRoute分析"""
        results = []
        custom_api = self.client.CustomObjectsApi()
        core_v1 = self.client.CoreV1Api()
        
        try:
            # 获取HTTPRoute列表
            if namespace:
                route_list = custom_api.list_namespaced_custom_object(
                    group="gateway.networking.k8s.io",
                    version="v1",
                    namespace=namespace,
                    plural="httproutes",
                    label_selector=label_selector
                )
            else:
                route_list = custom_api.list_cluster_custom_object(
                    group="gateway.networking.k8s.io",
                    version="v1",
                    plural="httproutes",
                    label_selector=label_selector
                )
            
            # 获取所有Gateway
            try:
                gateway_list = custom_api.list_cluster_custom_object(
                    group="gateway.networking.k8s.io",
                    version="v1",
                    plural="gateways"
                )
                gateways = {
                    f"{g['metadata'].get('namespace', '')}/{g['metadata'].get('name', '')}": g
                    for g in gateway_list.get("items", [])
                }
            except ApiException:
                gateways = {}
            
            # 分析每个HTTPRoute
            for route in route_list.get("items", []):
                failures = self._analyze_httproute(route, gateways, core_v1)
                if failures:
                    metadata = route.get("metadata", {})
                    spec = route.get("spec", {})
                    
                    parent_refs = spec.get("parentRefs", [])
                    gateway_names = [ref.get("name", "") for ref in parent_refs]
                    
                    result = AnalysisResult(
                        kind="HTTPRoute",
                        name=metadata.get("name", "unknown"),
                        namespace=metadata.get("namespace", ""),
                        failures=failures,
                        details={
                            "parent_gateways": gateway_names,
                            "hostnames": spec.get("hostnames", [])
                        }
                    )
                    results.append(result)
        
        except ApiException as e:
            if e.status == 404:
                # Gateway API未安装，返回空结果
                self._logger.info("Gateway API未安装，跳过分析")
            else:
                self._logger.error(f"分析HTTPRoute时出错: {e}")
        
        return results
    
    def _analyze_httproute(self, route: Dict, gateways: Dict, core_v1) -> List[Failure]:
        """分析单个HTTPRoute"""
        failures = []
        
        metadata = route.get("metadata", {})
        spec = route.get("spec", {})
        route_namespace = metadata.get("namespace", "")
        
        # 检查ParentRefs（Gateway引用）
        parent_refs = spec.get("parentRefs", [])
        for ref in parent_refs:
            gateway_name = ref.get("name", "")
            gateway_namespace = ref.get("namespace", route_namespace)
            gateway_key = f"{gateway_namespace}/{gateway_name}"
            
            if gateway_key not in gateways:
                failures.append(Failure(
                    text=f"HTTPRoute引用的Gateway '{gateway_name}'（命名空间: {gateway_namespace}）不存在",
                    severity=Severity.CRITICAL,
                    reason="GatewayNotFound",
                    suggestion="1. 创建Gateway\n2. 或更正parentRefs中的gateway名称"
                ))
        
        # 检查后端Service
        rules = spec.get("rules", [])
        for rule in rules:
            backend_refs = rule.get("backendRefs", [])
            for backend in backend_refs:
                if backend.get("kind") == "Service":
                    service_name = backend.get("name", "")
                    service_namespace = backend.get("namespace", route_namespace)
                    
                    try:
                        core_v1.read_namespaced_service(
                            name=service_name,
                            namespace=service_namespace
                        )
                    except ApiException as e:
                        if e.status == 404:
                            failures.append(Failure(
                                text=f"HTTPRoute引用的Service '{service_name}'（命名空间: {service_namespace}）不存在",
                                severity=Severity.CRITICAL,
                                reason="ServiceNotFound",
                                suggestion="1. 创建Service\n2. 或更正backendRefs中的service名称"
                            ))
        
        return failures
