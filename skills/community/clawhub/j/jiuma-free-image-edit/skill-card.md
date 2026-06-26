## Description: <br>
Uses the Jiuma AI API to edit or fuse up to three images from text prompts and return task status plus generated image links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dddcn1](https://clawhub.ai/user/dddcn1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to submit image-editing or multi-image fusion jobs to Jiuma AI, then poll for completion and retrieve hosted output image links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected images, image URLs, and prompts are sent to Jiuma for cloud processing. <br>
Mitigation: Avoid submitting private, regulated, confidential, copyrighted, or sensitive personal images unless the user has reviewed and accepted Jiuma processing. <br>
Risk: The login flow stores the Jiuma API key locally as plaintext under the OpenClaw workspace .jiuma directory. <br>
Mitigation: Protect workspace permissions, avoid shared or synced machines, and remove or rotate the key when it is no longer needed. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/dddcn1/jiuma-free-image-edit) <br>
- [Login and API Key Documentation](LOGIN.md) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Image URLs, Shell commands] <br>
**Output Format:** [JSON command output with task IDs, status values, messages, and generated image or download URLs.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Submits prompt text and up to three images or image URLs to Jiuma; successful tasks return hosted image URLs.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
