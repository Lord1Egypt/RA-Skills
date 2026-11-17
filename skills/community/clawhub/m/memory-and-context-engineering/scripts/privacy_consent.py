"""
隐私同意增强模块

提供不可篡改的隐私同意记录、数据删除权和同意版本管理

Copyright (c) 2024 Agent Memory System
SPDX-License-Identifier: GPL-3.0-or-later
"""

import hashlib
import json
import os
import time
import uuid
import secrets
import warnings
from datetime import datetime
from typing import Optional
from dataclasses import dataclass, field, asdict
from enum import Enum

try:
    from typing import Self
except ImportError:
    Self = None


class ConsentType(Enum):
    """同意类型"""
    MEMORY_STORAGE = "memory_storage"  # 记忆存储
    DATA_COLLECTION = "data_collection"  # 数据收集
    ANALYTICS = "analytics"  # 分析
    MARKETING = "marketing"  # 营销
    THIRD_PARTY_SHARING = "third_party_sharing"  # 第三方分享
    CUSTOM = "custom"  # 自定义


class ConsentStatus(Enum):
    """同意状态"""
    NOT_REQUESTED = "not_requested"
    PENDING = "pending"
    GRANTED = "granted"
    DENIED = "denied"
    WITHDRAWN = "withdrawn"
    EXPIRED = "expired"


@dataclass
class ConsentRecord:
    """
    同意记录

    使用哈希链确保记录不可篡改
    """
    record_id: str
    user_id: str
    consent_type: str
    version: str
    status: str
    granted_at: str
    ip_address_hash: str = ""  # 哈希存储 IP 地址
    user_agent: str = ""
    expires_at: Optional[str] = None
    previous_hash: str = ""
    integrity_hash: str = ""
    metadata: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        """转换为字典"""
        return asdict(self)

    @staticmethod
    def compute_hash(data: dict) -> str:
        """
        计算数据的哈希值

        Args:
            data: 数据字典

        Returns:
            str: SHA-256 哈希值
        """
        # 按键排序确保一致性
        json_str = json.dumps(data, sort_keys=True, ensure_ascii=False)
        return hashlib.sha256(json_str.encode()).hexdigest()


@dataclass
class ConsentValidationResult:
    """同意验证结果"""
    valid: bool
    record: Optional[ConsentRecord] = None
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)


