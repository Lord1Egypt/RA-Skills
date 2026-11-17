## Description:

Escrow + trust scoring on Base mainnet. Checks 24K+ agents BEFORE you pay. Real dispute resolution. Works with any x402 API -- vendor doesn't need it installed.

This skill is ready for commercial/non-commercial use.

## Publisher:

[michu5696](https://clawhub.ai/user/michu5696)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use PayCrow to check an Ethereum counterparty address against PayCrow trust scoring before sending funds or calling a paid x402 API. The skill guides payment decisions based on score, confidence, and recommendation values returned by the PayCrow Trust API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may cause an agent to rely on PayCrow's external Trust API when deciding whether to pay a counterparty.

Mitigation: Review the returned score, confidence, and recommendation before acting, and use smaller payments or escrow when the result indicates caution or insufficient data.

Risk: Counterparty wallet addresses may be sent to PayCrow's external Trust API during checks.

Mitigation: Use the trust check only when sharing the wallet address with the PayCrow API is acceptable for the payment workflow.

Risk: The optional PayCrow MCP escrow flow is separate from this skill and may introduce different operational risks.

Mitigation: Review and approve any separate PayCrow MCP server installation independently before enabling escrow tool calls.

## Reference(s):

- [PayCrow ClawHub skill page](https://clawhub.ai/michu5696/skills/paycrow)
- [PayCrow source code](https://github.com/michu5696/paycrow)
- [PayCrow npm package](https://www.npmjs.com/package/paycrow)
- [PayCrow Trust API](https://paycrow-app.fly.dev)
- [PayCrow contract on BaseScan](https://basescan.org/address/0xDcA5E5Dd1E969A4b824adDE41569a5d80A965aDe)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, API Calls, Markdown]

**Output Format:** [Markdown with inline bash code blocks and trust-score interpretation guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include a curl command that queries PayCrow's external Trust API with a counterparty wallet address.]

## Skill Version(s):

1.2.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
