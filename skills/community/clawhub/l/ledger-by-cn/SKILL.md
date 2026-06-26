---
name: ledger
description: 个人记账与账本管理工具。支持多账本、自然语言/批量记账、期初结余初始化、跨月余额趋势图、分类统计、多账本对比图、CSV导出、飞书云盘同步等。
version: "1.3.0"
author: "Victor"
emoji: "💰🐰"
tags: ["finance", "accounting", "ledger", "budget", "feishu"]
---

# Ledger - 个人记账技能（优化版）

## 核心职责（触发条件）

当用户提到以下任一场景时，必须使用本技能，不要用其他方式代替：

- 记账、记录收入/支出、批量添加交易
- 查看某账本某月/多月汇总、流水、余额
- 画余额趋势图、支出饼图、柱状图等
- 导出 CSV / 同步到飞书云盘 / 上传文件
- 查询/设置分类、预算（未来扩展）
- 任何提到"账本""期初""结余""画图""同步""飞书"等关键词

## 数据存储与重要约定（严格遵守）

- **【重要】每次查询账本时，必须从账本目录读取最新数据，不要使用上下文缓存或假设数据**
- 根路径：`~/.openclaw/skills_data/ledger/<账本名>/` （账本名如 "default"，不区分大小写但保持用户输入一致）


- 后续任何计算余额趋势、累计余额、月度汇总时：
  - **查询汇总时**：用户说"所有/全部"则包含所有月份数据，否则只统计指定月份
  - 所有统计到的月份数据直接累加

## 日期解析规则（容错增强）

用户输入日期可能简写，必须智能补全为 YYYY-MM-DD：

- "0114" / "14" → 当前月份的 14 日（例如当前 2026-03 → 2026-03-14）
- "1" → 当前月份 1 日（2026-03-01）
- "3月15日" → 当前年 03-15（2026-03-15）
- "2026-3-5" → 补零为 2026-03-05
- "去年12月" → 2025-12 (当年往前推一年)
- 无日期 → 默认当天（当前时间：2026-03-15）
- 如果跨月/跨年模糊，或输入如"上个月""明年"等相对时间，主动询问确认：
  示例回复："您说的'上个月'是指 2026 年 2 月吗？请确认日期范围。"

## 处理流程（Agent 必须严格遵循的思考链）

1. **解析用户输入**
   - 确定账本名（从上下文提取，如"我的账本"，默认 "default"）
   - 提取日期、金额、分类、账户、备注
     - 支持批量：多行"日期 金额 [分类] [账户] [备注]"
     - 金额识别：正数/负数/"+""-""花了""收入"等关键词判断正负



### SQLite CLI 工具（推荐，使用 uv 运行）

```bash
# 创建账本
uv run python ~/.openclaw/skills/ledger/src/cli.py create --name 新账本

# 列出账本
uv run python ~/.openclaw/skills/ledger/src/cli.py list

# 查看账本日期范围（输出格式：开始月份 结束月份）
uv run python ~/.openclaw/skills/ledger/src/cli.py range --name 兔兔
# 输出示例：2025-12 2026-03

# 查看所有交易
uv run python ~/.openclaw/skills/ledger/src/cli.py show --name 兔兔

# 查看单月汇总
uv run python ~/.openclaw/skills/ledger/src/cli.py show --name 兔兔 --month 2026-03

# 查看日期范围
uv run python ~/.openclaw/skills/ledger/src/cli.py show --name 兔兔 --from 2026-01 --to 2026-03

# 查看余额趋势
uv run python ~/.openclaw/skills/ledger/src/cli.py trend --name 兔兔

# 绘制账单折线图（单个账本） # 需要先查看记账范围
uv run python ~/.openclaw/skills/ledger/src/cli.py chart --name 兔兔 --from 2026-01 --to 2026-03

# 绘制多账本对比图 # 需要先查看记账范围
uv run python ~/.openclaw/skills/ledger/src/cli.py chart --name 兔兔 vk --from 2026-01 --to 2026-03

# 保存到指定路径
uv run python ~/.openclaw/skills/ledger/src/cli.py chart --name 兔兔 --output /tmp/chart.png

# 添加交易（日期默认当天）
uv run python ~/.openclaw/skills/ledger/src/cli.py add --name 兔兔 --amount -50 --category 餐饮
```

### Markdown 输出（飞书群聊）

添加 `--markdown` 参数输出 Markdown 格式：

```bash
# Markdown 格式查看单月汇总
uv run python ~/.openclaw/skills/ledger/src/cli.py show --name 兔兔 --month 2026-03 --markdown

# Markdown 格式查看余额趋势
uv run python ~/.openclaw/skills/ledger/src/cli.py trend --name 兔兔 --markdown
```

### SQLite 原生命令查询

```bash
# 按月统计收支
sqlite3 ~/.openclaw/skills_data/ledger/兔兔/ledger.db -header -column \
  "SELECT substr(date,1,7) as month, 
          SUM(CASE WHEN amount > 0 THEN amount ELSE 0 END) as income,
          SUM(CASE WHEN amount < 0 THEN amount ELSE 0 END) as expense
   FROM transactions GROUP BY month ORDER BY month;"

# 按分类统计支出
sqlite3 ~/.openclaw/skills_data/ledger/兔兔/ledger.db -header -column \
  "SELECT category, SUM(ABS(amount)) as total 
   FROM transactions WHERE amount < 0 
   GROUP BY category ORDER BY total DESC;"

# 查询2025年数据
sqlite3 ~/.openclaw/skills_data/ledger/兔兔/ledger.db -header -column \
  "SELECT id, date, amount, category, account, description 
   FROM transactions WHERE date LIKE '2025%';"
```

## 安全与边界

- 单笔 |amount| > 10000 必须二次确认
- 输入严重模糊或矛盾时，主动询问澄清，不要擅自假设
- 所有文件操作使用安全路径，避免越界
