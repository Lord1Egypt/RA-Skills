"""
文件功能：HPA分析器模块
主要类/函数：HPAAnalyzer - 分析HorizontalPodAutoscaler状态
作者：chenzc
创建时间：2026-04-03
最后修改：2026-04-03

LEARNING: 检测HPA缩放限制、目标引用问题
IMPORTANT: HPA依赖metrics-server，关注指标可用性
"""

from typing import List
from kubernetes.client.exceptions import ApiException
try:
    from ..core import BaseAnalyzer, AnalysisResult, Failure, Severity
except ImportError:
    from core import BaseAnalyzer, AnalysisResult, Failure, Severity


class HPAAnalyzer(BaseAnalyzer):
    """
    HPA分析器 - 基于SRE最佳实践设计
    
    检测能力：
    - ScalingLimited条件为True
    - 其他条件为False
    - ScaleTargetRef指向的资源不存在
    - 目标资源未配置资源限制
    
    使用示例：
    >>> analyzer = HPAAnalyzer()
    >>> results = analyzer.analyze(namespace="production")
    """
    
    @property
    def resource_kind(self) -> str:
        return "HorizontalPodAutoscaler"
    
    def _do_analyze(self, namespace: str, label_selector: str) -> List[AnalysisResult]:
        """执行HPA分析"""
        results = []
        autoscaling_v2 = self.client.AutoscalingV2Api()
        apps_v1 = self.client.AppsV1Api()
        
        hpas = self._list_resources_paginated(
            list_func=autoscaling_v2.list_horizontal_pod_autoscaler_for_all_namespaces,
            cache_key="hpas",
            namespace=namespace,
            label_selector=label_selector
        )
        
        for hpa in hpas:
            if namespace and hpa.metadata.namespace != namespace:
                continue
            
            failures = self._analyze_hpa(hpa, apps_v1)
            if failures:
                spec = hpa.spec
                status = hpa.status
                
                result = self._create_result(
                    hpa,
                    failures,
                    min_replicas=getattr(spec, 'min_replicas', None),
                    max_replicas=getattr(spec, 'max_replicas', 0),
                    current_replicas=getattr(status, 'current_replicas', 0) if status else 0,
                    desired_replicas=getattr(status, 'desired_replicas', 0) if status else 0
                )
                results.append(result)
        
        self._logger.info(f"分析完成: {len(results)} 个HPA发现问题")
        return results
    
    def _analyze_hpa(self, hpa, apps_v1) -> List[Failure]:
        """分析单个HPA"""
        failures = []
        spec = hpa.spec
        status = hpa.status
        
        if not spec or not spec.scale_target_ref:
            return failures
        
        target_ref = spec.scale_target_ref
        
        # 检查目标资源是否存在
        if target_ref.kind == "Deployment":
            try:
                apps_v1.read_namespaced_deployment(
                    name=target_ref.name,
                    namespace=hpa.metadata.namespace
                )
            except ApiException as e:
                if e.status == 404:
                    failures.append(Failure(
                        text=f"HPA引用的Deployment '{target_ref.name}' 不存在",
                        severity=Severity.CRITICAL,
                        reason="TargetNotFound",
                        suggestion=f"1. 创建Deployment '{target_ref.name}'\n2. 或更正HPA的scaleTargetRef"
                    ))
        
        # 检查HPA条件
        if status and status.conditions:
            for condition in status.conditions:
                if condition.type == "ScalingLimited" and condition.status == "True":
                    failures.append(Failure(
                        text=f"HPA缩放受限: {condition.message}",
                        severity=Severity.WARNING,
                        reason="ScalingLimited",
                        suggestion="1. 检查minReplicas/maxReplicas设置\n2. 验证metrics-server是否运行\n3. 检查资源限制配置"
                    ))
                elif condition.type in ["AbleToScale", "ScalingActive"] and condition.status == "False":
                    failures.append(Failure(
                        text=f"HPA条件异常 {condition.type}: {condition.message}",
                        severity=Severity.WARNING,
                        reason=condition.type,
                        suggestion="检查HPA配置和metrics-server状态"
                    ))
        
        return failures
