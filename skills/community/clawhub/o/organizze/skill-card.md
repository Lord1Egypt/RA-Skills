## Description: <br>
Manage Organizze personal finance data through the Organizze API, including bank accounts, credit cards, invoices, transactions, transfers, categories, and budgets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rafaels-dev](https://clawhub.ai/user/rafaels-dev) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External Organizze users use this skill to let an agent inspect and manage personal finance records through local Organizze API calls. It supports account, card, invoice, transaction, transfer, category, budget, and user workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read and change Organizze financial records when provided with the user's Organizze credentials. <br>
Mitigation: Install only when agent access to Organizze finance data is intended, and require confirmation of exact record IDs, amounts, dates, and target resources before write or delete actions. <br>
Risk: Organizze email and API token exposure could allow unauthorized access to financial data. <br>
Mitigation: Keep credentials in environment variables when possible, never reveal or log them, and rotate the API token if exposure is suspected. <br>


## Reference(s): <br>
- [Organizze API v2](https://api.organizze.com.br/rest/v2) <br>
- [Organizze API key settings](https://app.organizze.com.br/configuracoes/api-keys) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local environment variables for Organizze credentials and may propose read, write, update, or delete API calls.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
