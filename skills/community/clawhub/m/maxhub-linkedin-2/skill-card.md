## Description:

Queries LinkedIn professional data through the MaxHub API, including profiles, companies, jobs, posts, comments, and ads, with V1/V2 API support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiewxx](https://clawhub.ai/user/xiewxx)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to query and summarize LinkedIn profile, company, job, post, comment, and advertising data through MaxHub, with optional multi-endpoint analysis and comparison.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review flags the LinkedIn-only scope, a Douyin fallback, and disclosure of search terms or identifiers to MaxHub for review.

Mitigation: Check the skill's scope and fallback routes, and confirm which search terms or identifiers will be sent to MaxHub before using it.

Risk: The installation command is unpinned, and the scan was partial because two references could not be resolved.

Mitigation: Verify and pin the release or source before installation, and review the unresolved references when available.

## Reference(s):

- [Source repository](https://github.com/XieWxx/maxhub-linkedin/tree/6addd78937c89ab8094bb48cd1b15a5a5b76afc1)
- [User API reference](https://github.com/XieWxx/maxhub-linkedin/blob/6addd78937c89ab8094bb48cd1b15a5a5b76afc1/references/api-user.md)
- [Company API reference](https://github.com/XieWxx/maxhub-linkedin/blob/6addd78937c89ab8094bb48cd1b15a5a5b76afc1/references/api-company.md)
- [Search and jobs API reference](https://github.com/XieWxx/maxhub-linkedin/blob/6addd78937c89ab8094bb48cd1b15a5a5b76afc1/references/api-search-jobs.md)
- [Content and ads API reference](https://github.com/XieWxx/maxhub-linkedin/blob/6addd78937c89ab8094bb48cd1b15a5a5b76afc1/references/api-content.md)
- [Parameter mappings](https://github.com/XieWxx/maxhub-linkedin/blob/6addd78937c89ab8094bb48cd1b15a5a5b76afc1/references/param-mappings.md)
- [MaxHub API service and API key signup](https://www.aconfig.cn)

## Skill Output:

**Output Type(s):** [Text, Markdown, Analysis, API data summaries]

**Output Format:** [Concise text or Markdown, with tables for analyses and comparisons]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses follow the user's language; counts use K/M/B in English or 万/亿 in Chinese.]

## Skill Version(s):

0.1.0 (source: server-resolved ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
