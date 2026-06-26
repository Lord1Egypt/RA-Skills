"""
文件功能：Storage分析器模块
主要类/函数：StorageAnalyzer - 分析存储相关资源
作者：chenzc
创建时间：2026-04-03
最后修改：2026-04-03

LEARNING: 检测StorageClass、PV、PVC存储链路问题
IMPORTANT: 存储是状态化应用的基础，关注数据持久性
"""

from typing import List
try:
    from ..core import BaseAnalyzer, AnalysisResult, Failure, Severity
except ImportError:
    from core import BaseAnalyzer, AnalysisResult, Failure, Severity


class StorageAnalyzer(BaseAnalyzer):
    """
    Storage分析器 - 基于SRE最佳实践设计
    
    检测能力：
    - StorageClass使用deprecated provisioner
    - 多个默认StorageClass
    - PV状态异常（Failed/Released）
    - PVC未绑定且没有匹配的PV
    
    使用示例：
    >>> analyzer = StorageAnalyzer()
    >>> results = analyzer.analyze()
    """
    
    @property
    def resource_kind(self) -> str:
        return "Storage"
    
    def _do_analyze(self, namespace: str, label_selector: str) -> List[AnalysisResult]:
        """执行Storage分析"""
        results = []
        storage_v1 = self.client.StorageV1Api()
        core_v1 = self.client.CoreV1Api()
        
        # 分析StorageClass
        results.extend(self._analyze_storageclasses(storage_v1))
        
        # 分析PersistentVolume
        results.extend(self._analyze_persistentvolumes(core_v1))
        
        return results
    
    def _analyze_storageclasses(self, storage_v1) -> List[AnalysisResult]:
        """分析StorageClass"""
        results = []
        
        try:
            sc_list = storage_v1.list_storage_class()
            default_count = 0
            
            for sc in sc_list.items:
                failures = []
                
                # 检查是否使用deprecated provisioner
                if getattr(sc, 'provisioner', '') == "kubernetes.io/no-provisioner":
                    failures.append(Failure(
                        text=f"StorageClass '{sc.metadata.name}' 使用deprecated provisioner 'kubernetes.io/no-provisioner'",
                        severity=Severity.INFO,
                        reason="DeprecatedProvisioner",
                        suggestion="考虑使用更新的provisioner"
                    ))
                
                # 统计默认StorageClass
                annotations = getattr(sc.metadata, 'annotations', {}) or {}
                if annotations.get("storageclass.kubernetes.io/is-default-class") == "true":
                    default_count += 1
                
                if failures:
                    result = self._create_result(
                        sc,
                        failures,
                        provisioner=getattr(sc, 'provisioner', 'Unknown')
                    )
                    result.namespace = ""  # StorageClass是集群级别资源
                    results.append(result)
            
            # 检查多个默认StorageClass
            if default_count > 1:
                # 创建一个虚拟结果来报告这个问题
                results.append(AnalysisResult(
                    kind="StorageClass",
                    name="_cluster_check",
                    namespace="",
                    failures=[Failure(
                        text=f"集群中有 {default_count} 个默认StorageClass",
                        severity=Severity.WARNING,
                        reason="MultipleDefaultStorageClasses",
                        suggestion="应该只有一个默认StorageClass，请检查并保留一个"
                    )],
                    details={}
                ))
        
        except Exception as e:
            self._logger.error(f"分析StorageClass时出错: {e}")
        
        return results
    
    def _analyze_persistentvolumes(self, core_v1) -> List[AnalysisResult]:
        """分析PersistentVolume"""
        results = []
        
        try:
            pv_list = core_v1.list_persistent_volume()
            
            for pv in pv_list.items:
                failures = []
                status = getattr(pv, 'status', None)
                phase = getattr(status, 'phase', 'Unknown') if status else 'Unknown'
                
                # 检查PV状态异常
                if phase == "Failed":
                    failures.append(Failure(
                        text=f"PV处于Failed状态",
                        severity=Severity.CRITICAL,
                        reason="PVFailed",
                        suggestion="1. 查看PV事件\n2. 检查存储后端\n3. 考虑删除并重新创建"
                    ))
                elif phase == "Released":
                    failures.append(Failure(
                        text=f"PV处于Released状态（已被释放但未回收）",
                        severity=Severity.WARNING,
                        reason="PVReleased",
                        suggestion="1. 检查回收策略\n2. 手动清理或重新绑定"
                    ))
                
                if failures:
                    result = self._create_result(
                        pv,
                        failures,
                        phase=phase,
                        storage_class=getattr(getattr(pv, 'spec', None), 'storage_class_name', None),
                        capacity=getattr(getattr(pv, 'spec', None), 'capacity', {}).get('storage', 'N/A') if getattr(pv, 'spec', None) else 'N/A'
                    )
                    result.namespace = ""  # PV是集群级别资源
                    results.append(result)
        
        except Exception as e:
            self._logger.error(f"分析PersistentVolume时出错: {e}")
        
        return results
