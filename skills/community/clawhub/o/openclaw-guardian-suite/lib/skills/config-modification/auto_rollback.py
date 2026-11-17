#!/usr/bin/env python3
# [OC-WM] licensed-to: macmini@MacminideMac-mini | bundle: vendor-suite | ts: 2026-03-09T17:30:16Z
"""
auto_rollback.py — 失败自动回滚 + 告警系统
=========================================

功能:
- 检测校验失败 → 自动回滚 → 发送告警
- 支持多种告警渠道
- 可配置告警规则

使用:
  from auto_rollback import AutoRollback, ALERT_RULES, check_and_rollback
"""

import subprocess
import json
import os
from datetime import datetime
from pathlib import Path
from typing import Optional
from dataclasses import dataclass, asdict

CONFIG_DIR = Path.home() / ".openclaw"
WORKSPACE_DIR = CONFIG_DIR / "workspace"
LOG_DIR = CONFIG_DIR / "logs"

# 告警规则定义
ALERT_RULES = {
    "schema_fail": {
        "severity": "critical",
        "action": "rollback",
        "notify": ["telegram", "log"],
        "message": "配置 Schema 校验失败，已自动回滚"
    },
    "diff_critical": {
        "severity": "high",
        "action": "rollback",
        "notify": ["telegram", "log"],
        "message": "检测到关键配置变更，已自动回滚"
    },
    "rollback_fail": {
        "severity": "critical",
        "action": "alert_only",
        "notify": ["telegram", "log", "signal"],
        "message": "回滚失败！需要人工介入！"
    },
    "health_fail": {
        "severity": "medium",
        "action": "retry_then_rollback",
        "notify": ["log"],
        "message": "Gateway 健康检查失败，尝试重试后回滚"
    },
    "partial_fail": {
        "severity": "low",
        "action": "notify_only",
        "notify": ["log"],
        "message": "部分校验未通过，请检查配置"
    }
}

# 严重等级
SEVERITY_LEVELS = {
    "critical": 4,
    "high": 3,
    "medium": 2,
    "low": 1
}


@dataclass
class AlertEvent:
    """告警事件"""
    rule: str
    severity: str
    message: str
    timestamp: str
    details: dict
    
    def to_dict(self):
        return asdict(self)


class AlertManager:
    """告警管理器"""
    
    def __init__(self):
        self.pending_alerts: list[AlertEvent] = []
    
    def send_alert(self, rule_key: str, message: str, details: dict = None):
        """发送告警"""
        rule = ALERT_RULES.get(rule_key, {})
        severity = rule.get("severity", "low")
        
        event = AlertEvent(
            rule=rule_key,
            severity=severity,
            message=message,
            timestamp=datetime.now().isoformat(),
            details=details or {}
        )
        
        self.pending_alerts.append(event)
        
        # 按渠道发送
        notify_channels = rule.get("notify", ["log"])
        
        for channel in notify_channels:
            if channel == "telegram":
                self._send_telegram(event)
            elif channel == "log":
                self._send_log(event)
            elif channel == "signal":
                self._send_signal(event)
    
    def _send_telegram(self, event: AlertEvent):
        """发送 Telegram 告警"""
        # 写入待发送队列，由主进程处理
        queue_file = LOG_DIR / "alert_queue.json"
        
        alerts = []
        if queue_file.exists():
            with open(queue_file) as f:
                alerts = json.load(f)
        
        alerts.append({
            "channel": "telegram",
            "event": event.to_dict()
        })
        
        with open(queue_file, "w") as f:
            json.dump(alerts, f, indent=2)
        
        # 同时打印日志
        self._log_alert(event, "telegram")
    
    def _send_log(self, event: AlertEvent):
        """写入日志"""
        self._log_alert(event, "log")
    
    def _send_signal(self, event: AlertEvent):
        """发送 Signal 告警（如果配置）"""
        self._log_alert(event, "signal")
    
    def _log_alert(self, event: AlertEvent, channel: str):
        """记录告警到日志"""
        LOG_DIR.mkdir(parents=True, exist_ok=True)
        log_file = LOG_DIR / "alerts.log"
        
        emoji = {
            "critical": "🚨",
            "high": "⚠️",
            "medium": "⚡",
            "low": "ℹ️"
        }.get(event.severity, "📝")
        
        entry = (
            f"[{event.timestamp}] [{emoji}] [{event.severity.upper()}] "
            f"[{channel}] {event.message}"
        )
        
        print(entry)
        
        with open(log_file, "a") as f:
            f.write(entry + "\n")


