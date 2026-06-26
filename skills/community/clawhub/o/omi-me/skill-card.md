## Description: <br>
Complete Omi.me integration for memories, action items (tasks), and conversations with CRUD and sync capabilities for OpenClaw. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[CaioIsCoding](https://clawhub.ai/user/CaioIsCoding) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to configure an Omi.me API token and manage memories, action items, conversations, and sync flows from the command line. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Credential handling could expose an Omi API token. <br>
Mitigation: Do not use a real Omi API token until the API_URL versus OMI_API_URL bug is fixed; use a limited or disposable token for testing and set chmod 600 on ~/.config/omi-me/token. <br>
Risk: Endpoint scoping flaws could route requests incorrectly when API_URL or OMI_API_URL is set unexpectedly. <br>
Mitigation: Clear any API_URL environment variable before testing and verify the endpoint behavior before using the skill with live data. <br>
Risk: Update and delete commands operate on live Omi.me memories, tasks, and conversations. <br>
Mitigation: Review command arguments carefully and test against disposable data before running delete, update, or sync operations on an active account. <br>
Risk: Token printing can leak credentials in logs or shared terminals. <br>
Mitigation: Avoid omi-token.sh get in logged, recorded, or shared terminal sessions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/CaioIsCoding/omi-me) <br>
- [Publisher profile](https://clawhub.ai/user/CaioIsCoding) <br>
- [Omi.me](https://omi.me) <br>
- [Omi developer API overview](https://docs.omi.me/doc/developer/api/overview) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Bash commands and JSON or text CLI output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires omi, omi-token, and OMI_API_TOKEN; commands may read, create, update, delete, or sync live Omi.me account data.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
