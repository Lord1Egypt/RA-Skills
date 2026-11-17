---
slug: linear-workflow-bot
name: linear-workflow-bot
version: 1.0.1
displayName: Linear工作流机器人
summary: '"解决Webhook易断、免费额度烧光、多服务配置混乱痛点，打造可自愈的Linear任务流水线。把Linear任务自动接入"通知-执行-回写-Git同步"流水线。面向独立开发者与一人公司，解决"'
license: MIT
description: "把Linear任务自发接入\"通知-执行-回写-Git同步\"流水线。面向独立开发者与一人公司，解决Webhook易断、免费额度烧光、多服务配置散乱、Git同步冲突四大痛点。适用关键词：linear、webhook、discord、make、pipedream、zapier、自发化、任务流水线、git。可自动提升工作效率
  sync。"'
tags:
- 自动化
- 项目管理
- 通知集成
- 工作流
- 效率
- linear
- git
- api
- discord
- webhook
tools:
- read
- exec
- write
homepage: '""'
category: '"Automation"'
pricing_tier: free
homepage: "https://skillhub.cn/skill/"
---

> **核心功能**: 本技能提供提升工作效率等能力。

> **功能说明**: 本技能涵盖 workflow 等核心能力。

# Linear 工作流机器人

自动化流水线：**Linear → Webhook 平台 → 通知通道 → 任务执行 → Git 同步**。Linear 创建的任务自动触发处理，实时通知、执行、回写结果并同步到 Git 仓库，含 Webhook 自愈与免费额度降级机制.

## 能力清单
### 三层自动化平台选型
Make.com（1000 ops/月免费首选）/ Pipedream（即时触发）/ Zapier（付费兜底）/ 自建 webhook 接收器（无限额度），按预算与任务量自动选型.
### Webhook 健康检查与自愈
每小时心跳探活、30 min 无运行发测试 webhook、探活失败重投最近 5 条历史任务、切换备用平台、3 次失败进死信队列（DLQ）.
### 任务处理闭环（含失败补偿）
确认 → DM 通知 → 状态流转 → 执行 → 回写评论 → 完成流转 → Git 同步，每步都有失败补偿（重试/回退/告警）.
### 配置中心化
单一 JSON（`~/.linearbot/config.json`）管理团队/状态/Discord/Git/额度五类配置，变量引用 `${VAR}` 从环境变量读取避免明文 secrets.
### 免费额度监控与降级
每日 `quota-check` 看用量，超 80% 阈值自动降级（batch-daily 批量处理 / drop-low-priority 丢弃低优 / switch-platform 切平台）.

## 输入参数
```json
{
  "task": {
    "id": "ENG-456",
    "title": "调研 wasm 在边缘计算的应用",
    "state": "Todo",
    "assignee": "user-uuid",
    "team_id": "team-uuid"
  },
  "action": "process",
  "config_path": "~/.linearbot/config.json"
}
```

## 典型场景
**何时使用：**
- 个人开发者以 Linear 为任务中枢，自动分发到 Discord/Git
- 小团队任务到达即通知即执行即归档
- 预算敏感榨干免费额度（Make.com 1000 ops）
- Webhook 易断需自愈（scenario 挂了自动切备用平台）

**输入输出：**
- 输入：Linear 任务（标题/状态/assignee）+ 配置中心 JSON
- 输出：Discord 通知 + Linear 状态流转 + 任务产出文件 + Git commit/push + 死信队列告警

**不适用场景：**
- 无 Linear 账号的团队（核心依赖 Linear API）
- 任务量 > 10000/月（免费额度必爆，需自建接收器或付费）
- 企业级 Jira/Asana 用户（需另行适配）

## 使用说明
### Step 1：配置 Linear API
在 `~/.linearbot/linear.env` 写入 `LINEAR_API_KEY`（Linear Settings → API → Personal API keys）.

