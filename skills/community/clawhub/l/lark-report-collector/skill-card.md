## Description: <br>
Collects weekly reports from Lark Reports, summarizes them into Lark Docs, and supports notifications. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Pengxiao-Wang](https://clawhub.ai/user/Pengxiao-Wang) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Employees and operations teams use this skill to collect weekly Lark report submissions for selected teams or templates, identify missing submissions, create summary documents, and send follow-up notifications. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can operate through a logged-in Lark session and access employee report data. <br>
Mitigation: Before use, specify the exact Lark account, team or template, reporting week, output document location, and whether local report files may be created. <br>
Risk: Generated summaries or notification recipients may be incorrect or broader than intended. <br>
Mitigation: Review the generated summary, document link, and recipient list before any notification is sent. <br>
Risk: Temporary extraction files may contain sensitive report data. <br>
Mitigation: Delete or protect any temporary extraction files after the collection workflow is complete. <br>


## Reference(s): <br>
- [Lark Reports entry page](https://oa.larksuite.com/report/record/entry) <br>
- [ClawHub skill page](https://clawhub.ai/Pengxiao-Wang/lark-report-collector) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, API calls, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with browser automation steps, JavaScript snippets, API usage notes, and generated document or notification content.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an active Lark browser session and user review before sending notifications.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
