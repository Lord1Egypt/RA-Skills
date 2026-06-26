## Description: <br>
Generates images through ThinkZone AI when users request image creation or image-to-image workflows, supporting Gemini, MiniMax, and Seedream models. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[renjicode](https://clawhub.ai/user/renjicode) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to generate images or image variants from prompts and optional reference images through ThinkZone AI models. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Bundled ThinkZone API keys appear in code and documentation. <br>
Mitigation: Do not use bundled keys; the publisher should revoke and remove them, and users should provide their own THINKZONE_API_KEY. <br>
Risk: Prompts and reference images may be sent to a paid external image-generation service. <br>
Mitigation: Use only approved data and account policies; avoid private, regulated, or confidential content unless policy allows it. <br>
Risk: External image generation may incur charges or fail when the ThinkZone account lacks balance. <br>
Mitigation: Confirm account balance and cost expectations before running image generation. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/renjicode/keplerjai-image-gen) <br>
- [ThinkZone AI platform](https://open.thinkzoneai.com) <br>
- [ThinkZone image generation endpoint](https://open.thinkzoneai.com/v3/images/generations) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, files, guidance] <br>
**Output Format:** [Markdown guidance with shell commands; generated images are saved as image files with JSON metadata.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires THINKZONE_API_KEY and sends prompts or reference images to ThinkZone for external image-generation calls.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
