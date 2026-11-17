## Description:

Runs a structured five-perspective, three-round debate in a single LLM call to challenge strategic assumptions and produce consensus, contested points, a verdict, and a controllability assessment.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dodge1218](https://clawhub.ai/user/dodge1218)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and business users can use this skill to pressure-test strategic decisions, leverage audits, weekly retrospectives, and opportunity framing with five fixed viewpoints before acting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Recurring forum runs may collect and send sensitive business metrics, logs, customer data, or lead data to a hosted model.

Mitigation: Require explicit approval before scheduling, redact logs and customer or lead data, and share only summarized metrics needed for the forum question.

Risk: Scheduled OpenClaw cron jobs can continue running after the original review context has changed.

Mitigation: Maintain clear controls to list, pause, and delete scheduled jobs, and review active schedules during operational handoffs.

## Reference(s):

- [Skill source artifact](artifact/SKILL.md)
- [ClawHub skill page](https://clawhub.ai/dodge1218/skills/multi-perspective-forum)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown debate transcript with structured headings and optional shell-style scheduling configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses caller-provided data and question inputs; requested debate output is capped under 3,000 tokens by the skill prompt.]

## Skill Version(s):

1.0.0 (source: skill frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
