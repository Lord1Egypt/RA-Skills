# OpenForge Changelog

## v2.0.0 — 2026-03-25 — Clean Rebuild

**Breaking change: complete rewrite.** v1 is incompatible with v2. PRDs must be reformatted.

### What changed

**Architecture**
- Removed Python CLI dependency entirely — OpenForge now runs as a pure agent skill using native OpenClaw tools (`sessions_spawn`, `exec`, `read`, `write`)
- No install step, no `uv`, no custom agent registration required
- Removed all external scripts (`scripts/`, `pkg/`, `config/`) — skill is now self-contained in SKILL.md

**Parallel execution**
- Phases tagged `[parallel]` with no unmet dependencies now spawn simultaneously as sub-agents
- Dependency graph evaluation determines each "wave" of phases that can run at once
- v1 was strictly sequential — no parallelism at all

**Review-to-fix loop**
- Review phases (`Type: review`) now trigger an automatic fix cycle when findings include Blocking or Required Changes items
- Fix sub-agent is spawned with the findings as context; review re-runs after fixes
- Loop repeats up to 3 cycles before escalating
- v1 produced review findings with no automatic remediation

**Model routing**
- Simplified alias system: `haiku` / `sonnet` / `gpt` / `opus`
- Aliases map to whatever models are configured in the OpenClaw instance
- No hardcoded agent names; no registration step
- v1 required agents to be pre-registered in `~/.openclaw/openclaw.json` by name

**Quality gates**
- Gate commands run after every phase via `exec`
- Failures trigger retries with failure output passed as context
- `Max-Retries` per phase (default: 2)
- v1 had per-task `check:` commands but no retry loop

**Security**
- Removed complex secret-scanning and redaction pipeline (which provided false confidence)
- Replaced with clear security contract: PRDs are trusted input; don't put secrets in them
- Removed scope-enforcement (declared `produces:` paths) — not enforceable without a sandbox
- Removed atomic config write/restore for agent workspace manipulation (no longer needed)
- Honest about what OpenForge cannot protect against

**Escalation**
- Structured escalation message with specific failure reason, retry history, and recommended next step
- Triggers on: gate exhaustion, review loop exhaustion, PRD parse error, sub-agent unrecoverable error

### What was removed

- `scripts/install.sh` — no longer needed
- `scripts/openforge` CLI — replaced by agent execution loop
- `pkg/` Python package
- `config/agents.example.json` — no agent registration required
- `references/` directory (prd-format.md, model-routing.md, security.md) — consolidated into SKILL.md
- `templates/` directory — examples are now inline in SKILL.md
- INSTALL.md
- Exit code table (CLI-specific)
- Learning accumulation feature (stateful; requires persistent storage not available in sub-agents)
- Auto-commit feature (opinionated; removed to reduce footprint)
- Scope enforcement (`produces:` paths) — not enforceable without OS-level sandbox

### Migration from v1

v1 PRDs used YAML blocks for task configuration. v2 uses markdown headers and bullet lists.

**v1 task block:**
```yaml
```task
id: build-routes
executor: cloud
reads: [src/routes/]
produces: [src/routes/export.ts]
checks: [npm run build]
```
```

**v2 equivalent:**
```markdown
### Phase: build-routes
**Model:** sonnet
**Tasks:**
- Create the route handler in `src/routes/export.ts`

**Gate:** `npm run build`
```

---

## v1.1.0 — Security hardening (superseded)

- Secret scanning and redaction before prompt dispatch
- Atomic config write/restore for agent workspace
- Expanded secret file pattern list

## v1.0.0 — Initial release (superseded)

- Python CLI with `validate`, `plan`, `run`, `resume`, `status`, `list` commands
- Sequential phase execution
- Per-task quality checks
- Learning accumulation
- Auto-commit on task success
- Scope enforcement via `produces:` paths
