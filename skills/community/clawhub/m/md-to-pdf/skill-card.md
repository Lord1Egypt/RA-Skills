## Description:

MD to PDF converts Markdown files into professional PDFs with optional cover pages, tables of contents, Chinese text, tables, emoji, code highlighting, and Mermaid diagram rendering.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shanghaiyangming](https://clawhub.ai/user/shanghaiyangming)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content authors use this skill to convert Markdown documents into polished PDF deliverables with cover pages, tables of contents, normalized Markdown structure, and custom CSS styling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Browser-based rendering of Markdown can expose untrusted document content, raw HTML, or diagram code to local browser execution and possible network access.

Mitigation: Use the skill only with trusted Markdown, sanitize or disable raw HTML for sensitive documents, and disable Mermaid rendering when external script loading is not acceptable.

Risk: The skill includes a QQ Bot sharing path that can send generated PDFs outside the local workflow.

Mitigation: Treat QQ Bot sending as a separate user-confirmed action and review the destination before sharing generated PDFs.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/shanghaiyangming/skills/md-to-pdf)
- [Publisher Profile](https://clawhub.ai/user/shanghaiyangming)

## Skill Output:

**Output Type(s):** [files, shell commands, configuration, guidance]

**Output Format:** [PDF files generated from Markdown, plus concise command guidance when invoked by an agent]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Pandoc, Chrome with remote debugging on 127.0.0.1:9222, Playwright, and PyPDF2; Mermaid rendering can load a CDN script unless disabled.]

## Skill Version(s):

4.0.0 (source: server release metadata and skill version history)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
