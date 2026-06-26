# Agent Patterns: Full Implementations

Full Python implementations for each agent module. SKILL.md shows signatures and key design
choices; load this file when you need the complete runnable code.

Each agent dispatches on `cfg.agents.<agent>.backend`:
- `"claude"` → claude_agent_sdk agentic loop (default)
- `"codex"` → Codex CLI subprocess via `_run_codex()`
- `"deepcode"` → claude_agent_sdk loop with `ClaudeAgentOptions.cli_path` set to `deepcode`

`self_assess()` and `strategic_decision()` always use Claude regardless of generator backend.

---

## Shared: `_run_codex()` Helper

Add this as a module-level function in any agent file that needs it (or extract to
`harness/codex_runner.py` and import it). Import `subprocess` and `shutil` at the top.

```python
import shutil
import subprocess

def _run_codex(
    prompt: str,
    agent_cfg: "SingleAgentConfig",
    cwd: str | None = None,
    timeout: float | None = None,
) -> str:
    """Run Codex CLI as a subprocess and return its stdout.

    ⚠️  Verify exact flag names with `codex --help` before deploying — the Codex CLI
    evolves quickly. Flags here are accurate as of mid-2025.
    """
    if not shutil.which("codex"):
        raise RuntimeError(
            "Codex CLI not found. Install: npm install -g @openai/codex\n"
            "Then set OPENAI_API_KEY in your environment."
        )
    cmd = ["codex"]
    if agent_cfg.codex.quiet:
        cmd.append("--quiet")
    cmd.extend(["--approval-mode", agent_cfg.codex.approval_mode])
    if agent_cfg.model:
        cmd.extend(["--model", agent_cfg.model])
    if agent_cfg.codex.provider:
        cmd.extend(["--provider", agent_cfg.codex.provider])
    if agent_cfg.codex.reasoning_effort:
        # --reasoning-effort is supported by o-series models (o3, o4-mini, etc.)
        # Omit or set to "medium" for non-reasoning models.
        cmd.extend(["--reasoning-effort", agent_cfg.codex.reasoning_effort])
    for arg in agent_cfg.codex.extra_args:
        cmd.append(arg)
    cmd.append(prompt)

    result = subprocess.run(
        cmd,
        cwd=cwd,
        capture_output=True,
        text=True,
        timeout=timeout or 1500,
    )
    if result.returncode != 0:
        raise RuntimeError(
            f"Codex exited with code {result.returncode}.\n"
            f"stderr: {result.stderr[:600]}"
        )
    return result.stdout.strip()
```

---

## Deepcode Backend

`deepcode` is not a raw subprocess backend. It uses Claude Agent SDK with:

```python
ClaudeAgentOptions(cli_path="/Users/xzhao/.local/bin/deepcode", env={...})
```

This preserves the Claude SDK programming model while running Claude Code `2.1.153` against
DeepSeek. `_claude_options()` below applies `cli_path` and env automatically when
`agent_cfg.backend == "deepcode"`.

---

## `harness/agents/planner.py`

**Claude path:** multi-turn session with `resume=session_id`; loop until `SPEC_COMPLETE`.
**Codex path:** single-shot — pass brief + instructions in one prompt; Codex must emit
`SPEC_COMPLETE` at the end. No interactive clarification loop; `session_id` is always `None`.

