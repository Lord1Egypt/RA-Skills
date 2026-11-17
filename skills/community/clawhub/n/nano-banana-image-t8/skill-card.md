## Description:

Nano Banana Image T8 helps agents run Nano Banana text-to-image and image-edit tests through the bundled API test script, using user prompts, optional uploaded images, model choices, and size or aspect-ratio options.

This skill is ready for commercial/non-commercial use.

## Publisher:

[flywhale-666](https://clawhub.ai/user/flywhale-666)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and image workflow testers use this skill to validate Nano Banana text-to-image and image-to-image generation with real API calls. It helps agents collect required prompts, image inputs, API key state, model selection, and output paths for concise test results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A reusable API key may be saved under ~/.whaleclaw/credentials and reused by later runs.

Mitigation: Use a limited or throwaway API key, keep file permissions restrictive, and remove the saved key when it is no longer needed.

Risk: Changing the API base URL could send credentials, prompts, and images to an unintended endpoint.

Mitigation: Use the documented default endpoint and avoid custom base URLs until endpoint validation or removal is available.

Risk: Image prompts and uploaded images are sent to an external image API and generated images may be downloaded from returned URLs.

Mitigation: Use non-sensitive inputs, review the service terms, and run the skill only in trusted environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/flywhale-666/skills/nano-banana-image-t8)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, files, guidance]

**Output Format:** [Markdown or plain text with shell commands, structured errors, and generated image file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a user prompt, optional uploaded image paths, optional model selection, optional aspect ratio or size, and a Nano Banana API key.]

## Skill Version(s):

0.1.5 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
