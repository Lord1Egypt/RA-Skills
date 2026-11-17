# AI-* Family — Platform Capabilities

**Purpose:** Honest disclosure of what works on each platform. Not all features are portable — this document tells you exactly what you get.

---

## Design Philosophy

The AI-* Family packages are **pure Markdown prompt-engineering artifacts**. No compiled code, no proprietary format, no runtime dependencies. Any AI agent that reads text and follows instructions can execute these workflows.

However, some features depend on **platform-specific infrastructure** that not all AI IDEs provide. This document maps feature availability honestly.

---

## Platform Compatibility Matrix

### Workflow Packages (AI-ILC, AI-PILC, AI-ADLC, AI-POLC, AI-UXD, AI-PPM, AI-FLO)

| Feature | Kiro | Claude Code | claude.ai | Cursor | Cline | Amazon Q | Copilot | Codex CLI |
|---------|:----:|:-----------:|:---------:|:------:|:-----:|:--------:|:-------:|:---------:|
| Core workflow execution | ✅ | ✅ | ✅¹ | ✅ | ✅ | ✅ | ✅ | ✅ |
| On-demand file loading | ✅ | ✅ | ❌² | ✅ | ✅ | ✅ | ✅ | ✅ |
| Template generation | ✅ | ✅ | ⚠️³ | ✅ | ✅ | ✅ | ✅ | ✅ |
| State file persistence | ✅ | ✅ | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Session continuity (cold resume) | ✅ | ✅ | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Chain marker detection | ✅ | ✅ | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Depth adaptation (Min/Std/Comp) | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |

> ¹ Requires pasting `core-workflow.md` content as system prompt or into Projects knowledge.
> ² claude.ai has no file system access. All stage-detail files must be pasted manually into the conversation or pre-loaded as Project knowledge.
> ³ The AI will produce template content in conversation but cannot write files to disk.

**Bottom line:** If your platform has workspace file access, workflow packages work at 100%.

---

### Generator Package (AI-DWG)

| Feature | Kiro | Claude Code | claude.ai | Cursor | Cline | Amazon Q | Copilot | Codex CLI |
|---------|:----:|:-----------:|:---------:|:------:|:-----:|:--------:|:-------:|:---------:|
| Workspace generation | ✅ | ✅ | ❌⁴ | ✅ | ✅ | ✅ | ✅ | ✅ |
| File creation (multi-file) | ✅ | ✅ | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Steering file output | ✅ | ✅ | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ |

> ⁴ AI-DWG is a file generator — it needs to write ~30+ files. Not possible in a web chat context.

---

### Governance Engine (AI-GCE) — Most Platform-Dependent

| Feature | Kiro | Claude Code | claude.ai | Cursor | Cline | Amazon Q | Copilot | Codex CLI |
|---------|:----:|:-----------:|:---------:|:------:|:-----:|:--------:|:-------:|:---------:|
| Rule generation (`.governance/rules/`) | ✅ | ✅ | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Hook generation (`.kiro/hooks/`) | ✅ Native | ⚠️ Generated but inert | ❌ | ⚠️ Generated but inert | ⚠️ Generated but inert | ⚠️ Generated but inert | ⚠️ Generated but inert | ⚠️ Generated but inert |
| **Hook execution (auto-enforcement)** | ✅ Native | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Agent generation (`.kiro/agents/`) | ✅ Native | ⚠️ Generated but inert | ❌ | ⚠️ Generated but inert | ⚠️ Generated but inert | ⚠️ Generated but inert | ⚠️ Generated but inert | ⚠️ Generated but inert |
| **Agent shortcut triggers (`SDC__`, etc.)** | ✅ Native | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Compliance logging (JSONL) | ✅ Auto | ⚠️ Manual | ❌ | ⚠️ Manual | ⚠️ Manual | ⚠️ Manual | ⚠️ Manual | ⚠️ Manual |
| Tier activation (progressive) | ✅ Auto | ⚠️ Manual | ❌ | ⚠️ Manual | ⚠️ Manual | ⚠️ Manual | ⚠️ Manual | ⚠️ Manual |
| Re-derivation (Mode 2) | ✅ Auto-triggered | ⚠️ User-initiated | ❌ | ⚠️ User-initiated | ⚠️ User-initiated | ⚠️ User-initiated | ⚠️ User-initiated | ⚠️ User-initiated |
| Brownfield baseline (Mode 3) | ✅ | ✅ | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ |
| `.governance/rules/*.md` (readable rules) | ✅ | ✅ | ⚠️⁵ | ✅ | ✅ | ✅ | ✅ | ✅ |

> ⁵ Rules can be read as Project knowledge but won't be auto-enforced.

---

### Test Governance Engine (AI-TGE)

| Feature | Kiro | Claude Code | claude.ai | Cursor | Cline | Amazon Q | Copilot | Codex CLI |
|---------|:----:|:-----------:|:---------:|:------:|:-----:|:--------:|:-------:|:---------:|
| Test governance logic | ✅ | ✅ | ⚠️ | ✅ | ✅ | ✅ | ✅ | ✅ |
| File generation | ✅ | ✅ | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ |

---

## What "Generated but Inert" Means

AI-GCE will still generate hook JSON files and agent Markdown files on any platform. The files are structurally valid. But:

- **Hooks won't fire** — only Kiro has an event system (`fileEdited`, `agentStop`, `preToolUse`) that reads `.kiro/hooks/*.json` and auto-executes them.
- **Agents won't auto-trigger** — only Kiro reads `.kiro/agents/*.md` and activates them via shortcuts.

**On non-Kiro platforms, you get:**
- The governance **rules** (`.governance/rules/*.md`) — fully readable, manually enforceable
- The compliance **documentation** — team knows what's expected
- The **intent** of each hook as a reference for setting up CI/CD enforcement

**You don't get:**
- Real-time IDE-level enforcement on every file save
- Automatic compliance logging without manual action
- Shortcut-triggered process agents

---

## Alternative Enforcement Strategies (Non-Kiro)

If you're on Claude Code, Cursor, or another platform and want active enforcement:

| Strategy | Effort | Coverage |
|----------|--------|----------|
| Include `.governance/rules/` in your rules/steering (always loaded) | Low | The AI reads and follows rules voluntarily — advisory, not enforced |
| Pre-commit hooks + CI gates | Medium | Translate GCE rules into linter configs or custom scripts |
| Periodic manual audit ("run compliance check") | Low | Ask the AI to check current files against `.governance/rules/` on demand |
| Platform-native rule files | Medium | Translate hooks into `.cursorrules`, `CLAUDE.md` enforcement sections, etc. |

---

## Summary by Use Case

| "I want to…" | Any platform | Kiro only |
|--------------|:------------:|:---------:|
| Run a workflow (PILC, ADLC, etc.) | ✅ | — |
| Generate a workspace (DWG) | ✅ | — |
| Generate governance rules | ✅ | — |
| Have rules auto-enforced on every file save | — | ✅ |
| Use process agents at milestones | — | ✅ |
| Get compliance logging automatically | — | ✅ |
| Read rules and follow them voluntarily | ✅ | — |

---

## Claude — Deep Dive (Primary Secondary Platform)

Claude is the most important non-Kiro target. Here's the complete picture.

### Claude Code (CLI/IDE Agent) — Near-Full Support

Claude Code has workspace file access. This means:

| What Works | How |
|-----------|-----|
| All 9 workflow/generator packages | Cores + rule-details install in `.aiflc/pdlc/`; the orchestrator (imported by `CLAUDE.md` via `@import`) `Read`s them on demand |
| Slash commands (`/pdlc:<key>`) | The installer generates `.claude/commands/pdlc/*.md` — one per package (e.g. `/pdlc:pilc`) plus destination agent shortcuts (`/pdlc:dat`, `/pdlc:fhc`, …), each a pointer that `Read`s the canonical core |
| On-demand file loading | Core workflow instructs Claude to read detail files — Claude Code does this natively |
| State file persistence | `pilc-state.md` etc. written and read between sessions |
| Chain marker detection | Claude reads marker files to detect predecessor outputs |
| Template output | Claude writes files to disk |
| AI-GCE rule generation | Full mode 1/2/3/4 execution — all files generated |
| Brownfield baseline | Claude reads existing code and baselines violations |

| What Doesn't Work | Why | Workaround |
|-------------------|-----|------------|
| Hook auto-execution | No event bus in Claude Code | Append critical rules to `CLAUDE.md` as "always check" instructions |
| GCE-generated agent shortcuts (`SDC__`, etc.) | No `.kiro/agents/` runtime | Paste the agent's prompt directly, or include it in `CLAUDE.md`. (Note: package keys + AI-DFE/AI-FLO destination shortcuts ARE exposed as `/pdlc:*` slash commands — see "What Works".) |
| Automatic compliance logging | Logging is triggered by hooks | Ask Claude to log manually: "Log this check to compliance-log/" |
| Re-derivation auto-trigger | Requires fileEdited events | Say "Steering changed — re-derive" manually (Mode 2 still works) |
| Tier auto-progression | Hook reads `.compliance-state.json` | Say "Activate next compliance tier" manually (Mode 4 still works) |

### Best Practice: Claude Code + AI-GCE Enforcement

To get maximum governance value on Claude Code:

1. Run AI-GCE normally — it generates all files including hooks
2. After generation, append the top-tier rules to your `CLAUDE.md`:
   ```markdown
   ## Governance Rules (Always Enforce)
   
   The following rules from `.governance/rules/` apply to ALL work in this workspace.
   Check compliance on every file you create or modify.
   
   - See: .governance/rules/security-rules.md (CRITICAL — never skip)
   - See: .governance/rules/architecture-rules.md
   - See: .governance/rules/naming-conventions.md
   - See: .governance/COMPLIANCE_README.md for full rule index
   ```