```python
from __future__ import annotations
import asyncio
import concurrent.futures
import os
import shutil
import subprocess
from pathlib import Path

from claude_agent_sdk import query, ClaudeAgentOptions, AssistantMessage, ResultMessage
from config import HarnessConfig, SingleAgentConfig
import log

_SYSTEM_PROMPT = (Path(__file__).parent.parent / "prompts" / "planner.md").read_text()


def _run_async(coro):
    with concurrent.futures.ThreadPoolExecutor(max_workers=1) as pool:
        return pool.submit(asyncio.run, coro).result()


def run_planner(
    brief: str,
    session_id: str | None = None,
    cfg: HarnessConfig | None = None,
) -> tuple[str, str | None]:
    """Run one planning turn. Returns (reply, session_id).
    Caller loops until 'SPEC_COMPLETE' appears in reply, passing returned session_id back in.
    With Codex backend, session_id is always None and SPEC_COMPLETE appears on the first call.
    """
    agent_cfg = cfg.agents.planner if cfg else SingleAgentConfig(model="claude-haiku-4-5-20251001")
    if agent_cfg.backend == "codex":
        return _run_planner_codex(brief, agent_cfg)
    return _run_async(_run_planner_async(brief, session_id, agent_cfg))


def _run_planner_codex(brief: str, agent_cfg: SingleAgentConfig) -> tuple[str, None]:
    """Single-shot Codex planner: no interactive clarification loop."""
    logger = log.get()
    logger.info("  [Planner/Codex] Running single-shot spec generation...")
    prompt = (
        f"{_SYSTEM_PROMPT}\n\n"
        f"---\n\n"
        f"Brief:\n{brief}\n\n"
        f"Write the complete SPEC now. Do NOT ask clarifying questions — infer reasonable "
        f"defaults for anything unclear. End your response with exactly: SPEC_COMPLETE"
    )
    reply = _run_codex(prompt, agent_cfg)
    logger.info(f"  [Planner/Codex] {reply[:200]}")
    if "SPEC_COMPLETE" not in reply:
        reply = reply + "\nSPEC_COMPLETE"
    return reply, None

async def _run_planner_async(
    brief: str,
    session_id: str | None,
    agent_cfg: SingleAgentConfig,
) -> tuple[str, str | None]:
    logger = log.get()
    options = _claude_options(agent_cfg, _SYSTEM_PROMPT, resume=session_id)
    reply = ""
    new_session_id = session_id
    async for message in query(prompt=brief, options=options):
        if isinstance(message, AssistantMessage):
            for block in message.content:
                if hasattr(block, "text") and block.text.strip():
                    reply = block.text
                    logger.info(f"  [Planner] {block.text[:200]}")
            if message.session_id:
                new_session_id = message.session_id
        elif isinstance(message, ResultMessage):
            if message.session_id:
                new_session_id = message.session_id
            if message.result and not reply:
                reply = message.result
    return reply, new_session_id
```

---

## `harness/agents/generator.py` — Core Loop

**Claude path:** full agentic loop via claude_agent_sdk with file tools.
**Codex path:** subprocess with `--approval-mode full-auto`; Codex manages its own tool use
(file reads/writes, shell commands) internally. The harness gets only the final stdout summary.

