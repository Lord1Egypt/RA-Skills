# OpenClaw 多 Agent 编排方法论

> 本 skill 定义了 OpenClaw 多 Agent 团队的编排方法论：两种协作模式的本质区别、如何共存、配置落点、排障指南。主 Agent 在需要搭建或调整团队协作时加载此 skill。

---

## 一、两种协作模式

OpenClaw 多 Agent 协作有两条独立链路。理解它们的区别是搭建团队的前提。

### 模式 A：后台调度（Backend Spawn）—— 主链路

主 Agent 通过 `sessions_spawn` 在后台拉起子 Agent。用户只和主 Agent 对话。

```
用户 → 主Agent → sessions_spawn(agentId, task) → 专业Agent → 结果回传 → 主Agent汇总输出
```

调用示例：

```js
sessions_spawn({
  agentId: "finance",
  task: "分析这份财报，给出结论、依据和风险提示",
  mode: "run",
  runtime: "subagent"
})
```

特征：
- 子任务后台完成，用户不可见
- 主 Agent 统一汇总、统一对外
- 不依赖任何 Discord 配置
- 适合研究、分析、复核、技术执行等编排型工作

### 模式 B：Discord @Mention —— 外显层

Agent 作为独立 Discord Bot 出现，用户或其他 Bot 通过 `@` 直接触发。

```
Discord用户 → @某Bot → Discord Account → Gateway Binding → 对应Agent → 回复用户
```

特征：
- Agent 以独立身份在频道发言
- 需要额外维护 Discord token、binding、频道权限
- 适合公开协作、角色人格化、分频道值守

### 模式 C：Bot-Bot @Mention —— 增强层（第三优先级）

Bot 之间在 Discord 里互相 `@`。**非主流程，仅在明确需要公开协作时启用。**

要求 `allowBots: true` 且 bot ID 进入白名单。核心调度仍应走 spawn。

---

## 二、两种模式的本质区别

| 维度 | Backend Spawn | Discord @Mention |
|------|--------------|-----------------|
| **本质** | 主Agent的内部编排能力 | 外部渠道的接入入口 |
| **触发方式** | 主Agent代码调用 `sessions_spawn` | 用户在Discord频道 `@` Bot |
| **用户感知** | 只看到主Agent的汇总输出 | 看到独立Bot在频道发言 |
| **配置依赖** | `agents.list` + `subagents.allowAgents` | 额外需要 token + accounts + bindings |
| **是否必须** | **是（核心链路）** | 否（可选增强） |
| **Agent间协作** | 主Agent内部路由，用户无感 | Bot之间公开@，用户可见 |
| **适合场景** | 内部编排、复杂任务链、统一输出 | 角色外显、分频道值守、公开协作 |

---

## 三、两种模式如何同时运行

**核心机制：同一个 Agent 可以同时被两种方式触发。**

```
配置层面：
  agents.list 注册 Agent 身份    → spawn 链路使用
  discord accounts + bindings   → @mention 链路使用
  两套配置独立，互不冲突

运行层面：
  主Agent后台 spawn finance     → finance 在后台处理并返回结果
  用户在Discord @finance Bot   → finance 在频道直接回复
  两条链路并行，互不干扰
```

### 共存配置示例

一个 Agent 同时支持两种模式，需要两块配置：

**1) `agents.list` 中注册（spawn 用）：**

```json
{
  "id": "finance",
  "name": "财务分析师",
  "workspace": "/Users/{USER}/.openclaw/workspace-finance",
  "identity": { "name": "财务分析师", "emoji": "📊" },
  "model": "kimi-coding/k2p5",
  "subagents": { "allowAgents": ["*"] }
}
```

**2) Discord accounts + bindings 中配置（@mention 用）：**

```json
// accounts 部分
"finance": {
  "name": "财务分析师",
  "token": "BOT_TOKEN",
  "groupPolicy": "allowlist",
  "guilds": { "GUILD_ID": {} }
}

// bindings 部分
{
  "agentId": "finance",
  "match": { "channel": "discord", "accountId": "finance" }
}
```

**只要 spawn 不要 Discord？** 只配 `agents.list`，不配 accounts/bindings。
**只要 Discord 不要 spawn？** 不推荐，但技术上可以只配 Discord 侧。
**两个都要？** 两块都配，各自生效。

---

## 四、三种部署模式选择

### 模式 A：后台编排优先（推荐默认）

- 用户只找 main
- main 后台 spawn 专业 Agent
- Discord 只保留 main + rescue
- **最干净、最少运维、最适合复杂任务**

