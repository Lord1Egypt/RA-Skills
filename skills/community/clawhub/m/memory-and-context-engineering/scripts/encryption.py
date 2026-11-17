# Agent Memory System
# Copyright (C) 2024 kiwifruit
#
# This file is part of Agent Memory System.
#
# Agent Memory System is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Agent Memory System is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Agent Memory System.  If not, see <https://www.gnu.org/licenses/>.


"""
Agent Memory System - 数据加密模块

=== 依赖与环境声明 ===
- 运行环境：Python >=3.9
- 直接依赖:
  * cryptography: >=41.0.0
    - 用途：AES-256-GCM 加密算法
  * pydantic: >=2.0.0
    - 用途：数据模型验证
- 标准配置文件:
  ```text
  # requirements.txt
  pydantic>=2.0.0
  typing-extensions>=4.0.0
  cryptography>=41.0.0
  ```
=== 声明结束 ===

安全提醒：
1. 密钥应存储在安全位置（环境变量/密钥管理服务）
2. 定期轮换密钥
3. 不要在日志或错误信息中泄露密钥
"""

from __future__ import annotations

import base64
import hashlib
import json
import os
import secrets
from datetime import datetime
from pathlib import Path
from typing import Any, Optional

from pydantic import BaseModel, Field

# 延迟导入 cryptography，避免未安装时报错
try:
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM
    CRYPTO_AVAILABLE = True
except ImportError:
    CRYPTO_AVAILABLE = False
    AESGCM = None  # type: ignore


# ============================================================================
# 常量定义
# ============================================================================

# AES-256-GCM 参数
KEY_LENGTH: int = 32  # 256 bits
NONCE_LENGTH: int = 12  # 96 bits (推荐值)
TAG_LENGTH: int = 16  # 128 bits

# 密钥派生参数
KDF_ITERATIONS: int = 100_000  # PBKDF2 迭代次数
SALT_LENGTH: int = 16  # 盐值长度


# ============================================================================
# 数据模型
# ============================================================================


class EncryptedData(BaseModel):
    """加密数据容器"""

    version: str = "1.0"
    algorithm: str = "AES-256-GCM"
    nonce: str  # Base64 编码的 nonce
    ciphertext: str  # Base64 编码的密文
    salt: Optional[str] = None  # Base64 编码的盐值（密钥派生时使用）
    created_at: datetime = Field(default_factory=datetime.now)


class KeyInfo(BaseModel):
    """密钥信息（不包含实际密钥）"""

    key_id: str
    algorithm: str = "AES-256-GCM"
    created_at: datetime = Field(default_factory=datetime.now)
    is_active: bool = True


class EncryptionConfig(BaseModel):
    """加密配置"""

    enabled: bool = True
    algorithm: str = "AES-256-GCM"
    key_derivation: str = "PBKDF2"
    kdf_iterations: int = KDF_ITERATIONS
    auto_encrypt_sensitive: bool = True  # 自动加密敏感数据


# ============================================================================
# 密钥管理
# ============================================================================


class KeyStrengthResult(BaseModel):
    """密钥强度验证结果"""

    is_valid: bool
    score: int = Field(ge=0, le=100, description="强度评分 (0-100)")
    issues: list[str] = Field(default_factory=list, description="问题列表")
    suggestions: list[str] = Field(default_factory=list, description="改进建议")

    @property
    def strength_level(self) -> str:
        """获取强度等级"""
        if self.score >= 80:
            return "strong"
        elif self.score >= 60:
            return "medium"
        elif self.score >= 40:
            return "weak"
        else:
            return "very_weak"


