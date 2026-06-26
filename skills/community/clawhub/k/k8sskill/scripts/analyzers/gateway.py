"""
文件功能：Gateway分析器模块
主要类/函数：GatewayAnalyzer - 分析Gateway API Gateway资源
作者：chenzc
创建时间：2026-04-03
最后修改：2026-04-03

LEARNING: 检测GatewayClass引用、Gateway接受状态
IMPORTANT: Gateway API是Ingress的下一代替代方案
NOTE: 需要集群支持Gateway API（CRD已安装）
"""

from typing import List, Dict, Set
from kubernetes.client.exceptions import ApiException
try:
    from ..core import BaseAnalyzer, AnalysisResult, Failure, Severity
except ImportError:
    from core import BaseAnalyzer, AnalysisResult, Failure, Severity


class GatewayAnalyzer(BaseAnalyzer):
    """
    Gateway分析器（Gateway API）- 基于SRE最佳实践设计
    
    检测能力：
    - Gateway引用的GatewayClass不存在
    - Gateway状态未接受（Accepted=False）
    
    使用示例：
    >>> analyzer = GatewayAnalyzer()
    >>> results = analyzer.analyze(namespace="production")
    
    NOTE: 需要集群支持Gateway API（CRD已安装）
    """
    
    @property
    def resource_kind(self) -> str:
        return "Gateway"
    
    def _do_analyze(self, namespace: str, label_selector: str) -> List[AnalysisResult]:
        """执行Gateway分析"""
        results = []
        custom_api = self.client.CustomObjectsApi()
        
        try:
            # 获取Gateway列表
            if namespace:
                gateway_list = custom_api.list_namespaced_custom_object(
                    group="gateway.networking.k8s.io",
                    version="v1",
                    namespace=namespace,
                    plural="gateways",
                    label_selector=label_selector
                )
            else:
                gateway_list = custom_api.list_cluster_custom_object(
                    group="gateway.networking.k8s.io",
                    version="v1",
                    plural="gateways",
                    label_selector=label_selector
                )
            
            # 获取GatewayClass列表
            try:
                gatewayclass_list = custom_api.list_cluster_custom_object(
                    group="gateway.networking.k8s.io",
                    version="v1",
                    plural="gatewayclasses"
                )
                gatewayclass_names = {gc["metadata"]["name"] for gc in gatewayclass_list.get("items", [])}
            except ApiException:
                gatewayclass_names = set()
            
            # 分析每个Gateway
            for gateway in gateway_list.get("items", []):
                failures = self._analyze_gateway(gateway, gatewayclass_names)
                if failures:
                    metadata = gateway.get("metadata", {})
                    spec = gateway.get("spec", {})
                    
                    result = AnalysisResult(
                        kind="Gateway",
                        name=metadata.get("name", "unknown"),
                        namespace=metadata.get("namespace", ""),
                        failures=failures,
                        details={
                            "gateway_class_name": spec.get("gatewayClassName", ""),
                            "listeners_count": len(spec.get("listeners", []))
                        }
                    )
                    results.append(result)
        
        except ApiException as e:
            if e.status == 404:
                # Gateway API未安装，返回空结果
                self._logger.info("Gateway API未安装，跳过分析")
            else:
                self._logger.error(f"分析Gateway时出错: {e}")
        
        return results
    
    def _analyze_gateway(self, gateway: Dict, gatewayclass_names: Set[str]) -> List[Failure]:
        """分析单个Gateway"""
        failures = []
        
        spec = gateway.get("spec", {})
        status = gateway.get("status", {})
        
        # 检查GatewayClass是否存在
        gateway_class_name = spec.get("gatewayClassName", "")
        if gateway_class_name and gateway_class_name not in gatewayclass_names:
            failures.append(Failure(
                text=f"Gateway使用的GatewayClass '{gateway_class_name}' 不存在",
                severity=Severity.CRITICAL,
                reason="GatewayClassNotFound",
                suggestion="1. 创建GatewayClass\n2. 或更新Gateway的gatewayClassName"
            ))
        
        # 检查Gateway状态
        conditions = status.get("conditions", [])
        accepted_found = False
        
        for condition in conditions:
            if condition.get("type") == "Accepted":
                accepted_found = True
                if condition.get("status") != "True":
                    failures.append(Failure(
                        text=f"Gateway未被接受: {condition.get('message', 'Unknown')}",
                        severity=Severity.CRITICAL,
                        reason="GatewayNotAccepted",
                        suggestion="1. 检查GatewayClass配置\n2. 查看控制器日志"
                    ))
                break
        
        if not accepted_found:
            failures.append(Failure(
                text="Gateway没有Accepted状态条件",
                severity=Severity.WARNING,
                reason="NoAcceptedCondition",
                suggestion="等待Gateway控制器处理"
            ))
        
        return failures
