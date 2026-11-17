## Description:

Supercharged Memory helps an agent capture, store, consolidate, and search conversation-derived memory across sessions using workspace files, QMD search, and optional vector search.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nollio](https://clawhub.ai/user/nollio)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users can use this skill to give an agent persistent, searchable memory for preferences, decisions, project context, and session continuity across chats.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent memory can capture conversation-derived facts, decisions, preferences, and project details across sessions.

Mitigation: Limit capture to explicit memories where possible, periodically inspect MEMORY.md and memory files, and remove sensitive entries that should not persist.

Risk: Broad workspace indexing can include more local project content than intended.

Mitigation: Review QMD collection scope before reindexing, keep indexing within intended workspace paths, and avoid broad workspace reindexing until the scope is clear.

Risk: Optional Mem0, cloud embeddings, or Supabase sync can introduce external data handling.

Mitigation: Leave optional cloud or vector features disabled until transmitted data, provider retention, and deletion paths are understood; keep API keys in environment variables.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/nollio/skills/normieclaw-supercharged-memory)
- [README](artifact/README.md)
- [Security Guidance](artifact/SECURITY.md)
- [First-Run Setup](artifact/SETUP-PROMPT.md)
- [Consolidation Rules](artifact/config/consolidation-rules.md)
- [Memory Dashboard Companion Kit](artifact/dashboard-kit/DASHBOARD-SPEC.md)
- [Qdrant Quick Start](https://qdrant.tech/documentation/quick-start/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, JSON configuration, and memory file updates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates or updates local memory files and search indexes; optional vector search remains disabled until explicitly configured.]

## Skill Version(s):

1.0.3 (source: server release metadata; changelog: security fixes for script confinement and setup traversal)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
