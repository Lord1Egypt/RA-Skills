## Description:

AI-driven settlement assistant for parsing natural-language activity rules, confirming award-pool logic, processing local CSV or Excel data, and producing settlement results for equal-split, ranking, mixed, and weighted payout modes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[luxieng030124-max](https://clawhub.ai/user/luxieng030124-max)

### License/Terms of Use:

MIT-0

## Use Case:

External operators and developers use this skill to settle creator, marketing, sales, or challenge activities from local CSV or Excel data after reviewing and confirming the interpreted payout rules.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill attempts to override normal agent instruction hierarchy during settlement workflows.

Mitigation: Do not allow the skill to override platform, system, or user instructions; review the prompt behavior before installing or running it.

Risk: Settlement outputs affect financial or payout decisions and may be incorrect or misleading.

Mitigation: Independently verify payout totals, eligibility logic, and exported reports before using results for payment.

Risk: Exported CSV files may be unsafe to open in spreadsheet applications until formula neutralization is added.

Mitigation: Treat generated CSV files as untrusted and inspect or sanitize them before opening in spreadsheet software.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/luxieng030124-max/skills/jiesuan)
- [README](artifact/README.md)
- [Release notes](artifact/RELEASE.md)
- [Install guide](artifact/INSTALL.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python code and CSV settlement output references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Prompts users to confirm interpreted payout rules before local processing and reports settlement checks after calculation.]

## Skill Version(s):

2.1.3 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
