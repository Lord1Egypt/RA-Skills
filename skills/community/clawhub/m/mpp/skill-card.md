## Description: <br>
Build with MPP (Machine Payments Protocol), an open protocol for HTTP 402 machine-to-machine payments across paid APIs, payment-gated content, AI agent and MCP tool payments, pay-per-token streaming, and payment methods such as Tempo, Stripe, Lightning, and custom rails. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tenequm](https://clawhub.ai/user/tenequm) <br>

### License/Terms of Use: <br>
Apache 2.0 <br>


## Use Case: <br>
Developers and engineers use this skill to implement HTTP 402 payment flows for paid APIs, payment-gated services, AI agent payments, MCP tool payments, streaming usage billing, and multi-method payment acceptance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Payment and wallet examples may involve financially sensitive secrets or real funds if adapted directly. <br>
Mitigation: Use testnet or sandbox funds first, keep private keys, mnemonics, and server signing secrets in secret storage, and avoid hardcoding production credentials. <br>
Risk: Automatic HTTP 402 payment handling can let agents or services initiate payments without enough business controls. <br>
Mitigation: Add spend limits, allowlists, and explicit user or policy confirmation before enabling automatic payment handling against real endpoints. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tenequm/skills/mpp) <br>
- [Project homepage](https://github.com/tenequm/skills/tree/main/skills/mpp) <br>
- [Protocol specification](references/protocol-spec.md) <br>
- [TypeScript SDK](references/typescript-sdk.md) <br>
- [Python SDK](references/python-sdk.md) <br>
- [Rust SDK](references/rust-sdk.md) <br>
- [Sessions](references/sessions.md) <br>
- [Transports and MCP](references/transports.md) <br>
- [Tempo payment method](references/tempo-method.md) <br>
- [Stripe payment method](references/stripe-method.md) <br>
- [Lightning payment method](references/lightning-method.md) <br>
- [Custom payment methods](references/custom-methods.md) <br>
- [IETF Payment HTTP Authentication draft](https://datatracker.ietf.org/doc/draft-ryan-httpauth-payment/) <br>
- [Tempo documentation](https://docs.tempo.finance) <br>
- [Privy agentic wallets guide](https://docs.privy.io/recipes/agent-integrations/agentic-wallets) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with code snippets, install commands, protocol examples, and configuration notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference payment-related environment variables such as MPP_SECRET_KEY, MNEMONIC, server_secret, and TEMPO_RPC_URL.] <br>

## Skill Version(s): <br>
0.8.1 (source: server release evidence, skill metadata, and changelog; released 2026-07-01) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
