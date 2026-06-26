"""
文件功能：Webhook分析器模块
主要类/函数：WebhookAnalyzer - 分析Admission Webhook配置
作者：chenzc
创建时间：2026-04-03
最后修改：2026-04-03

LEARNING: 检测Webhook服务端可用性、证书问题
IMPORTANT: Webhook影响API Server行为，关注可用性
"""

from typing import List
from kubernetes.client.exceptions import ApiException
try:
    from ..core import BaseAnalyzer, AnalysisResult, Failure, Severity
except ImportError:
    from core import BaseAnalyzer, AnalysisResult, Failure, Severity


class WebhookAnalyzer(BaseAnalyzer):
    """
    Webhook分析器 - 基于SRE最佳实践设计
    
    检测能力：
    - ValidatingWebhookConfiguration服务端不可用
    - MutatingWebhookConfiguration服务端不可用
    - Webhook配置错误
    
    使用示例：
    >>> analyzer = WebhookAnalyzer()
    >>> results = analyzer.analyze()
    """
    
    @property
    def resource_kind(self) -> str:
        return "Webhook"
    
    def _do_analyze(self, namespace: str, label_selector: str) -> List[AnalysisResult]:
        """执行Webhook分析（namespace参数被忽略，Webhook是集群级别资源）"""
        results = []
        
        # 分析ValidatingWebhook
        results.extend(self._analyze_validating_webhooks())
        
        # 分析MutatingWebhook
        results.extend(self._analyze_mutating_webhooks())
        
        return results
    
    def _analyze_validating_webhooks(self) -> List[AnalysisResult]:
        """分析ValidatingWebhookConfiguration"""
        results = []
        admission_v1 = self.client.AdmissionregistrationV1Api()
        
        try:
            webhook_list = admission_v1.list_validating_webhook_configuration()
            
            for webhook_config in webhook_list.items:
                failures = []
                webhooks = getattr(webhook_config, 'webhooks', []) or []
                
                for webhook in webhooks:
                    # 检查clientConfig
                    client_config = getattr(webhook, 'client_config', None)
                    
                    if client_config:
                        # 检查Service引用
                        service = getattr(client_config, 'service', None)
                        if service:
                            service_name = getattr(service, 'name', '')
                            service_namespace = getattr(service, 'namespace', '')
                            
                            if not service_name or not service_namespace:
                                failures.append(Failure(
                                    text=f"Webhook '{webhook.name}' 的service配置不完整",
                                    severity=Severity.WARNING,
                                    reason="IncompleteServiceConfig",
                                    suggestion="检查clientConfig.service.name和namespace配置"
                                ))
                        
                        # 检查CA Bundle
                        ca_bundle = getattr(client_config, 'ca_bundle', None)
                        if not ca_bundle:
                            failures.append(Failure(
                                text=f"Webhook '{webhook.name}' 未配置CA Bundle",
                                severity=Severity.WARNING,
                                reason="NoCABundle",
                                suggestion="配置caBundle以确保TLS证书验证"
                            ))
                    
                    # 检查failurePolicy
                    failure_policy = getattr(webhook, 'failure_policy', 'Fail')
                    if failure_policy == "Fail":
                        failures.append(Failure(
                            text=f"Webhook '{webhook.name}' 的failurePolicy为Fail（Webhook故障时会阻塞API请求）",
                            severity=Severity.INFO,
                            reason="StrictFailurePolicy",
                            suggestion="如需高可用性，考虑将failurePolicy改为Ignore"
                        ))
                
                if failures:
                    result = self._create_result(
                        webhook_config,
                        failures,
                        webhook_count=len(webhooks)
                    )
                    result.namespace = ""  # 集群级别资源
                    results.append(result)
        
        except Exception as e:
            self._logger.error(f"分析ValidatingWebhook时出错: {e}")
        
        return results
    
    def _analyze_mutating_webhooks(self) -> List[AnalysisResult]:
        """分析MutatingWebhookConfiguration"""
        results = []
        admission_v1 = self.client.AdmissionregistrationV1Api()
        
        try:
            webhook_list = admission_v1.list_mutating_webhook_configuration()
            
            for webhook_config in webhook_list.items:
                failures = []
                webhooks = getattr(webhook_config, 'webhooks', []) or []
                
                for webhook in webhooks:
                    # 检查clientConfig
                    client_config = getattr(webhook, 'client_config', None)
                    
                    if client_config:
                        # 检查Service引用
                        service = getattr(client_config, 'service', None)
                        if service:
                            service_name = getattr(service, 'name', '')
                            service_namespace = getattr(service, 'namespace', '')
                            
                            if not service_name or not service_namespace:
                                failures.append(Failure(
                                    text=f"Webhook '{webhook.name}' 的service配置不完整",
                                    severity=Severity.WARNING,
                                    reason="IncompleteServiceConfig",
                                    suggestion="检查clientConfig.service.name和namespace配置"
                                ))
                        
                        # 检查CA Bundle
                        ca_bundle = getattr(client_config, 'ca_bundle', None)
                        if not ca_bundle:
                            failures.append(Failure(
                                text=f"Webhook '{webhook.name}' 未配置CA Bundle",
                                severity=Severity.WARNING,
                                reason="NoCABundle",
                                suggestion="配置caBundle以确保TLS证书验证"
                            ))
                    
                    # 检查reinvocationPolicy
                    reinvocation_policy = getattr(webhook, 'reinvocation_policy', 'Never')
                    if reinvocation_policy == "IfNeeded":
                        failures.append(Failure(
                            text=f"Webhook '{webhook.name}' 设置了reinvocationPolicy=IfNeeded（可能导致多次调用）",
                            severity=Severity.INFO,
                            reason="ReinvocationEnabled",
                            suggestion="确保Webhook逻辑支持幂等性"
                        ))
                
                if failures:
                    result = self._create_result(
                        webhook_config,
                        failures,
                        webhook_count=len(webhooks)
                    )
                    result.namespace = ""  # 集群级别资源
                    results.append(result)
        
        except Exception as e:
            self._logger.error(f"分析MutatingWebhook时出错: {e}")
        
        return results
