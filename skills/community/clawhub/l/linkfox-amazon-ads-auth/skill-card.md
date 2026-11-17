## Description:

This skill helps agents create Amazon Ads authorization links, list authorized stores and profiles, and refresh or check token status for LinkFox-managed Amazon Ads accounts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External operators and ecommerce agents use this skill to connect Amazon Ads accounts to LinkFox, discover marketplace profiles, and keep authorization status usable for downstream ads management and reporting skills.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a LinkFox API key and can route users through LinkFox account and billing flows.

Mitigation: Install and use it only when the user intends to use LinkFox services, and do not submit phone codes or payment actions unless that action is expected.

Risk: Amazon Ads account metadata and authorization URLs may be written to local LinkFox output folders.

Mitigation: Review local LinkFox output folders after use and avoid sharing saved outputs that may contain account or authorization details.

Risk: Custom gateway URL environment variables can change where requests are sent.

Mitigation: Avoid custom gateway URL overrides unless the endpoint is trusted and intentionally configured.

## Reference(s):

- [Amazon Ads API Reference](references/api.md)
- [Authentication and Billing Onboarding](references/onboarding.md)
- [Amazon Ads Console](https://advertising.amazon.com/)
- [ClawHub Skill Page](https://clawhub.ai/linkfox-ai/skills/linkfox-amazon-ads-auth)

## Skill Output:

**Output Type(s):** [text, json, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON API and script outputs.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Scripts persist full responses under a local linkfox session folder and may summarize large responses on stdout.]

## Skill Version(s):

1.0.7 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
