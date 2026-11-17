## Description:

Taggun (taggun.io). Use this skill for ANY Taggun request — searching and reading data. Whenever a task involves Taggun, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use the skill to search Taggun account data, extract receipt or invoice details from public HTTPS URLs, inspect campaign settings, and validate receipts against campaign rules.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The oo CLI dependency may automatically install persistent skills beyond Taggun without clearly disclosing that broader change; the deployed connector implementation was not verified.

Mitigation: Review the CLI dependency before automatic setup, use a reviewed release, and set OO_SKILLS_SYNC_DISABLED=1 to disable startup skill synchronization.

Risk: Receipt or invoice URLs submitted for extraction or validation will be processed by OOMOL and Taggun.

Mitigation: Submit only document URLs you intend OOMOL and Taggun to process.

## Reference(s):

- [Taggun homepage](https://www.taggun.io/)
- [Taggun API documentation](https://api.taggun.io/)
- [oo CLI controls](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Shell commands, Guidance]

**Output Format:** [JSON connector responses with shell command examples and Markdown guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Receipt and invoice extraction responses may contain data from submitted public HTTPS URLs.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
