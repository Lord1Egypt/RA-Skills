# AI-GCE — Installation Guide

## Recommended: Family Installer

The easiest way to install AI-GCE is via the AI-* Family installer (from the family root folder):

### Windows (PowerShell)
```powershell
.\installer\install.ps1 -TargetWorkspace "C:\path\to\your\project" -Platform kiro -Packages "ai-gce"
```

### macOS / Linux
```bash
./installer/install.sh --target ~/path/to/your/project --platform kiro --packages ai-gce
```

The installer places package files in the correct location for your platform and creates the family workspace (`pdlc-ws/`) where AI-GCE writes its output.

---

## What Gets Installed (Kiro example)

```
your-workspace/
├── .kiro/
│   └── steering/
│       └── session-orchestrator.md           ← the ONLY always-loaded file (routes to cores)
├── .aiflc/
│   └── pdlc/
│       ├── ai-gce-rules/core-generator.md   ← core, read on demand by the orchestrator
│       └── ai-gce-rule-details/             ← rule details, read on demand by the core
└── pdlc-ws/                                  ← AI-GCE OUTPUT lands here (created by installer)
```

> **The AIFLC model:** the session orchestrator is the only always-loaded file (it sits in Kiro's `.kiro/steering/` slot); the package core and its rule-details live together in the uniform home `.aiflc/pdlc/`, read on demand. The `.aiflc/pdlc/` layout is identical on every platform.

---

## Manual Install (Per Platform)

If you prefer manual install, copy the package core to `.aiflc/pdlc/ai-gce-rules/core-generator.md` and the rule-details to `.aiflc/pdlc/ai-gce-rule-details/` (identical on every platform), then place the **session orchestrator** — the only always-loaded file — in your platform's native slot:

| Platform | Session orchestrator (always-loaded) → |
|----------|----------------------------------------|
| Kiro | `.kiro/steering/session-orchestrator.md` |
| Amazon Q | `.amazonq/rules/pdlc/session-orchestrator.md` |
| Cursor | `.cursor/rules/pdlc-session-orchestrator.mdc` (with `alwaysApply: true` frontmatter) |
| Cline | `.clinerules/pdlc-session-orchestrator.md` |
| Claude Code | root `CLAUDE.md` importing `@CLAUDE_PDLC_ORCHESTRATOR.md` |
| Copilot | `.github/copilot-instructions.md` (orchestrator block) |
| Codex | `AGENTS.md` (orchestrator block) |

The core (`core-generator.md`) and `ai-gce-rule-details/` are plain copies under `.aiflc/pdlc/` on every platform — there are no per-package `.mdc`, `.instructions.md`, or `CLAUDE_PDLC_AI_*` files anymore.

---

## Verify

1. Open your workspace in your IDE.
2. Confirm the core file loads as steering (Kiro: check the Steering panel).
3. Start a chat: "Using AI-GCE, generate the compliance engine for this workspace".
4. AI-GCE output appears under `pdlc-ws/`.

---

## Notes

- The session orchestrator is always-loaded; the package core and rule-details load on demand.
- AI-GCE coexists with other AI-* packages — each is family-scoped under `.aiflc/pdlc/`. Run AI-DWG first to generate the development workspace, then AI-GCE to derive compliance.
- AI-GCE reads existing steering files but never modifies them.
- Runtime output is written under `pdlc-ws/`, never at the workspace root.

---

## Input Prerequisites

AI-GCE derives a compliance layer by reading an AI-DWG development workspace. For full derivation it expects these steering files in the target workspace:

- `rules/workspace-rules.md` (marker file — MUST exist)
- `rules/tech-stack.md` (technology drives hook patterns)
- `rules/module-structure.md` (module paths drive hook patterns)

Without these, AI-GCE can only apply the 10 built-in baseline rules.

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| AI doesn't find rule-details | Ensure the rule-details folder is at the correct location for your platform (see Manual Install) |
| "No steering files found" | Ensure `rules/workspace-rules.md` exists (minimum requirement) |
| Only baseline rules generated | Steering files are missing or incomplete — add `tech-stack.md` and `module-structure.md` for full derivation |
| Hooks not firing | Check `.governance/hooks/ENFORCEMENT-GUIDE.md` for tier-based activation instructions |
| Re-derivation overwrites customs | Ensure team-added rules are marked with `<!-- custom -->` comments |

---

## Uninstallation

To remove AI-GCE generated output from a workspace (does NOT affect steering files from AI-DWG):

```powershell
# Windows (PowerShell)
Remove-Item -Recurse -Force ".kiro\hooks"
Remove-Item -Recurse -Force ".governance"
Remove-Item -Force ".compliance-state.json"
Remove-Item -Force "docs\compliance-dashboard.md"
```

```bash
# macOS/Linux
rm -rf .governance/hooks/
rm -rf .governance/
rm -f .compliance-state.json
rm -f management_framework/dashboards/compliance-dashboard.md
```

---

## Test Mode (Optional)

AI-GCE includes a built-in **test mode** for capturing feedback (bugs, improvements, root-cause analyses) during package usage. Test mode is entirely optional and does not affect normal operation.

### Kiro IDE

Test mode ships automatically with the package's rule-details — the file lives at `.aiflc/pdlc/ai-gce-rule-details/common/test-mode.md` on every platform (Kiro included). Nothing extra is installed for Kiro.

It is **not** auto-loaded and does **not** appear in Kiro's Steering panel — nothing under `.aiflc/` auto-loads.

**To activate:** tell the active package "enable test mode" (or "load test mode"). It reads `test-mode.md` from its rule-details home on demand and starts offering the optional feedback checkpoints.

### Amazon Q Developer / Cursor / Cline / Claude Code / Copilot / Codex

No manual copy needed — `test-mode.md` is installed with the package under `.aiflc/pdlc/ai-gce-rule-details/common/`, the same on every platform.

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
