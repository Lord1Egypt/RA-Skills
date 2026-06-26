"""
文件功能：CronJob分析器模块
主要类/函数：CronJobAnalyzer - 分析CronJob配置
作者：chenzc
创建时间：2026-04-03
最后修改：2026-04-03

LEARNING: 检测Cron表达式格式、调度配置问题
IMPORTANT: CronJob依赖定时调度，关注时间配置
"""

import re
from typing import List
try:
    from ..core import BaseAnalyzer, AnalysisResult, Failure, Severity
except ImportError:
    from core import BaseAnalyzer, AnalysisResult, Failure, Severity


class CronJobAnalyzer(BaseAnalyzer):
    """
    CronJob分析器 - 基于SRE最佳实践设计
    
    检测能力：
    - CronJob被挂起
    - Cron表达式格式无效
    - 负数的startingDeadlineSeconds
    
    使用示例：
    >>> analyzer = CronJobAnalyzer()
    >>> results = analyzer.analyze(namespace="scheduled-tasks")
    """
    
    @property
    def resource_kind(self) -> str:
        return "CronJob"
    
    def _do_analyze(self, namespace: str, label_selector: str) -> List[AnalysisResult]:
        """执行CronJob分析"""
        results = []
        batch_v1 = self.client.BatchV1Api()
        
        cronjobs = self._list_resources_paginated(
            list_func=batch_v1.list_cron_job_for_all_namespaces,
            cache_key="cronjobs",
            namespace=namespace,
            label_selector=label_selector
        )
        
        for cronjob in cronjobs:
            if namespace and cronjob.metadata.namespace != namespace:
                continue
            
            failures = self._analyze_cronjob(cronjob)
            if failures:
                spec = cronjob.spec
                
                result = self._create_result(
                    cronjob,
                    failures,
                    schedule=getattr(spec, 'schedule', ''),
                    suspend=getattr(spec, 'suspend', False),
                    concurrency_policy=getattr(spec, 'concurrency_policy', '')
                )
                results.append(result)
        
        self._logger.info(f"分析完成: {len(results)} 个CronJob发现问题")
        return results
    
    def _analyze_cronjob(self, cronjob) -> List[Failure]:
        """分析单个CronJob"""
        failures = []
        spec = cronjob.spec
        
        if not spec:
            return failures
        
        # 检查是否被挂起
        if getattr(spec, 'suspend', False):
            failures.append(Failure(
                text="CronJob被挂起",
                severity=Severity.INFO,
                reason="CronJobSuspended",
                suggestion="CronJob当前处于挂起状态，不会按计划执行"
            ))
            return failures
        
        # 检查Cron表达式格式（简化检查）
        schedule = spec.schedule
        if schedule:
            # 基本的Cron格式验证：5-6个字段
            parts = schedule.split()
            if len(parts) < 5 or len(parts) > 6:
                failures.append(Failure(
                    text=f"CronJob的调度表达式格式无效: {schedule}",
                    severity=Severity.WARNING,
                    reason="InvalidCronSchedule",
                    suggestion="1. 检查Cron表达式格式\n2. 参考: https://en.wikipedia.org/wiki/Cron"
                ))
        
        # 检查startingDeadlineSeconds
        deadline = getattr(spec, 'starting_deadline_seconds', None)
        if deadline is not None and deadline < 0:
            failures.append(Failure(
                text="CronJob的startingDeadlineSeconds为负数",
                severity=Severity.WARNING,
                reason="NegativeDeadline",
                suggestion="startingDeadlineSeconds必须是非负数"
            ))
        
        return failures
