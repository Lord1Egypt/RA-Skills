## Description: <br>
Send WhatsApp messages to other people or search/sync WhatsApp history via the wacli CLI, not for normal user chats. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[danielsinewe](https://clawhub.ai/user/danielsinewe) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to have an agent operate the wacli CLI for explicit WhatsApp send requests, chat discovery, message search, synchronization, and history backfill. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent access to WhatsApp messaging and local message history through wacli. <br>
Mitigation: Install only in environments where that access is acceptable, review the upstream wacli project, and remove or protect ~/.wacli when stored access is no longer wanted. <br>
Risk: A message could be sent to the wrong recipient or with unintended content if the request is ambiguous. <br>
Mitigation: Require an explicit recipient and message text, ask a clarifying question when anything is unclear, and confirm the recipient and message before sending. <br>
Risk: The tool is not intended for routine chats with the user over WhatsApp. <br>
Mitigation: Use wacli only for explicit requests to contact another person or to sync or search WhatsApp history. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/danielsinewe/openclaw-wacli-playbook) <br>
- [wacli homepage](https://wacli.sh) <br>
- [wacli Go install module](https://github.com/steipete/wacli) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May use JSON output from wacli when parsing command results.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
