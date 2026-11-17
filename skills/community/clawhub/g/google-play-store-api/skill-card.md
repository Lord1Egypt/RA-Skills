## Description:

Guides agents to search Google Play through Scavio, retrieve Android app listings and install counts, and page through reviews.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scavio-ai](https://clawhub.ai/user/scavio-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and app researchers use this skill to find Android apps, compare store listings and install counts, inspect data safety information, and analyze reviews across locales.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Requests use Scavio as a third-party API provider.

Mitigation: Confirm that use of this provider is acceptable before sending app queries.

Risk: Exposing the Scavio API key could allow unauthorized use.

Mitigation: Keep SCAVIO_API_KEY in an environment variable or secret store; do not commit it.

Risk: Large review crawls incur credit charges, and locale choices can change the returned storefront.

Mitigation: Confirm the credit budget and locale before crawling; limit review pages and reuse reviews already in app listings.

## Reference(s):

- [Scavio Google Play search documentation](https://scavio.dev/docs/google-play-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=google-play-store-api)
- [Scavio rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=google-play-store-api)
- [ClawHub skill listing](https://clawhub.ai/scavio-ai/skills/google-play-store-api)

## Skill Output:

**Output Type(s):** [Text, JSON, Code, Shell commands, Guidance]

**Output Format:** [Markdown guidance and examples; structured JSON returned by the API]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Review pages use cursors; language and country select the storefront.]

## Skill Version(s):

1.0.4 (source: ClawHub release; bundled frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
