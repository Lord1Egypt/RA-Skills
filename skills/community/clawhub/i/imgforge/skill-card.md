## Description: <br>
Generate AI images for free using Z-Image-Turbo. Say "generate an image of..." and get stunning results in seconds. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[futurizerush](https://clawhub.ai/user/futurizerush) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to let an AI assistant generate image files from natural-language prompts through ModelScope's Z-Image-Turbo API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and generation parameters are sent to ModelScope/Alibaba services. <br>
Mitigation: Use the skill only with prompts and parameters that are acceptable to share with that external service. <br>
Risk: MODELSCOPE_API_KEY is a credential required for image generation. <br>
Mitigation: Store the token as a secret environment variable and avoid pasting it into chats, logs, or committed files. <br>
Risk: Account setup may require phone verification, a payment method, and referral or invite links. <br>
Mitigation: Review the ModelScope and Alibaba Cloud account requirements before installing or enabling the skill. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/futurizerush/imgforge) <br>
- [Publisher profile](https://clawhub.ai/user/futurizerush) <br>
- [Source homepage](https://github.com/FuturizeRush/zimage-skill) <br>
- [Z-Image project](https://github.com/Tongyi-MAI/Z-Image) <br>
- [Z-Image-Turbo model](https://huggingface.co/Tongyi-MAI/Z-Image-Turbo) <br>
- [ModelScope API inference limits](https://modelscope.ai/docs/model-service/API-Inference/limits) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Text, JSON, Shell commands, Configuration guidance] <br>
**Output Format:** [Image files with status text or optional JSON output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires MODELSCOPE_API_KEY; supports prompt text, output path, width, height, and optional JSON mode.] <br>

## Skill Version(s): <br>
1.1.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
