## Description: <br>
Transfers the visual style of a reference image to a target photo using Pixify image-to-image processing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangyang-youloft](https://clawhub.ai/user/wangyang-youloft) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and creative teams use this skill to transform a target photo so it matches the lighting, mood, color grading, and composition of a reference image. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Reference and target image URLs are sent to the third-party Pixify/ngmob service. <br>
Mitigation: Use a dedicated API key, keep it out of logs and shared prompts, and avoid submitting sensitive or private photos unless the provider's handling and retention policies are acceptable. <br>
Risk: The order of the two image inputs changes the generated result. <br>
Mitigation: Provide the reference style image as the first input and the target photo as the second input before running the workflow. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/wangyang-youloft/masterpiece-clone) <br>
- [Pixify product console](https://ai.ngmob.com) <br>
- [Pixify API base URL](https://api.ngmob.com) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with JSON and bash examples; API output is a generated image URL.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Pixify/ngmob API key, two publicly accessible image URLs, and asynchronous polling for task completion.] <br>

## Skill Version(s): <br>
1.0.2 (source: release evidence and artifact manifest) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
