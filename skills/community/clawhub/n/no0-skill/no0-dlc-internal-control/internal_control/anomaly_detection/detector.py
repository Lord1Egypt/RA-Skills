"""
异常检测与上报模块

检测异常访问模式并上报：
- 高频拒绝检测（短时间内多次被拒绝）
- 敏感数据异常访问（L5/L6尝试访问）
- 批量操作异常（超大批量导出）
- 跨域传输异常（敏感数据跨境）
- 时间异常（非工作时间访问）
- 权限升级异常（低权限Agent尝试高权限操作）

上报方式：
- 本地日志记录
- 系统通知
- 可选：飞书/钉钉通知
"""

import asyncio
import logging
from datetime import datetime, timedelta
from enum import Enum
from typing import Dict, List, Optional, Any, Callable, Set
from dataclasses import dataclass, field
from collections import defaultdict
import threading

from ..reference_monitor import (
    AccessDecision, DataLevel, AccessOperation, AuditEventType
)

logger = logging.getLogger(__name__)


class AnomalyType(Enum):
    """异常类型"""
    HIGH_FREQUENCY_DENIAL = "high_frequency_denial"      # 高频拒绝
    SENSITIVE_ACCESS_ATTEMPT = "sensitive_access_attempt"  # 敏感数据尝试访问
    BULK_OPERATION_ANOMALY = "bulk_operation_anomaly"    # 批量操作异常
    CROSS_DOMAIN_SENSITIVE = "cross_domain_sensitive"    # 跨境敏感传输
    OFF_HOURS_ACCESS = "off_hours_access"                # 非工作时间访问
    PRIVILEGE_ESCALATION = "privilege_escalation"        # 权限升级尝试
    UNUSUAL_PATTERN = "unusual_pattern"                  # 异常模式
    SYSTEM_DEGRADATION = "system_degradation"            # 系统降级


class AnomalySeverity(Enum):
    """异常严重程度"""
    LOW = "low"           # 低 - 记录即可
    MEDIUM = "medium"     # 中 - 通知管理员
    HIGH = "high"         # 高 - 立即告警
    CRITICAL = "critical" # 严重 - 阻断并告警


@dataclass
class AnomalyEvent:
    """异常事件"""
    event_id: str
    anomaly_type: AnomalyType
    severity: AnomalySeverity
    agent_id: str
    resource_path: Optional[str]
    operation: Optional[AccessOperation]
    data_level: Optional[DataLevel]
    description: str
    context: Dict[str, Any]
    detected_at: datetime
    related_events: List[str] = field(default_factory=list)
    status: str = "open"  # open, acknowledged, resolved, false_positive


@dataclass
class AnomalyThreshold:
    """异常检测阈值配置"""
    # 高频拒绝检测
    denial_window_seconds: int = 60          # 时间窗口（秒）
    denial_count_threshold: int = 5          # 拒绝次数阈值
    
    # 敏感数据检测
    sensitive_levels: Set[DataLevel] = field(default_factory=lambda: {
        DataLevel.L5_SECRET, DataLevel.L6_CRITICAL
    })
    
    # 批量操作检测
    bulk_count_threshold: int = 1000         # 批量数量阈值
    bulk_upgrade_threshold: int = 100        # 批量升级阈值
    
    # 时间检测
    work_hours_start: int = 9                # 工作开始时间（小时）
    work_hours_end: int = 18                 # 工作结束时间（小时）
    work_days: Set[int] = field(default_factory=lambda: {0, 1, 2, 3, 4})  # 周一到五
    
    # 冷却时间（避免重复告警）
    alert_cooldown_seconds: int = 300        # 5分钟冷却