```python
from __future__ import annotations
import asyncio
import concurrent.futures
import json
import os
import re
import shutil
import subprocess
from pathlib import Path

from claude_agent_sdk import (
    query, ClaudeAgentOptions, AssistantMessage, ResultMessage,
    tool, create_sdk_mcp_server,
)
from models.state import SprintContract, HandoffState, SuccessCriterion, format_handoff_for_prompt
from config import HarnessConfig, SingleAgentConfig
import log

_SYSTEM_PROMPT = (Path(__file__).parent.parent / "prompts" / "generator.md").read_text()
_FILE_TOOLS = ["Write", "Read", "Edit", "Bash", "Glob"]


def _run_async(coro, timeout: float | None = None):
    with concurrent.futures.ThreadPoolExecutor(max_workers=1) as pool:
        future = pool.submit(asyncio.run, coro)
        try:
            return future.result(timeout=timeout)
        except concurrent.futures.TimeoutError:
            raise TimeoutError(f"Generator exceeded {timeout:.0f}s timeout")


def run_generator(
    spec: str,
    contract: SprintContract,
    project_dir: Path,
    handoff: HandoffState | None = None,
    strategic_framing: str | None = None,
    cfg: HarnessConfig | None = None,
) -> str:
    agent_cfg = cfg.agents.generator if cfg else SingleAgentConfig(model="claude-opus-4-7")
    timeout = cfg.loop.generator_timeout_seconds if cfg else 1500
    workspace = cfg.workspace if cfg else None
    app_dir = project_dir / (workspace.app_root if workspace else "src")
    app_dir.mkdir(parents=True, exist_ok=True)
    if agent_cfg.backend == "codex":
        return _run_generator_codex(
            spec, contract, app_dir, handoff, strategic_framing, agent_cfg, timeout, workspace
        )
    return _run_async(
        _run_generator_async(spec, contract, app_dir, handoff, strategic_framing, agent_cfg, workspace),
        timeout=timeout,
    )


def _run_generator_codex(
    spec: str,
    contract: SprintContract,
    app_dir: Path,
    handoff: HandoffState | None,
    strategic_framing: str | None,
    agent_cfg: SingleAgentConfig,
    timeout: float,
    workspace=None,
) -> str:
    logger = log.get()
    logger.info(f"  [Generator/Codex] Sprint {contract.sprint_number} — starting...")
    system_text = _build_system_prompt(spec, contract, handoff, workspace)
    opening = f"Implement Sprint {contract.sprint_number}: {contract.goal}"
    if strategic_framing:
        opening = f"{strategic_framing}\n\n---\n\n{opening}"
    prompt = f"{system_text}\n\n---\n\n{opening}"
    summary = _run_codex(prompt, agent_cfg, cwd=str(app_dir), timeout=timeout)
    logger.info(f"  [Generator/Codex] Done. Summary: {summary[:200]}")
    return summary or "(codex completed with no stdout)"

async def _run_generator_async(
    spec: str,
    contract: SprintContract,
    app_dir: Path,
    handoff: HandoffState | None,
    strategic_framing: str | None,
    agent_cfg: SingleAgentConfig,
    workspace=None,
) -> str:
    logger = log.get()
    system = _build_system_prompt(spec, contract, handoff, workspace)
    opening = f"Implement Sprint {contract.sprint_number}: {contract.goal}"
    if strategic_framing:
        opening = f"{strategic_framing}\n\n---\n\n{opening}"

    options = _claude_options(
        agent_cfg, system,
        allowed_tools=_FILE_TOOLS,
        permission_mode="bypassPermissions",
        cwd=str(app_dir),
    )

    logger.info(f"  [Generator] Sprint {contract.sprint_number} — starting...")
    summary = ""
    async for message in query(prompt=opening, options=options):
        if isinstance(message, AssistantMessage):
            for block in message.content:
                if hasattr(block, "text") and block.text.strip():
                    summary = block.text
                elif hasattr(block, "name"):
                    tool_name = block.name
                    tool_input = getattr(block, "input", {}) or {}
                    logger.info(f"  [Generator] Tool: {tool_name}")
                    for key, value in tool_input.items():
                        val_str = str(value).replace("\n", "\\n")
                        if len(val_str) > 300:
                            val_str = val_str[:300] + "…"
                        logger.info(f"  [Generator]   {key}: {val_str}")
        elif isinstance(message, ResultMessage):
            if message.result:
                summary = message.result
    return summary


def _build_system_prompt(
    spec: str,
    contract: SprintContract,
    handoff: HandoffState | None,
    workspace=None,
) -> str:
    criteria_block = "\n".join(
        f"- {sc.id}: {sc.description}" for sc in contract.success_criteria
    )
    out_of_scope_block = (
        "\n".join(f"- {item}" for item in contract.out_of_scope)
        if contract.out_of_scope else "- (none specified)"
    )
    if workspace and workspace.mode != "greenfield":
        workspace_rules = (
            f"Workspace mode: {workspace.mode}\n"
            f"Editable path allowlist:\n" +
            "\n".join(f"- {p}" for p in workspace.write_allowlist) +
            f"\n\nProtected paths:\n" +
            "\n".join(f"- {p}" for p in workspace.protected_paths) +
            f"\n\nAll generated evidence, screenshots, logs, reports, temp files, and manifests "
            f"must go under {workspace.evidence_root}, {workspace.tmp_root}, or {workspace.log_root}."
        )
    else:
        workspace_rules = (
            "Workspace mode: greenfield\n"
            "Write all generated app code, tests, package files, and assets inside the current working directory only.\n"
            "Do not create or edit files in harness-state, harness-logs, project root docs, public evidence folders, or sibling directories."
        )
    parts = [
        _SYSTEM_PROMPT,
        f"## SPEC\n\n{spec}",
        (
            f"## Sprint Contract Enforcement\n\n"
            f"Sprint {contract.sprint_number}: {contract.goal}\n\n"
            f"SUCCESS CRITERIA (ALL must be verifiable by an Evaluator opening the app):\n"
            f"{criteria_block}\n\n"
            f"OUT OF SCOPE THIS SPRINT:\n{out_of_scope_block}\n\n"
            f"Rules:\n"
            f"- Build ONLY what is in scope. Do not build ahead.\n"
            f"- {workspace_rules}\n"
            f"- Each criterion must be demonstrable via observable interaction.\n"
            f"- When done, write a brief summary and any known issues."
        ),
    ]
    if handoff:
        parts.append(format_handoff_for_prompt(handoff))
    return "\n\n".join(parts)
```

