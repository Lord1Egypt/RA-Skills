# How Multi-Platform Support Works

**Purpose:** Explains how AI-* Family packages work across different AI coding platforms (Kiro, Cursor, Windsurf, GitHub Copilot, Cline, and others) — the abstraction layer, platform-specific adapters, and what's universal vs. platform-dependent.

---

## The Platform-Agnostic Design

AI-* packages are designed as **platform-agnostic markdown workflows**. The content (rules, stages, templates) is identical regardless of which AI platform executes it. Only the LOADING MECHANISM differs per platform.

```
┌─────────────────────────────────────────────────────────────────────┐
│  UNIVERSAL LAYER (same across all platforms)                         │
│                                                                      │
│  ├── Core workflow files (orchestration logic)                       │
│  ├── Detail files (stage-specific rules)                             │
│  ├── Templates (output formats)                                      │
│  ├── Chain contracts (handoff mechanics)                             │
│  └── State files (session continuity)                                │
└─────────────────────────────────────────────────────────────────────┘
        │
        ▼  (thin adapter layer)
┌──────┐ ┌──────┐ ┌──────────┐ ┌────────┐ ┌───────┐ ┌─────────┐
│ Kiro │ │Cursor│ │ Windsurf │ │ Copilot│ │ Cline │ │ Generic │
└──────┘ └──────┘ └──────────┘ └────────┘ └───────┘ └─────────┘
```

---

## What's Universal (Works Everywhere)

| Capability | Platform Dependency |
|-----------|:-------------------:|
| Workflow logic (stages, gates, decisions) | None — pure markdown |
| Templates (output formats) | None — pure markdown |
| State files (session continuity) | None — file-based |
| Chain contracts (marker detection) | None — file-based |
| Role/persona adoption | None — prompt-based |
| Depth levels (Minimal/Standard/Comprehensive) | None — logic-based |
| Output generation (PIP, AP, DW) | None — file creation |

---

## What's Platform-Specific (Adapter Layer)

| Capability | Platform Mechanism |
|-----------|-------------------|
| **Auto-loading rules at session start** | Platform-specific config file |
| **Steering files (AI-DWG output)** | `.kiro/steering/` (Kiro) vs. equivalent per platform |
| **Hooks (AI-GCE output)** | `.kiro/hooks/` (Kiro) vs. alternative enforcement per platform |
| **Agents (AI-GCE output)** | `.kiro/agents/` (Kiro) vs. equivalent automation per platform |
| **File-match inclusion** | Kiro feature (conditional steering based on active file) |

---

## Platform Adapter Details

### Kiro (Full Support — Primary Target)

