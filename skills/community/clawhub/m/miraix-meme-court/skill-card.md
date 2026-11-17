## Description:

Miraix Meme Court shortlists Solana meme candidates, applies Rug Court safety and liquidity checks, approves one disciplined trade, and can prepare or check an unsigned order payload when live execution is available.

This skill is ready for commercial/non-commercial use.

## Publisher:

[richard7463](https://clawhub.ai/user/richard7463)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to run a concise Solana meme-trade screening workflow: fetch a desk result, summarize the approved trade and Rug Court findings, and optionally prepare or check an unsigned order payload.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can contact app.miraix.fun with wallet, budget, strategy, trade, and order details.

Mitigation: Use it only when sharing those fields with that service is acceptable, and confirm the wallet, budget, risk mode, strategy, and payload-preparation request before running the workflow.

Risk: Crypto trade recommendations can be incorrect, stale, or based on preview-mode data.

Mitigation: Surface API warnings and dataMode, preserve important numeric fields, and state preview mode explicitly when the API reports fallback data.

Risk: Users may mistake unsigned payload preparation for a signed, submitted, or filled trade.

Mitigation: Do not claim live signing, order creation, submission, or fills unless the API response proves that outcome.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/richard7463/skills/miraix-meme-court)
- [Miraix meme rotation desk API](https://app.miraix.fun/api/meme-rotation-desk)
- [Miraix payload preparation API](https://app.miraix.fun/api/meme-rotation-desk/prepare)
- [Miraix order status API](https://app.miraix.fun/api/meme-rotation-desk/order-status)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Concise Markdown summary with optional curl API calls and JSON-derived field values]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include trade size, allocation, rationale, invalidation, take-profit ladder, execution readiness, warnings, and preview-mode status.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
