## Description:

AWS SRE health check with FinOps that queries CloudWatch, SQS DLQ, and Cost Explorer, generates a Bedrock-powered incident diagnosis, and sends a structured report to Telegram.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vieiradiego](https://clawhub.ai/user/vieiradiego)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and SRE teams use this skill to monitor an AWS pipeline, summarize operational health, report FinOps status, and produce incident follow-up actions for human operators.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Raw DLQ message bodies can be included in Bedrock diagnosis input and Telegram reports.

Mitigation: Use only queues whose message bodies are approved for those destinations, or redact or disable DLQ samples before production use.

Risk: The documented IAM policy includes broad resources for some AWS read and model-invocation actions.

Mitigation: Deploy with least-privilege IAM scoped to the exact queues, Lambda functions, Cost Explorer needs, and Bedrock model used by the report.

Risk: Generated incident CTAs may contain operational commands that are incomplete or inappropriate for the live incident.

Mitigation: Treat CTAs as guidance and require operator review before running AWS CLI commands or redrive actions.

Risk: Telegram bot credentials and chat destinations control where operational reports are sent.

Mitigation: Store Telegram credentials securely and verify the chat destination before enabling scheduled reports.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/vieiradiego/skills/openclaw-aws-sre-report)
- [OpenClaw](https://clawhub.ai)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Telegram MarkdownV2 report, TypeScript report object, and incident CTAs with AWS CLI commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires AWS and Telegram configuration; Cost Explorer and Bedrock failures are handled with graceful fallbacks.]

## Skill Version(s):

1.0.2 (source: server release metadata; artifact frontmatter and package.json are 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