class PrivacyConsent:
    """
    增强的隐私同意管理器

    特性：
    1. 同意记录不可篡改（使用哈希链）
    2. 同意版本管理
    3. 数据删除权（GDPR）
    4. 审计日志
    5. IP 地址哈希存储（保护隐私）
    """

    # 同意类型描述
    CONSENT_DESCRIPTIONS: dict[str, str] = {
        "memory_storage": "是否允许存储交互记忆以提供更好的服务？",
        "data_collection": "是否允许收集使用数据以改进产品？",
        "analytics": "是否允许分析您的数据以提供个性化体验？",
        "marketing": "是否允许向您发送营销信息？",
        "third_party_sharing": "是否允许与第三方分享您的数据？",
    }

    def __init__(
        self,
        storage_path: str = "./privacy_data",
        enable_hash_chain: bool = True,
        default_consent_version: str = "1.0",
        max_consent_age_days: int = 365,
    ):
        """
        初始化隐私同意管理器

        Args:
            storage_path: 存储路径
            enable_hash_chain: 是否启用哈希链
            default_consent_version: 默认同意版本
            max_consent_age_days: 最大同意有效期（天）
        """
        self.storage_path = storage_path
        self.enable_hash_chain = enable_hash_chain
        self.default_consent_version = default_consent_version
        self.max_consent_age_days = max_consent_age_days

        # 内存缓存
        self._consent_cache: dict[str, ConsentRecord] = {}
        self._hash_chain: list[str] = []

        # 确保存储目录存在
        os.makedirs(storage_path, exist_ok=True)

        # 加载现有记录
        self._load_records()

    def grant_consent(
        self,
        user_id: str,
        consent_type: str,
        ip_address: str = "",
        user_agent: str = "",
        version: Optional[str] = None,
        expires_in_days: Optional[int] = None,
        metadata: Optional[dict] = None,
    ) -> ConsentRecord:
        """
        授予用户同意

        Args:
            user_id: 用户 ID
            consent_type: 同意类型
            ip_address: IP 地址
            user_agent: 用户代理
            version: 同意版本
            expires_in_days: 过期天数
            metadata: 元数据

        Returns:
            ConsentRecord: 同意记录
        """
        now = datetime.now()
        record_id = f"consent_{uuid.uuid4().hex[:12]}"

        # 计算过期时间
        if expires_in_days is None:
            expires_in_days = self.max_consent_age_days
        expires_at = None
        if expires_in_days > 0:
            from datetime import timedelta
            expires_at = (now + timedelta(days=expires_in_days)).isoformat()

        # 哈希 IP 地址
        ip_hash = self._hash_ip(ip_address) if ip_address else ""

        # 创建记录
        record = ConsentRecord(
            record_id=record_id,
            user_id=user_id,
            consent_type=consent_type,
            version=version or self.default_consent_version,
            status=ConsentStatus.GRANTED.value,
            granted_at=now.isoformat(),
            ip_address_hash=ip_hash,
            user_agent=user_agent,
            expires_at=expires_at,
            metadata=metadata or {},
        )

        # 计算哈希链
        if self.enable_hash_chain:
            record.previous_hash = self._hash_chain[-1] if self._hash_chain else "genesis"
            record.integrity_hash = self._compute_integrity_hash(record)
            self._hash_chain.append(record.integrity_hash)

        # 保存记录
        self._save_record(record)
        self._consent_cache[self._get_cache_key(user_id, consent_type)] = record

        return record

    def withdraw_consent(
        self,
        user_id: str,
        consent_type: str,
        reason: str = "",
    ) -> ConsentRecord:
        """
        撤回同意

        Args:
            user_id: 用户 ID
            consent_type: 同意类型
            reason: 撤回原因

        Returns:
            ConsentRecord: 更新后的记录
        """
        # 获取现有记录
        existing = self.get_consent_record(user_id, consent_type)
        if not existing:
            raise ValueError(f"Consent not found for user {user_id}, type {consent_type}")

        if existing.status == ConsentStatus.WITHDRAWN.value:
            raise ValueError("Consent already withdrawn")

        # 创建撤回记录
        now = datetime.now()
        existing.status = ConsentStatus.WITHDRAWN.value
        existing.metadata["withdrawn_at"] = now.isoformat()
        existing.metadata["withdraw_reason"] = reason

        # 重新计算哈希
        if self.enable_hash_chain:
            existing.previous_hash = self._hash_chain[-1] if self._hash_chain else "genesis"
            existing.integrity_hash = self._compute_integrity_hash(existing)
            self._hash_chain.append(existing.integrity_hash)

        # 保存
        self._save_record(existing)
        self._consent_cache[self._get_cache_key(user_id, consent_type)] = existing

        return existing

    def verify_consent(
        self,
        user_id: str,
        consent_type: str,
    ) -> ConsentValidationResult:
        """
        验证用户同意是否有效

        Args:
            user_id: 用户 ID
            consent_type: 同意类型

        Returns:
            ConsentValidationResult: 验证结果
        """
        errors: list[str] = []
        warnings_list: list[str] = []

        # 获取记录
        record = self.get_consent_record(user_id, consent_type)
        if not record:
            errors.append("Consent record not found")
            return ConsentValidationResult(valid=False, errors=errors)

        # 检查哈希完整性
        if self.enable_hash_chain:
            if not self._verify_integrity(record):
                errors.append("Consent record integrity check failed - possible tampering")
                return ConsentValidationResult(
                    valid=False,
                    record=record,
                    errors=errors,
                )

        # 检查状态
        if record.status != ConsentStatus.GRANTED.value:
            errors.append(f"Consent status is {record.status}, not granted")

        # 检查过期
        if record.expires_at:
            expires_at = datetime.fromisoformat(record.expires_at)
            if expires_at < datetime.now():
                warnings_list.append("Consent has expired")
                # 过期不一定无效，取决于业务需求

        # 检查版本
        if record.version != self.default_consent_version:
            warnings_list.append(f"Consent version {record.version} differs from current {self.default_consent_version}")

        valid = len(errors) == 0
        return ConsentValidationResult(
            valid=valid,
            record=record,
            errors=errors,
            warnings=warnings_list,
        )

    def get_consent_record(
        self,
        user_id: str,
        consent_type: str,
    ) -> Optional[ConsentRecord]:
        """
        获取同意记录

        Args:
            user_id: 用户 ID
            consent_type: 同意类型

        Returns:
            Optional[ConsentRecord]: 同意记录
        """
        cache_key = self._get_cache_key(user_id, consent_type)

        # 先检查缓存
        if cache_key in self._consent_cache:
            return self._consent_cache[cache_key]

        # 从文件加载
        file_path = self._get_file_path(user_id, consent_type)
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                record = ConsentRecord(**data)
                self._consent_cache[cache_key] = record
                return record

        return None

    def has_valid_consent(
        self,
        user_id: str,
        consent_type: str,
    ) -> bool:
        """
        检查用户是否有有效的同意

        Args:
            user_id: 用户 ID
            consent_type: 同意类型

        Returns:
            bool: 是否有有效同意
        """
        result = self.verify_consent(user_id, consent_type)
        return result.valid

    def delete_user_data(
        self,
        user_id: str,
        consent_type: Optional[str] = None,
        reason: str = "",
    ) -> dict[str, bool]:
        """
        删除用户数据（GDPR 数据删除权）

        Args:
            user_id: 用户 ID
            consent_type: 同意类型（None 表示全部）
            reason: 删除原因

        Returns:
            dict: 删除结果
        """
        results = {}

        if consent_type:
            # 删除特定类型
            file_path = self._get_file_path(user_id, consent_type)
            if os.path.exists(file_path):
                os.remove(file_path)
                results[consent_type] = True

                # 清除缓存
                cache_key = self._get_cache_key(user_id, consent_type)
                if cache_key in self._consent_cache:
                    del self._consent_cache[cache_key]
            else:
                results[consent_type] = False
        else:
            # 删除所有数据
            for consent_type_enum in ConsentType:
                file_path = self._get_file_path(user_id, consent_type_enum.value)
                if os.path.exists(file_path):
                    os.remove(file_path)
                    results[consent_type_enum.value] = True

                    cache_key = self._get_cache_key(user_id, consent_type_enum.value)
                    if cache_key in self._consent_cache:
                        del self._consent_cache[cache_key]
                else:
                    results[consent_type_enum.value] = False

        # 记录删除操作
        self._log_deletion(user_id, results, reason)

        return results

    def _hash_ip(self, ip_address: str) -> str:
        """
        哈希 IP 地址

        Args:
            ip_address: 原始 IP 地址

        Returns:
            str: 哈希值
        """
        # 添加盐值
        salt = secrets.token_hex(16)
        salted = f"{salt}:{ip_address}"
        return hashlib.sha256(salted.encode()).hexdigest() + f":{salt}"

    def _compute_integrity_hash(self, record: ConsentRecord) -> str:
        """
        计算记录的完整性哈希

        Args:
            record: 同意记录

        Returns:
            str: 完整性哈希
        """
        data = {
            "record_id": record.record_id,
            "user_id": record.user_id,
            "consent_type": record.consent_type,
            "version": record.version,
            "status": record.status,
            "granted_at": record.granted_at,
            "ip_address_hash": record.ip_address_hash,
            "expires_at": record.expires_at,
            "previous_hash": record.previous_hash,
        }
        return ConsentRecord.compute_hash(data)

    def _verify_integrity(self, record: ConsentRecord) -> bool:
        """
        验证记录完整性

        Args:
            record: 同意记录

        Returns:
            bool: 是否完整
        """
        expected_hash = self._compute_integrity_hash(record)
        return expected_hash == record.integrity_hash

    def _get_cache_key(self, user_id: str, consent_type: str) -> str:
        """获取缓存键"""
        return f"{user_id}:{consent_type}"

    def _get_file_path(self, user_id: str, consent_type: str) -> str:
        """获取文件路径"""
        return os.path.join(self.storage_path, f"{user_id}_{consent_type}.json")

    def _save_record(self, record: ConsentRecord) -> None:
        """保存记录到文件"""
        file_path = self._get_file_path(record.user_id, record.consent_type)
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(record.to_dict(), f, indent=2, ensure_ascii=False)

    def _load_records(self) -> None:
        """加载所有记录"""
        if not os.path.exists(self.storage_path):
            return

        for filename in os.listdir(self.storage_path):
            if filename.endswith('.json'):
                file_path = os.path.join(self.storage_path, filename)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        record = ConsentRecord(**data)
                        cache_key = self._get_cache_key(record.user_id, record.consent_type)
                        self._consent_cache[cache_key] = record

                        # 重建哈希链
                        if self.enable_hash_chain and record.integrity_hash:
                            self._hash_chain.append(record.integrity_hash)
                except Exception:
                    pass

    def _log_deletion(
        self,
        user_id: str,
        results: dict[str, bool],
        reason: str,
    ) -> None:
        """记录删除操作"""
        log_file = os.path.join(self.storage_path, "deletion_log.txt")
        timestamp = datetime.now().isoformat()
        log_entry = f"[{timestamp}] User: {user_id}, Reason: {reason}, Results: {results}\n"

        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(log_entry)


