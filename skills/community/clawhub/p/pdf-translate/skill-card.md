## Description: <br>
Translates PDF documents to Chinese by extracting text, guiding section-by-section Markdown translation, and generating CJK-capable PDFs with WeasyPrint. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chrislee121](https://clawhub.ai/user/chrislee121) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, researchers, and document authors use this skill to translate English PDFs into editable Chinese Markdown and polished PDF documents while preserving headings, tables, lists, code blocks, and citations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: PDFs may contain sensitive local content and the workflow writes translated Markdown and PDF outputs to local paths. <br>
Mitigation: Confirm the input document and output paths before extraction or conversion, especially for confidential files. <br>
Risk: Legacy scripts may be confusing because the current release recommends the Markdown-to-PDF workflow instead. <br>
Mitigation: Use scripts/md2pdf.py for normal conversion and review or modify scripts/translate_pdf.py and scripts/generate_complete_pdf.py before running them as standalone translators. <br>
Risk: Scanned, encrypted, or unusually encoded PDFs may produce incomplete extracted text. <br>
Mitigation: Preview extracted text before translation and use OCR or decryption steps when the source PDF requires them. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/chrislee121/pdf-translate) <br>
- [Translation Standards](references/translation-standards.md) <br>
- [Font Configuration](references/font-configuration.md) <br>
- [Troubleshooting](references/troubleshooting.md) <br>
- [Complete Workflow Example](references/complete-example.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline Python and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local Markdown and PDF files when the recommended conversion script is run.] <br>

## Skill Version(s): <br>
4.0.0 (source: server release metadata, SKILL.md, CHANGELOG, target metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
