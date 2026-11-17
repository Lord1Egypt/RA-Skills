## Description:

Layered Memory Manager guides OpenClaw agents in maintaining a two-tier persistent memory system with L1 hot-cache summaries, L2 detailed storage, hygiene tracking, promotion, demotion, archiving, and manual memory controls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chyern](https://clawhub.ai/user/chyern)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to help persistent OpenClaw agents organize, search, update, and prune long-lived workspace memories across hot and cold storage layers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent memory can influence unrelated future tool actions or decisions.

Mitigation: Treat stored memory as advisory context only; review relevant memory entries before use and keep current user instructions, policy, and safety boundaries authoritative.

Risk: The skill can read, rewrite, archive, and after confirmation potentially delete old memory records during hygiene workflows.

Mitigation: Review MEMORY.md, memory/*.md, memory/hygiene.json, and archive candidates before hygiene runs; require explicit confirmation for permanent deletion.

Risk: Stored private memory may be exposed in inappropriate contexts.

Mitigation: Keep MEMORY.md and memory layer files private, avoid loading them in group chats, and share only the minimum memory content needed for the current task.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chyern/skills/layered-memory-manager)
- [Artifact README](artifact/README.md)
- [Artifact manifest](artifact/manifest.json)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline commands and structured memory file conventions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce memory-health summaries, promotion and demotion plans, archive and restore actions, and updates to MEMORY.md, memory/*.md, memory/hygiene.json, or memory/archive/.]

## Skill Version(s):

1.0.3 (source: server release evidence and artifact/manifest.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
