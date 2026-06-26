## Description: <br>
AI-powered video generation skill. Use when the user wants to generate videos from text descriptions, browse video recipes, upload assets, or manage video creation workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sunnykui](https://clawhub.ai/user/sunnykui) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, creators, and developers use this skill to ask an agent to generate videos from text prompts, user-provided media, or recipe templates and deliver the completed video through supported chat platforms. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Chat-platform tokens or token-bearing URLs may be exposed in logs during attachment handling. <br>
Mitigation: Avoid Telegram attachment upload until token-bearing URL logging is fixed; use environment variables or a secret manager and least-privilege bot or app credentials. <br>
Risk: Prompts, uploaded media, generated videos, and delivery data are sent to Medeo and selected chat platforms. <br>
Mitigation: Use the skill only for content acceptable to share with those services, and avoid sensitive or regulated media unless approved by policy. <br>
Risk: Local job history and configuration can remain in the medeo-video workspace after use. <br>
Mitigation: Clear the local medeo-video workspace when prompts, media references, generated links, or job history are sensitive. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/sunnykui/medeo-video) <br>
- [Medeo Platform](https://medeo.app) <br>
- [Medeo API key setup](https://medeo.app/dev/apikey) <br>
- [Medeo API documentation](https://docs.prd.medeo.app/) <br>
- [Asset upload guide](docs/assets-upload.md) <br>
- [Feishu delivery guide](docs/feishu-send.md) <br>
- [Multi-platform delivery guide](docs/multi-platform.md) <br>
- [Recipe guide](docs/recipes.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, API calls, Files] <br>
**Output Format:** [Markdown guidance with shell commands and JSON command outputs; generated video files or URLs may be delivered through chat platforms.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Medeo API key and may use chat-platform credentials for native delivery.] <br>

## Skill Version(s): <br>
1.5.2 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
