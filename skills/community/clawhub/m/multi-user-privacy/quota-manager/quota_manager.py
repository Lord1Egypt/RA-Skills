#!/usr/bin/env python3
"""
高级配额管理系统 (Advanced Quota Management System)

功能：
1. 按用户类型设置配额（VIP/普通）
2. 配额继承（组配额）
3. 配额借用（临时增加）
4. 配额报表（导出 CSV）
5. 配额审计日志
"""

import json
import os
import csv
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field, asdict
from pathlib import Path
import threading


@dataclass
class QuotaConfig:
    """配额配置"""
    disk_quota_mb: int = 100  # 磁盘配额 (MB)
    token_quota: int = 100000  # Token 配额
    message_quota: int = 1000  # 消息配额
    session_timeout_hours: int = 24  # 会话超时 (小时)
    api_calls_per_hour: int = 100  # 每小时 API 调用次数
    storage_files_max: int = 50  # 最大文件数


@dataclass
class UserQuota:
    """用户配额实例"""
    user_id: str
    user_type: str = "normal"  # normal, vip, admin
    group_id: Optional[str] = None
    quota: QuotaConfig = field(default_factory=QuotaConfig)
    used: Dict[str, int] = field(default_factory=lambda: {
        "disk_mb": 0,
        "tokens": 0,
        "messages": 0,
        "api_calls": 0,
        "files": 0
    })
    borrowed_quota: Dict[str, int] = field(default_factory=lambda: {
        "disk_mb": 0,
        "tokens": 0,
        "messages": 0,
        "api_calls": 0,
        "files": 0
    })
    borrow_expires_at: Optional[str] = None
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now().isoformat())


@dataclass
class GroupQuota:
    """组配额配置"""
    group_id: str
    group_name: str
    quota: QuotaConfig = field(default_factory=QuotaConfig)
    member_ids: List[str] = field(default_factory=list)
    inherit_to_members: bool = True  # 是否继承给组成员
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())


@dataclass
class BorrowRecord:
    """配额借用记录"""
    record_id: str
    user_id: str
    quota_type: str  # disk_mb, tokens, messages, api_calls, files
    amount: int
    granted_at: str
    expires_at: str
    used: int = 0
    status: str = "active"  # active, expired, returned
    approved_by: str = "system"


