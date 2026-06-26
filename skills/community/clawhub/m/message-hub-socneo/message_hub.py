#!/usr/bin/env python3
"""
Message Hub - AI 团队消息枢纽客户端
AI 团队消息枢纽的 Python 客户端

作者：AI Team Collaboration
  - 天马 (阿里云 OpenClaw) - 核心开发
  - 小八 (WorkBuddy) - 安全审计 & Hub 集成
  - 小卷 (OpenClaw) - 安全审查
  - 小零 (飞书助手) - 文档整理
发布者：socneo
版本：v1.0.0
日期：2026-03-17
"""

import os
import json
import time
import hmac
import hashlib
import requests
from datetime import datetime
from typing import Dict, List, Optional

class MessageHubError(Exception):
    """消息枢纽错误基类"""
    pass

class AuthError(MessageHubError):
    """认证错误"""
    pass

class RetryError(MessageHubError):
    """重试错误"""
    pass

class MessageHub:
    """AI 团队消息枢纽客户端"""
    
    def __init__(self, base_url: Optional[str] = None, api_key: Optional[str] = None,
                 sender: Optional[str] = None, retry_times: int = 3, retry_delay: int = 5):
        """
        初始化消息枢纽客户端
        
        Args:
            base_url: 消息枢纽地址（可从 MESSAGE_HUB_URL 环境变量读取）
            api_key: API Key（可从 MESSAGE_HUB_API_KEY 环境变量读取）
            sender: 发送者名称（可从 MESSAGE_HUB_SENDER 环境变量读取）
            retry_times: 重试次数
            retry_delay: 重试延迟（秒）
        """
        self.base_url = base_url or os.getenv("MESSAGE_HUB_URL", "http://localhost:8000")
        self.api_key = api_key or os.getenv("MESSAGE_HUB_API_KEY")
        self.sender = sender or os.getenv("MESSAGE_HUB_SENDER", "Unknown")
        self.retry_times = retry_times
        self.retry_delay = retry_delay
        
        if not self.api_key:
            raise ValueError("API Key 必须配置（通过参数或 MESSAGE_HUB_API_KEY 环境变量）")
        
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json",
            "X-API-Key": self.api_key
        })
    
    def _request(self, method: str, endpoint: str, data: Optional[Dict] = None) -> Dict:
        """发送 HTTP 请求（带重试）"""
        url = f"{self.base_url}{endpoint}"
        
        for attempt in range(self.retry_times):
            try:
                response = self.session.request(method, url, json=data, timeout=30)
                response.raise_for_status()
                return response.json()
            except requests.exceptions.RequestException as e:
                if attempt == self.retry_times - 1:
                    raise RetryError(f"请求失败（已重试{self.retry_times}次）: {e}")
                time.sleep(self.retry_delay * (attempt + 1))
    
    def _sign_message(self, message: Dict) -> str:
        """生成消息签名"""
        msg_data = json.dumps({
            "message_id": message.get("message_id"),
            "sender": message.get("sender"),
            "content": message.get("content"),
            "timestamp": message.get("timestamp")
        }, sort_keys=True)
        return hmac.new(self.api_key.encode(), msg_data.encode(), hashlib.sha256).hexdigest()
    
    def push_message(self, message_type: str, recipients: List[str], content: Dict,
                     priority: str = "medium", task_type: str = "general") -> Dict:
        """
        推送消息到中转站
        
        Args:
            message_type: 消息类型（task/notification/response/broadcast）
            recipients: 接收者列表
            content: 消息内容
            priority: 优先级（high/medium/low）
            task_type: 任务类型
        
        Returns:
            API 响应结果
        """
        message = {
            "message_type": message_type,
            "sender": self.sender,
            "recipients": recipients,
            "priority": priority,
            "task_type": task_type,
            "content": content,
            "timestamp": datetime.now().isoformat()
        }
        
        # 添加签名
        message["signature"] = self._sign_message(message)
        
        result = self._request("POST", "/api/v1/message/push", message)
        return result
    
    def pull_messages(self, receiver: Optional[str] = None) -> List[Dict]:
        """
        拉取待处理消息
        
        Args:
            receiver: 接收者（默认为初始化时设置的 sender）
        
        Returns:
            消息列表
        """
        receiver = receiver or self.sender
        result = self._request("GET", f"/api/v1/message/pull/{receiver}")
        return result.get("messages", [])
    
    def broadcast_message(self, content: Dict, priority: str = "medium") -> Dict:
        """
        广播消息到飞书群（仅天马可用）
        
        Args:
            content: 消息内容
            priority: 优先级
        
        Returns:
            API 响应结果
        """
        message = {
            "message_type": "broadcast",
            "sender": self.sender,
            "recipients": ["all"],
            "priority": priority,
            "content": content,
            "timestamp": datetime.now().isoformat()
        }
        
        message["signature"] = self._sign_message(message)
        
        result = self._request("POST", "/api/v1/message/broadcast", message)
        return result
    
    def send_task(self, recipient: str, task_text: str, priority: str = "medium",
                  task_type: str = "general") -> Dict:
        """
        便捷方法：发送任务
        
        Args:
            recipient: 接收者
            task_text: 任务内容
            priority: 优先级
            task_type: 任务类型
        
        Returns:
            API 响应结果
        """
        return self.push_message(
            message_type="task",
            recipients=[recipient],
            content={"text": task_text},
            priority=priority,
            task_type=task_type
        )
    
    def send_notification(self, recipients: List[str], notification_text: str,
                          priority: str = "low") -> Dict:
        """
        便捷方法：发送通知
        
        Args:
            recipients: 接收者列表
            notification_text: 通知内容
            priority: 优先级
        
        Returns:
            API 响应结果
        """
        return self.push_message(
            message_type="notification",
            recipients=recipients,
            content={"text": notification_text},
            priority=priority
        )
    
    def health_check(self) -> Dict:
        """
        健康检查
        
        Returns:
            服务状态信息
        """
        result = self._request("GET", "/api/v1/health")
        return result
    
    def get_stats(self) -> Dict:
        """
        获取统计信息
        
        Returns:
            统计信息
        """
        result = self._request("GET", "/api/v1/stats")
        return result


