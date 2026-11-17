# Sub-Agent Communication Protocol v2.0

This file defines the **communication contract** between the master controller and sub-Agents in PM Master. All sub-Agents must follow this protocol,
and the master validates sub-Agent output through it.

---

## 1. Sub-Agent Output Contract (JSON Schema)

After each sub-Agent completes its task, it must report a structured JSON back to the master:

```json
{
  "agent_role": "planner-agent",
  "status": "success|partial|failed",
  "artifacts": [
    {
      "key": "wbs",
      "path": "/workspace/<slug>/plans/wbs.md",
      "rendered": true
    }
  ],
  "data_files": ["/workspace/<slug>/plans/wbs_data.yaml"],
  "project_yaml_updates": {
    "artifacts.wbs": "plans/wbs.md",
    "project.scope": "..."
  },
  "key_findings": [
    "The WBS contains 23 work packages, of which 5 are SOW-level and 18 are leaf packages",
    "The critical path is SOW1→SOW3→SOW5, with a total duration of about 12 weeks",
    "3 cross-domain dependencies were identified that need coordination"
  ],
  "warnings": [
    "SOW4 lacks an explicit owner, marked as (TBD)"
  ],
  "errors": []
}
```

### Field Descriptions

| Field | Required | Description |
|------|------|------|
| `agent_role` | Yes | sub-Agent role name (aligned with agents.md) |
| `status` | Yes | success=fully complete, partial=partially complete, failed=failed |
| `artifacts` | Yes | list of produced files, each with key (artifacts key name) and path |
| `data_files` | No | paths of produced data YAML files |
| `project_yaml_updates` | No | updates the master should write into project.yaml (the master writes them together after aggregation) |
| `key_findings` | Yes | 3-5 key findings |
| `warnings` | No | issues to note but not blocking |
| `errors` | No | blocking issues (when present, status should be failed) |

---

## 2. Sub-Agent Behavior Rules

### 2.1 Must Do

1. **Read project.yaml first**: use `project_state.py show` or directly Read the file
2. **Render with render.py**: do not handwrite Markdown; must use `render.py --template ... --data ... --out ...`
3. **Write back data**: artifact paths must be reported to the master, which writes them into project.yaml together
4. **Numeric estimates**: all estimate fields must be numeric values >0
5. **Fill unknowns with "(TBD)"**: do not leave blanks or fabricate data

### 2.2 Must Not Do

1. **Do not reply to the user directly**: all output is reported only to the master
2. **Do not modify other Agents' files**: write only your own responsible directory
3. **Do not fabricate data**: fill uncertain items with "(TBD)" and annotate
4. **Do not skip render.py**: template rendering must use render.py
5. **Do not modify project.yaml**: the master writes it together after aggregation

### 2.3 Exception Handling

When encountering problems:
- Missing data → fill "(TBD)", explain in warnings
- Template does not exist → report in errors, status=partial
- Dependency file does not exist → report in errors, status=failed
- Unsure how to proceed → explain in warnings, continue with best judgment

---

## 3. Master Aggregation Flow

```
1. Wait for all sub-Agents to report (or time out)
2. For each sub-Agent report:
   a. Validate JSON format integrity
   b. Verify the artifact files actually exist
   c. Aggregate project_yaml_updates
3. Write into project.yaml together (avoid concurrency conflicts)
4. Run consistency_check.py
5. If there are issues, hand the issue list to the corresponding sub-Agent to fix
6. Deliver after passing
```

---

## 4. Sub-Agent Role → Artifact Mapping

| Role | Produced files | artifacts key |
|------|---------|--------------|
| planner-agent | plans/wbs.md or plans/product_backlog.md | wbs / backlog |
| scheduler-agent | plans/schedule_gantt.md | schedule_gantt |
| risk-agent | risks/risk_register.md, risks/raid_log.md | risk_register, raid_log |
| stakeholder-agent | docs/stakeholder_register.md, docs/raci.md, docs/communication_plan.md | stakeholder, raci, communication_plan |
| reporter-agent | reports/status_report.md | status_report |
| program-agent | docs/program_charter.md, reports/portfolio_dashboard.md, risks/dependency_map.md, reports/benefits_realization.md | program_charter, portfolio_dashboard, dependency_map, benefits_realization |
| communication-agent | email draft (not sent directly) | email_draft |
| monitoring-agent | reports/status_report.md, artifacts/control_report.md | status_report, control_report |

---

## 5. Brief Template (master sends to sub-Agent)

```markdown
You are the [<role>] sub-Agent of PM Master. Your task is to independently produce the following files and report to the master when done.

## Input
- Project source of truth: <absolute path>/project.yaml (read with project_state.py or the Read tool)
- Template: <SKILL_DIR>/templates/<path>/<template>.md
- Render engine: <SKILL_DIR>/scripts/render.py

## Task
1. Read project.yaml to understand the project background
2. Organize the data needed for this artifact and write it as <slug>_data.yaml
3. Run: python3 <SKILL_DIR>/scripts/render.py --template <template path> --data <slug>_data.yaml --out <output path>
4. Verify the artifact file has been generated

## Report Format (must strictly follow)
When done, report in the following JSON format:
{
  "agent_role": "<your role>",
  "status": "success|partial|failed",
  "artifacts": [{"key": "<artifacts key name>", "path": "<artifact absolute path>"}],
  "data_files": ["<data file path>"],
  "project_yaml_updates": {"<key>": "<value>"},
  "key_findings": ["finding 1", "finding 2", "finding 3"],
  "warnings": [],
  "errors": []
}

## Constraints
- Only produce the files you are responsible for; do not touch other roles' files
- Must render with render.py; do not handwrite Markdown
- Estimates must be numeric (>0); fill unknown fields with "(TBD)"
- Do not reply to the user directly; report only to the master
```
