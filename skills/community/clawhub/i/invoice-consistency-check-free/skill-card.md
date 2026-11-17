## Description:

Checks invoice and expense-claim text for locally recomputable arithmetic, date, title/entity, duplicate-invoice, placeholder, and amount-writing inconsistencies, with each finding tied to source evidence.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, finance reviewers, and developers use this skill to check invoice or reimbursement text before submission or review. It identifies self-contained inconsistencies in amounts, taxes, totals, dates, entities, duplicates, and placeholders without making tax, audit, authenticity, or business-approval decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may treat consistency findings or a clean result as tax, audit, invoice-authenticity, or reimbursement-approval advice.

Mitigation: Treat outputs as arithmetic and text evidence only, and keep tax, audit, authenticity, and policy decisions in human or institutional review.

Risk: The skill only processes invoice or reimbursement text that the user intentionally supplies.

Mitigation: Run it only on intended files and convert PDFs or images to text before use; do not expect it to inspect unprovided documents or images.

Risk: Insufficient or unlabeled input can prevent reliable checks.

Mitigation: Provide labeled invoice fields or table-like line items; when evidence is inadequate, rely on the insufficient-input result rather than treating it as a clean check.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/invoice-consistency-check-free)
- [ClawHub publisher profile](https://clawhub.ai/user/chenqg618)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Human-readable text or JSON containing findings, summary verdict, executed checks, withheld checks, evidence, and advice.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Local Node.js execution; returns insufficient-input status instead of a clean verdict when invoice evidence is not adequate.]

## Skill Version(s):

1.0.50 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
