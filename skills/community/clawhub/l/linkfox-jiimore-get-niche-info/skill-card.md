## Description:

Queries and summarizes Jiimore Amazon niche market intelligence for a single niche ID, including market metrics, buyer review insights, competitive landscape, price trends, and growth trends.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External sellers, analysts, and commerce operators use this skill to retrieve and interpret Amazon niche market data from Jiimore by known niche ID. It supports market overview, pricing, demand, competition, product launch, inventory, review, advertising, and profitability analysis for the US, JP, and DE marketplaces.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Niche IDs and related market context are sent to LinkFox/Jiimore.

Mitigation: Use the skill only when the user accepts sharing that market context with the provider, and avoid submitting confidential or unnecessary data.

Risk: The skill includes an automatic feedback path that can report user intent or result quality.

Mitigation: Avoid feedback reporting unless the user has given explicit consent and sensitive content has been redacted.

Risk: Authentication, phone verification, payment handling, and API key setup are part of the onboarding flow.

Mitigation: Use onboarding only with a trusted provider relationship, keep OTPs and API keys protected, and prefer a secure secret store for credentials.

Risk: Full API responses and request cache entries are written to local LinkFox data directories.

Mitigation: Review local storage expectations before use, limit sensitive queries, and clear saved response or cache files when retention is not needed.

## Reference(s):

- [Jiimore Niche Market Info API Reference](references/api.md)
- [Authentication and Billing Onboarding](references/onboarding.md)
- [ClawHub Skill Page](https://clawhub.ai/linkfox-ai/skills/linkfox-jiimore-get-niche-info)
- [LinkFox Skills](https://skill.linkfox.com/)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown summaries and tables, JSON API responses, local JSON data files, and setup or onboarding shell commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Queries one niche ID per call, supports US, JP, and DE marketplaces, caches matching requests for 24 hours, and writes full API responses under the local linkfox session data directory.]

## Skill Version(s):

1.0.7 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
