## Description:

Access Google Search Console API via cURL with managed OAuth through Maton to manage sites, sitemaps, and search analytics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[otman-ai](https://clawhub.ai/user/otman-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, site owners, and SEO operators use this skill to issue cURL requests through Maton for Google Search Console workflows such as listing sites, querying search analytics, and managing sitemaps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: MATON_API_KEY exposure could disclose access to the user's Maton-connected services.

Mitigation: Store the key in an environment variable and avoid pasting or printing the full value in chats, logs, or support tickets.

Risk: DELETE and PUT examples can change connections or sitemap state when placeholders are replaced with real values.

Mitigation: Verify connection IDs, site URLs, and sitemap feed paths before running write or delete requests.

Risk: Incorrectly encoded site URLs or paths can query or modify the wrong Search Console resource.

Mitigation: URL-encode site URLs and review generated request URLs before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/otman-ai/skills/google-search-console-maton)
- [Maton](https://maton.ai)
- [Maton control console](https://ctrl.maton.ai)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with cURL commands, JSON request bodies, and configuration notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a MATON_API_KEY and valid Google Search Console connection.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
