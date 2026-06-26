"""
WeChat Notifier Module
负责通过微信发送通知
"""

import requests
import json
import logging
from typing import Dict, Any, Optional
from datetime import datetime

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class WeChatNotifier:
    def __init__(self, corp_id: str = None, secret: str = None, agent_id: int = None):
        """
        初始化微信通知器
        
        Args:
            corp_id: 企业微信CorpID
            secret: 企业微信Secret
            agent_id: 企业微信应用ID
        """
        self.corp_id = corp_id
        self.secret = secret
        self.agent_id = agent_id
        self.access_token = None
        self.token_expires_at = None
        
    def _get_access_token(self) -> str:
        """
        获取企业微信access_token
        
        Returns:
            access_token字符串
        """
        if not self.corp_id or not self.secret:
            logger.warning("缺少企业微信配置信息，无法获取access_token")
            return ""
            
        try:
            url = f"https://qyapi.weixin.qq.com/cgi-bin/gettoken"
            params = {
                "corpid": self.corp_id,
                "corpsecret": self.secret
            }
            
            response = requests.get(url, params=params)
            result = response.json()
            
            if result.get("errcode") == 0:
                self.access_token = result.get("access_token")
                # token有效期为7200秒，提前10分钟刷新
                self.token_expires_at = datetime.now().timestamp() + 7100
                logger.info("成功获取access_token")
                return self.access_token
            else:
                logger.error(f"获取access_token失败: {result}")
                return ""
                
        except Exception as e:
            logger.error(f"获取access_token异常: {e}")
            return ""
    
    def _is_token_valid(self) -> bool:
        """检查access_token是否有效"""
        if not self.access_token:
            return False
        if not self.token_expires_at:
            return False
        return datetime.now().timestamp() < self.token_expires_at
    
    def send_notification(self, users: list, message: str, 
                         title: str = "Issue Request通知") -> bool:
        """
        发送微信通知
        
        Args:
            users: 接收者用户列表
            message: 通知消息内容
            title: 消息标题
            
        Returns:
            发送是否成功
        """
        # 检查是否需要获取token
        if not self._is_token_valid():
            token = self._get_access_token()
            if not token:
                logger.error("无法获取有效的access_token，通知发送失败")
                return False
        
        try:
            # 构造消息内容
            msg_content = {
                "touser": "|".join(users),  # 多个用户用|分隔
                "msgtype": "text",
                "agentid": self.agent_id,
                "text": {
                    "content": f"{title}\n\n{message}"
                },
                "safe": 0
            }
            
            # 发送消息
            url = f"https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={self.access_token}"
            headers = {"Content-Type": "application/json; charset=utf-8"}
            
            response = requests.post(url, 
                                  data=json.dumps(msg_content, ensure_ascii=False).encode('utf-8'),
                                  headers=headers)
            
            result = response.json()
            
            if result.get("errcode") == 0:
                logger.info(f"微信通知发送成功，接收者: {users}")
                return True
            else:
                logger.error(f"微信通知发送失败: {result}")
                return False
                
        except Exception as e:
            logger.error(f"发送微信通知异常: {e}")
            return False
    
    def notify_new_issue(self, issue: Dict[str, Any], recipients: list) -> bool:
        """
        通知新创建的Issue
        
        Args:
            issue: Issue对象
            recipients: 接收者列表
            
        Returns:
            发送是否成功
        """
        message = (
            f"📌 新建Issue!\n"
            f"ID: {issue.get('id', 'N/A')}\n"
            f"标题: {issue.get('title', 'N/A')}\n"
            f"类型: {issue.get('type', 'N/A')}\n"
            f"优先级: {issue.get('priority', 'N/A')}\n"
            f"描述: {issue.get('description', 'N/A')[:100]}...\n"
            f"创建时间: {issue.get('created_at', 'N/A')}"
        )
        
        title = f"新Issue: {issue.get('title', '无标题')}"
        return self.send_notification(recipients, message, title)
    
    def notify_issue_update(self, issue: Dict[str, Any], 
                           update_type: str, recipients: list) -> bool:
        """
        通知Issue更新
        
        Args:
            issue: Issue对象
            update_type: 更新类型 (status_changed, assigned, commented)
            recipients: 接收者列表
            
        Returns:
            发送是否成功
        """
        # 根据更新类型构造消息
        if update_type == "status_changed":
            message = (
                f"🔄 Issue状态变更!\n"
                f"ID: {issue.get('id', 'N/A')}\n"
                f"标题: {issue.get('title', 'N/A')}\n"
                f"新状态: {issue.get('status', 'N/A')}\n"
                f"更新时间: {issue.get('updated_at', 'N/A')}"
            )
            title = f"Issue状态更新: {issue.get('title', '无标题')}"
            
        elif update_type == "assigned":
            message = (
                f"🎯 Issue已分配!\n"
                f"ID: {issue.get('id', 'N/A')}\n"
                f"标题: {issue.get('title', 'N/A')}\n"
                f"分配给: {issue.get('assignee', 'N/A')}\n"
                f"分配时间: {issue.get('updated_at', 'N/A')}"
            )
            title = f"Issue分配: {issue.get('title', '无标题')}"
            
        elif update_type == "commented":
            message = (
                f"💬 新评论!\n"
                f"ID: {issue.get('id', 'N/A')}\n"
                f"标题: {issue.get('title', 'N/A')}\n"
                f"评论时间: {issue.get('updated_at', 'N/A')}"
            )
            title = f"新评论: {issue.get('title', '无标题')}"
            
        else:
            message = (
                f"🔔 Issue更新!\n"
                f"ID: {issue.get('id', 'N/A')}\n"
                f"标题: {issue.get('title', 'N/A')}\n"
                f"更新类型: {update_type}\n"
                f"更新时间: {issue.get('updated_at', 'N/A')}"
            )
            title = f"Issue更新: {issue.get('title', '无标题')}"
            
        return self.send_notification(recipients, message, title)
    
    def notify_issue_closed(self, issue: Dict[str, Any], recipients: list) -> bool:
        """
        通知Issue关闭
        
        Args:
            issue: Issue对象
            recipients: 接收者列表
            
        Returns:
            发送是否成功
        """
        message = (
            f"✅ Issue已关闭!\n"
            f"ID: {issue.get('id', 'N/A')}\n"
            f"标题: {issue.get('title', 'N/A')}\n"
            f"关闭时间: {issue.get('updated_at', 'N/A')}\n"
            f"最终状态: {issue.get('status', 'N/A')}"
        )
        
        title = f"Issue关闭: {issue.get('title', '无标题')}"
        return self.send_notification(recipients, message, title)

# 使用示例
if __name__ == "__main__":
    # 注意：实际使用时需要配置真实的企业微信参数
    notifier = WeChatNotifier(
        corp_id="your_corp_id",
        secret="your_secret", 
        agent_id=1000001
    )
    
    # 测试发送通知
    # notifier.send_notification(["user1", "user2"], "测试通知内容")