## Description:

Fetches product lists for a specified Ozon category from Seerfar, including category aggregates such as sales, revenue, average price, rating, seasonality, and per-product metrics for category analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External sellers, marketplace analysts, and developers use this skill to inspect Ozon category capacity, price bands, seasonality, and ranked product performance when they already have or can resolve an Ozon category ID.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can handle account setup, phone/SMS login, payment ordering, and API key configuration.

Mitigation: Use official LinkFox account channels and a secret manager for credentials; avoid sharing OTPs or persisting keys in shell profile files unless reviewed by the user.

Risk: The skill writes full API responses and cached data to local linkfox directories.

Mitigation: Review saved response files before sharing a workspace and avoid querying confidential marketplace data in untrusted environments.

Risk: The security scan reports silent feedback-reporting behavior to LinkFox.

Mitigation: Install and run the skill only when the user accepts sharing relevant feedback and queried data with LinkFox.

Risk: Repeated calls consume paid compute credits.

Mitigation: Use the built-in cache and get user confirmation before repeated, paginated, or exploratory calls that may add cost.

## Reference(s):

- [API reference](artifact/references/api.md)
- [Authentication and billing onboarding](artifact/references/onboarding.md)
- [ClawHub skill page](https://clawhub.ai/linkfox-ai/skills/linkfox-seerfar-ozon-category-search)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Files, Shell commands, Configuration guidance]

**Output Format:** [Markdown tables and summaries with saved JSON response files and optional shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Full API responses are saved under a local linkfox data directory; large responses are summarized unless inline output is requested.]

## Skill Version(s):

1.0.6 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
