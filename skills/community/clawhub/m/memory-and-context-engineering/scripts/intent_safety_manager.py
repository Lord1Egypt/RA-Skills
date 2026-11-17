"""
意图安全与审计管理器

提供操作白名单验证、权限分级控制、审计日志记录和操作确认机制。
采用"纵深防御"策略，确保系统安全性。

Author: kiwifruit
Version: 1.0.0
License: GPL-3.0
"""

from __future__ import annotations

import hashlib
import json
import uuid
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Optional


class OperationRisk(str, Enum):
    """操作风险级别"""
    LOW = "low"       # 低风险：只读操作
    MEDIUM = "medium"  # 中风险：写入操作
    HIGH = "high"     # 高风险：删除操作
    CRITICAL = "critical"  # 极高风险：系统操作


class OperationType(str, Enum):
    """操作类型枚举"""
    READ_MEMORY = "read_memory"          # 读取记忆
    READ_CONTEXT = "read_context"        # 读取上下文
    READ_STATE = "read_state"            # 读取状态
    WRITE_MEMORY = "write_memory"        # 写入记忆
    WRITE_CONTEXT = "write_context"      # 写入上下文
    UPDATE_STATE = "update_state"        # 更新状态
    DELETE_MEMORY = "delete_memory"      # 删除记忆
    DELETE_CONTEXT = "delete_context"    # 删除上下文
    CLEAR_STATE = "clear_state"          # 清除状态
    BACKUP = "backup"                   # 备份
    RESTORE = "restore"                 # 恢复
    EXPORT = "export"                   # 导出
    IMPORT = "import"                   # 导入
    EXECUTE_TOOL = "execute_tool"       # 执行工具
    QUERY_KNOWLEDGE = "query_knowledge"  # 查询知识
    UNKNOWN = "unknown"                 # 未知操作


class PermissionLevel(str, Enum):
    """用户权限级别"""
    GUEST = "guest"         # 访客：只读操作
    USER = "user"           # 普通用户：读写操作
    POWER_USER = "power_user"  # 高级用户：读写+部分删除
    ADMIN = "admin"         # 管理员：所有操作


class AuditLog:
    """审计日志记录"""

    def __init__(
        self,
        operation_id: str,
        operation: str,
        user_id: str,
        user_level: str,
        risk_level: str,
        ip_address: Optional[str],
        user_agent: Optional[str],
        success: bool,
        message: str,
        params: Optional[dict] = None,
    ):
        self.operation_id = operation_id
        self.operation = operation
        self.user_id = user_id
        self.user_level = user_level
        self.risk_level = risk_level
        self.ip_address = ip_address
        self.user_agent = user_agent
        self.success = success
        self.message = message
        self.params = params
        self.timestamp = datetime.now().isoformat()

    def to_dict(self) -> dict[str, Any]:
        return {
            "operation_id": self.operation_id,
            "operation": self.operation,
            "user_id": self.user_id,
            "user_level": self.user_level,
            "risk_level": self.risk_level,
            "ip_address": self.ip_address,
            "user_agent": self.user_agent,
            "success": self.success,
            "message": self.message,
            "params": self.params,
            "timestamp": self.timestamp,
        }


class OperationResult:
    """操作检查结果"""

    def __init__(
        self,
        success: bool,
        allowed: bool,
        operation_id: str,
        message: str,
        requires_confirmation: bool = False,
        confirmation_token: Optional[str] = None,
        risk_level: Optional[str] = None,
        audit_log: Optional[AuditLog] = None,
    ):
        self.success = success
        self.allowed = allowed
        self.operation_id = operation_id
        self.message = message
        self.requires_confirmation = requires_confirmation
        self.confirmation_token = confirmation_token
        self.risk_level = risk_level
        self.audit_log = audit_log

    def to_dict(self) -> dict[str, Any]:
        return {
            "success": self.success,
            "allowed": self.allowed,
            "operation_id": self.operation_id,
            "message": self.message,
            "requires_confirmation": self.requires_confirmation,
            "confirmation_token": self.confirmation_token,
            "risk_level": self.risk_level,
        }


