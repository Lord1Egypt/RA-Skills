## Description:

Manage LNbits Lightning Wallet (Balance, Pay, Invoice)

This skill is ready for commercial/non-commercial use.

## Publisher:

[talvasconcelos](https://clawhub.ai/user/talvasconcelos)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to manage an LNbits Lightning wallet from an agent, including checking balances, creating invoices, decoding invoices, and paying invoices after explicit confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can use an LNbits key with authority to view wallet data and send Lightning payments.

Mitigation: Use a dedicated LNbits wallet with limited funds and install only when this payment authority is acceptable.

Risk: Wallet admin keys and related credentials could be exposed if copied into chat or logs.

Mitigation: Store LNBITS_API_KEY and LNBITS_BASE_URL outside chat in environment configuration and do not display admin keys, user IDs, or wallet IDs.

Risk: Payments may be sent to an unintended invoice or server.

Mitigation: Set LNBITS_BASE_URL only to a trusted HTTPS LNbits server, decode and manually verify every invoice, check balance first, and require explicit yes/no confirmation before payment.

## Reference(s):

- [LNbits](https://lnbits.com)
- [ClawHub skill page](https://clawhub.ai/talvasconcelos/skills/lnbits)
- [LNbits demo server](https://demo.lnbits.com)
- [LNbits default server used by helper script](https://legend.lnbits.com)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, JSON, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON CLI responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 plus LNBITS_API_KEY and LNBITS_BASE_URL environment variables for normal wallet operations.]

## Skill Version(s):

1.0.0 (source: server evidence release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
