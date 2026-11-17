## Description:

Convert PDF and image documents to clean Markdown via the PDF2Markdown CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qthans](https://clawhub.ai/user/qthans)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to convert PDFs and common image formats into Markdown or JSON, including larger documents through the CLI's async parsing workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unpinned npm or npx execution could install a package version that has not been reviewed.

Mitigation: Use a pinned, vetted PDF2Markdown CLI version before installing or running the skill.

Risk: Parsed documents may contain private or sensitive content, and server evidence notes that remote processing is not clearly scoped.

Mitigation: Confirm where documents are sent before parsing sensitive files and keep converted output in a gitignored .pdf2markdown/ directory.

Risk: API keys can be exposed if passed inline or logged during setup.

Mitigation: Use safer login or secret-management flows and avoid exposing PDF2MARKDOWN_API_KEY in command history, logs, or committed files.

## Reference(s):

- [PDF2Markdown API Docs](https://pdf2markdown.io/docs)
- [pdf2markdown-cli npm package](https://www.npmjs.com/package/pdf2markdown-cli)
- [ClawHub skill page](https://clawhub.ai/qthans/skills/pdf2markdown)
- [Publisher profile](https://clawhub.ai/user/qthans)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and optional JSON file output from the CLI]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Converted content is typically written to .pdf2markdown/ files; async parsing supports large files up to 100MB.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
