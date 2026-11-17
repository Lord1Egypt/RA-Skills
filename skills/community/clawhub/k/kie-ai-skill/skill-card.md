## Description:

Kie Ai Skill gives OpenClaw agents unified kie.ai access for image generation across models such as Nano Banana Pro, Flux, and 4o-image, with local storage, optional Google Drive upload, usage tracking, and task resume.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jon-xo](https://clawhub.ai/user/jon-xo)

### License/Terms of Use:

MIT

## Use Case:

Developers and OpenClaw users use this skill to generate and retrieve images through kie.ai from agent prompts, inspect model pricing and balance information, resume tasks, and optionally upload generated files to Google Drive.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A credential-handling flaw could send the kie.ai API key to an untrusted image-download URL.

Mitigation: Use a low-value or scoped KIE_API_KEY, treat keys used with untrusted task results as potentially exposed, and remove the Authorization header from image downloads or enforce a strict HTTPS host allowlist with redirect validation before broad use.

Risk: Image prompts are sent to kie.ai, and generated image files are stored locally or sent to Maton only when Drive upload is enabled.

Mitigation: Avoid sensitive prompt content unless kie.ai and Maton handling is acceptable for the use case; leave Drive upload disabled unless Google Drive export is required.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jon-xo/skills/kie-ai-skill)
- [Kie Ai Skill repository](https://github.com/jon-xo/kie-ai-skill)
- [kie.ai documentation](https://docs.kie.ai)
- [kie.ai pricing](https://docs.kie.ai/pricing)
- [Maton Drive upload service](https://maton.ai)

## Skill Output:

**Output Type(s):** [Text, Files, Shell commands, Configuration]

**Output Format:** [Terminal text, local image files, optional JSON responses, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires KIE_API_KEY for kie.ai requests; MATON_API_KEY is optional for Google Drive upload; generated files and task state are stored locally.]

## Skill Version(s):

1.0.1 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
