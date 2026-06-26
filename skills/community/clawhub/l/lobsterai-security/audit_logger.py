"""
审计日志系统
记录所有安全事件、操作日志、授权决策

设计原则：
- 不可篡改（后续可集成数字签名）
- 日志轮转（保留 90 天）
- 敏感信息自动脱敏
- 支持本地存储 + 远程 SIEM 转发
"""

import json
import os
import time
import hmac
import hashlib
import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Any, Optional, List
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from output_sanitizer import OutputSanitizer


class AuditLogger:
    """审计日志记录器"""

    def __init__(self, log_dir: Optional[str] = None):
        self.lobsterai_home = os.getenv('LOBSTERAI_HOME', os.path.expanduser('~/.lobsterai'))
        self.log_dir = log_dir or os.path.join(self.lobsterai_home, 'logs', 'security')
        self.max_age_days = 90

        # 确保日志目录存在
        Path(self.log_dir).mkdir(parents=True, exist_ok=True)

        # 当前日志文件路径（按日期分割）
        self.current_log_file = self._get_log_file_path()

        # 日志格式：JSON Lines（每行一个 JSON 对象）
        # 字段：
        # - timestamp: ISO 8601 时间戳
        # - event_type: 事件类型（authorization, execution, error, scan 等）
        # - user_id: 用户标识
        # - skill_id: 技能ID
        # - details: 事件详情
        # - level: 日志级别（info, warning, error, critical）
        # - signature: 日志签名（防篡改）

        # 初始化文件轮转
        self._rotate_logs()

    def _get_log_file_path(self, date: Optional[datetime] = None) -> str:
        """获取日志文件路径（按日期）"""
        if date is None:
            date = datetime.now()
        filename = f"audit-{date.strftime('%Y-%m-%d')}.jsonl"
        return os.path.join(self.log_dir, filename)

    def _rotate_logs(self):
        """日志轮转：删除超过保留期的日志"""
        cutoff_date = datetime.now() - timedelta(days=self.max_age_days)

        for filename in os.listdir(self.log_dir):
            if filename.startswith('audit-') and filename.endswith('.jsonl'):
                try:
                    # 从文件名提取日期
                    date_str = filename.replace('audit-', '').replace('.jsonl', '')
                    file_date = datetime.strptime(date_str, '%Y-%m-%d')

                    if file_date < cutoff_date:
                        file_path = os.path.join(self.log_dir, filename)
                        os.remove(file_path)
                        print(f"[AuditLogger] Deleted old log file: {filename}")
                except Exception as e:
                    print(f"[AuditLogger] Error rotating log {filename}: {e}")

    def log_event(self,
                   event_type: str,
                   details: Dict[str, Any],
                   user_id: Optional[str] = None,
                   skill_id: Optional[str] = None,
                   level: str = 'info',
                   sensitive_data: Optional[str] = None):
        """
        记录审计事件

        Args:
            event_type: 事件类型（authorization, execution, error, scan, config_change 等）
            details: 事件详情字典
            user_id: 用户标识（从会话获取）
            skill_id: 技能ID（如果适用）
            level: 日志级别（info, warning, error, critical）
            sensitive_data: 可能包含敏感信息的原始输出（用于脱敏）
        """
        # 检查是否需要轮转（每天一次）
        log_date = datetime.now().date()
        current_log_date = Path(self.current_log_file).stem.replace('audit-', '')
        if current_log_date != log_date.strftime('%Y-%m-%d'):
            self.current_log_file = self._get_log_file_path(log_date)
            self._rotate_logs()

        # 构建日志条目
        log_entry = {
            'timestamp': self.format_timestamp(),
            'event_type': event_type,
            'user_id': user_id or 'anonymous',
            'skill_id': skill_id or 'unknown',
            'details': self._sanitize_details(details),
            'level': level
        }

        # 如果有敏感数据，记录脱敏前后的对比（仅用于调试）
        if sensitive_data:
            log_entry['sensitive_data_preview'] = {
                'original_length': len(sensitive_data),
                'sanitized': OutputSanitizer.sanitize(sensitive_data[:200]) + '...' if len(sensitive_data) > 200 else OutputSanitizer.sanitize(sensitive_data)
            }

        # 计算签名（使用时间戳 + 密钥，如果可用）
        signature = self._calculate_signature(log_entry)
        log_entry['signature'] = signature

        # 写入文件（JSON Lines 格式）
        try:
            with open(self.current_log_file, 'a', encoding='utf-8') as f:
                f.write(json.dumps(log_entry, ensure_ascii=False) + '\n')
        except Exception as e:
            print(f"[AuditLogger] Failed to write log: {e}")

    def _sanitize_details(self, details: Dict[str, Any]) -> Dict[str, Any]:
        """递归清理详情中的敏感信息"""
        sanitized = {}
        for key, value in details.items():
            if isinstance(value, str):
                sanitized[key] = OutputSanitizer.sanitize(value)
            elif isinstance(value, dict):
                sanitized[key] = self._sanitize_details(value)
            elif isinstance(value, list):
                sanitized[key] = [
                    self._sanitize_details(item) if isinstance(item, dict) else
                    OutputSanitizer.sanitize(item) if isinstance(item, str) else
                    item
                    for item in value
                ]
            else:
                sanitized[key] = value
        return sanitized

    def _calculate_signature(self, log_entry: Dict[str, Any]) -> str:
        """计算日志签名（HMAC-SHA256）"""
        secret = os.getenv('LOBSTERAI_AUDIT_SECRET')
        if not secret:
            return 'no-secret-configured'

        # 使用时间戳 + 事件类型 + 详情 作为签名数据
        data = f"{log_entry['timestamp']}{log_entry['event_type']}{json.dumps(log_entry['details'], sort_keys=True)}"
        signature = hmac.new(
            secret.encode('utf-8'),
            data.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        return signature

    def format_timestamp(self) -> str:
        """生成 ISO 8601 时间戳"""
        return datetime.now().isoformat(timespec='milliseconds')

    def get_recent_logs(self, hours: int = 24, event_type: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        获取最近的审计日志（用于监控/调查）

        Args:
            hours: 查询最近多少小时
            event_type: 过滤事件类型

        Returns:
            List[Dict]: 日志条目列表
        """
        logs = []
        cutoff_time = datetime.now() - timedelta(hours=hours)

        # 扫描日志文件
        for filename in sorted(os.listdir(self.log_dir)):
            if not filename.startswith('audit-') or not filename.endswith('.jsonl'):
                continue

            file_path = os.path.join(self.log_dir, filename)
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    for line in f:
                        try:
                            entry = json.loads(line.strip())
                            entry_time = datetime.fromisoformat(entry['timestamp'].replace('Z', '+00:00'))

                            if entry_time >= cutoff_time:
                                if event_type is None or entry['event_type'] == event_type:
                                    logs.append(entry)
                        except json.JSONDecodeError:
                            continue
            except Exception as e:
                print(f"[AuditLogger] Error reading log {filename}: {e}")

        return logs

    def search_logs(self,
                    user_id: Optional[str] = None,
                    skill_id: Optional[str] = None,
                    level: Optional[str] = None,
                    start_time: Optional[datetime] = None,
                    end_time: Optional[datetime] = None) -> List[Dict[str, Any]]:
        """
        搜索审计日志

        Returns:
            List[Dict]: 匹配的日志条目
        """
        logs = self.get_recent_logs(hours=24*7)  # 查询最近7天

        results = []
        for entry in logs:
            if user_id and entry.get('user_id') != user_id:
                continue
            if skill_id and entry.get('skill_id') != skill_id:
                continue
            if level and entry.get('level') != level:
                continue
            if start_time:
                entry_time = datetime.fromisoformat(entry['timestamp'].replace('Z', '+00:00'))
                if entry_time < start_time:
                    continue
            if end_time:
                entry_time = datetime.fromisoformat(entry['timestamp'].replace('Z', '+00:00'))
                if entry_time > end_time:
                    continue

            results.append(entry)

        return results

    def get_statistics(self, hours: int = 24) -> Dict[str, Any]:
        """获取审计统计信息"""
        logs = self.get_recent_logs(hours)

        stats = {
            'total_events': len(logs),
            'by_event_type': {},
            'by_level': {},
            'by_user': {},
            'by_skill': {},
            'security_incidents': 0
        }

        for entry in logs:
            # 按事件类型统计
            event_type = entry['event_type']
            stats['by_event_type'][event_type] = stats['by_event_type'].get(event_type, 0) + 1

            # 按级别统计
            level = entry['level']
            stats['by_level'][level] = stats['by_level'].get(level, 0) + 1

            # 按用户统计
            user_id = entry['user_id']
            stats['by_user'][user_id] = stats['by_user'].get(user_id, 0) + 1

            # 按技能统计
            skill_id = entry['skill_id']
            stats['by_skill'][skill_id] = stats['by_skill'].get(skill_id, 0) + 1

            # 安全事件计数（error 或 critical 级别）
            if level in ['error', 'critical']:
                stats['security_incidents'] += 1

        return stats


# 全局审计日志器实例
_global_audit_logger: Optional[AuditLogger] = None


def get_audit_logger() -> AuditLogger:
    """获取全局审计日志器实例"""
    global _global_audit_logger
    if _global_audit_logger is None:
        _global_audit_logger = AuditLogger()
    return _global_audit_logger


# 默认实例
audit_logger = get_audit_logger()


# CLI 入口：支持命令行调用审计日志器
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Audit Logger CLI")
    parser.add_argument("--event", required=True, choices=["start", "end", "error"], help="Event type: start, end, error")
    parser.add_argument("--skill", required=True, help="Skill ID")
    parser.add_argument("--data", default="{}", help="JSON string with event data")
    parser.add_argument("--duration", type=int, help="Duration in milliseconds (for end event)")
    parser.add_argument("--error", help="Error message (for error event)")
    parser.add_argument("--user-id", dest="user_id", help="User ID (overrides LOBSTERAI_USER_ID env)")
    args = parser.parse_args()

    # 解析 data JSON
    try:
        data = json.loads(args.data) if args.data else {}
    except json.JSONDecodeError:
        print("Error: --data must be valid JSON", file=sys.stderr)
        sys.exit(1)

    # 获取审计日志器
    logger = get_audit_logger()
    user_id = args.user_id or os.getenv('LOBSTERAI_USER_ID', 'anonymous')

    if args.event == "start":
        logger.log_event("skill_execution_start", data, user_id=user_id, skill_id=args.skill)
    elif args.event == "end":
        details = {"result": data}
        if args.duration is not None:
            details["duration_ms"] = args.duration
        logger.log_event("skill_execution_end", details, user_id=user_id, skill_id=args.skill)
    elif args.event == "error":
        details = {"input": data}
        if args.error:
            details["error"] = args.error
        logger.log_event("skill_execution_error", details, user_id=user_id, skill_id=args.skill, level="error")
