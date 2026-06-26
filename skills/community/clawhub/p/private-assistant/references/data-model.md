# Data Model

主数据目录：`HERMES_HOME/data/private-assistant/`

## Files

- `transactions.jsonl`：账目流水
- `memos.jsonl`：备忘与感悟
- `settings.json`：默认币种、分类、回复风格、洞察订阅偏好
- `index.json`：最近一条记录和最近查询上下文

不会新增 `digests.jsonl`。洞察结果按需计算，不做长期摘要正文存储。

## Transaction

每条账目字段：

- `id`
- `type`: `expense | income`
- `amount`
- `currency`
- `category`
- `occurred_at`
- `counterparty`
- `note`
- `tags`
- `source`
- `created_at`
- `updated_at`

默认支出分类：

- `餐饮`
- `交通`
- `购物`
- `住房`
- `娱乐`
- `医疗`
- `学习`
- `人情`
- `其他`

默认收入分类：

- `工资`
- `报销`
- `副业`
- `转账`
- `理财`
- `红包`
- `其他`

## Memo

每条备忘字段：

- `id`
- `kind`: `note | reflection`
- `title`
- `content`
- `tags`
- `mood`
- `created_at`
- `updated_at`
- `reminder_at`
- `cron_job_id`
- `source`

## Settings

`settings.json` 最少包含：

- `default_currency`
- `expense_categories`
- `income_categories`
- `reply_style`
- `insight_preferences`

`insight_preferences` 字段：

- `weekly_enabled`
- `monthly_enabled`
- `focus`
- `memo_context_enabled`
- `suggestion_style`
- `low_signal_mode`
- `weekly_cron_job_id`
- `monthly_cron_job_id`

## Persistence Rules

- 主体数据只存本地 JSONL，不写入 memory
- `settings.json` 缺失时自动初始化
- 洞察偏好只写入 `settings.json`
- `index.json` 用于支持“修改上一条”“删除刚才那条”
- 读取 JSONL 时跳过坏行，不让单条坏记录阻塞整个查询
- 摘要、复盘、异常观察等分析结果不写入 `MEMORY.md`
