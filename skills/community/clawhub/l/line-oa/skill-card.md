## Description: <br>
Operate LINE Official Account Manager (chat.line.biz) via browser automation to check LINE messages, reply to LINE customers, and manage the LINE OA chat interface. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[PicSeeInc](https://clawhub.ai/user/PicSeeInc) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Employees or support agents use this skill to operate a LINE Official Account through an isolated OpenClaw browser session, including checking unread customer chats, reading conversation history, replying to customers, and managing account chat notes or tags. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read customer chat content from a LINE Official Account. <br>
Mitigation: Install and use it only for accounts where the agent is authorized to view customer messages. <br>
Risk: The skill can send live replies and change notes or tags in the LINE OA chat interface. <br>
Mitigation: Supervise the agent and require confirmation before sending replies or making chat metadata changes. <br>
Risk: The skill can forward customer images outside LINE. <br>
Mitigation: Forward customer images only when there is a clear business need and the handling is allowed by the account's data policy. <br>
Risk: An active browser session can keep LINE OA access available after use. <br>
Mitigation: Log out or stop the OpenClaw browser service when the session should no longer be available. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/PicSeeInc/line-oa) <br>
- [LINE Official Account Manager](https://chat.line.biz/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline browser actions, shell commands, JavaScript snippets, and structured chat summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May return chat names, message previews, timestamps, unread status, recent message text, image presence, and setup configuration guidance.] <br>

## Skill Version(s): <br>
1.0.2 (source: ClawHub release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
