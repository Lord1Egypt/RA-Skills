## Description: <br>
Remove image-based watermarks from PDF files by deleting matching drawing instructions from content streams and removing related XObject references. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ucrossmym1nd](https://clawhub.ai/user/ucrossmym1nd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and document-processing agents use this skill to remove image-based PDF watermarks from local files when they have permission to modify the document. It is intended for position- and size-based watermark cleanup, with optional removal of matching link annotations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Watermark removal can modify documents in ways the user is not authorized to make. <br>
Mitigation: Use the skill only when the user has permission to modify the PDF and keep an unchanged copy of the original file. <br>
Risk: Broad position or size thresholds can remove unrelated images from the PDF. <br>
Mitigation: Keep detection thresholds narrow and verify the output PDF page by page before using or sharing it. <br>
Risk: Removing link annotations without a domain filter can delete links unrelated to the watermark. <br>
Mitigation: Use --remove-links only with a specific --link-domain for the watermark provider. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Code, Files, Guidance] <br>
**Output Format:** [Markdown guidance with bash commands and local PDF output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Python 3.8+ and pymupdf; users should review the generated PDF page by page.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
