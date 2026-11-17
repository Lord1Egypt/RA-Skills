# JSON Output Schema

Place the JSON object under `## JSON Output`. Keep the seven keys in this order. Use `Not provided` for unknown values and `Conflict detected; human review required` for conflicts.

```json
{
  "project_overview": {
    "project_name": "Not provided",
    "time_range": "Not provided",
    "current_phase": "Not provided",
    "overall_status": "Not provided",
    "summary": "Not provided",
    "evidence": "Not provided"
  },
  "progress": [
    {"item": "Not provided", "status": "Not provided", "evidence": "Not provided"}
  ],
  "confirmed_decisions": [
    {"decision": "Not provided", "result": "Not provided", "confirmed_by": "Not provided", "evidence": "Not provided"}
  ],
  "action_items": [
    {"task": "Not provided", "owner": "Not provided", "department": "Not provided", "ddl": "Not provided", "deliverable": "Not provided", "status": "Not provided", "evidence": "Not provided"}
  ],
  "risks_dependencies": [
    {"type": "Not provided", "description": "Not provided", "impact": "Not provided", "mitigation": "Not provided", "owner": "Not provided", "evidence": "Not provided"}
  ],
  "cross_department_relationships": [
    {"from": "Not provided", "to": "Not provided", "collaboration_item": "Not provided", "status": "Not provided", "evidence": "Not provided"}
  ],
  "needs_human_confirmation": [
    {"item": "Not provided", "reason": "Not provided", "suggested_confirm_with": "Not provided", "evidence": "Not provided"}
  ]
}
```
