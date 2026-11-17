## Description:

Generate a video task based on user-provided text and images, including image URLs and local file paths, and submit it to a remote video service using an API key.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhangyuangao](https://clawhub.ai/user/zhangyuangao)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to turn a text prompt and a source image into a remote image-to-video generation task, then receive the created task ID and final video URL.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends selected image inputs to the MagicLight remote service.

Mitigation: Use it only with images approved for remote processing, and avoid private documents, credential files, internal URLs, localhost URLs, and cloud metadata URLs.

Risk: The client can fetch arbitrary image URLs or upload any readable local file path provided as image input.

Mitigation: Prefer a known image file in a dedicated folder or a trusted public HTTPS image URL.

Risk: Passing the API key on the command line may expose credentials through shell history or process listings.

Mitigation: Provide MAGIC_API_KEY through a protected environment variable rather than the --api-key option.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhangyuangao/skills/magic-image2video)
- [MagicLight remote service endpoint](https://open-test.magiclight.ai)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and parsed JSON results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires MAGIC_API_KEY and returns a task ID followed by a video URL when generation succeeds.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
