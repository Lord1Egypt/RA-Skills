## Description:

Generates images by calling a configured third-party image generation API that follows an OpenAI-compatible request and response format.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zuoanco](https://clawhub.ai/user/zuoanco)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to configure credentials, submit image prompts to a chosen compatible provider, and save returned images as PNG files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and request metadata are sent to the configured third-party image API provider.

Mitigation: Use only trusted providers and avoid prompts that contain secrets, personal data, or confidential business information.

Risk: Provider responses may include image URLs that the script downloads and saves locally.

Mitigation: Prefer providers that return base64 image data or verify that returned URLs cannot resolve to internal or otherwise untrusted destinations.

Risk: Generated images are saved in the current working directory.

Mitigation: Run the skill in an intended workspace and review generated files before sharing or reusing them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zuoanco/skills/image-generator-custom)
- [Publisher profile](https://clawhub.ai/user/zuoanco)
- [OpenAI-compatible image generation endpoint example](https://api.openai.com/v1/images/generations)

## Skill Output:

**Output Type(s):** [Files, Shell commands, Configuration instructions, Guidance]

**Output Format:** [PNG image files with terminal status text and Markdown usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses IMAGE_API_URL and IMAGE_API_KEY, optionally IMAGE_MODEL_ID, to call the configured provider; supports prompt, model, size, count, quality, and output-prefix parameters.]

## Skill Version(s):

0.0.2 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
