## Description:

Google News API helps agents retrieve Google News search results, latest and section headlines, language-region codes, topic headlines, and decoded article URLs through fetcher.sh.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fetcher-sh](https://clawhub.ai/user/fetcher-sh)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agent builders use this skill to integrate paid Google News search, headline retrieval, topic lookup, language-region discovery, and redirect decoding into news monitoring, aggregation, media tracking, and press mention workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Queries and Google News redirect URLs are sent to fetcher.sh as part of normal API use.

Mitigation: Avoid private, account-specific, or sensitive URLs and confidential query terms; review the third-party service fit before using it for sensitive monitoring.

Risk: The skill uses a paid third-party API and may require a FETCHER_API_KEY or x402 payment flow.

Mitigation: Confirm that paid API use is acceptable for the deployment, and store FETCHER_API_KEY in normal secret or configuration storage rather than hardcoding it in shared files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fetcher-sh/skills/google-news)
- [Server-resolved GitHub source](https://github.com/fetcher-sh/fetcher-skills/tree/main/skills/google-news)
- [Full agent setup](https://google-news.fetcher.sh/skill.md)
- [OpenAPI 3.1 contract](https://google-news.fetcher.sh/openapi.json)
- [Condensed catalog](https://google-news.fetcher.sh/llms.txt)
- [Service site](https://google-news.fetcher.sh)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with HTTP endpoint examples, curl commands, and MCP configuration JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce paid external API requests to fetcher.sh when an agent executes the documented calls.]

## Skill Version(s):

0.1.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
