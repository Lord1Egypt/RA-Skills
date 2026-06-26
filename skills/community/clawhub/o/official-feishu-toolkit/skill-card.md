## Description: <br>
Integrates with Feishu Open Platform APIs for calendar and meeting room booking, messaging, approvals, Bitable records, contacts, and attendance workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[radium0028](https://clawhub.ai/user/radium0028) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Employees and workplace automation users use this skill to let an agent perform Feishu office tasks such as scheduling meetings, sending messages, creating or processing approvals, updating Bitable records, looking up contacts, and checking attendance data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent live access to workplace messages, calendars, approvals, Bitable records, contacts, and attendance data. <br>
Mitigation: Use a dedicated low-privilege Feishu app and grant only the scopes needed for the specific deployment. <br>
Risk: State-changing actions may send messages, alter approvals, delete calendar events, or edit records. <br>
Mitigation: Require human confirmation before any action that changes Feishu data or communicates on behalf of a user or bot. <br>
Risk: The Feishu app secret can expose tenant access if it is shared or logged. <br>
Mitigation: Keep FEISHU_APP_SECRET out of chats, repositories, and logs; load it from a protected local environment or secret store. <br>
Risk: The artifact documents a remote `curl | sh` installer path. <br>
Mitigation: Prefer the `claw skill install` path and review the artifact before installation. <br>
Risk: Exposing the local API server beyond the local machine could broaden access to Feishu actions. <br>
Mitigation: Bind the service to localhost unless there is an explicit deployment review and access control plan. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/radium0028/official-feishu-toolkit) <br>
- [Feishu Open Platform](https://open.feishu.cn/) <br>
- [Feishu Developer Documentation](https://open.feishu.cn/document/) <br>
- [Feishu API Explorer](https://open.feishu.cn/api-explorer) <br>
- [Calendar and Meeting Rooms](references/calendar.md) <br>
- [Messaging](references/messaging.md) <br>
- [Approvals](references/approval.md) <br>
- [Bitable](references/bitable.md) <br>
- [Contacts](references/contacts.md) <br>
- [Attendance](references/attendance.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, API calls, JSON] <br>
**Output Format:** [Markdown guidance with shell commands and JSON API request or response payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires FEISHU_APP_ID and FEISHU_APP_SECRET; available actions depend on the configured Feishu app permissions.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata; artifact frontmatter lists 1.0.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
