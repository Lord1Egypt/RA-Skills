## Description:

Helps agents discover LocalSquare town-board ad space and, with explicit user approval, claim a paid local business advertising pin through x402.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thatdudefreak](https://clawhub.ai/user/thatdudefreak)

### License/Terms of Use:


## Use Case:

Small-business owners, marketers, and agents use this skill to find available LocalSquare grid cells by ZIP code and claim an advertising pin after the user approves the town, cell, cost, and payment details.

### Deployment Geography for Use:

United States

## Known Risks and Mitigations:

Risk: The workflow can initiate a real paid advertising claim and public posting.

Mitigation: Require explicit user approval before payment, show the town, cell, price, and total cost, and verify recipient and payment details before signing.

Risk: Wallet signing could expose funds if private keys are pasted into the agent or payment details are not checked.

Mitigation: Use only an external wallet signer, never provide raw private keys to the agent, and confirm the x402 facilitator, recipient, network, and amount before signing.

Risk: Lifetime-versus-expiration language could affect user expectations about the purchased pin.

Mitigation: Clarify the lifetime, expiration, and renewal terms with LocalSquare before purchase when that commitment matters to the user.

Risk: Business address, phone number, and listing details may become publicly visible on the advertising page.

Mitigation: Confirm with the user which business details should be included before submitting the claim.

## Reference(s):

- [LocalSquare homepage](https://yourlocalsquare.com)
- [LocalSquare AI documentation](https://yourlocalsquare.com/llms.txt)
- [LocalSquare agent API status](https://yourlocalsquare.com/api/agent/status)
- [LocalSquare x402 discovery](https://yourlocalsquare.com/.well-known/x402.json)
- [x402 protocol](https://x402.org)
- [ClawHub skill page](https://clawhub.ai/thatdudefreak/skills/localsquare-ads)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with HTTP endpoint examples, JSON payloads, and user-consent guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes free discovery calls, paid claim workflow details, wallet-safety requirements, and post-claim result links.]

## Skill Version(s):

2.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
