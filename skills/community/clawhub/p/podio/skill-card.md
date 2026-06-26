## Description: <br>
Podio API integration with managed OAuth for managing workspaces, apps, items, tasks, comments, and files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[byungkyu](https://clawhub.ai/user/byungkyu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to connect an agent to Podio through Maton-managed OAuth so it can read and manage organizations, workspaces, apps, items, tasks, comments, and files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create, update, or delete Podio data through the connected account. <br>
Mitigation: Confirm the exact target resource and intended effect before approving any write or delete operation. <br>
Risk: MATON_API_KEY and OAuth connection URLs grant access to sensitive account workflows. <br>
Mitigation: Treat API keys and connection URLs as secrets, avoid exposing them in shared outputs, and choose the intended Podio connection when more than one account is available. <br>


## Reference(s): <br>
- [ClawHub Podio Skill](https://clawhub.ai/byungkyu/podio) <br>
- [Maton](https://maton.ai) <br>
- [Podio API Documentation](https://developers.podio.com/doc) <br>
- [Podio API Authentication](https://developers.podio.com/authentication) <br>
- [Podio Items API](https://developers.podio.com/doc/items) <br>
- [Podio Tasks API](https://developers.podio.com/doc/tasks) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline code examples and API request guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires MATON_API_KEY and an active Podio OAuth connection through Maton.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
