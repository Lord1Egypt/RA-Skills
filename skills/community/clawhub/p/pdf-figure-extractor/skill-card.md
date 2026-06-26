## Description: <br>
Extracts clean figures from academic PDF papers by analyzing document structure, locating captions, cropping figure regions, and validating output image quality. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[438061781](https://clawhub.ai/user/438061781) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and academic writers use this skill to guide agents through extracting clean figure images from local academic PDFs for manuscripts, Word documents, and academic communications. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Cropped figure images may accidentally include captions, surrounding body text, or sensitive PDF content. <br>
Mitigation: Use the skill only on PDFs intended for analysis, choose a safe output location, and review generated images before reuse. <br>
Risk: Incorrect crop boundaries can omit subfigures, axes, labels, or other parts of the intended figure. <br>
Mitigation: Analyze PDF text blocks and caption coordinates before cropping, then verify that each extracted image is complete. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [guidance, code, files] <br>
**Output Format:** [Markdown guidance with Python code snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May result in PNG figure files saved to a user-specified local output path.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