### 模式 B：后台编排 + Discord 外显并存

- main 负责后台调度
- 部分专业 Agent 也在 Discord 外显
- 用户既可以找 main，也可以在特定频道直连角色
- 代价：更多 token / binding / 权限维护

### 模式 C：全 Discord 可见协作

- 大量 Bot 在 Discord 互相可见协作
- 需要 `allowBots: true` + bot ID 白名单
- 仅在需要「公开表演式协作」时启用
- 核心调度仍建议走 spawn

---

## 五、Agent vs Skill 判断

| 需求 | 用 Agent | 用 Skill |
|------|---------|---------|
| 独立 workspace / session / 记忆 | Yes | |
| 需要被主Agent后台 spawn | Yes | |
| 需要在Discord作为独立Bot | Yes | |
| 只是临时换个专业视角 | | Yes |
| 只是输出格式变化 | | Yes |
| 不想增加运维成本 | | Yes |

**判断标准：** 独立身份/记忆/调度 → Agent；专业视角/格式转换 → Skill。

---

## 六、推荐架构分层

```
主控层  → main（任务理解、拆解、调度、汇总、对外输出）
专业层  → finance / compliance / news / ...（接收后台子任务）
技术层  → product-manager / frontend / backend / qa（产品研发落地）
接入层  → Discord accounts / bindings / channel rules（外部入口）
工具层  → skills（knowledge-organizer / coding-agent / ppt-writer）
```

每个角色必须定义三件事：
1. **职责** —— 它负责什么
2. **边界** —— 它不负责什么，什么时候交给别人
3. **协作关系** —— 它什么时候该找谁复核、补充、执行

---

## 七、配置落点总览

### 文件结构

```
~/.openclaw/
├── openclaw.json                # 主Gateway配置（agents/discord/bindings）
├── openclaw-rescue.json         # Rescue Gateway独立配置
├── workspace/                   # 主Agent workspace
│   ├── SOUL.md                  # 角色定位、职责、边界
│   ├── IDENTITY.md              # 身份显示
│   ├── HEARTBEAT.md             # 定时/心跳
│   ├── TEAM.md                  # 团队花名册
│   └── skills/                  # Skills目录
└── workspace-{agent-id}/        # 各专业Agent workspace
    ├── SOUL.md
    ├── IDENTITY.md
    └── HEARTBEAT.md
```

### 改完是否需要重启

| 改了什么 | 是否重启 Gateway |
|---------|----------------|
| `openclaw.json` | 必须重启 |
| `openclaw-rescue.json` | 必须重启 rescue |
| `SOUL.md` / `IDENTITY.md` | 新 session 生效，必要时重启 |
| `TEAM.md` | 不需要 |
| `skills/` 下的 SKILL.md | 新调用生效 |

---

## 八、完整搭建流程

### Step 1：创建 Agent Workspace

```bash
mkdir -p ~/.openclaw/workspace-{agent-id}
```

**SOUL.md 四段式模板：**

```markdown
## 你是谁
一句话定义角色定位。

## 职责
- 负责什么、产出什么、工作范围

## 做事风格
- 如何分析问题、如何组织回答、输出格式要求

## 边界
- 不做什么、什么时候转交给其他角色、协作关系
```

**IDENTITY.md 示例：**

```markdown
- **Name:** 角色名称
- **Creature:** AI XXX专家
- **Vibe:** 严谨 / 保守 / 数据导向
- **Emoji:** 🎯
```

### Step 2：在 `openclaw.json` 注册 Agent

```json
{
  "agents": {
    "defaults": {
      "workspace": "/Users/{USER}/.openclaw/workspace"
    },
    "list": [
      {
        "id": "main",
        "default": true,
        "name": "主Agent",
        "workspace": "/Users/{USER}/.openclaw/workspace",
        "identity": { "name": "OpenClaw", "emoji": "🦞" },
        "model": "anthropic/claude-opus-4-6"
      },
      {
        "id": "your-agent-id",
        "name": "角色名称",
        "workspace": "/Users/{USER}/.openclaw/workspace-your-agent-id",
        "identity": { "name": "角色名称", "emoji": "🎯" },
        "model": "kimi-coding/k2p5",
        "subagents": { "allowAgents": ["*"] }
      }
    ]
  }
}
```

**关键：** `main` 必须显式存在、`"default": true`、放 list 第一位。

### Step 3：重启 Gateway

```bash
openclaw gateway restart
```

### Step 4：验证后台 Spawn

