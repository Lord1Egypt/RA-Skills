## Description:

Provides a Chinese introductory guide to OpenClaw covering product positioning, architecture, core capabilities, setup configuration, skill development, model selection, and security practices.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ruiyongwang](https://clawhub.ai/user/ruiyongwang)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and AI agent learners use this skill to understand OpenClaw's platform concepts, deployment options, workspace configuration, Skills development workflow, model choices, and security practices.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The guide includes user-run setup examples that install packages or run containers from external package sources.

Mitigation: Verify official OpenClaw package sources before use, prefer pinned versions or Docker digests where available, and avoid unnecessary global installs.

Risk: Deployment or configuration choices could grant an agent broader local or container permissions than intended.

Mitigation: Run OpenClaw with only necessary directory mounts, avoid unnecessary container privileges, and review workspace security settings before deployment.

## Reference(s):

- [Beijing University OpenClaw Chapter Index](references/章节索引.md)
- [OpenClaw Official Website](https://openclaw.ai)
- [ClawHub Marketplace](https://clawhub.ai)
- [OpenClawmp](https://openclawmp.stepfun.com)
- [Pkuhb Openclaw Skill on ClawHub](https://clawhub.ai/ruiyongwang/skills/pkuhb-openclaw-skill)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance]

**Output Format:** [Markdown guidance with inline shell command examples and tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only skill; no hidden or automatic execution behavior is reported by the security evidence.]

## Skill Version(s):

1.0.5 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
