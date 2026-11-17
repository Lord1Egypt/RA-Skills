## Description:

Parse PDF, image, Word, or PPT files with SoMark and publish the result to Feishu, DingTalk, or Notion as editable documents, spreadsheets, record tables, or databases.

This skill is ready for commercial/non-commercial use.

## Publisher:

[soul-code](https://clawhub.ai/user/soul-code)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and document operations users use this skill to convert SoMark-parsed PDFs, images, Word, or PPT files into editable Feishu, DingTalk, or Notion documents, spreadsheets, record tables, or databases.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Spreadsheet image workflows can fetch arbitrary URLs from parsed content and upload the results to cloud workbooks.

Mitigation: Use only trusted documents and trusted SoMark Markdown/JSON; avoid spreadsheet imports containing untrusted image URLs until downloader host restrictions are enforced.

Risk: The skill can create or modify cloud documents, sheets, Bases, or Notion pages with the user's authenticated platform tools.

Mitigation: Review the destination, route, and authenticated profile before execution, and inspect generated previews or manifests for unexpected changes.

Risk: Parsed document content and local output directories may contain sensitive information.

Mitigation: Store outputs only in approved locations and clean up local artifacts when the parsed content is sensitive.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/soul-code/skills/pdf-online)
- [DingTalk common foundation contract](platforms/dingtalk/references/common-contract.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown instructions, command invocations, JSON lifecycle events, and generated Markdown or JSON artifacts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or modify Feishu, DingTalk, or Notion resources through authenticated platform tools; local manifests and reports support auditability.]

## Skill Version(s):

1.0.1 (source: server release metadata and artifact/_meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
