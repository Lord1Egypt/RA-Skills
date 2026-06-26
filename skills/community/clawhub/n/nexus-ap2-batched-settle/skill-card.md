## Description: <br>
Atomically settle up to 20 AI agent payments in a single XRPL Batch transaction. Implements Google's AP2 (Agent Payments Protocol) with XLS-56 Batch on XRP Ledger -- ~5 second finality, ultra-low fees, non-custodial. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cyberforexblockchain](https://clawhub.ai/user/cyberforexblockchain) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and autonomous-agent operators use this skill to create AP2 payment mandates and prepare unsigned XRPL single or batched settlement transactions for user wallet signing. It is intended for agent-payment workflows where buyers retain custody and independently review payment details before broadcast. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill prepares payment mandates and wallet transactions through a hosted NEXUS service. <br>
Mitigation: Use testnet and sandbox signatures first, verify the hosted endpoint and selected network, and deploy only when an agent-payment workflow tied to this service is intentional. <br>
Risk: Unsigned XRPL transactions can transfer value if the user signs and broadcasts incorrect details. <br>
Mitigation: Independently check every amount, destination, currency, issuer, mandate, trust line, and batch item before signing or broadcasting. <br>
Risk: Wallet secrets or private keys could be exposed if entered into the wrong tool or service. <br>
Mitigation: Never share wallet seeds or private keys with the hosted service or the agent; sign only in a trusted local wallet. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/cyberforexblockchain/nexus-ap2-batched-settle) <br>
- [AP2 Protocol](https://ap2-protocol.org/) <br>
- [XRPL Batch Transactions](https://xrpl.org/docs/concepts/transactions/batch-transactions) <br>
- [AP2 Config Endpoint](https://ai-service-hub-15.emergent.host/api/ap2/config) <br>
- [XRPL Config Endpoint](https://ai-service-hub-15.emergent.host/api/xrpl/config) <br>
- [A2A Agent Card](https://ai-service-hub-15.emergent.host/.well-known/agent.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance, JSON] <br>
**Output Format:** [Markdown guidance with curl examples and JSON transaction payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces unsigned XRPL payment or XLS-56 batch transaction JSON for local wallet review, signing, and broadcast.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
