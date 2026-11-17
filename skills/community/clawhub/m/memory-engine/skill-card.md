## Description:

Dist is an OpenClaw 3.8+ memory and context management plugin for local storage, semantic search, listing, and statistics over conversation memories.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lizhelong0907](https://clawhub.ai/user/lizhelong0907)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external OpenClaw users use this skill to persist selected conversation knowledge locally, recall relevant memories, and inspect memory statistics during agent workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can retain selected conversation content in a local plaintext memory database.

Mitigation: Avoid sharing secrets while enabled, restrict the database path and filesystem permissions, and add opt-in storage plus sensitive-data filtering before production use.

Risk: Recalled memories may affect later agent behavior when memory boundaries are weak.

Mitigation: Review recalled memories, provide deletion and review controls, and constrain how recalled memory is inserted into downstream prompts.

Risk: Debug output or broad storage settings can expose retained conversation content.

Mitigation: Keep debug logging off by default and review retention, cleanup, and minimum-storage settings for the deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lizhelong0907/skills/memory-engine)
- [Publisher profile](https://clawhub.ai/user/lizhelong0907)

## Skill Output:

**Output Type(s):** [Text, JSON, Configuration]

**Output Format:** [Tool responses containing memory records, search results, statistics, and configuration values]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores and retrieves local SQLite-backed memory records for OpenClaw workflows.]

## Skill Version(s):

3.0.0 (source: server release metadata; artifact frontmatter and package metadata list 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
