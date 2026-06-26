## Description: <br>
Real-time crypto token data, DeFi analytics, blockchain data, Twitter/X social intelligence, enhanced web search, and crypto project search in one agent skill. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wjw12](https://clawhub.ai/user/wjw12) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External developers and agent users use this skill to configure access to Heurist Mesh and query crypto token, DeFi, wallet, Twitter/X, web search, and research agents for market analysis and blockchain intelligence. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Paid crypto-data requests can spend credits or USDC if an agent proceeds without explicit approval. <br>
Mitigation: Show the tool name, request details, and price before each paid call, and require user approval before any paid request or signing action. <br>
Risk: x402 and Inflow paths can require wallet or payment private keys. <br>
Mitigation: Prefer the Heurist API-key credit path; if wallet payments are needed, use a dedicated low-balance wallet and keep payment secrets out of shared project files. <br>
Risk: Crypto analytics and market summaries can be incomplete, stale, or unsuitable as financial advice. <br>
Mitigation: Treat outputs as research inputs, verify important claims against primary sources, and avoid presenting skill output as investment advice. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/wjw12/heurist-mesh) <br>
- [Heurist Mesh](https://mesh.heurist.ai) <br>
- [Heurist API Documentation](https://docs.heurist.ai) <br>
- [Heurist Credits](https://heurist.ai/credits) <br>
- [Heurist API Key](references/heurist-api-key.md) <br>
- [x402 On-Chain Payment](references/x402-payment.md) <br>
- [Inflow Payment Platform](references/inflow-payment.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON payloads, shell commands, and API request examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce setup steps, credential checks, tool schema inspection guidance, payment flow instructions, and crypto analytics request payloads.] <br>

## Skill Version(s): <br>
1.0.3 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
