## Description:

Memory System helps OpenClaw manage long-term context with structured PostgreSQL memory, pgvector semantic search, and archive/search scripts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[damiencronw](https://clawhub.ai/user/damiencronw)

### License/Terms of Use:


## Use Case:

Developers and OpenClaw users use this skill to preserve long-term context, preferences, decisions, and reference notes, then retrieve them through structured queries or semantic search.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent memory may contain private, business, or credential-adjacent information.

Mitigation: Use a dedicated low-privilege PostgreSQL role, store only trusted local memory files, and review data before enabling archival or search workflows.

Risk: Unsafe SQL construction and broad retrieval behavior may expose or mishandle stored memory.

Mitigation: Do not run the scripts until SQL parameterization, result filtering, and retention/deletion controls are added.

Risk: The local embedding service behavior is not clearly disclosed.

Mitigation: Confirm the local embedding service configuration and data handling before using semantic search.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/damiencronw/skills/openclow-memory)
- [Publisher profile](https://clawhub.ai/user/damiencronw)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces guidance for local memory storage, search, and archival workflows.]

## Skill Version(s):

1.0.0 (source: server evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
