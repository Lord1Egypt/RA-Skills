---
name: okr-work-manager
description: >
  KPI/OKR 工作管理系统。支持季度/年度 OKR 目标设置，通过自然语言记录工作日志
  自动追踪目标进度，生成周报、月报、季报、年报，实现目标管理+工作记录+进度追踪+复盘总结的完整闭环。
version: 2.0.0
tags: [okr, kpi, work-management, productivity, time-tracking, weekly-report, goal-tracking]
author: QClab
license: MIT-0
---

# KPI/OKR 工作管理

将零散的工作日志转化为结构化的 OKR 管理，实现从目标设置到成果总结的完整数据闭环。

## 何时使用此技能

- 用户要记录每日工作日志
- 用户要创建/查看/更新周计划
- 用户要生成周报、月报、季报或年报
- 用户要设置或查看 OKR 目标和进度
- 用户要复盘季度或年度 OKR 完成情况

## 核心原则

1. **自然语言输入**：任意格式，Agent 智能解析工时、标签
2. **零依赖**：Agent 直接读写 JSON 文件，无需安装任何工具
3. **自动追踪**：工作日志关联 OKR，自动累计进度
4. **渐进分析**：周报(轻度) -> 月报(对齐) -> 季报(提炼) -> 年报(复盘)

## 数据存储

数据存放在 `{workspace}/.okr-work-manager/` 目录下：

```
.okr-work-manager/
├── daily/           # 工作日志 (YYYY-MM-DD.json)
├── plans/           # 周计划 (YYYY-Www.json)
├── weekly/          # 周报 (YYYY-Www-report.json)
├── monthly/         # 月报 (YYYY-MM-report.json)
├── quarterly/       # 季报 (YYYY-QX-report.json)
├── yearly/          # 年报 (YYYY-report.json)
├── okr_config.json  # OKR 配置
└── okr_progress.json # OKR 进度
```

> 完整 JSON schema 参见 [data-schema.md](references/data-schema.md)

## 定时调度（Gateway Cron）

通过 Agent Gateway Cron 实现定期报告生成。

### 首次使用：初始化定时任务

Agent 通过 `cron.add` 创建 3 个隔离式 cron 任务：

```json
{
  "name": "okr:weekly-report",
  "schedule": { "kind": "cron", "expr": "0 18 * * 5", "tz": "Asia/Shanghai" },
  "sessionTarget": "isolated",
  "payload": {
    "kind": "agentTurn",
    "message": "执行本周工作周报。读取 {workspace}/.okr-work-manager/daily/ 本周日志和 plans/ 本周计划，汇总工时、标签、OKR 贡献，保存到 weekly/ 目录。参考 skills/okr-work-manager/references/data-schema.md",
    "model": "haiku"
  },
  "delivery": { "mode": "announce" }
}
```

```json
{
  "name": "okr:monthly-report",
  "schedule": { "kind": "cron", "expr": "0 20 28 * *", "tz": "Asia/Shanghai" },
  "sessionTarget": "isolated",
  "payload": {
    "kind": "agentTurn",
    "message": "执行本月 OKR 对齐分析月报。读取 {workspace}/.okr-work-manager/ 本月全部日志，对比 okr_config.json 分析对齐度和进度预警，保存到 monthly/ 目录。参考 skills/okr-work-manager/references/data-schema.md",
    "model": "haiku"
  },
  "delivery": { "mode": "announce" }
}
```

CLI 方式（将 `{cli}` 替换为实际命令）：

```bash
{cli} cron add \
  --name "okr:weekly-report" \
  --cron "0 18 * * 5" \
  --tz "Asia/Shanghai" \
  --session isolated \
  --message "执行本周工作周报..." \
  --model haiku --announce
```

### 默认值

| 任务 | 默认时间 | cron 表达式 | 说明 |
|------|---------|------------|------|
| 周报 | 每周五 18:00 | `0 18 * * 5` | 工作日结束前 |
| 月报 | 每月 28 日 20:00 | `0 20 28 * *` | 月底提前 |
| 季报/年报 | 不自动执行 | — | 由用户手动触发 |