class IntentSafetyManager:
    """
    意图安全与审计管理器

    采用"纵深防御"策略：
    1. 操作白名单验证
    2. 权限分级控制
    3. 审计日志记录
    4. 操作确认机制

    Attributes:
        allowed_operations: 允许的操作集合
        permission_levels: 权限级别定义
        sensitive_operations: 高风险操作列表
        audit_logs: 审计日志列表
        confirmation_tokens: 待确认操作令牌
    """

    # 权限级别定义：权限级别 -> 可执行的操作类型
    PERMISSION_OPERATION_MAP = {
        "guest": {
            "read_memory",
            "read_context",
            "read_state",
            "query_knowledge",
        },
        "user": {
            "read_memory",
            "read_context",
            "read_state",
            "write_memory",
            "write_context",
            "update_state",
            "query_knowledge",
        },
        "power_user": {
            "read_memory",
            "read_context",
            "read_state",
            "write_memory",
            "write_context",
            "update_state",
            "delete_memory",
            "delete_context",
            "query_knowledge",
        },
        "admin": {
            "read_memory",
            "read_context",
            "read_state",
            "write_memory",
            "write_context",
            "update_state",
            "delete_memory",
            "delete_context",
            "clear_state",
            "backup",
            "restore",
            "export",
            "import",
            "query_knowledge",
        },
    }

    # 操作风险级别定义
    OPERATION_RISK_MAP = {
        "read_memory": "low",
        "read_context": "low",
        "read_state": "low",
        "write_memory": "medium",
        "write_context": "medium",
        "update_state": "medium",
        "delete_memory": "high",
        "delete_context": "high",
        "clear_state": "high",
        "backup": "medium",
        "restore": "high",
        "export": "medium",
        "import": "high",
        "execute_tool": "critical",
        "query_knowledge": "low",
        "unknown": "critical",
    }

    # 需要确认的高风险操作
    HIGH_RISK_OPERATIONS = {
        "delete_memory",
        "delete_context",
        "clear_state",
        "restore",
        "import",
        "execute_tool",
    }

    def __init__(
        self,
        storage_path: Optional[str] = None,
        enable_audit: bool = True,
        max_audit_logs: int = 10000,
        confirmation_timeout: int = 300,
    ):
        """
        初始化意图安全管理器

        Args:
            storage_path: 审计日志存储路径
            enable_audit: 是否启用审计日志
            max_audit_logs: 最大审计日志数量
            confirmation_timeout: 确认超时时间（秒）
        """
        self.storage_path = storage_path or "./privacy_data"
        self.enable_audit = enable_audit
        self.max_audit_logs = max_audit_logs
        self.confirmation_timeout = confirmation_timeout

        # 审计日志列表（内存缓存）
        self.audit_logs: list[AuditLog] = []

        # 待确认操作令牌
        self.confirmation_tokens: dict[str, dict] = {}

        # 确保存储目录存在
        Path(self.storage_path).mkdir(parents=True, exist_ok=True)

    def check_operation(
        self,
        operation: str,
        user_level: str,
        params: Optional[dict] = None,
        user_id: str = "anonymous",
        session_id: Optional[str] = None,
    ) -> OperationResult:
        """
        检查操作是否允许执行

        Args:
            operation: 操作类型
            user_level: 用户权限级别
            params: 操作参数
            user_id: 用户ID
            session_id: 会话ID

        Returns:
            操作结果
        """
        operation_id = self._generate_operation_id()

        # 1. 检查操作是否在白名单中
        if not self._is_operation_allowed(operation):
            return self._create_result(
                success=False,
                allowed=False,
                operation_id=operation_id,
                message=f"Operation '{operation}' is not in the whitelist",
                user_level=user_level,
                operation=operation,
            )

        # 2. 获取操作风险级别
        risk_level = self._get_operation_risk(operation)

        # 3. 检查用户权限
        if not self._has_permission(user_level, operation):
            return self._create_result(
                success=False,
                allowed=False,
                operation_id=operation_id,
                message=f"User level '{user_level}' does not have permission for '{operation}'",
                user_level=user_level,
                operation=operation,
                risk_level=risk_level,
            )

        # 4. 检查是否需要确认
        if operation in self.HIGH_RISK_OPERATIONS:
            confirmation_token = self._generate_confirmation_token(
                operation_id, operation, user_id
            )
            return self._create_result(
                success=True,
                allowed=True,
                operation_id=operation_id,
                message=f"Operation '{operation}' requires confirmation",
                requires_confirmation=True,
                confirmation_token=confirmation_token,
                user_level=user_level,
                operation=operation,
                risk_level=risk_level,
            )

        # 5. 创建审计日志
        audit_log = self._create_audit_log(
            operation_id=operation_id,
            operation=operation,
            user_id=user_id,
            user_level=user_level,
            risk_level=risk_level,
            success=True,
            message="Operation allowed",
            params=params,
        )

        return self._create_result(
            success=True,
            allowed=True,
            operation_id=operation_id,
            message="Operation allowed",
            user_level=user_level,
            operation=operation,
            risk_level=risk_level,
            audit_log=audit_log,
        )

    def confirm_operation(
        self,
        confirmation_token: str,
        user_id: str,
    ) -> OperationResult:
        """
        确认高风险操作

        Args:
            confirmation_token: 确认令牌
            user_id: 用户ID

        Returns:
            操作结果
        """
        if confirmation_token not in self.confirmation_tokens:
            return OperationResult(
                success=False,
                allowed=False,
                operation_id="",
                message="Invalid confirmation token",
            )

        token_data = self.confirmation_tokens[confirmation_token]
        if token_data["user_id"] != user_id:
            return OperationResult(
                success=False,
                allowed=False,
                operation_id=token_data["operation_id"],
                message="Token user mismatch",
            )

        # 删除令牌
        del self.confirmation_tokens[confirmation_token]

        # 创建审计日志
        audit_log = self._create_audit_log(
            operation_id=token_data["operation_id"],
            operation=token_data["operation"],
            user_id=user_id,
            user_level=token_data["user_level"],
            risk_level=self._get_operation_risk(token_data["operation"]),
            success=True,
            message="Operation confirmed and executed",
        )

        return OperationResult(
            success=True,
            allowed=True,
            operation_id=token_data["operation_id"],
            message="Operation confirmed and executed",
            risk_level=self._get_operation_risk(token_data["operation"]),
            audit_log=audit_log,
        )

    def get_audit_logs(
        self,
        user_id: Optional[str] = None,
        operation: Optional[str] = None,
        limit: int = 100,
    ) -> list[dict[str, Any]]:
        """
        获取审计日志

        Args:
            user_id: 用户ID（可选）
            operation: 操作类型（可选）
            limit: 返回数量限制

        Returns:
            审计日志列表
        """
        logs = self.audit_logs

        if user_id:
            logs = [log for log in logs if log.user_id == user_id]

        if operation:
            logs = [log for log in logs if log.operation == operation]

        return [log.to_dict() for log in logs[-limit:]]

    def _is_operation_allowed(self, operation: str) -> bool:
        """检查操作是否在白名单中"""
        return operation in {op.value for op in OperationType}

    def _has_permission(self, user_level: str, operation: str) -> bool:
        """检查用户是否有权限执行操作"""
        allowed_ops = self.PERMISSION_OPERATION_MAP.get(user_level, set())
        return operation in allowed_ops

    def _get_operation_risk(self, operation: str) -> str:
        """获取操作的风险级别"""
        return self.OPERATION_RISK_MAP.get(operation, "critical")

    def _generate_operation_id(self) -> str:
        """生成操作ID"""
        return f"op_{uuid.uuid4().hex[:12]}"

    def _generate_confirmation_token(
        self,
        operation_id: str,
        operation: str,
        user_id: str,
    ) -> str:
        """生成确认令牌"""
        token = hashlib.sha256(
            f"{operation_id}{operation}{user_id}{uuid.uuid4()}".encode()
        ).hexdigest()[:32]

        self.confirmation_tokens[token] = {
            "operation_id": operation_id,
            "operation": operation,
            "user_id": user_id,
            "created_at": datetime.now().isoformat(),
        }

        return token

    def _create_result(
        self,
        success: bool,
        allowed: bool,
        operation_id: str,
        message: str,
        requires_confirmation: bool = False,
        confirmation_token: Optional[str] = None,
        user_level: Optional[str] = None,
        operation: Optional[str] = None,
        risk_level: Optional[str] = None,
        audit_log: Optional[AuditLog] = None,
    ) -> OperationResult:
        """创建操作结果"""
        result = OperationResult(
            success=success,
            allowed=allowed,
            operation_id=operation_id,
            message=message,
            requires_confirmation=requires_confirmation,
            confirmation_token=confirmation_token,
            risk_level=risk_level,
            audit_log=audit_log,
        )

        # 如果有审计日志且启用审计，记录日志
        if audit_log and self.enable_audit:
            self._record_audit_log(audit_log)

        return result

    def _create_audit_log(
        self,
        operation_id: str,
        operation: str,
        user_id: str,
        user_level: str,
        risk_level: str,
        success: bool,
        message: str,
        params: Optional[dict] = None,
    ) -> AuditLog:
        """创建审计日志"""
        return AuditLog(
            operation_id=operation_id,
            operation=operation,
            user_id=user_id,
            user_level=user_level,
            risk_level=risk_level,
            ip_address=None,
            user_agent=None,
            success=success,
            message=message,
            params=params,
        )

    def _record_audit_log(self, audit_log: AuditLog) -> None:
        """记录审计日志"""
        self.audit_logs.append(audit_log)

        # 保持日志数量在限制内
        if len(self.audit_logs) > self.max_audit_logs:
            self.audit_logs = self.audit_logs[-self.max_audit_logs:]

        # 保存到文件
        self._save_audit_log(audit_log)

    def _save_audit_log(self, audit_log: AuditLog) -> None:
        """保存审计日志到文件"""
        try:
            log_file = Path(self.storage_path) / "audit_logs.jsonl"
            with open(log_file, "a", encoding="utf-8") as f:
                f.write(json.dumps(audit_log.to_dict(), ensure_ascii=False) + "\n")
        except Exception:
            # 静默处理文件写入错误
            pass