---

## Generator Self-Assessment (`self_assess`)

**Always uses Claude regardless of generator backend.** The `submit_assessment` MCP tool
requires claude_agent_sdk — it is not available to Codex. The model used is
`cfg.agents.generator.self_assess_model` (defaults to `claude-haiku-4-5-20251001`).

Add to `harness/agents/generator.py`:

```python
def self_assess(
    spec: str,
    contract: SprintContract,
    files_changed: list[str],
    generator_summary: str,
    cfg: HarnessConfig | None = None,
) -> tuple[bool, list[str]]:
    """Returns (confident, concerns). Always runs via Claude (never Codex)."""
    agent_cfg = cfg.agents.generator if cfg else SingleAgentConfig()
    assess_model = agent_cfg.self_assess_model or "claude-haiku-4-5-20251001"
    return _run_async(_self_assess_async(spec, contract, files_changed, generator_summary, assess_model))


async def _self_assess_async(spec, contract, files_changed, generator_summary, model: str):
    result: dict = {}

    async def _handler(args: dict) -> dict:
        result["data"] = args
        return {"content": [{"type": "text", "text": "Assessment submitted."}]}

    assess_tool = tool(
        name="submit_assessment",
        description="Submit a self-assessment of the completed sprint implementation.",
        input_schema={
            "type": "object",
            "properties": {
                "confident": {
                    "type": "boolean",
                    "description": "True if ALL criteria are believed to be met.",
                },
                "criterion_assessments": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "id": {"type": "string"},
                            "met": {"type": "boolean"},
                            "concern": {
                                "type": "string",
                                "description": "Describe the gap if met=false, else empty.",
                            },
                        },
                        "required": ["id", "met", "concern"],
                    },
                },
            },
            "required": ["confident", "criterion_assessments"],
        },
    )(_handler)

    server = create_sdk_mcp_server("assess", tools=[assess_tool])
    criteria_block = "\n".join(
        f"- {sc.id}: {sc.description}" for sc in contract.success_criteria
    )
    files_block = "\n".join(f"- {f}" for f in files_changed) or "- (none tracked)"

    options = ClaudeAgentOptions(
        system_prompt="\n\n".join([_SYSTEM_PROMPT, f"## SPEC\n\n{spec}"]),
        model=model,
        tools=[],
        mcp_servers={"assess": server},
        permission_mode="bypassPermissions",
        max_turns=3,
    )

    prompt = (
        f"You just completed Sprint {contract.sprint_number}: {contract.goal}\n\n"
        f"**What you built:**\n{generator_summary}\n\n"
        f"**Files changed:**\n{files_block}\n\n"
        f"**Success criteria:**\n{criteria_block}\n\n"
        f"For each criterion, assess whether an evaluator opening the app right now "
        f"would see it satisfied. Flag any criterion you are not fully confident about. "
        f"Call submit_assessment."
    )

    async for _ in query(prompt=prompt, options=options):
        pass

    if "data" not in result:
        raise RuntimeError("Generator did not call submit_assessment.")

    data = result["data"]
    concerns = [
        f"{a['id']}: {a['concern']}"
        for a in data["criterion_assessments"] if not a["met"]
    ]
    return data["confident"], concerns
```

