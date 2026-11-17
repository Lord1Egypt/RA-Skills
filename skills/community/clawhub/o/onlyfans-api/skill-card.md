## Description:

Query OnlyFans data and analytics via the OnlyFansAPI.com platform, including revenue summaries, model performance, trial-link conversion, tracking-link conversion, and link earnings comparisons.

This skill is ready for commercial/non-commercial use.

## Publisher:

[martingalovic](https://clawhub.ai/user/martingalovic)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to query OnlyFansAPI.com for connected-account analytics, including agency-level revenue, model rankings, link conversion rates, and earnings breakdowns. It is intended for explicit analytics and reporting requests where the user has configured an OnlyFansAPI API key.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can access sensitive multi-account business, earnings, model, link, and account analytics.

Mitigation: Use it only for explicit analytics or reporting requests, scope requests to the needed accounts and dates, and treat returned results as sensitive business information.

Risk: The skill summary and behavior are broad enough to activate on casual or underspecified OnlyFans prompts when an API key is available.

Mitigation: Confirm the user's reporting intent before making API calls for broad prompts, and avoid using the skill for unrelated or casual OnlyFans discussion.

Risk: The skill depends on an API key and live network calls to OnlyFansAPI.com.

Mitigation: Require the ONLYFANSAPI_API_KEY environment variable, avoid exposing the key in output, and report failed requests, rate limits, or unauthenticated accounts before continuing.

## Reference(s):

- [OnlyFansAPI Docs](https://docs.onlyfansapi.com)
- [OnlyFansAPI Console](https://app.onlyfansapi.com)
- [OnlyFans API Access on ClawHub](https://clawhub.ai/martingalovic/skills/onlyfans-api)
- [ClawHub Publisher Profile](https://clawhub.ai/user/martingalovic)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown tables with inline shell commands and summarized API results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires ONLYFANSAPI_API_KEY, curl, jq, and network access to app.onlyfansapi.com.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
