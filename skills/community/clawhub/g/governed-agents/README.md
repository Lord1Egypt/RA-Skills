# governed-agents

**Deterministic verification + reputation scoring for AI sub-agents.**

Prevents hallucinated success ("I did it!") by verifying claims independently before updating the agent's score. Extends from code tasks to open-ended tasks (research, strategy, writing) via a 3-layer verification pipeline.

---

## Runtime Dependencies

- codex: spawns the Codex CLI for governed sub-agent execution.
- openclaw: spawns OpenClaw agent sessions for non-code or fallback execution.
- git: initializes temporary repos for Codex task runs.
- pytest: executes verification test suites.
- ruff: optional lint gate (fast Python linter).
- flake8: optional lint gate (legacy Python linter).
- pylint: optional lint gate (deep static analysis).

## The Problem

AI agents hallucinate success. They say "Done!" when files are missing, tests fail, or the output is empty. Without independent verification, a reputation system just rewards confident lying.

**For coding tasks:** Tests either pass or fail. Binary signal. Easy.  
**For open-ended tasks:** No ground truth. An agent can produce fluent, confident, completely wrong output. Harder — and exactly why @almai85 proposed the 3-layer architecture below.

---

## Architecture

```
Task Completion
     │
     ▼
verification_mode?
     │
     ├─ "deterministic" ──► Gates 1–4 (Files, Tests, Lint, AST)
     │                       Binary pass/fail for coding tasks
     │
     └─ "council" ──► task_type?
                           │
                           ▼
                    ┌─────────────────┐
                    │ LAYER 1         │ < 1s, deterministic
                    │ Structural Gate │ format, word count,
                    │                 │ required sections
                    └────────┬────────┘
                    FAIL ◄───┘ PASS
                    (no Council)  │
                                  ▼
                    ┌─────────────────┐
                    │ LAYER 2         │ 5–30s, semi-deterministic
                    │ Grounding Gate  │ URL reachability,
                    │                 │ source/citation checks
                    └────────┬────────┘
                    FAIL ◄───┘ PASS
                    (no Council)  │
                                  ▼
                    ┌─────────────────┐
                    │ LAYER 3         │ 30–120s, probabilistic
                    │ LLM Council     │ N independent reviewers
                    │                 │ majority vote → score
                    └─────────────────┘
```

**Short-circuit principle** (credit: @almai85): if Layer 1 fails, Layer 3 is never invoked — zero LLM calls, instant result, bounded cost.

### Formal Model

**Reputation update (EMA):**
```
R(t+1) = (1 − α) · R(t) + α · s(t),   α = 0.3
```

**Score function:**
```
        ⎧ +1.0  if verification passed (first try)
        ⎪ +0.7  if verification passed (after retry)
s(t) =  ⎪ +0.5  if honest blocker report
        ⎪  0.0  if failed but tried
        ⎩ −1.0  if hallucinated success (verification failed)
```

**Gate composition (deterministic mode):**
```
V = Gate_Files ∧ Gate_Tests ∧ Gate_Lint ∧ Gate_AST
```

**3-Layer composition (council mode):**
```
V(task) = Gate_Structural(task) ∧ Gate_Grounding(task) ∧ Council_Score(task) ≥ θ
```

**Supervision thresholds:**
```
R > 0.8  →  autonomous   (full trust)
R > 0.6  →  standard     (normal supervision)
R > 0.4  →  supervised   (checkpoints, progress reports)
R > 0.2  →  strict       (model override to Opus)
R ≤ 0.2  →  suspended    (task blocked)
```

---

## Gates 1–4: Deterministic Verification (Coding Tasks)

| Gate | Check | Signal |
|------|-------|--------|
| **Files** | Required files exist and are non-empty | Hard fail |
| **Tests** | `run_tests` command exits 0 | Hard fail |
| **Lint** | No lint errors (graceful skip if tool missing) | Hard fail |
| **AST** | Python files parse without SyntaxError | Hard fail |

If an agent claims SUCCESS but any gate fails → score override to `-1.0` (hallucination penalty).

---

## Gate 5: LLM Council (Open-ended Tasks)

For tasks without deterministic verification — research, analysis, strategy, writing, planning.

```python
contract = TaskContract(
    objective="Design the rate limiting strategy",
    acceptance_criteria=[
        "Sliding window algorithm documented",
        "Redis vs in-memory trade-offs explained",
        "Failure mode (circuit breaker) addressed",
    ],
    verification_mode="council",
    council_size=3,               # number of independent reviewers
    task_type="analysis",         # activates Layer 1 + 2 automatically
)

g = GovernedOrchestrator(contract, model="openai/gpt-5.2-codex")

# After worker completes:
prompts = g.generate_council_tasks(worker_output)

# Spawn each reviewer (main agent does this via sessions_spawn)
# Each reviewer returns structured JSON:
# {"verdict": "approve", "confidence": 0.9, "strengths": [...], "weaknesses": [...]}

result = g.record_council_verdict(raw_reviewer_outputs)
print(result.summary)
# → "Council: 2/3 approved (score=0.67, PASS ✅)"
# → "Weaknesses: no per-user limits; missing burst handling"
```

**Strict majority:** 50/50 split = FAIL (not pass).  
**Parse failure:** pessimistic — malformed reviewer output = reject.  
**Security note:** reviewer model should be ≥ task model to prevent prompt injection escalation from the reviewed output.

---

## Layer 1: Structural Gate

Deterministic checks, runs in < 1 second. No external calls.

