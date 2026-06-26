# Mentor: Workflow Plans

Read this file before executing `mentor.plan.list`, `mentor.plan.run`, `mentor.plan.status`, `mentor.plan.resume`, or `mentor.plan.history`.

See `spec-ocas-workflow-plans.md` for the canonical plan file format specification.

---

## What Plans Are

Plans are pre-authored, parameterized task sequences stored at `~/openclaw/data/ocas-mentor/plans/*.plan.md`. Each plan defines an ordered set of steps, the skill and command each step invokes, what inputs each step receives, and what outputs it produces for downstream steps.

Use `mentor.plan.run` when a user invokes a known workflow by name or via cron/heartbeat automation. Use `mentor.project.create` for open-ended goals that require on-the-fly task decomposition.

---

## Executing a Plan

### 1. Load and validate the plan

Read the plan file at `~/openclaw/data/ocas-mentor/plans/{plan_id}.plan.md`.

Validate:
- All required parameters are present (from `--arg` flags or user prompt)
- All step IDs are unique
- All `{{steps.x.y}}` references point to steps that appear earlier in the sequence

If validation fails, abort before starting. Report which parameter or reference is invalid.

### 2. Initialize the plan run

Generate `plan_run_id` using the format `pr_{hash}`.

Create directory `~/openclaw/data/ocas-mentor/plan-runs/{plan_run_id}/`.

Write initial `state.json` with:
- All step statuses set to `pending`
- `status: running`
- `current_step`: first step ID
- `params`: all resolved parameter values (defaults applied for omitted optional params)
- `invoked_by`: `manual`, `cron:{job-name}`, or `heartbeat` based on context

### 3. Execute each step in order

For each step in the frontmatter `steps` array:

**a. Resolve inputs** -- expand all `{{params.x}}` and `{{steps.y.z}}` variables using the current `state.json`. If a variable resolves to `null` and the input is required, skip this step (if `on_failure: skip`) or abort (if `on_failure: abort` or `retry`).

**b. Invoke the skill** -- execute the step's skill and command with the resolved inputs. Follow the step's Notes for any special handling (identity heuristics, extraction patterns, write-back behavior).

**c. Capture outputs** -- extract the named outputs defined in the step's Outputs block from the skill's response. Store them in `state.json` under `steps.{step_id}.outputs`.

**d. Update state** -- write updated `state.json` atomically after each step. Mark the step `complete`, `skipped`, or `failed`. Append a DecisionRecord to `decisions.jsonl`.

**e. Apply on_failure if needed** -- if the step failed, apply `on_failure` behavior per the spec:
- `abort`: mark run `failed`, stop, log
- `skip`: mark step `skipped`, continue
- `retry`: retry once, then abort if still failing

### 4. Complete the plan run

After the final step, update `state.json`:
- `status`: `complete` (or `failed` if the run was aborted)
- `completed_at`: current timestamp

Write a final DecisionRecord summarizing the run outcome.

Write a journal entry via `mentor.journal` covering the plan run.

---

## Resuming a Failed Run

When `mentor.plan.resume {plan_run_id}` is invoked:

1. Read `state.json` from `~/openclaw/data/ocas-mentor/plan-runs/{plan_run_id}/`.
2. Identify the first step with status `pending` or `failed`.
3. Resume execution from that step using the original `params` from `state.json`.
4. Do not re-run steps with status `complete`.

---

## Argument Passing

Parameters come from three sources, in priority order (highest first):
1. `--arg name=value` flags at invocation time
2. `default` values declared in the plan frontmatter
3. Interactive prompt (for required params with no `--arg` supplied, manual invocations only)

For cron and heartbeat invocations, required parameters with no `--arg` and no `default` cause the run to abort immediately with a logged error.

### Type coercion

- `number`: parse the string value as float. Abort if not numeric.
- `boolean`: accept `true` or `false` (case-insensitive). Abort if other value.
- `contact_id`: pass as-is. If the value is `"random"` or the parameter is omitted with `required: false`, Mentor queries Weave for a random Person node: `MATCH (p:Person) RETURN p ORDER BY rand() LIMIT 1`.

---

## Available Plans

Plans in `~/openclaw/data/ocas-mentor/plans/` (discovered at runtime):

Use `mentor.plan.list` to see all available plans with their current version and description.

Bundled plans shipped with Mentor:

| Plan ID | Description |
|---|---|
| `contact-enrichment` | Enriches a Weave contact by scanning Gmail, running Scout OSINT, and Sift web search |

---

## Writing New Plans

See `references/plans/template.plan.md` for a blank template with all fields documented.

Follow `spec-ocas-workflow-plans.md` for the complete format specification and error handling rules.
