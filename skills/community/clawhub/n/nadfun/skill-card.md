## Description: <br>
Decentralized Monad token launchpad guidance for bonding curve trading, token creation, event streaming, and historical data querying with viem. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[portdeveloper](https://clawhub.ai/user/portdeveloper) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, traders, bot builders, and analytics teams use this skill to integrate with NadFun on Monad for quotes, trades, token creation, token operations, event indexing, and agent-facing REST API access. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill guides agents through real crypto wallet and NadFun account operations. <br>
Mitigation: Use a dedicated low-balance wallet and require human review before signing or sending transactions. <br>
Risk: Examples involve private keys, session cookies, and API keys. <br>
Mitigation: Never paste, hardcode, print, or log production secrets; store credentials outside prompts and code snippets. <br>
Risk: Token approvals and spender addresses can authorize asset movement. <br>
Mitigation: Verify contract, spender, network, and approval amount before signing; avoid unlimited approvals unless intentionally accepted. <br>
Risk: The skill includes remote download instructions from nad.fun. <br>
Mitigation: Review downloaded files before execution or reliance. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/portdeveloper/nadfun) <br>
- [Publisher profile](https://clawhub.ai/user/portdeveloper) <br>
- [NadFun integration guide](https://nad.fun/skill.md) <br>
- [NadFun agent API guide](https://nad.fun/agent-api.md) <br>
- [NadFun trading guide](https://nad.fun/trading.md) <br>
- [NadFun token creation guide](https://nad.fun/create.md) <br>
- [NadFun wallet guide](https://nad.fun/wallet.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with TypeScript and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes viem examples, API request patterns, contract addresses, and network configuration for Monad testnet and mainnet.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
