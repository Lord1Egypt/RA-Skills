## Description:

Manage Organizze personal finance data through the Organizze API, including bank accounts, credit cards, invoices, transactions, transfers, categories, budgets, and users.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rafaels-dev](https://clawhub.ai/user/rafaels-dev)

### License/Terms of Use:


## Use Case:

External users and finance-focused agent operators use this skill to inspect and manage Organizze accounts, cards, invoices, transactions, transfers, categories, and budgets through API-backed shell commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read, create, update, and delete sensitive financial records.

Mitigation: Approve every create, update, or delete operation only after checking the target resource IDs, dates, and monetary amounts.

Risk: Credentials grant access to Organizze financial data.

Mitigation: Use session environment variables or a secret manager, avoid storing tokens in shared config, and rotate the API token if exposure is suspected.

Risk: The release is non-official and has a suspicious security verdict.

Mitigation: Install only after reviewing the skill behavior and accepting the requested financial-data access.

## Reference(s):

- [Organizze API v2](https://api.organizze.com.br/rest/v2)
- [Organizze API token settings](https://app.organizze.com.br/configuracoes/api-keys)
- [ClawHub skill page](https://clawhub.ai/rafaels-dev/skills/organizze)

## Skill Output:

**Output Type(s):** [shell commands, configuration, guidance, text, JSON]

**Output Format:** [Markdown with inline shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires ORGANIZZE_EMAIL, ORGANIZZE_API_TOKEN, and ORGANIZZE_USER_AGENT environment variables.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
