## Description:

HTS全岗位通用AI助理生成器，支持管理、技术、业务、职能等各类岗位，自动生成负责人画像、助理规范及OpenClaw完整配置文件，实现一岗一AI助手。

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiangdong-3](https://clawhub.ai/user/jiangdong-3)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and managers use this skill to turn a complete HTS job description into a role-specific AI assistant profile, operating rules, and OpenClaw configuration files for internal workplace workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Job descriptions may contain personal data, compensation details, confidential strategy, credentials, or other sensitive internal information.

Mitigation: Remove sensitive and unnecessary details before pasting job descriptions into the assistant.

Risk: Generated OpenClaw configuration may encode incorrect role boundaries, communication norms, or operational assumptions.

Mitigation: Review the generated configuration and assistant behavior rules before using them in an internal workflow.

Risk: Pasted job descriptions can act as untrusted input that influences generated assistant behavior.

Mitigation: Treat source job descriptions as untrusted and inspect the resulting assistant profile and files before deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jiangdong-3/skills/hts-job-assistant-generator)
- [README.md](README.md)
- [IDENTITY.md](references/IDENTITY.md)
- [SOUL.md](references/SOUL.md)
- [AGENTS.md](references/AGENTS.md)
- [USER.md](references/USER.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Configuration, Guidance]

**Output Format:** [Markdown documents and OpenClaw configuration content]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generates a responsible-person profile, assistant job description, assistant identity and behavior rules, and IDENTITY.md, SOUL.md, AGENTS.md, and USER.md content.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
