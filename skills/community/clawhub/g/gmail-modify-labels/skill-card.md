## Description: <br>
Atomic node skill to modify email labels in Gmail using the gog CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zvirb](https://clawhub.ai/user/zvirb) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to add or remove Gmail labels on a specific email message or thread through a local gog CLI setup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The local gog CLI may be configured for a different Gmail account than the user intends. <br>
Mitigation: Confirm the active Gmail account before running label changes. <br>
Risk: Label removals or broad commands can affect the wrong message, thread, or label set. <br>
Mitigation: Show the exact message or thread ID and the labels to add or remove before execution. <br>
Risk: The label modification command may fail or return an error. <br>
Mitigation: Retry up to three times with a short delay, then report the error and stop. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zvirb/gmail-modify-labels) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance, Text] <br>
**Output Format:** [Markdown guidance with inline shell commands and a JSON command example] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a local gog CLI configured for the intended Gmail account.] <br>

## Skill Version(s): <br>
1.0.3 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