def create_intent_safety_manager(
    storage_path: Optional[str] = None,
    enable_audit: bool = True,
) -> IntentSafetyManager:
    """
    创建意图安全管理器实例

    Args:
        storage_path: 审计日志存储路径
        enable_audit: 是否启用审计日志

    Returns:
        IntentSafetyManager实例
    """
    return IntentSafetyManager(
        storage_path=storage_path,
        enable_audit=enable_audit,
    )


if __name__ == "__main__":
    # 演示用法
    print("=" * 60)
    print("意图安全管理器演示")
    print("=" * 60)

    # 创建管理器
    manager = IntentSafetyManager(storage_path="./privacy_data")

    # 测试1：Guest 读取内存（应允许）
    print("\n【测试1】Guest 读取内存")
    result = manager.check_operation(
        operation="read_memory",
        user_level="guest",
        user_id="test_user",
    )
    print(f"   结果: {result.to_dict()}")

    # 测试2：Guest 删除内存（应拒绝）
    print("\n【测试2】Guest 删除内存")
    result = manager.check_operation(
        operation="delete_memory",
        user_level="guest",
        user_id="test_user",
    )
    print(f"   结果: {result.to_dict()}")

    # 测试3：Admin 删除内存（应需要确认）
    print("\n【测试3】Admin 删除内存")
    result = manager.check_operation(
        operation="delete_memory",
        user_level="admin",
        user_id="admin_user",
    )
    print(f"   结果: {result.to_dict()}")

    # 测试4：确认操作
    if result.requires_confirmation and result.confirmation_token:
        print(f"\n【测试4】确认操作")
        print(f"   确认令牌: {result.confirmation_token[:16]}...")
        confirm_result = manager.confirm_operation(
            confirmation_token=result.confirmation_token,
            user_id="admin_user",
        )
        print(f"   确认结果: {confirm_result.to_dict()}")

    # 测试5：User 写入内存（应允许）
    print("\n【测试5】User 写入内存")
    result = manager.check_operation(
        operation="write_memory",
        user_level="user",
        user_id="test_user",
    )
    print(f"   结果: {result.to_dict()}")

    print("\n" + "=" * 60)
    print("演示完成")
    print("=" * 60)