class KeyManager:
    """
    密钥管理器

    负责密钥的生成、派生、存储和轮换
    """

    def __init__(
        self,
        user_id: str = "default_user",
        key_storage_path: str = "./keys",
    ) -> None:
        """
        初始化密钥管理器

        Args:
            user_id: 用户ID
            key_storage_path: 密钥存储路径
        """
        self.user_id: str = user_id
        self.key_storage_path: Path = Path(key_storage_path)
        self.key_storage_path.mkdir(parents=True, exist_ok=True)

        self._current_key: Optional[bytes] = None
        self._key_id: Optional[str] = None
        self._key_history: list[tuple[str, datetime]] = []  # 密钥历史

    @staticmethod
    def validate_key_strength(key: str) -> KeyStrengthResult:
        """
        验证密钥强度

        Args:
            key: 要验证的密钥

        Returns:
            KeyStrengthResult: 验证结果
        """
        issues: list[str] = []
        suggestions: list[str] = []
        score: int = 0

        # 检查长度
        length = len(key)
        if length < 16:
            issues.append(f"密钥长度过短 ({length} < 16)")
            suggestions.append("建议使用至少 16 个字符的密钥")
            score += length * 2
        elif length < 32:
            issues.append(f"密钥长度较短 ({length} < 32)")
            suggestions.append("建议使用至少 32 个字符的密钥以提高安全性")
            score += 30
        else:
            score += 40

        # 检查字符类型
        has_lower = any(c.islower() for c in key)
        has_upper = any(c.isupper() for c in key)
        has_digit = any(c.isdigit() for c in key)
        has_special = any(not c.isalnum() for c in key)

        char_types = sum([has_lower, has_upper, has_digit, has_special])
        if char_types < 3:
            issues.append(f"密钥复杂度不足 (仅 {char_types} 种字符类型)")
            suggestions.append("建议混合使用大小写字母、数字和特殊字符")
            score += char_types * 5
        else:
            score += 15

        # 检查常见模式
        common_patterns = [
            ("123456", "连续数字"),
            ("password", "常见密码"),
            ("qwerty", "键盘模式"),
            ("admin", "管理员账户名"),
        ]
        key_lower = key.lower()
        for pattern, name in common_patterns:
            if pattern in key_lower:
                issues.append(f"包含常见模式 ({name})")
                suggestions.append("避免使用常见密码或模式")
                score -= 10

        # 检查重复字符
        if len(set(key)) < length * 0.5:
            issues.append("密钥包含大量重复字符")
            suggestions.append("建议使用更多样的字符")
            score -= 10

        # 限制分数范围
        score = max(0, min(100, score))

        # 判断是否有效
        is_valid = length >= 16 and char_types >= 3 and score >= 40

        return KeyStrengthResult(
            is_valid=is_valid,
            score=score,
            issues=issues,
            suggestions=suggestions
        )

    def generate_key(self) -> tuple[str, bytes]:
        """
        生成新的加密密钥

        Returns:
            (key_id, key_bytes)
        """
        key_id: str = f"key_{secrets.token_hex(8)}"
        key_bytes: bytes = secrets.token_bytes(KEY_LENGTH)

        return key_id, key_bytes

    def set_key(self, key_id: str, key: bytes) -> None:
        """
        设置当前使用的密钥

        Args:
            key_id: 密钥ID
            key: 密钥字节
        """
        self._key_id = key_id
        self._current_key = key

    def get_key(self) -> tuple[str, bytes]:
        """
        获取当前密钥

        Returns:
            (key_id, key_bytes)

        Raises:
            ValueError: 密钥未设置
        """
        if self._current_key is None or self._key_id is None:
            raise ValueError("密钥未设置，请先调用 set_key 或从环境变量加载")

        return self._key_id, self._current_key

    def load_key_from_env(self, env_var: str) -> bool:
        """
        从环境变量加载密钥

        Args:
            env_var: 环境变量名（由调用方指定，如 "MEMORY_ENCRYPTION_KEY"）

        Returns:
            是否成功加载
        """
        key_b64: Optional[str] = os.getenv(env_var)

        if key_b64 is None:
            return False

        try:
            key: bytes = base64.b64decode(key_b64)

            if len(key) != KEY_LENGTH:
                return False

            self._key_id = f"env_{env_var}"
            self._current_key = key
            return True

        except Exception:
            return False

    def rotate_key(self) -> tuple[str, bytes]:
        """
        轮换密钥

        生成新密钥，保留旧密钥历史

        Returns:
            tuple[str, bytes]: (新密钥ID, 新密钥)

        Note:
            - 旧密钥保留在历史中用于解密历史数据
            - 建议定期轮换密钥以提高安全性
        """
        # 保存旧密钥历史
        if self._key_id and self._current_key:
            self._key_history.append((
                self._key_id,
                datetime.now()
            ))

            # 限制历史记录数量（保留最近 5 个）
            if len(self._key_history) > 5:
                self._key_history = self._key_history[-5:]

        # 生成新密钥
        new_key_id, new_key = self.generate_key()
        self._current_key = new_key
        self._key_id = new_key_id

        # 保存新密钥
        self.save_key_to_file(new_key_id, new_key)

        return new_key_id, new_key

    def get_key_history(self) -> list[dict[str, Any]]:
        """
        获取密钥历史

        Returns:
            list[dict]: 密钥历史列表
        """
        return [
            {
                "key_id": key_id,
                "rotated_at": rotated_at.isoformat()
            }
            for key_id, rotated_at in self._key_history
        ]

    @staticmethod
    def derive_key_from_password(
        password: str,
        salt: Optional[bytes] = None,
        iterations: int = 600000,
    ) -> tuple[bytes, bytes]:
        """
        使用 PBKDF2 从密码派生密钥

        Args:
            password: 用户密码
            salt: 盐值（可选，自动生成）
            iterations: PBKDF2 迭代次数（OWASP 建议 >= 600000）

        Returns:
            tuple[bytes, bytes]: (派生密钥, 盐值)

        Note:
            - 使用 SHA-256 作为哈希算法
            - 迭代次数遵循 OWASP 最新建议
        """
        from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
        from cryptography.hazmat.primitives import hashes

        # 生成或使用提供的盐
        if salt is None:
            salt = secrets.token_bytes(32)

        # PBKDF2 密钥派生
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=iterations,
        )
        key = kdf.derive(password.encode("utf-8"))

        return key, salt

    def save_key_to_file(
        self,
        key_id: str,
        key: bytes,
        password: Optional[str] = None,
    ) -> Path:
        """
        保存密钥到文件

        Args:
            key_id: 密钥ID
            key: 密钥字节
            password: 可选密码保护

        Returns:
            密钥文件路径
        """
        key_file: Path = self.key_storage_path / f"{self.user_id}_{key_id}.key"

        if password:
            # 使用密码加密密钥
            salt, encrypted_key = encrypt_data_with_password(
                key, password
            )
            data: dict[str, Any] = {
                "key_id": key_id,
                "encrypted": True,
                "salt": base64.b64encode(salt).decode("utf-8"),
                "key": base64.b64encode(encrypted_key).decode("utf-8"),
            }
        else:
            # 直接存储（不推荐）
            data = {
                "key_id": key_id,
                "encrypted": False,
                "key": base64.b64encode(key).decode("utf-8"),
            }

        # 设置文件权限
        with open(key_file, "w", encoding="utf-8") as f:
            json.dump(data, f)

        key_file.chmod(0o600)  # 仅所有者可读写

        return key_file

    def load_key_from_file(
        self,
        key_id: str,
        password: Optional[str] = None,
    ) -> Optional[bytes]:
        """
        从文件加载密钥

        Args:
            key_id: 密钥ID
            password: 密码（如果密钥被加密）

        Returns:
            密钥字节，失败返回 None
        """
        key_file: Path = self.key_storage_path / f"{self.user_id}_{key_id}.key"

        if not key_file.exists():
            return None

        try:
            with open(key_file, "r", encoding="utf-8") as f:
                data: dict[str, Any] = json.load(f)

            key_b64: str = data["key"]

            if data.get("encrypted"):
                if password is None:
                    raise ValueError("密钥已加密，需要提供密码")

                salt: bytes = base64.b64decode(data["salt"])
                encrypted_key: bytes = base64.b64decode(key_b64)

                key: bytes = decrypt_data_with_password(
                    encrypted_key, password, salt
                )
            else:
                key = base64.b64decode(key_b64)

            self._key_id = key_id
            self._current_key = key
            return key

        except Exception:
            return None


