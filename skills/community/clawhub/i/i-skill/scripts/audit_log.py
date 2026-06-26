"""
Audit Log - 操作审计与防御日志模块（i-skill）

修复记录（v2.1.0）：
- [P0] 补全缺失的 _load_security_log() 方法（实为 _load_defensive_log 的别名）
- [P0] 修正 log() 中 level 类型判断：str 与 AuditLevel Enum 混用导致 ERROR/CRITICAL
       永远无法路由到防御日志的 bug
- [P0] 修正 _update_metrics() 接收 action 参数类型：统一使用字符串比较
- [P1] export_log() 增加路径安全校验，防止路径穿越
- [P2] 所有文件 IO 操作增加 try-except，文件损坏时返回空数据而非崩溃
- [P2] get_all_skills_summary() 优化为单次扫描，降低复杂度
- [P3] 统一使用字符串常量，消除 Enum 与字符串的混用

修复记录（v2.2.0）：
- [P1] 默认 user_data_path 改为技能目录下的 user_data/，而非运行时 cwd
- [P1] 支持 ISKILL_DATA_PATH 环境变量覆盖
"""

import json
import os
from typing import Dict, List, Optional, Tuple
from pathlib import Path
from datetime import datetime
from enum import Enum


def _get_skill_directory() -> Path:
    """获取技能所在目录（相对于运行时的 cwd，确保数据存储在技能工具区）"""
    # 优先使用环境变量指定的路径
    env_path = os.environ.get('ISKILL_DATA_PATH')
    if env_path:
        return Path(env_path).resolve()
    # 默认使用技能所在目录 + user_data/
    return Path(__file__).parent.parent / "user_data"


class AuditAction(Enum):
    READ = "READ"
    WRITE = "WRITE"
    DELETE = "DELETE"
    CONSENT_GRANTED = "CONSENT_GRANTED"
    CONSENT_DENIED = "CONSENT_DENIED"
    CONSENT_REVOKED = "CONSENT_REVOKED"
    CONSENT_RESTORED = "CONSENT_RESTORED"
    ACCESS_DENIED = "ACCESS_DENIED"
    VALIDATION_FAILED = "VALIDATION_FAILED"
    SANITIZATION_APPLIED = "SANITIZATION_APPLIED"
    PROFILE_UPDATED = "PROFILE_UPDATED"
    PROFILE_RESET = "PROFILE_RESET"
    SKILL_ACTIVATED = "SKILL_ACTIVATED"
    SKILL_DEACTIVATED = "SKILL_DEACTIVATED"


class AuditLevel(Enum):
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


# 高级别集合（字符串），用于字符串比较
_HIGH_LEVELS = {AuditLevel.ERROR.value, AuditLevel.CRITICAL.value}


