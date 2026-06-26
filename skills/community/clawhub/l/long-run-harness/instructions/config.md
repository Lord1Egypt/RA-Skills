# Config: `config.yaml` + `config.py`

All tunable parameters live here. `config.yaml` is what the user edits; `config.py` is the
loader. Dataclass defaults are the fallback when a key is absent from the YAML.

Each agent (`planner`, `generator`, `evaluator`) has its own block with:
- `backend`: `claude` (default), `codex`, or `deepcode`
- `model`: model ID passed to the selected backend
- Claude-specific: `thinking`, `max_tokens`, `temperature`
- Codex-specific: `codex.approval_mode`, `codex.reasoning_effort`, `codex.quiet`, etc.
- Deepcode-specific: `deepcode.cli_path`, `deepcode.env`

`strategic_decision()` in the iteration loop always uses Claude — it is a meta-reasoning step,
not a file-writing step. Configure it via `loop.strategic_decision_model`.

---

## `harness/config.py` — Full Implementation

```python
from __future__ import annotations
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional
import yaml


@dataclass
class ThinkingConfig:
    enabled: bool = False
    budget_tokens: int = 8000   # ignored when enabled=False
    # Note: when enabled=True, temperature is forced to 1.0 by the API.
    # The API also requires betas=["interleaved-thinking-2025-05-14"] — pass via ClaudeAgentOptions
    # extra kwargs if the SDK version does not expose it natively.


@dataclass
class CodexSettings:
    approval_mode: str = "full-auto"    # suggest | auto-edit | full-auto
    quiet: bool = True                  # suppress interactive UI output
    reasoning_effort: str = "medium"    # low | medium | high — o-series models only
    provider: str = "openai"            # openai | azure | anthropic | gemini | ...
    # ⚠️  Verify exact flag names with `codex --help` — the CLI evolves quickly.
    # extra_args are passed verbatim after all other flags, before the prompt.
    extra_args: list = field(default_factory=list)


@dataclass
class DeepcodeSettings:
    # Local wrapper that runs Claude Code 2.1.153 against DeepSeek.
    cli_path: str = "/Users/xzhao/.local/bin/deepcode"
    env: dict[str, str] = field(default_factory=dict)


@dataclass
class SingleAgentConfig:
    backend: str = "claude"                  # claude | codex | deepcode
    model: str = ""                          # model ID; empty string = per-agent default
    max_tokens: int = 8192                   # Claude only; Codex ignores this
    temperature: Optional[float] = None      # Claude only; None = API default
                                             # ignored (forced to 1.0) when thinking.enabled
    thinking: ThinkingConfig = field(default_factory=ThinkingConfig)
    codex: CodexSettings = field(default_factory=CodexSettings)
    deepcode: DeepcodeSettings = field(default_factory=DeepcodeSettings)
    # Generator only: self_assess always runs via Claude, regardless of generator backend.
    # This is the model used for that internal Claude call.
    self_assess_model: str = "claude-haiku-4-5-20251001"

    @classmethod
    def _from_dict(cls, d: dict) -> "SingleAgentConfig":
        return cls(
            backend=d.get("backend", "claude"),
            model=d.get("model", ""),
            max_tokens=d.get("max_tokens", 8192),
            temperature=d.get("temperature", None),
            thinking=ThinkingConfig(**d.get("thinking", {})),
            codex=CodexSettings(**d.get("codex", {})),
            deepcode=DeepcodeSettings(**d.get("deepcode", {})),
            self_assess_model=d.get("self_assess_model", "claude-haiku-4-5-20251001"),
        )


# Default models per agent when model field is empty:
_DEFAULTS = {
    "planner":   "claude-haiku-4-5-20251001",
    "generator": "claude-opus-4-7",
    "evaluator": "claude-opus-4-7",
}


@dataclass
class AgentConfig:
    planner: SingleAgentConfig = field(default_factory=lambda: SingleAgentConfig(
        backend="claude", model=_DEFAULTS["planner"]
    ))
    generator: SingleAgentConfig = field(default_factory=lambda: SingleAgentConfig(
        backend="claude", model=_DEFAULTS["generator"]
    ))
    evaluator: SingleAgentConfig = field(default_factory=lambda: SingleAgentConfig(
        backend="claude", model=_DEFAULTS["evaluator"]
    ))

    @classmethod
    def _from_dict(cls, d: dict) -> "AgentConfig":
        def _load(key: str) -> SingleAgentConfig:
            raw = d.get(key, {})
            cfg = SingleAgentConfig._from_dict(raw)
            if not cfg.model:
                cfg.model = _DEFAULTS[key]
            return cfg
        return cls(planner=_load("planner"), generator=_load("generator"), evaluator=_load("evaluator"))


@dataclass
class LoopConfig:
    max_iterations: int = 15
    min_iterations: int = 5
    generator_timeout_seconds: int = 1500
    contract_review_rounds: int = 2
    # strategic_decision() always uses Claude — it is meta-reasoning, not code generation.
    strategic_decision_model: str = "claude-opus-4-7"


@dataclass
class VerdictConfig:
    pass_threshold: float = 3.0
    conditional_pass_threshold: float = 2.0


@dataclass
class WorkspaceGitConfig:
    enabled: bool = True
    strategy: str = "path-scoped"  # disabled | path-scoped | all


@dataclass
class WorkspaceConfig:
    mode: str = "greenfield"       # greenfield | existing-codebase | production-qa
    app_root: str = "src"          # greenfield: src; existing-codebase: . or service root
    artifact_root: str = "harness-state"
    log_root: str = "harness-logs"
    evidence_root: str = "harness-state/evidence"
    tmp_root: str = "harness-state/tmp"
    keep_last_runs: int = 10
    keep_last_evidence_per_sprint: int = 3
    write_allowlist: list[str] = field(default_factory=lambda: ["src/**", "package.json", "package-lock.json"])
    protected_paths: list[str] = field(default_factory=lambda: [
        ".git/**", ".env", ".env.*", "node_modules/**", ".next/**",
        "dist/**", "build/**", "harness-state/**", "harness-logs/**",
    ])
    git: WorkspaceGitConfig = field(default_factory=WorkspaceGitConfig)

    @classmethod
    def _from_dict(cls, d: dict) -> "WorkspaceConfig":
        d = d or {}
        git_raw = d.get("git") or {}
        return cls(
            mode=d.get("mode", "greenfield"),
            app_root=d.get("app_root", "src"),
            artifact_root=d.get("artifact_root", "harness-state"),
            log_root=d.get("log_root", "harness-logs"),
            evidence_root=d.get("evidence_root", "harness-state/evidence"),
            tmp_root=d.get("tmp_root", "harness-state/tmp"),
            keep_last_runs=d.get("keep_last_runs", 10),
            keep_last_evidence_per_sprint=d.get("keep_last_evidence_per_sprint", 3),
            write_allowlist=d.get("write_allowlist") or ["src/**", "package.json", "package-lock.json"],
            protected_paths=d.get("protected_paths") or [
                ".git/**", ".env", ".env.*", "node_modules/**", ".next/**",
                "dist/**", "build/**", "harness-state/**", "harness-logs/**",
            ],
            git=WorkspaceGitConfig(**git_raw),
        )


@dataclass
class HarnessConfig:
    agents: AgentConfig = field(default_factory=AgentConfig)
    loop: LoopConfig = field(default_factory=LoopConfig)
    verdict: VerdictConfig = field(default_factory=VerdictConfig)
    workspace: WorkspaceConfig = field(default_factory=WorkspaceConfig)

    @classmethod
    def load(cls, path: Path) -> "HarnessConfig":
        data = yaml.safe_load(path.read_text())
        return cls(
            agents=AgentConfig._from_dict(data.get("agents", {})),
            loop=LoopConfig(**data.get("loop", {})),
            verdict=VerdictConfig(**data.get("verdict", {})),
            workspace=WorkspaceConfig._from_dict(data.get("workspace", {})),
        )
```

