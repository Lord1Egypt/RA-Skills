# Onboarding Guide

This document provides the full onboarding conversation script for the agent
to follow when this skill is first installed or updated.

## Detection

The agent should initiate onboarding when:

1. **First install** — no `memory/topics/` directory exists and no
   `memory_structure` configuration is found in the workspace config.
2. **Update from v2.x** — `memory/weekly/` exists but `memory/topics/` does
   not.
3. **Update from v3.1.x or earlier** — `memory/daily/` exists. OpenClaw does
   not read that directory; offer the daily-note migration (below).
4. **User explicitly requests** — user says "set up memory", "configure
   memory skill", runs `/hierarchical_agent_memory setup`, or similar.

## Conversation Script

### Opening (First Install)

> I just installed the hierarchical-agent-memory skill. It organizes memory
> into topic-based working files with optional time-based archival layers.
>
> There are three presets:
> - **minimal** — just a lean MEMORY.md index on top of OpenClaw's daily notes
> - **standard** — adds topic files and contact files
> - **full** — adds weekly/monthly/yearly archival summaries on top of standard
>
> Which fits your workflow? Or I can walk through the options in more detail.

### Opening (Update from v2.x)

> The hierarchical-agent-memory skill has been updated to v3. The main change
> is adding topic-based working memory alongside the existing time-based
> structure.
>
> Your existing daily/weekly/monthly/yearly files are untouched. The new
> feature is `memory/topics/` — dedicated files per project or workstream
> that serve as the authoritative source for each subject.
>
> Want me to scan your current MEMORY.md and suggest topic files to create?
> I won't change anything without your approval.

### Opening (Update from v3.1.x or earlier)

> The hierarchical-agent-memory skill has been updated to v3.2. Earlier
> versions kept daily notes in `memory/daily/`, but OpenClaw reads and writes
> daily notes at `memory/YYYY-MM-DD.md`: that is where the start-of-session
> preload, the pre-compaction memory flush, and dreaming all look.
>
> I found [N] notes in `memory/daily/`. Want me to move them to `memory/`?
> I'll use `git mv` if this workspace is a repo, merge rather than overwrite
> if a date already exists at the root, and show you the list first. Nothing
> gets loaded that wasn't loaded before; older notes stay on-demand through
> memory_search.

If the user declines, record that in the daily note and do not ask again
until the next skill update. Do not read `memory/daily/` as intake while it
remains unmigrated; say so if asked why a note was missed.

### Follow-up Questions

After preset selection, ask only the questions relevant to their choice:

**For standard or full:**
- "Want me to look at your current MEMORY.md and create starter topic files
  for projects I find there?"
- "Do you also use the companion skills agent-session-state or
  agent-provenance? They work alongside this skill for session isolation
  and governance."

**For full only:**
- If `memory-wiki` is enabled or dreaming is on, say so and recommend
  `standard` once before continuing.
- "What timezone are you in? I'll set the distillation automations
  accordingly." (Default: system timezone)
- "Weekly synthesis defaults to Sunday 2:00 AM. Does that work?"
- Name each job `hierarchical-agent-memory <weekly|monthly|yearly> synthesis`
  and tell the user how to list, disable, or remove it.

**If user says "just use defaults" at any point:**
- Apply `standard` preset
- Create directory structure
- Confirm what was created
- Stop asking questions

### Migration Offer

If the hand-maintained part of MEMORY.md (everything without dreaming's
`<!-- trigger: … -->` / `<!-- importance: N -->` markers) exceeds ~3KB:

> Your MEMORY.md is currently [X]KB of hand-written content. For best results
> it should be under 3KB — just pointers and active constraints. Want me to
> suggest how to split it into topic files? I'll show you the plan before
> making changes. Entries that dreaming promoted stay as they are.

### Closing

> Setup complete. Here's what was created:
> [list directories and files]
>
> From now on, I'll maintain MEMORY.md as a lean routing table and distill
> daily note content into topic files when projects are active.
> [If full preset: Weekly/monthly/yearly summaries will generate automatically.]

## Important Rules for Onboarding

- NEVER create directories or files before the user confirms a preset
- NEVER modify existing memory files without explicit approval
- If the user is clearly uninterested in configuration ("just do it",
  "whatever works"), apply standard and move on quickly
- Keep explanations short — the user can read references/configuration.md
  for full details
- If the user asks questions about specific settings, answer concisely and
  link to the configuration reference
