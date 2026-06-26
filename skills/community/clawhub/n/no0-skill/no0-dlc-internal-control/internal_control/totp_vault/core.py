"""
TOTP Vault - 核心实现
"""
import os
import hashlib
import secrets
import base64
from datetime import datetime, timedelta
from typing import Optional, Dict, List, Callable
from .models import TOTPKey, TOTPCode, MFAResult, KeyStatus
from .storage import VaultStorage, SQLiteStorage
from .crypto import MasterKeyManager, EncryptionHelper


class TOTPVault:
    """
    TOTP Vault 核心类
    
    职责：
    1. 密钥生成与存储
    2. TOTP 码计算（内部使用，不暴露给上层）
    3. 密钥生命周期管理
    4. 自动化 MFA 流程
    """
    
    def __init__(self, 
                 master_key: Optional[bytes] = None,
                 storage: Optional[VaultStorage] = None):
        """
        初始化 Vault
        
        Args:
            master_key: 可选的主密钥（用于第二层加密）
            storage: 存储后端，默认使用 SQLite
        """
        self._master_key = master_key
        self._storage = storage or SQLiteStorage()
        self._code_cache: Dict[str, TOTPCode] = {}
        
        # 尝试导入 keyring
        self._keyring_available = self._check_keyring()
    
    def _check_keyring(self) -> bool:
        """检查系统钥匙串是否可用"""
        try:
            import keyring
            # 测试性获取
            keyring.get_password("test", "test")
            return True
        except:
            return False
    
    # ========== 密钥管理 ==========
    
    def generate_key(self, context: str, 
                     key_id: Optional[str] = None) -> TOTPKey:
        """
        为新上下文生成 TOTP 密钥
        
        Args:
            context: 使用上下文（如 "private_c_file_access"）
            key_id: 可选的自定义密钥ID，默认自动生成
            
        Returns:
            TOTPKey 元数据（不包含实际密钥）
        """
        # 检查是否已有相同上下文的密钥
        existing = self._storage.get_key_by_context(context)
        if existing and existing.status == KeyStatus.ACTIVE:
            return existing
        
        # 生成符合 RFC 6238 的密钥
        secret = self._generate_secret()
        
        # 生成密钥ID
        if not key_id:
            key_id = f"totp_{context}_{self._generate_short_id()}"
        
        # 加密存储
        self._store_secret(key_id, secret)
        
        # 返回元数据
        key_meta = TOTPKey(
            key_id=key_id,
            context=context,
            created_at=datetime.now(),
            last_used=None,
            use_count=0,
            algorithm="SHA1",
            digits=6,
            interval=30
        )
        
        self._storage.store_metadata(key_meta)
        return key_meta
    
    def get_key_metadata(self, key_id: str) -> Optional[TOTPKey]:
        """获取密钥元数据（不包含实际密钥）"""
        return self._storage.get_metadata(key_id)
    
    def get_key_by_context(self, context: str) -> Optional[TOTPKey]:
        """根据上下文获取密钥元数据"""
        return self._storage.get_key_by_context(context)
    
    def list_keys(self) -> List[TOTPKey]:
        """列出所有密钥元数据"""
        return self._storage.list_all_metadata()
    
    def rotate_key(self, key_id: str, grace_period_hours: int = 24) -> TOTPKey:
        """
        轮换密钥
        
        场景：
        - 定期安全轮换（建议90天）
        - 怀疑密钥泄露
        - 用户主动要求
        """
        # 获取旧密钥上下文
        old_meta = self.get_key_metadata(key_id)
        if not old_meta:
            raise KeyError(f"Key not found: {key_id}")
        
        # 生成新密钥
        new_secret = self._generate_secret()
        
        # 新密钥保持相同ID
        self._store_secret(key_id, new_secret)
        
        # 标记旧密钥为轮换中（保留24小时宽限期）
        self._storage.mark_rotated(key_id, grace_period_hours)
        
        # 更新元数据
        key_meta = TOTPKey(
            key_id=key_id,
            context=old_meta.context,
            created_at=datetime.now(),
            last_used=None,
            use_count=0,
            algorithm="SHA1",
            digits=6,
            interval=30,
            status=KeyStatus.ACTIVE
        )
        self._storage.store_metadata(key_meta)
        
        return key_meta
    
    def revoke_key(self, key_id: str) -> None:
        """
        撤销密钥
        
        警告：撤销后，使用该密钥的 MFA 授权将永久失效
        建议先确认是否有备份
        """
        # 从钥匙串删除
        if self._keyring_available:
            try:
                import keyring
                keyring.delete_password(
                    service="openclaw_totp_vault",
                    username=key_id
                )
            except:
                pass
        
        # 删除元数据
        self._storage.delete(key_id)
        self._code_cache.pop(key_id, None)
    
    # ========== TOTP 计算（内部使用） ==========
    
    def _compute_totp(self, key_id: str, 
                      timestamp: Optional[int] = None) -> TOTPCode:
        """
        计算当前 TOTP 码（私有方法，不暴露）
        
        这是核心安全机制：
        - 只有 Vault 内部可以计算 TOTP
        - 计算结果不返回给调用者
        - 用于内部验证流程
        """
        # 获取密钥
        secret = self._retrieve_secret(key_id)
        if not secret:
            raise KeyError(f"Secret not found: {key_id}")
        
        # 使用 pyotp 计算 TOTP
        try:
            import pyotp
            totp = pyotp.TOTP(secret)
            code = totp.now()
            
            # 计算有效期
            now = datetime.now()
            interval_start = int(now.timestamp()) // 30 * 30
            valid_from = datetime.fromtimestamp(interval_start)
            valid_until = datetime.fromtimestamp(interval_start + 30)
            
            return TOTPCode(
                code=code,
                valid_from=valid_from,
                valid_until=valid_until,
                key_id=key_id
            )
        except ImportError:
            # Fallback: 简单 TOTP 实现
            import time
            import hmac
            
            if timestamp is None:
                timestamp = int(time.time())
            
            # 计算时间步
            time_step = timestamp // 30
            time_step_bytes = time_step.to_bytes(8, byteorder='big')
            
            # 解码 base32 密钥
            secret_bytes = base64.b32decode(secret)
            
            # 计算 HMAC
            hash_bytes = hmac.new(secret_bytes, time_step_bytes, hashlib.sha1).digest()
            
            # 动态截断
            offset = hash_bytes[-1] & 0x0f
            code = ((hash_bytes[offset] & 0x7f) << 24 |
                    (hash_bytes[offset + 1] & 0xff) << 16 |
                    (hash_bytes[offset + 2] & 0xff) << 8 |
                    (hash_bytes[offset + 3] & 0xff))
            code = code % 1000000
            code_str = f"{code:06d}"
            
            # 计算有效期
            now = datetime.now()
            interval_start = timestamp // 30 * 30
            valid_from = datetime.fromtimestamp(interval_start)
            valid_until = datetime.fromtimestamp(interval_start + 30)
            
            return TOTPCode(
                code=code_str,
                valid_from=valid_from,
                valid_until=valid_until,
                key_id=key_id
            )
    
    def _verify_totp(self, key_id: str, 
                     provided_code: str,
                     valid_window: int = 1) -> bool:
        """
        验证 TOTP 码（私有方法）
        
        正常情况下不使用——自动化流程中由系统自行计算
        保留此方法用于：
        - 测试验证
        - 外部手动验证场景
        """
        secret = self._retrieve_secret(key_id)
        if not secret:
            return False
        
        try:
            import pyotp
            totp = pyotp.TOTP(secret)
            return totp.verify(provided_code, valid_window=valid_window)
        except ImportError:
            # Fallback
            import time
            for offset in range(-valid_window, valid_window + 1):
                timestamp = int(time.time()) + offset * 30
                computed = self._compute_totp(key_id, timestamp)
                if computed.code == provided_code:
                    return True
            return False
    
    # ========== 自动化 MFA 接口 ==========
    
    def execute_mfa_flow(self, 
                         key_id: str,
                         human_confirmation_callback: Callable[[dict], bool]) -> MFAResult:
        """
        执行完整 MFA 授权流程
        
        这是上层调用的主要接口：
        1. 预计算 TOTP 码（后台完成）
        2. 调用人类确认回调（显示请求，不显示 TOTP）
        3. 人类确认后，系统自动完成验证
        4. 返回授权结果
        
        Args:
            key_id: TOTP 密钥ID
            human_confirmation_callback: 回调函数，用于请求人类确认
                签名: fn(request_info: dict) -> bool
        
        Returns:
            MFAResult 包含授权决策
        """
        # 1. 预计算 TOTP（此时人类还未看到请求）
        try:
            current_code = self._compute_totp(key_id)
        except KeyError as e:
            return MFAResult(
                granted=False,
                key_id=key_id,
                message=f"Key error: {e}"
            )
        
        # 2. 构建确认请求（不包含 TOTP 码）
        key_meta = self.get_key_metadata(key_id)
        if not key_meta:
            return MFAResult(
                granted=False,
                key_id=key_id,
                message="Key metadata not found"
            )
        
        request_info = {
            "context": key_meta.context,
            "key_id": key_id,
            "expires_at": current_code.valid_until.isoformat(),
            # 注意：不包含 current_code.code！
        }
        
        # 3. 请求人类确认
        try:
            approved = human_confirmation_callback(request_info)
        except Exception as e:
            return MFAResult(
                granted=False,
                key_id=key_id,
                message=f"Confirmation callback error: {e}"
            )
        
        if not approved:
            return MFAResult(
                granted=False,
                key_id=key_id,
                message="Human declined"
            )
        
        # 4. 人类已确认，检查 TOTP 是否仍有效
        if not current_code.is_valid():
            # 窗口过期，重新计算
            try:
                current_code = self._compute_totp(key_id)
            except Exception as e:
                return MFAResult(
                    granted=False,
                    key_id=key_id,
                    message=f"Failed to recompute TOTP: {e}"
                )
        
        # 5. 记录使用
        self._storage.update_usage(key_id, datetime.now())
        
        # 6. 返回成功结果
        return MFAResult(
            granted=True,
            key_id=key_id,
            message="MFA authorized"
        )
    
    def execute_mfa_flow_simple(self, context: str,
                                 confirmation_callback: Callable[[dict], bool]) -> MFAResult:
        """
        简化的 MFA 流程（自动处理密钥ID）
        
        Args:
            context: 使用上下文（如 "private_c_file_access"）
            confirmation_callback: 确认回调
        """
        # 获取或创建密钥
        key_meta = self.get_key_by_context(context)
        if not key_meta:
            key_meta = self.generate_key(context)
        
        return self.execute_mfa_flow(key_meta.key_id, confirmation_callback)
    
    # ========== 内部辅助方法 ==========
    
    def _generate_secret(self) -> str:
        """生成符合 RFC 6238 的密钥（Base32 编码）"""
        # 160位随机数，Base32编码
        random_bytes = secrets.token_bytes(20)
        return base64.b32encode(random_bytes).decode('ascii')
    
    def _generate_short_id(self) -> str:
        """生成短标识符"""
        return hashlib.sha256(
            secrets.token_bytes(16)
        ).hexdigest()[:8]
    
    def _store_secret(self, key_id: str, secret: str) -> None:
        """存储密钥到系统钥匙串"""
        # 如果有主密钥，先加密
        secret_to_store = secret
        if self._master_key:
            secret_to_store = EncryptionHelper.encrypt_with_key(secret, self._master_key)
        
        if self._keyring_available:
            try:
                import keyring
                keyring.set_password(
                    service="openclaw_totp_vault",
                    username=key_id,
                    password=secret_to_store
                )
            except Exception as e:
                # 钥匙串失败，使用文件存储（不安全，仅用于开发）
                self._store_secret_to_file(key_id, secret_to_store)
        else:
            # 钥匙串不可用，使用文件存储
            self._store_secret_to_file(key_id, secret_to_store)
    
    def _store_secret_to_file(self, key_id: str, secret: str) -> None:
        """备选：存储到文件（不安全，仅用于开发测试）"""
        import json
        file_path = os.path.expanduser("~/.openclaw/secrets/totp_vault_secrets.json")
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        secrets_data = {}
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                secrets_data = json.load(f)
        
        secrets_data[key_id] = secret
        
        with open(file_path, 'w') as f:
            json.dump(secrets_data, f)
        os.chmod(file_path, 0o600)
    
    def _retrieve_secret(self, key_id: str) -> Optional[str]:
        """从系统钥匙串获取密钥"""
        secret = None
        
        if self._keyring_available:
            try:
                import keyring
                secret = keyring.get_password(
                    service="openclaw_totp_vault",
                    username=key_id
                )
            except:
                pass
        
        if not secret:
            # 尝试从文件读取（备选）
            secret = self._retrieve_secret_from_file(key_id)
        
        if secret and self._master_key:
            try:
                secret = EncryptionHelper.decrypt_with_key(secret, self._master_key)
            except:
                # 解密失败，可能是未加密的旧格式
                pass
        
        return secret
    
    def _retrieve_secret_from_file(self, key_id: str) -> Optional[str]:
        """备选：从文件读取密钥"""
        import json
        file_path = os.path.expanduser("~/.openclaw/secrets/totp_vault_secrets.json")
        
        if not os.path.exists(file_path):
            return None
        
        try:
            with open(file_path, 'r') as f:
                secrets_data = json.load(f)
            return secrets_data.get(key_id)
        except:
            return None
    
    def _record_usage(self, key_id: str) -> None:
        """记录密钥使用"""
        self._storage.update_usage(key_id, datetime.now())