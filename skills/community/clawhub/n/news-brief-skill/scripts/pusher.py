#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
News Pusher Module
推送模块：处理多渠道推送，状态反馈，失败切换
"""

import os
import json
import smtplib
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import requests

class NewsPusher:
    """新闻推送器"""
    
    def __init__(self, user_id: str, user_config: Dict[str, Any]):
        self.user_id = user_id
        self.user_config = user_config
        self.project_root = Path(__file__).parent.parent
        
        # 推送渠道配置
        self.channels = {
            'wechat': self._push_wechat,
            'email': self._push_email, 
            'dingtalk': self._push_dingtalk,
            'telegram': self._push_telegram
        }
        
        # 日志设置
        self.logger = self._setup_logger()
    
    def _setup_logger(self):
        """设置日志"""
        import logging
        log_dir = self.project_root / "data" / "logs"
        log_dir.mkdir(parents=True, exist_ok=True)
        
        logger = logging.getLogger(f"NewsPusher_{self.user_id}")
        if not logger.handlers:
            handler = logging.FileHandler(
                log_dir / f"push_log_{datetime.now().strftime('%Y%m%d')}.log"
            )
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            logger.setLevel(logging.INFO)
        return logger
    
    def push_brief(self, brief_content: str) -> Dict[str, Any]:
        """
        推送新闻简报
        
        Args:
            brief_content: 简报内容
            
        Returns:
            推送结果字典
        """
        try:
            self.logger.info(f"开始推送简报给用户 {self.user_id}")
            
            # 获取推送配置
            primary_channel = self.user_config.get('primary_channel', 'wechat')
            backup_channels = self.user_config.get('backup_channels', [])
            
            # 尝试主渠道推送
            result = self._try_push_channel(primary_channel, brief_content)
            
            if result['success']:
                self.logger.info(f"主渠道 {primary_channel} 推送成功")
                return result
            
            # 主渠道失败，尝试备用渠道
            self.logger.warning(f"主渠道 {primary_channel} 推送失败，尝试备用渠道")
            
            for backup_channel in backup_channels:
                result = self._try_push_channel(backup_channel, brief_content)
                if result['success']:
                    self.logger.info(f"备用渠道 {backup_channel} 推送成功")
                    return result
            
            # 所有渠道都失败
            self.logger.error("所有推送渠道都失败")
            return {
                'success': False,
                'channel': 'all_failed',
                'error': '所有推送渠道都失败',
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"推送简报时出错: {e}")
            return {
                'success': False,
                'channel': 'exception',
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    def push_preview(self, preview_content: str, optimization_type: str) -> Dict[str, Any]:
        """
        推送优化预览版简报
        
        Args:
            preview_content: 预览内容
            optimization_type: 优化类型
            
        Returns:
            推送结果字典
        """
        try:
            # 添加预览标识
            full_preview = f"【优化预览】{optimization_type}\n\n{preview_content}"
            return self.push_brief(full_preview)
            
        except Exception as e:
            self.logger.error(f"推送预览时出错: {e}")
            return {
                'success': False,
                'channel': 'exception',
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    def _try_push_channel(self, channel: str, content: str) -> Dict[str, Any]:
        """尝试指定渠道推送"""
        try:
            if channel not in self.channels:
                return {
                    'success': False,
                    'channel': channel,
                    'error': f'不支持的推送渠道: {channel}',
                    'timestamp': datetime.now().isoformat()
                }
            
            push_func = self.channels[channel]
            success = push_func(content)
            
            return {
                'success': success,
                'channel': channel,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"渠道 {channel} 推送失败: {e}")
            return {
                'success': False,
                'channel': channel,
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    def _push_wechat(self, content: str) -> bool:
        """微信推送（通过OpenClaw）"""
        try:
            # OpenClaw会自动处理微信推送
            # 这里只需要返回True，实际推送由OpenClaw框架处理
            print(content)  # 在OpenClaw环境中，print会自动发送到用户
            return True
            
        except Exception as e:
            self.logger.error(f"微信推送失败: {e}")
            return False
    
    def _push_email(self, content: str) -> bool:
        """邮件推送"""
        try:
            # 获取邮件配置
            smtp_server = self.user_config.get('smtp_server', 'smtp.gmail.com')
            smtp_port = self.user_config.get('smtp_port', 587)
            email_user = self.user_config.get('email_user')
            email_password = self.user_config.get('email_password')
            recipient_email = self.user_config.get('recipient_email')
            
            if not all([smtp_server, email_user, email_password, recipient_email]):
                self.logger.warning("邮件配置不完整")
                return False
            
            # 创建邮件
            msg = MIMEMultipart()
            msg['From'] = email_user
            msg['To'] = recipient_email
            msg['Subject'] = f"新闻简报 - {datetime.now().strftime('%Y-%m-%d')}"
            
            msg.attach(MIMEText(content, 'plain', 'utf-8'))
            
            # 发送邮件
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
            server.login(email_user, email_password)
            text = msg.as_string()
            server.sendmail(email_user, recipient_email, text)
            server.quit()
            
            return True
            
        except Exception as e:
            self.logger.error(f"邮件推送失败: {e}")
            return False
    
    def _push_dingtalk(self, content: str) -> bool:
        """钉钉推送"""
        try:
            webhook_url = self.user_config.get('dingtalk_webhook')
            if not webhook_url:
                self.logger.warning("钉钉Webhook未配置")
                return False
            
            # 钉钉消息格式
            message = {
                "msgtype": "text",
                "text": {
                    "content": content
                }
            }
            
            response = requests.post(webhook_url, json=message, timeout=10)
            return response.status_code == 200
            
        except Exception as e:
            self.logger.error(f"钉钉推送失败: {e}")
            return False
    
    def _push_telegram(self, content: str) -> bool:
        """Telegram推送"""
        try:
            bot_token = self.user_config.get('telegram_bot_token')
            chat_id = self.user_config.get('telegram_chat_id')
            
            if not bot_token or not chat_id:
                self.logger.warning("Telegram配置不完整")
                return False
            
            telegram_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
            payload = {
                'chat_id': chat_id,
                'text': content,
                'parse_mode': 'HTML'
            }
            
            response = requests.post(telegram_url, json=payload, timeout=10)
            return response.status_code == 200
            
        except Exception as e:
            self.logger.error(f"Telegram推送失败: {e}")
            return False
    
    def get_push_status_message(self, push_result: Dict[str, Any]) -> str:
        """
        获取推送状态消息
        
        Args:
            push_result: 推送结果
            
        Returns:
            状态消息字符串
        """
        if push_result['success']:
            return f"✅ 新闻简报已成功推送至{push_result['channel']}"
        else:
            error_msg = push_result.get('error', '未知错误')
            return f"❌ 推送失败: {error_msg}，已尝试备用渠道"
    
    def test_channel_connectivity(self, channel: str) -> Dict[str, Any]:
        """
        测试渠道连通性
        
        Args:
            channel: 渠道名称
            
        Returns:
            测试结果
        """
        try:
            if channel == 'wechat':
                # 微信在OpenClaw中总是可用的
                return {'success': True, 'message': '微信渠道可用'}
            
            elif channel == 'email':
                # 测试SMTP连接
                smtp_server = self.user_config.get('smtp_server')
                smtp_port = self.user_config.get('smtp_port', 587)
                email_user = self.user_config.get('email_user')
                email_password = self.user_config.get('email_password')
                
                if not all([smtp_server, email_user, email_password]):
                    return {'success': False, 'message': '邮件配置不完整'}
                
                server = smtplib.SMTP(smtp_server, smtp_port)
                server.starttls()
                server.login(email_user, email_password)
                server.quit()
                return {'success': True, 'message': '邮件渠道可用'}
                
            elif channel == 'dingtalk':
                webhook = self.user_config.get('dingtalk_webhook')
                if not webhook:
                    return {'success': False, 'message': '钉钉Webhook未配置'}
                
                test_msg = {"msgtype": "text", "text": {"content": "测试消息"}}
                response = requests.post(webhook, json=test_msg, timeout=5)
                if response.status_code == 200:
                    return {'success': True, 'message': '钉钉渠道可用'}
                else:
                    return {'success': False, 'message': f'钉钉渠道不可用: {response.status_code}'}
                    
            elif channel == 'telegram':
                bot_token = self.user_config.get('telegram_bot_token')
                chat_id = self.user_config.get('telegram_chat_id')
                if not bot_token or not chat_id:
                    return {'success': False, 'message': 'Telegram配置不完整'}
                
                test_url = f"https://api.telegram.org/bot{bot_token}/getMe"
                response = requests.get(test_url, timeout=5)
                if response.status_code == 200:
                    return {'success': True, 'message': 'Telegram渠道可用'}
                else:
                    return {'success': False, 'message': f'Telegram渠道不可用: {response.status_code}'}
                    
            else:
                return {'success': False, 'message': f'不支持的渠道: {channel}'}
                
        except Exception as e:
            return {'success': False, 'message': f'测试失败: {str(e)}'}