class AnomalyDetector:
    """
    异常检测器
    
    实时分析访问模式，检测异常行为
    """
    
    def __init__(self, threshold: Optional[AnomalyThreshold] = None):
        self.threshold = threshold or AnomalyThreshold()
        
        # 事件历史（用于模式检测）
        self._event_history: List[Dict[str, Any]] = []
        self._history_lock = threading.RLock()
        self._max_history_size = 10000
        
        # 已检测异常（避免重复告警）
        self._detected_anomalies: Dict[str, datetime] = {}
        self._anomaly_lock = threading.RLock()
        
        # 上报回调
        self._reporters: List[Callable[[AnomalyEvent], None]] = []
        
        # Agent行为基线（学习正常行为）
        self._agent_baselines: Dict[str, Dict[str, Any]] = defaultdict(lambda: {
            "normal_hours": set(),
            "normal_resources": set(),
            "access_count": 0,
            "denial_count": 0
        })
    
    def add_reporter(self, reporter: Callable[[AnomalyEvent], None]):
        """添加上报回调"""
        self._reporters.append(reporter)
    
    def analyze_access(self,
                       agent_id: str,
                       resource_path: str,
                       operation: AccessOperation,
                       decision: AccessDecision,
                       data_level: DataLevel,
                       context: Dict[str, Any]) -> Optional[AnomalyEvent]:
        """
        分析单次访问，返回检测到的异常（如有）
        """
        # 记录事件
        event = {
            "timestamp": datetime.now(),
            "agent_id": agent_id,
            "resource_path": resource_path,
            "operation": operation.value,
            "decision": decision.value,
            "data_level": data_level.value if data_level else None,
            "context": context
        }
        self._record_event(event)
        
        # 更新Agent基线
        self._update_agent_baseline(agent_id, event)
        
        # 执行各项检测
        anomaly = None
        
        # 1. 高频拒绝检测
        if decision == AccessDecision.DENY:
            anomaly = self._check_high_frequency_denial(agent_id)
        
        # 2. 敏感数据尝试访问
        if not anomaly and data_level in self.threshold.sensitive_levels:
            anomaly = self._check_sensitive_access(agent_id, data_level, decision, context)
        
        # 3. 批量操作异常
        if not anomaly and context.get("is_bulk_operation"):
            anomaly = self._check_bulk_anomaly(agent_id, context, decision)
        
        # 4. 跨境传输异常
        if not anomaly and context.get("destination"):
            anomaly = self._check_cross_domain_anomaly(agent_id, data_level, context)
        
        # 5. 非工作时间访问
        if not anomaly:
            anomaly = self._check_off_hours_access(agent_id, context)
        
        # 6. 权限升级尝试
        if not anomaly and decision == AccessDecision.DENY:
            anomaly = self._check_privilege_escalation(agent_id, data_level, context)
        
        # 上报异常
        if anomaly and self._should_alert(anomaly):
            self._report_anomaly(anomaly)
            return anomaly
        
        return None
    
    def _record_event(self, event: Dict[str, Any]):
        """记录事件到历史"""
        with self._history_lock:
            self._event_history.append(event)
            # 限制历史大小
            if len(self._event_history) > self._max_history_size:
                self._event_history = self._event_history[-self._max_history_size:]
    
    def _update_agent_baseline(self, agent_id: str, event: Dict[str, Any]):
        """更新Agent行为基线"""
        baseline = self._agent_baselines[agent_id]
        baseline["access_count"] += 1
        
        if event["decision"] == "deny":
            baseline["denial_count"] += 1
        
        # 记录正常访问时间（小时）
        hour = event["timestamp"].hour
        if event["decision"] == "allow":
            baseline["normal_hours"].add(hour)
        
        # 记录正常访问资源
        if event["decision"] == "allow":
            baseline["normal_resources"].add(event["resource_path"])
    
    def _check_high_frequency_denial(self, agent_id: str) -> Optional[AnomalyEvent]:
        """检测高频拒绝"""
        cutoff = datetime.now() - timedelta(seconds=self.threshold.denial_window_seconds)
        
        with self._history_lock:
            recent_denials = [
                e for e in self._event_history
                if e["agent_id"] == agent_id
                and e["decision"] == "deny"
                and e["timestamp"] > cutoff
            ]
        
        if len(recent_denials) >= self.threshold.denial_count_threshold:
            return AnomalyEvent(
                event_id=self._generate_event_id(),
                anomaly_type=AnomalyType.HIGH_FREQUENCY_DENIAL,
                severity=AnomalySeverity.HIGH,
                agent_id=agent_id,
                resource_path=None,
                operation=None,
                data_level=None,
                description=f"Agent {agent_id} 在 {self.threshold.denial_window_seconds} 秒内被拒绝 {len(recent_denials)} 次",
                context={"denial_count": len(recent_denials), "window_seconds": self.threshold.denial_window_seconds},
                detected_at=datetime.now(),
                related_events=[e.get("event_id", "") for e in recent_denials[:5]]
            )
        return None
    
    def _check_sensitive_access(self, agent_id: str, data_level: DataLevel,
                                decision: AccessDecision, context: Dict[str, Any]) -> Optional[AnomalyEvent]:
        """检测敏感数据访问"""
        # L6 任何尝试都告警
        if data_level == DataLevel.L6_CRITICAL:
            severity = AnomalySeverity.CRITICAL if decision == AccessDecision.ALLOW else AnomalySeverity.HIGH
            return AnomalyEvent(
                event_id=self._generate_event_id(),
                anomaly_type=AnomalyType.SENSITIVE_ACCESS_ATTEMPT,
                severity=severity,
                agent_id=agent_id,
                resource_path=context.get("resource_path"),
                operation=context.get("operation"),
                data_level=data_level,
                description=f"Agent {agent_id} 尝试访问 L6 核心机密数据",
                context={"decision": decision.value, "resource": context.get("resource_path")},
                detected_at=datetime.now()
            )
        
        # L5 被拒绝也告警（可能是在探测）
        if data_level == DataLevel.L5_SECRET and decision == AccessDecision.DENY:
            return AnomalyEvent(
                event_id=self._generate_event_id(),
                anomaly_type=AnomalyType.SENSITIVE_ACCESS_ATTEMPT,
                severity=AnomalySeverity.MEDIUM,
                agent_id=agent_id,
                resource_path=context.get("resource_path"),
                operation=context.get("operation"),
                data_level=data_level,
                description=f"Agent {agent_id} 尝试访问 L5 秘密级数据被拒绝",
                context={"resource": context.get("resource_path")},
                detected_at=datetime.now()
            )
        
        return None
    
    def _check_bulk_anomaly(self, agent_id: str, context: Dict[str, Any],
                           decision: AccessDecision) -> Optional[AnomalyEvent]:
        """检测批量操作异常"""
        bulk_count = context.get("bulk_record_count", 0)
        
        # 超大批量
        if bulk_count >= self.threshold.bulk_count_threshold:
            return AnomalyEvent(
                event_id=self._generate_event_id(),
                anomaly_type=AnomalyType.BULK_OPERATION_ANOMALY,
                severity=AnomalySeverity.HIGH,
                agent_id=agent_id,
                resource_path=None,
                operation=context.get("operation"),
                data_level=context.get("data_level"),
                description=f"Agent {agent_id} 执行超大批量操作: {bulk_count} 条记录",
                context={"bulk_count": bulk_count, "decision": decision.value},
                detected_at=datetime.now()
            )
        
        # 批量升级异常
        upgraded_count = context.get("upgraded_count", 0)
        if upgraded_count >= self.threshold.bulk_upgrade_threshold:
            return AnomalyEvent(
                event_id=self._generate_event_id(),
                anomaly_type=AnomalyType.BULK_OPERATION_ANOMALY,
                severity=AnomalySeverity.MEDIUM,
                agent_id=agent_id,
                resource_path=None,
                operation=context.get("operation"),
                data_level=context.get("data_level"),
                description=f"Agent {agent_id} 批量操作中 {upgraded_count} 条记录触发级别升级",
                context={"upgraded_count": upgraded_count, "bulk_count": bulk_count},
                detected_at=datetime.now()
            )
        
        return None
    
    def _check_cross_domain_anomaly(self, agent_id: str, data_level: DataLevel,
                                   context: Dict[str, Any]) -> Optional[AnomalyEvent]:
        """检测跨境传输异常"""
        destination = context.get("destination", "")
        
        # 只有外部目的地才检测
        if not destination.startswith("external_"):
            return None
        
        # L3+ 数据跨境是高风险
        if data_level.value >= DataLevel.L3_RESTRICTED.value:
            return AnomalyEvent(
                event_id=self._generate_event_id(),
                anomaly_type=AnomalyType.CROSS_DOMAIN_SENSITIVE,
                severity=AnomalySeverity.HIGH,
                agent_id=agent_id,
                resource_path=context.get("resource_path"),
                operation=context.get("operation"),
                data_level=data_level,
                description=f"Agent {agent_id} 尝试将 {data_level.value} 数据传输到 {destination}",
                context={"destination": destination, "resource": context.get("resource_path")},
                detected_at=datetime.now()
            )
        
        return None
    
    def _check_off_hours_access(self, agent_id: str, context: Dict[str, Any]) -> Optional[AnomalyEvent]:
        """检测非工作时间访问"""
        now = datetime.now()
        hour = now.hour
        weekday = now.weekday()
        
        # 检查是否在工作时间外
        is_work_hours = (
            self.threshold.work_hours_start <= hour < self.threshold.work_hours_end
            and weekday in self.threshold.work_days
        )
        
        if is_work_hours:
            return None
        
        # 检查Agent是否有非工作时间访问的历史
        baseline = self._agent_baselines[agent_id]
        if hour in baseline["normal_hours"]:
            return None  # 该Agent之前在这个时间访问过，不算异常
        
        return AnomalyEvent(
            event_id=self._generate_event_id(),
            anomaly_type=AnomalyType.OFF_HOURS_ACCESS,
            severity=AnomalySeverity.LOW,
            agent_id=agent_id,
            resource_path=context.get("resource_path"),
            operation=context.get("operation"),
            data_level=context.get("data_level"),
            description=f"Agent {agent_id} 在非工作时间 ({now.strftime('%H:%M')}) 发起访问",
            context={"hour": hour, "weekday": weekday},
            detected_at=datetime.now()
        )
    
    def _check_privilege_escalation(self, agent_id: str, data_level: DataLevel,
                                   context: Dict[str, Any]) -> Optional[AnomalyEvent]:
        """检测权限升级尝试"""
        # 获取Agent的正常访问级别
        baseline = self._agent_baselines[agent_id]
        
        # 如果Agent之前没有成功访问过，不做判断
        if baseline["access_count"] < 5:
            return None
        
        # 计算Agent的正常访问级别（历史上成功访问的最高级别）
        # 简化：如果拒绝率高，可能是权限升级尝试
        denial_rate = baseline["denial_count"] / baseline["access_count"]
        
        if denial_rate > 0.5 and baseline["access_count"] > 10:
            return AnomalyEvent(
                event_id=self._generate_event_id(),
                anomaly_type=AnomalyType.PRIVILEGE_ESCALATION,
                severity=AnomalySeverity.MEDIUM,
                agent_id=agent_id,
                resource_path=context.get("resource_path"),
                operation=context.get("operation"),
                data_level=data_level,
                description=f"Agent {agent_id} 拒绝率高达 {denial_rate:.1%}，可能存在权限探测行为",
                context={"denial_rate": denial_rate, "total_access": baseline["access_count"]},
                detected_at=datetime.now()
            )
        
        return None
    
    def _should_alert(self, anomaly: AnomalyEvent) -> bool:
        """检查是否应该告警（避免重复）"""
        with self._anomaly_lock:
            key = f"{anomaly.agent_id}:{anomaly.anomaly_type.value}"
            last_alert = self._detected_anomalies.get(key)
            
            if last_alert:
                cooldown = timedelta(seconds=self.threshold.alert_cooldown_seconds)
                if datetime.now() - last_alert < cooldown:
                    return False  # 冷却期内，不重复告警
            
            # 更新最后告警时间
            self._detected_anomalies[key] = datetime.now()
            return True
    
    def _report_anomaly(self, anomaly: AnomalyEvent):
        """上报异常"""
        # 本地日志
        logger.warning(f"[ANOMALY] {anomaly.severity.value}: {anomaly.description}")
        
        # 调用所有上报器
        for reporter in self._reporters:
            try:
                reporter(anomaly)
            except Exception as e:
                logger.error(f"上报器失败: {e}")
    
    def _generate_event_id(self) -> str:
        """生成事件ID"""
        import secrets
        return f"ANM-{secrets.token_hex(8)}"
    
    def get_stats(self) -> Dict[str, Any]:
        """获取检测统计"""
        with self._history_lock:
            total_events = len(self._event_history)
        
        with self._anomaly_lock:
            total_anomalies = len(self._detected_anomalies)
        
        return {
            "total_events_analyzed": total_events,
            "total_anomalies_detected": total_anomalies,
            "agent_baselines": len(self._agent_baselines),
            "threshold": {
                "denial_window": self.threshold.denial_window_seconds,
                "denial_count": self.threshold.denial_count_threshold,
                "bulk_threshold": self.threshold.bulk_count_threshold
            }
        }