class AutoRollback:
    """
    自动回滚控制器
    
    检测失败 → 自动回滚 → 发送告警
    """
    
    def __init__(self):
        self.alert_manager = AlertManager()
        self.rollback_script = WORKSPACE_DIR / ".lib" / "config-rollback-guard.py"
    
    def check_and_rollback(self, check_results: list, config_path: str) -> bool:
        """
        检查校验结果，必要时触发回滚
        
        Args:
            check_results: 四联校验的结果列表
            config_path: 配置文件路径
        
        Returns:
            True if all passed (no rollback needed)
            False if rollback was triggered
        """
        # 1. 确定失败类型
        failed_phases = [r for r in check_results if not r.passed]
        
        if not failed_phases:
            return True  # 全部通过
        
        # 2. 记录失败
        print(f"\n⚠️ 检测到 {len(failed_phases)} 个校验失败:")
        for phase in failed_phases:
            print(f"  - {phase.phase}: {phase.message}")
        
        # 3. 确定告警规则
        alert_rule = self._determine_alert_rule(failed_phases)
        
        # 4. 执行回滚
        if alert_rule["action"] in ["rollback", "retry_then_rollback"]:
            success = self._execute_rollback(config_path)
            
            if not success:
                # 回滚失败，使用更严重的告警
                self.alert_manager.send_alert(
                    "rollback_fail",
                    ALERT_RULES["rollback_fail"]["message"],
                    {"config": config_path, "failed_phases": [p.phase for p in failed_phases]}
                )
                return False
            
            # 回滚成功，发送告警
            self.alert_manager.send_alert(
                alert_rule["rule"],
                alert_rule["message"],
                {
                    "config": config_path,
                    "failed_phases": [p.phase for p in failed_phases],
                    "rollback": "success"
                }
            )
        else:
            # 只通知不回滚
            self.alert_manager.send_alert(
                alert_rule["rule"],
                alert_rule["message"],
                {"config": config_path, "failed_phases": [p.phase for p in failed_phases]}
            )
        
        return False
    
    def _determine_alert_rule(self, failed_phases: list) -> dict:
        """根据失败阶段确定告警规则"""
        phase_names = [p.phase for p in failed_phases]
        
        # 优先级判断
        if "schema" in phase_names:
            return {"rule": "schema_fail", **ALERT_RULES["schema_fail"]}
        elif "diff" in phase_names:
            return {"rule": "diff_critical", **ALERT_RULES["diff_critical"]}
        elif "health" in phase_names:
            return {"rule": "health_fail", **ALERT_RULES["health_fail"]}
        elif "rollback" in phase_names:
            return {"rule": "rollback_fail", **ALERT_RULES["rollback_fail"]}
        else:
            return {"rule": "partial_fail", **ALERT_RULES["partial_fail"]}
    
    def _execute_rollback(self, config_path: str) -> bool:
        """执行回滚"""
        print(f"\n🔄 正在执行自动回滚: {config_path}")
        
        try:
            result = subprocess.run(
                ["python3", str(self.rollback_script), "rollback"],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                print("✅ 回滚执行成功")
                return True
            else:
                print(f"❌ 回滚执行失败: {result.stderr}")
                return False
                
        except subprocess.TimeoutExpired:
            print("❌ 回滚执行超时")
            return False
        except Exception as e:
            print(f"❌ 回滚执行异常: {e}")
            return False
    
    def manual_rollback(self, config_path: str) -> bool:
        """手动触发回滚"""
        return self._execute_rollback(config_path)


# 便捷函数
def check_and_rollback(check_results: list, config_path: str) -> bool:
    """便捷函数：检查并回滚"""
    controller = AutoRollback()
    return controller.check_and_rollback(check_results, config_path)


# CLI 接口
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage:")
        print("  auto_rollback.py rollback           # 手动执行回滚")
        print("  auto_rollback.py test-alert          # 测试告警")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "rollback":
        controller = AutoRollback()
        config_path = sys.argv[2] if len(sys.argv) > 2 else str(CONFIG_DIR / "openclaw.json")
        success = controller.manual_rollback(config_path)
        sys.exit(0 if success else 1)
    
    elif command == "test-alert":
        manager = AlertManager()
        manager.send_alert(
            "test",
            "这是一条测试告警",
            {"test": True}
        )
        print("✅ 测试告警已发送")
        sys.exit(0)
    
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)
