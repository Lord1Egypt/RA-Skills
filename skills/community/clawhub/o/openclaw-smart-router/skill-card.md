## Description:

Automatically routes AI requests to cost-optimal models based on task complexity, budget, and learned usage patterns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[atlaspa](https://clawhub.ai/user/atlaspa)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators use this skill to automatically choose models for AI requests, reduce model spend, track routing outcomes, and tune routing behavior across providers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill automatically hooks model requests and can change model routing behavior.

Mitigation: Review routing settings and monitor selections before relying on it for high-cost or quality-sensitive workflows.

Risk: The skill stores local routing, payment, quota, and learning history.

Mitigation: Keep the local data directory protected and avoid sharing wallet or routing history files unnecessarily.

Risk: The local dashboard exposes routing and payment-related endpoints.

Mitigation: Bind and access the dashboard only on localhost, and do not expose port 9093 to untrusted networks.

Risk: The x402 Pro payment flow is not production-safe according to the security guidance.

Mitigation: Use external spend controls and explicit human approval, and do not enable wallet payments until transaction verification and wallet ownership checks are fixed.

## Reference(s):

- [Openclaw Smart Router on ClawHub](https://clawhub.ai/atlaspa/skills/openclaw-smart-router)
- [README](artifact/README.md)
- [Smart Router API Reference](artifact/API-REFERENCE.md)
- [Routing Guide](artifact/ROUTING-GUIDE.md)
- [Database Implementation](artifact/DATABASE-IMPLEMENTATION.md)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown, CLI text, JSON API responses, and local configuration files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include model recommendations, complexity scores, cost estimates, routing history, quota status, and dashboard/API responses.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
