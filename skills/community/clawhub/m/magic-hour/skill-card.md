## Description:

Generate AI video and images with the Magic Hour API (Sora 2, Veo 3.1, Kling 3.0, WAN 2.2, GPT-image, Nano Banana Pro). Text-to-video, image-to-video, image generation; free tier available.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rhythmp28](https://clawhub.ai/user/rhythmp28)

### License/Terms of Use:

MIT

## Use Case:

Developers and agents use this skill to generate images, text-to-video clips, image-to-video clips, and job status checks through Magic Hour using a hosted MCP server or local Python scripts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and selected media are sent to Magic Hour for generation.

Mitigation: Use a dedicated API key and avoid secrets, private files, or sensitive content in prompts and uploads.

Risk: The image-to-video workflow accepts local file paths and could upload an unintended image file.

Mitigation: Run the skill in an isolated working directory and pass only explicit, reviewed, non-sensitive image paths.

Risk: Generated media URLs may expose output content to anyone with access to the URL while they remain valid.

Mitigation: Download outputs only to approved locations and handle returned URLs as sensitive when the prompt or media is sensitive.

## Reference(s):

- [Magic Hour Raw HTTP Reference](references/api.md)
- [Magic Hour Model Catalogue](references/models.md)
- [Magic Hour Documentation](https://docs.magichour.ai)
- [Magic Hour Hosted MCP](https://magichour.ai/mcp)
- [Magic Hour Developer Signup](https://magichour.ai/developer)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, JSON, Files, Guidance]

**Output Format:** [Markdown guidance with shell commands and single-object JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated media may be returned as hosted URLs or downloaded files when a download directory is supplied.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
