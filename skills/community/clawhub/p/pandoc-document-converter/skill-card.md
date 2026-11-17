## Description:

Pandoc文档转换 helps agents guide Pandoc-based document conversion workflows across formats such as Markdown, HTML, PDF, and Word-style documents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, automation teams, and document-processing users can use this skill to plan or run local Pandoc conversion tasks and troubleshoot common conversion failures. It is suited to format conversion, batch document handling, and extraction-oriented workflows, not encrypted-file bypass or credential-heavy service deployment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documentation describes API credentials and REST service setup that the security evidence says are unsupported, which could lead users or agents to overgrant secrets or permissions.

Mitigation: Use the skill only as a local Pandoc conversion aid; do not provide API keys, tokens, or service credentials based on this artifact alone.

Risk: The skill may propose shell commands or file writes for document conversion, including on private documents.

Mitigation: Review every command, source path, and output path before execution, and avoid running conversions on untrusted or sensitive documents without local policy approval.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/pandoc-document-converter)
- [Pandoc installation documentation](https://pandoc.org/installing.html)
- [Python downloads](https://www.python.org/downloads/)
- [Flask documentation](https://flask.palletsprojects.com/)
- [Requests documentation](https://requests.readthedocs.io/en/master/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with optional JSON examples and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference source and target file paths, desired output formats, local Pandoc options, and troubleshooting steps.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
