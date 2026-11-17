## Description:

A Google Play Store API guide for using fetcher.sh to search Android apps and fetch details, reviews, permissions, data safety disclosures, similar apps, and developer catalogs with prepaid credits or x402 payments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fetcher-sh](https://clawhub.ai/user/fetcher-sh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, agents, and app-market analysts use this skill to query Google Play app search, details, reviews, permissions, data safety disclosures, similar apps, and developer catalogs without Play Console access.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses fetcher.sh with either a Bearer API key or an x402 payment flow.

Mitigation: Confirm trust in fetcher.sh before use, protect and rotate API keys, and review payment authorization before enabling paid calls.

Risk: Paid calls are disclosed as non-refundable if upstream failures occur.

Mitigation: Start with low-volume tests, monitor credit balance or x402 spending, and account for failed upstream requests in operational workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fetcher-sh/skills/google-play-api)
- [Server-resolved GitHub provenance](https://github.com/fetcher-sh/fetcher-skills/tree/main/skills/google-play)
- [Full agent setup](https://googleplay.fetcher.sh/skill.md)
- [OpenAPI 3.1 contract](https://googleplay.fetcher.sh/openapi.json)
- [Condensed catalog](https://googleplay.fetcher.sh/llms.txt)
- [Google Play fetcher site](https://googleplay.fetcher.sh)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, API calls]

**Output Format:** [Markdown guidance with curl examples, endpoint descriptions, and MCP JSON configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides calls to a paid external API whose service responses are JSON.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
