# AI-DFE — Installation

**Package:** AI-DFE — AI-Driven Data Fabric
**Version:** 1.0.0

AI-DFE is the data layer for the AI-* PDLC Family. It installs like the other family packages — one always-loaded session orchestrator in the platform's native slot, with the engine core and its rule-details in the uniform home `.aiflc/pdlc/`, read on demand — plus a one-time bootstrap of its runtime territory.

---

## Kiro (reference platform)

Kiro auto-loads steering only from `.kiro/steering/`. Under the AIFLC model the only always-loaded file is the **session orchestrator**; the engine core and its rule-details live in the uniform home `.aiflc/pdlc/`, read on demand:

```
{AIFLC-workspace-root}/
├── .kiro/
│   └── steering/
│       └── session-orchestrator.md         ← the ONLY always-loaded file (routes to cores)
└── .aiflc/
    └── pdlc/
        ├── ai-dfe-rules/
        │   └── core-engine.md              ← the engine, read on demand by the orchestrator
        └── ai-dfe-rule-details/            ← on-demand (stages, templates, data-schema)
            ├── common/  configure/  operate/  govern/
            ├── data-schema/
            └── templates/
```

**Steps:**
1. Copy `ai-dfe-rules/` → `.aiflc/pdlc/ai-dfe-rules/` and `ai-dfe-rule-details/` → `.aiflc/pdlc/ai-dfe-rule-details/`.
2. Copy the session orchestrator into Kiro's auto-load slot → `.kiro/steering/session-orchestrator.md` (the only always-loaded file).
3. **Install the agents:** copy `ai-dfe-rule-details/templates/agents/data-fabric-health-check.md` and `ai-dfe-rule-details/templates/agents/data-fabric-agent.md` → `.kiro/agents/`.
4. **Register the shortcuts:** append `ai-dfe-rule-details/templates/agents/shortcut-rules-block.md` (between its `<!-- BEGIN/END AI-DFE AGENT SHORTCUTS -->` markers) into `.kiro/steering/workspace-rules.md` — registers both `DHC__` and `DFA__`.
5. **Bootstrap territory:** ensure `pdlc-ws/data/` exists with an empty `REGISTRY.json`, an empty `CONSUMER_REGISTRY.md` (copy from `ai-dfe-rule-details/templates/CONSUMER_REGISTRY.md`, no rows), a template `dfe-state.md`, and empty `demands/` and `history/` folders. (The family installer already does this; create them manually only if running standalone.)
6. Run `DHC__` to confirm readiness, then `DAT__ all` to populate the data surface.

> The runtime `data/` folder starts **empty**. Generic sample data ships inside this package at `ai-dfe-rule-details/templates/data-samples/` for reference/testing — it is never copied into the runtime folder.

---

## Other Platforms

The engine core (`.aiflc/pdlc/ai-dfe-rules/core-engine.md`) and rule-details (`.aiflc/pdlc/ai-dfe-rule-details/`) are identical on every platform — only the always-loaded **session orchestrator** goes in each platform's native slot:

| Platform | Session orchestrator (always-loaded) location |
|----------|-----------------------------------------------|
| Amazon Q | `.amazonq/rules/pdlc/session-orchestrator.md` |
| Cursor | `.cursor/rules/pdlc-session-orchestrator.mdc` (with `alwaysApply: true` frontmatter) |
| Cline | `.clinerules/pdlc-session-orchestrator.md` |
| Claude Code | root `CLAUDE.md` importing `@CLAUDE_PDLC_ORCHESTRATOR.md` |
| Copilot | `.github/copilot-instructions.md` (orchestrator block) |
| Codex | `AGENTS.md` (orchestrator block) |

Runtime paths inside the rules are workspace-root-relative (`pdlc-ws/data/…`), so they resolve identically regardless of where the package files land. Follow the family-level `INSTALL_GUIDE_*.md` for the verified per-platform path table.

---

## Verify

After install:
- `_DFE_` activates AI-DFE (first line reports `Active package: AI-DFE`).
- `DHC__` runs the readiness health check and returns a verdict (HEALTHY / DEGRADED / NOT READY / IDLE).
- `DAT__ status` reports per-package freshness.
- `DFA__` runs a read-only integrity pass (18 checks / 5 categories).
- `DAT__ all` produces `pdlc-ws/data/REGISTRY.json` + per-package `{pkg}-data.json`.