class AnomalyReporter:
    """
    异常上报器基类
    """
    
    def report(self, anomaly: AnomalyEvent):
        """上报异常（子类实现）"""
        raise NotImplementedError


class LoggingReporter(AnomalyReporter):
    """日志上报器"""
    
    def report(self, anomaly: AnomalyEvent):
        """记录到日志"""
        logger.warning(
            f"[ANOMALY-{anomaly.severity.value.upper()}] "
            f"Type: {anomaly.anomaly_type.value}, "
            f"Agent: {anomaly.agent_id}, "
            f"Desc: {anomaly.description}"
        )


class NotificationReporter(AnomalyReporter):
    """系统通知上报器"""
    
    def __init__(self, notify_func: Optional[Callable[[str, str], None]] = None):
        self._notify = notify_func or self._default_notify
    
    def _default_notify(self, title: str, message: str):
        """默认通知实现（macOS）"""
        import subprocess
        try:
            subprocess.run([
                "osascript", "-e",
                f'display notification "{message}" with title "{title}"'
            ], check=False)
        except:
            pass
    
    def report(self, anomaly: AnomalyEvent):
        """发送系统通知"""
        title = f"🚨 安全异常 - {anomaly.severity.value.upper()}"
        message = f"{anomaly.anomaly_type.value}: {anomaly.agent_id}"
        self._notify(title, message)


