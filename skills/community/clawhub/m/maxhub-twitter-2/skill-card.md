## Description:

Queries Twitter/X posts, user profiles, comments, search results, and trends through the MaxHub API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiewxx](https://clawhub.ai/user/xiewxx)

### License/Terms of Use:

MIT-0

## Use Case:

Communications and social media teams use this skill to retrieve Twitter/X posts, user data, comments, search results, and trends, then summarize or compare the results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms and request data are sent to an external API service.

Mitigation: Avoid including confidential or sensitive terms in queries.

Risk: The security review notes that the installer command is unpinned and its analysis is incomplete.

Mitigation: Review the source and release before installing, and use a pinned release when available.

Risk: API requests require a MaxHub API key.

Mitigation: Store MAXHUB_API_KEY securely and keep its value out of prompts and generated output.

## Reference(s):

- [Server-resolved source repository](https://github.com/XieWxx/maxhub-twitter)
- [ClawHub release](https://clawhub.ai/xiewxx/skills/maxhub-twitter-2)
- [MaxHub API service](https://www.aconfig.cn)
- [Tweet API reference](artifact/references/api-tweet.md)
- [Search and trending API reference](artifact/references/api-search-trending.md)
- [Parameter mappings](artifact/references/param-mappings.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Analysis, Guidance]

**Output Format:** [Markdown summaries, tables, and setup guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses follow the user's English or Chinese language; results depend on the external API.]

## Skill Version(s):

0.1.0 (source: ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
