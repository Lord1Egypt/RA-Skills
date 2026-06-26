## Description: <br>
Patent marketplace via trade.9235.net (listings, deals, open license, procurement, Excel export). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[windinwing](https://clawhub.ai/user/windinwing) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to search patent marketplace listings, inspect sellers and deal history, find open licenses and procurement demand, and export patent transaction results for diligence workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Patent transaction searches and diligence activity are sent to trade.9235.net. <br>
Mitigation: Install only when the organization approves sharing this activity with the external marketplace service. <br>
Risk: TRADE_API_TOKEN is a sensitive credential and this client places it in request URLs for the default skill endpoint. <br>
Mitigation: Protect and rotate the token, avoid logging request URLs, and limit token scope where the service supports it. <br>
Risk: Excel export can install openpyxl at runtime and creates files containing patent transaction data. <br>
Mitigation: Preinstall or review the export dependency path before deployment, and treat generated Excel or CSV files as business-confidential. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/windinwing/patent-transaction) <br>
- [Patent marketplace homepage](https://trade.9235.net) <br>
- [Trade Skill API endpoint](https://trade.9235.net/api/skill) <br>
- [Due diligence workflow](due-diligence.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, API calls, Files, Shell commands, Configuration] <br>
**Output Format:** [Markdown tables and status messages, JSON-compatible result objects, and Excel or CSV export files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Exports may create outbound file assets; API access requires TRADE_API_TOKEN for the default skill endpoint.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
