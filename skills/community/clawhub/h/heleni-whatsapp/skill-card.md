## Description: <br>
Helps OpenClaw agents manage WhatsApp conversation memory, track unanswered messages, prevent reply loops, and coordinate multiple personal assistants. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[netanel-abergel](https://clawhub.ai/user/netanel-abergel) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators of OpenClaw agents use this skill to manage WhatsApp DMs and groups with local conversation memory, unanswered-message tracking, and reply safety rules. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide automatic WhatsApp replies and reactions. <br>
Mitigation: Require explicit operating rules for which chats may be answered automatically and when human approval is required before sending. <br>
Risk: The skill can persist private WhatsApp conversation data in cleartext local files. <br>
Mitigation: Define which chats may be logged, retention duration, and who can read the memory and inbox files before deployment. <br>
Risk: The troubleshooting guidance includes gateway restarts, log review, and API-key checks. <br>
Mitigation: Require explicit approval before running administrative commands or inspecting logs and credentials. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/netanel-abergel/heleni-whatsapp) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell and Python snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide local file writes for WhatsApp memory and unanswered-message tracking.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
