## Description:

The Primer guides an agent through setting up a persistent personal-growth tutor that adapts to life stage, defines goals, calibrates challenge permissions, and establishes accountability check-ins.

This skill is ready for commercial/non-commercial use.

## Publisher:

[brucko](https://clawhub.ai/user/brucko)

### License/Terms of Use:


## Use Case:

External ClawHub users use this skill to configure an AI assistant as a personal-growth tutor for life transitions, growth goals, accountability systems, and permissioned challenge.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill creates a long-lived coaching mode that may persist beyond the user's original intent.

Mitigation: Install only when that ongoing coaching behavior is intentional, and define an expiration or removal plan for scheduled tasks.

Risk: The skill can write to PRIMER.md, AGENTS.md, SOUL.md, memory files, and scheduled job configuration.

Mitigation: Review and manually approve each proposed file or schedule change before applying it.

Risk: The generated Primer may store sensitive personal-growth goals, patterns, and accountability details for future agents to read.

Mitigation: Avoid storing highly sensitive personal material unless the user is comfortable with future agents accessing it.

## Reference(s):

- [Life Stages Framework](references/life-stages.md)
- [The Miranda Protocol](references/miranda-protocol.md)
- [Primer Permissions](references/permissions.md)
- [Primer Template](assets/PRIMER-TEMPLATE.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and optional generated files and configuration updates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update PRIMER.md, AGENTS.md, SOUL.md, memory files, and scheduled job configuration during setup.]

## Skill Version(s):

1.1.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
