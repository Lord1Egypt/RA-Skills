## Description: <br>
Free basic version that converts Notion-style task records into weekly report markdown. Reserves premium upgrade hooks for trend analysis and management summary automation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wingogx](https://clawhub.ai/user/wingogx) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users, developers, and operators use this skill to convert Notion-style task records into weekly report Markdown with basic progress statistics, highlights, and risks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The generated upgrade metadata can include a payment_url assembled from environment variables. <br>
Mitigation: Treat payment_url as informational and verify that it points to the expected SkillPay domain before opening or sharing it. <br>


## Reference(s): <br>
- [SkillPay API Contract](references/skillpay-api-contract.md) <br>
- [ClawHub skill page](https://clawhub.ai/wingogx/notion-db-weekly-report-generator) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, JSON, Guidance] <br>
**Output Format:** [JSON object containing report statistics, weekly report Markdown, and upgrade metadata.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Validates user_id, week_label, and a non-empty records array; premium tier currently returns upgrade-required metadata.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
