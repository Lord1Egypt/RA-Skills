# Layered Memory Audit Checklist

Use this checklist when evaluating an existing memory setup.

## Step 1: Inventory the current memory surfaces
List where memory currently lives:
- hot memory / profile / system prompt notes
- project notes
- daily logs
- summaries / dashboards / state files
- long-term docs
- databases / vector stores / knowledge bases

Question:
- Is memory spread across surfaces with no clear boundary rules?

## Step 2: Classify each memory surface
For each surface, decide whether it is mostly:
- hot canon
- durable doctrine
- project-scoped working memory
- episodic history
- generated live summary
- mixed / unclear

Question:
- Which surfaces are doing multiple jobs badly?

## Step 3: Look for mixed-authority problems
Flag cases where one memory surface mixes:
- durable truth + temporary status
- doctrine + raw logs
- project notes + global canon
- old snapshots + current truth

Question:
- Where could stale operational state be mistaken for durable memory?

## Step 4: Check the hot path
Inspect the most frequently loaded memory.

Question:
- Is it genuinely hot and cross-cutting?
- Or is it overloaded with detail, logs, counters, or stale history?

Good sign:
- short, curated, high-value memory only

Bad sign:
- giant summary blob pretending to be hot memory

## Step 5: Check retrieval order
Ask how the system retrieves memory for a task.

Good pattern:
1. hot canon
2. index/selector
3. relevant doctrine
4. project memory if needed
5. generated summaries for live-state questions
6. raw logs only for verification

Bad pattern:
- search everything at once
- no authority separation
- raw history competes equally with canon

## Step 6: Check promotion / demotion rules
Ask:
- How does fresh information become durable memory?
- How does stale detail cool off?
- Is anything ever deduped, rewritten, or demoted?

Good sign:
- explicit promotion and cleanup rules

Bad sign:
- append-only forever

## Step 7: Check project isolation
Ask:
- Can one project dump irrelevant detail into global memory?
- Is project-specific working memory kept separate from cross-project doctrine?

Good sign:
- project memory has a defined boundary

Bad sign:
- everything is stored in one giant global memory layer

## Step 8: Check live-state handling
Ask:
- Are dashboards, alerts, or health summaries treated as durable truth?
- Are generated summaries clearly marked as derived state?

Good sign:
- live summaries exist, but remain rebuildable and non-canonical

Bad sign:
- transient system state fossilized into long-term memory

## Step 9: Score the system
Use these dimensions:
- architecture quality
- retrieval clarity
- truthfulness about live state
- token efficiency
- long-term maintainability
- project scoping
- operator trust

## Step 10: Recommend the smallest useful next step
Prefer one or two concrete fixes:
- split hot canon from deep memory
- create a project memory layer
- demote generated status into summaries
- add an index/selector
- add promotion/demotion rules
- dedupe the hot layer

## Output format
When reporting the audit, include:
- current memory surfaces
- main boundary failures
- top 3 risks
- smallest useful architecture changes
- whether the system is blob-memory, partially layered, or properly layered
