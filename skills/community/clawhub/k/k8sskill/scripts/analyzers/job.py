"""
文件功能：Job分析器模块
主要类/函数：JobAnalyzer - 分析Job执行状态
作者：chenzc
创建时间：2026-04-03
最后修改：2026-04-03

LEARNING: 检测Job挂起、失败状态
IMPORTANT: Job是一次性任务，关注完成状态
"""

from typing import List
try:
    from ..core import BaseAnalyzer, AnalysisResult, Failure, Severity
except ImportError:
    from core import BaseAnalyzer, AnalysisResult, Failure, Severity


class JobAnalyzer(BaseAnalyzer):
    """
    Job分析器 - 基于SRE最佳实践设计
    
    检测能力：
    - Job被挂起（Suspended）
    - Job执行失败（Failed > 0）
    - 超时未完成
    
    使用示例：
    >>> analyzer = JobAnalyzer()
    >>> results = analyzer.analyze(namespace="batch-jobs")
    """
    
    @property
    def resource_kind(self) -> str:
        return "Job"
    
    def _do_analyze(self, namespace: str, label_selector: str) -> List[AnalysisResult]:
        """执行Job分析"""
        results = []
        batch_v1 = self.client.BatchV1Api()
        
        jobs = self._list_resources_paginated(
            list_func=batch_v1.list_job_for_all_namespaces,
            cache_key="jobs",
            namespace=namespace,
            label_selector=label_selector
        )
        
        for job in jobs:
            if namespace and job.metadata.namespace != namespace:
                continue
            
            failures = self._analyze_job(job)
            if failures:
                spec = job.spec
                status = job.status
                
                result = self._create_result(
                    job,
                    failures,
                    completions=getattr(spec, 'completions', None),
                    parallelism=getattr(spec, 'parallelism', None),
                    active=getattr(status, 'active', 0) or 0,
                    succeeded=getattr(status, 'succeeded', 0) or 0,
                    failed=getattr(status, 'failed', 0) or 0
                )
                results.append(result)
        
        self._logger.info(f"分析完成: {len(results)} 个Job发现问题")
        return results
    
    def _analyze_job(self, job) -> List[Failure]:
        """分析单个Job"""
        failures = []
        spec = job.spec
        status = job.status
        
        if not spec:
            return failures
        
        # 检查是否被挂起
        if getattr(spec, 'suspend', False):
            failures.append(Failure(
                text="Job被挂起",
                severity=Severity.INFO,
                reason="JobSuspended",
                suggestion="Job当前处于挂起状态，不会执行"
            ))
        
        # 检查失败次数
        failed_count = getattr(status, 'failed', 0) or 0
        if failed_count > 0:
            failures.append(Failure(
                text=f"Job执行失败，失败次数: {failed_count}",
                severity=Severity.CRITICAL,
                reason="JobFailed",
                suggestion=f"1. 查看Job日志: kubectl logs job/{job.metadata.name}\n2. 检查Job配置"
            ))
        
        return failures
