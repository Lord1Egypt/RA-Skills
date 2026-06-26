## Description: <br>
Nanobanana helps agents generate images, edit local images, and run multimodal chat through the Nano Banana 2 Pro API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[moxunjinmu](https://clawhub.ai/user/moxunjinmu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to call a Nano Banana 2 Pro-compatible image service for text-to-image generation, image editing from a local input image, and text chat. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and input images are sent to the configured third-party API endpoint. <br>
Mitigation: Use the skill only when the endpoint is trusted, and avoid private images or sensitive prompts unless sharing them with that service is acceptable. <br>
Risk: A real API key placed in shared source files or published bundles could be exposed. <br>
Mitigation: Keep credentials out of the skill bundle and use local environment or secret-management configuration for any real key. <br>
Risk: Generated image files are saved locally and may contain sensitive or copyrighted content from the prompt or source image. <br>
Mitigation: Review saved outputs before sharing or redistribution, and remove files that should not be retained. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/moxunjinmu/nanobanana) <br>
- [Configured Nano Banana API base URL](https://claw.cjcook.site/v1) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, files] <br>
**Output Format:** [Command-line output plus locally saved JPEG image files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated images are written to the skill script output directory; text responses may be printed when returned by the API.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
