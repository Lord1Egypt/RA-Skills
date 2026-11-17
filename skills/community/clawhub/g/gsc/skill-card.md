## Description:

Read Google Search Console properties, Search Analytics, URL Inspection, and sitemaps for explicit Search Console or GSC SEO performance, indexing, and freshness analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jdrhyne](https://clawhub.ai/user/jdrhyne)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, site owners, and SEO analysts use this skill to authenticate read-only Google Search Console access and inspect properties, Search Analytics rows, URL Inspection state, and sitemaps. It is intended for bounded GSC analysis, not general web search.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires OAuth access to Google Search Console data.

Mitigation: Grant only the documented read-only scope and install it only where access to the relevant Search Console data is acceptable.

Risk: OAuth client secrets and token files could expose account data if mishandled.

Mitigation: Keep credential files private, use protected local paths, and avoid sharing secrets, authorization codes, refresh tokens, or access tokens in chat or command arguments.

Risk: Python dependencies are version-ranged rather than pinned by a lockfile.

Mitigation: Use an isolated Python environment and pin or lock dependencies before production use.

Risk: Search Console returns top rows and bounded pagination can produce partial results.

Mitigation: Preserve and review pagination, freshness, has_more, partial, and provider_top_rows_only metadata before treating results as complete.

## Reference(s):

- [Search Analytics query](https://developers.google.com/webmaster-tools/v1/searchanalytics/query)
- [URL Inspection](https://developers.google.com/webmaster-tools/v1/urlInspection.index/inspect)
- [Installed-app OAuth](https://developers.google.com/identity/protocols/oauth2/native-app)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, JSON, Guidance]

**Output Format:** [Markdown guidance with shell commands and JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should preserve Search Console freshness and pagination metadata, including partial result indicators.]

## Skill Version(s):

1.3.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
