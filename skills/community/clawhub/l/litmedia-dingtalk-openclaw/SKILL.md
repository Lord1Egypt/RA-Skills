---
name: dingtalk-openclaw
description: 钉钉 Stream 模式连接 OpenClaw AI 对话。通过钉钉机器人接收用户消息，调用 OpenClaw HTTP API 获取 AI 回复，再用 Webhook 发回钉钉。用于实现"钉钉 AI 助手"场景。
---

# 钉钉连接 OpenClaw

本 skill 指导你将钉钉机器人连接到 OpenClaw，实现通过钉钉与 AI 对话。

## 架构

```
钉钉消息 → dingtalk_stream → OpenClaw API → AI回复 → 钉钉Webhook → 用户
```

## 前置条件

1. 钉钉企业应用（创建应用并开通 Stream 模式）
2. OpenClaw 已运行并启用 HTTP API
3. Python 3.8+

## 配置步骤

### 1. 安装依赖

```bash
pip install dingtalk-stream requests
```

### 2. 创建配置文件 config.py

```python
# -*- coding: utf-8 -*-

# 钉钉应用凭证（从钉钉开放平台获取）
AGENT_ID = "你的AgentId"
APP_KEY = "你的AppKey"
APP_SECRET = "你的AppSecret"

# 机器人消息回调Topic
BOT_MESSAGE_TOPIC = "/v1.0/im/bot/messages/get"

# 日志配置
LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_FILE = "logs/dingtalk_stream.log"
```

### 3. 创建主程序 main.py

```python
# -*- coding: utf-8 -*-
"""
钉钉机器人 Stream 模式 - 连接 OpenClaw AI
"""

import sys
import logging
import requests
from pathlib import Path

try:
    import dingtalk_stream
    from dingtalk_stream import AckMessage
except ImportError:
    print("请先安装: pip install dingtalk-stream")
    sys.exit(1)

import config

# ============ 配置区域（根据你的环境修改）============
# OpenClaw API 地址
OPENCLAW_URL = "http://127.0.0.1:18789/v1/responses"
# OpenClaw Gateway Token（在 openclaw.json 中配置）
OPENCLAW_TOKEN = "你的OpenClaw_Token"

# 钉钉 Webhook（用于发送回复）
# 创建机器人后获取：群设置 → 智能群助手 → 添加机器人 → 自定义机器人
WEBHOOK_URL = "你的钉钉Webhook_URL"
# ==================================================

PROCESSED_FILE = Path("C:/Users/MyPC/.openclaw/workspace/dingtalk_processed.txt")
PROCESSED_IDS = set()

def load_processed():
    global PROCESSED_IDS
    if PROCESSED_FILE.exists():
        with open(PROCESSED_FILE, "r", encoding="utf-8") as f:
            PROCESSED_IDS = set(line.strip() for line in f if line.strip())

def save_processed(msg_id):
    with open(PROCESSED_FILE, "a", encoding="utf-8") as f:
        f.write(msg_id + "\n")
    PROCESSED_IDS.add(msg_id)

# 调用 OpenClaw AI
def get_openclaw_response(user_msg: str) -> str:
    try:
        headers = {
            "Authorization": f"Bearer {OPENCLAW_TOKEN}",
            "Content-Type": "application/json"
        }
        data = {
            "model": "openclaw",
            "input": user_msg
        }
        r = requests.post(OPENCLAW_URL, headers=headers, json=data, timeout=60)
        if r.status_code == 200:
            result = r.json()
            output = result.get("output", [])
            if output:
                content = output[0].get("content", [])
                if content:
                    return content[0].get("text", "抱歉，我无法回答这个问题。")
        logging.error(f"OpenClaw API 错误: {r.status_code} {r.text}")
        return "抱歉，我现在有点忙，请稍后再试。"
    except Exception as e:
        logging.error(f"调用 OpenClaw 失败: {e}")
        return "抱歉，连接出现问题，请稍后再试。"

# 发送回复到钉钉
def send_reply(content):
    data = {
        "msgtype": "text",
        "text": {"content": content},
        "at": {"atUserIds": [], "isAtAll": False}
    }
    try:
        r = requests.post(WEBHOOK_URL, json=data, timeout=10)
        result = r.json()
        logging.info(f"回复结果: {result}")
        return result.get("errcode", 1) == 0
    except Exception as e:
        logging.error(f"发送失败: {e}")
        return False

# 消息处理器
class Handler(dingtalk_stream.ChatbotHandler):
    def __init__(self):
        super().__init__()
    
    async def process(self, callback):
        try:
            msg = dingtalk_stream.ChatbotMessage.from_dict(callback.data)
            content = msg.text.content if msg.text else ""
            
            if not content:
                return AckMessage.STATUS_OK, 'OK'
            
            msg_id = f"{msg.conversation_id}_{msg.sender_id}_{len(content)}"
            
            if msg_id in PROCESSED_IDS:
                logging.info(f"重复消息，跳过: {content[:20]}")
                return AckMessage.STATUS_OK, 'OK'
            
            save_processed(msg_id)
            logging.info(f"收到: {content}")
            
            # 获取 AI 回复
            response = get_openclaw_response(content)
            logging.info(f"回复: {response}")
            
            # 发送到钉钉
            send_reply(response)
            
            return AckMessage.STATUS_OK, 'OK'
        except Exception as e:
            logging.error(f"处理失败: {e}")
            return AckMessage.STATUS_ERROR, str(e)

def main():
    print("=" * 50)
    print("  钉钉 + OpenClaw AI 对话机器人")
    print("=" * 50)
    
    load_processed()
    logging.info(f"已加载 {len(PROCESSED_IDS)} 条已处理消息")
    
    credential = dingtalk_stream.Credential(config.APP_KEY, config.APP_SECRET)
    client = dingtalk_stream.DingTalkStreamClient(credential)
    client.register_callback_handler(dingtalk_stream.ChatbotMessage.TOPIC, Handler())
    
    logging.info("正在连接钉钉...")
    client.start_forever()

if __name__ == "__main__":
    main()
```

### 4. 启用 OpenClaw HTTP API

编辑 `C:\Users\MyPC\.openclaw\openclaw.json`，添加：

```json
{
  "gateway": {
    "http": {
      "endpoints": {
        "responses": {
          "enabled": true
        }
      }
    }
  }
}
```

重启 OpenClaw Gateway 后生效。

### 5. 运行

```bash
python main.py
```

## 注意事项

1. **APP_KEY 和 APP_SECRET** 在钉钉开放平台的企业应用详情页获取
2. **WEBHOOK_URL** 创建自定义机器人后获取，注意安全设置（加签）
3. **OPENCLAW_TOKEN** 在 openclaw.json 的 `gateway.auth.token` 中查看
4. 确保 OpenClaw Gateway 运行在 `127.0.0.1:18789`

## 调试

查看日志文件 `logs/dingtalk_stream.log` 排查问题。
