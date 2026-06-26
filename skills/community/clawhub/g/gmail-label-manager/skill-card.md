## Description: <br>
Automates unread Gmail organization by applying labels, removing irrelevant labels, and archiving messages based on patterns from archived emails. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Coenenp](https://clawhub.ai/user/Coenenp) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and Gmail power users can use this skill to run a local Gmail automation script that classifies unread messages, adjusts labels, archives matching mail, and optionally emits notifications or calendar events. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can change mailbox state by applying or removing labels and archiving Gmail messages. <br>
Mitigation: Test on a limited set of messages first, confirm the gog OAuth scopes, and keep a rollback plan for archived or mislabeled messages. <br>
Risk: If configured, the script can forward sensitive email details to Telegram and create calendar events without those behaviors being clearly disclosed in the skill instructions. <br>
Mitigation: Disable or tightly restrict Telegram forwarding and calendar creation unless those data flows are explicitly intended and reviewed. <br>
Risk: Calendar command construction may allow crafted email content to affect shell execution. <br>
Mitigation: Fix the calendar command construction before use and avoid running the script on untrusted inbox content until that issue is resolved. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Coenenp/gmail-label-manager) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown instructions and bash script behavior] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs locally with gog, jq, curl, Gmail access, and optional Telegram credentials.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
