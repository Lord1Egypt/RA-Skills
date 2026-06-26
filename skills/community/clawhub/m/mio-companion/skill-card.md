## Description: <br>
Mio Companion learns local conversation habits, tracks todos and schedules, and returns proactive chat or task-management responses. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[libaiqwq](https://clawhub.ai/user/libaiqwq) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this companion to keep local memory of recent conversation context, infer habits, surface todos, and decide when to prompt proactive chats or task execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores chat-derived context, inferred habits, todos, schedules, and recent logs in local workspace files. <br>
Mitigation: Avoid sharing secrets with the skill, periodically review or delete the mio-companion-data directory, and limit use to trusted workspaces. <br>
Risk: Scheduled proactive checks can initiate chats or surface tasks when the user expected manual-only behavior. <br>
Mitigation: Disable cron/proactive triggers when only manual chat is desired and review generated todo or task actions before acting on them. <br>


## Reference(s): <br>
- [Mio Companion on ClawHub](https://clawhub.ai/libaiqwq/mio-companion) <br>
- [Publisher profile](https://clawhub.ai/user/libaiqwq) <br>


## Skill Output: <br>
**Output Type(s):** [text, configuration, guidance] <br>
**Output Format:** [JSON-like JavaScript objects with action, message, and data fields] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local habits, todos, schedule, and log JSON files under mio-companion-data.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and config.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
