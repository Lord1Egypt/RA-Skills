## Description:

Document Pro helps an agent read, extract, convert, and summarize PDF, Word, PowerPoint, Excel, text, and Markdown documents, including optional AI analysis through SkillBoss API Hub.

This skill is ready for commercial/non-commercial use.

## Publisher:

[marjoriebroad](https://clawhub.ai/user/marjoriebroad)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can use this skill to process uploaded documents, extract text and tables, generate summaries and key points, and convert supported document formats.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Full document text may be sent to SkillBoss API Hub without a clear consent, minimization, or redaction step.

Mitigation: Use only with documents users are permitted to share, ask before remote analysis, and redact confidential, personal, legal, financial, medical, or proprietary content before sending it to the API.

Risk: Scanned PDFs, complex layouts, images, and charts may produce incomplete or inaccurate extraction results.

Mitigation: Use OCR for scanned PDFs, tell users when extraction is limited, and verify summaries against the original document before relying on them.

Risk: Remote AI analysis requires a SkillBoss API key.

Mitigation: Store SKILLBOSS_API_KEY in environment or secret management and avoid exposing it in prompts, logs, or generated files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/marjoriebroad/skills/mar-document-pro)
- [Publisher profile](https://clawhub.ai/user/marjoriebroad)
- [SkillBoss API Hub endpoint](https://api.heybossai.com/v1)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown and text with optional Python code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include document type and page count, summaries, three to five key points, and suggested next actions.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
