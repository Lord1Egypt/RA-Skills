---
name: kiro-cli-openclaw-integration
description: 通过本地 ACP-to-OpenAI Bridge 将 OpenClaw（或任何 OpenAI 兼容客户端）连接到 kiro-cli 的 ACP 后端，支持流式响应和工具调用。
metadata:
  openclaw:
    homepage: https://github.com/LuoShiXi/kiro-cli-openclaw-bridge
    requires:
      bins:
        - kiro-cli
---

# Kiro CLI 与 OpenClaw 集成

Local proxy that translates OpenAI/Anthropic API requests into ACP JSON-RPC calls, enabling OpenClaw and other OpenAI-compatible clients to use kiro-cli as the AI backend.

## Architecture

```
OpenClaw / Any Client  ──HTTP──▶  Bridge (FastAPI)  ──stdio──▶  kiro-cli acp
                                  :18788/v1                     JSON-RPC 2.0
```

---

## 从零开始完整搭建指南

### Step 1: 安装 kiro-cli

```bash
# 下载安装 kiro-cli（如已安装跳过）
# 参考 kiro 官方文档安装，确保 kiro-cli 在 PATH 中
which kiro-cli  # 验证安装
```

### Step 2: 认证 kiro-cli

```bash
kiro-cli login
# 按提示完成登录认证，确保能正常使用
# 验证：
kiro-cli acp --help  # 应显示帮助信息
```

### Step 3: 获取 Bridge

推荐从 GitHub Releases 下载预编译二进制（无需 Python 环境）：

```bash
# 下载预编译二进制（约 15MB，支持 Linux/WSL 和 macOS）
# https://github.com/LuoShiXi/kiro-cli-openclaw-bridge/releases

# 或从源码构建：
git clone https://github.com/LuoShiXi/kiro-cli-openclaw-bridge.git
cd kiro-cli-openclaw-bridge
```

### Step 4: 安装 Python 环境（源码运行方式）

```bash
# 需要 Python 3.10+
python3 --version  # 验证版本

# 创建虚拟环境
python3 -m venv .venv
source .venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

依赖清单（`requirements.txt`）：
```
fastapi==0.115.12
uvicorn==0.34.3
pytest==8.3.5
pytest-asyncio==0.25.3
pyinstaller==6.12.0
```

### Step 5: 启动 Bridge

```bash
# 方式 A：源码运行
source .venv/bin/activate
python -m acp_openai_bridge.main --cwd /your/project

# 方式 B：使用预编译二进制（如已构建）
./dist/acp-bridge --cwd /your/project

# 方式 C：构建后运行
./build.sh
./dist/acp-bridge --cwd /your/project
```

指定模型（可选）：
```bash
python -m acp_openai_bridge.main --cwd /your/project --model claude-sonnet-4-20250514
```

启动成功标志：
```
ACP-to-OpenAI Bridge running at http://127.0.0.1:18788
```

### Step 6: 验证 Bridge 运行

```bash
# 健康检查
curl http://127.0.0.1:18788/health
# 应返回：{"status":"ok","acp_available":true}

# 模型列表
curl http://127.0.0.1:18788/v1/models
# 应返回包含 kiro-acp 的模型列表

