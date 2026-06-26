## Description: <br>
gpt-image-2 generates 1024x1024 PNG images from text prompts after the user provides an access key. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kiribon43567](https://clawhub.ai/user/kiribon43567) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users or agent operators use this skill to generate PNG images from text prompts and check remaining image-generation quota after validating an access key. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and the access key are sent to an undisclosed unencrypted HTTP image service. <br>
Mitigation: Use only limited, revocable image-service keys and non-sensitive prompts, and review the service trust boundary before deployment. <br>
Risk: Generated PNG files may remain in the system temporary directory. <br>
Mitigation: Delete temporary outputs after use or set an explicit output path in a managed location. <br>
Risk: The security verdict is suspicious because the skill under-discloses important network and credential handling behavior. <br>
Mitigation: Review the skill before installing and restrict use to environments where that behavior is acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kiribon43567/gpt-image-2) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, files, guidance] <br>
**Output Format:** [Plain text status messages and PNG image file attachments] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generates fixed 1024x1024 PNG images; each image generation consumes one quota unit.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
