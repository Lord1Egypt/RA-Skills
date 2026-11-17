## Description:

Searches and analyzes TikTok video performance across TikTok Shop marketplaces using region, creator, product, category, engagement, duration, publish-time, advertising, selling, and AI-video filters.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External sellers, marketers, and analysts use this skill to discover TikTok videos, compare engagement trends, and estimate video-level sales attribution across supported TikTok Shop regions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a LinkFox API key and may handle account signup or login flows.

Mitigation: Install only when the user accepts LinkFox API-key use, and review account signup, SMS-code, and API-key handling before allowing the skill.

Risk: EchoTik queries consume paid LinkFox compute credits and the onboarding flow can involve billing or payment QR behavior.

Mitigation: Confirm user intent before repeated or paid queries, and review billing, plan, and payment behavior before enabling it.

Risk: The skill can persist full query results locally and can report feedback automatically.

Mitigation: Keep generated linkfox output directories out of shared or committed project files, and review feedback-reporting behavior before installation.

Risk: Custom LINKFOX_* endpoint environment variables could redirect API traffic.

Mitigation: Avoid setting custom LinkFox endpoint environment variables unless the endpoint is explicitly trusted.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/linkfox-ai/skills/linkfox-echotik-list-video)
- [EchoTik list video API reference](artifact/references/api.md)
- [Authentication and billing onboarding](artifact/references/onboarding.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON API responses and saved JSON result files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May summarize large API responses while saving full JSON results to a local linkfox output directory.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
