## Description:

NeoBoost GEO 服务 helps users query brand visibility, health, snapshots, AI preference analysis, AI source statistics, topic words, prompt words, competitors, materials, aliases, and AI-assisted content generation or optimization in GEO or NeoBoost.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chinaberg](https://clawhub.ai/user/chinaberg)

### License/Terms of Use:

MIT-0

## Use Case:

External business, brand, and marketing users use this skill to request NeoBoost or GEO brand analytics, competitor visibility data, prompt and topic management, and AI-assisted content work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Brand, competitor, prompt, and content-generation requests may include sensitive business information processed by the NeoBoost service.

Mitigation: Use the skill only with data appropriate for the configured NeoBoost account and privacy expectations.

Risk: The skill requires a NeoBoost API key for access.

Mitigation: Store NEOBOOST_API_KEY in the agent environment, limit access to trusted users, and rotate the key if it is exposed.

## Reference(s):

- [NeoBoost homepage](https://neoboost.oneaix.com)
- [ClawHub skill page](https://clawhub.ai/chinaberg/skills/neoboost)

## Skill Output:

**Output Type(s):** [Text, Guidance, Shell commands, Configuration]

**Output Format:** [Markdown or plain text responses with optional shell commands and configuration steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl and a NEOBOOST_API_KEY environment variable for NeoBoost access.]

## Skill Version(s):

0.2.2 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
