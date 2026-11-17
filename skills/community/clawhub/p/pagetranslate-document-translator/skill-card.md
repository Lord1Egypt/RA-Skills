## Description:

Use this skill whenever the user wants a Word document or business file translated and returned as the same kind of file: DOCX contracts, manuals, HR policies, marketing material, financial reports, CVs. Keeps headings, tables, lists and images. Shows the exact price first.

This skill is ready for commercial/non-commercial use.

## Publisher:

[catorch](https://clawhub.ai/user/catorch)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to translate business documents into a requested language while retaining an editable file and its layout. It obtains a quote before any paid translation begins.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Documents submitted for translation are sent to PageTranslate, which processes their contents.

Mitigation: Upload only documents the user explicitly selected and is comfortable sharing with PageTranslate.

Risk: The security scan was partial because one referenced local path could not be resolved, so the scan evidence is incomplete.

Mitigation: Review the unresolved reference and the complete release contents before deployment.

## Reference(s):

- [PageTranslate document translation software](https://pagetranslate.ai/document-translation-software)
- [PageTranslate DOCX translator](https://pagetranslate.ai/docx-translator)
- [How to translate a Word document](https://pagetranslate.ai/faq/how-to-translate-word-document)

## Skill Output:

**Output Type(s):** [Files, Guidance]

**Output Format:** [Translated document file in the corresponding supported format, with status and pricing guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Preserves document structure and formatting where supported; saves the translated file in the source folder without overwriting an existing file.]

## Skill Version(s):

0.1.3 (source: release metadata, frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
