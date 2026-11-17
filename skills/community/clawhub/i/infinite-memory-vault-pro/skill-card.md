## Description:

Provides an agent with a parallel local memory vault for structured long-term storage, semantic search, automatic synchronization from built-in memory, and large-scale indexing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and teams use this skill to organize long-running project knowledge, contacts, decisions, research notes, and other agent memory into searchable local files. It is suited to workflows that need durable structured recall beyond an agent's built-in memory.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is designed to automatically capture, copy, index, and retain user and built-in memory data on disk.

Mitigation: Install only when durable local memory capture is desired, configure narrow synchronization rules, and avoid storing sensitive personal or business data unless necessary.

Risk: Saved memory can persist across sessions and may include information that later needs deletion or correction.

Mitigation: Confirm how to stop the daemon and delete, redact, archive, or de-duplicate saved entries before enabling automatic capture.

Risk: The security summary notes one inconsistent synchronization instruction.

Mitigation: Review synchronization direction and rules before use, and keep synchronization one-way from built-in memory to the vault unless explicitly approved.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/infinite-memory-vault-pro)
- [Publisher profile](https://clawhub.ai/user/thcjp)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline command examples and file-organization guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local memory entries, indexes, synchronization rules, and operational guidance for agent-managed knowledge storage.]

## Skill Version(s):

1.0.0 (source: server release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
