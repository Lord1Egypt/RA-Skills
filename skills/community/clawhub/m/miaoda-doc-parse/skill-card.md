## Description:

Use when user needs to parse, extract, or read content from documents (PDF, Word, Excel, PPT, etc.) and convert them to Markdown via IDP (Intelligent Document Parsing).

This skill is ready for commercial/non-commercial use.

## Publisher:

[johnnycdb](https://clawhub.ai/user/johnnycdb)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to extract content from local or remote documents, including PDF, Word, Excel, PowerPoint, CSV, text, Markdown, and HTML files, and receive Markdown text or JSON output for downstream analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Document parsing can expose confidential local files or sensitive remote URLs to the configured parsing service.

Mitigation: Use the skill only with documents and URLs appropriate for that service, and avoid confidential content unless the processing location and trust boundary are acceptable.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with command-line examples; the invoked parser can return plain text or JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Parses a required file path or URL and supports an optional text/json output selector.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
