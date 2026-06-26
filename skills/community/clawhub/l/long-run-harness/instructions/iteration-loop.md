# Iteration Loop: Refine vs. Pivot

The original skill used `MAX_RETRIES = 2`. This works for correctness (fixing broken
features) but not for quality (improving design). The article runs 5–15 iterations per
sprint, with the Generator making a **strategic decision** after each failed evaluation:
continue in the current direction (refine) or abandon it entirely (pivot).

Without this, the loop is just bug-fixing. With it, the loop is creative amplification.

---

## Root Cause of the Original Omission

`MAX_RETRIES = 2` encodes an engineering assumption: retries exist to handle failures.
But for visual/design quality, "failure" isn't a bug to fix — it's a direction to improve.
Two retries can patch a broken form. Twelve iterations can push a mediocre design toward
distinctive. The skill was built to produce *working* apps; the article was building
*excellent* ones. That's a different loop.

---

## Score History Data Structure

Track scores across iterations within a sprint to detect trend:

```python
score_history: list[dict] = []

# After each evaluation, append:
score_history.append({
    "iteration": iteration,
    "verdict": result.verdict,
    "rubric_average": result.rubric_average,
    "failing_sc": [sc.id for sc in result.contract_results if sc.status == "fail"],
})
```

---

## `strategic_decision()` — Generator reviews its own trend

```python
_STRATEGY_TOOL = {
    "name": "set_strategy",
    "description": "Set the strategy for the next generation iteration based on score trend.",
    "input_schema": {
        "type": "object",
        "properties": {
            "decision": {
                "type": "string",
                "enum": ["refine", "pivot"],
                "description": (
                    "refine = scores trending up or feedback is actionable; keep direction. "
                    "pivot = scores flat/declining ≥2 iterations; try a new approach entirely."
                ),
            },
            "reasoning": {"type": "string"},
            "framing": {
                "type": "string",
                "description": (
                    "Concrete directive for next pass. "
                    "Refine: 2-3 specific things to fix. "
                    "Pivot: new direction — layout, color, typography, component style."
                ),
            },
        },
        "required": ["decision", "reasoning", "framing"],
    },
}


def strategic_decision(
    spec: str,
    contract: SprintContract,
    score_history: list[dict],
    latest_feedback: str,
    handoff: HandoffState | None = None,
    cfg: "HarnessConfig | None" = None,
) -> tuple[str, str]:
    """Returns (decision, framing) for the next iteration."""
    history_lines = [
        f"  Iter {e['iteration']}: verdict={e['verdict']}, "
        f"rubric_avg={e['rubric_average']:.2f}, failing=[{', '.join(e['failing_sc'])}]"
        for e in score_history
    ]
    avgs = [e["rubric_average"] for e in score_history]
    trend = "insufficient data"
    if len(avgs) >= 2:
        delta = avgs[-1] - avgs[-2]
        overall = avgs[-1] - avgs[0]
        if delta > 0.3:
            trend = f"improving (+{delta:.2f} last, +{overall:.2f} overall)"
        elif delta < -0.1:
            trend = f"declining ({delta:+.2f} last, {overall:+.2f} overall)"
        else:
            trend = f"flat ({delta:+.2f} last, {overall:+.2f} overall)"

    system = [
        {"type": "text", "text": _SYSTEM_PROMPT, "cache_control": {"type": "ephemeral"}},
        {"type": "text", "text": f"## SPEC\n\n{spec}", "cache_control": {"type": "ephemeral"}},
    ]
    if handoff:
        system.append({"type": "text", "text": format_handoff_for_prompt(handoff)})

    messages = [{
        "role": "user",
        "content": (
            f"Reviewing iteration history for Sprint {contract.sprint_number}.\n\n"
            f"Score history:\n" + "\n".join(history_lines) + f"\n\nTrend: {trend}\n\n"
            f"Latest evaluator feedback:\n{latest_feedback}\n\n"
            f"REFINE if: scores improving, feedback specific and fixable.\n"
            f"PIVOT if: scores flat/declining ≥2 iterations, current approach not working.\n\n"
            f"Call set_strategy."
        ),
    }]

    # strategic_decision always uses Claude — pass cfg.loop.strategic_decision_model
    _model = cfg.loop.strategic_decision_model if cfg else "claude-opus-4-7"
    response = _client.messages.create(
        model=_model,
        max_tokens=1024,
        system=system,
        tools=[_STRATEGY_TOOL],
        tool_choice={"type": "any"},
        messages=messages,
    )
    for block in response.content:
        if block.type == "tool_use" and block.name == "set_strategy":
            d = block.input
            return d["decision"], d["framing"]
    raise RuntimeError("Generator did not call set_strategy.")
```

---

## Updated `run_generator` signature

Accept `strategic_framing` so each iteration starts with an explicit directive:

