## Description: <br>
Next Video Gen helps AI coding agents generate images and videos through the Volcengine Ark API, including text-to-image, text-to-video, image-to-video, and video-to-video workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vennduan](https://clawhub.ai/user/vennduan) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent users use this skill to turn natural-language prompts and optional image, video, or audio references into generated media through Volcengine Ark models. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a sensitive Volcengine Ark API key. <br>
Mitigation: Use a limited-scope API key and avoid persisting it in shell startup files unless plaintext storage is acceptable. <br>
Risk: Prompts and media URLs are sent to Volcengine Ark for generation. <br>
Mitigation: Avoid private, regulated, or otherwise sensitive content when using this skill. <br>
Risk: The security summary flags weak guardrails and an overbroad authenticated request helper. <br>
Mitigation: Prefer the fixed generation scripts for normal use and review requests before execution. <br>


## Reference(s): <br>
- [Next Video Gen ClawHub Page](https://clawhub.ai/vennduan/next-video-gen) <br>
- [Project Homepage](https://github.com/vennduan/next-video-gen) <br>
- [API Parameters](references/api-params.md) <br>
- [Volcengine Ark Console](https://console.volcengine.com/ark) <br>
- [Doubao Seedream 5.0 Model](https://console.volcengine.com/ark/model_detail?Id=doubao-seedream-5-0-260128) <br>
- [Doubao Seedance 1.5 Pro Model](https://console.volcengine.com/ark/model_detail?Id=doubao-seedance-1-5-pro-251215) <br>
- [Doubao Seedance 2.0 Model](https://console.volcengine.com/ark/model_detail?Id=doubao-seedance-2-0-260128) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and generated media links or local file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include image URLs, video URLs, local saved file paths, resolution, aspect ratio, duration, audio status, and elapsed generation time.] <br>

## Skill Version(s): <br>
1.0.6 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
