---
name: meeting-assistant
description: "Zoom/Teams/Meet 远程会议AI助手。Use when: user asks to join a meeting, monitor a meeting, record a meeting, assist in a medical consultation, help doctor-patient communication, transcribe meeting audio, analyze meeting screenshots, send chat in meeting, or provide real-time meeting assistance. The agent joins the meeting autonomously as a bot, performs real-time speech-to-text, vision analysis via Claude AI, and participants can communicate with the agent directly via meeting chat."
---

# Meeting Assistant — 远程会议智能助手

让 Agent 作为 AI 参会者加入 Zoom / Teams / Google Meet，实时分析会议内容并与参会者双向交互。

## 架构总览

```
                    ┌─────────────────┐
                    │   你（用户）      │
                    │  在会议聊天发消息 │
                    └────────┬────────┘
                             │ 会议聊天（双向）
                    ┌────────▼────────┐
                    │   Vexa Bot      │  ← AI 机器人，会议参与者
                    │ (Docker 容器)   │
                    └────────┬────────┘
                             │ Vexa REST API
                    ┌────────▼────────┐
                    │  meeting_bot.py │  ← 主控程序
                    │  双线程运行:     │
                    │  • 聊天轮询(5s) │  → 读聊天 → Claude → 回答
                    │  • 分析循环(30s)│  → 截图+转录 → Claude → 建议
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │  claude_client  │  ← Anthropic API
                    │  • 图像分析      │
                    │  • 转录理解      │
                    │  • 聊天问答      │
                    │  • 会议摘要      │
                    └─────────────────┘
```

**用户交互方式**：用户在 Zoom/Teams/Meet 的会议聊天中输入问题或命令，Bot 通过 Claude AI 生成回答并发回聊天。整个过程无需其他工具，完全在会议内进行。

---

## 快速开始

### 前置条件

```bash
# 1. 启动 Vexa Bot 服务（Docker）
cd skills/meeting-assistant
docker compose up -d

# 2. 设置 Claude API Key
export ANTHROPIC_API_KEY="sk-ant-..."

# 3. 安装 Python 依赖
pip install anthropic requests
```

### 方式 A：通过 agent_tool.py（推荐，Claude Code 调用）

```bash
PYTHON="D:/program/codesupport/anaconda/envs/meeting-assistant/python.exe"

# 加入会议并启动 AI 助手（后台运行）
$PYTHON scripts/agent_tool.py start "https://zoom.us/j/123456789?pwd=xxx" --mode general

# 查看状态
$PYTHON scripts/agent_tool.py status

# 向会议聊天发消息
$PYTHON scripts/agent_tool.py chat "大家好，我是 AI 助手"

# 获取当前转录
$PYTHON scripts/agent_tool.py transcript

# 获取截图
$PYTHON scripts/agent_tool.py screenshot

# 查看助手日志
$PYTHON scripts/agent_tool.py logs

# 停止助手（自动生成摘要后离开）
$PYTHON scripts/agent_tool.py stop
```

### 方式 B：通过 meeting_bot.py（直接运行）

```bash
PYTHON="D:/program/codesupport/anaconda/envs/meeting-assistant/python.exe"

# 全自动 AI 助手模式（加入 + 分析 + 聊天）
$PYTHON scripts/meeting_bot.py assist "https://zoom.us/j/123456789" --mode medical --interval 30

# 单独命令
$PYTHON scripts/meeting_bot.py join "https://zoom.us/j/123456789"
$PYTHON scripts/meeting_bot.py chat "这是发给会议的消息"
$PYTHON scripts/meeting_bot.py read-chat
$PYTHON scripts/meeting_bot.py transcript
$PYTHON scripts/meeting_bot.py screenshot
$PYTHON scripts/meeting_bot.py status
$PYTHON scripts/meeting_bot.py leave
```

### 方式 C：本地监控（无需 Vexa）

```bash
$PYTHON scripts/meeting_monitor.py start --mode medical --interval 30
$PYTHON scripts/meeting_monitor.py snapshot
$PYTHON scripts/meeting_monitor.py transcript --last 5
$PYTHON scripts/meeting_monitor.py stop
```

---

## 与用户的聊天交互

Bot 加入会议后，用户可以在**会议自带的聊天框**中直接和 AI 交流：

| 用户在聊天中输入 | Bot 响应 |
|---------------|---------|
| `刚才那个药名是什么？` | Claude 基于转录内容回答 |
| `帮我总结一下刚才讨论的` | Claude 分析转录并总结 |
| `@助手 这个症状正常吗？` | Claude 给出信息性解释（附免责声明） |
| `？什么是高血压` | Claude 用通俗语言解释 |

