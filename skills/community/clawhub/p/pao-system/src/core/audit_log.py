"""
PAO System - Immutable Audit Log Module

不可变审计日志模块，用于记录任务分发过程的完整追溯信息。
采用追加写入 + 哈希链校验机制确保日志不可篡改。
"""

import json
import hashlib
import uuid
from datetime import datetime
from dataclasses import dataclass, field, asdict
from typing import List, Optional, Dict, Any
from pathlib import Path


@dataclass
class AuditLogEntry:
    """审计日志条目"""
    timestamp: str                    # ISO 格式时间戳
    log_id: str                       # 唯一日志ID (uuid)
    prev_hash: str                     # 前一条日志的哈希（用于形成哈希链）
    actor: str                        # 操作者 (system/worker_id/user)
    action: str                       # 操作类型 (dispatch/send/result/error)
    target: str                       # 目标资源 (task_id/worker_id)
    result: str                       # 操作结果 (success/failure/pending)
    details: Dict[str, Any] = field(default_factory=dict)  # 额外详情
    entry_hash: str = ""              # 本条日志的哈希

    def __post_init__(self):
        if not self.entry_hash:
            self.entry_hash = self._compute_hash()

    def _compute_hash(self) -> str:
        """计算本条日志的哈希值（不含 entry_hash 自身）"""
        content = f"{self.timestamp}{self.log_id}{self.prev_hash}{self.actor}{self.action}{self.target}{self.result}{json.dumps(self.details, sort_keys=True)}"
        return hashlib.sha256(content.encode()).hexdigest()[:16]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "timestamp": self.timestamp,
            "log_id": self.log_id,
            "prev_hash": self.prev_hash,
            "actor": self.actor,
            "action": self.action,
            "target": self.target,
            "result": self.result,
            "details": self.details,
            "entry_hash": self.entry_hash
        }


class ImmutableAuditLog:
    """
    不可变审计日志存储器

    采用哈希链机制确保日志不可篡改：
    - 每条日志包含前一条日志的哈希值
    - 任何历史日志被修改都会导致哈希链断裂
    """

    def __init__(self, log_dir: str = ".pao/audit_logs"):
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.log_file = self.log_dir / "audit_log.jsonl"
        self._last_hash = self._load_last_hash()

    def _load_last_hash(self) -> str:
        """加载最后一条日志的哈希值"""
        if not self.log_file.exists():
            return "0" * 16  # 创世哈希

        try:
            with open(self.log_file, "r", encoding="utf-8") as f:
                lines = f.readlines()
                if lines:
                    last_entry = json.loads(lines[-1].strip())
                    return last_entry.get("entry_hash", "0" * 16)
        except (json.JSONDecodeError, FileNotFoundError):
            pass

        return "0" * 16

    def append(self, actor: str, action: str, target: str, result: str, details: Dict[str, Any] = None) -> AuditLogEntry:
        """
        追加一条审计日志

        Args:
            actor: 操作者
            action: 操作类型 (dispatch/send/result/error)
            target: 目标资源
            result: 操作结果
            details: 额外详情

        Returns:
            AuditLogEntry: 创建的日志条目
        """
        entry = AuditLogEntry(
            timestamp=datetime.now().isoformat(timespec='milliseconds'),
            log_id=f"log_{uuid.uuid4().hex[:12]}",
            prev_hash=self._last_hash,
            actor=actor,
            action=action,
            target=target,
            result=result,
            details=details or {}
        )

        # 追加写入文件
        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry.to_dict(), ensure_ascii=False) + "\n")

        # 更新最后哈希
        self._last_hash = entry.entry_hash

        return entry

    def verify_integrity(self) -> tuple[bool, List[str]]:
        """
        验证日志完整性

        Returns:
            (is_valid, error_messages): 是否完整及错误信息列表
        """
        if not self.log_file.exists():
            return True, []

        errors = []
        expected_prev_hash = "0" * 16

        try:
            with open(self.log_file, "r", encoding="utf-8") as f:
                for line_num, line in enumerate(f, 1):
                    try:
                        entry = json.loads(line.strip())

                        # 验证哈希链
                        if entry["prev_hash"] != expected_prev_hash:
                            errors.append(f"行 {line_num}: 哈希链断裂，期望 {expected_prev_hash}, 实际 {entry['prev_hash']}")

                        # 验证本条哈希
                        entry_obj = AuditLogEntry(**{k: v for k, v in entry.items() if k != "entry_hash"})
                        if entry_obj.entry_hash != entry["entry_hash"]:
                            errors.append(f"行 {line_num}: 日志内容被篡改")

                        expected_prev_hash = entry["entry_hash"]
                    except json.JSONDecodeError as e:
                        errors.append(f"行 {line_num}: JSON 解析失败 - {e}")
        except FileNotFoundError:
            pass

        return len(errors) == 0, errors

    def query(self, action: str = None, actor: str = None, target: str = None,
              start_time: str = None, end_time: str = None, limit: int = 100) -> List[AuditLogEntry]:
        """
        查询审计日志

        Args:
            action: 按操作类型过滤
            actor: 按操作者过滤
            target: 按目标过滤
            start_time: 开始时间 (ISO格式)
            end_time: 结束时间 (ISO格式)
            limit: 返回条数限制

        Returns:
            List[AuditLogEntry]: 匹配的日志条目列表
        """
        if not self.log_file.exists():
            return []

        results = []

        try:
            with open(self.log_file, "r", encoding="utf-8") as f:
                for line in f:
                    try:
                        entry = json.loads(line.strip())

                        # 应用过滤器
                        if action and entry["action"] != action:
                            continue
                        if actor and entry["actor"] != actor:
                            continue
                        if target and entry["target"] != target:
                            continue
                        if start_time and entry["timestamp"] < start_time:
                            continue
                        if end_time and entry["timestamp"] > end_time:
                            continue

                        results.append(AuditLogEntry(**{k: v for k, v in entry.items() if k != "entry_hash"}))
                    except json.JSONDecodeError:
                        continue
        except FileNotFoundError:
            pass

        # 返回最新的一条
        return results[-limit:] if len(results) > limit else results

    def get_task_history(self, task_id: str) -> List[AuditLogEntry]:
        """获取某个任务的完整历史"""
        return self.query(target=task_id, limit=1000)

    def get_worker_history(self, worker_id: str) -> List[AuditLogEntry]:
        """获取某个工作区的操作历史"""
        return self.query(actor=worker_id, limit=1000)

    def export_json(self) -> List[Dict[str, Any]]:
        """导出所有日志为 JSON 列表"""
        if not self.log_file.exists():
            return []

        results = []
        with open(self.log_file, "r", encoding="utf-8") as f:
            for line in f:
                try:
                    results.append(json.loads(line.strip()))
                except json.JSONDecodeError:
                    continue
        return results
