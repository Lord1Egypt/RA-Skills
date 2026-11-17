## Description:

AI Agent 营销操作系统 — 包含 Virtual CMO（战略大脑）和 Marketing Operator（执行引擎），提供市场分析、策略制定、Campaign 规划与执行追踪全链路能力。

This skill is ready for commercial/non-commercial use.

## Publisher:

[forevercrab321-svg](https://clawhub.ai/user/forevercrab321-svg)

### License/Terms of Use:

MIT-0

## Use Case:

Marketing teams, operators, and agent developers use this skill to analyze market signals, identify and score opportunities, generate go-to-market strategy, plan campaigns, track execution, and feed measured learnings back into future strategy.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can persist market insights, campaign records, and learnings that may contain confidential strategy or customer information.

Mitigation: Use retention, redaction, and data-boundary controls before supplying customer PII or confidential business strategy to workflows.

Risk: Configured adapters can enable external CRM, content, and data-source actions.

Mitigation: Keep external adapters disabled until scoped credentials, approval gates, and intended endpoints are configured.

Risk: Automated campaign execution can affect publishing, CRM writes, and budget-sensitive decisions.

Mitigation: Run with auto_mode off by default and require human approval for publishing, CRM writes, budget or spend changes, and memory promotion.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/forevercrab321-svg/skills/marketing-os)
- [Marketing OS README](artifact/README.md)
- [Runtime configuration](artifact/configs/system.config.json)
- [CMO to Operator schema](artifact/schemas/cmo_to_operator.schema.json)
- [Campaign schema](artifact/schemas/campaign.schema.json)
- [Feedback schema](artifact/schemas/feedback.schema.json)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Structured Markdown and JSON-compatible campaign, task, strategy, and feedback objects]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses schema-shaped outputs for market analysis, mission briefs, campaign records, task plans, execution metrics, and feedback.]

## Skill Version(s):

1.0.0 (source: release evidence and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
