## Description:

Access Monzo bank account - check balance, view transactions, manage pots, send feed notifications. For personal finance queries and banking automation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rhesketh](https://clawhub.ai/user/rhesketh)

### License/Terms of Use:

MIT

## Use Case:

External users and agents use this skill to access a user's Monzo account for balance checks, transaction review, savings pot management, receipts, webhooks, and in-app feed notifications.

### Deployment Geography for Use:

United Kingdom

## Known Risks and Mitigations:

Risk: The skill handles banking OAuth tokens and money-related actions.

Mitigation: Install only on a machine the user controls, store MONZO_KEYRING_PASSWORD in a password manager or secret manager, and require explicit confirmation before deposits, withdrawals, receipt deletion, or webhook changes.

Risk: OAuth secrets or the keyring password may be exposed through command-line use, environment handling, or command history.

Mitigation: Avoid passing OAuth secrets on the command line, restrict configuration file permissions, and rotate or revoke Monzo OAuth credentials if the environment or history may have been exposed.

Risk: Changing the Monzo API endpoint could redirect sensitive requests.

Mitigation: Leave MONZO_API_BASE unset unless the endpoint has been audited.

## Reference(s):

- [ClawHub Monzo skill page](https://clawhub.ai/rhesketh/skills/monzo)
- [OpenClaw repository](https://github.com/openclaw/openclaw)
- [Monzo developer portal](https://developers.monzo.com/)
- [Monzo website](https://monzo.com)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Human-readable CLI text or JSON from shell scripts, with setup and troubleshooting guidance in Markdown.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return sensitive banking account, balance, transaction, pot, receipt, webhook, and authentication status data.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
