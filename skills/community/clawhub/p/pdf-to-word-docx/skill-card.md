## Description: <br>
PDF to Word Converter helps agents convert PDF and supported image files into editable DOCX and other document formats using the ComPDFKit Conversion SDK with layout analysis, table recognition, OCR, and image-retention options. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[compdf-youna](https://clawhub.ai/user/compdf-youna) <br>

### License/Terms of Use: <br>
Commercial / Proprietary <br>


## Use Case: <br>
External users and developers use this skill to convert PDFs or supported image files into editable Word, Excel, PowerPoint, HTML, RTF, text, JSON, Markdown, CSV, or image outputs while preserving layout where possible. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may download a vendor license file and a roughly 525 MB Document AI model on first use. <br>
Mitigation: Pre-provision the license and model files in sensitive or offline environments, and allow downloads only from trusted ComPDF endpoints when network access is acceptable. <br>
Risk: The included trial license is limited to 200 conversions and is not suitable for production use under the vendor terms. <br>
Mitigation: Review the ComPDFKit license terms before deployment and provide a valid production license for commercial workflows. <br>
Risk: Conversions depend on the proprietary ComPDFKitConversion package and platform support for Windows or macOS. <br>
Mitigation: Verify package installation, platform compatibility, and expected conversion quality in the target runtime before relying on the skill. <br>


## Reference(s): <br>
- [ComPDF Conversion SDK Python Overview](https://www.compdf.com/guides/conversion-sdk/python/overview) <br>
- [ComPDF Python PDF to Word Guide](https://www.compdf.com/guides/conversion-sdk/python/pdf-to-word) <br>
- [ComPDF Python PDF to Excel Guide](https://www.compdf.com/guides/conversion-sdk/python/pdf-to-excel) <br>
- [ComPDF Python PDF to PPT Guide](https://www.compdf.com/guides/conversion-sdk/python/pdf-to-ppt) <br>
- [ComPDF Python Apply License Guide](https://www.compdf.com/guides/conversion-sdk/python/apply-license) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Text, Markdown, Shell commands, Configuration instructions] <br>
**Output Format:** [Converted document files such as DOCX, PPTX, XLSX, HTML, RTF, images, TXT, JSON, Markdown, or CSV, plus status and error text.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires ComPDFKitConversion and may download a trial license file and an approximately 525 MB Document AI model on first use.] <br>

## Skill Version(s): <br>
1.2.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
