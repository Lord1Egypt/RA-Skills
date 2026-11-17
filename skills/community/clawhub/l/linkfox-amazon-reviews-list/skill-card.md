## Description:

Fetches and analyzes Amazon product reviews by ASIN across 15 marketplaces with star, keyword, verified-purchase, sort, format, and media filters.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External sellers, ecommerce analysts, and agents use this skill to retrieve Amazon reviews for a single ASIN, filter them by marketplace, star rating, keyword, media, or verified-purchase status, and summarize customer praise, complaints, and product improvement signals.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan reports under-disclosed account, billing, credential, and automatic feedback-reporting behavior.

Mitigation: Review the LinkFox account, billing, and feedback flows before installation; make feedback submission explicit opt-in for sensitive deployments.

Risk: The skill handles API keys and may guide users to configure credentials in shell startup files.

Mitigation: Prefer a managed secret store or scoped environment injection, and avoid committing or sharing shell profiles that contain API keys.

Risk: The skill can create persistent local review result files and may process customer review data from live third-party services.

Mitigation: Run it only in appropriate workspaces, disclose paid API use before large requests, and clean local result files according to the user's data retention requirements.

## Reference(s):

- [Amazon Reviews API Reference](references/api.md)
- [Authentication and Billing Onboarding](references/onboarding.md)
- [ClawHub Skill Page](https://clawhub.ai/linkfox-ai/skills/linkfox-amazon-reviews-list)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown responses with JSON result files and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes full API responses to workspace-local linkfox session data files; stdout may contain full JSON or a compact summary depending on response size.]

## Skill Version(s):

1.0.10 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
