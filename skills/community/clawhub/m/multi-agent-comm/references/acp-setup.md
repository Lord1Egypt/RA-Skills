# ACP Setup Guide — Agent Communication Protocol 配置指南

## 1. 在 OpenClaw Gateway 中定义多 Agent

OpenClaw 支持在 gateway 配置中定义多个独立 Agent，每个有自己的 system prompt、skills 和模型配置。

### gateway.yaml 中的 agents 配置结构

```yaml
agents:
  main:
    # 主 agent（QClaw），已有配置，无需额外操作

  student-assistant:
    # 学生工作助理 Agent
    systemPrompt: |
      你是学生工作助理，专门帮助学生处理日常事务...
    skills:
      - email-skill
      - kdocs
      - calendar
    model:
      default: qclaw/pool-glm-5-turbo
    workspace: ~/.qclaw/workspace  # 可共享或独立

  academic-assistant:
    # 学术研究助手 Agent
    systemPrompt: |
      你是学术研究助手，专门处理文献检索、论文写作...
    skills:
      - academic-research-hub
      - arxiv-scholar-search
      - pdf
    model:
      default: qclaw/pool-glm-5-turbo
```

### 配置步骤

1. **编辑 gateway 配置**：
   ```markdown
   - 用 gateway config.schema.lookup 查询 agents 配置结构
   - 用 gateway config.patch 安全地增量添加新 agent
   ```

2. **重启 gateway**：配置生效后 gateway 会自动重启

3. **验证 agent 可用**：
   ```markdown
   - agents_list() 查看可用 agent id 列表
   - 确认新 agent 出现在列表中
   ```

## 2. ACP 通信流程

### 单次任务（Run Mode）

```markdown
1. 主 Agent 发起：
   sessions_spawn(
     runtime="acp",
     agentId="student-assistant",
     task="帮我检查今天的邮件，标记紧急的",
     mode="run"
   )

2. 目标 Agent 在隔离环境中执行任务

3. 结果返回给主 Agent
```

### 持久会话（Session Mode）

```markdown
1. 创建持久 ACP 会话：
   sessions_spawn(
     runtime="acp",
     agentId="student-assistant",
     task="开始协助处理学生事务，等待指令",
     mode="session",
     label="student-work"
   )

2. 后续交互：
   sessions_send(
     sessionKey="<session-key>",
     message="帮我整理本周的学生会议纪要"
   )

3. 会话保持上下文，无需重复初始化
```

### 恢复已有会话

```markdown
sessions_spawn(
  runtime="acp",
  resumeSessionId="<session-uuid>"  # 从 ~/.codex/sessions/ 获取
)
```

## 3. 跨 Agent 信息传递模式

### 请求-响应模式

```
Agent A ──[sessions_spawn/acp]──► Agent B
Agent A ◄──[result]────────────── Agent B
```

### 委托-回调模式

```
Agent A ──[sessions_spawn]──► Agent B (子任务)
Agent B ──[sessions_send]──► Agent C (进一步委托)
Agent C ◄──[result]────────── Agent B
Agent B ◄──[result]────────── Agent A
```

### 事件通知模式

```
Agent A (后台运行) ──[sessions_send]──► Agent B (主 Agent)
                     "检测到新邮件，需处理"
```

## 4. Skills 共享策略

### 公共 Skills 库（推荐）

所有 Agent 共用 `~/.agents/skills/` 目录：

```
~/.agents/skills/
├── multi-agent-comm/      ← 本 skill
├── superpowers-repo/      ← obra/superpowers
├── academic-research-hub/ ← 学术研究
├── email-skill/           ← 邮件
└── ...                    ← 其他公共 skills

# 各 Agent 通过 junction 链接访问
~/.claude/skills/ → junctions to ~/.agents/skills/
~/.qclaw/skills/  → junctions to ~/.agents/skills/
```

### Agent 专属 Skills

某些 skill 只需特定 Agent 使用，放在该 Agent 的独立 workspace 下。

## 5. 跨设备复用清单

将 skill 和配置迁移到新设备的步骤：

1. **Skills 迁移**：复制 `~/.agents/skills/multi-agent-comm/` 到新设备，建立 junction
2. **Agent 定义**：在新设备的 gateway config 中定义相同的 agent 配置
3. **环境变量**：确保新设备设置了必要的 API key 和代理
4. **验证通信**：在新设备上执行 `agents_list()` 和一个简单的 `sessions_spawn` 测试

### 迁移脚本示例

```powershell
# 在新设备上执行
$src = "$env:USERPROFILE\.agents\skills\multi-agent-comm"
$dest = "$env:USERPROFILE\.qclaw\skills\multi-agent-comm"
if (-not (Test-Path $dest)) {
    cmd /c "mklink /J `"$dest`" `"$src`""
}
```
