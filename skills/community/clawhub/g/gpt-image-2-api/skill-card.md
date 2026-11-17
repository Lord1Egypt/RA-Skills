## Description:

Generate and edit images via OpenAI gpt-image-2 model. Agent-agnostic CLI that supports configurable base_url/api_key, text-to-image generation, and image-to-image editing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jancong](https://clawhub.ai/user/jancong)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to add command-line image generation and editing workflows through the OpenAI gpt-image-2 API. It helps agents create image files, edit existing images, and manage API configuration without adding Python package dependencies.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send API keys, prompts, and uploaded images to a configured API base URL.

Mitigation: Use the default OpenAI API base URL unless the configured relay is trusted with credentials and image content.

Risk: Inline API keys passed through command-line arguments may be exposed through shell history or process listings.

Mitigation: Prefer configuration that references an environment variable, such as OPENAI_API_KEY or GPT_IMAGE2_API_KEY, and review file permissions on config files.

Risk: The bundled Node.js execSync example is unsafe for untrusted prompts.

Mitigation: Use argument-array subprocess APIs or otherwise avoid shell interpolation when integrating this skill with untrusted input.

Risk: The skill writes generated or edited image files to paths selected by the agent or user.

Mitigation: Review output paths before execution and run the skill with filesystem permissions appropriate for the workspace.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jancong/skills/gpt-image-2-api)
- [Publisher profile](https://clawhub.ai/user/jancong)
- [Default OpenAI API base URL](https://api.openai.com/v1)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with shell commands and generated image files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The CLI prints status text and saved image paths; image outputs are written to the configured filesystem path.]

## Skill Version(s):

2.0.0 (source: server release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
