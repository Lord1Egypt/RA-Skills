## Description: <br>
Buy and sell NFTs on OpenSea's Seaport marketplace, including fulfillment, offers, new orders, cross-chain purchases, and listing sweeps with wallet signing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[opensea](https://clawhub.ai/user/opensea) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and external agents use this skill to prepare OpenSea Seaport marketplace trades, including listing fulfillment, offer acceptance, cross-chain purchases, and sweeps. It is intended for workflows where transaction details are checked before any wallet signs or broadcasts an onchain action. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Marketplace, trade, and swap flows can affect real assets when an agent has wallet-signing authority. <br>
Mitigation: Use a managed wallet with scoped policies, keep balances low, and require explicit human review before signing or broadcasting any transaction. <br>
Risk: The bundle mixes read-only guidance with transaction-building APIs and generic POST helpers. <br>
Mitigation: Route read-only tasks to opensea-api, and require extra review before using generic POST or transaction-builder helpers. <br>
Risk: OpenSea API keys, auth tokens, and wallet credentials can remain available to the agent after use. <br>
Mitigation: Provide credentials through environment variables only, avoid logging them, and remove or rotate cached API keys and auth tokens when no longer needed. <br>


## Reference(s): <br>
- [OpenSea Skill Repository](https://github.com/ProjectOpenSea/opensea-skill) <br>
- [OpenSea Marketplace API Reference](opensea-marketplace/references/marketplace-api.md) <br>
- [Seaport Reference](opensea-marketplace/references/seaport.md) <br>
- [OpenSea CLI](https://github.com/ProjectOpenSea/opensea-cli) <br>
- [OpenSea Developer Docs](https://docs.opensea.io/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, API calls, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, API request examples, and transaction review steps] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce transaction payload guidance that requires human review before signing or broadcasting.] <br>

## Skill Version(s): <br>
2.15.3 (source: package.json, CHANGELOG, and ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
