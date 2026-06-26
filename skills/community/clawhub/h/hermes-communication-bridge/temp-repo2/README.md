# Hermes-WorkBuddy 通信桥

> 通过共享文件队列（`queue.json`）实现 WorkBuddy 与 Hermes Agent 的双向直接通信，无需外部服务依赖。

## 架构

```
WorkBuddy  ←── queue.json ──▶  Hermes
              (每小时 cron)
```

## 核心文件

| 文件 | 用途 |
|------|------|
| `scripts/communication_queue.py` | 队列管理器（CommunicationQueue 类） |
| `scripts/hermes_comm.py` | WorkBuddy 侧 CLI 工具 |
| `scripts/process_queue.py` | Hermes 侧消息处理器 |
| `scripts/auto_poller.py` | 持续轮询脚本（测试用） |
| `config/default_config.json` | 队列默认配置 |
| `config/message_types.json` | 消息类型定义 |

## 快速开始

### WorkBuddy → Hermes 发消息

```bash
python3 ~/.workbuddy/skills/hermes-communication-bridge/scripts/hermes_comm.py send -c "你好 Hermes！"
```

### 收取 Hermes 回复

```bash
python3 ~/.workbuddy/skills/hermes-communication-bridge/scripts/hermes_comm.py receive
```

### Hermes 侧配置 Cron（每小时自动处理）

```bash
hermes cron create --script ~/.workbuddy/skills/hermes-communication-bridge/scripts/process_queue.py "every 1h"
```

## 队列存储

- 队列文件：`~/.hermes/shared/communication/queue.json`
- 历史文件：`~/.hermes/shared/communication/history.json`

## 依赖

- Python 3.10+
- Hermes Agent（已安装并运行）

## 许可证

MIT
