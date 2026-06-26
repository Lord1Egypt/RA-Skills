# Usage Guide (Agent-Driven)

**Version**: v2 (2026-03-18)

**Core principle**: The agent handles all OpenClaw API calls (spawn/history). Python scripts handle pure data analysis only.

---

## Two-Layer Architecture

```
Layer 1: Agent (main session)
  ├─ Read evals.json
  ├─ sessions_spawn → subagents
  ├─ sessions_history → extract data
  └─ Write files to raw/ directory

Layer 2: Python scripts (run via exec)
  ├─ Read JSON/txt from raw/
  ├─ Compute statistics
  └─ Generate reports
```

---

## Workflow 1: Trigger Rate Test

### Step 1: Agent spawns subagents

For each eval query, spawn one subagent:

```
task = """
You are an OpenClaw assistant.
Decide whether to read the skill file at {skill_path} before answering.
If the query is relevant to the skill, read it and use it. Otherwise answer directly.

Query: {query}
"""

sessions_spawn(task=task, mode="run", cleanup="keep", label="trigger-eval-{id}")
```

Wait for all subagents to complete (receive announce signals).

### Step 2: Agent fetches history and writes files

```
For each session key, call:
sessions_history(sessionKey=sk, includeTools=True)

Write results to:
workspace/{skill}/iter-{n}/raw/histories/eval-{id}.json
Format: {"eval_id": 1, "query": "...", "expected": true, "messages": [...]}
```

### Step 3: Script analysis

```bash
python3 scripts/analyze_triggers.py \
    --evals evals/{skill}/triggers.json \
    --histories workspace/{skill}/iter-{n}/raw/histories/ \
    --output workspace/{skill}/iter-{n}/trigger_results.json
```

### Step 4 (optional): Diagnostics

```bash
python3 scripts/run_diagnostics.py \
    --evals evals/{skill}/triggers.json \
    --skill-path /path/to/SKILL.md \
    --trigger-results workspace/{skill}/iter-{n}/trigger_results.json \
    --output-dir workspace/{skill}/iter-{n}/diagnostics/
```

---

## Workflow 2: Quality Compare (with vs without skill)

### Step 1: Agent spawns two groups

For each eval, spawn two subagents:

```
# With skill
sessions_spawn(
    task=f"Read {skill_path}. Then: {prompt}",
    mode="run", cleanup="keep", label="q-eval-{id}-with"
)

# Without skill
sessions_spawn(
    task=prompt,
    mode="run", cleanup="keep", label="q-eval-{id}-without"
)
```

Wait for all to complete.

### Step 2: Agent extracts transcripts and writes files

```
sessions_history(sessionKey=sk_with, includeTools=False)
→ Extract the last assistant text message
→ Write to workspace/{skill}/iter-{n}/raw/transcripts/eval-{id}-with.txt

Repeat for without.
```

### Step 3: Script analysis

```bash
python3 scripts/analyze_quality.py \
    --evals evals/{skill}/quality.json \
    --transcripts workspace/{skill}/iter-{n}/raw/transcripts/ \
    --output workspace/{skill}/iter-{n}/quality_results.json
```

---

## Workflow 3: Model Comparison

### Step 1: Agent spawns (models × evals × N runs)

For each (model, eval, run):
```
sessions_spawn(
    task=f"Read {skill_path}. Then: {prompt}",
    model=full_model_name,  # e.g. "anthropic/claude-haiku-4-5"
    mode="run", cleanup="keep",
    label="mc-eval-{id}-{model}-run-{n}"
)

Record spawn time: start = time.now()
After receiving announce: elapsed = time.now() - start
```

### Step 2: Agent writes data files

```
Transcript:
workspace/{skill}/iter-{n}/raw/model-compare/eval-{id}-{model}-run-{n}-transcript.txt

Timing:
workspace/{skill}/iter-{n}/raw/model-compare/eval-{id}-{model}-run-{n}-timing.json
Format: {"eval_id": 1, "model": "haiku", "run": 1, "elapsed_seconds": 9.2}
```

### Step 3: Script analysis

```bash
python3 scripts/analyze_model_compare.py \
    --evals evals/{skill}/quality.json \
    --data-dir workspace/{skill}/iter-{n}/raw/model-compare/ \
    --models haiku,sonnet \
    --dimensions quality,speed \
    --output-dir workspace/{skill}/iter-{n}/model-compare/
```

---

## Workflow 4: Latency Profile

### Step 1: Agent spawns (same eval, N runs)

```
for run in range(1, n_runs+1):
    sessions_spawn(
        task=f"Read {skill_path}. Then: {prompt}",
        model=model,
        mode="run", cleanup="keep",
        label="lat-eval-{id}-{model}-run-{run}"
    )
    # Record elapsed time after announce
```

### Step 2: Agent writes timing files

```
workspace/{skill}/iter-{n}/raw/timings/eval-{id}-{model}-run-{r}.json
{"eval_id": 1, "model": "sonnet", "run": 1, "elapsed_seconds": 12.3}
```

### Step 3: Script analysis

```bash
python3 scripts/analyze_latency.py \
    --evals evals/{skill}/quality.json \
    --timings-dir workspace/{skill}/iter-{n}/raw/timings/ \
    --models haiku,sonnet \
    --output-dir workspace/{skill}/iter-{n}/latency/
```

---

## Directory Structure Convention

```
workspace/
└── {skill}/
    └── iter-{n}/
        ├── raw/
        │   ├── histories/              ← trigger test session histories
        │   │   └── eval-{id}.json
        │   ├── transcripts/            ← quality compare transcripts
        │   │   ├── eval-{id}-with.txt
        │   │   └── eval-{id}-without.txt
        │   ├── model-compare/          ← model comparison data
        │   │   ├── eval-{id}-{model}-run-{n}-transcript.txt
        │   │   └── eval-{id}-{model}-run-{n}-timing.json
        │   └── timings/                ← latency profile timings
        │       └── eval-{id}-{model}-run-{n}.json
        │
        ├── trigger_results.json        ← analyze_triggers output
        ├── quality_results.json        ← analyze_quality output
        ├── model-compare/              ← analyze_model_compare output
        │   ├── compare_matrix.json
        │   └── model_comparison_report.md
        ├── latency/                    ← analyze_latency output
        │   ├── latency_report.json
        │   └── latency_report.md
        └── diagnostics/                ← run_diagnostics output
            ├── diagnosis.json
            └── RECOMMENDATIONS.md
```

---

## Naming Conventions

| Variable | Example |
|----------|---------|
| `{skill}` | `weather`, `summarize`, `github` |
| `{n}` | `1`, `2`, `3` (increment each iteration) |
| `{id}` | eval's id field |
| `{model}` | `haiku`, `sonnet`, `opus` |
| `{r}` / `{run}` | starts from 1 |

---

## Important Notes

- **Each iteration gets its own folder**: `iter-1/`, `iter-2/`... never overwrite historical data
- **Spawn first, then wait**: agent spawns all subagents, waits for all announce signals, then batch-fetches histories
- **Timing starts at spawn**: record `start = time.now()` before calling `sessions_spawn`; record `elapsed` after receiving the announce signal
- **Transcript extraction**: take the last `role=assistant` text message from `sessions_history`
