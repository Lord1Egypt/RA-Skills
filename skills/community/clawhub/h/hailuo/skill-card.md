## Description:

Guides agents in generating Hailuo videos from text or images through AceDataCloud's API, including director-mode animation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[acedatacloud](https://clawhub.ai/user/acedatacloud)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and creators use this skill to request text-to-video and image-to-video generation and monitor asynchronous tasks through AceDataCloud's Hailuo API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The AceDataCloud API key could be exposed or used beyond the intended video endpoints.

Mitigation: Keep the key out of prompts and committed files, and restrict allowed APIs to the endpoints needed.

Risk: Submitted prompts and source image URLs are sent to AceDataCloud's hosted service.

Mitigation: Submit only prompts and image URLs approved for sharing with the provider.

Risk: Retrying video generation while an asynchronous task is pending can incur additional charges.

Mitigation: Check the existing task ID and balance before submitting another generation request.

## Reference(s):

- [Hailuo Video on ClawHub](https://clawhub.ai/acedatacloud/skills/hailuo)
- [AceDataCloud application and API key setup](https://platform.acedata.cloud/console/applications)
- [Asynchronous task polling guide referenced by the skill](https://github.com/AceDataCloud/Skills/blob/main/skills/_shared/async-tasks.md)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, API request guidance]

**Output Format:** [Markdown with bash and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides asynchronous task polling; generated videos come from the external service.]

## Skill Version(s):

1.0.1 (source: server-resolved ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
