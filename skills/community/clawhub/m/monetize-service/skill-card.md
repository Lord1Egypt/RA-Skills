## Description:

Build and deploy a paid API that other agents can pay to use via x402.

This skill is ready for commercial/non-commercial use.

## Publisher:

[0xrag](https://clawhub.ai/user/0xrag)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to create Express APIs that charge per request in USDC over x402, configure paid routes, and test payment flows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide real-money USDC payment flows on Base mainnet.

Mitigation: Test on base-sepolia first, verify the payment recipient address independently, and require explicit user confirmation before any command that can spend funds.

Risk: The skill uses executable npm and npx tooling, including latest-tag commands.

Mitigation: Run in a sandboxed workspace and pin exact package versions before production use.

Risk: Production facilitator setup can involve CDP credentials.

Mitigation: Protect CDP_API_KEY_ID and CDP_API_KEY_SECRET, avoid exposing them in logs or committed files, and confirm before commands that use wallet or CDP credentials.

## Reference(s):

- [Monetize Service on ClawHub](https://clawhub.ai/0xrag/skills/monetize-service)
- [Coinbase Developer Platform portal](https://portal.cdp.coinbase.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash and JavaScript code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance covers wallet setup, payment recipient configuration, route pricing, network choice, testing, and credential considerations.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
