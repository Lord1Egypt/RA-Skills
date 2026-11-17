## Description:

Orange Wallet provides a command-line Lightning wallet for AI agents, with JSON shell commands for balances, invoices, payments, transactions, channels, events, and wallet information.

This skill is ready for commercial/non-commercial use.

## Publisher:

[benthecarman](https://clawhub.ai/user/benthecarman)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to give an AI agent a Lightning wallet interface for receiving payments, sending payments, monitoring wallet events, and integrating webhook or polling-based payment flows. It is intended for small, carefully reviewed balances because the release handles real funds.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles real Lightning funds and the security evidence flags the release for review before use with real funds.

Mitigation: Review before installing or operating it, start only with small test balances, and avoid using it for large sums.

Risk: The wallet seed is stored plainly in the configured storage directory.

Mitigation: Protect and back up the seed file, restrict permissions on the storage directory, and treat the storage path as sensitive wallet material.

Risk: Payment events can be sent to arbitrary webhook endpoints.

Mitigation: Use HTTPS endpoints you trust, configure bearer tokens, verify webhook authorization, and avoid HTTP webhooks.

Risk: Setup instructions include remote shell installation flows for dependencies.

Mitigation: Prefer safer Rust and protoc installation methods that match the operator's platform and supply-chain policy.

## Reference(s):

- [ClawHub Orange Wallet skill page](https://clawhub.ai/benthecarman/skills/orange-wallet)
- [Agent payment flows](docs/agent-payment-flows.md)
- [Orange SDK](https://github.com/lightningdevkit/orange-sdk)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Configuration, Guidance]

**Output Format:** [Markdown instructions with shell command examples, TOML configuration snippets, and JSON command output examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces wallet commands and event-handling guidance for a local CLI daemon; command responses are structured JSON and errors are returned as JSON with non-zero exit codes.]

## Skill Version(s):

0.1.0 (source: release metadata and Cargo.toml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
