## Description: <br>
xAI Grok Imagine API integration that helps agents generate and edit images and videos from text prompts, source images, or video URLs using an xAI API key. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[DevvGwardo](https://clawhub.ai/user/DevvGwardo) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent operators use this skill to connect chat or automation workflows to xAI media generation for creating images, generating video clips, animating images, editing media with natural-language instructions, polling long-running jobs, and downloading outputs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and media URLs are sent to xAI for media generation and may expose sensitive content. <br>
Mitigation: Use a dedicated xAI API key and avoid submitting private or sensitive prompts or media without consent. <br>
Risk: Media generation can incur account costs and consume quota. <br>
Mitigation: Monitor usage, rate limits, and concurrent jobs before running large or repeated generation requests. <br>
Risk: Generated files are downloaded from temporary URLs and could be saved outside the intended workspace. <br>
Mitigation: Download outputs promptly and save them only to an intended workspace output directory. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/DevvGwardo/grok-imagine-video) <br>
- [Bundled xAI Grok Imagine API reference](references/api_reference.md) <br>
- [xAI image generation documentation](https://docs.x.ai/developers/model-capabilities/images/generation) <br>
- [xAI video generation documentation](https://docs.x.ai/developers/model-capabilities/video/generation) <br>
- [xAI console](https://console.x.ai/) <br>
- [OpenClaw documentation](https://docs.openclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [Code, Shell commands, Configuration, Guidance, Files] <br>
**Output Format:** [Markdown guidance with Python and bash examples; API calls can download generated image or video files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires XAI_API_KEY; sends prompts and media URLs to xAI; generated media URLs are temporary and should be downloaded to the intended workspace output directory.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
