# AI-ILC — Installation Guide

## Recommended: Family Installer

The easiest way to install AI-ILC is via the AI-* Family installer (from the family root folder):

### Windows (PowerShell)
```powershell
.\installer\install.ps1 -TargetWorkspace "C:\path\to\your\project" -Platform kiro -Packages "ai-ilc"
```

### macOS / Linux
```bash
./installer/install.sh --target ~/path/to/your/project --platform kiro --packages ai-ilc
```

The installer places package files in the correct location for your platform and creates the family workspace (`pdlc-ws/`) where AI-ILC writes its output.

---

## What Gets Installed (Kiro example)

```
your-workspace/
├── .kiro/
│   └── steering/
│       └── session-orchestrator.md         ← the ONLY always-loaded file (routes to cores)
├── .aiflc/
│   └── pdlc/
│       ├── ai-ilc-rules/core-workflow.md   ← core, read on demand by the orchestrator
│       └── ai-ilc-rule-details/            ← rule details, read on demand by the core
└── pdlc-ws/                                 ← AI-ILC OUTPUT lands here (created by installer)
```

> **The AIFLC model:** the session orchestrator is the only always-loaded file (it sits in Kiro's `.kiro/steering/` slot); the package core and its rule-details live together in the uniform home `.aiflc/pdlc/`, read on demand. The `.aiflc/pdlc/` layout is identical on every platform.

---

## Manual Install (Per Platform)

If you prefer manual install, copy the package core to `.aiflc/pdlc/ai-ilc-rules/core-workflow.md` and the rule-details to `.aiflc/pdlc/ai-ilc-rule-details/` (identical on every platform), then place the **session orchestrator** — the only always-loaded file — in your platform's native slot:

| Platform | Session orchestrator (always-loaded) → |
|----------|----------------------------------------|
| Kiro | `.kiro/steering/session-orchestrator.md` |
| Amazon Q | `.amazonq/rules/pdlc/session-orchestrator.md` |
| Cursor | `.cursor/rules/pdlc-session-orchestrator.mdc` (with `alwaysApply: true` frontmatter) |
| Cline | `.clinerules/pdlc-session-orchestrator.md` |
| Claude Code | root `CLAUDE.md` importing `@CLAUDE_PDLC_ORCHESTRATOR.md` |
| Copilot | `.github/copilot-instructions.md` (orchestrator block) |
| Codex | `AGENTS.md` (orchestrator block) |

The core (`core-workflow.md`) and `ai-ilc-rule-details/` are plain copies under `.aiflc/pdlc/` on every platform — there are no per-package `.mdc`, `.instructions.md`, or `CLAUDE_PDLC_AI_*` files anymore.

---

## Verify

1. Open your workspace in your IDE.
2. Confirm the core file loads as steering (Kiro: check the Steering panel).
3. Start a chat: "Using AI-ILC, help me ...".
4. AI-ILC output appears under `pdlc-ws/`.

---

## Notes

- The session orchestrator is always-loaded; the package core and rule-details load on demand.
- AI-ILC coexists with other AI-* packages — each is family-scoped under `.aiflc/pdlc/`.
- Runtime output is written under `pdlc-ws/`, never at the workspace root.

---

## Using AI-ILC

After installation, these phrases activate the workflow:

| Say | Effect |
|-----|--------|
| "I have an idea" | Start new idea capture |
| "I have a new idea for..." | Start capture with initial context |
| "Resume" | Continue a previously-started idea |
| "Show the idea register" | Display all ideas in the pipeline |
| "Revisit parked idea" | Re-enter a parked idea |

---

## Configuration (Optional)

### Custom Evaluation Rubric

If your organization wants custom scoring criteria, create a config file at `.aiflc/pdlc/ilc-evaluation-config.md` and define custom criteria there. AI-ILC's two-source model will use your criteria where provided and fall back to the built-in baseline where you're silent.

### Persona Steering (Optional)

If you want AI-ILC's personas to use your organization's voice/style, ensure the relevant persona files are in your `.kiro/steering/` folder. AI-ILC references `#persona-product-manager` (lead at most stages), `#persona-process-designer` (lead at Scope), and sub-roles: business-analyst, financial-analyst, resource-planner, risk-analyst, change-manager.

---

## Test Mode (Optional)

AI-ILC includes a built-in **test mode** for capturing feedback (bugs, improvements, root-cause analyses) during package usage. Test mode is entirely optional and does not affect normal operation.

### Kiro IDE

Test mode ships automatically with the package's rule-details — the file lives at `.aiflc/pdlc/ai-ilc-rule-details/common/test-mode.md` on every platform (Kiro included). Nothing extra is installed for Kiro.

It is **not** auto-loaded and does **not** appear in Kiro's Steering panel — nothing under `.aiflc/` auto-loads.

**To activate:** tell the active package "enable test mode" (or "load test mode"). It reads `test-mode.md` from its rule-details home on demand and starts offering the optional feedback checkpoints.

### Amazon Q Developer / Cursor / Cline / Claude Code / Copilot / Codex

No manual copy needed — `test-mode.md` is installed with the package under `.aiflc/pdlc/ai-ilc-rule-details/common/`, the same on every platform.

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
