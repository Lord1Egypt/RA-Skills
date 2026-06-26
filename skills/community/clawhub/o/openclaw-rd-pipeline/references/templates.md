# Templates

Use these templates to keep outputs consistent across subagents.

## 1) project_context

```yaml
project_context:
  requirement_id: ""
  feishu:
    group_id: ""
    source_message_url: ""
    master_task_id: ""
  requester: ""
  priority: "medium"
  deadline: ""
  project:
    name: ""
    repository_url: ""
    production_branch: ""
    owner: ""
    role_mapping:
      pm: ""
      dev: ""
      reviewer: ""
      tester: ""
```

## 2) structured_requirement + refined_prompt

```yaml
structured_requirement:
  business_goal: ""
  input_output:
    inputs: []
    outputs: []
  boundaries:
    in_scope: []
    out_of_scope: []
  dependencies:
    modules: []
    apis: []
  non_functional:
    performance: ""
    compatibility: ""
    security: ""
  acceptance_criteria: []

refined_prompt:
  task_summary: ""
  implementation_notes: []
  historical_references: []
  knowledge_base_references: []
  done_definition: []
```

## 3) PR description block

```markdown
## Context
- Requirement ID: <id>
- Feishu Task ID: <id>
- Knowledge Links: <url1>, <url2>

## Change Summary
- <change 1>
- <change 2>

## Risk and Rollback
- Risk: <text>
- Rollback: <text>

## Validation
- Lint: <pass/fail>
- Type Check: <pass/fail>
- Unit Test: <pass/fail>
- E2E: <pass/fail>

## UI Evidence (required for UI change)
- Screenshot/Video: <url>
```

## 4) review checklist

```markdown
- Logic and boundary handling
- Exception handling and resilience
- Security (injection, authorization, sensitive data)
- Performance and scalability risk
- Reuse and maintainability
- Naming, structure, readability
- UI/interaction conformance (if frontend)
```

## 5) test report

```yaml
test_report:
  lint: pass
  type_check: pass
  unit_test:
    status: pass
    cases: 0
  e2e:
    status: pass
    cases: 0
  coverage:
    line: "0%"
    branch: "0%"
  defects: []
  ci_gate:
    ui_evidence_required: false
    ui_evidence_present: false
    merge_allowed: true
```

## 6) final owner notification

```markdown
任务已完成。

- Feishu任务卡片: <url>
- PM简报: <text>
- 开发简报: branch=<name>, PR=<url>, delta=<stats>
- 评审简报: result=<pass/fail>, issues=<count>, refs=<norm links>
- 测试简报: CI=<pass/fail>, coverage=<value>, cases=<count>
- 总耗时: <duration>
- 历史任务对比: <optional>
```
