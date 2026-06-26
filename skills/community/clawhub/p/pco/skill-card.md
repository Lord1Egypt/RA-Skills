## Description: <br>
Provides command-line guidance for using a local Planning Center Services CLI to manage service plans, teams, songs, media, people, and related church planning data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rubyrunsstuff](https://clawhub.ai/user/rubyrunsstuff) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Church operations staff, developers, and automation agents use this skill to run Planning Center Services CLI commands for inspecting and managing service plans, scheduled people, songs, media, teams, and related resources. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill relies on an external local pco.ts CLI that was not included for review in the artifact. <br>
Mitigation: Install and use this skill only after reviewing and trusting the local pco.ts CLI it invokes. <br>
Risk: Raw POST, PATCH, and DELETE commands can modify or delete live Planning Center Services data. <br>
Mitigation: Use least-privilege Planning Center credentials and require explicit human confirmation before running mutating raw API commands. <br>
Risk: Planning Center credentials grant access to church planning data. <br>
Mitigation: Store credentials only in approved local configuration or secret storage, avoid exposing them in chats or logs, and revoke or rotate credentials when no longer needed. <br>


## Reference(s): <br>
- [PCO CLI - Planning Center Services on ClawHub](https://clawhub.ai/rubyrunsstuff/pco) <br>
- [Publisher profile](https://clawhub.ai/user/rubyrunsstuff) <br>
- [Planning Center Services API documentation](https://developer.planning.center/docs/#/apps/services) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown command reference with inline shell command examples and notes about JSON, table, and quiet CLI output modes.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires local access to the external pco.ts CLI and Planning Center credentials stored outside the skill.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
