---
name: slack-helper
description: Slack助手 - 发送消息/搜索历史/管理频道/集成通知，基于Slack API的Python实现，支持Webhook和Socket Mode
metadata: {"openclaw": {"requires": {"python": ["slack-sdk", "aiohttp"]}, "install": ["pip install slack-sdk aiohttp"]}}
tags: [slack, messaging, notification, team, communication, webhook, bot]
version: 1.0.0
author: laosi
source: adapted
---

# Slack Helper - Slack助手

> 激活词: Slack / 消息 / 通知 / 团队

## 安装

```bash
pip install slack-sdk aiohttp
```

## 获取Token

1. 访问 https://api.slack.com/apps
2. 创建新App → 选择 "From scratch"
3. 添加 Bot Token Scopes: `chat:write`, `channels:read`, `channels:history`
4. 安装App到工作区，复制 Bot User OAuth Token

## Python实现

### 1. 发送消息到频道

```python
from slack_sdk import WebClient

class SlackHelper:
    def __init__(self, token: str):
        self.client = WebClient(token=token)
    
    def post_message(self, channel: str, text: str, blocks: list = None):
        """发送文本或富文本消息"""
        params = {"channel": channel, "text": text}
        if blocks:
            params["blocks"] = blocks
        resp = self.client.chat_postMessage(**params)
        return resp["ts"]  # 消息时间戳，可用于回复/编辑
    
    def post_blocks(self, channel: str, blocks: list, fallback: str = ""):
        """发送Block Kit富消息"""
        return self.post_message(channel, fallback, blocks=blocks)

slack = SlackHelper("xoxb-your-token-here")
slack.post_message("#general", "Hello from AI assistant!")
```

### 2. Block Kit 富消息模板

```python
def alert_block(title: str, message: str, severity: str = "warning"):
    colors = {"info": "#3498db", "warning": "#f39c12", "error": "#e74c3c", "success": "#2ecc71"}
    return [
        {
            "type": "header",
            "text": {"type": "plain_text", "text": f"⚠️ {title}"}
        },
        {
            "type": "section",
            "text": {"type": "mrkdwn", "text": message}
        },
        {
            "type": "context",
            "elements": [{"type": "mrkdwn", "text": f"Severity: *{severity}*"}]
        }
    ]

slack.post_blocks("#alerts", alert_block("Deploy Failed", "Build #42 failed on staging"))
```

### 3. 频道列表和管理

```python
def list_channels(self, limit: int = 100):
    """列出所有公开频道"""
    resp = self.client.conversations_list(limit=limit)
    return [{"id": c["id"], "name": c["name"], "members": c.get("num_members", 0)}
            for c in resp["channels"]]

def create_channel(self, name: str, is_private: bool = False):
    """创建频道"""
    resp = self.client.conversations_create(name=name, is_private=is_private)
    return resp["channel"]["id"]

def invite_to_channel(self, channel_id: str, user_ids: list):
    """邀请用户到频道"""
    self.client.conversations_invite(channel=channel_id, users=",".join(user_ids))
```

### 4. 搜索历史消息

```python
def search_messages(self, query: str, limit: int = 10):
    """搜索消息历史"""
    resp = self.client.search_messages(query=query, count=limit)
    results = []
    for msg in resp["messages"]["matches"]:
        results.append({
            "channel": msg["channel"]["name"],
            "user": msg.get("username", msg.get("user", "unknown")),
            "text": msg["text"][:200],
            "ts": msg["ts"],
            "permalink": msg.get("permalink", "")
        })
    return results

def get_channel_history(self, channel_id: str, limit: int = 50):
    """获取频道最近消息"""
    resp = self.client.conversations_history(channel=channel_id, limit=limit)
    return [{"user": m.get("user", "unknown"), "text": m["text"][:200], "ts": m["ts"]}
            for m in resp["messages"]]
```

### 5. Webhook方式（无需Bot Token）

```python
import requests
import json

def send_via_webhook(webhook_url: str, text: str):
    """通过Incoming Webhook发送消息"""
    payload = {"text": text}
    resp = requests.post(webhook_url, json=payload)
    return resp.status_code == 200

# 创建Webhook: Slack API → Incoming Webhooks → Add New Webhook
send_via_webhook("https://hooks.slack.com/services/T00/B00/xxxxx",
                 "Deployment complete: v2.3.1 is live!")
```

### 6. 文件上传

```python
def upload_file(self, channel_id: str, filepath: str, title: str = ""):
    """上传文件到频道"""
    with open(filepath, "rb") as f:
        resp = self.client.files_upload_v2(
            channel=channel_id,
            file=f,
            title=title or os.path.basename(filepath)
        )
    return resp["file"]["permalink"]
```

## 使用场景

1. **自动通知**: CI/CD部署状态、监控告警、定时报告推送
2. **团队协作**: AI助手自动回复常见问题、创建任务频道
3. **消息存档**: 按关键词搜索历史，追溯决策记录
4. **告警集成**: 服务宕机、错误率飙升时自动通知值班人员
5. **文件分发**: 自动分享报表、日志到指定频道

## 配置

```yaml
token: "xoxb-xxxxxxxxxxxx"
default_channel: "#general"
webhook_url: "https://hooks.slack.com/services/..."
bot_name: "AI Assistant"
bot_icon: ":robot_face:"
```

## 错误处理

```python
def safe_post(self, channel: str, text: str) -> bool:
    try:
        self.post_message(channel, text)
        return True
    except SlackApiError as e:
        if e.response["error"] == "not_in_channel":
            self.client.conversations_join(channel=channel)
            return self.safe_post(channel, text)
        elif e.response["error"] == "channel_not_found":
            print(f"Channel not found: {channel}")
            return False
        else:
            print(f"Slack API error: {e.response['error']}")
            return False
```
