# Marketing Operator — Core Logic

## Role

The Marketing Operator is the **execution engine** of the Marketing OS. It translates strategy into action, manages tasks, and generates performance feedback.

---

## Workflow (Step-by-Step)

### Step 1: Receive Mission Brief

**Input:** `schemas/cmo_to_operator.schema.json`

**Validation:**
1. Verify all required fields are present: `mission_id`, `objective`, `strategy`, `priority`, `actions[]`
2. If `target_audience` is missing → request clarification from CMO
3. If `priority` is `critical` → bypass normal queue, execute immediately

---

### Step 2: Task Decomposition

**Prompt Used:** `prompts/operator-planning.txt`

**Processing Logic:**
1. Break each `action` from the mission brief into atomic tasks
2. For each task, define:
   - `task_id` — Unique identifier (format: `TASK-{mission_id}-{seq}`)
   - `title` — Clear, action-oriented title
   - `description` — What exactly needs to be done
   - `priority` — Inherited from mission or adjusted based on dependencies
   - `owner` — Who/what executes (agent / human / api)
   - `deadline` — Calculated from mission urgency and task complexity
   - `status` — Initial: `pending`
   - `expected_result` — What success looks like (measurable)
   - `dependencies[]` — Other task_ids that must complete first
   - `estimated_effort` — time estimate

3. Validate no circular dependencies exist
4. Order tasks topologically by dependency chain

**Output:** Array conforming to `schemas/operator_task.schema.json`

---

### Step 3: Resource Allocation

**Processing Logic:**
1. Map each task to required resources:
   - Budget allocation (if applicable)
   - Channel access requirements
   - Tool/API requirements (→ check `adapters/`)
   - Content requirements
2. Flag resource conflicts or shortages
3. If budget exceeds available → reprioritize tasks, drop `low` priority items first

---

### Step 4: Campaign Assembly

**Processing Logic:**
1. Group related tasks into a campaign record
2. Define campaign metadata:
   - `campaign_id` — Unique identifier
   - `name` — Descriptive campaign name
   - `mission_id` — Links back to CMO mission
   - `status` — `planning` → `active` → `completed` / `paused` / `failed`
   - `start_date` / `end_date`
   - `tasks[]` — References to task_ids
   - `budget_allocated` / `budget_spent`
   - `target_metrics` — KPIs from CMO strategy
3. Write to `memory/campaigns.json`

**Output:** `schemas/campaign.schema.json`

---

### Step 5: Execution Tracking

**Prompt Used:** `prompts/operator-execution.txt`

**Processing Logic:**
1. For each active task:
   - Check status: `pending` → `in_progress` → `completed` / `blocked` / `failed`
   - If `blocked` → identify blocker, escalate if deadline at risk
   - If `failed` → log failure reason, assess retry viability
   - If `completed` → capture result metrics
2. Update campaign status based on task completion rate
3. Log every state change to `logs/execution.log.json`

---

### Step 6: Metrics Collection

**Processing Logic:**
1. For each completed task, collect:
   - Quantitative metrics (impressions, clicks, conversions, revenue)
   - Qualitative metrics (engagement quality, brand sentiment)
   - Cost metrics (CPM, CPC, CPA, ROAS)
2. Aggregate at campaign level
3. Compare actual vs. target_metrics from campaign definition

---

### Step 7: Generate Feedback

**Output Schema:** `schemas/feedback.schema.json`

Generate feedback for CMO containing:
- `execution_result` — Summary of what happened
- `metrics` — Actual performance data
- `learnings[]` — What worked, what didn't, why
- `issues[]` — Problems encountered with severity
- `recommendations[]` — Suggested strategic adjustments
- `confidence_in_data` — How reliable the metrics are

---

### Step 8: Update Memory

Write to:
- `memory/campaigns.json` — Updated campaign record
- `memory/learnings.json` — New patterns and insights

---

## Decision Rules

| Condition | Action |
|---|---|
| Mission priority = `critical` | Execute immediately, skip queue |
| Task blocked > 24h | Escalate to human review |
| Campaign metrics < 50% of target at midpoint | Trigger strategy review with CMO |
| Budget exhausted before completion | Pause remaining tasks, notify CMO |
| Task fails 3 times | Mark as `failed`, remove from active queue, log root cause |
| All tasks complete | Transition campaign to `completed`, generate final feedback |

---

## Interaction with Virtual CMO

- Operator **receives** mission briefs via `cmo_to_operator.schema.json`
- Operator **sends** feedback via `feedback.schema.json`
- Operator **never** modifies strategy — only proposes adjustments via feedback
- Operator **escalates** to CMO when metrics deviate > 30% from targets

---

## Error Handling

- If `operator_mission` is malformed → Return error with specific missing/invalid fields
- If no tasks can be generated → Return `"status": "cannot_decompose"` with reason
- If adapter is unavailable → Mark dependent tasks as `blocked`, continue with independent tasks
- If execution log write fails → Buffer in memory, retry on next cycle
