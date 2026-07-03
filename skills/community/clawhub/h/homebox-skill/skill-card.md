## Description: <br>
HomeBox Skill helps an agent manage a self-hosted HomeBox inventory through its REST API, including search, item details, add, update, delete, location, tag, and statistics workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ukeyboard](https://clawhub.ai/user/ukeyboard) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
HomeBox users and developers use this skill to let an agent search and maintain a personal or household inventory in a self-hosted HomeBox instance. It supports natural-language inventory lookup, item creation and edits, location/tag management, and API-version-aware CLI operations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires sensitive HomeBox credentials and can print login tokens. <br>
Mitigation: Install only when the publisher is trusted, use the least-privileged token available, and avoid exposing tokens in shared terminals, logs, or transcripts. <br>
Risk: Disabling TLS verification can expose HomeBox traffic on untrusted networks. <br>
Mitigation: Prefer a valid certificate; use NODE_TLS_REJECT_UNAUTHORIZED=0 only on a trusted local network and only for the commands that require it. <br>
Risk: The HomeBox API surface includes destructive or sensitive actions such as delete, export, group, notifier, account, and admin operations. <br>
Mitigation: Require explicit user confirmation before delete, bulk, account, group, notifier, export, or admin actions, and review the exact target IDs immediately before execution. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/ukeyboard/homebox-skill) <br>
- [Publisher profile](https://clawhub.ai/user/ukeyboard) <br>
- [HomeBox API Reference](references/api-reference.md) <br>
- [Old API Swagger Summary](references/old-api-swagger-summary.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, JSON] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON output from the HomeBox CLI.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js 18 or newer, HOMEBOX_BASE_URL, and a HomeBox bearer token for authenticated API operations.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
