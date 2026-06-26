# openclaw-eval-skill 🔬

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Evaluation framework for any OpenClaw skill. Tests description trigger accuracy, output quality (with vs without skill), model performance comparison, and latency profiling.

**No `claude` CLI dependency** — all agent execution runs through `sessions_spawn` + `sessions_history`.

---

## How It Works (Two-Layer Architecture)

```
Layer 1: Agent (main OpenClaw session)
  ├─ Reads evals.json
  ├─ sessions_spawn → subagents        ← agent does this directly
  ├─ sessions_history → extract data   ← agent does this directly
  └─ Writes raw data to workspace/

Layer 2: Python scripts (run via exec)
  ├─ Read JSON/txt from workspace/     ← pure data processing
  ├─ Compute statistics
  └─ Generate reports
```

> **Critical**: Python scripts cannot call `sessions_spawn` themselves. The agent in the main session drives the entire workflow. See `USAGE.md`.

---

## Quick Start (5 minutes)

```bash
# 1. Clone and register
git clone https://github.com/jarosik9/skill-eval.git
# Add parent directory to skills.load.extraDirs in openclaw.json

# 2. Ask your OpenClaw agent
evaluate weather trigger

# 3. Check output
cat eval-workspace/weather/iter-1/trigger_results.json
```

If `trigger_results.json` shows pass/fail per eval, you're ready.

---

## Three Evaluation Modes

| Mode | What It Tests | Key Output |
|------|--------------|------------|
| **Trigger Rate** | Does the `description` cause the agent to read SKILL.md at the right times? | `trigger_results.json` |
| **Quality Compare** | Does the skill improve output quality vs no-skill baseline? | `quality_results.json` |
| **Model Comparison** | How does quality + speed vary across `haiku` / `sonnet` / `opus`? | `model_comparison_report.md` |

---

## Running an Evaluation

All evaluation is **agent-driven**. Ask your OpenClaw agent:

```
Evaluate the <skill-name> skill. Use:
  evals: evals/<skill>/quality.json
  skill path: /path/to/SKILL.md
  output: eval-workspace/<skill>/iter-1/
Follow the Quality Compare workflow in USAGE.md.
```

The agent will:
1. Spawn subagents (with skill / without skill)
2. Collect session histories
3. Run analysis scripts via `exec`
4. Produce a graded report

---

## Directory Structure

```
openclaw-eval-skill/
├── SKILL.md          ← Full execution guide (read this first)
├── README.md         ← This file
├── USAGE.md          ← Step-by-step agent-driven workflows
├── CHANGELOG.md      ← Version history
├── LICENSE
│
├── agents/
│   ├── grader.md     ← Assertion checker + behavior anomaly tracker
│   ├── comparator.md ← Blind A/B judge (no assertion bias)
│   └── analyzer.md   ← Cross-eval pattern analysis
│
├── evals/
│   ├── weather/                ← Ready-to-run weather skill evals
│   │   ├── quality.json
│   │   └── triggers.json
│   └── fake-tool/              ← Test skill for trigger validation
│
├── templates/
│   └── cli-wrapper/            ← Eval templates for CLI tool skills (more coming)
│
├── scripts/
│   ├── analyze_triggers.py     ← Trigger detection from session histories
│   ├── analyze_quality.py      ← Quality scoring from transcripts
│   ├── analyze_model_compare.py← Model comparison matrix
│   ├── analyze_latency.py      ← Latency p50/p90 from timing files
│   ├── aggregate_benchmark.py  ← Summarize all gradings
│   ├── resolve_paths.py        ← Auto-detect skill/eval paths
│   └── legacy/                 ← v1 scripts (reference only)
│
├── viewer/
│   ├── generate_review.py      ← Generate HTML review from grading JSON
│   └── viewer.html             ← Interactive eval result viewer
│
├── tests/                      ← Unit tests (pytest)
│
└── docs/
    └── ARCHITECTURE.md         ← Three-dimension eval framework
```

---

## evals.json Schema

**Quality Compare** (`prompt` + `assertions`):
```json
{
  "skill_name": "my-skill",
  "evals": [
    {
      "id": 1,
      "name": "onboarding-fresh",
      "prompt": "Check the weather in Tokyo",
      "context": "Clean machine, no prior setup. Context for grader only.",
      "expected_output": "Install → configure → verify profile",
      "assertions": [
        { "id": "a1-1", "description": "Install command executed",
          "type": "output_contains", "value": "pip install" },
        { "id": "a1-2", "description": "Profile verified",
          "type": "output_contains", "value": "profile current", "priority": true }
      ]
    }
  ]
}
```

**Trigger Rate** (`query` + `expected`):
```json
{
  "skill_name": "my-skill",
  "evals": [
    { "id": 1, "name": "direct-trigger",
      "query": "What's the weather in Singapore?",
      "expected": true, "category": "positive" },
    { "id": 2, "name": "no-trigger",
      "query": "What is 2 + 2?",
      "expected": false, "category": "negative" }
  ]
}
```

See `SKILL.md` for the full list of assertion types.

---

## Issue Priority (grader output)

```
🔴 P0 Critical  — Core functionality completely broken
🟠 P1 High      — Significantly impacts usability
🟡 P2 Medium    — Room for improvement but acceptable
🟢 P3 Low       — Minor polish
```

---

## Key Constraints

- `sandbox="inherit"` — subagents must inherit the skill registration environment
- `cleanup="keep"` — history must be retained for trigger detection
- Skill must be in a real directory under `skills.load.extraDirs` (symlinks rejected by security check)

## Trigger Rate Limitation

**Trigger detection works best for skills the model doesn't already know.**

| Skill Type | Example | Reads SKILL.md? | Why |
|------------|---------|-----------------|-----|
| Model-unknown | custom internal tools, fake-tool | ✅ Yes | Must read guide to know how |
| Model-known | weather (wttr.in), gh (GitHub CLI) | ❌ Often skips | Uses training knowledge directly |

For well-known tools like `weather` or `gh`, the model may complete the task correctly **without** reading SKILL.md — it already knows how to use `curl wttr.in` or `gh pr list` from training data.

**Recommendation**: Use trigger rate testing primarily for custom/internal skills where the model has no prior knowledge. For model-known skills, use Quality Compare instead to measure whether your skill improves output quality.

**Future improvement**: We plan to add detection for "used skill capability" (not just "read SKILL.md") to cover model-known skills. See [issue tracking](https://github.com/jarosik9/skill-eval/issues).

---

## Documentation

| File | Purpose |
|------|---------|
| `SKILL.md` | Full execution guide — eval formats, assertion types, mode details |
| `USAGE.md` | Agent-driven workflows for all 4 eval modes |
| `CHANGELOG.md` | Version history |
| `docs/ARCHITECTURE.md` | Three-dimension framework design |

---

## Result Viewer

After running evals, generate an interactive HTML report:

```bash
python viewer/generate_review.py eval-workspace/<skill>/iter-1/ --skill-name <skill>
# Opens a local HTTP server. Visit http://localhost:8080 to browse results.
```

The viewer shows per-eval grading, behavior anomalies, and assertion pass/fail breakdown.

---

---

## Roadmap

### v1.1 (Next)
- [ ] Screenshot/GIF of trigger_results.json output
- [ ] Additional eval templates (API integration, conversational skills)
- [ ] Capability-based trigger detection for model-known skills

### v1.2 (Planned)
- [ ] **Cross-skill Conflict Detection** — detect when two skill descriptions overlap and may compete for the same queries
- [ ] **Error Recovery Testing** — measure how well agents recover when skill commands fail

---

## License

MIT — see [LICENSE](LICENSE).
