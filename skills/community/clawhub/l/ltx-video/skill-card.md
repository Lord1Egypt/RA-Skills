## Description:

Generate videos via LTX-2.3 API for text-to-video, image-to-video, audio-to-video lip-sync, video extension, and retake workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pauldelavallaz](https://clawhub.ai/user/pauldelavallaz)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and creators use this skill to call LTX-2.3 video endpoints and write prompts for generating, animating, lip-syncing, extending, or retaking videos from text, images, and audio.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The artifact exposes a specific LTX API key.

Mitigation: Revoke the exposed key, remove it from published copies, and require users to supply their own key through a protected secret mechanism.

Risk: The artifact recommends third-party media upload instructions for files used by video-generation requests.

Mitigation: Use a user-controlled or official private upload path and confirm HTTPS access, MIME type handling, and retention behavior before sending media URLs to the API.

Risk: The ComfyUI custom node install command clones an unpinned repository.

Mitigation: Pin the ComfyUI node to a reviewed commit or release before installation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/pauldelavallaz/skills/ltx-video)
- [LTX Video API base URL](https://api.ltx.video/v1)
- [ComfyUI LTX node](https://github.com/PauldeLavallaz/comfyui-ltx-node)

## Skill Output:

**Output Type(s):** [Guidance, API Calls, Shell commands, Code, Configuration]

**Output Format:** [Markdown with inline bash and Python code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce MP4 files when the generated API calls are executed by the user]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
