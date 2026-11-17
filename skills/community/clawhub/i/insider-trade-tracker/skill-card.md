## Description:

Track and interpret SEC Form 4 insider buying and selling activity across US-listed equities using the Finskills API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[finskills](https://clawhub.ai/user/finskills)

### License/Terms of Use:

MIT-0

## Use Case:

Investors, analysts, and financial research agents use this skill to retrieve SEC-reported insider transactions, filter open-market purchases and sales, detect cluster signals, and summarize insider sentiment for US-listed equities.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Requested symbols, CIKs, and watchlist contents are sent to the Finskills API.

Mitigation: Avoid submitting confidential trading plans or nonpublic investment research unless external API use is acceptable.

Risk: Insider transaction signals can be delayed, ambiguous, or incomplete as standalone investment evidence.

Mitigation: Treat the report as financial research context, verify filings and timing, and compare against fundamentals, valuation, and other public information.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/finskills/skills/insider-trade-tracker)
- [Finskills API](https://finskills.net)
- [Finskills API Key Registration](https://finskills.net/register)
- [Project Homepage](https://github.com/finskills/insider-trade-tracker)

## Skill Output:

**Output Type(s):** [Text, Markdown, API calls, Guidance]

**Output Format:** [Markdown report with transaction tables, signal analysis, caveats, and an overall verdict]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires FINSKILLS_API_KEY and sends requested symbols, CIKs, or watchlist contents to the Finskills API.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata; artifact frontmatter reports 1.0.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
