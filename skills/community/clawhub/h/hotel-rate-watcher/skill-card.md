## Description:

Watch Google Hotels rates and get alerted only when a nightly price drops or hits a target. Use when the user wants hotel price tracking, rate-drop alerts for a destination and dates, or a one-off hotel search with structured rates. Runs the magnova/hotel-price-watch Actor through the Apify plugin for OpenClaw; hotel records cost $0.002 and drop alerts $0.02 on the user's own Apify account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[memeanalyst](https://clawhub.ai/user/memeanalyst)

### License/Terms of Use:

MIT-0

## Use Case:

Travelers use this skill to run a hotel search or track nightly rates for a destination and stay dates, with optional target-price alerts. It reports baseline rates and changes such as price drops or target hits.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A search shares the destination, stay dates, and optional target price with Apify.

Mitigation: Before setup, tell the user what travel details will be shared; use the user's own Apify account and token.

## Reference(s):

- [Hotel Price Watch Actor](https://apify.com/magnova/hotel-price-watch)
- [Hotel Rate Watcher on ClawHub](https://clawhub.ai/memeanalyst/skills/hotel-rate-watcher)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown summaries with structured hotel rate results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include property names, nightly rates, price changes, target-price alerts, errors, and Google Hotels links.]

## Skill Version(s):

1.0.0 (source: frontmatter, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
