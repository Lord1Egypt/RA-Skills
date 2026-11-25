## Description:

Translates PDFs into layout-preserving English–Chinese bilingual or Chinese-only PDF documents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yjkj999999](https://clawhub.ai/user/yjkj999999)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and document-processing teams use the skill to translate PDFs into English–Chinese bilingual or Chinese-only documents while retaining the source layout. The workflow extracts text with BabelDOC, translates segments with an LLM, and renders the result.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence reports persistent changes to BabelDOC that bypass font and CMap hash checks.

Mitigation: Review the patch and its effect before applying it; use an isolated Python environment and keep a restorable copy of the installed dependency.

Risk: The security evidence reports broad process cleanup; the workflow terminates processes using its configured proxy port.

Mitigation: Check which process is listening on the selected port and use a dedicated port before running the workflow.

Risk: The security evidence reports potentially destructive workspace cleanup, and the scripts remove cache, working-directory, and translation files.

Mitigation: Set dedicated work and cache paths, inspect the paths before each run, and back up translations or other files that must be retained.

## Reference(s):

- [IBCAT release on ClawHub](https://clawhub.ai/yjkj999999/skills/ibcat)
- [BabelDOC PDF engine](https://github.com/funstory-ai/BabelDOC)
- [pdfplumber PDF verification library](https://github.com/jsvine/pdfplumber)
- [Noto CJK fonts](https://github.com/notofonts/noto-cjk)

## Skill Output:

**Output Type(s):** [PDF files, JSON, Shell commands, Guidance]

**Output Format:** [Bilingual or Chinese-only PDF files, JSON translation segment files, and Markdown instructions with shell commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Bilingual PDFs place source and translated text side by side; CJK fonts are required, and scanned PDFs need OCR preprocessing. Translation quality depends on the selected LLM.]

## Skill Version(s):

1.0.2 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
