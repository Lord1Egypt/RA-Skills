# JSON Output Schema

JSON 输出必须放在 `## JSON 输出` 模块下，并使用 `json` fenced code block。

未知值统一使用 `"未提供"`。冲突值统一使用 `"存在冲突，需人工确认"`。

```json
{
  "project_overview": {
    "project_name": "未提供",
    "time_range": "未提供",
    "current_phase": "未提供",
    "overall_status": "未提供",
    "summary": "未提供",
    "evidence": "未提供"
  },
  "progress": [
    {
      "item": "未提供",
      "status": "未提供",
      "evidence": "未提供"
    }
  ],
  "confirmed_decisions": [
    {
      "decision": "未提供",
      "result": "未提供",
      "confirmed_by": "未提供",
      "evidence": "未提供"
    }
  ],
  "action_items": [
    {
      "task": "未提供",
      "owner": "未提供",
      "department": "未提供",
      "ddl": "未提供",
      "deliverable": "未提供",
      "status": "未提供",
      "evidence": "未提供"
    }
  ],
  "risks_dependencies": [
    {
      "type": "未提供",
      "description": "未提供",
      "impact": "未提供",
      "mitigation": "未提供",
      "owner": "未提供",
      "evidence": "未提供"
    }
  ],
  "cross_department_relationships": [
    {
      "from": "未提供",
      "to": "未提供",
      "collaboration_item": "未提供",
      "status": "未提供",
      "evidence": "未提供"
    }
  ],
  "needs_human_confirmation": [
    {
      "item": "未提供",
      "reason": "未提供",
      "suggested_confirm_with": "未提供",
      "evidence": "未提供"
    }
  ]
}
```

