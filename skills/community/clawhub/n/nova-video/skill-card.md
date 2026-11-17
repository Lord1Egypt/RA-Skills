## Description:

Generate images or videos using the Nova Video OpenAPI from a single user prompt.

This skill is ready for commercial/non-commercial use.

## Publisher:

[onesoloapp](https://clawhub.ai/user/onesoloapp)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use NovaVideo to generate still images, create short videos, poll video generation status, and list prior image or video generations through the Nova Video API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and reference images are sent to Nova Video.

Mitigation: Avoid sensitive, private, proprietary, or non-consented prompts and media.

Risk: Installation guidance delegates control to mutable remote skill instructions.

Mitigation: Review fetched skill content before following it, and prefer a registry-validated release when available.

Risk: Credentialed requests can use a configurable base URL.

Mitigation: Set NOVA_BASE_URL only to the intended HTTPS Nova endpoint before using NOVA_API_KEY.

## Reference(s):

- [NovaVideo ClawHub listing](https://clawhub.ai/onesoloapp/skills/nova-video)
- [Nova Video API service](https://nova-video.onesolo.app)
- [Publisher profile](https://clawhub.ai/user/onesoloapp)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance, Files]

**Output Format:** [Markdown guidance with bash curl commands and API response handling.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write long signed video URLs to video_url.txt to preserve the full link.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