---

## `harness/config.yaml` — Starter Template (all Claude)

```yaml
# harness/config.yaml
# Edit this file to tune the harness. All keys are optional — omit any to use the default.

agents:
  planner:
    backend: claude
    model: claude-haiku-4-5-20251001
    max_tokens: 4096
    # temperature: 0.7   # uncomment to override API default

  generator:
    backend: claude
    model: claude-opus-4-7
    max_tokens: 16384
    thinking:
      enabled: false
      budget_tokens: 10000    # active only when enabled: true
    # self_assess always runs via Claude even when backend: codex
    self_assess_model: claude-haiku-4-5-20251001

  evaluator:
    backend: claude
    model: claude-opus-4-7
    max_tokens: 8192
    thinking:
      enabled: false
      budget_tokens: 10000

loop:
  max_iterations: 15
  min_iterations: 5
  generator_timeout_seconds: 1500
  contract_review_rounds: 2
  strategic_decision_model: claude-opus-4-7   # always Claude; not swappable

verdict:
  pass_threshold: 3.0
  conditional_pass_threshold: 2.0

workspace:
  mode: greenfield
  app_root: src
  artifact_root: harness-state
  log_root: harness-logs
  evidence_root: harness-state/evidence
  tmp_root: harness-state/tmp
  keep_last_runs: 10
  keep_last_evidence_per_sprint: 3
  write_allowlist:
    - src/**
    - package.json
    - package-lock.json
  protected_paths:
    - .git/**
    - .env
    - .env.*
    - node_modules/**
    - .next/**
    - dist/**
    - build/**
    - harness-state/**
    - harness-logs/**
  git:
    enabled: true
    strategy: path-scoped
```

