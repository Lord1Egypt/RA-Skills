## Description:

Nano Banana, Nano Banana Pro, Nano Banana 2 - Google AI image generation models for AI agents. Ultra-high character consistency, 1K-4K resolution, up to 14 reference images, extreme aspect ratios up to 21:9 and 8:1.

This skill is ready for commercial/non-commercial use.

## Publisher:

[seekton](https://clawhub.ai/user/seekton)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to create images through the Monet API with Nano Banana models, including character-consistent image series, high-resolution generations, style transfer, and ultra-wide image formats.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, reference image URLs, and uploaded image files are sent to monet.vision under the user's Monet account.

Mitigation: Avoid sensitive prompts and files, and use the skill only when sharing that content with Monet is acceptable.

Risk: The MONET_API_KEY is required for API calls and could be exposed through logs or shared transcripts.

Mitigation: Store the key in an environment variable, keep it out of logs and transcripts, and avoid verbose request output that may disclose request details.

Risk: Uploaded image files are hosted by Monet for temporary access.

Mitigation: Upload only files suitable for temporary third-party hosting and account for the documented 24-hour retention window.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/seekton/skills/nano-banana-skill)
- [Monet API Platform](https://monet.vision)
- [Monet API Keys](https://monet.vision/skills/keys)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code, Configuration]

**Output Format:** [Markdown with bash, JSON, and TypeScript examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires MONET_API_KEY; generated image tasks return asynchronous task metadata and hosted output URLs from Monet.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
