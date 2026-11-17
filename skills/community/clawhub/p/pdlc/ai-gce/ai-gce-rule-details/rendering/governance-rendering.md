<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Governance Rendering — AI-Agnostic GCE Output (Canonical + Per-Platform Adapters)

## Purpose

Defines how AI-GCE renders its OWN governance layer (compliance rules, hooks, agents, drift infra) into platform-native form based on `manifest.platformTargets`. GCE is **build-method-agnostic AND platform-agnostic** — it produces **canonical governance** once, then wires it per selected platform. Mirrors AI-DWG's renderer model (`rendering/renderer-model.md`), applied to governance output.

**Grounding:** Layout design Part 3E principle P2 (GCE output is AI-agnostic). Companion to DWG's renderer.

> **Scope boundary (P1):** This file governs GCE's OWN output only. GCE never renders into DWG's canonical files — it reads those (read-only). GCE writes canonical governance to `.governance/` + adapters to platform locations.

---

## MANDATORY: Stage Sub-Role — Automation Engineer

Automation Engineer mindset (one source, N packagings; deterministic wiring). ADDS a dimension — does NOT replace the primary Compliance/Governance role.

### Anti-Patterns
- Do NOT hardcode `.kiro/hooks/` as the only output — render per `platformTargets`
- Do NOT author governance content in an adapter — adapters wire canonical `.governance/` content
- Do NOT fake a capability a platform lacks — degrade to CI/CD + advisory, disclose it

---

## Canonical + Adapter Model (GCE Governance)

```
GCE derives governance (from DWG workspace, read-only)
        │
        ▼
  .governance/                       ← SINGLE canonical home for ALL GCE + TGE (P3)
   ├── GOVERNANCE_INDEX.md            AI entry point — discovers all governance machinery
   ├── engine/                        GCE + TGE core workflows (canonical, platform-neutral)
   │   ├── ai-gce/  ·  ai-tge/
   ├── rules/*.md                     compliance rules (prescriptive, MUST/NEVER)
   ├── agents/*.md                    agent specs (GCE: drift-detect, compliance-audit, … + TGE: test-governance, coverage-review)
   ├── hooks/*.json                   canonical hook definitions (platform-neutral)
   ├── drift-register.md              drift state
   ├── test/                          TGE artifacts (strategy, register, coverage, debt, defect-log, tge-state)
   ├── compliance-log/                audit trail
   └── AGENT_REGISTRY.md · AGENT-GUIDE.md
        │
        ├──▶ Kiro adapter        → .kiro/hooks/*.json + .kiro/agents/*.md  (reference .governance/)
        ├──▶ Claude Code adapter → .claude/agents/*/AGENT.md + settings.json hooks  (reference .governance/)
        ├──▶ Cursor adapter      → advisory docs + .github/workflows/ CI gates  (reference .governance/)
        ├──▶ Codex adapter       → advisory docs + CI gates  (reference .governance/)
        └──▶ Generic             → .github/workflows/ / scripts (CI only)  (reference .governance/)
```

**P3 — `.governance/` is the single home.** ALL GCE + TGE content — engine, rules, agents, hooks, logs, test artifacts, state — lives under `.governance/`. Platform adapters (`.kiro/hooks/`, `.claude/agents/`, …) are thin pointers that reference `.governance/` canonical content; they never duplicate it. `GOVERNANCE_INDEX.md` is the AI's discovery entry point (surfaced via the adapter + manifest `governance:` section).

**Invariant:** the governance CONTENT (rules, agent logic, drift infra) lives canonically in `.governance/`. Adapters are thin wiring that make the platform's AI *enforce* it. No adapter contains original governance content.

---

## Capability Matrix (GCE Output)

| GCE output | Kiro | Claude Code | Cursor | Codex | Generic |
|------------|:----:|:-----------:|:------:|:-----:|:-------:|
| Compliance rules | ✅ steering | ✅ `.claude/rules/` | ⚠️ advisory | ⚠️ advisory | ⚠️ docs |
| Audit/process agents | ✅ `.kiro/agents/` | ✅ subagents | ❌ → docs | ❌ → docs | ❌ → docs |
| Automation hooks (block on violation) | ✅ `.kiro/hooks/` | ✅ `settings.json` (exit 2) | ❌ → CI/CD | ❌ → CI/CD | ⚠️ CI/CD |
| Drift detection (`DFT__`) | ✅ agent+hook | ✅ subagent+hook | ⚠️ manual+CI | ⚠️ manual+CI | ⚠️ CI |
| Drift gate enforcement (block on unresolved HARD drift, Step 0) | ✅ hook hard-stop | ✅ `PreToolUse` exit 2 | ⚠️ CI gate | ⚠️ CI gate | ⚠️ CI gate |
| Compliance log | ✅ | ✅ | ✅ | ✅ | ✅ |

✅ native · ⚠️ degraded (advisory/CI) · ❌ not supported (→ docs/CI)

---

## Per-Platform Rendering

### Kiro
- **Rules:** `.kiro/steering/*.md` (`inclusion: fileMatch`) referencing `.governance/rules/`
- **Agents:** `.kiro/agents/{agent}.md` (compliance-audit, drift-detect, session-discipline, …) + `{XXX}__` shortcuts
- **Hooks:** `.kiro/hooks/*.json` — security-critical on `fileEdited`, advisory on `agentStop`
- **Enforcement:** automatic, event-driven — hooks can block

