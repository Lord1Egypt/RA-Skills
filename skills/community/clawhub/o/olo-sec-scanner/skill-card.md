## Description: <br>
SEC EDGAR filing analysis for M&A due diligence - extract financials, detect risks, and track corporate events from 10-K, 10-Q, and 8-K filings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aniebyl](https://clawhub.ai/user/aniebyl) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
M&A analysts, finance teams, and diligence reviewers use this skill to structure SEC EDGAR filing review, extract XBRL financial signals, identify risk-factor changes, and summarize material corporate events. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may make public SEC EDGAR requests for companies or filings the user asks about. <br>
Mitigation: Avoid using sensitive deal strategy, non-public target information, or confidential assumptions in prompts sent through public filing workflows. <br>
Risk: Financial and legal analysis can be incomplete or misleading if treated as definitive due-diligence advice. <br>
Mitigation: Use the output as due-diligence support and have qualified finance, legal, or compliance reviewers verify conclusions before business decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/aniebyl/olo-sec-scanner) <br>
- [Publisher profile](https://clawhub.ai/user/aniebyl) <br>
- [Author website](https://ololand.ai) <br>
- [SEC EDGAR Company Facts API](https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json) <br>
- [SEC EDGAR Submissions API](https://data.sec.gov/submissions/CIK{cik}.json) <br>
- [SEC EDGAR Full-Text Search](https://efts.sec.gov/LATEST/search-index?q=...) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown due-diligence analysis with financial summaries, risk flags, material events, ownership notes, and M&A-specific checks.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only output; no local access, credentials, persistence, or account-changing permissions are requested.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
