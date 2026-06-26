---
name: openclaw-aligenie-genie
version: "1.0.0"
description: OpenClaw Agent 通过云服务器与天猫精灵双向通信的技能。触发时机：(1) 用户要求与天猫精灵通信或接收天猫精灵消息时 (2) 配置天猫精灵与 OpenClaw 的连接时 (3) 天猫精灵发送指令到 OpenClaw 需要处理时。
---

# openclaw-aligenie-genie

> OpenClaw Agent 通过云服务器与天猫精灵双向通信的技能。

## 文档

| 文档 | 内容 |
|------|------|
| `SPEC.md` | 完整技术规格（架构/数据库/API/安全） |
| `DEPLOY.md` | 部署指南 |
| `genie_client.py` | Agent 端 Python 客户端 |

## 快速开始

### 1. 部署云服务器

详见 `DEPLOY.md`

### 2. 配置 Agent

```bash
ALIGENIE_SERVER=http://你的云服务器IP:58472
ALIGENIE_API_KEY=ak_xxx   # 从 CLI 获取
ALIGENIE_AGENT_ID=lobster  # 你的 agent ID
```

### 3. 启动注册

```python
from genie_client import GenieClient

client = GenieClient(
    server_url="http://101.43.110.225:58472",
    agent_id="lobster",
    api_key="ak_xxx"
)
client.register("session_key_here")
client.start_heartbeat_loop(interval=60)
```

### 4. 处理请求

```python
def handle(req):
    utterance = req["utterance"]
    reply = f"你说了：{utterance}"
    return reply

client.start_polling_loop(handle)
```

## 架构

详见 `SPEC.md`

## 前置条件

1. 云服务器已部署 AligenieServer
2. 阿里云开发者账号已创建个人技能（Genie2）
3. 用户已在天猫精灵App 添加技能
