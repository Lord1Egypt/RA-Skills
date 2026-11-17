## Description:

Use this skill whenever the user wants a scanned PDF, a photographed page or an image of text (PNG, JPG, WEBP, TIFF) translated. PageTranslate reads the scan with OCR, translates it and puts the translation back on the page, so the result is still a PDF or image, not loose text.

This skill is ready for commercial/non-commercial use.

## Publisher:

[catorch](https://clawhub.ai/user/catorch)

### License/Terms of Use:

MIT-0

## Use Case:

People who need scanned PDFs or images of text translated use the skill to OCR and translate the document while preserving it as a PDF or image.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan was partial, so its clean verdict does not cover all referenced content.

Mitigation: Review the skill before installing and inspect any unresolved local-path reference.

Risk: Translating a document sends it to PageTranslate and requires a PageTranslate API key.

Mitigation: Upload only the document the user requested, confirm it may be processed by PageTranslate, and keep the API key private.

## Reference(s):

- [PageTranslate scanned PDF guide](https://pagetranslate.ai/faq/how-to-translate-scanned-pdf)
- [PageTranslate PDF translator](https://pagetranslate.ai/pdf-translator)
- [ClawHub release page](https://clawhub.ai/catorch/skills/pagetranslate-scanned-pdf-translator)
- [PageTranslate API key setup](https://pagetranslate.ai/dashboard/api-keys)

## Skill Output:

**Output Type(s):** [Files, API Calls, Shell commands, Guidance]

**Output Format:** [A translated PDF or image, with concise Markdown status and pricing updates.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The output retains the submitted document format; the target language is selected for each translation.]

## Skill Version(s):

0.1.3 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
