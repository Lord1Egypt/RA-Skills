---
name: long-run-harness
description: >
  Use when building a Planner→Generator→Evaluator multi-agent harness or long-running
  orchestrator. Triggers: "build a harness", "multi-agent pipeline", "agent loop",
  "automate app building with agents", "GAN-style agent system", "sprint-based agent
  workflow", "I want agents to plan, build, and evaluate automatically".
  NOT for: asking Codex to build an app directly, single-file edits, pure API usage questions.
---

# Long-Running App Harness — SDK Implementation

Produces a runnable harness that orchestrates Claude SDK agents, with optional Codex CLI
or DeepSeek-backed `deepcode` SDK backends for selected roles.
**You are writing the harness, not running inside it.**

Use `query()` + `ClaudeAgentOptions` for agentic loops; `tool()` + `create_sdk_mcp_server()`
for structured output.

Default to SDK-only provider access. Direct provider clients are allowed only behind a small
adapter when the SDK does not expose a needed capability (for example, image/vision scoring);
put the adapter behind config and keep the rest of the harness SDK-based.

```
uv venv
uv pip install claude-agent-sdk pyyaml
```

Harness template structure:
```
harness/
  harness.py; config.yaml; config.py; log.py
  agents/ planner.py; generator.py; evaluator.py
  models/ state.py
  prompts/ planner.md; generator.md; evaluator.md
```

Run output structure:
```
project_dir/
  src/                         # ALL Generator-created app code lives here
  harness-state/
    spec.md                    # Planner output
    sprints.md                 # Human-readable sprint plan / scope
    contracts/ contract-sprint-N.json
    handoffs/ handoff-sprint-N.json
    evals/ eval-sprint-N-iter-M.json
    evidence/
      sprint-N/
        screenshots/
        axe/
        lighthouse/
        browser/
        artifacts/
    tmp/                       # disposable run files; cleaned by retention policy
  harness-logs/ run-YYYYMMDD-HHMMSS.log
```

**Clean workspace boundary:** Harness state, logs, screenshots, test output, browser traces,
Lighthouse reports, axe reports, temporary manifests, and evaluation artifacts stay under
`harness-state/` or `harness-logs/`. They do not go in `src/`, `public/`, root docs, or app
routes unless the sprint contract explicitly declares a public evidence surface and a cleanup
plan.

**Default hard boundary:** For greenfield app generation, Generator file tools and Codex cwd
point at `project_dir/src`, not `project_dir`.

**Existing-codebase exception:** For maintenance or production-hardening harnesses over an
existing repo, Generator may need repo-root cwd. In that case you MUST define write allowlists,
protected paths, artifact directories, and git safety rules before generation starts.
**Load:** `$SKILL_DIR/instructions/mode-selection.md`
**Load:** `$SKILL_DIR/instructions/workspace-hygiene.md`

---

## Routing

| User Signal | Route |
|---|---|
| "build a harness / pipeline" | Start at Phase 1 |
| "add an evaluator" | Jump to Phase 4 |
| "add state / handoff" | Jump to Phase 5 |
| "looping forever / broken" | Check feedback loop termination in Phase 5 |
| "just explain what a harness does" | Explain concept, don't write code |

---

## Phase 1: Design the Harness

**Load:** `$SKILL_DIR/instructions/planner-questions.md`

**⚠️ HARD GATE:** Ask the design questions. Get answers to 1–3 before writing any code:
1. What does the harness build? (sets Generator tools + Evaluator rubric)
2. Python or TypeScript? (default: Python)
3. Backend + model per agent? (default: all `claude`; all choices → `config.yaml`)
   Ask: planner/generator/evaluator — `claude`, `codex`, or `deepcode`?
   - If `claude`: which model? Thinking enabled?
   - If `codex`: which model + `reasoning_effort`?
   - If `deepcode`: which model? Confirm `/Users/xzhao/.local/bin/deepcode` and `DEEPSEEK_API_KEY`.
4. Harness mode:
   - `greenfield`: create a new app under `project_dir/src`
   - `existing-codebase`: modify an existing repo
   - `production-qa`: mostly evaluate/build/test and generate targeted fix sprints
5. Artifact policy: where should screenshots, logs, eval JSON, build output, browser traces,
   temp files, and evidence manifests go? Default: `harness-state/evidence/` and
   `harness-logs/`; never scatter them through the repo.

Create skeleton:
```bash
mkdir -p harness/agents harness/models harness/prompts
touch harness/harness.py harness/log.py harness/agents/__init__.py harness/models/__init__.py
```

At runtime, create the project folders before agents run:
```python
APP_DIR = PROJECT_DIR / "src"
STATE_DIR = PROJECT_DIR / "harness-state"
LOG_DIR = PROJECT_DIR / "harness-logs"
for path in [
    APP_DIR,
    STATE_DIR / "contracts",
    STATE_DIR / "handoffs",
    STATE_DIR / "evals",
    STATE_DIR / "evidence",
    STATE_DIR / "tmp",
    LOG_DIR,
]:
    path.mkdir(parents=True, exist_ok=True)
```

