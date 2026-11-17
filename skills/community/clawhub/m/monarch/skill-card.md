## Description:

Access Monarch Money financial data for accounts, transactions, budgets, cashflow, and linked-account refreshes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[silentknight87](https://clawhub.ai/user/silentknight87)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to query a user's Monarch Money account for balances, transactions, budgets, monthly cashflow, and account refresh status through local CLI wrapper scripts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles highly sensitive financial credentials and long-lived Monarch Money sessions.

Mitigation: Use only on a trusted personal machine, avoid shared or recorded terminals, and delete ~/.monarchmoney/mm_session.pickle when local access should no longer be retained.

Risk: Server security guidance flags weak local safeguards around password prompting and session-file permissions.

Mitigation: Review before installing and consider fixing the password prompt and session-file permissions before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/silentknight87/skills/monarch)
- [Publisher profile](https://clawhub.ai/user/silentknight87)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, JSON data]

**Output Format:** [JSON from CLI commands with Markdown setup guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires prior interactive authentication and a local Monarch Money session file.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
