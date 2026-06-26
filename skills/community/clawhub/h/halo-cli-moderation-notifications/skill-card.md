## Description: <br>
Use when moderating Halo comments or replies, creating official replies, listing unread notifications, deleting notifications, or marking notifications as read. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ruibaby](https://clawhub.ai/user/ruibaby) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and site operators use this skill to guide Halo CLI moderation workflows for comments, replies, official responses, and notification cleanup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Moderation commands can make irreversible or externally visible changes, including deletes, approvals, hidden replies, public replies, and mark-all notification actions. <br>
Mitigation: Before mutation, confirm the active Halo profile, site, exact resource ID, and reversibility, then require explicit approval for the action. <br>
Risk: Agent-generated moderation guidance may omit needed visibility context for public or hidden replies. <br>
Mitigation: Review the exact reply content and visibility setting before executing create-reply or approval commands. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/ruibaby/halo-cli-moderation-notifications) <br>
- [Publisher profile](https://clawhub.ai/user/ruibaby) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Halo CLI commands for moderation and notification operations.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
