## Description:

PayMe enables agents to connect to PayMe smart wallets, check balances, send USDC/USDT payments, manage contacts and history, and sell crypto for local currency through supported P2P workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[variousfoot](https://clawhub.ai/user/variousfoot)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to let an agent operate PayMe wallet workflows after account connection, including balance checks, stablecoin transfers, contact management, and P2P sell flows with user confirmation.

### Deployment Geography for Use:

Global for wallet features; P2P sell workflows are documented for Nigeria, Ghana, Kenya, South Africa, Cameroon, Senegal, Benin, Togo, Tanzania, and Uganda.

## Known Risks and Mitigations:

Risk: Broad renewable payment tokens can grant wallet access and payment capabilities if exposed.

Mitigation: Use encrypted secret storage, avoid logging or committing tokens, surface token expiry to the user, and revoke tokens when access is no longer needed.

Risk: Chat-based account creation can expose a newly chosen financial PIN in the conversation transcript.

Mitigation: Prefer the web-generated connection-code flow; if account creation is used, tell the user to delete the PIN message and rotate the PIN in PayMe afterward.

Risk: Direct Execute can complete transfers in one API call when the user has explicitly enabled it.

Mitigation: Keep Direct Execute off unless the user intentionally accepts one-call transfers, and use the preview plus explicit confirmation flow for normal payments.

## Reference(s):

- [PayMe Agent API Reference](references/api-reference.md)
- [PayMe Homepage](https://payme.feedom.tech)
- [ClawHub Skill Page](https://clawhub.ai/variousfoot/skills/payme)

## Skill Output:

**Output Type(s):** [Guidance, API calls, Shell commands, Configuration]

**Output Format:** [Markdown guidance with REST API request examples and JSON payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Instruction-only artifact; no executable code, scripts, or binaries.]

## Skill Version(s):

1.0.27 (source: server release metadata, created 2026-03-25T10:00:02Z)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
