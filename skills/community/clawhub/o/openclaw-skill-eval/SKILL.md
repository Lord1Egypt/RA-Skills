---
name: skill-eval
description: "Skill evaluation framework. Use when: testing trigger rate, quality compare (with/without skill), or model comparison. Runs via sessions_spawn + sessions_history. Trigger words: evaluate skill, benchmark, trigger rate, A/B compare. NOT for: debugging conversations, general testing unrelated to skill evaluation."
metadata: { "openclaw": { "emoji": "🔬" } }
---

# openclaw-eval-skill

Evaluation framework for any OpenClaw skill. No claude CLI dependency — all agent execution runs through `sessions_spawn` + `sessions_history`.

**Scope**: Works with CLI tool skills, conversational skills, and API integration skills.

---

## Runtime Actions Disclosure

This skill performs the following actions during evaluation:

| Action | Purpose | When |
|--------|---------|------|
| Read `~/.openclaw/openclaw.json` | Find skill directories (extraDirs) | Path resolution |
| Write to `eval-workspace/` | Store evaluation results | Every eval run |
| Call `sessions_spawn` | Run test queries in isolated sessions | Trigger & quality tests |
| Call `sessions_history` | Collect conversation data for analysis | After each spawn |
| Persist `cleanup="keep"` sessions | Required for trigger detection | Trigger rate tests |

**NOT performed automatically**: Gateway restart, config modification, skill installation. These require manual user action (see "Bundled Test Skill" section).

---

## Quick Eval

Just say:
```
evaluate weather
```

The agent will:
1. Run `scripts/resolve_paths.py weather` to find all paths
2. Execute trigger rate + quality compare with detected evals
3. Output results to `eval-workspace/weather/iter-N/`

**Options**:
- `evaluate weather trigger` — trigger rate only
- `evaluate weather quality` — quality compare only
- `evaluate github --mode all` — explicit mode

**What gets auto-detected**:
- Skill path: from OpenClaw built-in skills or registered extraDirs
- Evals: from `evals/{skill-name}/` or fallback to `evals/example-*.json`
- Output: next available `iter-N` directory

**First step for agent**: Run the resolver to get paths:
```bash
python scripts/resolve_paths.py {skill-name} --mode {trigger|quality|all}
```

Use the JSON output to fill in paths for the workflows below.

---

## Bundled Test Skill: fake-tool

A test skill (`test-skills/fake-tool/`) is included for validating trigger rate detection. It simulates a fictional "Zephyr API" that models cannot know from training.

**Manual setup required**: The agent will NOT automatically install fake-tool or restart your gateway. If you want to test with fake-tool:

1. **Copy fake-tool** to your skills directory:
   ```bash
   cp -r test-skills/fake-tool ~/.openclaw/workspace/skills/
   ```

2. **Restart OpenClaw gateway** (from terminal):
   ```bash
   openclaw gateway restart
   ```

3. **Verify registration**:
   ```bash
   python scripts/resolve_paths.py fake-tool
   ```

If step 3 returns a valid path, fake-tool is ready. If "not found", check that your `~/.openclaw/openclaw.json` includes the skills directory in `skills.load.extraDirs`.

---

## Evaluation Scenarios

### Tier 1: Core (Always Run)

| Scenario | What It Tests | Output |
|----------|---------------|--------|
| **Trigger Rate** | Does description trigger SKILL.md reads at the right times? Includes positive (should trigger) AND negative (should NOT trigger) cases. | recall, specificity, precision, F1 |
| **Quality Compare** | Does skill improve output vs no-skill baseline? | quality_score, assertion pass rate |
| **Description Diagnosis** | Why did triggers fail? Analyzes both false negatives AND false positives. | gap analysis, recommendations |

### Tier 2: Optional (Run When Needed)

| Scenario | What It Tests | When to Use |
|----------|---------------|-------------|
| **Model Comparison** | Quality + speed across haiku/sonnet/opus | Before deployment: which model is enough? |
| **Efficiency Profile** | Response time + retry patterns | When skill feels slow: is agent walking wrong paths? |

### Tier 3: Future (Roadmap)

| Scenario | What It Tests | Status |
|----------|---------------|--------|
| **Cross-skill Conflict** | Two skills with overlapping descriptions | Planned |
| **Error Recovery** | Does agent recover when CLI fails? | Planned |

---

## How This Skill Works

**Two-layer architecture**:

```
Layer 1: Agent (main OpenClaw session) — YOU ARE HERE
  → Reads evals.json
  → Calls sessions_spawn to run subagents
  → Calls sessions_history to collect results
  → Writes raw data to workspace/

Layer 2: Python analysis scripts (run via exec)
  → Read the raw data from workspace/
  → Compute statistics
  → Generate reports
```

