## Description:

Google Search Console data analysis and site management via google-search-console-cli for search performance, query analysis, URL index inspection, sitemap management, and site property review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bin-huang](https://clawhub.ai/user/bin-huang)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and SEO teams use this skill to have an agent run Google Search Console CLI workflows for search performance analysis, URL inspection, sitemap review, and site property management.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs agents to install an unpinned npm package globally.

Mitigation: Install only after trusting the npm package and source, prefer isolated project-local tooling over global installation, and document the installed version.

Risk: The skill includes Search Console commands that can add or remove sites and submit or delete sitemaps.

Mitigation: Require explicit user confirmation before running site-add, site-remove, sitemap-submit, or sitemap-delete, and prefer read-only Search Console credentials for analysis tasks.

Risk: Search Console credentials and exported search data may expose sensitive site information.

Mitigation: Use least-privilege Google credentials, avoid exposing credential file contents, and handle command outputs as potentially sensitive.

## Reference(s):

- [Google Search Console CLI documentation](https://github.com/Bin-Huang/google-search-console-cli)
- [Search Analytics API](https://developers.google.com/webmaster-tools/v1/searchanalytics/query)
- [URL Inspection API](https://developers.google.com/webmaster-tools/v1/urlInspection.index/inspect)
- [Sites API](https://developers.google.com/webmaster-tools/v1/sites)
- [Sitemaps API](https://developers.google.com/webmaster-tools/v1/sitemaps)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown with JSON examples and inline bash command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Search Console API JSON or compact NDJSON results when commands are run.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
