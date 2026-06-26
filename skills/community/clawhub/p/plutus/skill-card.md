## Description: <br>
Plutus parses receipts and expense descriptions from raw text or CSV transactions into categorized expense reports with totals, monthly trends, and budget comparisons. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[occupythemilkyway](https://clawhub.ai/user/occupythemilkyway) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, freelancers, and small business operators use this skill to turn expense text or CSV transaction exports into local budget and bookkeeping summaries. It helps compare spending against category budgets and identify large transactions without using a spreadsheet. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can save sensitive financial reports and summaries on local disk. <br>
Mitigation: Run it in a private directory you control, review generated Markdown and CSV files, and delete or redact reports that should not remain on disk. <br>
Risk: The install flow includes a pip dependency and the artifact describes an optional paid Pro purchase/install path. <br>
Mitigation: Install dependencies only in an environment you trust and review any optional Pro purchase or installation steps before using them. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/occupythemilkyway/plutus) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with shell and Python code blocks; local Markdown and CSV report files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses optional EXPENSES_FILE, EXPENSES_TEXT, BUDGET_JSON, CURRENCY, and REPORT_MONTH settings; generated reports are saved to local disk.] <br>

## Skill Version(s): <br>
1.0.4 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
