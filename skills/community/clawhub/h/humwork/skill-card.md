## Description:

Humwork lets an agent consult verified human domain experts in real time for software, design, law, finance, medical, and product questions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[humwork](https://clawhub.ai/user/humwork)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agent operators use Humwork when a task is stalled, high stakes, environment-specific, or outside the agent's domain. The skill helps the agent open a paid consultation with a human expert, exchange focused context, and incorporate the expert's answer into its response.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can start paid third-party human consultations and send selected task context outside the agent runtime.

Mitigation: Require explicit approval before every consult and review the exact text sent to the service.

Risk: Consultation context may contain secrets, credentials, regulated data, production user records, or unrelated personal information.

Mitigation: Redact sensitive material and share only the smallest sanitized snippet needed for the expert to answer.

Risk: Billing can continue while a consultation session remains open.

Mitigation: Close each session promptly with close_chat when the consult is done and confirm the final response reflects that closure.

## Reference(s):

- [Humwork homepage](https://humwork.ai)
- [Humwork MCP API endpoint](https://api.humwork.ai/api/v1)
- [Humwork ClawHub skill page](https://clawhub.ai/humwork/skills/humwork)

## Skill Output:

**Output Type(s):** [Guidance, Text, Shell commands, Configuration]

**Output Format:** [Markdown with inline tool-call and shell-command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include third-party human consultation content; consult sessions should be closed and rated after use.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
