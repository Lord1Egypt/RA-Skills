## Description: <br>
Integrates Privy authentication, embedded wallets, and agent payment protocols into web and agentic apps. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tenequm](https://clawhub.ai/user/tenequm) <br>

### License/Terms of Use: <br>
Apache 2.0 <br>


## Use Case: <br>
Developers and agent builders use this skill to add Privy authentication, embedded or agentic wallets, wallet policies, Solana and EVM integrations, and x402 or MPP payments to web and agentic applications. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Wallet and payment examples can lead to real-money transfers or signed transactions if copied into an agent without controls. <br>
Mitigation: Use testnet or sandbox defaults first, require explicit user confirmation, set spend caps, and enforce recipient and domain allowlists before any production use. <br>
Risk: Autonomous wallet or private-key operations can exceed user intent without strict approval boundaries. <br>
Mitigation: Apply strict approval policies, audit logging, and revocation paths for autonomous or private-key operations. <br>
Risk: Privy server flows rely on sensitive credentials and webhook secrets. <br>
Mitigation: Store secrets outside source control, redact them from logs, and verify webhook signatures before trusting inbound events. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tenequm/privy-integration) <br>
- [ClawHub metadata homepage](https://github.com/tenequm/skills/tree/main/skills/privy-integration) <br>
- [Privy LLM documentation index](https://docs.privy.io/llms-full.txt) <br>
- [React SDK Reference](references/react-sdk.md) <br>
- [Server SDK Reference](references/server-sdk.md) <br>
- [Wallets Reference](references/wallets.md) <br>
- [Solana Integration Reference](references/solana.md) <br>
- [Agent Payments Reference](references/agent-payments.md) <br>
- [Agent Auth and Agentic Wallets Reference](references/agent-auth.md) <br>
- [x402 protocol](https://x402.org) <br>
- [MPP protocol](https://mpp.dev) <br>
- [Agent Auth Protocol](https://agentauthprotocol.com) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with TypeScript, TSX, JSON, and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces integration guidance and examples for Privy authentication, wallets, policies, and payment flows; it does not itself execute wallet or payment operations.] <br>

## Skill Version(s): <br>
0.4.0 (source: SKILL.md metadata and CHANGELOG, released 2026-06-04) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