---

## `harness/agents/evaluator.py` — Core Evaluation

**Claude path:** MCP `submit_grade` tool + optional Playwright tools for browser testing.
**Codex path:** no MCP tools available. Codex reads files and runs shell commands, then
outputs a JSON block. The harness parses it. **Limitation:** Codex cannot do browser
interaction — use Claude for any sprint that needs Playwright evaluation.
**Deepcode path:** same Claude SDK path with `cli_path=/Users/xzhao/.local/bin/deepcode`;
use it when DeepSeek-backed Claude Code should evaluate with the Claude SDK tool model.

```python
from __future__ import annotations
import asyncio
import concurrent.futures
import json
import os
import re
import shutil
import subprocess
from pathlib import Path

from claude_agent_sdk import (
    query, ClaudeAgentOptions, AssistantMessage, ResultMessage,
    tool, create_sdk_mcp_server,
)
from models.state import SprintContract, EvalResult, SuccessCriterion
from config import HarnessConfig, SingleAgentConfig
import log

_SYSTEM_PROMPT = (Path(__file__).parent.parent / "prompts" / "evaluator.md").read_text()


def _run_async(coro):
    with concurrent.futures.ThreadPoolExecutor(max_workers=1) as pool:
        return pool.submit(asyncio.run, coro).result()


def run_evaluator(
    spec: str,
    contract: SprintContract,
    app_url: str,
    rubric_track: str = "A",
    cfg: HarnessConfig | None = None,
    project_dir: Path | None = None,
) -> EvalResult:
    agent_cfg = cfg.agents.evaluator if cfg else SingleAgentConfig(model="claude-opus-4-7")
    if agent_cfg.backend == "codex":
        return _run_evaluator_codex(spec, contract, app_url, project_dir, rubric_track, agent_cfg, cfg)
    return _run_async(_run_evaluator_async(spec, contract, app_url, rubric_track, agent_cfg, cfg))


def _run_evaluator_codex(
    spec: str,
    contract: SprintContract,
    app_url: str,
    project_dir: Path | None,
    rubric_track: str,
    agent_cfg: SingleAgentConfig,
    cfg: HarnessConfig | None,
) -> EvalResult:
    """Codex evaluator: code + file inspection only. No browser interaction.
    Use Claude evaluator for any sprint requiring Playwright / UI testing.
    """
    logger = log.get()
    logger.info(f"  [Evaluator/Codex] Sprint {contract.sprint_number} (code review mode)...")
    app_dir = (project_dir / "src") if project_dir else None
    criteria_block = "\n".join(
        f"- {sc.id}: {sc.description}" for sc in contract.success_criteria
    )
    prompt = (
        f"{_SYSTEM_PROMPT}\n\n"
        f"## SPEC\n\n{spec}\n\n"
        f"## Sprint Contract\n"
        f"Sprint {contract.sprint_number} — {contract.goal}\n\n"
        f"Success criteria:\n{criteria_block}\n\n"
        f"## Instructions\n"
        f"Evaluate the implementation in the current directory (project_dir/src). The app may be running at {app_url}.\n"
        f"You can read files, run shell commands (e.g. `curl {app_url}`), and inspect the codebase.\n"
        f"You CANNOT open a browser — test via HTTP requests and file inspection only.\n\n"
        f"When done, output a JSON block in EXACTLY this format (no other text after it):\n\n"
        f"```json\n"
        f"{{\n"
        f'  "contract_results": [{{"id": "SC-1", "status": "pass", "evidence": "..."}}],\n'
        f'  "rubric_scores": {{"C1": 4, "C4": 3}},\n'
        f'  "feedback": "..."\n'
        f"}}\n"
        f"```"
    )
    output = _run_codex(prompt, agent_cfg, cwd=str(app_dir) if app_dir else None, timeout=600)
    return _parse_codex_eval(output, contract, cfg)

