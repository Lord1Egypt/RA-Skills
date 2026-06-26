## Description: <br>
Google Chat: Send a message to a space. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[googleworkspace-bot](https://clawhub.ai/user/googleworkspace-bot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents use this skill to send a plain-text Google Chat message to a specified space through the user's configured gws CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can post messages to Google Chat spaces through the user's gws setup. <br>
Mitigation: Confirm the exact destination space and message text with the user before running any send command. <br>
Risk: The skill depends on the local gws CLI and generated shared instructions for authentication and global flags. <br>
Mitigation: Verify the installed gws CLI and gws-shared instructions are trusted before use. <br>


## Reference(s): <br>
- [Gws Chat Send on ClawHub](https://clawhub.ai/googleworkspace-bot/gws-chat-send) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the gws CLI and user confirmation before sending a message.] <br>

## Skill Version(s): <br>
1.0.12 (source: ClawHub release evidence); artifact metadata version 0.22.5 (source: SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
