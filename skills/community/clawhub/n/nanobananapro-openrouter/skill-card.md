## Description:

Generate and edit images with Nano Banana Pro (Gemini 3 Pro Image) through OpenRouter, including text-to-image and image-to-image workflows at 1K, 2K, and 4K resolutions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liberalchang](https://clawhub.ai/user/liberalchang)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and creative teams use this skill to generate new PNG images or edit existing images through OpenRouter using prompt-driven workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and input images may be sent to OpenRouter for generation or editing.

Mitigation: Use the skill only when sharing that content with OpenRouter is acceptable, and avoid submitting sensitive or regulated data.

Risk: API keys can be provided in command arguments, which may expose credentials in shell history or process listings.

Mitigation: Set OPENROUTER_KEY in the environment instead of passing keys in chat or command arguments.

Risk: Generated files can be written outside the default output directory when custom paths are used.

Mitigation: Use simple filenames in the skill's output_images directory and review any custom output directory before execution.

## Reference(s):

- [OpenRouter chat completions API](https://openrouter.ai/api/v1/chat/completions)
- [ClawHub skill page](https://clawhub.ai/liberalchang/skills/nanobananapro-openrouter)
- [Publisher profile](https://clawhub.ai/user/liberalchang)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, code, configuration, files]

**Output Format:** [Markdown guidance with shell commands and generated PNG image files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated images are saved as PNG files, with default output in the skill's output_images directory unless a custom output directory is provided.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
