## Description:

Answer OpenClaw-related questions by querying and analyzing the official documentation at docs.openclaw.ai.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wx528](https://clawhub.ai/user/wx528)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, engineers, and OpenClaw users use this skill to answer OpenClaw configuration, command, troubleshooting, architecture, and best-practice questions from official documentation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can steer OpenClaw-related answers toward official documentation even when OpenClaw is only one part of a broader solution.

Mitigation: Use it when OpenClaw is relevant, cite docs.openclaw.ai, and state when documentation is unclear or missing.

Risk: Suggested configuration validation commands could be copied into a user's local shell without review.

Mitigation: Present validation commands as user-controlled steps, do not execute local commands, and do not request credentials or sensitive files.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/wx528/skills/openclaw-doc-helper)
- [Publisher Profile](https://clawhub.ai/user/wx528)
- [OpenClaw Documentation](https://docs.openclaw.ai)
- [OpenClaw FAQ](https://docs.openclaw.ai/faq)
- [OpenClaw Troubleshooting](https://docs.openclaw.ai/troubleshooting)
- [OpenClaw Configuration](https://docs.openclaw.ai/config)
- [OpenClaw GitHub Repository](https://github.com/openclaw/openclaw)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with citations and inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses official OpenClaw documentation as the source for answers and presents local validation commands as user-controlled steps.]

## Skill Version(s):

1.0.3 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
