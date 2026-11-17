## Description:

SIF-关键词流量 analyzes Amazon keyword traffic across competing ASINs, breaking down organic search, Sponsored Products ads, brand and video ads, recommendation placements, and AC/ER/TR exposure with ASIN, date-range, marketplace, and source filters.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External Amazon sellers, ecommerce analysts, and agent operators use this skill to inspect which ASINs receive traffic for a keyword and how that exposure is split across organic search, paid ads, and recommendation surfaces.

### Deployment Geography for Use:

Global; API coverage is limited to the US, UK, DE, CA, JP, FR, ES, IT, MX, AU, AE, BR, and SA Amazon marketplaces.

## Known Risks and Mitigations:

Risk: The skill sends keyword, ASIN, account, and billing-related requests to LinkFox services.

Mitigation: Install and run it only when the user trusts LinkFox with the queried business data, account details, and credential flow.

Risk: Onboarding can handle phone-based login, expose generated API keys, create paid credit orders, and display payment artifacts.

Mitigation: Use a private environment, keep API keys out of shared logs or transcripts, and require explicit user confirmation before registration or purchase steps.

Risk: The skill can write full API responses and cache files to local linkfox directories.

Mitigation: Review stored response files for sensitive business data and clean session or cache directories when retention is not needed.

Risk: Endpoint override environment variables can redirect LinkFox API traffic.

Mitigation: Use the default endpoints unless the publisher documents a trusted override, and avoid running with inherited environment overrides in shared shells.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/linkfox-ai/skills/linkfox-sif-keyword-summary)
- [SIF keyword traffic API reference](references/api.md)
- [Authentication and billing onboarding](references/onboarding.md)
- [LinkFox Skills](https://skill.linkfox.com/)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, configuration, guidance]

**Output Format:** [Markdown summaries and tables, JSON API responses, and shell command snippets.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The API script writes full response JSON to a local linkfox session data directory, prints small responses inline, summarizes large responses, and caches matching requests for 24 hours.]

## Skill Version(s):

1.0.8 (source: server release evidence and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
