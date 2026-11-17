## Description:

Automates page-by-page PDF text extraction, glossary-aware Chinese translation, dynamic terminology updates, and DOCX output for long-form documents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cecil727](https://clawhub.ai/user/cecil727)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, translators, and document-processing agents use this skill to translate long PDFs into Chinese while preserving terminology consistency across pages. It is intended for novels, academic papers, technical white papers, standards, and other terminology-heavy PDF workflows where users provide the source PDF, glossary files, page range, and DOCX output path.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow reads local PDFs and glossary files and writes or appends DOCX and dynamic glossary files.

Mitigation: Use explicit local paths, prefer a new output DOCX path, and review generated glossary terms before reusing them.

Risk: Untrusted PDFs may expose the agent session or local tooling to malformed-document risk.

Mitigation: Avoid processing hostile or unknown PDFs in a tool-rich agent session; process only documents from trusted sources when possible.

Risk: Custom regex highlight rules can cause unexpected matching behavior or processing overhead.

Mitigation: Do not pass untrusted custom regex highlight rules; review patterns before execution.

## Reference(s):

- [Professional PDF Translator on ClawHub](https://clawhub.ai/cecil727/skills/professional-pdf-translator)
- [Publisher profile](https://clawhub.ai/user/cecil727)
- [tiangong-wps-word-automation-cn](https://clawhub.com/skill/tiangong-wps-word-automation-cn)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, files]

**Output Format:** [Markdown instructions with shell commands, JSON extraction results, glossary text, and DOCX file output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python with pymupdf and python-docx; reads local PDFs and glossary files, writes or appends DOCX output, and can maintain a dynamic glossary file.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