def _parse_codex_eval(output: str, contract: SprintContract, cfg: HarnessConfig | None) -> EvalResult:
    """Extract the JSON block from Codex output and build an EvalResult."""
    match = re.search(r"```json\s*(\{.*?\})\s*```", output, re.DOTALL)
    if not match:
        # Fallback: try raw JSON anywhere in output
        match = re.search(r"\{.*\"contract_results\".*\}", output, re.DOTALL)
    if not match:
        raise RuntimeError(
            f"Codex evaluator did not produce a parseable JSON block.\n"
            f"Output tail: {output[-500:]}"
        )
    try:
        g = json.loads(match.group(1) if match.lastindex else match.group(0))
    except json.JSONDecodeError as e:
        raise RuntimeError(f"Codex evaluator JSON parse error: {e}\nRaw: {match.group(0)[:300]}")
    return _build_eval_result(g, contract, cfg)


async def _run_evaluator_async(spec, contract, app_url, rubric_track, agent_cfg, cfg):
    logger = log.get()
    grade_result: dict = {}

    async def _submit_grade(args: dict) -> dict:
        grade_result["data"] = args
        return {"content": [{"type": "text", "text": "Grade submitted."}]}

    grade_tool = tool(
        name="submit_grade",
        description="Submit the final evaluation result for this sprint.",
        input_schema={
            "type": "object",
            "properties": {
                "contract_results": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "id": {"type": "string"},
                            "status": {"type": "string", "enum": ["pass", "fail"]},
                            "evidence": {"type": "string"},
                        },
                        "required": ["id", "status", "evidence"],
                    },
                },
                "rubric_scores": {
                    "type": "object",
                    "description": "Map criterion ID to score 1–5",
                    "additionalProperties": {"type": "number"},
                },
                "verdict": {"type": "string", "enum": ["pass", "conditional_pass", "fail"]},
                "feedback": {"type": "string"},
            },
            "required": ["contract_results", "rubric_scores", "verdict", "feedback"],
        },
    )(_submit_grade)

    # Add domain-specific observation tools here (Playwright, API clients, etc.)
    # For browser testing see evaluation-rubrics.md for navigate/screenshot/check_element.
    server = create_sdk_mcp_server("eval", tools=[grade_tool])

    criteria_block = "\n".join(
        f"- {sc.id}: {sc.description}" for sc in contract.success_criteria
    )
    system_prompt = "\n\n".join([
        _SYSTEM_PROMPT,
        f"## SPEC\n\n{spec}",
        (
            f"## Sprint Contract\n"
            f"Sprint {contract.sprint_number} — {contract.goal}\n\n"
            f"Success criteria:\n{criteria_block}\n\n"
            f"Rubric track: Track {rubric_track}"
        ),
    ])

    options = _claude_options(
        agent_cfg, system_prompt,
        tools=[],
        mcp_servers={"eval": server},
        permission_mode="bypassPermissions",
    )

    logger.info(f"  [Evaluator] Sprint {contract.sprint_number} at {app_url}...")
    async for _ in query(
        prompt=f"Evaluate the app at {app_url}. Call submit_grade with your findings.",
        options=options,
    ):
        pass

    if "data" not in grade_result:
        raise RuntimeError("Evaluator did not call submit_grade.")

    return _build_eval_result(grade_result["data"], contract, cfg)


def _build_eval_result(g: dict, contract: SprintContract, cfg: HarnessConfig | None) -> EvalResult:
    scores = g.get("rubric_scores", {})
    avg = sum(scores.values()) / len(scores) if scores else 0.0
    all_pass = all(r["status"] == "pass" for r in g.get("contract_results", []))
    pt = cfg.verdict.pass_threshold if cfg else 3.0
    cpt = cfg.verdict.conditional_pass_threshold if cfg else 2.0

    if not all_pass:
        verdict = "fail"
    elif avg >= pt:
        verdict = "pass"
    elif avg >= cpt:
        verdict = "conditional_pass"
    else:
        verdict = "fail"

    contract_map = {sc.id: sc.description for sc in contract.success_criteria}
    criteria = [
        SuccessCriterion(
            id=r["id"],
            description=contract_map.get(r["id"], ""),
            status=r["status"],
            evidence=r.get("evidence", ""),
        )
        for r in g.get("contract_results", [])
    ]
    return EvalResult(
        verdict=verdict,
        rubric_average=round(avg, 2),
        contract_results=criteria,
        feedback=g.get("feedback", ""),
    )
