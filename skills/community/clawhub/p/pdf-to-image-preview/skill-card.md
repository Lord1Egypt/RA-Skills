## Description: <br>
Converts each page of a PDF into PNG or JPG image files with configurable DPI and optional ZIP packaging. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wuchubuzai2018](https://clawhub.ai/user/wuchubuzai2018) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and document-processing users use this skill to convert PDFs into per-page images for previews, extraction, and image-based archiving. It is suited for local PDF conversion workflows where output format, DPI, and optional ZIP packaging need to be controlled. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The conversion script writes image files and can overwrite an existing ZIP file at the selected destination. <br>
Mitigation: Review the output directory and ZIP output path before running the command, and use a dedicated empty output folder for each conversion. <br>
Risk: PDF conversion depends on the local PyMuPDF installation and large or complex PDFs may take longer to process. <br>
Mitigation: Install PyMuPDF from a trusted environment, test conversion settings on a small sample first, and split PDFs that exceed the 100-page limit. <br>


## Reference(s): <br>
- [PDF To Image Preview Usage Guide](references/usage-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown guidance with bash commands; generated PNG or JPG image files and optional ZIP archive] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports png or jpg output, configurable DPI, and PDFs up to 100 pages.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
