---
name: ioc-patrol-report
description: 为 IOC（智能运营中心）生成智能巡检报告。自动分析设备状态、报警记录、能耗数据，生成专业的巡检日报/周报。支持连接 PostgreSQL 数据库读取实时数据，输出 Markdown/HTML 报告。适用于物业管理、商业综合体、工业园区等场景。
---

# IOC 智能巡检报告

为智能建筑/园区自动生成专业巡检报告。

## 功能

- **设备状态巡检**：分析设备在线率、故障分布
- **报警处理分析**：统计报警数量、响应时长、处理率
- **能耗数据分析**：对比昨日/上周能耗，识别异常
- **工单进度追踪**：统计工单完成率、SLA 达成情况
- **智能建议生成**：基于数据生成运维建议

## 使用方法

### 1. 配置数据源

编辑 `~/.openclaw/skills/ioc-patrol-report/config.yaml`：

```yaml
database:
  host: localhost
  port: 5432
  name: ioc_db
  user: admin
  password: ${DB_PASSWORD}

tables:
  devices: devices
  alarms: alarms
  work_orders: work_orders
  energy: energy_records
```

### 2. 生成日报

```bash
# 生成今日巡检报告
uv run scripts/generate_report.py --type daily --date 2026-03-10

# 生成本周巡检报告
uv run scripts/generate_report.py --type weekly --week 2026-W10
```

### 3. 读取报告

```python
# 查看生成的报告
read ~/.openclaw/skills/ioc-patrol-report/reports/daily-2026-03-10.md
```

## 报告模板

报告模板位于 `assets/report-template.md`，可自定义：

- 公司 Logo
- 报告标题格式
- 重点关注指标
- 建议模板

## 进阶：自定义分析规则

编辑 `scripts/analyze.py` 添加自定义分析逻辑：

```python
# 示例：添加自定义 KPI
def custom_kpi(df):
    return df['value'].mean() * 1.2
```

## 参考

- IOC 系统知识：`references/ioc-knowledge.md`
- 数据库表结构说明：`references/db-schema.md`
