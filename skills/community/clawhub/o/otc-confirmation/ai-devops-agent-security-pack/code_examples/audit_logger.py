"""
Audit Logger — Structured Operation Logging for AI Agents

Provides structured, sanitized, queryable audit logging for all agent operations.
Outputs JSONL (one JSON object per line) for easy processing.

Usage:
    logger = AuditLogger(log_dir="~/.openclaw/audit")
    
    # Log an operation
    logger.record(
        event_type=EventType.OPERATION,
        operation="exec_command",
        command="kubectl rollout restart deployment/api",
        decision="CONFIRMED",
        agent_id="deploy-bot",
        session_id="sess_main",
    )
    
    # Query logs
    results = logger.query(
        since=datetime(2026, 3, 1),
        decision="DENY",
    )

Requirements:
    Python 3.10+
    No external dependencies
"""

import gzip
import json
import os
import re
import uuid
from dataclasses import asdict, dataclass, field
from datetime import datetime, timedelta, timezone
from enum import Enum
from pathlib import Path
from typing import Any, Generator, Optional


# =============================================================
# Configuration
# =============================================================

@dataclass
class AuditConfig:
    """Audit logger configuration."""
    log_dir: str = "~/.openclaw/audit"
    file_prefix: str = "audit"
    max_file_size_mb: int = 50
    compress_after_days: int = 7
    
    # Retention (days)
    retention_security: int = 365
    retention_confirmed: int = 90
    retention_allowed: int = 30
    retention_readonly: int = 7
    
    # Sanitization
    sanitize_patterns: bool = True


# =============================================================
# Data Models
# =============================================================

class EventType(Enum):
    OPERATION = "operation"
    SECURITY = "security"
    OTC = "otc"
    RATE_LIMIT = "rate_limit"
    SYSTEM = "system"


@dataclass
class AuditEvent:
    """A single audit event."""
    timestamp: str
    event_id: str
    event_type: str
    
    # Actor
    agent_id: str = ""
    agent_role: str = ""
    session_id: str = ""
    
    # Operation
    operation: str = ""
    command: str = ""
    target: str = ""
    parameters: dict = field(default_factory=dict)
    
    # Decision
    decision: str = ""              # ALLOW, DENY, CONFIRMED, CONFIRM_FAILED, BLOCKED
    decision_reason: str = ""
    guard_rule: str = ""
    risk_score: int = 0
    otc_verified: bool = False
    otc_attempts: int = 0
    
    # Result
    result_status: str = ""         # success, failure, timeout, error
    result_exit_code: Optional[int] = None
    result_duration_ms: int = 0
    
    # Context
    triggered_by: str = ""          # user_request, cron, heartbeat, agent
    user_id: str = ""
    channel: str = ""
    
    # Metadata
    extra: dict = field(default_factory=dict)


# =============================================================
# Sanitization
# =============================================================

SANITIZE_RULES = [
    # Passwords and tokens
    (r'(?i)(password|passwd|pass|token|secret|key|api_key|apikey)\s*[=:]\s*\S+',
     r'\1=***REDACTED***'),
    
    # Authorization headers
    (r'(?i)(authorization:\s*)(bearer\s+)?\S+',
     r'\1***REDACTED***'),
    
    # Connection strings with passwords
    (r'((?:mysql|postgres|mongodb|redis)://\S+?:)\S+(@)',
     r'\1***@\2'),
    
    # AWS credentials
    (r'(AKIA[A-Z0-9]{16})',
     r'***AWS_KEY***'),
    
    # Base64-encoded secrets (long base64 strings)
    (r'(?<=[=:\s])[A-Za-z0-9+/]{40,}={0,2}(?=\s|$)',
     r'***BASE64_REDACTED***'),
    
    # Email body content (keep recipient, redact body)
    (r'(--mail-data\s+).+',
     r'\1***REDACTED_BODY***'),
]


def sanitize(text: str) -> str:
    """Remove sensitive data from text before logging."""
    result = text
    for pattern, replacement in SANITIZE_RULES:
        result = re.sub(pattern, replacement, result)
    return result