**触发条件**（满足任一即回应）：
- 包含 `OpenClaw` / `助手` / `AI` 等关键词
- 包含 `?` 或 `？`
- 医疗模式下包含医疗关键词
- 以 `/`、`!`、`请问`、`请` 开头

---

## 实时分析循环

助手运行两个并发循环：

### 聊天轮询（每 5 秒）
```
读取会议聊天 → 检测新用户消息 → Claude 生成回答 → 发回聊天
```

### 分析循环（每 30 秒，可调）
```
截图 → 获取转录增量 → Claude 视觉+文本分析 → 若有建议则发聊天 → 保存日志
```

分析结束后自动调用 Claude 生成完整会议摘要（`meeting_summary.md`）。

---

## 医疗辅助模式 (`--mode medical`)

启用后额外功能：
- 自动识别医学术语 → 通俗解释 → 发到聊天
- 检测处方/诊断/用药信息 → 用 ⚠️ 标记
- 患者版简明摘要（去除专业术语）
- 医学术语对照表（中英文）
- 复诊/随访提醒

参考：`references/medical-terms-guide.md`

---

## 作为 Anthropic Tool Use 使用

```python
import anthropic
from scripts.agent_tool import tool_definitions, handle_tool_call

client = anthropic.Anthropic()

# 让 Claude 决定是否加入会议
response = client.messages.create(
    model="claude-sonnet-4-6",
    tools=tool_definitions(),
    messages=[{
        "role": "user",
        "content": "帮我加入这个会议并用医疗模式监控：https://zoom.us/j/123?pwd=xxx"
    }]
)

# 处理 tool_use 块
for block in response.content:
    if block.type == "tool_use":
        result = handle_tool_call(block.name, block.input)
        print(result)
```

### 可用工具

| Tool Name | 功能 |
|-----------|------|
| `meeting_start` | 加入会议并启动 AI 助手 |
| `meeting_stop` | 停止助手并生成摘要 |
| `meeting_status` | 查看当前状态 |
| `meeting_send_chat` | 向会议聊天发消息 |
| `meeting_get_transcript` | 获取转录文本 |
| `meeting_screenshot` | 截取会议画面 |
| `meeting_read_chat` | 读取聊天记录 |
| `meeting_get_summary` | 获取会议摘要 |
| `meeting_get_logs` | 查看调试日志 |

---

## 配置 (`config.json`)

```json
{
  "claude": {
    "api_key": "",          // 或设置 ANTHROPIC_API_KEY 环境变量
    "model": "claude-sonnet-4-6",
    "max_tokens": 1024
  },
  "chat_poll_interval": 5,  // 聊天轮询间隔（秒）
  "bot": {
    "vexa_url": "http://localhost:8056",
    "vexa_api_key": "",
    "bot_name": "OpenClaw 助手"
  },
  "medical": {
    "enabled": false
  }
}
```

---

## 输出文件结构

```
recordings/bot_20260313_143000/
├── session.json              # 会话元数据（bot_id, 平台, 开始时间等）
├── screenshots/              # 截图（screen_HHMMSS.png）
├── analysis/
│   └── cycle_log.jsonl       # 每次分析循环的详细记录
├── transcript_log.json       # 完整转录记录（JSON 数组）
├── suggestions_log.json      # Bot 发送的所有聊天消息记录
└── meeting_summary.md        # AI 生成的完整会议摘要
```

---

## 支持的会议平台

| 平台 | URL 格式 |
|------|---------|
| Zoom | `https://zoom.us/j/123456789?pwd=xxx` |
| Microsoft Teams | `https://teams.microsoft.com/l/meetup-join/...` |
| Google Meet | `https://meet.google.com/abc-defg-hij` |

---

## 与其他 Skill 联动

- **pc-control**: 截屏增强 + 会议窗口控制
- **agent-browser-core**: 会议中查询资料
- **eva-tts**: 将分析结果语音播报

参考：`references/integration-guide.md`

---

## 注意事项

- 录音/录制前需获得所有参会者同意
- 医疗信息严格保密，建议加密存储录制文件
- Bot 模式需要 Docker 运行 Vexa 服务
- Vexa 的 Zoom 支持需要 Zoom Marketplace OAuth 凭证
- Claude API Key 建议通过环境变量设置，不要写入 config.json