---

## `harness/config.yaml` — Mixed Backend Example (Codex generator)

```yaml
# Codex handles code generation; Claude handles planning, evaluation, and meta-reasoning.

agents:
  planner:
    backend: claude
    model: claude-haiku-4-5-20251001
    max_tokens: 4096

  generator:
    backend: codex
    model: o4-mini              # passed as --model to Codex CLI
    codex:
      approval_mode: full-auto  # full-auto required for headless operation
      quiet: true               # suppress interactive TUI
      reasoning_effort: high    # low | medium | high — o-series models only
      provider: openai
      # extra_args: ["--no-git-add"]  # passthrough CLI flags if needed
    self_assess_model: claude-haiku-4-5-20251001   # self_assess always Claude

  evaluator:
    backend: claude
    model: claude-opus-4-7
    max_tokens: 8192
    thinking:
      enabled: true             # extended thinking improves evaluation thoroughness
      budget_tokens: 10000

loop:
  max_iterations: 15
  min_iterations: 5
  generator_timeout_seconds: 1800   # Codex may need more time than Claude
  strategic_decision_model: claude-opus-4-7

verdict:
  pass_threshold: 3.0
  conditional_pass_threshold: 2.0

workspace:
  mode: existing-codebase
  app_root: .
  artifact_root: harness-state
  log_root: harness-logs
  evidence_root: harness-state/evidence
  tmp_root: harness-state/tmp
  write_allowlist:
    - src/**
    - prisma/**
    - scripts/**
    - tests/**
    - package.json
    - package-lock.json
  protected_paths:
    - .git/**
    - .env
    - .env.*
    - node_modules/**
    - .next/**
    - harness-state/**
    - harness-logs/**
  git:
    enabled: false
    strategy: disabled
```

---

## `harness/config.yaml` — Deepcode Backend Example