# ============================================================================
# 加密器
# ============================================================================


class DataEncryptor:
    """
    数据加密器

    提供 AES-256-GCM 加密/解密功能
    """

    def __init__(
        self,
        key_manager: Optional[KeyManager] = None,
        config: Optional[EncryptionConfig] = None,
    ) -> None:
        """
        初始化加密器

        Args:
            key_manager: 密钥管理器
            config: 加密配置
        """
        self.key_manager: KeyManager = key_manager or KeyManager()
        self.config: EncryptionConfig = config or EncryptionConfig()

        # 检查加密库是否可用
        if self.config.enabled and not CRYPTO_AVAILABLE:
            raise ImportError(
                "加密功能需要 cryptography 库。"
                "请运行: pip install cryptography>=41.0.0"
            )

    def encrypt(
        self,
        plaintext: bytes | str | dict[str, Any],
    ) -> EncryptedData:
        """
        加密数据

        Args:
            plaintext: 明文数据（字节、字符串或字典）

        Returns:
            加密数据容器

        Raises:
            ValueError: 密钥未设置
        """
        if not self.config.enabled:
            raise ValueError("加密功能已禁用")

        # 获取密钥
        key_id, key = self.key_manager.get_key()

        # 准备明文
        if isinstance(plaintext, dict):
            plaintext_bytes: bytes = json.dumps(
                plaintext, ensure_ascii=False
            ).encode("utf-8")
        elif isinstance(plaintext, str):
            plaintext_bytes = plaintext.encode("utf-8")
        else:
            plaintext_bytes = plaintext

        # 生成 nonce
        nonce: bytes = secrets.token_bytes(NONCE_LENGTH)

        # 加密
        aesgcm: Any = AESGCM(key)
        ciphertext: bytes = aesgcm.encrypt(nonce, plaintext_bytes, None)

        # 构建结果
        return EncryptedData(
            algorithm="AES-256-GCM",
            nonce=base64.b64encode(nonce).decode("utf-8"),
            ciphertext=base64.b64encode(ciphertext).decode("utf-8"),
        )

    def decrypt(
        self,
        encrypted_data: EncryptedData,
    ) -> bytes:
        """
        解密数据

        Args:
            encrypted_data: 加密数据容器

        Returns:
            明文字节

        Raises:
            ValueError: 密钥未设置或解密失败
        """
        if not self.config.enabled:
            raise ValueError("加密功能已禁用")

        # 获取密钥
        _, key = self.key_manager.get_key()

        # 解码
        nonce: bytes = base64.b64decode(encrypted_data.nonce)
        ciphertext: bytes = base64.b64decode(encrypted_data.ciphertext)

        # 解密
        aesgcm: Any = AESGCM(key)

        try:
            plaintext: bytes = aesgcm.decrypt(nonce, ciphertext, None)
            return plaintext
        except Exception as e:
            raise ValueError(f"解密失败: {str(e)}") from e

    def decrypt_to_string(self, encrypted_data: EncryptedData) -> str:
        """
        解密为字符串

        Args:
            encrypted_data: 加密数据容器

        Returns:
            明文字符串
        """
        return self.decrypt(encrypted_data).decode("utf-8")

    def decrypt_to_dict(self, encrypted_data: EncryptedData) -> dict[str, Any]:
        """
        解密为字典

        Args:
            encrypted_data: 加密数据容器

        Returns:
            明文字典
        """
        plaintext: str = self.decrypt_to_string(encrypted_data)
        return json.loads(plaintext)


