# 让 Kiro CLI 突破终端限制：我用 ACP 协议打通了 OpenClaw

## Kiro CLI 很强，但被困在终端里

如果你用过 Kiro CLI，一定体会过它的强大——代码理解、文件操作、终端执行，几乎是一个完整的 AI 编程搭档。

但问题是：**它只能在终端里用。**

每次都要开一个终端窗口，输入命令，等待响应。没有多端同步，没有消息通知，没有和其他工具联动的能力。

而 OpenClaw 是一个开源的 AI Agent 平台，支持接入 Telegram、Discord、Slack、飞书等多种聊天渠道，有完善的对话管理和插件生态。

**如果能让 OpenClaw 直接调用 Kiro 的 AI 后端呢？**

这就是这个项目要解决的问题。

---

## 关键发现：ACP 协议

翻看 Kiro CLI 的帮助文档，发现了一个子命令：

```
kiro-cli acp
```

ACP（Agent Client Protocol）是 Kiro CLI 官方暴露的标准化通信接口：

- 基于 JSON-RPC 2.0 协议
- 通过 stdin/stdout 管道通信
- 支持会话管理、流式响应、工具调用

这是一个**官方公开的集成点**，不需要逆向工程。

---

## 架构：一个本地 HTTP 代理

思路很直接——写一个 Bridge，把 OpenAI 格式的 HTTP 请求翻译成 ACP 协议：

```
OpenClaw        ──HTTP──▶  Bridge (FastAPI)  ──stdio──▶  kiro-cli acp
任意客户端                   :18788/v1                    JSON-RPC 2.0
```

Bridge 的职责：

1. **维护持久连接** — 启动 `kiro-cli acp` 子进程，完成初始化握手，保持长连接
2. **协议翻译** — OpenAI Chat Completion ↔ ACP session/prompt
3. **流式转发** — 将 ACP 的 `agent_message_chunk` 通知实时转换为 SSE 推送

---

## 核心技术挑战

### 异步消息分发

ACP 通过 stdout 输出两种消息：

- **Response**（带 id）：请求的响应
- **Notification**（无 id）：流式文本块、工具调用状态

需要一个异步读取器持续监听，根据消息类型分发到对应的 Future 或 Queue。

### 流式响应转换

ACP 的流式通知格式和 OpenAI 的 SSE 格式完全不同。Bridge 需要实时转换，同时正确处理工具调用中间状态（有通知但不产生文本）。

### 工具调用代理

Kiro 的 agent 在工作过程中会请求读写文件、执行命令。Bridge 需要在指定的项目目录内响应这些请求，并将结果返回给 agent。

### 上下文溢出处理

当对话上下文达到模型限制时，Bridge 会自动检测错误、创建新会话，并通知用户重新发送问题。

---

## 最终效果

配置完成后，在 OpenClaw 中选择 `kiro-b/kiro-acp` 模型：

✅ 流式响应，逐字输出  
✅ 代码理解和生成  
✅ 项目文件读写  
✅ 终端命令执行  
✅ 上下文溢出自动恢复  
✅ 支持 Windows / macOS / Linux  

---

## 5 分钟上手

**第一步：确保 kiro-cli 已认证**

```bash
kiro-cli login
```

**第二步：启动 Bridge**

```bash
git clone https://github.com/LuoShiXi/kiro-cli-openclaw-bridge.git
cd kiro-cli-openclaw-bridge
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python -m acp_openai_bridge.main --cwd /your/project
```

看到以下输出说明启动成功：

```
ACP-to-OpenAI Bridge running at http://127.0.0.1:18788
```

**第三步：配置 OpenClaw**

编辑 `~/.openclaw/openclaw.json`，添加 provider：

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

重启 OpenClaw，选择模型，开始对话。

---

## 也可以打包为可执行文件

不想装 Python？可以打包为单文件二进制（约 15MB）：

**Linux / macOS / WSL：**
```bash
./build.sh
./dist/acp-bridge --cwd /your/project
```

**Windows：**
```powershell
pyinstaller acp_bridge.spec --clean --noconfirm
.\dist\acp-bridge.exe --cwd C:\your\project
```

---

## 不只是 OpenClaw

由于 Bridge 暴露的是标准的 OpenAI Chat Completion API，**任何支持自定义 Base URL 的 OpenAI 兼容客户端都能接入**：

- OpenClaw
- ChatBox
- LobeChat
- 自定义脚本
- ……

只需将 Base URL 指向 `http://127.0.0.1:18788/v1`。

---

## 开源地址

| 资源 | 链接 |
|------|------|
| Bridge 源码 | https://github.com/LuoShiXi/kiro-cli-openclaw-bridge |
| OpenClaw Skill | https://github.com/LuoShiXi/kiro-cli-openclaw-skill |
| ClawHub 安装 | `clawhub install kiro-cli-openclaw-bridge` |

协议：CC BY-NC 4.0（允许自由使用和修改，禁止商业用途）

---

## 免责声明

本项目为非官方社区工具，与 Amazon Web Services (AWS)、Kiro 或其关联公司无任何关联、认可或赞助关系。Kiro CLI 受 AWS Customer Agreement 和 AWS Intellectual Property License 约束。用户需使用自己的 Kiro CLI 认证账号，并对自身使用行为承担全部责任。
