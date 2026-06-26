---
name: hermes-self-audit
description: "定期审计 Hermes Agent 的自改进行为 - skill 变更、curator 状态、记忆库健康度。防止 Agent 在用户不知情的情况下悄悄进化。建议配合 cronjob 每周运行一次。"
version: 1.0.0
category: devops
tags: [hermes, safety, audit, curator, skills, memory]
license: MIT-0
homepage: https://clawhub.ai/freepengyang/hermes-self-audit
issues: https://github.com/freepengyang/hermes-self-audit/issues
created_by: human
inputs:
  - "run via cronjob (no manual trigger needed)"
  - "output: chat platform formatted audit report"
triggers:
  - "manual: hermes self-audit"
  - "auto: cron schedule '0 10 * * 1' (weekly Mon 10:00)"
outputs:
  - 飞书/Discord/群消息格式的审计报告
  - 本地审计日志存到 ~/.hermes/logs/audit.log
---

# Hermes Self-Audit Skill

## 用途

审计 Hermes Agent 的自改进行为，防止它在用户不知情的情况下悄悄创建/修改/归档 skill。定期报告让用户真正掌握 Agent 的学习轨迹。

## 适用人群

- 使用 Hermes Agent 的运维/SRE 工程师
- 关注 AI 自成长行为安全的团队
- 需要定期审计 Agent skill 变更的运维管理者

## 审计维度

### 1. Curator 状态
- curator 是否在运行
- 当前启用的策略（enabled, interval, stale_days 等）
- 最近是否有 skill 被归档

### 2. Skill 变更检测
- 最近创建的 skill（created_by: agent）
- 最近修改的 skill
- 被归档的 skill
- 异常高频修改的 skill（可能存在震荡）

### 3. Skill 使用统计
- use_count 最高的 skill
- 长时间未使用的 skill（可能已过时）

### 4. Memory Provider 健康度
- 当前 memory provider（内置 / honcho / mem0 等）
- honcho 状态（如果启用）：peer 数、session 数
- 是否有异常

### 5. 配置变更检测
- config.yaml 最近的变更（如果可访问）
- memory.provider 是否被意外修改

## 报告格式

```
🛡️ Hermes 自改进审计报告
━━━━━━━━━━━━━━━━━━
📅 审计时间：2026-05-07 10:00
⏰ 上次审计：N 天前

【Curator 状态】
  运行状态：启用 / 暂停
  自动归档：开启 / 关闭
  归档阈值：N 天未使用

【Skill 变更 (近 N 天)】
  🆕 新建：2 个
    - 调研报告模板（2026-05-06）
    - 故障排查清单（2026-05-05）
  ✏️ 修改：1 个
    - react-expert（2026-05-04, 3次调用）
  📦 归档：0 个

【高频使用 Top 5】
  1. react-expert — 23 次
  2. shell-script — 18 次
  3. python-debugpy — 12 次

【长期未使用 (90天+)】
  - finnhub (最后使用: 2026-02-01)
  - listenhub (最后使用: 2026-03-15)

【Memory Provider】
  当前：honcho
  状态：正常
  Peers：2 个

【配置检查】
  memory.provider: honcho ✅ 未变更
  curator.enabled: true ✅

━━━━━━━━━━━━━━━━━━
⚠️ 如有异常，请登录服务器检查
```

## 实施步骤

### 步骤 1：安装 Skill

```bash
clawhub install hermes-self-audit
# 或手动复制 SKILL.md 到 ~/.hermes/skills/hermes-self-audit/
```

### 步骤 2：创建 Cronjob

```bash
hermes cron create "0 10 * * 1" \
  --name "Hermes Self-Audit" \
  --deliver "feishu:<你的飞书ChatID>" \
  --skills "hermes-self-audit"
```

> **提示**：将 `--deliver` 替换为你实际使用的聊天平台和目标 ID。
> 支持平台：feishu、discord、telegram 等。

### 步骤 3：手动触发测试

```bash
hermes self-audit
# 或通过 cronjob 手动运行
hermes cron run <job_id>
```

## 安全说明

- 此审计不改变任何配置，只读取状态
- 所有操作都是只读的安全检查
- 报告推送到聊天平台后，用户自行判断是否有异常
- 如需回滚任何变更，参考：`hermes curator rollback <skill-name>`

## 依赖

- hermes cli
- curator 已启用（检查 `~/.hermes/config.yaml` 里的 `curator.enabled`）
- 可选：honcho（如果用作 memory provider）

## 示例：真实场景

以下示例为通用场景，帮助理解报告各项含义：

---

### 示例 1：Curator 发现高频修改的 skill

```
【Skill 变更 (近 7 天)】
  ⚠️ 高频修改：调研报告模板
    - 2026-05-06 10:00（创建）
    - 2026-05-06 14:30（修改：添加「成本」维度）
    - 2026-05-06 16:45（修改：添加「运维复杂度」维度）
    - 24h内修改 3 次 → 建议：检查是否存在 prompt 震荡
```

