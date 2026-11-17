## Description:

Searches the live web, extracts content from top results, and returns source material that an agent can summarize with citations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill when they need current online information, news, trends, Reddit or community discussion, product research, fact checks, or source-backed web retrieval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: LinkFox receives search queries and account or onboarding data.

Mitigation: Use the skill only for queries and account workflows appropriate to share with LinkFox.

Risk: Full search responses and payment QR artifacts may remain in local LinkFox data and cache files.

Mitigation: Review and clean local LinkFox output directories when results or payment artifacts contain sensitive information.

Risk: Endpoint override environment variables can redirect requests away from the default LinkFox services.

Mitigation: Set override environment variables only for destinations that are fully trusted.

Risk: Generated API keys can appear in logs or shell configuration during onboarding.

Mitigation: Treat generated API keys as secrets and avoid sharing logs, terminal output, or shell configuration that contains them.

Risk: The skill consumes paid credits for searches and includes billing flows.

Mitigation: Confirm expected usage volume and credit cost before high-frequency calls.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/linkfox-ai/skills/linkfox-tsearch-search)
- [Web search API reference](artifact/references/api.md)
- [Authentication and billing onboarding guide](artifact/references/onboarding.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown summaries and JSON search responses with titles, URLs, extracted content, and cost metadata.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Searches use a single keyword parameter up to 1000 characters; full responses may be written to local LinkFox data and cache files.]

## Skill Version(s):

1.0.6 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
