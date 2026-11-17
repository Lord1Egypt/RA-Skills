## Description:

Helps agents access x402 paid API endpoints and gated content through Finance District wallet commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rachidjarray-hk-qa-fdt](https://clawhub.ai/user/rachidjarray-hk-qa-fdt)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to let an agent check wallet status, inspect balance, authorize x402 payments, and retrieve paid API or gated content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The normal one-step payment flow can spend wallet funds without a mandatory cap or precise approval step.

Mitigation: Require the agent to show the exact endpoint, amount, asset, network, recipient, and payment cap before every payment.

Risk: Unfamiliar x402 URLs can trigger paid requests through an authenticated wallet.

Mitigation: Use wallet-level limits and avoid unfamiliar endpoints unless the user has reviewed the payment details.

Risk: The artifact allows payment commands that can authorize payment and retrieve content.

Mitigation: Prefer pre-authorization or explicit human confirmation for high amounts, unfamiliar endpoints, or unclear payment requirements.

## Reference(s):

- [Pay For Service on ClawHub](https://clawhub.ai/rachidjarray-hk-qa-fdt/skills/pay-for-service-2)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return fetched paid content after wallet authentication and payment authorization.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
