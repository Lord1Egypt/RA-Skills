---
name: gitea-workflow
description: "Gitea 多角色协作工作流 (issue + pr 驱动)。2 类角色:实现者(推进分配 issue + 完成后 @协调者) + 协调者(统筹所有 issue + 审阅评论 + 按计划推进阶段)。本技能只描述角色工作流,不教 Gitea API,适用于任何 Gitea 工作室(游戏/文档/开发)。"
metadata: {"openclaw":{"emoji":"🎯","requires":{"anyBins":[]}}}
---

# Gitea 协作工作流

> 本技能定义**多角色 agent + Gitea Issue** 的协作模式。**不**讲解 Gitea API 用法(假定所有 agent 已具备),只描述**角色分工 + 循环节奏 + 通讯约定 + Loop 启停**。
>
> 适用范围:任何多角色 Gitea 工作室(游戏开发、文档协作、产品研发等)。

## 适用场景

- 项目需求/功能**通过 Gitea Issue 推进**,信息流集中在 issue 评论里
- 实现者按分配推进,不需要持续盯群
- 协调者(制作人/team lead)是总协调,只在阶段切换或异常时介入
- 群里消息**大幅减少**,只保留关键通知

## 角色抽象

任何工作室都可以套这个模式。游戏工作室示例供参考:

| 抽象角色 | 游戏工作室示例 | 通用职责 |
|----------|----------------|----------|
| **Implementer (实现者)** | programmer / designer / tester / artist | 推进分配到的 issue |
| **Coordinator (协调者)** | producer (制作人 / team lead) | 统筹 + 审阅 + 阶段推进 |

> 其他示例:
> - 文档协作:Implementer = 各专题作者;Coordinator = 主编
> - 产品研发:Implementer = 工程师;Coordinator = PM
> - 设计团队:Implementer = 设计师;Coordinator = 设计总监

---

## Implementer 循环 (programmer/designer/tester/artist 类)

每次被 cron 唤醒(默认 15-30 分钟一次)执行:

### 步骤 1: 拉取分配给我的 issue

用 Gitea API 查自己仓库的 open issue 列表:

- **首选**:`/api/v1/repos/{owner}/{repo}/issues?state=open&assignee={my-username}`
- 备选:`/api/v1/repos/{owner}/{repo}/issues?state=open` + 自行 grep 标题/正文里 `@my-username`

### 步骤 2: 分类每个 issue

| 状态 | 判断依据 | 处理 |
|------|----------|------|
| **未开始** | 无进度评论 | 推进:实现/写文档/画图等 |
| **进行中** | 有进度评论,未 close | 继续推进(可加评论更新状态) |
| **阻塞** | 评论或 label 显示 blocked | 在 issue 评论说明阻塞原因,**@coordinator 求助**(群里也 @ 一次) |
| **已完成** | 我刚 close 了 | 见步骤 3 |
| **不是我的** | assignee 不我 | 跳过 |

### 步骤 3: 完成通知(只在刚 close issue 时)

- 在 issue 评论加简短的 close summary(可选)
- **群里发一条**:`<issue-link> 已完成,@<coordinator-name>`

### 步骤 4: 退出

不发任何"还在工作"之类的中间消息。

---

## Coordinator 循环 (producer / team lead 类)

每次被 cron 唤醒(默认 30-60 分钟一次)执行:

### 步骤 1: 拉取所有 issue + 审阅新评论

```text
组织/项目名下所有仓库,open issues 列表 + 关闭时间在 [上次唤醒, 现在] 的 issues
按 repo 分组,按状态分组(未开始/进行中/阻塞/已完成)
```

### 步骤 2: 审阅通知

| 来源 | 处理 |
|------|------|
| 我被 @ 的 issue 评论 | **立即回复**(在 issue 里,不在群里) |
| 实现者发的"完成通知"群里消息 | 在 issue 上确认(close 或 reopen),群里简短回 `✅` |
| 阻塞通知 | 评估:开新 issue 协调/找人/换方案 |
| 纯讨论(无 @) | 不看,避免噪音 |

### 步骤 3: 判断项目阶段

| 情况 | 处理 |
|------|------|
| 当前阶段所有 issue 已 close | **创建下一阶段 issue**(P{N+1})+ 在群里发阶段转换通知 |
| 有未 close 但无阻塞的 issue | 催最关键的(评论 + 群里 @ 该 agent) |
| 有阻塞 issue | 评估是否能协调;不能就升级到 @老板 |
| 都没事做 | 不发任何消息,继续睡 |

### 步骤 4: 退出

只在**阶段切换**或**异常升级**时发群里消息。

---

## 通讯约定

### Implementer → 群里

