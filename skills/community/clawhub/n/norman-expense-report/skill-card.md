## Description: <br>
Generate a detailed expense breakdown by category for a given period. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[stanlee000](https://clawhub.ai/user/stanlee000) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Employees and finance operators use this skill to generate readable expense reports for a requested period, including category totals, top vendors, trends, and comparisons with previous periods when data is available. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may expose transaction history, vendors, amounts, categories, and balance context to the agent through the Norman finance MCP connection. <br>
Mitigation: Install and run it only with a trusted Norman finance MCP connection and limit requests to reporting periods the user intends to analyze. <br>
Risk: Expense reports can be misleading if the requested period, transaction filters, or prior-period data are incomplete. <br>
Mitigation: Review the requested period and report assumptions before using the results for business decisions, and drill down into categories when figures look unusual. <br>


## Reference(s): <br>
- [Norman Finance](https://norman.finance) <br>
- [ClawHub skill page](https://clawhub.ai/stanlee000/norman-expense-report) <br>
- [Publisher profile](https://clawhub.ai/user/stanlee000) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown expense report with category, vendor, trend, and comparison sections] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Amounts are presented in EUR; reports may offer follow-up drill-down by category.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
