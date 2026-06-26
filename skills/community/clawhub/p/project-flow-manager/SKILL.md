---
name: project-flow-manager
description: 全流程项目管理工具，用于梳理项目关键节点、管理参与部门与任务排期、跟踪KPI完成度、生成定期报告、发送进度提醒邮件、创建可视化看板。适用于需要结构化项目管理的场景，包括项目启动、里程碑跟踪、跨部门协作、进度汇报、风险预警等。
---

# 项目流程管理器 (Project Flow Manager)

全流程项目管理工具，支持从项目规划到落地复盘的全生命周期管理。

## 核心功能

### 1. 项目结构管理
- **关键节点梳理**: 定义项目里程碑、阶段目标、交付物
- **参与部门管理**: 记录各部门职责、对接人、协作关系
- **任务分解**: 将项目拆解为可执行的具体任务
- **任务排期**: 设置起止时间、依赖关系、优先级

### 2. 进度跟踪
- **进展更新**: 记录任务完成百分比、阻塞问题、备注
- **KPI监控**: 跟踪关键指标完成情况
- **风险预警**: 识别延期风险、资源瓶颈
- **落地效果**: 记录项目成果、数据复盘

### 3. 报告与通知
- **定期报告**: 自动生成周报/月报/阶段报告
- **邮件提醒**: 发送任务进度提醒、截止预警
- **看板可视化**: 生成项目状态看板（Markdown/HTML）

## 数据结构

项目数据存储在 `projects/` 目录下，每个项目一个 JSON 文件：

```json
{
  "id": "project-001",
  "name": "项目名称",
  "description": "项目描述",
  "status": "进行中",
  "startDate": "2024-01-01",
  "endDate": "2024-06-30",
  "departments": [
    {
      "id": "dept-001",
      "name": "技术部",
      "owner": "张三",
      "responsibility": "系统开发"
    }
  ],
  "milestones": [
    {
      "id": "ms-001",
      "name": "需求确认",
      "date": "2024-01-15",
      "status": "已完成"
    }
  ],
  "tasks": [
    {
      "id": "task-001",
      "name": "数据库设计",
      "departmentId": "dept-001",
      "milestoneId": "ms-001",
      "startDate": "2024-01-10",
      "endDate": "2024-01-20",
      "status": "进行中",
      "progress": 60,
      "priority": "高",
      "assignee": "李四",
      "blockers": []
    }
  ],
  "kpis": [
    {
      "id": "kpi-001",
      "name": "系统可用性",
      "target": "99.9%",
      "current": "99.5%",
      "status": "接近目标"
    }
  ],
  "reports": []
}
```

## 使用流程

### 创建新项目

```bash
# 交互式创建
python3 scripts/create_project.py

# 或从模板创建
python3 scripts/create_project.py --template it-project
```

### 管理项目数据

```bash
# 添加部门
python3 scripts/add_department.py <project-id> --name "市场部" --owner "王五"

# 添加里程碑
python3 scripts/add_milestone.py <project-id> --name "上线发布" --date "2024-03-01"

# 添加任务
python3 scripts/add_task.py <project-id> --name "前端开发" --dept "dept-001" --start "2024-02-01" --end "2024-02-28"

# 更新任务进度
python3 scripts/update_task.py <project-id> <task-id> --progress 80 --status "进行中"
```

### 生成报告和看板

```bash
# 生成周报
python3 scripts/generate_report.py <project-id> --type weekly

# 生成项目看板
python3 scripts/generate_board.py <project-id> --format markdown

# 发送进度提醒邮件
python3 scripts/send_reminder.py <project-id> --recipient manager@company.com
```

## 命令速查

| 操作 | 命令 |
|------|------|
| 创建项目 | `python3 scripts/create_project.py` |
| 列出项目 | `python3 scripts/list_projects.py` |
| 查看项目 | `python3 scripts/view_project.py <id>` |
| 添加部门 | `python3 scripts/add_department.py <pid> --name <n>` |
| 添加里程碑 | `python3 scripts/add_milestone.py <pid> --name <n> --date <d>` |
| 添加任务 | `python3 scripts/add_task.py <pid> --name <n> --dept <d>` |
| 更新任务 | `python3 scripts/update_task.py <pid> <tid> --progress <p>` |
| 生成报告 | `python3 scripts/generate_report.py <pid> --type <t>` |
| 生成看板 | `python3 scripts/generate_board.py <pid> --format <f>` |
| 发送提醒 | `python3 scripts/send_reminder.py <pid> --recipient <email>` |

## 项目模板

参考 `references/project-templates.md` 了解可用的项目模板：
- `it-project`: IT系统开发项目
- `marketing-campaign`: 营销活动项目
- `product-launch`: 产品上线项目
- `custom`: 自定义项目

## 高级用法

### 批量导入任务

```bash
python3 scripts/import_tasks.py <project-id> --file tasks.csv
```

### 设置自动提醒

```bash
# 设置每日检查并发送逾期提醒
python3 scripts/schedule_reminders.py <project-id> --frequency daily --time 09:00
```

### 导出项目数据

```bash
python3 scripts/export_project.py <project-id> --format json --output backup.json
```

## 数据存储

- 项目数据: `projects/<project-id>.json`
- 报告输出: `reports/<project-id>-<date>-<type>.md`
- 看板输出: `boards/<project-id>-board.md`

## 依赖

- Python 3.8+
- 邮件功能需要配置 SMTP（见 `references/email-config.md`）

## 最佳实践

1. **定期更新**: 建议每周至少更新一次任务进度
2. **及时记录**: 遇到问题或变更立即记录，避免遗忘
3. **里程碑检查**: 每个里程碑完成后进行复盘
4. **KPI对齐**: 确保KPI与业务目标一致，定期评估
