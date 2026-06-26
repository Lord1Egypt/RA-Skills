## Description: <br>
Generates AI images and videos through the AI Artist/DeepSop API from text prompts and optional reference media, then polls asynchronously until the task completes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kukuoai](https://clawhub.ai/user/kukuoai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to turn image or video generation requests into AI Artist API calls, including model selection, optional reference-media upload, cost checks, and result delivery. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and selected reference images, videos, or audio are sent to AI Artist/DeepSop. <br>
Mitigation: Avoid sensitive media unless the external upload is acceptable for the use case, and review AI Artist/DeepSop terms before deployment. <br>
Risk: The skill requires a sensitive AI_ARTIST_TOKEN and can consume paid generation credits. <br>
Mitigation: Use a revocable API key, keep it out of source control, monitor credit usage, and rely on the built-in cost check or dry-run flow before submitting jobs. <br>
Risk: If FEISHU_WEBHOOK_URL is configured, prompts and generated links may be forwarded to that webhook. <br>
Mitigation: Leave the webhook unset unless the destination is trusted and intended for these results. <br>


## Reference(s): <br>
- [AI Artist API Detailed Documentation](references/api.md) <br>
- [Chat Integration Examples](references/chat-integration.md) <br>
- [Feishu Image Sending Guide](references/feishu-integration.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/kukuoai/image-video-gen) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and optional URL, JSON, Markdown image, or downloaded-file outputs from the generation script.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an AI_ARTIST_TOKEN API key; may upload selected reference media to AI Artist/DeepSop; progress is logged separately from final script output.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
