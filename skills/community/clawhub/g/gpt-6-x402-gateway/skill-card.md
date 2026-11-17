## Description:

Guides agents in using a third-party, pay-per-call GPT-6 gateway for chat and specialized tasks through x402 payments on Base.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangletiand](https://clawhub.ai/user/wangletiand)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents with an x402-compatible wallet use the gateway for paid chat completions, translation, research, and task-specific analysis without a provider API key.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic wallet payments can incur USDC charges without clear consent or a spending limit.

Mitigation: Require explicit payment confirmation, spending limits, and payment logs before enabling x402 calls.

Risk: Prompts and documents sent to the third-party gateway may contain sensitive information without reviewed data-handling terms.

Mitigation: Review and approve the operator and its data-handling terms before use; do not send secrets, regulated data, proprietary code, or private documents without approval.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/wangletiand/skills/gpt-6-x402-gateway)
- [Gateway documentation for agents](https://gpt.558686.xyz/llms.txt)
- [Gateway OpenAPI specification](https://gpt.558686.xyz/openapi.json)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Guidance]

**Output Format:** [Text or JSON responses, depending on the endpoint]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Endpoint-dependent chat, translation, research, and analysis results]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
