## Description:

Translates PDFs into layout-preserving bilingual side-by-side and monolingual Chinese PDFs using BabelDOC and an LLM bridge.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yjkj999999](https://clawhub.ai/user/yjkj999999)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to translate source PDFs, especially English-to-Chinese documents, into bilingual side-by-side PDFs while preserving layout. It also guides batching extracted text for LLM translation and rendering and verifying the final PDF outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup workflow patches BabelDOC inside the active Python environment and disables BabelDOC font and CMap hash checks.

Mitigation: Run the skill only in an isolated virtual environment or container, avoid shared Python installations, and rebuild the environment after use.

Risk: The workflow can install packages with --break-system-packages and uses unpinned dependencies or system packages.

Mitigation: Pin and review dependency versions in a disposable environment before processing important documents.

Risk: The scripts clear BabelDOC caches and terminate processes bound to the configured local proxy port.

Mitigation: Use a dedicated work directory and port, review running processes first, and avoid running as root.

Risk: Input PDF text segments and translations are written to local JSON files and may be exposed to LLM or sub-agent workflows.

Mitigation: Do not process confidential PDFs unless that exposure is acceptable, and remove work files after the translation is complete.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yjkj999999/skills/ibcat)
- [BabelDOC](https://github.com/funstory-ai/BabelDOC)
- [pdfplumber](https://github.com/jsvine/pdfplumber)
- [Noto CJK Fonts](https://github.com/notofonts/noto-cjk)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance, Files]

**Output Format:** [Markdown guidance with shell commands and generated PDF and JSON file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [When the workflow is run, it can produce bilingual .dual.pdf files, monolingual .mono.pdf files, segments.json, translations.json, and PDF verification output.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact documentation)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