3. Periodically ask Claude: "Run a compliance check against `.governance/rules/` on recent changes"
4. For process governance, paste the agent prompt when needed (e.g., copy the session-discipline-agent content before session end)

This gives you ~70% of Kiro's enforcement value through voluntary compliance + manual triggers.

### claude.ai (Web/Projects) — Limited

| Works | Doesn't Work |
|-------|-------------|
| Core workflow logic (if pasted as Project knowledge) | File system access |
| Depth adaptation, persona adoption | State persistence |
| Template content (output in conversation) | Multi-file generation |
| Advisory governance (rules as reference) | Any file-based feature |

**Practical use:** Good for running AI-PILC/AI-ILC in "conversation mode" where the output is discussion-quality deliverables rather than files. Not suitable for AI-DWG, AI-GCE, or any package that generates workspace artifacts.

### Claude API — System Prompt Integration

For developers building on the Claude API:
- Inject `core-workflow.md` as system prompt content
- Implement file I/O via tool use (function calling) for on-demand loading
- State persistence requires your own storage layer
- Works for workflow packages if you handle the file operations

---

## OpenAI Codex CLI — Deep Dive

Codex CLI is the most important OpenAI-ecosystem target. It has full workspace file access via its sandboxed environment and reads `AGENTS.md` files automatically.

### Capabilities Summary

| What Works | How |
|-----------|-----|
| All 10 workflow/generator packages | `AGENTS.md` in workspace root or subdirectories; rule-details in `.ai-{package}-rule-details/` |
| On-demand file loading | Core workflow instructs Codex to read detail files — Codex does this natively within its sandbox |
| State file persistence | `pilc-state.md` etc. written and read between sessions |
| Chain marker detection | Codex reads marker files to detect predecessor outputs |
| Template output | Codex writes files to disk (within sandbox writable root) |
| AI-GCE rule generation | Full mode 1/2/3/4 execution — all files generated |
| Brownfield baseline | Codex reads existing code and baselines violations |

| What Doesn't Work | Why | Workaround |
|-------------------|-----|------------|
| Hook auto-execution | No event bus in Codex | Append critical rules to root `AGENTS.md` as "always check" instructions |
| Agent shortcuts (`SDC__`, etc.) | No `.kiro/agents/` runtime | Paste the agent's prompt directly, or include it in `AGENTS.md` |
| Automatic compliance logging | Logging is triggered by hooks | Ask Codex to log manually |
| Re-derivation auto-trigger | Requires fileEdited events | Say "re-derive governance" manually |
| Tier auto-progression | Hook reads `.compliance-state.json` | Say "Activate next compliance tier" manually |

### Best Practice: Codex + AI-GCE Enforcement

To get maximum governance value on Codex:

1. Run AI-GCE normally — it generates all files including hooks
2. After generation, append the top-tier rules to your root `AGENTS.md`:
   ```markdown
   ## Governance Rules (Always Enforce)
   
   The following rules from `.governance/rules/` apply to ALL work in this workspace.
   Check compliance on every file you create or modify.
   
   - See: .governance/rules/security-rules.md (CRITICAL)
   - See: .governance/rules/architecture-rules.md
   - See: .governance/rules/naming-conventions.md
   - See: .governance/COMPLIANCE_README.md for full rule index
   ```
3. Periodically ask Codex: "Run a compliance check against `.governance/rules/` on recent changes"

This gives you ~70% of Kiro's enforcement value through advisory compliance + manual triggers.

### Sandbox Considerations

Codex runs in a sandboxed environment. Default (`workspace-write`) allows reading files broadly and writing within the workspace root. This is fully compatible with AI-* packages since all output stays within the project directory. If you're using a more restrictive sandbox mode, ensure the `.ai-*-rule-details/` folders are within the readable path.

---

## Planned Enhancements (Roadmap)

| Enhancement | Target | What It Solves |
|-------------|--------|----------------|
| Platform-Portable Governance Adapters (Idea 011) | AI-GCE v1.1 | Auto-emits enforcement in each platform's native format (`.cursorrules`, `CLAUDE.md` appendix, etc.) |
| SKILL.md Wrappers (Idea 013) | Beta 2 / GA | Adds Agent Skills standard discovery file — 25+ agent products auto-detect the packages |

---

## Honest Positioning

**9 of 10 packages are 100% compatible with Claude Code, Codex CLI, and all file-access-capable platforms** — they're interactive workflows and generators that only need file access and instruction-following.

**AI-GCE is ~70% compatible on Claude Code and Codex CLI** — all rules generate correctly, but real-time auto-enforcement (hooks + agents) requires Kiro's event system. On Claude/Codex, governance becomes advisory/manual rather than automatic.

**This is not a deficiency in the packages.** It reflects the current state of AI IDE infrastructure — most platforms don't have event-driven hook systems yet. As platforms mature (or when Idea 011 ships), the gap closes.

---

*Document Version: 1.1.0 | Updated: 2026-06-19 | Author: Maheri*
