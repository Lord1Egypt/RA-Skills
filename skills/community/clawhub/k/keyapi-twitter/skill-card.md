## Description:

Keyapi Twitter helps agents analyze Twitter/X data through the KeyAPI REST API using live official KeyAPI documentation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xyzzero](https://clawhub.ai/user/xyzzero)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts use this skill to route Twitter/X research questions into KeyAPI-backed workflows for tweets, profiles, timelines, social graph data, trends, communities, lists, jobs, and Spaces. It is useful when an agent needs current API documentation, credential setup guidance, live API calls, and concise analysis that separates returned facts from inference.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: KeyAPI receives the Twitter/X queries, identifiers, and analysis targets used in live API calls.

Mitigation: Use the skill only for Twitter/X requests that are appropriate to send to KeyAPI, and avoid submitting sensitive research targets unless the user has authorized that disclosure.

Risk: The authentication setup flow can persist KEYAPI_TOKEN in shell profile files, and passing a token with --token can expose it through local command history or process metadata.

Mitigation: Prefer a session-scoped KEYAPI_TOKEN or a dedicated secret manager, review shell profile changes before deployment, and avoid passing real tokens on the command line.

## Reference(s):

- [Global Rules](references/global-rules.md)
- [Routing Policy](references/routing-policy.md)
- [Scenario Cards](references/scenarios.md)
- [Twitter/X Rules](references/twitter-rules.md)
- [Twitter/X Content Module Rules](references/twitter-content-rules.md)
- [Twitter/X Profile And Social Module Rules](references/twitter-profile-social-rules.md)
- [Twitter/X Community Module Rules](references/twitter-community-rules.md)
- [Setup And Auth](references/setup-and-auth.md)
- [KeyAPI Docs Index](https://docs.keyapi.ai/llms.txt)
- [KeyAPI Twitter Documentation](https://docs.keyapi.ai/en/twitter/)
- [KeyAPI Bearer Authentication](https://docs.keyapi.ai/overview/authentication#bearer-authentication)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and optional JSON/API result summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include live API-backed observations, setup instructions, endpoint details, and analysis that separates returned facts from inference.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