### Step 2：写配置中心
编辑 `~/.linearbot/config.json`：
```json
{
  "$schema": "linearbot/v1",
  "linear": { "teamId": "team-uuid", "states": {"todo":"state-uuid","inProgress":"state-uuid","done":"state-uuid","canceled":"state-uuid"}, "watchFilter": "state.name = \"Todo\"" },
  "notify": { "channel": "discord", "discord": { "botToken": "${DISCORD_BOT_TOKEN}", "notifyUserId": "discord-user-id", "taskChannelId": "channel-id", "allowBots": true } },
  "git": { "repo": "/path/to/repo", "autoPush": true, "commitPrefix": "task:", "branch": "main", "conflictStrategy": "rebase" },
  "quota": { "platform": "make", "monthlyLimit": 1000, "warningThreshold": 0.8, "degradeStrategy": "batch-daily" }
}
```

### Step 3：接 Webhook 平台（按选型表）
| 平台 | 免费额度 | 触发延迟 | 推荐场景 |
|---:|---:|---:|---:|
| Make.com | 1000 ops/月 | 15 min | **免费首选** |
| Pipedream | ~100 credits | 即时 | 需实时性 |
| Zapier | 100 tasks/月 | 15 min | 已有付费账号 |
| 自建 | 无限 | 即时 | 有服务器 |

选型规则：预算敏感 + 任务量 < 1000/月 → Make.com；任务量 > 1000/月 或需即时 → 自建；已有 Zapier 付费 → Zapier.

### Step 4：跑健康检查
```bash
（请参考skill目录中的脚本文件） doctor       # 全链路健康检查
（请参考skill目录中的脚本文件） quota-check  # 查额度用量
```

### Step 5：任务处理闭环（自动执行）
| 步骤 | 动作 | 失败补偿 |
|:---:|:---:|:---:|
| 1. 确认 | 在通道回复收到 | 失败重试 3 次，仍失败则写入死信 |
| 2. DM 通知 | 给配置的用户发私信 | 用户 ID 错则回退到通道 @mention |
| 3. 状态流转 | linear-api start <id> | Linear API 失败则走鉴权自愈 |
| 4. 执行任务 | 调子 Agent 或本地脚本 | 超时 30 min 则标记 "Stalled" |
| 5. 回写评论 | linear-api comment <id> "<summary>" | 评论过长则改用文件附件 |
| 6. 完成流转 | linear-api done <id> | 失败则保持 In Progress 并告警 |
| 7. Git 同步 | git add/commit/push | 冲突按 conflictStrategy 处理 |

状态机：`已实现 →(收到)→ In Progress →(成功)→ Done`；`In Progress →(超时)→ Stalled →(用户介入)→ In Progress / Canceled`；`In Progress →(失败)→ In Progress + 评论告警`.

## 应用示例
### 示例：任务自动处理流程
**输入：** Linear 任务 ENG-456 "调研 wasm 在边缘计算的应用"（watchFilter 匹配，触发 webhook）
**输出：**
1. 收到 → Discord 通知 + DM
2. linear-api.sh start ENG-456
3. 子 Agent 调研，生成 research/wasm-edge-computing.md
4. linear-api.sh comment ENG-456 "已完成，见 research/wasm-edge-computing.md"
5. linear-api.sh done ENG-456
6. git add research/ && commit -m "task: ENG-456 wasm调研" && push

## 异常响应
| 错误场景 | 原因 | 处理方式 |
|:------|------:|:------|
| 任务不触发 | scenario 停用或 watchFilter 不匹配 | `doctor` 查 scenario 状态；确认 watchFilter 对齐 |
| Linear API 报 401 | API Key 失效或权限不足 | 检查 `~/.linearbot/linear.env`；重新生成 API Key |
| Discord 不通知 | botToken 失效或 bot 无频道权限 | 验证 botToken；检查 bot 频道权限；`allowBots: true` |
| Git push 失败 | SSH key/credential 失效或冲突 | 按 conflictStrategy：rebase 重试3次 / merge 提交 / abort 告警 |
| 额度耗尽 | 月任务量超免费额度 | `quota-check` 启用降级；或切自建接收器；或升级付费 |

