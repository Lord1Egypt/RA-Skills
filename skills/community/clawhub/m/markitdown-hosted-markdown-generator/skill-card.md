## Description:

MarkItDown Hosted Markdown Generator converts files and URLs to Markdown through AgentPMT-hosted remote tool calls, supporting PDF, Word, Excel, PowerPoint, HTML, CSV, JSON, XML, images, audio, EPub, ZIP archives, and plain text.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agentpmt](https://clawhub.ai/user/agentpmt)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to convert documents, web pages, spreadsheets, presentations, images, audio, and archives into Markdown for analysis, indexing, summarization, or downstream workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Hosted conversion may expose submitted files, audio, images, archives, or URLs to AgentPMT processing.

Mitigation: Submit only content that is approved for hosted processing; avoid secrets, regulated data, internal-only links, and signed URLs unless explicitly approved.

Risk: Floating install commands for related setup skills can introduce supply-chain uncertainty in production workflows.

Mitigation: Use vetted or pinned installs for related setup skills in production.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/agentpmt/skills/markitdown-hosted-markdown-generator)
- [AgentPMT MarkItDown marketplace page](https://www.agentpmt.com/marketplace/markitdown)
- [Action schema](./schema.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, configuration]

**Output Format:** [Markdown text returned in JSON tool responses, plus Markdown guidance for invoking the hosted converter.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The convert action accepts exactly one of url, file_id, or file_base64; files are limited to 50 MB.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
