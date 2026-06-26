## Description: <br>
AWS SRE health check with FinOps that queries CloudWatch, SQS DLQ, and Cost Explorer, generates a Bedrock-powered incident diagnosis, and sends a structured report to Telegram. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vieiradiego](https://clawhub.ai/user/vieiradiego) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and SRE teams use this skill to monitor AWS pipeline health, cost trends, SLO status, DLQ depth, and Lambda errors, then receive incident-oriented next actions through Telegram. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: AWS operational metrics, cost data, and incident context are sent to a configured Telegram chat. <br>
Mitigation: Use a private Telegram destination, a dedicated bot token, and limit access to the chat where reports are delivered. <br>
Risk: Incident diagnosis may include sampled DLQ message content sent to Bedrock for summarization. <br>
Mitigation: Avoid placing secrets, PII, or customer payloads in DLQ messages that may be sampled. <br>
Risk: The skill requires AWS permissions for CloudWatch, SQS, Cost Explorer, and Bedrock. <br>
Mitigation: Grant least-privilege IAM permissions scoped to the monitored queues, Lambda functions, metrics, and model access needed for the deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/vieiradiego/openclaw-aws-sre-report) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Telegram MarkdownV2 report with structured incident context, findings, and AWS CLI next actions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports include AWS operational metrics, cost summaries, SLO calculations, and optional Bedrock-generated incident diagnosis.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
