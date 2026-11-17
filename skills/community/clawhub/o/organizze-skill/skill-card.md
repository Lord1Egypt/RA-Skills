## Description:

Runs Organizze personal finance API operations from the terminal for accounts, categories, transactions, credit cards, invoices, payments, and transfers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leaofelipe](https://clawhub.ai/user/leaofelipe)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to query and manage Organizze personal finance data through CLI commands that call the Organizze REST API. It supports account, category, transaction, credit card, invoice, payment, and transfer workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create, update, or delete sensitive financial records in an Organizze account.

Mitigation: Verify target IDs with list or get commands, ask the agent to summarize planned changes, and require explicit approval before any mutation or deletion.

Risk: The skill requires Organizze account credentials and can return personal finance data.

Mitigation: Install only when account access is intended, do not print or log credential values, and mask personal or financial details when summarizing results.

## Reference(s):

- [Organizze API documentation](https://github.com/organizze/api-doc)
- [Organizze app](https://app.organizze.com.br)
- [Organizze API token settings](https://app.organizze.com.br/configuracoes/api-keys)
- [ClawHub Organizze Skill page](https://clawhub.ai/leaofelipe/skills/organizze-skill)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands; CLI commands return JSON on stdout]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js, npm, ORGANIZZE_EMAIL, ORGANIZZE_TOKEN, and ORGANIZZE_USER_AGENT.]

## Skill Version(s):

1.3.4 (source: frontmatter, package.json, ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
