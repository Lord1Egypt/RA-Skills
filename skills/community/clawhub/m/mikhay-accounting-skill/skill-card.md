## Description:

Helps users maintain a Chinese personal ledger by importing, recording, validating, and summarizing transactions, assets, credit cards, and planned purchases using local files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mikhayeeer](https://clawhub.ai/user/mikhayeeer)

### License/Terms of Use:

MIT

## Use Case:

External users can use the skill to import and manage personal ledger data, track assets and credit-card activity, organize planned purchases, and produce monthly summaries. The skill is intended for Chinese-language bookkeeping and keeps ledger files on the user's local machine.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Using --overwrite replaces whole ledger files and can remove records absent from the new bill.

Mitigation: Keep a backup of data/ and use --overwrite only when intentionally replacing the target files.

Risk: Default refund handling changes original transaction amounts, which may not preserve the transaction history a user needs.

Mitigation: Keep raw bills and request separate linked adjustment entries when preserving transaction history is important.

Risk: Following an installation command without checking its source revision may use code the user has not reviewed.

Mitigation: Review the installer and pin the repository revision before installing.

Risk: Reimbursement-related tag breakdowns may need verification when reviewing reports.

Mitigation: Cross-check reimbursement-related tag breakdowns against the source ledger.

## Reference(s):

- [Project homepage](https://github.com/MikhayEeer/mikhay-accounting-skill)
- [ClawHub release](https://clawhub.ai/mikhayeeer/skills/mikhay-accounting-skill)
- [FAQ](references/faq.md)
- [Troubleshooting](references/troubleshooting.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, JSON, CSV, Shell commands]

**Output Format:** [Conversational guidance and summaries, with local JSON/CSV ledger and configuration files and shell commands for validation and reporting.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Ledger, asset, and wishlist data stay in local files; totals should come from the provided reporting scripts.]

## Skill Version(s):

0.4.2 (source: frontmatter, changelog, released 2026-10-20)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
