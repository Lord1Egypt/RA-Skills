"""
文件功能：PVC分析器模块
主要类/函数：PVCAnalyzer - 分析PersistentVolumeClaim状态
作者：chenzc
创建时间：2026-04-03
最后修改：2026-04-03

LEARNING: 检测PVC绑定状态、存储供应失败
IMPORTANT: PVC依赖StorageClass和PV，关注存储链路
"""

from typing import List
try:
    from ..core import BaseAnalyzer, AnalysisResult, Failure, Severity
except ImportError:
    from core import BaseAnalyzer, AnalysisResult, Failure, Severity


class PVCAnalyzer(BaseAnalyzer):
    """
    PVC分析器 - 基于SRE最佳实践设计
    
    检测能力：
    - PVC绑定状态（Pending）
    - 存储供应失败（ProvisioningFailed）
    - 容量不足警告
    
    使用示例：
    >>> analyzer = PVCAnalyzer()
    >>> results = analyzer.analyze(namespace="production")
    >>> for r in results:
    ...     if r.has_issues:
    ...         print(f"PVC {r.name} 绑定失败: {r.failures[0].text}")
    """
    
    @property
    def resource_kind(self) -> str:
        return "PersistentVolumeClaim"
    
    def _do_analyze(self, namespace: str, label_selector: str) -> List[AnalysisResult]:
        """执行PVC分析"""
        results = []
        v1 = self.client.CoreV1Api()
        
        pvcs = self._list_resources_paginated(
            list_func=v1.list_persistent_volume_claim_for_all_namespaces,
            cache_key="pvcs",
            namespace=namespace,
            label_selector=label_selector
        )
        
        for pvc in pvcs:
            if namespace and pvc.metadata.namespace != namespace:
                continue
            
            failures = self._analyze_pvc(pvc, v1)
            if failures:
                spec = pvc.spec
                status = pvc.status
                
                capacity = {}
                if status and status.capacity:
                    capacity = status.capacity
                
                result = self._create_result(
                    pvc,
                    failures,
                    phase=status.phase if status else "Unknown",
                    storage_class=getattr(spec, 'storage_class_name', None) if spec else None,
                    capacity=capacity.get('storage', 'N/A'),
                    access_modes=getattr(spec, 'access_modes', []) if spec else []
                )
                results.append(result)
        
        self._logger.info(f"分析完成: {len(results)} 个PVC发现问题")
        return results
    
    def _analyze_pvc(self, pvc, v1) -> List[Failure]:
        """分析单个PVC"""
        failures = []
        status = pvc.status
        
        if not status:
            return failures
        
        # 检查Pending状态
        if status.phase == "Pending":
            # 尝试获取相关事件
            try:
                events = v1.list_namespaced_event(
                    namespace=pvc.metadata.namespace,
                    field_selector=f"involvedObject.name={pvc.metadata.name}"
                )
                
                provisioning_failed = False
                for event in events.items:
                    if event.reason == "ProvisioningFailed" and event.message:
                        failures.append(Failure(
                            text=f"存储供应失败: {event.message}",
                            severity=Severity.CRITICAL,
                            reason="ProvisioningFailed",
                            suggestion="1. 检查StorageClass配置\n2. 验证存储后端可用性\n3. 查看存储供应商日志"
                        ))
                        provisioning_failed = True
                        break
                
                if not provisioning_failed:
                    failures.append(Failure(
                        text="PVC处于Pending状态，等待存储供应",
                        severity=Severity.WARNING,
                        reason="Pending",
                        suggestion="1. 检查StorageClass是否存在\n2. 确认存储后端有足够资源\n3. 查看PVC事件: kubectl describe pvc"
                    ))
                    
            except Exception:
                pass
        
        return failures
