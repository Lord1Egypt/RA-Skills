## Description:

Convert pasted articles, local Markdown/TXT files, or PDF documents into 5-8 concise knowledge cards with a title, core knowledge summary, brief explanation, and example or self-test question.

This skill is ready for commercial/non-commercial use.

## Publisher:

[slyum123](https://clawhub.ai/user/slyum123)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to turn pasted articles or local Markdown, TXT, and text-based PDF documents into concise Markdown study cards for review and self-testing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: PDF support depends on pypdf, creating a minor dependency-hardening concern when processing untrusted or unusually large PDFs.

Mitigation: Install dependencies in a virtual environment, keep pypdf reviewed and updated, and avoid untrusted or unusually large PDFs without resource limits.

Risk: Encrypted, scanned, or unsupported document formats can fail extraction or require manual preparation before card generation.

Mitigation: Use pasted text, Markdown, TXT, or text-based PDFs; decrypt protected PDFs and run OCR on scanned PDFs before use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/slyum123/skills/make-knowledge-cards)

## Skill Output:

**Output Type(s):** [Markdown, Text, Shell commands, Guidance]

**Output Format:** [Markdown knowledge cards with optional inline shell commands for PDF extraction setup]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces 5-8 cards by default, or fewer when the source lacks enough distinct knowledge points.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