# CLI 工具
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="AI 团队消息枢纽客户端")
    parser.add_argument("command", choices=["push", "pull", "broadcast", "health", "stats"],
                        help="命令：push（推送）, pull（拉取）, broadcast（广播）, health（健康检查）, stats（统计）")
    parser.add_argument("--type", dest="msg_type", default="task",
                        choices=["task", "notification", "response", "broadcast"],
                        help="消息类型")
    parser.add_argument("--to", nargs="+", help="接收者列表（push 命令使用）")
    parser.add_argument("--content", help="消息内容")
    add_argument("--priority", default="medium", choices=["high", "medium", "low"],
                        help="优先级")
    parser.add_argument("--task-type", default="general", help="任务类型")
    
    args = parser.parse_args()
    
    hub = MessageHub()
    
    if args.command == "push":
        if not all([args.to, args.content]):
            print("❌ 错误：push 命令需要 --to 和 --content 参数")
            exit(1)
        
        result = hub.push_message(
            message_type=args.msg_type,
            recipients=args.to,
            content={"text": args.content},
            priority=args.priority,
            task_type=args.task_type
        )
        print(f"✅ 消息推送成功！")
        print(f"   消息 ID: {result.get('message_id')}")
    
    elif args.command == "pull":
        messages = hub.pull_messages()
        if messages:
            print(f"📬 收到 {len(messages)} 条消息：")
            for msg in messages:
                print(f"  [{msg['priority']}] {msg['sender']}: {msg['content'].get('text', 'N/A')}")
        else:
            print("ℹ️ 无新消息")
    
    elif args.command == "broadcast":
        if not args.content:
            print("❌ 错误：broadcast 命令需要 --content 参数")
            exit(1)
        
        result = hub.broadcast_message({"text": args.content}, args.priority)
        print(f"✅ 广播成功！")
    
    elif args.command == "health":
        status = hub.health_check()
        print(f"🏥 健康状态：{status['status']}")
        print(f"   版本：{status['version']}")
        print(f"   运行时长：{status['uptime']:.2f} 小时")
        print(f"   消息数：{status['message_count']}")
        print(f"   活跃用户：{status['active_recipients']}")
    
    elif args.command == "stats":
        stats = hub.get_stats()
        print(f"📊 统计信息：")
        print(f"   存储：{stats.get('store', {})}")
        print(f"   配置：{stats.get('config', {})}")
