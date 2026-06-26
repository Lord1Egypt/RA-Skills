## Description: <br>
Use this skill whenever the user wants to do anything with PDF files, including reading or extracting text and tables, merging, splitting, rotating, watermarking, creating PDFs, filling forms, encrypting or decrypting PDFs, extracting images, and OCR on scanned PDFs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yang1002378395-cmyk](https://clawhub.ai/user/yang1002378395-cmyk) <br>

### License/Terms of Use: <br>
Proprietary <br>


## Use Case: <br>
Developers and external users use this skill to inspect, transform, generate, and fill PDF documents with Python libraries and command-line tools. It supports both fillable PDF forms and non-fillable forms that require coordinate-based annotations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads local PDF documents and can create derived files that may contain sensitive document content. <br>
Mitigation: Use copies for important documents and avoid processing sensitive PDFs unless the local environment and output location are appropriate. <br>
Risk: The skill includes guidance for decrypting or removing protection from PDFs. <br>
Mitigation: Only decrypt or remove protection from PDFs that the user is authorized to access. <br>
Risk: Coordinate-based filling of non-fillable forms can place annotations incorrectly if bounding boxes are inaccurate. <br>
Mitigation: Validate bounding boxes and review generated validation images before relying on filled forms. <br>


## Reference(s): <br>
- [PDF form handling guide](forms.md) <br>
- [PDF processing advanced reference](reference.md) <br>
- [ClawHub release page](https://clawhub.ai/yang1002378395-cmyk/pdf-processor-cn) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Shell commands, Configuration, Files] <br>
**Output Format:** [Markdown guidance with inline Python and shell examples, plus generated PDF, PNG, JSON, and text files when scripts are run] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Local file operations may read source PDFs and create derived PDF, image, JSON, text, or spreadsheet outputs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
