## Description: <br>
GStable AI Payment Protocol - enables AI Agents to discover, negotiate, and execute cryptocurrency payments on behalf of users. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[d5c5ceb0](https://clawhub.ai/user/d5c5ceb0) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and external agent users use this skill to let an OpenClaw agent inspect GStable payment links, create signed payment sessions, check balances and allowances, and prepare or submit supported stablecoin payments on Polygon, Ethereum, Arbitrum, and Base. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent broad live-wallet authority, including automatic on-chain payments. <br>
Mitigation: Use only a dedicated low-balance hot wallet and review every payment link, chain, token, recipient or executor contract, calldata, gas cost, and allowance before running payment commands. <br>
Risk: Token approvals can expose funds if approvals are broad or left in place. <br>
Mitigation: Prefer exact approval amounts for the intended payment and revoke allowances after use. <br>
Risk: A primary wallet private key would expose high-value funds to agent-driven signing and transaction execution. <br>
Mitigation: Do not use a primary wallet key; provide only the dedicated wallet key through `WALLET_PRIVATE_KEY`. <br>


## Reference(s): <br>
- [GStable AI Payment Protocol Docs](https://docs.gstable.io/zh-Hans/docs/category/ai-payment-protocol) <br>
- [GStable AI Agent Integration Docs](https://docs.gstable.io/zh-Hans/docs/category/ai-agent-integration) <br>
- [ClawHub Skill Page](https://clawhub.ai/d5c5ceb0/gstable-ai-payment) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with CLI commands and JSON command results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires WALLET_PRIVATE_KEY for signing and transaction execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: pyproject.toml and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
