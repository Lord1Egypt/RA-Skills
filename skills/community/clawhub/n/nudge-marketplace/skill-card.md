## Description:

Browse, submit, and manage AI agents on the Nudge marketplace, a wellness platform using $NUDGE tokens and the x402 payment protocol.

This skill is ready for commercial/non-commercial use.

## Publisher:

[0xrichyrich](https://clawhub.ai/user/0xrichyrich)

### License/Terms of Use:


## Use Case:

Developers and marketplace operators use this skill to discover Nudge marketplace agents, submit new agents, inspect submitted agents, and follow the documented payment flow for listings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Payment instructions include conflicting blockchain details.

Mitigation: Verify payment requirements through the live official service or UI immediately before any transaction, then confirm the chain, token contract, amount, recipient, and fees in the wallet.

Risk: Example code signs token transfers with a raw private key.

Mitigation: Use secure wallet or key management and do not paste real wallet private keys into agent workflows or examples.

Risk: Marketplace submissions can include system prompts or operational details.

Mitigation: Remove secrets and private operational details from any systemPrompt submitted to the marketplace.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/0xrichyrich/skills/nudge-marketplace)
- [Nudge marketplace website](https://www.littlenudge.app)
- [Nudge add-agent UI](https://www.littlenudge.app/add-agent)
- [x402 protocol](https://x402.org)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with curl examples, JSON payloads, and TypeScript code snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes API endpoint descriptions, request and response examples, and payment workflow guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
