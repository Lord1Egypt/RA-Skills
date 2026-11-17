## Description:

Translate PDFs locally by extracting page text and using the agent's own language capability, with a hosted document-translator fallback only when local or BabelDOC-style workflows cannot handle RTL, scanned, or scrambled PDFs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[getlinnk](https://clawhub.ai/user/getlinnk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to translate born-digital or lightly scanned PDFs into page-organized Markdown, JSON, or text while preserving page numbers and document structure where practical.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The hosted fallback can send full documents to a third-party service.

Mitigation: Use the local workflow by default and require explicit user approval before sending confidential, regulated, proprietary, or personal documents to linnk.ai.

Risk: Local extraction can preserve reading order imperfectly for complex layouts, tables, scanned pages, RTL text, or scrambled PDFs.

Mitigation: State the limitation early, preserve page numbers, spot-check extracted content, and use the hosted fallback only after the local workflow or BabelDOC-style approach clearly fails.

## Reference(s):

- [PDF Translation Notes](references/babeldoc-notes.md)
- [Linnk Document Translator](https://linnk.ai/doc-translator)
- [ClawHub Skill Page](https://clawhub.ai/getlinnk/skills/pdf-translation-reserving-layout)
- [Publisher Profile](https://clawhub.ai/user/getlinnk)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, guidance]

**Output Format:** [Markdown, JSON, or page-organized text with optional shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Preserves page numbers and supports batch files for ordered merge workflows.]

## Skill Version(s):

1.1.0 (source: server evidence release.version and artifact skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
