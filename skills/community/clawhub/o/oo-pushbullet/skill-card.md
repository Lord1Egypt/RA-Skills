## Description: <br>
Pushbullet (pushbullet.com). Use this skill for ANY Pushbullet request - reading, creating, updating, and deleting data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to operate Pushbullet through an OOMOL-connected account, including reading user profile, chat, device, and push data and creating, updating, or deleting Pushbullet resources. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: This skill requires sensitive Pushbullet credentials through an OOMOL-connected account. <br>
Mitigation: Install and use it only in a trusted ClawHub or development environment and rely on server-side credential injection rather than handling raw tokens. <br>
Risk: Write actions can create or update Pushbullet chats, devices, and pushes. <br>
Mitigation: Confirm the exact payload and expected effect with the user before running actions tagged as write operations. <br>
Risk: Destructive actions can delete pushes, chats, devices, or all pushes. <br>
Mitigation: Require explicit approval for the specific target before running any action tagged as destructive. <br>


## Reference(s): <br>
- [Pushbullet homepage](https://www.pushbullet.com) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [ClawHub skill page](https://clawhub.ai/oomol/oo-pushbullet) <br>
- [OOMOL publisher profile](https://clawhub.ai/user/oomol) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, guidance, text, JSON] <br>
**Output Format:** [Markdown with inline shell commands and JSON payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Responses from connector actions include data and execution metadata when run with JSON output.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
