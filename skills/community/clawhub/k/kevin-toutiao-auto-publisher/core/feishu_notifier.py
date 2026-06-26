#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
飞书通知器 - 发送飞书通知
支持从配置文件读取飞书凭证
"""

import requests
import json
import os


class FeishuNotifier:
    """飞书通知器"""

    def __init__(self, app_id=None, app_secret=None, open_id=None, config_file=None):
        """
        初始化飞书通知器

        Args:
            app_id: 飞书应用ID
            app_secret: 飞书应用密钥
            open_id: 用户OpenID
            config_file: 配置文件路径，包含 feishu_config 字段
        """
        # 如果提供了配置文件，优先从中读取
        if config_file and os.path.exists(config_file):
            with open(config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
            feishu_config = config.get("feishu_config", {})
            self.app_id = app_id or feishu_config.get("app_id")
            self.app_secret = app_secret or feishu_config.get("app_secret")
            self.open_id = open_id or feishu_config.get("open_id")
        else:
            self.app_id = app_id
            self.app_secret = app_secret
            self.open_id = open_id

        self.access_token = None

    def get_tenant_access_token(self):
        """获取租户访问令牌"""
        if not self.app_id or not self.app_secret:
            print("[飞书通知器] 缺少 app_id 或 app_secret 配置，跳过通知")
            return None

        url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
        payload = {
            "app_id": self.app_id,
            "app_secret": self.app_secret
        }

        try:
            response = requests.post(url, json=payload)
            data = response.json()

            if data.get("code") == 0:
                self.access_token = data.get("tenant_access_token")
                return self.access_token
            else:
                print(f"[飞书通知器] 获取访问令牌失败: {data}")
                return None

        except Exception as e:
            print(f"[飞书通知器] 获取访问令牌异常: {e}")
            return None

    def send_notification(self, title, body, notification_type="info"):
        """
        发送飞书通知

        Args:
            title: 通知标题
            body: 通知内容
            notification_type: 通知类型（success/error/warning/info）

        Returns:
            bool: 是否发送成功
        """
        # 获取访问令牌
        if not self.access_token:
            self.get_tenant_access_token()

        if not self.access_token:
            print("[飞书通知器] 无法获取访问令牌，发送通知失败")
            return False

        # 构建消息内容
        message = self._build_message(title, body, notification_type)

        # 发送消息
        url = "https://open.feishu.cn/open-apis/message/v4/send"
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }

        payload = {
            "receive_id": self.open_id,
            "receive_id_type": "open_id",
            "msg_type": "interactive",
            "content": message
        }

        try:
            response = requests.post(url, headers=headers, json=payload)
            data = response.json()

            if data.get("code") == 0:
                print(f"[飞书通知器] 通知发送成功")
                return True
            else:
                print(f"[飞书通知器] 通知发送失败: {data}")
                return False

        except Exception as e:
            print(f"[飞书通知器] 发送通知异常: {e}")
            return False

    def _build_message(self, title, body, notification_type):
        """
        构建飞书消息内容

        Args:
            title: 通知标题
            body: 通知内容
            notification_type: 通知类型

        Returns:
            dict: 消息内容
        """
        # 根据类型选择图标
        icons = {
            "success": "🎉",
            "error": "❌",
            "warning": "⚠️",
            "info": "ℹ️"
        }

        icon = icons.get(notification_type, "ℹ️")

        # 构建卡片消息
        card_content = {
            "config": {
                "wide_screen_mode": True
            },
            "header": {
                "title": {
                    "content": f"{icon} {title}",
                    "tag": "plain_text"
                },
                "template": notification_type
            },
            "elements": [
                {
                    "tag": "div",
                    "text": {
                        "content": body,
                        "tag": "lark_md"
                    }
                },
                {
                    "tag": "hr"
                },
                {
                    "tag": "div",
                    "text": {
                        "content": f"发送时间: {self._get_current_time()}",
                        "tag": "plain_text"
                    }
                }
            ]
        }

        return card_content

    def _get_current_time(self):
        """获取当前时间"""
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def main():
    """测试飞书通知器"""
    notifier = FeishuNotifier()

    # 测试发送通知
    success = notifier.send_notification(
        title="测试通知",
        body="这是一条测试通知消息。",
        notification_type="success"
    )

    print(f"通知发送结果: {'成功' if success else '失败'}")


if __name__ == "__main__":
    main()
