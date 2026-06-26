## Description: <br>
Microsoft Outlook API integration with managed OAuth for reading, sending, and managing emails, folders, calendar events, and contacts via Microsoft Graph. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[byungkyu](https://clawhub.ai/user/byungkyu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to connect an authorized Outlook account through Maton and perform mailbox, calendar, folder, and contact operations through CLI, Python, JavaScript, or HTTP API examples. Write actions should be confirmed before execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read and change mailbox, calendar, and contact data through the connected Outlook account. <br>
Mitigation: Use the intended Microsoft account and confirm every send, create, update, or delete action before it runs. <br>
Risk: The Maton API key grants access to brokered Outlook operations. <br>
Mitigation: Keep MATON_API_KEY out of shared logs, screenshots, and pasted command output, and rotate or revoke it if exposed. <br>
Risk: Unused OAuth connections may retain access longer than needed. <br>
Mitigation: Periodically remove unused Outlook OAuth connections. <br>


## Reference(s): <br>
- [ClawHub Outlook skill page](https://clawhub.ai/byungkyu/outlook-api) <br>
- [Microsoft Graph API overview](https://learn.microsoft.com/en-us/graph/api/overview) <br>
- [Microsoft Graph Mail API](https://learn.microsoft.com/en-us/graph/api/resources/mail-api-overview) <br>
- [Microsoft Graph Calendar API](https://learn.microsoft.com/en-us/graph/api/resources/calendar) <br>
- [Microsoft Graph Contacts API](https://learn.microsoft.com/en-us/graph/api/resources/contact) <br>
- [Microsoft Graph query parameters](https://learn.microsoft.com/en-us/graph/query-parameters) <br>
- [Maton CLI Manual](https://cli.maton.ai/manual) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Code, Configuration, API calls] <br>
**Output Format:** [Markdown with CLI, HTTP, Python, and JavaScript examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires network access, MATON_API_KEY, and an authorized Outlook OAuth connection.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release metadata; artifact frontmatter reports 1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
