# Kiro CLI OpenClaw Bridge

将 [OpenClaw](https://github.com/openclaw/openclaw) 或任何 OpenAI 兼容客户端连接到 [Kiro CLI](https://kiro.dev) 的 ACP 后端，支持 SSE 流式响应和工具调用。

## 架构

```
OpenClaw / 任意客户端  ──HTTP──▶  Bridge (FastAPI)  ──stdio──▶  kiro-cli acp
                                  :18788/v1                     JSON-RPC 2.0
```

Bridge 维护一个持久的 `kiro-cli acp` 子进程，完成 JSON-RPC 初始化握手，管理会话，并在 OpenAI API 格式与 ACP 协议之间双向翻译。

## 前置条件

- **kiro-cli** 已安装并完成认证（`kiro-cli login`）
- **Python 3.10+**（源码运行）或使用预编译二进制

## 快速开始

### 方式一：源码运行

```bash
git clone https://github.com/LuoShiXi/kiro-cli-openclaw-bridge.git
cd kiro-cli-openclaw-bridge

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

python -m acp_openai_bridge.main --cwd /your/project
```

### 方式二：构建为单文件可执行程序

**Linux / macOS / WSL：**

```bash
./build.sh
./dist/acp-bridge --cwd /your/project
```

**Windows（PowerShell / CMD）：**

```powershell
pip install -r requirements.txt
pyinstaller acp_bridge.spec --clean --noconfirm
.\dist\acp-bridge.exe --cwd C:\your\project
```

构建产物约 15MB，无需 Python 环境即可运行。

> **注意**：PyInstaller 不支持交叉编译，打包产物只能在构建时的操作系统上运行。如需在不同平台使用，需在对应平台（Windows / macOS / Linux）上分别执行构建。

### 验证运行

```bash
# 健康检查
curl http://127.0.0.1:18788/health

# 快速测试
curl -X POST http://127.0.0.1:18788/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model":"kiro-acp","messages":[{"role":"user","content":"hello"}],"stream":false}'
```

## 命令行参数

| 参数 | 环境变量 | 默认值 | 说明 |
|------|---------|--------|------|
| `--host` | `ACP_BRIDGE_HOST` | `127.0.0.1` | 监听地址 |
| `--port` | `ACP_BRIDGE_PORT` | `18788` | 监听端口 |
| `--kiro-cli-path` | `ACP_BRIDGE_KIRO_CLI_PATH` | 自动查找 | kiro-cli 可执行文件路径 |
| `--cwd` | `ACP_BRIDGE_CWD` | 当前目录 | ACP 会话工作目录 |
| `--timeout` | `ACP_BRIDGE_TIMEOUT` | `300` | 请求超时（秒） |
| `--model` | `ACP_BRIDGE_MODEL` | kiro-cli 默认 | 模型 ID（如 `claude-sonnet-4-20250514`） |

## OpenClaw 配置

编辑 `~/.openclaw/openclaw.json`，在 `models.providers` 中添加 kiro bridge provider：

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

然后在 `agents.defaults` 中设置为默认模型（可选）：

```json
{
  "agents": {
    "defaults": {
      "model": {
        "primary": "kiro-b/kiro-acp"
      },
      "models": {
        "kiro-b/kiro-acp": {
          "alias": "Kiro"
        }
      }
    }
  }
}
```

配置完成后重启 OpenClaw 即可在对话中使用 `kiro-b/kiro-acp` 模型。

## API 端点

| Method | Path | 说明 |
|--------|------|------|
| POST | `/v1/chat/completions` | OpenAI 聊天补全（支持 `stream: true`） |
| POST | `/v1/messages` | Anthropic Messages API（支持 `stream: true`） |
| GET | `/v1/models` | 模型列表 |
| GET | `/health` | 健康检查 |

## 流式响应

当请求中 `stream: true` 时，Bridge 会：
1. 将请求翻译为 ACP `session/prompt` 调用
2. 持续读取 ACP 的 `session/update` 通知中的 `agent_message_chunk`
3. 实时转换为 OpenAI SSE `chat.completion.chunk` 格式推送给客户端
4. 收到最终响应后发送 `finish_reason` 和 `[DONE]`

## 工具调用

Bridge 透传 kiro-cli 的内置能力，所有操作受限于 `--cwd` 指定的项目目录。建议仅在信任的项目目录中使用，并保持服务绑定在 localhost。

## 跨平台支持

| 平台 | 说明 |
|------|------|
| Windows | 支持，需安装 Windows 版 kiro-cli，可打包为 `.exe` |
| Windows (WSL) | 支持，自动检测 WSL 环境 |
| macOS ARM (Apple Silicon) | 支持，自动查找 `/opt/homebrew/bin/kiro-cli` |
| macOS Intel | 支持，自动查找 `/usr/local/bin/kiro-cli` |
| Linux | 支持，通过 PATH 或 `~/.local/bin/kiro-cli` 查找 |

> **注意**：PyInstaller 不支持交叉编译，打包产物只能在构建时的操作系统上运行。如需在不同平台使用，需在对应平台（Windows / macOS / Linux）上分别执行 `./build.sh` 构建。

## 项目结构

```
├── acp_openai_bridge/
│   ├── main.py              # 入口，FastAPI 应用和生命周期管理
│   ├── config.py            # 配置解析（CLI 参数 + 环境变量）
│   ├── process_manager.py   # kiro-cli acp 子进程生命周期
│   ├── session_manager.py   # ACP 会话管理
│   ├── acp_reader.py        # stdout 异步读取和消息分发
│   ├── jsonrpc_writer.py    # JSON-RPC 请求写入
│   ├── request_translator.py  # OpenAI → ACP 请求翻译
│   ├── response_translator.py # ACP → OpenAI 响应翻译
│   ├── routes.py            # API 路由（OpenAI + Anthropic）
│   └── sse_emitter.py       # SSE 流式输出
├── tests/                   # 单元测试
├── build.sh                 # PyInstaller 构建脚本
├── acp_bridge.spec          # PyInstaller 配置
└── requirements.txt         # Python 依赖
```

## License

[CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/) — 允许自由使用和修改，禁止商业用途。

## 免责声明

本项目为非官方社区工具，与 Amazon Web Services (AWS)、Kiro 或其关联公司无任何关联、认可或赞助关系。

Kiro CLI 受 [AWS Customer Agreement](https://aws.amazon.com/agreement/) 和 [AWS Intellectual Property License](https://aws.amazon.com/legal/aws-ip-license-terms/) 约束。使用本工具前，请确保您已阅读并遵守相关服务条款。

本工具仅作为本地开发辅助用途，用户需使用自己的 Kiro CLI 认证账号，并对自身使用行为承担全部责任。作者不对因使用本工具而产生的任何违规、损失或法律责任负责。

如有疑问，请联系 Kiro 官方确认您的使用场景是否符合其服务条款。
