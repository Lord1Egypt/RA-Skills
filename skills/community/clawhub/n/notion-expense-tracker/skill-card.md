## Description: <br>
Log daily expenses to Notion from natural language input, parsing item, amount, category, payment method, and transaction date into a configured database. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[huang-zi-zheng](https://clawhub.ai/user/huang-zi-zheng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Individuals and operators use this skill to capture everyday expenses through chat-style entries and write structured records into their own Notion expense database. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Expense records and descriptions may contain sensitive personal or financial information stored in Notion. <br>
Mitigation: Use a dedicated Notion integration shared only with the intended expense database and avoid entering unnecessary sensitive details. <br>
Risk: A leaked Notion token or overly broad database sharing could expose or alter expense data. <br>
Mitigation: Keep the token private, scope database access narrowly, and rotate the token if it is exposed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/huang-zi-zheng/notion-expense-tracker) <br>
- [Publisher profile](https://clawhub.ai/user/huang-zi-zheng) <br>
- [Notion integration setup](https://www.notion.so/my-integrations) <br>
- [Expense tracker Notion template](https://huangzizheng.notion.site/33c25bdf2d8880728ec1e2856ff9aa65?v=33c25bdf2d88816c80d8000c605efe3b&source=copy_link) <br>


## Skill Output: <br>
**Output Type(s):** [text, api calls, configuration] <br>
**Output Format:** [Text status messages and structured Notion database entries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires NOTION_API_KEY and EXPENSE_DATABASE_ID environment variables and a Notion database with matching properties.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
