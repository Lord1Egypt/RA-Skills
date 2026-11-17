## Description:

Buy, hold, rebalance and sell a basket of Coinbase tokenized US stocks (NVDA, AAPL, META, GOOGL) on Base from $1 through the free Liquid Agent API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leftychris13](https://clawhub.ai/user/leftychris13)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to guide an agent through buying, checking, rebalancing, transferring, or redeeming a four-stock tokenized equity basket on Base using USDC and wallet-signed transactions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks agents to sign wallet authorizations and server-generated blockchain transactions.

Mitigation: Use only a wallet suitable for experimental on-chain trading and verify every transaction, permit, and typed-data prompt before signing.

Risk: Gasless EIP-7702 signing and x402 paid retries can introduce delegation or payment-control risk.

Mitigation: Avoid gasless EIP-7702 signing unless the user understands the delegation, and require explicit approval before any paid x402 retry.

Risk: Send and redeem actions are irreversible once mined.

Mitigation: Require explicit confirmation of the recipient, shares, amount, and action before broadcasting.

## Reference(s):

- [Liquid Agent API](https://api.liquidagent.ai)
- [Liquid Agent Guide](https://api.liquidagent.ai/v1/guide)
- [Liquid Agent OpenAPI Specification](https://api.liquidagent.ai/openapi.json)
- [Liquid Agent LLM Instructions](https://api.liquidagent.ai/llms.txt)
- [Base Mainnet RPC](https://mainnet.base.org)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with HTTP endpoint examples and inline bash commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl and a Base wallet that can review and sign transactions or typed data.]

## Skill Version(s):

1.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