# 快速测试对话
curl -X POST http://127.0.0.1:18788/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model":"kiro-acp","messages":[{"role":"user","content":"hello"}],"stream":false}'
```

### Step 7: 配置 OpenClaw

编辑 `~/.openclaw/openclaw.json`，在 `models.providers` 中添加：

```json
{
  "models": {
    "mode": "merge",
    "providers": {
      "kiro-b": {
        "api": "openai-completions",
        "baseUrl": "http://127.0.0.1:18788/v1",
        "apiKey": "any-value",
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

设置为默认模型（可选），在 `agents.defaults` 中添加：

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

重启 OpenClaw 即可使用。

保存后在 OpenClaw 中选择该 Provider 和 `kiro-acp` 模型即可开始对话。

---

## 命令行参数

| 参数 | 环境变量 | 默认值 | 说明 |
|------|---------|--------|------|
| `--host` | `ACP_BRIDGE_HOST` | `127.0.0.1` | 监听地址 |
| `--port` | `ACP_BRIDGE_PORT` | `18788` | 监听端口 |
| `--kiro-cli-path` | `ACP_BRIDGE_KIRO_CLI_PATH` | 自动查找 | kiro-cli 路径 |
| `--cwd` | `ACP_BRIDGE_CWD` | 当前目录 | ACP 会话工作目录 |
| `--timeout` | `ACP_BRIDGE_TIMEOUT` | `300` | 请求超时（秒） |
| `--model` | `ACP_BRIDGE_MODEL` | kiro-cli 默认 | 模型 ID |

## API 端点

| Method | Path | Description |
|--------|------|-------------|
| POST | `/v1/chat/completions` | OpenAI 聊天补全（支持 `stream: true`） |
| POST | `/v1/messages` | Anthropic Messages API（支持 `stream: true`） |
| GET | `/v1/models` | 模型列表 |
| GET | `/health` | 健康检查 |

## 流式响应

当 `stream: true` 时：
1. Bridge 发送 `session/prompt` 到 ACP 子进程
2. 持续读取 `session/update` 中的 `agent_message_chunk`
3. 实时转换为 OpenAI SSE `chat.completion.chunk` 格式
4. 完成后发送 `finish_reason` 和 `[DONE]`

## 工具执行

Bridge 透传 kiro-cli 的内置能力，所有操作受限于 `--cwd` 指定的项目目录。建议仅在信任的项目目录中使用，并保持服务绑定在 localhost。

## 故障排查

| 问题 | 解决方案 |
|------|---------|
| Bridge 启动但无响应 | 确认 `kiro-cli login` 已完成；检查 `--cwd` 指向有效目录 |
| Agent 卡在 tool_call | stdout 缓冲区已设为 10MB；检查日志是否有 `readline buffer overflow` |
| OpenClaw 连接被拒 | `curl http://127.0.0.1:18788/health` 验证 bridge 运行中 |
| 超时错误 | 增大 `--timeout 600`；复杂任务需要更多时间 |
| kiro-cli 找不到 | 用 `--kiro-cli-path /path/to/kiro-cli` 显式指定 |

## 平台支持

| 平台 | 说明 |
|------|------|
| Windows | 支持，需安装 Windows 版 kiro-cli，可打包为 `.exe` |
| Windows (WSL) | 支持，自动检测 WSL 环境 |
| macOS ARM (Apple Silicon) | 支持，自动查找 `/opt/homebrew/bin/kiro-cli` |
| macOS Intel | 支持，自动查找 `/usr/local/bin/kiro-cli` |
| Linux | 支持，通过 PATH 或 `~/.local/bin/kiro-cli` 查找 |

## 构建打包

**Linux / macOS / WSL：**

```bash
./build.sh        # 构建单文件可执行程序 → dist/acp-bridge (~15MB)
./build.sh clean  # 清理构建产物
```

**Windows（PowerShell / CMD）：**

```powershell
pip install -r requirements.txt
pyinstaller acp_bridge.spec --clean --noconfirm
.\dist\acp-bridge.exe --cwd C:\your\project
```

构建后的二进制无需 Python 环境即可运行。

> PyInstaller 不支持交叉编译，需在各平台（Windows / macOS / Linux）上分别构建。

## 项目地址

- GitHub：https://github.com/LuoShiXi/kiro-cli-openclaw-bridge

## 免责声明

本项目为非官方社区工具，与 Amazon Web Services (AWS)、Kiro 或其关联公司无任何关联、认可或赞助关系。

Kiro CLI 受 [AWS Customer Agreement](https://aws.amazon.com/agreement/) 和 [AWS Intellectual Property License](https://aws.amazon.com/legal/aws-ip-license-terms/) 约束。使用本工具前，请确保您已阅读并遵守相关服务条款。

本工具仅作为本地开发辅助用途，用户需使用自己的 Kiro CLI 认证账号，并对自身使用行为承担全部责任。作者不对因使用本工具而产生的任何违规、损失或法律责任负责。

如有疑问，请联系 Kiro 官方确认您的使用场景是否符合其服务条款。
