## Description:

Gxpcode Translator supports specialized text and PDF translation with terminology protection, PDF OCR parsing, and bilingual HTML and Markdown export.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gxpcode-hezhong](https://clawhub.ai/user/gxpcode-hezhong)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to translate domain-specific text or PDF documents while preserving glossary terms. For PDF inputs, it can parse pages through OCR, translate page groups, and export bilingual HTML and Markdown files for review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Full source and translated document contents may be retained in plaintext logs.

Mitigation: Use only with non-sensitive documents unless durable plaintext logging is acceptable; review and clear generated logs according to local retention policy.

Risk: PDF workflows may send document content to cloud OCR processing.

Mitigation: Avoid confidential PDFs unless the user is comfortable with cloud OCR processing or has arranged an approved local OCR path.

Risk: Generated HTML can behave as active content if source document markup is embedded.

Mitigation: Treat generated HTML as active content and open it only in trusted environments after reviewing the source document.

Risk: PDF and browser-style workflows have insufficient safeguards for untrusted PDFs or paths.

Mitigation: Avoid PDFs or paths from untrusted sources and review the skill before installing or running it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gxpcode-hezhong/skills/gxpcode-translator)
- [Publisher profile](https://clawhub.ai/user/gxpcode-hezhong)
- [Server-resolved GitHub source](https://github.com/Gxpcode-hezhong/Gxpcode-translator)
- [Gxpcode translation rules](refs/Gxpcode-rules.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Plain translated text for text inputs; bilingual HTML and Markdown files plus logs for PDF workflows.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a CSV terminology dictionary and configurable output directory; PDF workflows may use cloud OCR and write intermediate files.]

## Skill Version(s):

0.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
