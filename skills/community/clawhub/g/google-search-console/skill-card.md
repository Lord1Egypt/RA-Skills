## Description:

Access Google Search Console through Maton to review search performance, inspect URL indexing, and manage sitemaps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[byungkyu](https://clawhub.ai/user/byungkyu)

### License/Terms of Use:

MIT-0

## Use Case:

Site owners, marketers, and developers use this skill to examine search analytics and index status, review sitemaps, and request approved sitemap changes through their connected Search Console account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sitemap changes or new connections can affect a different site or grant broader access than intended.

Mitigation: Confirm the account, site, scope, and exact write operation with the user before connecting or changing a sitemap; prefer read-only queries otherwise.

Risk: Hosted functions, triggers, and destinations may persist or automatically forward data.

Mitigation: Obtain separate approval for the automation, destination, scope, and persistence before enabling it; send only necessary data.

Risk: Raw API keys and full API responses may expose credentials or personal data.

Mitigation: Prefer OAuth through the CLI, keep any API key out of commands and logs, and share only the response fields needed for the task.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/byungkyu/skills/google-search-console)
- [Maton homepage](https://maton.ai)
- [Maton CLI manual](https://cli.maton.ai/manual)
- [Google Search Console API reference](https://developers.google.com/webmaster-tools/v1/api_reference_index)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with command examples and summarized API results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the connected account's authorization and the requested Search Console operation.]

## Skill Version(s):

1.2.6 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
