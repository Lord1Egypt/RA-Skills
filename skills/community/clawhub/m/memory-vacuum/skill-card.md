## Description:

Memory Vacuum helps an agent keep local memory files lightweight by daily sharding conversation journals and compressing MEMORY.md to retain essential information.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liujw0214](https://clawhub.ai/user/liujw0214)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to keep long-running AI memory stores compact, organized, and available across restarts without preloading full conversation history.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may persist every message into local memory files, increasing exposure of sensitive conversation content.

Mitigation: Enable it only in workspaces where persistent local journals are acceptable, and add confirmation or sensitive-data exclusions before writing.

Risk: Automatic compression and reorganization may alter memory records and leave retention expectations unclear.

Mitigation: Keep backups and define retention and deletion controls before using it on important memory stores.

## Reference(s):

- [Memory Vacuum README](artifact/README.md)
- [Memory Vacuum English Listing](artifact/LISTING_EN.md)
- [Memory Vacuum ClawHub Page](https://clawhub.ai/liujw0214/skills/memory-vacuum)

## Skill Output:

**Output Type(s):** [Markdown, Files, Guidance]

**Output Format:** [Markdown memory notes and concise operational guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or reorganize local memory/YYYY-MM-DD.md and MEMORY.md files when the host agent follows it.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
