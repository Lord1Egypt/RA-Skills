"""
文件功能：Secret分析器模块
主要类/函数：SecretAnalyzer - 分析Secret使用情况
作者：chenzc
创建时间：2026-04-03
最后修改：2026-04-03

LEARNING: 检测未使用的Secret、TLS证书格式问题
IMPORTANT: Secret包含敏感信息，关注安全性和正确使用
"""

from typing import List, Dict
try:
    from ..core import BaseAnalyzer, AnalysisResult, Failure, Severity
except ImportError:
    from core import BaseAnalyzer, AnalysisResult, Failure, Severity


class SecretAnalyzer(BaseAnalyzer):
    """
    Secret分析器 - 分析Secret使用情况和潜在问题
    
    检测能力：
    - 未被任何Pod使用的Secret
    - 空的Secret（无数据）
    - 缺少必要字段（如tls.crt/tls.key对于TLS类型）
    
    使用示例：
    >>> analyzer = SecretAnalyzer()
    >>> results = analyzer.analyze(namespace="production")
    """
    
    @property
    def resource_kind(self) -> str:
        return "Secret"
    
    def _do_analyze(self, namespace: str, label_selector: str) -> List[AnalysisResult]:
        """执行Secret分析"""
        results = []
        v1 = self.client.CoreV1Api()
        
        secrets = self._list_resources_paginated(
            list_func=v1.list_secret_for_all_namespaces,
            cache_key="secrets",
            namespace=namespace,
            label_selector=label_selector
        )
        
        # 获取所有Pod以检查Secret使用情况
        pods = self._list_resources_paginated(
            list_func=v1.list_pod_for_all_namespaces,
            cache_key="pods",
            namespace="",
            label_selector=""
        )
        
        used_secrets = self._get_used_secrets(pods)
        
        for secret in secrets:
            if namespace and secret.metadata.namespace != namespace:
                continue
            
            # 跳过系统Secret
            if getattr(secret, 'type', '') == "kubernetes.io/service-account-token":
                continue
            
            failures = self._analyze_secret(secret, used_secrets)
            if failures:
                data = getattr(secret, 'data', {})
                result = self._create_result(
                    secret,
                    failures,
                    type=getattr(secret, 'type', 'Opaque'),
                    data_keys=list(data.keys()) if data else []
                )
                results.append(result)
        
        self._logger.info(f"分析完成: {len(results)} 个Secret发现问题")
        return results
    
    def _get_used_secrets(self, pods) -> Dict[str, List[str]]:
        """获取被使用的Secret及其使用者"""
        used = {}
        
        for pod in pods.items if hasattr(pods, 'items') else pods:
            spec = pod.spec
            if not spec:
                continue
            
            pod_name = pod.metadata.name
            
            # 检查ImagePullSecrets
            for secret_ref in getattr(spec, 'image_pull_secrets', []) or []:
                secret_name = getattr(secret_ref, 'name', None)
                if secret_name:
                    if secret_name not in used:
                        used[secret_name] = []
                    used[secret_name].append(pod_name)
            
            # 检查Volume挂载
            for volume in getattr(spec, 'volumes', []) or []:
                if volume.secret:
                    secret_name = getattr(getattr(volume, 'secret', None), 'secret_name', None)
                    if secret_name:
                        if secret_name not in used:
                            used[secret_name] = []
                        used[secret_name].append(pod_name)
            
            # 检查环境变量
            for container in getattr(spec, 'containers', []) or []:
                for env in getattr(container, 'env', []) or []:
                    if env.value_from and env.value_from.secret_key_ref:
                        secret_name = getattr(getattr(env.value_from, 'secret_key_ref', None), 'name', None)
                        if secret_name:
                            if secret_name not in used:
                                used[secret_name] = []
                            used[secret_name].append(pod_name)
        
        return used
    
    def _analyze_secret(self, secret, used_secrets: Dict) -> List[Failure]:
        """分析单个Secret"""
        failures = []
        
        secret_name = secret.metadata.name
        secret_type = getattr(secret, 'type', 'Opaque')
        data = getattr(secret, 'data', {}) or {}
        
        # 检查是否被使用
        if secret_name not in used_secrets:
            failures.append(Failure(
                text="Secret未被任何Pod使用",
                severity=Severity.INFO,
                reason="UnusedSecret",
                suggestion="1. 删除未使用的Secret\n2. 或在Pod中引用此Secret"
            ))
        
        # 检查是否为空
        if not data:
            failures.append(Failure(
                text="Secret为空（无数据）",
                severity=Severity.INFO,
                reason="EmptySecret",
                suggestion="删除空的Secret或添加数据"
            ))
        
        # 检查TLS Secret格式
        if secret_type == "kubernetes.io/tls":
            if "tls.crt" not in data:
                failures.append(Failure(
                    text="TLS Secret缺少tls.crt字段",
                    severity=Severity.WARNING,
                    reason="MissingTLSCert",
                    suggestion="添加tls.crt证书数据"
                ))
            if "tls.key" not in data:
                failures.append(Failure(
                    text="TLS Secret缺少tls.key字段",
                    severity=Severity.WARNING,
                    reason="MissingTLSKey",
                    suggestion="添加tls.key私钥数据"
                ))
        
        # 检查docker-registry Secret格式
        if secret_type == "kubernetes.io/dockerconfigjson":
            if ".dockerconfigjson" not in data:
                failures.append(Failure(
                    text="Docker Registry Secret缺少.dockerconfigjson字段",
                    severity=Severity.WARNING,
                    reason="MissingDockerConfig",
                    suggestion="添加.dockerconfigjson认证数据"
                ))
        
        return failures
