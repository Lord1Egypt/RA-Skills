# AI-FLO — Installation Guide

## Recommended: Family Installer

The easiest way to install AI-FLO is via the AI-* Family installer (from the family root folder):

### Windows (PowerShell)
```powershell
.\installer\install.ps1 -TargetWorkspace "C:\path\to\your\project" -Platform kiro -Packages "ai-flo"
```

### macOS / Linux
```bash
./installer/install.sh --target ~/path/to/your/project --platform kiro --packages ai-flo
```

The installer places package files in the correct location for your platform and creates the family workspace (`pdlc-ws/`) where AI-FLO writes its output.

---

## What Gets Installed (Kiro example)

```
your-workspace/
├── .kiro/
│   ├── steering/
│   │   └── session-orchestrator.md           ← the ONLY always-loaded file (routes to cores)
│   └── agents/
│       ├── flo-health-check.md               ← FHC__ health check (Kiro)
│       └── flow-integrity-agent.md           ← FIA__ integrity agent (Kiro)
├── .aiflc/
│   └── pdlc/
│       ├── ai-flo-rules/core-engine.md       ← core, read on demand by the orchestrator
│       ├── ai-flo-rule-details/              ← rule details, read on demand by the core
│       ├── FAMILY_BINDINGS.md                ← fabric trio (routing graph) — REQUIRED
│       ├── GATE_PROTOCOL.md                  ← fabric trio (gate matching)  — REQUIRED
│       └── FAMILY_INTERFACE.md               ← fabric trio (discovery)      — REQUIRED
└── pdlc-ws/                                   ← AI-FLO OUTPUT lands here (created by installer)
```

