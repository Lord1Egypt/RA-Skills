# IOC 智能巡检报告

> 为智能建筑/园区自动生成专业巡检报告

## 🎯 功能特性

- **📊 设备状态巡检**：分析设备在线率、故障分布
- **🚨 报警处理分析**：统计报警数量、响应时长、处理率
- **⚡ 能耗数据分析**：对比昨日/上周能耗，识别异常
- **📋 工单进度追踪**：统计工单完成率、SLA 达成情况
- **💡 智能建议生成**：基于数据生成运维建议

## 📦 安装

```bash
# 克隆到 OpenClaw skills 目录
git clone <repo> ~/.openclaw/skills/ioc-patrol-report
cd ~/.openclaw/skills/ioc-patrol-report

# 安装依赖
pip install psycopg2-binary pyyaml
# 或使用 uv
uv sync
```

## ⚙️ 配置

编辑 `config.yaml`：

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

## 🚀 使用

### 生成日报
```bash
uv run scripts/generate_report.py --type daily --date 2026-03-10
```

### 生成本周报告
```bash
uv run scripts/generate_report.py --type weekly --week 2026-W10
```

### 在 OpenClaw 中使用
```
请为我生成今天的 IOC 巡检报告
```

## 📁 文件结构

```
ioc-patrol-report/
├── SKILL.md              # 技能文档
├── README.md             # 项目说明
├── package.json          # 包信息
├── pyproject.toml        # Python 配置
├── config.yaml           # 数据库配置
├── scripts/
│   └── generate_report.py  # 报告生成器
├── assets/
│   └── report-template.md  # 报告模板
├── references/
│   ├── ioc-knowledge.md    # 知识库
│   └── db-schema.md        # 数据库文档
└── reports/              # 输出目录
```

## 🔧 高级配置

### 自定义模板
编辑 `assets/report-template.md` 可自定义：
- 公司 Logo
- 报告标题格式
- 重点关注指标
- 建议模板

### 添加自定义分析
编辑 `scripts/generate_report.py`：

```python
def custom_kpi(df):
    return df['value'].mean() * 1.2
```

## 📄 许可证

MIT License

## 🏢 适用场景

- 智能楼宇/园区运维
- 物业管理公司
- 工业园区监控
- 商业综合体管理
- 数据中心运维

---

Made with ❤️ by ClawHub
