## Description: <br>
Launch, trade, and monitor Monad blockchain tokens using bonding curves, permit signatures, and on-chain event queries with viem integration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zaki9501](https://clawhub.ai/user/zaki9501) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to integrate with NadFun on Monad for token trading, token creation, quote retrieval, event monitoring, wallet setup, and API key management workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide agents through workflows that use crypto private keys, session cookies, and API keys. <br>
Mitigation: Use a dedicated low-balance wallet, keep credentials out of logs, and never use a main wallet key. <br>
Risk: The skill can support blockchain trading and token-launch transactions where incorrect token, amount, slippage, deadline, gas, recipient, or contract values can cause loss. <br>
Mitigation: Inspect transaction details before signing and require manual confirmation for token, amount, slippage, deadline, gas, recipient, and contract address before any transaction. <br>


## Reference(s): <br>
- [NadFun Skill Page](https://clawhub.ai/zaki9501/nadfun-skill) <br>
- [NadFun Integration Guide](https://nad.fun/skill.md) <br>
- [NadFun ABI Reference](https://nad.fun/abi.md) <br>
- [NadFun Quote Reference](https://nad.fun/quote.md) <br>
- [NadFun Trading Reference](https://nad.fun/trading.md) <br>
- [NadFun Token Reference](https://nad.fun/token.md) <br>
- [NadFun Token Creation Reference](https://nad.fun/create.md) <br>
- [NadFun Indexer Reference](https://nad.fun/indexer.md) <br>
- [NadFun Agent API Reference](https://nad.fun/agent-api.md) <br>
- [NadFun Wallet Reference](https://nad.fun/wallet.md) <br>
- [NadFun aUSD Reference](https://nad.fun/ausd.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with TypeScript and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance may include blockchain transaction setup details, contract addresses, API endpoints, and wallet or credential handling steps.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
