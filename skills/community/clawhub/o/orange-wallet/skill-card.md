## Description: <br>
Orange Wallet is a command-line Lightning wallet for AI agents that exposes JSON shell commands for receiving, sending, monitoring, and webhook-driven payment flows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[benthecarman](https://clawhub.ai/user/benthecarman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to give an AI agent a Lightning wallet, run wallet commands, receive payment events through polling or webhooks, and initiate payments with JSON command output. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles real funds through a Lightning wallet. <br>
Mitigation: Use only small amounts, review carefully before installing, and require explicit user approval and amount limits for agent-driven sends. <br>
Risk: Wallet recovery depends on a generated seed file stored under the configured storage path. <br>
Mitigation: Keep the seed file private with restrictive filesystem permissions and maintain encrypted backups. <br>
Risk: Webhook delivery can expose payment events or trigger downstream order fulfillment. <br>
Mitigation: Configure only HTTPS webhook endpoints you control, use bearer tokens, verify amounts and payment hashes, and make handlers idempotent. <br>
Risk: The security evidence marks the release suspicious because it handles wallet secrets and outbound payment webhooks with limited built-in safety guidance. <br>
Mitigation: Treat installation as high trust, review the skill behavior before deployment, and avoid unattended payment operations. <br>


## Reference(s): <br>
- [Orange Wallet on ClawHub](https://clawhub.ai/benthecarman/orange-wallet) <br>
- [Orange SDK](https://github.com/lightningdevkit/orange-sdk) <br>
- [Agent Payment Flows](docs/agent-payment-flows.md) <br>
- [SKILL.md](SKILL.md) <br>
- [README.md](README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands may operate on real Lightning wallet funds and may emit webhook payloads or wallet state as JSON.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata and Cargo.toml) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
