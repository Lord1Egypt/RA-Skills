## Description:

Enterprise AI agent orchestration platform for coordinating multiple AI agents on complex business workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangm-a3](https://clawhub.ai/user/wangm-a3)

### License/Terms of Use:

MIT-0

## Use Case:

Operations teams, enterprise users, and developers use this skill to route natural-language business requests to specialized planning agents for procurement, production, sales, finance, compliance, and operations workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release is flagged as suspicious because the evidence describes it as more like a lightweight planning assistant than a full enterprise automation system.

Mitigation: Evaluate it as a planning assistant, verify recommendations before operational use, and do not rely on it as an autonomous enterprise workflow system.

Risk: User task content may be sent to external LLM APIs during runtime.

Mitigation: Avoid entering sensitive customer, financial, or operational details unless external API handling is acceptable for the deployment.

Risk: The security evidence notes API and dependency scope beyond what the shipped scripts use.

Mitigation: Remove unused dependencies where practical, pin required dependencies, and configure only the API credentials needed for the intended runtime.

## Reference(s):

- [OpenClaw homepage](https://openclaw.ai)
- [ClawHub skill page](https://clawhub.ai/wangm-a3/skills/openclaw-enterprise)
- [OpenClaw GitHub profile listed in metadata](https://github.com/openclaw)
- [Keyword routing table](references/routing_tables/keyword_routing.md)
- [Usage guide](templates/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, shell commands, configuration]

**Output Format:** [Markdown or plain text with optional command and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include planning reports, workflow recommendations, route selections, risk notes, and generated business analysis.]

## Skill Version(s):

2.0.3 (source: release evidence and SKILL.md frontmatter; package.json reports 1.2.4)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
