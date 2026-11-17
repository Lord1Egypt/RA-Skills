## Description:

MiniMax Agent self-evolution system with 5-layer memory for continuous learning, error analysis, and persistent personalized context management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ruiyongwang](https://clawhub.ai/user/ruiyongwang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to give a MiniMax Agent a persistent memory workflow for learning from user corrections, command failures, project context, and completed tasks across sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent memory can save broad conversation, project, and error details across sessions.

Mitigation: Use it only when persistent local memory is intended; avoid storing secrets, private project details, raw command output, or sensitive user information, and periodically inspect and delete generated memory and .learnings files.

Risk: Error logging can capture command output into local learning files.

Mitigation: Redact sensitive command output before logging and review generated error entries before keeping or sharing them.

Risk: Packaging can include local skill contents in distributable archives.

Mitigation: Review package contents before distribution and remove unintended local files or sensitive generated memories.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ruiyongwang/skills/max-self-improvement)
- [Detailed Architecture](references/architecture.md)
- [Evolution Cases](references/evolution_cases.md)
- [Memory Templates](references/memory_templates.md)
- [Learning Templates](assets/SKILL-TEMPLATE.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, templates, and generated local memory or learning files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update persistent local memory and .learnings files during agent use.]

## Skill Version(s):

1.0.1 (source: server release evidence and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
