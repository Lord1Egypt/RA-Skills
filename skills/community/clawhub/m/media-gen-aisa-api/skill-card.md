## Description:

Generate images and videos with AIsa across supported Gemini, Wan, and Seedream image models plus Wan text-to-video and image-to-video variants.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bibaofeng](https://clawhub.ai/user/bibaofeng)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users can use this skill to generate images, submit asynchronous video jobs, poll task status, and download generated media through the AIsa API using one API key.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, reference image URLs, task IDs, and the AIsa API key are sent to AIsa.

Mitigation: Use non-sensitive prompts and reference images, and provide the key through AISA_API_KEY instead of command-line arguments.

Risk: The helper can download API-provided URLs and write generated media to arbitrary output paths.

Mitigation: Run the skill in a workspace with limited file permissions and choose output paths that cannot overwrite important files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bibaofeng/skills/media-gen-aisa-api)
- [AIsa homepage](https://aisa.one)
- [AIsa API reference](https://aisa.one/docs/api-reference)
- [Google Gemini Chat generateContent](https://aisa.one/docs/api-reference/chat/generatecontent)
- [Image Generation via Chat](https://aisa.one/docs/api-reference/chat/image-generation)
- [OpenAI-Compatible Image Generations](https://aisa.one/docs/api-reference/chat/openai-image-generations)
- [Create video generation task](https://aisa.one/docs/api-reference/video/post_services-aigc-video-generation-video-synthesis)
- [Get video generation task result](https://aisa.one/docs/api-reference/video/get_services-aigc-tasks)
- [Agent Skills specification](https://agentskills.io/specification)

## Skill Output:

**Output Type(s):** [Files, JSON, Shell commands, Guidance]

**Output Format:** [Markdown guidance with CLI commands; generated image or video files and JSON task/status responses.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python 3 and AISA_API_KEY; output files are written to user-selected paths.]

## Skill Version(s):

1.0.0 (source: evidence.release.version and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
