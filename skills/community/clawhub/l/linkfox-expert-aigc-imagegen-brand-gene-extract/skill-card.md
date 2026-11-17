## Description:

Extracts a structured brand visual gene from product images and brand parameters, including core color, typography, localized background direction, lighting, and brand placement guidance for downstream image-generation workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, ecommerce teams, and agent workflows use this skill to convert product images and brand settings into reusable visual identity JSON for product image sets and related AIGC pipelines.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and product image or video URLs may be processed by LinkFox-hosted services.

Mitigation: Use only media and prompts authorized for LinkFox-hosted processing; avoid private media, confidential product assets, and secrets unless that processing has been approved.

Risk: The bundled onboarding and billing flows can involve account registration, API keys, plan selection, and payment steps.

Mitigation: Treat these as sensitive account operations, verify LinkFox account pages and terms before use, and prefer a secure secret store over writing API keys into shell profile files.

Risk: Endpoint and session path behavior can be influenced by environment variables.

Mitigation: Set LinkFox endpoint variables and SESSION_ID only from trusted configuration, especially in shared workspaces and automated agent environments.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/linkfox-ai/skills/linkfox-expert-aigc-imagegen-brand-gene-extract)
- [AI 生文 API 参考](artifact/skills/linkfox-aigc-textgen/references/api.md)
- [解决认证和算力问题](artifact/skills/linkfox-aigc-textgen/references/onboarding.md)

## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration, guidance]

**Output Format:** [Structured JSON plus saved JSON files and command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a length-1 brandGeneJson list with brand color, background strategy, typography, heading/body color strategy, and layout guidance.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
