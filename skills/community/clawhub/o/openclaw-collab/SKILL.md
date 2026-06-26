---
name: openclaw-collab
description: Hermes 与本地 OpenClaw 协同工作 — 模型互调、记忆共享、任务分工
version: 1.0
created: 2026-04-19
---

# OpenClaw 协同 Skill

## 环境信息

- OpenClaw: /usr/local/bin/openclaw, 版本 2026.4.15
- Gateway: localhost:18789 (WebSocket + Control UI)
- Workspace: ~/.openclaw/workspace/
- 桥接脚本: ~/.hermes/scripts/openclaw-bridge.py
- 消息发送工具: ~/.hermes/scripts/hermes-to-openclaw.py (推荐)

## 三条协同路径

### 1. 模型互调 — openclaw-bridge.py

**重要区别**: `chat` 和 `write` 有不同的用途

```bash
# 基本聊天 - 仅调用模型，不发送消息给OpenClaw
python3.11 ~/.hermes/scripts/openclaw-bridge.py chat -p "问题"

# 指定模型
python3.11 ~/.hermes/scripts/openclaw-bridge.py chat -m google/gemma-3-27b-it -p "问题"

# 带系统提示 + JSON输出
python3.11 ~/.hermes/scripts/openclaw-bridge.py chat -p "问题" --system "系统提示" --json

# 读取 OpenClaw 记忆
python3.11 ~/.hermes/scripts/openclaw-bridge.py read memory/2026-04-19.md
python3.11 ~/.hermes/scripts/openclaw-bridge.py read memory/projects/

# 写入 OpenClaw 记忆 - 这是发送消息给OpenClaw的正确方式
python3.11 ~/.hermes/scripts/openclaw-bridge.py write memory/collab/hermes-to-openclaw.md "内容"
```

**使用场景**:
- `chat`: 需要OpenClaw模型回答问题，但不需要持久化消息
- `write`: 需要OpenClaw看到并处理消息（任务分配、通知、协同工作）

**常见错误**: 使用 `chat` 试图发送消息给OpenClaw，但OpenClaw不会收到。应该使用 `write memory/collab/`。

### 1.5 直接唤醒OpenClaw — hermes-to-openclaw.py (推荐)

**新工具**: `hermes-to-openclaw.py` - 直接唤醒OpenClaw处理消息，无需轮询

```bash
# 基本用法 - 写入消息并直接唤醒OpenClaw
~/.hermes/scripts/hermes-to-openclaw.py "消息内容"

# 指定agent
~/.hermes/scripts/hermes-to-openclaw.py "消息内容" --agent main

# 只写入消息，不唤醒OpenClaw
~/.hermes/scripts/hermes-to-openclaw.py "消息内容" --write-only

# JSON格式输出
~/.hermes/scripts/hermes-to-openclaw.py "消息内容" --json
```

**使用场景**:
- 需要OpenClaw立即处理消息（实时协同）
- 需要获取OpenClaw的回复
- 任务分配、通知、协同工作

**优势**:
- 直接唤醒OpenClaw，无需轮询
- 实时获取回复
- 支持JSON格式输出
- 可选只写入消息模式

**与openclaw-bridge.py的对比**:
- `openclaw-bridge.py write`: 只写入消息，需要OpenClaw轮询检查
- `hermes-to-openclaw.py`: 写入消息并直接唤醒OpenClaw，实时获取回复

**详细文档**: `~/.hermes/scripts/HERMES-TO-OPENCLAW.md`

可用模型（NVIDIA API）:
- minimaxai/minimax-m2.5 (推荐，稳定)
- minimaxai/minimax-m2.7
- z-ai/glm5 (不稳定，容易超时!)
- z-ai/glm-5.1
- google/gemma-3-27b-it
- google/gemma-3-12b-it

### 2. 记忆共享 — 文件系统

共享目录: `~/.openclaw/workspace/`

规则:
- Hermes 可自由读取 OpenClaw 的 memory/
- Hermes 写入时在内容末尾标注 `[by Hermes]`
- 协同消息放入 `memory/collab/` 目录
- 不直接修改 OpenClaw 的日志原文，写独立文件

也可直接用 read_file/write_file/patch 操作 workspace 下的文件。

### 3. 任务分工

| 任务类型 | 负责 | 原因 |
|----------|------|------|
| 达梦数据库/SQL | Hermes | 专门 skill |
| Python/脚本 | Hermes | 原生支持 |
| 飞书/微信交互 | OpenClaw | 原生集成 |
| Web搜索/资讯 | OpenClaw | web-search 插件 |
| 代码审查 | 双模型交叉 | 各审一遍 |

## 已知问题

1. **openclaw agent CLI 超时** — GLM5 在 NVIDIA 上不稳定，用 bridge 直接调 API 绕过
2. **openclaw.json 修复记录** — includeDefaultMemor->includeDefaultMemory，移除非法 memory.flush 键
3. **skills symlink escape 警告** — 不影响使用
4. **消息发送混淆** — `chat` 命令只是调用模型对话，不会发送消息给OpenClaw。要发送消息必须使用 `write memory/collab/` 或直接写入文件

## 常见错误

### 错误1: 使用 chat 试图发送消息给OpenClaw

**错误做法**:
```bash
# 这只是调用模型，OpenClaw不会收到消息
~/.hermes/scripts/openclaw-bridge.py chat -p "请帮我上传skill到clawhub"
```

