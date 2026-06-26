## Description: <br>
Operate Twilio through an OOMOL-connected account for account lookup, message reads, usage reporting, and outbound SMS or MMS sending. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to let an agent operate their connected Twilio account through OOMOL, including reading account and message data, listing usage, and preparing confirmed outbound messages. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send outbound SMS or MMS messages through the connected Twilio account, which can contact unintended recipients or incur cost. <br>
Mitigation: Before running send_message or any other write action, verify the recipient, message body, account or project, full payload, and potential cost with the user. <br>
Risk: Broad Twilio invocation wording could be mistaken for permission to make changes. <br>
Mitigation: Treat broad Twilio requests as routing context only, and require explicit user confirmation before write or destructive actions. <br>


## Reference(s): <br>
- [Twilio homepage](https://www.twilio.com) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON connector payloads or responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires live schema inspection before connector actions; write actions require user confirmation.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