```

---

## Shared `_claude_options()` Helper

Add this module-level function in each agent file (or extract to a shared `harness/claude_utils.py`).
It builds `ClaudeAgentOptions` from a `SingleAgentConfig`, applying thinking and temperature.

```python
from claude_agent_sdk import ClaudeAgentOptions
from config import SingleAgentConfig
import os

def _claude_options(
    agent_cfg: SingleAgentConfig,
    system_prompt: str,
    *,
    allowed_tools: list[str] | None = None,
    tools: list | None = None,
    mcp_servers: dict | None = None,
    permission_mode: str = "bypassPermissions",
    cwd: str | None = None,
    resume: str | None = None,
    max_turns: int | None = None,
) -> ClaudeAgentOptions:
    """Build ClaudeAgentOptions from a SingleAgentConfig.

    Thinking and temperature notes:
    - When thinking.enabled=True, temperature is forced to 1.0 by the API.
    - ClaudeAgentOptions may not expose thinking/temperature directly in all SDK versions.
      If not, pass them via extra_kwargs once the SDK supports it, or use the raw
      anthropic.Anthropic() client for that specific call.
    """
    kwargs: dict = dict(
        system_prompt=system_prompt,
        model=agent_cfg.model,
        permission_mode=permission_mode,
    )
    if agent_cfg.backend == "deepcode":
        kwargs["cli_path"] = agent_cfg.deepcode.cli_path
        kwargs["env"] = {
            **os.environ,
            **{
                k: (os.environ.get(v[2:-1], "") if isinstance(v, str) and v.startswith("${") and v.endswith("}") else v)
                for k, v in agent_cfg.deepcode.env.items()
            },
        }
    if allowed_tools is not None:
        kwargs["allowed_tools"] = allowed_tools
    if tools is not None:
        kwargs["tools"] = tools
    if mcp_servers is not None:
        kwargs["mcp_servers"] = mcp_servers
    if cwd is not None:
        kwargs["cwd"] = cwd
    if resume is not None:
        kwargs["resume"] = resume
    if max_turns is not None:
        kwargs["max_turns"] = max_turns

    # Thinking + temperature — pass if SDK version supports these kwargs.
    # If ClaudeAgentOptions raises on unknown kwargs, remove these and apply at the
    # anthropic.Anthropic() level instead.
    if agent_cfg.thinking.enabled:
        kwargs["thinking"] = {
            "type": "enabled",
            "budget_tokens": agent_cfg.thinking.budget_tokens,
        }
        kwargs["temperature"] = 1.0    # required by API when thinking is enabled
    elif agent_cfg.temperature is not None:
        kwargs["temperature"] = agent_cfg.temperature

    if agent_cfg.max_tokens:
        kwargs["max_tokens"] = agent_cfg.max_tokens

    return ClaudeAgentOptions(**kwargs)
```

Replace every `ClaudeAgentOptions(model=..., system_prompt=..., ...)` call in the agent files
with `_claude_options(agent_cfg, system_prompt, ...)`.

---

## Contract Proposal + Revision (Generator)

Add `propose_contract()` and `revise_contract()` to `harness/agents/generator.py`.
See `$SKILL_DIR/instructions/sprint-contracts.md` for the full negotiation protocol
(`negotiate_contract()` in harness.py wires Generator ↔ Evaluator for pre-sprint review).

Both functions always use the Claude path (via `_claude_options`) — contract negotiation
is conversational reasoning, not code generation, so Codex adds no value here.
