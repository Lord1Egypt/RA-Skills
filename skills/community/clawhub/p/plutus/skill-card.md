## Description:

Plutus parses receipts and expense descriptions from pasted text or CSV transactions into categorized expense reports with totals, monthly trends, and budget-versus-actual comparisons.

This skill is ready for commercial/non-commercial use.

## Publisher:

[occupythemilkyway](https://clawhub.ai/user/occupythemilkyway)

### License/Terms of Use:

MIT-0

## Use Case:

Individuals, freelancers, and small business operators use this skill to turn transaction text or CSV exports into categorized spending summaries, budget comparisons, trend tables, and local Markdown/CSV reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated expense reports can persist financial data as plaintext files in the working directory.

Mitigation: Run the skill in a controlled directory and handle generated Markdown and CSV files according to the user's data retention and privacy requirements.

Risk: The documented install command uses an unpinned dependency and modifies the system Python environment.

Mitigation: Prefer a virtual environment with a pinned dependency version before running the skill.

Risk: The paid Pro skill and license flow are referenced but were not reviewed as part of this artifact.

Mitigation: Review the Pro skill, purchase link, and license handling separately before installing or relying on them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/occupythemilkyway/skills/plutus)
- [ClawHub metadata homepage](https://clawhub.ai/occupythemilkyway/plutus)
- [Publisher profile](https://clawhub.ai/user/occupythemilkyway)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with shell and Python code blocks; when run, it writes Markdown and CSV expense report files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses EXPENSES_FILE or EXPENSES_TEXT as optional input, with optional BUDGET_JSON, CURRENCY, and REPORT_MONTH configuration.]

## Skill Version(s):

1.0.4 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
