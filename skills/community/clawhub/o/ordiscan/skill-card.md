## Description:

Inscribe content on Bitcoin via the Ordiscan API, with per-request USDC payments on Base using the x402 protocol.

This skill is ready for commercial/non-commercial use.

## Publisher:

[t4t5](https://clawhub.ai/user/t4t5)

### License/Terms of Use:


## Use Case:

External developers and agents use Ordiscan to query Ordinals data or inscribe user-provided content on Bitcoin. The skill guides paid Ordiscan API requests through x402 using either a local signing script or an existing authenticated wallet flow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles raw wallet private keys and signs USDC transfer authorizations for x402 payments.

Mitigation: Use a dedicated low-balance wallet, avoid exposing a primary private key through X402_PRIVATE_KEY or ~/.evm-wallet.json, and verify every payment amount and recipient out of band before signing.

Risk: Paid Ordiscan requests can spend USDC without enough local validation or hard spending controls.

Mitigation: Prefer pinned, reviewed dependencies or a wallet flow that enforces a hard maximum spend, and check the 402 price response before retrying with a payment signature.

Risk: Inscription content and recipient addresses are sent to Ordiscan, and inscription content becomes permanently public on Bitcoin.

Mitigation: Only submit content intended for public blockchain publication and avoid private, sensitive, or regulated data.

## Reference(s):

- [Ordiscan API documentation](https://ordiscan.com/docs/api)
- [Ordiscan API markdown documentation](https://ordiscan.com/docs/api.md)
- [ClawHub skill page](https://clawhub.ai/t4t5/skills/ordiscan)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions, API Calls]

**Output Format:** [Markdown with inline bash and JSON code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include x402 payment headers, Ordiscan API responses, and Bitcoin inscription links.]

## Skill Version(s):

0.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
