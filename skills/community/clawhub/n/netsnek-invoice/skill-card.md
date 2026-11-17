## Description:

Creates and manages invoices as JSON files on GitHub with sequential numbering, preview, and upload.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kleberbaum](https://clawhub.ai/user/kleberbaum)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to create, preview, list, and upload invoice or offer JSON records to a private GitHub repository for downstream PDF generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unsafe user-influenced prefix, year, or invoice number values may reach local scripts.

Mitigation: Constrain prefix, year, and invoice number values to expected formats before running scripts; reject arbitrary values.

Risk: Existing invoice records can be overwritten despite the stated guardrails.

Mitigation: Require the upload path to refuse existing-file overwrites unless a separate explicit overwrite confirmation is implemented.

Risk: Business-sensitive invoice data and GitHub credentials are handled by the workflow.

Mitigation: Use a dedicated private invoice repository and a short-lived fine-grained GitHub token limited to that repository.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/kleberbaum/skills/netsnek-invoice)
- [README](artifact/README.md)
- [Basic Invoice Creation Example](artifact/examples/basic.md)
- [Invoice Commands Example](artifact/examples/commands.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration instructions]

**Output Format:** [Markdown/plain text guidance with JSON invoice records and bash command invocations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires GITHUB_TOKEN and INVOICE_REPO; can write invoice JSON files to a configured GitHub repository.]

## Skill Version(s):

1.1.0 (source: frontmatter, claw.json, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
