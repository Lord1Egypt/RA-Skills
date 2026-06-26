# Templates

Parameterized templates for files this skill generates. Read this when filling out
the project folder in Step 7 of SKILL.md. Substitute every `{{placeholder}}` with the
appropriate value from the user's interview answers and approved plan.

---

## Table of Contents

- [PROJECT.md Template](#projectmd-template)
- [project.json Template](#projectjson-template)
- [project-lock.json (Initial State)](#project-lockjson-initial-state)
- [STATE.md (Initial)](#statemd-initial)
- [Empty File Headers](#empty-file-headers)
- [AGENTS.md Active Projects Block](#agentsmd-active-projects-block)
- [Placeholder Reference](#placeholder-reference)

---

## PROJECT.md Template

The team rulebook. This is the single most important generated file — every agent
reads it. Fill in every placeholder, expand every conditional. If a section
doesn't apply (e.g. `{{#if visual_assets_enabled}}` is false), omit the entire
section rather than leaving an empty heading.

```markdown
# Project: {{project_display_name}}

**Project ID:** {{project_id}}
**Type:** {{team_type}}
**Purpose:** {{project_purpose}}

---

## The Team

{{#each participants}}
- **{{role}} ({{agentId}})** — {{role_description}}
{{/each}}
{{#if operator}}
- **Operator (Human, alias: {{operator}})** — Final authority. Sign-off, unresolvable escalations, client engagement when agents can't reach the client.
{{/if}}

---

## Source of Truth

| What | Where |
|---|---|
| Task ownership and status | {{task_manager_type}} |
| Accepted scope | `workspace/SPEC-CURRENT.md` |
| How to produce deliverables | `workspace/DELIVERABLES_GUIDE.md` |
| Cross-agent knowledge | `SHARED_MEMORY.md` |
| Decision history | `DECISIONS.md` |
| Accepted limitations | `KNOWN_ISSUES.md` |
| Project conventions | `RUNBOOK.md` |
| Current phase and ownership | `project-lock.json` |
| Human-readable status | `STATE.md` |

---

## Stages ({{task_manager_type}} Columns)

| Stage | Meaning | Owner |
|---|---|---|
{{#each stages}}
| {{name}} | {{purpose}} | {{owner}} |
{{/each}}

---

## Shared Working Medium

**Type:** {{shared_medium_type}}
**Location:** {{shared_medium_location}}

{{shared_medium_conventions}}

---

{{#if visual_assets_enabled}}
## Visual / Media Assets

When a task involves visual or media reference material:

- **Primary storage:** {{task_manager_type}} task attachments (retrieved via the installed {{task_manager_type}} skill)
- **Fallback storage:** `./workspace/{{media_folder_name}}/`
- **Naming convention:** `{{visual_naming_convention}}`
- **Task description must reference the asset filename** so executors and QA can locate it

**Vision-required roles:** {{vision_required_roles_list}}

These roles should use a vision-capable model when working with tasks that reference visual assets. If the asset cannot be retrieved from either source, treat it as a blocker and escalate per normal escalation rules.

---
{{/if}}

## Workflow

### Phase 1: Intake

**Owner:** {{client_facing_role}}
**Lock phase:** `intake`

1. {{client_facing_role}} receives or drafts {{intake_term}} from the client.
2. {{client_facing_role}} writes a draft to `workspace/SPEC-v[N]-[YYYY-MM-DD].md` (new version, never overwrite). Updates `SPEC-CURRENT.md`.
3. {{client_facing_role}} posts to `queues/to-{{feasibility_reviewer_role}}-feasibility.md`: "New scope draft ready for feasibility review."
4. {{feasibility_reviewer_role}} reviews for {{feasibility_concerns}}. Posts numbered issues back.
5. {{client_facing_role}} translates issues to client-friendly language. Sends to client via email skill or `to-{{operator}}.md` for relay.
6. Client responds to each numbered issue: Accept / Provide solution / Descope.
7. {{client_facing_role}} logs response in `DECISIONS.md` verbatim with date.
8. Loop until all issues resolved. {{feasibility_reviewer_role}} marks `SPEC-CURRENT.md` ACCEPTED.
9. `project-lock.json` → phase: `planning`.

**Client no-response rule:** No response in {{client_no_response_hours}}h → client-facing follows up. Still no response → posts to `to-{{operator}}.md`. Task moves to Blocked.

### Phase 2: Planning

**Owner:** {{feasibility_reviewer_role}}
**Lock phase:** `planning`

1. {{feasibility_reviewer_role}} writes `workspace/DELIVERABLES_GUIDE.md`. Each numbered section = one task.
2. Updates `KNOWN_ISSUES.md` with limitations accepted during intake.
3. Posts to `to-{{client_facing_role}}.md`: "Deliverables guide ready."
4. {{client_facing_role}} creates tasks in {{task_manager_type}} from guide, assigns to roles, places in {{first_stage_name}}.
5. `project-lock.json` → phase: `execution`, sprint_id set.

### Phase 3: Execution

**Owner:** Executors (per assigned task)
**Escalation owner:** {{feasibility_reviewer_role}}

1. Executor picks up task → moves to "In Progress" stage.
2. Reads DELIVERABLES_GUIDE.md, RUNBOOK.md, their queue.
{{#if visual_assets_enabled}}
3. If task references a visual asset and executor's role requires vision: switch to vision-capable model, retrieve asset.
{{/if}}
4. Produces deliverable in shared medium ({{shared_medium_type}}).
5. When complete: {{completion_action}}, move task to "In Review" stage, post to `to-{{qa_role}}.md`.

**Hard stop rule (universal):** If executor escalates same issue {{stuck_re_escalations_threshold}}x to reviewer OR is stuck {{stuck_hours_threshold}}h, executor stops. Posts full summary to `to-{{client_facing_role}}.md`. {{client_facing_role}} posts to `to-{{operator}}.md`. Task moves to Blocked. **No further AI cycles spent until operator resolves.**

### Phase 4: Review

**Owner:** {{qa_role}}

1. {{qa_role}} picks up task from "In Review" stage.
2. Reads KNOWN_ISSUES.md, SPEC-CURRENT.md, DELIVERABLES_GUIDE.md.
{{#if visual_assets_enabled}}
3. If deliverable includes visual output and task references a mockup: use vision to compare output to reference.
{{/if}}
4. Reviews against all references.

**Pass:** Move task to "Completed". Post to `to-{{operator}}.md` with deliverable pointer.
**Fail:** Post specific failures to `to-{{feasibility_reviewer_role}}.md`. Move task back to "In Progress".

{{#if operator}}
### Phase 5: {{operator}} Sign-off

1. {{operator}} reviews `to-{{operator}}.md`.
2. {{operator}} validates the deliverable (pulls/reviews/tests as appropriate for medium).
3. If satisfied: {{operator}} approves delivery via {{delivery_action}}.
4. `project-lock.json` → `phase: close`.
{{/if}}

### Phase 6: Close

**Owner:** {{client_facing_role}}

1. Verify all sprint tasks are "Completed" in {{task_manager_type}}.
2. Archive completed tasks.
3. Verify DECISIONS.md and KNOWN_ISSUES.md are current.
4. Write sprint summary to SHARED_MEMORY.md.
5. Update STATE.md: "Sprint [N] closed. Ready for next intake."
6. Archive queue entries (mark READ, do not delete).
7. `project-lock.json` → `phase: idle`.
8. Post to `to-{{operator}}.md`: "Sprint closed."

{{#if sprint_mode_one_at_a_time}}
**One sprint at a time:** {{client_facing_role}} does not accept new intake until project-lock.json is `idle`.
{{else}}
**Continuous flow:** {{client_facing_role}} can accept new intake at any time.
{{/if}}

---

## Escalation Rules

| Situation | Action | Threshold |
|---|---|---|
| Client not responding | {{client_facing_role}} follows up; then to operator | {{client_no_response_hours}}h |
| Executor stuck on task | Escalate to {{feasibility_reviewer_role}} | Immediately |
| Same issue re-escalated {{stuck_re_escalations_threshold}}x | Hard stop; client-facing → operator | {{stuck_re_escalations_threshold}} escalations |
| Executor stuck {{stuck_hours_threshold}}h | Hard stop; client-facing → operator | {{stuck_hours_threshold}}h |
| Task in Blocked with no movement | Client-facing → operator | {{blocked_task_operator_escalation_hours}}h |

**No agent continues spending AI cycles on a blocked path.**

---

## Communication Protocol

All inter-agent communication uses queue files in `queues/`.

**Format:**

    [YYYY-MM-DD HH:MM] [FROM: agent-id] [TO: agent-id] [TASK: task-id or N/A]
    Message body. Be specific.
    ---

- Queues are append-only. Never delete entries.
- Mark processed entries with `[READ]` — do not remove the line.
- Archive at sprint close.
- Each agent checks their queue at session start, before any other action.
- `to-{{feasibility_reviewer_role}}-feasibility.md` is used **only during intake phase**.

---

## Reference Block for Each Agent's AGENTS.md

Every participating agent's workspace AGENTS.md must include the block defined
in [AGENTS.md Active Projects Block](#agentsmd-active-projects-block) below.

{{#each user_specific_notes}}
---

## {{section_title}}

{{section_body}}
{{/each}}
```

---

## project.json Template

Machine-readable project config. Substitute every placeholder, then validate the
result is valid JSON before writing to disk.

```json
{
  "id": "{{project_id}}",
  "name": "{{project_display_name}}",
  "purpose": "{{project_purpose}}",
  "team_type": "{{team_type}}",
  "task_manager": {
    "type": "{{task_manager_type}}",
    "project_id": "{{task_manager_project_id}}",
    "columns": {
      "{{stage_key_1}}": { "id": "{{stage_id_1}}", "purpose": "{{stage_purpose_1}}" },
      "{{stage_key_2}}": { "id": "{{stage_id_2}}", "purpose": "{{stage_purpose_2}}" },
      "{{stage_key_3}}": { "id": "{{stage_id_3}}", "purpose": "{{stage_purpose_3}}" },
      "{{stage_key_4}}": { "id": "{{stage_id_4}}", "purpose": "{{stage_purpose_4}}" },
      "{{stage_key_5}}": { "id": "{{stage_id_5}}", "purpose": "{{stage_purpose_5}}" },
      "blocked": { "id": "{{blocked_stage_id}}", "purpose": "Work waiting on external resolution. Client-facing agent owns escalation." }
    }
  },
  "participants": [
    {
      "agentId": "{{participant_agent_id}}",
      "workspace": "{{participant_workspace_path}}",
      "role": "{{participant_role_display}}",
      "role_key": "{{participant_role_key}}"
    }
  ],
  "client_facing_role": "{{client_facing_role_key}}",
  "feasibility_reviewer_role": "{{feasibility_reviewer_role_key}}",
  "qa_role": "{{qa_role_key}}",
  "operator": "{{operator_alias_or_null}}",
  "shared_workspace": "./workspace",
  "shared_medium": {
    "type": "{{shared_medium_type}}",
    "path_or_url": "{{shared_medium_location}}",
    "convention_notes": "{{shared_medium_conventions}}"
  },
  "spec_path": "./workspace/SPEC-CURRENT.md",
  "deliverables_guide_path": "./workspace/DELIVERABLES_GUIDE.md",
  "shared_memory": "./SHARED_MEMORY.md",
  "decisions_log": "./DECISIONS.md",
  "known_issues": "./KNOWN_ISSUES.md",
  "runbook": "./RUNBOOK.md",
  "queues": {
    "{{client_facing_role_key}}": "./queues/to-{{client_facing_role_key}}.md",
    "{{feasibility_reviewer_role_key}}": "./queues/to-{{feasibility_reviewer_role_key}}.md",
    "{{feasibility_reviewer_role_key}}_feasibility": "./queues/to-{{feasibility_reviewer_role_key}}-feasibility.md",
    "{{qa_role_key}}": "./queues/to-{{qa_role_key}}.md",
    "operator": "./queues/to-{{operator_alias_or_null}}.md"
  },
  "visual_assets": {
    "enabled": false,
    "primary_storage": "task_manager_attachments",
    "fallback_storage": "./workspace/{{media_folder_name}}",
    "naming_convention": "[task-id]-[short-description].[ext]",
    "vision_required_roles": []
  },
  "escalation_rules": {
    "client_no_response_hours": 48,
    "stuck_re_escalations_threshold": 2,
    "stuck_hours_threshold": 24,
    "blocked_task_operator_escalation_hours": 48
  },
  "sprint_mode": "one_at_a_time"
}
```

If `visual_assets.enabled` is set to `true`, populate `vision_required_roles` with
the role keys that need vision capability. Set `fallback_storage` to the actual
media folder path the skill creates in `workspace/`.

If there is no operator, set `"operator": null` (without quotes) and **omit the
`"operator"` key from the `queues` block entirely** rather than leaving it
pointing at a queue file that won't exist.

---

## project-lock.json (Initial State)

Initialize fresh on every project creation:

```json
{
  "phase": "idle",
  "sprint_id": null,
  "sprint_opened": null,
  "waiting_on": null,
  "last_updated": "{{today_iso_date}}",
  "last_updated_by": "operator",
  "context": "Project initialized. Ready to receive first work.",
  "blocked_tasks": []
}
```

---

## STATE.md (Initial)

Initialize fresh on every project creation:

```markdown
# {{project_display_name}} — Current State
**Phase:** Idle — Ready for first work
**Last updated:** {{today_iso_date}} by operator
```

---

## Empty File Headers

Use these for the files that start empty but need a header so agents know what
they are.

### SHARED_MEMORY.md

```markdown
# {{project_display_name}} — Shared Memory

Cross-agent knowledge that needs to persist across sessions but doesn't belong
in the task manager. Append entries with date and author.

Format for new entries:

    ## [YYYY-MM-DD] [agent-id] — [topic]
    Content here.
    ---
```

### DECISIONS.md

```markdown
# {{project_display_name}} — Decision Log

Append-only record of every significant decision made during intake or scope
negotiation. Never edit existing entries. Written by {{client_facing_role}}.

Format for new entries:

    ## [YYYY-MM-DD] — [Sprint ID]: [Decision Topic]

    **Issue surfaced by [feasibility reviewer]:** ...

    **Client response (received [date]):** ...

    **Resolution:** Accept as known outcome / Client-proposed alternative / Descoped

    **Accepted by:** [Client name], [feasibility reviewer agent], [client-facing agent]
    **Logged by:** [client-facing agent]
    ---
```

### KNOWN_ISSUES.md

```markdown
# {{project_display_name}} — Known Issues

Accepted limitations and trade-offs. QA reads this before reviewing — do not
file failures against items here. Written by {{feasibility_reviewer_role}}.

Format for new entries:

    ## [Sprint ID] — [Issue Title]
    - **Accepted:** [date]
    - **Context:** [why this limitation exists]
    - **Impact:** [what users/clients/operators will experience]
    ---
```

### RUNBOOK.md (stub)

```markdown
# {{project_display_name}} — Runbook

This is a starting stub. The {{feasibility_reviewer_role}} should expand each
section as they learn the project. All agents read this before starting work.

## Local Setup / Access

How to access the shared working medium ({{shared_medium_type}}).

## Conventions

How this team formats work, names things, and structures deliverables.

## Definition of Done

What counts as complete on this project.

## Known Gotchas

Pitfalls specific to this project — things that have tripped up agents before.

{{#each team_type_specific_sections}}
## {{section_title}}

{{section_body_or_placeholder}}
{{/each}}
```

### Queue Files

Initialize each queue file with:

```markdown
# Queue: to-{{role_key}}

Format for entries:

    [YYYY-MM-DD HH:MM] [FROM: agent-id] [TO: agent-id] [TASK: task-id or N/A]
    Message body. Be specific.
    ---

Append-only. Never delete entries. Mark processed entries with [READ] prepended.
Archive at sprint close (mark READ, leave in place).
```

---

## AGENTS.md Active Projects Block

Insert (or append) this block in each participating agent's workspace AGENTS.md.
If the agent is already on other projects, append — never overwrite.

```markdown
## Active Projects

- **{{project_display_name}}** — I am the {{my_role}} on this project.
  - Full rules: ~/.openclaw/projects/{{project_id}}/PROJECT.md
  - My queue: ~/.openclaw/projects/{{project_id}}/queues/to-{{my_role_key}}.md
  - Shared workspace: ~/.openclaw/projects/{{project_id}}/workspace/
  - Check my queue at the start of every session before doing anything else.
  - Check ~/.openclaw/projects/{{project_id}}/project-lock.json to know what
    phase we are in before acting.
```

---

## Placeholder Reference

Every placeholder used across the templates above. Source column tells you
where the value comes from.

| Placeholder | Source |
|---|---|
| `{{project_id}}` | Pass 1 #3 |
| `{{project_display_name}}` | Pass 1 #3 |
| `{{project_purpose}}` | Pass 1 #1 |
| `{{team_type}}` | Pass 1 #2 |
| `{{participants}}` (list) | Pass 1 #4 — each entry has `agentId`, `role`, `role_key`, `role_description`, `workspace` |
| `{{operator}}` | Pass 1 #8 (alias) or null |
| `{{client_facing_role}}` | Pass 1 #5 (display name) |
| `{{client_facing_role_key}}` | Pass 1 #5 (slug form) |
| `{{feasibility_reviewer_role}}` | Pass 1 #6 (display name) |
| `{{feasibility_reviewer_role_key}}` | Pass 1 #6 (slug) |
| `{{qa_role}}` | Pass 1 #7 (display name) |
| `{{qa_role_key}}` | Pass 1 #7 (slug) |
| `{{task_manager_type}}` | Pass 2 #1 — `asana` or `clickup` |
| `{{task_manager_project_id}}` | From Step 6 (after board creation) |
| `{{stages}}` (list) | Pass 2 #2 — each has `name`, `key`, `id`, `purpose`, `owner` |
| `{{first_stage_name}}` | Pass 2 #2 (first column) |
| `{{shared_medium_type}}` | Pass 2 #3 — `git`, `folder`, `external_system`, or `none` |
| `{{shared_medium_location}}` | Pass 2 #3 |
| `{{shared_medium_conventions}}` | Inferred in Step 4, user-confirmed |
| `{{visual_assets_enabled}}` | Pass 2 #7 (boolean) |
| `{{media_folder_name}}` | Inferred from team type — e.g. `mockups`, `photos`, `media` |
| `{{visual_naming_convention}}` | Default: `[task-id]-[short-description].[ext]` |
| `{{vision_required_roles_list}}` | Inferred in Step 4 from team type |
| `{{intake_term}}` | Per team type — e.g. "requirements", "brief", "lead" |
| `{{feasibility_concerns}}` | Per team type — see team-archetypes.md |
| `{{completion_action}}` | Per team type — e.g. "push to sprint branch and update PR" |
| `{{delivery_action}}` | Per team type — e.g. "merge to main", "send to client", "publish to MLS" |
| `{{sprint_mode_one_at_a_time}}` | Pass 2 #5 (boolean) |
| `{{client_no_response_hours}}` | Pass 2 #6 (default 48) |
| `{{stuck_hours_threshold}}` | Pass 2 #6 (default 24) |
| `{{stuck_re_escalations_threshold}}` | Pass 2 #6 (default 2) |
| `{{blocked_task_operator_escalation_hours}}` | Default 48 |
| `{{user_specific_notes}}` | Pass 2 #8 (free-form additions) |
| `{{today_iso_date}}` | Today's date in YYYY-MM-DD |
| `{{my_role}}` / `{{my_role_key}}` | Per-agent when generating their AGENTS.md block |
