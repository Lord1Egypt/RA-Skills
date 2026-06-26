---
name: ioc-patrol-report
version: 1.0.0
description: 🏢 IOC智能运维报告生成器 - 为智能建筑/园区自动生成专业巡检报告。分析设备状态、报警记录、能耗数据、工单进度，生成日报/周报。支持PostgreSQL数据库连接，输出Markdown/HTML格式。适用于物业管理、商业综合体、工业园区、医院学校等智能建筑运维场景。
metadata: {"openclaw":{"emoji":"📊","category":"reporting","keywords":["ioc","patrol","report","maintenance","building-management","smart-building","facility-management","运维报告","巡检报告","智能建筑","物业管理"],"triggers":["巡检报告","运维报告","IOC报告","设备巡检","能源报告","物业报告","智能运维","运维日报","运维周报","智能建筑报告"]}}
---

# 🏢 IOC 智能巡检报告

**为智能建筑/园区自动生成专业巡检报告**

---

## ✨ 核心功能

| 功能模块 | 描述 |
|----------|------|
| 📊 **设备状态巡检** | 分析设备在线率、故障分布、运行状态 |
| 🚨 **报警处理分析** | 统计报警数量、响应时长、处理率、重复报警 |
| ⚡ **能耗数据分析** | 对比昨日/上周能耗，识别异常用能点 |
| 📝 **工单进度追踪** | 统计工单完成率、SLA达成情况、积压情况 |
| 💡 **智能建议生成** | 基于数据自动生成运维优化建议 |

---

## 🚀 快速开始

### 安装

```bash
clawhub install ioc-patrol-report
```

### 配置数据源

编辑 `~/.openclaw/skills/ioc-patrol-report/config.yaml`：

```yaml
database:
  host: localhost
  port: 5432
  name: ioc_db
  user: admin
  password: ${DB_PASSWORD}  # 建议使用环境变量

tables:
  devices: devices          # 设备表
  alarms: alarms            # 报警表
  work_orders: work_orders  # 工单表
  energy: energy_records    # 能耗表

report:
  company_name: "XX物业管理有限公司"
  project_name: "XX商业综合体"
  output_dir: "./reports"
```

### 生成报告

```bash
# 生成今日巡检报告
cd skills/ioc-patrol-report
uv run scripts/generate_report.py --type daily

# 生成指定日期报告
uv run scripts/generate_report.py --type daily --date 2026-03-20

# 生成本周巡检报告
uv run scripts/generate_report.py --type weekly --week 2026-W12
```

---

## 📋 报告示例

### 日报输出格式

```markdown
# 📊 IOC智能巡检日报 - 2026-03-20

## 一、设备状态总览

| 类型 | 总数 | 在线 | 离线 | 故障 | 在线率 |
|------|------|------|------|------|--------|
| 空调 | 128 | 125 | 2 | 1 | 97.7% |
| 照明 | 356 | 354 | 2 | 0 | 99.4% |
| 电梯 | 24 | 24 | 0 | 0 | 100% |
| 消防 | 89 | 89 | 0 | 0 | 100% |

## 二、报警处理情况

- 今日报警总数：23 条
- 已处理：21 条
- 处理中：2 条
- 平均响应时间：8.5 分钟
- 处理率：91.3%

### 重点关注报警
1. 🔴 3F-空调机组A异常（处理中）
2. 🟡 地下室照明回路故障（已处理）

## 三、能耗分析

| 能源类型 | 今日用量 | 昨日用量 | 环比 |
|----------|----------|----------|------|
| 电(kWh) | 12,345 | 12,100 | +2.0% |
| 水(m³) | 456 | 480 | -5.0% |
| 天然气(m³) | 123 | 130 | -5.4% |

## 四、工单进度

- 新增工单：5 个
- 已完成：4 个
- 进行中：3 个
- SLA达成率：92%

## 五、运维建议

1. ⚠️ 3F空调机组需重点关注，建议安排检修
2. ✅ 能耗整体平稳，用水量持续下降，节水措施见效
3. 📝 建议增加地下室照明巡检频次

---
*报告生成时间：2026-03-20 08:00*
*IOC智能运维系统*
```

---

## 📖 使用案例

### 案例1：商业综合体日常巡检

**场景**：某商业综合体物业每天需要生成巡检报告

**配置**：
```yaml
report:
  company_name: "XX物业管理公司"
  project_name: "XX购物中心"
```

**定时任务**：
```bash
# crontab -e
0 8 * * * cd /root/clawd/skills/ioc-patrol-report && uv run scripts/generate_report.py --type daily
```

### 案例2：工业园区周报汇总

**场景**：工业园区每周汇总运维数据

**配置**：
```yaml
report:
  company_name: "XX工业园区"
  project_name: "A区厂房"
  weekly_summary: true
```

**执行**：
```bash
# 每周一早8点生成
0 8 * * 1 uv run scripts/generate_report.py --type weekly
```

### 案例3：医院智能运维

**场景**：医院后勤部门需要重点关注设备运行

**自定义配置**：
```yaml
priority_devices:
  - type: "医用气体"
    alert_threshold: 99.9%  # 可用性要求
  - type: "净化空调"
    alert_threshold: 99%
  - type: "电梯"
    alert_threshold: 99.5%
```

### 案例4：数据中心巡检

**场景**：数据中心需要严格监控温湿度和电力

**自定义指标**：
```yaml
custom_metrics:
  temperature:
    range: [18, 27]  # 合规范围
    alert_deviation: 2  # 偏差告警阈值
  humidity:
    range: [40, 60]
  ups_load:
    max: 80%  # 负载上限
```

---

## ⚙️ 高级配置

### 自定义报告模板

编辑 `assets/report-template.md`：

```markdown
# {{company_name}} 巡检报告

## {{project_name}} - {{date}}

{% for section in sections %}
{{ section.content }}
{% endfor %}
```

### 自定义分析规则

编辑 `scripts/analyze.py`：

```python
def custom_kpi(df):
    """自定义KPI计算"""
    return {
        'availability': df['online'] / df['total'],
        'efficiency': df['output'] / df['input']
    }

def anomaly_detection(df):
    """能耗异常检测"""
    threshold = df['value'].mean() * 1.5
    return df[df['value'] > threshold]
```

---

## 📁 目录结构

```
ioc-patrol-report/
├── SKILL.md              # 本文档
├── package.json          # 技能配置
├── config.yaml           # 数据源配置
├── scripts/
│   ├── generate_report.py  # 主程序
│   ├── analyze.py          # 分析模块
│   └── db_connector.py     # 数据库连接
├── assets/
│   └── report-template.md  # 报告模板
├── references/
│   ├── ioc-knowledge.md    # IOC知识库
│   └── db-schema.md        # 数据库结构说明
└── tests/
    └── test_report.py      # 单元测试
```

---

## 🔧 技术要求

- Python >= 3.10
- PostgreSQL >= 12
- 必需依赖：psycopg2-binary, pyyaml, pandas, jinja2

---

## 📊 适用场景

| 场景 | 报告周期 | 重点关注 |
|------|----------|----------|
| 商业综合体 | 日报/周报 | 客流、能耗、设备 |
| 工业园区 | 周报/月报 | 设备运行、能耗成本 |
| 医院学校 | 日报 | 关键设备、环境参数 |
| 数据中心 | 实时/日报 | 温湿度、电力、网络 |
| 智慧社区 | 周报 | 安防、能耗、设备 |

---

**让运维报告自动化、智能化 📊**