# ============================================================================
# 辅助函数
# ============================================================================


def encrypt_data_with_password(
    data: bytes,
    password: str,
) -> tuple[bytes, bytes]:
    """
    使用密码加密数据

    Args:
        data: 明文数据
        password: 密码

    Returns:
        (salt, encrypted_data)
    """
    # 派生密钥
    key, salt = KeyManager.derive_key_from_password(password)

    # 加密
    nonce: bytes = secrets.token_bytes(NONCE_LENGTH)
    aesgcm: Any = AESGCM(key)
    ciphertext: bytes = aesgcm.encrypt(nonce, data, None)

    # 组合: nonce + ciphertext
    return salt, nonce + ciphertext


def decrypt_data_with_password(
    encrypted_data: bytes,
    password: str,
    salt: bytes,
) -> bytes:
    """
    使用密码解密数据

    Args:
        encrypted_data: 加密数据（nonce + ciphertext）
        password: 密码
        salt: 盐值

    Returns:
        明文数据
    """
    # 派生密钥
    key, _ = KeyManager.derive_key_from_password(password, salt)

    # 分离 nonce 和 ciphertext
    nonce: bytes = encrypted_data[:NONCE_LENGTH]
    ciphertext: bytes = encrypted_data[NONCE_LENGTH:]

    # 解密
    aesgcm: Any = AESGCM(key)
    return aesgcm.decrypt(nonce, ciphertext, None)


