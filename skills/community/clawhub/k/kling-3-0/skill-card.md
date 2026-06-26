## Description: <br>
Kling 3.0 video generation on RunComfy, covering Standard, Pro, and 4K text-to-video and image-to-video endpoints through the local RunComfy CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kalvinrv](https://clawhub.ai/user/kalvinrv) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and creative operators use this skill to choose a Kling 3.0 tier and invoke RunComfy jobs for cinematic text-to-video or image-to-video generation. It is suited for previews, social clips, 1080p hero clips, native 4K masters, and image animation workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: RunComfy jobs can incur paid video-generation costs, especially for longer clips, audio, or 4K output. <br>
Mitigation: Confirm tier, duration, audio settings, and expected cost before submitting jobs; iterate with lower-cost Standard settings when possible. <br>
Risk: The skill requires a RunComfy token and may store or read credentials from the local RunComfy configuration. <br>
Mitigation: Protect RUNCOMFY_TOKEN and ~/.config/runcomfy, avoid sharing credentials, and use scoped or revocable tokens where available. <br>
Risk: Prompts and image URLs are processed by RunComfy and upstream model infrastructure. <br>
Mitigation: Avoid confidential prompts or private image URLs unless provider-side processing is acceptable for the intended use. <br>


## Reference(s): <br>
- [RunComfy](https://www.runcomfy.com) <br>
- [RunComfy CLI documentation](https://docs.runcomfy.com/cli/introduction) <br>
- [Kling 3.0 on RunComfy](https://www.runcomfy.com/models/kling/kling-3.0) <br>
- [ClawHub skill page](https://clawhub.ai/kalvinrv/kling-3-0) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Markdown] <br>
**Output Format:** [Markdown guidance with inline JSON and bash command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces RunComfy CLI invocation guidance; generated media files are produced by the external RunComfy service, not by the skill text itself.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
