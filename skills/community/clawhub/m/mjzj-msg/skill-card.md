## Description: <br>
卖家之家(跨境电商)私信查询和发送 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mjzj-tec](https://clawhub.ai/user/mjzj-tec) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and marketplace operators use this skill to query MJZJ private-message conversations, read message history with another user, and send private messages through the MJZJ API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access MJZJ private messages and send messages from the user's account. <br>
Mitigation: Install only when this access is intended, keep MJZJ_API_KEY in trusted environments, and verify recipients and message text before sending. <br>
Risk: A stale, exposed, or misplaced MJZJ_API_KEY could allow unintended account access. <br>
Mitigation: Rotate or revoke the API key when it is no longer needed and reconfigure the skill after token resets or authorization failures. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mjzj-tec/mjzj-msg) <br>
- [MJZJ homepage](https://mjzj.com) <br>
- [MJZJ API key page](https://mjzj.com/user/agentapikey) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and API request guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires MJZJ_API_KEY and returns or sends private-message data through approved MJZJ message endpoints.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
