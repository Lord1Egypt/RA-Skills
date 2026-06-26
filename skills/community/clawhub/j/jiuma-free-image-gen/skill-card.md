## Description: <br>
Generates images from text prompts through the Jiuma AI API, with configurable image dimensions up to 832 by 832 pixels. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dddcn1](https://clawhub.ai/user/dddcn1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and developers use this skill to submit text-to-image generation jobs to Jiuma, check job status, and retrieve generated image URLs. It is suited for workflows that need quick image generation from user-provided prompts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Image prompts and task metadata are sent to Jiuma's remote service. <br>
Mitigation: Avoid submitting confidential, personal, or sensitive prompt content unless the user accepts the remote-service data handling risk. <br>
Risk: The login flow can save a Jiuma API key locally in plaintext. <br>
Mitigation: Use private local workspaces, avoid synced or shared directories for the saved key, and delete or rotate the key if exposure is suspected. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dddcn1/jiuma-free-image-gen) <br>
- [Jiuma text-to-image submission API](https://api.jiuma.com/api/textImage/add) <br>
- [Jiuma text-to-image status API](https://api.jiuma.com/api/textImage/status) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, JSON, Shell commands, Guidance] <br>
**Output Format:** [JSON responses and command-line guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns task identifiers, generation status, and image URLs when generation succeeds.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