def generate_encryption_key() -> str:
    """
    生成加密密钥（Base64 编码）

    用于存储到环境变量

    Returns:
        Base64 编码的密钥
    """
    key: bytes = secrets.token_bytes(KEY_LENGTH)
    return base64.b64encode(key).decode("utf-8")


# ============================================================================
# 加密文件存储
# ============================================================================


class EncryptedFileStorage:
    """
    加密文件存储

    提供透明的加密文件读写
    """

    def __init__(
        self,
        encryptor: DataEncryptor,
        storage_path: str = "./encrypted_storage",
    ) -> None:
        """
        初始化加密文件存储

        Args:
            encryptor: 数据加密器
            storage_path: 存储路径
        """
        self.encryptor: DataEncryptor = encryptor
        self.storage_path: Path = Path(storage_path)
        self.storage_path.mkdir(parents=True, exist_ok=True)

    def save(
        self,
        filename: str,
        data: dict[str, Any],
    ) -> Path:
        """
        保存加密数据

        Args:
            filename: 文件名
            data: 数据字典

        Returns:
            文件路径
        """
        encrypted: EncryptedData = self.encryptor.encrypt(data)

        file_path: Path = self.storage_path / f"{filename}.enc"

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(encrypted.model_dump(mode="json"), f, ensure_ascii=False, indent=2)

        return file_path

    def load(
        self,
        filename: str,
    ) -> dict[str, Any]:
        """
        加载并解密数据

        Args:
            filename: 文件名

        Returns:
            数据字典
        """
        file_path: Path = self.storage_path / f"{filename}.enc"

        if not file_path.exists():
            raise FileNotFoundError(f"文件不存在: {file_path}")

        with open(file_path, "r", encoding="utf-8") as f:
            data: dict[str, Any] = json.load(f)

        encrypted: EncryptedData = EncryptedData.model_validate(data)
        return self.encryptor.decrypt_to_dict(encrypted)

    def exists(self, filename: str) -> bool:
        """
        检查文件是否存在

        Args:
            filename: 文件名

        Returns:
            是否存在
        """
        file_path: Path = self.storage_path / f"{filename}.enc"
        return file_path.exists()

    def delete(self, filename: str) -> bool:
        """
        删除文件

        Args:
            filename: 文件名

        Returns:
            是否成功
        """
        file_path: Path = self.storage_path / f"{filename}.enc"

        if file_path.exists():
            file_path.unlink()
            return True

        return False


# ============================================================================
# 导出
# ============================================================================

__all__ = [
    # 常量
    "KEY_LENGTH",
    "NONCE_LENGTH",
    "TAG_LENGTH",
    "KDF_ITERATIONS",
    "SALT_LENGTH",
    # 数据模型
    "EncryptedData",
    "KeyInfo",
    "EncryptionConfig",
    # 组件
    "KeyManager",
    "DataEncryptor",
    "EncryptedFileStorage",
    # 辅助函数
    "encrypt_data_with_password",
    "decrypt_data_with_password",
    "generate_encryption_key",
    # 状态
    "CRYPTO_AVAILABLE",
]
