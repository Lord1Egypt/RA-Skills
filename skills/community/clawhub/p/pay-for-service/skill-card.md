## Description:

Make a paid API request to an x402 endpoint with automatic USDC payment.

This skill is ready for commercial/non-commercial use.

## Publisher:

[0xrag](https://clawhub.ai/user/0xrag)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to call paid x402 API endpoints after finding a service, with wallet authentication and sufficient USDC balance in place.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can make automatic USDC payments through an authenticated wallet without mandatory per-request approval or a built-in spending cap.

Mitigation: Use it only with trusted x402 endpoints and the trusted awal CLI source, and enforce confirmation and spending limits outside the skill; use --max-amount where appropriate.

Risk: Paid requests require an authenticated wallet with sufficient USDC balance.

Mitigation: Check wallet authentication and balance before making requests, and stop if the endpoint or payment amount is unclear.

## Reference(s):


## Skill Output:

**Output Type(s):** [Shell commands, Guidance, Text, Configuration]

**Output Format:** [Markdown guidance with inline shell commands; command output may be text or JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands may make paid USDC requests through an authenticated wallet.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
