"""
文件功能：Pod分析器模块
主要类/函数：PodAnalyzer - 分析Pod状态和故障
作者：chenzc
创建时间：2026-04-03
最后修改：2026-04-03

LEARNING: 基于SRE最佳实践设计Pod故障检测
IMPORTANT: 检测CrashLoopBackOff、ImagePullBackOff等常见故障
"""

from typing import List
try:
    from ..core import BaseAnalyzer, AnalysisResult, Failure, Severity
except ImportError:
    from core import BaseAnalyzer, AnalysisResult, Failure, Severity


class PodAnalyzer(BaseAnalyzer):
    """
    Pod分析器 - 基于SRE最佳实践设计
    
    检测能力：
    - Pending状态分析（Unschedulable等）
    - Container状态检查（CrashLoopBackOff、OOMKilled等）
    - Init容器错误
    - 健康检查失败
    
    使用示例：
    >>> analyzer = PodAnalyzer()
    >>> results = analyzer.analyze(namespace="production")
    >>> for r in results:
    ...     if r.has_issues:
    ...         print(f"Pod {r.name} 有问题: {r.failures[0].text}")
    """
    
    # 故障原因关键词映射
    ERROR_REASONS = {
        "CrashLoopBackOff", "ImagePullBackOff", "CreateContainerConfigError",
        "PreCreateHookError", "CreateContainerError", "PreStartHookError",
        "RunContainerError", "ImageInspectError", "ErrImagePull",
        "ErrImageNeverPull", "InvalidImageName"
    }
    
    @property
    def resource_kind(self) -> str:
        return "Pod"
    
    def _do_analyze(self, namespace: str, label_selector: str) -> List[AnalysisResult]:
        """执行Pod分析"""
        results = []
        v1 = self.client.CoreV1Api()
        
        pods = self._list_resources_paginated(
            list_func=v1.list_pod_for_all_namespaces,
            cache_key="pods",
            namespace=namespace,
            label_selector=label_selector
        )
        
        for pod in pods:
            if namespace and pod.metadata.namespace != namespace:
                continue
            
            failures = self._analyze_pod(pod)
            if failures:
                result = self._create_result(
                    pod,
                    failures,
                    phase=pod.status.phase if pod.status else "Unknown",
                    restart_count=self._get_restart_count(pod),
                    node_name=pod.spec.node_name if pod.spec else None
                )
                results.append(result)
        
        self._logger.info(f"分析完成: {len(results)} 个Pod发现问题")
        return results
    
    def _analyze_pod(self, pod) -> List[Failure]:
        """分析单个Pod"""
        failures = []
        
        if not pod or not pod.status:
            return failures
        
        if pod.status.phase == "Pending":
            failures.extend(self._check_pending_status(pod))
        
        if pod.status.init_container_statuses:
            failures.extend(self._check_containers(
                pod.status.init_container_statuses,
                pod.metadata.name if pod.metadata else "unknown",
                "Init"
            ))
        
        if pod.status.container_statuses:
            failures.extend(self._check_containers(
                pod.status.container_statuses,
                pod.metadata.name if pod.metadata else "unknown",
                pod.status.phase
            ))
        
        return failures
    
    def _check_pending_status(self, pod) -> List[Failure]:
        """检查Pending状态的Pod"""
        failures = []
        
        if pod.status.conditions:
            for condition in pod.status.conditions:
                if condition.type == "PodScheduled" and condition.reason == "Unschedulable":
                    failures.append(Failure(
                        text=condition.message or "Pod无法调度",
                        severity=Severity.CRITICAL,
                        reason="Unschedulable",
                        suggestion="检查节点资源、亲和性规则或污点"
                    ))
        
        return failures
    
    def _check_containers(self, statuses, pod_name: str, phase: str) -> List[Failure]:
        """检查容器状态"""
        failures = []
        
        if not statuses:
            return failures
        
        for container in statuses:
            if not container:
                continue
            
            container_name = container.name if hasattr(container, 'name') else "unknown"
            
            # 检查Waiting状态
            if container.state and container.state.waiting:
                waiting = container.state.waiting
                reason = waiting.reason if waiting.reason else "Unknown"
                
                if reason == "CrashLoopBackOff":
                    last_reason = "Unknown"
                    if container.last_state and container.last_state.terminated:
                        last_reason = container.last_state.terminated.reason or "Unknown"
                    
                    failures.append(Failure(
                        text=f"容器 {container_name} 处于 CrashLoopBackOff，上次终止原因: {last_reason}",
                        severity=Severity.CRITICAL,
                        reason="CrashLoopBackOff",
                        suggestion=f"1. 查看日志: kubectl logs {pod_name} --previous\n2. 检查资源限制\n3. 验证镜像和配置"
                    ))
                
                elif reason == "ImagePullBackOff":
                    failures.append(Failure(
                        text=f"容器 {container_name} 镜像拉取失败",
                        severity=Severity.CRITICAL,
                        reason="ImagePullBackOff",
                        suggestion="1. 检查镜像名称和标签\n2. 验证镜像仓库访问权限\n3. 检查网络连接"
                    ))
                
                elif reason in self.ERROR_REASONS and waiting.message:
                    failures.append(Failure(
                        text=f"容器 {container_name}: {waiting.message}",
                        severity=Severity.CRITICAL,
                        reason=reason,
                        suggestion="检查容器配置和镜像"
                    ))
            
            # 检查Terminated状态
            elif container.state and container.state.terminated:
                terminated = container.state.terminated
                exit_code = terminated.exit_code if terminated.exit_code is not None else -1
                term_reason = terminated.reason if terminated.reason else "Unknown"
                if exit_code != 0:
                    failures.append(Failure(
                        text=f"容器 {container_name} 异常终止，Exit Code: {exit_code}, Reason: {term_reason}",
                        severity=Severity.WARNING,
                        reason=term_reason,
                        suggestion="查看容器日志分析退出原因"
                    ))
            
            # 检查未就绪状态
            elif hasattr(container, 'ready') and not container.ready and phase == "Running":
                failures.append(Failure(
                    text=f"容器 {container_name} 运行中但未就绪（健康检查失败）",
                    severity=Severity.WARNING,
                    reason="NotReady",
                    suggestion="1. 检查 readinessProbe 配置\n2. 查看应用日志\n3. 验证依赖服务可用性"
                ))
        
        return failures
    
    def _get_restart_count(self, pod) -> int:
        """获取Pod总重启次数"""
        count = 0
        if pod.status and pod.status.container_statuses:
            for c in pod.status.container_statuses:
                count += getattr(c, 'restart_count', 0)
        return count
