## Description:

Use this skill whenever the user wants a PDF translated into another language and returned as a PDF with its pages, tables, fonts and images in place: manuals, contracts, reports, papers, brochures, large PDFs. Uploads the file to PageTranslate, shows the exact price first, and downloads the translated PDF.

This skill is ready for commercial/non-commercial use.

## Publisher:

[catorch](https://clawhub.ai/user/catorch)

### License/Terms of Use:

MIT-0

## Use Case:

External users can translate PDFs, especially long or layout-sensitive documents, into another language and receive a translated PDF while reviewing the quote before paying.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The source document is uploaded to PageTranslate for translation.

Mitigation: Disclose the external upload and upload only the file the user asked to translate.

Risk: The workflow requires a PageTranslate API key and may incur a translation charge.

Mitigation: Keep the key in the required environment variable without printing or saving it, show the exact quote first, and wait for the user to approve payment.

## Reference(s):

- [PageTranslate PDF translator](https://pagetranslate.ai/pdf-translator)
- [Translate a large PDF](https://pagetranslate.ai/pdf-translator/translate-large-pdf)
- [Translate a scanned PDF](https://pagetranslate.ai/faq/how-to-translate-scanned-pdf)

## Skill Output:

**Output Type(s):** [Files, Text]

**Output Format:** [Translated PDF and concise user-facing price or status details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns the service-generated PDF; layout retention depends on source quality and service processing.]

## Skill Version(s):

0.1.3 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
