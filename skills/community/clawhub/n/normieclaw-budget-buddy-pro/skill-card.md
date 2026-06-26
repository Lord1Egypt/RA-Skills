## Description: <br>
Budget Buddy Pro turns an AI agent into a local personal finance coach that parses bank and credit card statements, categorizes transactions, builds budgets, tracks bills, savings goals, and net worth, and generates spending summaries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nollio](https://clawhub.ai/user/nollio) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users use this skill to manage personal finances locally with an agent: importing statements, reviewing spending, creating budgets, tracking recurring bills, setting savings goals, and generating financial summaries. It is an organization and tracking aid, not a licensed financial advisor. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles sensitive bank, credit card, income, bill, and net worth data in local files. <br>
Mitigation: Install and run it only in a trusted local workspace, keep restrictive file permissions, and use disk encryption where appropriate. <br>
Risk: Merchant names, transaction descriptions, and exchange-rate lookups could disclose financial details if web search is used. <br>
Mitigation: Disable or avoid web_search for transaction-derived lookups unless the user explicitly approves each lookup. <br>
Risk: Raw statements and generated financial records may persist after setup or import. <br>
Mitigation: Back up existing budget data before setup and delete raw statements from the skill data directory when they are no longer needed. <br>
Risk: Budget summaries and insights may be mistaken for investment, tax, legal, or professional financial advice. <br>
Mitigation: Treat outputs as informational organization and tracking assistance, and consult a licensed professional for personalized advice. <br>


## Reference(s): <br>
- [Budget Buddy Pro on ClawHub](https://clawhub.ai/nollio/normieclaw-budget-buddy-pro) <br>
- [README](artifact/README.md) <br>
- [Security Audit](artifact/SECURITY.md) <br>
- [Setup Prompt](artifact/SETUP-PROMPT.md) <br>
- [Dashboard Companion Kit Spec](artifact/dashboard-kit/DASHBOARD-SPEC.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON data files and optional shell, Python, PNG, or PDF report outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill may write local budget, transaction, rule, recurring bill, savings goal, and net worth files under its data directory.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
