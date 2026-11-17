## Description:

Use Nano Banana 2 (Gemini 3.1 Flash Image), the newest image model focused on faster iteration, lower cost, and strong quality. Published 2026-02-26 as the latest Flash-image generation family update. Supports image generation/edit, image-to-image, and 1K/2K/4K.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wegoagain-dev](https://clawhub.ai/user/wegoagain-dev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and creative agents use this skill to generate or edit images through Google's Gemini image service, including draft-to-final workflows at 1K, 2K, or 4K resolution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API keys may be exposed if passed directly in chat or command arguments.

Mitigation: Prefer setting GEMINI_API_KEY through a protected environment or secret manager.

Risk: Prompts and input images are sent to Google's Gemini service during generation or editing.

Mitigation: Avoid sensitive prompts or private images unless the user is comfortable sending them to that service.

Risk: Dependencies and script execution may affect the local environment.

Mitigation: Consider pinning dependencies or running the script in a restricted environment before installing or executing it.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and generated image file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can save PNG image files in the user's current working directory when invoked with a Gemini API key.]

## Skill Version(s):

1.0.5 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
