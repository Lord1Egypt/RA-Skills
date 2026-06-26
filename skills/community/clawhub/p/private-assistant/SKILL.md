---
name: private-assistant
description: Personal bookkeeping, memo/journal, reminder, and spending-insight assistant for Hermes. Use when the user wants to record income or expenses, save notes or reflections, query summaries, review spending patterns, correlate spending with memos, or manage explicit reminders backed by local JSONL files and cron.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [personal, bookkeeping, memo, journal, reminder, productivity]
    related_skills: [apple-notes, apple-reminders]
---

# Private Assistant

消息平台优先的私人助手 skill，覆盖三条子链路：

- 记录：收入、支出、备忘、感悟
- 提醒：创建、查看、取消
- 洞察：消费总结、异常观察、消费与备忘联动复盘、可选订阅简报

## References

- `references/data-model.md`：字段和存储约定
- `references/interaction-rules.md`：输入解析与输出模板
- `references/insight-rules.md`：洞察信号、低打扰策略、关联边界
- `references/insight-templates.md`：周摘要、月复盘、异常观察、联动复盘模板

## Scripts

- `python SKILL_DIR/scripts/records.py ...`
- `python SKILL_DIR/scripts/reminders.py ...`
- `python SKILL_DIR/scripts/insights.py ...`

`SKILL_DIR` 是当前 skill 根目录。数据固定写入 `HERMES_HOME/data/private-assistant/`，按当前 profile 自动隔离。

## When To Use

- 用户要“记一笔”“记账”“查账”“看本月花了多少”
- 用户要“记一下”“备忘”“写个感悟”“找一下上周那条记录”
- 用户要“提醒我明天 8 点”“取消刚才那个提醒”“看看还有哪些提醒”
- 用户要“本周消费总结”“本月花销复盘”“最近消费有什么异常”
- 用户要“最近消费和备忘一起看一下”“开启每周简报”“关闭月度复盘”

## Core Rules

1. 普通对话默认只给一条最终回复，不发送过程信息。
2. 回复在一条消息内保持结构清晰，优先用 `｜` 和短标签组织。
3. 缺少一个关键字段时，只追问一个问题；不要发散追问。
4. 不把正文或账目流水写入 memory。`memory` 只用于稳定偏好，例如“默认币种改成 USD”。
5. 默认币种是 `CNY`，时间未写明时按当前本地时间处理。
6. 洞察默认只支持手动查询；订阅式周/月简报只有在用户明确开启时才创建。
7. 定时洞察在低信号时必须保持静默；如果脚本返回 `[SILENT]`，就不要向用户发送额外说明。

## Workflow

### 1. 先判断意图

- 账目：收入 / 支出 / 查询 / 汇总 / 修改 / 删除
- 备忘：记录 / 查询 / 修改 / 删除
- 提醒：创建 / 查看 / 取消
- 洞察：手动总结 / 异常观察 / 联动复盘 / 开启订阅 / 关闭订阅

如果一句话同时包含“记一下”和明确金额，优先按记账处理；如果是情绪、感受、复盘、状态，优先按感悟处理。

### 2. 记账

新增账目：

```bash
python SKILL_DIR/scripts/records.py transaction-add --type expense --amount 32 --category 餐饮 --note "午饭"
python SKILL_DIR/scripts/records.py transaction-add --type income --amount 8000 --category 工资 --note "四月工资"
```

查询和汇总：

```bash
python SKILL_DIR/scripts/records.py transaction-list --range today --limit 5
python SKILL_DIR/scripts/records.py transaction-list --range week --category 餐饮
python SKILL_DIR/scripts/records.py transaction-summary --range month
```

修改和删除：

```bash
python SKILL_DIR/scripts/records.py transaction-update --last --amount 28
python SKILL_DIR/scripts/records.py transaction-delete --last
```

处理规则：

- 记账至少需要 `type` 和 `amount`
- `category` 未提供时，可依赖脚本自动补默认分类
- `counterparty` 用于商家、来源、对方名称
- 如果金额是算式，例如 `81+13`，默认先换算总额并只记 **一笔**，即 `94`；只有用户明确要求拆分时才分多笔写入

### 3. 备忘与感悟

新增记录：

```bash
python SKILL_DIR/scripts/records.py memo-add --content "明天联系房东" --kind note
python SKILL_DIR/scripts/records.py memo-add --content "我最近总熬夜，有点焦虑" --kind reflection
```

查询：

```bash
python SKILL_DIR/scripts/records.py memo-list --range 7d --limit 5
python SKILL_DIR/scripts/records.py memo-list --keyword 焦虑 --kind reflection
```

修改和删除：

```bash
python SKILL_DIR/scripts/records.py memo-update --last --content "明天联系房东并确认租金"
python SKILL_DIR/scripts/records.py memo-delete --last
```

处理规则：

- 明显是想法、情绪、复盘时用 `reflection`
- 明显是待办、提醒事项时用 `note`
- 用户没给标题时，脚本会从正文生成短标题

### 4. 提醒

创建提醒时，先确保对应 memo 已存在，再创建 cron 任务。

创建流程：

1. 用 `records.py memo-add` 新建或确认目标 memo
2. 生成提醒 payload：

