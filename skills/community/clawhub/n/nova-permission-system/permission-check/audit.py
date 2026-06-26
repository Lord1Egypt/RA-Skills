"""
审计日志模块
记录所有权限相关操作
"""

import json
from datetime import datetime
from pathlib import Path

LOG_DIR = Path("/workspace/logs")
LOG_FILE = LOG_DIR / "audit.log"


def log_operation(operation: str, user_id: str = None, open_id: str = None, 
                  identity: str = None, result: str = None, details: dict = None):
    """记录操作日志"""
    LOG_DIR.mkdir(exist_ok=True)
    
    log_entry = {
        "timestamp": datetime.now().isoformat() + "Z",
        "operation": operation,
        "user_id": user_id,
        "open_id": open_id,
        "identity": identity,
        "result": result,
        "details": details or {}
    }
    
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")
    
    return log_entry


def get_logs(limit: int = 50) -> list:
    """获取最近的日志"""
    if not LOG_FILE.exists():
        return []
    
    logs = []
    with open(LOG_FILE, "r", encoding="utf-8") as f:
        lines = f.readlines()
        for line in lines[-limit:]:
            try:
                logs.append(json.loads(line))
            except:
                continue
    return logs


def get_user_logs(open_id: str = None, user_id: str = None) -> list:
    """获取指定用户的日志"""
    all_logs = get_logs(limit=1000)
    return [l for l in all_logs if l.get("open_id") == open_id or l.get("user_id") == user_id]


# 便捷函数
def log_permission_check(open_id: str, action: str, result: bool, reason: str = None):
    """记录权限检查"""
    log_operation(
        operation="permission_check",
        open_id=open_id,
        result="allowed" if result else "denied",
        details={"action": action, "reason": reason}
    )


def log_identity_verification(open_id: str, verified: bool, reason: str = None):
    """记录身份验证"""
    log_operation(
        operation="identity_verification",
        open_id=open_id,
        result="verified" if verified else "failed",
        details={"reason": reason}
    )


def log_identity_change(user_id: str, old_identity: str, new_identity: str, reason: str = None):
    """记录身份变更"""
    log_operation(
        operation="identity_change",
        user_id=user_id,
        result="success",
        details={
            "old_identity": old_identity, 
            "new_identity": new_identity,
            "reason": reason
        }
    )


def log_account_bind(open_id: str, user_id: str, result: str):
    """记录账号绑定"""
    log_operation(
        operation="account_bind",
        open_id=open_id,
        user_id=user_id,
        result=result
    )


def log_contact(user_id: str, open_id: str, channel: str):
    """记录沟通"""
    log_operation(
        operation="contact",
        user_id=user_id,
        open_id=open_id,
        identity=None,
        result="success",
        details={"channel": channel}
    )
