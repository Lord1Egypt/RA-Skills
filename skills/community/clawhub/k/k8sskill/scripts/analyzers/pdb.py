"""
文件功能：PDB分析器模块
主要类/函数：PDBAnalyzer - 分析PodDisruptionBudget状态
作者：chenzc
创建时间：2026-04-03
最后修改：2026-04-03

LEARNING: 检测PDB中断允许状态、选择器匹配问题
IMPORTANT: PDB保护Pod免受自愿中断，关注高可用性
"""

from typing import List
try:
    from ..core import BaseAnalyzer, AnalysisResult, Failure, Severity
except ImportError:
    from core import BaseAnalyzer, AnalysisResult, Failure, Severity


class PDBAnalyzer(BaseAnalyzer):
    """
    PodDisruptionBudget分析器 - 基于SRE最佳实践设计
    
    检测能力：
    - PDB不允许中断（DisruptionAllowed=False）
    - PDB选择器不匹配任何Pod
    
    使用示例：
    >>> analyzer = PDBAnalyzer()
    >>> results = analyzer.analyze(namespace="production")
    """
    
    @property
    def resource_kind(self) -> str:
        return "PodDisruptionBudget"
    
    def _do_analyze(self, namespace: str, label_selector: str) -> List[AnalysisResult]:
        """执行PDB分析"""
        results = []
        policy_v1 = self.client.PolicyV1Api()
        core_v1 = self.client.CoreV1Api()
        
        pdbs = self._list_resources_paginated(
            list_func=policy_v1.list_pod_disruption_budget_for_all_namespaces,
            cache_key="pdbs",
            namespace=namespace,
            label_selector=label_selector
        )
        
        for pdb in pdbs:
            if namespace and pdb.metadata.namespace != namespace:
                continue
            
            failures = self._analyze_pdb(pdb, core_v1)
            if failures:
                spec = pdb.spec
                selector = getattr(getattr(spec, 'selector', None), 'match_labels', {}) if spec else {}
                
                result = self._create_result(
                    pdb,
                    failures,
                    min_available=getattr(spec, 'min_available', None),
                    max_unavailable=getattr(spec, 'max_unavailable', None),
                    selector=selector
                )
                results.append(result)
        
        self._logger.info(f"分析完成: {len(results)} 个PDB发现问题")
        return results
    
    def _analyze_pdb(self, pdb, core_v1) -> List[Failure]:
        """分析单个PDB"""
        failures = []
        status = pdb.status
        spec = pdb.spec
        
        if not spec:
            return failures
        
        # 检查PDB状态
        if status and status.conditions:
            for condition in status.conditions:
                if condition.type == "DisruptionAllowed" and condition.status == "False":
                    selector = getattr(getattr(spec, 'selector', None), 'match_labels', {}) or {}
                    label_str = ", ".join([f"{k}={v}" for k, v in selector.items()])
                    
                    failures.append(Failure(
                        text=f"PDB不允许中断: {getattr(condition, 'reason', 'Unknown')}，期望Pod标签: {label_str}",
                        severity=Severity.WARNING,
                        reason="DisruptionNotAllowed",
                        suggestion="1. 检查匹配Pod数量\n2. 调整minAvailable/maxUnavailable\n3. 检查Pod标签"
                    ))
        
        # 检查PDB选择器是否匹配任何Pod
        selector = getattr(getattr(spec, 'selector', None), 'match_labels', None)
        if selector:
            try:
                label_selector = ",".join([f"{k}={v}" for k, v in selector.items()])
                pod_list = core_v1.list_namespaced_pod(
                    namespace=pdb.metadata.namespace,
                    label_selector=label_selector
                )
                
                if not pod_list.items:
                    failures.append(Failure(
                        text="PDB选择器未匹配到任何Pod",
                        severity=Severity.WARNING,
                        reason="NoMatchingPods",
                        suggestion="1. 检查selector标签\n2. 确保有Pod使用该标签"
                    ))
            except Exception:
                pass
        
        return failures
