---
name: paseo-manager
description: 在独立的 Paseo Manager 入口项目中接收需求，动态找到对应 workspace，复用合适的 agent 或通过 paseo-handoff 新建 agent 并交接。用于“找对应项目处理”“交给之前的 agent”或入口项目的默认需求分流；不是在所有业务仓库中强制转派的通用规则。
---

# Paseo Manager

把当前目录当作**需求入口，不是业务代码仓库**。默认先定位目标，再用 [[paseo-handoff]] 交接；不要为了省事直接在入口实现其他项目的需求。明确属于入口自身的维护可以就地处理。

## 前置能力与边界

- 先读取 [[paseo]] 和 [[paseo-handoff]]。它们由 Paseo 环境提供，本 skill 不复制或安装它们；缺失时说明缺少哪项，不声称已执行 handoff。
- 优先使用 Paseo MCP；没有这些工具时，读 [references/cli.md](references/cli.md) 使用 CLI。不要用当前模型的临时子代理代替 Paseo agent：后者才有持久的 workspace 归属。
- 用户指定的项目、host、workspace、agent、profile 和工作范围优先。不要把“调查”升级为修改、把“修复”升级为发布，也不要替用户扩大权限。
- 不固化本机路径、workspace ID、agent ID 或模型名称。每次任务从 Paseo 当前状态发现；历史路由仅作线索。

## 1. 找到目标 workspace

1. 提取需求中的项目/仓库、功能模块、分支/PR、环境和“继续之前任务”等线索；保留用户原始意图。
2. 调用 `list_hosts`，再查询相关 host 的 `list_workspaces`。未指定 host 时先查本机；本机没有明确匹配再查可达的已注册 host。远端的 `serverId`、`workspaceId`、路径必须来自同一 host。
3. 根据以下证据筛选，而不是把整份 workspace 列表甩给用户：
   - 用户明确指定的 ID/仓库路径；
   - workspace 的项目、名称、路径、worktree/分支与任务是否相符；
   - 候选 workspace 中 agent 的任务标题与近期活动；
   - 仍有必要时，只读查看候选目录的 `AGENTS.md`、README、git remote/branch，确认职责。
4. **同一 `cwd` 可能有多个 workspace**，不能按路径合并，也不能取列表第一项。`list_agents` 的 `cwd` 过滤只缩小范围，仍需用返回的 workspace 归属区分。拿不到归属就继续查详情，不猜测。
5. 默认忽略 archived/background；用户点名历史任务，或普通列表无匹配时，才扩展查询 background/archived 线索。不要自动恢复、归档、删除或改名已有 workspace/agent。

明确匹配就行动；两个候选会导致实质不同的工作时，简短说明差异，只问一个消歧问题。不要因同一项目存在多个 workspace 就一律要求用户自己找。

## 2. 复用 agent，还是新建

在选定 workspace 查询 `list_agents`，对少量相关候选用 `get_agent_status` / `get_agent_activity` 核实：

| 情况 | 动作 |
|---|---|
| 用户指定某个 agent | 核实 host、workspace 与状态后使用；不匹配或不可用先说明 |
| 同一任务的续接，已有空闲且上下文相关的 agent | 复用，发送完整的增量交接，不另开重复任务 |
| 原 agent 正在处理同一任务，用户补充要求 | `send_agent_prompt` 显式 `activeTurnBehavior: "steer"`；注意 provider 不支持 steer 时可能退化为 interrupt，有不能中断的工作则先澄清 |
| agent 忙于无关任务，或在等待权限/用户决定 | 不抢占、不自动审批；选择其他合适的空闲 agent 或新建 |
| 没有合适的 agent，但有明确目标 workspace | 按 [[paseo-handoff]] 在**该 workspace** 新建 |

复用是本 skill 对 handoff 的扩展：保留 [[paseo-handoff]] 的上下文交接方式，用 `send_agent_prompt` 而不是机械地 `create_agent`。发送前再次核实状态；不默认更改已有 agent 的 provider、模型或模式。用户明确指定 profile 而现有 agent 不匹配时，优先新建，不悄悄重配它。

新建前按 [[paseo]] 调用 `list_profiles`，阅读所有 profile 的 `notes`，优先用户点名或职责最匹配者，并把字段展开为 `create_agent` 参数。没有适合 profile 时明确说明，再用 provider discovery，不能猜模型 ID。传入已选 `workspaceId`；跨 host 同时传正确 `serverId`，**不能省略 workspaceId 后意外落在 Manager**。标题用 `[Handoff] <简短任务>`。

除非用户要求隔离，优先已有 workspace；需要新 worktree 时沿用 [[paseo-handoff]] 的 isolation 流程。多个 agent 共享一个本地目录不等于文件隔离；发现会与进行中的修改冲突时，先澄清隔离方式。

## 3. 交接内容

无论复用还是新建，接收者都不应靠猜测理解任务。沿用 [[paseo-handoff]] 的 briefing，至少包括：

```text
## Task
用户原始需求；要执行什么，以及只调查/允许修改/允许提交发布的边界。

## Destination
目标 host、workspace ID、目录；为什么选这里。

## Context / Current state
已确认的事实、相关文件、已完成和未完成的部分。
若没有调查过，明确写尚未调查，不编造结论。

## Decisions / What was tried
需要保留的决定、尝试及其结果；没有则省略。

## Acceptance criteria
可以核验的交付物或完成条件。

## Constraints
用户限制；不要覆盖其他人的未提交修改；在目标目录读取适用的 AGENTS.md。
这是已完成路由的执行任务，直接在目标 workspace 执行，不再转回 Manager。
```

仅传任务相关信息；不要复制整个会话、无关 workspace 列表或密钥。需要凭据时说明目标环境的获取方式，不内嵌 token。不要把 slash 字符串 `/paseo-handoff` 当成已经调用工具的证据。

## 4. 交接回执，然后结束本轮

- 从创建/发送的真实回执记录 `{serverId, workspaceId, agentId}`。只对一次请求派发一次；发送超时等结果不明时先查目标状态/活动确认，不能盲目重发或重复创建。
- 简短回复：**目标项目/workspace、选择理由、复用或新建、agent ID、已交接内容**。工具返回可用链接时可以附上，不拼凑未经验证的链接。
- 区分“已排队/已交接”和“工作已完成”。默认保留 `notifyOnFinish: true`，结束本轮等通知，不轮询、不等待业务任务完成。
- 新建 agent 仍可能在当前 agent 的 subagent track 中，同时出现在目标 workspace。需要独立时由用户在界面 detach；不要调用 CLI/wire detach，也不要通过清除调用者身份绕过亲子关系。
- 用户之后追问同一任务时，重新核实上次目标并续接，不另开重复 agent。

## 没有合适目标时

“没有适合的 agent”不是回退条件——有 workspace 就在其中新建。

- **确实没有合适 workspace**：说明查了哪些范围。纯咨询、无归属的一次性小任务可以在入口处理；需要新业务项目/仓库时先确认名称与位置，不能把入口变成杂物仓库。用户已明确给出新项目和位置时可据此创建。
- **已有明确仓库但未登记**：确认目录存在且职责匹配后，可为它创建 local workspace 再交接；路径未知时询问，不扫描整块磁盘。
- **Paseo 连接失败、权限不足、相关 host 离线或查询不完整**：属于发现失败，不等于没有匹配。说明限制，不能据此自行在入口实现本应交接的任务。
- **入口自身的规则、安装配置或文档维护**：在入口处理，不把自己交接给自己形成循环。
