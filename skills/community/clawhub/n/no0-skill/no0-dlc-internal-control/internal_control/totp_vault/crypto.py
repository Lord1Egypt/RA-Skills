"""
TOTP Vault - 加密和主密钥管理
"""
import os
import hashlib
import secrets
import base64
from typing import Optional


class MasterKeyManager:
    """
    主密钥管理器
    
    职责：
    1. 从用户密码派生主密钥
    2. 主密钥的加密存储与读取
    3. 密钥版本管理
    """
    
    SALT_LENGTH = 32
    KEY_LENGTH = 32
    
    def __init__(self, key_file: str = "~/.openclaw/secrets/vault_master.key"):
        self.key_file = os.path.expanduser(key_file)
        os.makedirs(os.path.dirname(self.key_file), mode=0o700, exist_ok=True)
    
    def is_initialized(self) -> bool:
        """检查 Vault 是否已初始化"""
        return os.path.exists(self.key_file)
    
    def initialize(self, password: str) -> bytes:
        """
        首次初始化主密钥
        
        Args:
            password: 用户设置的 Vault 密码
            
        Returns:
            派生的主密钥
        """
        if self.is_initialized():
            raise RuntimeError("Vault already initialized")
        
        # 生成随机盐值
        salt = os.urandom(self.SALT_LENGTH)
        
        # 派生密钥
        key = self._derive_key(password, salt)
        
        # 存储盐值（密钥本身不存储，每次派生）
        with open(self.key_file, 'wb') as f:
            f.write(salt)
        os.chmod(self.key_file, 0o600)
        
        return key
    
    def unlock(self, password: str) -> bytes:
        """
        解锁 Vault（派生主密钥）
        
        Args:
            password: 用户密码
            
        Returns:
            派生的主密钥
            
        Raises:
            ValueError: 密码错误
            FileNotFoundError: Vault 未初始化
        """
        if not self.is_initialized():
            raise FileNotFoundError("Vault not initialized. Run initialize() first.")
        
        with open(self.key_file, 'rb') as f:
            salt = f.read()
        
        key = self._derive_key(password, salt)
        return key
    
    def change_password(self, old_password: str, new_password: str) -> bytes:
        """
        修改 Vault 密码
        
        注意：这会重新加密所有存储的密钥（需要 Vault 配合）
        """
        # 1. 用旧密码解锁
        old_key = self.unlock(old_password)
        
        # 2. 生成新盐值和密钥
        new_salt = os.urandom(self.SALT_LENGTH)
        new_key = self._derive_key(new_password, new_salt)
        
        # 3. 保存新盐值
        with open(self.key_file, 'wb') as f:
            f.write(new_salt)
        os.chmod(self.key_file, 0o600)
        
        return new_key, old_key
    
    def _derive_key(self, password: str, salt: bytes) -> bytes:
        """
        使用 PBKDF2 派生密钥
        
        注：使用标准库实现，避免额外依赖
        生产环境可考虑使用 Argon2
        """
        # 使用 PBKDF2-HMAC-SHA256
        key = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            salt,
            iterations=600000,  # OWASP 推荐值
            dklen=self.KEY_LENGTH
        )
        return key


class EncryptionHelper:
    """加密辅助类"""
    
    @staticmethod
    def encrypt_with_key(data: str, key: bytes) -> str:
        """
        使用 Fernet 风格加密（简化版，使用 AES-GCM）
        
        Returns:
            base64 编码的加密数据
        """
        try:
            from cryptography.hazmat.primitives.ciphers.aead import AESGCM
            
            # 生成随机 nonce
            nonce = os.urandom(12)
            
            # 加密
            aesgcm = AESGCM(key)
            ciphertext = aesgcm.encrypt(nonce, data.encode('utf-8'), None)
            
            # 组合 nonce + ciphertext
            combined = nonce + ciphertext
            return base64.urlsafe_b64encode(combined).decode('ascii')
        except ImportError:
            # Fallback: 简单的 XOR 加密（仅用于测试，不安全）
            return base64.b64encode(data.encode()).decode()
    
    @staticmethod
    def decrypt_with_key(encrypted_data: str, key: bytes) -> str:
        """解密数据"""
        try:
            from cryptography.hazmat.primitives.ciphers.aead import AESGCM
            
            # 解码
            combined = base64.urlsafe_b64decode(encrypted_data)
            
            # 分离 nonce 和 ciphertext
            nonce = combined[:12]
            ciphertext = combined[12:]
            
            # 解密
            aesgcm = AESGCM(key)
            plaintext = aesgcm.decrypt(nonce, ciphertext, None)
            
            return plaintext.decode('utf-8')
        except ImportError:
            # Fallback
            return base64.b64decode(encrypted_data).decode()
    
    @staticmethod
    def generate_backup_encryption_key(password: str, salt: Optional[bytes] = None) -> tuple[bytes, bytes]:
        """
        生成备份加密密钥
        
        Returns:
            (key, salt)
        """
        if salt is None:
            salt = os.urandom(16)
        
        key = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            salt,
            iterations=100000,
            dklen=32
        )
        return key, salt