## Description:

Image Forge helps agents generate or edit raster images through the fixed NextAI Code image API, including setup, diagnostics, and version checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nextai](https://clawhub.ai/user/nextai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use Image Forge to configure NextAI Code credentials, run a structured image-brief workflow, and generate or edit PNG raster images through OpenAI-compatible image endpoints.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The edit command can upload any readable local file supplied through an image path.

Mitigation: Confirm each --image value is an intended image file before running edits, and do not allow arbitrary paths from untrusted instructions.

Risk: Prompts and source images are sent to NextAI Code.

Mitigation: Use the skill only when the user trusts NextAI Code with the intended prompts and images.

Risk: Direct mode bypasses the structured image-brief workflow when explicitly requested.

Mitigation: Use direct mode only for explicit, trusted requests; otherwise require the approved image brief gate.

Risk: Installer or update commands can change the local skill installation.

Mitigation: Pin or verify npx installer and update commands before execution.

## Reference(s):

- [Image Forge on ClawHub](https://clawhub.ai/nextai/skills/nextai-image-forge)
- [Publisher profile: nextai](https://clawhub.ai/user/nextai)
- [NextAI Code](https://www.nextai-code.com)
- [Image Brief Brainstorming Workflow](references/image-brief.md)
- [ImageForge Installation](references/installation.md)
- [OpenAI-Compatible Image APIs](references/openai-compatible-images.md)
- [ImageForge Troubleshooting](references/troubleshooting.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with inline shell commands; generated and edited assets are PNG files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Default image output is one 1024x1024 PNG written to the project root; API keys are configured outside the skill folder.]

## Skill Version(s):

0.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