| 何时 | 内容模板 |
|------|----------|
| issue 完成时(close 后) | `<issue-link> 已完成,@<coordinator-name>` |
| 阻塞需要协调时 | `<issue-link> 阻塞:[原因],@<coordinator-name>` |

### Coordinator → 群里

| 何时 | 内容模板 |
|------|----------|
| 阶段切换 | `P{N} 完成,进入 P{N+1}` + 列新 issue 链接 |
| 严重阻塞需 @老板 | `P{N} 卡住:[原因],@<老板-name>` |

### 不发群

- ❌ Implementer 日常 git commit / push 通知(走 PR / issue comment)
- ❌ Implementer "还在工作"中间消息(沉默)
- ❌ Coordinator 重复"在监督"无内容消息
- ❌ cron 心跳触发本身的通知
- ❌ token、密码、内部 IP、deployment 内部细节

---

## Loop 启停

每个 agent 用 `scripts/` 下的脚本控制自己的循环:

```bash
# 启用循环
gitea-workflow loop-on

# 停用循环(暂停 cron)
gitea-workflow loop-off

# 查看状态(当前 cron 状态 + 上次唤醒时间 + 当前 issue 计数)
gitea-workflow status
```

> 脚本具体配置(Gitea token、agent ID、cron name)由**各 agent 自己**配置(在 `references/cron-setup.md`)。
> 本技能只约定**使用方式**,不写死任何 agent 标识符。

---

## Loop 机制选择

**推荐 cron**(已采用):

| 角色 | 周期 | 原因 |
|------|------|------|
| Implementer | 15-30 分钟 | 检查 issue 不频繁,频率过高浪费 token |
| Coordinator | 30-60 分钟 | 审阅评论、推进项目,容许更长间隔 |

**为什么不选 goal/plan**:

- 多 agent 在不同 workspace,单 goal 难协调
- plan 适合单人长任务,不适合"持续监控+按需响应"
- cron 更适合"无人值守、定期唤醒"

**heartbeat 可作为 cron 补充**(更轻量),但**不要替代**:

- 适合"立刻响应"场景(如 coordinator 收到 @ 后立即检查)
- 周期可能更短(分钟级)

**实际使用会找最合适的**:本技能以 cron 为默认实现,各 agent 可根据实际负载调整。

---

## 异常处理

| 异常 | 处理 |
|------|------|
| Gitea API 返回 401 (token 失效) | 内部换 token,**不在群里发**(避免噪音 + 安全) |
| Gitea API 返回 5xx | 跳过本次循环,下次再说 |
| issue 卡住 >2 天 | Implementer 自动升级 → 群里 @coordinator |
| Coordinator 错过循环 >3 次 | 内部状态记一笔,下次唤醒时优先 review |
| Gitea API 返回空数组 `[]` | **不是"0 issue"** — 必须看 HTTP code + JSON `message` 字段 (反幻觉 fail mode) |

---

## 与群的关系

- **群 = 通知渠道**:只发关键节点(完成/阻塞/阶段切换)
- **issue = 工作场所**:所有讨论、决策、状态变化都在 issue / PR 评论里
- **避免在群里讨论 issue 细节**:会污染群 + 不利于跨 session 持久化

这样:

- 信息流集中在 issue,参与者(尤其跨 session 唤醒的 agent)能直接读 issue 拿到完整上下文
- 群消息大幅减少,人(或老板)不被噪音打扰
- agent loop 更简单:只看自己分配的 issue,推进或反馈

---

## 适配新工作室

把这个 skill 用到非游戏工作室:

1. **定义仓库结构**:把 `<your-org>/<your-repo>` 填到 `references/cron-setup.md` 的 cron 配置里
2. **定义角色**:把你的团队成员映射到 Implementer / Coordinator (可以一对多)
3. **配置 cron**:按 `references/cron-setup.md` 创建每个 agent 的循环
4. **初始化 issue**:Coordinator 开 P0 issue(实现者仓库的 5-10 个 starter tasks)
5. **试运行**:观察 1 周,调周期

---

## 不在本技能范围

- ❌ Gitea API 用法(基础 agent 应已具备)
- ❌ Gitea 部署(参考 Gitea 部署文档)
- ❌ Gitea token 生成(各 agent 自行管理)
- ❌ 具体 git push / commit 工作流(各 agent 自行决定)
- ❌ Issue label / milestone 命名规范(各工作室自定)

---

## 相关

- 反幻觉教训(coordinator 自检):参考 LLM 通用 anti-hallucination 经验 — API call 拿空对象前必须看 HTTP code + JSON `message` 字段
- 通用 daily-log / memory-review:`skills/daily-log/` `skills/memory-review/`(通用 OpenClaw 技能,与本 workflow 正交)
