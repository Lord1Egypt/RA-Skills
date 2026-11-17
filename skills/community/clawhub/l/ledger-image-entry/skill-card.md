## Description:

Identifies receipt, order, or invoice details from images and converts merchant, date, amount, and item details into structured ledger entries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shing19](https://clawhub.ai/user/shing19)

### License/Terms of Use:

MIT-0

## Use Case:

External users can use this skill to convert receipt, order, or invoice images into itemized bookkeeping entries, including merchant, date, category, amount, notes, and a confirmation table.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Receipt, order, or invoice images may contain sensitive purchase data.

Mitigation: Install only if users are comfortable sending images to the configured image-recognition model, and review sensitive receipts manually.

Risk: Image recognition may miss unclear details or infer categories or dates incorrectly.

Mitigation: Review extracted entries before bookkeeping; ask the user to confirm unclear receipts or categories and use the current date only when no date is visible.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/shing19/skills/ledger-image-entry)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown confirmation table with ledger rows and total amount]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Amounts use two decimal places; ambiguous dates or categories may require user confirmation.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