class ConsoleReporter(AnomalyReporter):
    """控制台上报器"""
    
    def report(self, anomaly: AnomalyEvent):
        """打印到控制台"""
        severity_colors = {
            AnomalySeverity.LOW: "\033[90m",      # 灰色
            AnomalySeverity.MEDIUM: "\033[93m",   # 黄色
            AnomalySeverity.HIGH: "\033[91m",     # 红色
            AnomalySeverity.CRITICAL: "\033[95m"  # 紫色
        }
        reset = "\033[0m"
        color = severity_colors.get(anomaly.severity, "")
        
        print(f"\n{color}🚨 ANOMALY DETECTED [{anomaly.severity.value.upper()}]{reset}")
        print(f"   Type: {anomaly.anomaly_type.value}")
        print(f"   Agent: {anomaly.agent_id}")
        print(f"   Time: {anomaly.detected_at.strftime('%H:%M:%S')}")
        print(f"   Desc: {anomaly.description}")
        print()


# 便捷函数
def create_default_detector() -> AnomalyDetector:
    """创建默认配置的检测器"""
    detector = AnomalyDetector()
    
    # 添加控制台上报器
    detector.add_reporter(ConsoleReporter().report)
    
    # 添加日志上报器
    detector.add_reporter(LoggingReporter().report)
    
    return detector