| Check | What it verifies |
|-------|-----------------|
| `word_count` | Output ≥ `min_word_count` words |
| `required_sections` | All specified headers appear in output |
| `no_empty_sections` | No section < 10 chars |
| `sources_list` | At least one URL or reference pattern present |
| `has_steps` | Numbered list present (for planning tasks) |

---

## Layer 2: Grounding Gate

Semi-deterministic checks, 5–30 seconds. stdlib only, no external dependencies.

| Check | What it verifies |
|-------|-----------------|
| `url_reachable` | All URLs in output respond with 2xx/3xx (HEAD, timeout 3s, max 5) |
| `citations_present` | Citation patterns found: `Author et al.`, `[1]`, `(Smith 2024)` |
| `numbers_consistent` | Same number not used with conflicting units (warn only) |
| `cross_refs_resolve` | "see section X" references → section X exists in output |
| `dates_valid` | No dates > 10y past or > 5y future (warn only) |

Warnings don't fail the gate — only hard failures trigger short-circuit.

---

## Task-Type Profiles

Pre-configured gate combinations per task category:

| `task_type` | Layer 1 checks | Layer 2 checks | Min words |
|-------------|---------------|----------------|-----------|
| `research` | word_count, sources_list, no_empty_sections | url_reachable, citations_present | 200 |
| `analysis` | word_count, required_sections, no_empty_sections | numbers_consistent | 150 |
| `strategy` | required_sections, no_empty_sections, word_count | cross_refs_resolve | 100 |
| `writing` | word_count, no_empty_sections | — | 50 |
| `planning` | required_sections, has_steps, no_empty_sections | dates_valid | 50 |
| `custom` | (none — configure manually) | (none) | 0 |

---

## Hallucination Taxonomy (by task type)

Credit: @almai85

| Task type | Failure mode | Example |
|-----------|-------------|---------|
| Research | Fabricated sources | "According to Smith et al. (2024)..." — paper doesn't exist |
| Research | Inaccurate extraction | Real paper, wrong conclusions attributed |
| Analysis | Unfounded claims | "Market will grow 40%" — no data backing |
| Strategy | Circular reasoning | Plan that sounds good but collapses under scrutiny |
| Writing | Embedded factual errors | Confident, grammatically perfect, wrong |
| Planning | Missing dependencies | Timeline that ignores critical prerequisites |

---

## Reputation System

```python
from governed_agents.reputation import get_agent_stats

stats = get_agent_stats()
for agent in stats:
    print(f"{agent['agent_id']}: {agent['reputation']:.3f} ({agent['supervision']['level']})")

# → openai-gpt-5_2-codex: 0.823 (autonomous)
# → anthropic-claude-haiku-4-5: 0.608 (standard)
```

Scores persist in SQLite (`.state/governed_agents/reputation.db`).

---

## Comparison with Other Frameworks

| Framework | Post-task verification | Persistent reputation | Non-coding gates | Council mode |
|-----------|----------------------|----------------------|-----------------|--------------|
| **governed-agents** | ✅ Deterministic gates 1–4 + 3-layer pipeline | ✅ EMA per model | ✅ Structural + Grounding | ✅ LLM Council |
| CrewAI | ❌ `expected_output` is text description, not verified | ❌ | ❌ | ❌ |
| LangGraph | ❌ Orchestration only, no post-task verification | ❌ | ❌ | ❌ |
| AutoGen | ⚠️ `CodeExecutorAgent` runs LLM-generated code¹ | ❌ | ❌ | ❌ |
| LlamaIndex | ❌ LLM self-reports completion | ❌ | ❌ | ❌ |

¹ AutoGen's `CodeExecutorAgent` executes code produced by the LLM — it is not a post-task verification mechanism for arbitrary task output.

---

## Quick Start

```python
from governed_agents.contract import TaskContract
from governed_agents.orchestrator import GovernedOrchestrator

# Coding task (deterministic gates)
contract = TaskContract(
    objective="Add JWT auth endpoint",
    acceptance_criteria=["POST /api/auth returns JWT", "Tests pass"],
    required_files=["api/auth.py", "tests/test_auth.py"],
    run_tests="pytest tests/test_auth.py -v",
)
g = GovernedOrchestrator(contract, model="openai/gpt-5.2-codex")
# Pass g.spawn_task() to sessions_spawn, then:
result = g.record_success()  # verifies gates, updates reputation

# Open-ended task (3-layer pipeline)
contract2 = TaskContract(
    objective="Write architecture decision record for auth module",
    acceptance_criteria=["Trade-offs documented", "Decision stated"],
    verification_mode="council",
    task_type="analysis",
    council_size=3,
)
g2 = GovernedOrchestrator(contract2, model="openai/gpt-5.2-codex")
prompts = g2.generate_council_tasks(worker_output)
result2 = g2.record_council_verdict(raw_reviewer_outputs)
```

---

## Tests

```bash
python3 -m pytest governed_agents/test_verification.py \
                   governed_agents/test_council.py \
                   governed_agents/test_profiles.py -v
# 37 passed
```

Covers: files/tests/lint/AST gates, score override on hallucination, honest blocker scoring, LLM Council majority vote, parse failure pessimism, structural gate checks, grounding gate checks, 3-layer pipeline short-circuit.

---

## Acknowledgments

- **[@almai85](https://github.com/almai85)** — LLM Council design and the 3-layer verification architecture (Structural → Grounding → Council), cost-bounding short-circuit principle, and hallucination taxonomy per task type
- **DrNeuron** — code reviews (9 rounds), threshold fix (50/50 = FAIL), confidence clamping, type validation hardening

---

## License

MIT