Python scripts (`analyze_*.py`) are data processors — they cannot call `sessions_spawn`. The agent drives the workflow.

---

## Usage

**Follow `USAGE.md` for all workflows.**

Quick reference:

| Workflow | What It Tests | USAGE.md Section |
|----------|---------------|------------------|
| Trigger Rate | Does `description` trigger SKILL.md reads at the right times? | Workflow 1 |
| Quality Compare | Does skill improve output vs no-skill baseline? | Workflow 2 |
| Model Comparison | Quality + Speed across haiku/sonnet/opus | Workflow 3 |
| Latency Profile | Response time p50/p90 | Workflow 4 |

Each workflow follows the same pattern:
1. Agent spawns subagents using `sessions_spawn`
2. Agent collects histories using `sessions_history`
3. Agent writes raw data to `workspace/{skill}/iter-{n}/raw/`
4. Agent runs analysis script via `exec`

---

## Core Principles

1. **Never modify the evaluated skill** — observe only, give recommendations
2. **Keep eval records in workspace** — output goes to `eval-workspace/<skill-name>/iteration-N/`
3. **Keep full records** — save `full_history.json` (including tool_use + tool_result)

---

## agents/ Reference

| File | Purpose | When to Use |
|------|---------|-------------|
| `grader.md` | Check assertions, record behavior anomalies, give priority recommendations | Required for every Quality Compare eval |
| `comparator.md` | Blind A/B comparison without assertions | When unbiased comparison is needed |
| `analyzer.md` | Analyze cross-eval patterns after all evals complete | Post-analysis |

---

## Directory Structure

```
eval-workspace/<skill-name>/
├── evals.json                    ← Eval definition (shared across iterations)
└── iteration-1/
    ├── raw/
    │   ├── histories/            ← Trigger test session histories
    │   └── transcripts/          ← Quality compare transcripts
    ├── trigger_results.json      ← analyze_triggers output
    ├── quality_results.json      ← analyze_quality output
    └── diagnostics/
        └── RECOMMENDATIONS.md
```

---

## evals.json Format

**Quality Compare** (prompt + assertions):
```json
{
  "skill_name": "my-skill",
  "evals": [
    {
      "id": 1,
      "name": "onboarding-fresh",
      "prompt": "Check the weather in Tokyo",
      "context": "Clean machine, no prior setup. For grader only.",
      "expected_output": "Install → configure → verify profile",
      "assertions": [
        {
          "id": "a1-1",
          "description": "Install command executed",
          "type": "output_contains",
          "value": "pip install"
        },
        {
          "id": "a1-2",
          "description": "Profile verified after setup",
          "type": "output_contains",
          "value": "profile current",
          "priority": true
        }
      ]
    }
  ]
}
```

**Trigger Rate** (query + expected):
```json
{
  "id": 1,
  "name": "direct-weather",
  "query": "What's the weather in Singapore?",
  "expected": true,
  "category": "positive"
}
```

---

## Assertion Types

| Type | Detection |
|------|-----------|
| `output_contains` | Value appears in conversation or tool output |
| `output_not_contains` | Value does not appear |
| `output_count_max` | Occurrences ≤ max |
| `tool_called` | Specific tool called at least once |
| `tool_not_called` | Specific tool not called |
| `conversation_contains` | Value appears anywhere in conversation |
| `conversation_contains_any` | At least one value appears |

**Priority assertions** (`"priority": true`): any failure → overall=FAIL.
**Gap assertions** (`"note": "Best practice..."`): failure = skill design gap.

---

## Issue Priority (grader output)

```
🔴 P0 Critical  — Core functionality broken
🟠 P1 High      — Significantly impacts usability
🟡 P2 Medium    — Room for improvement
🟢 P3 Low       — Minor polish
```

---

## Behavior Anomaly Tracking

Grader records these signals beyond assertions:

| Field | Trigger |
|-------|---------|
| `path_corrections` | Wrong path then self-corrected |
| `retry_count` | Same command executed multiple times |
| `missing_file_reads` | Attempted to read non-existent files |
| `skipped_steps` | Steps required by skill were not executed |
| `hallucinations` | Fabricated non-existent commands/APIs |

---

## Key Constraints

- **`sandbox="inherit"`** — subagents inherit skill registration environment
- **`cleanup="keep"`** — history must be retained for trigger detection
- Skill must be in a real directory under `skills.load.extraDirs` (symlinks rejected)