if __name__ == "__main__":
    print("=== PrivacyConsent 测试 ===\n")

    # 创建实例
    consent = PrivacyConsent(
        storage_path="./test_privacy_data",
        enable_hash_chain=True,
    )

    # 测试1：授予同意
    print("测试 1: 授予同意")
    record = consent.grant_consent(
        user_id="user_001",
        consent_type="memory_storage",
        ip_address="192.168.1.1",
        user_agent="Mozilla/5.0",
    )
    print(f"  记录 ID: {record.record_id}")
    print(f"  状态: {record.status}")
    print(f"  完整性哈希: {record.integrity_hash[:20]}...")
    print()

    # 测试2：验证同意
    print("测试 2: 验证同意")
    result = consent.verify_consent("user_001", "memory_storage")
    print(f"  有效: {result.valid}")
    print(f"  错误: {result.errors}")
    print()

    # 测试3：检查有效同意
    print("测试 3: 检查有效同意")
    has_consent = consent.has_valid_consent("user_001", "memory_storage")
    print(f"  有有效同意: {has_consent}")
    print()

    # 测试4：撤回同意
    print("测试 4: 撤回同意")
    withdrawn = consent.withdraw_consent("user_001", "memory_storage", reason="用户请求")
    print(f"  状态: {withdrawn.status}")
    print()

    # 测试5：删除用户数据
    print("测试 5: 删除用户数据")
    results = consent.delete_user_data("user_001", consent_type="memory_storage", reason="GDPR 请求")
    print(f"  删除结果: {results}")
    print()

    # 测试6：验证撤回后的同意
    print("测试 6: 验证撤回后的同意")
    result = consent.verify_consent("user_001", "memory_storage")
    print(f"  有效: {result.valid}")
    print(f"  错误: {result.errors}")
    print()

    print("=== 测试完成 ===")
