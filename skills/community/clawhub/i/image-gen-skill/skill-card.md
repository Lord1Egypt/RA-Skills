## Description: <br>
Image Gen helps OpenClaw agents generate or edit images from text prompts or reference images through a configured Nano-banana-compatible image API, compressing large results and saving them to the workspace. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zweien](https://clawhub.ai/user/zweien) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external OpenClaw users use this skill to generate images from prompts or edit images from user-provided references, then save the generated image files for follow-up use or sharing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and reference images may be sent to the configured image API provider. <br>
Mitigation: Avoid private, regulated, copyrighted, or confidential inputs unless the provider account and data-handling terms permit that use. <br>
Risk: A misconfigured API base URL could send generation requests or uploaded image data to an unintended provider. <br>
Mitigation: Verify IMAGE_API_BASE_URL and account credentials before use. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/zweien/image-gen-skill) <br>
- [Nano-banana API](https://api.imyaigc.top) <br>
- [OpenClaw](https://github.com/openclaw/openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and generated image files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated images are saved with timestamped filenames; images over 1 MB may be compressed while originals are retained.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
