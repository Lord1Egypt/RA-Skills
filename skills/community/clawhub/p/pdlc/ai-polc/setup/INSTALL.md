# AI-POLC — Installation Guide

## Recommended: Family Installer

The easiest way to install AI-POLC is via the AI-* Family installer (from the family root folder):

### Windows (PowerShell)
```powershell
.\installer\install.ps1 -TargetWorkspace "C:\path\to\your\project" -Platform kiro -Packages "ai-polc"
```

### macOS / Linux
```bash
./installer/install.sh --target ~/path/to/your/project --platform kiro --packages ai-polc
```

The installer places package files in the correct location for your platform and creates the family workspace (`pdlc-ws/`) where AI-POLC writes its output.

---

## What Gets Installed (Kiro example)

```
your-workspace/
├── .kiro/
│   └── steering/
│       └── session-orchestrator.md          ← the ONLY always-loaded file (routes to cores)
├── .aiflc/
│   └── pdlc/
│       ├── ai-polc-rules/core-workflow.md   ← core, read on demand by the orchestrator
│       └── ai-polc-rule-details/            ← rule details, read on demand by the core
└── pdlc-ws/                                  ← AI-POLC OUTPUT lands here (created by installer)
```

> **The AIFLC model:** the session orchestrator is the only always-loaded file (it sits in Kiro's `.kiro/steering/` slot); the package core and its rule-details live together in the uniform home `.aiflc/pdlc/`, read on demand. The `.aiflc/pdlc/` layout is identical on every platform.

---

## Manual Install (Per Platform)

If you prefer manual install, copy the package core to `.aiflc/pdlc/ai-polc-rules/core-workflow.md` and the rule-details to `.aiflc/pdlc/ai-polc-rule-details/` (identical on every platform), then place the **session orchestrator** — the only always-loaded file — in your platform's native slot:

| Platform | Session orchestrator (always-loaded) → |
|----------|----------------------------------------|
| Kiro | `.kiro/steering/session-orchestrator.md` |
| Amazon Q | `.amazonq/rules/pdlc/session-orchestrator.md` |
| Cursor | `.cursor/rules/pdlc-session-orchestrator.mdc` (with `alwaysApply: true` frontmatter) |
| Cline | `.clinerules/pdlc-session-orchestrator.md` |
| Claude Code | root `CLAUDE.md` importing `@CLAUDE_PDLC_ORCHESTRATOR.md` |
| Copilot | `.github/copilot-instructions.md` (orchestrator block) |
| Codex | `AGENTS.md` (orchestrator block) |

The core (`core-workflow.md`) and `ai-polc-rule-details/` are plain copies under `.aiflc/pdlc/` on every platform — there are no per-package `.mdc`, `.instructions.md`, or `CLAUDE_PDLC_AI_*` files anymore.

---

## Verify

1. Open your workspace in your IDE.
2. Confirm the core file loads as steering (Kiro: check the Steering panel).
3. Start a chat: "Start the AI-POLC workflow for product ownership".
4. AI-POLC output appears under `pdlc-ws/`.

---

## Notes

- The session orchestrator is always-loaded; the package core and rule-details load on demand.
- AI-POLC coexists with other AI-* packages — each is family-scoped under `.aiflc/pdlc/`. It can consume PIP (AI-PILC) and/or AP (AI-ADLC) as input and produces a Product Backlog Package (PBP).
- Runtime output is written under `pdlc-ws/`, never at the workspace root.

---

## Usage

### New Product (Cold Start)

```
Start the AI-POLC workflow for product ownership.
My product is: {product name}
```

AI-POLC will display the welcome message and begin Stage 1 (Workspace Detection).

### Chain Mode (After AI-PILC / AI-ADLC)

```
Start the AI-POLC workflow. I have upstream output:
- PIP location: <path-to-pip-output>
- Architecture Package: <path-to-ap-output>
```

AI-POLC will detect `pilc-state.md` / `adlc-state.md` and enter chain mode automatically.

### Resume Session

```
Resume my AI-POLC session.
```

AI-POLC will read `polc-state.md`, scan for upstream changes, and continue from where you left off.

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| AI doesn't recognize workflow | Verify the core file is in a steering/rules path the AI reads (see Manual Install) |
| "File not found" errors | Check that the `ai-polc-rule-details/` folder is at the correct location for your platform |
| Template errors | Ensure the `templates/` folder was copied completely (17 files) |
| Chain mode not detecting upstream | Verify predecessor marker files exist (`pilc-state.md`, `adlc-state.md`) in an accessible path |
| Extensions not activating | Say the trigger phrase (e.g., "full traceability") or check context factors |
| Welcome message re-displays | Delete or check `polc-state.md` — its presence suppresses the welcome |

---

## Test Mode (Optional)

AI-POLC includes a built-in **test mode** for capturing feedback (bugs, improvements, root-cause analyses) during package usage. Test mode is entirely optional and does not affect normal operation.

### Kiro IDE

Test mode ships automatically with the package's rule-details — the file lives at `.aiflc/pdlc/ai-polc-rule-details/common/test-mode.md` on every platform (Kiro included). Nothing extra is installed for Kiro.

It is **not** auto-loaded and does **not** appear in Kiro's Steering panel — nothing under `.aiflc/` auto-loads.

**To activate:** tell the active package "enable test mode" (or "load test mode"). It reads `test-mode.md` from its rule-details home on demand and starts offering the optional feedback checkpoints.

### Amazon Q Developer / Cursor / Cline / Claude Code / Copilot / Codex

No manual copy needed — `test-mode.md` is installed with the package under `.aiflc/pdlc/ai-polc-rule-details/common/`, the same on every platform.

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
