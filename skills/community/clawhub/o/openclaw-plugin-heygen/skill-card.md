## Description: <br>
Adds HeyGen as a first-class OpenClaw video generation provider for identity-first avatar and presenter videos through the built-in video_generate tool. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[eve-builds](https://clawhub.ai/user/eve-builds) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and OpenClaw users use this plugin to let agents generate scripted HeyGen avatar or presenter videos with selected avatar, voice, style, orientation, image context, and webhook options. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The plugin requires a HeyGen API key and can expose credentials if handled carelessly. <br>
Mitigation: Use a dedicated HeyGen API key where possible, store it in HEYGEN_API_KEY or the approved OpenClaw auth flow, and avoid pasting it into prompts or logs. <br>
Risk: Video generation and smoke tests can spend HeyGen credits. <br>
Mitigation: Confirm user approval before running real generation, keep verification clips short, and check account credits or plan status before repeated use. <br>
Risk: Prompts, image attachments, avatar or voice choices, and webhook URLs are sent to HeyGen for processing. <br>
Mitigation: Avoid sensitive scripts, images, or callback URLs unless approved, and use incognito_mode when the workflow requires reduced provider-side retention. <br>
Risk: Generated presenter videos can be misleading if viewers are not told they are synthetic or avatar-based. <br>
Mitigation: Use the plugin for approved avatar-presenter workflows and disclose synthetic or avatar-generated content where policy, audience, or jurisdiction requires it. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/eve-builds/openclaw-plugin-heygen) <br>
- [HeyGen API documentation](https://docs.heygen.com) <br>
- [HeyGen Video Agent API reference](https://developers.heygen.com/reference/list-video-agent-sessions.md) <br>
- [OpenClaw plugin documentation](https://docs.openclaw.com/plugins) <br>
- [Bundled HeyGen setup notes](docs/heygen.md) <br>


## Skill Output: <br>
**Output Type(s):** [Video, Files, Configuration, Guidance] <br>
**Output Format:** [MP4 video asset with generation metadata, plus Markdown setup guidance and configuration examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generates one video per request, supports 16:9 and 9:16 aspect ratios, accepts up to 20 image attachments, requires HEYGEN_API_KEY, and may spend HeyGen credits.] <br>

## Skill Version(s): <br>
0.1.2 (source: frontmatter, package.json, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
