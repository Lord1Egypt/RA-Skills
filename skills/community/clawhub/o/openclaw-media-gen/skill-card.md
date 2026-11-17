## Description:

Generate AI images or videos through AIsa for creative generation, asset drafts, and media workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[baofeng-tech](https://clawhub.ai/user/baofeng-tech)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, creators, and agent operators use this skill to generate image or video drafts through AIsa-backed workflows, including creative assets, product-demo concepts, and media workflow prototypes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles AISA_API_KEY and also accepts an explicit API key flag, which can expose credentials through shell history or process listings.

Mitigation: Use AISA_API_KEY from the environment or a credential manager, and avoid passing API keys on the command line.

Risk: The skill can download service-provided media URLs into local workspace paths with limited safety controls.

Mitigation: Run it only in workspaces where generated files can be safely written, review output paths, and enable automatic downloads only when the AIsa response path is trusted.

## Reference(s):

- [Openclaw Media Gen ClawHub Page](https://clawhub.ai/baofeng-tech/skills/openclaw-media-gen)
- [baofeng-tech ClawHub Publisher Profile](https://clawhub.ai/user/baofeng-tech)
- [AIsa API v1 Base](https://api.aisa.one/v1)
- [AIsa Video API Base](https://api.aisa.one/apis/v1)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Files]

**Output Format:** [Markdown guidance with CLI commands; bundled script responses are JSON and generated media files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires AISA_API_KEY and python3; optional downloads can write generated image or video files to the workspace.]

## Skill Version(s):

1.1.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
