## Description:

Openclaw Media Gen helps agents generate images and videos through AIsa using Gemini, Wan, and Seedream models with one API key.

This skill is ready for commercial/non-commercial use.

## Publisher:

[baofeng-tech](https://clawhub.ai/user/baofeng-tech)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to generate images, create video tasks, poll video status, and download generated media from AIsa-supported models. It is suited for agent workflows that need routed image or video API calls from concise prompts and optional reference image URLs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, reference image URLs, and the AIsa API key are sent to a third-party service.

Mitigation: Install and run the skill only when the user trusts AIsa with those inputs, and prefer the AISA_API_KEY environment variable over command-line key arguments.

Risk: Generated media may be downloaded from provider-returned URLs that are not allowlisted or size-limited by the client.

Mitigation: Run the skill in a workspace where downloads cannot overwrite important files, review output paths before execution, and treat automatic downloads as higher risk until URL allowlisting, private-network blocking, content validation, and size limits are added.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/baofeng-tech/skills/openclaw-media-gen-aisa)
- [AIsa API Reference](https://aisa.one/docs/api-reference)
- [AIsa Google Gemini GenerateContent](https://aisa.one/docs/api-reference/chat/generatecontent)
- [AIsa Image Generation via Chat](https://aisa.one/docs/api-reference/chat/image-generation)
- [AIsa OpenAI-Compatible Image Generations](https://aisa.one/docs/api-reference/chat/openai-image-generations)
- [AIsa Create Video Generation Task](https://aisa.one/docs/api-reference/video/post_services-aigc-video-generation-video-synthesis)
- [AIsa Get Video Generation Task Result](https://aisa.one/docs/api-reference/video/get_services-aigc-tasks)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and generated media files from API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and AISA_API_KEY; generated media downloads are written to local output paths selected by the user or client defaults.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
