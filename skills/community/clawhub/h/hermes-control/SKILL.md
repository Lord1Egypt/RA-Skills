---
name: hermes-control
description: 通过 OpenClaw 操控 Hermes Agent 的完整指令参考。包含所有 Hermes CLI 命令、斜杠命令、工具集、配置项、网关操作、多代理协调、定时任务、技能管理等完整操作指南。当用户需要完整操控 Hermes Agent 时使用此技能。关键词：hermes、hermes agent、hermes-agent、hermes 控制、hermes 操控、hermes 自动化。
---

# OpenClaw 操控 Hermes Agent 完整指令参考

本技能整合了 Hermes Agent 所有可通过 OpenClaw (agent-browser、anysearch 等) 操控的指令、配置、工作流。适用于需要通过自动化方式完整操控 Hermes Agent 的场景。

## 目录

1. [核心 CLI 命令](#核心-cli-命令)
2. [会话内斜杠命令](#会话内斜杠命令)
3. [工具集与技能管理](#工具集与技能管理)
4. [配置管理](#配置管理)
5. [网关/消息平台操作](#网关消息平台操作)
6. [多代理与任务委派](#多代理与任务委派)
7. [定时任务](#定时任务)
8. [MCP 服务器管理](#mcp-服务器管理)
9. [配置文件与路径](#配置文件与路径)
10. [Webhooks 与自动化](#webhooks-与自动化)
11. [桌面应用与仪表盘](#桌面应用与仪表盘)
12. [自动化蓝图](#自动化蓝图)
13. [自动化操控最佳实践](#自动化操控最佳实践)
14. [故障排查](#故障排查)

---

## 核心 CLI 命令

### 安装与启动

```bash
# 安装（推荐官方安装脚本）
curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash

# 或通过 PyPI
pip install hermes-agent

# 交互式聊天（默认界面）
hermes

# 单次查询（非交互）
hermes chat -q "你的问题"

# 启动向导 / 模型选择 / 健康检查
hermes setup
hermes model
hermes doctor

# 其他界面
hermes desktop      # 原生桌面应用
hermes dashboard    # Web 管理面板 + 嵌入式聊天
hermes proxy        # OpenAI 兼容本地代理
```

### 全局标志

```bash
hermes [flags] [command]

  --version, -V           显示版本
  --resume, -r SESSION    按 ID 或标题恢复会话
  --continue, -c [NAME]   按名称恢复，或最近会话
  --worktree, -w          隔离 git worktree 模式（并行代理）
  --skills, -s SKILL      预加载技能（逗号分隔或重复）
  --profile, -p NAME      使用命名配置文件
  --yolo                  跳过危险命令确认
  --pass-session-id       在系统提示中包含会话 ID
```

### 聊天命令

```bash
hermes chat [flags]
  -q, --query TEXT        单次查询，非交互
  -m, --model MODEL       模型（如 anthropic/claude-sonnet-4）
  -t, --toolsets LIST     逗号分隔的工具集列表
  --provider PROVIDER     强制提供商（openrouter, anthropic, nous 等）
  -v, --verbose           详细输出
  -Q, --quiet             抑制横幅、加载器、工具预览
  --checkpoints           启用文件系统检查点（/rollback）
  --source TAG            会话来源标签（默认: cli）
```

### 配置命令

```bash
hermes setup [section]           # 交互式向导（model|terminal|gateway|tools|agent）
hermes model                     # 交互式模型/提供商选择器
hermes config                    # 查看当前配置
hermes config edit               # 在 $EDITOR 中打开 config.yaml
hermes config set KEY VAL        # 设置配置值
hermes config path               # 打印 config.yaml 路径
hermes config env-path           # 打印 .env 路径
hermes config check              # 检查缺失/过时配置
hermes config migrate            # 更新配置新选项
hermes doctor [--fix]            # 检查依赖与配置
hermes status [--all]            # 显示组件状态
```

### 凭证与池

```bash
hermes auth                      # 交互式凭证管理器
hermes auth add [PROVIDER]       # 添加 OAuth 或 API 密钥（如 nous, openai-codex, qwen-oauth, anthropic）
hermes auth list [PROVIDER]      # 列出池化凭证
hermes auth remove P INDEX       # 按提供商 + 索引移除
hermes auth reset PROVIDER       # 清除耗尽状态
```

### 工具与技能

```bash
hermes tools                     # 交互式工具启用/禁用（curses UI）
hermes tools list                # 显示所有工具及状态
hermes tools enable NAME         # 启用工具集
hermes tools disable NAME        # 禁用工具集

hermes skills list               # 列出已安装技能
hermes skills search QUERY       # 搜索技能中心
hermes skills install ID         # 安装技能（ID 可为中心标识符或直接 https://.../SKILL.md）
hermes skills inspect ID         # 预览不安装
hermes skills config             # 按平台启用/禁用技能
hermes skills check              # 检查更新
hermes skills update             # 更新过期技能
hermes skills uninstall N        # 移除中心技能
hermes skills publish PATH       # 发布到注册表
hermes skills browse             # 浏览所有可用技能
hermes skills tap add REPO       # 添加 GitHub 仓库作为技能源
```

### MCP 服务器

```bash
hermes mcp serve                 # 将 Hermes 作为 MCP 服务器运行
hermes mcp add NAME              # 添加 MCP 服务器（--url 或 --command）
hermes mcp remove NAME           # 移除 MCP 服务器
hermes mcp list                  # 列出配置的服务器
hermes mcp test NAME             # 测试连接
hermes mcp configure NAME        # 切换工具选择
```

### 网关（消息平台）

```bash
hermes gateway run               # 前台运行网关
hermes gateway install           # 安装为后台服务
hermes gateway start/stop        # 控制服务
hermes gateway restart           # 重启服务
hermes gateway status            # 检查状态
hermes gateway setup             # 配置平台
```

**支持 20+ 平台**：Telegram, Discord, Slack, WhatsApp, iMessage, Signal, Matrix, Mattermost, Teams, LINE, SimpleX, ntfy, Google Chat, Home Assistant, DingTalk, Feishu, WeCom, Weixin, Raft, API Server, Webhooks.

### 会话管理

```bash
hermes sessions list             # 列出最近会话
hermes sessions browse           # 交互式选择器
hermes sessions export OUT       # 导出为 JSONL
hermes sessions rename ID T      # 重命名会话
hermes sessions delete ID        # 删除会话
hermes sessions prune            # 清理旧会话（--older-than N days）
hermes sessions stats            # 会话存储统计
```

### 定时任务

```bash
hermes cron list                 # 列出任务（--all 含禁用）
hermes cron create SCHED         # 创建：'30m', 'every 2h', '0 9 * * *'
hermes cron edit ID              # 编辑计划、提示、投递
hermes cron pause/resume ID      # 控制任务状态
hermes cron run ID               # 下一周期触发
hermes cron remove ID            # 删除任务
hermes cron status               # 调度器状态
```

### Webhooks

```bash
hermes webhook subscribe N       # 在 /webhooks/<name> 创建路由
hermes webhook list              # 列出订阅
hermes webhook remove NAME       # 移除订阅
hermes webhook test NAME         # 发送测试 POST
```

### 配置文件

```bash
hermes profile list              # 列出所有配置文件
hermes profile create NAME       # 创建（--clone, --clone-all, --clone-from）
hermes profile use NAME          # 设置粘性默认值
hermes profile delete NAME       # 删除配置文件
hermes profile show NAME         # 显示详情
hermes profile alias NAME        # 管理包装脚本
hermes profile rename A B        # 重命名配置文件
hermes profile export NAME       # 导出为 tar.gz
hermes profile import FILE       # 从归档导入
```

### 其他命令

```bash
hermes insights [--days N]       # 使用分析
hermes update                    # 更新到最新版本
hermes desktop / gui             # 启动原生桌面应用
hermes dashboard                 # Web 管理面板
hermes proxy                     # OpenAI 兼容本地代理
hermes portal                    # 快速设置 / 通过 Nous Portal 登录
hermes kanban <verb>             # 多代理工作队列看板
hermes pairing list/approve/revoke  # DM 授权
hermes plugins list/install/remove  # 插件管理
hermes secrets bitwarden ...     # 外部密钥存储
hermes memory setup/status/off   # 记忆提供商配置
hermes send                      # 通过网关平台发送一次性消息
hermes completion bash|zsh       # Shell 补全
hermes acp                       # ACP 服务器（IDE 集成）
hermes claw migrate              # 从 OpenClaw 迁移
hermes uninstall                 # 卸载 Hermes
```

---

## 会话内斜杠命令

在交互式聊天会话中输入以下命令：

### 会话控制

```
/new (/reset)          新会话
/clear                 清屏 + 新会话（CLI）
/retry                 重发最后一条消息
/undo                  撤销最后一轮对话
/title [name]          命名会话
/compress              手动压缩上下文
/stop                  终止后台进程
/rollback [N]          恢复文件系统检查点
/snapshot [sub]        创建/恢复 Hermes 配置/状态快照（CLI）
/background <prompt>   后台运行提示
/queue <prompt>        排队下一轮
/steer <prompt>        在下一个工具调用后注入消息不中断
/agents (/tasks)       显示活跃代理与运行任务
/resume [name]         恢复命名会话
/goal [text|sub]       设置跨轮持续目标（子命令: status, pause, resume, clear）
/redraw                强制完整 UI 重绘（CLI）
```

### 配置

```
/config                显示配置（CLI）
/model [name]          显示或切换模型
/personality [name]    设置人格
/reasoning [level]     设置推理级别（none|minimal|low|medium|high|xhigh|max|ultra|show|hide）
/verbose               循环：off → new → all → verbose
/voice [on|off|tts]    语音模式
/yolo                  切换审批绕过
/busy [sub]            控制工作时 Enter 键行为（CLI）（sub: queue, steer, interrupt, status）
/indicator [style]     选择 TUI 忙碌指示器样式（kaomoji, emoji, unicode, ascii）
/footer [on|off]       切换网关运行时元数据页脚
/skin [name]           切换主题（CLI）
/statusbar             切换状态栏（CLI）
```

### 工具与技能

```
/tools                 管理工具（CLI）
/toolsets              列出工具集（CLI）
/skills                搜索/安装技能（CLI）
/skill <name>          加载技能到会话
/reload-skills         重新扫描 ~/.hermes/skills/ 新增/移除
/reload                重新加载 .env 变量到运行会话（CLI）
/reload-mcp            重新加载 MCP 服务器
/cron                  管理定时任务（CLI）
/curator [sub]         后台技能维护（status, run, pin, archive, …）
/kanban [sub]          多配置文件协作看板
/plugins               列出插件（CLI）
```

### 网关

```
/approve               批准待定命令（网关）
/deny                  拒绝待定命令（网关）
/restart               重启网关（网关）
/sethome               设置当前聊天为家庭频道（网关）
/update                更新 Hermes 到最新（网关）
/topic [sub]           启用/检查 Telegram DM 话题会话（网关）
/platforms (/gateway)  显示平台连接状态（网关）
```

### 实用工具

```
/help                  显示命令
/commands [page]       浏览所有命令（网关）
/usage                 Token 使用量
/insights [days]       使用分析
/status                会话信息（网关）
/profile               活跃配置文件信息
/debug                 上传调试报告（系统信息 + 日志）获取可分享链接
```

### 退出

```
/quit (/exit, /q)      退出 CLI
```

---

## 工具集与技能管理

### 可用工具集

| 工具集 | 提供内容 |
|--------|----------|
| `web` | 网页搜索与内容提取 |
| `search` | 仅网页搜索（`web` 子集） |
| `browser` | 浏览器自动化（Browserbase, Camofox, 本地 Chromium） |
| `terminal` | Shell 命令与进程管理 |
| `file` | 文件读/写/搜索/补丁 |
| `code_execution` | 沙箱 Python 执行 |
| `vision` | 图像分析 |
| `image_gen` | AI 图像生成与图生图编辑 |
| `video` | 视频分析/生成 |
| `x_search` | 一等 X (Twitter) 搜索 |
| `tts` | 文本转语音 |
| `skills` | 技能浏览与管理 |
| `memory` | 跨会话持久记忆 |
| `session_search` | 搜索历史对话 |
| `delegation` | 子代理任务委派 |
| `cronjob` | 定时任务管理 |
| `clarify` | 向用户提问澄清 |
| `messaging` | 跨平台消息发送 |
| `todo` | 会话内任务规划追踪 |
| `kanban` | 多代理工作队列工具（仅工作节点） |
| `debugging` | 额外内省/调试工具（默认关闭） |
| `safe` | 最小化、低风险工具集（锁定会话） |
| `spotify` | Spotify 播放与歌单控制 |
| `homeassistant` | 智能家居控制（默认关闭） |
| `discord` | Discord 集成工具 |
| `discord_admin` | Discord 管理/审核工具 |
| `feishu_doc` | 飞书文档工具 |
| `feishu_drive` | 飞书云盘工具 |
| `yuanbao` | 元宝集成工具 |
| `rl` | 强化学习工具（默认关闭） |

### 工具集管理命令

```bash
# 启用/禁用（在新会话生效，需 /reset 或重启）
hermes tools enable web
hermes tools disable browser

# 交互式管理
hermes tools
hermes tools list
```

### 技能管理

```bash
# 列出/搜索/安装
hermes skills list
hermes skills search "browser automation"
hermes skills install skill-name
hermes skills install https://example.com/SKILL.md

# 配置平台启用
hermes skills config

# 更新/检查/移除
hermes skills check
hermes skills update
hermes skills uninstall skill-name
```

---

## 配置管理

### 主配置文件

```
~/.hermes/config.yaml        # 主配置
~/.hermes/.env               # API 密钥与密钥（$HERMES_HOME 下如已设置）
```

### 配置节概览

| 节 | 关键选项 |
|-----|----------|
| `model` | `default`, `provider`, `base_url`, `api_key`, `context_length` |
| `agent` | `max_turns` (90), `tool_use_enforcement` |
| `terminal` | `backend` (local/docker/ssh/modal), `cwd`, `timeout` (180) |
| `compression` | `enabled`, `threshold` (0.50), `target_ratio` (0.20) |
| `display` | `skin`, `interface` (cli/tui), `tool_progress`, `show_reasoning`, `show_cost`, `language` |
| `stt` | `enabled`, `provider` (local/groq/openai/mistral) |
| `tts` | `provider` (edge/elevenlabs/openai/minimax/mistral/neutts) |
| `memory` | `memory_enabled`, `user_profile_enabled`, `provider` |
| `security` | `tirith_enabled`, `website_blocklist` |
| `delegation` | `model`, `provider`, `base_url`, `api_key`, `max_iterations` (50), `reasoning_effort` |
| `checkpoints` | `enabled`, `max_snapshots` (50) |
| `curator` | `enabled`, `consolidate` (false), `interval_hours`, `stale_after_days`, `archive_after_days`, `backup.*` |

### 常用配置操作

```bash
# 查看/编辑
hermes config
hermes config edit

# 设置值
hermes config set model.default anthropic/claude-sonnet-4
hermes config set model.provider anthropic
hermes config set agent.max_turns 120
hermes config set display.language zh

# 秘钥管理（需重启会话）
hermes config set security.redact_secrets true    # 默认开启
hermes config set security.redact_secrets false   # 仅调试时关闭

# PII 脱敏（网关消息）
hermes config set privacy.redact_pii true
hermes config set privacy.redact_pii false        # 默认关闭

# 审批模式
hermes config set approvals.mode smart   # 推荐
hermes config set approvals.mode manual  # 始终提示
hermes config set approvals.mode off     # 等同 --yolo

# 单次调用绕过
hermes --yolo chat -q "...
export HERMES_YOLO_MODE=1
```

---

## 网关/消息平台操作

### 支持的平台（20+）

Telegram, Discord, Slack, WhatsApp (Baileys + 官方 Business Cloud API), iMessage (Photon — `hermes photon setup`, 无需 Mac 中继), Signal, Email, SMS, Matrix, Mattermost, Microsoft Teams, LINE, SimpleX, ntfy, Google Chat, Home Assistant, DingTalk, Feishu, WeCom, Weixin (WeChat), Raft (代理网络), API Server, Webhooks.

### 网关操作

```bash
# 启动/管理
hermes gateway run          # 前台运行
hermes gateway install      # 安装为 systemd/launchd 服务
hermes gateway start        # 启动服务
hermes gateway stop         # 停止服务
hermes gateway restart      # 重启
hermes gateway status       # 状态检查
hermes gateway setup        # 交互式平台配置
```

### 网关斜杠命令（在消息平台中使用）

```
/approve        批准待定命令
/deny           拒绝待定命令
/restart        重启网关
/sethome        设置当前聊天为家庭频道
/update         更新 Hermes
/topic          Telegram DM 话题会话
/platforms      显示平台连接状态
```

### 发送一次性消息

```bash
hermes send --platform telegram --chat -1001234567890 "Hello from Hermes!"
```

---

## 多代理与任务委派

### 委派模式对比

| 特性 | `delegate_task` | 生成 `hermes` 进程 |
|------|-----------------|-------------------|
| 隔离 | 独立对话，共享进程 | 完全独立进程 |
| 持续时间 | 分钟（受父循环限制） | 小时/天 |
| 工具访问 | 父工具子集 | 完整工具访问 |
| 交互性 | 否 | 是（PTY 模式） |
| 用例 | 快速并行子任务 | 长期自主任务 |

### delegate_task 工具（会话内）

```python
# 单任务
delegate_task(goal="Research GRPO papers", context="Write summary to ~/research/grpo.md")

# 批量并行（最多 3 个并发）
delegate_task(tasks=[
    {"goal": "Task A", "context": "..."},
    {"goal": "Task B", "context": "..."},
    {"goal": "Task C", "context": "..."}
])

# 角色：leaf（默认，不可再委派）或 orchestrator（可生成子 worker）
delegate_task(goal="...", role="orchestrator")
```

### 生成独立 Hermes 进程（通过 terminal 工具）

```bash
# 单次模式（火后不管）
terminal(command="hermes chat -q 'Research GRPO and write to ~/research/grpo.md'", timeout=300)

# 后台长任务
terminal(command="hermes chat -q 'Set up CI/CD for ~/myapp'", background=true, notify_on_complete=true)

# 交互式 PTY 模式（通过 tmux）
terminal(command="tmux new-session -d -s agent1 -x 120 -y 40 'hermes'", timeout=10)
terminal(command="sleep 8 && tmux send-keys -t agent1 'Build FastAPI auth service' Enter", timeout=15)
terminal(command="sleep 20 && tmux capture-pane -t agent1 -p", timeout=5)
terminal(command="tmux send-keys -t agent1 'Add rate limiting' Enter", timeout=5)
terminal(command="tmux send-keys -t agent1 '/exit' Enter && sleep 2 && tmux kill-session -t agent1", timeout=10)
```

### 多代理协调示例

```bash
# Agent A: 后端
tmux new-session -d -s backend -x 120 -y 40 'hermes -w'
tmux send-keys -t backend 'Build REST API for user management' Enter

# Agent B: 前端
tmux new-session -d -s frontend -x 120 -y 40 'hermes -w'
tmux send-keys -t frontend 'Build React dashboard for user management' Enter

# 检查进度、中继上下文
tmux capture-pane -t backend -p | tail -30
tmux send-keys -t frontend 'Here is the API schema from backend: ...' Enter
```

### 会话恢复

```bash
# 恢复最近会话
tmux new-session -d -s resumed 'hermes --continue'

# 恢复特定会话
tmux new-session -d -s resumed 'hermes --resume 20260225_143052_a1b2c3'
```

---

## 定时任务

### cronjob 工具（会话内）

```python
# 创建定时任务
cronjob(action="create", 
        schedule="0 9 * * *",           # 每天 9:00
        prompt="Daily briefing: summarize yesterday's emails and calendar",
        skills=["email", "lark-calendar"],
        deliver="telegram:-1001234567890:17585",
        name="Daily Morning Briefing")

# 列出任务
cronjob(action="list")

# 暂停/恢复/运行/删除
cronjob(action="pause", job_id="job_123")
cronjob(action="resume", job_id="job_123")
cronjob(action="run", job_id="job_123")
cronjob(action="remove", job_id="job_123")

# 链式任务：job B 消费 job A 的输出
cronjob(action="create", 
        schedule="every 1h",
        prompt="Process data from previous job",
        context_from=["job_data_collector"])
```

### CLI 定时任务

```bash
hermes cron create "0 9 * * *"          # 交互式创建
hermes cron list
hermes cron edit job_123
hermes cron pause job_123
hermes cron resume job_123
hermes cron run job_123
hermes cron remove job_123
hermes cron status
```

### 关键参数

- **调度格式**：`30m`、`every 2h`、`0 9 * * *`、ISO 时间戳
- **技能**：按顺序加载的技能列表
- **模型/提供商**：每任务覆盖
- **脚本**：运行前数据收集脚本（`no_agent=True` 时脚本即整个任务）
- **context_from**：链式任务，注入上游输出
- **workdir**：在特定目录运行（加载该目录的 AGENTS.md/CLAUDE.md）
- **投递**：`origin`（默认）、`local`（仅保存）、`all`（广播）、或 `platform:chat_id:thread_id`

---

## MCP 服务器管理

### 添加/移除/列出/测试

```bash
hermes mcp add NAME --url http://localhost:3000/mcp
hermes mcp add NAME --command "npx @modelcontextprotocol/server-filesystem /path"
hermes mcp remove NAME
hermes mcp list
hermes mcp test NAME
hermes mcp configure NAME    # 切换工具选择
```

### 作为 MCP 服务器运行 Hermes

```bash
hermes mcp serve
```

### 内置 MCP 客户端

- 自动发现工具
- 作为一等工具暴露
- 目录安装：`hermes mcp install <name>`

详细文档：`skill_view(name="hermes-agent", file_path="references/native-mcp.md")`

---

## 配置文件与路径

### 关键路径

```
~/.hermes/config.yaml              # 主配置
~/.hermes/.env                     # API 密钥
$HERMES_HOME/skills/               # 已安装技能
~/.hermes/sessions/                # 网关路由索引、请求转储、*.jsonl 转录
~/.hermes/state.db                 # 规范会话存储（SQLite + FTS5）
~/.hermes/logs/                    # 网关与错误日志
~/.hermes/auth.json                # OAuth 令牌与凭证池
~/.hermes/hermes-agent/            # 源码（如 git 安装）
```

### 配置文件隔离

```
~/.hermes/profiles/<name>/         # 相同布局：config.yaml, .env, skills/, sessions/, logs/, auth.json
```

### 项目上下文文件（按优先级自动注入）

| 文件 | 发现范围 | 适用场景 |
|------|----------|----------|
| `.hermes.md` / `HERMES.md` | 向上遍历父目录至 git 根 | 多层级项目规则（根 + 子包覆盖） |
| `AGENTS.md` / `agents.md` | **仅当前工作目录** | 可移植代理指令（Hermes, Claude Code, Codex 等） |
| `CLAUDE.md` / `claude.md` | 仅当前工作目录 | 同上，Claude 风味 |
| `.cursorrules` / `.cursor/rules/*.mdc` | 仅当前工作目录 | 从 Cursor 迁移 |

`SOUL.md`（在 `$HERMES_HOME`）独立且始终加载——设定代理身份而非项目规则。

### 禁用单次会话

```bash
hermes --ignore-rules    # 跳过所有项目上下文文件 + SOUL.md + 用户配置 + 插件 + MCP
```

---

## Webhooks 与自动化

### Webhook 订阅

```bash
hermes webhook subscribe my-webhook   # 在 /webhooks/my-webhook 创建路由
hermes webhook list
hermes webhook test my-webhook
hermes webhook remove my-webhook
```

### 载荷模板与事件驱动模式

详见：`skill_view(name="hermes-agent", file_path="references/webhooks.md")`

---

## 桌面应用与仪表盘

### 桌面应用（Electron）

```bash
hermes desktop    # 或 hermes gui
```

功能：流式聊天、会话列表、拖拽/剪贴板粘贴文件、Cmd+K 调色板、状态栏模型选择器、可重绑定快捷键、原生通知、实时子代理观察窗口、VS Code Marketplace 主题、每配置文件远程网关登录（OAuth 或用户名/密码）。

### Web 仪表盘

```bash
hermes dashboard
```

完整管理面板：配置所有消息渠道、MCP 目录、webhooks/hooks、记忆、完整配置文件构建器（模型 + 技能 + MCP），以及嵌入式 `hermes --tui` 聊天。OAuth/token 门保护。

### OpenAI 兼容代理

```bash
hermes proxy
```

暴露 `http://localhost:port` OpenAI API，由当前 OAuth 提供商支持（Claude Pro, ChatGPT Pro, SuperGrok）。指向 Codex CLI、Aider、Cline、Continue 或任意脚本——无需 API 密钥。

---

## 自动化蓝图

选择命名自动化，Hermes 询问所需参数（无需 cron 语法）。一个定义渲染为：
- 仪表盘表单
- 斜杠命令
- 代理对话
- 文档目录条目

---

## 自动化操控最佳实践

### 通过 OpenClaw (agent-browser) 操控 Web 仪表盘

```powershell
# 1. 确保 Chrome/CDP 就绪（参考 agent-browser skill）
& $agentBrowserCmd --cdp 9222 open http://localhost:3000  # dashboard 默认端口
& $agentBrowserCmd --cdp 9222 wait --load networkidle
& $agentBrowserCmd --cdp 9222 snapshot -i

# 2. 登录（如需）
# 3. 导航配置页面、技能管理、网关设置等
# 4. 使用 fill/click/snapshot 循环完成操作
```

### 通过终端自动化 CLI

```bash
# 非交互单次查询（最适合自动化）
hermes chat -q "Your prompt here" --model anthropic/claude-sonnet-4 --toolsets web,terminal,file

# 后台长任务
hermes chat -q "Long running task" --background  # 或使用 terminal(background=true)
```

### 通过网关 API / Webhook 触发

```bash
# 发送消息触发代理
curl -X POST http://localhost:8080/webhooks/my-webhook \
  -H "Content-Type: application/json" \
  -d '{"text": "Run the daily report"}'
```

### 会话恢复自动化

```bash
# 获取最近会话 ID
hermes sessions list --limit 1 --format json

# 恢复指定会话
hermes --resume <session_id> chat -q "Continue where we left off"
```

---

## 故障排查

### 常见问题快速诊断

| 问题 | 排查步骤 |
|------|----------|
| 语音不工作 | 1. `stt.enabled: true` in config.yaml<br>2. `pip install faster-whisper` 或设置 API key<br>3. 网关: `/restart`; CLI: 退出重启 |
| 工具不可用 | 1. `hermes tools` 检查工具集启用状态<br>2. 检查 `.env` 必需环境变量<br>3. `/reset` 后生效 |
| 模型/提供商问题 | 1. `hermes doctor`<br>2. `hermes auth` 重新认证<br>3. 检查 `.env` API key |
| 更改不生效 | - 工具/技能: `/reset` 新会话<br>- 配置: 网关 `/restart`, CLI 退出重启<br>- 代码: 重启 CLI 或网关进程 |
| 技能不显示 | 1. `hermes skills list` 验证安装<br>2. `hermes skills config` 检查平台启用<br>3. 显式加载: `/skill name` 或 `hermes -s name` |
| 网关问题 | `grep -i "failed to send\|error" ~/.hermes/logs/gateway.log | tail -20` |

### 平台特定问题

- **Discord 机器人静默**：必须在 Bot → Privileged Gateway Intents 启用 **Message Content Intent**
- **Slack 仅 DM 工作**：必须订阅 `message.channels` 事件
- **Windows 网关随 SSH 登出死亡**：`sudo loginctl enable-linger $USER`
- **WSL2 网关关闭**：`/etc/wsl.conf` 设置 `systemd=true`
- **网关崩溃循环**：`systemctl --user reset-failed hermes-gateway`

### Windows 特有问题

- **Alt+Enter 不换行**：用 **Ctrl+Enter**（CLI 在 Windows 绑定为换行）
- **配置 UTF-8 BOM**：`hermes config edit` 正确写入；记事本会加 BOM
- **WinError 10106**：沙箱子进程无法创建 AF_INET socket，通常是环境清理丢了 `SYSTEMROOT`/`WINDIR`/`COMSPEC`

---

## 快速参考卡片

### 最常用命令速查

```bash
# 启动聊天
hermes

# 单次查询
hermes chat -q "question"

# 切换模型
hermes model

# 启用工具
hermes tools enable web

# 安装技能
hermes skills install skill-name

# 网关启动
hermes gateway run

# 定时任务
hermes cron create "0 9 * * *"

# 查看配置
hermes config

# 会话列表
hermes sessions list
```

### 会话内最常用斜杠命令

```
/new           新会话
/skill name    加载技能
/tools         管理工具
/config        查看配置
/model name    切换模型
/voice on      开启语音
/yolo          绕过确认
/help          查看所有命令
```

---

## 扩展阅读

- **官方文档**: https://hermes-agent.nousresearch.com/docs/
- **源码**: https://github.com/NousResearch/hermes-agent
- **CLI 帮助**: `hermes --help` / `hermes <command> --help`
- **斜杠命令**: 会话内 `/help` 或 [在线参考](https://hermes-agent.nousresearch.com/docs/reference/slash-commands)
- **技能目录**: `hermes skills browse` 或 [在线目录](https://hermes-agent.nousresearch.com/docs/reference/skills-catalog)
- **工具参考**: [工具参考](https://hermes-agent.nousresearch.com/docs/reference/tools-reference)
- **配置参考**: [配置文档](https://hermes-agent.nousresearch.com/docs/user-guide/configuration)
- **提供商设置**: [提供商指南](https://hermes-agent.nousresearch.com/docs/integrations/providers)
- **平台设置**: `hermes gateway setup` 或 [消息指南](https://hermes-agent.nousresearch.com/docs/user-guide/messaging/)
- **MCP 指南**: [MCP 文档](https://hermes-agent.nousresearch.com/docs/user-guide/features/mcp)
- **配置文件**: [配置文件文档](https://hermes-agent.nousresearch.com/docs/user-guide/profiles)
- **定时任务**: [Cron 文档](https://hermes-agent.nousresearch.com/docs/user-guide/features/cron)
- **记忆**: [记忆文档](https://hermes-agent.nousresearch.com/docs/user-guide/features/memory)
- **环境变量**: [环境变量参考](https://hermes-agent.nousresearch.com/docs/reference/environment-variables)