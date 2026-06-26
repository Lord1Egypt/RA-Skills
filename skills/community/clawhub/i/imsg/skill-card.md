## Description: <br>
iMessage/SMS CLI for listing chats, history, watch, and sending. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[steipete](https://clawhub.ai/user/steipete) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators on macOS use this skill to inspect Messages.app chats, retrieve message history, watch conversations, and prepare iMessage or SMS send commands through the imsg CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires terminal access to Messages data through macOS permissions. <br>
Mitigation: Grant Full Disk Access only after reviewing the prompt and confirming the terminal session is trusted. <br>
Risk: Sending commands can deliver iMessage or SMS content to unintended recipients. <br>
Mitigation: Confirm the recipient, service selection, message text, and attachments before executing any send command. <br>
Risk: Conversation history or attachments may expose sensitive local communications. <br>
Mitigation: Limit history and watch commands to the specific chat needed, and avoid sharing command output that contains private message content. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/steipete/imsg) <br>
- [Publisher profile](https://clawhub.ai/user/steipete) <br>
- [imsg homepage](https://imsg.to) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [macOS-only; expects the imsg binary, Messages.app sign-in, Full Disk Access, and Automation permission for sending.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
