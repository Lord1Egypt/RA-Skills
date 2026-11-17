## Description:

An Instagram data assistant that queries user, post, Reels, Stories, comment, search, hashtag, and location data through MaxHub’s V1, V2, and V3 APIs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiewxx](https://clawhub.ai/user/xiewxx)

### License/Terms of Use:

MIT-0

## Use Case:

External users can ask an agent to retrieve and summarize Instagram account, post, comment, Reels, Stories, hashtag, and location data, or compare results across queries. The skill sends read requests to the MaxHub API service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security assessment notes that the instructions include Douyin operations outside the skill’s Instagram purpose.

Mitigation: Review the Douyin fallback steps before use and confirm they fit the intended task; keep queries within the expected Instagram scope unless those steps are approved.

Risk: The security assessment notes an unpinned installer and authenticated requests to an external service; its analysis is marked partial.

Mitigation: Review the installer source and pin it to a trusted version where possible. Confirm the MaxHub service is intended before configuring MAXHUB_API_KEY or sending authenticated requests.

## Reference(s):

- [Server-resolved source repository](https://github.com/XieWxx/maxhub-instagram)
- [Publisher profile](https://clawhub.ai/user/xiewxx)
- [MaxHub API service and key setup](https://www.aconfig.cn)
- [User API reference](references/api-user.md)
- [Post API reference](references/api-post.md)
- [Search API reference](references/api-search.md)
- [API parameter mappings](references/param-mappings.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Analysis]

**Output Format:** [Concise English or Chinese summaries, lists, and Markdown tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include data returned by API queries and comparisons; no files are produced.]

## Skill Version(s):

0.1.0 (source: server-resolved ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
