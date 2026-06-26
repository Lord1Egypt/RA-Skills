"""
HTTP 授权服务 - 安全令牌库

设计原则：
1. 令牌只在 Vault 内部生成和消费
2. Agent 只获得"授权通过"的状态，不接触令牌
3. 令牌一次性使用，防止重放攻击
4. 短期有效（默认30分钟）
"""

import hashlib
import hmac
import json
import secrets
import threading
import time
from datetime import datetime, timedelta
from typing import Optional, Dict


class SecureTokenVault:
    """
    安全令牌库
    
    使用简单 JWT 风格的令牌（不依赖外部库）
    """
    
    def __init__(self, secret_key: Optional[str] = None):
        # JWT 签名密钥
        self._secret = secret_key or secrets.token_hex(32)
        
        # 已消费令牌记录（防止重放）
        self._consumed_tokens: set = set()
        self._lock = threading.Lock()
    
    def generate_token(self,
                       request_id: str,
                       resource_path: str,
                       operation: str,
                       expires_minutes: int = 30) -> str:
        """
        生成授权令牌
        
        Returns:
            JWT 格式的授权令牌
        """
        # 构建 payload
        payload = {
            "iss": "openclaw_auth_service",
            "sub": request_id,
            "resource": resource_path,
            "operation": operation,
            "iat": int(time.time()),
            "exp": int(time.time()) + expires_minutes * 60,
            "jti": secrets.token_hex(16)  # 唯一令牌ID
        }
        
        # 编码 payload
        payload_json = json.dumps(payload, sort_keys=True)
        payload_b64 = self._base64_encode(payload_json)
        
        # 生成签名
        signature = self._generate_signature(payload_b64)
        
        # 组合令牌
        token = f"{payload_b64}.{signature}"
        return token
    
    def verify_and_consume(self, token: str) -> Optional[Dict]:
        """
        验证并消费令牌
        
        Returns:
            令牌 payload（如果有效）
            None（如果无效或已消费）
        """
        try:
            # 解析令牌
            parts = token.split(".")
            if len(parts) != 2:
                return None
            
            payload_b64, signature = parts
            
            # 验证签名
            expected_signature = self._generate_signature(payload_b64)
            if not hmac.compare_digest(signature, expected_signature):
                return None
            
            # 解码 payload
            payload_json = self._base64_decode(payload_b64)
            payload = json.loads(payload_json)
            
            # 检查过期时间
            if payload.get("exp", 0) < int(time.time()):
                return None
            
            # 检查是否已消费（防重放）
            jti = payload.get("jti")
            with self._lock:
                if jti in self._consumed_tokens:
                    return None
                
                # 标记为已消费
                self._consumed_tokens.add(jti)
            
            return payload
            
        except Exception as e:
            return None
    
    def hash_token(self, token: str) -> str:
        """计算令牌哈希（用于审计日志，不存储原文）"""
        return hashlib.sha256(token.encode()).hexdigest()[:16]
    
    def _generate_signature(self, payload_b64: str) -> str:
        """生成签名"""
        message = f"{payload_b64}.{self._secret}"
        return hashlib.sha256(message.encode()).hexdigest()[:32]
    
    def _base64_encode(self, data: str) -> str:
        """Base64 编码"""
        import base64
        return base64.urlsafe_b64encode(data.encode()).decode().rstrip("=")
    
    def _base64_decode(self, data: str) -> str:
        """Base64 解码"""
        import base64
        # 添加填充
        padding = 4 - len(data) % 4
        if padding != 4:
            data += "=" * padding
        return base64.urlsafe_b64decode(data).decode()
    
    def cleanup_consumed_tokens(self) -> int:
        """清理消费记录（简单实现：超过一定数量后清空）"""
        with self._lock:
            if len(self._consumed_tokens) > 10000:
                self._consumed_tokens.clear()
                return 10000
            return 0
