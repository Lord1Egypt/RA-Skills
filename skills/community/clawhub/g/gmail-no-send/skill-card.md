## Description: <br>
Read-only Gmail CLI that cannot send email by design; it lets agents search and read mail, create or update drafts, and archive messages using user-provided Google OAuth credentials. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[meimakes](https://clawhub.ai/user/meimakes) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external users, developers, and agents use this skill to work with Gmail inbox content, prepare draft responses for human review, and archive messages while keeping send capability out of the provided CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill has no send command, but it can create drafts and archive messages with powerful Gmail OAuth access. <br>
Mitigation: Require human review before draft creation or archive actions, and install only when Gmail draft and message-modification access is acceptable. <br>
Risk: A saved local token can be reused outside the CLI if it is exposed. <br>
Mitigation: Protect the token file, revoke OAuth access when no longer needed, and avoid sharing the local configuration directory. <br>
Risk: Gmail compose scope is required for draft creation and technically permits sending outside this application. <br>
Mitigation: Rely on the no-send CLI only as an application-layer control, pin and review the installed version, and monitor the audit log. <br>


## Reference(s): <br>
- [Threat Model](references/threat-model.md) <br>
- [Project homepage](https://github.com/meimakes/gmail-no-send) <br>
- [ClawHub listing](https://clawhub.ai/meimakes/gmail-no-send) <br>
- [Publisher profile](https://clawhub.ai/user/meimakes) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands; CLI commands return JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Python 3.9+, user-provided Google Cloud OAuth credentials, and local token storage.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
