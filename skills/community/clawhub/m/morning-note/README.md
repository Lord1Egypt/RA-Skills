# Morning Note — 投资晨报 Skill

每日投资晨报生成工具，整合宏观动态、行业信号、持仓异动和催化事件日历。

## 功能

- 📰 宏观扫描：美股、汇率、大宗商品隔夜动态
- 🏭 行业信号：5大集群（能源建材/有色化工/制造/金融地产/消费服务）见底信号匹配
- 💼 持仓异动：ETF组合净值、汇率监控、自选股异动
- 📅 催化日历：未来7天重要事件前瞻
- 🧠 IMA 知识库同步：晨报自动归档

## 触发方式

- 说 "生成晨报" / "今日晨报" / "morning note"
- 通过 cron 定时任务每周自动触发

## 依赖

- `neodata-financial-search` skill（金融数据查询）
- IMA 知识库（可选，用于归档）

## 输出

结构化 Markdown 晨报，保存至 `morning-note/reports/YYYY-MM-DD-morning-note.md`

## 版本

v1.0.0 — 初始版本
