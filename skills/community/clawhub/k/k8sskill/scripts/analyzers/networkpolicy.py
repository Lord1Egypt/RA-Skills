"""
文件功能：NetworkPolicy分析器模块
主要类/函数：NetworkPolicyAnalyzer - 分析网络策略配置
作者：chenzc
创建时间：2026-04-03
最后修改：2026-04-03

LEARNING: 检测NetworkPolicy选择器问题、过度宽松策略
IMPORTANT: NetworkPolicy控制Pod间网络流量，关注安全性
"""

from typing import List
try:
    from ..core import BaseAnalyzer, AnalysisResult, Failure, Severity
except ImportError:
    from core import BaseAnalyzer, AnalysisResult, Failure, Severity


class NetworkPolicyAnalyzer(BaseAnalyzer):
    """
    NetworkPolicy分析器 - 基于SRE最佳实践设计
    
    检测能力：
    - NetworkPolicy允许所有Pod的流量（空selector）
    - NetworkPolicy未应用到任何Pod
    
    使用示例：
    >>> analyzer = NetworkPolicyAnalyzer()
    >>> results = analyzer.analyze(namespace="production")
    """
    
    @property
    def resource_kind(self) -> str:
        return "NetworkPolicy"
    
    def _do_analyze(self, namespace: str, label_selector: str) -> List[AnalysisResult]:
        """执行NetworkPolicy分析"""
        results = []
        networking_v1 = self.client.NetworkingV1Api()
        core_v1 = self.client.CoreV1Api()
        
        policies = self._list_resources_paginated(
            list_func=networking_v1.list_network_policy_for_all_namespaces,
            cache_key="networkpolicies",
            namespace=namespace,
            label_selector=label_selector
        )
        
        for policy in policies:
            if namespace and policy.metadata.namespace != namespace:
                continue
            
            failures = self._analyze_networkpolicy(policy, core_v1)
            if failures:
                spec = policy.spec
                
                result = self._create_result(
                    policy,
                    failures,
                    pod_selector=getattr(getattr(spec, 'pod_selector', None), 'match_labels', {}) if spec else {},
                    policy_types=getattr(spec, 'policy_types', []) if spec else []
                )
                results.append(result)
        
        self._logger.info(f"分析完成: {len(results)} 个NetworkPolicy发现问题")
        return results
    
    def _analyze_networkpolicy(self, policy, core_v1) -> List[Failure]:
        """分析单个NetworkPolicy"""
        failures = []
        spec = policy.spec
        
        if not spec:
            return failures
        
        pod_selector = getattr(spec, 'pod_selector', None)
        match_labels = getattr(pod_selector, 'match_labels', None) if pod_selector else None
        
        # 检查是否允许所有Pod的流量（空selector）
        if not match_labels:
            failures.append(Failure(
                text=f"NetworkPolicy '{policy.metadata.name}' 允许所有Pod的流量（未指定podSelector）",
                severity=Severity.WARNING,
                reason="AllowAllPods",
                suggestion="1. 指定podSelector以限制策略范围\n2. 考虑使用更具体的标签选择器"
            ))
        else:
            # 检查是否应用到任何Pod
            try:
                label_selector = ",".join([f"{k}={v}" for k, v in match_labels.items()])
                pod_list = core_v1.list_namespaced_pod(
                    namespace=policy.metadata.namespace,
                    label_selector=label_selector
                )
                
                if not pod_list.items:
                    failures.append(Failure(
                        text=f"NetworkPolicy '{policy.metadata.name}' 未应用到任何Pod",
                        severity=Severity.INFO,
                        reason="NoMatchingPods",
                        suggestion="1. 检查podSelector标签\n2. 确保有Pod匹配该标签"
                    ))
            except Exception:
                pass
        
        return failures
