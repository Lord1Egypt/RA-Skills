## Description:

Multi Search helps agents query 16 Chinese and international web search and knowledge engines with advanced operators, time filters, site search, and no API key.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sclawbot](https://clawhub.ai/user/sclawbot)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to choose suitable search engines for Chinese or international queries, fetch search result pages, and aggregate findings into a concise search report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms are sent to third-party search engines, despite source text claiming data stays local.

Mitigation: Avoid secrets, credentials, customer data, private document text, internal hostnames, and sensitive investigation terms; require confirmation of selected engines before multi-engine searches.

Risk: Automated multi-engine requests may trigger rate limits or conflict with individual search engine terms.

Mitigation: Use the documented request delays and batch limits, reduce engine count for repeated queries, and confirm permitted use against each selected search engine's terms.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/sclawbot/skills/msearch)
- [ClawHub Homepage](https://clawhub.ai/sclawbot/msearch)
- [Domestic Search Engine Deep Search Guide](references/advanced-search.md)
- [International Search Engine Deep Search Guide](references/international-search.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, guidance]

**Output Format:** [Markdown search report with optional web_fetch examples and source links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search queries may be sent to selected third-party search engines; no API key is required.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