class AuditLog:
    def __init__(self, user_data_path: str = None, config_path: str = None):
        # 默认使用技能目录下的 user_data/
        if user_data_path is None:
            user_data_path = str(_get_skill_directory())
        self.user_data_path = Path(user_data_path).resolve()

        self.config = self._load_config(config_path)
        self.audit_log_file = self.user_data_path / "audit_log.json"
        self.defensive_log_file = self.user_data_path / "defensive_log.json"
        self.metrics_file = self.user_data_path / "audit_metrics.json"

        self._initialized = False

    # ------------------------------------------------------------------
    # 配置加载
    # ------------------------------------------------------------------

    def _load_config(self, config_path: str) -> Dict:
        if config_path:
            try:
                p = Path(config_path)
                if p.exists() and p.stat().st_size <= 1024 * 1024:
                    with open(p, 'r', encoding='utf-8') as f:
                        return json.load(f)
            except Exception:
                pass  # 配置读取失败则使用默认值

        return {
            "audit": {
                "log_all_access": True,
                "log_all_writes": True,
                "log_all_consents": True,
                "log_validation_failures": True,
                "log_sanitization": True,
                "max_log_size": 10000,
                "log_rotation": True,
                "export_format": "json"
            }
        }

    # ------------------------------------------------------------------
    # 初始化（延迟执行）
    # ------------------------------------------------------------------

    def _ensure_initialized(self):
        """确保目录和文件已初始化，在第一次写入数据时调用"""
        if self._initialized:
            return
        
        self.user_data_path.mkdir(parents=True, exist_ok=True)
        self._initialize_audit_log()
        self._initialize_defensive_log()
        self._initialize_metrics()
        self._initialized = True

    def _initialize_audit_log(self):
        if not self.audit_log_file.exists():
            self._safe_write_json(self.audit_log_file, [])

    def _initialize_defensive_log(self):
        if not self.defensive_log_file.exists():
            self._safe_write_json(self.defensive_log_file, [])

    def _initialize_metrics(self):
        if not self.metrics_file.exists():
            self._safe_write_json(self.metrics_file, {
                "total_entries": 0,
                "total_reads": 0,
                "total_writes": 0,
                "total_denied": 0,
                "total_consents": 0,
                "total_validations": 0,
                "total_sanitizations": 0,
                "skill_access_count": {},
                "last_updated": None
            })

    # ------------------------------------------------------------------
    # 安全文件 IO（统一异常处理）
    # ------------------------------------------------------------------

    def _safe_read_json(self, path: Path, default):
        """安全读取 JSON 文件；损坏或不存在时返回 default"""
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return default

    def _safe_write_json(self, path: Path, data):
        """安全写入 JSON 文件"""
        try:
            self._ensure_initialized()
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            return True
        except Exception:
            return False

    # ------------------------------------------------------------------
    # 加载 / 保存（供内部调用）
    # ------------------------------------------------------------------

    def _load_audit_log(self) -> List[Dict]:
        return self._safe_read_json(self.audit_log_file, [])

    def _save_audit_log(self, log: List[Dict]):
        self._safe_write_json(self.audit_log_file, log)

    def _load_defensive_log(self) -> List[Dict]:
        return self._safe_read_json(self.defensive_log_file, [])

    def _save_defensive_log(self, log: List[Dict]):
        self._safe_write_json(self.defensive_log_file, log)

    # [P0修复] _load_security_log 是 _load_defensive_log 的别名
    # 原代码中 get_recent_activity / get_anomaly_report 调用了该方法，但它不存在
    def _load_security_log(self) -> List[Dict]:
        """_load_defensive_log 的别名，保持向后兼容"""
        return self._load_defensive_log()

    def _load_metrics(self) -> Dict:
        default = {
            "total_entries": 0, "total_reads": 0, "total_writes": 0,
            "total_denied": 0, "total_consents": 0, "total_validations": 0,
            "total_sanitizations": 0, "skill_access_count": {}, "last_updated": None
        }
        return self._safe_read_json(self.metrics_file, default)

    def _save_metrics(self, metrics: Dict):
        metrics["last_updated"] = datetime.now().isoformat()
        self._safe_write_json(self.metrics_file, metrics)

    # ------------------------------------------------------------------
    # 计量更新
    # [P0修复] action 统一以字符串接收，与 Enum.value 比较而非与 Enum 对象比较
    # ------------------------------------------------------------------

    def _update_metrics(self, action: str, skill_name: Optional[str] = None):
        """更新审计计量器。action 为字符串（如 'READ'）"""
        try:
            metrics = self._load_metrics()
            metrics["total_entries"] += 1

            if action == AuditAction.READ.value:
                metrics["total_reads"] += 1
            elif action == AuditAction.WRITE.value:
                metrics["total_writes"] += 1
            elif action == AuditAction.ACCESS_DENIED.value:
                metrics["total_denied"] += 1
            elif action in (AuditAction.CONSENT_GRANTED.value,
                            AuditAction.CONSENT_DENIED.value,
                            AuditAction.CONSENT_REVOKED.value):
                metrics["total_consents"] += 1
            elif action == AuditAction.VALIDATION_FAILED.value:
                metrics["total_validations"] += 1
            elif action == AuditAction.SANITIZATION_APPLIED.value:
                metrics["total_sanitizations"] += 1

            if skill_name:
                metrics["skill_access_count"].setdefault(skill_name, 0)
                metrics["skill_access_count"][skill_name] += 1

            self._save_metrics(metrics)
        except Exception:
            pass  # 计量更新失败不影响主流程

    # ------------------------------------------------------------------
    # 核心日志接口
    # [P0修复] level 比较统一为字符串 vs 字符串，消除 str vs Enum 混用
    # ------------------------------------------------------------------

    def log(self, skill_name: str, action: str, message: str,
            details: Optional[Dict] = None, level: str = "INFO",
            user_consent: Optional[bool] = None, success: bool = True) -> Tuple[bool, str]:

        if not self._should_log(action):
            return True, "Logging disabled for this action type"

        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "action": action,
            "level": level,
            "message": message,
            "success": success,
            "skill_name": skill_name,
            "user_consent": user_consent,
            "details": details or {}
        }

        try:
            # [P0修复] 使用字符串比较，而非 str vs AuditLevel Enum
            if level in _HIGH_LEVELS:
                self._log_to_defensive_log(log_entry)
            else:
                self._log_to_audit_log(log_entry)

            # [P0修复] 传入字符串而非 Enum 对象
            self._update_metrics(action, skill_name)

            return True, "Log entry created successfully"

        except Exception as e:
            return False, f"Failed to create log entry: {str(e)}"

    def _should_log(self, action: str) -> bool:
        cfg = self.config["audit"]
        if action == AuditAction.READ.value and not cfg["log_all_access"]:
            return False
        if action == AuditAction.WRITE.value and not cfg["log_all_writes"]:
            return False
        if action in (AuditAction.CONSENT_GRANTED.value,
                      AuditAction.CONSENT_DENIED.value,
                      AuditAction.CONSENT_REVOKED.value) and not cfg["log_all_consents"]:
            return False
        if action == AuditAction.VALIDATION_FAILED.value and not cfg["log_validation_failures"]:
            return False
        if action == AuditAction.SANITIZATION_APPLIED.value and not cfg["log_sanitization"]:
            return False
        return True

    def _log_to_audit_log(self, log_entry: Dict):
        log = self._load_audit_log()
        log.append(log_entry)
        cfg = self.config["audit"]
        if cfg["log_rotation"] and len(log) > cfg["max_log_size"]:
            log = log[-cfg["max_log_size"]:]
        self._save_audit_log(log)

    def _log_to_defensive_log(self, log_entry: Dict):
        log = self._load_defensive_log()
        log.append(log_entry)
        cfg = self.config["audit"]
        if cfg["log_rotation"] and len(log) > cfg["max_log_size"]:
            log = log[-cfg["max_log_size"]:]
        self._save_defensive_log(log)

    # ------------------------------------------------------------------
    # 查询接口
    # ------------------------------------------------------------------

    def get_audit_log(self, skill_name: Optional[str] = None,
                      action: Optional[AuditAction] = None,
                      level: Optional[AuditLevel] = None,
                      limit: int = 100,
                      offset: int = 0) -> List[Dict]:
        log = self._load_audit_log()

        if skill_name:
            log = [e for e in log if e.get("skill_name") == skill_name]
        if action:
            log = [e for e in log if e.get("action") == action.value]
        if level:
            log = [e for e in log if e.get("level") == level.value]

        return log[offset:offset + limit]

    def get_defensive_log(self, skill_name: Optional[str] = None,
                          level: Optional[AuditLevel] = None,
                          limit: int = 100,
                          offset: int = 0) -> List[Dict]:
        log = self._load_defensive_log()

        if skill_name:
            log = [e for e in log if e.get("skill_name") == skill_name]
        if level:
            log = [e for e in log if e.get("level") == level.value]

        return log[offset:offset + limit]

    def get_metrics(self) -> Dict:
        return self._load_metrics()

    def get_skill_access_summary(self, skill_name: str) -> Dict:
        metrics = self._load_metrics()
        entries = [e for e in self._load_audit_log() if e.get("skill_name") == skill_name]

        reads = sum(1 for e in entries if e.get("action") == AuditAction.READ.value)
        writes = sum(1 for e in entries if e.get("action") == AuditAction.WRITE.value)
        denied = sum(1 for e in entries if e.get("action") == AuditAction.ACCESS_DENIED.value)
        errors = sum(1 for e in entries if e.get("level") in _HIGH_LEVELS)

        return {
            "skill_name": skill_name,
            "total_access": len(entries),
            "reads": reads,
            "writes": writes,
            "denied": denied,
            "errors": errors,
            "access_count": metrics["skill_access_count"].get(skill_name, 0),
            "last_access": entries[-1]["timestamp"] if entries else None
        }

    def get_all_skills_summary(self) -> List[Dict]:
        """
        [P2优化] 单次扫描所有条目，O(N+M) 而非原来的 O(N×M)
        """
        metrics = self._load_metrics()
        audit_log = self._load_audit_log()

        # 按 skill_name 分组
        skill_entries: Dict[str, List[Dict]] = {}
        for entry in audit_log:
            name = entry.get("skill_name")
            if name:
                skill_entries.setdefault(name, []).append(entry)

        summaries = []
        for skill_name, entries in skill_entries.items():
            reads = sum(1 for e in entries if e.get("action") == AuditAction.READ.value)
            writes = sum(1 for e in entries if e.get("action") == AuditAction.WRITE.value)
            denied = sum(1 for e in entries if e.get("action") == AuditAction.ACCESS_DENIED.value)
            errors = sum(1 for e in entries if e.get("level") in _HIGH_LEVELS)

            summaries.append({
                "skill_name": skill_name,
                "total_access": len(entries),
                "reads": reads,
                "writes": writes,
                "denied": denied,
                "errors": errors,
                "access_count": metrics["skill_access_count"].get(skill_name, 0),
                "last_access": entries[-1]["timestamp"] if entries else None
            })

        summaries.sort(key=lambda x: x["total_access"], reverse=True)
        return summaries

    # ------------------------------------------------------------------
    # 导出
    # [P1修复] 增加路径安全校验，防止路径穿越写入系统任意位置
    # ------------------------------------------------------------------

    def export_log(self, output_path: str, log_type: str = "audit",
                   format: str = "json", filters: Optional[Dict] = None) -> Tuple[bool, str]:
        try:
            # [P1修复] 路径安全校验：输出文件必须在 user_data_path 下
            output_file = Path(output_path).resolve()
            if not str(output_file).startswith(str(self.user_data_path)):
                return False, f"安全拒绝：导出路径必须位于 {self.user_data_path} 目录内"

            if log_type == "audit":
                log = self._load_audit_log()
            elif log_type == "defensive":
                log = self._load_defensive_log()
            else:
                return False, f"未知日志类型: {log_type}"

            if filters:
                if filters.get("skill_name"):
                    log = [e for e in log if e.get("skill_name") == filters["skill_name"]]
                if filters.get("action"):
                    log = [e for e in log if e.get("action") == filters["action"]]
                if filters.get("level"):
                    log = [e for e in log if e.get("level") == filters["level"]]

            output_file.parent.mkdir(parents=True, exist_ok=True)

            if format == "json":
                with open(output_file, 'w', encoding='utf-8') as f:
                    json.dump(log, f, indent=2, ensure_ascii=False)
            elif format == "csv":
                import csv
                if log:
                    with open(output_file, 'w', newline='', encoding='utf-8') as f:
                        writer = csv.DictWriter(f, fieldnames=log[0].keys())
                        writer.writeheader()
                        writer.writerows(log)
            else:
                return False, f"不支持的格式: {format}"

            return True, f"日志已导出至 {output_path}"

        except Exception as e:
            return False, f"导出失败: {str(e)}"

    def clear_log(self, log_type: str = "audit") -> Tuple[bool, str]:
        try:
            if log_type == "audit":
                self._save_audit_log([])
            elif log_type == "defensive":
                self._save_defensive_log([])
            else:
                return False, f"未知日志类型: {log_type}"
            return True, f"{log_type} 日志已清空"
        except Exception as e:
            return False, f"清空失败: {str(e)}"

    # ------------------------------------------------------------------
    # 活动分析
    # [P0修复] get_recent_activity / get_anomaly_report 调用的 _load_security_log 已补全
    # ------------------------------------------------------------------

    def get_recent_activity(self, hours: int = 24, limit: int = 50) -> List[Dict]:
        from datetime import timedelta

        audit_log = self._load_audit_log()
        defensive_log = self._load_security_log()  # 现在已补全，不再崩溃

        all_logs = audit_log + defensive_log
        cutoff_time = datetime.now() - timedelta(hours=hours)

        recent = []
        for entry in all_logs:
            try:
                if datetime.fromisoformat(entry["timestamp"]) >= cutoff_time:
                    recent.append(entry)
            except (KeyError, ValueError):
                continue

        recent.sort(key=lambda x: x.get("timestamp", ""), reverse=True)
        return recent[:limit]

    def get_defensive_events(self, hours: int = 24) -> List[Dict]:
        from datetime import timedelta

        log = self._load_defensive_log()
        cutoff_time = datetime.now() - timedelta(hours=hours)

        recent = []
        for entry in log:
            try:
                if datetime.fromisoformat(entry["timestamp"]) >= cutoff_time:
                    recent.append(entry)
            except (KeyError, ValueError):
                continue

        recent.sort(key=lambda x: x.get("timestamp", ""), reverse=True)
        return recent

    def get_anomaly_report(self) -> Dict:
        metrics = self._load_metrics()
        audit_log = self._load_audit_log()
        # [P0修复] _load_security_log 已补全
        self._load_security_log()  # 确保方法可调用（此处结果用于 recent_defensive_events）

        denied_entries = [e for e in audit_log if e.get("action") == AuditAction.ACCESS_DENIED.value]
        error_entries = [e for e in audit_log if e.get("level") in _HIGH_LEVELS]

        skill_denials: Dict[str, int] = {}
        for entry in denied_entries:
            name = entry.get("skill_name", "unknown")
            skill_denials[name] = skill_denials.get(name, 0) + 1

        return {
            "total_denied_access": len(denied_entries),
            "total_errors": len(error_entries),
            "high_denial_skills": [
                {"skill": s, "denials": c}
                for s, c in sorted(skill_denials.items(), key=lambda x: x[1], reverse=True)[:5]
            ],
            "recent_defensive_events": len(self.get_defensive_events(hours=24)),
            "recommendations": self._generate_recommendations(denied_entries, error_entries)
        }

    def _generate_recommendations(self, denied_entries: List[Dict], error_entries: List[Dict]) -> List[str]:
        recommendations = []

        if len(denied_entries) > 10:
            recommendations.append("检测到大量访问拒绝，建议检查授权配置。")

        skill_denials: Dict[str, int] = {}
        for entry in denied_entries:
            name = entry.get("skill_name", "unknown")
            skill_denials[name] = skill_denials.get(name, 0) + 1

        for skill, count in skill_denials.items():
            if count > 5:
                recommendations.append(f"技能 '{skill}' 被拒绝 {count} 次，建议检查其授权状态。")

        if len(error_entries) > 5:
            recommendations.append("检测到多处错误，建议查看系统日志。")

        return recommendations
