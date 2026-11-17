## Description:

27 tools for DeFi, DEX swaps, cross-chain bridges, Twitter/X, on-chain token data, crypto utilities, and LLM access via x402 micro-payments on Base.

This skill is ready for commercial/non-commercial use.

## Publisher:

[foodaka](https://clawhub.ai/user/foodaka)

### License/Terms of Use:


## Use Case:

External users, developers, and agents use Paytoll to access paid DeFi intelligence, DEX swap and bridge quotes, on-chain token analytics, Twitter/X actions, crypto utilities, and LLM calls through a configured wallet on Base.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The MCP package receives a raw wallet private key and is installed from npm without a pinned version in this artifact.

Mitigation: Use a dedicated wallet with minimal funds, review or pin the MCP server package before use, monitor the wallet, and never configure a main or broadly funded wallet key.

Risk: Tool calls make paid USDC micropayments automatically from the configured wallet.

Mitigation: Inform the user before paid calls, batch requests to reduce cost, and keep only enough USDC and ETH on Base for the intended activity.

Risk: DeFi transaction-building tools can produce unsigned transaction data for swaps, bridges, lending, borrowing, repayment, and withdrawal workflows.

Mitigation: Require user review before signing or broadcasting any transaction and remind the user that generated transaction data is not executed by the skill.

## Reference(s):

- [Paytoll ClawHub page](https://clawhub.ai/foodaka/skills/paytoll)
- [Paytoll homepage](https://paytoll.io)
- [Paytoll MCP repository](https://github.com/foodaka/paytoll-mcp)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown or plain text responses with tool outputs and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Tool calls may incur USDC micropayments on Base and transaction-building tools return unsigned transaction data.]

## Skill Version(s):

1.0.8 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
