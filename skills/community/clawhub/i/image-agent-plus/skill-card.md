## Description:

Use image-agent-plus CLI to generate images, prioritizing image2 for high-quality text and prompt-following, with Codex/Gemini fallback.

This skill is ready for commercial/non-commercial use.

## Publisher:

[webkubor](https://clawhub.ai/user/webkubor)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and creative teams use this skill to have an agent invoke the image-agent-plus CLI for prompt-based image generation through OpenAI/image2, Codex, or Gemini. It supports provider checks, aspect-ratio selection, output counts, file output paths, and collection of images generated in an active Codex session.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Direct provider API mode may read OpenAI API keys from environment variables when configured.

Mitigation: Run image-agent-plus check before use and configure provider keys only through approved shell or agent secret-management mechanisms.

Risk: Codex collection copies generated images from Codex's generated image folder to a user-selected output location.

Mitigation: Review the selected output path and generated image before sharing, moving, or publishing the file.

Risk: Nested non-interactive Codex CLI image generation can hang or fail.

Mitigation: Use the active Codex image tool first, then run image-agent-plus collect-codex after Codex reports the generated image.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/webkubor/skills/image-agent-plus)
- [Project homepage](https://github.com/webkubor/image-agent-plus)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, files]

**Output Format:** [Markdown with inline shell commands and CLI option guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated images are written to the requested output path or the documented default output folder; Codex-generated images may be copied from the active Codex generated image folder.]

## Skill Version(s):

2.0.5 (source: frontmatter and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
