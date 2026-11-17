## Description:

Uses plaid-cli to help agents link Plaid institutions, list account balances, and query transactions by date range.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jverdi](https://clawhub.ai/user/jverdi)

### License/Terms of Use:


## Use Case:

Developers and external users can use this skill to operate Plaid account-linking, balance, transaction search, and simple monitoring workflows through plaid-cli.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Plaid credentials and account data are handled by a third-party CLI.

Mitigation: Review the upstream plaid-cli source before installing and use sandbox or narrowly scoped Plaid credentials.

Risk: Credential and token storage protections are weakly documented.

Mitigation: Avoid plaintext config where possible, restrict ~/.plaid-cli permissions, and do not print tokens into transcripts or logs.

Risk: The monitoring example stores transaction state in /tmp.

Mitigation: Use a private per-user state directory for polling or scheduled monitoring workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jverdi/skills/plaid)
- [plaid-cli Go module](https://github.com/jverdi/plaid-cli)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with inline shell commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference JSON or CSV outputs produced by plaid-cli.]

## Skill Version(s):

0.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
