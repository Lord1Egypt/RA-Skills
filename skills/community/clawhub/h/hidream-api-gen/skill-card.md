## Description: <br>
Hidream Aigc helps agents call HiDream/OpenClaw/Vivago image and video generation models through Python and CLI interfaces. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhy2015](https://clawhub.ai/user/zhy2015) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to generate images and videos with supported HiDream/OpenClaw models, including Kling, Sora-2-Pro, Seedance, Minimax Hailuo, Seedream, and Nano Banana. It supports direct Python calls and CLI invocation with credential-based access to the Vivago service. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, task metadata, API tokens, and any provided image or video files may be sent to the configured HiDream/Vivago endpoint. <br>
Mitigation: Use only trusted endpoints, avoid private local files unless upload is intended, and use a dedicated or revocable API token where possible. <br>
Risk: A custom HIDREAM_ENDPOINT or OPENCLAW_ENDPOINT could redirect requests to an untrusted host. <br>
Mitigation: Do not set custom endpoint variables unless the host is trusted and expected for the release. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zhy2015/hidream-api-gen) <br>
- [Vivago service](https://vivago.ai) <br>
- [Vivago API token page](https://vivago.ai/platform/token) <br>
- [Vivago account and credits page](https://vivago.ai/platform/info) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, API calls, files] <br>
**Output Format:** [Markdown guidance, Python or shell command snippets, JSON API responses, and saved image or video files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated media may be downloaded to the skill's local assets directory when a media URL is returned.] <br>

## Skill Version(s): <br>
0.1.9 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
