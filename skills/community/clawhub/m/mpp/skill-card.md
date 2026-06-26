## Description: <br>
mpp helps developers build Machine Payments Protocol integrations for HTTP 402 paid APIs, payment-gated services, agent payment flows, MCP tool payments, and pay-as-you-go streaming. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tenequm](https://clawhub.ai/user/tenequm) <br>

### License/Terms of Use: <br>
Apache 2.0 <br>


## Use Case: <br>
Developers and engineers use this skill to implement paid API endpoints, payment-aware clients, and payment-enabled MCP or streaming workflows with MPP SDKs across TypeScript, Python, and Rust. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Payment examples can create services or clients that spend funds, sign transactions, or call paid providers. <br>
Mitigation: Review generated code before execution, use testnet or regtest while experimenting, and require explicit spending limits for automatic retry behavior. <br>
Risk: Wallet mnemonics, private keys, OAuth tokens, and payment signing secrets may be exposed if copied into source, logs, or client bundles. <br>
Mitigation: Store secrets in appropriate secret managers or server-side environment variables, keep them out of logs and client bundles, and rotate server signing secrets with an overlap period. <br>
Risk: Payment automation against untrusted endpoints can trigger unintended charges. <br>
Mitigation: Limit automatic payment flows to trusted origins and inspect challenges before enabling unattended payments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tenequm/mpp) <br>
- [Skill homepage from metadata](https://github.com/tenequm/skills/tree/main/skills/mpp) <br>
- [MPP website](https://mpp.dev) <br>
- [Payment HTTP Authentication Scheme](https://datatracker.ietf.org/doc/draft-ryan-httpauth-payment/) <br>
- [Protocol reference](references/protocol-spec.md) <br>
- [TypeScript SDK reference](references/typescript-sdk.md) <br>
- [Python SDK reference](references/python-sdk.md) <br>
- [Rust SDK reference](references/rust-sdk.md) <br>
- [Tempo payment method reference](references/tempo-method.md) <br>
- [Stripe payment method reference](references/stripe-method.md) <br>
- [Session payment reference](references/sessions.md) <br>
- [Transport bindings reference](references/transports.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline code blocks and command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include SDK-specific examples for TypeScript, Python, Rust, HTTP, MCP, and WebSocket integrations.] <br>

## Skill Version(s): <br>
0.7.0 (source: frontmatter, changelog, release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
