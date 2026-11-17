## Description:

Generate AI images via the Infinimo AI Design API--model/aspect/resolution selection, reference uploads, job submission, and result polling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anyunzhong](https://clawhub.ai/user/anyunzhong)

### License/Terms of Use:

MIT-0

## Use Case:

External developers, e-commerce sellers, and creative teams use this skill to generate, edit, and retrieve product or reference-based images through the Infinimo AI Design API. It helps agents choose generation settings, upload optional references, submit jobs, and return output image links with the relevant parameters.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, selected images, and API tokens are sent to the Clawec/Infinimo service.

Mitigation: Use the skill only with data that is appropriate for that service, avoid confidential or regulated images, and prefer a narrowly scoped or disposable API key when available.

Risk: The upload helper can send any local file path provided to it and does not enforce the documented image-only limit.

Mitigation: Review each upload path before execution and do not allow the agent to upload arbitrary local files.

## Reference(s):

- [Infinimo AI Design](https://design.infinimo.ai/?source=q-i-d-clawhub)
- [Infinimo API Key](https://design.infinimo.ai/api-key?source=q-i-d-clawhub)
- [AI Image Generation Response Schema](references/response-schema.md)
- [ClawHub Skill Page](https://clawhub.ai/anyunzhong/skills/infinimo-ai-design-image-create)
- [ClawHub Publisher Profile](https://clawhub.ai/user/anyunzhong)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown summary with image URLs, selected generation parameters, reference counts, and inline shell commands when useful]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include model, aspect ratio, resolution, prompt, reference image count, result URLs, failure status, and credit usage when returned by the API.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
