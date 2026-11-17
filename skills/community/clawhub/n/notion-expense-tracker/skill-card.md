## Description:

Log daily expenses to Notion using natural language input, auto-parsing item, amount, category, and payment method into a configured database.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huang-zi-zheng](https://clawhub.ai/user/huang-zi-zheng)

### License/Terms of Use:

MIT-0

## Use Case:

Users with a Notion expense database use this skill to capture daily spending from short natural-language messages and store normalized expense records for tracking, filtering, and summary review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Expense details are stored in Notion and may contain sensitive personal financial information.

Mitigation: Use a dedicated Notion integration token shared only with the intended expense database and review database permissions before use.

Risk: Misconfigured Notion credentials or database permissions can prevent expense logging or write to the wrong workspace.

Mitigation: Set NOTION_API_KEY and EXPENSE_DATABASE_ID deliberately, confirm the database is shared with the integration, and verify the required database properties before logging expenses.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/huang-zi-zheng/skills/notion-expense-tracker)
- [Publisher profile](https://clawhub.ai/user/huang-zi-zheng)
- [Notion integration setup](https://www.notion.so/my-integrations)
- [Expense tracker Notion template](https://huangzizheng.notion.site/33c25bdf2d8880728ec1e2856ff9aa65?v=33c25bdf2d88816c80d8000c605efe3b&source=copy_link)

## Skill Output:

**Output Type(s):** [Text, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with Python code behavior and shell environment variable setup]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes parsed expense records to a user-configured Notion database when supplied with valid Notion credentials.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
