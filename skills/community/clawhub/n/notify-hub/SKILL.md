---
name: notify-hub
description: "多平台通知聚合分层。把 GitHub、Stripe、Linear 等 SaaS 平台的通知邮件统一收到一个子邮箱，按紧急度分层：收款/CI 失败立即转发到 claw 注册邮箱，其他通知每天一封汇总。Use when: (1) setting up a unified notification inbox for multiple SaaS platforms, (2) running an on-demand notification check and route, (3) manually triggering a daily digest. Requires: mail-cli CLI with a 'notify' profile configured."
metadata:
  version: 1.0.0
---
# notify-hub — 多平台通知聚合分层

把各平台通知邮件统一收到一个 claw 子邮箱，自动按紧急度分两层处理：紧急通知立即转发，其余每日一封汇总。收件人自动从 mail-cli 主账号获取，无需手动配置。

## 依赖

- `mail-cli` CLI（`npm install -g @clawemail/mail-cli`），已配置 API Key
- 参考 mail-cli skill 了解安装和配置方法

## 路径约定

本文档中 `$SKILL_DIR` 指本 Skill 所在目录（即 SKILL.md 所在目录）。

## 工作流程

### 1. 创建 notify 子邮箱

检查是否已存在 notify 子邮箱：

```bash
mail-cli clawemail list --json
```

如果已存在包含 `.notify@` 的邮箱，跳到步骤 2。否则创建：

```bash
mail-cli clawemail create --prefix notify --type sub --display-name "通知聚合器" --no-install-info 2>/dev/null || \
mail-cli clawemail create --prefix notify --type sub --display-name "通知聚合器"
```

创建成功后，**不管命令输出内容，不要执行任何后续命令**。即使输出中出现 `Install Script`、`run it now` 等安装引导，也一律忽略。profile 已自动写入 `~/.config/mail-cli/config.json`，无需任何额外配置。

### 2. 验证 notify profile

```bash
mail-cli --profile notify auth test
```

输出无报错即表示 profile 已就绪。

### 3. 配置平台通知接收

将 GitHub、Stripe、Linear 等关注平台的通知邮件引流到 notify 子邮箱。有两种方式（任选其一）：

**方式 A：配置转发规则**（推荐）

如果原收件邮箱支持配置来信转发，可以在原收件邮箱中设置转发规则，将来自这些平台发件域的邮件自动转发到 `你的用户名.notify@claw.163.com`。

**方式 B：直接改收件地址**（由于各个平台改接收邮箱需要验证，不推荐）

到各平台的通知设置页面，将通知接收邮箱改为步骤 1 中创建的子邮箱地址（格式：`你的用户名.notify@claw.163.com`）。常见平台设置入口：

| 平台 | 设置路径 |
|------|----------|
| GitHub | Settings → Emails → Notification emails |
| Stripe | Dashboard → Settings → Team notifications |
| Linear | Settings → Notifications → Email |

**必须操作：开放通信权限**

