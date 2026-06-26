"""
安全工具
"""

import json
import re
from typing import Dict, Any
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import base64


class InputValidator:
    """输入验证器"""
    
    @staticmethod
    def validate_and_sanitize(params: Dict[str, Any],
                             schema: Dict[str, Any]) -> Dict[str, Any]:
        """
        验证和清理输入参数
        
        参数:
            params: 输入参数
            schema: JSON Schema
        
        返回:
            验证后的参数
        """
        validated = {}
        
        for field, field_schema in schema.get("properties", {}).items():
            if field not in params:
                if field in schema.get("required", []):
                    raise ValueError(f"缺少必需字段: {field}")
                continue
            
            value = params[field]
            field_type = field_schema.get("type")
            
            # 类型检查
            if field_type == "string":
                if not isinstance(value, str):
                    raise ValueError(f"字段 {field} 必须是字符串")
                # 防止 SQL 注入
                value = InputValidator.sanitize_string(value)
            
            elif field_type == "number":
                if not isinstance(value, (int, float)):
                    raise ValueError(f"字段 {field} 必须是数字")
                # 检查范围
                if "minimum" in field_schema and value < field_schema["minimum"]:
                    raise ValueError(f"字段 {field} 小于最小值")
                if "maximum" in field_schema and value > field_schema["maximum"]:
                    raise ValueError(f"字段 {field} 大于最大值")
            
            elif field_type == "object":
                if not isinstance(value, dict):
                    raise ValueError(f"字段 {field} 必须是对象")
            
            validated[field] = value
        
        return validated
    
    @staticmethod
    def sanitize_string(value: str) -> str:
        """
        清理字符串,防止注入攻击
        
        参数:
            value: 输入字符串
        
        返回:
            清理后的字符串
        """
        # 移除危险字符
        dangerous_patterns = [
            r"'",
            r'"',
            r";",
            r"--",
            r"/\*",
            r"\*/",
            r"xp_",
            r"sp_"
        ]
        
        for pattern in dangerous_patterns:
            value = re.sub(pattern, "", value)
        
        # 限制长度
        max_length = 1000
        if len(value) > max_length:
            value = value[:max_length]
        
        return value


class DataEncryption:
    """数据加密"""
    
    def __init__(self, key: bytes):
        """
        初始化加密器
        
        参数:
            key: 加密密钥(32 字节)，生产环境必须提供
        """
        if key is None or len(key) != 32:
            raise ValueError("加密密钥必须为 32 字节，生产环境必须提供有效密钥")
        self.key = key
    
    @classmethod
    def from_env(cls, env_key: str = "PAYMENT_ENCRYPTION_KEY") -> "DataEncryption":
        """
        从环境变量创建加密器
        
        参数:
            env_key: 环境变量名称
        """
        import os
        key_str = os.environ.get(env_key)
        if not key_str:
            raise ValueError(f"环境变量 {env_key} 未设置，生产环境必须提供加密密钥")
        key_bytes = key_str.encode()[:32].ljust(32, b'0')
        return cls(key_bytes)
    
    def encrypt_sensitive_data(self, data: Dict[str, Any]) -> str:
        """
        加密敏感数据
        
        参数:
            data: 数据字典
        
        返回:
            加密后的数据(Base64 编码)
        """
        # 标记敏感字段
        sensitive_fields = ["api_key", "password", "token", "card_number"]
        
        encrypted_data = data.copy()
        
        for field in sensitive_fields:
            if field in encrypted_data:
                # 加密敏感字段
                plaintext = str(encrypted_data[field]).encode()
                
                # 生成随机 nonce
                nonce = get_random_bytes(16)
                
                # 创建加密器
                cipher = AES.new(self.key, AES.MODE_GCM, nonce=nonce)
                
                # 加密
                ciphertext, tag = cipher.encrypt_and_digest(plaintext)
                
                # 存储加密后的数据
                encrypted_data[field] = {
                    "encrypted": base64.b64encode(ciphertext).decode(),
                    "nonce": base64.b64encode(nonce).decode(),
                    "tag": base64.b64encode(tag).decode()
                }
        
        return json.dumps(encrypted_data)
    
    def decrypt_sensitive_data(self, encrypted_data: str) -> Dict[str, Any]:
        """
        解密敏感数据
        
        参数:
            encrypted_data: 加密后的数据(JSON 字符串)
        
        返回:
            解密后的数据
        """
        data = json.loads(encrypted_data)
        
        for field, value in data.items():
            if isinstance(value, dict) and "encrypted" in value:
                # 解密敏感字段
                ciphertext = base64.b64decode(value["encrypted"])
                nonce = base64.b64decode(value["nonce"])
                tag = base64.b64decode(value["tag"])
                
                # 创建解密器
                cipher = AES.new(self.key, AES.MODE_GCM, nonce=nonce)
                
                # 解密
                plaintext = cipher.decrypt_and_verify(ciphertext, tag)
                data[field] = plaintext.decode()
        
        return data
