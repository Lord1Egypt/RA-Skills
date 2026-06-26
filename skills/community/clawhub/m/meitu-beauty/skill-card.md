## Description: <br>
Meitu Beauty enhances single-person portrait photos with AI beautification such as skin smoothing, whitening, and facial refinement. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[meitu](https://clawhub.ai/user/meitu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent operators use this skill to validate a single-person portrait, choose a natural or enhanced beautification strength, run the Meitu CLI, and deliver one processed image. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses Meitu API credentials and sends portrait photos through Meitu tooling for processing. <br>
Mitigation: Use only when external processing by Meitu and account usage are acceptable; avoid sensitive facial images unless that processing is approved. <br>
Risk: The skill is limited to single-person portrait photos and may fail or produce poor results for images without a clear single face. <br>
Mitigation: Perform the documented preflight checks for no face, multiple people, small faces, or blurry faces before execution, and stop or ask for a better image when checks fail. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/meitu/meitu-beauty) <br>
- [Publisher profile](https://clawhub.ai/user/meitu) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown guidance with CLI commands and generated image file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces one beautified single-person portrait image, usually preserving the source image format.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact frontmatter says 1.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
