## Description:

Nanobanana Plus helps agents call the nanobanana-plus CLI to generate images with per-call model selection and aspect-ratio controls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[webkubor](https://clawhub.ai/user/webkubor)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and creative agents use this skill to generate local image files through a Node.js CLI using Gemini or Imagen image models. It is suited for workflows that need prompt-driven image generation with explicit model, aspect-ratio, and output-count controls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can execute an external nanobanana-plus JavaScript program with access to the agent environment, including API keys.

Mitigation: Install only from a trusted publisher and use a dedicated, limited-scope API key for image generation.

Risk: Executable resolution can fall back to a nanobanana-plus command from the surrounding environment.

Mitigation: Run the skill from a controlled installation and avoid directories where untrusted files or commands could shadow the intended executable.

Risk: Image prompts may be sent to an external model provider.

Mitigation: Do not include secrets, confidential data, or sensitive personal information in prompts.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/webkubor/skills/nanobanana-plus)

## Skill Output:

**Output Type(s):** [Files, Shell commands, Guidance]

**Output Format:** [Markdown guidance with inline shell commands; CLI execution can produce local image files and terminal output.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js and a Gemini-compatible API key supplied through the environment.]

## Skill Version(s):

1.5.5 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
