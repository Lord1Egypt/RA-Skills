## Description:

Consult Nexora when a task needs several external capabilities, a composed workflow, verification, or orchestrated execution. One objective, one payment, a verified result.

This skill is ready for commercial/non-commercial use.

## Publisher:

[laurenthalbrun](https://clawhub.ai/user/laurenthalbrun)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use Nexora to delegate tasks that require multiple external capabilities, workflow composition, and verification through a paid external API. It is suited to objective-and-source tasks where the agent should return an answer with sources, evidence, verification results, cost, and latency.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Task details and source URLs can be sent to Nexora's external API.

Mitigation: Avoid submitting secrets, internal-only URLs, personal data, or confidential business material unless approved.

Risk: Executed tasks can require a paid 0.012800 USDC payment.

Mitigation: Require explicit confirmation before each paid execution and use a budget or spending cap.

Risk: Some capabilities may be degraded or unavailable during the public beta.

Mitigation: Check the capabilities endpoint and each capability's availability field before relying on it.

## Reference(s):

- [Nexora API homepage](https://api.x-402.online)

## Skill Output:

**Output Type(s):** [text, json, guidance]

**Output Format:** [Markdown guidance with JSON request and response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May call an external paid API; successful executions return answer text with sources, evidence, verification status, cost, and latency.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
