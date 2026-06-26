## Description: <br>
Convert PDF files to PowerPoint presentations via intermediate image rendering. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jvtop](https://clawhub.ai/user/jvtop) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and document teams use this skill to convert visual PDF documents into PowerPoint presentations while preserving page layout as slide images. It is suited for scanned presentations, design drawings, complex-layout PDFs, and batch conversion workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The converter writes a PPTX file and intermediate image files to local paths, which can expose confidential PDF content if directories are chosen carelessly. <br>
Mitigation: Choose output and image directories deliberately, keep sensitive conversions in controlled locations, and delete intermediate images when they are no longer needed. <br>
Risk: Installing dependencies into a shared system Python can affect other local projects. <br>
Mitigation: Install PyMuPDF and python-pptx in a virtual environment where possible. <br>
Risk: Very large PDFs or high zoom settings can consume significant memory and produce large output files. <br>
Mitigation: Process large PDFs in batches, reduce the zoom factor when needed, or use JPG output when smaller files are acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jvtop/pdf-to-ppt) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/jvtop) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Files, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and a Python conversion script that produces PPTX files plus intermediate PNG or JPG images.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Output file paths, image directory, zoom factor, slide dimensions, and image format are configurable.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
