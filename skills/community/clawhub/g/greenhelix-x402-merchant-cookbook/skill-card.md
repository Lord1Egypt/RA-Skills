## Description:

The x402 Merchant Integration Cookbook provides practical recipes for integrating x402 payments into Express.js, FastAPI, and Cloudflare Workers services, including payment verification, settlement, and deployment patterns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mirni](https://clawhub.ai/user/mirni)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this guide to add x402 payment gates to APIs and services. It is aimed at API monetization workflows that need examples for Node.js, Python, edge workers, verification, settlement, testing, and deployment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Payment-control examples may be unsafe if copied directly into services handling real funds or protected content.

Mitigation: Treat the content as educational material and complete a security review before using it with production payment flows.

Risk: Misconfigured credentials or copied private-key examples can expose payment infrastructure.

Mitigation: Align environment variable names, remove unnecessary secrets, keep balances server-side, and avoid placing real private keys in copied test code.

Risk: Weak facilitator validation can allow access when payment verification fails or is unavailable.

Mitigation: Validate facilitator responses strictly and fail closed on verification problems before serving protected content.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mirni/skills/greenhelix-x402-merchant-cookbook)
- [GreenHelix sandbox](https://sandbox.greenhelix.net)
- [x402 protocol specification](https://www.x402.org)
- [x402 facilitator endpoint](https://x402.org/facilitator)
- [Agent Production Hardening Guide](https://clawhub.ai/skills/greenhelix-agent-production-hardening)
- [Base Sepolia faucet](https://www.coinbase.com/faucets/base-ethereum-sepolia-faucet)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guide with code blocks, configuration examples, and command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Non-executable educational material; examples require user-supplied payment, wallet, and service credentials.]

## Skill Version(s):

1.3.1 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
