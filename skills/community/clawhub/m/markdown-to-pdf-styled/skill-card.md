## Description: <br>
Convert Markdown files to styled PDF documents using pandoc and wkhtmltopdf with built-in or custom CSS styles. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mengwuzhi](https://clawhub.ai/user/mengwuzhi) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and writers use this skill to convert Markdown documents into consistently styled PDFs with selectable built-in CSS themes or a custom CSS file. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Rendering enables local file access, so untrusted Markdown or CSS may cause local or remote resources to be included in the PDF. <br>
Mitigation: Use trusted Markdown and CSS inputs, inspect resource references before conversion, and avoid rendering documents from unknown sources. <br>
Risk: Supplying an existing output path can overwrite a PDF file. <br>
Mitigation: Choose an explicit output path in a safe working directory and check whether the target file already exists before running the conversion. <br>


## Reference(s): <br>
- [Usage Guide](references/usage.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/mengwuzhi/markdown-to-pdf-styled) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash commands and generated PDF file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces a local PDF file from a Markdown input and selected CSS style.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
