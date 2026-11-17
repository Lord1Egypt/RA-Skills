## Description:

Generate images & videos with AIsa. Gemini 3 Pro Image (image) + Qwen Wan 2.6 (video) via one API key.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chaimengphp](https://clawhub.ai/user/chaimengphp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to generate image files and create, poll, and optionally download video generation tasks through AIsa using one API key.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, reference image URLs, task IDs, and generated media metadata are sent to AIsa's external service.

Mitigation: Use the skill only for data appropriate for AIsa, avoid secrets and internal URLs, and review prompts before submission.

Risk: The skill requires an AISA_API_KEY for authenticated API calls.

Mitigation: Use a dedicated, revocable API key and avoid sharing it in prompts, command history, or generated files.

Risk: Generated media downloads may create or overwrite local files at the selected output path.

Mitigation: Choose output paths deliberately and inspect existing files before running download commands.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chaimengphp/skills/openclaw-aisa-media-gen)
- [OpenClaw homepage](https://openclaw.ai)
- [AIsa API Reference](https://docs.aisa.one/reference/)
- [AIsa GenerateContent API](https://docs.aisa.one/reference/generatecontent)
- [AIsa video synthesis API](https://docs.aisa.one/reference/post_services-aigc-video-generation-video-synthesis)
- [AIsa task polling API](https://docs.aisa.one/reference/get_services-aigc-tasks)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash examples and JSON command responses from the client script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or overwrite local image and MP4 files when generation or download commands are run.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