# =============================================================
# Audit Logger
# =============================================================

class AuditLogger:
    """Structured audit logger with JSONL output."""
    
    def __init__(self, config: Optional[AuditConfig] = None):
        self.config = config or AuditConfig()
        self.log_dir = Path(os.path.expanduser(self.config.log_dir))
        self.log_dir.mkdir(parents=True, exist_ok=True)
    
    def record(
        self,
        event_type: EventType = EventType.OPERATION,
        operation: str = "",
        command: str = "",
        target: str = "",
        parameters: Optional[dict] = None,
        decision: str = "",
        decision_reason: str = "",
        guard_rule: str = "",
        risk_score: int = 0,
        otc_verified: bool = False,
        otc_attempts: int = 0,
        result_status: str = "",
        result_exit_code: Optional[int] = None,
        result_duration_ms: int = 0,
        agent_id: str = "",
        agent_role: str = "",
        session_id: str = "",
        triggered_by: str = "",
        user_id: str = "",
        channel: str = "",
        **extra,
    ) -> AuditEvent:
        """Record an audit event."""
        
        # Sanitize sensitive data
        if self.config.sanitize_patterns:
            command = sanitize(command)
            target = sanitize(target)
            if parameters:
                parameters = json.loads(sanitize(json.dumps(parameters)))
        
        event = AuditEvent(
            timestamp=datetime.now(timezone.utc).isoformat(),
            event_id=f"evt_{uuid.uuid4().hex[:12]}",
            event_type=event_type.value,
            agent_id=agent_id,
            agent_role=agent_role,
            session_id=session_id,
            operation=operation,
            command=command,
            target=target,
            parameters=parameters or {},
            decision=decision,
            decision_reason=decision_reason,
            guard_rule=guard_rule,
            risk_score=risk_score,
            otc_verified=otc_verified,
            otc_attempts=otc_attempts,
            result_status=result_status,
            result_exit_code=result_exit_code,
            result_duration_ms=result_duration_ms,
            triggered_by=triggered_by,
            user_id=user_id,
            channel=channel,
            extra=extra,
        )
        
        self._write(event)
        return event
    
    def query(
        self,
        since: Optional[datetime] = None,
        until: Optional[datetime] = None,
        decision: Optional[str] = None,
        operation: Optional[str] = None,
        agent_id: Optional[str] = None,
        event_type: Optional[str] = None,
        min_risk_score: int = 0,
        limit: int = 100,
    ) -> list[dict]:
        """Query audit logs with filters."""
        results = []
        
        for event in self._read_events(since, until):
            # Apply filters
            if decision and event.get("decision") != decision:
                continue
            if operation and event.get("operation") != operation:
                continue
            if agent_id and event.get("agent_id") != agent_id:
                continue
            if event_type and event.get("event_type") != event_type:
                continue
            if event.get("risk_score", 0) < min_risk_score:
                continue
            
            results.append(event)
            if len(results) >= limit:
                break
        
        return results
    
    def daily_summary(self, date: Optional[datetime] = None) -> dict:
        """Generate a daily audit summary."""
        if date is None:
            date = datetime.now(timezone.utc)
        
        start = date.replace(hour=0, minute=0, second=0, microsecond=0)
        end = start + timedelta(days=1)
        
        events = self.query(since=start, until=end, limit=10000)
        
        decisions = {}
        operations = {}
        agents = set()
        alerts = []
        
        for e in events:
            dec = e.get("decision", "UNKNOWN")
            decisions[dec] = decisions.get(dec, 0) + 1
            
            op = e.get("operation", "unknown")
            operations[op] = operations.get(op, 0) + 1
            
            if e.get("agent_id"):
                agents.add(e["agent_id"])
            
            if dec in ("DENY", "CONFIRM_FAILED", "BLOCKED"):
                alerts.append({
                    "time": e["timestamp"],
                    "operation": op,
                    "decision": dec,
                    "reason": e.get("decision_reason", ""),
                })
        
        return {
            "date": start.strftime("%Y-%m-%d"),
            "total_events": len(events),
            "by_decision": decisions,
            "by_operation": operations,
            "unique_agents": list(agents),
            "alert_count": len(alerts),
            "alerts": alerts[:20],  # Top 20 alerts
        }
    
    def cleanup(self):
        """Remove expired log files based on retention policy."""
        now = datetime.now(timezone.utc)
        
        for log_file in sorted(self.log_dir.glob(f"{self.config.file_prefix}-*.jsonl*")):
            # Extract date from filename
            try:
                date_str = log_file.stem.replace(f"{self.config.file_prefix}-", "").replace(".jsonl", "")
                file_date = datetime.strptime(date_str, "%Y-%m-%d").replace(tzinfo=timezone.utc)
            except ValueError:
                continue
            
            age_days = (now - file_date).days
            
            # Compress old files
            if age_days > self.config.compress_after_days and log_file.suffix != ".gz":
                self._compress(log_file)
                continue
            
            # Delete expired files (use most conservative retention)
            if age_days > self.config.retention_security:
                log_file.unlink()
    
    # --- Internal ---
    
    def _write(self, event: AuditEvent):
        """Append event to today's log file."""
        date_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        log_file = self.log_dir / f"{self.config.file_prefix}-{date_str}.jsonl"
        
        event_dict = asdict(event)
        # Remove None values and empty strings for cleaner output
        event_dict = {k: v for k, v in event_dict.items() if v not in (None, "", {}, [])}
        
        with open(log_file, "a") as f:
            f.write(json.dumps(event_dict, ensure_ascii=False) + "\n")
    
    def _read_events(
        self, 
        since: Optional[datetime], 
        until: Optional[datetime]
    ) -> Generator[dict, None, None]:
        """Read events from log files within date range."""
        log_files = sorted(self.log_dir.glob(f"{self.config.file_prefix}-*.jsonl*"))
        
        for log_file in reversed(log_files):  # Most recent first
            opener = gzip.open if log_file.suffix == ".gz" else open
            mode = "rt" if log_file.suffix == ".gz" else "r"
            
            try:
                with opener(log_file, mode) as f:
                    for line in f:
                        line = line.strip()
                        if not line:
                            continue
                        try:
                            event = json.loads(line)
                        except json.JSONDecodeError:
                            continue
                        
                        ts = datetime.fromisoformat(event.get("timestamp", ""))
                        if since and ts < since:
                            continue
                        if until and ts > until:
                            continue
                        
                        yield event
            except (OSError, IOError):
                continue
    
    def _compress(self, file_path: Path):
        """Compress a log file with gzip."""
        gz_path = file_path.with_suffix(file_path.suffix + ".gz")
        with open(file_path, "rb") as f_in:
            with gzip.open(gz_path, "wb") as f_out:
                f_out.writelines(f_in)
        file_path.unlink()


# =============================================================
# Example Usage
# =============================================================

if __name__ == "__main__":
    logger = AuditLogger(AuditConfig(log_dir="/tmp/otc_audit_demo"))
    
    # Simulate some operations
    logger.record(
        operation="file_read",
        command="cat /etc/hostname",
        decision="ALLOW",
        risk_score=5,
        agent_id="laicai",
        session_id="sess_main",
    )
    
    logger.record(
        operation="send_email",
        command="curl --ssl-reqd smtps://smtp.gmail.com --mail-data 'Hello world'",
        decision="CONFIRMED",
        otc_verified=True,
        otc_attempts=1,
        risk_score=35,
        agent_id="laicai",
        session_id="sess_main",
        result_status="success",
    )
    
    logger.record(
        event_type=EventType.SECURITY,
        operation="exec_command",
        command="rm -rf /",
        decision="DENY",
        decision_reason="Catastrophic: recursive delete from root",
        guard_rule="recursive-root-delete",
        risk_score=100,
        agent_id="laicai",
    )
    
    # Generate summary
    summary = logger.daily_summary()
    print(json.dumps(summary, indent=2, ensure_ascii=False))
