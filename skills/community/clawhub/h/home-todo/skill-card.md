## Description: <br>
Checks a local home-todo file and reminds the user about unfinished household tasks whenever they send a Dashboard webchat message. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[CyberRaccoonX](https://clawhub.ai/user/CyberRaccoonX) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to maintain lightweight household reminders and have unfinished home tasks surfaced automatically in Dashboard conversations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent household reminders may expose sensitive personal or household details during Dashboard conversations. <br>
Mitigation: Avoid storing sensitive details in ~/.openclaw/workspace/.home-todos.md and periodically review or clear the file when persistent reminder memory is not desired. <br>


## Reference(s): <br>
- [Home Todo on ClawHub](https://clawhub.ai/CyberRaccoonX/home-todo) <br>
- [CyberRaccoonX publisher profile](https://clawhub.ai/user/CyberRaccoonX) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown reminder text appended to agent responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May also guide updates to the local ~/.openclaw/workspace/.home-todos.md todo file.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
