## Description: <br>
Analyzes financial statements for earnings manipulation and accounting fraud risk using Beneish M-Score, Dechow F-Score, cash-flow checks, red flags, and structured evidence. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hollis9087](https://clawhub.ai/user/hollis9087) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Analysts, finance teams, and agents use this skill to screen company filings or structured financial data for accounting-risk signals. It supports single-company review and batch-style screening, with conclusions framed as risk levels rather than determinations of fraud. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Financial fraud analysis may be mistaken for a definitive finding of misconduct. <br>
Mitigation: Treat outputs as risk-screening signals, verify source data, and require qualified human review before making legal, investment, or enforcement decisions. <br>
Risk: Some documented batch and reference workflows are missing or incomplete. <br>
Mitigation: Review or supply the missing fetch and benchmark scripts, and confirm any network fetching before running batch analysis. <br>
Risk: Results depend on complete, consistently prepared financial statements. <br>
Mitigation: Align reporting periods and accounting bases before calculation, and mark missing or uncertain inputs as unable to judge. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hollis9087/holli-financial-fraud-analyzer) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown analysis with tables, risk ratings, evidence summaries, and optional JSON or terminal output from scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes metric tables, Beneish and Dechow calculations, red flags, limitations, and recommended follow-up checks.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
