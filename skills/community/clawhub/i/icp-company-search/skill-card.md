## Description:

This skill guides an agent to find ICP-matched company prospect lists with initial research summaries from public or authorized business sources.

This skill is ready for commercial/non-commercial use.

## Publisher:

[summerzb](https://clawhub.ai/user/summerzb)

### License/Terms of Use:

MIT-0

## Use Case:

Sales, business development, and market research users can use this skill to turn an ICP description into a sourced company list with fit rationale, signal notes, and priority tiers. It is especially focused on China-oriented company research using public or authorized business-information channels.

### Deployment Geography for Use:

China-focused; review before use in other jurisdictions.

## Known Risks and Mitigations:

Risk: Broad lead-research triggers could activate the skill for prospecting tasks that involve paid databases, exported account data, or contact-related fields.

Mitigation: Review activation before use and confirm that each source is public, officially authorized, or accessed through the user's own account with permission.

Risk: Some referenced company-information sources have login walls, CAPTCHA, or frequency limits.

Mitigation: Use official APIs or user-authorized channels, do not bypass access controls, and follow the skill's stated rate-limit guidance such as spacing requests by at least 10 seconds where applicable.

Risk: Company lists can contain stale, ambiguous, or unsupported entries, especially for duplicate company names.

Mitigation: Keep the source column for every included company, mark unsupported facts as not found, and disambiguate names using region, legal representative, or official domain before prioritizing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/summerzb/skills/icp-company-search)
- [Qichacha official MCP endpoint](https://mcp.qcc.com/basic/stream)
- [CNINFO announcement query endpoint](https://www.cninfo.com.cn/new/hisAnnouncement/query)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown or CSV-style company list table with source notes and follow-up recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes company name, priority tier, region, business summary, size, signal type and date, ICP fit rationale, source column, Top 3-5 outreach targets, and a search-path summary.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
