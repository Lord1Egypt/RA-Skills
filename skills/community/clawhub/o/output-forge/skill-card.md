## Description:

Transform raw AI output into platform-ready content with formatting, metadata, and cleanup for Markdown, HTML, plain text, and structured outputs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[theshadowrose](https://clawhub.ai/user/theshadowrose)

### License/Terms of Use:

MIT

## Use Case:

Content creators, writers, marketers, developers, and teams use this skill to convert existing AI-generated text into platform-ready posts, newsletters, documents, and social threads. It helps standardize formatting, add metadata, batch-process plain-text files, and optionally remove common AI-disclosure or hedging patterns before publication.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Default cleanup can remove AI provenance, capability limits, or uncertainty statements from text.

Mitigation: Review output before publishing and use --no-clean when those statements must remain.

Risk: HTML-oriented outputs are not sanitized and may carry unsafe content when the input is untrusted.

Mitigation: Use the skill only on text you control or sanitize HTML output separately before publishing or pasting into admin surfaces.

Risk: Formatting does not verify facts, grammar, plagiarism, or platform-specific publishing requirements.

Mitigation: Treat the generated files as drafts and perform human review before external publication.

## Reference(s):

- [Output Forge on ClawHub](https://clawhub.ai/theshadowrose/skills/output-forge)
- [Publisher profile](https://clawhub.ai/user/theshadowrose)
- [README](artifact/README.md)
- [Limitations](artifact/LIMITATIONS.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown and plain text guidance with examples of generated HTML, Markdown, LaTeX, social-thread text, configuration JSON, and shell commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are local files or stdout; supported formats include WordPress HTML, Medium Markdown, email HTML, Twitter/X threads, LinkedIn posts, Markdown, LaTeX, and plain text.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
