---
name: agent-creator
description: 创建新的 OpenClaw Agent。用于当用户要求创建新 agent、添加新机器人、配置新模型测试环境时触发。
---

# Agent Creator

创建新 OpenClaw Agent 的完整 checklist。

## 创建步骤

### 1. 创建工作区目录

```bash
mkdir -p ~/.openclaw/workspace-{agentId}/agent
mkdir -p ~/.openclaw/agents/{agentId}/agent
```

### 2. 必需的基础文件

在 `~/.openclaw/workspace-{agentId}/` 下创建：

| 文件 | 用途 | 模板位置 |
|-----|------|---------|
| **IDENTITY.md** | 身份定义（名字、emoji、风格） | [templates/IDENTITY.md](templates/IDENTITY.md) |
| **SOUL.md** | 灵魂/个性定义 | [templates/SOUL.md](templates/SOUL.md) |
| **USER.md** | 用户信息 | [templates/USER.md](templates/USER.md) |
| **AGENTS.md** | Agent 行为协议 | [templates/AGENTS.md](templates/AGENTS.md) |
| **MEMORY.md** | 热缓存 | [templates/MEMORY.md](templates/MEMORY.md) |

⚠️ **常见遗漏**：AGENTS.md 和 MEMORY.md 容易被漏掉，必须从 templates 复制。

### 3. Agent 配置目录

在 `~/.openclaw/workspace-{agentId}/agent/` 下创建：

| 文件 | 内容 |
|-----|------|
| **models.json** | 模型配置（从主 agent 复制并修改 provider） |
| **auth.json** | 认证配置（空对象 `{}` 或从主 agent 复制） |

### 4. 更新 openclaw.json

修改 `~/.openclaw/openclaw.json`：

1. **agents.list** — 添加新 agent：
```json
{
  "id": "{agentId}",
  "workspace": "/home/axelhu/.openclaw/workspace-{agentId}",
  "model": {
    "primary": "{provider}/{modelId}",
    "fallbacks": []
  }
}
```

2. **agentToAgent.allow** — 添加 agentId 到列表

3. **可选：bindings + channels** — 如需飞书绑定：
```json
{
  "agentId": "{agentId}",
  "match": {
    "channel": "feishu",
    "accountId": "{accountId}"
  }
}
```

并在 `channels.accounts` 中添加对应配置

### 5. 验证

运行 `openclaw status` 确认新 agent 已加载。

## 完整示例

```bash
# 1. 创建目录
mkdir -p ~/.openclaw/workspace-{agentId}/agent

# 2. 复制模板文件（必须！）
cp ~/.openclaw/skills/agent-creator/templates/IDENTITY.md ~/.openclaw/workspace-{agentId}/
cp ~/.openclaw/skills/agent-creator/templates/SOUL.md ~/.openclaw/workspace-{agentId}/
cp ~/.openclaw/skills/agent-creator/templates/USER.md ~/.openclaw/workspace-{agentId}/
cp ~/.openclaw/skills/agent-creator/templates/AGENTS.md ~/.openclaw/workspace-{agentId}/
cp ~/.openclaw/skills/agent-creator/templates/MEMORY.md ~/.openclaw/workspace-{agentId}/

# 3. 创建 agent 配置
# 编辑 agent/models.json 和 agent/auth.json

# 4. 更新 openclaw.json
# 添加到 agents.list, agentToAgent.allow, bindings, channels
```

## 检查清单

创建完成后确认：
- [ ] IDENTITY.md 存在（从 templates 复制）
- [ ] SOUL.md 存在（从 templates 复制）
- [ ] USER.md 存在（从 templates 复制）
- [ ] AGENTS.md 存在（从 templates 复制）
- [ ] MEMORY.md 存在（从 templates 复制）
- [ ] agent/models.json 存在
- [ ] agent/auth.json 存在
- [ ] openclaw.json 中 agents.list 已更新
- [ ] openclaw.json 中 agentToAgent.allow 已更新
- [ ] ✅ 完成后询问用户：是否需要配置飞书绑定？

## 飞书绑定（可选）

如需配置飞书，需要以下信息：

### 需要用户提供
1. **accountId**: 飞书机器人账号 ID（如 `longcat`）
2. **botName**: 机器人名称（如 "测试龙猫"）
3. **appId**: 飞书应用 ID
4. **appSecret**: 飞书应用密钥

### 配置步骤

1. **在 openclaw.json 中添加 bindings**：
```json
{
  "agentId": "{agentId}",
  "match": {
    "channel": "feishu",
    "accountId": "{accountId}"
  }
}
```

2. **在 openclaw.json 中添加 channels 配置**：
```json
"{accountId}": {
  "appId": "{appId}",
  "appSecret": "{appSecret}",
  "botName": "{botName}"
}
```

### 完整示例

创建完成后，询问用户：
> "Agent 创建完成！是否需要配置飞书机器人绑定？如需要，请提供：accountId、botName、appId、appSecret"
