## Description:

Generates images through ThinkZone AI when an agent is asked to draw, create, or transform an image, with support for Gemini, MiniMax, and Seedream image models.

This skill is ready for commercial/non-commercial use.

## Publisher:

[renjicode](https://clawhub.ai/user/renjicode)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to have an agent generate image assets from prompts or reference images through the configured ThinkZone AI API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Bundled plaintext API credentials may be exposed or reused.

Mitigation: Remove bundled keys, rotate any exposed ThinkZone credentials, and configure a user-owned THINKZONE_API_KEY at runtime.

Risk: Prompts and reference images may be uploaded to the configured external API endpoint.

Mitigation: Avoid sensitive prompts or private reference images unless the user intends to send them to the ThinkZone endpoint.

Risk: Loosely scoped API base URL configuration can redirect requests.

Mitigation: Review THINKZONE_BASE_URL before use and keep it set to the intended ThinkZone AI endpoint.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/renjicode/skills/keplerjai-image-gen)
- [ThinkZone AI platform](https://open.thinkzoneai.com)

## Skill Output:

**Output Type(s):** [Files, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Image files with JSON metadata and Markdown usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires THINKZONE_API_KEY and may upload prompts or reference images to the configured external API endpoint.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
