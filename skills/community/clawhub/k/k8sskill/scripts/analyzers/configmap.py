"""
文件功能：ConfigMap分析器模块
主要类/函数：ConfigMapAnalyzer - 分析ConfigMap使用情况
作者：chenzc
创建时间：2026-04-03
最后修改：2026-04-03

LEARNING: 检测未使用的ConfigMap
IMPORTANT: ConfigMap是配置管理，关注资源利用率
"""

from typing import List, Dict, Set
try:
    from ..core import BaseAnalyzer, AnalysisResult, Failure, Severity
except ImportError:
    from core import BaseAnalyzer, AnalysisResult, Failure, Severity


class ConfigMapAnalyzer(BaseAnalyzer):
    """
    ConfigMap分析器 - 基于SRE最佳实践设计
    
    检测能力：
    - 未被任何Pod使用的ConfigMap
    - 空的ConfigMap（无数据）
    
    使用示例：
    >>> analyzer = ConfigMapAnalyzer()
    >>> results = analyzer.analyze(namespace="production")
    """
    
    @property
    def resource_kind(self) -> str:
        return "ConfigMap"
    
    def _do_analyze(self, namespace: str, label_selector: str) -> List[AnalysisResult]:
        """执行ConfigMap分析"""
        results = []
        v1 = self.client.CoreV1Api()
        
        configmaps = self._list_resources_paginated(
            list_func=v1.list_config_map_for_all_namespaces,
            cache_key="configmaps",
            namespace=namespace,
            label_selector=label_selector
        )
        
        # 获取所有Pod以检查ConfigMap使用情况
        pods = self._list_resources_paginated(
            list_func=v1.list_pod_for_all_namespaces,
            cache_key="pods",
            namespace="",
            label_selector=""
        )
        
        used_configmaps = self._get_used_configmaps(pods)
        
        for cm in configmaps:
            if namespace and cm.metadata.namespace != namespace:
                continue
            
            # 跳过系统ConfigMap
            if cm.metadata.name.startswith("kube-") or cm.metadata.name.startswith("extension-"):
                continue
            
            failures = self._analyze_configmap(cm, used_configmaps)
            if failures:
                result = self._create_result(
                    cm,
                    failures,
                    data_keys=list(getattr(cm, 'data', {}).keys()) if getattr(cm, 'data', None) else []
                )
                results.append(result)
        
        self._logger.info(f"分析完成: {len(results)} 个ConfigMap发现问题")
        return results
    
    def _get_used_configmaps(self, pods) -> Set[str]:
        """获取被使用的ConfigMap集合"""
        used = set()
        
        for pod in pods.items if hasattr(pods, 'items') else pods:
            spec = pod.spec
            if not spec:
                continue
            
            # 检查Volume挂载
            for volume in getattr(spec, 'volumes', []) or []:
                if volume.config_map:
                    name = getattr(getattr(volume, 'config_map', None), 'name', None)
                    if name:
                        used.add(f"{pod.metadata.namespace}/{name}")
            
            # 检查环境变量引用
            for container in getattr(spec, 'containers', []) or []:
                for env_from in getattr(container, 'env_from', []) or []:
                    if env_from.config_map_ref:
                        name = getattr(getattr(env_from, 'config_map_ref', None), 'name', None)
                        if name:
                            used.add(f"{pod.metadata.namespace}/{name}")
                
                for env in getattr(container, 'env', []) or []:
                    if env.value_from and env.value_from.config_map_key_ref:
                        name = getattr(getattr(env.value_from, 'config_map_key_ref', None), 'name', None)
                        if name:
                            used.add(f"{pod.metadata.namespace}/{name}")
        
        return used
    
    def _analyze_configmap(self, cm, used_configmaps: Set[str]) -> List[Failure]:
        """分析单个ConfigMap"""
        failures = []
        
        cm_key = f"{cm.metadata.namespace}/{cm.metadata.name}"
        
        # 检查是否被使用
        if cm_key not in used_configmaps:
            failures.append(Failure(
                text="ConfigMap未被任何Pod使用",
                severity=Severity.INFO,
                reason="UnusedConfigMap",
                suggestion="1. 删除未使用的ConfigMap\n2. 或在Pod中引用此ConfigMap"
            ))
        
        # 检查是否为空
        data = getattr(cm, 'data', None)
        if not data:
            failures.append(Failure(
                text="ConfigMap为空（无数据）",
                severity=Severity.INFO,
                reason="EmptyConfigMap",
                suggestion="删除空的ConfigMap或添加配置数据"
            ))
        
        return failures