For existing-codebase mode, `APP_DIR` is usually `PROJECT_DIR`, but artifact paths stay the
same and write guards become mandatory.

**`config.yaml` + `config.py`** — all tunable parameters here; never hardcode in agent files.
**Load:** `$SKILL_DIR/instructions/config.md` for the full `HarnessConfig` dataclass.
```python
cfg = HarnessConfig.load(Path(__file__).parent / "config.yaml")
# Always: cfg.agents.generator.model  — never: "claude-opus-4-7"
# Backend:  cfg.agents.generator.backend   ("claude" | "codex" | "deepcode")
# Thinking: cfg.agents.evaluator.thinking.enabled / .budget_tokens
# Codex:    cfg.agents.generator.codex.reasoning_effort
# Deepcode: cfg.agents.generator.deepcode.cli_path / .env
# Workspace: cfg.workspace.mode / cfg.workspace.artifact_root / cfg.workspace.write_allowlist
```

**`models/state.py`** — write first; all other files import from it.
**Load:** `$SKILL_DIR/instructions/context-handoff.md` (`HandoffState`, `EvalResult`, `format_handoff_for_prompt`).
**Load:** `$SKILL_DIR/instructions/sprint-contracts.md` (`SprintContract` + negotiation protocol).

**`log.py`** — dual stdout + timestamped file under `harness-logs/`.
**Load:** `$SKILL_DIR/instructions/logging.md` for full implementation.
```python
log.setup(PROJECT_DIR, label="run")  # once in main()
logger = log.get()                   # in every agent
```

---

## Phase 2: Planner Agent

**Load:** `$SKILL_DIR/instructions/planner-questions.md` for system prompt template.
**Load:** `$SKILL_DIR/instructions/agent-patterns.md` for full `run_planner` implementation.

`run_planner(brief, session_id, cfg)` → `(reply, new_session_id)`.
`ClaudeAgentOptions(resume=session_id)` continues session without resending history.

```python
def extract_sprint_plan(spec: str) -> str:
    marker = "## Sprint Definitions"
    return spec[spec.find(marker):].strip() if marker in spec else spec.strip()

spec, session_id = "", None
while "SPEC_COMPLETE" not in spec:
    user_input = input("[Planner asks]: ").strip() if session_id else initial_brief
    spec, session_id = run_planner(user_input, session_id, cfg)
STATE_DIR.joinpath("spec.md").write_text(spec.replace("SPEC_COMPLETE", "").strip())
STATE_DIR.joinpath("sprints.md").write_text(extract_sprint_plan(spec))
```

`sprints.md` is the human-readable sprint plan copied or derived from the SPEC's sprint
definitions. Confirmed executable contracts are stored separately as JSON under
`harness-state/contracts/`.

---

## Phase 3: Generator Agent

**Load:** `$SKILL_DIR/instructions/agent-patterns.md` for `run_generator` + `self_assess` implementations.
**If mode is not greenfield:** load `$SKILL_DIR/instructions/git-safety.md`.

```python
def run_generator(
    spec, contract, project_dir,
    handoff=None, strategic_framing=None, cfg=None,
) -> str: ...

ClaudeAgentOptions(
    model=cfg.agents.generator.model,
    allowed_tools=["Write", "Read", "Edit", "Bash", "Glob"],
    cwd=str(project_dir / "src"), permission_mode="bypassPermissions",
)
```

The Generator must treat `project_dir/src` as the app root. It may read harness state
through the prompt, but it must not create code, package files, or tests outside `src`.

In existing-codebase mode, replace that rule with:
- cwd may be repo root.
- Generator may edit only paths matching `cfg.workspace.write_allowlist`.
- Generator must never write logs, screenshots, reports, traces, generated eval JSON, or
  temporary manifests outside the harness artifact roots.
- Generator must not use `git add -A`; commits are either disabled or path-scoped.

After generation, call `self_assess()` — catches gaps before the Evaluator via
`submit_assessment` MCP tool. If not confident → extra pass with concerns as `strategic_framing`.

**`self_assess()` always uses Claude** regardless of generator backend. It uses
`cfg.agents.generator.self_assess_model` (default: `claude-haiku-4-5-20251001`).
When generator backend is `codex` or `deepcode`, do not call backend-specific helpers directly
for the extra pass. Call `run_generator` normally — backend dispatch still comes from config.

---

## Phase 4: Evaluator Agent

**Load:** `$SKILL_DIR/instructions/agent-patterns.md` for full implementation.
**Load:** `$SKILL_DIR/instructions/evaluation-rubrics.md` for system prompt + rubric criteria.
**For browser/API/build evidence collection:** load `$SKILL_DIR/instructions/evaluator-evidence.md`.

Two roles: `run_evaluator()` (post-generation gate) + `review_contract()` (pre-sprint criteria review).

