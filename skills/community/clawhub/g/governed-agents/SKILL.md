---
name: governed-agents
description: "Deterministic verification + reputation scoring for AI sub-agents. Prevents hallucinated success via 4 code gates (files, tests, lint, AST) and a 3-layer pipeline (Structural → Grounding → LLM Council) for open-ended tasks."
source: https://github.com/Nefas11/governed-agents
homepage: https://github.com/Nefas11/governed-agents
install: {"kind": "script", "script": "install.sh"}
filesystem_writes: ["~/.openclaw/workspace/.state/governed_agents/"]
capabilities: ["persistent_db_writes", "external_cli_execution", "network_requests"]
network_access: true
env_vars:
  OPENCLAW_WORKSPACE: {"required": false, "description": "Workspace root directory (default: ~/.openclaw/workspace)"}
  GOVERNED_WORK_DIR: {"required": false, "description": "Temporary working directory (default: /tmp/governed)"}
  GOVERNED_DB_PATH: {"required": false, "description": "SQLite reputation database path"}
  GOVERNED_AUTH_TOKEN: {"required": false, "description": "Bearer token for HTTP API mode"}
metadata:
  {
    "openclaw":
      {
        "emoji": "🛡️",
        "type": "executable/with-install",
        "source": "https://github.com/Nefas11/governed-agents",
        "requires": { "bins": ["codex", "git", "pytest"] },
        "optional_bins": ["ruff", "flake8", "pylint"],
        "install":
          [
            {
              "id": "script",
              "kind": "script",
              "command": "bash install.sh",
              "label": "Install governed-agents (copy to workspace)",
            },
          ],
      },
  }
capability_flags:
  network-capable: true
  subprocess-capable: true
---

# Governed Agents

Deterministic verification + reputation scoring for AI sub-agents. Prevents hallucinated success ("I did it!") by verifying claims independently before updating the agent's score.

**Pure Python stdlib — zero external dependencies.**

## Capabilities

Spawns external CLIs (codex, openclaw, git, pytest) and makes HTTP HEAD requests.

## When to Use

Use this skill when you need to:

- **Spawn sub-agents** and verify their output automatically
- **Score agent reliability** across tasks (EMA-based reputation)
- **Detect hallucinated success** — agent claims "done" but files are missing or tests fail
- **Verify open-ended tasks** (research, analysis, strategy) via LLM Council
- **Enforce supervision levels** based on agent track record

## Quick Start

### Coding Tasks (Deterministic Verification)

```python
from governed_agents.contract import TaskContract
from governed_agents.orchestrator import GovernedOrchestrator

contract = TaskContract(
    objective="Add JWT auth endpoint",
    acceptance_criteria=["POST /api/auth returns JWT", "Tests pass"],
    required_files=["api/auth.py", "tests/test_auth.py"],
    run_tests="pytest tests/test_auth.py -v",
)

g = GovernedOrchestrator(contract, model="openai/gpt-5.2-codex")
# After agent completes:
result = g.record_success()  # runs gates, updates reputation
```

### Open-Ended Tasks (3-Layer Pipeline + LLM Council)

```python
contract = TaskContract(
    objective="Write architecture decision record for auth module",
    acceptance_criteria=["Trade-offs documented", "Decision stated"],
    verification_mode="council",
    task_type="analysis",
    council_size=3,
)

g = GovernedOrchestrator(contract, model="openai/gpt-5.2-codex")
prompts = g.generate_council_tasks(worker_output)
result = g.record_council_verdict(raw_reviewer_outputs)
# → "Council: 2/3 approved (score=0.67, PASS ✅)"
```

### CLI Spawning (Codex / OpenClaw)

```python
from governed_agents.openclaw_wrapper import spawn_governed

contract = TaskContract(
    objective="Build a REST API for todos",
    acceptance_criteria=["CRUD endpoints work", "Tests pass"],
    required_files=["api.py", "tests/test_api.py"],
)

# Uses Codex 5.3 CLI by default
result = spawn_governed(contract, engine="codex53")
# Or via OpenClaw agent CLI:
result = spawn_governed(contract, engine="openclaw")
```

## Verification Modes

### Deterministic (Coding Tasks)

4 gates run automatically — all must pass:

| Gate | Check | Signal |
|------|-------|--------|
| **Files** | Required files exist and are non-empty | Hard fail |
| **Tests** | Test command exits 0 | Hard fail |
| **Lint** | No lint errors | Hard fail |
| **AST** | Python files parse without SyntaxError | Hard fail |

If agent claims SUCCESS but any gate fails → score override to `-1.0` (hallucination penalty).

### Council (Open-Ended Tasks)

3-layer pipeline with short-circuit:

1. **Structural Gate** (<1s) — word count, required sections, no empty sections
2. **Grounding Gate** (5–30s) — URL reachability, citation checks
3. **LLM Council** (30–120s) — N independent reviewers, majority vote

If Layer 1 fails → no LLM calls, instant result, zero cost.

## Reputation System

```
R(t+1) = (1 − α) · R(t) + α · s(t),   α = 0.3
```

| Score | Meaning |
|-------|---------|
| +1.0 | Verified success (first try) |
| +0.7 | Verified success (after retry) |
| +0.5 | Honest blocker report |
|  0.0 | Failed but tried |
| −1.0 | Hallucinated success |

### Supervision Levels

| Reputation | Level | Effect |
|-----------|-------|--------|
| > 0.8 | autonomous | Full trust |
| > 0.6 | standard | Normal supervision |
| > 0.4 | supervised | Checkpoints required |
| > 0.2 | strict | Model override to Opus |
| ≤ 0.2 | suspended | Task blocked |

## Task-Type Profiles

Pre-configured gate combinations:

| `task_type` | Layer 1 | Layer 2 | Min words |
|-------------|---------|---------|-----------|
| `research` | word_count, sources_list | url_reachable, citations | 200 |
| `analysis` | word_count, required_sections | numbers_consistent | 150 |
| `strategy` | required_sections, word_count | cross_refs_resolve | 100 |
| `writing` | word_count | — | 50 |
| `planning` | required_sections, has_steps | dates_valid | 50 |

## Installation

```bash
bash install.sh
# → Copies governed_agents/ to $OPENCLAW_WORKSPACE/governed_agents/
# → Runs verification suite (37 tests)
```

## Tests

```bash
python3 -m pytest governed_agents/test_verification.py \
                   governed_agents/test_council.py \
                   governed_agents/test_profiles.py -v
# 37 passed
```