**正确做法**:
```bash
# 方法1: 写入collab目录，OpenClaw会读取（需要轮询）
~/.hermes/scripts/openclaw-bridge.py write memory/collab/upload-skill.md "任务内容"

# 方法2: 直接唤醒OpenClaw（推荐，实时获取回复）
~/.hermes/scripts/hermes-to-openclaw.py "请帮我上传skill到clawhub"
```

### 错误2: 消息格式不规范

**错误做法**:
```bash
# 没有标识来源
echo "消息内容" > ~/.openclaw/workspace/memory/collab/message.md
```

**正确做法**:
```bash
# 方法1: 使用hermes-to-openclaw.py（推荐，自动格式化）
~/.hermes/scripts/hermes-to-openclaw.py "消息内容"

# 方法2: 手动创建，包含时间戳和来源标识
cat > ~/.openclaw/workspace/memory/collab/message.md << 'EOF'
# Hermes -> OpenClaw 消息

## 时间: 2026-04-26 08:45

## 内容: 任务描述

[by Hermes]
EOF
```

### 错误3: 使用openclaw-bridge.py write期望实时回复

**错误做法**:
```bash
# openclaw-bridge.py write只写入消息，不会唤醒OpenClaw
~/.hermes/scripts/openclaw-bridge.py write memory/collab/message.md "消息内容"
# 然后期望立即得到回复 - 不会发生！
```

**正确做法**:
```bash
# 使用hermes-to-openclaw.py直接唤醒OpenClaw并获取回复
~/.hermes/scripts/hermes-to-openclaw.py "消息内容"
```

## 模型可用性总结（实测 2026-04-19）

| 模型 | bridge chat | openclaw agent --local | openclaw agent (gateway路由) | 备注 |
|------|-------------|----------------------|-----------------------------|------|
| z-ai/glm5 | 502 Bad Gateway (超时) | 超时 >120s | 路由到其他模型 | 最不稳定 |
| minimaxai/minimax-m2.5 | 可用 | 超时 >120s | 未测试 | bridge推荐，但agent CLI也慢 |
| minimaxai/minimax-m2.7 | 未测试 | 未测试 | 未测试 | OpenClaw main agent默认配置 |
| google/gemma-3-27b-it | 可用 | 未测试 | **schema rejected** | 不支持OpenClaw工具调用schema |

结论: **三条路径都有模型问题**，bridge最可靠但仅限纯聊天，OpenClaw agent CLI普遍超时，gateway路由可能切到不支持工具的模型。

## openclaw agent CLI 命令参考

```bash
# 通过 gateway 路由发消息给 agent（会路由到 main agent 配置的模型）
openclaw agent --agent main --message "问题" --json --timeout 30

# 本地模式（需要 shell 里有 API key）
openclaw agent --agent main --local --message "问题" --json

# 指定 session
openclaw agent --session-id <id> --message "问题"
```

注意: `--json` 输出包含完整的 systemPromptReport，能看到实际使用的模型、工具列表、skill 列表等诊断信息。

## ClawHub 发布

**工作流程**: Hermes完成skill开发后，通过消息发送给OpenClaw去上传到clawhub.ai，不要自己直接使用clawhub CLI上传。这是协同工作的分工，OpenClaw负责发布任务。

### Hermes -> OpenClaw 发布流程

```bash
# 1. Hermes完成skill开发和测试
# 2. Hermes发送发布请求给OpenClaw
~/.hermes/scripts/hermes-to-openclaw.py "请将 /Users/a1234/.openclaw/workspace/skills/ops-maintenance 这个skill发布到clawhub.ai上。

Skill信息：
- 名称: 运维助手 v2.0
- Slug: ops-maintenance
- 版本: 2.0.1
- 更新日志: v2.0 优化：使用ssh2库替代child_process.exec，添加SSH连接池、SFTP文件传输、审计日志等优化功能。"
```

### OpenClaw 发布步骤

OpenClaw收到消息后，执行以下步骤：

```bash
# 1. 检查skill目录结构
ls -la /Users/a1234/.openclaw/workspace/skills/ops-maintenance/

# 2. 检查SKILL.md格式
cat /Users/a1234/.openclaw/workspace/skills/ops-maintenance/SKILL.md

# 3. 发布到clawhub.ai
clawhub publish /Users/a1234/.openclaw/workspace/skills/ops-maintenance \
  --slug ops-maintenance \
  --name "运维助手 v2.0" \
  --version 2.0.1 \
  --changelog "v2.0 优化：使用ssh2库替代child_process.exec，添加SSH连接池、SFTP文件传输、审计日志等优化功能"

# 4. 验证发布结果
clawhub search ops-maintenance
```

### 发布消息模板

```bash
~/.hermes/scripts/hermes-to-openclaw.py "请将 [skill路径] 这个skill发布到clawhub.ai上。

Skill信息：
- 名称: [skill名称]
- Slug: [skill-slug]
- 版本: [版本号]
- 更新日志: [更新内容]"
```

### 注意事项

1. **不要自己发布** - Hermes不要直接使用clawhub CLI发布skill
2. **消息格式** - 包含完整的skill信息（名称、slug、版本、更新日志）
3. **验证发布** - OpenClaw发布后需要验证搜索结果
4. **协同分工** - Hermes负责开发测试，OpenClaw负责发布部署

## 之前卡顿的根因

NVIDIA 平台上的 GLM5 模型频繁超时（gateway 日志: `timeout from=nvidia/z-ai/glm5`），导致 OpenClaw agent 无法正常回复。解决方法：默认使用 minimax-m2.5。但实际上所有模型在 OpenClaw agent CLI 模式下都可能超时，根本原因是模型推理速度 + 工具调用链长度。
