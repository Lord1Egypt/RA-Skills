# Interaction Rules

## Intent Routing

优先顺序：

1. 明确金额且像流水：走记账
2. 明确是想法、心情、复盘：走感悟
3. 明确是待办、联系、提醒事项：走备忘
4. 明确包含“提醒我”：走提醒流程
5. 明确在问消费趋势、异常、复盘或简报开关：走洞察

## Parsing Rules

### 记账

最低需要：

- `type`
- `amount`

可选补充：

- `category`
- `occurred_at`
- `counterparty`
- `note`
- `tags`

如果只缺一个关键字段，只追问一次。

### 备忘

最低需要：

- `content`

可选补充：

- `kind`
- `title`
- `tags`
- `mood`

### 提醒

最低需要：

- `事项`
- `提醒时间`

先创建或定位 memo，再创建 cron job，再回写 `cron_job_id`。

### 洞察

最低需要：

- `period`
- `view`

默认映射：

- `本周消费总结` → `period=week` `view=summary`
- `本月花销复盘` → `period=month` `view=summary`
- `最近消费有什么异常` → `period=7d` `view=anomaly`
- `最近消费和备忘一起看一下` → `period=7d` `view=combined`

订阅开关：

- `开启每周简报` / `关闭每周简报`
- `开启月度复盘` / `关闭月度复盘`

订阅默认关闭；只有用户明确要求时才创建或删除 cron。

Reminder rule:
Never mentally convert reminder times yourself.
Always pass the raw user time phrase, such as `1分钟后`, `今晚9点`, or `明早8点`,
to `python SKILL_DIR/scripts/reminders.py create-payload --reminder-at "..."`.

## Output Rules

- 一条消息完成回复
- 优先使用 `｜` 分段
- 信息顺序：结果 -> 关键字段 -> 最近相关记录
- 内容超长时先压缩，不够再拆分
- 洞察类回复最多带 1 条建议
- 低信号定时摘要必须完全静默，不补发解释

## Example Inputs

- `今天午饭 32`
- `收到工资 8000`
- `本月收入和支出汇总`
- `记一下，下周一联系房东`
- `记一下：我最近状态不好，总是睡得很晚`
- `找找上周关于焦虑的记录`
- `提醒我明晚 8 点交水电费`
- `本周消费总结`
- `本月花销复盘`
- `最近消费有什么异常`
- `最近消费和备忘一起看一下`
- `开启每周简报`
