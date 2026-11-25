## Description:

Operate PDFCraft through an OOMOL-connected account to read, create, update, and delete PDFCraft data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Users and developers use this skill to inspect PDFCraft action schemas, submit PDF or EPUB transformations, and retrieve task results through an OOMOL-connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: First-time setup includes an unpinned installer downloaded from the internet and run with the user's account privileges; the scanner could not assess its behavior and marked the scan partial.

Mitigation: Review the installer source and contents and confirm it is the expected oo CLI installer before running it.

Risk: Some PDFCraft actions can change state, delete or overwrite data, or use OOMOL credits.

Mitigation: Inspect the live action schema and confirm the exact effect and payload with the user before running tagged write or destructive actions.

## Reference(s):

- [PDFCraft MCP documentation](https://pdfcraft.ai/zh-CN/docs/getting-started/mcp)
- [PDFCraft homepage](https://pdfcraft.ai)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [oo CLI install guide](https://cli.oomol.com/install-guide.md)
- [PDFCraft ClawHub release](https://clawhub.ai/oomol/skills/oo-pdfcraft)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Guidance]

**Output Format:** [Shell command examples and JSON payload guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Actions may read data, change state, or use OOMOL credits; confirm tagged write and destructive actions before running them.]

## Skill Version(s):

1.0.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
