## Description:

Plutus Lite summarizes up to 15 pasted expenses into categories and a basic spend breakdown, serving as a free preview of Plutus Pro.

This skill is ready for commercial/non-commercial use.

## Publisher:

[occupythemilkyway](https://clawhub.ai/user/occupythemilkyway)

### License/Terms of Use:

MIT-0

## Use Case:

External users can paste a small list of expenses and ask an agent to run a quick categorization and spend summary. The skill is useful for lightweight personal expense review, not full budgeting, tax, or forecasting workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documented install command uses a system-package override.

Mitigation: Install dependencies inside a virtual environment or remove the --break-system-packages option before running the command.

Risk: Expense text can contain personal, merchant, account, or financial details.

Mitigation: Redact unnecessary sensitive details before placing expenses in EXPENSES_TEXT.

Risk: The skill includes paid Pro upgrade prompts and external purchase links.

Mitigation: Review those links and treat the paid products as separately trusted external offerings.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/occupythemilkyway/skills/plutus-lite)
- [Plutus Lite homepage](https://clawhub.ai/occupythemilkyway/plutus-lite)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown instructions with bash and Python code blocks; runtime output is terminal tables and panels.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Processes up to 15 pasted transactions and supports USD, EUR, and GBP currency symbols.]

## Skill Version(s):

1.0.4 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
