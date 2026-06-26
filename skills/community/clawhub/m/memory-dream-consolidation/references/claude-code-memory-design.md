# Claude Code Memory System — Source Analysis

> Extracted from Claude Code source leak (2026-03-31). For educational reference.

## Memory Types (from memoryTypes.ts)

Claude Code uses exactly 4 memory types:

- **user**: User's role, goals, responsibilities, knowledge. "Build up an understanding of who the user is and how you can be most helpful to them specifically."
- **feedback**: Corrections AND confirmations. "Record from failure AND success: if you only save corrections, you will avoid past mistakes but drift away from approaches the user has already validated."
- **project**: Ongoing work, goals, initiatives, bugs. "Always convert relative dates to absolute dates."
- **reference**: Pointers to external systems. "Where to look to find up-to-date information outside of the project directory."

## Body Structure for feedback/project types

"Lead with the rule itself, then a **Why:** line (the reason the user gave) and a **How to apply:** line (when/where this guidance kicks in). Knowing *why* lets you judge edge cases instead of blindly following the rule."

## What NOT to Save

- Code patterns, conventions, architecture, file paths, project structure
- Git history, recent changes, who-changed-what
- Debugging solutions or fix recipes
- Anything already documented in CLAUDE.md files
- Ephemeral task details, temporary state, current conversation context

"These exclusions apply even when the user explicitly asks you to save. If they ask you to save a PR list or activity summary, ask what was *surprising* or *non-obvious* about it — that is the part worth keeping."

## Dream System (from services/autoDream/)

### Trigger Gates (cheapest first)
1. Time: hours since lastConsolidatedAt >= minHours (default 24h)
2. Sessions: transcript count with mtime > lastConsolidatedAt >= minSessions (default 5)
3. Lock: no other process mid-consolidation

### Four Phases (from consolidationPrompt.ts)
1. **Orient**: ls memory directory, read MEMORY.md, skim existing topic files
2. **Gather Recent Signal**: Find new information worth persisting (daily logs → drifted memories → transcript search)
3. **Consolidate**: Write or update memory files. Convert relative dates to absolute. Delete contradicted facts.
4. **Prune and Index**: Keep MEMORY.md under 200 lines AND ~25KB. Remove stale pointers. Resolve contradictions.

Prompt: "You are performing a dream - a reflective pass over your memory files. Synthesize what you've learned recently into durable, well-organized memories so that future sessions can orient quickly."

Dream subagent gets **read-only bash** — can look at project but not modify anything.

## Memory Retrieval (from findRelevantMemories.ts)

Not all memories are loaded. Instead:
1. Scan all memory files' headers (filename + description frontmatter)
2. Use a lighter model (Sonnet) to select the most relevant ones (up to 5) based on current query
3. Only load selected memories into context

Selection prompt: "Return a list of filenames for the memories that will clearly be useful... Only include memories that you are certain will be helpful based on their name and description."

## Memory Drift Caveat

"Memory records can become stale over time. Use memory as context for what was true at a given point in time. Before answering the user or building assumptions based solely on information in memory records, verify that the memory is still correct and up-to-date by reading the current state of the files or resources. If a recalled memory conflicts with current information, trust what you observe now — and update or remove the stale memory rather than acting on it."

"A memory that names a specific function, file, or flag is a claim that it existed *when the memory was written*. It may have been renamed, removed, or never merged."