```python
def run_generator(
    spec: str,
    contract: SprintContract,
    project_dir: Path,
    handoff: HandoffState | None = None,
    strategic_framing: str | None = None,   # ← NEW
) -> str:
    ...
    opening = f"Implement Sprint {contract.sprint_number}: {contract.goal}"
    if strategic_framing:
        opening = f"{strategic_framing}\n\n---\n\n{opening}"
    messages = [{"role": "user", "content": opening}]
```

---

## Updated `run_sprint` loop (replace `MAX_RETRIES` block)

```python
MAX_ITERATIONS = 15  # default ceiling; override via config.yaml loop.max_iterations

def run_sprint(...) -> tuple[EvalResult, HandoffState]:
    score_history: list[dict] = []
    strategic_framing: str | None = None
    iteration = 0

    while iteration < MAX_ITERATIONS:
        iteration += 1
        summary = run_generator(spec, contract, project_dir, handoff,
                                strategic_framing=strategic_framing)
        handoff = build_handoff(contract.sprint_number, project_dir, summary)

        # self-assess before evaluator (see Phase 3.4)
        confident, concerns = self_assess(spec, contract, handoff.files_changed, summary)
        if not confident and iteration < MAX_ITERATIONS:
            iteration += 1
            summary = run_generator(spec, contract, project_dir, handoff,
                                    strategic_framing="Fix these gaps:\n" +
                                    "\n".join(f"- {c}" for c in concerns))
            handoff = build_handoff(contract.sprint_number, project_dir, summary)

        result = run_evaluator(spec, contract, app_url, project_dir=project_dir)
        save_eval_result(project_dir, contract.sprint_number, iteration, result)
        score_history.append({
            "iteration": iteration, "verdict": result.verdict,
            "rubric_average": result.rubric_average,
            "failing_sc": [sc.id for sc in result.contract_results if sc.status == "fail"],
        })

        if result.verdict in ("pass", "conditional_pass"):
            return result, handoff

        # Strategic decision: refine or pivot
        decision, framing = strategic_decision(
            spec, contract, score_history, result.feedback, handoff
        )
        strategic_framing = f"## Strategic directive — {decision.upper()}\n\n{framing}"
        if handoff:
            handoff.known_broken.append(f"Iter {iteration} ({decision}): {framing[:200]}")

    # Exhausted — escalate to user
    input("Max iterations reached. Fix manually, then press Enter to re-evaluate...")
    return run_sprint(spec, contract, project_dir, handoff, eval_only=True)
```

---

## `min_iterations` — Quality Floor

`MAX_ITERATIONS` is a ceiling. `min_iterations` is a floor: even when the Evaluator passes, the
loop continues until this count is reached — but with a **qualitatively different directive**.
Below the floor, the Generator isn't fixing failures; it's raising the bar on quality.

```python
if result.verdict in ("pass", "conditional_pass"):
    if iteration < cfg.loop.min_iterations:
        # Carry forward any conditional debt before continuing
        if result.verdict == "conditional_pass" and handoff:
            handoff.known_broken.append(
                f"Sprint {contract.sprint_number} conditional debt: {result.feedback[:200]}"
            )
        strategic_framing = (
            f"## Quality improvement pass ({iteration + 1}/{cfg.loop.min_iterations})\n\n"
            "All criteria PASS. Now raise the bar: improve craft and coherence, "
            "remove placeholder-feeling elements, polish details that passed but felt rough. "
            "Do NOT regress any passing criterion.\n\n"
            f"Previous evaluator feedback (for reference):\n{result.feedback or '(none)'}"
        )
        continue  # ← loop back; don't return yet
    # Below this line: all criteria pass AND min_iterations met → exit
    git_commit(project_dir, f"feat: sprint {contract.sprint_number} complete")
    return result, handoff
```

**Why this matters:** Without a minimum floor, the loop exits on the first pass — which may
be iteration 1. A single-attempt pass is rarely at the quality ceiling. Three iterations
costs roughly 3× the time but dramatically raises the output quality for tasks with an
aesthetic or craft dimension.

Set `min_iterations = 1` in `config.yaml` for correctness-only tasks where first-pass is
good enough.

---

## Generator Crash Recovery

A crashed generator (timeout or exception) is a valid outcome — evaluate the current project
state rather than aborting the sprint. This pattern keeps the harness running in long sessions
where occasional agent failures are expected:

```python
try:
    summary = run_generator(spec, contract, project_dir, handoff,
                            strategic_framing=strategic_framing, cfg=cfg)
except Exception as e:
    logger.info(f"  [Generator] crashed: {e} — evaluating current state")
    summary = f"Generator crashed ({type(e).__name__}) — state unchanged"
# Continue to self-assess and evaluate regardless
handoff = build_handoff(contract.sprint_number, project_dir, summary)
```

Apply the same pattern to the self-assessment extra pass:

```python
if not confident and iteration < cfg.loop.max_iterations:
    iteration += 1
    try:
        summary = run_generator(..., strategic_framing="Fix gaps:\n" + ...)
    except Exception as e:
        logger.info(f"  [Generator] crashed on self-assess pass: {e}")
        # summary keeps its previous value; build_handoff will still run
    handoff = build_handoff(contract.sprint_number, project_dir, summary)
```

