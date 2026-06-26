## Description: <br>
Access and search Apple Contacts on macOS using AppleScript. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[NeriRos](https://clawhub.ai/user/NeriRos) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
macOS users use this skill to let an agent look up names, phone numbers, email addresses, and detailed entries from their local Apple Contacts when they ask contact-related questions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can expose sensitive local address-book details in the agent session. <br>
Mitigation: Grant macOS Contacts permission only when this access is intended, and avoid broad list-all or full-detail queries unless sharing those contact details is acceptable. <br>
Risk: The reviewed package references an AppleScript file that was not included in the artifact. <br>
Mitigation: Confirm the referenced AppleScript exists in the installed skill and inspect it before running osascript commands. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/NeriRos/macos-contacts) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text contact search results and Markdown guidance with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill is macOS-only and depends on local Contacts permission.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
