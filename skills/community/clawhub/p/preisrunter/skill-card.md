## Description:

Searches and compares grocery prices and promotions in Austria and Germany via the Preisrunter API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[davidus05](https://clawhub.ai/user/davidus05)

### License/Terms of Use:


## Use Case:

External users and shopping assistants use this skill to search grocery prices and promotions in Austria and Germany, compare stores, filter by region or shop, and return source product links.

### Deployment Geography for Use:

Austria and Germany

## Known Risks and Mitigations:

Risk: Grocery search terms and filters are sent to Preisrunter's API.

Mitigation: Avoid entering sensitive personal information in searches or filters.

Risk: The upstream API may rate-limit requests or return no-product responses.

Mitigation: Avoid aggressive polling and handle HTTP 429 and HTTP 404 responses gracefully.

## Reference(s):

- [Preisrunter](https://preisrunter.at)
- [Preisrunter OpenClaw Products API](https://api.preisrunter.net/wrapper/openclaw-v1/products/)
- [ClawHub Skill Page](https://clawhub.ai/davidus05/skills/preisrunter)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown or plain text with API-backed grocery result summaries and source product links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No API key is required; searches require curl and jq when using the documented shell examples.]

## Skill Version(s):

1.0.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
