## Description:

A Lemon8 data assistant for searching and analyzing posts, users, comments, topics, and trending content through MaxHub.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiewxx](https://clawhub.ai/user/xiewxx)

### License/Terms of Use:

MIT-0

## Use Case:

External users and marketing or research teams can use the skill to explore Lemon8 search results, posts, user profiles, comments, topics, and trends, then summarize the returned data in English or Chinese.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan marks the release suspicious and the scan is incomplete, citing instructions that route some requests to Douyin APIs.

Mitigation: Follow the scan guidance: review the Douyin fallback and external data flow before installation, and do not install until the concern is resolved.

Risk: The skill requires a MaxHub API key and sends API requests to the external service at aconfig.cn.

Mitigation: Confirm the service and data flow are appropriate for your use, and keep the API key confidential.

## Reference(s):

- [Server-resolved source repository](https://github.com/XieWxx/maxhub-lemon8)
- [MaxHub service](https://www.aconfig.cn)
- [Search and discovery API reference](references/api-search-discover.md)
- [Post and user API reference](references/api-post-user.md)
- [Parameter mappings](references/param-mappings.md)

## Skill Output:

**Output Type(s):** [API Calls, Analysis, Text, Markdown]

**Output Format:** [Bilingual natural-language summaries and Markdown tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Summarizes data returned by the service; supports English and Chinese.]

## Skill Version(s):

0.1.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
