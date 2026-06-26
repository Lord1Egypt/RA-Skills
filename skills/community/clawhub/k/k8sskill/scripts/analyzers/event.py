"""
文件功能：Event分析器模块
主要类/函数：EventAnalyzer - 分析集群事件
作者：chenzc
创建时间：2026-04-03
最后修改：2026-04-03

LEARNING: 检测警告事件、异常事件模式
IMPORTANT: 事件是排查问题的重要线索
"""

from typing import List
from datetime import datetime, timedelta
try:
    from ..core import BaseAnalyzer, AnalysisResult, Failure, Severity
except ImportError:
    from core import BaseAnalyzer, AnalysisResult, Failure, Severity


class EventAnalyzer(BaseAnalyzer):
    """
    事件分析器 - 分析集群中的警告和异常事件
    
    检测能力：
    - 最近的警告事件
    - 重复发生的事件
    - 异常事件模式
    
    使用示例：
    >>> analyzer = EventAnalyzer()
    >>> results = analyzer.analyze(namespace="production", hours=1)
    """
    
    # 需要关注的警告事件类型
    WARNING_REASONS = {
        "Failed", "FailedScheduling", "FailedMount", "FailedCreatePodSandBox",
        "Unhealthy", "Killing", "BackOff", "FailedBinding"
    }
    
    @property
    def resource_kind(self) -> str:
        return "Event"
    
    def analyze(self, namespace: str = "", label_selector: str = "", hours: int = 1) -> List[AnalysisResult]:
        """
        分析事件（扩展参数hours）
        
        参数说明：
        - hours: [int] 分析最近几小时的事件，默认1小时
        """
        self._hours = hours
        return super().analyze(namespace, label_selector)
    
    def _do_analyze(self, namespace: str, label_selector: str) -> List[AnalysisResult]:
        """执行Event分析"""
        results = []
        v1 = self.client.CoreV1Api()
        
        # 计算时间范围
        hours = getattr(self, '_hours', 1)
        since_time = datetime.utcnow() - timedelta(hours=hours)
        since_time_str = since_time.strftime("%Y-%m-%dT%H:%M:%SZ")
        
        try:
            if namespace:
                events = v1.list_namespaced_event(
                    namespace=namespace,
                    field_selector=f"type=Warning,lastTimestamp>={since_time_str}"
                )
            else:
                events = v1.list_event_for_all_namespaces(
                    field_selector=f"type=Warning,lastTimestamp>={since_time_str}"
                )
            
            # 按涉及对象分组
            event_groups = {}
            for event in events.items:
                involved = event.involved_object
                key = f"{involved.kind}/{involved.namespace}/{involved.name}"
                
                if key not in event_groups:
                    event_groups[key] = {
                        "kind": involved.kind,
                        "name": involved.name,
                        "namespace": involved.namespace,
                        "events": []
                    }
                event_groups[key]["events"].append(event)
            
            # 分析每个对象的事件
            for key, group in event_groups.items():
                failures = self._analyze_events(group["events"])
                if failures:
                    result = AnalysisResult(
                        kind=group["kind"],
                        name=group["name"],
                        namespace=group["namespace"],
                        failures=failures,
                        details={"event_count": len(group["events"])}
                    )
                    results.append(result)
        
        except Exception as e:
            self._logger.error(f"分析事件时出错: {e}", exc_info=True)
        
        self._logger.info(f"分析完成: {len(results)} 个对象有警告事件")
        return results
    
    def _analyze_events(self, events: List) -> List[Failure]:
        """分析事件列表"""
        failures = []
        
        # 统计事件原因
        reason_counts = {}
        for event in events:
            reason = event.reason
            reason_counts[reason] = reason_counts.get(reason, 0) + 1
            
            # 关注特定原因
            if reason in self.WARNING_REASONS:
                if reason_counts[reason] == 1:  # 只记录一次
                    severity = Severity.CRITICAL if reason in ["Failed", "FailedScheduling"] else Severity.WARNING
                    failures.append(Failure(
                        text=f"{reason}: {event.message}",
                        severity=severity,
                        reason=reason,
                        suggestion=f"查看相关资源状态和日志，共发生 {reason_counts[reason]} 次"
                    ))
        
        return failures