### Claude Code
- **Rules:** `.claude/rules/*.md` with `paths:` referencing `.governance/rules/`
- **Agents:** `.claude/agents/{agent}/AGENT.md` (isolated subagents — governance without polluting main session)
- **Hooks:** `.claude/settings.json` — `PreToolUse` (command, exit code 2 = hard block), `Stop` (drift subagent)
- **Enforcement:** deterministic hooks + isolated subagents

### Cursor
- **Rules:** `.cursor/rules/*.mdc` (globs) referencing `.governance/rules/`
- **Agents:** ❌ → `docs/governance/{agent}.md` advisory playbooks
- **Hooks:** ❌ → `.github/workflows/` CI gates (lint, compliance scan, drift-check-on-CI)
- **Enforcement:** advisory (editor) + CI/CD (pipeline)

### Codex
- **Rules:** `AGENTS.md` governance section referencing `.governance/rules/`
- **Agents/Hooks:** ❌ → advisory docs + CI/CD
- **Enforcement:** advisory + CI/CD

### Generic
- **Rules:** `.governance/rules/*.md` readable as-is + `docs/governance/` index
- **Agents/Hooks:** ❌ → `.github/workflows/` / scripts only
- **Enforcement:** CI/CD + human discipline

---

## Rendering Step (Where This Fits)

```
GCE derivation flow:
  ... derive governance from DWG workspace (read-only) → write canonical .governance/ ...
  ↓
  GOVERNANCE RENDERING STEP (this file):
    1. Read manifest.platformTargets
    2. FOR EACH target: render adapter (hooks/agents/rules wiring → references .governance/)
    3. Generate/append PLATFORM_NOTES.md for below-full-capability targets
    4. Register agent shortcuts ({XXX}__) in the platform's entry point
  ↓
  ... update AGENT_REGISTRY.md + AGENT-GUIDE.md ...
```

Multi-target: render one adapter per selected platform, all referencing the same canonical `.governance/`.

---

## Drift Infrastructure Rendering (Register + Agent + Gate)

The drift surface is three canonical artifacts under `.governance/`, rendered per platform like all other governance:

| Artifact | Canonical location | Per-platform wiring |
|----------|--------------------|---------------------|
| **Drift register** | `.governance/drift-register.md` | **Never** placed in an adapter and **never** written by any adapter/hook — GCE is the sole writer (INV-L4-006). Adapters only *read* it (gate/agent). |
| **Drift-detect agent (`DFT__`)** | `.governance/agents/drift-detect-agent.md` | Kiro → `.kiro/agents/` + **session-end `agentStop` hook** (invokes the agent at session close, silent when clean) · Claude → `.claude/agents/` subagent + **`Stop` hook** · Cursor/Codex/Generic → advisory doc + CI (manual `DFT__` / CI step). Manual `DFT__` + pre-gate work on all platforms. *(Destination session-end — NOT the internal build `SEG__`.)* |
| **Drift gate enforcement (Step 0)** | `drift/gate-integration.md` logic (blocks on `status == OPEN` HARD) | Kiro → hook hard-stop · Claude → `PreToolUse` exit 2 · Cursor/Codex/Generic → CI gate (fails pipeline on unresolved HARD drift), disclosed in `PLATFORM_NOTES.md` |

The drift-detect agent and gate wiring follow the same adapter rules as any GCE agent/hook — see the per-platform sections above. Full gate logic + platform enforcement table: `drift/gate-integration.md`.

---

## PLATFORM_NOTES.md (GCE Governance Section)

Appended to the workspace `PLATFORM_NOTES.md` (shared with DWG's disclosure):

```markdown
## Governance Enforcement (AI-GCE)
Targets: {platformTargets}

✅ Automatic (editor-level): {platforms with hooks/agents}
⚠️ CI/CD + advisory: {platforms without hooks — governance runs in pipeline + manual}

On advisory platforms, compliance rules are readable and drift detection (DFT__) is
manual/CI; hard-blocking happens at the CI gate, not the editor.
```

---

## Interaction with Other Files

| Related | Relationship |
|---------|--------------|
| `generators/hooks-from-steering.md` | Produces canonical hook logic → this file renders per platform |
| `generators/agents-from-steering.md` | Produces canonical agent specs → rendered per platform |
| `drift/*` | Drift infra is canonical governance → rendered per platform |
| `templates/agents/*` | Agent templates → placed via the platform adapter |
| (DWG `rendering/renderer-model.md`) | Same canonical+adapter model; GCE mirrors it for governance |

---

## Output Validation

- [ ] Canonical governance written to `.governance/` regardless of platform count
- [ ] One adapter rendered per selected `platformTarget`
- [ ] No adapter contains original governance content (all reference `.governance/`)
- [ ] Hooks/agents rendered natively where supported; degraded to CI/CD + advisory elsewhere
- [ ] Drift trio rendered per platform: register (`.governance/`, GCE-sole-writer, never in an adapter), drift-detect agent, gate Step-0 enforcement (`drift/gate-integration.md`)
- [ ] Drift gate blocks on unresolved HARD drift natively (Kiro/Claude) or via CI gate (Cursor/Codex/Generic), disclosed in `PLATFORM_NOTES.md`
- [ ] `PLATFORM_NOTES.md` governance section discloses degradation
- [ ] Agent shortcuts registered in each platform's entry point
- [ ] GCE never wrote into DWG's canonical files (P1 respected)