```python
# submit_grade schema: contract_results[{id, status, evidence}], rubric_scores{id: 1–5}, feedback
def run_evaluator(spec, contract, app_url, rubric_track="A", cfg=None, project_dir=None) -> EvalResult: ...
```

**⚠️ Deterministic verdict:** Never trust `verdict` from the LLM. Recompute in
`_build_eval_result()` from `contract_results` + `rubric_scores` using `cfg.verdict.*` thresholds.

**Evidence first:** collect deterministic evidence before asking the LLM to grade:
navigation, screenshots, DOM summaries, buttons/forms, viewport overflow, axe, Lighthouse,
API probes, command output, and contract-declared source excerpts. Store all raw evidence under
`harness-state/evidence/sprint-N/`.

---

## Phase 5: Harness Loop

**Load:** `$SKILL_DIR/instructions/iteration-loop.md` for `run_sprint`, `strategic_decision`, `git_commit`.
**Load:** `$SKILL_DIR/instructions/workspace-hygiene.md` before implementing artifact writes.

```python
def main():
    cfg = HarnessConfig.load(Path(__file__).parent / "config.yaml")
    log.setup(PROJECT_DIR, label="run")

def run_sprint(spec, contract, project_dir, handoff=None, cfg=None):
    while iteration < cfg.loop.max_iterations:
        # 1. Generate — try/except; crash is a valid (poor) outcome
        # 2. Self-assess — extra pass if not confident
        # 3. save handoff → harness-state/handoffs/
        # 4. save raw artifacts → harness-state/evidence/sprint-N/
        # 5. git_commit("wip: sprint N iter I") if git checkpointing is enabled
        # 6. Evaluate → EvalResult; save eval → harness-state/evals/
        # 5a. Pass + iteration < min_iterations → quality-improvement continue
        #     Pass + min_iterations met → git_commit("feat") + return
        # 5b. Fail → strategic_decision() → REFINE or PIVOT → set strategic_framing
    # Exhausted: input() if isatty() else return last result
```

Git checkpoints (see `iteration-loop.md` for `git_commit()` helper):

| Event | Message |
|---|---|
| Spec written | `feat: generate spec.md` |
| Contract negotiated | `chore: sprint N contract` |
| Each iteration | `wip: sprint N iteration I` |
| Sprint passes | `feat: sprint N complete` |

For existing-codebase mode, prefer `git checkpoint` or path-scoped staging over `git add -A`.
If path-scoped commit cannot be implemented safely, disable auto-commit and write a diff summary
to `harness-state/evidence/sprint-N/git/`.

Setup: `uv venv && uv pip install claude-agent-sdk pyyaml && export ANTHROPIC_API_KEY=sk-...`
Verify: `uv run python -c "from agents.planner import run_planner; print('OK')"`

---

## Common Mistakes

| Mistake | Fix |
|---|---|
| Trusting LLM's `verdict` field | Recompute in `_build_eval_result()` from `contract_results` + `rubric_scores` |
| Hardcoding model names | Use `cfg.agents.generator.model` — never a string literal |
| Not calling `handoff.save()` before Evaluator | On crash, Evaluator result is lost |
| Letting Generator write in `project_dir` | Set Generator cwd to `project_dir/src`; keep state/logs outside `src` |
| Reusing greenfield boundaries for an existing repo | Switch to existing-codebase mode and define allowlists/protected paths |
| Scattering screenshots, build logs, reports, and JSON through app/public/docs | Route all generated artifacts through `harness-state/evidence/` and `harness-logs/` |
| Adding public evidence routes with no cleanup plan | Declare them in the contract and add a cleanup sprint |
| Using `input()` in CI | Guard with `sys.stdin.isatty()` first |
| Accumulating messages across sprints | Each sprint is a fresh `query()` call — no cross-sprint history |
| Marking `completed_features` from Generator claim | Only promote after Evaluator PASS verdict |
| Using Codex evaluator for UI sprints | Codex can't open a browser — use Claude or deepcode evaluator for Playwright testing |
| Calling `self_assess()` with Codex model kwargs | `self_assess` always uses Claude SDK; model comes from `self_assess_model` |
| Setting `temperature` when `thinking.enabled: true` | Omit temperature or set to `1.0`; the API enforces this |
| Using `codex` backend for Planner expecting interactive Q&A | Codex Planner is single-shot — no clarifying questions loop |
| Treating `deepcode` as raw subprocess | Use Claude Agent SDK with `cli_path=/Users/xzhao/.local/bin/deepcode`, not an arbitrary command adapter |

---

## When to Simplify

| Component | Remove / simplify when |
|---|---|
| Planner agent | User provides SPEC directly |
| Contract negotiation | Human has strong opinions; use config-file mode |
| Generator self-assessment | Evaluator consistently passes first attempt |
| `max_iterations` → 3 | Correctness-only task, no quality/aesthetic goal |
| `min_iterations` → 1 | Early passes are always good enough |
| Refine/pivot `strategic_decision` | Single sprint or correctness task |
| `HandoffState` | Sprint fits in one context window |
| Evaluator | Task within Generator's reliable baseline |