```js
sessions_spawn({
  agentId: "your-agent-id",
  task: "做一个最小测试回复",
  mode: "run",
  runtime: "subagent"
})
```

验证顺序：最小任务能拉起 → 输出符合 SOUL.md → 接入真实工作流。

**到此后台调度链路已打通。以下为可选的 Discord 外显配置。**

### Step 5（可选）：暴露为 Discord Bot

**5a. 创建 Discord Bot：**
- Discord Developer Portal 创建 Application → 获取 Token → 邀请到服务器
- 注意：连续创建多个 Bot 会被限流，建议分批

**5b. 配置 Discord accounts：**

```json
"channels": {
  "discord": {
    "enabled": true,
    "groupPolicy": "allowlist",
    "allowBots": true,
    "allowFrom": ["USER_ID"],
    "guilds": {
      "GUILD_ID": { "requireMention": true, "users": ["USER_ID"] }
    },
    "accounts": {
      "your-agent-id": {
        "name": "角色名称",
        "token": "BOT_TOKEN",
        "groupPolicy": "allowlist",
        "guilds": { "GUILD_ID": {} }
      }
    }
  }
}
```

**5c. 配置 binding：**

```json
"bindings": [{
  "agentId": "your-agent-id",
  "match": { "channel": "discord", "accountId": "your-agent-id" }
}]
```

**5d. 重启 Gateway 并在 Discord 验证。**

---

## 九、Discord `requireMention` 三层覆盖

覆盖优先级：**channel > account > top-level**

| 层级 | 配置位置 | 效果 |
|------|---------|------|
| top-level | `channels.discord.guilds.GUILD_ID` | 全局默认 |
| per-account | `accounts.{id}.guilds.GUILD_ID` | 覆盖该Bot的默认行为 |
| per-channel | `accounts.{id}.guilds.GUILD_ID.channels.CH_ID` | 覆盖该Bot在特定频道的行为 |

**最佳实践：**
- 顶层 `requireMention: true`（默认需要@）
- main / rescue 的 account 设 `false`（随时待命）
- 其他 Agent 用空对象 `{}` 继承顶层 `true`
- 特定频道用 `channels` 单独覆盖

---

## 十、模型选择

| 角色 | 推荐模型 | 理由 |
|------|---------|------|
| 主 Agent (main) | `anthropic/claude-opus-4-6` | 最强推理，负责编排 |
| 专业 Agent | `kimi-coding/k2p5` | 成本优化，262K上下文 |
| Rescue Agent | `kimi-coding/k2p5` | 独立配置文件管理 |

Rescue 的模型在 `~/.openclaw/openclaw-rescue.json` 中单独配置：

```json
{
  "agents": {
    "defaults": {
      "model": {
        "primary": "kimi-coding/k2p5",
        "fallbacks": ["anthropic/claude-opus-4-6", "anthropic/claude-sonnet-4-5"]
      }
    }
  }
}
```

---

## 十一、故障排查

| 问题 | 原因 | 解决 |
|------|------|------|
| 主Agent身份被覆盖 | `main` 没显式配置或没设 `default: true` | main 放 list 第一位，设 `"default": true` |
| spawn 调不到成员 | Gateway 没加载新配置 | `openclaw gateway restart` |
| `requireMention` 行为不符预期 | 三层覆盖冲突 | 检查 channel > account > top-level 优先级 |
| Bot A @ Bot B 无响应 | `allowBots` 非 true 或 bot ID 不在白名单 | 设 `allowBots: true`，bot ID 加入 `allowFrom` 和 `users` |
| Discord Bot 创建限流 | 连续创建太多 | 分批创建，先验证 spawn 再补 Discord |
| Rescue 模型不对 | 改错了配置文件 | 修改 `openclaw-rescue.json`（非主配置） |
| 配了但不生效 | 没重启 Gateway | 所有 `openclaw.json` 改动后 `openclaw gateway restart` |

---

## 十二、核心原则总结

1. **后台 spawn 是主链路，Discord @mention 是外显层** —— 先打通 spawn，再按需加 Discord
2. **同一 Agent 两种模式可并行** —— `agents.list` 管 spawn，`accounts + bindings` 管 Discord，互不冲突
3. **bot-bot @ 是增强不是主流程** —— 核心调度走 spawn，公开协作才用 bot-bot @
4. **改配置必须重启 Gateway** —— 最常见的「不生效」原因
5. **每个角色定义职责、边界、协作关系** —— 没有清晰边界的 Agent 不如不建
