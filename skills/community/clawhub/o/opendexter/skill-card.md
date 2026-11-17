## Description:

Use OpenDexter to search, price-check, and pay for any x402 API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[branchmanager69](https://clawhub.ai/user/branchmanager69)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use OpenDexter to find paid x402 APIs, inspect pricing, check wallet setup, and call selected endpoints with USDC payment from a configured wallet.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can make paid x402 API calls using USDC from a configured wallet.

Mitigation: Before each paid call, require the agent to show the endpoint, exact price, chain, and whether the action repeats, then get explicit approval.

Risk: Payment may proceed without a clear final confirmation for each call.

Mitigation: Use the pricing check first and approve only one clearly described paid action at a time.

## Reference(s):

- [OpenDexter ClawHub skill page](https://clawhub.ai/branchmanager69/skills/opendexter)

## Skill Output:

**Output Type(s):** [text, JSON, API calls, guidance]

**Output Format:** [Agent-facing text and JSON-like API results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include marketplace search results, endpoint prices, wallet status, API response data, and payment receipt details.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
