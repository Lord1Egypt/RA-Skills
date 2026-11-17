---
name: codex-juxingyi-setup
display_name: "Codex 接入聚星逸"
description: "安装 Codex 桌面版/CLI 并接入聚星逸网关，配置 Agent 感知 Codex 工作状态。三步：install → configure → perceive。"
tags:
  - codex
  - openai
  - gateway
  - juxingyi
  - openclaw
  - agent-integration
version: 1.0.0
---

# Codex 接入聚星逸 · OpenClaw Skill

> 让 Codex 桌面版/CLI 使用聚星逸网关调用 50+ 大模型，并让 AI Agent 感知 Codex 的工作状态。

## 前置条件

- macOS（ChatGPT 桌面版仅支持 macOS/Windows）
- `jq` 已安装（`brew install jq`）
- `curl` 已安装（macOS 自带）
- 聚星逸 API Key（在 `https://fireworks-simulator.huo15.com/app/` 控制台创建，`fsk-` 开头）

## 环境变量

| 变量 | 默认值 | 说明 |
|---|---|---|
| `JUXINGYI_API_BASE` | `https://fireworks-simulator-api.huo15.com/v1` | 聚星逸网关地址 |
| `CODEX_HOME` | `~/.codex` | Codex 配置目录 |

## 使用方式

### 步骤 1：安装 Codex

```bash
bash skills/codex-juxingyi-setup/scripts/install.sh
```

检测并安装：
- **ChatGPT 桌面版**（含 Codex 面板）：检测 `/Applications/ChatGPT.app`，未安装则引导 `brew install --cask chatgpt` 或手动下载
- **Codex CLI**：检测 `which codex`，未安装则 `npm install -g @openai/codex`

已安装则报告版本并跳过。

### 步骤 2：配置聚星逸接入

```bash
# 交互式配置（会询问 API Key 和模型选择）
bash skills/codex-juxingyi-setup/scripts/configure.sh

# 非交互式（CI/自动化场景）
JUXINGYI_API_KEY="fsk-xxxx" JUXINGYI_MODEL="deepseek-v4-flash" \
  bash skills/codex-juxingyi-setup/scripts/configure.sh
```

配置过程：
1. 备份现有 `~/.codex/config.toml`
2. 从聚星逸 `GET /v1/models` 拉可用模型列表
3. 写入聚星逸 provider 配置（保留原有 plugins/mcp_servers/projects 段）
4. 验证连通性（用配置的 key 调一次 `/v1/models`）

写入的配置段：
```toml
model_provider = "juxingyi"
openai_base_url = "https://fireworks-simulator-api.huo15.com/v1"
model = "deepseek-v4-flash"
```

### 步骤 3：Agent 感知 Codex 工作

```bash
# 查看 Codex 当前状态（模型、provider、最近会话、活跃项目）
bash skills/codex-juxingyi-setup/scripts/codex-status.sh

# 列出最近 10 条会话
bash skills/codex-juxingyi-setup/scripts/codex-sessions.sh --limit 10

# 查看某条会话详情
bash skills/codex-juxingyi-setup/scripts/codex-sessions.sh --detail <session_id>

# 聚合全部上下文（供 Agent 一次性读取）
bash skills/codex-juxingyi-setup/scripts/codex-context.sh
```

**Agent 感知内容：**

| 数据 | 来源 | 用途 |
|---|---|---|
| 当前模型/provider | `config.toml` | 知道 Codex 在用哪个模型 |
| 最近会话列表 | `session_index.jsonl` | 知道用户最近和 Codex 聊了什么 |
| 会话详情 | `sessions/**/*.jsonl` | 读取完整对话内容 |
| 活跃项目 | `config.toml [projects.*]` | 知道 Codex 在操作哪些项目 |
| 工作目录 | session `payload.cwd` | 知道每个会话的工作目录 |

## 复用说明

其他 OpenClaw 实例复用本 skill：

1. **复制目录**：`cp -r skills/codex-juxingyi-setup /目标路径/`
2. **设置环境变量**（可选）：
   ```bash
   export JUXINGYI_API_BASE="https://your-gateway.example.com/v1"  # 自定义网关
   export CODEX_HOME="$HOME/.codex"  # 自定义 Codex 目录
   ```
3. **运行**：按上述三步执行即可
4. **无需修改**：脚本不硬编码任何用户私有信息，所有参数通过环境变量/交互输入

## Codex 配置参考

聚星逸网关已原生支持 Responses API（`POST /v1/responses`），Codex v0.84+ 强制要求该协议，无需额外代理。

完整 `config.toml` 示例：
```toml
model = "deepseek-v4-flash"
model_provider = "juxingyi"
openai_base_url = "https://fireworks-simulator-api.huo15.com/v1"
model_reasoning_effort = "medium"
approval_policy = "on-request"
sandbox_mode = "workspace-write"

[sandbox_workspace_write]
network_access = true
```

## 故障排查

| 问题 | 原因 | 解决 |
|---|---|---|
| `codex` 命令找不到 | CLI 未安装或不在 PATH | `npm install -g @openai/codex` |
| `/v1/models` 返回 401 | API Key 无效 | 在聚星逸控制台重新创建 Key |
| Codex 报 "wire_api" 错误 | 旧版本不支持 Responses API | 升级 Codex：`npm update -g @openai/codex` |
| 会话列表为空 | 从未用过 Codex | 先用 Codex 创建一次会话 |
