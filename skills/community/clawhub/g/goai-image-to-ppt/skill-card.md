## Description: <br>
Convert images to PowerPoint presentations via GoAI API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[goai](https://clawhub.ai/user/goai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to convert local image files or remote image URLs into PowerPoint presentations through the GoAI service. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uploads selected local images to GoAI for remote processing. <br>
Mitigation: Use it only with images that are acceptable to send to GoAI; avoid confidential screenshots or private documents unless that processing is approved. <br>
Risk: The skill uses GOAI_API_KEY and may consume account credits. <br>
Mitigation: Configure a scoped GoAI key where possible, monitor account usage, and confirm that credit consumption is expected before running large conversions. <br>
Risk: The generated presentation is opened automatically after download, including through a Windows shell path noted in the security guidance. <br>
Mitigation: Review the source and run environment before execution; prefer a version or workflow that asks before opening downloaded presentations on Windows. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/goai/goai-image-to-ppt) <br>
- [GoAI website](https://mustgoai.com) <br>
- [GoAI PPT service](https://ppt.mustgoai.com) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [PowerPoint file with text status lines containing local and remote result URLs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires uv and GOAI_API_KEY; successful runs produce a .pptx file and a public download URL.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
