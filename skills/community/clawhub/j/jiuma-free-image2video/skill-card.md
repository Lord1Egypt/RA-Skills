## Description: <br>
Generates videos from first-frame or first-and-last-frame images with prompts using the Jiuma AI API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dddcn1](https://clawhub.ai/user/dddcn1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to submit local or remote images plus prompts to Jiuma AI, poll generation status, and retrieve generated video URLs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Images and prompts selected by the user are sent to Jiuma for processing. <br>
Mitigation: Use only images and prompts that are acceptable to share with Jiuma; avoid personal, confidential, or sensitive content. <br>
Risk: The optional login flow saves a reusable Jiuma API key locally in plaintext under the workspace. <br>
Mitigation: Use the login flow only on trusted machines, restrict workspace access, and delete or rotate the saved key when it is no longer needed. <br>
Risk: Generated video URLs may be temporary and hosted remotely. <br>
Mitigation: Download generated videos promptly when long-term access is needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dddcn1/jiuma-free-image2video) <br>
- [Login and API key workflow](LOGIN.md) <br>
- [jiuma-free-image-gen related skill](https://clawhub.ai/dddcn1/jiuma-free-image-gen) <br>
- [jiuma-free-image-edit related skill](https://clawhub.ai/dddcn1/jiuma-free-image-edit) <br>
- [jiuma-free-meta-human related skill](https://clawhub.ai/dddcn1/jiuma-free-meta-human) <br>
- [jiuma-free-voice-clone related skill](https://clawhub.ai/dddcn1/jiuma-free-voice-clone) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, API Calls, Shell commands, Files] <br>
**Output Format:** [JSON status payloads with task IDs, generated video URLs, and error messages] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May save a reusable Jiuma API key locally in plaintext after the optional login flow.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