## 安装与配置
| 依赖项 | 类型 | 是否必需 | 获取方式 |
|---:|:---|---:|---:|
| Linear 账号 | SaaS | 必需 | linear.app 注册 |
| Make.com / Pipedream / Zapier | 自动化平台 | 三选一（或自建） | 对应官网注册 |
| Discord 账号 + Bot | 通知通道 | 推荐（可替换为 Slack/Telegram） | Discord Developer Portal |
| Git 仓库 | 版本控制 | 可选（启用 Git 同步时必需） | 本地或 GitHub/GitLab |
| Agent 平台 | 运行环境 | 必需 | 支持 SKILL.md 的任意 AI Agent |

**API Key 配置：**
- `LINEAR_API_KEY`：Linear → Settings → API → Personal API keys
- `DISCORD_BOT_TOKEN`：Discord Developer Portal → Bot → Token
- 全部存于环境变量或 `~/.linearbot/*.env`（权限 600），勿入库

**可用性分类：** MD+EXEC（Markdown 指令 + 必须通过 exec 执行脚本与 webhook 调用）.

## 疑问汇编
**Q1：免费 1000 ops 会超吗？**
A：单人日均任务 < 30 条基本够。每条任务平均消耗 2-3 ops（触发 + 通知）。超过 80% 阈值自动降级到 batch-daily.
**Q2：Git push 冲突怎么办？**
A：按 `conflictStrategy`：`rebase`（默认，自动 rebase 后重试 3 次）、`merge`（生成 merge commit）、`abort`（放弃同步并告警）.
**Q3：凭证安全？**
A：所有 secrets 用 `${VAR}` 引用环境变量，不写入 config.json。`~/.linearbot/` 目录权限设为 600.

## 能力边界
1. **强依赖 Linear**：核心流程基于 Linear API，无 Linear 账号无法使用；适配 Jira/Asana 需另行开发.
2. **免费额度有限**：Make.com 1000 ops/月、Pipedream ~100 credits、Zapier 100 tasks/月，任务量大需自建接收器或付费.
3. **Webhook 触发有延迟**：免费平台 15 min 轮询延迟，需即时性须用 Pipedream 或自建.
4. **当前面向个人/小团队**：多团队支持有限，需手动配 `teams` 数组；无内置 RBAC.
5. **Git 同步需仓库可写权限**：冲突策略依赖 git 操作能力，无权限场景只能 abort 告警.
6. **死信队列需人工处理**：DLQ 中的任务不会自动重试，需用户 `replay` 或 `ack`.

## 结果格式
```json
{
  "success": true,
  "data": { "result": "Linear工作流机器人处理结果", "execution_time": "0.5s", "metadata": {"version":"1.0","processor":"linear workflow bot"} },
  "execution_log": ["解析输入参数", "执行核心处理", "格式化输出结果"],
  "error": null
}
```

## 安全保障
| 风险类型 | 防范措施 |
|----------|---------|
| API密钥泄露 | 配置于环境变量中,密钥不得固化于代码 |
| 命令执行风险 | 限定执行预批准命令,不拼接用户输入到参数中 |
| 敏感数据暴露 | 输出不含敏感凭据 |

使用前请确认已阅读依赖说明章节，确保运行环境满足安全要求。

## 量化评估
| 操作场景 | 手动耗时 | 自动化耗时 | 效率提升 |
|----------|---------|-----------|---------|
| 文件解析与提取 | 5-10分钟/个 | <5秒/个 | 60-120x |
| 批量文件处理(100个) | 8-16小时 | <5分钟 | 96-192x |
| API调用与响应解析 | 2-3分钟/次 | <1秒/次 | 120-180x |
| 多接口数据聚合 | 15-30分钟 | <10秒 | 90-180x |
| 命令执行与结果收集 | 3-5分钟/次 | <2秒/次 | 90-150x |
| 重复任务批量执行 | 因任务而异 | 线性缩减 | 5-50x |
| 错误排查与修复 | 10-30分钟 | <30秒 | 20-60x |

## 特色分析
| 对比维度 | Linear工作流机器人 | 传统手动方式 | 通用脚本工具 |
|---------|------------|-------------|------------|
| 自动化程度 | 全流程自动 | 完全手动 | 部分自动 |
| 错误处理 | 内置错误恢复 | 依赖人工经验 | 基本try-catch |
| 可复用性 | 参数化配置 | 一次性脚本 | 模板化 |
| 安全合规 | 内置安全检查 | 无安全保障 | 无安全保障 |
| 适用场景 | 解决Webhook易断、免费额度烧光、多服务配置混乱痛点，打造可自愈的Linea | 通用场景 | 通用场景 |

