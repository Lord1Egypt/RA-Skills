"""
文件功能：Security分析器模块
主要类/函数：SecurityAnalyzer - 分析安全相关配置
作者：chenzc
创建时间：2026-04-03
最后修改：2026-04-03

LEARNING: 检测特权容器、不安全配置
IMPORTANT: 安全是生产环境的关键，关注最小权限原则
"""

from typing import List
try:
    from ..core import BaseAnalyzer, AnalysisResult, Failure, Severity
except ImportError:
    from core import BaseAnalyzer, AnalysisResult, Failure, Severity


class SecurityAnalyzer(BaseAnalyzer):
    """
    Security分析器 - 基于SRE最佳实践设计
    
    检测能力：
    - 特权容器（privileged=true）
    - 以root用户运行
    - 不安全的capabilities
    - 共享主机命名空间
    
    使用示例：
    >>> analyzer = SecurityAnalyzer()
    >>> results = analyzer.analyze(namespace="production")
    """
    
    @property
    def resource_kind(self) -> str:
        return "Security"
    
    def _do_analyze(self, namespace: str, label_selector: str) -> List[AnalysisResult]:
        """执行Security分析"""
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
            
            failures = self._analyze_pod_security(pod)
            if failures:
                result = self._create_result(
                    pod,
                    failures,
                    pod_name=pod.metadata.name
                )
                results.append(result)
        
        self._logger.info(f"分析完成: {len(results)} 个Pod存在安全问题")
        return results
    
    def _analyze_pod_security(self, pod) -> List[Failure]:
        """分析Pod安全配置"""
        failures = []
        spec = pod.spec
        
        if not spec:
            return failures
        
        # 检查主机命名空间共享
        if getattr(spec, 'host_network', False):
            failures.append(Failure(
                text="Pod使用hostNetwork（共享主机网络命名空间）",
                severity=Severity.WARNING,
                reason="HostNetwork",
                suggestion="避免使用hostNetwork，除非确实需要"
            ))
        
        if getattr(spec, 'host_pid', False):
            failures.append(Failure(
                text="Pod使用hostPID（共享主机PID命名空间）",
                severity=Severity.WARNING,
                reason="HostPID",
                suggestion="避免使用hostPID，除非确实需要"
            ))
        
        if getattr(spec, 'host_ipc', False):
            failures.append(Failure(
                text="Pod使用hostIPC（共享主机IPC命名空间）",
                severity=Severity.WARNING,
                reason="HostIPC",
                suggestion="避免使用hostIPC，除非确实需要"
            ))
        
        # 检查容器安全配置
        for container in getattr(spec, 'containers', []) or []:
            security_context = getattr(container, 'security_context', None)
            
            if security_context:
                # 检查特权模式
                if getattr(security_context, 'privileged', False):
                    failures.append(Failure(
                        text=f"容器 {container.name} 以特权模式运行",
                        severity=Severity.CRITICAL,
                        reason="PrivilegedContainer",
                        suggestion="1. 避免使用特权容器\n2. 使用securityContext.capabilities添加所需权限"
                    ))
                
                # 检查root用户
                run_as_user = getattr(security_context, 'run_as_user', None)
                if run_as_user == 0:
                    failures.append(Failure(
                        text=f"容器 {container.name} 以root用户运行（UID=0）",
                        severity=Severity.WARNING,
                        reason="RunAsRoot",
                        suggestion="1. 使用非root用户运行容器\n2. 在Dockerfile中设置USER指令"
                    ))
                
                # 检查capabilities
                capabilities = getattr(security_context, 'capabilities', None)
                if capabilities:
                    add_caps = getattr(capabilities, 'add', []) or []
                    dangerous_caps = {"NET_ADMIN", "SYS_ADMIN", "SYS_PTRACE", "SYS_MODULE", "DAC_READ_SEARCH"}
                    
                    for cap in add_caps:
                        if cap in dangerous_caps:
                            failures.append(Failure(
                                text=f"容器 {container.name} 添加了危险Capability: {cap}",
                                severity=Severity.WARNING,
                                reason="DangerousCapability",
                                suggestion=f"1. 移除不必要的Capability {cap}\n2. 使用最小权限原则"
                            ))
        
        return failures
