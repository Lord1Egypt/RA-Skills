## Description:

Helps Chinese-speaking OpenClaw users install and configure ClawHub, set up a mirror, discover skills, and manage skill install, update, enable, and disable workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[binbin](https://clawhub.ai/user/binbin)

### License/Terms of Use:

MIT

## Use Case:

Developers and OpenClaw users use this skill to get concise ClawHub setup guidance, configure a China-accessible mirror, find relevant skills, and manage installed skills.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unpinned global package and skill installs can change the agent environment unexpectedly.

Mitigation: Review package and skill sources first, prefer pinned versions, and avoid elevated privileges unless the source has been independently verified.

Risk: Bulk updates can alter many installed skills at once in sensitive environments.

Mitigation: Inspect and update skills individually when environment stability or review requirements matter.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/binbin/skills/openclaw-skills-setup-cn)
- [Aliyun ClawHub mirror](https://mirror.aliyun.com/clawhub/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands are advisory and should be reviewed before changing an agent environment.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