class QuotaManager:
    """配额管理器"""
    
    # 预定义的配额模板
    QUOTA_TEMPLATES = {
        "normal": QuotaConfig(
            disk_quota_mb=100,
            token_quota=100000,
            message_quota=1000,
            session_timeout_hours=24,
            api_calls_per_hour=100,
            storage_files_max=50
        ),
        "vip": QuotaConfig(
            disk_quota_mb=1000,
            token_quota=1000000,
            message_quota=10000,
            session_timeout_hours=168,  # 7 天
            api_calls_per_hour=1000,
            storage_files_max=500
        ),
        "admin": QuotaConfig(
            disk_quota_mb=10000,
            token_quota=10000000,
            message_quota=100000,
            session_timeout_hours=720,  # 30 天
            api_calls_per_hour=10000,
            storage_files_max=5000
        )
    }
    
    def __init__(self, config_path: str = None):
        self.config_path = config_path or os.path.join(
            os.path.dirname(__file__), 
            "quota_config.json"
        )
        self.lock = threading.RLock()
        
        # 数据缓存
        self.users: Dict[str, UserQuota] = {}
        self.groups: Dict[str, GroupQuota] = {}
        self.borrow_records: Dict[str, BorrowRecord] = {}
        
        # 加载数据
        self._load_data()
    
    def _load_data(self):
        """加载持久化数据"""
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                # 加载用户配额
                for user_data in data.get("users", []):
                    user_quota = UserQuota(
                        user_id=user_data["user_id"],
                        user_type=user_data.get("user_type", "normal"),
                        group_id=user_data.get("group_id"),
                        quota=QuotaConfig(**user_data.get("quota", {})),
                        used=user_data.get("used", {}),
                        borrowed_quota=user_data.get("borrowed_quota", {}),
                        borrow_expires_at=user_data.get("borrow_expires_at"),
                        created_at=user_data.get("created_at", datetime.now().isoformat()),
                        updated_at=user_data.get("updated_at", datetime.now().isoformat())
                    )
                    self.users[user_quota.user_id] = user_quota
                
                # 加载组配额
                for group_data in data.get("groups", []):
                    group_quota = GroupQuota(
                        group_id=group_data["group_id"],
                        group_name=group_data["group_name"],
                        quota=QuotaConfig(**group_data.get("quota", {})),
                        member_ids=group_data.get("member_ids", []),
                        inherit_to_members=group_data.get("inherit_to_members", True),
                        created_at=group_data.get("created_at", datetime.now().isoformat())
                    )
                    self.groups[group_quota.group_id] = group_quota
                
                # 加载借用记录
                for record_data in data.get("borrow_records", []):
                    record = BorrowRecord(
                        record_id=record_data["record_id"],
                        user_id=record_data["user_id"],
                        quota_type=record_data["quota_type"],
                        amount=record_data["amount"],
                        granted_at=record_data["granted_at"],
                        expires_at=record_data["expires_at"],
                        used=record_data.get("used", 0),
                        status=record_data.get("status", "active"),
                        approved_by=record_data.get("approved_by", "system")
                    )
                    self.borrow_records[record.record_id] = record
                    
            except Exception as e:
                print(f"加载配额配置失败：{e}")
                self._init_default_data()
        else:
            self._init_default_data()
    
    def _init_default_data(self):
        """初始化默认数据"""
        # 创建默认管理员组
        self.create_group(
            group_id="admin_group",
            group_name="管理员组",
            quota=self.QUOTA_TEMPLATES["admin"],
            inherit_to_members=True
        )
        
        # 创建默认 VIP 组
        self.create_group(
            group_id="vip_group",
            group_name="VIP 用户组",
            quota=self.QUOTA_TEMPLATES["vip"],
            inherit_to_members=True
        )
        
        self._save_data()
    
    def _save_data(self):
        """保存数据到文件"""
        with self.lock:
            data = {
                "version": "1.0",
                "updated_at": datetime.now().isoformat(),
                "users": [self._user_to_dict(u) for u in self.users.values()],
                "groups": [self._group_to_dict(g) for g in self.groups.values()],
                "borrow_records": [self._record_to_dict(r) for r in self.borrow_records.values()]
            }
            
            # 确保目录存在
            os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
            
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
    
    def _user_to_dict(self, user: UserQuota) -> dict:
        """用户配额转字典"""
        return {
            "user_id": user.user_id,
            "user_type": user.user_type,
            "group_id": user.group_id,
            "quota": asdict(user.quota),
            "used": user.used,
            "borrowed_quota": user.borrowed_quota,
            "borrow_expires_at": user.borrow_expires_at,
            "created_at": user.created_at,
            "updated_at": user.updated_at
        }
    
    def _group_to_dict(self, group: GroupQuota) -> dict:
        """组配额转字典"""
        return {
            "group_id": group.group_id,
            "group_name": group.group_name,
            "quota": asdict(group.quota),
            "member_ids": group.member_ids,
            "inherit_to_members": group.inherit_to_members,
            "created_at": group.created_at
        }
    
    def _record_to_dict(self, record: BorrowRecord) -> dict:
        """借用记录转字典"""
        return asdict(record)
    
    # ========== 用户配额管理 ==========
    
    def create_user(self, user_id: str, user_type: str = "normal", 
                    group_id: Optional[str] = None) -> UserQuota:
        """创建用户配额"""
        with self.lock:
            if user_id in self.users:
                raise ValueError(f"用户 {user_id} 已存在")
            
            # 获取配额模板
            quota_template = self.QUOTA_TEMPLATES.get(
                user_type, 
                self.QUOTA_TEMPLATES["normal"]
            )
            
            user_quota = UserQuota(
                user_id=user_id,
                user_type=user_type,
                group_id=group_id,
                quota=QuotaConfig(
                    disk_quota_mb=quota_template.disk_quota_mb,
                    token_quota=quota_template.token_quota,
                    message_quota=quota_template.message_quota,
                    session_timeout_hours=quota_template.session_timeout_hours,
                    api_calls_per_hour=quota_template.api_calls_per_hour,
                    storage_files_max=quota_template.storage_files_max
                )
            )
            
            # 如果有组且启用继承，应用组配额
            if group_id and group_id in self.groups:
                group = self.groups[group_id]
                if group.inherit_to_members:
                    user_quota.quota = QuotaConfig(
                        disk_quota_mb=group.quota.disk_quota_mb,
                        token_quota=group.quota.token_quota,
                        message_quota=group.quota.message_quota,
                        session_timeout_hours=group.quota.session_timeout_hours,
                        api_calls_per_hour=group.quota.api_calls_per_hour,
                        storage_files_max=group.quota.storage_files_max
                    )
                group.member_ids.append(user_id)
            
            self.users[user_id] = user_quota
            self._save_data()
            return user_quota
    
    def get_user_quota(self, user_id: str) -> Optional[UserQuota]:
        """获取用户配额"""
        return self.users.get(user_id)
    
    def update_user_type(self, user_id: str, user_type: str) -> UserQuota:
        """更新用户类型"""
        with self.lock:
            if user_id not in self.users:
                raise ValueError(f"用户 {user_id} 不存在")
            
            user = self.users[user_id]
            user.user_type = user_type
            user.updated_at = datetime.now().isoformat()
            
            # 应用新的配额模板
            quota_template = self.QUOTA_TEMPLATES.get(
                user_type,
                self.QUOTA_TEMPLATES["normal"]
            )
            user.quota = QuotaConfig(
                disk_quota_mb=quota_template.disk_quota_mb,
                token_quota=quota_template.token_quota,
                message_quota=quota_template.message_quota,
                session_timeout_hours=quota_template.session_timeout_hours,
                api_calls_per_hour=quota_template.api_calls_per_hour,
                storage_files_max=quota_template.storage_files_max
            )
            
            self._save_data()
            return user
    
    def delete_user(self, user_id: str):
        """删除用户配额"""
        with self.lock:
            if user_id not in self.users:
                raise ValueError(f"用户 {user_id} 不存在")
            
            # 从组中移除
            user = self.users[user_id]
            if user.group_id and user.group_id in self.groups:
                group = self.groups[user.group_id]
                if user_id in group.member_ids:
                    group.member_ids.remove(user_id)
            
            del self.users[user_id]
            self._save_data()
    
    # ========== 组配额管理 ==========
    
    def create_group(self, group_id: str, group_name: str,
                     quota: QuotaConfig = None, 
                     inherit_to_members: bool = True) -> GroupQuota:
        """创建组配额"""
        with self.lock:
            if group_id in self.groups:
                raise ValueError(f"组 {group_id} 已存在")
            
            group = GroupQuota(
                group_id=group_id,
                group_name=group_name,
                quota=quota or QuotaConfig(),
                inherit_to_members=inherit_to_members
            )
            
            self.groups[group_id] = group
            self._save_data()
            return group
    
    def add_user_to_group(self, user_id: str, group_id: str, 
                          apply_inheritance: bool = True):
        """添加用户到组"""
        with self.lock:
            if user_id not in self.users:
                raise ValueError(f"用户 {user_id} 不存在")
            if group_id not in self.groups:
                raise ValueError(f"组 {group_id} 不存在")
            
            user = self.users[user_id]
            group = self.groups[group_id]
            
            # 从原组移除
            if user.group_id and user.group_id in self.groups:
                old_group = self.groups[user.group_id]
                if user_id in old_group.member_ids:
                    old_group.member_ids.remove(user_id)
            
            # 添加到新组
            user.group_id = group_id
            if user_id not in group.member_ids:
                group.member_ids.append(user_id)
            
            # 应用组配额继承
            if apply_inheritance and group.inherit_to_members:
                user.quota = QuotaConfig(
                    disk_quota_mb=group.quota.disk_quota_mb,
                    token_quota=group.quota.token_quota,
                    message_quota=group.quota.message_quota,
                    session_timeout_hours=group.quota.session_timeout_hours,
                    api_calls_per_hour=group.quota.api_calls_per_hour,
                    storage_files_max=group.quota.storage_files_max
                )
            
            user.updated_at = datetime.now().isoformat()
            self._save_data()
    
    def remove_user_from_group(self, user_id: str, group_id: str):
        """从组中移除用户"""
        with self.lock:
            if user_id not in self.users:
                raise ValueError(f"用户 {user_id} 不存在")
            if group_id not in self.groups:
                raise ValueError(f"组 {group_id} 不存在")
            
            user = self.users[user_id]
            group = self.groups[group_id]
            
            if user.group_id != group_id:
                raise ValueError(f"用户 {user_id} 不在组 {group_id} 中")
            
            user.group_id = None
            if user_id in group.member_ids:
                group.member_ids.remove(user_id)
            
            # 恢复默认配额
            quota_template = self.QUOTA_TEMPLATES.get(
                user.user_type,
                self.QUOTA_TEMPLATES["normal"]
            )
            user.quota = QuotaConfig(
                disk_quota_mb=quota_template.disk_quota_mb,
                token_quota=quota_template.token_quota,
                message_quota=quota_template.message_quota,
                session_timeout_hours=quota_template.session_timeout_hours,
                api_calls_per_hour=quota_template.api_calls_per_hour,
                storage_files_max=quota_template.storage_files_max
            )
            
            user.updated_at = datetime.now().isoformat()
            self._save_data()
    
    # ========== 配额借用 ==========
    
    def borrow_quota(self, user_id: str, quota_type: str, amount: int,
                     duration_hours: int = 24, 
                     approved_by: str = "system") -> BorrowRecord:
        """借用配额"""
        with self.lock:
            if user_id not in self.users:
                raise ValueError(f"用户 {user_id} 不存在")
            
            valid_types = ["disk_mb", "tokens", "messages", "api_calls", "files"]
            if quota_type not in valid_types:
                raise ValueError(f"无效的配额类型：{quota_type}")
            
            user = self.users[user_id]
            record_id = f"borrow_{user_id}_{quota_type}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
            
            now = datetime.now()
            expires_at = now + timedelta(hours=duration_hours)
            
            record = BorrowRecord(
                record_id=record_id,
                user_id=user_id,
                quota_type=quota_type,
                amount=amount,
                granted_at=now.isoformat(),
                expires_at=expires_at.isoformat(),
                approved_by=approved_by
            )
            
            # 增加借用配额
            user.borrowed_quota[quota_type] = user.borrowed_quota.get(quota_type, 0) + amount
            user.borrow_expires_at = expires_at.isoformat()
            user.updated_at = now.isoformat()
            
            self.borrow_records[record_id] = record
            self._save_data()
            
            return record
    
    def return_quota(self, record_id: str):
        """归还借用配额"""
        with self.lock:
            if record_id not in self.borrow_records:
                raise ValueError(f"借用记录 {record_id} 不存在")
            
            record = self.borrow_records[record_id]
            if record.status != "active":
                raise ValueError(f"借用记录 {record_id} 状态为 {record.status}，无法归还")
            
            user = self.users.get(record.user_id)
            if user:
                quota_type = record.quota_type
                user.borrowed_quota[quota_type] = max(
                    0,
                    user.borrowed_quota.get(quota_type, 0) - record.amount
                )
                user.updated_at = datetime.now().isoformat()
            
            record.status = "returned"
            self._save_data()
    
    def check_expired_borrows(self):
        """检查并处理过期的借用"""
        with self.lock:
            now = datetime.now()
            expired_count = 0
            
            for record in self.borrow_records.values():
                if record.status == "active":
                    expires_at = datetime.fromisoformat(record.expires_at)
                    if now > expires_at:
                        record.status = "expired"
                        expired_count += 1
            
            if expired_count > 0:
                self._save_data()
            
            return expired_count
    
    # ========== 配额使用追踪 ==========
    
    def record_usage(self, user_id: str, quota_type: str, amount: int):
        """记录配额使用"""
        with self.lock:
            if user_id not in self.users:
                raise ValueError(f"用户 {user_id} 不存在")
            
            valid_types = ["disk_mb", "tokens", "messages", "api_calls", "files"]
            if quota_type not in valid_types:
                raise ValueError(f"无效的使用类型：{quota_type}")
            
            user = self.users[user_id]
            user.used[quota_type] = user.used.get(quota_type, 0) + amount
            user.updated_at = datetime.now().isoformat()
            
            self._save_data()
    
    def check_quota_available(self, user_id: str, quota_type: str, 
                               required: int) -> bool:
        """检查配额是否足够"""
        if user_id not in self.users:
            return False
        
        user = self.users[user_id]
        quota_attr = f"{quota_type}_quota" if quota_type != "disk_mb" else quota_type
        
        if not hasattr(user.quota, quota_attr):
            return False
        
        limit = getattr(user.quota, quota_attr)
        borrowed = user.borrowed_quota.get(quota_type, 0)
        used = user.used.get(quota_type, 0)
        
        total_available = limit + borrowed - used
        return total_available >= required
    
    def get_available_quota(self, user_id: str) -> Dict[str, int]:
        """获取用户可用配额"""
        if user_id not in self.users:
            return {}
        
        user = self.users[user_id]
        
        return {
            "disk_mb": user.quota.disk_quota_mb + user.borrowed_quota.get("disk_mb", 0) - user.used.get("disk_mb", 0),
            "tokens": user.quota.token_quota + user.borrowed_quota.get("tokens", 0) - user.used.get("tokens", 0),
            "messages": user.quota.message_quota + user.borrowed_quota.get("messages", 0) - user.used.get("messages", 0),
            "api_calls": user.quota.api_calls_per_hour + user.borrowed_quota.get("api_calls", 0) - user.used.get("api_calls", 0),
            "files": user.quota.storage_files_max + user.borrowed_quota.get("files", 0) - user.used.get("files", 0)
        }
    
    # ========== 报表导出 ==========
    
    def export_csv(self, output_path: str = None, report_type: str = "all") -> str:
        """导出 CSV 报表"""
        if output_path is None:
            output_path = f"quota_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        with self.lock:
            if report_type == "users":
                self._export_users_csv(output_path)
            elif report_type == "groups":
                self._export_groups_csv(output_path)
            elif report_type == "borrows":
                self._export_borrows_csv(output_path)
            else:  # all
                self._export_users_csv(output_path.replace(".csv", "_users.csv"))
                self._export_groups_csv(output_path.replace(".csv", "_groups.csv"))
                self._export_borrows_csv(output_path.replace(".csv", "_borrows.csv"))
                output_path = output_path.replace(".csv", "_users.csv")
            
            return output_path
    
    def _export_users_csv(self, output_path: str):
        """导出用户配额 CSV"""
        with open(output_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([
                "用户 ID", "用户类型", "组 ID", 
                "磁盘配额 (MB)", "已用磁盘 (MB)", "剩余磁盘 (MB)",
                "Token 配额", "已用 Token", "剩余 Token",
                "消息配额", "已用消息", "剩余消息",
                "API 调用配额", "已用 API 调用", "剩余 API 调用",
                "文件配额", "已用文件数", "剩余文件",
                "借用配额", "借用过期时间", "创建时间", "更新时间"
            ])
            
            for user in self.users.values():
                available = self.get_available_quota(user.user_id)
                writer.writerow([
                    user.user_id,
                    user.user_type,
                    user.group_id or "",
                    user.quota.disk_quota_mb,
                    user.used.get("disk_mb", 0),
                    available.get("disk_mb", 0),
                    user.quota.token_quota,
                    user.used.get("tokens", 0),
                    available.get("tokens", 0),
                    user.quota.message_quota,
                    user.used.get("messages", 0),
                    available.get("messages", 0),
                    user.quota.api_calls_per_hour,
                    user.used.get("api_calls", 0),
                    available.get("api_calls", 0),
                    user.quota.storage_files_max,
                    user.used.get("files", 0),
                    available.get("files", 0),
                    json.dumps(user.borrowed_quota, ensure_ascii=False),
                    user.borrow_expires_at or "",
                    user.created_at,
                    user.updated_at
                ])
    
    def _export_groups_csv(self, output_path: str):
        """导出组配额 CSV"""
        with open(output_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([
                "组 ID", "组名称", "成员数量", "成员列表",
                "磁盘配额 (MB)", "Token 配额", "消息配额",
                "API 调用配额", "文件配额", "继承启用", "创建时间"
            ])
            
            for group in self.groups.values():
                writer.writerow([
                    group.group_id,
                    group.group_name,
                    len(group.member_ids),
                    ";".join(group.member_ids),
                    group.quota.disk_quota_mb,
                    group.quota.token_quota,
                    group.quota.message_quota,
                    group.quota.api_calls_per_hour,
                    group.quota.storage_files_max,
                    "是" if group.inherit_to_members else "否",
                    group.created_at
                ])
    
    def _export_borrows_csv(self, output_path: str):
        """导出借用记录 CSV"""
        with open(output_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([
                "记录 ID", "用户 ID", "配额类型", "借用数量",
                "批准人", "借用时间", "过期时间", "已用数量", "状态"
            ])
            
            for record in self.borrow_records.values():
                writer.writerow([
                    record.record_id,
                    record.user_id,
                    record.quota_type,
                    record.amount,
                    record.approved_by,
                    record.granted_at,
                    record.expires_at,
                    record.used,
                    record.status
                ])
    
    # ========== 查询和统计 ==========
    
    def get_all_users(self) -> List[UserQuota]:
        """获取所有用户"""
        return list(self.users.values())
    
    def get_all_groups(self) -> List[GroupQuota]:
        """获取所有组"""
        return list(self.groups.values())
    
    def get_users_by_type(self, user_type: str) -> List[UserQuota]:
        """按类型获取用户"""
        return [u for u in self.users.values() if u.user_type == user_type]
    
    def get_users_by_group(self, group_id: str) -> List[UserQuota]:
        """按组获取用户"""
        return [u for u in self.users.values() if u.group_id == group_id]
    
    def get_active_borrows(self, user_id: str = None) -> List[BorrowRecord]:
        """获取活跃借用记录"""
        records = [r for r in self.borrow_records.values() if r.status == "active"]
        if user_id:
            records = [r for r in records if r.user_id == user_id]
        return records
    
    def get_quota_summary(self) -> Dict[str, Any]:
        """获取配额汇总统计"""
        total_users = len(self.users)
        total_groups = len(self.groups)
        active_borrows = len([r for r in self.borrow_records.values() if r.status == "active"])
        
        users_by_type = {}
        for user in self.users.values():
            users_by_type[user.user_type] = users_by_type.get(user.user_type, 0) + 1
        
        total_usage = {
            "disk_mb": sum(u.used.get("disk_mb", 0) for u in self.users.values()),
            "tokens": sum(u.used.get("tokens", 0) for u in self.users.values()),
            "messages": sum(u.used.get("messages", 0) for u in self.users.values()),
            "api_calls": sum(u.used.get("api_calls", 0) for u in self.users.values()),
            "files": sum(u.used.get("files", 0) for u in self.users.values())
        }
        
        return {
            "total_users": total_users,
            "total_groups": total_groups,
            "active_borrows": active_borrows,
            "users_by_type": users_by_type,
            "total_usage": total_usage,
            "generated_at": datetime.now().isoformat()
        }


# ========== CLI 接口 ==========

def main():
    """命令行接口"""
    import argparse
    
    parser = argparse.ArgumentParser(description="高级配额管理系统")
    parser.add_argument("--config", "-c", help="配置文件路径")
    parser.add_argument("--action", "-a", required=True, 
                        choices=["create-user", "update-user", "delete-user",
                                "create-group", "add-to-group", "remove-from-group",
                                "borrow", "return", "check", "export", "summary"],
                        help="操作类型")
    parser.add_argument("--user-id", "-u", help="用户 ID")
    parser.add_argument("--group-id", "-g", help="组 ID")
    parser.add_argument("--user-type", "-t", choices=["normal", "vip", "admin"],
                        help="用户类型")
    parser.add_argument("--quota-type", help="配额类型")
    parser.add_argument("--amount", "-n", type=int, help="数量")
    parser.add_argument("--duration", "-d", type=int, default=24, 
                        help="借用时长 (小时)")
    parser.add_argument("--output", "-o", help="输出文件路径")
    parser.add_argument("--report-type", choices=["users", "groups", "borrows", "all"],
                        default="all", help="报表类型")
    
    args = parser.parse_args()
    
    manager = QuotaManager(args.config)
    
    try:
        if args.action == "create-user":
            user = manager.create_user(args.user_id, args.user_type or "normal", args.group_id)
            print(f"✓ 用户 {args.user_id} 创建成功")
            print(f"  类型：{user.user_type}")
            print(f"  组：{user.group_id or '无'}")
        
        elif args.action == "update-user":
            user = manager.update_user_type(args.user_id, args.user_type)
            print(f"✓ 用户 {args.user_id} 更新成功")
            print(f"  新类型：{user.user_type}")
        
        elif args.action == "delete-user":
            manager.delete_user(args.user_id)
            print(f"✓ 用户 {args.user_id} 删除成功")
        
        elif args.action == "create-group":
            group = manager.create_group(args.group_id, args.user_id or "默认组")
            print(f"✓ 组 {args.group_id} 创建成功")
        
        elif args.action == "add-to-group":
            manager.add_user_to_group(args.user_id, args.group_id)
            print(f"✓ 用户 {args.user_id} 已加入组 {args.group_id}")
        
        elif args.action == "remove-from-group":
            manager.remove_user_from_group(args.user_id, args.group_id)
            print(f"✓ 用户 {args.user_id} 已离开组 {args.group_id}")
        
        elif args.action == "borrow":
            record = manager.borrow_quota(
                args.user_id, 
                args.quota_type, 
                args.amount,
                args.duration
            )
            print(f"✓ 配额借用成功")
            print(f"  记录 ID: {record.record_id}")
            print(f"  类型：{record.quota_type}")
            print(f"  数量：{record.amount}")
            print(f"  过期：{record.expires_at}")
        
        elif args.action == "return":
            manager.return_quota(args.user_id)
            print(f"✓ 配额归还成功")
        
        elif args.action == "check":
            if args.user_id:
                available = manager.get_available_quota(args.user_id)
                print(f"用户 {args.user_id} 可用配额:")
                for k, v in available.items():
                    print(f"  {k}: {v}")
            else:
                summary = manager.get_quota_summary()
                print("配额汇总:")
                print(f"  总用户数：{summary['total_users']}")
                print(f"  总组数：{summary['total_groups']}")
                print(f"  活跃借用：{summary['active_borrows']}")
                print(f"  用户类型分布：{summary['users_by_type']}")
        
        elif args.action == "export":
            output = manager.export_csv(args.output, args.report_type)
            print(f"✓ 报表已导出：{output}")
        
        elif args.action == "summary":
            summary = manager.get_quota_summary()
            print(json.dumps(summary, ensure_ascii=False, indent=2))
    
    except ValueError as e:
        print(f"✗ 错误：{e}")
        exit(1)
    except Exception as e:
        print(f"✗ 系统错误：{e}")
        exit(1)


if __name__ == "__main__":
    main()
