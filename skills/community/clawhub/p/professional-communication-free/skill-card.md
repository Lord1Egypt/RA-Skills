## Description: <br>
Helps technical teams draft clear status update emails, escalation requests, and Slack/Teams messages that put key information first, stay scannable, and make action requests explicit. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, developers, and technical teams use this skill to turn workplace context into concise status updates, escalation messages, and chat drafts with clear next actions. It is intended for routine professional communication, not legal, compliance, HR, performance, or conflict-sensitive formal notices. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requests command execution and write capability even though its stated purpose is workplace communication drafting. <br>
Mitigation: Review before installing and prefer a version that removes exec, explains any write access, and limits permissions to the drafting workflow. <br>
Risk: Generated workplace messages may omit context or create misleading action requests when the user provides incomplete details. <br>
Mitigation: Review drafts before sending and confirm placeholders, recipients, deadlines, and requested actions against the actual business context. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/professional-communication-free) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/thcjp) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown or plain text message drafts with concise bullets and action-request structure] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include bracketed placeholders when the user has not supplied required business context.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
