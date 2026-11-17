## Description:

Restructure flat MEMORY.md files into a tiered memory system with an entity graph.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kapslap](https://clawhub.ai/user/kapslap)

### License/Terms of Use:


## Use Case:

Developers and agent users use this skill to reorganize large flat memory files into a compact router, active and archived memory tiers, stable protocols, and a JSONL entity graph for faster lookup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill rewrites persistent agent memory files, which can move or preserve directives in unintended ways.

Mitigation: Back up MEMORY.md before use and review the generated router and protocols.md before relying on them.

Risk: The skill can create searchable plaintext records of contacts, accounts, chat IDs, emails, and relationships.

Mitigation: Exclude secrets and sensitive account data, then periodically prune archive and ontology entries that should no longer be retained.

## Reference(s):

- [Memory Architect ClawHub Skill Page](https://clawhub.ai/kapslap/skills/memory-architect)

## Skill Output:

**Output Type(s):** [Files, Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Markdown files, JSONL entity records, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Rewrites persistent memory and creates searchable plaintext records; review changes before use.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
