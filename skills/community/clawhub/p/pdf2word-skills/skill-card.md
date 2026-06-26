## Description: <br>
Convert scanned PDF documents into Word text documents using a free, local OCR engine or remote API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[scottkiss](https://clawhub.ai/user/scottkiss) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and document-processing teams use this skill to convert scanned PDF files into editable Word documents. It supports local OCR by default and can pass optional arguments to the underlying OCR tool for alternate engines and table handling. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The installer downloads an executable OCR binary without checksum or signature verification. <br>
Mitigation: Review the installer before use and install only after the binary source is pinned or verified by checksum or signature. <br>
Risk: Remote OCR engines such as Gemini may send document contents to an external provider. <br>
Mitigation: Use the local RapidOCR path for confidential documents unless external processing has been approved. <br>
Risk: Gemini API credentials may be stored in a plaintext configuration file. <br>
Mitigation: Restrict permissions on any API-key configuration file and rotate credentials if they are exposed. <br>
Risk: The conversion flow writes extracted document text to a temporary plaintext file during processing. <br>
Mitigation: Run the skill in a trusted workspace and confirm temporary output is removed after conversion, especially for sensitive PDFs. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/scottkiss/pdf2word-skills) <br>
- [Publisher profile](https://clawhub.ai/user/scottkiss) <br>
- [docr binary release download pattern](https://github.com/scottkiss/doc-ocr/releases/download/$VERSION/$FILENAME) <br>
- [Skill README](artifact/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown instructions with shell commands and generated .docx files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates a temporary text file next to the requested output document and removes it after conversion.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
