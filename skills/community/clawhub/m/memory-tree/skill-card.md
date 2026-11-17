## Description:

Memory Tree helps OpenClaw generate weekly memory reports, search saved memories by keyword, and mark important memories as permanent.

This skill is ready for commercial/non-commercial use.

## Publisher:

[masongmx](https://clawhub.ai/user/masongmx)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users and developers use this skill to inspect local memory files, produce weekly memory summaries, search remembered items, and pin important memories for long-term retention.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads local OpenClaw memory files and channel configuration, which may contain sensitive personal or workspace information.

Mitigation: Install only if this access is acceptable and review generated weekly reports before sharing them.

Risk: Generated weekly reports may be sent to a configured Feishu destination if a user runs the printed send command.

Mitigation: Review the generated report path and Feishu target before running any printed send command.

Risk: Documentation and inspected behavior differ around cron, cloud APIs, and automatic decay.

Mitigation: Use the server security guidance as authoritative and do not rely on unsupported documentation claims about automation, cloud APIs, or decay behavior.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/masongmx/skills/memory-tree)
- [Memory-Like-A-Tree](https://github.com/loryoncloud/Memory-Like-A-Tree)
- [Lobster Doctor](https://github.com/Masongmx/lobster-doctor)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration]

**Output Format:** [Terminal text, Markdown weekly reports, and suggested shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Weekly reports are written under the local OpenClaw memory workspace; send commands are printed for review rather than executed by the skill.]

## Skill Version(s):

2.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
