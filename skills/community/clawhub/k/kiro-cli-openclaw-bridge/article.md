# 让 Kiro CLI 突破终端限制：我用 ACP 协议打通了 OpenClaw

> 通过 ACP 协议将 Kiro CLI 的 AI 能力从终端中解放出来，接入 OpenClaw 的多平台生态。

## 起因

Kiro CLI 是一个强大的 AI 编程助手，但它被锁在终端里。每次使用都要开一个终端窗口，对话体验受限于命令行界面。

而 OpenClaw 是一个开源的 AI Agent 平台，支持多种聊天渠道（Telegram、Discord、Slack、飞书……），有完善的对话管理、技能系统和插件生态。

我想：**能不能让 OpenClaw 直接调用 Kiro CLI 的 AI 后端？**

这样就能在任何 OpenClaw 支持的渠道里，享受 Kiro 的代码理解、文件操作和终端执行能力。

## 发现 ACP 协议

翻看 `kiro-cli --help-all`，发现了一个关键子命令：

```
kiro-cli acp
```

ACP（Agent Client Protocol）是 Kiro CLI 暴露的标准化通信接口，基于 JSON-RPC 2.0，通过 stdio 管道通信。这意味着：

- 可以通过子进程与 Kiro 的 AI 后端建立持久连接
- 支持会话管理、流式响应、工具调用
- 不需要逆向工程，这是官方公开的集成点

## 架构设计

思路很清晰——写一个本地 HTTP 代理，把 OpenAI 格式的请求翻译成 ACP 协议：

```
OpenClaw / 任意客户端  ──HTTP──▶  Bridge (FastAPI)  ──stdio──▶  kiro-cli acp
                                  :18788/v1                     JSON-RPC 2.0
```

Bridge 做三件事：
1. 维护一个持久的 `kiro-cli acp` 子进程
2. 在 OpenAI Chat Completion API 和 ACP JSON-RPC 之间双向翻译
3. 将 ACP 的流式通知实时转换为 SSE 推送

## 技术实现

### 核心挑战

**1. 子进程生命周期管理**

`kiro-cli acp` 启动后需要完成 JSON-RPC 的 `initialize` 握手，之后保持长连接。如果进程意外退出，需要自动重启并重新初始化。

**2. 异步消息分发**

ACP 通过 stdout 输出两种消息：
- **Response**（带 `id`）：对应请求的响应
- **Notification**（无 `id`）：`session/update` 通知，包含流式文本块

需要一个异步读取器持续监听 stdout，根据消息类型分发到不同的 Future 或 Queue。

**3. 流式响应转换**

ACP 的 `agent_message_chunk` 通知需要实时转换为 OpenAI 的 SSE `chat.completion.chunk` 格式，同时处理工具调用中间状态（不产生文本输出但不能中断流）。

**4. 工具调用代理**

Kiro 的 agent 在执行过程中会请求文件读写和终端命令。Bridge 需要响应这些请求，在指定的项目目录内执行操作并返回结果。

### 技术栈

- **Python 3.10+** + **FastAPI** + **uvicorn**
- **asyncio** 子进程管理和并发
- **PyInstaller** 打包为单文件可执行程序（~15MB）

## 使用效果

配置完成后，在 OpenClaw 中选择 `kiro-b/kiro-acp` 模型，就能像使用 Claude 或 GPT 一样与 Kiro 对话：

- ✅ 流式响应，逐字输出
- ✅ 代码理解和生成
- ✅ 文件读写操作（受限于指定项目目录）
- ✅ 终端命令执行
- ✅ 上下文溢出自动重建会话

## 5 分钟快速上手

### 1. 确保 kiro-cli 已认证

```bash
kiro-cli login
```

### 2. 启动 Bridge

```bash
git clone https://github.com/LuoShiXi/kiro-cli-openclaw-bridge.git
cd kiro-cli-openclaw-bridge
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python -m acp_openai_bridge.main --cwd /your/project
```

### 3. 配置 OpenClaw

编辑 `~/.openclaw/openclaw.json`：

```json
{
  "models": {
    "mode": "merge",
    "providers": {
      "kiro-b": {
        "api": "openai-completions",
        "baseUrl": "http://127.0.0.1:18788/v1",
        "apiKey": "local-cli",
        "models": [
          {
            "id": "kiro-acp",
            "name": "Kiro ACP",
            "input": ["text"],
            "contextWindow": 200000,
            "maxTokens": 65536
          }
        ]
      }
    }
  }
}
```

重启 OpenClaw，选择 `kiro-b/kiro-acp` 模型，开始对话。

## 跨平台支持

| 平台 | 状态 |
|------|------|
| Windows（原生 / WSL） | ✅ 支持，可打包为 .exe |
| macOS（Apple Silicon / Intel） | ✅ 支持 |
| Linux | ✅ 支持 |

## 开源地址

- **Bridge 源码**：https://github.com/LuoShiXi/kiro-cli-openclaw-bridge
- **OpenClaw Skill**：https://github.com/LuoShiXi/kiro-cli-openclaw-skill
- **ClawHub**：`clawhub install kiro-cli-openclaw-bridge`

协议：CC BY-NC 4.0（允许自由使用和修改，禁止商业用途）

## 写在最后

这个项目的核心价值在于：**让 Kiro CLI 的 AI 能力不再局限于终端**。通过 ACP 这个官方公开的协议接口，任何支持 OpenAI API 格式的客户端都能接入 Kiro 的后端。

如果你也在用 Kiro CLI，不妨试试这个 Bridge。有问题欢迎在 GitHub 提 Issue。

---

**免责声明**：本项目为非官方社区工具，与 AWS、Kiro 无关联。用户需使用自己的 Kiro CLI 认证账号，并遵守相关服务条款。
