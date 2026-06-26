# 数据结构参考

本文档定义 OKR 工作管理系统的所有 JSON 数据结构。

## 目录

- [工作日志](#工作日志)
- [周计划](#周计划)
- [周报](#周报)
- [月报](#月报)
- [季报](#季报)
- [年报](#年报)
- [OKR 配置](#okr-配置)
- [OKR 进度](#okr-进度)

---

## 工作日志

**路径**：`{data_dir}/daily/YYYY-MM-DD.json`

```json
{
  "date": "2026-03-06",
  "weekday": 4,
  "week": 10,
  "year": 2026,
  "week_id": "2026-W10",
  "logs": [
    {
      "content": "排查深圳友联流程数据重复",
      "hours": 1.0,
      "tags": ["#深圳友联", "#流程"],
      "okr_id": "q_2026-Q1_1",
      "timestamp": "2026-03-06T10:30:00",
      "original_input": "排查深圳友联流程数据重复(1h)"
    }
  ],
  "metadata": {
    "total_hours": 7.2,
    "total_items": 5,
    "tags_summary": {"#深圳友联": 3.0, "#后端": 4.2},
    "created_at": "2026-03-06T23:59:00"
  }
}
```

### 字段说明

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `date` | string | 是 | 日期，YYYY-MM-DD 格式 |
| `weekday` | number | 是 | 周几（1=周一，7=周日） |
| `week` | number | 是 | ISO 8601 周数 |
| `year` | number | 是 | 年份 |
| `week_id` | string | 是 | ISO 8601 周标识，YYYY-Www 格式 |
| `logs` | array | 是 | 工作记录数组 |
| `logs[].content` | string | 是 | 工作内容描述 |
| `logs[].hours` | number | 是 | 工时（小时） |
| `logs[].tags` | array | 否 | 标签数组，以 # 开头 |
| `logs[].okr_id` | string | 否 | 关联的 OKR ID |
| `logs[].timestamp` | string | 是 | 记录时间，ISO 8601 格式 |
| `logs[].original_input` | string | 否 | 用户原始输入（用于溯源） |
| `metadata` | object | 是 | 元数据 |
| `metadata.total_hours` | number | 是 | 当日总工时 |
| `metadata.total_items` | number | 是 | 当日工作条数 |
| `metadata.tags_summary` | object | 否 | 标签工时汇总 |
| `metadata.created_at` | string | 是 | 文件创建时间 |

---

## 周计划

**路径**：`{data_dir}/plans/YYYY-Www.json`

```json
{
  "year": 2026,
  "week": 10,
  "week_str": "10",
  "week_id": "2026-W10",
  "period": {
    "start": "2026-03-02",
    "end": "2026-03-08"
  },
  "created_at": "2026-03-02T10:00:00",
  "updated_at": "2026-03-02T10:00:00",
  "status": "active",
  "goals": ["完成系统架构升级", "解决生产环境问题"],
  "tasks": [
    {
      "id": "task-abc123",
      "description": "任务描述",
      "priority": "high",
      "tags": ["#标签"],
      "estimated_hours": 4.0,
      "okr_id": "q_2026-Q1_1",
      "completed": false,
      "actual_hours": 0,
      "created_at": "2026-03-02T10:00:00"
    }
  ],
  "focus_areas": ["重点领域1", "重点领域2"],
  "notes": "备注信息"
}
```

### 字段说明

| 字段 | 类型 | 说明 |
|------|------|------|
| `status` | string | 计划状态：`active` / `completed` / `archived` |
| `tasks[].priority` | string | 优先级：`high` / `medium` / `low` |
| `tasks[].completed` | boolean | 是否已完成 |
| `tasks[].actual_hours` | number | 实际耗时（完成后填写） |

---

## 周报

**路径**：`{data_dir}/weekly/YYYY-Www-report.json`

```json
{
  "report_type": "weekly",
  "period": "2026-W10",
  "year": 2026,
  "week": 10,
  "date_range": {
    "start": "2026-03-02",
    "end": "2026-03-08"
  },
  "generated_at": "2026-03-08T18:00:00",
  "summary": {
    "total_hours": 42.5,
    "total_tasks": 25,
    "work_days": 5
  },
  "category_distribution": {
    "#深圳友联": 15.0,
    "#系统优化": 12.0,
    "#会议": 8.5
  },
  "top_tags": [
    {"tag": "#深圳友联", "hours": 15.0, "count": 8}
  ],
  "plan_comparison": {
    "planned_tasks": 8,
    "completed_tasks": 6,
    "completion_rate": 0.75
  },
  "okr_contributions": {
    "q_2026-Q1_1": {
      "objective": "完成系统架构升级",
      "hours": 25.0,
      "tasks_count": 12
    }
  },
  "daily_breakdown": [
    {"date": "2026-03-02", "hours": 8.5, "tasks": 5},
    {"date": "2026-03-03", "hours": 7.0, "tasks": 4}
  ]
}
```

---

## 月报

**路径**：`{data_dir}/monthly/YYYY-MM-report.json`

```json
{
  "report_type": "monthly",
  "period": "2026-03",
  "year": 2026,
  "month": 3,
  "date_range": {
    "start": "2026-03-01",
    "end": "2026-03-31"
  },
  "generated_at": "2026-03-31T20:00:00",
  "summary": {
    "total_hours": 168.0,
    "total_tasks": 95,
    "work_days": 22,
    "avg_daily_hours": 7.6
  },
  "okr_alignment": {
    "aligned_hours": 142.0,
    "alignment_rate": 0.85,
    "aligned_okrs": ["q_2026-Q1_1", "q_2026-Q1_2"],
    "unaligned_work": [
      {
        "description": "临时运维支持",
        "hours": 12.0,
        "reason": "无对应 OKR 覆盖"
      }
    ]
  },
  "okr_progress": {
    "q_2026-Q1_1": {
      "objective": "完成系统架构升级",
      "month_hours": 68.0,
      "progress_estimate": 0.72,
      "status": "on_track",
      "alert": null
    },
    "q_2026-Q1_2": {
      "objective": "提升系统性能",
      "month_hours": 35.0,
      "progress_estimate": 0.45,
      "status": "at_risk",
      "alert": "进度落后，建议增加投入"
    }
  },
  "category_trend": {
    "#系统优化": {"hours": 65.0, "change": 0.15},
    "#会议": {"hours": 18.0, "change": -0.10}
  },
  "next_month_suggestions": [
    {
      "okr_id": "q_2026-Q1_2",
      "suggestion": "增加性能优化专项投入",
      "estimated_hours": 40.0
    }
  ]
}
```

### 字段说明

| 字段 | 类型 | 说明 |
|------|------|------|
| `okr_alignment.alignment_rate` | number | OKR 对齐率（已对齐工时/总工时） |
| `okr_progress[].status` | string | `on_track` / `at_risk` / `behind` / `completed` |
| `okr_progress[].alert` | string\|null | 进度预警消息，null 表示正常 |
| `category_trend[].change` | number | 工时占比环比变化（正=增加，负=减少） |

---

## 季报

**路径**：`{data_dir}/quarterly/YYYY-QX-report.json`

```json
{
  "report_type": "quarterly",
  "period": "2026-Q1",
  "year": 2026,
  "quarter": 1,
  "date_range": {
    "start": "2026-01-01",
    "end": "2026-03-31"
  },
  "generated_at": "2026-03-31T20:00:00",
  "summary": {
    "total_hours": 520.0,
    "total_tasks": 280,
    "work_days": 63,
    "active_okrs": 3,
    "completed_okrs": 1
  },
  "okr_results": [
    {
      "id": "q_2026-Q1_1",
      "objective": "完成系统架构升级",
      "target_hours": 200,
      "actual_hours": 185.0,
      "completion_rate": 0.92,
      "status": "mostly_complete",
      "key_result_progress": [
        {"description": "完成核心模块重构", "progress": 1.0},
        {"description": "完成性能优化", "progress": 0.8}
      ]
    }
  ],
  "work_pattern": {
    "top_categories": [
      {"category": "#系统优化", "hours": 180.0, "percentage": 0.35}
    ],
    "monthly_trend": [
      {"month": "2026-01", "hours": 160.0},
      {"month": "2026-02", "hours": 172.0},
      {"month": "2026-03", "hours": 188.0}
    ]
  },
  "next_quarter_okr_suggestions": [
    {
      "suggested_objective": "深化系统性能优化",
      "evidence": "Q1 性能优化投入 120h，已完成 80%",
      "suggested_key_results": [
        "将核心接口响应时间降至 50ms 以下",
        "完成负载均衡方案落地"
      ]
    }
  ]
}
```

### 季报 OKR 状态

| status | 说明 |
|--------|------|
| `completed` | 100% 完成 |
| `mostly_complete` | 75%-99% 完成 |
| `partially_complete` | 30%-74% 完成 |
| `at_risk` | 低于 30% 或进度严重落后 |
| `not_started` | 未投入工时 |

---

## 年报

**路径**：`{data_dir}/yearly/YYYY-report.json`

```json
{
  "report_type": "yearly",
  "period": "2026",
  "year": 2026,
  "date_range": {
    "start": "2026-01-01",
    "end": "2026-12-31"
  },
  "generated_at": "2026-12-31T20:00:00",
  "summary": {
    "total_hours": 2080.0,
    "total_tasks": 1100,
    "work_days": 260,
    "quarterly_okrs": 4,
    "yearly_okrs": 2,
    "yearly_okr_completion_rate": 0.75
  },
  "quarterly_okr_summary": [
    {
      "quarter": "Q1",
      "okrs_total": 3,
      "okrs_completed": 2,
      "total_hours": 520.0
    }
  ],
  "yearly_okr_alignment": {
    "y_2026_1": {
      "objective": "技术架构现代化",
      "quarters_contributed": ["Q1", "Q2", "Q3"],
      "total_hours": 680.0,
      "completion_rate": 0.85
    }
  },
  "work_pattern": {
    "top_categories": [
      {"category": "#系统优化", "hours": 580.0, "percentage": 0.28}
    ],
    "quarterly_trend": [
      {"quarter": "Q1", "hours": 520.0},
      {"quarter": "Q2", "hours": 540.0},
      {"quarter": "Q3", "hours": 510.0},
      {"quarter": "Q4", "hours": 510.0}
    ]
  },
  "next_year_okr_suggestions": [
    {
      "suggested_objective": "构建自动化运维体系",
      "evidence": "全年运维投入 360h，占 17%，具备自动化基础",
      "suggested_key_results": [
        "实现核心服务 90% 自动化部署",
        "建立完善的监控告警体系"
      ]
    }
  ]
}
```

---

## OKR 配置

**路径**：`{data_dir}/okr_config.json`

```json
{
  "quarterly": {
    "2026-Q1": [
      {
        "id": "q_2026-Q1_1",
        "objective": "完成系统架构升级",
        "key_results": [
          {
            "id": "kr_1_1",
            "description": "完成核心模块重构",
            "target": 100,
            "unit": "小时",
            "current": 68
          }
        ],
        "target_hours": 200,
        "created_at": "2026-01-01T09:00:00",
        "status": "active"
      }
    ]
  },
  "yearly": {
    "2026": [
      {
        "id": "y_2026_1",
        "objective": "技术架构现代化",
        "key_results": [
          {
            "id": "ykr_1_1",
            "description": "完成微服务架构迁移",
            "target": 4,
            "unit": "个服务",
            "current": 2
          }
        ],
        "target_hours": 800,
        "created_at": "2026-01-01T09:00:00",
        "status": "active"
      }
    ]
  }
}
```

### OKR ID 命名规则

| 类型 | 格式 | 示例 |
|------|------|------|
| 季度 OKR | `q_{year}-Q{quarter}_{index}` | `q_2026-Q1_1` |
| 季度 KR | `kr_{okr_index}_{kr_index}` | `kr_1_1` |
| 年度 OKR | `y_{year}_{index}` | `y_2026_1` |
| 年度 KR | `ykr_{okr_index}_{kr_index}` | `ykr_1_1` |

### OKR 状态

| status | 说明 |
|--------|------|
| `active` | 当前活跃 |
| `completed` | 已完成 |
| `archived` | 已归档 |

---

## OKR 进度

**路径**：`{data_dir}/okr_progress.json`

```json
{
  "last_updated": "2026-03-31T20:00:00",
  "quarterly": {
    "2026-Q1": [
      {
        "id": "q_2026-Q1_1",
        "objective": "完成系统架构升级",
        "total_target_hours": 200,
        "accumulated_hours": 185.0,
        "progress_rate": 0.92,
        "key_results": [
          {
            "id": "kr_1_1",
            "description": "完成核心模块重构",
            "target": 100,
            "unit": "小时",
            "current": 95,
            "progress_rate": 0.95
          }
        ],
        "weekly_trend": [
          {"week": "2026-W09", "hours": 42.0},
          {"week": "2026-W10", "hours": 38.0},
          {"week": "2026-W11", "hours": 45.0}
        ],
        "status": "mostly_complete",
        "estimated_completion_week": "2026-W13"
      }
    ]
  },
  "yearly": {
    "2026": [
      {
        "id": "y_2026_1",
        "objective": "技术架构现代化",
        "total_target_hours": 800,
        "accumulated_hours": 580.0,
        "progress_rate": 0.73,
        "status": "on_track",
        "quarterly_breakdown": [
          {"quarter": "Q1", "hours": 180.0},
          {"quarter": "Q2", "hours": 200.0},
          {"quarter": "Q3", "hours": 200.0}
        ]
      }
    ]
  }
}
```

### 字段说明

| 字段 | 类型 | 说明 |
|------|------|------|
| `progress_rate` | number | 完成进度（0.0-1.0） |
| `weekly_trend` | array | 每周工时投入趋势（季度 OKR） |
| `quarterly_breakdown` | array | 每季度工时投入（年度 OKR） |
| `estimated_completion_week` | string | 预计完成周（仅季度 OKR） |
