## Description:

Natural language bookkeeping skill that parses Chinese, English, or mixed expense descriptions and appends confirmed entries to a QianJi CSV ledger.

This skill is ready for commercial/non-commercial use.

## Publisher:

[deusyu](https://clawhub.ai/user/deusyu)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to turn natural-language bookkeeping notes into structured QianJi CSV entries. It supports category inference, multi-entry previews, explicit confirmation before writes, and append-only ledger updates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can append financial records to an unconstrained user-supplied file path.

Mitigation: Use it only with a dedicated QianJi CSV file you trust and confirm the exact destination path before any write.

Risk: Ledger notes or other text fields may contain formula-like content that spreadsheet tools could interpret.

Mitigation: Avoid opening exported ledgers in spreadsheet tools when fields may contain formula-like text, or sanitize those fields before opening.

Risk: Default account and recorder values may not match the user's bookkeeping context.

Mitigation: Review and set the recorder and account defaults before relying on the generated ledger entries.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/deusyu/skills/nl2ledger)
- [Category keyword mapping](artifact/references/category_map.md)
- [QianJi CSV schema](artifact/references/csv_schema.md)
- [Append entry script](artifact/scripts/append_entry.py)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration]

**Output Format:** [Markdown/text previews with bash command invocations and CSV row append operations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires explicit user confirmation before writing; appends one QianJi CSV row per confirmed entry.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
