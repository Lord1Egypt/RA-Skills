# OpenClaw Workflow Patterns

Use these patterns as starting templates. Adapt them instead of designing from scratch every time.

## 1. Precise reminder

**Use when:** the user wants an exact-time reminder.

**Primitive:** `cron` with `sessionTarget="main"` and `payload.kind="systemEvent"`

**Template:**
- Trigger: one-shot or recurring schedule
- Payload text: natural-language reminder with context
- Delivery: none beyond main-session injection unless a specific target is required

**Rule:** mention enough context that the reminder still makes sense hours later.

## 2. Scheduled report

**Use when:** the user wants a daily/weekly brief, watchlist, or summary.

**Primitive:** `cron` isolated `agentTurn`

**Template:**
1. schedule at exact time
2. fetch source data
3. summarize into a stable output format
4. announce to the right channel

**Good for:** market reports, topic digests, morning briefings, AI news summaries.

## 3. Monitor and alert

**Use when:** the user cares about important changes, not every raw event.

**Primitive:** `cron` or `HEARTBEAT.md` depending on timing strictness

**Template:**
1. fetch candidate items
2. deduplicate against state
3. score importance
4. alert only on threshold
5. store the rest for digest or later review

**State ideas:** URL hash set, symbol+timestamp key, article ID ledger.

## 4. Multi-agent content pipeline

**Use when:** collection and production require different minds.

**Primitive:** `cron` or manual trigger + spawned sessions

**Template:**
1. research-oriented agent gathers raw material
2. save shortlist to file
3. writing-oriented agent turns shortlist into publishable draft
4. optional final human review

**Rule:** use a file handoff so stages are inspectable.

## 5. Knowledge ingest pipeline

**Use when:** the user wants URLs, files, or documents captured into a local knowledge base.

**Primitive:** script or MCP + optional scheduled wrapper

**Template:**
1. detect or receive source
2. extract readable content
3. normalize metadata
4. chunk and index
5. optionally create a short note or summary

**Rule:** make ingest idempotent; re-running the same source should not create garbage.

## 6. Maintenance sweep

**Use when:** the system needs periodic cleanup, audits, or memory distillation.

**Primitive:** `HEARTBEAT.md`

**Template:**
1. cheap gate checks whether work is due
2. if not due, stay silent
3. if due, inspect recent artifacts
4. distill or clean up
5. update state marker

**Good for:** memory review, stale-job cleanup, document compaction, backlog pruning.

## 7. External adapter pattern

**Use when:** a SaaS connector is required but the thinking should stay local.

**Primitive:** OpenClaw as brain, Zapier/Make/n8n as adapter

**Template:**
1. OpenClaw decides what should happen
2. external tool handles the app-specific connector or webhook
3. OpenClaw receives or logs the result

**Rule:** keep decision logic, scoring, and summarization out of the visual workflow when possible.

## 8. Human approval checkpoint

**Use when:** the workflow ends in a risky external action.

**Primitive:** any execution plane + explicit confirmation step

**Template:**
1. prepare draft output
2. show user exactly what will be sent or changed
3. wait for approval
4. execute only after confirmation

**Good for:** emails, public posts, payments, destructive operations, config changes.

## Compression Heuristic

If a workflow feels complicated, compress it into this sentence:

**"On [trigger], use [execution plane] to turn [input] into [artifact], then [deliver/action], while storing [state] and handling failures by [fallback]."**

If you cannot write that sentence clearly, the architecture is still muddy.