| Feature | Implementation |
|---------|---------------|
| Rule loading | `.kiro/steering/*.md` (auto-loaded every session) |
| Hook enforcement | `.kiro/hooks/*.json` (event-driven automation) |
| Agents | `.kiro/agents/*.md` (process governance agents) |
| File-match steering | Front-matter `inclusion: fileMatch` with pattern |
| Manual inclusion | Front-matter `inclusion: manual` (user provides via #) |

**Full AI-GCE output works natively** — hooks fire on IDE events, agents activate at workflow milestones.

### Claude Code (Most Important Secondary Platform)

| Feature | Implementation |
|---------|---------------|
| Rule loading | `CLAUDE.md` in workspace root (auto-loaded every session) |
| Hook enforcement | ❌ Not available — no event system. Use `CLAUDE.md` enforcement appendix + CI |
| Agents | ❌ Not available — no shortcut triggers. Paste agent prompt manually or include in `CLAUDE.md` |
| Steering | `CLAUDE.md` (primary) + file reads from workspace (detail files) |
| State files | ✅ Full support — Claude Code reads/writes workspace files |
| On-demand loading | ✅ Full support — Claude Code reads files when instructed by core workflow |

**What works natively:** All workflow packages (AI-PILC, AI-ADLC, AI-ILC, AI-POLC, AI-UXD, AI-PPM, AI-FLO), the generator (AI-DWG), and AI-GCE's rule generation all execute as expected. The core-workflow becomes `CLAUDE.md` and detail files are read on demand.

**What doesn't work:** Event-driven hooks and agent shortcuts. Claude Code has no IDE event bus — it cannot intercept file saves, detect tool use, or fire triggers automatically. AI-GCE will generate the `.kiro/hooks/` folder, but those files are documentation artifacts only.

**Workaround for enforcement:** Append a "Governance Rules — Always Check" section to `CLAUDE.md` that lists the most critical rules from `.governance/rules/`. Claude will voluntarily follow them on every response. Not as strong as event-driven hooks, but covers 60-70% of the enforcement value.

### Cursor

| Feature | Implementation |
|---------|---------------|
| Rule loading | `.cursorrules` file or `.cursor/rules/*.md` |
| Hook enforcement | Not native — use pre-commit hooks or CI checks instead |
| Agents | Not native — use custom command patterns |
| Steering | Include in `.cursorrules` or project-level rules folder |

**Adaptation:** AI-GCE generates `.kiro/hooks/` by default. For Cursor users, these translate to guidelines in `.cursorrules` + CI enforcement.

### Windsurf

| Feature | Implementation |
|---------|---------------|
| Rule loading | `.windsurfrules` file |
| Hook enforcement | Not native — CI/pre-commit alternative |
| Steering | Include in `.windsurfrules` |

### GitHub Copilot

| Feature | Implementation |
|---------|---------------|
| Rule loading | `.github/copilot-instructions.md` |
| Hook enforcement | GitHub Actions + branch protection rules |
| Steering | Instructions file + repository-level settings |

### Cline

| Feature | Implementation |
|---------|---------------|
| Rule loading | `.clinerules` file |
| Hook enforcement | Not native — pre-commit + CI |
| Steering | Include in `.clinerules` |

### Generic (Any AI Assistant)

| Feature | Implementation |
|---------|---------------|
| Rule loading | Include core file in system prompt or project context |
| Hook enforcement | External tooling (pre-commit, CI/CD, linters) |
| Steering | Project documentation that the AI reads |

---

## The Installation Guide Pattern

Every package includes `setup/INSTALL.md` with:
1. **Prerequisites** for all platforms
2. **Platform-specific sections** (6 platforms + Universal)
3. **Dual-OS commands** (PowerShell for Windows, Bash for macOS/Linux)
4. **Verification steps** (confirm the AI loaded the rules)
5. **Coexistence notes** (running multiple packages)

This ensures consistent installation experience regardless of platform choice.

---

## Governance Portability

AI-GCE's output (hooks, rules, agents) is designed for Kiro but translatable:

| AI-GCE Output | Kiro | Other Platforms |
|--------------|------|-----------------|
| `.kiro/hooks/*.json` | Native hook execution | Translate to pre-commit hooks or CI checks |
| `.kiro/agents/*.md` | Native agent triggers | Include as documentation / manual checklists |
| `.governance/rules/*.md` | Referenced by hooks | Documentation + manual/CI enforcement |
| `.compliance-state.json` | Read by hooks for tier logic | Read by scripts for CI gate decisions |

**Key principle:** The RULES are portable (markdown). The ENFORCEMENT mechanism varies. A team on Cursor gets the same rules as a team on Kiro — just enforced differently (CI instead of IDE hooks).

---

## Choosing a Platform

| If You Need | Recommended Platform |
|-------------|---------------------|
| Full AI-GCE enforcement (hooks, agents) | Kiro |
| IDE-native governance with hook firing | Kiro |
| Workflow packages only (no live enforcement) | Any platform |
| CI-based enforcement (not IDE-based) | Any platform + CI integration |
| Team uses multiple AI tools | Install rules in each; use CI for enforcement |

---

## Known Limitations (Honest Disclosure)

Not all platforms are equal. Here's what **doesn't work** outside Kiro:

| Feature | Why It's Kiro-Only |
|---------|-------------------|
| Event-driven hooks (fileEdited, agentStop, preToolUse) | Only Kiro has a hook runtime that intercepts IDE events and executes JSON hook definitions |
| Agent shortcut triggers (`SDC__`, `CRV__`, etc.) | Only Kiro reads `.kiro/agents/*.md` and activates them via typed shortcuts |
| Automatic compliance logging | Hooks write JSONL on execution — no hook execution = no automatic log entries |
| Re-derivation triggers | Mode 2 fires automatically when steering files change — only possible with fileEdited hooks |
| Tier state machine (automatic progression) | `.compliance-state.json` is read by hooks — without hooks, tier logic is manual |

**What this means in practice:**
- **9 of 10 packages** (all except AI-GCE's enforcement layer) work identically on every platform
- **AI-GCE on non-Kiro platforms** generates valid governance rules but can't auto-enforce them. Enforcement becomes advisory (the AI follows rules if instructed) or requires CI/CD translation
- **No code change fixes this** — it's an infrastructure gap in competing platforms, not a gap in the packages

**Planned fix:** Idea 011 (Platform-Portable Governance Adapters) will add a translation layer that emits enforcement in each platform's native format. Target: AI-GCE v1.1.

For the full cross-platform compatibility matrix, see `PLATFORM_CAPABILITIES.md`.

---

## Related Documents

| Document | Location |
|----------|----------|
| How Package Installation Works | `knowledge_docs/HOW_PACKAGE_INSTALLATION_WORKS.md` |
| How Steering File Loading Works | `knowledge_docs/HOW_STEERING_FILE_LOADING_WORKS.md` |
| How GCE Derivation Pipeline Works | `knowledge_docs/HOW_GCE_DERIVATION_PIPELINE_WORKS.md` |
| How to Adopt Governance on a Project | `knowledge_docs/HOW_TO_ADOPT_GOVERNANCE_ON_A_PROJECT.md` |

*Knowledge Document | Created: 2026-06-12 | Updated: 2026-06-13 | Author: [Mohammad Maheri](https://www.linkedin.com/in/mohammad-maheri-8399565b)*
