# Feishu Field Mapping

Use this file to map your real Feishu task/doc schema to OpenClaw workflow fields.

## Minimal Mapping

```yaml
feishu_mapping:
  source:
    group_id: ""
    message_url: ""
    requester: ""
    requirement_text: ""
  requirement:
    requirement_id: ""
    priority: ""
    project_tag: ""
    deadline: ""
  task:
    master_task_id: ""
    master_status: ""
    subtasks:
      coding_task_id: ""
      review_task_id: ""
      testing_task_id: ""
      bug_task_ids: []
  status_values:
    todo: "待开始"
    in_progress: "进行中"
    done: "已完成"
    blocked: "已阻塞"
  links:
    knowledge_base_urls: []
    historical_task_query_url: ""
```

## Suggested Extra Fields

```yaml
feishu_optional:
  owner_openid: ""
  qa_openid: ""
  reviewer_openid: ""
  biz_owner_openid: ""
  project_code: ""
  sprint: ""
  severity: ""
  requirement_type: ""
```

## Mapping Rules

- Normalize all status values to `待开始/进行中/已完成/已阻塞` before pipeline decisions.
- Keep `requirement_id` and `master_task_id` immutable once created.
- Store PR URL, branch, and CI URL as task custom fields for traceability.
- If project has multiple repos, map each module to repository + production branch explicitly.
