## Description:

SEC EDGAR filing analysis for M&A due diligence — extract financials, detect risks, and track corporate events from 10-K, 10-Q, and 8-K filings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aniebyl](https://clawhub.ai/user/aniebyl)

### License/Terms of Use:

MIT

## Use Case:

M&A analysts, finance teams, and agents supporting acquisition diligence use this skill to structure SEC EDGAR filing review, extract financial indicators, identify disclosure risks, and summarize material corporate events.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Company identifiers or search terms may be sent to SEC public data endpoints during use.

Mitigation: Use public or approved company identifiers and avoid submitting confidential deal names, internal code names, or non-public diligence terms as SEC search queries.

Risk: Broad filing-related triggers may activate the skill in generic annual or quarterly report contexts.

Mitigation: Confirm that the task involves SEC EDGAR filing analysis for M&A or diligence before relying on the skill's workflow.

Risk: Filing summaries and risk scores can omit context or misstate diligence significance if source filings are incomplete or stale.

Mitigation: Review cited filings, dates, and extracted financial concepts before using the output in transaction decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aniebyl/skills/olo-sec-scanner)
- [SEC EDGAR Company Facts API](https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json)
- [SEC EDGAR Submissions API](https://data.sec.gov/submissions/CIK{cik}.json)
- [SEC EDGAR Full-Text Search](https://efts.sec.gov/LATEST/search-index?q=...)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown analysis report with structured financial summary, risk flags, material event timeline, and insider activity sections.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference public SEC EDGAR data sources and should include filing type, date range, and company identifier when available.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
