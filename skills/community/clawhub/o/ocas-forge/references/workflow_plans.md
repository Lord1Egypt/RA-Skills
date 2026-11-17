# OCAS Workflow Plans

Spec Version: 1.1.3
Author: Indigo Karasu

Changes from 1.0: added Expected Bundled Plans section; added plan init registration pattern; added notes on graceful skill-absent handling in plan runs.

---

## Purpose

Workflow Plans are reusable, parameterized task sequences that Mentor executes by name. A plan encodes a complete multi-skill workflow -- the ordered steps, what each step receives from prior steps, and how to handle failures -- so the same workflow can be triggered repeatedly without reconstructing the task graph from scratch each time.

Plans are distinct from ad-hoc Mentor projects. A project is created on-the-fly in response to a goal. A plan is pre-authored and invokable by name with typed parameters. Plans may be bundled with skills (as part of the skill package) or created by the user independently.

---

## General Rules

- Plans are Markdown files with YAML frontmatter, stored at `{agent_root}/commons/data/ocas-mentor/plans/`.
- Skills that ship bundled plans include them at `references/plans/` in the skill package. Mentor copies bundled plans during initialization -- skipping any plan file already present to preserve user modifications.
- Plans are discovered by scanning `{agent_root}/commons/data/ocas-mentor/plans/` for `*.plan.md` files.
- Parameters are declared in frontmatter and passed at invocation time via `--arg name=value`.
- Steps reference prior step outputs via `{{steps.step_id.output_name}}`.
- Parameters are referenced via `{{params.param_name}}`.
- Every plan run is tracked in `{agent_root}/commons/data/ocas-mentor/plan-runs/{plan_run_id}/`.
- Plans must not hardcode user-specific values. Use parameters for anything that varies between invocations.
- Plan files are authoritative. Editing a plan file changes behavior for all future runs. In-progress runs use the state snapshot in their `state.json` -- they are not affected by edits.

---

## Storage Layout

```
{agent_root}/commons/data/ocas-mentor/
  plans/
    {plan_id}.plan.md          -- plan definitions (bundled or user-created)
  plan-runs/
    {plan_run_id}/
      state.json               -- run params, step status, step outputs, overall status
      decisions.jsonl          -- per-step DecisionRecord entries
```

Plan IDs are globally unique across all plans in the directory. Filename must match `plan_id` exactly.

---

## Plan File Format

Plans are Markdown files with YAML frontmatter. The filename must be `{plan_id}.plan.md`.

### Frontmatter

```yaml
---
plan_id: example-plan
name: Human-Readable Plan Name
version: 1.0.0
description: One sentence. What this plan does and when to run it.
parameters:
  param_name:
    type: string | number | boolean | contact_id
    required: true | false
    default: value          # only when required: false
    description: What this parameter controls.
steps:
  - id: step-one
    name: Step One Name
    skill: ocas-weave
    command: weave.query
    on_failure: abort | skip | retry
  - id: step-two
    name: Step Two Name
    skill: gog
    command: gmail-scan
    on_failure: abort
---
```

The `steps` list in frontmatter is an ordered index for machine parsing. All step details live in the markdown body.

### Body Structure

The body defines each step in full. Use this structure for every step:

```markdown
## Step N: step-id

**Skill:** {skill-name}
**Command:** {command-name}

**Inputs:**
- `field_name`: literal value, `{{params.x}}`, or `{{steps.prior-step-id.output_name}}`

**Outputs:**
- `output_name`: description -- what is stored from this step's result for use by later steps

**Identity heuristics** (required for Scout and Sift steps):
- Require: name + at least one of (email | location | employer | phone)
- Common name guard: require name + two secondary facts before accepting a result

**On failure:** abort | skip | retry
**Notes:** Additional execution guidance specific to this step.
```

---

## Parameter Types

| Type | Description | Notes |
|---|---|---|
| `string` | Free text | Quoted at invocation if it contains spaces |
| `number` | Numeric value (integer or float) | Parsed from string at invocation |
| `boolean` | `true` or `false` | |
| `contact_id` | A Weave `person_id` | If omitted or set to `"random"`, Mentor queries Weave for a random Person node |

---

## Variable Interpolation

Within step input definitions, use double-brace syntax:

| Syntax | Resolves to |
|---|---|
| `{{params.name}}` | The parameter value at invocation time |
| `{{steps.step_id.output_name}}` | The named output from a completed prior step |
| `{{plan_run_id}}` | The unique ID of the current plan run |
| `{{now}}` | Current ISO 8601 timestamp |

A variable referencing an output from a skipped step resolves to `null`. Steps that receive a `null` on a required input must skip themselves and log the reason to `decisions.jsonl`. Steps that receive `null` on an optional input proceed with the missing value absent.

---

## Plan Run Tracking

### state.json

Written at run start, updated atomically after each step completes or fails.