**含义**：高频修改可能表示 Agent 在自我适应过程中出现了不稳定调整。

---

### 示例 2：Agent 自创 skill 被发现

```
【Skill 变更 (近 7 天)】
  🆕 Agent 创建：cso（2026-05-05 15:20）
    - created_by: agent
    - 来源：根据用户多次提到某场景自动生成
    - 内容：跨服数据聚合操作手册
  📦 归档：0 个
```

**含义**：部分 Agent 支持根据工作流自动创建 skill。审计可发现这些「隐藏的学习」，确保它们符合用户预期。

---

### 示例 3：长期未使用的 skill

```
【长期未使用 (90天+)】
  ⚠️ stock-monitor (最后使用: 2026-02-01, 95天未用)
    - 用途：股票数据查询
    - 建议：归档或删除
  ⚠️ podcast-generator (最后使用: 2026-03-15, 52天未用)
    - 用途：播客内容生成
    - 建议：确认是否仍需要

  ✅ 正常（高频使用）：
    - shell-script（最后使用: 2026-05-06）
    - python-debugpy（最后使用: 2026-05-07）
```

**含义**：与当前工作无关的 skill 长期未用是正常的，可归档处理。

---

### 示例 4：Curator 异常 — 意外归档

```
【Curator 状态】
  ⚠️ 异常：调研报告模板 已被归档
    - 归档时间：2026-05-07 02:00
    - 最后使用：2026-04-10（87天前）
    - 触发条件：archive_after_days=90，但 curator 提前归档
    - 可能原因：curator 误判 / 时间计算 bug
    → 建议：用 `hermes curator rollback 调研报告模板` 恢复

【配置检查】
  curator.archive_after_days: 90 ✅
  curator.stale_after_days: 30 ✅
  ⚠️ 实际行为与配置不符，需检查 curator 日志
```

**含义**：配置值与实际行为不符时，可能存在 curator bug 或配置被意外修改。

---

### 示例 5：Memory Provider 被意外切换

```
【Memory Provider】
  ⚠️ 警告：provider 从「honcho」变更为「mem0」
    - 检测时间：2026-05-07 10:00
    - 可能原因：用户执行了 `hermes memory setup` 或配置被修改
    - 影响：用户画像、历史记忆可能丢失或格式不兼容
    → 建议：确认是否为预期操作

【配置检查】
  memory.provider: mem0 ⚠️ 与上次不同（上次：honcho）
  memory.memory_enabled: true ✅
```

**含义**：memory provider 变更会影响 Agent 对用户的理解连续性（偏好、习惯等）。

---

### 示例 6：正常状态的审计报告

```
🛡️ Hermes 自改进审计报告
━━━━━━━━━━━━━━━━━━
📅 审计时间：2026-05-07 10:00
⏰ 上次审计：7 天前

【Curator 状态】
  运行状态：✅ 启用
  自动归档：开启
  归档阈值：90 天未使用
  上次运行：2 小时前

【Skill 变更 (近 7 天)】
  🆕 新建：1 个
    - hermes-self-audit（2026-05-06，人工创建）
  ✏️ 修改：0 个
  📦 归档：0 个
  ✅ Agent 自创 skill：0 个

【高频使用 Top 5】
  1. shell-script — 18 次
  2. python-debugpy — 12 次
  3. systematic-debugging — 8 次
  4. kanban-orchestrator — 5 次
  5. writing-plans — 4 次

【长期未使用 (90天+)】
  - finnhub（最后使用: 2026-02-01）

【Memory Provider】
  当前：honcho ✅
  状态：正常
  Peers：1 个

【配置检查】
  curator.enabled: true ✅
  memory.provider: honcho ✅ 未变更

━━━━━━━━━━━━━━━━━━
✅ 无异常项目，下次审计：2026-05-14 10:00
```

---

## 常见问题

**Q: 报告里发现异常的 skill 怎么办？**
A: 用 `hermes skills inspect <skill-name>` 查看详情，用 `hermes curator status` 查看 curator 是否有策略自动处理。

**Q: 能关掉自动归档吗？**
A: 可以，`hermes config set curator.enabled false`，但建议保持开启以防止 skill 无限膨胀。

**Q: 90 天未使用是怎么算的？**
A: Curator 会追踪每个 skill 的 `last_activity_at` 时间戳，90 天内有调用则不算未使用。

**Q: Agent 自创的 skill 安全吗？**
A: Agent 自创的 skill 会被标记 `created_by: agent`。审计可以发现这些「隐藏学习」，确保它们符合用户预期。如有非预期的 skill，建议检查并决定是否保留。

**Q: 什么情况下需要人工介入？**
A: 以下情况建议人工检查：
- Agent 自创了非预期的 skill
- memory.provider 被意外切换
- 大量 skill 在短时间内被归档
- 配置值与预期不符

**Q: 支持哪些平台推送报告？**
A: 支持 Hermes 支持的所有平台：飞书（feishu）、Discord、Telegram、Slack 等。使用 `--deliver` 参数指定目标，格式为 `平台:chat_id`。
