## Description:

Generates and refines images from text prompts or input images using Google Gemini Nano Banana models through the Wisdom Gate API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[0n1onr1ng](https://clawhub.ai/user/0n1onr1ng)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to generate, edit, combine, and iteratively refine images from prompts or reference images while selecting model, aspect ratio, size, and output path.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, selected input images, and refinement context may be sent to Wisdom Gate or Gemini services.

Mitigation: Avoid sensitive or regulated images unless approved, and use a dedicated API key.

Risk: Multi-turn refinement can persist conversation history in conversation.json or a custom history file.

Mitigation: Keep history files out of shared folders, backups, and source control, and reset or delete them when no longer needed.

Risk: Running the scripts requires local Python dependencies and an API key in the execution environment.

Mitigation: Install dependencies in a virtual environment and scope credentials to this use case.

## Reference(s):

- [Nano Banana Image Skills on ClawHub](https://clawhub.ai/0n1onr1ng/skills/nano-banana-skills)
- [Wisdom Gate](https://wisgate.ai)
- [Wisdom Gate Gemini generateContent endpoint](https://api.wisgate.ai/v1beta/models/{model}:generateContent)

## Skill Output:

**Output Type(s):** [Files, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands; generated PNG image files and JSON conversation history when scripts are run.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Image outputs are PNG by default; refinement can persist conversation history in a JSON file.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
