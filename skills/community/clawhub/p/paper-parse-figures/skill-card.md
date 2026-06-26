## Description: <br>
Parse academic PDF papers into markdown with figure extraction. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Chen-Li-17](https://clawhub.ai/user/Chen-Li-17) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and researchers use this skill to convert academic PDFs into markdown, structured JSON metadata, and extracted figure images for downstream reading or analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs a local Python PDF parser through uv-managed dependencies. <br>
Mitigation: Review or pin the PyMuPDF and pymupdf4llm dependencies before use in stricter environments. <br>
Risk: The skill reads user-selected PDFs and writes extracted text, metadata, and images to disk. <br>
Mitigation: Use explicit local PDF and output paths, and review generated files before sharing them outside the intended environment. <br>


## Reference(s): <br>
- [Paper Parse ClawHub release](https://clawhub.ai/Chen-Li-17/paper-parse-figures) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, JSON, Images, Text] <br>
**Output Format:** [Markdown files, JSON metadata, PNG images, and JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates an output directory containing paper content, parsed metadata, figure screenshots, and a cover title/authors snapshot.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
