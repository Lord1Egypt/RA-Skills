# Three-Layer Knowledge Architecture

## Prerequisite: Independent Workspace

**Every consulting agent MUST have its own dedicated workspace.** OpenClaw loads `AGENTS.md` from the workspace root — sharing a workspace with another agent means both read the same file, causing identity confusion.

Create a dedicated agent first: `openclaw agents add <agent-id>`, which generates an isolated workspace at `~/.openclaw/workspace-<agent-id>/`.

## Why Layering Matters

You can't dump everything into one file. OpenClaw has file size limits (`bootstrapMaxChars`: 20000 default), and different files have different loading guarantees. Understanding this determines your entire architecture.

## The Three Layers

### Layer 1: AGENTS.md — Must-Know (Deterministic)

**Loading**: Auto-injected at the start of every session, including group chats. Sub-agents also receive this file.

**What goes here**:
- Core knowledge summaries (extracted from full documents)
- Behavioral constraints and service boundaries
- Safety red lines (identity protection, no file sharing, no self-modification)
- Key data points the Agent must always know
- Reference instructions pointing to knowledge/ directory
- Tool permissions and search guidelines

**Size guideline**: 10-25KB. Enough to cover essentials, not so large it gets truncated.

**Critical rule**: If a constraint MUST be enforced in every context (DMs, groups, sub-agent calls), it MUST be in AGENTS.md. This is the only file with 100% deterministic loading.

### Layer 2: MEMORY.md — Important Memory (Conditional)

**Loading**: Loaded at the start of DM sessions. NOT guaranteed in group chat scenarios.

**What goes here**:
- Identity reinforcement ("I am a [DOMAIN] consultant")
- Behavioral constraint backup (duplicate of AGENTS.md safety rules)
- Knowledge directory index (list of files in knowledge/)
- Key FAQ summaries
- Client interaction history notes

**Why duplicate safety constraints?**: Because MEMORY.md loads in DM sessions where you might configure the Agent, and the duplication reinforces the rules. But never RELY on it as the only location.

### Layer 3: knowledge/ — Reference Library (On-Demand)

**Loading**: This is a self-built directory. OpenClaw does NOT auto-load files from it. The Agent must actively read files using tools.

**What goes here**:
- Complete policy documents
- Full industry regulations
- Detailed guides and manuals
- Terminology dictionaries
- Historical data and case studies
- Any document too large for AGENTS.md

**How to make the Agent use it**: Add instructions in AGENTS.md:
```markdown
## Knowledge Reference
- When uncertain about facts, check the knowledge/ directory
- Do NOT answer from memory alone — verify against reference materials
- Available reference files:
  - knowledge/platform-policies.md — Official platform rules
  - knowledge/best-practices.md — Proven strategies and methods
  - knowledge/faq-database.md — Common questions and verified answers
```

## Decision Flowchart

```
Is this information critical for EVERY interaction?
  ├── YES → AGENTS.md (Layer 1)
  └── NO
      ├── Is it important context the Agent should remember?
      │   ├── YES → MEMORY.md (Layer 2)
      │   └── NO
      │       └── Is it reference material needed for accuracy?
      │           ├── YES → knowledge/ (Layer 3)
      │           └── NO → Don't include it
      └── Is it a safety constraint?
          └── ALWAYS → AGENTS.md (even if also in MEMORY.md)
```

## Common Mistakes

1. **Putting everything in AGENTS.md** → File gets truncated, Agent loses critical info
2. **Safety constraints only in MEMORY.md** → Not loaded in group chats, constraints ignored
3. **Not indexing knowledge/ in AGENTS.md** → Agent doesn't know the directory exists
4. **Full documents in AGENTS.md instead of summaries** → Wastes context window on details that could be looked up on demand
