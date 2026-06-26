# OpenClaw + Feishu 多 Agent 参考方案

## 适用范围

本参考方案适用于两类用户：

1. **已配置多 agent**
   - 已有多个 agent
   - 已有多个 Feishu bot / app
   - 但路由、`@`、群回投、agent 串联讨论不稳定

2. **未配置多 agent**
   - 想从零搭建一套 OpenClaw + Feishu 多 agent 协作系统
   - 希望角色、人设、职责可以完全自定义

## 一句话架构

**飞书负责“显示 @”，OpenClaw 负责“真实投递”。**

链路如下：

1. 飞书群消息进入协调者 agent
2. 协调者决定谁参与
3. 协调者在群里发 `<at>`
4. 协调者对每个目标发一次 `sessions_send`
5. 目标 agent 被唤醒后，用自己的 `message` 工具直接回同一个飞书群
6. 如需继续拉人，重复 3-5

## 先收集的信息

至少收集这一张表：

| 字段 | 说明 |
|---|---|
| `agentId` | OpenClaw 内部 agent 标识 |
| `roleName` | 角色名，可自定义 |
| `accountId` | Feishu 账号绑定名 |
| `appId` / `appSecret` | 可选；如果希望直接产出或应用账号配置，建议一并提供 |
| `openId` | 飞书 bot 的 open_id，用于 `<at>` |
| `workspace` | 该 agent 的 workspace，可选 |
| `agentDir` | 该 agent 的工作目录，可选 |
| `responsibility` | 它负责什么 |
| `triggerTerms` | 用户在群里常用哪些称呼触发它 |
| `isCoordinator` | 是否是默认总调度 |

如果用户还没定义角色，就先让用户确认这张表。

## 已配置多 agent 的实施流程

### 第 1 步：检查 `openclaw.json`

重点看：

- `agents.list`
- `bindings`
- `tools.agentToAgent.enabled`
- `tools.agentToAgent.allow`
- `channels.feishu.accounts`

目标是：

- 每个 Feishu bot 都有单独 `accountId`
- 每个 `accountId` 都绑定到一个明确的 `agentId`
- 所有需要互相协作的 agent 都在 `tools.agentToAgent.allow`

### 第 2 步：统一协议文件

在 `~/.openclaw/PROTOCOL.md` 中写清楚：

- `<at>` 只是视觉层
- `sessions_send` 才是真实投递
- 每次委派必须同时做这两步
- 收到 `sessions_send` 后，不回发起者，直接回群
- 如需继续拉人，重复“可视化 @ + 内部投递”

### 第 3 步：修协调者 agent

协调者 agent 的 `IDENTITY.md` 应明确：

- 它是默认总调度
- 新问题先判断“谁主答 / 是否需要多人讨论”
- 广义团队召集时，要覆盖完整团队，而不是默认漏掉某个角色
- 不要把裸文本 `@角色` 当成真实通知机制

### 第 4 步：修专业 agent

专业 agent 的 `IDENTITY.md` 应明确：

- 收到 `sessions_send` 后直接回飞书群
- 如果需要其他 agent 参与，也必须继续执行：
  - 群里 `<at>`
  - 再发 `sessions_send`

### 第 5 步：检查会话存储

如果某个 agent “像是收到了，但不回群”，检查对应 session store。

重点看目标群 session 是否还是：

```json
{
  "channel": "feishu",
  "chatType": "group",
  "deliveryContext": {
    "channel": "feishu",
    "to": "chat:oc_xxx",
    "accountId": "target-account"
  },
  "lastChannel": "feishu",
  "lastTo": "chat:oc_xxx",
  "lastAccountId": "target-account"
}
```

如果它被写成了：

- `channel = webchat`
- 没有 `deliveryContext.to`
- 没有 `accountId`

那它很可能无法正确把消息回投到飞书群。

### 第 6 步：重启 gateway

修改协议、身份文件、配置或 session store 后，都要重启 OpenClaw gateway。

### 第 7 步：真实验证

建议用这类测试话术：

```text
@协调者 让其他人一起讨论一下这个问题，分别从各自角度给我判断。
```

预期结果：

1. 协调者先发总调度消息
2. 协调者显式 `<at>` 所有应该参与的角色
3. 每个目标 agent 分别独立回群
4. 某个 agent 如继续拉人，会再次出现新的 `<at>` 和后续回复

## 未配置多 agent 的实施流程

### 第 1 步：先定义角色表

不要一上来先写文件。先确认角色结构，例如：

- 一个协调者
- 两到五个专业 agent

角色可以是：

- 产品 / 设计 / 开发 / 运营
- 法务 / 财务 / HR
- 研究 / 内容 / 销售 / 交付
- 或任何用户自定义角色

