## Description: <br>
Generate videos through the LTX-2.3 API for text-to-video, image-to-video, audio-to-video lip-sync, video extension, and retake workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[PauldeLavallaz](https://clawhub.ai/user/PauldeLavallaz) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and creative operators use this skill to generate or modify MP4 videos with LTX-2.3 from prompts, images, audio, and existing video clips. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The artifact contains a live-looking API key. <br>
Mitigation: Do not use the embedded key; rotate it if owned by the publisher and provide user-specific credentials through an environment variable or secret manager. <br>
Risk: The skill recommends uploading audio, image, or video files to a public file host. <br>
Mitigation: Avoid sending sensitive portraits, voice recordings, or private videos to public hosts unless retention and access policies are acceptable; prefer controlled HTTPS storage. <br>


## Reference(s): <br>
- [LTX Video API base URL](https://api.ltx.video/v1) <br>
- [ComfyUI LTX node](https://github.com/PauldeLavallaz/comfyui-ltx-node) <br>
- [ClawHub release page](https://clawhub.ai/PauldeLavallaz/ltx-video) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with curl examples, Python snippets, endpoint notes, and prompting guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an LTX API key and HTTPS media URLs; API responses are MP4 binary downloads.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