```json
{
  "plan_run_id": "pr_{hash}",
  "plan_id": "string",
  "plan_version": "string",
  "invoked_by": "string -- manual | cron:{job-name} | heartbeat",
  "params": { "param_name": "resolved_value" },
  "status": "string -- running | paused | complete | failed",
  "current_step": "string -- step_id of current or most recent step",
  "steps": {
    "{step_id}": {
      "status": "string -- pending | running | complete | skipped | failed",
      "started_at": "string | null",
      "completed_at": "string | null",
      "outputs": "object | null",
      "error": "string | null"
    }
  },
  "started_at": "string -- ISO 8601",
  "completed_at": "string | null"
}
```

Write `state.json` atomically: write to `state.json.tmp`, then rename to `state.json`.

### decisions.jsonl

Append-only DecisionRecord log. Write one record for each: step start, step completion, step skip, step failure, plan completion, plan failure.

---

## Invocation

### Manual

```
mentor.plan.run {plan_id}
mentor.plan.run {plan_id} --arg param_name=value --arg param_name2=value2
```

Arguments are key=value pairs. String values containing spaces should be quoted in the shell. If a required parameter is omitted, Mentor prompts for it before starting. If an optional parameter is omitted, its declared `default` is used.

### Cron

```
openclaw cron add --name {job-name} \
  --schedule "0 2 * * *" \
  --command "mentor.plan.run {plan_id} --arg param_name=value" \
  --sessionTarget isolated --lightContext true --wakeMode next-heartbeat \
  --timezone America/Los_Angeles
```

### Cron

All background tasks use cron. Hermes has no heartbeat mechanism.

### Resuming a Failed or Paused Run

```
mentor.plan.resume {plan_run_id}
```

Mentor reads `state.json`, skips all steps with `status: complete`, and continues from the first non-complete step. Parameters from the original invocation are preserved in `state.json` -- they are not re-read from the command line on resume.

---

## Error Handling

| `on_failure` | Behavior |
|---|---|
| `abort` | Stop the plan run immediately. Mark run status `failed`. Log error to `decisions.jsonl`. |
| `skip` | Mark step `skipped`. Pass `null` outputs to dependent steps. Continue to next step. |
| `retry` | Retry the step once with identical inputs. If it fails again, behave as `abort`. |

If a step's skill is not available, treat it as a step failure and apply `on_failure` behavior.

---

## Commands

Mentor exposes these commands for plan management:

- `mentor.plan.list` -- list all plans in `{agent_root}/commons/data/ocas-mentor/plans/` with plan_id, version, and description
- `mentor.plan.run {plan_id} [--arg name=value ...]` -- execute a named plan
- `mentor.plan.status {plan_run_id}` -- show current state of a running or recent plan run
- `mentor.plan.resume {plan_run_id}` -- continue a paused or failed run from the first incomplete step
- `mentor.plan.history [--plan plan_id] [--limit N]` -- list recent plan run summaries ordered by start time

---

## Adding New Plans

1. Write a `{plan_id}.plan.md` file following the format above.
2. Place it in `{agent_root}/commons/data/ocas-mentor/plans/` for user-created plans, or in a skill's `references/plans/` for bundled plans.
3. If bundled with a skill, add a row to that skill's Support file map referencing the plan.
4. Mentor discovers new files at next `mentor.plan.list` or `mentor.plan.run` invocation.

Do not hardcode user-specific values in plan files. Use parameters for all variable inputs.

---

## Expected Bundled Plans

The following skills are expected to ship bundled plans. Plans are copied to `{agent_root}/commons/data/ocas-mentor/plans/` during `mentor.init`. Existing files are never overwritten (user modifications are preserved).

| Skill | Plan ID | Description |
|---|---|---|
| ocas-scout | `contact-enrichment` | Research a contact by name/email, enrich via Weave, emit entities |
| ocas-sift | `research-deep-dive` | Multi-source research on a topic: broad scan → depth pass → entity extraction |
| ocas-rally | `portfolio-rebalance` | Signal refresh → scoring → allocation review → optional trade plan |
| ocas-voyage | `trip-planning` | Destination research → itinerary construction → accommodation options |
| ocas-taste | `preference-scan` | Ingest recent browsing and media activity → update preference model |

### Plan Init Registration

Skills that bundle plans must add a copy step to their `{skill}.init` command:

```
Copy all *.plan.md files from {skill}/references/plans/ to {agent_root}/commons/data/ocas-mentor/plans/
Skip any file that already exists at the destination (preserve user modifications)
Log each copy operation as a DecisionRecord
```

### Absent Skill Handling

If a plan step references a skill that is not installed:
- Treat it as a step failure.
- Apply the step's `on_failure` policy (`abort`, `skip`, or `retry`).
- Do not silently succeed.
- Log the missing skill name and step ID to `decisions.jsonl`.