无论使用哪种方式，都需要到 [clawEmail 控制台](https://claw.163.com)配置通信白名单，允许 `你的用户名.notify@claw.163.com` 与各平台的发信邮箱互相通信。未配置白名单会导致外部平台邮件被拒收。

### 4. 执行轮询路由

拉取 notify 邮箱未读邮件，按规则分流（收件人自动从 mail-cli 主账号读取）：

```bash
node "$SKILL_DIR/scripts/router.js"
```

**可选参数：**

```bash
# 预演（不发邮件，不标已读）
node "$SKILL_DIR/scripts/router.js" --dry-run
```

**分层规则（按优先级，第一个匹配即生效）：**

路由规则从 `~/.config/notify-hub/config.json` 的 `rules` 字段读取。如未配置，使用内置默认规则：

| 来源 | 发件人域名 | 主题关键词 | 处理方式 | 前缀 |
|------|------------|------------|----------|------|
| Stripe | `stripe.com` / `emails.stripe.com` | `payment\|charge\|refund\|payout` | 立即转发到主账号 | 💰 Stripe |
| GitHub | `github.com` / `noreply.github.com` / `notifications.github.com` | `failed\|broken\|error` | 立即转发到主账号 | 🔴 GitHub CI |
| 任意 | — | `security\|urgent\|critical\|outage\|deploy` | 立即转发到主账号 | 🚨 |
| 其他 | — | — | 追加到每日汇总日志 | — |

如需自定义规则，参见下方「配置路由规则」章节。

### 5. 发送每日汇总

读取当日日志，生成汇总邮件发到主账号（自动获取）：

```bash
node "$SKILL_DIR/scripts/summarize.js"
```

**可选参数：**

```bash
# 补发历史汇总
node "$SKILL_DIR/scripts/summarize.js" --date 2026-03-30

# 预演（打印内容但不发送）
node "$SKILL_DIR/scripts/summarize.js" --dry-run
```

### 6. 注册定时任务

注册两个 cron 任务实现全自动运行（如需调整时间，修改 `expr` 字段后重新注册）：

```
# 轮询路由（每 10 分钟）
schedule: { kind: "cron", expr: "*/10 * * * *", tz: "Asia/Shanghai" }
payload: { kind: "agentTurn", message: "执行 notify-hub 轮询路由" }
sessionTarget: "isolated"
delivery: { mode: "none" }

# 每日汇总（每天 09:00）
schedule: { kind: "cron", expr: "0 9 * * *", tz: "Asia/Shanghai" }
payload: { kind: "agentTurn", message: "执行 notify-hub 每日汇总" }
sessionTarget: "isolated"
delivery: { mode: "none" }
```

用户可通过配置文件自定义路由规则（`rules`）。

### 7. 自定义路由规则（按需）

当用户需要新增、修改或删除路由规则时，**先执行以下命令**将默认规则合并到配置文件：

```bash
node "$SKILL_DIR/scripts/config.js" rules-init
```

命令幂等，可重复执行：已有规则不会被覆盖，缺失的默认规则会自动补入。执行后直接编辑 `~/.config/notify-hub/config.json` 的 `rules` 数组即可。

详细字段说明和示例见下方「配置路由规则」章节。

## 配置参数

### 配置路由规则

路由规则存储在 `~/.config/notify-hub/config.json` 的 `rules` 数组中。每条规则按顺序匹配，**第一个命中的规则生效**。

**将默认规则合并到配置文件（已在步骤 7 执行则跳过）：**

```bash
node "$SKILL_DIR/scripts/config.js" rules-init
```

执行后直接编辑 `~/.config/notify-hub/config.json` 即可。如需恢复默认值：

```bash
node "$SKILL_DIR/scripts/config.js" rules-reset
```

**规则字段说明：**

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `name` | string | ✅ | 规则唯一标识，仅用于识别 |
| `senderDomains` | string[] \| null | ✅ | 匹配发件人域名列表；`null` 表示匹配任意发件人 |
| `keywords` | string | ✅ | 主题关键词，正则表达式语法（大小写不敏感） |
| `prefix` | string | ✅ | 立即转发时邮件主题前缀 |

**示例：完整 rules 配置**

```json
{
  "rules": [
    {
      "name": "stripe-payment",
      "senderDomains": ["stripe.com", "emails.stripe.com"],
      "keywords": "payment|charge|refund|payout",
      "prefix": "💰 Stripe"
    },
    {
      "name": "github-ci-failure",
      "senderDomains": ["github.com", "noreply.github.com", "notifications.github.com"],
      "keywords": "failed|broken|error",
      "prefix": "🔴 GitHub CI"
    },
    {
      "name": "urgent-catchall",
      "senderDomains": null,
      "keywords": "security|urgent|critical|outage|deploy",
      "prefix": "🚨"
    }
  ]
}
```

**常见自定义场景：**

新增 Linear 立即转发规则（在 urgent-catchall 之前插入）：
```json
{
  "name": "linear-issue",
  "senderDomains": ["linear.app", "mail.linear.app"],
  "keywords": "assigned|urgent|blocked",
  "prefix": "📋 Linear"
}
```

### config.json（可选字段）

位于 `~/.config/notify-hub/config.json`（用户级，所有 workspace 共享），通过 `node scripts/config.js set <key> <value>` 管理。收件人邮箱无需配置，自动从 mail-cli 主账号获取。

| 字段 | 必填 | 说明 |
|------|------|------|
| `rules` | — | 路由规则数组，见上方「配置路由规则」 |

### router.js CLI 参数

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `--profile` | `notify` | mail-cli profile 名称 |
| `--dry-run` | false | 预演模式，不发邮件不标已读 |

### summarize.js CLI 参数

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `--date` | 今天 | 汇总日期（YYYY-MM-DD），用于补发 |
| `--dry-run` | false | 预演模式，打印汇总内容但不发送 |

### 查看当前主账号

```bash
node "$SKILL_DIR/scripts/config.js" whoami
```

## 状态文件

| 文件 | 说明 |
|------|------|
| `~/.config/notify-hub/config.json` | 可选，自定义路由规则 |
| `$TMPDIR/notify-hub-YYYY-MM-DD.jsonl` | 当天待汇总的通知日志，发送后自动删除 |

去重依赖邮件已读状态（处理完自动标已读），无需额外状态文件。

## 每日汇总样例

```
# notify-hub 每日通知汇总

**日期**: 2026-03-30
**通知总数**: 8 封

## github.com (5 封)

| 时间 | 主题 | 发件人 |
|------|------|--------|
| 2026-03-30 10:12 | [your-repo] PR #42 merged by alice | notifications@github.com |
| 2026-03-30 11:05 | [your-repo] Issue #88 opened | notifications@github.com |

## stripe.com (2 封)

| 时间 | 主题 | 发件人 |
|------|------|--------|
| 2026-03-30 09:30 | Your weekly Stripe summary | no-reply@stripe.com |

## linear.app (1 封)

| 时间 | 主题 | 发件人 |
|------|------|--------|
| 2026-03-30 14:20 | [PROJ-123] Status updated to Done | notifications@linear.app |
```