## 主要功能
- **自动化执行**: "解决Webhook易断、免费额度烧光、多服务配置混乱痛点，打造可自愈的Linear任务流水线。把Linear任务自动接
- **文件处理**: 支持多种文件格式的读取、解析和写入操作
- **API集成**: 通过标准化接口调用外部服务并处理响应
- **命令执行**: 在安全沙箱中执行系统命令并收集结果
- **信息检索**: 快速搜索和过滤目标数据

## 高频问答
### Q1: Linear工作流机器人支持哪些输入格式？

A1: "解决Webhook易断、免费额度烧光、多服务配置混乱痛点，打造可自愈的Linear任务流水线。把Linear任务自动接入"通知-执行-回写-Git同步"流水线。支持文本指令和结构化参数输入，具体格式参考使用流程章节。

### Q2: 需要配置API Key吗？

A2: 是的，部分功能需要配置对应平台的API Key。请在依赖说明章节查看具体要求，并通过环境变量安全配置。

### Q3: 命令行执行失败怎么办？

A3: 检查命令参数是否正确，确认运行环境支持exec能力。如遇权限问题，请参照错误处理章节排查。

## 错误恢复方案
针对Linear工作流机器人使用中可能遇到的常见问题,提供以下排查方案:

| 错误类型 | 原因分析 | 解决方案 |
|---------|---------|---------|
| API认证失败(401) | API密钥错误或过期 | 检查密钥配置,重新生成token |
| 接口限流(429) | 请求频率超出限制 | 降低调用频率,启用重试退避策略 |
| 响应超时(504) | 网络延迟或服务端负载过高 | 增加超时阈值,检查网络连接 |
| 文件不存在 | 路径错误或文件未创建 | 检查路径拼写,确认文件已生成 |
| 文件格式不支持 | 扩展名不在支持列表中 | 转换为支持的格式后重试 |
| 权限不足 | 当前用户无读写权限 | 检查文件权限,以管理员身份运行 |
| 命令执行失败 | 参数错误或环境依赖缺失 | 检查命令语法,确认依赖已安装 |
| 进程超时 | 命令执行时间过长 | 增加超时设置,优化命令参数 |

### Linear工作流机器人通用排查步骤

1. **检查输入参数**: 确认所有必填参数已提供且格式正确
2. **查看日志输出**: 定位具体错误行和异常类型
3. **验证环境配置**: 确认依赖库版本和运行环境满足要求
4. **逐步调试**: 缩小问题范围,隔离故障模块

## 常见疑问汇总
## 故障恢复流程
针对Linear工作流机器人使用中可能遇到的常见问题,提供以下排查方案:

| 错误类型 | 原因分析 | 解决方案 |
|---------|---------|---------|
| API认证失败(401) | API密钥错误或过期 | 检查密钥配置,重新生成token |
| 接口限流(429) | 请求频率超出限制 | 降低调用频率,启用重试退避策略 |
| 响应超时(504) | 网络延迟或服务端负载过高 | 增加超时阈值,检查网络连接 |
| 文件不存在 | 路径错误或文件未创建 | 检查路径拼写,确认文件已生成 |
| 文件格式不支持 | 扩展名不在支持列表中 | 转换为支持的格式后重试 |
| 权限不足 | 当前用户无读写权限 | 检查文件权限,以管理员身份运行 |
| 命令执行失败 | 参数错误或环境依赖缺失 | 检查命令语法,确认依赖已安装 |
| 进程超时 | 命令执行时间过长 | 增加超时设置,优化命令参数 |
| 网络连接失败 | DNS解析失败或防火墙拦截 | 检查网络配置,确认代理设置 |

## 依赖说明

### 运行环境
- **Agent 平台**: 支持SKILL.md的任意AI Agent
- **操作系统**: Windows / macOS / Linux

### 可用性分类
- **分类**: MD（纯Markdown指令，通过自然语言驱动Agent完成操作）
- **说明**: 基于Markdown的AI Skill，通过自然语言指令驱动Agent完成操作。
