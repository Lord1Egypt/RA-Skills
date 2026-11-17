## Description:

Production-ready decentralized search for AI agents. Privacy-first, uncensored web search via distributed node infrastructure.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nosytlabs](https://clawhub.ai/user/nosytlabs)

### License/Terms of Use:


## Use Case:

Developers and external agent users use this skill to configure AI agents to call the Presearch Search API for privacy-oriented web search results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries are sent to Presearch's external API and may expose sensitive terms if users include secrets, private customer data, or confidential project details.

Mitigation: Do not include passwords, secrets, private customer data, or confidential project details in search queries.

Risk: The skill requires a Presearch bearer token for API access.

Mitigation: Store and handle the bearer token as a secret, and install the skill only when external Presearch API usage is acceptable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nosytlabs/skills/presearch)
- [Presearch Search API endpoint](https://na-us-1.presearch.com/v1/search)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown API reference with code examples and JSON response shape]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Describes bearer-token authentication, query parameters, rate limits, error codes, and expected search result fields.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
