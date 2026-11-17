## Description:

Huo15 Furniture Mfg helps agents answer and act on furniture manufacturing operations in the HeySleep/和栖家居 test manufacturing system, including order tracking, production, inventory, quality, purchasing, customer records, daily overviews, confirmed write actions, and document generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaobod1](https://clawhub.ai/user/zhaobod1)

### License/Terms of Use:

MIT-0

## Use Case:

Manufacturing employees use this skill to query sales orders, production work, inventory, quality checks, purchasing, customers, and daily operating summaries from the HeySleep furniture manufacturing system. It can also prepare confirmed operational updates, customer or quote drafts, QC photo actions, and PDF business documents after user review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles ERP credentials and business records.

Mitigation: Use a least-privilege Odoo API key, keep credentials out of chat and command arguments, and review installation before use.

Risk: The promised test-only boundary is not technically enforced by the package.

Mitigation: Confirm the configured URL is https://test.heysleep.cn with db=test and avoid production credentials until endpoint and HTTPS allowlisting are enforced.

Risk: Write-capable workflows can change operational records if approved.

Mitigation: Inspect each dry-run preview before approving any command with --yes.

Risk: Generated PDFs may contain sensitive business information.

Mitigation: Treat generated PDFs as confidential business documents and share them only with intended recipients.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/zhaobod1/skills/huo15-furniture-mfg)
- [Command Reference](references/commands.md)
- [HeySleep Manufacturing API Notes](references/heysleep-mfg-api.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, code, guidance]

**Output Format:** [Markdown summaries with inline shell commands and generated local files when documents are requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Write-capable workflows are designed around dry-run previews followed by explicit user approval.]

## Skill Version(s):

1.4.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
