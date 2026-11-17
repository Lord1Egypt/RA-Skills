## Description:

Professional Quantitative Intelligence & DeFi Execution for AI Agents. 10 years of news-price correlation, Enso DeFi super-aggregator (200+ DEXs, 15+ chains), cross-chain bridge (Across Protocol), and Privy TEE-secured wallets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bidurs](https://clawhub.ai/user/bidurs)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agent builders use this skill to guide agents through YieldCircle crypto intelligence, DeFi execution, cross-chain bridge, wallet, and paid proxy API workflows. It supports market analysis and transaction-oriented API calls that should remain subject to explicit user approval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Agents may initiate crypto swaps, bridges, yield actions, wallet creation, email, SMS, or scraping through external APIs.

Mitigation: Require explicit approval before each execution path and set spending, slippage, route, and action limits before deployment.

Risk: Incorrect receiver addresses, chain IDs, token amounts, or bridge routes can cause irreversible financial loss.

Mitigation: Verify receiver addresses, chain IDs, token symbols, amounts, and dry-run outputs before submitting any transaction.

Risk: The skill uses API keys or x402 payment headers and may involve sensitive wallet or personal data.

Mitigation: Store credentials outside prompts, avoid sharing private keys or wallet credentials, and send only necessary personal data to the API.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bidurs/skills/newsriver-intelligence)
- [YieldCircle homepage](https://showcase.yieldcircle.app)
- [YieldCircle pricing](https://agent.yieldcircle.app/#pricing)

## Skill Output:

**Output Type(s):** [Guidance, API Calls, Shell commands, Analysis, Configuration instructions]

**Output Format:** [Markdown with inline HTTP endpoint descriptions and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference API-key or x402 payment authentication and transaction parameters such as receiver addresses, slippage, chain IDs, and asset amounts.]

## Skill Version(s):

1.0.13 (source: ClawHub release metadata, created 2026-03-10T15:49:29Z)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
