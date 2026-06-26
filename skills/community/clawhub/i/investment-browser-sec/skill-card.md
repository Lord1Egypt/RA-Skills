## Description: <br>
Professional SEC EDGAR 10-Q/10-K parser for institutional investors that extracts financial metrics, MD&A risk factors, and exports CSV, HTML, PDF, and Markdown reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lettywyse](https://clawhub.ai/user/lettywyse) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External investors and analysts use this skill to direct an agent to retrieve recent SEC EDGAR filings for a ticker, extract core financial metrics and MD&A risks, and prepare analysis reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated report or spreadsheet links may expose financial analysis artifacts if shared unintentionally. <br>
Mitigation: Confirm whether PDF or Google Sheet exports should be created, and keep generated links private unless they are intentionally shared. <br>
Risk: Financial metrics and risk summaries may be incomplete or misleading if the wrong ticker, filing, or tables are selected. <br>
Mitigation: Confirm the ticker and source filing before running the skill, then review extracted metrics against the SEC filing before relying on the report. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lettywyse/investment-browser-sec) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files] <br>
**Output Format:** [Markdown analysis with tables and links to CSV, HTML, PDF, and Google Sheet outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Ticker-driven workflow; users should confirm the ticker, filing source, and sharing settings for generated report links.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
