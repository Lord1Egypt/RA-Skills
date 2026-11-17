## Description:

Transforms natural-language image requests into structured Gemini image-generation prompts with style-specific details for photography, illustration, anime, 3D, watercolor, product, minimalist, and surreal outputs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[minilozio](https://clawhub.ai/user/minilozio)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent users use this skill to convert casual image requests into detailed structured prompts and command examples for Gemini-based image generation or image editing workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompt text may be shaped by the user and then passed through a documented local shell command.

Mitigation: Review commands before execution and prefer implementations that pass prompt JSON as a separate process argument, file, or stdin.

Risk: Generated output filenames or paths could overwrite existing files or write outside the intended location.

Mitigation: Use agent-derived safe filenames, check for collisions, and confirm any non-default output path before running the generator.

Risk: The workflow requires GEMINI_API_KEY for image generation.

Mitigation: Install and use the skill only in environments where local command execution and access to that API key are acceptable.

## Reference(s):

- [Structured Prompt Guide for Gemini Image Generation](references/prompt-guide.md)
- [ClawHub Release Page](https://clawhub.ai/minilozio/skills/nano-banana-prompting)
- [Google AI Studio API Key](https://aistudio.google.com/apikey)
- [OpenClaw](https://openclaw.ai)
- [Claude Code](https://code.claude.com)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [Markdown guidance with JSON prompt templates and bash command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires uv, GEMINI_API_KEY, and a compatible Gemini image-generation script or skill.]

## Skill Version(s):

1.0.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
