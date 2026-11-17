## Description:

KokoChat Search lets an OpenClaw agent retrieve web search results through KokoChat's hosted Brave-backed search proxy without storing search API keys on the user's machine.

This skill is ready for commercial/non-commercial use.

## Publisher:

[komako-workshop](https://clawhub.ai/user/komako-workshop)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to let agents run lightweight web searches and receive normalized search results without configuring a local search-provider key.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms are sent to KokoChat's hosted search service at deeply.plus by default.

Mitigation: Use the skill only for queries that are acceptable to share with that hosted service, or configure a private endpoint and token for private deployments.

Risk: The hosted search endpoint can fail, be unconfigured, or rate-limit requests.

Mitigation: Check JSON responses for ok:false and report the failure instead of inventing URLs or search results.

## Reference(s):

- [ClawHub KokoChat Search release page](https://clawhub.ai/komako-workshop/skills/kokochat-search)
- [Default KokoChat hosted search endpoint](https://deeply.plus/deeply/search)

## Skill Output:

**Output Type(s):** [Text, API Calls]

**Output Format:** [JSON object with search result titles, URLs, snippets, provider metadata, and JSON error responses on failure]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search query input is capped at 500 characters, result count is clamped to 1-10, and the default request timeout is 15 seconds.]

## Skill Version(s):

0.2.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
