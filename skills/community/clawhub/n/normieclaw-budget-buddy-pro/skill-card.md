## Description:

Budget Buddy Pro helps an AI agent organize local personal-finance data by parsing statements, categorizing transactions, building budgets, tracking bills, savings goals, and net worth, and producing spending summaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nollio](https://clawhub.ai/user/nollio)

### License/Terms of Use:

MIT-0

## Use Case:

External users and personal-finance agents use this skill to organize transaction history, create and review budgets, track recurring bills, savings goals, and net worth, and generate local spending summaries. Outputs are informational financial organization aids, not licensed financial, tax, legal, or investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Financial records may include highly sensitive merchant names, transaction details, balances, income, debt, and net-worth information.

Mitigation: Keep the local data directory protected, avoid uploading real bank or credit-card statements until reviewed, and confirm the agent platform's session retention behavior before use.

Risk: The skill's local-only privacy claims conflict with allowed web_search use for vendor lookup and exchange rates.

Mitigation: Disable web_search for this skill or require explicit per-query approval, and never send merchant names, transaction descriptions, or other transaction-derived details to external lookup tools.

Risk: The bundled scripts need hardening before handling sensitive financial data.

Mitigation: Review and harden report HTML escaping and parser output-path restrictions, then scan the scripts again before processing real statements.

## Reference(s):

- [Budget Buddy Pro ClawHub page](https://clawhub.ai/nollio/skills/normieclaw-budget-buddy-pro)
- [README.md](artifact/README.md)
- [SECURITY.md](artifact/SECURITY.md)
- [Dashboard Companion Kit Spec](artifact/dashboard-kit/DASHBOARD-SPEC.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown chat guidance, JSON data files, shell command snippets, configuration files, and optional PNG or PDF budget reports.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Processes sensitive financial records locally, stores budget data in JSON files, and may generate local visual reports; users should review outputs before making financial decisions.]

## Skill Version(s):

1.0.3 (source: server release metadata and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
