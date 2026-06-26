## Description: <br>
Gmail: Read a message and extract its body or headers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[googleworkspace-bot](https://clawhub.ai/user/googleworkspace-bot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and agents use this skill to read a specific Gmail message by ID and retrieve its body or selected headers through the local gws CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can expose Gmail message content from the account configured for the local gws CLI. <br>
Mitigation: Confirm the intended Gmail account, OAuth scopes, and message ID before reading messages, and avoid highly sensitive messages unless access is necessary. <br>
Risk: The skill depends on local gws CLI behavior and authentication state. <br>
Mitigation: Install and use this skill only in environments where the local gws CLI and Google Workspace authentication setup are trusted. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/googleworkspace-bot/gws-gmail-read) <br>
- [Publisher profile](https://clawhub.ai/user/googleworkspace-bot) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and text or JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the local gws CLI and an authenticated Google Workspace setup; message output may include Gmail content.] <br>

## Skill Version(s): <br>
1.0.12 (source: server release evidence; skill metadata version 0.22.5) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
