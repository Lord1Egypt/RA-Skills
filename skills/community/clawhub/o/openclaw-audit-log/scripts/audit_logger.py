#!/usr/bin/env python3
"""
OpenClaw Audit Logger
记录所有敏感操作到 audit log 文件，供后续审计分析使用。
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path

AUDIT_DIR = Path.home() / ".openclaw" / "audit"
AUDIT_FILE = AUDIT_DIR / "audit.log"

# 敏感操作类型
OP_TYPES = {
    "file_delete": "文件删除",
    "file_write": "文件写入",
    "file_move": "文件移动",
    "external_send": "外部发送",
    "config_change": "配置修改",
    "credential_access": "凭证访问",
    "permission_change": "权限变更",
    "external_api": "外部API调用",
    "user_data_access": "用户数据访问",
    "destruction": "高危操作",
}

# 风险等级
RISK_LEVELS = {
    "file_delete": "high",
    "destruction": "critical",
    "credential_access": "critical",
    "external_send": "high",
    "config_change": "medium",
    "file_write": "medium",
    "file_move": "medium",
    "permission_change": "high",
    "external_api": "medium",
    "user_data_access": "medium",
}

# 需要飞书确认的高危操作（事中拦截）
CONFIRM_REQUIRED = {"critical", "high"}


def ensure_dir():
    AUDIT_DIR.mkdir(parents=True, exist_ok=True)


def log(
    operation: str,
    detail: str,
    session_key: str = "",
    risk_level: str = None,
    metadata: dict = None,
    realtime_alert: bool = True,
):
    """
    写入一条审计日志（JSONL格式，每行一条）。
    """
    ensure_dir()
    if risk_level is None:
        risk_level = RISK_LEVELS.get(operation, "low")

    record = {
        "timestamp": datetime.now().isoformat(),
        "operation": operation,
        "operation_name": OP_TYPES.get(operation, operation),
        "detail": detail,
        "session_key": session_key,
        "risk_level": risk_level,
        "metadata": metadata or {},
    }

    ensure_dir()
    with open(AUDIT_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")

    # critical 级别自动实时预警
    if realtime_alert and risk_level == "critical":
        try:
            from audit_feishu import send_realtime_alert
            send_realtime_alert(operation, detail, risk_level)
        except Exception:
            pass  # 预警失败不影响主流程

    return record


def query(
    operation: str = None,
    risk_level: str = None,
    since: str = None,  # ISO格式时间字符串
    limit: int = 100,
) -> list:
    """
    查询审计日志。
    """
    if not AUDIT_FILE.exists():
        return []

    records = []
    with open(AUDIT_FILE, "r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            try:
                r = json.loads(line)
            except Exception:
                continue

            if operation and r.get("operation") != operation:
                continue
            if risk_level and r.get("risk_level") != risk_level:
                continue
            if since and r.get("timestamp", "") < since:
                continue

            records.append(r)

    return records[-limit:]


def summary(days: int = 7) -> dict:
    """
    生成最近 N 天的审计摘要。
    """
    from datetime import timedelta

    cutoff = (datetime.now() - timedelta(days=days)).isoformat()
    records = query(since=cutoff, limit=10000)

    total = len(records)
    by_op = {}
    by_risk = {"critical": 0, "high": 0, "medium": 0, "low": 0}
    by_day = {}

    for r in records:
        op = r.get("operation", "unknown")
        by_op[op] = by_op.get(op, 0) + 1
        risk = r.get("risk_level", "low")
        by_risk[risk] = by_risk.get(risk, 0) + 1
        day = r.get("timestamp", "")[:10]
        by_day[day] = by_day.get(day, 0) + 1

    return {
        "period_days": days,
        "total_operations": total,
        "by_operation": by_op,
        "by_risk_level": by_risk,
        "by_day": by_day,
        "records": records[-50:],  # 最近50条
    }


def confirm_required(operation: str) -> bool:
    """判断操作是否需要飞书确认"""
    risk = RISK_LEVELS.get(operation, "low")
    return risk in CONFIRM_REQUIRED


def send_confirm_request(operation: str, detail: str, session_key: str = "") -> str:
    """发送飞书确认请求，返回 confirm_id"""
    import urllib.request
    import json as _json

    risk = RISK_LEVELS.get(operation, "high")

    # 调用 confirm.py request
    import subprocess
    result = subprocess.run(
        ["python3",
         str(Path(__file__).parent / "confirm.py"),
         "request", operation, detail, "", risk],
        capture_output=True, text=True, timeout=30
    )

    confirm_id = ""
    for line in result.stdout.splitlines():
        if line.startswith("CONFIRM_ID="):
            confirm_id = line.split("=", 1)[1].strip()
    return confirm_id


def check_confirm_and_execute(operation: str, detail: str,
                               confirmed_cb=None,
                               rejected_cb=None,
                               timeout_cb=None,
                               wait_sec: int = 600) -> str:
    """
    两阶段执行：先确认，执行后记录。
    返回：'confirmed' / 'rejected' / 'timeout'
    """
    import subprocess
    import time as _time

    risk = RISK_LEVELS.get(operation, "high")
    confirm_id = send_confirm_request(operation, detail)

    # 轮询等待用户回复
    start = _time.time()
    while _time.time() - start < wait_sec:
        result = subprocess.run(
            ["python3",
             str(Path(__file__).parent / "confirm.py"),
             "check"],
            capture_output=True, text=True, timeout=30
        )

        # 解析状态
        status = None
        for line in result.stdout.splitlines():
            if line.startswith(f"[{confirm_id}]"):
                parts = line.split(":")
                if len(parts) >= 2:
                    status = parts[1].strip()
            elif line.startswith("UPDATED=") and "yes" in line:
                # 重新检查
                pass

        if status and status != "pending":
            # 记录结果
            if status == "confirmed":
                log(operation, f"{detail} [确认执行]", session_key="", risk_level=risk)
                if confirmed_cb:
                    confirmed_cb()
            elif status == "rejected":
                log(operation, f"{detail} [已拦截-用户拒绝]", session_key="")
                if rejected_cb:
                    rejected_cb()
            elif status == "timeout":
                log(operation, f"{detail} [已拦截-超时未确认]", session_key="")
                if timeout_cb:
                    timeout_cb()

            return status

        _time.sleep(5)

    # 超时
    log(operation, f"{detail} [已拦截-超时未确认]", session_key="")
    if timeout_cb:
        timeout_cb()
    return "timeout"


def clear_before(days: int = 90):
    """
    清理 N 天之前的旧日志（保留最近 N 天）。
    """
    from datetime import timedelta

    cutoff = (datetime.now() - timedelta(days=days)).isoformat()
    ensure_dir()

    kept = []
    deleted = 0
    if AUDIT_FILE.exists():
        with open(AUDIT_FILE, "r", encoding="utf-8") as f:
            for line in f:
                if not line.strip():
                    continue
                try:
                    r = json.loads(line)
                    if r.get("timestamp", "") >= cutoff:
                        kept.append(line)
                    else:
                        deleted += 1
                except Exception:
                    pass

        with open(AUDIT_FILE, "w", encoding="utf-8") as f:
            f.writelines(kept)

    return deleted


if __name__ == "__main__":
    # 命令行用法
    if len(sys.argv) < 2:
        print("Usage: audit_logger.py <command> [args]")
        print("Commands: log, query, summary, clear")
        sys.exit(1)

    cmd = sys.argv[1]

    if cmd == "log":
        if len(sys.argv) < 4:
            print("Usage: audit_logger.py log <operation> <detail>")
            sys.exit(1)
        log(sys.argv[2], sys.argv[3])
        print("OK")

    elif cmd == "query":
        records = query(limit=20)
        for r in records:
            print(json.dumps(r, ensure_ascii=False))

    elif cmd == "summary":
        days = int(sys.argv[2]) if len(sys.argv) > 2 else 7
        result = summary(days)
        print(json.dumps(result, ensure_ascii=False, indent=2))

    elif cmd == "clear":
        days = int(sys.argv[2]) if len(sys.argv) > 2 else 90
        n = clear_before(days)
        print(f"Deleted {n} old records")

    else:
        print(f"Unknown command: {cmd}")
        sys.exit(1)
