## Description:

Generate images from text prompts using the Jimeng API with configurable size, scale, seed, and output path.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gkhcsc](https://clawhub.ai/user/gkhcsc)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to call the Jimeng image-generation API from Python, save generated PNG files, and return the resulting image through the agent's user channel.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses unpinned dependency installation guidance for an external image API client.

Mitigation: Install dependencies in an isolated environment and pin volcengine-python-sdk to a reviewed version before use.

Risk: The skill requires Jimeng API credentials and submits prompt text to an external service.

Mitigation: Use credentials scoped for image generation and avoid submitting sensitive prompts or confidential content.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gkhcsc/skills/jimeng-image-skill-openclaw)

## Skill Output:

**Output Type(s):** [Shell commands, Code, Files, Guidance]

**Output Format:** [Markdown guidance with shell commands and generated PNG image files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated images are saved to the configured output path, defaulting to ~/.openclaw/workspace/images.]

## Skill Version(s):

0.1.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
