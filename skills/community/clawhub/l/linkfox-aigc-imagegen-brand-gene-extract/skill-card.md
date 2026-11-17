## Description:

Extracts brand visual DNA from product images and brand inputs, producing structured brandGeneJson for downstream LinkFox image generation workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and e-commerce teams use this skill in LinkFox image-generation pipelines to derive a reusable brand visual profile from product images, brand color, font, platform, region, and language inputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill includes account login, API-key issuance, and payment-order flows in addition to brand-style extraction.

Mitigation: Use the onboarding and payment commands only when LinkFox account setup or billing actions are explicitly intended.

Risk: The skill can use LinkFox API base URL override environment variables.

Mitigation: Do not set LinkFox API base URL overrides unless they point to trusted LinkFox hosts.

Risk: API keys may be copied into persistent shell startup files during onboarding.

Mitigation: Prefer a secret manager or temporary environment variable, and remove or rotate persistent keys when they are no longer needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/linkfox-ai/skills/linkfox-aigc-imagegen-brand-gene-extract)
- [Onboarding guide](references/onboarding.md)
- [LinkFox agent portal](https://agent.linkfox.com/)

## Skill Output:

**Output Type(s):** [text, json, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and structured JSON output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a complete brandGeneJson object and writes it to a session data file for downstream image-generation skills.]

## Skill Version(s):

1.2.2 (source: server release metadata; artifact _meta.json lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