### 频率调整

```
周报改成每周五 17 点
月报改成每月最后一天
暂停自动周报
恢复周报
```

## 四级分析体系

### 1. 周报（轻度展示）

- 读取本周日志，对比周计划完成情况
- 汇总各 OKR 的本周贡献
- 保存至 `weekly/YYYY-Www-report.json`

### 2. 月报 + OKR 对齐分析（中度）

- 读取本月全部日志和周报
- 工作与 OKR 对齐度分析，识别未对齐工作
- OKR 进度预警（落后/超前）
- 下月对齐建议
- 保存至 `monthly/YYYY-MM-report.json`

### 3. 季报 + OKR 智能提炼（深度）

- 读取季度内所有月报
- OKR 完成情况总结，KR 级进度评估
- 基于工作分布智能提炼下一季度 OKR 建议
- 保存至 `quarterly/YYYY-QX-report.json`

### 4. 年报 + 年度 OKR 复盘（全面）

- 读取全年季报
- 季度 OKR 与年度 OKR 对齐分析
- 全年工作模式识别和趋势分析
- 下一年度 OKR 建议
- 保存至 `yearly/YYYY-report.json`

| 分析类型 | 对齐分析 | 进度预警 | OKR 提炼 | 趋势分析 | 调整建议 |
|----------|---------|---------|---------|---------|---------|
| 周报 | - | - | - | - | - |
| 月报 | OKR 对齐 | 超前/落后 | - | - | 下月 |
| 季报 | OKR 对齐 | OKR 完成 | 智能提炼 | - | 下季度 |
| 年报 | 季度-年度 | 全年完成 | OKR 建议 | 季度趋势 | 下一年度 |

## OKR 管理

### 双重模式

| 模式 | 说明 |
|------|------|
| **主动设置** | 用户在季度/年度开始前设置目标，实时追踪进度 |
| **智能提炼** | 季报/年报基于工作数据自动生成 OKR 建议 |

### OKR ID 命名

| 类型 | 格式 | 示例 |
|------|------|------|
| 季度 OKR | `q_{year}-Q{quarter}_{index}` | `q_2026-Q1_1` |
| 年度 OKR | `y_{year}_{index}` | `y_2026_1` |

### 操作方式

- 设置 OKR：`"设置 Q1 OKR：1.完成架构升级（200h）- 核心模块重构（100h）..."`
- 查看进度：`"查看 Q1 OKR 进度"`
- 更新 KR 进度：Agent 根据工作日志自动累计

## 时间计算规则

- **ISO 8601 标准**：周从周一开始，第1周包含1月4日
- **季度**：Q1(1-3月)、Q2(4-6月)、Q3(7-9月)、Q4(10-12月)

## 依赖技能

无外部依赖。Agent 直接读写 JSON 文件。

## 参考文档

- **[data-schema.md](references/data-schema.md)** — 全部 JSON 数据结构定义（日志、计划、报告、OKR 配置、OKR 进度）
- **[troubleshooting.md](references/troubleshooting.md)** — 常见问题、数据修复、从 Python 版本迁移

## 使用示例

- **[basic-usage.md](examples/basic-usage.md)** — 记录日志、创建计划、生成周报
- **[advanced-usage.md](examples/advanced-usage.md)** — OKR 设置、进度查看、月报对齐分析、季报提炼、年报复盘

## 版本历史

| 版本 | 日期 | 变更 |
|------|------|------|
| 2.0.0 | 2026-03-31 | 重构为分层文档架构；补全月报/季报/年报/进度 JSON schema；统一路径为 {workspace}；增加 Gateway Cron 调度；增加标准 frontmatter 字段 |
| 1.0.0 | 2026-03-27 | Agent 纯驱动重构：移除 Python 脚本，单 SKILL.md |
