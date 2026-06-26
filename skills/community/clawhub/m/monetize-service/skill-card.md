## Description: <br>
Build and deploy a paid API that other agents can pay to use via x402. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[0xRAG](https://clawhub.ai/user/0xRAG) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to create Express APIs that charge per request in USDC through x402, including route pricing, payment middleware setup, wallet address configuration, and endpoint testing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow can involve real USDC payments, paid test requests, and public deployment on Base mainnet. <br>
Mitigation: Prefer Base Sepolia for testing and require explicit confirmation before any mainnet payment, paid test request, or public deployment. <br>
Risk: The skill proposes npm, npx, node, and curl commands that install packages, run local services, or contact endpoints. <br>
Mitigation: Review package names, command arguments, and curl targets before execution. <br>
Risk: Production facilitator use requires CDP credentials and wallet-related configuration. <br>
Mitigation: Keep CDP keys and wallet credentials in environment variables or a secret manager, and avoid exposing them in code or logs. <br>


## Reference(s): <br>
- [Coinbase Developer Platform Portal](https://portal.cdp.coinbase.com) <br>
- [Monetize Service on ClawHub](https://clawhub.ai/0xRAG/monetize-service) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with bash and JavaScript code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes Express and x402 route configuration, wallet setup commands, test commands, and pricing guidance.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
