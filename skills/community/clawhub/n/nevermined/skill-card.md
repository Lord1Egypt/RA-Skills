## Description: <br>
Guides agents and developers through Nevermined payment operations, including x402 purchases, card or stablecoin delegations, API key setup, plan and agent registration, credit checks, seller revenue checks, and payment protection for TypeScript and Python agent services. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nevermined-io](https://clawhub.ai/user/nevermined-io) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and autonomous agents use this skill to buy or sell access through Nevermined, manage payment delegations, and add x402 payment protection to agent endpoints. It is intended for payment-enabled agent services that need concrete REST, SDK, and configuration guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Agents using this skill may initiate payment-related actions with real funds or live customer accounts. <br>
Mitigation: Start in the sandbox environment, use small spending limits and short delegation durations, and move to live only when the operator explicitly chooses it. <br>
Risk: API keys, delegation IDs, wallet addresses, transaction hashes, or customer identifiers could be exposed through logs or plaintext storage. <br>
Mitigation: Store NVM_API_KEY and delegation identifiers in a secret store, require HTTPS outside localhost, and avoid logging payment tokens or customer/payment identifiers. <br>


## Reference(s): <br>
- [Nevermined Payments Skill on ClawHub](https://clawhub.ai/nevermined-io/skills/nevermined) <br>
- [Nevermined App](https://nevermined.app) <br>
- [Autonomous Agent Operations](references/autonomous-operations.md) <br>
- [Client-Side Integration](references/client-integration.md) <br>
- [x402 Protocol](references/x402-protocol.md) <br>
- [Payment Plans](references/payment-plans.md) <br>
- [Seller Operations](references/seller-operations.md) <br>
- [Express.js Integration](references/express-integration.md) <br>
- [FastAPI Integration](references/fastapi-integration.md) <br>
- [MCP Server Paywall](references/mcp-paywall.md) <br>
- [Google A2A Integration](references/a2a-integration.md) <br>
- [Strands Agent Integration](references/strands-integration.md) <br>
- [LangChain and LangGraph Integration](references/langchain-integration.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration instructions, API Calls] <br>
**Output Format:** [Markdown with inline code blocks, JSON examples, and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires NVM_API_KEY for authenticated Nevermined operations.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