### 第 2 步：在 `openclaw.json` 建立 agent 与 Feishu 绑定

至少需要：

- `agents.list`
- `channels.feishu.accounts`
- `bindings`
- `tools.agentToAgent.allow`

### 第 3 步：为每个 agent 写身份文件

每个 agent 至少需要：

- `IDENTITY.md`
- `SOUL.md`

其中：

- 协调者强调“路由、召集、收束”
- 专业角色强调“收到任务后直接回群”

### 第 4 步：建立统一协议

把共通的飞书协作协议放在：

- `~/.openclaw/PROTOCOL.md`

这样每个 agent 都读同一份规则，避免不同 agent 使用不同委派方式。

### 第 5 步：测试最小链路

先测一跳：

- 协调者 -> 专业角色

再测两跳：

- 协调者 -> 角色 A -> 角色 B

不要一开始就测复杂多跳。

## 最容易踩坑的点

### 1. 裸文本 `@角色`

问题：

- 群里看起来像点名了
- 但 bot 不会因此被另一个 bot 唤醒

正确做法：

- `<at>` + `sessions_send`

### 2. `sessions_send` 参数错了

错误：

- 传 `agentId`

正确：

- 传 `sessionKey`

### 3. 角色规则写死成特定人设

错误：

- 方案只能用于 Steve / Jony / Brendan / Seth

正确：

- 抽象为协调者与专业角色
- 名字、人设、职责、触发词全都可替换

### 4. 协调者默认漏人

问题：

- 用户说“大家一起讨论”
- 协调者只叫两个角色

正确：

- 对“其他人 / 大家 / 团队”设置默认完整召集规则

### 5. 群 session 被写坏

问题：

- `sessions_send` 超时
- 或者 agent 看起来收到了，但没回群

重点排查：

- 会话 `channel`
- `deliveryContext`
- `chatType`
- `accountId`

## 故障排查顺序

### 情况 A：没看到显式 @

排查：

1. 协调者提示词
2. 协议文件
3. 是否真的发了 `message`

### 情况 B：看到了 @，但目标 agent 没回

排查：

1. 是否有对应 `sessions_send`
2. `sessions_send` 返回值
3. 目标 agent session 是否生成
4. 目标 session 是否保持 `feishu group`

### 情况 C：`sessions_send` 超时

排查：

1. 目标 agent 是否正在长时间读文档 / 跑工具
2. 日志中是否出现 nested run timeout
3. 目标 session metadata 是否损坏

## 推荐交付物

如果要把这套方案做成可复用包，建议至少包含：

1. 主 `SKILL.md`
2. 通用参考文档
3. 通用模板
4. 一组测试话术
5. 一组可执行脚本

## 推荐脚本分工

### `scripts/manage_feishu_multi_agent.py`

统一入口。

支持：

- `render`
- `audit`
- `repair`
- `apply`
- `bootstrap`

其中 `bootstrap` 适合从角色表快速走完整条链路：

1. 生成产物
2. dry-run 或写入 `~/.openclaw/`
3. 再跑一次审计

### `scripts/apply_feishu_multi_agent.py`

半自动落地脚本。

特点：

- 默认 dry-run，不会直接改用户环境
- 加 `--write` 后才真正写入
- 加 `--backup` 会先备份旧文件
- 加 `--apply-identities` 会把生成的身份规则写到各自 `agentDir`

适合：

- 已有多 agent，但想快速批量对齐配置
- 刚定义完角色表，想先半自动落地再人工微调

### `scripts/render_feishu_multi_agent.py`

输入角色表，输出：

- `PROTOCOL.generated.md`
- `openclaw.generated.json`
- `identities/*.IDENTITY.generated.md`

适合“还没配置多 agent”的用户。

### `scripts/audit_feishu_multi_agent.py`

把角色表与现有 `openclaw.json` 对照，快速发现：

- 缺失 agent
- 缺失 Feishu account
- 缺失 binding
- 缺失 allowlist
- `tools.sessions.visibility` 不正确

适合“已经配置，但不确定哪里不一致”的用户。

### `scripts/repair_feishu_group_sessions.py`

扫描或修复某个 Feishu 群对应的 agent session metadata。

重点处理：

- `channel` 被写成 `webchat`
- `deliveryContext` 丢失
- `lastTo` / `lastAccountId` 丢失

适合“agent 似乎收到任务，但没有回群”的用户。

## 一句话原则

**OpenClaw 多 agent 对接飞书时，不要把“飞书 bot 互相 @”当成真实通信机制；真实通信必须落在 OpenClaw 的 `sessions_send` 上。**