```yaml
# Deepcode runs Claude Code 2.1.153 via /Users/xzhao/.local/bin/deepcode,
# backed by DeepSeek. The wrapper reads DEEPSEEK_API_KEY from env.

agents:
  planner:
    backend: claude
    model: claude-haiku-4-5-20251001

  generator:
    backend: deepcode
    model: deepseek-v4-pro[1m]
    deepcode:
      cli_path: /Users/xzhao/.local/bin/deepcode
      env:
        DEEPSEEK_API_KEY: "${DEEPSEEK_API_KEY}"
    self_assess_model: claude-haiku-4-5-20251001

  evaluator:
    backend: claude
    model: claude-opus-4-7
```

For `deepcode`, use `claude_agent_sdk` exactly like the Claude backend, but set
`ClaudeAgentOptions(cli_path=agent_cfg.deepcode.cli_path, env={...})`. Do not run `deepcode` as
an arbitrary subprocess; the point is to preserve Claude SDK behavior while swapping the
underlying Claude Code executable/provider.

---

## Usage Rules

1. **Load once at startup, pass down as `cfg`** — every agent function takes
   `cfg: HarnessConfig | None = None`. Pass `None` in unit tests; defaults kick in.

2. **Never hardcode model names** — use `cfg.agents.generator.model`, never `"claude-opus-4-7"`.
   The new per-agent config is `cfg.agents.<agent>.<field>`, not flat `cfg.agents.<agent>_model`.

3. **Check backend before building options** — agent files dispatch on `cfg.agents.<agent>.backend`.
   The helper in `agent-patterns.md` shows the full dispatch pattern.

4. **`strategic_decision()` is always Claude** — it reasons about trend data, not code. Use
   `cfg.loop.strategic_decision_model` for its model, not `cfg.agents.generator.model`.

5. **`self_assess()` is always Claude** — even when generator backend is `codex`, self_assess
   runs a fresh Claude call using `cfg.agents.generator.self_assess_model`.

6. **Thinking + temperature** — when `thinking.enabled: true`, the API forces `temperature=1.0`.
   Set `temperature: null` (or omit it) whenever thinking is enabled; the agent code enforces this.

7. **Verdict thresholds are harness logic** — use `cfg.verdict.*` when computing verdict in harness
   code. Never trust the LLM's `verdict` string field from `submit_grade`.

8. **Workspace config owns every artifact path** — do not hardcode `harness-state`,
   `harness-logs`, screenshot directories, Lighthouse output paths, or temp folders in agent code.
   Build them from `cfg.workspace.*`.

9. **Mode controls cwd and git behavior** — `greenfield` uses `project_dir / app_root` as the
   Generator cwd. `existing-codebase` and `production-qa` may use repo/service root but must enforce
   `write_allowlist`, `protected_paths`, and the configured git strategy.

10. **Deepcode backend is still Claude SDK** — use `ClaudeAgentOptions(cli_path=...)`; require
    `DEEPSEEK_API_KEY`; keep the user's default `claude` untouched.

---

## Extending for New Parameters

Add a new sub-dataclass if a group of parameters belongs to a new concern:

```python
@dataclass
class OutputConfig:
    keep_last_n_logs: int = 10
    checkpoint_every_n_iterations: int = 1

@dataclass
class HarnessConfig:
    agents: AgentConfig = field(default_factory=AgentConfig)
    loop: LoopConfig = field(default_factory=LoopConfig)
    verdict: VerdictConfig = field(default_factory=VerdictConfig)
    output: OutputConfig = field(default_factory=OutputConfig)

    @classmethod
    def load(cls, path: Path) -> "HarnessConfig":
        data = yaml.safe_load(path.read_text())
        return cls(
            agents=AgentConfig._from_dict(data.get("agents", {})),
            loop=LoopConfig(**data.get("loop", {})),
            verdict=VerdictConfig(**data.get("verdict", {})),
            output=OutputConfig(**data.get("output", {})),
        )
```
