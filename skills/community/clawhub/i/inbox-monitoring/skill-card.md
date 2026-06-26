## Description: <br>
Use this skill when the user wants to monitor Pulse inbox activity, check new conversations/messages, track pending requests, or run periodic inbox checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xisen-w](https://clawhub.ai/user/xisen-w) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Pulse users and agent operators use this skill to check conversations, pending network requests, and optional network context, then summarize new urgent items and suggested next actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a Pulse API key and reads inbox, pending request, and optional network-context data. <br>
Mitigation: Protect PULSE_API_KEY, use the narrowest inbox view and limit that meet the task, and avoid logging full message contents. <br>
Risk: Recurring inbox checks can broaden access or create unnecessary records of sensitive communication activity. <br>
Mitigation: Confirm before running broad or recurring checks and review any external cron script before scheduling it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xisen-w/inbox-monitoring) <br>
- [Publisher profile](https://clawhub.ai/user/xisen-w) <br>
- [Pulse API base URL](https://www.aicoo.io/api/v1) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash commands and structured activity summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports newMessages, newIncomingRequests, urgent items, and suggested next actions; returns a single no-activity line when nothing changed.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