> **The AIFLC model:** the session orchestrator is the only always-loaded file (it sits in Kiro's `.kiro/steering/` slot); the package core, its rule-details, and the fabric trio all live together in the uniform home `.aiflc/pdlc/`, read on demand. The `.aiflc/pdlc/` layout is identical on every platform.

> **Fabric trio (REQUIRED):** AI-FLO reads `FAMILY_BINDINGS.md`, `GATE_PROTOCOL.md`, and `FAMILY_INTERFACE.md` from `.aiflc/pdlc/` at runtime to build its routing graph. Without them FLO returns **NOT READY** — "no bindings = no routing; FLO never invents routes." The installer deploys them automatically; manual installers must copy them (see below). AI-FLO runs in the **planning / orchestration workspace** (where the lifecycle packages live), never inside an AI-DWG-generated dev workspace — so the trio belongs here, not in a generated workspace.

---

## Manual Install (Per Platform)

If you prefer manual install, copy the package core to `.aiflc/pdlc/ai-flo-rules/core-engine.md` and the rule-details to `.aiflc/pdlc/ai-flo-rule-details/` (identical on every platform), then place the **session orchestrator** — the only always-loaded file — in your platform's native slot:

| Platform | Session orchestrator (always-loaded) → |
|----------|----------------------------------------|
| Kiro | `.kiro/steering/session-orchestrator.md` |
| Amazon Q | `.amazonq/rules/pdlc/session-orchestrator.md` |
| Cursor | `.cursor/rules/pdlc-session-orchestrator.mdc` (with `alwaysApply: true` frontmatter) |
| Cline | `.clinerules/pdlc-session-orchestrator.md` |
| Claude Code | root `CLAUDE.md` importing `@CLAUDE_PDLC_ORCHESTRATOR.md` |
| Copilot | `.github/copilot-instructions.md` (orchestrator block) |
| Codex | `AGENTS.md` (orchestrator block) |

The core (`core-engine.md`) and `ai-flo-rule-details/` are plain copies under `.aiflc/pdlc/` on every platform — there are no per-package `.mdc`, `.instructions.md`, or `CLAUDE_PDLC_AI_*` files anymore.

### Manual: copy the fabric trio (REQUIRED)

After placing the core + rule-details, copy the three fabric files from the family root into `.aiflc/pdlc/` — the same uniform home, identical on every platform:

```powershell
# Windows (PowerShell)
Copy-Item "<family-root>\FAMILY_BINDINGS.md","<family-root>\GATE_PROTOCOL.md","<family-root>\FAMILY_INTERFACE.md" ".aiflc\pdlc\"
```

```bash
# macOS/Linux
cp <family-root>/FAMILY_BINDINGS.md <family-root>/GATE_PROTOCOL.md <family-root>/FAMILY_INTERFACE.md .aiflc/pdlc/
```

### Manual: install the FLO agents (Kiro)

```powershell
Copy-Item "<src>\ai-flo-rule-details\templates\agents\flo-health-check.md","<src>\ai-flo-rule-details\templates\agents\flow-integrity-agent.md" ".kiro\agents\"
```

Then add the `FHC__` / `FIA__` shortcut blocks (see `ai-flo-rule-details/templates/agents/shortcut-rules-block.md`) to your workspace rules. On non-Kiro platforms, agents are invoked via these shortcut blocks rather than an `agents/` folder.

---

## Verify

1. Open your workspace in your IDE.
2. Confirm the core file loads as steering (Kiro: check the Steering panel).
3. Run a health check: type `FHC__` in a chat. A **HEALTHY** (or **IDLE** if no project yet) verdict confirms the fabric trio resolved correctly.
4. Start a chat: "Show AI-FLO status". AI-FLO output appears under `pdlc-ws/`.

---

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| `FHC__` returns **NOT READY** / "no routing graph" | Fabric trio missing from `.aiflc/pdlc/` | Run the family installer, or copy `FAMILY_BINDINGS.md` / `GATE_PROTOCOL.md` / `FAMILY_INTERFACE.md` into `.aiflc/pdlc/` (see Manual: copy the fabric trio). |
| FLO activates but won't route | `FAMILY_BINDINGS.md` present but empty/partial | Confirm the family root copy has internal edges; regenerate if needed. |
| `FHC__` / `FIA__` not recognized | Agent files or shortcut blocks not installed | Install the agents (Kiro) or add the shortcut blocks (other platforms). |

---

## Notes

- The session orchestrator is always-loaded; the package core and rule-details load on demand.
- AI-FLO coexists with other AI-* packages — each is family-scoped under `.aiflc/pdlc/`. Install order doesn't matter; AI-FLO detects available packages by marker file.
- AI-FLO is the only cross-layer transport: it routes decisions down from AI-PPM and relays telemetry up from Project-layer packages.
- Runtime output is written under `pdlc-ws/`, never at the workspace root.

---

## Agent Installation (Optional)

The Flow Integrity Agent (`FIA__`) provides on-demand validation of routing state. Copy the agent template from the package source into your workspace agents folder:

```powershell
# Windows (PowerShell)
Copy-Item "<src>\ai-flo-rule-details\templates\agents\flow-integrity-agent.md" ".kiro\agents\"
```

```bash
# macOS/Linux
cp <src>/ai-flo-rule-details/templates/agents/flow-integrity-agent.md .kiro/agents/
```

Then add the shortcut block from `templates/agents/shortcut-rules-block.md` to your workspace steering rules. Invoke with `FIA__` in any prompt.

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "No project markers found" | Install at least one other AI-* package first (AI-PILC, AI-ADLC, etc.) |
| Routing fails silently | Verify the target package's state file exists in an accessible path |
| Core file not loading | Confirm it's in the correct steering location for your platform (see Manual Install) |
| `FIA__` shortcut not recognized | Install the Flow Integrity Agent (see Agent Installation above) |

---

## Test Mode (Optional)

AI-FLO includes a built-in **test mode** for capturing feedback (bugs, improvements, root-cause analyses) during package usage. Test mode is entirely optional and does not affect normal operation.

### Kiro IDE

Test mode ships automatically with the package's rule-details — the file lives at `.aiflc/pdlc/ai-flo-rule-details/common/test-mode.md` on every platform (Kiro included). Nothing extra is installed for Kiro.

It is **not** auto-loaded and does **not** appear in Kiro's Steering panel — nothing under `.aiflc/` auto-loads.

**To activate:** tell the active package "enable test mode" (or "load test mode"). It reads `test-mode.md` from its rule-details home on demand and starts offering the optional feedback checkpoints.

### Amazon Q Developer / Cursor / Cline / Claude Code / Copilot / Codex

No manual copy needed — `test-mode.md` is installed with the package under `.aiflc/pdlc/ai-flo-rule-details/common/`, the same on every platform.

Activate it the same way: tell the AI "enable test mode". It reads `test-mode.md` from the rule-details home on demand and starts offering the optional feedback checkpoints.

### What Test Mode Does

- Adds brief feedback checkpoints after each phase (non-blocking — always skippable)
- Assists in filling structured bug/improvement/RCA templates via conversation
- Saves findings to a local `test-feedback-outbox/` folder (gitignored, never transmitted)
- Submission to maintainers is 100% manual and opt-in

### Privacy

- ❌ No network calls, no telemetry, no data collection
- ❌ No PII fields in templates
- ✅ All data stays local until you manually submit
- ✅ Review obligation rests entirely with you (the end user)

See `TEST_MODE_USER_GUIDE.md` (in this folder) for the full user guide.
