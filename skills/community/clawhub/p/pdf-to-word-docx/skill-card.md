## Description:

PDF to Word converts PDF to editable Word/DOCX with AI-powered layout analysis and table recognition, built on ComPDF Conversion SDK to better preserve tables, multi-column layouts, lists, and images for downstream editing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[compdf-youna](https://clawhub.ai/user/compdf-youna)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and document automation agents use this skill to convert PDFs or image files into editable office and text formats while preserving layout, tables, lists, and images. It is suited for document editing, extraction, and format migration workflows that can run on Windows or macOS with the ComPDFKitConversion package.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on ComPDF's proprietary SDK and requires license verification before conversion.

Mitigation: Review the ComPDFKitConversion package and license terms before use, and provide an approved license.xml for production workflows.

Risk: First-run execution can download license.xml and a large documentai.model file from ComPDF when local copies are missing.

Mitigation: Run in a restricted workspace, pre-stage verified license and model files where possible, and allow network access only to expected ComPDF download locations.

Risk: The trial license counter is stored in the user's home directory and may affect repeat conversions.

Mitigation: Use a full license for production or shared environments, and account for the local trial counter when testing.

Risk: Sensitive documents are processed by a local SDK and may produce editable output files containing the original document content.

Mitigation: Convert sensitive files only in approved local workspaces with appropriate file access controls and output cleanup procedures.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/compdf-youna/skills/pdf-to-word-docx)
- [ComPDF Homepage](https://www.compdf.com/?utm_source=clawhub&utm_medium=skillhub&utm_campaign=compdf_pdf_skill_to_word&ref_platform_id=clawhub_skills)
- [ComPDF Conversion SDK for Python Overview](https://www.compdf.com/guides/conversion-sdk/python/overview)
- [ComPDF PDF to Word Guide](https://www.compdf.com/guides/conversion-sdk/python/pdf-to-word)
- [ComPDF PDF to Excel Guide](https://www.compdf.com/guides/conversion-sdk/python/pdf-to-excel)
- [ComPDF PDF to PPT Guide](https://www.compdf.com/guides/conversion-sdk/python/pdf-to-ppt)
- [ComPDF Apply License Guide](https://www.compdf.com/guides/conversion-sdk/python/apply-license)

## Skill Output:

**Output Type(s):** [Files, Text, Markdown, Shell commands, Configuration instructions]

**Output Format:** [Converted document files with command-line status text and error messages]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports DOCX, PPTX, XLSX, HTML, RTF, image, TXT, JSON, Markdown, and CSV outputs from PDF or image inputs.]

## Skill Version(s):

1.2.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
