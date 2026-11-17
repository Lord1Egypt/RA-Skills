## Description:

Discover product ideas, validate them through market and competitor research, build MVPs, and send reports by email.

This skill is ready for commercial/non-commercial use.

## Publisher:

[morvanzhou](https://clawhub.ai/user/morvanzhou)

### License/Terms of Use:

MIT-0

## Use Case:

External builders, founders, and developers use this skill to move from product inspiration to feasibility validation and a working MVP plan or implementation. It supports product discovery across public communities and creates Chinese-language research reports, validation artifacts, code, and launch guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores API tokens, SMTP credentials, user profile data, cached search results, and reusable browser session data in local runtime directories.

Mitigation: Keep .skills-data out of version control and backups, restrict filesystem permissions, use dedicated credentials or accounts, and clear browser cache data after use.

Risk: The skill can send email reports through configured SMTP credentials.

Mitigation: Review generated content and recipient settings before sending, and use a dedicated sender credential with limited privileges.

Risk: Server security guidance says the WeChat search script should be avoided until TLS verification is fixed.

Mitigation: Skip the WeChat search script or disable that data source until the TLS verification issue is remediated and rescanned.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/morvanzhou/skills/idea2mvp)
- [Publisher Profile](https://clawhub.ai/user/morvanzhou)
- [Find Ideas Guide](references/find-ideas.md)
- [Validate Ideas Guide](references/validate-ideas.md)
- [Idea Expansion Method](references/idea-expansion.md)
- [Evaluation Framework](references/evaluation-framework.md)
- [Build MVP Guide](references/build-mvp.md)
- [Frontend Design Guide](references/frontend-design.md)
- [Email Notification Guide](references/send-email.md)
- [Feasibility Report Template](assets/report-template.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Chinese-language Markdown, code edits, shell commands, and configuration instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write local runtime files under .skills-data/idea2mvp and send email when configured by the user.]

## Skill Version(s):

1.0.18 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
