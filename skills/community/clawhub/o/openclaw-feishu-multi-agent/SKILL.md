---
name: openclaw-feishu-multi-agent
description: Build and troubleshoot OpenClaw multi-agent workflows on Feishu. This skill teaches coordinator and specialist agents to combine visible `<at>` mentions with `sessions_send` so delegation, handoffs, and multi-hop discussions work reliably in group chats. Use it to scaffold new setups, audit existing configs, repair broken session metadata, and generate reusable role-based artifacts.
---

# OpenClaw Feishu Multi-Agent

## Goal

让 OpenClaw 的多个独立 agent 在同一个飞书群里协作：

- 协调者 agent 负责读群消息、决定谁处理
- 群里能看到显式 `<at>`
- 被点名的 agent 会主动回群
- agent 之间可以继续串联讨论

## 先判断是哪种场景

### 场景 A：用户已经有多 agent

优先检查并修复：

1. `~/.openclaw/openclaw.json`
2. `~/.openclaw/PROTOCOL.md`
3. 各 agent 的 `IDENTITY.md` / `SOUL.md`
4. 会话存储是否把 Feishu 群上下文写坏
5. gateway 重启后是否恢复

### 场景 B：用户还没有多 agent

先帮助用户定义角色表，再补齐：

1. agent roster
2. Feishu account bindings
3. 协调协议
4. 各 agent 身份文件
5. 验证话术

## 核心规则

### 规则 1

飞书里的 `<at>` 只是“给人看见谁被点名了”。

### 规则 2

OpenClaw 里的 `sessions_send` 才是“真正唤醒另一个 agent”。

### 规则 3

每一次委派都必须同时做两步：

1. 在飞书群里发可视化 `<at>`
2. 用 `sessions_send` 向目标 agent 投递任务

少一步都不算成功。

### 规则 4

`sessions_send` 默认使用 `sessionKey`：

```text
agent:{targetAgentId}:feishu:group:oc_xxx
```

不要给 `sessions_send` 传 `agentId`。

## 推荐实施顺序

1. 盘点角色、agentId、Feishu accountId、Open ID、职责和触发词
2. 标准化 `~/.openclaw/PROTOCOL.md`
3. 把协调者 agent 写成“默认总调度”
4. 把专业 agent 写成“收到 sessions_send 后直接回群”
5. 检查 `openclaw.json` 的 `agents.list`、`bindings`、`tools.agentToAgent.allow`
6. 检查群 session 是否保持 `channel=feishu`、`chatType=group`
7. 重启 gateway
8. 用真实飞书话术验证

## 角色设计要求

不要把方案写死成 Steve / Jonathan / Brendan / Seth。

始终把角色抽象成：

- `coordinator`: 默认调度者
- `specialists`: 一个或多个专业 agent

角色名、人设、职责、触发词都应该允许自定义。

## 你需要产出的东西

根据用户场景，通常会创建或更新：

- `~/.openclaw/PROTOCOL.md`
- `~/.openclaw/openclaw.json`
- `{agentDir}/IDENTITY.md`
- 可选：一个团队协作 skill，避免 agent 退回单 bot 多角色思路

## 修复时重点检查

### 1. 路由遗漏

如果协调者只叫了部分 agent：

- 检查它的默认召集规则
- 检查“其他人 / 大家 / 团队一起讨论”是否被错误窄化

### 2. sessions_send 超时

超时不等于没收到。继续检查：

- 目标 agent session 是否生成
- 目标 agent 是否进入长时间工具执行
- 日志里是否出现 nested run / timeout

### 3. 会话写坏

如果目标 agent “像是收到了，但没回群”，重点检查 session store：

- `channel` 是否被错误写成 `webchat`
- `deliveryContext.to` 是否缺失
- `accountId` 是否缺失
- `chatType` 是否还是 `group`

## 参考文件

