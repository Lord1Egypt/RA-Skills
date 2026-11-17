## Description:

Sort, rename, and organize invoices, receipts, bills, statements, and related PDF or image files into a predictable folder structure.

This skill is ready for commercial/non-commercial use.

## Publisher:

[benboby](https://clawhub.ai/user/benboby)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to clean up finance document folders, standardize invoice-like filenames, separate files by vendor, month, or document type, and prepare auditable records for bookkeeping or reimbursement workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Batch renames or moves could misfile finance documents or make records harder to audit if the proposed rule is wrong.

Mitigation: Point the agent at a specific folder, review the dry-run naming and move plan before allowing batch changes, place ambiguous files in a review folder, and preserve originals unless deletion is explicitly requested.

Risk: Invoice folders may contain sensitive financial information.

Mitigation: Limit the task scope to the intended local folder and read document contents only when filenames or metadata are insufficient for classification.

## Reference(s):

- [Invoice Sorter on ClawHub](https://clawhub.ai/benboby/skills/invoice-sorter)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown report with optional shell commands and file-operation summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include detected files, proposed folder structure, planned renames or moves, ambiguous items, and completed changes.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
