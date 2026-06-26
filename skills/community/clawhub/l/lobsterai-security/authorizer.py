"""
RBAC 授权器 - 基于角色的访问控制
不修改 LobsterAI 主程序，提供独立的技能权限检查

设计原则：
- 最小权限原则
- 职责分离（管理员、审计员、普通用户）
- 所有授权决策记录到审计日志
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Set, Optional, Any
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from audit_logger import audit_logger


class RBACAuthorizer:
    """基于角色的访问控制授权器"""

    # 预定义角色
    ROLES = {
        'admin': {
            'description': '管理员 - 所有权限',
            'permissions': ['execute:*', 'read:*', 'write:*', 'delete:*', 'manage:users']
        },
        'auditor': {
            'description': '审计员 - 只读权限 + 审计日志访问',
            'permissions': ['read:*', 'audit:read', 'execute:readonly']
        },
        'operator': {
            'description': '操作员 - 可执行白名单技能',
            'permissions': ['execute:whitelist']
        },
        'user': {
            'description': '普通用户 - 受限权限',
            'permissions': ['execute:public']
        }
    }

    def __init__(self, config_path: Optional[str] = None):
        """
        初始化授权器

        Args:
            config_path: 配置文件路径，默认使用 LOBSTERAI_HOME 下的配置
        """
        self.lobsterai_home = os.getenv('LOBSTERAI_HOME', os.path.expanduser('~/.lobsterai'))
        self.config_path = config_path or os.path.join(self.lobsterai_home, 'security', 'rbac_config.json')

        # 加载配置
        self.role_assignments: Dict[str, Dict[str, Any]] = {}  # user_id -> {roles: [], restrictions: {}}
        self.skill_permissions: Dict[str, List[str]] = {}  # skill_id -> [allowed_roles, ...]
        self.whitelist_skills: Set[str] = set()  # operator 角色可执行的技能白名单
        self.public_skills: Set[str] = set()  # user 角色可执行的技能公开列表

        self._load_config()

    def _load_config(self):
        """加载 RBAC 配置文件"""
        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    config = json.load(f)

                self.role_assignments = config.get('role_assignments', {})
                self.skill_permissions = config.get('skill_permissions', {})
                self.whitelist_skills = set(config.get('whitelist_skills', []))
                self.public_skills = set(config.get('public_skills', []))

                audit_logger.log_event(
                    event_type='rbac_config_loaded',
                    details={'config_path': self.config_path, 'users': len(self.role_assignments)}
                )
            else:
                # 默认配置：所有技能公开
                audit_logger.log_event(
                    event_type='rbac_config_missing',
                    details={'config_path': self.config_path},
                    level='warning'
                )
        except Exception as e:
            audit_logger.log_event(
                event_type='rbac_config_error',
                details={'error': str(e)},
                level='error'
            )
            raise

    def get_user_roles(self, user_id: str) -> List[str]:
        """获取用户的角色列表"""
        return self.role_assignments.get(user_id, {}).get('roles', ['user'])

    def has_permission(self, user_id: str, skill_id: str, action: str = 'execute') -> bool:
        """
        检查用户是否有权限执行某个技能

        Args:
            user_id: 用户标识（来自会话）
            skill_id: 技能ID
            action: 操作类型（execute, read, write 等）

        Returns:
            bool: 是否允许
        """
        roles = self.get_user_roles(user_id)
        permissions_needed = []

        # 收集所需权限
        for role in roles:
            role_perms = self.ROLES.get(role, {}).get('permissions', [])
            permissions_needed.extend(role_perms)

        # 检查通配符权限
        for perm in permissions_needed:
            if perm == '*':
                return True
            if perm == 'execute:*':
                return True
            if perm == f'{action}:*':
                return True

            # 检查特定技能权限
            if perm == f'execute:{skill_id}':
                return True

        # 检查技能白名单
        if action == 'execute':
            if 'execute:whitelist' in permissions_needed:
                return skill_id in self.whitelist_skills
            if 'execute:public' in permissions_needed:
                return skill_id in self.public_skills

        # 检查技能配置中的角色限制
        allowed_roles = self.skill_permissions.get(skill_id, [])
        if allowed_roles:
            # 如果技能配置了允许的角色，检查用户是否在其中
            if not any(role in allowed_roles for role in roles):
                audit_logger.log_event(
                    event_type='authorization_denied',
                    user_id=user_id,
                    skill_id=skill_id,
                    details={'reason': 'role not in skill allowed list', 'user_roles': roles},
                    level='warning'
                )
                return False
            return True

        # 默认拒绝（最小权限原则）
        audit_logger.log_event(
            event_type='authorization_denied',
            user_id=user_id,
            skill_id=skill_id,
            details={'reason': 'no matching permission', 'user_roles': roles},
            level='warning'
        )
        return False

    def can_execute(self, user_id: str, skill_id: str, context: Optional[Dict[str, Any]] = None) -> bool:
        """
        检查用户是否有权限执行技能（便捷方法）

        Args:
            user_id: 用户标识
            skill_id: 技能ID
            context: 额外上下文（如资源ID、时间等）

        Returns:
            bool: 是否允许
        """
        # 记录授权检查
        audit_logger.log_event(
            event_type='authorization_check',
            user_id=user_id,
            skill_id=skill_id,
            details={'context': context or {}}
        )

        allowed = self.has_permission(user_id, skill_id, 'execute')

        # 记录授权结果
        audit_logger.log_event(
            event_type='authorization_result',
            user_id=user_id,
            skill_id=skill_id,
            details={'allowed': allowed, 'context': context or {}}
        )

        return allowed

    def list_user_permissions(self, user_id: str) -> Dict[str, List[str]]:
        """
        列出用户的所有权限（用于调试/审计）

        Returns:
            dict: {role: [permissions]} 格式
        """
        roles = self.get_user_roles(user_id)
        permissions = {}

        for role in roles:
            permissions[role] = self.ROLES.get(role, {}).get('permissions', [])

        return permissions

    def reload_config(self):
        """重新加载配置（用于热更新）"""
        self._load_config()
        audit_logger.log_event(
            event_type='rbac_config_reloaded',
            details={'config_path': self.config_path}
        )


# 全局授权器实例（单例）
_global_authorizer: Optional[RBACAuthorizer] = None


def get_authorizer() -> RBACAuthorizer:
    """获取全局授权器实例"""
    global _global_authorizer
    if _global_authorizer is None:
        _global_authorizer = RBACAuthorizer()
    return _global_authorizer


def can_execute_skill(user_id: str, skill_id: str, context: Optional[Dict[str, Any]] = None) -> bool:
    """
    便捷函数：检查用户是否有权限执行技能

    使用示例：
        from security.authorizer import can_execute_skill

        if can_execute_skill('user_123', 'web-search'):
            # 执行技能
            pass
    """
    return get_authorizer().can_execute(user_id, skill_id, context)
