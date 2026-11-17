## Description:

Generate images via NewAPI Banana API (nano-banana, Gemini). Supports text-to-image and image-to-image.

This skill is ready for commercial/non-commercial use.

## Publisher:

[loobayn](https://clawhub.ai/user/loobayn)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to generate or edit images through the NewAPI Banana service from text prompts or reference images.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API keys may be exposed through chat or command-line handling.

Mitigation: Configure keys outside chat using a protected secret store, tightly permissioned config, or environment variable; rotate any key already shared in chat or used with the documented HTTP endpoint.

Risk: Credentials and user content may be sent to the NewAPI Banana provider over plain HTTP.

Mitigation: Use the skill only if the provider is trusted and the network path is acceptable; the publisher should switch the API URL to HTTPS-only.

Risk: Generated image downloads may come from URLs returned by the provider.

Mitigation: Validate downloaded image URLs and file contents before relying on or redistributing generated outputs.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/loobayn/skills/newapi-banana)
- [API Key Setup Guide](references/api-key-setup.md)
- [Image Generation Guide](references/image-generation.md)
- [Output Delivery Guide](references/output-delivery.md)

## Skill Output:

**Output Type(s):** [Files, Text, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Generated image files with text status, cost, and error messages]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses NEWAPI_API_KEY, requires python3 and curl, and writes generated images to /tmp/openclaw/newapi-output.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
