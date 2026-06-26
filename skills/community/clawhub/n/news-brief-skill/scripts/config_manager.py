#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Config Manager Module
配置管理模块：处理用户配置、加密存储、备份恢复
"""

import os
import json
import shutil
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64

class ConfigManager:
    """配置管理器"""
    
    def __init__(self):
        self.project_root = Path(__file__).parent.parent
        self.users_dir = self.project_root / "data" / "users"
        self.config_dir = self.project_root / "config"
        self.backups_dir = self.project_root / "data" / "backups"
        
        # 确保目录存在
        self.users_dir.mkdir(parents=True, exist_ok=True)
        self.backups_dir.mkdir(parents=True, exist_ok=True)
        
        # 加密密钥（实际使用中应该从环境变量或安全存储获取）
        self.encryption_key = self._get_or_create_encryption_key()
    
    def _get_or_create_encryption_key(self) -> bytes:
        """获取或创建加密密钥"""
        key_file = self.config_dir / "encryption.key"
        if key_file.exists():
            with open(key_file, 'rb') as f:
                return f.read()
        else:
            # 生成新的加密密钥
            key = Fernet.generate_key()
            with open(key_file, 'wb') as f:
                f.write(key)
            return key
    
    def _encrypt_data(self, data: str) -> str:
        """加密数据"""
        f = Fernet(self.encryption_key)
        return base64.b64encode(f.encrypt(data.encode())).decode()
    
    def _decrypt_data(self, encrypted_data: str) -> str:
        """解密数据"""
        f = Fernet(self.encryption_key)
        decrypted = f.decrypt(base64.b64decode(encrypted_data.encode()))
        return decrypted.decode()
    
    def create_user_config(self, user_id: str, initial_config: Dict[str, Any]) -> bool:
        """
        创建用户配置
        
        Args:
            user_id: 用户ID
            initial_config: 初始配置
            
        Returns:
            是否成功
        """
        try:
            user_dir = self.users_dir / user_id
            user_dir.mkdir(exist_ok=True)
            
            # 备份现有配置（如果存在）
            config_file = user_dir / "current_config.json"
            if config_file.exists():
                self._backup_user_config(user_id)
            
            # 加密敏感信息
            encrypted_config = self._encrypt_sensitive_fields(initial_config.copy())
            
            # 保存配置
            with open(config_file, 'w', encoding='utf-8') as f:
                json.dump(encrypted_config, f, ensure_ascii=False, indent=2)
            
            return True
            
        except Exception as e:
            print(f"创建用户配置失败: {e}")
            return False
    
    def load_user_config(self, user_id: str) -> Optional[Dict[str, Any]]:
        """
        加载用户配置
        
        Args:
            user_id: 用户ID
            
        Returns:
            用户配置字典，如果不存在返回None
        """
        try:
            config_file = self.users_dir / user_id / "current_config.json"
            if not config_file.exists():
                return None
            
            with open(config_file, 'r', encoding='utf-8') as f:
                encrypted_config = json.load(f)
            
            # 解密敏感信息
            decrypted_config = self._decrypt_sensitive_fields(encrypted_config)
            return decrypted_config
            
        except Exception as e:
            print(f"加载用户配置失败: {e}")
            return None
    
    def update_user_config(self, user_id: str, new_config: Dict[str, Any]) -> bool:
        """
        更新用户配置
        
        Args:
            user_id: 用户ID
            new_config: 新配置
            
        Returns:
            是否成功
        """
        try:
            # 先备份当前配置
            self._backup_user_config(user_id)
            
            # 加密敏感信息
            encrypted_config = self._encrypt_sensitive_fields(new_config.copy())
            
            # 保存新配置
            user_dir = self.users_dir / user_id
            config_file = user_dir / "current_config.json"
            with open(config_file, 'w', encoding='utf-8') as f:
                json.dump(encrypted_config, f, ensure_ascii=False, indent=2)
            
            return True
            
        except Exception as e:
            print(f"更新用户配置失败: {e}")
            return False
    
    def _encrypt_sensitive_fields(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """加密敏感字段"""
        sensitive_fields = [
            'email_password', 'dingtalk_token', 'wechat_token',
            'smtp_password', 'api_keys'
        ]
        
        encrypted_config = config.copy()
        for field in sensitive_fields:
            if field in encrypted_config and encrypted_config[field]:
                encrypted_config[field] = self._encrypt_data(str(encrypted_config[field]))
        
        return encrypted_config
    
    def _decrypt_sensitive_fields(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """解密敏感字段"""
        sensitive_fields = [
            'email_password', 'dingtalk_token', 'wechat_token',
            'smtp_password', 'api_keys'
        ]
        
        decrypted_config = config.copy()
        for field in sensitive_fields:
            if field in decrypted_config and decrypted_config[field]:
                try:
                    decrypted_config[field] = self._decrypt_data(decrypted_config[field])
                except:
                    # 解密失败，保留原值
                    pass
        
        return decrypted_config
    
    def _backup_user_config(self, user_id: str):
        """备份用户配置"""
        try:
            user_dir = self.users_dir / user_id
            config_file = user_dir / "current_config.json"
            
            if not config_file.exists():
                return
            
            # 创建备份目录
            backup_dir = self.backups_dir / user_id
            backup_dir.mkdir(exist_ok=True)
            
            # 生成备份文件名
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_file = backup_dir / f"config_backup_{timestamp}.json"
            
            # 复制配置文件
            shutil.copy2(config_file, backup_file)
            
            # 只保留最近7天的备份
            self._cleanup_old_backups(user_id)
            
        except Exception as e:
            print(f"备份用户配置失败: {e}")
    
    def _cleanup_old_backups(self, user_id: str, keep_days: int = 7):
        """清理旧备份"""
        try:
            backup_dir = self.backups_dir / user_id
            if not backup_dir.exists():
                return
            
            cutoff_date = datetime.now() - timedelta(days=keep_days)
            for backup_file in backup_dir.glob("config_backup_*.json"):
                file_time = datetime.strptime(
                    backup_file.stem.split('_')[2], '%Y%m%d'
                )
                if file_time < cutoff_date:
                    backup_file.unlink()
                    
        except Exception as e:
            print(f"清理旧备份失败: {e}")
    
    def get_all_users(self) -> List[str]:
        """
        获取所有用户ID列表
        
        Returns:
            用户ID列表
        """
        try:
            users = []
            for user_dir in self.users_dir.iterdir():
                if user_dir.is_dir():
                    users.append(user_dir.name)
            return users
        except Exception as e:
            print(f"获取用户列表失败: {e}")
            return []
    
    def restore_user_config(self, user_id: str, backup_timestamp: str) -> bool:
        """
        恢复用户配置到指定时间点
        
        Args:
            user_id: 用户ID
            backup_timestamp: 备份时间戳
            
        Returns:
            是否成功
        """
        try:
            backup_file = self.backups_dir / user_id / f"config_backup_{backup_timestamp}.json"
            if not backup_file.exists():
                return False
            
            # 备份当前配置
            self._backup_user_config(user_id)
            
            # 恢复备份配置
            config_file = self.users_dir / user_id / "current_config.json"
            shutil.copy2(backup_file, config_file)
            
            return True
            
        except Exception as e:
            print(f"恢复用户配置失败: {e}")
            return False
    
    def save_optimization_log(self, user_id: str, optimization_data: Dict[str, Any]):
        """
        保存优化日志
        
        Args:
            user_id: 用户ID
            optimization_data: 优化数据
        """
        try:
            user_dir = self.users_dir / user_id
            log_file = user_dir / "optimization_log.json"
            
            # 读取现有日志
            if log_file.exists():
                with open(log_file, 'r', encoding='utf-8') as f:
                    logs = json.load(f)
            else:
                logs = []
            
            # 添加新日志
            optimization_data['timestamp'] = datetime.now().isoformat()
            logs.append(optimization_data)
            
            # 只保留最近100条日志
            logs = logs[-100:]
            
            # 保存日志
            with open(log_file, 'w', encoding='utf-8') as f:
                json.dump(logs, f, ensure_ascii=False, indent=2)
                
        except Exception as e:
            print(f"保存优化日志失败: {e}")
    
    def save_feedback_history(self, user_id: str, feedback_data: Dict[str, Any]):
        """
        保存反馈历史
        
        Args:
            user_id: 用户ID
            feedback_data: 反馈数据
        """
        try:
            user_dir = self.users_dir / user_id
            history_file = user_dir / "feedback_history.json"
            
            # 读取现有历史
            if history_file.exists():
                with open(history_file, 'r', encoding='utf-8') as f:
                    history = json.load(f)
            else:
                history = []
            
            # 添加新反馈
            feedback_data['timestamp'] = datetime.now().isoformat()
            history.append(feedback_data)
            
            # 只保留最近200条反馈
            history = history[-200:]
            
            # 保存历史
            with open(history_file, 'w', encoding='utf-8') as f:
                json.dump(history, f, ensure_ascii=False, indent=2)
                
        except Exception as e:
            print(f"保存反馈历史失败: {e}")