Do not mentally convert relative or natural-language reminder times into timestamps.
Pass the raw user time phrase directly to `reminders.py create-payload --reminder-at ...`.
```bash
python SKILL_DIR/scripts/reminders.py create-payload --last --reminder-at "明早8点"
python SKILL_DIR/scripts/reminders.py create-payload --last --reminder-at "1分钟后提醒我回消息"
```

3. 调用 `cronjob` 工具：

```python
cronjob(
    action="create",
    schedule=payload["schedule"],
    prompt=payload["prompt"],
    name=payload["name"],
)
```

4. 创建成功后回写：

```bash
python SKILL_DIR/scripts/reminders.py link --last --cron-job-id "<job_id>" --reminder-at "<payload['reminder_at']>"
```

查看提醒：

```bash
python SKILL_DIR/scripts/reminders.py list
```

取消提醒：

1. 找到目标提醒：

```bash
python SKILL_DIR/scripts/reminders.py get --last
```

2. 调用：

```python
cronjob(action="remove", job_id=record["cron_job_id"])
```

3. 本地解绑：

```bash
python SKILL_DIR/scripts/reminders.py unlink --last
```

提醒用的 cron prompt 必须自包含，不能依赖短期上下文。

### 5. 洞察

手动洞察优先用 `insights.py digest`：

```bash
python SKILL_DIR/scripts/insights.py digest --period week --mode manual --view summary
python SKILL_DIR/scripts/insights.py digest --period month --mode manual --view summary
python SKILL_DIR/scripts/insights.py digest --period 7d --mode manual --view anomaly
python SKILL_DIR/scripts/insights.py digest --period 7d --mode manual --view combined
```

映射规则固定为：

- `本周消费总结` → `--period week --view summary`
- `本月花销复盘` → `--period month --view summary`
- `最近消费有什么异常` → `--period 7d --view anomaly`
- `最近消费和备忘一起看一下` → `--period 7d --view combined`

订阅开启时：

1. 先生成 cron payload：

```bash
python SKILL_DIR/scripts/insights.py create-payload --period week
python SKILL_DIR/scripts/insights.py create-payload --period month
```

2. 用 `cronjob` 创建任务，并把 `skills=payload["skills"]` 一并传入。
3. 创建成功后，把开关和 `cron_job_id` 写回设置：

```bash
python SKILL_DIR/scripts/insights.py prefs-update --weekly-enabled true --weekly-cron-job-id "<job_id>"
python SKILL_DIR/scripts/insights.py prefs-update --monthly-enabled true --monthly-cron-job-id "<job_id>"
```

关闭订阅时：

1. 删除对应 cron job
2. 关闭本地偏好并清空 job id：

```bash
python SKILL_DIR/scripts/insights.py prefs-update --weekly-enabled false --weekly-cron-job-id ""
python SKILL_DIR/scripts/insights.py prefs-update --monthly-enabled false --monthly-cron-job-id ""
```

洞察规则：

- 先看账本，再引用 0 到 2 条同周期 memo 作为“同期记录”
- 不把 memo 写成强因果结论
- 最多给 1 条建议
- 低信号订阅返回 `[SILENT]`，不要补发解释

### 6. 定时任务注意事项

- cron job 在全新 session 里运行，没有当前对话上下文；prompt 必须自包含，不能依赖“刚才那条”“上一条消息”之类引用。
- 定时任务运行时不能向用户追问；如果时间、目标对象、频率、投递位置等关键字段还不明确，先在创建前问清楚，不要带着模糊参数落任务。
- 时间解析、相对时间换算、日期区间计算、cron 表达式生成，统一交给 `reminders.py` / `insights.py` 的 payload 脚本处理；不要用模型心算或临时手推。
- 金额汇总、窗口统计、异常阈值、周期边界等可脚本化计算，也应交给脚本产出；模型只负责意图判断、调用工具和整理最终话术。
- 创建提醒或订阅时，只有在 `cronjob(action=\"create\", ...)` 成功后，才能回写本地 `cron_job_id`；删除时也要先删 cron job，再解绑本地记录，避免状态不一致。
- `deliver` 默认留空以回投当前会话；只有用户明确要求发到其他会话、群组或线程时，才显式指定投递目标。
- 定时任务的最终输出要短、稳、可直接发送；不要在 cron prompt 里要求模型解释执行过程、复盘推理链，或再去创建新的 cron job。
- 定时洞察延续低打扰原则：脚本返回 `[SILENT]` 就直接静默，不补发“本次无内容”等解释性消息。

## Output Style

始终优先单条、结构化、极简回复。默认模板：

- 成功记账：`已记录｜支出 32 元｜分类：餐饮｜时间：今天 12:30｜备注：午饭`
- 成功备忘：`已保存备忘｜类型：感悟｜时间：今天 22:10｜内容：我最近总熬夜，有点焦虑`
- 查询汇总：`查询结果｜范围：本月｜支出：320 元｜收入：8000 元｜净额：7680 元｜最近记录：午饭 32 元`
- 提醒成功：`已设置提醒｜时间：明晚 20:00｜事项：交水电费`
- 洞察总结：`本周消费简报｜支出：268 元｜较上周：+22%｜Top1：餐饮 132 元｜高峰日：周三 68 元｜同期记录：周三提到“熬夜、状态差”｜建议：下周先只盯餐饮支出。`

不要输出：

- 工具调用过程
- 调试信息
- 多条碎片化回复
- 冗长解释
