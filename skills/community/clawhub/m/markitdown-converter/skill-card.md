## Description: <br>
Converts document formats such as PDF, Word, PowerPoint, Excel, HTML, text, and images to Markdown using Microsoft's markitdown library, with scripts for single-file conversion, batch conversion, and image extraction. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wang-junjian](https://clawhub.ai/user/wang-junjian) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and document-processing users use this skill to convert individual files or folders of common office, web, PDF, text, and OCR-supported image documents into Markdown, and to extract images from source documents when supported. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Batch conversion can create or overwrite local Markdown and extracted-image output files. <br>
Mitigation: Use narrow input folders and choose a new or empty output directory before running conversion or extraction scripts. <br>
Risk: The markitdown dependency and optional format-specific tools may affect the local Python environment. <br>
Mitigation: Install dependencies in a virtual environment and add optional system packages only for the document formats being processed. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/wang-junjian/markitdown-converter) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Files, Shell commands, Guidance] <br>
**Output Format:** [Markdown files, extracted image files, and command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes local output files and may create output directories; batch mode recursively processes supported files unless disabled.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