- 详细方案和诊断步骤：见 [reference.md](reference.md)
- 可复用模板：见 [templates.md](templates.md)
- 角色样例：见 [roles.example.json](roles.example.json)

## Utility Scripts

### 1. 统一入口

优先使用统一入口，避免记多个脚本名：

```bash
python ".cursor/skills/openclaw-feishu-multi-agent/scripts/manage_feishu_multi_agent.py" --help
```

如果想一把跑完“生成 -> 落地 -> 审计”：

```bash
python ".cursor/skills/openclaw-feishu-multi-agent/scripts/manage_feishu_multi_agent.py" bootstrap \
  --roles ".cursor/skills/openclaw-feishu-multi-agent/roles.example.json" \
  --output-dir "/tmp/openclaw-feishu-artifacts" \
  --apply-identities
```

加上 `--write --backup` 才会真正写入 `~/.openclaw/`。

### 2. 生成可落地模板

当用户还没配好多 agent，或希望把角色表转换成可落地文档时，运行：

```bash
python ".cursor/skills/openclaw-feishu-multi-agent/scripts/render_feishu_multi_agent.py" \
  --roles ".cursor/skills/openclaw-feishu-multi-agent/roles.example.json" \
  --output-dir "/tmp/openclaw-feishu-artifacts"
```

产出：

- `PROTOCOL.generated.md`
- `openclaw.generated.json`
- `roles.generated.json`
- `identities/*.IDENTITY.generated.md`

`openclaw.generated.json` 现在会同时带出：

- `agents.list`
- `bindings`
- `channels.feishu.accounts`
- `tools.sessions.visibility`
- `tools.agentToAgent.allow`

### 3. 审计现有配置

当用户已经有多 agent，想快速检查 `openclaw.json` 是否与角色表一致时，运行：

```bash
python ".cursor/skills/openclaw-feishu-multi-agent/scripts/audit_feishu_multi_agent.py" \
  --roles "/path/to/roles.json" \
  --config "~/.openclaw/openclaw.json"
```

重点检查：

- `agents.list`
- `bindings`
- `channels.feishu.accounts`
- `tools.sessions.visibility`
- `tools.agentToAgent.allow`

### 4. 半自动落地到 `~/.openclaw/`

当用户希望把角色表直接应用到自己的 OpenClaw 环境时，先 dry-run：

```bash
python ".cursor/skills/openclaw-feishu-multi-agent/scripts/apply_feishu_multi_agent.py" \
  --roles "/path/to/roles.json" \
  --apply-identities
```

确认无误后再写入：

```bash
python ".cursor/skills/openclaw-feishu-multi-agent/scripts/apply_feishu_multi_agent.py" \
  --roles "/path/to/roles.json" \
  --apply-identities \
  --write --backup
```

这个脚本会：

- 合并 `openclaw.json` 里的 `agents.list`
- 合并 `channels.feishu.accounts`
- 合并 `bindings`
- 打开 `tools.sessions.visibility=all`
- 打开 `tools.agentToAgent.enabled=true`
- 补齐 `tools.agentToAgent.allow`
- 写入 `~/.openclaw/PROTOCOL.md`
- 可选写入各 agent 的 `IDENTITY.md`

### 5. 修复 Feishu 群 session

当某个 agent “像是收到了，但没回群”，优先检查并按需修复 session metadata：

```bash
python ".cursor/skills/openclaw-feishu-multi-agent/scripts/repair_feishu_group_sessions.py" \
  --roles "/path/to/roles.json" \
  --group-id "oc_xxx"
```

如需直接写回：

```bash
python ".cursor/skills/openclaw-feishu-multi-agent/scripts/repair_feishu_group_sessions.py" \
  --roles "/path/to/roles.json" \
  --group-id "oc_xxx" \
  --fix --backup
```

## 交付风格

- 中文说明为主
- 代码、路径、键名、命令用英文
- 默认提供通用模板，不绑定用户现有角色名