---

## Non-Interactive Fallback at Max Iterations

`input()` hangs in CI, scheduled runs, and piped execution. Check `sys.stdin.isatty()` before
prompting:

```python
import sys

# After exhausting max_iterations:
if sys.stdin.isatty():
    input("Max iterations reached. Fix manually, then press Enter to re-evaluate...")
    return run_sprint(spec, contract, project_dir, handoff, cfg=cfg)
logger.info("[Harness] Non-interactive — returning last result.")
return result, handoff
```

---

## `git_commit()` Helper

Commit at every significant state transition so the run is replayable and diffs are meaningful.
Called from within `run_sprint()` — see SKILL.md Phase 5.3 for the checkpoint table.

```python
import subprocess

def git_commit(project_dir: Path, message: str) -> None:
    logger = log.get()
    try:
        subprocess.run(
            ["git", "add", "-A"],
            cwd=project_dir, check=True, capture_output=True,
        )
        result = subprocess.run(
            ["git", "diff", "--cached", "--quiet"],
            cwd=project_dir,
        )
        if result.returncode == 0:
            return  # nothing staged — skip
        subprocess.run(
            ["git", "commit", "-m", message],
            cwd=project_dir, check=True, capture_output=True,
        )
        logger.info(f"  [Git] Committed: {message}")
    except subprocess.CalledProcessError as e:
        logger.info(f"  [Git] Commit skipped ({e})")
```

---

## Runtime Artifact Helpers

Keep orchestration artifacts out of generated app code. These helpers belong in `harness.py`
and are called from the planner, contract negotiation, and sprint loop:

```python
def ensure_project_layout(project_dir: Path, cfg=None, sprint: int | None = None) -> dict[str, Path]:
    workspace = cfg.workspace if cfg else None
    state = project_dir / (workspace.artifact_root if workspace else "harness-state")
    logs = project_dir / (workspace.log_root if workspace else "harness-logs")
    evidence = project_dir / (workspace.evidence_root if workspace else "harness-state/evidence")
    tmp = project_dir / (workspace.tmp_root if workspace else "harness-state/tmp")
    paths = {
        "app": project_dir / (workspace.app_root if workspace else "src"),
        "state": state,
        "contracts": state / "contracts",
        "handoffs": state / "handoffs",
        "evals": state / "evals",
        "evidence": evidence,
        "tmp": tmp,
        "logs": logs,
    }
    if sprint is not None:
        sprint_root = evidence / f"sprint-{sprint}"
        paths.update({
            "sprint_evidence": sprint_root,
            "commands": sprint_root / "commands",
            "screenshots": sprint_root / "screenshots",
            "browser": sprint_root / "browser",
            "axe": sprint_root / "axe",
            "lighthouse": sprint_root / "lighthouse",
            "source": sprint_root / "source",
            "api": sprint_root / "api",
            "git": sprint_root / "git",
            "artifacts": sprint_root / "artifacts",
        })
    for path in paths.values():
        path.mkdir(parents=True, exist_ok=True)
    return paths


def save_spec(project_dir: Path, spec: str, cfg=None) -> None:
    paths = ensure_project_layout(project_dir, cfg)
    paths["state"].joinpath("spec.md").write_text(spec.strip())


def save_sprint_plan(project_dir: Path, sprint_plan: str, cfg=None) -> None:
    paths = ensure_project_layout(project_dir, cfg)
    paths["state"].joinpath("sprints.md").write_text(sprint_plan.strip())


def save_contract(project_dir: Path, contract: SprintContract, cfg=None) -> None:
    paths = ensure_project_layout(project_dir, cfg)
    contract.save(paths["contracts"] / f"contract-sprint-{contract.sprint_number}.json")


def save_eval_result(project_dir: Path, sprint_number: int, iteration: int, result: EvalResult, cfg=None) -> None:
    paths = ensure_project_layout(project_dir, cfg, sprint=sprint_number)
    result.save(paths["evals"] / f"eval-sprint-{sprint_number}-iter-{iteration}.json")
```

`project_dir/src` is the only directory the Generator writes to in greenfield mode.
In existing-codebase mode, editable paths come from `cfg.workspace.write_allowlist`.
`harness-state` and `harness-logs` are harness-owned in all modes.

All screenshots, browser traces, axe reports, Lighthouse reports, command output, source
excerpts, and temporary manifests must be written through `ensure_project_layout(..., sprint=N)`.
Do not create `public/__sprint-*`, `src/app/api/sprint-*`, root `lh-report.json`, or loose
`output.txt` files unless the sprint contract explicitly declares them.

---

## When to Simplify

| Remove when |
|---|
| Task is correctness-only — set `max_iterations: 3`, `min_iterations: 1` in config.yaml |
| Evaluator consistently passes on first attempt — the loop earns no cost |
| Single sprint already produces passing quality — skip sprint decomposition |
